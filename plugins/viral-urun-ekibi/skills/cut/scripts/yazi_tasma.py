#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ekran yazısı taşma ölçümü (denetim 2026-11-25 #24, V3; SINAV-01-03:42 "yazı taşmasını ölçen kapı yok"): göz değil ölçüm.

  python3 yazi_tasma.py ayar.json [--yan-pay 54]

ayar.json = hizli_kurgu biçimi. Her ekran yazısı (planlar[].yazi, yazilar[].yazi + satir2, cta.satir1/satir2) hizli_kurgu'nun kendi yazı yerleşimiyle
(aynı font, boyut, satır bölme `satirlara_bol`, kutulu/kontur payı) ölçülür: en geniş satır + kutu payı (kutulu: 2×28) ya da kontur payı, kare genişliği
1080 − 2×yan_pay (varsayılan 54 = %5 Reels güvenli yan alan) içine SIĞMALI. Tek kelime bile sığmıyorsa (satır bölünemez) kanca kareden taşar → HATA.
Çıkış: 0 hepsi sığıyor · 1 taşan yazı var (plan, yazı, genişlik) · 3 font/Pillow yok ya da ölçülecek yazı yok (ölçülemedi) · 2 kullanım.
"""
import argparse
import json
import os
import sys

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)


def olc(ayar, ayar_dizin, yan_pay):
    from PIL import Image, ImageDraw
    import hizli_kurgu as hk
    kutulu = ayar.get("yazi_stil") == "kutulu"
    font_yol = ayar.get("font", "")
    if not os.path.isabs(font_yol):
        font_yol = os.path.join(ayar_dizin, font_yol)
    d = ImageDraw.Draw(Image.new("RGB", (hk.W, hk.H)))
    sinir = hk.W - 2 * yan_pay
    ogeler = []
    for i, p in enumerate(ayar.get("planlar") or []):
        if p.get("yazi"):
            ogeler.append(("plan %d" % (i + 1), p["yazi"], p.get("boyut", 112)))
    for i, z in enumerate(ayar.get("yazilar") or []):
        if z.get("yazi"):
            ogeler.append(("yazı %d" % (i + 1), z["yazi"], z.get("boyut", 96)))
        if z.get("satir2"):
            ogeler.append(("yazı %d satır2" % (i + 1), z["satir2"], z.get("boyut2", 60)))
    cta = ayar.get("cta") or {}
    for ad, vars_ in (("satir1", 112), ("satir2", 60)):
        if cta.get(ad):
            ogeler.append(("cta " + ad, cta[ad], cta.get("boyut" if ad == "satir1" else "boyut2", vars_)))
    if not ogeler:
        return None, []
    taşan = []
    for yer, metin, boyut in ogeler:
        f = hk.font_yukle(font_yol, boyut, ayar.get("font_agirlik"))
        pay = 56 if kutulu else 2 * max(4, int(boyut * ayar.get("kontur_oran", hk.KONTUR_ORAN)))
        bosluk = d.textlength(" ", font=f)
        for s in hk.satirlara_bol(d, metin, f, 860 if kutulu else 900):
            gen = sum(d.textlength(k, font=f) for k in s) + bosluk * (len(s) - 1) + pay
            if gen > sinir:
                taşan.append((yer, " ".join(s), round(gen), boyut))
    return len(ogeler), taşan


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ayar")
    ap.add_argument("--yan-pay", type=int, default=54)
    a = ap.parse_args()
    try:
        ayar = json.load(open(a.ayar, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("HATA: ayar okunamadı: %s" % e)
        return 2
    try:
        n, tasan = olc(ayar, os.path.dirname(os.path.abspath(a.ayar)), a.yan_pay)
    except ImportError as e:
        print("ÖLÇÜLEMEDİ: Pillow/hizli_kurgu yüklenemedi (%s)" % e)
        return 3
    except SystemExit as e:
        print("ÖLÇÜLEMEDİ: %s" % e)
        return 3
    if n is None:
        print("ÖLÇÜLEMEDİ: ölçülecek ekran yazısı yok (ayarda yazı/yazilar/cta alanı bulunamadı)")
        return 3
    for yer, satir, gen, boyut in tasan:
        print("TAŞMA %s: «%s» %d px (en çok %d; boyut %d)" % (yer, satir[:40], gen, 1080 - 2 * a.yan_pay, boyut))
    print("YAZI TAŞMA: %s (%d yazı ölçüldü, %d taşan)" % ("KALDI" if tasan else "GEÇTİ", n, len(tasan)))
    return 1 if tasan else 0


if __name__ == "__main__":
    sys.exit(main())
