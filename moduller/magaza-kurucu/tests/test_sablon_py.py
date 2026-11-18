# -*- coding: utf-8 -*-
"""scripts/sablon.py --demo, skill dışındaki bir çalışma klasöründen çalışıyor mu (font yolu skill içi göreli)."""
import os
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(KOK, "skills", "gorseller", "scripts", "sablon.py")


def sentetik_urun(yol):
    """Beyaz zeminde koyu mavi kupa benzeri sentetik ürün (başka mağaza görseli kullanılmaz)."""
    im = Image.new("RGB", (800, 800), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((220, 200, 520, 640), radius=40, fill=(28, 52, 110))
    d.ellipse((470, 320, 640, 520), outline=(28, 52, 110), width=36)
    d.rectangle((300, 300, 440, 360), fill=(200, 160, 60))
    im.save(yol)


class SablonDemo(unittest.TestCase):
    def test_demo_calisir(self):
        with tempfile.TemporaryDirectory() as tmp:
            urun = os.path.join(tmp, "urun.png")
            sentetik_urun(urun)
            env = dict(os.environ)
            env.pop("MK_FONT_DIR", None)
            r = subprocess.run([sys.executable, SCRIPT, "--demo", "--urun", urun, "--outdir", "cikti"],
                               cwd=tmp, env=env, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            pngler = sorted(f for f in os.listdir(os.path.join(tmp, "cikti")) if f.endswith(".png"))
            self.assertEqual(len(pngler), 10, pngler)
            for f in pngler:
                with Image.open(os.path.join(tmp, "cikti", f)) as im:
                    self.assertEqual(im.size, (1080, 1080), f)
            self.assertTrue(os.path.exists(os.path.join(tmp, "cikti", "_olcum.json")))

    def test_fontlar_skill_icinde(self):
        fdir = os.path.join(KOK, "skills", "gorseller", "assets", "fonts")
        for f in ("Anton-Regular.ttf", "Barlow-Bold.ttf", "Barlow-SemiBold.ttf", "Barlow-Medium.ttf",
                  "OFL-Anton.txt", "OFL-Barlow.txt"):
            self.assertTrue(os.path.exists(os.path.join(fdir, f)), f)


if __name__ == "__main__":
    unittest.main()
