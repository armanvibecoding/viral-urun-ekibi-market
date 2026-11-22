#!/usr/bin/env python3
"""karne_uret.py kırma testi (sentetik proje). Kullanım: python3 karne_test.py → hepsi geçerse 0."""
import json
import os
import subprocess
import sys
import tempfile

BURASI = os.path.dirname(os.path.abspath(__file__))
KARNE = os.path.join(BURASI, "karne_uret.py")
SONUC = []


def yaz(yol, icerik):
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(icerik)


def kos(proje, *a):
    r = subprocess.run([sys.executable, KARNE, "--proje", proje, "--bugun", "2026-03-20"] + list(a), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def satir(cikti, rol):
    return next((s for s in cikti.splitlines() if s.startswith("| %s |" % rol)), "")


def bekle(ad, kosul, cikti=""):
    SONUC.append((ad, bool(kosul)))
    if not kosul:
        print("--- %s\n%s" % (ad, cikti))


def main():
    kok = tempfile.mkdtemp(prefix="karne_test_")
    bos = os.path.join(kok, "bos"); os.makedirs(os.path.join(bos, ".ekip"))
    k, c = kos(bos)
    bekle("boş proje: 10 rol satırı, hepsi 'veri yok', uydurma sayı yok",
          k == 0 and c.count("| veri yok |") == 10 and "Verisi olan rol: 0 / 10" in c and "%" not in "".join(s.split("|")[3] for s in c.splitlines() if s.startswith("| ") and "Rol" not in s and "---" not in s), c)
    bekle("boş proje: her satır eksik kaynağı söyler", c.count("eksik:") == 10, c)
    bekle("boş proje: KARNE.md ve karne.jsonl yazıldı", os.path.exists(os.path.join(bos, ".ekip", "KARNE.md")) and os.path.exists(os.path.join(bos, ".ekip", "karne.jsonl")))

    p = os.path.join(kok, "dolu"); e = os.path.join(p, ".ekip")
    yaz(os.path.join(p, "is", "firsat", "ivme.csv"), "urun,pazar,olcum,tarih,reklam_sayisi\na,US,t0,2026-03-01,2\na,US,t7,2026-03-08,6\nb,US,t0,2026-03-01,5\nb,US,t7,2026-03-08,3\nc,US,t0,2026-03-10,1\n")
    yaz(os.path.join(p, "is", "firsat", "kanit", "01-a.md"), "# a\nsonuc_30gun: ayakta\n")
    yaz(os.path.join(p, "is", "firsat", "kanit", "02-b.md"), "# b\nsonuc_30gun: birakildi\n")
    yaz(os.path.join(p, "is", "firsat", "kanit", "03-c.md"), "# c (henüz sonuç yok)\n")
    yaz(os.path.join(p, "is", "kesfet", "desen-test.tsv"), "desen\ttuttu\nK2\tevet\nK7\thayir\nK9\tevet\nK12\tevet\n")
    yaz(os.path.join(p, "is", "01-urun", "yayin", "olcum.csv"),
        "video,platform,saat,izlenme,ort_izlenme_sn,tutma_yuzde,begeni,yorum,cta_yorum,paylasim,kaydetme\n"
        "01,instagram,48,10000,,,200,,,100,\n02,instagram,48,20000,,,300,,,100,\n03,instagram,48,500,,,5,,,400,\n04,instagram,48,,,,,,,,\n")
    yaz(os.path.join(e, "juri-kalibrasyon.jsonl"), json.dumps({"tarih": "2026-03-10", "n": 12, "kopya": 3, "rho": 0.31, "hukum": "ZAYIF"}) + "\n"
        + json.dumps({"tarih": "2026-03-18", "n": 20, "kopya": 3, "rho": 0.56, "hukum": "UYUMLU"}) + "\n")
    j = [{"video": "V01", "tur": 1, "mod": "teslim", "gecti": False}, {"video": "V01", "tur": 2, "mod": "teslim", "gecti": True},
         {"video": "V02", "tur": 1, "mod": "teslim", "gecti": False}, {"video": "V02", "tur": 4, "mod": "teslim", "gecti": True},
         {"video": "V03", "tur": 1, "mod": "teslim", "gecti": True}]
    yaz(os.path.join(p, "is", "01-urun", "elestiri", "juri.jsonl"), "".join(json.dumps(x) + "\n" for x in j))
    def kapi(t, sonuc, ses1, ses2):
        return {"tarih": t, "gecis": "yayin", "is": "01-urun", "sonuc": sonuc, "kapilar": [
            {"kapi": "teknik@V01", "durum": "GEÇTİ"}, {"kapi": "ses@V01", "durum": ses1}, {"kapi": "goruntu@V01", "durum": "GEÇTİ"},
            {"kapi": "teknik@V02", "durum": "GEÇTİ"}, {"kapi": "ses@V02", "durum": ses2}, {"kapi": "goruntu@V02", "durum": "KALDI"},
            {"kapi": "kurgu@V01", "durum": "UYGULANMAZ"}, {"kapi": "defter", "durum": "GEÇTİ"}]}
    satirlar = [kapi("2026-03-18T10:00:00", "KALDI", "GEÇTİ", "KALDI"), kapi("2026-03-19T10:00:00", "AŞIMLA GEÇTİ", "GEÇTİ", "GEÇTİ"),
                {"tarih": "2026-03-17T09:00:00", "gecis": "kredi", "is": "01-urun", "sonuc": "GEÇTİ", "kapilar": []}]
    yaz(os.path.join(e, "kapi.jsonl"), "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in satirlar))
    yaz(os.path.join(p, "is", "01-urun", "magaza", "analitik.csv"),
        "tarih,oturum,sepete_ekleme,siparis\n2026-03-08,100,4,1\n2026-03-12,100,6,1\n2026-03-15,200,16,2\n2026-03-19,200,14,3\n")
    k, c = kos(p)
    bekle("dolu proje: avcı 1/2 büyüdü = %50, 2/3 aday yeniden okundu", "%50" in satir(c, "Fırsat avcısı") and "2 / 3 aday" in satir(c, "Fırsat avcısı"), c)
    bekle("dolu proje: savcı 1/2 ayakta = %50 (sonuçsuz dosya paydaya girmez)", "%50" in satir(c, "Kanıt savcısı") and "2 / 3 SAT" in satir(c, "Kanıt savcısı"), c)
    bekle("dolu proje: analist 3/4 = %75", "%75" in satir(c, "Kreatif analisti"), c)
    bekle("dolu proje: stratejist medyanı %0,75 (izlenme < 2000 ve boş satır hesaba girmez)", "%0,75" in satir(c, "İçerik stratejisti") and "2 video" in satir(c, "İçerik stratejisti"), c)
    bekle("dolu proje: jüri ρ 0,56 UYUMLU, değişim +0,25", "ρ 0,56 (UYUMLU)" in satir(c, "Kör jüri") and "+0,25" in satir(c, "Kör jüri"), c)
    bekle("dolu proje: direktör 2 kalan videodan 1'i ≤ 3 turda geçti = %50", "%50" in satir(c, "Direktör") and "2 kalan video" in satir(c, "Direktör"), c)
    bekle("dolu proje: ses ilk koşuda 1/2 = %50 (ikinci koşu sayılmaz)", "%50" in satir(c, "Ses tasarımcısı"), c)
    bekle("dolu proje: kurgu ilk koşuda 1/2 = %50 (UYGULANMAZ sayılmaz)", "%50" in satir(c, "Kurgu"), c)
    bekle("dolu proje: lider ilk koşuda 1/2 geçiş, aşım 1", "%50" in satir(c, "Ekip lideri") and "aşım 1" in satir(c, "Ekip lideri"), c)
    bekle("dolu proje: mağaza bu hafta 30/400 = %7,5, önceki hafta %5 → +2,5 puan", "%7,5" in satir(c, "Mağaza kolu") and "+2,5 puan" in satir(c, "Mağaza kolu"), c)
    bekle("dolu proje: az örnek notu düşülür", "(az örnek)" in satir(c, "Kreatif analisti"), c)
    bekle("dolu proje: 10 / 10 rolün verisi var", "Verisi olan rol: 10 / 10" in c, c)

    # 3 hafta üst üste veri yok → uyarı (iki önceki haftanın kaydı + bu koşu)
    uc = os.path.join(kok, "uc"); os.makedirs(os.path.join(uc, ".ekip"))
    yaz(os.path.join(uc, ".ekip", "karne.jsonl"), json.dumps({"tarih": "2026-03-06", "roller": {}}) + "\n" + json.dumps({"tarih": "2026-03-13", "roller": {}}) + "\n")
    k, c = kos(uc, "--yazma")
    bekle("3 hafta üst üste veri yok → kullanıcıya tek soru uyarısı", "3 HAFTA VERİ YOK" in satir(c, "Fırsat avcısı"), c)
    k, c = kos(bos, "--yazma")
    bekle("aynı hafta ikinci koşu 3 hafta sayılmaz", "3 HAFTA VERİ YOK" not in c, c)
    k, c = kos(os.path.join(kok, "yok"))
    bekle("proje klasörü yok → 2", k == 2, c)

    for ad, ok in SONUC:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    kalan = sum(1 for _, ok in SONUC if not ok)
    print("TOPLAM: %d test, %d kaldı" % (len(SONUC), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
