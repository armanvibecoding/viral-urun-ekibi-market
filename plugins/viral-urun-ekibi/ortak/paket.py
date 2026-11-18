#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mağaza Kurucu ile dosya alışverişi (arayüz sözleşmesi sürüm 1). Yalnız standart kütüphane.

  ürün bulundu (SAT)  -> urun-yaz   -> is/NN-urun/urun-paketi.json   (Mağaza Kurucu'nun girdisi)
  mağaza kuruldu      -> magaza-oku -> is/NN-urun/marka-kilidi.md    (video ekibinin okuduğu özet)
  videolar teslim     -> video-yaz  -> is/NN-urun/teslim/video-paketi.json (Mağaza Kurucu'ya geri dönüş)

Kullanım:
  python3 paket.py urun-yaz --cikti is/NN/urun-paketi.json --ad "<tedarikçideki ad>" --foto <dosya|URL> --ulke TR
          [--dil tr] [--para TRY] [--nis nis-gadget] [--tedarik "9.4 USD"]
          [--ozellik "ad|deger|birim|kaynak"]... [--varyant "Gri|var"]... [--rakip "marka|url|fiyat"]...
          [--kanit "kaynak|url|YYYY-AA-GG|ölçü"]...
  python3 paket.py magaza-oku is/NN/magaza-paketi.json [--cikti is/NN/marka-kilidi.md]
  python3 paket.py video-yaz is/NN/teslim [--pdp V02]... [--hero V03]... [--dil tr|yok]
          [--olcum "V01.mp4=1080x1920:12.4"]... [--urun <urun-paketi.json>] [--magaza <magaza-paketi.json>]

Şema ve doğrulayıcı yandaki sozlesme/ klasöründedir (Mağaza Kurucu ile bayt bayt aynı; burada düzenlenmez).
Bilinmeyen alan YAZILMAZ: verilmeyen seçenek dosyaya girmez, uydurulmaz. Çıkış: 0 geçti, 1 hata, 2 kullanım.
"""
import argparse
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))


def dogrulayici():
    yol = os.path.join(BURASI, "sozlesme", "paket_dogrula.py")
    if not os.path.exists(yol):
        raise SystemExit("HATA: doğrulayıcı yok: %s" % yol)
    spec = importlib.util.spec_from_file_location("paket_dogrula", yol)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


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


# ------------------------------------------------------------------ urun-yaz
def urun_yaz(a):
    pd = dogrulayici()
    urun = {"ad": a.ad, "fotograflar": a.foto}
    if a.nis:
        urun["nis"] = a.nis
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
    pazar = {"ulke": a.ulke}
    if a.dil:
        pazar["dil"] = a.dil
    if a.para:
        pazar["para"] = a.para
    veri = {"surum": "1", "urun": urun, "pazar": pazar}
    if a.rakip:
        veri["rakipler"] = []
        for r in a.rakip:
            marka, url, fiyat = parcala(r, 3, "rakip")
            satir = {"marka": marka}
            if url:
                satir["url"] = url
            if fiyat:
                satir["fiyat"] = sayi_ya_da_metin(fiyat)
            veri["rakipler"].append(satir)
    if a.kanit:
        veri["kanit"] = []
        for k in a.kanit:
            kaynak, url, tarih, olcu = parcala(k, 4, "kanit")
            satir = {"kaynak": kaynak, "olcu": olcu}
            if url:
                satir["url"] = url
            if tarih:
                satir["tarih"] = tarih
            veri["kanit"].append(satir)
    hatalar, uyarilar = pd.dogrula("urun", veri)
    if not veri.get("kanit"):
        uyarilar.append("kanit boş: SAT kararının kanıtı (reklam/satış ölçümü) dosyaya girmedi")
    if not hatalar:
        yaz_json(a.cikti, veri)
    return rapor(hatalar, uyarilar, a.cikti)


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
         "Kaynak: `%s` (Mağaza Kurucu, sözleşme sürüm %s). Bu dosya betikle üretilir; elle düzenleme, paketi yeniden oku."
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
    os.makedirs(os.path.dirname(os.path.abspath(cikti)), exist_ok=True)
    with open(cikti, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(s) + "\n")
    return rapor(hatalar, uyarilar, cikti)


# ------------------------------------------------------------------ video-yaz
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
    cikti = os.path.join(a.klasor, "video-paketi.json")
    uyarilar = []
    if not hatalar:
        ust = os.path.dirname(os.path.abspath(a.klasor))
        urun_yol = a.urun or os.path.join(ust, "urun-paketi.json")
        magaza_yol = a.magaza or os.path.join(ust, "magaza-paketi.json")
        if os.path.exists(urun_yol) and os.path.exists(magaza_yol):
            hatalar, uyarilar = pd.zincir(pd.yukle(urun_yol), pd.yukle(magaza_yol), liste)
        else:
            hatalar, uyarilar = pd.dogrula("video", liste)
            uyarilar.append("zincir kontrolü yapılmadı (urun-paketi.json ve magaza-paketi.json birlikte bulunamadı)")
    if not hatalar:
        yaz_json(cikti, liste)
    return rapor(hatalar, uyarilar, cikti)


def main():
    for akis in (sys.stdout, sys.stderr):
        if hasattr(akis, "reconfigure"):
            akis.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Mağaza Kurucu ile dosya alışverişi (urun-paketi / magaza-paketi / video-paketi)")
    alt = ap.add_subparsers(dest="komut", required=True)
    u = alt.add_parser("urun-yaz")
    u.add_argument("--cikti", required=True)
    u.add_argument("--ad", required=True)
    u.add_argument("--foto", action="append", required=True)
    u.add_argument("--ulke", required=True)
    for ad in ("dil", "para", "nis", "tedarik"):
        u.add_argument("--" + ad)
    for ad in ("ozellik", "varyant", "rakip", "kanit"):
        u.add_argument("--" + ad, action="append")
    u.set_defaults(is_=urun_yaz)
    m = alt.add_parser("magaza-oku")
    m.add_argument("dosya")
    m.add_argument("--cikti")
    m.set_defaults(is_=magaza_oku)
    v = alt.add_parser("video-yaz")
    v.add_argument("klasor")
    for ad in ("pdp", "hero", "olcum"):
        v.add_argument("--" + ad, action="append")
    for ad in ("dil", "urun", "magaza"):
        v.add_argument("--" + ad)
    v.set_defaults(is_=video_yaz)
    a = ap.parse_args()
    return a.is_(a)


if __name__ == "__main__":
    sys.exit(main())
