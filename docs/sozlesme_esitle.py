#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arayüz sözleşmesini Mağaza Kurucu deposundan bu depoya kopyalar ya da kopyanın güncelliğini denetler.

Tek kaynak: magaza-kurucu deposu, src/ortak/sozlesme/ + src/ortak/arayuz-sozlesmesi.md.
Kopya:      plugins/viral-urun-ekibi/ortak/sozlesme/   (elle DÜZENLENMEZ)

  python3 docs/sozlesme_esitle.py <magaza-kurucu deposunun yolu>           # kopyala
  python3 docs/sozlesme_esitle.py --kontrol [<magaza-kurucu deposunun yolu>] # yazmadan denetle

--kontrol: kopyadaki her dosyanın özeti OZET.json ile aynı mı (kaynak depo olmadan da çalışır); kaynak depo
verildiyse ya da yan klasörde (../magaza-kurucu) duruyorsa dosyalar bayt bayt karşılaştırılır. Çıkış: 0 aynı, 1 farklı.
"""
import hashlib
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KOPYA = os.path.join(KOK, "plugins", "viral-urun-ekibi", "ortak", "sozlesme")
BELGE = "arayuz-sozlesmesi.md"
OZET = "OZET.json"


def bayt(p):
    with open(p, "rb") as f:
        return f.read().replace(b"\r\n", b"\n")


def ozet(p):
    return hashlib.sha256(bayt(p)).hexdigest()


def kaynak_dosyalari(depo):
    """{kopyadaki göreli ad: kaynak yol}"""
    soz = os.path.join(depo, "src", "ortak", "sozlesme")
    if not os.path.isfile(os.path.join(soz, OZET)):
        raise SystemExit("HATA: Mağaza Kurucu deposu değil ya da sözleşme yok: %s" % soz)
    liste = json.loads(bayt(os.path.join(soz, OZET)).decode("utf-8"))["dosyalar"]
    d = {rel: os.path.join(soz, *rel.split("/")) for rel in liste if rel != BELGE}
    d[BELGE] = os.path.join(depo, "src", "ortak", BELGE)
    d[OZET] = os.path.join(soz, OZET)
    return d


def kontrol(depo):
    hatalar = []
    ozet_yolu = os.path.join(KOPYA, OZET)
    if not os.path.isfile(ozet_yolu):
        return ["kopya yok: %s" % ozet_yolu]
    liste = json.loads(bayt(ozet_yolu).decode("utf-8"))["dosyalar"]
    for rel, beklenen in sorted(liste.items()):
        p = os.path.join(KOPYA, *rel.split("/"))
        if not os.path.isfile(p):
            hatalar.append("eksik: %s" % rel)
        elif ozet(p) != beklenen:
            hatalar.append("OZET.json ile farklı (elle düzenlenmiş?): %s" % rel)
    mevcut = set()
    for k, klasorler, fs in os.walk(KOPYA):
        klasorler[:] = [x for x in klasorler if x != "__pycache__"]
        mevcut |= {os.path.relpath(os.path.join(k, f), KOPYA).replace(os.sep, "/") for f in fs}
    for rel in sorted(mevcut - set(liste) - {OZET}):
        hatalar.append("OZET.json'da olmayan dosya: %s" % rel)
    if depo:
        for rel, kaynak in sorted(kaynak_dosyalari(depo).items()):
            p = os.path.join(KOPYA, *rel.split("/"))
            if not os.path.isfile(p) or bayt(p) != bayt(kaynak):
                hatalar.append("kaynak depoyla farklı: %s" % rel)
    return hatalar


def kopyala(depo):
    n = 0
    for rel, kaynak in sorted(kaynak_dosyalari(depo).items()):
        hedef = os.path.join(KOPYA, *rel.split("/"))
        os.makedirs(os.path.dirname(hedef), exist_ok=True)
        if not os.path.isfile(hedef) or bayt(hedef) != bayt(kaynak):
            with open(hedef, "wb") as f:
                f.write(bayt(kaynak))
            n += 1
    return n


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    arg = [a for a in argv[1:] if a != "--kontrol"]
    yalniz_kontrol = "--kontrol" in argv[1:]
    depo = arg[0] if arg else None
    if depo is None:
        yan = os.path.join(os.path.dirname(KOK), "magaza-kurucu")
        depo = yan if os.path.isdir(os.path.join(yan, "src", "ortak", "sozlesme")) else None
    if not yalniz_kontrol:
        if depo is None:
            print(__doc__)
            return 2
        print("kopyalandı: %d dosya güncellendi (%s)" % (kopyala(depo), KOPYA))
    hatalar = kontrol(depo)
    for h in hatalar:
        print("HATA:", h)
    print("SONUÇ: %s (%s)" % ("AYNI" if not hatalar else "FARKLI",
                              "kaynak depoyla karşılaştırıldı" if depo else "yalnız OZET.json ile; kaynak depo yok"))
    return 0 if not hatalar else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
