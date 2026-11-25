#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ön uçuş: üretime (kredi, kare üretimi, jüri) BAŞLAMADAN eksikleri tek komutla söyler. Hiçbir şey üretmez, değiştirmez, ağa çıkmaz.

Neden (denetim 2026-11-25, V6): 7 sınavın 6'sında ilk tur kaybı rolün yargısından değil ön koşuldan çıktı (malzeme yok, referans yok, araç yok,
kütüphane başlığı yok). Bu betik o dört soruyu bir dakikada sorar.

  python3 on_ucus.py hepsi [--ozellik 01..07] [--is is/NN-urun] [--pazar US] [--referans-kok K] [--yayin]
  python3 on_ucus.py malzeme  IS_KLASORU [--yayin]       KAYNAK.tsv var mı, satırların dosyası var mı, (yayın için) lisans/kullanim dolu mu
  python3 on_ucus.py referans --tsv referanslar.tsv --pazar US [--tur video|kanca|gorsel|site] [--referans-kok K]   ≥ 3 pazar-uyumlu, yolu çözülen referans
  python3 on_ucus.py arac     [--icin video|ses|gorsel|site|urun-avi|hepsi]   ffmpeg, Pillow, OCR, Node, Chrome, Lighthouse/axe, openpyxl
  python3 on_ucus.py kutuphane                           kanca K1–K15, sahne S1–S10, pazar kartları, kartın kendi sınaması

`--ozellik NN`: sınav özelliği için araç + (jüri'li özelliklerde) vaka pazarlarına göre referans + kütüphane (+ --is varsa malzeme).
Çıkış: 0 hazır · 1 ÜRETİME BAŞLAMA (en az bir zorunlu eksik) · 3 başlanabilir ama bazı kapılar ölçülemez kalacak (listelenir; geçti sayılmaz) · 2 kullanım.
Her satır: [kapı] DURUM: neden · düzelt: <komut>. Yol bulunamayan kapı ölçülmüş sayılmaz.
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

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BURASI = os.path.dirname(os.path.abspath(__file__))
EKL = os.path.dirname(BURASI)
SINAV = os.path.join(BURASI, "sinav")
REF = os.environ.get("ON_UCUS_REF") or os.path.join(EKL, "skills", "studio", "referans")   # ON_UCUS_REF yalnız kırma testi için
HOME = os.path.expanduser("~")
OZELLIKLER = {"01": ("01-urun-videosu", "video", "video"), "02": ("02-kanca-senaryo", "kanca", "video"), "03": ("03-hikaye-videosu", "video", "video"),
              "04": ("04-ses-muzik", None, "ses"), "05": ("05-gorsel", "gorsel", "gorsel"), "06": ("06-urun-avi", None, "urun-avi"),
              "07": ("07-site", "site", "site")}   # özellik → (klasör, jüri referans türü, araç grubu)
PAZAR_UYUM = {"US": {"US"}, "TR": {"TR"}, "DE": {"DE", "UK", "FR", "ES", "US"}, "UK": {"UK", "DE", "FR", "ES", "US"},
              "FR": {"DE", "UK", "FR", "ES", "US"}, "ES": {"DE", "UK", "FR", "ES", "US"}}
EKSIK, OLCULEMEZ, TAMAM = "EKSİK", "olculemez", "TAMAM"
sorunlar = []   # (kapı, durum, neden, düzelt)


def bildir(kapi, durum, neden, duzelt=""):
    sorunlar.append((kapi, durum, neden, duzelt))


def modul(yol, ad):
    sp = importlib.util.spec_from_file_location(ad, yol)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


# ------------------------------------------------------------------ malzeme
def malzeme(klasor, yayin=False):
    """Gerçek ürün görüntüsü kaydı: KAYNAK.tsv (klasörde ya da en çok 6 üstte; tedarikci/, malzeme/ altında da aranır)."""
    mk = modul(os.path.join(EKL, "skills", "cut", "scripts", "malzeme_kaynak.py"), "malzeme_kaynak")
    yol = mk.bul(klasor)
    if not yol:
        bildir("malzeme", EKSIK, "KAYNAK.tsv yok: gerçek ürün görüntüsü (tedarikçi klibi, kurucu çekimi) kaydı bulunamadı — malzemesiz video üretilmez (01 tur1-2'nin kaybı)",
               "malzeme topla, KAYNAK.tsv'ye satır yaz (sütunlar: skills/cut/scripts/malzeme_kaynak.py başı)")
        return
    satirlar = mk.oku(yol)
    kullan = [s for s in satirlar if mk.kullanilabilir(s)]
    if not kullan:
        bildir("malzeme", EKSIK, "KAYNAK.tsv'de kullanılabilir satır yok (%s)" % yol, "gerçek ürün klibi ekle (`kullanma` işaretli satır sayılmaz)")
        return
    kok = os.path.dirname(yol)
    yok = []
    for s in kullan:
        d = s.get("dosya", "")
        v = s.get("vaka", "")
        adaylar = [os.path.join(kok, d), os.path.join(kok, "tedarikci", d), os.path.join(os.path.dirname(kok), d), os.path.join(os.path.dirname(kok), "tedarikci", d)]
        if v:
            adaylar += [os.path.join(kok, v, d), os.path.join(kok, "tedarikci", v, d)]
        if not d or not any(os.path.exists(a) for a in adaylar):
            yok.append(d or "(dosya sütunu boş)")
    if yok:
        bildir("malzeme", EKSIK, "KAYNAK.tsv satırı var ama dosya yok: %s" % ", ".join(yok[:4]), "dosyayı KAYNAK.tsv'nin yanına/tedarikci/ altına koy ya da satırı sil")
    eksik_lisans = [(s.get("dosya"), mk.lisans_sorunu(s)) for s in kullan if mk.lisans_sorunu(s)]
    if eksik_lisans and yayin:
        bildir("malzeme", EKSIK, "yayın için lisans/kullanim/yapay_mi/bakildi eksik: %s" % "; ".join("%s (%s)" % (d, ", ".join(p)) for d, p in eksik_lisans[:3]),
               "KAYNAK.tsv sütunlarını doldur (kapi.py yayin lisans@V aynı kuralı koşar)")
    elif eksik_lisans:
        bildir("malzeme", OLCULEMEZ, "%d satırda lisans/kullanim eksik: yalnız sınavda geçer, `kapi.py yayin` lisans kapısı KALIR (ilk: %s)" % (len(eksik_lisans), eksik_lisans[0][0]),
               "yayın öncesi KAYNAK.tsv lisans sütunlarını doldur")


# ------------------------------------------------------------------ referans
def referanslar_oku(tsv):
    with open(tsv, encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f, delimiter="\t") if (r.get("id") or "").strip() and not r["id"].startswith("#")]


def referans(tsv, pazar, tur, kok, ad=None):
    ad = ad or "referans(%s%s)" % (pazar, "/" + tur if tur else "")
    if not os.path.isfile(tsv):
        bildir(ad, EKSIK, "referanslar.tsv yok: %s" % tsv, "referans toplama (decoder/muse) ve TSV doldur")
        return
    uyum = PAZAR_UYUM.get(pazar, {pazar})
    adaylar = [r for r in referanslar_oku(tsv) if (r.get("pazar") or "").strip() in uyum and (not tur or (r.get("tur") or "").strip() == tur)
               and (r.get("kare_panosu_yolu") or "").strip()]
    cozulen = []
    for r in adaylar:
        y = r["kare_panosu_yolu"].strip()
        yol = y if os.path.isabs(y) else (os.path.join(kok, y) if kok else None)
        if yol and os.path.exists(yol):
            cozulen.append(r["id"])
    if len(cozulen) < 3:
        neden = "pazar %s için %d/3 çözülen referans (%d aday satır)" % (pazar, len(cozulen), len(adaylar))
        if adaylar and not kok:
            neden += "; --referans-kok / SINAV_REFERANS_KOK verilmedi"
        bildir(ad, EKSIK, neden + " — kör jüri kapısı olculemedi/KALDI kalır", "≥ 3 gerçekten izlenmiş pazar-uyumlu video kare panosu topla; referanslar.tsv'yi doldur")


# ------------------------------------------------------------------ araç
def ffmpeg_var():
    if os.environ.get("FFMPEG_DIZIN"):
        d = os.environ["FFMPEG_DIZIN"]
        if os.path.isfile(os.path.join(d, "ffmpeg")) and os.path.isfile(os.path.join(d, "ffprobe")):
            return True, ""
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        return True, ""
    try:
        import imageio_ffmpeg  # noqa: F401
        return True, ""
    except ImportError:
        return False, "ffmpeg/ffprobe PATH'te yok, FFMPEG_DIZIN verilmemiş, imageio_ffmpeg yok"


def py_modul(ad):
    try:
        __import__(ad)
        return True
    except ImportError:
        return False


def venv_py(ad):
    return os.path.join(HOME, ".local", "share", "viral-urun-ekibi", ad, "bin", "python")


def venvde_var(venv, modul_adi):
    p = venv_py(venv)
    if not os.path.isfile(p):
        return False
    return subprocess.run([p, "-c", "import %s" % modul_adi], capture_output=True).returncode == 0


def arac(icin):
    grup = {"video": ("ffmpeg", "pillow", "node"), "ses": ("ffmpeg",), "gorsel": ("pillow", "ocr", "tesseract"), "site": ("chrome", "node", "web_olcum", "pillow"),
            "urun-avi": ("openpyxl",), "hepsi": ("ffmpeg", "pillow", "ocr", "tesseract", "node", "chrome", "web_olcum", "openpyxl")}[icin]
    if "ffmpeg" in grup:
        ok, n = ffmpeg_var()
        if not ok:
            bildir("arac:ffmpeg", EKSIK, n + " (video/ses kapıları ölçemez)", "brew install ffmpeg  (ya da python3 -m pip install --user imageio-ffmpeg; FFMPEG_DIZIN ile klasör ver)")
    if "pillow" in grup and not py_modul("PIL"):
        bildir("arac:pillow", EKSIK, "Pillow yok (kare/pano/yazı katmanı üretilemez)", 'python3 -m pip install --user "pillow>=10"')
    if "ocr" in grup:
        if not (venvde_var("ocr-venv", "rapidocr_onnxruntime") or py_modul("rapidocr_onnxruntime")):
            bildir("arac:ocr", EKSIK, "RapidOCR yok (K2 yazım kapısı ölçemez: 05-gorsel yazım olculemedi kalır)",
                   "ocr-venv: python3 -m venv ~/.local/share/viral-urun-ekibi/ocr-venv && …/bin/python -m pip install rapidocr-onnxruntime")
    if "tesseract" in grup and not shutil.which(os.environ.get("OCR_TESSERACT") or "tesseract"):
        bildir("arac:tesseract", OLCULEMEZ, "Tesseract yok: Türkçe harfli öğeler (İ/ş/ğ…) 'gözle' kalır, K2 TR kapısı olculemedi (geçti sayılmaz)",
               "brew install tesseract tesseract-lang  (OCR_TESSDATA ile tur verisini göster)")
    if "node" in grup:
        yol = shutil.which("node")
        if not yol:
            bildir("arac:node", EKSIK, "Node.js yok (HyperFrames hareketli katman, Lighthouse)", "brew install node  (22.19+)")
        else:
            v = subprocess.run([yol, "--version"], capture_output=True, text=True).stdout.strip().lstrip("v")
            try:
                if tuple(int(x) for x in v.split(".")[:3]) < (22, 19, 0):
                    bildir("arac:node", EKSIK, "Node %s çok eski (22.19+ gerekir)" % v, "brew upgrade node")
            except ValueError:
                bildir("arac:node", EKSIK, "Node sürümü okunamadı: %r" % v, "node --version")
    if "chrome" in grup:
        wo = modul(os.path.join(BURASI, "web_olcum.py"), "web_olcum")
        if not wo.chrome_yolu():
            bildir("arac:chrome", EKSIK, "Chrome/Chromium yok (mobil ekran, Lighthouse, axe ölçemez)", "Chrome kur ya da CHROME_PATH ver")
    if "web_olcum" in grup:
        wo = modul(os.path.join(BURASI, "web_olcum.py"), "web_olcum")
        ok, sorun = wo.araclar()
        sorun = [x for x in sorun if "Chrome" not in x and "node" not in x.lower()]
        if sorun:
            bildir("arac:web-olcum", EKSIK, "; ".join(sorun) + " — 07 hiz_cwv/erisim_wcag olculemedi kalır", "python3 ortak/web_olcum.py kur  (sürümler sabit, ayrı klasör)")
    if "openpyxl" in grup and not (py_modul("openpyxl") or venvde_var("excel-venv", "openpyxl")):
        bildir("arac:openpyxl", EKSIK, "openpyxl yok (Excel çıktısı yazılamaz; excel_test olculemedi)",
               "python3 -m venv ~/.local/share/viral-urun-ekibi/excel-venv && …/bin/python -m pip install --only-binary=:all: openpyxl==3.1.5 et-xmlfile==2.0.0")


# ------------------------------------------------------------------ kütüphane
def kutuphane():
    def oku(ad):
        y = os.path.join(REF, ad)
        if not os.path.isfile(y):
            bildir("kutuphane", EKSIK, "dosya yok: skills/studio/referans/%s" % ad, "eklenti dosyası eksik: yeniden kur")
            return ""
        with open(y, encoding="utf-8") as f:
            return f.read()
    kut = oku("kanca-kutuphanesi.md")
    yok = [k for k in ("K%d" % i for i in range(1, 16)) if not re.search(r"^### %s\. " % k, kut, re.M)]
    if kut and yok:
        bildir("kutuphane", EKSIK, "kanca-kutuphanesi.md'de `### K<n>. ` başlığı yok: %s (on_uretim_karti.py ve kanca_varyasyon.py başlığı bu biçimde arar; tablo satırı başlık sayılmaz; 02 tur1'in kaybı)" % ", ".join(yok),
               "tablodaki aileye `### K<n>. <ad> — KURAL (n)` başlığı ekle")
    sah = oku("sahne-sablonlari.md")
    yok = [s for s in ("S%d" % i for i in range(1, 11)) if not re.search(r"^## %s\b" % s, sah, re.M)]
    if sah and yok:
        bildir("kutuphane", EKSIK, "sahne-sablonlari.md'de `## S<n>` başlığı yok: %s" % ", ".join(yok), "başlığı ekle")
    for p in ("US", "UK", "DE", "FR", "ES", "TR"):
        if not os.path.isfile(os.path.join(REF, "pazar-kartlari", p + ".md")):
            bildir("kutuphane", EKSIK, "pazar kartı yok: pazar-kartlari/%s.md" % p, "kartı _sablon.md'den yaz")
    if kut and sah:   # kartın kendi sınaması: şablon kart her pazarda geçmeli (kütüphane ile betik ayrışmadıysa)
        k = modul(os.path.join(EKL, "skills", "studio", "scripts", "on_uretim_karti.py"), "on_uretim_karti")
        for p in k.PAZARLAR:
            h = k.dogrula(k.sablon(p))
            if h:
                bildir("kutuphane", EKSIK, "on_uretim_karti şablonu %s pazarında geçmiyor: %s" % (p, h[0]), "kütüphane ile betik uyumsuz; on_uretim_karti.py sablon --pazar %s" % p)


# ------------------------------------------------------------------ özellik
def ozellik(no, a):
    klasor, tur, grup = OZELLIKLER[no]
    arac(grup)
    kutuphane()
    if tur:
        kok = a.referans_kok or os.environ.get("SINAV_REFERANS_KOK")
        tsv = os.path.join(SINAV, klasor, "referanslar.tsv")
        vakalar = sorted(glob.glob(os.path.join(SINAV, klasor, "vakalar", "*", "vaka.json")))
        pazarlar = sorted({json.load(open(v, encoding="utf-8"))["pazar"] for v in vakalar}) if not a.pazar else [a.pazar]
        for p in pazarlar:
            referans(tsv, p, tur, kok)
    if a.is_klasoru:
        malzeme(a.is_klasoru, a.yayin)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("komut", choices=["hepsi", "malzeme", "referans", "arac", "kutuphane"])
    ap.add_argument("is_klasoru", nargs="?", help="malzeme için iş klasörü (is/NN-urun)")
    ap.add_argument("--is", dest="is_opt")
    ap.add_argument("--ozellik")
    ap.add_argument("--pazar")
    ap.add_argument("--tur")
    ap.add_argument("--tsv")
    ap.add_argument("--referans-kok")
    ap.add_argument("--icin", default="hepsi", choices=["video", "ses", "gorsel", "site", "urun-avi", "hepsi"])
    ap.add_argument("--yayin", action="store_true", help="malzemede lisans eksiği de zorunlu eksik sayılır")
    a = ap.parse_args()
    if a.is_opt:
        a.is_klasoru = a.is_opt
    kok = a.referans_kok or os.environ.get("SINAV_REFERANS_KOK")
    if a.komut == "hepsi":
        if a.ozellik:
            no = a.ozellik.split("-")[0].zfill(2)
            if no not in OZELLIKLER:
                ap.error("özellik 01…07 olmalı")
            ozellik(no, a)
        else:
            arac(a.icin)
            kutuphane()
            if a.is_klasoru:
                malzeme(a.is_klasoru, a.yayin)
            if a.tsv and a.pazar:
                referans(a.tsv, a.pazar, a.tur, kok)
    elif a.komut == "malzeme":
        if not a.is_klasoru:
            ap.error("malzeme için iş klasörü ver")
        malzeme(a.is_klasoru, a.yayin)
    elif a.komut == "referans":
        if not (a.tsv and a.pazar):
            ap.error("referans için --tsv ve --pazar ver")
        referans(a.tsv, a.pazar, a.tur, kok)
    elif a.komut == "arac":
        arac(a.icin)
    else:
        kutuphane()
    eksik = [s for s in sorunlar if s[1] == EKSIK]
    olcul = [s for s in sorunlar if s[1] == OLCULEMEZ]
    for kapi, durum, neden, duzelt in sorunlar:
        print("[%s] %s: %s%s" % (kapi, durum, neden, " · düzelt: " + duzelt if duzelt else ""))
    if eksik:
        print("ÖN UÇUŞ: ÜRETİME BAŞLAMA — %d zorunlu eksik%s" % (len(eksik), ", %d kapı ölçülemez kalacak" % len(olcul) if olcul else ""))
        return 1
    if olcul:
        print("ÖN UÇUŞ: başlanabilir ama %d kapı ölçülemez kalacak (geçti sayılmaz)" % len(olcul))
        return 3
    print("ÖN UÇUŞ: HAZIR — malzeme/referans/araç/kütüphane eksiği yok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
