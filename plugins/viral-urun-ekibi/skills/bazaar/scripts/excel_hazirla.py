#!/usr/bin/env python3
"""excel_hazirla.py [KLASOR] [CIKTI.xlsx] [--marj-sonuc marj-sonuc.tsv]

Bazaar hazırlayıcısı (0.4.0): KLASOR/adaylar.tsv (+ marj-sonuc.tsv) → ortak şablonlu Excel (3 sayfa, 10 sütun).
KLASOR varsayılanı is/firsat/trendyol; çıktı varsayılanı KLASOR/urunler.xlsx.
Bu betik yalnız iki iş yapar: urunler.tsv hazırlar, sonra ortak/excel_yaz.py'yi alt süreç olarak çağırıp çıkış kodunu aynen döndürür.
Karar: `karar` sütunu aynen; boşsa on_karar (SAT-ADAYI → İZLE). SAT ve SAT (koşullu) yalnız kanıt dosyası (is/firsat/kanit/NN-*.md) varsa yazılır; SAT (koşullu) = marj ya da viral doğrulanamadı, diğer ölçütler SAT.
İlgi = "N yorum · puan". Marj çarpanı tr_marj.py'nin marj-sonuc.tsv dosyasından gelir; betik kendi hesaplamaz.
Çıkış: excel_yaz.py ile aynı (0 TAMAM · 1 veri hatası · 2 kullanım · 3 openpyxl yok).
"""
import csv
import datetime
import glob
import os
import re
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
ALANLAR = ["urun", "link", "ilgi", "ilgi_sayi", "alis", "satis", "para", "marj_kat", "karar", "neden", "kaynak", "tarih"]
ADAY_ALANLAR = ["no", "urun", "trendyol_link", "alis_tl", "yorum", "puan", "satici_sayisi", "satici", "gorsel_bakildi",
                "mekanizma", "aile", "viral_db", "viral_video", "meta_reklam", "onerilen_satis_tl", "on_karar", "karar",
                "neden", "okuma_tarihi"]
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


def tsv_satirlar(yol):
    with open(yol, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.reader(f, delimiter="\t") if any(h.strip() for h in r)]


def hazirla(klasor, marj_yol, tsv_cikti):
    adaylar_yol = os.path.join(klasor, "adaylar.tsv")
    s = tsv_satirlar(adaylar_yol)
    if not s or [h.strip() for h in s[0]] != ADAY_ALANLAR:
        raise SystemExit("HATA: adaylar.tsv başlığı tam %d alan olmalı (bazaar_kontrol.py denetle)" % len(ADAY_ALANLAR))
    mtime = datetime.date.fromtimestamp(os.path.getmtime(adaylar_yol)).isoformat()
    marj = {}
    if marj_yol and os.path.isfile(marj_yol):
        m = tsv_satirlar(marj_yol)
        for r in m[1:]:
            d = dict(zip(m[0], r))
            marj[d.get("urun", "").strip().lower()] = d
    kanit_dir = os.path.join(os.path.dirname(os.path.abspath(klasor)), "kanit")
    n_yazilan = 0
    with open(tsv_cikti, "w", encoding="utf-8", newline="") as f:
        f.write("\t".join(ALANLAR) + "\n")
        for ham in s[1:]:
            r = dict(zip(ADAY_ALANLAR, [h.strip() for h in ham + [""] * (len(ADAY_ALANLAR) - len(ham))]))
            karar = r["karar"] or {"SAT-ADAYI": "İZLE", "SAT-KOSULLU": "İZLE", "İZLE": "İZLE", "ELE": "ELE"}.get(r["on_karar"], "")
            if not karar:
                continue
            neden = r["neden"]
            if karar in ("SAT", "SAT (koşullu)"):
                no = re.sub(r"\D", "", r["no"]).zfill(2)
                if not glob.glob(os.path.join(kanit_dir, no + "-*.md")):
                    karar, neden = "İZLE", "%s denmiş ama kanıt dosyası yok; kanıt yazılana kadar İZLE." % karar
                elif karar == "SAT (koşullu)" and not re.search(r"koşul|doğrulanamad|dogrulanamad", neden, re.I):
                    neden = (neden + " " if neden else "") + "Koşul: marj ya da viral doğrulanamadı (kanıt dosyasına bak)."
            puan = r["puan"].replace(".", ",")
            ilgi = ("%s yorum" % r["yorum"]) + ((" · " + puan) if puan else "") if r["yorum"] else ""
            yorum_sayi = re.sub(r"[.,\s]", "", r["yorum"])
            mr = marj.get(r["urun"].lower(), {})
            kat = (mr.get("carpan") or "").replace("hesaplanmadi", "")
            alan = [r["urun"], r["trendyol_link"], ilgi, yorum_sayi if yorum_sayi.isdigit() else "", r["alis_tl"],
                    r["onerilen_satis_tl"], "TRY", kat, karar, kisalt(neden or "Karar bekliyor."), "Trendyol",
                    r["okuma_tarihi"] if re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["okuma_tarihi"]) else mtime]
            f.write("\t".join(h.replace("\t", " ").replace("\n", " ") for h in alan) + "\n")
            n_yazilan += 1
    return n_yazilan


def main():
    arg = sys.argv[1:]
    marj = None
    if "--marj-sonuc" in arg:
        i = arg.index("--marj-sonuc")
        marj = arg[i + 1]
        del arg[i:i + 2]
    klasor = arg[0] if arg else os.path.join("is", "firsat", "trendyol")
    cikti = arg[1] if len(arg) > 1 else os.path.join(klasor, "urunler.xlsx")
    marj = marj or os.path.join(klasor, "marj-sonuc.tsv")
    if not os.path.isfile(os.path.join(klasor, "adaylar.tsv")):
        sys.exit("HATA: %s yok" % os.path.join(klasor, "adaylar.tsv"))
    with tempfile.TemporaryDirectory(prefix="bazaar_excel_") as d:
        urunler = os.path.join(d, "urunler.tsv")
        if hazirla(klasor, marj, urunler) == 0:
            print("HATA: adaylar.tsv'de karar ya da on_karar dolu satır yok (önce bazaar_kontrol.py denetle)")
            return 1
        r = subprocess.run([sys.executable, excel_yaz_yolu(), "--urunler", urunler, "--kaynak", "bazaar",
                            "--cikti", cikti, "--ayrinti", os.path.join(klasor, "adaylar.tsv")])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
