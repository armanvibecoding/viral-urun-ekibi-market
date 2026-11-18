# -*- coding: utf-8 -*-
"""Eski prompt kapsamı: kural kaybı olmasın ama eski kural da kilitlenmesin.

- Eski promptun (kaynak/KAYNAK-PROMPT.md) her başlığı ve her dolu satırı ya bir
  references/ dosyasında birebir durur ya da docs/ESKIDI.md'de satır aralığıyla, gerekçesiyle
  iptal/değişmiş olarak yazılıdır.
- ESKIDI.md'nin her maddesi eksiksizdir (eski kural, neden, yeni yer) ve yeni yer repoda vardır.
- İptal edilen eski ifadeler pakette (SKILL.md + references) geri gelmez.
"""
import glob
import os
import re
import unittest

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYNAK = os.path.join(KOK, "kaynak", "KAYNAK-PROMPT.md")
ESKIDI = os.path.join(KOK, "docs", "ESKIDI.md")

BASLIK = re.compile(
    r"^(MASTER PROMPT|ROLÜN|ÇALIŞMA TARZI|GENEL KURALLAR|TEMA KISITLARI|ADIM \d/8|\d\.\d |"
    r"GÖRSEL KABUL KAPISI|Çıktı:|TEKNİK EK|T\d+(\.\d+)?[. ]|AKIŞ)")
AYRAC = re.compile(r"^─+$")

# İptal edilmiş eski kuralların imza ifadeleri: pakette hiçbir yerde geçmemeli.
YASAKLI_ESKI = [
    "TEK yanıtta 5",
    "urun-1..5",
    "mat traverten",
    "5 galeri fotoğraf",
    "| 5 galeri",
    "G1–G5",
    "Banner yazısı görselin içindedir",
    "model kullan (kararı gerekçelendir)",
    "önce tek yanıtta dene",
    "galeride ürün ortalı ve kare kırpmaya dayanıklı",
    "Galeri ve bölüm görsellerinde eklenen yazı",
    "puan ≥ 7",
    "gösterim için kritik yok ve puan",
    "kaynak kural (5c) geçerli",
    "Sağlık ve sonuç iddiası her zaman [DOĞRULA]",
    "Sağlıkta sağlık beyanı karşılaştırılmaz",
    "Rakip marka adı YASAK",
    "kendi boyunun en az %15'i kadar taşar",
]


def kaynak_satirlari():
    return open(KAYNAK, encoding="utf-8").read().split("\n")


def paket_dosyalari():
    return (glob.glob(os.path.join(KOK, "skills", "*", "references", "*.md"))
            + glob.glob(os.path.join(KOK, "skills", "*", "references", "*", "*.md"))
            + glob.glob(os.path.join(KOK, "skills", "*", "SKILL.md")))


def reference_satirlari():
    dosyalar = glob.glob(os.path.join(KOK, "skills", "*", "references", "*.md"))
    satirlar = set()
    for f in dosyalar:
        satirlar.update(l.rstrip() for l in open(f, encoding="utf-8").read().split("\n"))
    return satirlar, dosyalar


def eskidi_maddeleri():
    """[(id, aralıklar[(a, b)], eski, neden, yeni)]"""
    maddeler = []
    for l in open(ESKIDI, encoding="utf-8").read().split("\n"):
        m = re.match(r"^\|\s*(E\d+)\s*\|(.*)\|\s*$", l)
        if not m:
            continue
        hucre = [h.strip() for h in m.group(2).split("|")]
        if len(hucre) < 4:
            maddeler.append((m.group(1), None, "", "", ""))
            continue
        satir, eski, neden, yeni = hucre[0], hucre[1], hucre[2], "|".join(hucre[3:])
        araliklar = []
        if satir != "—":
            for parca in satir.split(","):
                ab = [int(x) for x in re.findall(r"\d+", parca)]
                araliklar.append((ab[0], ab[-1]))
        maddeler.append((m.group(1), araliklar, eski, neden, yeni))
    return maddeler


def eskidi_kapsar(no, maddeler):
    return any(a <= no <= b for _, ar, *_ in maddeler if ar for a, b in ar)


class KaynakKapsam(unittest.TestCase):
    def test_basliklar_ya_references_ya_eskidi(self):
        refs, dosyalar = reference_satirlari()
        self.assertTrue(dosyalar, "references dosyası bulunamadı")
        maddeler = eskidi_maddeleri()
        basliklar = [(i + 1, l.rstrip()) for i, l in enumerate(kaynak_satirlari()) if BASLIK.match(l)]
        self.assertGreaterEqual(len(basliklar), 30, "başlık deseni kaynakla uyuşmuyor")
        eksik = [(n, b) for n, b in basliklar if b not in refs and not eskidi_kapsar(n, maddeler)]
        self.assertEqual(eksik, [], "references'ta da ESKIDI.md'de de olmayan başlıklar")

    def test_her_kural_ya_references_ya_eskidi(self):
        refs, _ = reference_satirlari()
        maddeler = eskidi_maddeleri()
        eksik = [(i + 1, l[:70]) for i, l in enumerate(kaynak_satirlari())
                 if l.strip() and not AYRAC.match(l.strip()) and l.rstrip() not in refs
                 and not eskidi_kapsar(i + 1, maddeler)]
        self.assertEqual(eksik, [], "kaynaktaki bu satırlar references'ta yok ve ESKIDI.md'de gerekçesi yok")

    def test_eskidi_maddeleri_eksiksiz(self):
        maddeler = eskidi_maddeleri()
        self.assertGreaterEqual(len(maddeler), 20)
        idler = [m[0] for m in maddeler]
        self.assertEqual(len(idler), len(set(idler)), "ESKIDI.md'de tekrar eden madde no")
        n_kaynak = len(kaynak_satirlari())
        for mid, ar, eski, neden, yeni in maddeler:
            self.assertIsNotNone(ar, "%s: 5 sütun olmalı" % mid)
            for a, b in ar:
                self.assertTrue(1 <= a <= b <= n_kaynak, "%s: satır aralığı geçersiz %d–%d" % (mid, a, b))
            self.assertTrue(eski and neden and yeni, "%s: eski kural / neden / yeni yer boş" % mid)
            yollar = re.findall(r"`([^`]+)`", yeni)
            self.assertTrue(yollar, "%s: yeni yer sütununda `yol` yok" % mid)
            ilk = yollar[0].rstrip("/")
            adaylar = [os.path.join(KOK, ilk)] + glob.glob(os.path.join(KOK, "skills", "*", "references", ilk))
            self.assertTrue(any(os.path.exists(p) for p in adaylar), "%s: yeni yer bulunamadı: %s" % (mid, ilk))

    def test_iptal_edilen_ifadeler_pakette_yok(self):
        bulunan = []
        for f in paket_dosyalari():
            metin = open(f, encoding="utf-8").read()
            for ifade in YASAKLI_ESKI:
                if ifade in metin:
                    bulunan.append((os.path.relpath(f, KOK), ifade))
        self.assertEqual(bulunan, [], "ESKIDI.md'de iptal edilmiş kural pakete geri gelmiş")


if __name__ == "__main__":
    unittest.main()
