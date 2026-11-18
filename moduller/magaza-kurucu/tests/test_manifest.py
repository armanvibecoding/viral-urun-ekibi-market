# -*- coding: utf-8 -*-
"""Modül tutarlılığı: JSON geçerli, sürüm her yerde aynı (surum.json, README, birleşik eklenti README), lisans MIT, tema zip kaydı,
modülde ikinci eklenti manifesti yok (tek eklenti: plugins/viral-urun-ekibi)."""
import glob
import hashlib
import json
import os
import re
import unittest

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPO = os.path.dirname(os.path.dirname(KOK))
EKLENTI = os.path.join(DEPO, "plugins", "viral-urun-ekibi")
MANIFESTLER = ["surum.json"]
JSONLAR = MANIFESTLER + ["config/tema.json", "skills/shopify-kurulum/scripts/ayar-sozlugu.json"]
SURUM_RE = re.compile(r"^\d+\.\d+\.\d+$")


def oku(yol):
    with open(os.path.join(KOK, yol), encoding="utf-8") as f:
        return f.read()


def js(yol):
    return json.loads(oku(yol))


def manifest_surumu():
    return js("surum.json")["version"]


class JsonGecerli(unittest.TestCase):
    def test_hepsi_ayristirilir(self):
        for j in JSONLAR:
            with self.subTest(j):
                js(j)

    def test_skill_json_dosyalari(self):
        for f in glob.glob(os.path.join(KOK, "skills", "*", "**", "*.json"), recursive=True):
            with self.subTest(os.path.relpath(f, KOK)):
                with open(f, encoding="utf-8") as h:
                    json.load(h)


class Surum(unittest.TestCase):
    def test_manifest_surumleri_ayni_ve_semver(self):
        s = manifest_surumu()
        self.assertRegex(s, SURUM_RE)
        for m in MANIFESTLER:
            self.assertEqual(js(m)["version"], s, m)

    def test_tek_eklenti(self):
        """Modül ikinci bir eklenti/pazar yeri taşımaz; Shopify MCP kaydı birleşik eklentidedir."""
        for yasak in (".claude-plugin", ".codex-plugin", ".agents", "plugin.json", ".mcp.json"):
            self.assertFalse(os.path.exists(os.path.join(KOK, yasak)), yasak)
        with open(os.path.join(EKLENTI, ".mcp.json"), encoding="utf-8") as f:
            self.assertIn("shopify", json.load(f)["mcpServers"])
        with open(os.path.join(DEPO, ".claude-plugin", "marketplace.json"), encoding="utf-8") as f:
            self.assertEqual([p["name"] for p in json.load(f)["plugins"]], ["viral-urun-ekibi"])

    def test_readme_surumu(self):
        s = manifest_surumu()
        metin = oku("README.md")
        m = re.search(r"[Ss]ürüm (\d+\.\d+\.\d+)", metin)
        self.assertIsNotNone(m, "README.md'de 'sürüm X.Y.Z' yok")
        self.assertEqual(m.group(1), s)
        for z in re.findall(r"magaza-kurucu-plugin-(\d+\.\d+\.\d+)\.zip", metin):
            self.assertEqual(z, s)


class Lisans(unittest.TestCase):
    def test_mit(self):
        with open(os.path.join(DEPO, "LICENSE"), encoding="utf-8") as f:
            self.assertTrue(f.read().startswith("MIT License"))
        with open(os.path.join(EKLENTI, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f).get("license"), "MIT")


class Tema(unittest.TestCase):
    def test_tema_kaydi(self):
        t = js("config/tema.json")
        self.assertRegex(t["dosya_adi"], r"^Ana-Tema-temiz-\d{4}-\d{2}-\d{2}\.zip$")
        self.assertIn(t["surum"], t["dosya_adi"])
        self.assertRegex(t["sha256"], r"^[0-9a-f]{64}$")
        self.assertGreater(t["boyut_bayt"], 0)
        with open(os.path.join(EKLENTI, "README.md"), encoding="utf-8") as f:
            self.assertIn("temasız mod", f.read().lower().replace("i̇", "i"), "eklenti README'si temasız modu anlatmıyor")

    def test_tema_kopyasi_ayni(self):
        self.assertEqual(oku("config/tema.json"), oku("skills/shopify-kurulum/references/tema.json"))

    def test_zip_varsa_sha256_tutar(self):
        t = js("config/tema.json")
        aday = os.environ.get("MK_TEMA_ZIP", "")
        yol = aday if aday and os.path.isfile(aday) else None
        if not yol:
            self.skipTest("tema zip'i bu makinede yok (MK_TEMA_ZIP ile verilebilir)")
        with open(yol, "rb") as f:
            veri = f.read()
        self.assertEqual(len(veri), t["boyut_bayt"])
        self.assertEqual(hashlib.sha256(veri).hexdigest(), t["sha256"])


if __name__ == "__main__":
    unittest.main()
