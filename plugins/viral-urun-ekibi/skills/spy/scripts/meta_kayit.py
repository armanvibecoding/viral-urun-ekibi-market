#!/usr/bin/env python3
"""Meta Reklam Kütüphanesi ham dökümünü kayda çevirir.

  python3 meta_kayit.py kaydet --kok is/meta is/meta/ham/<dosya>.txt [parça2.txt ...]
  python3 meta_kayit.py alan   --kok is/meta --ulke TR --alan ornek.com --sonuc 180
  python3 meta_kayit.py denetle --kok is/meta        (= kayit_denetle.py)

Ham biçim (meta_aktar.js üretir; get_page_text ya da indirme ile alınır), her parça:
  #REKLAMAVI v1<TAB>ulke=TR<TAB>sorgu=...<TAB>nis=...<TAB>aile=S<TAB>siralama=yeni<TAB>baslangic=2026-11-07T10:00<TAB>kart=N<TAB>parca=1/2
  kod<TAB>sayfa<TAB>tarih_metni<TAB>kopya_metni<TAB>kart_tam(1/0)<TAB>link<TAB>cta<TAB>medya<TAB>govde
Kapılar:
  - Biçim/şema bozuk, parça eksik, kart sayısı başlıkla tutmuyor → çıkış 1
  - aramalar.tsv'de bugünün bu sorgusu yok (kota dışı tarama) → çıkış 1
  - 0 kart: sonrasında kontrol sorgusu kaydı yok → çıkış 2 (kontrolü aç, kaydet, tekrar çalıştır)
            kontrol de 0 → çıkış 3 "SINIRLAMA — bugün dur"; kontrol dolu → GERCEK-SIFIR, çıkış 0
"""
import argparse
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402
import kazanan_puan as kp  # noqa: E402
import nis_kelime as nk  # noqa: E402

KART_ALAN = ["kod", "sayfa", "tarih_metni", "kopya_metni", "kart_tam", "link", "cta", "medya", "govde"]
META_ALAN = ["ulke", "sorgu", "nis", "aile", "siralama", "baslangic", "kart", "parca"]


# ------------------------------------------------------------------ ham okuma + şema
def ham_oku(yollar):
    parcalar = {}
    meta0 = None
    for yol in yollar:
        if not os.path.exists(yol):
            raise o.VeriHatasi("ham dosya yok: %s" % yol)
        with open(yol, encoding="utf-8") as f:
            satirlar = [s.rstrip("\r") for s in f.read().split("\n")]
        guncel = None
        for no, s in enumerate(satirlar, start=1):
            if not s.strip():
                continue
            if s.startswith("#REKLAMAVI"):
                meta = baslik_coz(s, yol, no)
                anahtar = {k: v for k, v in meta.items() if k != "parca"}
                if meta0 is None:
                    meta0 = anahtar
                elif anahtar != meta0:
                    raise o.VeriHatasi("%s:%d parça başlığı ilk parçayla aynı sorguya ait değil" % (yol, no))
                i, n = meta["parca"]
                if i in parcalar:
                    raise o.VeriHatasi("%s:%d parça %d iki kez verilmiş" % (yol, no, i))
                parcalar[i] = {"n": n, "kartlar": []}
                guncel = parcalar[i]
                continue
            if guncel is None:
                raise o.VeriHatasi("%s:%d başlıksız satır (#REKLAMAVI v1 ile başlamalı)" % (yol, no))
            h = s.split("\t")
            if len(h) != len(KART_ALAN):
                raise o.VeriHatasi("%s:%d kart satırında %d alan var, %d bekleniyor" % (yol, no, len(h), len(KART_ALAN)))
            k = dict(zip(KART_ALAN, [x.strip() for x in h]))
            if not o.sayi_mi(k["kod"]):
                raise o.VeriHatasi("%s:%d Kütüphane Kodu sayı değil: %r" % (yol, no, k["kod"]))
            if k["kart_tam"] not in ("0", "1"):
                raise o.VeriHatasi("%s:%d kart_tam 0/1 olmalı: %r" % (yol, no, k["kart_tam"]))
            guncel["kartlar"].append(k)
    if meta0 is None:
        raise o.VeriHatasi("hiç #REKLAMAVI başlığı yok — dosya meta_aktar.js çıktısı değil")
    n = list(parcalar.values())[0]["n"]
    if sorted(parcalar) != list(range(1, n + 1)):
        raise o.VeriHatasi("parça eksik/fazla: elde %s, beklenen 1..%d" % (sorted(parcalar), n))
    kartlar = [k for i in sorted(parcalar) for k in parcalar[i]["kartlar"]]
    if len(kartlar) != meta0["kart"]:
        raise o.VeriHatasi("başlık kart=%d ama %d kart satırı okundu (kopyalama eksik/fazla)" % (meta0["kart"], len(kartlar)))
    return meta0, kartlar


def baslik_coz(s, yol, no):
    h = s.split("\t")
    if h[0].strip() != "#REKLAMAVI v1":
        raise o.VeriHatasi("%s:%d sürüm 'v1' değil" % (yol, no))
    m = {}
    for p in h[1:]:
        if "=" not in p:
            raise o.VeriHatasi("%s:%d başlık alanı anahtar=değer değil: %r" % (yol, no, p))
        k, v = p.split("=", 1)
        m[k.strip()] = v.strip()
    eksik = [k for k in META_ALAN if k not in m]
    if eksik:
        raise o.VeriHatasi("%s:%d başlıkta eksik: %s" % (yol, no, ",".join(eksik)))
    if m["ulke"] not in o.ULKELER:
        raise o.VeriHatasi("%s:%d ülke %r geçersiz (%s)" % (yol, no, m["ulke"], ",".join(o.ULKELER)))
    if m["aile"] not in o.SORGU_AILELERI:
        raise o.VeriHatasi("%s:%d aile %r geçersiz (U/S/K)" % (yol, no, m["aile"]))
    if m["siralama"] not in o.SIRALAMALAR:
        raise o.VeriHatasi("%s:%d sıralama %r geçersiz (%s)" % (yol, no, m["siralama"], ",".join(o.SIRALAMALAR)))
    if not o.iso_mu(m["baslangic"][:10]):
        raise o.VeriHatasi("%s:%d baslangic ISO tarih değil: %r" % (yol, no, m["baslangic"]))
    if not o.sayi_mi(m["kart"]):
        raise o.VeriHatasi("%s:%d kart sayı değil" % (yol, no))
    pm = re.fullmatch(r"(\d+)/(\d+)", m["parca"])
    if not pm or not (1 <= int(pm.group(1)) <= int(pm.group(2))):
        raise o.VeriHatasi("%s:%d parca 'i/N' biçiminde değil: %r" % (yol, no, m["parca"]))
    m["kart"] = int(m["kart"])
    m["parca"] = (int(pm.group(1)), int(pm.group(2)))
    if not m["sorgu"]:
        raise o.VeriHatasi("%s:%d sorgu boş" % (yol, no))
    return m


# ------------------------------------------------------------------ dönüşüm
def kart_satiri(k, meta, okuma, nis_sozluk):
    ilk = o.tarih_coz(k["tarih_metni"]) if k["kart_tam"] == "1" else None
    if k["kart_tam"] != "1":
        kopya = o.GORUNMUYOR                      # kart yapısı okunamadı: kopya da bilinmez
    else:
        n = o.kopya_coz(k["kopya_metni"])
        kopya = str(n) if n else ("1" if not k["kopya_metni"] else o.GORUNMUYOR)
    alan, yol = o.link_coz(k["link"])
    nis = meta["nis"] if meta["aile"] in ("U", "K") and meta["nis"] not in ("", "-") else \
        nk.nis_bul(nis_sozluk, meta["ulke"], k["govde"] + " " + yol)
    return {
        "kutuphane_kodu": k["kod"], "okuma_tarihi": okuma, "ulke": meta["ulke"], "nis": nis,
        "sorgu": meta["sorgu"], "aile": meta["aile"], "siralama": meta["siralama"],
        "sayfa_adi": k["sayfa"] or o.GORUNMUYOR,
        "ilk_yayin": ilk or o.GORUNMUYOR,
        "aktif_gun": str(o.gun_farki(okuma, ilk)) if ilk else o.GORUNMUYOR,
        "kopya": kopya,
        "govde_ilk200": (k["govde"] or o.GORUNMUYOR)[:200],
        "cta": k["cta"] or o.GORUNMUYOR,
        "hedef_alan": alan, "hedef_yol": yol, "tip": o.tip_bul(alan, yol),
        "medya": k["medya"] or o.GORUNMUYOR, "izlendi": "H", "not_no": "", "etiket": "",
    }


def birimleri_kur(kok, reklamlar):
    alan_olcek = {}
    for a in o.oku(kok, "alan"):
        alan_olcek[(a["ulke"], a["alan"])] = a["sonuc"]           # son yazılan kazanır
    gruplar = collections.OrderedDict()
    for r in reklamlar:
        gruplar.setdefault((r["ulke"], kp.birim_anahtari(r)), []).append(r)
    birimler = []
    for (ulke, birim), rs in gruplar.items():
        son = max(r["okuma_tarihi"] for r in rs)
        rs = [r for r in rs if o.gun_farki(son, r["okuma_tarihi"]) < o.ESIK["pencere_gun"]]
        tarihler = sorted(r["ilk_yayin"] for r in rs if o.iso_mu(r["ilk_yayin"]))
        gunler = [int(r["aktif_gun"]) for r in rs if o.sayi_mi(r["aktif_gun"])]
        yollar = []
        for r in rs:
            u = o.urun_yolu(r["hedef_yol"])
            if u and u not in yollar:
                yollar.append(u)
        nisler = [r["nis"] for r in rs if r["nis"] not in ("", "belirsiz")]
        birimler.append({
            "ulke": ulke, "birim": birim,
            "sayfa_adi": collections.Counter(r["sayfa_adi"] for r in rs).most_common(1)[0][0],
            "tip": collections.Counter(r["tip"] for r in rs).most_common(1)[0][0],
            "nis": collections.Counter(nisler).most_common(1)[0][0] if nisler else "belirsiz",
            "reklam_sayisi": str(len(rs)),
            "kopya_toplami": str(sum(int(r["kopya"]) for r in rs if o.sayi_mi(r["kopya"]))),
            "ilk_baslangic": tarihler[0] if tarihler else o.GORUNMUYOR,
            "son_baslangic": tarihler[-1] if tarihler else o.GORUNMUYOR,
            "max_aktif_gun": str(max(gunler)) if gunler else o.GORUNMUYOR,
            "kazanan_kreatif": "0",
            "alan_sorgu": alan_olcek.get((ulke, birim), ""),
            "son_okuma": son, "urun_yollari": ",".join(yollar)[:300], "etiket": "",
        })
    return birimler


def tum_kaydi_yenile(kok, reklamlar, dokunulan=()):
    o.yaz(kok, "reklam", reklamlar)
    birimler = birimleri_kur(kok, reklamlar)
    o.yaz(kok, "birim", birimler)
    if dokunulan:
        gecmis = o.oku(kok, "gecmis")
        anahtar = {(g["tarih"], g["ulke"], g["birim"]) for g in gecmis}
        for b in birimler:
            if (b["ulke"], b["birim"]) in dokunulan:
                s = {"tarih": b["son_okuma"], "ulke": b["ulke"], "birim": b["birim"],
                     "reklam_sayisi": b["reklam_sayisi"], "kopya_toplami": b["kopya_toplami"]}
                if (s["tarih"], s["ulke"], s["birim"]) in anahtar:
                    gecmis = [g for g in gecmis if (g["tarih"], g["ulke"], g["birim"]) != (s["tarih"], s["ulke"], s["birim"])]
                gecmis.append(s)
        o.yaz(kok, "gecmis", gecmis)
    r, b = kp.hesapla(kok)
    o.yaz(kok, "reklam", r)
    o.yaz(kok, "birim", b)
    return r, b


# ------------------------------------------------------------------ komutlar
def kaydet(kok, yollar, nisler_yolu):
    meta, kartlar = ham_oku(yollar)
    okuma = meta["baslangic"][:10]
    aramalar = o.oku(kok, "arama")
    idx = [i for i, a in enumerate(aramalar) if a["tarih"] == okuma and a["ulke"] == meta["ulke"]
           and a["sorgu"] == meta["sorgu"] and a["aile"] == meta["aile"]]
    if not idx:
        raise o.VeriHatasi("aramalar.tsv'de %s / %s / %r kaydı yok — sorgu `nis_kelime.py kaydet` ile kotaya "
                           "yazılmadan taranmış (kota dışı tarama kabul edilmez)" % (okuma, meta["ulke"], meta["sorgu"]))
    i = idx[-1]
    ham_ad = os.path.basename(yollar[0])
    if not kartlar:
        kontroller = [a for a in aramalar[i + 1:] if a["aile"] == "KONTROL" and a["tarih"] == okuma and o.sayi_mi(a["kart"])]
        if not kontroller:
            print("0 KART: şimdi kontrol sorgusunu yeniden aç, `nis_kelime.py kaydet --aile KONTROL ...` ve "
                  "`nis_kelime.py sonuc ...` ile yaz, sonra bu komutu tekrar çalıştır.")
            sys.exit(2)
        if int(kontroller[-1]["kart"]) == 0:
            aramalar[i].update(kart="0", durum="SINIRLAMA", ham_dosya=ham_ad)
            o.yaz(kok, "arama", aramalar)
            print("SINIRLAMA — bugün dur. Sorgu 0 kart ve kontrol sorgusu da 0 kart: Meta sessizce kısıtlıyor. "
                  "Bugün Meta'ya dokunma; sonuç 'doğrulanamadı'.")
            sys.exit(3)
        aramalar[i].update(kart="0", durum="GERCEK-SIFIR", ham_dosya=ham_ad)
        o.yaz(kok, "arama", aramalar)
        print("GERCEK-SIFIR: kontrol dolu (%s kart), bu sorgunun gerçekten sonucu yok — kaydedildi." % kontroller[-1]["kart"])
        return
    sozluk = nk.nisler_oku(nisler_yolu)
    yeni = collections.OrderedDict()
    for k in kartlar:                                   # aynı kod iki kez → son okuma kalır
        yeni[k["kod"]] = kart_satiri(k, meta, okuma, sozluk)
    reklamlar = o.oku(kok, "reklam")
    mevcut = {r["kutuphane_kodu"]: r for r in reklamlar}
    eklenen = guncellenen = 0
    for kod, r in yeni.items():
        if kod in mevcut:
            eski = mevcut[kod]
            for alan in ("izlendi", "not_no", "sorgu", "aile", "siralama"):
                r[alan] = eski[alan]
            if eski["nis"] not in ("", "belirsiz"):
                r["nis"] = eski["nis"]
            eski.update(r)
            guncellenen += 1
        else:
            reklamlar.append(r)
            mevcut[kod] = r
            eklenen += 1
    dokunulan = {(r["ulke"], kp.birim_anahtari(r)) for r in yeni.values()}
    r_son, b_son = tum_kaydi_yenile(kok, reklamlar, dokunulan)
    aramalar[i].update(kart=str(len(yeni)), durum="TAMAM", ham_dosya=ham_ad)
    o.yaz(kok, "arama", aramalar)
    gorunmeyen = sum(1 for r in yeni.values() if r["ilk_yayin"] == o.GORUNMUYOR)
    etk = collections.Counter(b["etiket"] for b in b_son if (b["ulke"], b["birim"]) in dokunulan)
    print("kaydedildi: %d kart (%d yeni, %d güncellendi, tarihi görünmeyen %d) · birim etiketleri %s · %s"
          % (len(yeni), eklenen, guncellenen, gorunmeyen, dict(etk), o.ESIK_NOTU))
    if gorunmeyen > len(yeni) / 2:
        print("UYARI: kartların yarısından fazlasında tarih okunamadı — meta_topla.js seçicileri sayfayla uyuşmuyor olabilir; "
              "ilk 5 kartı ekranla elle karşılaştır.")


def alan_kaydet(kok, ulke, alan, sonuc, bugun):
    if ulke not in o.ULKELER:
        raise o.VeriHatasi("ülke geçersiz: %s" % ulke)
    if not o.sayi_mi(sonuc):
        raise o.VeriHatasi("sonuç sayı olmalı ('~180 sonuç' → 180); okunamadıysa kaydetme")
    aramalar = o.oku(kok, "arama")
    if not any(a["tarih"] == bugun and a["ulke"] == ulke and a["aile"] == "ALAN" and a["sorgu"] == alan for a in aramalar):
        raise o.VeriHatasi("bugün %s için ALAN sorgusu kaydı yok (`nis_kelime.py kaydet --aile ALAN --sorgu %s`)" % (alan, alan))
    satirlar = o.oku(kok, "alan")
    satirlar.append({"tarih": bugun, "ulke": ulke, "alan": alan, "sonuc": sonuc})
    o.yaz(kok, "alan", satirlar)
    for a in aramalar:
        if a["tarih"] == bugun and a["ulke"] == ulke and a["aile"] == "ALAN" and a["sorgu"] == alan:
            a.update(kart=sonuc, durum="TAMAM")
    o.yaz(kok, "arama", aramalar)
    tum_kaydi_yenile(kok, o.oku(kok, "reklam"))
    print("alan ölçeği yazıldı: %s %s ~%s sonuç" % (ulke, alan, sonuc))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut")
    k = alt.add_parser("kaydet")
    k.add_argument("--kok", default="is/meta")
    k.add_argument("--nisler", default=nk.VARSAYILAN_NISLER)
    k.add_argument("dosyalar", nargs="+")
    a = alt.add_parser("alan")
    a.add_argument("--kok", default="is/meta")
    a.add_argument("--ulke", required=True)
    a.add_argument("--alan", required=True)
    a.add_argument("--sonuc", required=True)
    d = alt.add_parser("denetle")
    d.add_argument("--kok", default="is/meta")
    x = ap.parse_args()
    try:
        if x.komut == "kaydet":
            kaydet(x.kok, x.dosyalar, x.nisler)
        elif x.komut == "alan":
            alan_kaydet(x.kok, x.ulke, x.alan.lower().replace("www.", ""), x.sonuc, o.bugun().date().isoformat())
        elif x.komut == "denetle":
            import kayit_denetle
            sys.exit(kayit_denetle.calistir(x.kok))
        else:
            ap.print_help()
            sys.exit(1)
    except o.VeriHatasi as e:
        o.hata_cik(str(e))


if __name__ == "__main__":
    main()
