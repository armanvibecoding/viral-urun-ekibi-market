#!/usr/bin/env python3
"""Kreatif desen sayacı — kazanan ile kaybedeni KARŞILAŞTIRIR (hayatta kalan yanlılığına karşı).

  python3 desen_say.py is/kesfet/kreatif/kayit.csv [--cikti is/meta/desen-<tarih>.md] [--kaynak META-reklam]

Girdi: virgül ya da sekme ayrılmış, başlıklı tablo (şema: referans/kayit-semasi.md §kayit.csv). `kazanan` E/H'yi betik HESAPLAR:
  META-reklam / TTCC-topads : reklam_gun ≥30 ve kopya ≥3                                (DENEME)
  organik (IG/TT/YT/BIZ)    : izlenme/hesap_medyan ≥4,7 ve paylasim/izlenme ≥%0,61     (AB pazarında beğeni/izlenme ≥%1,01)
  Gerekli sayı görünmüyorsa satır "bilinmiyor" sayılır, karşılaştırmaya girmez.
Desen sütunları: kanca_ailesi, giris_turu, format, ses, cta, duygu, mizah, mekanizma.
Hüküm: AYIRT EDİYOR = kazananlarda oran kaybedenlerden yüksek VE ≥3 farklı hesapta · AYIRT ETMİYOR · YETERSİZ (n<3 hesap).
Reddeder (çıkış 1): dosya/başlık eksik · `kazanan` elle yazılmış ve hesapla çelişiyor · hiç kaybeden ya da hiç kazanan yok.
"""
import argparse
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

DESEN = ["kanca_ailesi", "giris_turu", "format", "ses", "cta", "duygu", "mizah", "mekanizma"]
ZORUNLU = ["id", "kaynak", "hesap", "pazar"] + DESEN
REKLAM_KAYNAK = ("META-reklam", "TTCC-topads")
ORG = {"aykirilik": 4.7, "paylasim": 0.0061, "begeni_ab": 0.0101}


def sayi(v):
    """'12000' · '0,61' · '1,5' → float; ham sayı yazılır (12B/1,2MN yazılmaz)."""
    v = (v or "").strip().replace(" ", "")
    v = v.replace(",", ".") if (v.count(",") == 1 and "." not in v) else v.replace(",", "")
    try:
        return float(v)
    except ValueError:
        return None


def kazanan_hesapla(r):
    k = r.get("kaynak", "")
    if k in REKLAM_KAYNAK:
        g, c = sayi(r.get("reklam_gun")), sayi(r.get("kopya"))
        if g is None or c is None:
            return None
        return "E" if (g >= o.ESIK["kreatif_aktif_gun"] and c >= o.ESIK["kreatif_kopya"]) else "H"
    iz, med = sayi(r.get("izlenme")), sayi(r.get("hesap_medyan"))
    if not iz or not med:
        return None
    ab = (r.get("pazar") or "").startswith("AB")
    ikinci = sayi(r.get("begeni")) if ab else sayi(r.get("paylasim"))
    if ikinci is None:
        return None
    esik2 = ORG["begeni_ab"] if ab else ORG["paylasim"]
    return "E" if (iz / med >= ORG["aykirilik"] and ikinci / iz >= esik2) else "H"


def oku(yol):
    if not os.path.exists(yol):
        raise o.VeriHatasi("dosya yok: %s" % yol)
    with open(yol, encoding="utf-8", newline="") as f:
        ilk = f.readline()
        f.seek(0)
        ayrac = "\t" if ilk.count("\t") > ilk.count(",") else ","
        satirlar = list(csv.DictReader(f, delimiter=ayrac))
    if not satirlar:
        raise o.VeriHatasi("tablo boş")
    eksik = [c for c in ZORUNLU if c not in satirlar[0]]
    if eksik:
        raise o.VeriHatasi("başlıkta eksik sütun: %s" % ", ".join(eksik))
    return satirlar


def say(satirlar, kaynak_suzgec):
    if kaynak_suzgec:
        satirlar = [r for r in satirlar if r["kaynak"] == kaynak_suzgec]
    celiski, kaz, kay, bilinmiyor = [], [], [], 0
    for r in satirlar:
        h = kazanan_hesapla(r)
        elle = (r.get("kazanan") or "").strip().upper()
        if elle in ("E", "H") and h is not None and elle != h:
            celiski.append("%s: elle=%s hesap=%s" % (r["id"], elle, h))
        if h == "E":
            kaz.append(r)
        elif h == "H":
            kay.append(r)
        else:
            bilinmiyor += 1
    if celiski:
        raise o.VeriHatasi("`kazanan` elle yazılmış ve hesapla çelişiyor (%d): %s" % (len(celiski), "; ".join(celiski[:10])))
    if not kaz or not kay:
        raise o.VeriHatasi("karşılaştırma yok: kazanan %d, kaybeden %d — iki taraf da ≥1 olmalı (yalnız kazanan sayılırsa desen "
                           "ayırt edici mi bilinemez)" % (len(kaz), len(kay)))
    sonuc = []
    for c in DESEN:
        degerler = collections.Counter(v.strip() for r in kaz + kay for v in [r.get(c, "")] if v.strip() and v.strip() != o.GORUNMUYOR)
        for d, _ in degerler.most_common():
            nk = sum(1 for r in kaz if r.get(c, "").strip() == d)
            nkb = sum(1 for r in kay if r.get(c, "").strip() == d)
            hesap = len({r["hesap"] for r in kaz if r.get(c, "").strip() == d})
            ok, okb = nk / len(kaz), nkb / len(kay)
            if hesap < 3:
                hukum = "YETERSİZ (n<3 hesap)"
            elif ok > okb:
                hukum = "AYIRT EDİYOR"
            else:
                hukum = "AYIRT ETMİYOR"
            sonuc.append((c, d, nk, len(kaz), nkb, len(kay), ok, okb, hesap, hukum))
    return sonuc, len(kaz), len(kay), bilinmiyor


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tablo")
    ap.add_argument("--cikti")
    ap.add_argument("--kaynak")
    a = ap.parse_args()
    try:
        sonuc, nk, nkb, nb = say(oku(a.tablo), a.kaynak)
    except o.VeriHatasi as e:
        o.hata_cik(str(e))
    satir = ["# Kreatif desen sayımı — kazanan %d · kaybeden %d · bilinmiyor %d (%s)" % (nk, nkb, nb, o.ESIK_NOTU), "",
             "| Sütun | Değer | Kazanan | Kaybeden | Oran K | Oran KB | Hesap (K) | Hüküm |", "|---|---|---|---|---|---|---|---|"]
    sonuc.sort(key=lambda s: (s[9] != "AYIRT EDİYOR", -(s[6] - s[7])))
    for c, d, a1, b1, a2, b2, ok, okb, h, hk in sonuc:
        satir.append("| %s | %s | %d/%d | %d/%d | %%%.0f | %%%.0f | %d | %s |" % (c, d, a1, b1, a2, b2, ok * 100, okb * 100, h, hk))
    metin = "\n".join(satir) + "\n"
    if a.cikti:
        with open(a.cikti, "w", encoding="utf-8") as f:
            f.write(metin)
        print("%s yazıldı (%d desen satırı, AYIRT EDİYOR %d)" % (a.cikti, len(sonuc), sum(1 for s in sonuc if s[9] == "AYIRT EDİYOR")))
    else:
        print(metin)


if __name__ == "__main__":
    main()
