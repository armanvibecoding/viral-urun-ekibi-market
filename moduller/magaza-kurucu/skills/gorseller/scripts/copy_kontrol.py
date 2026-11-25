#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copy yazı sınırı denetçisi (denetim 2026-11-25 #24, V3): ajan kendi kelime/karakter sayısını saymaz, betik sayar.

  python3 copy_kontrol.py METINLER.md [--pazar TR|US|DE…] [--bilgi URUN-KILIDI.md …] [--toplam 40]

Sınırlar (agents/copy.md "Sınırlar"): başlık ≤ 5 kelime · kart etiketi ≤ 14 karakter · açıklama ≤ 12 kelime · kare toplamı ≤ 40 kelime.
Biçim: uzun tire (— –), ünlem, "X değil Y" kalıbı (TR), TR'de ondalık nokta ("7.5 cm" → "7,5 cm").
Türkçe İ/I (yalnız pazar TR): büyük harfli satırda küçük harf i/ı/ş/ğ… kalmışsa (naif .upper() izi) ya da küçük harfli kelimede ortada büyük İ/I varsa
HATA; `--bilgi` dosyasındaki (URUN-KILIDI.md: doğrulanmış bilgi) kelimenin doğru Türkçe büyük harfi ile ASCII-eş ama farklı yazılmış büyük harfli
kelime ("BITIS" ↔ "BİTİŞ") HATA. Bilgi dosyasında olmayan kelime için İ/I doğruluğu ölçülemez: ÖLÇÜLEMEYEN olarak listelenir (geçti sayılmaz).
Çıkış: 0 sorun yok (ölçülemeyen yok) · 1 sınır/biçim hatası · 3 hata yok ama İ/I ölçülemeyen kelime var (TR) · 2 kullanım / yazı bulunamadı.
"""
import argparse
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metinler  # noqa: E402

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SINIR = {"baslik_kelime": 5, "etiket_karakter": 14, "aciklama_kelime": 12, "toplam_kelime": 40}
TR_ILE = str.maketrans({"i": "İ", "ı": "I"})
ASCII = str.maketrans({"İ": "I", "ı": "I", "i": "I", "Ş": "S", "ş": "S", "Ğ": "G", "ğ": "G", "Ü": "U", "ü": "U", "Ö": "O", "ö": "O", "Ç": "C", "ç": "C"})


def tr_ust(s):
    return s.translate(TR_ILE).upper()


def asc(s):
    return s.translate(ASCII).upper()


def kelimeler(metin):
    return re.findall(r"[^\W_]+(?:[’'.,][^\W_]+)*", metin, re.U)


def buyuk_satir(metin):
    harf = [c for c in metin if c.isalpha()]
    return len(harf) >= 3 and sum(c.isupper() for c in harf) / len(harf) >= 0.8


def kontrol(slotlar, pazar, bilgi_kelimeleri, toplam_sinir):
    hatalar, olculemeyen = [], set()
    for sl in slotlar:
        ad = "/".join(sl["adlar"])
        toplam = 0
        for t, m in sl["alanlar"]:
            n = len(kelimeler(m))
            toplam += n
            if t == "baslik" and n > SINIR["baslik_kelime"]:
                hatalar.append("%s: başlık %d kelime (en çok %d): %s" % (ad, n, SINIR["baslik_kelime"], m[:50]))
            if t == "etiket" and len(m) > SINIR["etiket_karakter"]:
                hatalar.append("%s: kart etiketi %d karakter (en çok %d): %s" % (ad, len(m), SINIR["etiket_karakter"], m))
            if t == "aciklama" and n > SINIR["aciklama_kelime"]:
                hatalar.append("%s: açıklama %d kelime (en çok %d): %s" % (ad, n, SINIR["aciklama_kelime"], m[:50]))
            if re.search(r"[—–]", m):
                hatalar.append("%s: uzun tire (yasak): %s" % (ad, m[:50]))
            if "!" in m:
                hatalar.append("%s: ünlem (yasak): %s" % (ad, m[:50]))
            if pazar == "TR":
                if re.search(r"\b\w+\s+değil[,.]?\s+\w+", m, re.I):
                    hatalar.append("%s: 'X değil Y' kalıbı (yasak): %s" % (ad, m[:50]))
                if re.search(r"\d\.\d+\s?(cm|mm|ml|kg|g|lt|l|m|dk|sn)\b", m, re.I):
                    hatalar.append("%s: ondalık nokta (Türkçede virgül): %s" % (ad, m[:50]))
                bu = buyuk_satir(m)
                for k in kelimeler(m):
                    if bu and re.search(r"[iışğüöç]", k):
                        hatalar.append("%s: büyük harfli satırda küçük harf kalmış ('%s'; naif .upper() izi): %s" % (ad, k, m[:50]))
                        break
                    if not bu and len(k) > 2 and re.search(r"[a-zçğıöşü][İI]", k) :
                        hatalar.append("%s: küçük harfli kelimede ortada büyük İ/I ('%s'): %s" % (ad, k, m[:50]))
                        break
                if bu:
                    for k in kelimeler(m):
                        if "I" in k or "İ" in k:
                            dogru = bilgi_kelimeleri.get(asc(k))
                            if dogru and dogru != k:
                                hatalar.append("%s: İ/I yanlış: '%s' (doğrulanmış bilgiye göre '%s')" % (ad, k, dogru))
                            elif not dogru and len(k) > 1:
                                olculemeyen.add(k)
        if toplam > toplam_sinir:
            hatalar.append("%s: kare toplamı %d kelime (en çok %d)" % (ad, toplam, toplam_sinir))
    return hatalar, sorted(olculemeyen)


def bilgi_oku(yollar):
    harita = {}
    for y in yollar:
        if not os.path.isfile(y):
            continue
        with open(y, encoding="utf-8") as f:
            for k in kelimeler(f.read()):
                if len(k) > 1 and not buyuk_satir(k):
                    harita.setdefault(asc(k), tr_ust(k))
    return harita


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("metinler")
    ap.add_argument("--pazar", default="TR")
    ap.add_argument("--bilgi", action="append")
    ap.add_argument("--toplam", type=int, default=SINIR["toplam_kelime"])
    a = ap.parse_args()
    if not os.path.isfile(a.metinler):
        print("HATA: dosya yok: %s" % a.metinler)
        return 2
    slotlar = metinler.oku(a.metinler)
    if not any(s["alanlar"] for s in slotlar):
        print("HATA: yazı bulunamadı (METINLER.md biçimi: `- slot: metin | alt satır: …` ya da `### G1` altında alan tablosu)")
        return 2
    bilgi = a.bilgi or [os.path.join(os.path.dirname(os.path.abspath(a.metinler)), "URUN-KILIDI.md")]
    hatalar, olculemeyen = kontrol(slotlar, a.pazar.upper(), bilgi_oku(bilgi), a.toplam)
    for h in hatalar:
        print("HATA:", h)
    if olculemeyen and not hatalar:
        print("ÖLÇÜLEMEYEN: İ/I doğruluğu bilgi dosyasında karşılığı olmayan büyük harfli kelimelerde ölçülemedi: %s (gözle kontrol; geçti sayılmaz)" % ", ".join(olculemeyen[:12]))
    print("COPY KONTROL: %s (%d slot, %d hata%s)" % ("KALDI" if hatalar else ("ölçülemeyen var" if olculemeyen else "GEÇTİ"), len(slotlar), len(hatalar),
                                                    ", %d kelime ölçülemedi" % len(olculemeyen) if olculemeyen else ""))
    return 1 if hatalar else (3 if olculemeyen else 0)


if __name__ == "__main__":
    sys.exit(main())
