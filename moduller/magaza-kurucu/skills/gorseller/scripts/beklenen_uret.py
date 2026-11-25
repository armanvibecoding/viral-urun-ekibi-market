#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""METINLER.md → ocr_kontrol.py'nin beklenen metin dosyaları (<görsel adı>.txt). Denetim #24 (V3): "elle yazma, kopyala" kuralının betiği.

  python3 beklenen_uret.py METINLER.md --cikti gorseller/ [--sadece galeri-1 …]

Her slot için `<ad>.txt`: her satır bir metin öğesi (başlık `/` ile satırlara bölünür; `alt satır:` gibi etiket atılır). "(yazı yok)" = BOŞ dosya
(görselde yazı olmamalı; ocr_kontrol fazla yazıyı yakalar). Aynı adı iki slot isterse HATA. Çıkış: 0 yazıldı · 1 çakışma/yazı yok · 2 kullanım.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metinler  # noqa: E402

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def satirlar(alanlar):
    out = []
    for t, m in alanlar:
        for parca in re.split(r"\s+/\s+", m.strip()) if t == "baslik" else [m.strip()]:
            if parca.strip():
                out.append(parca.strip())
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("metinler")
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--sadece", action="append")
    a = ap.parse_args()
    if not os.path.isfile(a.metinler):
        print("HATA: dosya yok: %s" % a.metinler)
        return 2
    slotlar = metinler.oku(a.metinler)
    yazilacak, hata = {}, []
    for s in slotlar:
        for ad in s["adlar"]:
            if a.sadece and ad not in a.sadece:
                continue
            if ad in yazilacak:
                hata.append("aynı ad iki slotta: %s" % ad)
            yazilacak[ad] = satirlar(s["alanlar"])
    if hata or not yazilacak:
        for h in hata or ["yazılacak slot bulunamadı (METINLER.md biçimi: `- slot: metin | alt satır: …`)"]:
            print("HATA:", h)
        return 1
    os.makedirs(a.cikti, exist_ok=True)
    for ad, sat in sorted(yazilacak.items()):
        with open(os.path.join(a.cikti, ad + ".txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(sat) + ("\n" if sat else ""))
    print("yazıldı: %d beklenen metin dosyası → %s" % (len(yazilacak), a.cikti))
    return 0


if __name__ == "__main__":
    sys.exit(main())
