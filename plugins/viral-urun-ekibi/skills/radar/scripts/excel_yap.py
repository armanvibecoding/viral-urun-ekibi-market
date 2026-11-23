#!/usr/bin/env python3
"""excel_yap.py [PROJE_KLASORU] [CIKTI.xlsx] [--md urunler.md]

Radar hazırlayıcısı (0.4.0): is/kesfet/urunler.md → ortak şablonlu Excel (3 sayfa, 10 sütun).
Bu betik yalnız iki iş yapar: urunler.tsv hazırlar, sonra ortak/excel_yaz.py'yi alt süreç olarak çağırıp çıkış kodunu aynen döndürür.
Karar eşlemesi: AL ve AL (sezonluk) → SAT (sezonluk notu Neden'in başına) · YEDEK → İZLE · ELE → ELE.
İlgi = izlenme. Tarih = urunler.md'nin son değişiklik günü (satırlarda okuma tarihi tutulmuyor).
Marka Skorları, Rakip & Notlar ve Özet sayfaları Excel'e girmez; marka-skorlari.md ve rakipler.md dosyalarında durur.
Çıkış: excel_yaz.py ile aynı (0 TAMAM · 1 veri hatası · 2 kullanım · 3 openpyxl yok).
"""
import datetime
import os
import re
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
ALANLAR = ["urun", "link", "ilgi", "ilgi_sayi", "alis", "satis", "para", "marj_kat", "karar", "neden", "kaynak", "tarih"]
KARAR = {"AL": "SAT", "YEDEK": "İZLE", "ELE": "ELE"}
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


def kisa_ad(urun, n=70):
    """Ürün hücresi kısa ad olmalı: uzunsa ilk parantez ya da tireden önceki kısmı al."""
    u = " ".join((urun or "").split())
    if len(u) > n:
        for ayrac in (" (", " — ", " - "):
            if ayrac in u:
                u = u.split(ayrac)[0]
                break
    return kisalt(u, n)


def tablo_oku(yol):
    satirlar = []
    for line in open(yol, encoding="utf-8"):
        if not line.startswith("|") or re.match(r"^\|\s*-", line):
            continue
        hucre = [c.strip() for c in line.strip().strip("|").split("|")]
        if re.match(r"^\d+$", hucre[0]):
            satirlar.append(hucre)
    return satirlar


def izlenme(metin):
    """'22,2M' → (22200000.0, '22,2 Mn izlenme'); '412B' → (412000.0, '412 Bin izlenme'); '9.949' → (9949.0, '9.949 izlenme')."""
    t = (metin or "").strip()
    m = re.match(r"^(\d[\d.,]*)\s*(milyon|mn|m|bin|b|k)?(?![A-Za-zÇĞİÖŞÜçğıöşü])", t, re.I)
    if not m:
        return None, (t + " izlenme" if t and t != "-" else "")
    ham, ek = m.group(1), (m.group(2) or "").lower()
    try:
        if ek:
            deger = float(ham.replace(",", "."))
            if ek in ("m", "mn", "milyon"):
                return deger * 1e6, "%s Mn izlenme" % ham
            return deger * 1e3, "%s Bin izlenme" % ham
        return float(ham.replace(".", "").replace(",", ".")), "%s izlenme" % ham
    except ValueError:
        return None, t + " izlenme"


def link_yap(site):
    ilk = (site or "").split()[0] if (site or "").strip() else ""
    if re.match(r"^https?://", ilk):
        return ilk
    if re.match(r"^[\w.-]+\.[a-z]{2,}(/\S*)?$", ilk, re.I):
        return "https://" + ilk
    return ""


def hazirla(md, tsv):
    tarih = datetime.date.fromtimestamp(os.path.getmtime(md)).isoformat()
    satirlar = [(r + [""] * 9)[:9] for r in tablo_oku(md)]
    with open(tsv, "w", encoding="utf-8", newline="") as f:
        f.write("\t".join(ALANLAR) + "\n")
        for no, urun, hesap, izl, begeni, profil, site, karar, neden in satirlar:
            anahtar = karar.split()[0].upper() if karar.split() else ""
            if anahtar not in KARAR:
                continue
            sezonluk = "sezonluk" in karar.lower()
            sayi, ilgi = izlenme(izl)
            neden = ("Sezonluk: " if sezonluk else "") + (neden or "")
            alan = [kisa_ad(urun), link_yap(site), ilgi, "" if sayi is None else "%d" % sayi, "", "", "", "",
                    KARAR[anahtar], kisalt(neden.replace("\t", " ")), "Instagram", tarih]
            f.write("\t".join(h.replace("\t", " ").replace("\n", " ") for h in alan) + "\n")
    return len(satirlar)


def main():
    arg = sys.argv[1:]
    md = None
    if "--md" in arg:
        i = arg.index("--md")
        md = arg[i + 1]
        del arg[i:i + 2]
    proje = arg[0] if len(arg) > 0 else os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    kesfet = os.path.join(proje, "is", "kesfet")
    cikti = arg[1] if len(arg) > 1 else os.path.join(kesfet, "kesfet-urunler.xlsx")
    md = md or os.path.join(kesfet, "urunler.md")
    if not os.path.exists(md):
        sys.exit("HATA: %s yok — önce baslat.sh" % md)
    with tempfile.TemporaryDirectory(prefix="radar_excel_") as d:
        tsv = os.path.join(d, "urunler.tsv")
        hazirla(md, tsv)
        r = subprocess.run([sys.executable, excel_yaz_yolu(), "--urunler", tsv, "--kaynak", "radar",
                            "--cikti", cikti, "--ayrinti", md])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
