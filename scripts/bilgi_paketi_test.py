#!/usr/bin/env python3
"""viral-urunler.tsv sansür testi. Kullanım: python3 scripts/bilgi_paketi_test.py [tsv] [--db analiz.db]
Çıkış 0 temiz · 1 KALDI. Kara liste (~/.config/viral-urun-ekibi/yasak.txt) okunur ama içeriği HİÇBİR yere yazılmaz;
ihlalde yalnız satır/sütun/desen sırası basılır. --db verilirse üretim iki kez koşulup bayt bayt aynılığı da ölçülür."""
import os
import re
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(KOK, "plugins", "viral-urun-ekibi", "ortak", "bilgi", "viral-urunler.tsv")
YASAK = os.environ.get("YASAK_DOSYASI", os.path.join(os.path.expanduser("~"), ".config", "viral-urun-ekibi", "yasak.txt"))
BEYAZ = ["urun_id", "ad_jenerik", "aile", "nis", "pazarlar", "video_sayisi", "hesap_sayisi", "viral_hesap_sayisi",
         "en_yuksek_izlenme", "toplam_izlenme", "medyan_izlenme_takipci", "ilk_gorulme", "son_gorulme", "hukum", "guncelleme"]
DESENLER = [
    ("@ işareti", re.compile(r"@")),
    ("http/www", re.compile(r"https?:|www\.|://", re.I)),
    ("e-posta", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("telefon", re.compile(r"\+\d[\d\s().-]{7,}\d|\(?\d{2,4}\)?[\s.-]\d{3,4}[\s.-]\d{2,4}(?:[\s.-]\d{2,4})?")),
    ("ev dizini yolu", re.compile(r"/Us" + r"ers/|/ho" + r"me/|~/|[A-Za-z]:\\Us" + r"ers", re.I)),
    ("alan adı", re.compile(r"\b[\w-]+\.(?:com|net|org|store|shop|co|io|app|me|tr|de|es)\b", re.I)),
]


def yasak_desenleri():
    out = []
    try:
        with open(YASAK, encoding="utf-8") as f:
            for satir in f:
                satir = satir.strip()
                if not satir or satir.startswith("#"):
                    continue
                try:
                    out.append(re.compile(satir, re.I))
                except re.error:
                    pass
    except OSError:
        return None
    return out


def kontrol(metin, yasaklar):
    """TSV metni -> ihlal listesi (desen adı/sırası, satır, sütun; içerik YOK)."""
    ih = []
    satirlar = metin.split("\n")
    if satirlar and satirlar[-1] == "":
        satirlar.pop()
    if not satirlar:
        return ["boş dosya"]
    if satirlar[0].split("\t") != BEYAZ:
        ih.append("sütunlar beyaz listeyle birebir değil")
    for n, s in enumerate(satirlar[1:], 2):
        hucre = s.split("\t")
        if len(hucre) != len(BEYAZ):
            ih.append("satır %d: sütun sayısı %d (beklenen %d)" % (n, len(hucre), len(BEYAZ)))
            continue
        for i, h in enumerate(hucre):
            for ad, d in DESENLER:
                if d.search(h):
                    ih.append("satır %d sütun %s: %s" % (n, BEYAZ[i], ad))
            for k, d in enumerate(yasaklar or []):
                if d.search(h):
                    ih.append("satır %d sütun %s: yasak desen #%d" % (n, BEYAZ[i], k + 1))
    return ih


def main(argv):
    yol, db = TSV, None
    a = argv[1:]
    if "--db" in a:
        db = a[a.index("--db") + 1]
        del a[a.index("--db"):a.index("--db") + 2]
    if a:
        yol = a[0]
    yasaklar = yasak_desenleri()
    hata = []
    if yasaklar is None or not yasaklar:
        hata.append("yasak.txt okunamadı/boş: kara liste kapısı ÖLÇÜLEMEDİ")
    if not os.path.isfile(yol):
        print("KALDI: tsv yok")
        return 1
    metin = open(yol, encoding="utf-8").read()
    ih = kontrol(metin, yasaklar)
    hata += ih
    n = max(0, metin.count("\n") - 1)
    if n < 100:
        hata.append("çok az satır (%d)" % n)
    # kırma 1: sahte satır YAKALANMALI
    sahte = metin + "\t".join(["vdeadbeef", "ornek @ornekhesap https://x", "", "", "", "1", "1", "0", "", "", "", "", "", "VIRAL-VIDEO", ""]) + "\n"
    k = kontrol(sahte, yasaklar)
    if not any("@ işareti" in x for x in k) or not any("http/www" in x for x in k):
        hata.append("KIRMA TUTMADI: @ornekhesap / https://x sahte satırı yakalanmadı (kapı ölçülmemiş)")
    # kırma 2: fazladan sütun YAKALANMALI
    if not kontrol(metin.replace("\tguncelleme\n", "\tguncelleme\turl\n", 1), yasaklar):
        hata.append("KIRMA TUTMADI: ek sütun yakalanmadı")
    # kırma 3: kara liste deseni YAKALANMALI (sentetik desen; gerçek içerik kullanılmaz)
    ky = kontrol(metin + "\t".join(["vdeadbeef", "zzqkaranlistesinavi", "", "", "", "1", "1", "0", "", "", "", "", "", "X", ""]) + "\n",
                 [re.compile("zzqkaranlistesinavi", re.I)])
    if not any("yasak desen" in x for x in ky):
        hata.append("KIRMA TUTMADI: kara liste deseni yakalanmadı")
    # kırma 4: telefon / e-posta / ev yolu
    for ad, parca in (("telefon", "+90 532 123 45 67"), ("e-posta", "ali.veli.x1y"), ("ev dizini yolu", "/Us" + "ers/biri/x")):
        satir = "\t".join(["vdeadbeef", "ornek " + (parca if ad != "e-posta" else "ali@ornek.com"), "", "", "", "1", "1", "0", "", "", "", "", "", "X", ""]) + "\n"
        if not any(ad in x or (ad == "e-posta" and "@" in x) for x in kontrol(metin + satir, [])):
            hata.append("KIRMA TUTMADI: %s yakalanmadı" % ad)
    # determinizm
    if db:
        betik = os.path.join(KOK, "scripts", "bilgi_paketi.py")
        with tempfile.TemporaryDirectory() as d:
            a1, a2 = os.path.join(d, "a.tsv"), os.path.join(d, "b.tsv")
            for o in (a1, a2):
                if subprocess.call([sys.executable, betik, db, "--cikti", o], stdout=subprocess.DEVNULL) != 0:
                    hata.append("üretim betiği hata verdi")
            if os.path.isfile(a1) and os.path.isfile(a2) and open(a1, "rb").read() != open(a2, "rb").read():
                hata.append("üretim deterministik değil")
            if os.path.isfile(a1) and open(a1, "rb").read() != open(yol, "rb").read():
                hata.append("depodaki TSV db'den üretilenle farklı (yeniden üret)")
    for h in hata:
        print("KALDI: " + h)
    print("bilgi_paketi_test: %s (%d satır, %d kara liste deseni okundu)" % ("KALDI" if hata else "GEÇTİ", n, len(yasaklar or [])))
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
