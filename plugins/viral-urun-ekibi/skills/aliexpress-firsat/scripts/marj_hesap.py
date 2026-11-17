#!/usr/bin/env python3
"""Inis maliyetli marj hesabi (yalniz Python 3 standart kutuphanesi).

Kullanim:
  marj_hesap.py MARJ.csv [--oranlar EK.tsv] [--cikti SONUC.tsv] [--bugun YYYY-AA-GG]

Oranlar: once eklentideki referans/pazar-oranlari.tsv okunur; sonra (varsa) projedeki
is/firsat/pazar-oranlari.tsv ve --oranlar dosyasi ustune yazilir (kullanici degeri kazanir).
Oran kodda yoktur; hepsi tarihli TSV'dedir.

Satir sutunlari (sablon/marj.csv):
  urun, pazar, para, satis_fiyati, urun_maliyeti, kargo, gumruk_orani_yuzde, tarife_kalemi,
  araci_sabit, odeme_yuzde, odeme_sabit, iade_orani_yuzde, iade_birim_maliyet, teslim_gun, kaynak_notu
Bos hucre -> oranlar dosyasindaki varsayilan; o da yoksa HATA (tahmin yapilmaz).

Hesap:
  matrah     = urun_maliyeti (+ kargo, pazar gumruk_matrahi_kargo_dahil=1 ise)
  gumruk     = satirda oran varsa matrah*oran; yoksa urun_maliyeti <= esik_deger ise
               matrah*esik_alti_gumruk_yuzde + esik_alti_sabit_kalem*tarife_kalemi; yoksa HATA
  odeme      = satis_fiyati*odeme_yuzde + odeme_sabit
  iade       = iade_orani_yuzde * iade_birim_maliyet   (beklenen, siparis basina; COD red dahil)
  inis       = urun + kargo + gumruk + araci + odeme + iade
  net_gelir  = satis_fiyati / (1 + kdv_yuzde)          (fiyat KDV dahil kabul)
  kar        = net_gelir - inis ;  carpan = net_gelir / inis
  P5 (urun puani): carpan <2 -> 0, 2-3 -> 1, >=3 -> 2 ; P6: teslim >15 -> 0, 8-15 -> 1, <=7 -> 2

Cikis: 0 = hesap tamam (uyari olabilir), 1 = veri hatasi, 2 = kullanim hatasi.
"""
import csv
import datetime as dt
import os
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
VARSAYILAN_ORAN = os.path.join(BURADA, "..", "referans", "pazar-oranlari.tsv")
PROJE_ORAN = os.path.join("is", "firsat", "pazar-oranlari.tsv")
PAZARLAR = {"US", "TR", "UK", "DE", "FR", "ES"}
SUTUNLAR = ["urun", "pazar", "para", "satis_fiyati", "urun_maliyeti", "kargo", "gumruk_orani_yuzde",
            "tarife_kalemi", "araci_sabit", "odeme_yuzde", "odeme_sabit", "iade_orani_yuzde",
            "iade_birim_maliyet", "teslim_gun", "kaynak_notu"]
ZORUNLU = ["urun", "pazar", "para", "satis_fiyati", "urun_maliyeti", "kargo", "teslim_gun"]
VARSAYILANLI = ["araci_sabit", "odeme_yuzde", "odeme_sabit", "iade_orani_yuzde", "iade_birim_maliyet"]
ESKI_GUN = 180


class VeriHatasi(Exception):
    pass


def oran_oku(yol, oranlar, kaynak):
    with open(yol, encoding="utf-8", newline="") as f:
        okuyucu = csv.DictReader(f, delimiter="\t")
        gerekli = {"pazar", "anahtar", "deger", "durum", "tarih"}
        if not gerekli.issubset(set(okuyucu.fieldnames or [])):
            raise VeriHatasi(f"{yol}: oran dosyasi basligi eksik ({', '.join(sorted(gerekli))} gerekli)")
        for i, s in enumerate(okuyucu, 2):
            p = (s.get("pazar") or "").strip().upper()
            a = (s.get("anahtar") or "").strip()
            if not p or not a:
                continue
            try:
                dt.date.fromisoformat((s.get("tarih") or "").strip())
            except ValueError:
                raise VeriHatasi(f"{yol}:{i}: tarih YYYY-AA-GG olmali")
            oranlar[(p, a)] = {"deger": (s.get("deger") or "").strip(), "durum": (s.get("durum") or "").strip(),
                               "tarih": s["tarih"].strip(), "kaynak": kaynak}


def sayi(metin, alan, etiket, bos_olur=False):
    m = (metin or "").strip().replace(",", ".")
    if m == "":
        if bos_olur:
            return None
        raise VeriHatasi(f"{etiket}: {alan} bos")
    try:
        v = float(m)
    except ValueError:
        raise VeriHatasi(f"{etiket}: {alan} sayi degil ('{metin}'). Bilinmiyorsa hesaplama; kanit dosyasina 'doğrulanamadı' yaz")
    if v < 0:
        raise VeriHatasi(f"{etiket}: {alan} negatif")
    return v


def hesapla(s, etiket, oranlar, bugun, uyarilar):
    for z in ZORUNLU:
        if not (s.get(z) or "").strip():
            raise VeriHatasi(f"{etiket}: zorunlu alan bos: {z}")
    pazar = s["pazar"].strip().upper()
    if pazar not in PAZARLAR:
        raise VeriHatasi(f"{etiket}: bilinmeyen pazar '{pazar}' ({'/'.join(sorted(PAZARLAR))})")
    kullanilan = []

    def oran(anahtar, zorunlu=True):
        k = oranlar.get((pazar, anahtar))
        if k is None or k["deger"] == "":
            if zorunlu:
                raise VeriHatasi(f"{etiket}: '{anahtar}' satirda da oranlar dosyasinda da yok ({pazar})")
            return None
        kullanilan.append((anahtar, k))
        return k["deger"]

    para = oran("para")
    if s["para"].strip().upper() != para:
        raise VeriHatasi(f"{etiket}: para {s['para']} ama {pazar} pazari {para}; satiri {para}'ye cevirip yaz")
    satis = sayi(s["satis_fiyati"], "satis_fiyati", etiket)
    urun = sayi(s["urun_maliyeti"], "urun_maliyeti", etiket)
    kargo = sayi(s["kargo"], "kargo", etiket)
    teslim = sayi(s["teslim_gun"], "teslim_gun", etiket)
    if satis <= 0 or urun <= 0:
        raise VeriHatasi(f"{etiket}: satis_fiyati ve urun_maliyeti > 0 olmali")
    kalem = sayi(s.get("tarife_kalemi"), "tarife_kalemi", etiket, bos_olur=True) or 1

    deger = {}
    for alan in VARSAYILANLI:
        v = sayi(s.get(alan), alan, etiket, bos_olur=True)
        if v is None:
            v = sayi(oran(alan), alan + " (oranlar)", etiket)
        deger[alan] = v
    for alan in ("odeme_yuzde", "iade_orani_yuzde"):
        if deger[alan] > 100:
            raise VeriHatasi(f"{etiket}: {alan} 100'den buyuk")

    kdv = sayi(oran("kdv_yuzde"), "kdv_yuzde (oranlar)", etiket)
    kargo_dahil = (oran("gumruk_matrahi_kargo_dahil", zorunlu=False) or "0") == "1"
    matrah = urun + (kargo if kargo_dahil else 0)
    g_oran = sayi(s.get("gumruk_orani_yuzde"), "gumruk_orani_yuzde", etiket, bos_olur=True)
    if g_oran is not None:
        if g_oran > 100:
            raise VeriHatasi(f"{etiket}: gumruk_orani_yuzde 100'den buyuk")
        gumruk, gumruk_not = matrah * g_oran / 100, f"satir %{g_oran:g}"
    else:
        esik = oran("esik_deger", zorunlu=False)
        if esik is None:
            raise VeriHatasi(f"{etiket}: gumruk_orani_yuzde bos ve {pazar} icin muafiyet esigi yok -> urunun tarife oranini yaz")
        esik = sayi(esik, "esik_deger (oranlar)", etiket)
        if urun > esik:
            raise VeriHatasi(f"{etiket}: urun degeri {urun:g} > esik {esik:g}; gumruk_orani_yuzde zorunlu")
        y = sayi(oran("esik_alti_gumruk_yuzde"), "esik_alti_gumruk_yuzde", etiket)
        sabit = sayi(oran("esik_alti_sabit_kalem", zorunlu=False), "esik_alti_sabit_kalem", etiket, bos_olur=True) or 0
        gumruk = matrah * y / 100 + sabit * kalem
        gumruk_not = f"esik alti: %{y:g} + {sabit:g}x{kalem:g} kalem"

    odeme = satis * deger["odeme_yuzde"] / 100 + deger["odeme_sabit"]
    iade = deger["iade_orani_yuzde"] / 100 * deger["iade_birim_maliyet"]
    inis = urun + kargo + gumruk + deger["araci_sabit"] + odeme + iade
    net = satis / (1 + kdv / 100)
    kar = net - inis
    carpan = net / inis
    p5 = 0 if carpan < 2 else (1 if carpan < 3 else 2)
    p6 = 0 if teslim > 15 else (1 if teslim > 7 else 2)

    for anahtar, k in kullanilan:
        if k["durum"] not in ("dogrulandi", "model"):
            uyarilar.append(f"{etiket}: {pazar}.{anahtar}={k['deger']} durum={k['durum']} ({k['kaynak']})")
        yas = (bugun - dt.date.fromisoformat(k["tarih"])).days
        if yas > ESKI_GUN:
            uyarilar.append(f"{etiket}: {pazar}.{anahtar} {yas} gunluk -> kaynaktan yeniden kontrol et")
    return {"urun": s["urun"].strip(), "pazar": pazar, "para": para, "satis": satis, "net_gelir": net,
            "urun_maliyeti": urun, "kargo": kargo, "gumruk": gumruk, "gumruk_not": gumruk_not,
            "araci": deger["araci_sabit"], "odeme": odeme, "iade": iade, "inis": inis, "kar": kar,
            "carpan": carpan, "eski_carpan": satis / (urun + kargo), "teslim_gun": teslim, "P5": p5, "P6": p6}


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    girdi = argv[1]
    ek = argv[argv.index("--oranlar") + 1] if "--oranlar" in argv else None
    cikti = argv[argv.index("--cikti") + 1] if "--cikti" in argv else None
    bugun = dt.date.fromisoformat(argv[argv.index("--bugun") + 1]) if "--bugun" in argv else dt.date.today()

    oranlar = {}
    try:
        oran_oku(VARSAYILAN_ORAN, oranlar, "eklenti")
        if os.path.isfile(PROJE_ORAN):
            oran_oku(PROJE_ORAN, oranlar, PROJE_ORAN)
        if ek:
            oran_oku(ek, oranlar, ek)
    except (OSError, VeriHatasi) as e:
        print(f"HATA: {e}")
        return 1
    if not os.path.isfile(girdi):
        print(f"HATA: dosya yok: {girdi}")
        return 1

    with open(girdi, encoding="utf-8-sig", newline="") as f:
        ornek = f.read(2048)
        f.seek(0)
        ayrac = "\t" if ornek.count("\t") > ornek.count(",") else ","
        okuyucu = csv.DictReader(f, delimiter=ayrac)
        eksik = [c for c in SUTUNLAR if c not in (okuyucu.fieldnames or [])]
        if eksik:
            print(f"HATA: eksik sutun: {', '.join(eksik)} (sablon/marj.csv basligini kullan)")
            return 1
        satirlar = list(okuyucu)
    if not satirlar:
        print("HATA: veri satiri yok")
        return 1

    hatalar, uyarilar, sonuc = [], [], []
    for i, s in enumerate(satirlar, 2):
        try:
            sonuc.append(hesapla(s, f"satir {i}", oranlar, bugun, uyarilar))
        except VeriHatasi as e:
            hatalar.append(str(e))

    for r in sonuc:
        print(f"{r['urun'][:40]} | {r['pazar']} | satis {r['satis']:.2f} {r['para']} (net {r['net_gelir']:.2f}) | "
              f"inis {r['inis']:.2f} [urun {r['urun_maliyeti']:.2f} + kargo {r['kargo']:.2f} + gumruk {r['gumruk']:.2f} "
              f"({r['gumruk_not']}) + araci {r['araci']:.2f} + odeme {r['odeme']:.2f} + iade {r['iade']:.2f}] | "
              f"kar {r['kar']:.2f} | carpan {r['carpan']:.2f}x (eski: satis/(urun+kargo) {r['eski_carpan']:.2f}x) | "
              f"teslim {r['teslim_gun']:g} g | P5={r['P5']} P6={r['P6']}")
    for u in dict.fromkeys(uyarilar):
        print(f"UYARI {u}")
    for h in hatalar:
        print(f"HATA {h}")
    if cikti and sonuc:
        alanlar = ["urun", "pazar", "para", "satis", "net_gelir", "urun_maliyeti", "kargo", "gumruk", "araci",
                   "odeme", "iade", "inis", "kar", "carpan", "eski_carpan", "teslim_gun", "P5", "P6"]
        with open(cikti, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(alanlar + ["hesap_tarihi"])
            for r in sonuc:
                w.writerow([f"{r[a]:.2f}" if isinstance(r[a], float) else r[a] for a in alanlar] + [bugun.isoformat()])
    print(f"TOPLAM: {len(sonuc)} hesaplandi, {len(hatalar)} hata, {len(set(uyarilar))} uyari")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
