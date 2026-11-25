#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Panel (kör görsel jürisi) medyanı ve puan tablosu: Director elle çıkarmaz, betik çıkarır (denetim 2026-11-25 #24, V3).

  python3 panel_medyan.py TUR_KLASORU [--esleme pano/_esleme.json] [--md PUAN.md] [--json PUAN.json]

Girdi: TUR_KLASORU/KOR-1.json … KOR-3.json (ya da kopya-<n>/KOR-<n>.json). Her dosya (Panel ajanı yazar):
  {"puanlar": {"A": {"tipografi": 7, "renk": 8, "kompozisyon": 6, "urun": 7, "metin": 6, "nise": 8, "mobil": 7}, "B": {…}, …},
   "sira": ["B", "A", "D", "C"],            1. en iyi; bütün kodların tek tek sıralaması
   "yapay": ["C"],                         "hangisi yapay zekâ üretimi olabilir" (boş olabilir)
   "ajans": {"A": true, "B": false, …},    "üst düzey ajans yayınlar mıydı"
   "pano_sorunu": ""}                      dolu ise (hesap adı, çerçeve farkı, kimlik sızıntısı) o kopya GEÇERSİZ
Eşleşme (`--esleme`): {"A": "bizim", "B": "referans-1", …} ya da {"kodlar": {…}} (Sentinel `seri` yazar, Panel'e KAPALI); verilirse bizim görsel
işaretlenir. Çıktı: boyut medyanı, toplam (7 boyut medyanının ortalaması), medyan sıra, yapay oyu, ajans evet oyu, kopyalar arası > 2 puan ayrışan
boyutlar. Aynı girdi → bayt bayt aynı çıktı (zaman damgası yok). Çıkış: 0 tamam · 1 geçersiz/yetersiz kopya (< 3 geçerli) · 2 kullanım.
"""
import argparse
import glob
import json
import os
import re
import statistics
import sys

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BOYUTLAR = ["tipografi", "renk", "kompozisyon", "urun", "metin", "nise", "mobil"]
MIN_KOPYA, AYRISMA = 3, 2


def sayi(x):
    return float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def kopyalari_oku(tur):
    yollar = sorted(glob.glob(os.path.join(tur, "KOR-*.json")) + glob.glob(os.path.join(tur, "kopya-*", "KOR-*.json")))
    gecerli, gecersiz = [], []
    for y in yollar:
        ad = os.path.relpath(y, tur)
        try:
            d = json.load(open(y, encoding="utf-8"))
        except ValueError as e:
            gecersiz.append("%s: JSON okunamadı (%s)" % (ad, e))
            continue
        if str(d.get("pano_sorunu") or "").strip():
            gecersiz.append("%s: pano_sorunu dolu → PANO GEÇERSİZ (%s)" % (ad, str(d["pano_sorunu"])[:80]))
            continue
        p, sira = d.get("puanlar") or {}, d.get("sira") or []
        kodlar = sorted(p)
        hata = []
        if len(kodlar) < 2:
            hata.append("en az 2 görsel puanlanmalı")
        if sorted(sira) != kodlar:
            hata.append("sıra bütün kodların tek tek sıralaması değil")
        for k in kodlar:
            for b in BOYUTLAR:
                v = sayi((p[k] or {}).get(b))
                if v is None or not 0 <= v <= 10:
                    hata.append("%s.%s 0–10 değil" % (k, b))
        if not hata and len(kodlar) >= 3 and sum(len({sayi(p[k][b]) for k in kodlar}) == 1 for b in BOYUTLAR) > len(BOYUTLAR) / 2:
            hata.append("ayırt etmiyor: 4+ boyutta bütün görsellere aynı puan")
        if hata:
            gecersiz.append("%s: %s" % (ad, "; ".join(hata[:3])))
        else:
            gecerli.append({"ad": ad, "kodlar": kodlar, "puanlar": p, "sira": sira, "yapay": d.get("yapay") or [], "ajans": d.get("ajans") or {}})
    return gecerli, gecersiz


def hesapla(gecerli):
    kodlar = gecerli[0]["kodlar"]
    sonuc = {}
    for k in kodlar:
        med = {b: statistics.median(c["puanlar"][k][b] for c in gecerli) for b in BOYUTLAR}
        ayr = [b for b in BOYUTLAR if max(c["puanlar"][k][b] for c in gecerli) - min(c["puanlar"][k][b] for c in gecerli) > AYRISMA]
        sonuc[k] = {"medyan": med, "toplam": round(sum(med.values()) / len(med) * 2) / 2, "ham_toplam": sum(med.values()) / len(med),
                    "sira": statistics.median(c["sira"].index(k) + 1 for c in gecerli),
                    "yapay_oy": sum(k in c["yapay"] for c in gecerli), "ajans_evet": sum(bool(c["ajans"].get(k)) for c in gecerli),
                    "ajans_oy": sum(k in c["ajans"] for c in gecerli), "ayrisan_boyut": ayr}
    return sonuc


def esleme_oku(yol):
    if not yol:
        return {}
    d = json.load(open(yol, encoding="utf-8"))
    return d.get("kodlar", d) if isinstance(d, dict) else {}


def tablo(sonuc, esleme, n_kopya):
    s = ["PANEL %d kopya · %d görsel" % (n_kopya, len(sonuc)),
         "| Görsel | Kim | " + " | ".join(BOYUTLAR) + " | Toplam | Medyan sıra | Yapay oyu | Ajans evet | Kopya ayrışması (> %d) |" % AYRISMA,
         "|---|---|" + "---|" * (len(BOYUTLAR) + 5)]
    for k in sorted(sonuc, key=lambda x: (sonuc[x]["sira"], x)):
        r = sonuc[k]
        kim = "bizim" if "bizim" in str(esleme.get(k, "")).lower() else ("referans" if esleme else "?")
        s.append("| %s | %s | %s | %.1f | %g | %d/%d | %s | %s |" % (
            k, kim, " | ".join("%g" % r["medyan"][b] for b in BOYUTLAR), r["toplam"], r["sira"], r["yapay_oy"], n_kopya,
            "%d/%d" % (r["ajans_evet"], r["ajans_oy"]) if r["ajans_oy"] else "-", ", ".join(r["ayrisan_boyut"]) or "-"))
    bizim = [k for k in sonuc if "bizim" in str(esleme.get(k, "")).lower()]
    for k in bizim:
        r = sonuc[k]
        s.append("BİZİM %s: toplam %.1f · medyan sıra %g/%d · yapay oyu %d/%d%s" % (
            k, r["toplam"], r["sira"], len(sonuc), r["yapay_oy"], n_kopya,
            " · kopyalar bölündü: " + ", ".join(r["ayrisan_boyut"]) if r["ayrisan_boyut"] else ""))
    return "\n".join(s) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tur")
    ap.add_argument("--esleme")
    ap.add_argument("--md")
    ap.add_argument("--json")
    a = ap.parse_args()
    if not os.path.isdir(a.tur):
        print("HATA: klasör yok: %s" % a.tur)
        return 2
    gecerli, gecersiz = kopyalari_oku(a.tur)
    for g in gecersiz:
        print("GEÇERSİZ KOPYA %s" % g)
    if len({tuple(c["kodlar"]) for c in gecerli}) > 1:
        print("HATA: kopyalar farklı görsel kodlarını puanlamış (aynı pano değil)")
        return 1
    if len(gecerli) < MIN_KOPYA:
        print("KALDI: %d geçerli kopya var, en az %d bağımsız kopya gerekli (tek kopya hüküm değildir)" % (len(gecerli), MIN_KOPYA))
        return 1
    try:
        esleme = esleme_oku(a.esleme)
    except (OSError, ValueError) as e:
        print("HATA: eşleşme okunamadı: %s" % e)
        return 2
    sonuc = hesapla(gecerli)
    metin = tablo(sonuc, esleme, len(gecerli))
    print(metin, end="")
    if a.md:
        open(a.md, "w", encoding="utf-8", newline="\n").write(metin)
    if a.json:
        json.dump({"kopya": len(gecerli), "sonuc": sonuc}, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
