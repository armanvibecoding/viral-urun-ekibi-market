#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arayüz sözleşmesi doğrulayıcısı (sürüm 1 ve 2). Yalnız standart kütüphane.

Ürün kolu -> urun-paketi.json -> mağaza kolu -> magaza-paketi.json -> video kolu -> video-paketi.json

  python paket_dogrula.py urun   <urun-paketi.json>
  python paket_dogrula.py magaza <magaza-paketi.json> [--tam]
  python paket_dogrula.py video  <video-paketi.json>
  python paket_dogrula.py zincir <urun-paketi.json> <magaza-paketi.json> [<video-paketi.json>]

Kurallar bu dosyanın yanındaki *.schema.json dosyalarından okunur (tek kaynak). Kaynak: moduller/magaza-kurucu/src/ortak/sozlesme/;
eklentideki kopya (plugins/viral-urun-ekibi/ortak/sozlesme/) bayt bayt aynıdır, scripts/sozlesme_esitle.py ile eşitlenir.
Sürüm alanları: teklif (urun-paketi) ve magaza.tema_modu (magaza-paketi) sürüm 2 ile geldi; surum "1" dosyada HATA.
Bilinmeyen değer UYDURULMAZ (denetim 2026-11-25 #17): magaza-paketi'nde marka.ad, urun.baslik, urun.fiyat, urun.para, gorseller `null` olabilir ve
her null `eksik[]` listesinde yolu ile yazılmalıdır (null ama listede yok = HATA). fiyat 0/negatif, yer tutucu ad/dosya ("yok-yer-tutucu.jpg",
"<marka>", "lorem"…) ve kaynağı (`marka.ad_kaynak`) olmayan marka adı HATA'dır. Dürüst eksik paket GEÇER ama "EKSİK: …" satırı basar;
yayın/teslim geçişinde `--tam` ile eksik de HATA olur. urun-paketi'nde kanıt yoksa "kanıt: yok" basılır (eksik sayılır).
Çıkış kodu: 0 = geçti (UYARI/EKSİK olabilir), 1 = HATA var (ya da --tam ile eksik var), 2 = kullanım ya da dosya hatası.
"""
import json
import os
import re
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
TURLER = ("urun", "magaza", "video")
YUKLENEN = ("pdp-galeri", "hero")       # mağaza kolunun mağazaya yüklediği video kullanımları
SURUM2 = {                              # sürüm 2 ile gelen alanlar: (yol, değeri bulan)
    "urun": [("teklif", lambda v: v.get("teklif"))],
    "magaza": [("magaza.tema_modu", lambda v: v.get("magaza", {}).get("tema_modu"))],
}


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


# Yer tutucu / uydurma ad desenleri (denetim #17). Boş ya da şablon metni dolu değer SAYILMAZ: bilinmiyorsa null + eksik[].
YER_TUTUCU = re.compile(r"yer[-_ ]?tutucu|placeholder|lorem|\bdummy\b|\btbd\b|\btodo\b|\bxxx+\b|<[^>]*>|\{[^}]*\}|\[[^\]]*\]"
                        r"|^\s*(yok|n/?a|-+|\?+|null|none|nan|undefined|marka(\s+ad[ıi])?|brand(\s+name)?|product(\s+name)?|ürün(\s+ad[ıi])?|test)\s*$", re.I)
UYDURMA_KAYNAK = re.compile(r"uydur|jenerik|placeholder|tahmin|varsay|geçici|gecici|rastgele|örnek|ornek", re.I)
MAGAZA_NULL_YOLLARI = ("marka.ad", "urun.baslik", "urun.fiyat", "urun.para", "gorseller", "magaza.pdp_url")


def _yol_degeri(veri, yol):
    d = veri
    for a in yol.split("."):
        if not isinstance(d, dict) or a not in d:
            return None
        d = d[a]
    return d


def fiyat_sayisi(f):
    """Fiyat değerinden sayı: sayıysa kendisi; metinse ilk sayı (virgül/nokta ondalık); yoksa None."""
    if isinstance(f, bool):
        return None
    if isinstance(f, (int, float)):
        return float(f)
    m = re.search(r"\d[\d.,]*", str(f))
    if not m:
        return None
    t = m.group(0).rstrip(".,")
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".") if t.rfind(",") > t.rfind(".") else t.replace(",", "")
    elif "," in t:
        t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def eksik_kontrol(tur, veri):
    """(hatalar, eksikler). eksikler: dosyanın dürüstçe 'bilinmiyor' dediği ya da hiç içermediği alanlar (liderin özetinde görünür)."""
    hatalar, eksikler = [], []
    if tur == "magaza":
        bildirilen = list(veri.get("eksik", []))
        for yol in MAGAZA_NULL_YOLLARI:
            deger = _yol_degeri(veri, yol)
            if deger is None:
                eksikler.append(yol)
                if yol not in bildirilen:
                    hatalar.append("%s: null ama `eksik[]` listesinde yok (bilinmeyen değer adıyla bildirilmeli)" % yol)
            elif yol in bildirilen:
                hatalar.append("eksik[]: %s listede ama dosyada dolu (çelişki)" % yol)
        for yol in bildirilen:
            if yol not in MAGAZA_NULL_YOLLARI:
                hatalar.append("eksik[]: %r bilinen null yollarından değil (%s)" % (yol, ", ".join(MAGAZA_NULL_YOLLARI)))
        ad = veri["marka"].get("ad")
        if ad is not None:
            if not str(ad).strip() or YER_TUTUCU.search(str(ad)):
                hatalar.append("marka.ad: boş ya da yer tutucu (%r); bilinmiyorsa null + eksik[]" % ad)
            kaynak = str(veri["marka"].get("ad_kaynak") or "").strip()
            if not kaynak:
                hatalar.append("marka.ad: kaynağı yok — `marka.ad_kaynak` (kurucu kararı / Atlas çıktısı / mağaza kaydı) yazılmalı; kaynaksız ad uydurma sayılır")
            elif UYDURMA_KAYNAK.search(kaynak):
                hatalar.append("marka.ad_kaynak %r kaynak sayılmaz (uydurma/jenerik/tahmin)" % kaynak)
        baslik = veri["urun"].get("baslik")
        if baslik is not None and (not str(baslik).strip() or YER_TUTUCU.search(str(baslik))):
            hatalar.append("urun.baslik: boş ya da yer tutucu (%r); bilinmiyorsa null + eksik[]" % baslik)
        fiyat, para = veri["urun"].get("fiyat"), veri["urun"].get("para")
        if fiyat is not None:
            n = fiyat_sayisi(fiyat)
            if n is None:
                hatalar.append("urun.fiyat: sayı değil (%r); bilinmiyorsa null + eksik[]" % (fiyat,))
            elif n <= 0:
                hatalar.append("urun.fiyat: %r yer tutucu sayılır (0/negatif fiyat olmaz); bilinmiyorsa null + eksik[]" % (fiyat,))
            if para is None:
                hatalar.append("urun.para: fiyat dolu ama para birimi null")
        gorseller = veri.get("gorseller")
        for i, g in enumerate(gorseller or []):
            if YER_TUTUCU.search(g["dosya"]) or YER_TUTUCU.search(g["kod"]):
                hatalar.append("gorseller[%d]: yer tutucu dosya/kod (%r); görsel yoksa gorseller null + eksik[]" % (i, g["dosya"]))
    if tur == "urun":
        for yol in veri.get("eksik", []):
            eksikler.append(yol)
        if not veri.get("kanit") and "kanit" not in eksikler:
            eksikler.append("kanit")
        if not veri["urun"].get("tedarik_fiyati") and "urun.tedarik_fiyati" not in eksikler:
            eksikler.append("urun.tedarik_fiyati")
    return hatalar, eksikler


def dogrula(tur, veri):
    """(hatalar, uyarilar) döner. tur: urun | magaza | video."""
    if tur not in TURLER:
        raise ValueError("tür urun | magaza | video olmalı: %r" % tur)
    hatalar, uyarilar = [], []
    _gez(veri, sema(tur), "", hatalar, uyarilar)
    if hatalar:
        return hatalar, uyarilar
    for yol, deger in SURUM2.get(tur, ()):
        if veri.get("surum") == "1" and deger(veri) is not None:
            hatalar.append("%s: bu alan surum 2 ile geldi; dosyada surum 1 yazıyor" % yol)
    if hatalar:
        return hatalar, uyarilar
    if tur in ("magaza", "urun"):
        h2, eksikler = eksik_kontrol(tur, veri)
        hatalar += h2
        if eksikler:
            uyarilar.append("EKSİK: %s%s" % (", ".join(eksikler), " (kanıt: yok)" if "kanit" in eksikler else ""))
        if hatalar:
            return hatalar, uyarilar
    if tur == "urun":
        for i, o in enumerate(veri["urun"].get("ozellikler", [])):
            if not o.get("kaynak"):
                uyarilar.append("urun.ozellikler[%d] (%s): kaynak yok, doğrulanmış sayılmaz" % (i, o["ad"]))
    if tur == "magaza":
        if veri.get("gorseller") and not any(g["kod"] == "G0" and g.get("yazisiz") is True for g in veri["gorseller"]):
            uyarilar.append("gorseller: yazısız G0 karesi yok (video için ürün referansı)")
        for i, d in enumerate(veri["onayli_metinler"]["iddialar"]):
            if not d["bilgi_notu"] and not d.get("kaynak"):
                uyarilar.append("onayli_metinler.iddialar[%d]: kaynak yok ve bilgi notu değil" % i)
        alan = veri["magaza"].get("alan_adi")
        if alan and veri["magaza"].get("pdp_url") and alan not in veri["magaza"]["pdp_url"]:
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
    if pazar.get("para") and magaza["urun"]["para"] and pazar["para"] != magaza["urun"]["para"]:
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
    tam = "--tam" in argv
    argv = [a for a in argv if a != "--tam"]
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
    if tam:
        for u in [u for u in uyarilar if u.startswith("EKSİK:") or ": EKSİK:" in u]:
            hatalar.append("--tam: %s" % u)
    for u in uyarilar:
        print("UYARI:", u)
    for h in hatalar:
        print("HATA:", h)
    print("SONUÇ: %s (%d hata, %d uyarı)" % ("GEÇTİ" if not hatalar else "KALDI", len(hatalar), len(uyarilar)))
    return 0 if not hatalar else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
