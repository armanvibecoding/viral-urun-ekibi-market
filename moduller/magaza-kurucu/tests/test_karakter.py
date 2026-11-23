# -*- coding: utf-8 -*-
"""0.3.3 karakter + ADHD iletişim kuralları pakette duruyor mu (ortak blok, hatırlatmalar, Namelix ajanı)."""
import glob
import os
import re

import yaml

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLER = ["urun-analiz", "teklif", "marka", "metinler", "gorseller", "shopify-kurulum"]


def oku(*p):
    with open(os.path.join(KOK, *p), encoding="utf-8") as f:
        return f.read()


def test_ortak_blokta_karakter_kurallari():
    t = oku("src", "ortak", "00-calisma-tarzi.md")
    blok = t[t.index("## KARAKTER VE MESAJ BİÇİMİ"):t.index("MASTER PROMPT")]
    for parca in ("`AŞAMA a/3 · ADIM n/9 · <Kod adı> · senden ~N dk · <şerit>`",
                  "`AŞAMA 1/3 · ADIM 4/9 · Atlas · senden ~30 sn · ✓1–3 ▶4 ○5–9`",
                  "en çok 5 madde", "≤5 madde", "`Sonraki: <tek iş> (<süre>)`",
                  "ONAYLI DEĞER DEĞİŞMEZ", "KOD BLOĞU YOK", "önce sonuç + önerin",
                  '"sen" diye konuşursun', "Giriş cümlesi yok"):
        assert parca in blok, parca
    # hukuk yasağı eklenmedi: yalnız bilgi notu
    assert "Bilgi notu (kullanıcının sorumluluğu)" in blok


def test_her_skill_ve_adim_dosyasinda_hatirlatma():
    for s in SKILLER:
        t = oku("skills", s, "SKILL.md")
        assert "**Karakter hatırlatma.**" in t, s
        assert re.search(r"`AŞAMA \d/3 · ADIM \d/9 · [^`]+ · senden ~[^`]+`", t), s
        assert "`Sonraki:`" in t and "kod bloğu yok" in t, s
    adimlar = glob.glob(os.path.join(KOK, "skills", "*", "references", "adim-*.md"))
    assert len(adimlar) == 7
    for f in adimlar:
        with open(f, encoding="utf-8") as h:
            assert h.readline().startswith("Biçim: KARAKTER bloğu ("), f
    assert "## Karakter (her mesaj, her aşama)" in oku("src", "tek", "SKILL.md")


def test_kullaniciya_kod_blogu_talimati_yok():
    for f in glob.glob(os.path.join(KOK, "skills", "*", "SKILL.md")) + [os.path.join(KOK, "src", "tek", "SKILL.md")]:
        with open(f, encoding="utf-8") as h:
            t = h.read()
        assert "kod bloğunda ver" not in t, f


def test_namelix_ajan_ve_sablon_tutarli():
    assert "references/namelix-ajan.md" in oku("skills", "marka", "SKILL.md")
    ajan = oku("skills", "marka", "references", "namelix-ajan.md")
    assert "AŞAMA 1/3 · ADIM 4/9 · Atlas" in ajan and "Yedek yol" in ajan
    sablon = oku("skills", "marka", "references", "namelix-sablonu.md")
    m = re.search(r"`\{K\}=([a-z ]+)`", sablon)
    assert m, "örnek anahtar kelime satırı yok"
    for kelime in m.group(1).split():
        for yasak in ("w", "q", "x", "th", "ph", "ee", "oo"):
            assert yasak not in kelime, "%s blacklist'teki %s'yi içeriyor" % (kelime, yasak)


def test_kisa_aciklama_30_karakter():
    yamllar = glob.glob(os.path.join(KOK, "skills", "*", "agents", "openai.yaml")) + [
        os.path.join(KOK, "src", "tek", "agents", "openai.yaml")]
    assert len(yamllar) == 7
    for f in yamllar:
        with open(f, encoding="utf-8") as h:
            kisa = yaml.safe_load(h)["interface"]["short_description"]
        assert len(kisa) <= 30, (f, kisa)
