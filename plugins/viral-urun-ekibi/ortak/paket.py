#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kollar arası dosya alışverişi (arayüz sözleşmesi sürüm 1 ve 2). Yalnız standart kütüphane.

  ürün bulundu (SAT)  -> urun-yaz   -> is/NN-urun/magaza/urun-paketi.json   (mağaza kolunun girdisi)
  mağaza kuruldu      -> magaza-oku -> is/NN-urun/magaza/marka-kilidi.md    (video kolunun okuduğu özet)
                                       [--cikti-dizin is/NN-urun/kurgu: video-ayar.json + onayli-iddialar.txt]
  videolar teslim     -> video-yaz  -> is/NN-urun/magaza/video-paketi.json  (mağazaya geri dönüş)

Kullanım:
  paket.py dogrula urun|magaza|video DOSYA          paket.py dogrula zincir URUN MAGAZA [VIDEO]
  paket.py urun-yaz --cikti F --ad "<tedarikçideki ad>" --foto <dosya|URL> (--ulke TR | --pazar ABD)
          [--dil tr] [--para TRY] [--nis nis-gadget | --nis-kodu evcil] [--tedarik "9.4 USD" | --marj-csv is/firsat/marj.csv]
          [--ozellik "ad|deger|birim|kaynak"]... [--varyant "Gri|var"]... [--rakip "marka|url|fiyat"]...
          [--kanit "kaynak|url|YYYY-AA-GG|ölçü"]... [--kanit-md is/firsat/kanit/NN.md] [--teklif-tsv is/NN/teklif/teklif.tsv]
  paket.py fiyat [--teklif-tsv F] [--pazar US]      teklifin TEK kaynağı (bizim satırı > sabit kural 2'li %10, 3'lü %18)
  paket.py magaza-oku MAGAZA-PAKETI.json [--cikti marka-kilidi.md] [--cikti-dizin is/NN/kurgu]
  paket.py iddia-kontrol MAGAZA-PAKETI.json METIN_ya_da_AYAR.json [...]   onaylı listede olmayan iddia = çıkış 1
  paket.py video-yaz TESLIM_KLASORU [--cikti is/NN/magaza/video-paketi.json] [--pdp V02]... [--hero V03]...
          [--dil tr|yok] [--olcum "V01.mp4=1080x1920:12.4"]... [--urun F] [--magaza F]
  paket.py video-sec VIDEO-PAKETI.json              mağazaya yüklenecekler (yalnız pdp-galeri ve hero)

Şema ve doğrulayıcı yandaki sozlesme/ klasöründedir (kaynağı moduller/magaza-kurucu/src/ortak/sozlesme/; burada
düzenlenmez, docs/sozlesme_esitle.py eşitler). Bilinmeyen alan YAZILMAZ: verilmeyen seçenek dosyaya girmez, uydurulmaz.
Teklif verilirse (--teklif-tsv) dosya sürüm 2 olur; verilmezse sürüm 1. Çıkış: 0 geçti, 1 hata, 2 kullanım.
"""
import argparse
import csv
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from urllib.parse import urlparse

BURASI = os.path.dirname(os.path.abspath(__file__))
NIS_ESLEME = os.path.join(BURASI, "nis-esleme.tsv")
# Sabit paket kuralı (mağaza aşamasının varsayılanı). Teklifte `bizim` satırı varsa KULLANILMAZ.
SABIT_PAKETLER = [{"adet": 1, "indirim_yuzde": 0}, {"adet": 2, "indirim_yuzde": 10}, {"adet": 3, "indirim_yuzde": 18}]
PAZAR = {  # ISO-3166 ülke -> (dil, para)
    "US": ("en", "USD"), "TR": ("tr", "TRY"), "GB": ("en", "GBP"), "DE": ("de", "EUR"), "FR": ("fr", "EUR"),
    "ES": ("es", "EUR"), "IT": ("it", "EUR"), "NL": ("nl", "EUR"), "CA": ("en", "CAD"), "AU": ("en", "AUD"),
}
PAZAR_AD = {"ABD": "US", "USA": "US", "UK": "GB", "TÜRKİYE": "TR", "TURKIYE": "TR", "İNGİLTERE": "GB", "ALMANYA": "DE",
            "FRANSA": "FR", "İSPANYA": "ES", "KANADA": "CA"}
_PD = None


def dogrulayici():
    global _PD
    if _PD is None:
        yol = os.path.join(BURASI, "sozlesme", "paket_dogrula.py")
        if not os.path.exists(yol):
            raise SystemExit("HATA: doğrulayıcı yok: %s" % yol)
        spec = importlib.util.spec_from_file_location("paket_dogrula", yol)
        _PD = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_PD)
    return _PD


def sema_hatalari(tur, veri):
    """Yalnız hata listesi (boş = geçerli). kurgu_kontrol.py gibi dış kullanıcılar için."""
    return dogrulayici().dogrula(tur, veri)[0]


def oku_json(yol):
    try:
        return dogrulayici().yukle(yol)
    except OSError:
        raise SystemExit("HATA: dosya yok ya da okunamadı: %s" % yol)
    except ValueError as e:
        raise SystemExit("HATA: JSON bozuk: %s (%s)" % (yol, e))


def parcala(metin, n, ad):
    p = [x.strip() for x in metin.split("|")]
    if len(p) > n:
        raise SystemExit("HATA: --%s en çok %d parça alır (| ile ayrılır): %r" % (ad, n, metin))
    return p + [""] * (n - len(p))


def sayi_ya_da_metin(s):
    try:
        f = float(s.replace(",", "."))
    except ValueError:
        return s
    return int(f) if f == int(f) and "." not in s and "," not in s else f


def sayi(metin):
    """'39,99' / '$39.99' / '1.299,00' -> float; okunamazsa None."""
    t = re.sub(r"[^\d.,]", "", metin or "")
    if not t:
        return None
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".") if t.rfind(",") > t.rfind(".") else t.replace(",", "")
    elif "," in t:
        t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def yaz_json(yol, veri):
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(veri, ensure_ascii=False, indent=2) + "\n")


def rapor(hatalar, uyarilar, yol):
    for u in uyarilar:
        print("UYARI:", u)
    for h in hatalar:
        print("HATA:", h)
    print("SONUÇ: %s — %s" % ("GEÇTİ" if not hatalar else "KALDI (dosya yazılmadı ya da kullanılmaz)", yol))
    return 0 if not hatalar else 1


# ------------------------------------------------------------------ yardımcılar (pazar, niş, teklif, kanıt)
def pazar_coz(kod):
    k = kod.strip().upper()
    k = PAZAR_AD.get(k, k)
    if k not in PAZAR:
        raise SystemExit("HATA: pazar tanınmadı: %s (ISO kodu ver: %s)" % (kod, ", ".join(sorted(PAZAR))))
    return k


def nis_coz(kod):
    """Ekibin niş kodu (reklam-kutuphanesi-avi referans/nisler.md) -> mağaza niş eki. (nis, uyarı|None)"""
    tablo = {}
    with open(NIS_ESLEME, encoding="utf-8") as f:
        for satir in f:
            if satir.startswith("#") or not satir.strip() or satir.startswith("kod\t"):
                continue
            a, b = satir.rstrip("\n").split("\t")
            tablo[a] = b
    if kod in tablo:
        return tablo[kod], None
    return "nis-gadget", "niş kodu '%s' eşleme tablosunda yok; nis-gadget yazıldı (ortak/nis-esleme.tsv)" % kod


def teklif_satirlari(yol, pazar=None):
    with open(yol, encoding="utf-8", newline="") as f:
        satirlar = list(csv.DictReader(f, delimiter="\t"))
    if pazar:
        esdeger = {pazar, "UK" if pazar == "GB" else pazar}
        satirlar = [s for s in satirlar if (s.get("pazar") or "").strip().upper() in esdeger]
    return satirlar


def paket_coz(metin):
    """teklif.tsv `paket` sütunu ('1x;2x:-15%;3x:-25%') -> [{adet, indirim_yuzde}]; okunamayan parça atlanır."""
    out = []
    for parca in (metin or "").split(";"):
        m = re.match(r"^\s*(\d+)\s*x\s*(?::\s*-?\s*(\d+(?:[.,]\d+)?)\s*%)?\s*$", parca)
        if m:
            y = float((m.group(2) or "0").replace(",", "."))
            out.append({"adet": int(m.group(1)), "indirim_yuzde": int(y) if y == int(y) else y})
    return out


def teklif_kaynagi(teklif_tsv, pazar):
    """TEK fiyat kaynağı. teklif.tsv'de bu pazar için `bizim` satırı varsa o (son satır geçerli); yoksa sabit kural."""
    if teklif_tsv and os.path.exists(teklif_tsv):
        bizim = [s for s in teklif_satirlari(teklif_tsv, pazar) if (s.get("tur") or "").strip() == "bizim"]
        if bizim:
            b = bizim[-1]
            t = {"kaynak": "teklif.tsv"}
            f = sayi(b.get("fiyat"))
            if f:
                t["fiyat"] = f
                t["para"] = (b.get("para") or PAZAR.get(pazar, ("", ""))[1]).strip().upper()
            t["paketler"] = paket_coz(b.get("paket")) or [{"adet": 1, "indirim_yuzde": 0}]
            for alan in ("garanti", "kargo_vaadi"):
                if (b.get(alan) or "").strip() not in ("", "-", "yok", "gorulmedi"):
                    t[alan] = b[alan].strip()
            return t
    return {"kaynak": "sabit-kural", "paketler": [dict(p) for p in SABIT_PAKETLER]}


def alan_adi(url):
    h = urlparse(url).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def kanit_coz(yol):
    """Kanıt dosyasındaki URL'li satırlar -> kanit[]. Tarih satırda yoksa dosyadaki ilk tarih; o da yoksa alan yazılmaz.
    Ölçü satırın URL dışındaki metnidir; satırda metin yoksa o URL alınmaz (ölçüsüz kanıt uydurulmaz)."""
    with open(yol, encoding="utf-8") as f:
        metin = f.read()
    genel = re.search(r"\d{4}-\d{2}-\d{2}", metin)
    out, gorulen = [], set()
    for satir in metin.splitlines():
        for url in re.findall(r"https?://[^\s)|>\]]+", satir):
            url = url.rstrip(".,;")
            if url in gorulen:
                continue
            gorulen.add(url)
            olcu = re.sub(r"https?://[^\s)|>\]]+", "", satir)
            olcu = re.sub(r"[|*`#\[\]()]", " ", olcu)
            olcu = re.sub(r"\s+", " ", olcu).strip(" -:·")
            if not olcu:
                continue
            k = {"kaynak": alan_adi(url), "olcu": olcu[:160], "url": url}
            t = re.search(r"\d{4}-\d{2}-\d{2}", satir) or genel
            if t:
                k["tarih"] = t.group(0)
            out.append(k)
    return out


# ------------------------------------------------------------------ urun-yaz
def urun_yaz(a):
    pd = dogrulayici()
    uyarilar = []
    if bool(a.ulke) == bool(a.pazar):
        raise SystemExit("HATA: --ulke ya da --pazar (yalnız biri) verilmeli")
    if a.nis and a.nis_kodu:
        raise SystemExit("HATA: --nis ya da --nis-kodu (yalnız biri)")
    if a.tedarik and a.marj_csv:
        raise SystemExit("HATA: --tedarik ya da --marj-csv (yalnız biri)")
    if a.pazar:
        ulke = pazar_coz(a.pazar)
        dil, para = a.dil or PAZAR[ulke][0], a.para or PAZAR[ulke][1]
    else:
        ulke, dil, para = a.ulke, a.dil, a.para
    urun = {"ad": a.ad, "fotograflar": a.foto}
    if a.nis:
        urun["nis"] = a.nis
    elif a.nis_kodu:
        urun["nis"], u = nis_coz(a.nis_kodu)
        if u:
            uyarilar.append(u)
    if a.ozellik:
        urun["ozellikler"] = []
        for o in a.ozellik:
            ad, deger, birim, kaynak = parcala(o, 4, "ozellik")
            satir = {"ad": ad, "deger": sayi_ya_da_metin(deger)}
            if birim:
                satir["birim"] = birim
            if kaynak:
                satir["kaynak"] = kaynak
            urun["ozellikler"].append(satir)
    if a.varyant:
        urun["varyantlar"] = []
        for v in a.varyant:
            ad, stok = parcala(v, 2, "varyant")
            satir = {"ad": ad}
            if stok:
                if stok.lower() not in ("var", "yok"):
                    raise SystemExit("HATA: --varyant stok değeri var | yok olmalı: %r" % v)
                satir["stok"] = stok.lower() == "var"
            urun["varyantlar"].append(satir)
    if a.tedarik:
        m = re.fullmatch(r"\s*([0-9]+(?:[.,][0-9]+)?)\s+([A-Z]{3})\s*", a.tedarik)
        if not m:
            raise SystemExit('HATA: --tedarik "9.4 USD" biçiminde olmalı: %r' % a.tedarik)
        urun["tedarik_fiyati"] = {"tutar": float(m.group(1).replace(",", ".")), "para": m.group(2)}
    elif a.marj_csv:
        if not os.path.exists(a.marj_csv):
            raise SystemExit("HATA: marj dosyası yok: %s" % a.marj_csv)
        with open(a.marj_csv, encoding="utf-8", newline="") as f:
            satirlar = [s for s in csv.DictReader(f) if (s.get("urun") or "").strip().lower() == a.ad.strip().lower()]
        tutar = sayi(satirlar[-1].get("urun_maliyeti")) if satirlar else None
        if tutar:
            urun["tedarik_fiyati"] = {"tutar": tutar, "para": (satirlar[-1].get("para") or para or "").strip().upper()}
        else:
            uyarilar.append("marj.csv'de '%s' satırı (urun_maliyeti) yok: tedarik_fiyati yazılmadı" % a.ad)
    pazar = {"ulke": ulke}
    if dil:
        pazar["dil"] = dil
    if para:
        pazar["para"] = para
    veri = {"surum": "1", "urun": urun, "pazar": pazar}
    rakipler = []
    for r in a.rakip or []:
        marka, url, fiyat = parcala(r, 3, "rakip")
        satir = {"marka": marka}
        if url:
            satir["url"] = url
        if fiyat:
            satir["fiyat"] = sayi_ya_da_metin(fiyat)
        rakipler.append(satir)
    if a.teklif_tsv and os.path.exists(a.teklif_tsv):
        for s in teklif_satirlari(a.teklif_tsv, ulke):
            url = (s.get("kaynak_url") or "").strip()
            if (s.get("tur") or "").strip() == "rakip" and url.startswith("http"):
                satir = {"marka": alan_adi(url), "url": url}
                f = sayi(s.get("fiyat"))
                if f:
                    satir["fiyat"] = f
                rakipler.append(satir)
    if rakipler:
        veri["rakipler"] = rakipler
    kanit = []
    for k in a.kanit or []:
        kaynak, url, tarih, olcu = parcala(k, 4, "kanit")
        satir = {"kaynak": kaynak, "olcu": olcu}
        if url:
            satir["url"] = url
        if tarih:
            satir["tarih"] = tarih
        kanit.append(satir)
    if a.kanit_md:
        if not os.path.exists(a.kanit_md):
            raise SystemExit("HATA: kanıt dosyası yok: %s" % a.kanit_md)
        bulunan = kanit_coz(a.kanit_md)
        if not bulunan:
            uyarilar.append("kanıt dosyasında ölçülü URL satırı bulunamadı: %s" % a.kanit_md)
        kanit += bulunan
    if kanit:
        veri["kanit"] = kanit
    if a.teklif_tsv:
        if not os.path.exists(a.teklif_tsv):
            uyarilar.append("teklif dosyası yok (%s): sabit kural yazıldı" % a.teklif_tsv)
        veri["teklif"] = teklif_kaynagi(a.teklif_tsv, ulke)
        veri["surum"] = "2"
    hatalar, u2 = pd.dogrula("urun", veri)
    uyarilar += u2
    if not veri.get("kanit"):
        uyarilar.append("kanit boş: SAT kararının kanıtı (reklam/satış ölçümü) dosyaya girmedi")
    if not hatalar:
        yaz_json(a.cikti, veri)
        print("yazıldı: sürüm %s · teklif kaynağı: %s · rakip %d · kanıt %d" % (
            veri["surum"], veri.get("teklif", {}).get("kaynak", "yok"), len(veri.get("rakipler", [])), len(veri.get("kanit", []))))
    return rapor(hatalar, uyarilar, a.cikti)


def fiyat(a):
    print(json.dumps(teklif_kaynagi(a.teklif_tsv, pazar_coz(a.pazar)), ensure_ascii=False))
    return 0


# ------------------------------------------------------------------ magaza-oku
def magaza_oku(a):
    pd = dogrulayici()
    try:
        m = pd.yukle(a.dosya)
    except (OSError, ValueError) as e:
        print("HATA: dosya okunamadı ya da geçerli JSON değil: %s" % e)
        return 2
    hatalar, uyarilar = pd.dogrula("magaza", m)
    cikti = a.cikti or os.path.join(os.path.dirname(os.path.abspath(a.dosya)), "marka-kilidi.md")
    if hatalar:
        return rapor(hatalar, uyarilar, a.dosya)
    marka, renk, tip, urun, om, mag = m["marka"], m["renkler"], m["tipografi"], m["urun"], m["onayli_metinler"], m["magaza"]
    ses = marka.get("ses", {})
    link = mag["pdp_url"]
    if mag.get("utm"):
        link += ("&" if "?" in link else "?") + mag["utm"]
    b = tip["baslik"]
    s = ["# Marka kilidi — %s" % marka["ad"], "",
         "Kaynak: `%s` (mağaza kolu, sözleşme sürüm %s). Bu dosya betikle üretilir; elle düzenleme, paketi yeniden oku."
         % (os.path.basename(a.dosya), m["surum"]), "",
         "## Ses (seslendirme, altyazı, caption tonu)"]
    if marka.get("slogan"):
        s.append("- Slogan: %s" % marka["slogan"])
    if ses.get("sifatlar"):
        s.append("- Böyle: %s" % ", ".join(ses["sifatlar"]))
    if ses.get("degil"):
        s.append("- Böyle değil: %s" % ", ".join(ses["degil"]))
    s += ["", "## Renk (altyazı kutusu, kapak, son kare — HEX birebir)", "| Rol | HEX |", "|---|---|"]
    s += ["| %s | `%s` |" % (k, renk[k]) for k in ("zemin", "metin", "ikincil", "kart", "vurgu")]
    s += ["", "## Yazı (mağazayla aynı aile; Google Fonts'ta aynı adla)",
          "- Başlık: %s%s%s" % (b["aile"], " %s" % b["agirlik"] if b.get("agirlik") else "",
                               ", BÜYÜK HARF" if b.get("buyuk_harf") else ""),
          "- Gövde: %s" % tip["govde"]["aile"],
          "", "## Ürün ve link",
          "- Ürün başlığı: %s" % urun["baslik"],
          "- Fiyat: %s %s (organik videoda ekrana yazılmaz; caption/bio/ürün sayfası)" % (urun["fiyat"], urun["para"])]
    if urun.get("varyantlar"):
        s.append("- Varyantlar: %s" % ", ".join(v if isinstance(v, str) else str(v.get("ad", v)) for v in urun["varyantlar"]))
    s += ["- Link (CTA, bio, DM): %s" % link,
          "  - `utm_source=` değeri yayın kanalına göre yazılır (instagram, tiktok, meta-reklam).",
          "", "## Söylenebilecekler (YALNIZ bunlar; listede olmayan iddia senaryoya, ekran yazısına, caption'a girmez)"]
    s += ["- Fayda: %s" % f for f in om["faydalar"]]
    for d in om["iddialar"]:
        s.append("- İddia: %s%s%s" % (d["metin"], " (kaynak: %s)" % d["kaynak"] if d.get("kaynak") else "",
                                     " — bilgi notuyla birlikte kullanılır" if d["bilgi_notu"] else ""))
    if om.get("g1_baslik"):
        s.append("- Onaylı başlık satırları: %s" % " / ".join(om["g1_baslik"]))
    g0 = [g for g in m["gorseller"] if g["kod"] == "G0"]
    s += ["", "## Ürün referansı (başlangıç kareleri için)"]
    if g0:
        s.append("- G0 temiz ürün karesi: `%s`%s → `is/NN/referans/` içine kopyalanır; ürün bu kareye göre kilitlenir."
                 % (g0[0]["dosya"], " (%s)" % g0[0]["olcu"] if g0[0].get("olcu") else ""))
    else:
        s.append("- G0 yok: ürün fotoğrafı kullanıcıdan istenir.")
    if m.get("logo", {}).get("dosya"):
        s.append("- Logo (yalnız son kare): `%s`%s" % (m["logo"]["dosya"], " (%s)" % m["logo"]["tur"] if m["logo"].get("tur") else ""))
    if mag.get("tema_modu"):
        s.append("- Tema modu: %s" % mag["tema_modu"])
    os.makedirs(os.path.dirname(os.path.abspath(cikti)), exist_ok=True)
    with open(cikti, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(s) + "\n")
    if a.cikti_dizin:
        ayar = {
            "kaynak": os.path.abspath(a.dosya),
            "marka": marka["ad"],
            "yazi": {"baslik_aile": b["aile"], "baslik_agirlik": b.get("agirlik"),
                     "buyuk_harf": b.get("buyuk_harf", False), "govde_aile": tip["govde"]["aile"]},
            "renkler": renk,
            "urun_referansi": g0[0]["dosya"] if g0 else None,
            "logo": m.get("logo", {}).get("dosya"),
            "link": link,
            "iddialar": [i["metin"] for i in om["iddialar"]],
            "faydalar": om.get("faydalar", []),
        }
        yaz_json(os.path.join(a.cikti_dizin, "video-ayar.json"), ayar)
        with open(os.path.join(a.cikti_dizin, "onayli-iddialar.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("# Videoda YALNIZ bu iddialar söylenir/yazılır. Kaynak: magaza-paketi.json onayli_metinler.iddialar\n")
            f.write("\n".join(ayar["iddialar"]) + ("\n" if ayar["iddialar"] else ""))
        print("yazıldı: %s/video-ayar.json, onayli-iddialar.txt" % a.cikti_dizin)
    return rapor(hatalar, uyarilar, cikti)


# ------------------------------------------------------------------ iddia kapısı (kurgu_kontrol.py da kullanır)
def norm(metin):
    t = unicodedata.normalize("NFKC", metin).replace("İ", "i").replace("I", "ı").lower()
    t = re.sub(r"[^\w%]+", " ", t, flags=re.UNICODE)
    return re.sub(r"\s+", " ", t).strip()


# İddia sinyali: sayı (+ birim/yüzde) ya da sonuç/üstünlük sözcüğü. Sinyalsiz satır (ör. "bunu izle") iddia sayılmaz.
IDDIA_SINYAL = re.compile(
    r"\d|%|\b(garanti\w*|kanıtl\w*|kanitl\w*|klinik\w*|onayl\w*|sertifika\w*|tescil\w*|patent\w*|en iyi|en hızlı|en hizli|"
    r"en güçlü|en guclu|tek ürün|tek urun|ilk ve tek|doktor\w*|uzman\w* öner\w*|tedavi\w*|iyileştir\w*|iyilestir\w*|"
    r"geçir\w*|gecir\w*|önle\w*|onle\w*|su geçirmez|su gecirmez|waterproof|guarantee\w*|proven|clinically|certified|"
    r"best|fastest|strongest|cures?|heals?|prevents?|doctor\w*|#1|no\.? ?1)\b", re.I)


def onayli_liste(paket):
    om = paket.get("onayli_metinler", {})
    liste = [i["metin"] for i in om.get("iddialar", [])]
    liste += om.get("faydalar", []) + om.get("g1_baslik", [])
    for v in (om.get("b2") or {}).values():
        if isinstance(v, str):
            liste.append(v)
    if paket.get("marka", {}).get("slogan"):
        liste.append(paket["marka"]["slogan"])
    return [norm(x) for x in liste if isinstance(x, str) and x.strip()]


def iddia_ihlalleri(paket, satirlar):
    """satirlar: [(kaynak, metin)]. Onaylı listede karşılığı olmayan iddia satırlarını döndürür."""
    onayli = onayli_liste(paket)
    u = paket.get("urun", {})
    serbest = [norm(v) for v in (u.get("baslik"), paket.get("marka", {}).get("ad")) if v]  # ürün/marka adı iddia değil
    ihlal = []
    fiyat_ = sayi(str(u.get("fiyat"))) if u.get("fiyat") is not None else None
    for kaynak, metin in satirlar:
        n = norm(metin)
        if not n or n in serbest:
            continue
        sinyal = metin
        if fiyat_:  # mağazadaki fiyatın birebir yazılması iddia değildir (para dosyadan taşınır)
            sinyal = "".join(p for p in re.split(r"(\d+(?:[.,]\d+)?)", metin)
                             if not (re.fullmatch(r"\d+(?:[.,]\d+)?", p) and sayi(p) == fiyat_))
        if not IDDIA_SINYAL.search(sinyal):
            continue
        if any(n == o or n in o or o in n for o in onayli):
            continue
        ihlal.append((kaynak, metin.strip()))
    return ihlal


YAZI_ANAHTAR = {"yazi", "satir1", "satir2", "altyazi", "metin", "baslik", "cta"}


def ayar_yazilari(veri, yol=""):
    """Kurgu ayar JSON'undaki ekrana basılan metinler (anahtar adına göre, iç içe)."""
    out = []
    if isinstance(veri, dict):
        for k, v in veri.items():
            if isinstance(v, str) and k in YAZI_ANAHTAR:
                out.append(("%s.%s" % (yol, k) if yol else k, v))
            else:
                out += ayar_yazilari(v, "%s.%s" % (yol, k) if yol else k)
    elif isinstance(veri, list):
        for i, v in enumerate(veri):
            out += ayar_yazilari(v, "%s[%d]" % (yol, i))
    return out


def metin_satirlari(yol):
    if yol.endswith(".json"):
        return [("%s:%s" % (os.path.basename(yol), k), v) for k, v in ayar_yazilari(oku_json(yol))]
    with open(yol, encoding="utf-8") as f:
        return [("%s:%d" % (os.path.basename(yol), i), s) for i, s in enumerate(f.read().splitlines(), 1)
                if s.strip() and not s.lstrip().startswith("#")]


def iddia_kontrol(a):
    paket = oku_json(a.paket)
    hatalar = sema_hatalari("magaza", paket)
    if hatalar:
        return rapor(hatalar, [], a.paket)
    satirlar = []
    for y in a.metin:
        if not os.path.exists(y):
            raise SystemExit("HATA: dosya yok: %s" % y)
        satirlar += metin_satirlari(y)
    ihlal = iddia_ihlalleri(paket, satirlar)
    for kaynak, metin in ihlal:
        print("HATA: [iddia] %s: \"%s\" onaylı listede yok (onayli_metinler.iddialar)" % (kaynak, metin))
    print("iddia kontrolü: %d satır okundu, %d ihlal → %s" % (len(satirlar), len(ihlal), "KALDI" if ihlal else "GEÇTİ"))
    return 1 if ihlal else 0


# ------------------------------------------------------------------ video-yaz / video-sec
def olc(yol):
    """(genişlik, yükseklik, süre sn) ya da None. ffprobe; yoksa ffmpeg -i çıktısı."""
    fp = shutil.which("ffprobe")
    if fp:
        r = subprocess.run([fp, "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height:format=duration", "-of", "json", yol], capture_output=True, text=True)
        try:
            j = json.loads(r.stdout)
            return int(j["streams"][0]["width"]), int(j["streams"][0]["height"]), float(j["format"]["duration"])
        except (ValueError, KeyError, IndexError):
            return None
    ff = shutil.which("ffmpeg")
    if not ff:
        try:
            import imageio_ffmpeg
            ff = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:  # noqa: BLE001
            return None
    cikti = subprocess.run([ff, "-hide_banner", "-i", yol], capture_output=True, text=True, errors="replace").stderr
    sure = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", cikti)
    boyut = re.search(r"Video:.*?\b(\d{3,5})x(\d{3,5})\b", cikti)
    if not (sure and boyut):
        return None
    return int(boyut.group(1)), int(boyut.group(2)), int(sure.group(1)) * 3600 + int(sure.group(2)) * 60 + float(sure.group(3))


def _ilk_var(*yollar):
    return next((y for y in yollar if y and os.path.exists(y)), None)


def video_yaz(a):
    pd = dogrulayici()
    elle = {}
    for o in a.olcum or []:
        m = re.fullmatch(r"(.+)=(\d+x\d+):(\d+(?:\.\d+)?)", o.strip())
        if not m:
            raise SystemExit('HATA: --olcum "V01.mp4=1080x1920:12.4" biçiminde olmalı: %r' % o)
        elle[m.group(1)] = (m.group(2), float(m.group(3)))
    dosyalar = sorted(set([os.path.basename(p) for p in glob.glob(os.path.join(a.klasor, "*.mp4"))] + list(elle)))
    if not dosyalar:
        print("HATA: %s içinde .mp4 yok (ve --olcum verilmedi)" % a.klasor)
        return 1
    govdeler = {os.path.splitext(d)[0] for d in dosyalar}
    for ad in (a.pdp or []) + (a.hero or []):
        if os.path.splitext(ad)[0] not in govdeler:
            raise SystemExit("HATA: --pdp/--hero ile verilen video klasörde yok: %s" % ad)
    pdp = {os.path.splitext(x)[0] for x in a.pdp or []}
    hero = {os.path.splitext(x)[0] for x in a.hero or []}
    liste, hatalar = [], []
    for d in dosyalar:
        if d in elle:
            olcu, sure = elle[d]
        else:
            o = olc(os.path.join(a.klasor, d))
            if o is None:
                hatalar.append('%s ölçülemedi (ffmpeg/ffprobe yok ya da dosya bozuk); --olcum "%s=GxY:sn" ver' % (d, d))
                continue
            olcu, sure = "%dx%d" % (o[0], o[1]), round(o[2], 2)
        g = os.path.splitext(d)[0]
        satir = {"dosya": d, "olcu": olcu, "sure_sn": sure,
                 "kullanim": "hero" if g in hero else ("pdp-galeri" if g in pdp else "reklam")}
        if a.dil:
            satir["altyazi_dili"] = None if a.dil == "yok" else a.dil
        liste.append(satir)
    cikti = a.cikti or os.path.join(a.klasor, "video-paketi.json")
    uyarilar = []
    if not hatalar:
        ust = os.path.dirname(os.path.abspath(a.klasor))
        hedef = os.path.dirname(os.path.abspath(cikti))
        urun_yol = a.urun or _ilk_var(*[os.path.join(k, "urun-paketi.json") for k in (hedef, ust, os.path.join(ust, "magaza"))])
        magaza_yol = a.magaza or _ilk_var(*[os.path.join(k, "magaza-paketi.json") for k in (hedef, ust, os.path.join(ust, "magaza"))])
        if urun_yol and magaza_yol and os.path.exists(urun_yol) and os.path.exists(magaza_yol):
            hatalar, uyarilar = pd.zincir(pd.yukle(urun_yol), pd.yukle(magaza_yol), liste)
        else:
            hatalar, uyarilar = pd.dogrula("video", liste)
            uyarilar.append("zincir kontrolü yapılmadı (urun-paketi.json ve magaza-paketi.json birlikte bulunamadı)")
    if not hatalar:
        yaz_json(cikti, liste)
        print("yazıldı: %s (%d video; mağazaya yüklenecek: %d)" % (
            cikti, len(liste), sum(1 for k in liste if k["kullanim"] in pd.YUKLENEN)))
    return rapor(hatalar, uyarilar, cikti)


def video_sec(a):
    pd = dogrulayici()
    liste = oku_json(a.paket)
    hatalar = sema_hatalari("video", liste)
    if hatalar:
        return rapor(hatalar, [], a.paket)
    sec = [k for k in liste if k["kullanim"] in pd.YUKLENEN]
    for k in sec:
        print("%s\t%s\t%s\t%s sn" % (k["kullanim"], k["dosya"], k["olcu"], k["sure_sn"]))
    print("mağazaya yüklenecek: %d / %d (reklam videoları yüklenmez; galeride G0'ın yerini almaz)" % (len(sec), len(liste)))
    return 0


def dogrula_komut(a):
    pd = dogrulayici()
    return pd.main(["paket_dogrula.py", a.tur] + a.dosya)


def main():
    for akis in (sys.stdout, sys.stderr):
        if hasattr(akis, "reconfigure"):
            akis.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut", required=True)
    d = alt.add_parser("dogrula")
    d.add_argument("tur", choices=["urun", "magaza", "video", "zincir"])
    d.add_argument("dosya", nargs="+")
    d.set_defaults(is_=dogrula_komut)
    u = alt.add_parser("urun-yaz")
    u.add_argument("--cikti", required=True)
    u.add_argument("--ad", required=True)
    u.add_argument("--foto", action="append", required=True)
    for ad in ("ulke", "pazar", "dil", "para", "nis", "nis-kodu", "tedarik", "marj-csv", "kanit-md", "teklif-tsv"):
        u.add_argument("--" + ad)
    for ad in ("ozellik", "varyant", "rakip", "kanit"):
        u.add_argument("--" + ad, action="append")
    u.set_defaults(is_=urun_yaz)
    f = alt.add_parser("fiyat")
    f.add_argument("--teklif-tsv")
    f.add_argument("--pazar", default="US")
    f.set_defaults(is_=fiyat)
    m = alt.add_parser("magaza-oku")
    m.add_argument("dosya")
    m.add_argument("--cikti")
    m.add_argument("--cikti-dizin")
    m.set_defaults(is_=magaza_oku)
    i = alt.add_parser("iddia-kontrol")
    i.add_argument("paket")
    i.add_argument("metin", nargs="+")
    i.set_defaults(is_=iddia_kontrol)
    v = alt.add_parser("video-yaz")
    v.add_argument("klasor")
    for ad in ("pdp", "hero", "olcum"):
        v.add_argument("--" + ad, action="append")
    for ad in ("dil", "urun", "magaza", "cikti"):
        v.add_argument("--" + ad)
    v.set_defaults(is_=video_yaz)
    s = alt.add_parser("video-sec")
    s.add_argument("paket")
    s.set_defaults(is_=video_sec)
    a = ap.parse_args()
    return a.is_(a)


if __name__ == "__main__":
    sys.exit(main())
