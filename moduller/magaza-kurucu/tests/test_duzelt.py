# -*- coding: utf-8 -*-
"""skills/gorseller/scripts/duzelt.py: sentetik görsellerle (başka mağaza görseli kullanılmaz)."""
import os
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BETIK = os.path.join(KOK, "skills", "gorseller", "scripts", "duzelt.py")
KREM = (240, 236, 228)
HEDEF = "#1F3A5F"


def calistir(*arg, cwd=None):
    return subprocess.run([sys.executable, BETIK] + list(arg), cwd=cwd, capture_output=True,
                          text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))


def gorsel(yol, kutu):
    """Krem zeminde koyu ürün kutusu."""
    im = Image.new("RGB", (600, 600), KREM)
    ImageDraw.Draw(im).rounded_rectangle(kutu, radius=30, fill=(40, 60, 90))
    im.save(yol)


class Zemin(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def test_kenara_degen_urun_red_ve_dosya_yok(self):
        girdi, cikti = os.path.join(self.tmp, "kenar.png"), os.path.join(self.tmp, "out.png")
        gorsel(girdi, (0, 150, 320, 450))          # sol kenara değiyor
        r = calistir("zemin", girdi, cikti, HEDEF)
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("RED", r.stdout)
        self.assertFalse(os.path.exists(cikti), "RED verilen görsel diske yazılmamalı")

    def test_duzgun_gorsel_gecer(self):
        girdi, cikti = os.path.join(self.tmp, "iyi.png"), os.path.join(self.tmp, "out.png")
        gorsel(girdi, (150, 150, 450, 450))        # her kenarda %25 boşluk
        r = calistir("zemin", girdi, cikti, HEDEF)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(cikti))
        hedef = tuple(int(HEDEF[i:i + 2], 16) for i in (1, 3, 5))
        with Image.open(cikti) as im:
            self.assertEqual(im.size, (600, 600))
            for p in [(2, 2), (597, 2), (2, 597), (597, 597)]:
                renk = im.getpixel(p)
                self.assertTrue(all(abs(a - b) <= 3 for a, b in zip(renk, hedef)), (p, renk))
            self.assertEqual(im.getpixel((300, 300)), (40, 60, 90))   # ürün boyanmadı

    def test_kenar_kucultme(self):
        girdi, cikti = os.path.join(self.tmp, "k.png"), os.path.join(self.tmp, "k_out.png")
        gorsel(girdi, (60, 60, 540, 540))
        r = calistir("kenar", girdi, cikti, "0.9")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with Image.open(cikti) as im:
            self.assertEqual(im.size, (600, 600))
            self.assertEqual(im.getpixel((50, 50)), KREM)


class Kullanim(unittest.TestCase):
    def test_argumansiz(self):
        r = calistir()
        self.assertEqual(r.returncode, 2)
        self.assertIn("zemin", r.stderr)

    def test_bilinmeyen_alt_komut(self):
        r = calistir("boya", "a.png", "b.png", "#ffffff")
        self.assertEqual(r.returncode, 2)
        self.assertIn("bilinmiyor", r.stderr)
        self.assertIn("kenar", r.stderr)

    def test_eksik_argument(self):
        r = calistir("zemin", "a.png")
        self.assertEqual(r.returncode, 2)

    def test_gecersiz_renk_ve_oran(self):
        self.assertEqual(calistir("zemin", "a.png", "b.png", "lacivert").returncode, 2)
        self.assertEqual(calistir("kenar", "a.png", "b.png", "yuzde90").returncode, 2)
        self.assertEqual(calistir("kenar", "a.png", "b.png", "1.5").returncode, 2)


if __name__ == "__main__":
    unittest.main()
