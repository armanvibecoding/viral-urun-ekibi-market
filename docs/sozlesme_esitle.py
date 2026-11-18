#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arayüz sözleşmesini içerideki Mağaza Kurucu modülünden eklentiye kopyalar ya da kopyanın güncelliğini denetler.

Tek kaynak: moduller/magaza-kurucu/src/ortak/sozlesme/ + moduller/magaza-kurucu/src/ortak/arayuz-sozlesmesi.md.
Kopya:      plugins/viral-urun-ekibi/ortak/sozlesme/   (elle DÜZENLENMEZ)

  python3 docs/sozlesme_esitle.py            # kaynaktaki OZET.json'u yeniden üret, kopyala, denetle
  python3 docs/sozlesme_esitle.py --kontrol  # yazmadan denetle

--kontrol: kopyadaki her dosyanın özeti OZET.json ile aynı mı; kaynaktaki OZET.json kaynağın kendisiyle tutarlı mı;
kopya kaynakla bayt bayt aynı mı. Çıkış: 0 aynı, 1 farklı. İsteğe bağlı argüman: başka bir kaynak modül yolu.
"""
import hashlib
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KOPYA = os.path.join(KOK, "plugins", "viral-urun-ekibi", "ortak", "sozlesme")
VARSAYILAN_KAYNAK = os.path.join(KOK, "moduller", "magaza-kurucu")
BELGE = "arayuz-sozlesmesi.md"
OZET = "OZET.json"


def bayt(p):
    with open(p, "rb") as f:
        return f.read().replace(b"\r\n", b"\n")


def ozet(p):
    return hashlib.sha256(bayt(p)).hexdigest()


def soz_klasoru(depo):
    soz = os.path.join(depo, "src", "ortak", "sozlesme")
    if not os.path.isdir(soz):
        raise SystemExit("HATA: Mağaza Kurucu modülü değil ya da sözleşme yok: %s" % soz)
    return soz


def kaynak_listesi(depo):
    """{göreli ad: kaynak yol}: kaynaktaki tüm sözleşme dosyaları (OZET.json hariç) + belge."""
    soz = soz_klasoru(depo)
    d = {}
    for k, klasorler, fs in os.walk(soz):
        klasorler[:] = [x for x in klasorler if x != "__pycache__"]
        for f in fs:
            rel = os.path.relpath(os.path.join(k, f), soz).replace(os.sep, "/")
            if rel != OZET and not f.endswith(".pyc") and f != ".DS_Store":
                d[rel] = os.path.join(k, f)
    d[BELGE] = os.path.join(depo, "src", "ortak", BELGE)
    return d


def ozet_uret(depo):
    """Kaynaktaki OZET.json'u kaynağın kendisinden yeniden yazar."""
    veri = {"surum": "2", "kaynak": "moduller/magaza-kurucu: src/ortak/sozlesme/ + src/ortak/arayuz-sozlesmesi.md",
            "dosyalar": {rel: ozet(p) for rel, p in sorted(kaynak_listesi(depo).items())}}
    with open(os.path.join(soz_klasoru(depo), OZET), "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(veri, ensure_ascii=False, indent=2) + "\n")


def kaynak_dosyalari(depo):
    """{kopyadaki göreli ad: kaynak yol}"""
    d = kaynak_listesi(depo)
    d[OZET] = os.path.join(soz_klasoru(depo), OZET)
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
        mevcut |= {os.path.relpath(os.path.join(k, f), KOPYA).replace(os.sep, "/") for f in fs
                   if not f.endswith(".pyc") and f != ".DS_Store"}
    for rel in sorted(mevcut - set(liste) - {OZET}):
        hatalar.append("OZET.json'da olmayan dosya: %s" % rel)
    kaynak_ozet_yolu = os.path.join(soz_klasoru(depo), OZET)
    if not os.path.isfile(kaynak_ozet_yolu):
        return hatalar + ["kaynakta OZET.json yok: python3 docs/sozlesme_esitle.py ile üret"]
    kaynak_ozet = json.loads(bayt(kaynak_ozet_yolu).decode("utf-8"))["dosyalar"]
    if kaynak_ozet != {rel: ozet(p) for rel, p in kaynak_listesi(depo).items()}:
        hatalar.append("kaynaktaki OZET.json kaynakla tutarsız (kaynak düzenlendi, eşitlenmedi): python3 docs/sozlesme_esitle.py")
    for rel, kaynak in sorted(kaynak_dosyalari(depo).items()):
        p = os.path.join(KOPYA, *rel.split("/"))
        if not os.path.isfile(p) or bayt(p) != bayt(kaynak):
            hatalar.append("kaynakla farklı: %s" % rel)
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
    depo = os.path.abspath(arg[0]) if arg else VARSAYILAN_KAYNAK
    if not yalniz_kontrol:
        ozet_uret(depo)
        print("kopyalandı: %d dosya güncellendi (%s)" % (kopyala(depo), os.path.relpath(KOPYA, KOK)))
    hatalar = kontrol(depo)
    for h in hatalar:
        print("HATA:", h)
    print("SONUÇ: %s (kaynak: %s)" % ("AYNI" if not hatalar else "FARKLI", os.path.relpath(depo, KOK)))
    return 0 if not hatalar else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
