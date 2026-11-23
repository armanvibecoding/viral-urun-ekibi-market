#!/usr/bin/env python3
"""excel_yaz.py: bütün ürün bulma becerilerinin (radar, spy, hunter, bazaar) ortak Excel yazıcısı.

Kullanım:
  python3 excel_yaz.py --urunler <urunler.tsv> --kaynak <radar|spy|hunter|bazaar> --cikti <dosya.xlsx>
                       [--ayrinti <ham.tsv|.csv|.md>] [--kopya <klasör ya da dosya.xlsx>]

Girdi urunler.tsv (sekme, başlıklı, UTF-8), 12 alan:
  urun, link, ilgi, ilgi_sayi, alis, satis, para, marj_kat, karar, neden, kaynak, tarih

Çıktı tam 3 sayfa: "Ürünler" (10 sütun) · "Ayrıntı" (ham tablo) · "Nasıl okunur".
Yazmadan önce doğrular (tutmazsa çıkış 1, dosya yazılmaz); yazdıktan sonra dosyayı yeniden açıp ölçer (tutmazsa çıkış 1).
Çıkış: 0 TAMAM · 1 veri ya da doğrulama hatası · 2 kullanım hatası · 3 openpyxl yok.
Gerekli paket: openpyxl  (kur: python3 -m pip install --user openpyxl)
"""
import argparse
import csv
import datetime
import os
import re
import shutil
import sys

ALANLAR = ["urun", "link", "ilgi", "ilgi_sayi", "alis", "satis", "para", "marj_kat", "karar", "neden", "kaynak", "tarih"]
KARARLAR = ["SAT", "SAT (koşullu)", "İZLE", "ELE"]
PARALAR = {"TRY": '#,##0.00 "₺"', "USD": '"$"#,##0.00', "EUR": '#,##0.00 "€"', "GBP": '"£"#,##0.00'}
KARAR_RENK = {"SAT": "C6EFCE", "SAT (koşullu)": "E2F0D9", "İZLE": "FFEB9C", "ELE": "FFC7CE"}
KAYNAKLAR = {"radar": "Instagram", "spy": "Meta reklam", "hunter": "AliExpress", "bazaar": "Trendyol"}
ILGI_TANIMI = {
    "radar": "Videonun izlenme sayısı (ör. 2,4 Mn izlenme).",
    "spy": "Reklam sayısı ve en uzun süredir açık reklamın günü (ör. 12 reklam · 45 gün).",
    "hunter": "AliExpress ürün sayfasında okunan satış sayısı (ör. 57 satış).",
    "bazaar": "Trendyol değerlendirme sayısı ve puan (ör. 969 yorum · 4,1). Satış adedi değil, talep vekilidir.",
}
SAYFALAR = ["Ürünler", "Ayrıntı", "Nasıl okunur"]
SUTUNLAR = [("Ürün", 38), ("Link", 9), ("İlgi", 22), ("Alış", 11), ("Satış", 11), ("Marj (kat)", 10),
            ("Karar", 9), ("Neden", 60), ("Kaynak", 12), ("Tarih", 11)]
NEDEN_MAX = 140


class Hata(Exception):
    pass


def sayi(metin, alan, satir):
    """Boş → None; ondalık virgül kabul edilir ('2,4' → 2.4; '1.250,5' → 1250.5)."""
    s = (metin or "").strip().replace(" ", "")
    if s == "":
        return None
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        raise Hata("satır %d: %s sayı değil: %r" % (satir, alan, metin))


def tsv_oku(yol):
    with open(yol, encoding="utf-8-sig", newline="") as f:
        okuyucu = csv.reader(f, delimiter="\t")
        satirlar = [r for r in okuyucu if any(h.strip() for h in r)]
    return satirlar


def urunleri_dogrula(yol):
    """Girdiyi doğrular. Döner: [{alan: değer}] (sayılar float/None, tarih datetime.date)."""
    if not os.path.isfile(yol):
        raise Hata("urunler dosyası yok: %s" % yol)
    satirlar = tsv_oku(yol)
    if not satirlar:
        raise Hata("urunler dosyası boş")
    baslik = [h.strip() for h in satirlar[0]]
    if baslik != ALANLAR:
        raise Hata("başlık tam bu %d alan olmalı (sekmeyle ayrılmış): %s; bulunan: %s"
                   % (len(ALANLAR), ", ".join(ALANLAR), ", ".join(baslik)))
    govde = satirlar[1:]
    if not govde:
        raise Hata("0 ürün: yazılacak satır yok")
    cikti = []
    for i, ham in enumerate(govde, 2):
        if len(ham) > len(ALANLAR):
            raise Hata("satır %d: %d alan var (en çok %d)" % (i, len(ham), len(ALANLAR)))
        ham = ham + [""] * (len(ALANLAR) - len(ham))
        r = dict(zip(ALANLAR, [h.strip() for h in ham]))
        if not r["urun"]:
            raise Hata("satır %d: urun boş" % i)
        if r["link"] and not r["link"].lower().startswith("http"):
            raise Hata("satır %d: link http ile başlamıyor: %r" % (i, r["link"]))
        if r["karar"] not in KARARLAR:
            raise Hata("satır %d: karar %r; izinli: %s" % (i, r["karar"], " / ".join(KARARLAR)))
        if len(r["neden"]) > NEDEN_MAX:
            raise Hata("satır %d: neden %d karakter (en çok %d)" % (i, len(r["neden"]), NEDEN_MAX))
        if r["para"] and r["para"] not in PARALAR:
            raise Hata("satır %d: para %r; izinli: %s ya da boş" % (i, r["para"], ", ".join(PARALAR)))
        for alan in ("alis", "satis", "marj_kat", "ilgi_sayi"):
            r[alan] = sayi(r[alan], alan, i)
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["tarih"]):
            raise Hata("satır %d: tarih YYYY-AA-GG olmalı: %r" % (i, r["tarih"]))
        try:
            r["tarih"] = datetime.date.fromisoformat(r["tarih"])
        except ValueError:
            raise Hata("satır %d: tarih geçerli bir gün değil: %r" % (i, r["tarih"]))
        cikti.append(r)
    return cikti


def ayrinti_oku(yol):
    """Ham tabloyu olduğu gibi okur: [[hücre]] (ilk satır sütun adları)."""
    if not os.path.isfile(yol):
        raise Hata("ayrıntı dosyası yok: %s" % yol)
    uz = os.path.splitext(yol)[1].lower()
    if uz == ".md":
        satirlar, icinde = [], False
        with open(yol, encoding="utf-8-sig") as f:
            for s in f:
                s = s.rstrip("\n")
                if s.lstrip().startswith("|"):
                    icinde = True
                    if re.match(r"^\s*\|[\s:\-|]+\|\s*$", s):
                        continue
                    satirlar.append([h.strip() for h in s.strip().strip("|").split("|")])
                elif icinde:
                    break
        if not satirlar:
            raise Hata("ayrıntı .md dosyasında Markdown tablosu yok: %s" % yol)
        return satirlar
    ayirac = "\t" if uz == ".tsv" else ","
    with open(yol, encoding="utf-8-sig", newline="") as f:
        satirlar = [r for r in csv.reader(f, delimiter=ayirac) if any(h.strip() for h in r)]
    if not satirlar:
        raise Hata("ayrıntı dosyası boş: %s" % yol)
    return satirlar


def sirala(urunler):
    sira = {k: i for i, k in enumerate(KARARLAR)}
    return sorted(urunler, key=lambda r: (sira[r["karar"]], -(r["ilgi_sayi"] if r["ilgi_sayi"] is not None else float("-inf"))))


def nasil_okunur(kaynak):
    return [
        ("Ürün", "Kısa ürün adı."),
        ("Link", "Ürünün sayfası; hücreye tıklayınca açılır."),
        ("İlgi", ILGI_TANIMI[kaynak]),
        ("Alış", "Ürünü bizim alış fiyatı; para birimi hücre biçiminde (₺ $ € £). Bilinmiyorsa boş."),
        ("Satış", "Önerilen ya da gözlenen satış fiyatı; aynı para birimi."),
        ("Marj (kat)", "Marj betiğinin verdiği satış / maliyet çarpanı. Bu dosya kendisi hesaplamaz; yoksa boş."),
        ("Karar", "SAT = kanıt dosyası olan aday · SAT (koşullu) = diğer ölçütler güçlü, marj ya da viral doğrulanamadı (neden sütununda hangisi) · İZLE = izlenecek ya da eksik kanıtlı · ELE = elenen."),
        ("Neden", "Kararın tek cümlelik gerekçesi (en çok 140 karakter)."),
        ("Kaynak", "Ürünün bulunduğu yer: Instagram, Meta reklam, AliExpress ya da Trendyol."),
        ("Tarih", "Verinin okunduğu gün (yyyy-aa-gg)."),
        ("Karar renkleri", "SAT yeşil (C6EFCE) · İZLE sarı (FFEB9C) · ELE kırmızı (FFC7CE). Sıralama: SAT, İZLE, ELE; her grupta ilgi büyükten küçüğe."),
        ("İlgi tanımı (bu dosya)", ILGI_TANIMI[kaynak]),
    ]


def yaz(urunler, kaynak, cikti, ayrinti, ham_baslik_yedek):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    kosu = PatternFill("solid", fgColor="1F2937")
    wb = Workbook()
    ws = wb.active
    ws.title = SAYFALAR[0]
    ws.append([a for a, _ in SUTUNLAR])
    for j, (_, g) in enumerate(SUTUNLAR, 1):
        ws.column_dimensions[get_column_letter(j)].width = g
    for r in sirala(urunler):
        ws.append([r["urun"], "aç" if r["link"] else None, r["ilgi"] or None, r["alis"], r["satis"], r["marj_kat"],
                   r["karar"], r["neden"] or None, r["kaynak"] or KAYNAKLAR[kaynak], r["tarih"]])
        satir = ws.max_row
        if r["link"]:
            ws.cell(satir, 2).hyperlink = r["link"]
            ws.cell(satir, 2).font = Font(color="0563C1", underline="single")
        fmt = PARALAR.get(r["para"])
        if fmt:
            ws.cell(satir, 4).number_format = fmt
            ws.cell(satir, 5).number_format = fmt
        ws.cell(satir, 6).number_format = '0.0"×"'
        k = ws.cell(satir, 7)
        k.fill = PatternFill("solid", fgColor=KARAR_RENK[r["karar"]])
        k.font = Font(bold=True)
        ws.cell(satir, 8).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(satir, 10).number_format = "yyyy-mm-dd"
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = kosu
        c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:J%d" % ws.max_row

    wa = wb.create_sheet(SAYFALAR[1])
    for s in (ayrinti if ayrinti else ham_baslik_yedek):
        wa.append(s)
    for c in wa[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = kosu
    for j in range(1, wa.max_column + 1):
        wa.column_dimensions[get_column_letter(j)].width = 18
    wa.freeze_panes = "A2"
    wa.auto_filter.ref = wa.dimensions

    wn = wb.create_sheet(SAYFALAR[2])
    wn.append(["Ne", "Anlamı"])
    for a, b in nasil_okunur(kaynak):
        wn.append([a, b])
    for c in wn[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = kosu
    wn.column_dimensions["A"].width = 24
    wn.column_dimensions["B"].width = 100
    for row in wn.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")

    klasor = os.path.dirname(os.path.abspath(cikti))
    os.makedirs(klasor, exist_ok=True)
    wb.save(cikti)


def olc(cikti, beklenen_satir):
    """Dosyayı yeniden açar ve 6 ölçüm yapar. Döner: hata listesi."""
    from openpyxl import load_workbook
    hatalar = []
    wb = load_workbook(cikti)
    if wb.sheetnames != SAYFALAR:
        hatalar.append("sayfa adları %s (beklenen %s)" % (wb.sheetnames, SAYFALAR))
        return hatalar
    ws = wb[SAYFALAR[0]]
    if ws.max_column != 10:
        hatalar.append("Ürünler %d sütun (beklenen 10)" % ws.max_column)
    if ws.max_row - 1 != beklenen_satir:
        hatalar.append("Ürünler %d veri satırı (beklenen %d)" % (ws.max_row - 1, beklenen_satir))
    birlesik = sum(len(w.merged_cells.ranges) for w in wb.worksheets)
    if birlesik:
        hatalar.append("%d birleştirilmiş hücre var (beklenen 0)" % birlesik)
    if ws.freeze_panes != "A2":
        hatalar.append("freeze_panes %r (beklenen 'A2')" % ws.freeze_panes)
    if not ws.auto_filter.ref:
        hatalar.append("auto_filter boş")
    return hatalar


def main(argv=None):
    ap = argparse.ArgumentParser(prog="excel_yaz.py", description="Ortak ürün Excel yazıcısı (3 sayfa, 10 sütun)")
    ap.add_argument("--urunler", required=True)
    ap.add_argument("--kaynak", required=True, choices=sorted(KAYNAKLAR))
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--ayrinti", action="append", default=[])
    ap.add_argument("--kopya")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        print("HATA: openpyxl yok. Kur: python3 -m pip install --user openpyxl  (Windows: py -m pip install openpyxl)")
        return 3
    try:
        urunler = urunleri_dogrula(a.urunler)
        ayrinti = None
        if a.ayrinti:
            ayrinti = ayrinti_oku(a.ayrinti[0])
            for fazla in a.ayrinti[1:]:
                print("UYARI: tek ham tablo kuralı: %s yazılmadı (yalnız ilk ayrıntı dosyası yazılır)" % fazla)
        ham_yedek = tsv_oku(a.urunler)
    except Hata as e:
        print("HATA: %s" % e)
        return 1
    yaz(urunler, a.kaynak, a.cikti, ayrinti, ham_yedek)
    hatalar = olc(a.cikti, len(urunler))
    if hatalar:
        for h in hatalar:
            print("HATA: ölçüm tutmadı: %s" % h)
        return 1
    if a.kopya:
        # dosya yolu (.xlsx ile biten ya da var olan dosya) → o dosyaya; aksi halde klasör
        dosya_mi = a.kopya.lower().endswith(".xlsx") or os.path.isfile(a.kopya)
        hedef_dizin = os.path.dirname(os.path.abspath(a.kopya)) if dosya_mi else a.kopya
        os.makedirs(hedef_dizin, exist_ok=True)
        shutil.copy2(a.cikti, a.kopya if dosya_mi else os.path.join(a.kopya, os.path.basename(a.cikti)))
    say = {k: sum(1 for r in urunler if r["karar"] == k) for k in KARARLAR}
    print("TAMAM %s · %d ürün (SAT %d / SAT-koşullu %d / İZLE %d / ELE %d)" % (a.cikti, len(urunler), say["SAT"], say["SAT (koşullu)"], say["İZLE"], say["ELE"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
