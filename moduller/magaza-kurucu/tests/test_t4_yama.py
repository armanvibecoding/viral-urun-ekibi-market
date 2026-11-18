# -*- coding: utf-8 -*-
"""skills/shopify-kurulum/scripts/t4_yama.py: gerçek Ana Tema şablonlarıyla (kopyaları üzerinde).

Tema deposu (MK_TEMA_KOK ortam değişkeni; yoksa ev klasöründe ana-tema) yoksa tema gerektiren testler atlanır.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BETIK = os.path.join(KOK, "skills", "shopify-kurulum", "scripts", "t4_yama.py")
SOZLUK = os.path.join(KOK, "skills", "shopify-kurulum", "scripts", "ayar-sozlugu.json")
TEMA_KOK = os.environ.get("MK_TEMA_KOK") or os.path.join(os.path.expanduser("~"), "ana-tema")
TEMA = os.path.join(TEMA_KOK, "theme")
TEMA_VAR = os.path.isfile(os.path.join(TEMA, "templates", "index.json"))

_spec = importlib.util.spec_from_file_location("t4_yama", BETIK)
T = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T)


def calistir(*arg, cwd=None):
    return subprocess.run([sys.executable, BETIK] + list(arg), cwd=cwd, capture_output=True,
                          text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))


@unittest.skipUnless(TEMA_VAR, "tema deposu yok: %s" % TEMA)
class GercekSablon(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for ad in ("index.json", "product.nis-saglik.json", "page.faq.json"):
            shutil.copy(os.path.join(TEMA, "templates", ad), os.path.join(self.tmp, ad))
        shutil.copy(os.path.join(TEMA, "config", "settings_data.json"), os.path.join(self.tmp, "settings_data.json"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def p(self, ad):
        return os.path.join(self.tmp, ad)

    def yama(self, veri, ad="yama.json"):
        with open(self.p(ad), "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False)
        return self.p(ad)

    def yamala(self, sablon, veri, *ek):
        cikti = self.p("cikti.json")
        if os.path.exists(cikti):
            os.remove(cikti)
        r = calistir("--sablon", self.p(sablon), "--yama", self.yama(veri), "--cikti", cikti, *ek)
        return r, cikti

    # ---------------------------------------------------------- geçen yamalar
    def test_index_gecerli_yama(self):
        veri = [{"yol": "e-serit/c1/i.icon", "deger": "truck"},
                {"yol": "e-kars.disabled", "deger": False},
                {"yol": "e-hero-b/sol/baslik.text", "deger": "<p>Gece boyu rahat nefes</p>"}]
        r, cikti = self.yamala("index.json", veri)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("GEÇTİ", r.stdout)
        self.assertIn("12 bölüm", r.stdout)
        metin = open(cikti, encoding="utf-8").read()
        yeni = json.loads(metin)
        self.assertEqual(metin, json.dumps(yeni, ensure_ascii=False, separators=(",", ":")), "sıkıştırılmış değil")
        self.assertFalse(metin.startswith("/*"))
        taban = T.oku_dosya(self.p("index.json"))
        self.assertEqual(T.harita(yeni), T.harita(taban))
        self.assertEqual(yeni["sections"]["e-serit"]["blocks"]["c1"]["blocks"]["i"]["settings"]["icon"], "truck")
        # yalnız istenen yerler değişti
        taban["sections"]["e-serit"]["blocks"]["c1"]["blocks"]["i"]["settings"]["icon"] = "truck"
        taban["sections"]["e-kars"].pop("disabled", None)
        taban["sections"]["e-hero-b"]["blocks"]["sol"]["blocks"]["baslik"]["settings"]["text"] = "<p>Gece boyu rahat nefes</p>"
        self.assertEqual(yeni, taban)

    def test_urun_sablonu_ic_ice_blok(self):
        veri = {"degisiklikler": [["main/product-details/title.alignment", "center"],
                                  ["e-serit/c2/i.icon", "return"],
                                  ["n-pc/bas/h.text", "<h2>Horlama neden olur?</h2>"]]}
        r, cikti = self.yamala("product.nis-saglik.json", veri)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        yeni = json.loads(open(cikti, encoding="utf-8").read())
        self.assertEqual(T.harita(yeni), T.harita(T.oku_dosya(self.p("product.nis-saglik.json"))))
        self.assertEqual(len(yeni["order"]), 15)

    def test_eksik_okuma_boyut_ve_bolum_sayisi(self):
        veri = [{"yol": "e-serit/c1/i.icon", "deger": "truck"}]
        boyut = os.path.getsize(self.p("index.json"))
        r, _ = self.yamala("index.json", veri, "--boyut", str(boyut), "--bolum-sayisi", "12")
        self.assertEqual(r.returncode, 0, r.stdout)
        r, cikti = self.yamala("index.json", veri, "--boyut", str(boyut + 500))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("okuma eksik", r.stdout)
        self.assertFalse(os.path.exists(cikti))
        r, cikti = self.yamala("index.json", veri, "--bolum-sayisi", "13")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertFalse(os.path.exists(cikti))

    def test_kontrol_sunucu_okumasi(self):
        veri = [{"yol": "e-serit/c1/i.icon", "deger": "truck"}]
        r, cikti = self.yamala("index.json", veri)
        self.assertEqual(r.returncode, 0, r.stdout)
        r = calistir("--kontrol", cikti, "--taban", self.p("index.json"), "--yama", self.p("yama.json"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("BİREBİR AYNI", r.stdout)
        # sunucudaki dosyada bölüm kaybı (ölçülmüş hata: 12 bölümden 4'ü kaldı)
        yeni = json.loads(open(cikti, encoding="utf-8").read())
        for k in list(yeni["order"])[4:]:
            yeni["sections"].pop(k)
        yeni["order"] = yeni["order"][:4]
        with open(self.p("kisalmis.json"), "w", encoding="utf-8") as f:
            json.dump(yeni, f)
        r = calistir("--kontrol", self.p("kisalmis.json"), "--taban", self.p("index.json"), "--yama", self.p("yama.json"))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("YAZMA", r.stdout)

    def test_faq_blok_ekleme_haric(self):
        veri = {"haric": ["faq"],
                "bloklar": [{"bolum": "faq", "id": "q_yeni", "type": "question", "sonra": "q_teslim",
                             "settings": {"question": "Kutuda ne var?", "answer": "<p>Cihaz ve kılıf.</p>"}}],
                "degisiklikler": [{"yol": "faq.heading", "deger": "Sık sorulanlar"}]}
        r, cikti = self.yamala("page.faq.json", veri)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        yeni = json.loads(open(cikti, encoding="utf-8").read())
        sira = yeni["sections"]["faq"]["block_order"]
        self.assertEqual(sira[sira.index("q_teslim") + 1], "q_yeni")
        # haric yoksa blok eklenemez
        veri.pop("haric")
        r, cikti = self.yamala("page.faq.json", veri)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertFalse(os.path.exists(cikti))

    def test_settings_data(self):
        r, cikti = self.yamala("settings_data.json", [{"yol": "badge_position", "deger": "top-left"}])
        if r.returncode != 0 and "seçeneklerde yok" in r.stdout:
            self.skipTest("badge_position seçenekleri farklı")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        r, cikti = self.yamala("settings_data.json", [{"yol": "olmayan_genel_ayar", "deger": 1}])
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertFalse(os.path.exists(cikti))

    # ---------------------------------------------------------- durdurulan yamalar (çıktı YAZILMAZ)
    def durmali(self, sablon, veri, beklenen):
        r, cikti = self.yamala(sablon, veri)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("YAZMA", r.stdout)
        self.assertIn(beklenen, r.stdout)
        self.assertFalse(os.path.exists(cikti), "hatada çıktı dosyası yazılmamalı")

    def test_olmayan_ayar_adi(self):   # K3: eski kod bunu sessizce kabul ediyordu
        self.durmali("index.json", [{"yol": "e-serit.olmayan_ayar", "deger": "x"}], "ayar yok")

    def test_yazim_hatali_ayar_adi_blokta(self):
        self.durmali("index.json", [{"yol": "e-serit/c1/i.ikon", "deger": "truck"}], "ayar yok")

    def test_olmayan_bolum(self):
        self.durmali("index.json", [{"yol": "e-yok/c1.text", "deger": "x"}], "bölüm yok")

    def test_olmayan_blok(self):
        self.durmali("index.json", [{"yol": "e-serit/c9/i.icon", "deger": "truck"}], "blok yok")

    def test_select_secenek_disi(self):
        self.durmali("index.json", [{"yol": "e-serit/c1/i.icon", "deger": "kamyon"}], "seçeneklerde yok")

    def test_checkbox_metin(self):
        self.durmali("index.json", [{"yol": "e-kars.disabled", "deger": "true"}], "true/false")

    def test_richtext_etiketsiz(self):
        self.durmali("product.nis-saglik.json", [{"yol": "n-pc/bas/h.text", "deger": "düz metin"}], "richtext")

    def test_ayni_yol_iki_kez(self):
        self.durmali("index.json", [{"yol": "e-serit/c1/i.icon", "deger": "truck"},
                                    {"yol": "e-serit/c1/i.icon", "deger": "box"}], "iki kez")

    # ---------------------------------------------------------- harita koruması (işlev düzeyi)
    def test_harita_blok_kaybi_ve_tip_degisimi(self):
        taban = T.oku_dosya(self.p("index.json"))
        yeni = json.loads(json.dumps(taban))
        yeni["sections"]["e-serit"]["blocks"]["c1"]["blocks"].pop("i")
        with self.assertRaises(T.YamaHatasi):
            T.harita_kontrol(taban, yeni, ())
        yeni = json.loads(json.dumps(taban))
        yeni["sections"]["e-kars"]["type"] = "hero"
        with self.assertRaises(T.YamaHatasi):
            T.harita_kontrol(taban, yeni, ())

    def test_sozluksuz_yalniz_mevcut_ayar(self):
        taban = T.oku_dosya(self.p("index.json"))
        T.uygula(taban, [("e-serit/c1/i.icon", "truck")], sozluk=None)
        with self.assertRaises(T.YamaHatasi):
            T.uygula(taban, [("e-serit/c1/i.yeni_ayar", 1)], sozluk=None)


@unittest.skipUnless(TEMA_VAR, "tema deposu yok: %s" % TEMA)
class SozlukGuncel(unittest.TestCase):
    def test_sozluk_temadan_yeniden_uretilenle_ayni(self):
        uretilen = T.sozluk_uret(TEMA_KOK)
        kayitli = json.load(open(SOZLUK, encoding="utf-8"))
        self.assertEqual(kayitli, uretilen,
                         "ayar-sozlugu.json temayla uyuşmuyor: python t4_yama.py --sozluk-uret <tema> --cikti ayar-sozlugu.json")

    def test_temadaki_her_ayar_sozlukte(self):
        import glob
        soz = json.load(open(SOZLUK, encoding="utf-8"))
        eksik = []
        dosyalar = glob.glob(os.path.join(TEMA, "templates", "*.json")) + glob.glob(os.path.join(TEMA, "sections", "*.json"))
        for f in dosyalar:
            t = T.oku_dosya(f)

            def gez(d, tur, yol, kok_tip):
                tan = T.ayar_tanimlari(soz, tur, d.get("type"), kok_tip)
                if tan is None:
                    eksik.append("%s %s tip yok: %s" % (os.path.basename(f), yol, d.get("type")))
                    return
                for k, v in (d.get("settings") or {}).items():
                    if k not in tan:
                        eksik.append("%s %s.%s" % (os.path.basename(f), yol, k))
                    else:
                        T.deger_kontrol(yol + "." + k, tan[k], v)   # mevcut değerler de geçerli sayılmalı
                for bid, b in (d.get("blocks") or {}).items():
                    gez(b, "blok", yol + "/" + bid, kok_tip)
            for sid, s in t["sections"].items():
                gez(s, "bolum", sid, s.get("type"))
        self.assertEqual(eksik, [])


class Kullanim(unittest.TestCase):
    def test_argumansiz_kod_2(self):
        r = calistir()
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)

    def test_bozuk_yama_dosyasi(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = os.path.join(tmp, "s.json")
            y = os.path.join(tmp, "y.json")
            open(s, "w", encoding="utf-8").write('{"sections":{"a":{"type":"x","settings":{"t":1}}},"order":["a"]}')
            open(y, "w", encoding="utf-8").write('[{"yol":"a.t"}]')
            r = calistir("--sablon", s, "--yama", y, "--cikti", os.path.join(tmp, "o.json"), "--sozluk", SOZLUK)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertFalse(os.path.exists(os.path.join(tmp, "o.json")))

    def test_sentetik_sablon_sozluksuz(self):
        """Tema deposu olmadan da çekirdek davranış: yorumlu şablon, mevcut ayar yazılır, sıkıştırılmış çıktı."""
        taban = T.oku_metin('/* yorum */\n{"sections":{"a":{"type":"bilinmeyen","settings":{"t":"eski"},'
                            '"blocks":{"b":{"type":"y","settings":{"u":1}}},"block_order":["b"]}},"order":["a"]}')
        yeni, rapor = T.uygula(taban, [("a/b.u", 2), ("a.t", "yeni")], sozluk={"bolumler": {}, "bloklar": {}})
        self.assertEqual(yeni["sections"]["a"]["blocks"]["b"]["settings"]["u"], 2)
        self.assertEqual(len(rapor), 2)
        with self.assertRaises(T.YamaHatasi):
            T.uygula(taban, [("a.yok", 1)], sozluk=None)


if __name__ == "__main__":
    unittest.main()
