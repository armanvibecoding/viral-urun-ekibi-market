#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""web_olcum.py kırma testleri (Lighthouse + axe). Kullanım: python3 web_olcum_test.py → 0 hepsi doğru · 1 bir kapı tutmadı · 3 araç/Chrome yok (ölçülemedi).

Kırma: kontrastı bilerek bozuk sayfa KALDI, temiz sayfa GEÇTİ; ana iş parçacığını kilitleyen sayfa hız KALDI, hafif sayfa GEÇTİ;
araç yok / sürüm sabit değil → "olculemedi" (çıkış 3), asla GEÇTİ. Ağ yok: sayfalar yerel 127.0.0.1 sunucusundan açılır.
"""
import json
import os
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
BETIK = os.path.join(BURADA, "web_olcum.py")
sys.path.insert(0, BURADA)
import web_olcum  # noqa: E402

SAYFA = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
         '<title>Heat mug</title>%s</head><body style="background:#ffffff;color:#111111"><main><h1>Heat mug</h1>'
         '<p style="color:%s">Pour hot liquid and the pattern appears.</p><a href="#buy" style="color:#0000ee">Buy now</a></main>%s</body></html>')
sonuclar = []


def kos(args, env=None):
    r = subprocess.run([sys.executable, BETIK] + args, capture_output=True, text=True, env=dict(os.environ, **(env or {})))
    return r.returncode, r.stdout + r.stderr


def bekle(ad, rc, beklenen, cikti, parca=None):
    ok = rc == beklenen and (parca is None or parca in cikti)
    sonuclar.append(ok)
    print("%s %s → çıkış %d (beklenen %d)%s" % ("GEÇTİ" if ok else "KALDI", ad, rc, beklenen, "" if ok else "\n    " + cikti.strip().replace("\n", "\n    ")[-600:]))


def yaz(klasor, ad, metin):
    y = os.path.join(klasor, ad)
    with open(y, "w", encoding="utf-8") as f:
        f.write(metin)
    return y


def main():
    tamam, sorun = web_olcum.araclar()
    if not tamam:
        print("ÖLÇÜLEMEDİ: araç yok (%s). Kur: python3 web_olcum.py kur" % "; ".join(sorun))
        return 3
    with tempfile.TemporaryDirectory() as k:
        temiz = yaz(k, "temiz.html", SAYFA % ("", "#111111", ""))
        bozuk = yaz(k, "bozuk-kontrast.html", SAYFA % ("", "#bbbbbb", ""))   # açık gri / beyaz = 1,91:1 (< 4,5)
        agir = yaz(k, "agir.html", SAYFA % ("", "#111111", "<script>var t=Date.now();while(Date.now()-t<3000){}</script>"))
        # erişim: kontrast
        rc, c = kos(["erisim", bozuk])
        bekle("erisim: kontrastı bozuk sayfa", rc, 1, c, "color-contrast")
        rc, c = kos(["erisim", temiz])
        bekle("erisim: temiz sayfa", rc, 0, c, "GEÇTİ")
        rc, c = kos(["erisim", bozuk, "--json", os.path.join(k, "sonuc.json")])
        j = json.load(open(os.path.join(k, "sonuc.json"), encoding="utf-8"))
        sonuclar.append(j["sonuc"][0]["erisim"]["ihlaller"][0]["kural"] == "color-contrast" and j["sonuc"][0]["etiket"] == "yerel")
        print("%s json: ihlal kuralı color-contrast, etiket yerel" % ("GEÇTİ" if sonuclar[-1] else "KALDI"))
        # hız: ana iş parçacığı kilidi
        rc, c = kos(["hiz", agir, "--kosu", "1"])
        bekle("hiz: ana iş parçacığını 3 sn kilitleyen sayfa", rc, 1, c, "TBT")
        rc, c = kos(["hiz", temiz, "--kosu", "1"])
        bekle("hiz: hafif sayfa", rc, 0, c, "GEÇTİ")
        # araç yok / sürüm sabit değil → ölçülemedi, GEÇTİ değil
        rc, c = kos(["hepsi", temiz], env={"WEB_OLCUM_DIZIN": os.path.join(k, "yok")})
        bekle("araç klasörü yok → ölçülemedi", rc, 3, c, "ÖLÇÜLEMEDİ")
        sahte = os.path.join(k, "sahte")
        for p, v in (("lighthouse", "9.9.9"), ("axe-core", "4.14.0"), ("puppeteer-core", "25.18.1")):
            os.makedirs(os.path.join(sahte, "node_modules", p), exist_ok=True)
            yaz(os.path.join(sahte, "node_modules", p), "package.json", json.dumps({"version": v}))
        rc, c = kos(["kontrol"], env={"WEB_OLCUM_DIZIN": sahte})
        bekle("sürüm sabit değil (lighthouse 9.9.9) → ölçülemedi", rc, 3, c, "sabit sürüm")
    kalan = sonuclar.count(False)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuclar), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
