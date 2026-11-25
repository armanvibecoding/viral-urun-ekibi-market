# -*- coding: utf-8 -*-
"""METINLER.md okuyucu (copy_kontrol.py ve beklenen_uret.py ortak). Yalnız standart kütüphane.

İki biçim okunur:
  madde:  `- galeri-2: SICAK SIVI DÖKÜNCE DESEN BELİRİR | alt satır: Seramik · 350 ml`   (adlar virgülle: `- b1-masaustu, b2-mobil: …`)
  tablo:  `### G1` başlığı altında `| alan | önerilen metin | yedek | kaynak | sayı |` satırları (alan: başlık / etiket / açıklama / buton)
Döner: [{"slot": "galeri-2", "adlar": ["galeri-2"], "alanlar": [(tur, metin), …]}], tur ∈ baslik | etiket | aciklama | buton | diger.
"(yazı yok)" ya da boş metin = o görselde yazı olmamalı (alanlar boş liste).
"""
import re

TURLER = (("baslik", r"başlık|baslik|headline|title|g1_baslik"), ("etiket", r"etiket|label"),
          ("aciklama", r"açıklama|aciklama|alt\s*satır|alt\s*satir|alt\s*metin|teknik\s*satır|description|subtitle"),
          ("buton", r"buton|düğme|dugme|button|cta"))


def tur(ad):
    a = (ad or "").strip().lower()
    for t, r in TURLER:
        if re.search(r, a):
            return t
    return "diger"


def bos_mu(metin):
    return not metin.strip() or re.fullmatch(r"\(?\s*(yazı yok|yazi yok|no text|yok)\s*\)?", metin.strip(), re.I) is not None


def oku(yol):
    with open(yol, encoding="utf-8") as f:
        satirlar = f.read().splitlines()
    slotlar, mevcut = [], None
    baslik_hucre = None
    for s in satirlar:
        m = re.match(r"^\s*[-*]\s+([^:|]{1,60}):\s*(.*)$", s)
        if m and not s.lstrip().startswith("|"):
            adlar = [a.strip() for a in m.group(1).split(",") if a.strip()]
            parcalar = [p.strip() for p in m.group(2).split("|")]
            alanlar = []
            if not bos_mu(m.group(2)):
                for i, p in enumerate(parcalar):
                    if not p:
                        continue
                    et = re.match(r"^([A-Za-zÇĞİÖŞÜçğıöşü ]{2,20}):\s*(.+)$", p)
                    if i == 0 or not et:
                        alanlar.append(("baslik" if i == 0 else "diger", p))
                    else:
                        alanlar.append((tur(et.group(1)), et.group(2).strip()))
            slotlar.append({"slot": adlar[0] if adlar else "?", "adlar": adlar, "alanlar": alanlar})
            continue
        h = re.match(r"^#{2,4}\s+(.+?)\s*$", s)
        if h:
            mevcut = {"slot": re.split(r"\s", h.group(1).strip())[0].lower(), "adlar": [h.group(1).strip().split()[0].lower()], "alanlar": []}
            slotlar.append(mevcut)
            baslik_hucre = None
            continue
        if s.strip().startswith("|") and mevcut is not None:
            hucre = [c.strip() for c in s.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in hucre if c):
                continue
            if baslik_hucre is None and re.search(r"alan", hucre[0], re.I):
                baslik_hucre = hucre
                continue
            if len(hucre) >= 2 and baslik_hucre is not None and not bos_mu(hucre[1]):
                mevcut["alanlar"].append((tur(hucre[0]), hucre[1]))
    return [s for s in slotlar if s["adlar"]]
