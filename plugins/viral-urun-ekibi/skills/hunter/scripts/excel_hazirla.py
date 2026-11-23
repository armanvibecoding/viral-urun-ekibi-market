#!/usr/bin/env python3
"""excel_hazirla.py [PROJE_KLASORU] [CIKTI.xlsx] [--adaylar adaylar.md] [--marj-sonuc marj-sonuc.tsv]

Hunter hazırlayıcısı (0.4.0): is/firsat/adaylar.md (+ marj_hesap.py --cikti dosyası) → ortak şablonlu Excel
(3 sayfa, 10 sütun): is/firsat/firsat-urunler.xlsx.
Bu betik yalnız iki iş yapar: urunler.tsv hazırlar, sonra ortak/excel_yaz.py'yi alt süreç olarak çağırıp çıkış kodunu aynen döndürür.
Karar eşlemesi: SAT → SAT (yalnız kanıt dosyası varsa; yoksa İZLE) · İZLE, AÇIK, KISA LİSTE → İZLE · ELE → ELE.
Alış, satış, para ve marj çarpanı marj sonucundan gelir (ürün adıyla eşleşirse); yoksa "Normal fiyat" sütunundan yalnız alış okunur.
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
KARAR = {"SAT": "SAT", "IZLE": "İZLE", "ACIK": "İZLE", "AÇIK": "İZLE", "KISA": "İZLE", "ELE": "ELE"}
PARA = {"$": "USD", "€": "EUR", "£": "GBP", "₺": "TRY"}
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


def md_tablo(yol):
    """İlk başlıklı Markdown tablosu: [{sütun adı: hücre}]."""
    baslik, satirlar = None, []
    for line in open(yol, encoding="utf-8"):
        if not line.startswith("|"):
            if baslik and satirlar:
                break
            continue
        if re.match(r"^\|[\s:\-|]+\|\s*$", line):
            continue
        h = [c.strip() for c in line.strip().strip("|").split("|")]
        if baslik is None:
            baslik = h
        else:
            satirlar.append(dict(zip(baslik, h + [""] * (len(baslik) - len(h)))))
    return satirlar


def sutun(r, *adaylar):
    for k in r:
        for a in adaylar:
            if k.lower().startswith(a.lower()):
                return r[k]
    return ""


def satis_oku(metin):
    """'57 sold (sayfa) · 5,0/8' → (57, '57 satış'); '1,2k sold' → (1200, '1,2k satış')."""
    m = re.search(r"(\d[\d.,]*)\s*(k|bin)?\+?\s*(sold|satış|satildi|satıldı|adet)", metin or "", re.I)
    if not m:
        t = " ".join((metin or "").split())
        return None, (t[:22] if t and t != "-" else "")
    ham, k = m.group(1), (m.group(2) or "").lower()
    try:
        deger = float(ham.replace(",", ".")) * 1000 if k else float(ham.replace(".", "").replace(",", "."))
    except ValueError:
        return None, ham + " satış"
    return int(deger), "%s%s satış" % (ham, (" " + k) if k else "")


def fiyat_oku(metin):
    m = re.search(r"([$€£₺])\s*(\d[\d.,]*)|(\d[\d.,]*)\s*(TL|₺)", metin or "")
    if not m:
        return "", ""
    if m.group(1):
        sayi, para = m.group(2), PARA[m.group(1)]
    else:
        sayi, para = m.group(3), "TRY"
    if "," in sayi and "." in sayi:
        sayi = sayi.replace(".", "").replace(",", ".")
    elif "," in sayi:
        sayi = sayi.replace(",", ".")
    return sayi, para


def hazirla(adaylar_yol, marj_yol, proje, tsv_cikti):
    mtime = datetime.date.fromtimestamp(os.path.getmtime(adaylar_yol)).isoformat()
    marj = {}
    if marj_yol and os.path.exists(marj_yol):
        with open(marj_yol, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                marj[(r.get("urun") or "").strip().lower()] = r
    elenen = {}
    elen_yol = os.path.join(os.path.dirname(adaylar_yol), "elenenler.md")
    if os.path.exists(elen_yol):
        for r in md_tablo(elen_yol):
            elenen[sutun(r, "Ürün").lower()] = sutun(r, "Sebep")
    yazilan = 0
    with open(tsv_cikti, "w", encoding="utf-8", newline="") as f:
        f.write("\t".join(ALANLAR) + "\n")
        for r in md_tablo(adaylar_yol):
            urun = sutun(r, "Ürün")
            if not urun or urun.startswith("<"):
                continue
            durum = sutun(r, "Durum")
            ilk = re.split(r"[\s—–-]+", durum.strip(), maxsplit=1)[0].upper().replace("İ", "I") if durum.strip() else ""
            if ilk not in KARAR:
                continue
            karar = KARAR[ilk]
            neden = re.split(r"\s[—–]\s", durum, maxsplit=1)[1] if re.search(r"\s[—–]\s", durum) else ""
            if karar == "SAT":
                kanit = re.search(r"(is/firsat/kanit/\S+?\.md)", durum)
                if not (kanit and os.path.isfile(os.path.join(proje, kanit.group(1)))):
                    karar, neden = "İZLE", "SAT denmiş ama kanıt dosyası bulunamadı; kanıt yazılana kadar İZLE."
                else:
                    neden = "Kanıt dosyası var: " + kanit.group(1)
            elif karar == "ELE":
                neden = elenen.get(urun.lower(), "") or neden or "Elendi (sebep elenenler.md'de)."
            if not neden:
                neden = sutun(r, "Zaten viral") or "Karar bekliyor."
            n, ilgi = satis_oku(sutun(r, "Ürün satışı", "Urun satisi"))
            link = sutun(r, "Ali link")
            link = link if re.match(r"^https?://", link) else ""
            m = marj.get(urun.lower())
            if m:
                alis, satis, para, kat = m.get("urun_maliyeti", ""), m.get("satis", ""), m.get("para", ""), m.get("carpan", "")
                para = para if para in ("TRY", "USD", "EUR", "GBP") else ""
            else:
                alis, para = fiyat_oku(sutun(r, "Normal fiyat"))
                satis, kat = "", ""
            alan = [urun, link, ilgi, "" if n is None else str(n), alis, satis, para, kat, karar,
                    kisalt(neden), "AliExpress", mtime]
            f.write("\t".join(h.replace("\t", " ").replace("\n", " ") for h in alan) + "\n")
            yazilan += 1
    return yazilan


def main():
    arg = sys.argv[1:]
    secenek = {}
    for ad in ("--adaylar", "--marj-sonuc"):
        if ad in arg:
            i = arg.index(ad)
            secenek[ad] = arg[i + 1]
            del arg[i:i + 2]
    proje = arg[0] if len(arg) > 0 else os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    firsat = os.path.join(proje, "is", "firsat")
    cikti = arg[1] if len(arg) > 1 else os.path.join(firsat, "firsat-urunler.xlsx")
    adaylar = secenek.get("--adaylar") or os.path.join(firsat, "adaylar.md")
    marj = secenek.get("--marj-sonuc") or os.path.join(firsat, "marj-sonuc.tsv")
    if not os.path.exists(adaylar):
        sys.exit("HATA: %s yok" % adaylar)
    with tempfile.TemporaryDirectory(prefix="hunter_excel_") as d:
        urunler = os.path.join(d, "urunler.tsv")
        if hazirla(adaylar, marj, proje, urunler) == 0:
            print("HATA: adaylar.md'de Durum'u SAT / İZLE / AÇIK / KISA LİSTE / ELE olan satır yok")
            return 1
        r = subprocess.run([sys.executable, excel_yaz_yolu(), "--urunler", urunler, "--kaynak", "hunter",
                            "--cikti", cikti, "--ayrinti", adaylar])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
