#!/usr/bin/env python3
"""KAÇAK kırma testi (denetim 2026-11-25 #12): 24–25 Kasım gecesi kapıların kaçırıp lider gözünün yakaladığı 4 kusur, yeni kapılar
tarafından ESKİ çıktılarda yakalanmalı (KALDI), iyi çıktıda GEÇTİ vermeli. Eski çıktılar <referans-kok>/sinav-kosu/ altındadır.

  python3 scripts/kacak_kirma_test.py --referans-kok <referans-kok>      (ya da ortam değişkeni SINAV_REFERANS_KOK)
  (a) 01 tur2/b-zor  yanlış ürün klibi        kurgu_kontrol [malzeme]    ↔ iyi: 01 tur3/b-zor (gerçek tedarikçi klibi) GEÇTİ
  (b) 01 tur3/a-kolay ilk 2 sn durağan         kurgu_kontrol [ilk2sn]     ↔ iyi: 01 tur3/b-zor GEÇTİ
  (c) 07 tur1 b-zor + c-tuzak kanıt anı sızıntısı  sinav_kos kanit_ani_sizinti ↔ iyi: aynı metin iç terimler silinince GEÇTİ
  (d) 07 tur1 mobil ekran taşması/yöntem hatası   mobil_ekran.py kontrol  ↔ iyi: mobil_ekran.py ekran ile yeniden alınan ekran GEÇTİ
Çıkış: 0 hepsi beklenen gibi · 1 en az bir kapı kaçağı yakalamadı ya da iyi çıktıyı reddetti · 3 referans kökü/araç yok (ölçülemedi; geçti sayılmaz).
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EKL = os.path.join(KOK, "plugins", "viral-urun-ekibi")
KURGU = os.path.join(EKL, "skills", "cut", "scripts", "kurgu_kontrol.py")
MOBIL = os.path.join(EKL, "ortak", "mobil_ekran.py")
SINAV_KOS = os.path.join(KOK, "scripts", "sinav_kos.py")
SONUC, OLCULEMEDI = [], []


def kos(*cmd):
    r = subprocess.run([sys.executable] + [str(c) for c in cmd], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def t(ad, ok, ayrinti=""):
    SONUC.append((ad, ok))
    if not ok:
        print("--- %s\n%s" % (ad, str(ayrinti)[-500:]))


def kurgu(vaka_dizin):
    return kos(KURGU, os.path.join(vaka_dizin, "ayar.json"), "--video", os.path.join(vaka_dizin, "video.mp4"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--referans-kok", default=os.environ.get("SINAV_REFERANS_KOK"))
    a = ap.parse_args()
    if not a.referans_kok or not os.path.isdir(os.path.join(a.referans_kok, "sinav-kosu")):
        print("OLCULEMEDI: referans kökü yok (--referans-kok ya da SINAV_REFERANS_KOK; <kök>/sinav-kosu/ gerekir). Kaçak testi koşulamadı, geçti sayılmaz.")
        return 3
    S = os.path.join(a.referans_kok, "sinav-kosu")
    v1 = os.path.join(S, "01-urun-videosu")
    # (a) + (b): ffmpeg gerekir
    try:
        sys.path.insert(0, os.path.join(EKL, "skills", "cut", "scripts"))
        import ffaraclar as F
        F.ffmpeg_bul()
        ffmpeg_var = True
    except SystemExit:
        ffmpeg_var = False
    if not ffmpeg_var:
        OLCULEMEDI.append("(a)(b) ffmpeg yok")
    else:
        rc, o = kurgu(os.path.join(v1, "tur2", "b-zor"))
        t("(a) 01 tur2/b-zor yanlış ürün klibi -> kurgu_kontrol KALDI [malzeme]", rc == 1 and "[malzeme]" in o, o)
        rc, o = kurgu(os.path.join(v1, "tur3", "b-zor"))
        t("(a)(b) iyi çıktı 01 tur3/b-zor -> kurgu_kontrol GEÇTİ", rc == 0, o)
        rc, o = kurgu(os.path.join(v1, "tur3", "a-kolay"))
        t("(b) 01 tur3/a-kolay ilk 2 sn durağan -> kurgu_kontrol KALDI [ilk2sn]", rc == 1 and "[ilk2sn]" in o, o)
    # (c) site metni
    v7 = os.path.join(S, "07-site", "tur1")
    for vaka in ("b-zor", "c-tuzak"):
        rc, o = kos(SINAV_KOS, "07", v7, "--vaka", vaka, "--sonuc", os.path.join(tempfile.mkdtemp(), "S.md"))
        t("(c) 07 tur1 %s kanıt anı/iç dil sızıntısı -> kanit_ani_sizinti KALDI" % vaka, re.search(r"kanit_ani_sizinti\s+KALDI", o) is not None, o)
        with tempfile.TemporaryDirectory(prefix="kacak_c_") as m:
            shutil.copytree(os.path.join(v7, vaka), os.path.join(m, vaka))
            for md in glob.glob(os.path.join(m, vaka, "site", "*.md")):
                x = open(md, encoding="utf-8").read()
                x = re.sub(r"(?im)^#+\s*(der moment|the moment|kanıt)\s*$", "## Im Alltag", x)
                x = re.sub(r"Kanıt, sayfanın kendisidir\.", "Sayfaya bakarsın, tüy orada.", x)
                open(md, "w", encoding="utf-8").write(x)
            rc, o = kos(SINAV_KOS, "07", m, "--vaka", vaka, "--sonuc", os.path.join(m, "S.md"))
            t("(c) iyi: %s metni iç terimler silinince kanit_ani_sizinti GEÇTİ" % vaka, "kanit_ani_sizinti" not in o, o)
    # (d) mobil ekran
    ciftler = [(h, os.path.splitext(h)[0] + "-390.png") for h in sorted(glob.glob(os.path.join(v7, "*", "ekran", "*.html")))]
    ciftler = [(h, p) for h, p in ciftler if os.path.isfile(p)]
    kontrol_rc = [kos(MOBIL, "kontrol", h, p)[0] for h, p in ciftler]
    if 2 in kontrol_rc or not ciftler:
        OLCULEMEDI.append("(d) Chrome yok ya da ekran çifti yok")
    else:
        t("(d) 07 tur1: %d eski mobil ekranın hepsi KALDI (yöntem hatası/taşma)" % len(ciftler), all(r == 1 for r in kontrol_rc), kontrol_rc)
        h, _ = ciftler[0]
        with tempfile.TemporaryDirectory(prefix="kacak_d_") as m:
            yeni = os.path.join(m, "yeni-390.png")
            kos(MOBIL, "ekran", h, yeni)
            rc, o = kos(MOBIL, "kontrol", h, yeni)
            t("(d) iyi: geniş pencere + 390 px iframe ile yeniden alınan ekran GEÇTİ", rc == 0, o)
    for ad, ok in SONUC:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    for x in OLCULEMEDI:
        print("OLCULEMEDI " + x)
    kalan = sum(1 for _, ok in SONUC if not ok)
    print("TOPLAM: %d test, %d kaldı, %d ölçülemedi" % (len(SONUC), kalan, len(OLCULEMEDI)))
    return 1 if kalan else (3 if OLCULEMEDI else 0)


if __name__ == "__main__":
    sys.exit(main())
