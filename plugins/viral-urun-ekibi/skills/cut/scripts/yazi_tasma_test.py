#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yazi_tasma.py kırma testleri. Kullanım: python3 yazi_tasma_test.py → 0 hepsi geçerse · 1 bir kapı tutmadı · 3 font/Pillow yok (ölçülemedi)."""
import json
import os
import subprocess
import sys
import tempfile

B = os.path.dirname(os.path.abspath(__file__))
YT = os.path.join(B, "yazi_tasma.py")
FONTLAR = ["/System/Library/Fonts/Supplemental/Arial Black.ttf", "C:/Windows/Fonts/ariblk.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
sonuc = []


def kos(y, *ek):
    r = subprocess.run([sys.executable, YT, y] + list(ek), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def bekle(ad, ok, ayrinti=""):
    sonuc.append(bool(ok))
    print("%s %s%s" % ("GEÇTİ" if ok else "KALDI", ad, "" if ok else "\n    " + str(ayrinti)[-400:]))


def main():
    font = next((f for f in FONTLAR if os.path.isfile(f)), None)
    try:
        import PIL  # noqa: F401
    except ImportError:
        font = None
    if not font:
        print("ÖLÇÜLEMEDİ: Pillow ya da kalın sistem fontu yok")
        return 3
    with tempfile.TemporaryDirectory() as k:
        def yaz(planlar, **ek):
            y = os.path.join(k, "a.json")
            json.dump(dict({"font": font, "planlar": planlar}, **ek), open(y, "w", encoding="utf-8"))
            return y
        rc, c = kos(yaz([{"klip": "a", "bas": 0, "bit": 1, "yazi": "IS THIS EVEN LEGAL?", "boyut": 100}]))
        bekle("iyi: kısa kanca sığar → çıkış 0", rc == 0 and "GEÇTİ" in c, c)
        rc, c = kos(yaz([{"klip": "a", "bas": 0, "bit": 1, "yazi": "SUPERCALIFRAGILISTICEXPIALIDOCIOUS", "boyut": 140}]))
        bekle("kırma: tek uzun kelime kareden taşar → çıkış 1", rc == 1 and "TAŞMA plan 1" in c, c)
        rc, c = kos(yaz([{"klip": "a", "bas": 0, "bit": 1, "yazi": "THIS HOOK IS WRAPPED INTO LINES AND FITS", "boyut": 90}]))
        bekle("iyi: uzun ama satıra bölünen kanca sığar", rc == 0, c)
        rc, c = kos(yaz([{"klip": "a", "bas": 0, "bit": 1, "yazi": "OK", "boyut": 90}], yazilar=[{"bas": 0, "bit": 1, "yazi": "ELEKTRİKSELCİHAZLARDÜNYASINDAYENİ", "boyut": 120}]))
        bekle("kırma: yazılar[] içindeki taşan yazı da yakalanır", rc == 1 and "yazı 1" in c, c)
        rc, c = kos(yaz([{"klip": "a", "bas": 0, "bit": 1}]))
        bekle("ölçülecek yazı yok → ölçülemedi (3), geçti değil", rc == 3, c)
        # yan pay parametresi: 0 ile sınır 1080'e genişler; taşma varsa mesaj bunu söyler
        rc0, c0 = kos(yaz([{"klip": "a", "bas": 0, "bit": 1, "yazi": "SUPERCALIFRAGILISTICEXPIALIDOCIOUS", "boyut": 140}]), "--yan-pay", "0")
        bekle("yan-pay 0: sınır 1080 olarak raporlanır (taşma varsa)", rc0 == 0 or "en çok 1080" in c0, c0)
    kalan = sonuc.count(False)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
