#!/usr/bin/env python3
"""excel_hazirla.py [PROJE_KLASORU] [CIKTI.xlsx] [--tsv sayfalar.tsv]

Spy hazırlayıcısı (0.4.0): is/meta/sayfalar.tsv → ortak şablonlu Excel (3 sayfa, 10 sütun): is/meta/reklam-urunler.xlsx.
Bu betik yalnız iki iş yapar: urunler.tsv hazırlar, sonra ortak/excel_yaz.py'yi alt süreç olarak çağırıp çıkış kodunu aynen döndürür.
Karar eşlemesi: OLCEKLENIYOR → İZLE (Neden: "Hunter eşlemesine girer") · ESKI-KAZANAN → ELE · TEST ve BILINMIYOR yalnız Ayrıntı sayfasında.
Spy hiçbir zaman SAT yazmaz (satış kanıtı bu beceride yok). İlgi = "N reklam · G gün".
Çıkış: excel_yaz.py ile aynı (0 TAMAM · 1 veri hatası · 2 kullanım · 3 openpyxl yok).
"""
import csv
import datetime
import os
import re
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
ALANLAR = ["urun", "link", "ilgi", "ilgi_sayi", "alis", "satis", "para", "marj_kat", "karar", "neden", "kaynak", "tarih"]
KARAR = {"OLCEKLENIYOR": "İZLE", "ESKI-KAZANAN": "ELE"}
GORUNMUYOR = {"", "görünmüyor", "gorunmuyor", "-"}
NEDEN_MAX = 140


def excel_yaz_yolu():
    adaylar = [os.path.join(BURADA, "..", "..", "..", "ortak", "excel_yaz.py"),
               os.path.join(BURADA, "..", "..", "ekip-bilgi", "references", "excel_yaz.py"),
               os.path.join(BURADA, "excel_yaz.py")]
    kok = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if kok:
        adaylar.insert(0, os.path.join(kok, "ortak", "excel_yaz.py"))
    for a in adaylar:
        if os.path.isfile(a):
            return os.path.abspath(a)
    sys.exit("HATA: ortak/excel_yaz.py bulunamadı")


def kisalt(s, n=NEDEN_MAX):
    s = " ".join((s or "").split())
    if len(s) <= n:
        return s
    kes = s[:n - 1].rsplit(" ", 1)[0] if " " in s[:n - 1] else s[:n - 1]
    return kes.rstrip(" ,;:.-") + "…"


def tam_sayi(s):
    s = (s or "").strip()
    return int(s) if re.fullmatch(r"\d+", s) else None


def hazirla(tsv_girdi, tsv_cikti):
    mtime = datetime.date.fromtimestamp(os.path.getmtime(tsv_girdi)).isoformat()
    with open(tsv_girdi, encoding="utf-8-sig", newline="") as f:
        satirlar = list(csv.DictReader(f, delimiter="\t"))
    yazilan = 0
    with open(tsv_cikti, "w", encoding="utf-8", newline="") as f:
        f.write("\t".join(ALANLAR) + "\n")
        for r in satirlar:
            etiket = (r.get("etiket") or "").strip().upper()
            if etiket not in KARAR:
                continue
            birim = (r.get("birim") or "").strip()
            ad = (r.get("sayfa_adi") or "").strip() or birim
            link = "https://" + birim if re.match(r"^[\w.-]+\.[a-z]{2,}$", birim, re.I) else ""
            n = tam_sayi(r.get("reklam_sayisi"))
            gun = tam_sayi(r.get("max_aktif_gun"))
            parcalar = []
            if n is not None:
                parcalar.append("%d reklam" % n)
            if gun is not None:
                parcalar.append("%d gün" % gun)
            bolge = " · ".join(x for x in ((r.get("ulke") or "").strip(), (r.get("nis") or "").strip()) if x)
            if etiket == "OLCEKLENIYOR":
                neden = "%s: %s aktif reklam; Hunter eşlemesine girer." % (bolge, " ".join(parcalar[:1]) or "reklam sayısı görünmüyor")
                if gun is not None:
                    neden = "%s: %s, en uzun %d gün; Hunter eşlemesine girer." % (bolge, " ".join(parcalar[:1]) or "reklam", gun)
            else:
                neden = "%s: eski kazanan (>180 gün), yeni dalga değil." % bolge
            tarih = (r.get("son_okuma") or "").strip()
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", tarih):
                tarih = mtime
            alan = [ad, link, " · ".join(parcalar), "" if n is None else str(n), "", "", "", "", KARAR[etiket],
                    kisalt(neden.replace("\t", " ").lstrip(": ")), "Meta reklam", tarih]
            f.write("\t".join(h.replace("\t", " ").replace("\n", " ") for h in alan) + "\n")
            yazilan += 1
    return yazilan


def main():
    arg = sys.argv[1:]
    tsv = None
    if "--tsv" in arg:
        i = arg.index("--tsv")
        tsv = arg[i + 1]
        del arg[i:i + 2]
    proje = arg[0] if len(arg) > 0 else os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    meta = os.path.join(proje, "is", "meta")
    cikti = arg[1] if len(arg) > 1 else os.path.join(meta, "reklam-urunler.xlsx")
    tsv = tsv or os.path.join(meta, "sayfalar.tsv")
    if not os.path.exists(tsv):
        sys.exit("HATA: %s yok — önce meta_kayit.py ile sayfa kaydı üret" % tsv)
    with tempfile.TemporaryDirectory(prefix="spy_excel_") as d:
        urunler = os.path.join(d, "urunler.tsv")
        if hazirla(tsv, urunler) == 0:
            print("HATA: OLCEKLENIYOR ya da ESKI-KAZANAN etiketli sayfa yok (TEST ve BILINMIYOR Excel'e girmez); önce kazanan_puan.py")
            return 1
        r = subprocess.run([sys.executable, excel_yaz_yolu(), "--urunler", urunler, "--kaynak", "spy",
                            "--cikti", cikti, "--ayrinti", tsv])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
