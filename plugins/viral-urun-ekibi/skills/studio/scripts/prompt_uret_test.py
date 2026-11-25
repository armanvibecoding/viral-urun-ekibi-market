#!/usr/bin/env python3
"""prompt_uret.py panoya() yedek yolu kırma testi (ağsız). Çıkış 0 = hepsi geçti."""
import os
import sys
import tempfile
from unittest import mock

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
import prompt_uret  # noqa: E402

sonuc = []


def t(ad, ok, ayrinti=""):
    sonuc.append(bool(ok))
    print(("GEÇTİ " if ok else "KALDI ") + ad + ("" if ok else " | " + str(ayrinti)))


with tempfile.TemporaryDirectory() as d:
    eski = os.getcwd()
    os.chdir(d)
    try:
        with mock.patch.object(prompt_uret, "pano_komutu", return_value=None):
            m = prompt_uret.panoya("deneme metni ğüşiöç")
        t("pano aracı yok -> dosya yedeği yazılır", os.path.isfile("prompt-pano.txt") and "prompt-pano.txt" in m, m)
        with open("prompt-pano.txt", encoding="utf-8") as f:
            t("dosya yedeği metni aynen taşır (UTF-8)", f.read() == "deneme metni ğüşiöç")
        os.remove("prompt-pano.txt")
        with mock.patch.object(prompt_uret, "pano_komutu", return_value=["bu-komut-yok-9z"]):
            m = prompt_uret.panoya("x")
        t("KIRMA pano aracı çalışmıyorsa (OSError) dosya yedeğine düşer, çökmez", os.path.isfile("prompt-pano.txt"), m)
        with mock.patch.object(prompt_uret, "pano_komutu", return_value=[sys.executable, "-c", "import sys; sys.stdin.read()"]):
            m = prompt_uret.panoya("y")
        t("pano aracı çalışıyorsa 'panoya kopyalandı'", m == "panoya kopyalandı", m)
    finally:
        os.chdir(eski)
kalan = sonuc.count(False)
print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
sys.exit(1 if kalan else 0)
