#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""panel_medyan.py kırma testleri. Kullanım: python3 panel_medyan_test.py → 0 hepsi geçerse, 1 biri tutmazsa.
Beklenen: elle hesaplanmış medyan/toplam/sıra; aynı girdi iki kez → bayt bayt aynı çıktı (Director elle çıkarırken tutmayan şey)."""
import json
import os
import subprocess
import sys
import tempfile

B = os.path.dirname(os.path.abspath(__file__))
PM = os.path.join(B, "panel_medyan.py")
BO = ["tipografi", "renk", "kompozisyon", "urun", "metin", "nise", "mobil"]
sonuc = []


def kos(*a):
    r = subprocess.run([sys.executable, PM] + list(a), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def bekle(ad, ok, ayrinti=""):
    sonuc.append(bool(ok))
    print("%s %s%s" % ("GEÇTİ" if ok else "KALDI", ad, "" if ok else "\n    " + str(ayrinti)[-500:]))


def kor(a, b, c, d, sira, yapay=(), **ek):
    def p(x):
        return {k: v for k, v in zip(BO, x)}
    return dict({"puanlar": {"A": p(a), "B": p(b), "C": p(c), "D": p(d)}, "sira": list(sira), "yapay": list(yapay)}, **ek)


def main():
    with tempfile.TemporaryDirectory() as k:
        A, Bb, C, D = [8, 8, 8, 8, 8, 8, 8], [6] * 7, [9, 9, 9, 9, 9, 9, 9], [4] * 7   # B bizim
        yaz = lambda ad, d: json.dump(d, open(os.path.join(k, ad), "w", encoding="utf-8"))   # noqa: E731
        yaz("KOR-1.json", kor(A, Bb, C, D, "CABD", ["B"]))
        yaz("KOR-2.json", kor([7] * 7, [5, 6, 6, 6, 6, 6, 9], [9] * 7, [4] * 7, "CABD", ["B"]))
        yaz("KOR-3.json", kor([8] * 7, [7] * 7, [9] * 7, [3] * 7, "CBAD", []))
        yaz("_esleme.json", {"A": "referans-1", "B": "bizim", "C": "referans-2", "D": "referans-3"})
        rc, c1 = kos(k, "--esleme", os.path.join(k, "_esleme.json"), "--json", os.path.join(k, "p.json"))
        j = json.load(open(os.path.join(k, "p.json"), encoding="utf-8"))["sonuc"]
        # elle: B medyanları: tipografi med(6,5,7)=6 · renk 6 · kompozisyon 6 · urun 6 · metin 6 · nise 6 · mobil med(6,9,7)=7 → toplam 43/7=6,14 → 6,0 (0,5'e yuvarlı) ; sıra: CABD→3, CABD→3, CBAD→2 → medyan 3
        bekle("elle hesap: B toplam 6.0, medyan sıra 3, yapay oyu 2/3", rc == 0 and j["B"]["toplam"] == 6.0 and j["B"]["sira"] == 3 and j["B"]["yapay_oy"] == 2, c1 + str(j["B"]))
        bekle("bizim satırı işaretlendi", "BİZİM B: toplam 6.0 · medyan sıra 3/4 · yapay oyu 2/3" in c1, c1)
        bekle("kopya ayrışması işaretli (B.mobil 6–9 = 3 > 2)", "mobil" in j["B"]["ayrisan_boyut"], j["B"]["ayrisan_boyut"])
        rc2, c2 = kos(k, "--esleme", os.path.join(k, "_esleme.json"))
        bekle("aynı girdi → bayt bayt aynı çıktı", c1 == c2, (c1, c2))
        # kırma: yetersiz kopya
        os.remove(os.path.join(k, "KOR-3.json"))
        rc, c = kos(k)
        bekle("kırma: 2 geçerli kopya → çıkış 1", rc == 1 and "en az 3" in c, c)
        # kırma: pano_sorunu dolu kopya geçersiz
        yaz("KOR-3.json", kor([8] * 7, [7] * 7, [9] * 7, [3] * 7, "CBAD", [], pano_sorunu="referansta hesap adı görünüyor"))
        rc, c = kos(k)
        bekle("kırma: pano_sorunu dolu → o kopya GEÇERSİZ, çıkış 1", rc == 1 and "pano_sorunu" in c, c)
        # kırma: puan aralık dışı / sıra bozuk / hepsine aynı puan
        yaz("KOR-3.json", kor([8] * 7, [11] + [7] * 6, [9] * 7, [3] * 7, "CBAD"))
        rc, c = kos(k)
        bekle("kırma: puan 11 → geçersiz kopya, çıkış 1", rc == 1 and "0–10 değil" in c, c)
        yaz("KOR-3.json", kor([8] * 7, [7] * 7, [9] * 7, [3] * 7, "CBA"))
        rc, c = kos(k)
        bekle("kırma: sıra eksik → geçersiz kopya", rc == 1 and "sıra" in c, c)
        yaz("KOR-3.json", kor([7] * 7, [7] * 7, [7] * 7, [7] * 7, "ABCD"))
        rc, c = kos(k)
        bekle("kırma: hepsine aynı puan (ayırt etmiyor) → geçersiz", rc == 1 and "ayırt etmiyor" in c, c)
        yaz("KOR-3.json", kor([8] * 7, [7] * 7, [9] * 7, [3] * 7, "CBAD"))
        rc, c = kos(k)
        bekle("iyi: 3 geçerli kopya → çıkış 0", rc == 0, c)
    kalan = sonuc.count(False)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
