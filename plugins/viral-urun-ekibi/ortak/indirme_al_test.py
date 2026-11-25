#!/usr/bin/env python3
"""indirme_al.py kırma testi: eski kurucu dosyası alınmaz/taşınmaz; yeni, yeterli büyüklükte, bitmiş dosya alınır."""
import os
import subprocess
import sys
import tempfile
import time

BURASI = os.path.dirname(os.path.abspath(__file__))
SONUC = []


def kos(*a):
    r = subprocess.run([sys.executable, os.path.join(BURASI, "indirme_al.py")] + list(a), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def t(ad, ok, ayrinti=""):
    SONUC.append((ad, ok))
    if not ok:
        print("--- %s\n%s" % (ad, ayrinti))


def yaz(yol, n, mtime=None):
    open(yol, "wb").write(b"x" * n)
    if mtime:
        os.utime(yol, (mtime, mtime))


def main():
    k = tempfile.mkdtemp(prefix="indirme_k_")
    h = os.path.join(tempfile.mkdtemp(prefix="indirme_h_"), "ham")
    eski = os.path.join(k, "galeri-eski.png")
    yaz(eski, 50000, time.time() - 86400)          # dünden kalma kurucu dosyası, ad deseni de uyuyor
    bas = str(time.time())
    rc, o = kos("--kaynak", k, "--hedef", h, "--baslangic", bas, "--ad", "galeri-*.png", "--min-boyut", "1000", "--bekle", "2")
    t("kırma: yalnız ESKİ dosya var -> 1 (yeni dosya yok), eski dosya alınmaz", rc == 1 and not os.path.exists(h), o)
    t("kırma: eski dosya yerinde, boyutu ve zamanı aynı (taşınmadı/değişmedi)", os.path.exists(eski) and os.path.getsize(eski) == 50000 and time.time() - os.path.getmtime(eski) > 80000)
    rc, o = kos("--kaynak", k, "--hedef", h, "--baslangic", bas, "--ad", "galeri-*.png", "--min-boyut", "1000", "--bekle", "2", "--tasi")
    t("kırma: --tasi ile bile eski dosya taşınmaz", rc == 1 and os.path.exists(eski), o)
    yaz(os.path.join(k, "galeri-1.png.crdownload"), 90000)
    yaz(os.path.join(k, "galeri-kucuk.png"), 10)
    rc, o = kos("--kaynak", k, "--hedef", h, "--baslangic", "simdi-5", "--ad", "galeri-*", "--min-boyut", "1000", "--bekle", "2")
    t("kırma: yarım (.crdownload) ve boyutu küçük dosya aday değil -> 1", rc == 1, o)
    os.remove(os.path.join(k, "galeri-1.png.crdownload"))   # indirme bitti
    yeni = os.path.join(k, "galeri-1.png")
    yaz(yeni, 60000)
    rc, o = kos("--kaynak", k, "--hedef", h, "--baslangic", bas, "--ad", "galeri-*.png", "--min-boyut", "1000", "--bekle", "5", "--yeni-ad", "g1.png")
    t("yeni, yeterli büyüklükte dosya -> 0, hedefe KOPYALANDI", rc == 0 and os.path.getsize(os.path.join(h, "g1.png")) == 60000 and os.path.exists(yeni), o)
    t("yeni dosya alınırken eski dosya yine yerinde", os.path.exists(eski) and os.path.getsize(eski) == 50000)
    rc, o = kos("--kaynak", k, "--hedef", h, "--baslangic", bas, "--ad", "galeri-1.png", "--bekle", "3", "--yeni-ad", "g1.png")
    t("hedefte aynı ad varsa üzerine yazılmaz -> 2", rc == 2, o)
    for ad, ok in SONUC:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    kalan = sum(1 for _, ok in SONUC if not ok)
    print("TOPLAM: %d test, %d kaldı" % (len(SONUC), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
