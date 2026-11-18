#!/usr/bin/env python3
"""teklif-ve-sayfa dogrulayicisi (yalniz Python 3 standart kutuphanesi).

Kullanim:
  teklif_kontrol.py sema TEKLIF.tsv                 sema + izinli degerler + 'bizim' satirinda yasak ifade
  teklif_kontrol.py tara [--pazar P] DOSYA...       sayfa/SSS/e-posta taslaginda yasak ifade taramasi

Yasak desenler kodda degil: referans/yasak-ifadeler.tsv (pazar '*' = hepsi). '{YER_TUTUCU}' icindeki metin taranmaz.
'rakip' satirlari gozlemdir, yasak ifade icin taranmaz (rakibin sahte aciliyetini kaydetmek serbest, kopyalamak yasak).
Cikis: 0 = temiz, 1 = sema hatasi ya da yasak ifade, 2 = kullanim hatasi.
"""
import csv
import datetime as dt
import os
import re
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
YASAK_DOSYASI = os.path.join(BURADA, "..", "referans", "yasak-ifadeler.tsv")
PARA = {"US": "USD", "TR": "TRY", "UK": "GBP", "DE": "EUR", "FR": "EUR", "ES": "EUR"}
SUTUNLAR = ["tur", "tarih", "pazar", "urun", "kaynak_url", "para", "fiyat", "karsilastirma_fiyati",
            "karsilastirma_kaniti", "paket", "garanti", "kargo_vaadi", "odeme_yontemleri", "sosyal_kanit_turu",
            "aciliyet", "itiraz_yanitlari", "upsell", "ilk_ekran", "not"]
BOS_OLAMAZ = ["urun", "paket", "garanti", "kargo_vaadi", "odeme_yontemleri", "sosyal_kanit_turu", "aciliyet",
              "itiraz_yanitlari", "upsell", "ilk_ekran"]
ODEME = {"kart", "kapida", "havale", "taksit", "paypal", "klarna", "afterpay", "shop_pay", "apple_pay",
         "google_pay", "fatura", "bizum", "diger"}
KANIT = {"yok", "gercek_yorum_uygulamasi", "alici_foto", "alici_video", "ugc_izinli", "basin", "sertifika",
         "satis_sayaci", "uydurma_supheli"}
TARANAN = ["urun", "paket", "garanti", "kargo_vaadi", "aciliyet", "itiraz_yanitlari", "upsell", "ilk_ekran", "not",
           "karsilastirma_kaniti"]


def normal(metin):
    """Turkce I/i sorununu onler: hem metin hem desen ayni bicime indirgenir (ı/İ/I -> i)."""
    return metin.replace("İ", "i").lower().replace("ı", "i").replace("i̇", "i")


def desen_oku(pazar):
    desenler = []
    with open(YASAK_DOSYASI, encoding="utf-8", newline="") as f:
        for s in csv.DictReader(f, delimiter="\t"):
            p = (s["pazar"] or "").strip().upper()
            if p == "*" or (pazar and p == pazar):
                desenler.append((re.compile(normal(s["desen"]), re.IGNORECASE), s["sebep"]))
    return desenler


def yasak_bul(metin, desenler):
    temiz = re.sub(r"\{[^{}]*\}", " ", metin)
    temiz = normal(temiz)
    return [(m.group(0), sebep) for d, sebep in desenler for m in [d.search(temiz)] if m]


def sayi(m):
    try:
        return float(m.strip().replace(",", "."))
    except ValueError:
        return None


def sema(yol):
    with open(yol, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f, delimiter="\t")
        alanlar = r.fieldnames or []
        eksik = [c for c in SUTUNLAR if c not in alanlar]
        if eksik:
            print(f"HATA: eksik sutun: {', '.join(eksik)} (sablon/teklif.tsv basligini kullan; ayrac TAB)")
            return 1
        fazla = [c for c in alanlar if c not in SUTUNLAR]
        satirlar = list(r)
    if fazla:
        print(f"UYARI: semada olmayan sutun: {', '.join(fazla)}")
    if not satirlar:
        print("HATA: veri satiri yok")
        return 1
    hatalar = []
    sayac = {"rakip": 0, "bizim": 0}
    for i, s in enumerate(satirlar, 2):
        et = f"satir {i}"
        h = []
        g = {k: (s.get(k) or "").strip() for k in SUTUNLAR}
        tur = g["tur"].lower()
        if tur not in sayac:
            hatalar.append(f"{et}: tur 'rakip' ya da 'bizim' olmali ('{g['tur']}')")
            continue
        sayac[tur] += 1
        try:
            dt.date.fromisoformat(g["tarih"])
        except ValueError:
            h.append("tarih YYYY-AA-GG olmali")
        pazar = g["pazar"].upper()
        if pazar not in PARA:
            h.append(f"bilinmeyen pazar '{g['pazar']}'")
        elif g["para"].upper() != PARA[pazar]:
            h.append(f"para {g['para']} ama {pazar} -> {PARA[pazar]}")
        if tur == "rakip" and not re.match(r"https?://\S+\.\S+", g["kaynak_url"]):
            h.append("rakip satirinda kaynak_url (http/https) zorunlu")
        fiyat = sayi(g["fiyat"])
        if fiyat is None or fiyat <= 0:
            h.append(f"fiyat sayi ve > 0 olmali ('{g['fiyat']}')")
        kf = g["karsilastirma_fiyati"].lower()
        if kf not in ("", "yok", "gorulmedi"):
            k = sayi(kf)
            if k is None:
                h.append(f"karsilastirma_fiyati sayi ya da 'yok' olmali ('{g['karsilastirma_fiyati']}')")
            elif fiyat is not None and k <= fiyat:
                h.append("karsilastirma_fiyati fiyattan buyuk degil")
            elif tur == "bizim" and g["karsilastirma_kaniti"].lower() in ("", "yok", "gorulmedi"):
                h.append("cizili fiyat var ama karsilastirma_kaniti yok (gercekten uygulanmis onceki fiyat kaniti sart)")
        for alan in BOS_OLAMAZ:
            if not g[alan]:
                h.append(f"{alan} bos (bilinmiyorsa 'gorulmedi', yoksa 'yok')")
        if g["odeme_yontemleri"] and g["odeme_yontemleri"].lower() != "gorulmedi":
            bil = [x for x in re.split(r"[;,]", g["odeme_yontemleri"].lower()) if x.strip() and x.strip() not in ODEME]
            if bil:
                h.append(f"bilinmeyen odeme yontemi: {', '.join(x.strip() for x in bil)}")
        if g["sosyal_kanit_turu"] and g["sosyal_kanit_turu"].lower() != "gorulmedi":
            turler = [x.strip() for x in re.split(r"[;,]", g["sosyal_kanit_turu"].lower()) if x.strip()]
            bil = [x for x in turler if x not in KANIT]
            if bil:
                h.append(f"bilinmeyen sosyal_kanit_turu: {', '.join(bil)}")
            if tur == "bizim" and "uydurma_supheli" in turler:
                h.append("bizim teklifte uydurma_supheli sosyal kanit olamaz")
        if tur == "bizim":
            ac = g["aciliyet"].lower()
            if pazar == "TR" and ac != "yok":
                h.append("TR teklifinde aciliyet/baski cumlesi yok: aciliyet 'yok' olmali")
            elif ac != "yok" and not re.fullmatch(r"kampanya_bitis:\d{4}-\d{2}-\d{2}", ac):
                h.append("bizim aciliyet yalniz 'yok' ya da 'kampanya_bitis:YYYY-AA-GG' (gercek kampanya)")
            desenler = desen_oku(pazar if pazar in PARA else None)
            for alan in TARANAN:
                for bulunan, sebep in yasak_bul(g[alan], desenler):
                    h.append(f"yasak ifade [{alan}] '{bulunan}' -> {sebep}")
        for x in h:
            hatalar.append(f"{et}: {x}")
    for x in hatalar:
        print(f"HATA {x}")
    if sayac["rakip"] < 10:
        print(f"UYARI: {sayac['rakip']} rakip satiri (<10) -> desen cikarma icin az; desenler 'tek ornek' sayilir")
    print(f"TOPLAM: {sayac['rakip']} rakip, {sayac['bizim']} bizim, {len(hatalar)} hata")
    return 1 if hatalar else 0


def tara(dosyalar, pazar):
    desenler = desen_oku(pazar)
    bulgu = 0
    for yol in dosyalar:
        if not os.path.isfile(yol):
            print(f"HATA: dosya yok: {yol}")
            bulgu += 1
            continue
        with open(yol, encoding="utf-8", errors="replace") as f:
            for no, satir in enumerate(f, 1):
                for bulunan, sebep in yasak_bul(satir, desenler):
                    print(f"{yol}:{no}: '{bulunan}' -> {sebep}")
                    bulgu += 1
    print(f"TOPLAM: {len(dosyalar)} dosya, {bulgu} bulgu (pazar: {pazar or 'ortak'})")
    return 1 if bulgu else 0


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if len(argv) >= 3 and argv[1] == "sema":
        if not os.path.isfile(argv[2]):
            print(f"HATA: dosya yok: {argv[2]}")
            return 1
        return sema(argv[2])
    if len(argv) >= 3 and argv[1] == "tara":
        args = argv[2:]
        pazar = None
        if "--pazar" in args:
            i = args.index("--pazar")
            pazar = args[i + 1].upper() if i + 1 < len(args) else None
            pazar = "UK" if pazar == "GB" else pazar  # köprü dosyaları ISO (GB) yazar; teklif tablosu UK der
            if pazar not in PARA:
                print(f"HATA: --pazar {'/'.join(PARA)} olmali")
                return 2
            args = args[:i] + args[i + 2:]
        if not args:
            print(__doc__)
            return 2
        return tara(args, pazar)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
