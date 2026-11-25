#!/usr/bin/env python3
"""tr_marj.py: Trendyol avı net marj hesabı (yalnız Python 3 standart kütüphanesi).

Kullanım: tr_marj.py MARJ.csv [--cikti SONUC.tsv] [--oranlar tr-oranlari.tsv] [--marka-roas 2.8] [--profil DOSYA]

Girdi sütunları (CSV, virgül ya da sekme):
  urun, satis_fiyati, alis_fiyati, alis_kdv_dahil(E/H), fatura_kurumsal(E/H), kdv_yuzde, tedarik_kargo, musteri_kargo,
  odeme_yuzde, odeme_sabit, kapida_odeme_orani_yuzde, kapida_ek_ucret, iade_orani_yuzde, iade_birim_maliyet,
  reklam_payi_yuzde, kaynak_notu
Boş hücre → referans/tr-oranlari.tsv varsayılanı; o da boşsa yerleşik TEMKİNLİ varsayılan (aşağıdaki TEMKINLI, "varsayim" etiketiyle
oran_kaynaklari sütununa yazılır): hesap oran yüzünden durmaz (kurucu kararı 2026-11-25). reklam_payi_yuzde boşsa net_kar hesaplanmaz.

  net_gelir = satis / (1 + kdv) · alis_net = alis / (1 + kdv) (alis_kdv_dahil=E ve fatura_kurumsal=E; değilse alis aynen)
  odeme = satis*odeme_yuzde + odeme_sabit + kapida_orani*kapida_ek · iade = iade_orani*iade_birim_maliyet
  maliyet = alis_net + tedarik_kargo + musteri_kargo + odeme + iade · katki = net_gelir - maliyet · carpan = net_gelir / maliyet
  basabas_roas = satis / katki (katki <= 0 → "zarar") · net_kar = katki - satis*reklam_payi
  karar_marj: ROAS markaya özeldir. pay = marka_roas / basabas_roas (marka_roas: --marka-roas ya da tr-oranlari.tsv
  "marka_roas"; markanın kendi reklam hesabındaki gerçek ROAS). Eşik esikler.tsv; marka_roas yoksa "dogrulanamadi".

Çıkış: 0 hesap tamam · 1 veri hatası · 2 kullanım hatası.
"""
import csv
import os
import sys
import datetime

BURADA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BURADA, "..", "..", "..", "..", "ortak"))
import profil as profil_mod  # noqa: E402  (danışanın işletme profili: .ekip/isletme-profili.tsv)

ORAN_YOLU = os.path.join(BURADA, "..", "referans", "tr-oranlari.tsv")
ESIK_YOLU = os.path.join(BURADA, "..", "referans", "esikler.tsv")
SUTUNLAR = ["urun", "satis_fiyati", "alis_fiyati", "alis_kdv_dahil", "fatura_kurumsal", "kdv_yuzde", "tedarik_kargo",
            "musteri_kargo", "odeme_yuzde", "odeme_sabit", "kapida_odeme_orani_yuzde", "kapida_ek_ucret",
            "iade_orani_yuzde", "iade_birim_maliyet", "reklam_payi_yuzde", "kaynak_notu"]
ORANLI = ["kdv_yuzde", "odeme_yuzde", "odeme_sabit", "musteri_kargo", "kapida_odeme_orani_yuzde", "kapida_ek_ucret",
          "iade_orani_yuzde", "iade_birim_maliyet"]
ZORUNLU = ["satis_fiyati", "alis_fiyati", "tedarik_kargo"]
# tr-oranlari.tsv'de değeri olmayan oran için kaynaklı/temkinli yerleşik varsayılan (tsv'deki kaynaklı değerlerle aynı; marj'ı şişirmez)
TEMKINLI = {"kdv_yuzde": "20", "odeme_yuzde": "4.29", "odeme_sabit": "0.25", "musteri_kargo": "150",
            "kapida_odeme_orani_yuzde": "0", "kapida_ek_ucret": "0", "iade_orani_yuzde": "10", "iade_birim_maliyet": "150"}
CIKTI = ["urun", "net_gelir", "alis_net", "odeme", "iade", "maliyet", "katki", "carpan", "basabas_roas", "reklam",
         "net_kar", "marka_roas", "marka_payi", "karar_marj", "oran_kaynaklari"]


class Hata(Exception):
    pass


def sayi(metin, alan, satir):
    s = (metin or "").strip().replace(" ", "")
    if s == "":
        return None
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        raise Hata("satır %d: %s sayı değil: %r" % (satir, alan, metin))


def tsv(yol):
    with open(yol, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.reader(f, delimiter="\t") if any(h.strip() for h in r)]


def oranlari_oku(yol):
    if not os.path.isfile(yol):
        raise Hata("oran dosyası yok: %s" % yol)
    s = tsv(yol)
    out = {}
    for r in s[1:]:
        r = r + [""] * 6
        out[r[0]] = {"deger": r[1].strip(), "durum": r[2].strip(), "tarih": r[3].strip(), "kaynak": r[4].strip()}
    return out


PROFIL_ORAN = ("kapida_odeme_orani_yuzde", "kapida_ek_ucret", "marka_roas")


def profil_uygula(oranlar, profil, yol):
    """Danışanın işletme profili eklenti varsayılanının ÜSTÜNE yazar (kaynak sırası: satır > profil > eklenti varsayılanı).
    Profil yoksa hiçbir şey değişmez; çıktıda "eklenti varsayılanı" notu basılır."""
    bugun = datetime.date.today().isoformat()
    for a in PROFIL_ORAN:
        if a in profil:
            oranlar[a] = {"deger": ("%g" % profil[a]), "durum": "profil", "tarih": bugun, "kaynak": os.path.basename(yol)}
    if profil:
        print("PROFIL: %s kullanıldı (%s)" % (", ".join(a for a in PROFIL_ORAN if a in profil) or "ilgili alan yok", yol))
    else:
        print("PROFIL: yok → eklenti varsayılanı kullanıldı (kapıda ödeme %s%%; kendi oranını .ekip/isletme-profili.tsv'ye yaz)"
              % oranlar.get("kapida_odeme_orani_yuzde", {}).get("deger", "0"))


def esik_oku(anahtar):
    for r in tsv(ESIK_YOLU)[1:]:
        if r[0] == anahtar:
            return r
    raise Hata("esikler.tsv'de %s yok" % anahtar)


def roas_karari(roas, marka_roas):
    """ROAS markaya özeldir (kurucu kararı 2026-11-25): sabit eşik yok. pay = marka_roas / basabas_roas.
    esikler.tsv basabas_roas: sat 'pay>=X', izle 'A-B'. Marka ROAS'ı yoksa dogrulanamadi (satır en fazla İZLE)."""
    if roas is None:
        return "ELE"
    if marka_roas is None:
        return "dogrulanamadi"
    r = esik_oku("basabas_roas")
    sat = float(r[2].replace("pay>=", ""))
    a = float(r[3].split("-")[0])
    pay = marka_roas / roas
    if pay >= sat:
        return "SAT"
    if pay >= a:
        return "İZLE"
    return "ELE"


def satir_oku(yol):
    with open(yol, encoding="utf-8-sig", newline="") as f:
        ilk = f.readline()
        f.seek(0)
        ayirac = "\t" if "\t" in ilk else ","
        okuyucu = csv.DictReader(f, delimiter=ayirac)
        if okuyucu.fieldnames is None or [h.strip() for h in okuyucu.fieldnames] != SUTUNLAR:
            raise Hata("başlık tam bu sütunlar olmalı: %s" % ", ".join(SUTUNLAR))
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in okuyucu]


def hesapla(r, no, oranlar, marka_roas=None):
    kul = []

    def al(alan, zorunlu_satir=False):
        v = sayi(r[alan], alan, no)
        if v is not None:
            return v
        if alan in oranlar and oranlar[alan]["deger"] != "":
            o = oranlar[alan]
            kul.append("%s=%s(%s,%s,%s)" % (alan, o["deger"], o["durum"], o["tarih"] or "-", o["kaynak"] or "-"))
            return sayi(o["deger"], alan, no)
        if alan in TEMKINLI:
            kul.append("%s=%s(varsayim,yerleşik temkinli)" % (alan, TEMKINLI[alan]))
            return float(TEMKINLI[alan])
        raise Hata("satır %d (%s): %s boş ve tr-oranlari.tsv'de değer yok: tahmin yapılmaz" % (no, r["urun"], alan))

    if not r["urun"]:
        raise Hata("satır %d: urun boş" % no)
    for a in ZORUNLU:
        if sayi(r[a], a, no) is None:
            raise Hata("satır %d (%s): %s zorunlu" % (no, r["urun"], a))
    for a in ("alis_kdv_dahil", "fatura_kurumsal"):
        if r[a].upper() not in ("E", "H"):
            raise Hata("satır %d (%s): %s E ya da H olmalı" % (no, r["urun"], a))
    satis, alis, tedarik = sayi(r["satis_fiyati"], "", no), sayi(r["alis_fiyati"], "", no), sayi(r["tedarik_kargo"], "", no)
    v = {a: al(a) for a in ORANLI + ["musteri_kargo"]}
    kdv = v["kdv_yuzde"] / 100.0
    net = satis / (1 + kdv)
    alis_net = alis / (1 + kdv) if r["alis_kdv_dahil"].upper() == "E" and r["fatura_kurumsal"].upper() == "E" else alis
    odeme = satis * v["odeme_yuzde"] / 100.0 + v["odeme_sabit"] + v["kapida_odeme_orani_yuzde"] / 100.0 * v["kapida_ek_ucret"]
    iade = v["iade_orani_yuzde"] / 100.0 * v["iade_birim_maliyet"]
    maliyet = alis_net + tedarik + v["musteri_kargo"] + odeme + iade
    katki = net - maliyet
    carpan = net / maliyet if maliyet > 0 else None
    roas = satis / katki if katki > 0 else None
    reklam_pay = sayi(r["reklam_payi_yuzde"], "reklam_payi_yuzde", no)
    if reklam_pay is None and oranlar.get("reklam_payi_yuzde", {}).get("deger", "") != "":
        o = oranlar["reklam_payi_yuzde"]
        kul.append("reklam_payi_yuzde=%s(%s,%s,%s)" % (o["deger"], o["durum"], o["tarih"] or "-", o["kaynak"] or "-"))
        reklam_pay = sayi(o["deger"], "reklam_payi_yuzde", no)
    reklam = satis * reklam_pay / 100.0 if reklam_pay is not None else None
    return {"urun": r["urun"], "net_gelir": net, "alis_net": alis_net, "odeme": odeme, "iade": iade, "maliyet": maliyet,
            "katki": katki, "carpan": carpan, "basabas_roas": "zarar" if roas is None else roas,
            "reklam": reklam, "net_kar": None if reklam is None else katki - reklam,
            "marka_roas": marka_roas, "marka_payi": (marka_roas / roas) if (roas and marka_roas) else None,
            "karar_marj": roas_karari(roas, marka_roas), "oran_kaynaklari": "; ".join(kul) or "satırdan"}


def bicim(v):
    if v is None:
        return "hesaplanmadi"
    return "%.2f" % v if isinstance(v, float) else str(v)


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    yol = argv[1]
    cikti = argv[argv.index("--cikti") + 1] if "--cikti" in argv else None
    oran_yol = argv[argv.index("--oranlar") + 1] if "--oranlar" in argv else ORAN_YOLU
    try:
        if not os.path.isfile(yol):
            raise Hata("girdi dosyası yok: %s" % yol)
        oranlar = oranlari_oku(oran_yol)
        profil_yol = argv[argv.index("--profil") + 1] if "--profil" in argv else None
        profil = profil_mod.oku(profil_yol)
        profil_uygula(oranlar, profil, profil_mod.yol_bul(profil_yol))
        satirlar = satir_oku(yol)
        if not satirlar:
            raise Hata("girdide satır yok")
        mr = argv[argv.index("--marka-roas") + 1] if "--marka-roas" in argv else oranlar.get("marka_roas", {}).get("deger", "")
        marka_roas = sayi(mr, "marka_roas", 0) if mr != "" else None
        if marka_roas is not None and marka_roas <= 0:
            raise Hata("marka_roas pozitif olmalı")
        sonuc = [hesapla(r, i, oranlar, marka_roas) for i, r in enumerate(satirlar, 2)]
    except (Hata, profil_mod.ProfilHatasi) as e:
        print("HATA: %s" % e)
        return 1
    for s in sonuc:
        print("%s | katki %s | carpan %s | basabas ROAS %s | net kar %s | %s" % (
            s["urun"], bicim(s["katki"]), bicim(s["carpan"]), bicim(s["basabas_roas"]), bicim(s["net_kar"]), s["karar_marj"]))
        print("  oranlar: %s" % s["oran_kaynaklari"])
    if cikti:
        with open(cikti, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(CIKTI)
            for s in sonuc:
                w.writerow([bicim(s[a]) if a != "oran_kaynaklari" else s[a] for a in CIKTI])
    print("TOPLAM: %d hesaplandı" % len(sonuc))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
