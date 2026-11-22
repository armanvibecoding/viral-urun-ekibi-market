# -*- coding: utf-8 -*-
"""Birleşik eklenti: üretilen beceri kaynakla aynı (kırılarak sınanır), tek lider, ekip kalıbı (unvan + ad + rol), köprü dosyası."""
import glob
import importlib.util
import os
import re
import unittest

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPO = os.path.dirname(os.path.dirname(KOK))
EKLENTI = os.path.join(DEPO, "plugins", "viral-urun-ekibi")
_spec = importlib.util.spec_from_file_location("mk_build2", os.path.join(KOK, "tools", "build.py"))
build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build)


def oku(*p):
    with open(os.path.join(*p), encoding="utf-8") as f:
        return f.read()


class BirlesikBeceri(unittest.TestCase):
    def test_kaynakla_ayni(self):
        hatalar = []
        n = build.kontrol_birlesik(hatalar)
        self.assertEqual(hatalar, [])
        self.assertGreater(n, 60)

    def test_kapi_kirilinca_yakalar(self):
        """Elle düzenleme, eksik dosya ve fazla dosya üçü de hata vermeli (kapı ölçüyor mu?)."""
        gercek = build.birlesik_mevcut()
        for ad, bozuk in (("FARKLI", dict(gercek, **{"SKILL.md": gercek["SKILL.md"] + b"\n"})),
                          ("EKSİK", {k: v for k, v in gercek.items() if k != "urun-analiz/ASAMA.md"}),
                          ("FAZLA", dict(gercek, **{"elle-eklenen.md": b"x"}))):
            eski = build.birlesik_mevcut
            build.birlesik_mevcut = lambda b=bozuk: b
            try:
                hatalar = []
                build.kontrol_birlesik(hatalar)
            finally:
                build.birlesik_mevcut = eski
            self.assertTrue(any(h.startswith("BİRLEŞİK " + ad) for h in hatalar), (ad, hatalar))

    def test_icinde_ic_ice_skill_yok(self):
        ic = [p for p in glob.glob(os.path.join(build.BIRLESIK, "**", "SKILL.md"), recursive=True)
              if os.path.dirname(p) != build.BIRLESIK]
        self.assertEqual(ic, [])

    def test_claude_degiskeni_yok(self):
        """Beceri ChatGPT paketine dönüştürülmeden girer: içinde ${CLAUDE_...} olmamalı."""
        for p in glob.glob(os.path.join(build.BIRLESIK, "**", "*.md"), recursive=True):
            self.assertNotIn("${CLAUDE_", oku(p), p)


class TekLider(unittest.TestCase):
    def test_siralayici_lideri_gosterir(self):
        t = oku(KOK, "src", "tek", "SKILL.md")
        self.assertIn("tek lideri `captain`", t)
        self.assertNotIn("yönlendirici)", t.split("\n")[5] if len(t.split("\n")) > 5 else "")

    def test_lider_magaza_isini_tasir(self):
        t = oku(EKLENTI, "skills", "captain", "SKILL.md")
        for parca in ("`builder`", "urun-yaz", "magaza-oku", "video-yaz", "temasız mod", "tek lideri sensin"):
            self.assertIn(parca, t, parca)

    def test_ikinci_lider_yok(self):
        """'Ekibi başlat / nerede kalmıştık' tetiği yalnız liderde; başka beceri kendini lider diye tanıtmaz."""
        for p in glob.glob(os.path.join(EKLENTI, "skills", "*", "SKILL.md")):
            ad = os.path.basename(os.path.dirname(p))
            if ad == "captain":
                continue
            bas = oku(p).split("---")[1]
            self.assertNotIn("Ekibi başlat", bas, ad)
            self.assertNotIn("nerede kalmıştık", bas, ad)


class EkipKalibi(unittest.TestCase):
    KALIP = re.compile(r"^description: ([A-Z][A-Za-z&() ]+) \(([A-ZÇĞİÖŞÜ][a-zçğıöşü]+) · ([^)]+)\)\. ", re.M)

    def test_her_ajan_unvan_ad_rol(self):
        kadro = oku(EKLENTI, "ortak", "ekip.md")
        adlar, unvanlar = [], []
        ajanlar = sorted(glob.glob(os.path.join(EKLENTI, "agents", "*.md")))
        self.assertEqual(len(ajanlar), 27)
        for p in ajanlar:
            t = oku(p)
            m = self.KALIP.search(t)
            self.assertIsNotNone(m, os.path.basename(p))
            unvan, ad = m.group(1), m.group(2)
            adlar.append(ad)
            unvanlar.append(unvan)
            self.assertIn("%s (%s)" % (unvan, ad), kadro, os.path.basename(p))
            self.assertIn("`%s`" % os.path.basename(p)[:-3], kadro)
            model = re.search(r"^model: (\w+)$", t, re.M)
            self.assertIsNotNone(model, os.path.basename(p))
            self.assertIn("| %s |" % model.group(1), [l for l in kadro.split("\n") if l.lstrip().startswith("|") and "`%s`" % os.path.basename(p)[:-3] in l][0])
        self.assertEqual(len(set(adlar)), len(adlar), "ad çakışması")
        self.assertEqual(len(set(unvanlar)), len(unvanlar), "unvan çakışması")

    def test_magaza_kolu_isareti(self):
        isaretli = [p for p in glob.glob(os.path.join(EKLENTI, "agents", "*.md")) if "<!-- kol: magaza -->" in oku(p)]
        self.assertEqual(len(isaretli), 20)

    def test_kisisel_iz_yok(self):
        for p in glob.glob(os.path.join(EKLENTI, "agents", "*.md")) + glob.glob(os.path.join(DEPO, ".claude", "agents", "*.md")):
            t = oku(p)
            for iz in ("C:\\", "research/", "anışman"):
                self.assertNotIn(iz, t, (os.path.basename(p), iz))


class Kopru(unittest.TestCase):
    def test_kopru_dosyasi_uc_asamada(self):
        for asama in ("urun-analiz", "metinler", "shopify-kurulum"):
            self.assertIn("references/ekip-koprusu.md", oku(KOK, "skills", asama, "SKILL.md"), asama)
        t = oku(KOK, "src", "ortak", "ekip-koprusu.md")
        for parca in ("Temasız mod", "`teklif.kaynak` = `teklif.tsv`", "2'li %10, 3'lü %18", "dogrula magaza", "video-sec"):
            self.assertIn(parca, t, parca)

    def test_sozlesme_testi_gecer(self):
        import subprocess
        import sys
        r = subprocess.run([sys.executable, os.path.join(DEPO, "scripts", "sozlesme_test.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-800:])


if __name__ == "__main__":
    unittest.main()
