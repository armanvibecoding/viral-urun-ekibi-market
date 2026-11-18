#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arayüz sözleşmesi doğrulayıcısı (sürüm 1). Yalnız standart kütüphane.

Ürün bulan ekip -> urun-paketi.json -> Mağaza Kurucu -> magaza-paketi.json -> video ekibi -> video-paketi.json

  python paket_dogrula.py urun   <urun-paketi.json>
  python paket_dogrula.py magaza <magaza-paketi.json>
  python paket_dogrula.py video  <video-paketi.json>
  python paket_dogrula.py zincir <urun-paketi.json> <magaza-paketi.json> [<video-paketi.json>]

Kurallar bu dosyanın yanındaki *.schema.json dosyalarından okunur (tek kaynak). Bu klasör iki plugin'de de
bayt bayt aynıdır; yalnız kaynağında (Mağaza Kurucu deposu, src/ortak/sozlesme/) düzenlenir.
Çıkış kodu: 0 = geçti (UYARI olabilir), 1 = HATA var, 2 = kullanım ya da dosya hatası.
"""
import json
import os
import re
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
TURLER = ("urun", "magaza", "video")
YUKLENEN = ("pdp-galeri", "hero")       # Mağaza Kurucu'nun mağazaya yüklediği video kullanımları


def yukle(yol):
    with open(yol, encoding="utf-8-sig") as f:
        return json.load(f)


def sema(tur):
    return yukle(os.path.join(BURASI, "%s-paketi.schema.json" % tur))


def _tur_uyar(deger, ad):
    if ad == "string":
        return isinstance(deger, str)
    if ad == "boolean":
        return isinstance(deger, bool)
    if ad == "integer":
        return isinstance(deger, int) and not isinstance(deger, bool)
    if ad == "number":
        return isinstance(deger, (int, float)) and not isinstance(deger, bool)
    if ad == "array":
        return isinstance(deger, list)
    if ad == "object":
        return isinstance(deger, dict)
    if ad == "null":
        return deger is None
    raise ValueError("şemada bilinmeyen tür: %s" % ad)


def _gez(deger, s, yol, hatalar, uyarilar):
    """JSON Schema alt kümesi: type, const, enum, pattern, minLength, minimum, required, properties,
    items, minItems, maxItems. Şemada olmayan alan HATA değil UYARI'dır (sözleşme dışı alan okunmaz)."""
    yer = yol or "(kök)"
    if "const" in s and deger != s["const"]:
        hatalar.append("%s: %r olmalı, bulunan %r" % (yer, s["const"], deger))
        return
    if "enum" in s and deger not in s["enum"]:
        hatalar.append("%s: %s değerlerinden biri olmalı, bulunan %r" % (yer, " | ".join(map(str, s["enum"])), deger))
        return
    if "type" in s:
        turler = s["type"] if isinstance(s["type"], list) else [s["type"]]
        if not any(_tur_uyar(deger, t) for t in turler):
            hatalar.append("%s: tür %s olmalı, bulunan %s" % (yer, "/".join(turler), type(deger).__name__))
            return
    if isinstance(deger, str):
        if len(deger) < s.get("minLength", 0):
            hatalar.append("%s: boş olamaz" % yer)
        if "pattern" in s and not re.search(s["pattern"], deger):
            hatalar.append("%s: biçim %s olmalı, bulunan %r" % (yer, s["pattern"], deger))
    if isinstance(deger, (int, float)) and not isinstance(deger, bool) and "minimum" in s and deger < s["minimum"]:
        hatalar.append("%s: en az %s olmalı, bulunan %r" % (yer, s["minimum"], deger))
    if isinstance(deger, list):
        if len(deger) < s.get("minItems", 0):
            hatalar.append("%s: en az %d öğe olmalı, bulunan %d" % (yer, s["minItems"], len(deger)))
        if "maxItems" in s and len(deger) > s["maxItems"]:
            hatalar.append("%s: en çok %d öğe olmalı, bulunan %d" % (yer, s["maxItems"], len(deger)))
        if "items" in s:
            for i, oge in enumerate(deger):
                _gez(oge, s["items"], "%s[%d]" % (yol, i), hatalar, uyarilar)
    if isinstance(deger, dict):
        for alan in s.get("required", []):
            if alan not in deger:
                hatalar.append("%s: zorunlu alan eksik" % (yol + "." + alan if yol else alan))
        ozellik = s.get("properties")
        if ozellik is not None:
            for alan, alt in deger.items():
                alt_yol = yol + "." + alan if yol else alan
                if alan in ozellik:
                    _gez(alt, ozellik[alan], alt_yol, hatalar, uyarilar)
                else:
                    uyarilar.append("%s: sözleşme dışı alan (okunmaz)" % alt_yol)


def dogrula(tur, veri):
    """(hatalar, uyarilar) döner. tur: urun | magaza | video."""
    if tur not in TURLER:
        raise ValueError("tür urun | magaza | video olmalı: %r" % tur)
    hatalar, uyarilar = [], []
    _gez(veri, sema(tur), "", hatalar, uyarilar)
    if hatalar:
        return hatalar, uyarilar
    if tur == "urun":
        for i, o in enumerate(veri["urun"].get("ozellikler", [])):
            if not o.get("kaynak"):
                uyarilar.append("urun.ozellikler[%d] (%s): kaynak yok, doğrulanmış sayılmaz" % (i, o["ad"]))
    if tur == "magaza":
        if not any(g["kod"] == "G0" and g.get("yazisiz") is True for g in veri["gorseller"]):
            uyarilar.append("gorseller: yazısız G0 karesi yok (video için ürün referansı)")
        for i, d in enumerate(veri["onayli_metinler"]["iddialar"]):
            if not d["bilgi_notu"] and not d.get("kaynak"):
                uyarilar.append("onayli_metinler.iddialar[%d]: kaynak yok ve bilgi notu değil" % i)
        alan = veri["magaza"].get("alan_adi")
        if alan and alan not in veri["magaza"]["pdp_url"]:
            uyarilar.append("magaza.pdp_url alan adını (%s) içermiyor" % alan)
    if tur == "video":
        adlar = [v["dosya"] for v in veri]
        for ad in sorted(set(a for a in adlar if adlar.count(a) > 1)):
            hatalar.append("dosya iki kez geçiyor: %s" % ad)
    return hatalar, uyarilar


def _varyant_adlari(liste):
    return [v if isinstance(v, str) else str(v.get("ad", "")) for v in liste or []]


def zincir(urun, magaza, video=None):
    """Dosyalar arası tutarlılık. Her dosya önce kendi şemasından geçer. (hatalar, uyarilar) döner."""
    hatalar, uyarilar = [], []
    for tur, veri in (("urun", urun), ("magaza", magaza), ("video", video)):
        if veri is None:
            continue
        h, u = dogrula(tur, veri)
        hatalar += ["%s-paketi: %s" % (tur, x) for x in h]
        uyarilar += ["%s-paketi: %s" % (tur, x) for x in u]
    if hatalar:
        return hatalar, uyarilar
    pazar = urun["pazar"]
    if pazar.get("para") and pazar["para"] != magaza["urun"]["para"]:
        hatalar.append("zincir: pazar parası %s, mağaza fiyatı %s" % (pazar["para"], magaza["urun"]["para"]))
    kaynak_v = set(_varyant_adlari(urun["urun"].get("varyantlar")))
    if kaynak_v:
        for ad in _varyant_adlari(magaza["urun"].get("varyantlar")):
            if ad not in kaynak_v:
                uyarilar.append("zincir: mağaza varyantı ürün paketinde yok: %s" % ad)
    if video is not None:
        dil = pazar.get("dil")
        for v in video:
            if dil and v.get("altyazi_dili") and v["altyazi_dili"] != dil:
                uyarilar.append("zincir: %s altyazı dili %s, pazar dili %s" % (v["dosya"], v["altyazi_dili"], dil))
        yuklenecek = [v["dosya"] for v in video if v["kullanim"] in YUKLENEN]
        print("zincir: mağazaya yüklenecek video: %s" % (", ".join(yuklenecek) or "yok (hepsi reklam)"))
    return hatalar, uyarilar


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(argv) < 3 or argv[1] not in TURLER + ("zincir",) or (argv[1] == "zincir" and len(argv) not in (4, 5)):
        print(__doc__)
        return 2
    try:
        veriler = [yukle(p) for p in argv[2:]]
    except (OSError, ValueError) as e:
        print("HATA: dosya okunamadı ya da geçerli JSON değil: %s" % e)
        return 2
    if argv[1] == "zincir":
        hatalar, uyarilar = zincir(*veriler)
    else:
        hatalar, uyarilar = dogrula(argv[1], veriler[0])
    for u in uyarilar:
        print("UYARI:", u)
    for h in hatalar:
        print("HATA:", h)
    print("SONUÇ: %s (%d hata, %d uyarı)" % ("GEÇTİ" if not hatalar else "KALDI", len(hatalar), len(uyarilar)))
    return 0 if not hatalar else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
