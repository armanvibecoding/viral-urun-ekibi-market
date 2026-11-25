#!/usr/bin/env python3
"""mobil_ekran.py Chrome yolu bulma (Windows yolları) kırma testi. Çıkış 0 = hepsi geçti."""
import os
import sys
import tempfile
from unittest import mock

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
import mobil_ekran  # noqa: E402

sonuc = []


def t(ad, ok, ayrinti=""):
    sonuc.append(bool(ok))
    print(("GEÇTİ " if ok else "KALDI ") + ad + ("" if ok else " | " + str(ayrinti)))


with tempfile.TemporaryDirectory() as d:
    uyd = os.path.join(d, "PF", "Google", "Chrome", "Application")
    os.makedirs(uyd)
    exe = os.path.join(uyd, "chrome.exe")
    bos = {k: "" for k in ("CHROME_YOLU", "ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")}
    with mock.patch.dict(os.environ, bos), mock.patch("shutil.which", return_value=None), \
            mock.patch("os.path.exists", side_effect=lambda p: p == exe):
        t("KIRMA Windows Chrome dosyası yok -> None (uydurma yol yok)", mobil_ekran.chrome() is None)
    open(exe, "w").close()
    with mock.patch.dict(os.environ, dict(bos, ProgramFiles=os.path.join(d, "PF"))), mock.patch("shutil.which", return_value=None), \
            mock.patch("os.path.exists", side_effect=lambda p: p == exe):
        t("ProgramFiles altındaki chrome.exe bulunur", mobil_ekran.chrome() == exe, mobil_ekran.chrome())
    with mock.patch.dict(os.environ, dict(bos, CHROME_YOLU=exe)), mock.patch("shutil.which", return_value=None):
        t("CHROME_YOLU yine önce gelir", mobil_ekran.chrome() == exe)
kalan = sonuc.count(False)
print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
sys.exit(1 if kalan else 0)
