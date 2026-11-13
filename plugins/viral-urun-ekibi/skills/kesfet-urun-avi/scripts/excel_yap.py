#!/usr/bin/env python3
"""excel_yap.py [PROJE_KLASORU] [CIKTI.xlsx]

is/kesfet/urunler.md (+ rakipler.md, marka-skorlari.md) → is/kesfet/kesfet-urunler.xlsx
Sayfalar: Ürünler (renkli karar, filtre, donmuş başlık) · Marka Skorları · Rakip & Notlar · Özet.
Yazdıktan sonra dosyayı yeniden açar ve satır sayısını md ile karşılaştırır; tutmazsa çıkış kodu 1.
Gerekli paket: openpyxl  (kur: python3 -m pip install --user openpyxl  ·  Windows: py -m pip install openpyxl)
"""
import os
import re
import sys
from collections import Counter

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:
    sys.exit("HATA: openpyxl yok. Kur: python3 -m pip install --user openpyxl  (Windows: py -m pip install openpyxl)")

BASLIK = ["#", "Ürün", "Hesap", "İzlenme", "Beğeni", "Profil notu", "Site / fiyat", "Karar", "Neden"]
GENISLIK = [5, 45, 22, 11, 10, 45, 35, 14, 70]
RENK = {"AL": "C6EFCE", "YEDEK": "FFEB9C", "ELE": "FFC7CE"}
KOYU = PatternFill("solid", fgColor="1F2937")


def tablo_oku(yol, ilk_hucre_sayi=True):
    satirlar = []
    if not os.path.exists(yol):
        return satirlar
    for line in open(yol, encoding="utf-8"):
        if not line.startswith("|") or re.match(r"^\|\s*-", line):
            continue
        hucre = [c.strip() for c in line.strip().strip("|").split("|")]
        if ilk_hucre_sayi and not re.match(r"^\d+$", hucre[0]):
            continue
        satirlar.append(hucre)
    return satirlar


def baslik_yaz(ws, basliklar, genislikler):
    ws.append(basliklar)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = KOYU
        c.alignment = Alignment(vertical="center", wrap_text=True)
    for i, w in enumerate(genislikler, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def karar_anahtari(deger):
    deger = str(deger or "").strip()
    return deger.split()[0] if deger else ""


def main():
    proje = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    kesfet = os.path.join(proje, "is", "kesfet")
    cikti = sys.argv[2] if len(sys.argv) > 2 else os.path.join(kesfet, "kesfet-urunler.xlsx")
    md = os.path.join(kesfet, "urunler.md")
    if not os.path.exists(md):
        sys.exit(f"HATA: {md} yok — önce baslat.sh")

    urunler = [(r[:9] + [""] * 9)[:9] for r in tablo_oku(md)]
    wb = Workbook()
    ws = wb.active
    ws.title = "Ürünler"
    baslik_yaz(ws, BASLIK, GENISLIK)
    for r in urunler:
        r[0] = int(r[0])
        ws.append(r)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)
        k = karar_anahtari(row[7].value)
        if k in RENK:
            row[7].fill = PatternFill("solid", fgColor=RENK[k])
            row[7].font = Font(bold=True)
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions

    skorlar = tablo_oku(os.path.join(kesfet, "marka-skorlari.md"), ilk_hucre_sayi=False)
    skorlar = [s for s in skorlar if s and s[0] != "# (urunler.md)"]
    ws_s = wb.create_sheet("Marka Skorları")
    baslik_yaz(ws_s, ["# (urunler.md)", "Hesap", "Odak", "Süreklilik", "Kimlik", "Site", "Tekrar", "TOPLAM",
                      "Sınıf", "Etiket", "Not"], [10, 24, 7, 10, 8, 6, 8, 9, 12, 14, 60])
    for s in skorlar:
        ws_s.append(s)

    ws_r = wb.create_sheet("Rakip & Notlar")
    baslik_yaz(ws_r, ["Not"], [160])
    rak = os.path.join(kesfet, "rakipler.md")
    if os.path.exists(rak):
        for line in open(rak, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("# "):
                ws_r.append([line.lstrip("- ")])
                ws_r.cell(ws_r.max_row, 1).alignment = Alignment(wrap_text=True)

    sayim = Counter(karar_anahtari(r[7]) for r in urunler)
    ws_o = wb.create_sheet("Özet")
    baslik_yaz(ws_o, ["Karar", "Adet"], [14, 10])
    for k in ["AL", "YEDEK", "ELE"]:
        ws_o.append([k, sayim.get(k, 0)])
    ws_o.append(["Toplam", len(urunler)])

    os.makedirs(os.path.dirname(os.path.abspath(cikti)), exist_ok=True)
    wb.save(cikti)

    # Doğrulama: dosyayı yeniden aç, satır sayısı md ile aynı mı?
    okunan = load_workbook(cikti, read_only=True)["Ürünler"].max_row - 1
    durum = "TAMAM" if okunan == len(urunler) else "UYUŞMAZLIK"
    print(f"{durum}: {cikti} | md={len(urunler)} excel={okunan} | "
          f"AL={sayim.get('AL', 0)} YEDEK={sayim.get('YEDEK', 0)} ELE={sayim.get('ELE', 0)} | marka skoru={len(skorlar)}")
    sys.exit(0 if durum == "TAMAM" else 1)


if __name__ == "__main__":
    main()
