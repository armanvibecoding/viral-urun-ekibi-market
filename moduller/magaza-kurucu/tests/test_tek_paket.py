# -*- coding: utf-8 -*-
"""Tek paket (magaza-kurucu.zip): kökte tek SKILL.md, geçerli YAML, router yolları pakette,
aşama dosyaları ASAMA.md (frontmatter'sız), Unix izinleri, LF, boyut. Zip bellekte kurulur."""
import importlib.util
import io
import os
import re
import unittest
import zipfile

import yaml

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("mk_build", os.path.join(KOK, "tools", "build.py"))
build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build)

K = build.TEK_KOK + "/"


def paket(chatgpt):
    return build.zip_bayt(build.tek_girdileri(chatgpt))


class TekPaket(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bayt = {h: paket(h == "chatgpt") for h in ("chatgpt", "claude")}
        cls.zip = {h: zipfile.ZipFile(io.BytesIO(b)) for h, b in cls.bayt.items()}

    def test_kontrol_gecer(self):
        for h, b in self.bayt.items():
            with self.subTest(h):
                hatalar = []
                n, acik, rb = build.kontrol_tek(b, h == "chatgpt", hatalar)
                self.assertEqual(hatalar, [])
                self.assertGreater(n, 40)
                self.assertLessEqual(rb, build.SKILL_MAX_BAYT)

    def test_kokte_tek_skill_md(self):
        for h, z in self.zip.items():
            with self.subTest(h):
                skill = [n for n in z.namelist() if n.endswith("SKILL.md")]
                self.assertEqual(skill, [K + "SKILL.md"])
                self.assertTrue(all(n.startswith(K) for n in z.namelist()))

    def test_router_yaml(self):
        metin = self.zip["chatgpt"].read(K + "SKILL.md").decode("utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", metin, re.S)
        self.assertIsNotNone(m)
        fm = yaml.safe_load(m.group(1))
        self.assertEqual(fm["name"], "magaza-kurucu")
        self.assertIsInstance(fm["description"], str)
        self.assertLessEqual(len(fm["description"]), build.DESC_MAX)
        self.assertIn("mağaza kur", fm["description"].lower())

    def test_asama_dosyalari(self):
        z = self.zip["chatgpt"]
        for ad in build.SKILLER:
            with self.subTest(ad):
                m = z.read("%s%s/ASAMA.md" % (K, ad)).decode("utf-8")
                self.assertFalse(m.startswith("---"))
                kaynak = open(os.path.join(KOK, "skills", ad, "SKILL.md"), encoding="utf-8").read()
                self.assertTrue(kaynak.endswith(m), "ASAMA.md gövdesi SKILL.md gövdesiyle aynı olmalı")
                self.assertIn("%s%s/references/01-kurallar.md" % (K, ad), z.namelist())

    def test_router_yollari_pakette(self):
        z = self.zip["chatgpt"]
        adlar = z.namelist()
        yollar = build.router_yollari(z.read(K + "SKILL.md").decode("utf-8"))
        self.assertTrue(yollar)
        for t in yollar:
            t2 = t.rstrip("/")
            with self.subTest(t):
                self.assertTrue(K + t2 in adlar or any(n.startswith(K + t2 + "/") for n in adlar))

    def test_betikler_ve_varliklar(self):
        adlar = self.zip["chatgpt"].namelist()
        for p in ("shopify-kurulum/scripts/t4_yama.py", "shopify-kurulum/scripts/ayar-sozlugu.json",
                  "gorseller/scripts/duzelt.py", "gorseller/scripts/sablon.py",
                  "gorseller/assets/fonts/Anton-Regular.ttf", "shopify-kurulum/references/tema.json"):
            self.assertIn(K + p, adlar)
        self.assertFalse(any("__pycache__" in n or n.endswith(".pyc") for n in adlar))

    def test_agents_yalniz_chatgpt(self):
        self.assertIn(K + "agents/openai.yaml", self.zip["chatgpt"].namelist())
        y = yaml.safe_load(self.zip["chatgpt"].read(K + "agents/openai.yaml").decode("utf-8"))
        self.assertEqual(y["interface"]["display_name"], "Mağaza Kurucu")
        self.assertFalse(any(n.startswith(K + "agents/") for n in self.zip["claude"].namelist()))

    def test_unix_izinleri(self):
        for i in self.zip["chatgpt"].infolist():
            self.assertEqual(i.create_system, 3, i.filename)
            self.assertEqual((i.external_attr >> 16) & 0o777, 0o755 if i.is_dir() else 0o644, i.filename)

    def test_lf_ve_boyut(self):
        z = self.zip["chatgpt"]
        for n in z.namelist():
            if n.endswith(build.METIN_UZANTI):
                self.assertNotIn(b"\r", z.read(n), n)
        self.assertLess(len(self.bayt["chatgpt"]), build.TEK_MAX_BAYT)

    def test_bozuk_paket_yakalanir(self):
        # iç içe SKILL.md ve eksik aşama dosyası hata vermeli
        g = [(b, a.replace("marka/ASAMA.md", "marka/SKILL.md")) for b, a in build.tek_girdileri(True)]
        hatalar = []
        build.kontrol_tek(build.zip_bayt(g), True, hatalar)
        self.assertTrue(any("SKILL.md" in h for h in hatalar), hatalar)
        self.assertTrue(any("marka/ASAMA.md" in h for h in hatalar), hatalar)

    def test_kaynak_lf(self):
        for f in ("src/tek/SKILL.md", "src/tek/agents/openai.yaml"):
            with open(os.path.join(KOK, f), "rb") as h:
                self.assertNotIn(b"\r", h.read(), f)


if __name__ == "__main__":
    unittest.main()
