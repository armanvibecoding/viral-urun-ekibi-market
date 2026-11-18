#!/usr/bin/env python3
"""Köprü dosyaları: urun-paketi.json (ürün ekibi -> mağaza), magaza-paketi.json (mağaza -> video),
video-paketi.json (video -> mağaza). Yalnız standart kütüphane. Şema: sema.json (bu klasör).

Komutlar (çıkış 0 = tamam, 1 = hata/ihlal, 2 = kullanım hatası):
  paket.py dogrula urun|magaza|video DOSYA
  paket.py urun-yaz --cikti is/NN-urun/magaza/urun-paketi.json --ad AD --nis KOD --pazar US --foto F [--foto F2 ...]
                    [--marj-csv is/firsat/marj.csv] [--teklif-tsv is/NN-urun/teklif/teklif.tsv]
                    [--kanit-md is/firsat/kanit/NN-urun.md] [--ozellik "ad=deger|birim|kaynakURL" ...] [--varyant AD ...]
  paket.py fiyat [--teklif-tsv F] [--pazar US]        teklifin TEK kaynağını söyler (bizim satırı > sabit kural)
  paket.py magaza-oku MAGAZA-PAKETI.json [--cikti-dizin is/NN-urun/kurgu]
                    video tarafı için: video-ayar.json + onayli-iddialar.txt yazar
  paket.py iddia-kontrol MAGAZA-PAKETI.json METIN_ya_da_AYAR.json [...]
                    videoda/altyazıda geçen iddia onaylı listede değilse çıkış 1
  paket.py video-yaz --cikti is/NN-urun/magaza/video-paketi.json --video DOSYA:kullanim[:dil[:GENxYUK:sure_sn]] [...]
  paket.py video-sec VIDEO-PAKETI.json                 mağazaya yüklenecekler (yalnız pdp-galeri ve hero)

Kurallar (arayüz sözleşmesi): sözleşme dışı alan yazılmaz · eksik zorunlu alan uydurulmaz (çıkış 1) · para, fiyat ve
onaylı metin birebir taşınır · video yalnız onayli_metinler.iddialar listesini söyler.
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from urllib.parse import urlparse

BURASI = os.path.dirname(os.path.abspath(__file__))
SEMA = json.load(open(os.path.join(BURASI, "sema.json"), encoding="utf-8"))
TUR_AD = {"urun": "urun-paketi", "magaza": "magaza-paketi", "video": "video-paketi"}
SURUM = "2"
# Sabit paket kuralı (mağaza aşamasının varsayılanı). Teklifte `bizim` satırı varsa KULLANILMAZ.
SABIT_PAKETLER = [{"adet": 1, "indirim_yuzde": 0}, {"adet": 2, "indirim_yuzde": 10}, {"adet": 3, "indirim_yuzde": 18}]
PAZAR = {  # ISO-3166 ülke -> (dil, para). UK girilirse GB'ye çevrilir.
    "US": ("en", "USD"), "TR": ("tr", "TRY"), "GB": ("en", "GBP"), "DE": ("de", "EUR"), "FR": ("fr", "EUR"),
    "ES": ("es", "EUR"), "IT": ("it", "EUR"), "NL": ("nl", "EUR"), "CA": ("en", "CAD"), "AU": ("en", "AUD"),
}
PAZAR_AD = {"ABD": "US", "USA": "US", "UK": "GB", "TÜRKİYE": "TR", "TURKIYE": "TR", "İNGİLTERE": "GB", "ALMANYA": "DE",
            "FRANSA": "FR", "İSPANYA": "ES", "KANADA": "CA"}


def hata_cik(m, kod=1):
    print("HATA: " + m, file=sys.stderr)
    sys.exit(kod)


def oku_json(yol):
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except OSError:
        hata_cik("dosya yok ya da okunamadı: " + yol)
    except json.JSONDecodeError as e:
        hata_cik("JSON bozuk: %s (%s)" % (yol, e))


def yaz_json(yol, veri):
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ---------- doğrulama ----------
def _tur_tamam(v, tur):
    if tur == "metin":
        return isinstance(v, str) and v.strip() != ""
    if tur == "sayi":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if tur == "tamsayi":
        return isinstance(v, int) and not isinstance(v, bool)
    if tur == "mantik":
        return isinstance(v, bool)
    if tur == "nesne":
        return isinstance(v, dict)
    if tur == "liste":
        return isinstance(v, list)
    return False


def _dogrula(v, s, yol, surum, hatalar):
    tur = s["tur"]
    if not _tur_tamam(v, tur):
        hatalar.append("%s: tür %s olmalı (gelen: %s)" % (yol, tur, json.dumps(v, ensure_ascii=False)[:60]))
        return
    if "secenek" in s and v not in s["secenek"]:
        hatalar.append("%s: '%s' geçersiz (seçenekler: %s)" % (yol, v, ", ".join(s["secenek"])))
    if "desen" in s and not re.search(s["desen"], v):
        hatalar.append("%s: '%s' biçime uymuyor (%s)" % (yol, v, s["desen"]))
    if "buyuktur" in s and not v > s["buyuktur"]:
        hatalar.append("%s: %s > %s olmalı" % (yol, v, s["buyuktur"]))
    if tur == "liste":
        if len(v) < s.get("en_az", 0):
            hatalar.append("%s: en az %d öğe gerekli" % (yol, s["en_az"]))
        for i, o in enumerate(v):
            _dogrula(o, s["oge"], "%s[%d]" % (yol, i), surum, hatalar)
    if tur == "nesne":
        alanlar = s.get("alanlar", {})
        for ad, alt in alanlar.items():
            if ad not in v:
                if alt.get("zorunlu"):
                    hatalar.append("%s.%s: zorunlu alan eksik" % (yol, ad))
                continue
            if alt.get("surum") and surum is not None and surum < alt["surum"]:
                hatalar.append("%s.%s: bu alan surum %s ile geldi; dosyada surum %s yazıyor" % (yol, ad, alt["surum"], surum))
            _dogrula(v[ad], alt, "%s.%s" % (yol, ad), surum, hatalar)
        if not s.get("serbest"):
            for ad in v:
                if ad not in alanlar:
                    hatalar.append("%s.%s: sözleşme dışı alan" % (yol, ad))


def dogrula(tur, veri):
    """Hata listesi döner (boş = geçerli)."""
    s = SEMA[TUR_AD[tur]]
    hatalar = []
    surum = veri.get("surum") if isinstance(veri, dict) else None
    _dogrula(veri, s, TUR_AD[tur], surum if isinstance(surum, str) else None, hatalar)
    return hatalar


# ---------- ürün paketi ----------
def pazar_coz(kod):
    k = kod.strip().upper()
    k = PAZAR_AD.get(k, k)
    if k not in PAZAR:
        hata_cik("pazar tanınmadı: %s (ISO kodu ver: %s)" % (kod, ", ".join(sorted(PAZAR))))
    return k


def nis_coz(kod):
    if re.match(r"^nis-[a-z]+$", kod):
        return kod, None
    tablo = {}
    with open(os.path.join(BURASI, "nis-esleme.tsv"), encoding="utf-8") as f:
        for satir in f:
            if satir.startswith("#") or not satir.strip() or satir.startswith("kod\t"):
                continue
            a, b = satir.rstrip("\n").split("\t")
            tablo[a] = b
    if kod in tablo:
        return tablo[kod], None
    return "nis-gadget", "niş kodu '%s' eşleme tablosunda yok; nis-gadget yazıldı (nis-esleme.tsv)" % kod


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


def teklif_satirlari(yol, pazar=None):
    with open(yol, encoding="utf-8", newline="") as f:
        satirlar = list(csv.DictReader(f, delimiter="\t"))
    if pazar:
        esdeger = {pazar, "UK" if pazar == "GB" else pazar}
        satirlar = [s for s in satirlar if (s.get("pazar") or "").strip().upper() in esdeger]
    return satirlar


def paket_coz(metin):
    """teklif.tsv `paket` sütunu ('1x;2x:-15%;3x:-25%') -> [{adet, indirim_yuzde}] ; okunamayan parça atlanır."""
    out = []
    for parca in (metin or "").split(";"):
        m = re.match(r"^\s*(\d+)\s*x\s*(?::\s*-?\s*(\d+(?:[.,]\d+)?)\s*%)?\s*$", parca)
        if m:
            out.append({"adet": int(m.group(1)), "indirim_yuzde": float((m.group(2) or "0").replace(",", "."))})
    for p in out:
        if p["indirim_yuzde"] == int(p["indirim_yuzde"]):
            p["indirim_yuzde"] = int(p["indirim_yuzde"])
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
                t["para"] = (b.get("para") or PAZAR[pazar][1]).strip().upper()
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
    """Kanıt dosyasındaki URL'li satırlar -> kanit[]. Tarih satırda yoksa dosyadaki ilk tarih; o da yoksa alan yazılmaz."""
    metin = open(yol, encoding="utf-8").read()
    genel = re.search(r"\d{4}-\d{2}-\d{2}", metin)
    out, gorulen = [], set()
    for satir in metin.splitlines():
        for url in re.findall(r"https?://[^\s)|>\]]+", satir):
            url = url.rstrip(".,;")
            if url in gorulen:
                continue
            gorulen.add(url)
            k = {"kaynak": alan_adi(url), "url": url}
            t = re.search(r"\d{4}-\d{2}-\d{2}", satir) or genel
            if t:
                k["tarih"] = t.group(0)
            olcu = re.sub(r"https?://[^\s)|>\]]+", "", satir)
            olcu = re.sub(r"[|*`#\[\]()]", " ", olcu)
            olcu = re.sub(r"\s+", " ", olcu).strip(" -:·")
            if olcu:
                k["olcu"] = olcu[:160]
            out.append(k)
    return out


def urun_yaz(a):
    pazar = pazar_coz(a.pazar)
    nis, uyari = nis_coz(a.nis)
    uyarilar = [uyari] if uyari else []
    dil, para = PAZAR[pazar]
    urun = {"ad": a.ad, "nis": nis, "fotograflar": list(a.foto or [])}
    ozellikler = []
    for o in a.ozellik or []:
        ad, _, kalan = o.partition("=")
        parca = (kalan.split("|") + ["", ""])[:3]
        oz = {"ad": ad.strip(), "deger": parca[0].strip()}
        if parca[1].strip():
            oz["birim"] = parca[1].strip()
        if parca[2].strip():
            oz["kaynak"] = parca[2].strip()
        else:
            uyarilar.append("özellik '%s' kaynaksız: mağaza tarafında doğrulanmış SAYILMAZ" % oz["ad"])
        ozellikler.append(oz)
    if ozellikler:
        urun["ozellikler"] = ozellikler
    if a.varyant:
        urun["varyantlar"] = [{"ad": v, "stok": True} for v in a.varyant]
    if a.marj_csv:
        if not os.path.exists(a.marj_csv):
            hata_cik("marj dosyası yok: " + a.marj_csv)
        with open(a.marj_csv, encoding="utf-8", newline="") as f:
            satirlar = [s for s in csv.DictReader(f) if (s.get("urun") or "").strip().lower() == a.ad.strip().lower()]
        if satirlar:
            s = satirlar[-1]
            tutar = sayi(s.get("urun_maliyeti"))
            if tutar:
                urun["tedarik_fiyati"] = {"tutar": tutar, "para": (s.get("para") or para).strip().upper()}
        else:
            uyarilar.append("marj.csv'de '%s' satırı yok: tedarik_fiyati yazılmadı" % a.ad)
    paket = {"surum": SURUM, "urun": urun, "pazar": {"ulke": pazar, "dil": dil, "para": para}}
    if a.teklif_tsv and os.path.exists(a.teklif_tsv):
        rakipler = []
        for s in teklif_satirlari(a.teklif_tsv, pazar):
            url = (s.get("kaynak_url") or "").strip()
            if (s.get("tur") or "").strip() == "rakip" and url.startswith("http"):
                r = {"marka": alan_adi(url), "url": url}
                f = sayi(s.get("fiyat"))
                if f:
                    r["fiyat"] = f
                rakipler.append(r)
        if rakipler:
            paket["rakipler"] = rakipler
    if a.kanit_md:
        if not os.path.exists(a.kanit_md):
            hata_cik("kanıt dosyası yok: " + a.kanit_md)
        k = kanit_coz(a.kanit_md)
        if k:
            paket["kanit"] = k
        else:
            uyarilar.append("kanıt dosyasında URL bulunamadı: kanit[] yazılmadı")
    paket["teklif"] = teklif_kaynagi(a.teklif_tsv, pazar)
    hatalar = dogrula("urun", paket)
    if hatalar:
        for h in hatalar:
            print("HATA  " + h)
        print("urun-paketi YAZILMADI (eksik alan uydurulmaz): %d hata" % len(hatalar))
        return 1
    yaz_json(a.cikti, paket)
    for u in uyarilar:
        print("UYARI " + u)
    print("yazıldı: %s · teklif kaynağı: %s · rakip %d · kanıt %d" % (
        a.cikti, paket["teklif"]["kaynak"], len(paket.get("rakipler", [])), len(paket.get("kanit", []))))
    return 0


# ---------- mağaza paketi -> video ----------
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
    serbest = []  # iddia değil: fiyat ve ürün/marka adı dosyadan birebir geliyorsa serbest
    u = paket.get("urun", {})
    for v in (u.get("baslik"), paket.get("marka", {}).get("ad")):
        if v:
            serbest.append(norm(v))
    ihlal = []
    fiyat = u.get("fiyat")
    for kaynak, metin in satirlar:
        n = norm(metin)
        if not n or n in serbest:
            continue
        sinyal = metin
        if fiyat:  # mağazadaki fiyatın birebir yazılması iddia değildir (para dosyadan taşınır)
            sinyal = "".join(p for p in re.split(r"(\d+(?:[.,]\d+)?)", metin)
                             if not (re.fullmatch(r"\d+(?:[.,]\d+)?", p) and sayi(p) == float(fiyat)))
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
    hatalar = dogrula("magaza", paket)
    if hatalar:
        for h in hatalar:
            print("HATA  " + h)
        return 1
    satirlar = []
    for y in a.metin:
        if not os.path.exists(y):
            hata_cik("dosya yok: " + y)
        satirlar += metin_satirlari(y)
    ihlal = iddia_ihlalleri(paket, satirlar)
    for kaynak, metin in ihlal:
        print("HATA  [iddia] %s: \"%s\" onaylı listede yok (onayli_metinler.iddialar)" % (kaynak, metin))
    print("iddia kontrolü: %d satır okundu, %d ihlal → %s" % (len(satirlar), len(ihlal), "KALDI" if ihlal else "GEÇTİ"))
    return 1 if ihlal else 0


def magaza_oku(a):
    paket = oku_json(a.paket)
    hatalar = dogrula("magaza", paket)
    if hatalar:
        for h in hatalar:
            print("HATA  " + h)
        print("magaza-paketi geçersiz: %d hata (eksik alan uydurulmaz; mağaza aşamasına geri dön)" % len(hatalar))
        return 1
    g0 = next((g for g in paket.get("gorseller", []) if g.get("kod") == "G0"), None)
    m = paket.get("magaza", {})
    link = m.get("pdp_url") or paket["urun"].get("url")
    if link and m.get("utm"):
        link += ("&" if "?" in link else "?") + m["utm"]
    ayar = {
        "kaynak": os.path.abspath(a.paket),
        "marka": paket["marka"]["ad"],
        "yazi": {"baslik_aile": paket["tipografi"]["baslik"]["aile"],
                 "baslik_agirlik": paket["tipografi"]["baslik"].get("agirlik"),
                 "buyuk_harf": paket["tipografi"]["baslik"].get("buyuk_harf", False),
                 "govde_aile": paket["tipografi"]["govde"]["aile"]},
        "renkler": paket["renkler"],
        "urun_referansi": g0["dosya"] if g0 else None,
        "logo": paket.get("logo", {}).get("dosya"),
        "link": link,
        "iddialar": [i["metin"] for i in paket["onayli_metinler"]["iddialar"]],
        "faydalar": paket["onayli_metinler"].get("faydalar", []),
    }
    print("marka: %s · başlık yazısı: %s · gövde: %s" % (ayar["marka"], ayar["yazi"]["baslik_aile"], ayar["yazi"]["govde_aile"]))
    print("renkler: zemin %s · metin %s · vurgu %s" % (paket["renkler"]["zemin"], paket["renkler"]["metin"], paket["renkler"]["vurgu"]))
    print("ürün referansı (G0): %s" % (ayar["urun_referansi"] or "YOK — kilit için ürün fotoğrafı kullanılır"))
    print("onaylı iddia: %d · link: %s" % (len(ayar["iddialar"]), link or "yok"))
    if a.cikti_dizin:
        yaz_json(os.path.join(a.cikti_dizin, "video-ayar.json"), ayar)
        with open(os.path.join(a.cikti_dizin, "onayli-iddialar.txt"), "w", encoding="utf-8") as f:
            f.write("# Videoda YALNIZ bu iddialar söylenir/yazılır. Kaynak: magaza-paketi.json onayli_metinler.iddialar\n")
            f.write("\n".join(ayar["iddialar"]) + ("\n" if ayar["iddialar"] else ""))
        print("yazıldı: %s/video-ayar.json, onayli-iddialar.txt" % a.cikti_dizin)
    return 0


# ---------- video paketi ----------
def ffmpeg_yolu():
    y = shutil.which("ffmpeg")
    if y:
        return y
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def video_olc(dosya):
    """(olcu 'GENxYUK', sure_sn) ya da (None, None)."""
    ff = ffmpeg_yolu()
    if not ff or not os.path.exists(dosya):
        return None, None
    r = subprocess.run([ff, "-hide_banner", "-i", dosya], capture_output=True, text=True, errors="replace")
    m = re.search(r"Video:.*?\b(\d{2,5})x(\d{2,5})\b", r.stderr)
    s = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", r.stderr)
    olcu = "%sx%s" % (m.group(1), m.group(2)) if m else None
    sure = round(int(s.group(1)) * 3600 + int(s.group(2)) * 60 + float(s.group(3)), 2) if s else None
    return olcu, sure


def video_yaz(a):
    liste = []
    for v in a.video:
        p = v.split(":")
        if len(p) < 2:
            hata_cik("--video biçimi: DOSYA:kullanim[:dil[:GENxYUK:sure_sn]] (gelen: %s)" % v, 2)
        dosya, kullanim = p[0], p[1]
        kayit = {"dosya": os.path.basename(dosya), "kullanim": kullanim}
        olcu, sure = (p[3], float(p[4])) if len(p) >= 5 else video_olc(dosya)
        if olcu is None or sure is None:
            print("HATA  %s: ölçü/süre okunamadı (ffmpeg yok ya da dosya açılmadı); elle ver: DOSYA:kullanim:dil:1080x1920:14.2" % dosya)
            return 1
        kayit["olcu"], kayit["sure_sn"] = olcu, sure
        if len(p) >= 3 and p[2]:
            kayit["altyazi_dili"] = p[2]
        liste.append(kayit)
    hatalar = dogrula("video", liste)
    if hatalar:
        for h in hatalar:
            print("HATA  " + h)
        print("video-paketi YAZILMADI: %d hata" % len(hatalar))
        return 1
    yaz_json(a.cikti, liste)
    print("yazıldı: %s (%d video; mağazaya yüklenecek: %d)" % (
        a.cikti, len(liste), sum(1 for k in liste if k["kullanim"] in ("pdp-galeri", "hero"))))
    return 0


def video_sec(a):
    liste = oku_json(a.paket)
    hatalar = dogrula("video", liste)
    if hatalar:
        for h in hatalar:
            print("HATA  " + h)
        return 1
    sec = [k for k in liste if k["kullanim"] in ("pdp-galeri", "hero")]
    for k in sec:
        print("%s\t%s\t%s\t%s sn" % (k["kullanim"], k["dosya"], k["olcu"], k["sure_sn"]))
    print("mağazaya yüklenecek: %d / %d (reklam videoları yüklenmez; galeride G0'ın yerini almaz)" % (len(sec), len(liste)))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut")
    p = alt.add_parser("dogrula")
    p.add_argument("tur", choices=sorted(TUR_AD))
    p.add_argument("dosya")
    p = alt.add_parser("urun-yaz")
    p.add_argument("--cikti", required=True)
    p.add_argument("--ad", required=True)
    p.add_argument("--nis", required=True)
    p.add_argument("--pazar", required=True)
    p.add_argument("--foto", action="append")
    p.add_argument("--marj-csv")
    p.add_argument("--teklif-tsv")
    p.add_argument("--kanit-md")
    p.add_argument("--ozellik", action="append")
    p.add_argument("--varyant", action="append")
    p = alt.add_parser("fiyat")
    p.add_argument("--teklif-tsv")
    p.add_argument("--pazar", default="US")
    p = alt.add_parser("magaza-oku")
    p.add_argument("paket")
    p.add_argument("--cikti-dizin")
    p = alt.add_parser("iddia-kontrol")
    p.add_argument("paket")
    p.add_argument("metin", nargs="+")
    p = alt.add_parser("video-yaz")
    p.add_argument("--cikti", required=True)
    p.add_argument("--video", action="append", required=True)
    p = alt.add_parser("video-sec")
    p.add_argument("paket")
    a = ap.parse_args(argv)
    if a.komut == "dogrula":
        hatalar = dogrula(a.tur, oku_json(a.dosya))
        for h in hatalar:
            print("HATA  " + h)
        print("%s: %s" % (a.dosya, "GEÇERLİ" if not hatalar else "%d hata" % len(hatalar)))
        return 1 if hatalar else 0
    if a.komut == "urun-yaz":
        return urun_yaz(a)
    if a.komut == "fiyat":
        t = teklif_kaynagi(a.teklif_tsv, pazar_coz(a.pazar))
        print(json.dumps(t, ensure_ascii=False))
        return 0
    if a.komut == "magaza-oku":
        return magaza_oku(a)
    if a.komut == "iddia-kontrol":
        return iddia_kontrol(a)
    if a.komut == "video-yaz":
        return video_yaz(a)
    if a.komut == "video-sec":
        return video_sec(a)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
