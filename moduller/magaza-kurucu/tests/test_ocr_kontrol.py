# -*- coding: utf-8 -*-
"""skills/gorseller/scripts/ocr_kontrol.py: sentetik kartta doğru metin geçer, tek harfi farklı beklenti (İ ↔ I) ❌ verir.
RapidOCR yoksa atlanır (geliştirme aracı; pakete girmez)."""
import os
import subprocess
import sys
import tempfile

import pytest

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(KOK, "skills", "gorseller", "assets", "fonts", "Barlow-SemiBold.ttf")

rapidocr = pytest.importorskip("rapidocr_onnxruntime")


def kart(yol):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (1080, 1080), "#1E2226")
    d = ImageDraw.Draw(im)
    buyuk = ImageFont.truetype(FONT, 120)
    kucuk = ImageFont.truetype(FONT, 44)
    d.text((80, 160), "İNCE GÖVDE", font=buyuk, fill="#F2F2EE")
    d.text((80, 300), "TEK DÜĞME", font=buyuk, fill="#F2F2EE")
    d.text((80, 900), "120 MM · 30 G · USB ŞARJ", font=kucuk, fill="#A9ADB2")
    im.save(yol)


def calistir(gorsel, beklenen):
    r = subprocess.run([sys.executable, os.path.join(KOK, "skills", "gorseller", "scripts", "ocr_kontrol.py"), gorsel, beklenen, "--dil", "tr"],
                       capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, r.stdout


def test_dogru_metin_gecer_ve_harf_hatasi_yakalanir():
    with tempfile.TemporaryDirectory() as t:
        g = os.path.join(t, "kart.png")
        kart(g)
        kod, cikti = calistir(g, "İNCE GÖVDE|TEK DÜĞME|120 MM|30 G|USB ŞARJ")
        assert kod == 0, cikti
        kod, cikti = calistir(g, "INCE GÖVDE|TEK DÜĞME|120 MM|30 G|USB ŞARJ")  # İ yerine I
        assert kod == 1, cikti
