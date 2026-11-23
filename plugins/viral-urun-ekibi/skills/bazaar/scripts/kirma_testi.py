#!/usr/bin/env python3
"""bazaar kırma testleri. Kullanım: python3 kirma_testi.py → hepsi geçerse 0, biri tutmazsa 1.

Her kapı önce bozuk girdiyle ≠ 0 görülür, sonra doğru girdiyle 0 (kırılmayan kapı yeşil sayılmaz).
"""
import csv
import os
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
KONTROL = os.path.join(BURADA, "bazaar_kontrol.py")
MARJ = os.path.join(BURADA, "tr_marj.py")
ALANLAR = ("no urun trendyol_link alis_tl yorum puan satici_sayisi satici gorsel_bakildi mekanizma aile viral_db viral_video "
           "meta_reklam onerilen_satis_tl on_karar karar neden okuma_tarihi").split()
MARJ_SUTUN = ("urun,satis_fiyati,alis_fiyati,alis_kdv_dahil,fatura_kurumsal,kdv_yuzde,tedarik_kargo,musteri_kargo,odeme_yuzde,"
              "odeme_sabit,kapida_odeme_orani_yuzde,kapida_ek_ucret,iade_orani_yuzde,iade_birim_maliyet,reklam_payi_yuzde,kaynak_notu").split(",")
sonuc = []


def kos(betik, args, env=None):
    e = dict(os.environ)
    e.update(env or {})
    return subprocess.run([sys.executable, betik] + args, capture_output=True, text=True, env=e)


def bekle(ad, r, beklenen, parca=None):
    ok = r.returncode == beklenen and (parca is None or parca in r.stdout + r.stderr)
    sonuc.append(ok)
    print(("GECTI | " if ok else "KALDI | ") + "%s | cikis %d (beklenen %d)%s" % (
        ad, r.returncode, beklenen, "" if ok else " | " + (r.stdout + r.stderr).strip()[:240]))


def kontrol(ad, ok, ayrinti=""):
    sonuc.append(bool(ok))
    print(("GECTI | " if ok else "KALDI | ") + ad + ("" if ok else " | " + str(ayrinti)))


def aday(**k):
    r = dict.fromkeys(ALANLAR, "")
    r.update(no="1", urun="Test ürünü", trendyol_link="https://www.trendyol.com/x-p-100", alis_tl="200", yorum="500", puan="4,5",
             satici_sayisi="3", meta_reklam="1", onerilen_satis_tl="500", viral_db="yok", okuma_tarihi="2026-11-23")
    r.update(k)
    return r


def adaylar_yaz(yol, satirlar, baslik=ALANLAR):
    with open(yol, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(baslik)
        for s in satirlar:
            w.writerow([s.get(a, "") for a in ALANLAR])


def on_karar(d, **k):
    y = os.path.join(d, "adaylar.tsv")
    adaylar_yaz(y, [aday(**k)])
    r = kos(KONTROL, ["denetle", y])
    with open(y, encoding="utf-8") as f:
        satir = list(csv.reader(f, delimiter="\t"))
    return r, (satir[1][ALANLAR.index("on_karar")] if len(satir) > 1 else None)


def marj_yaz(yol, **k):
    r = dict(urun="Deneme", satis_fiyati="600", alis_fiyati="200", alis_kdv_dahil="E", fatura_kurumsal="E", kdv_yuzde="20",
             tedarik_kargo="10", musteri_kargo="30", odeme_yuzde="3", odeme_sabit="1", kapida_odeme_orani_yuzde="50",
             kapida_ek_ucret="10", iade_orani_yuzde="5", iade_birim_maliyet="100", reklam_payi_yuzde="10", kaynak_notu="test")
    r.update(k)
    with open(yol, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(MARJ_SUTUN)
        w.writerow([r[c] for c in MARJ_SUTUN])


def marj_sonuc(yol):
    r = kos(MARJ, [yol, "--cikti", yol + ".sonuc"])
    d = None
    if os.path.exists(yol + ".sonuc"):
        with open(yol + ".sonuc", encoding="utf-8") as f:
            s = list(csv.reader(f, delimiter="\t"))
        d = dict(zip(s[0], s[1]))
    return r, d


def main():
    with tempfile.TemporaryDirectory(prefix="bazaar_test_") as d:
        # --- tr_marj: önce bozuk girdi (kırmızı), sonra doğru ---
        m = os.path.join(d, "marj.csv")
        marj_yaz(m, odeme_yuzde="")
        bekle("boş oran (tr-oranlari.tsv değeri de boş) -> HATA", kos(MARJ, [m]), 1, "tahmin yapılmaz")
        marj_yaz(m, odeme_yuzde="3")
        r, s = marj_sonuc(m)
        bekle("tam girdi -> hesap tamam", r, 0)
        kontrol("elle hesaplanan katki 264.33, carpan 2.12, basabas ROAS 2.27, net kar 204.33",
                s and s["katki"] == "264.33" and s["carpan"] == "2.12" and s["basabas_roas"] == "2.27" and s["net_kar"] == "204.33", s)
        kontrol("basabas ROAS 2.27 -> karar_marj İZLE (2.01-3.0)", s and s["karar_marj"] == "İZLE", s)
        marj_yaz(m, fatura_kurumsal="H")
        r, s = marj_sonuc(m)
        kontrol("kurumsal fatura yok -> KDV düşülmez (alis_net = alis)", s and s["alis_net"] == "200.00", s)
        marj_yaz(m, alis_fiyati="900")
        r, s = marj_sonuc(m)
        kontrol("katkı <= 0 -> basabas_roas 'zarar', karar ELE", s and s["basabas_roas"] == "zarar" and s["karar_marj"] == "ELE", s)
        marj_yaz(m, reklam_payi_yuzde="")
        r, s = marj_sonuc(m)
        kontrol("reklam payı boş -> net_kar hesaplanmaz", s and s["net_kar"] == "hesaplanmadi", s)
        marj_yaz(m, alis_kdv_dahil="X")
        bekle("alis_kdv_dahil E/H değil -> HATA", kos(MARJ, [m]), 1)

        # --- denetle eşik sınırları ---
        r, k = on_karar(d)
        bekle("kusursuz aday -> denetle 0", r, 0)
        kontrol("kusursuz aday on_karar SAT-ADAYI", k == "SAT-ADAYI", k)
        for yorum, beklenen in (("150", "SAT-ADAYI"), ("149", "İZLE"), ("50", "İZLE"), ("49", "ELE"), ("3000", "SAT-ADAYI"), ("3001", "ELE")):
            r, k = on_karar(d, yorum=yorum)
            kontrol("eşik sınırı: yorum %s -> %s" % (yorum, beklenen), k == beklenen, k)
        for puan, beklenen in (("4,2", "SAT-ADAYI"), ("4,1", "İZLE"), ("3,9", "ELE")):
            r, k = on_karar(d, puan=puan)
            kontrol("eşik sınırı: puan %s -> %s" % (puan, beklenen), k == beklenen, k)
        r, k = on_karar(d, onerilen_satis_tl="390", alis_tl="150")
        kontrol("kat 2.6 ama satış < 399 TL -> İZLE", k == "İZLE", k)
        r, k = on_karar(d, satici_sayisi="")
        kontrol("okunamayan ölçüt (satıcı sayısı boş) -> en fazla İZLE", k == "İZLE", k)
        r, k = on_karar(d, viral_db="ayni-urun-viral")
        kontrol("ayni-urun-viral -> ELE", k == "ELE", k)
        r, k = on_karar(d, viral_db="")
        kontrol("viral_db boş (doğrulanamadı), diğer ölçütler SAT -> SAT-KOSULLU", k == "SAT-KOSULLU", k)
        r, k = on_karar(d, viral_db="", yorum="100")
        kontrol("viral doğrulanamadı + yorum 100 (İZLE) -> İZLE (koşullu değil)", k == "İZLE", k)
        r, k = on_karar(d, viral_db="", puan="3,9")
        kontrol("viral doğrulanamadı + puan 3,9 (ELE) -> ELE", k == "ELE", k)
        r, k = on_karar(d, onerilen_satis_tl="")
        kontrol("marj (kat) hesaplanamadı, diğer ölçütler SAT -> SAT-KOSULLU", k == "SAT-KOSULLU", k)
        r, k = on_karar(d, viral_db="", satici_sayisi="")
        kontrol("viral + satıcı sayısı doğrulanamadı -> İZLE (satıcı koşul olamaz)", k == "İZLE", k)

        # --- şema ve veri hataları ---
        y = os.path.join(d, "bozuk.tsv")
        adaylar_yaz(y, [aday()], baslik=ALANLAR[:-1])
        bekle("bozuk TSV (18 alanlı başlık) -> HATA", kos(KONTROL, ["denetle", y]), 1, "başlık")
        adaylar_yaz(y, [aday(yorum="çok")])
        bekle("sayı olmayan yorum -> HATA", kos(KONTROL, ["denetle", y]), 1, "yorum")
        adaylar_yaz(y, [aday(viral_db="belki")])
        bekle("geçersiz viral_db değeri -> HATA", kos(KONTROL, ["denetle", y]), 1, "viral_db")
        adaylar_yaz(y, [aday(), aday(no="2", urun="İkinci")])
        bekle("tekrar eden link -> DAHA ONCE GORULDU", kos(KONTROL, ["denetle", y]), 1, "DAHA ONCE GORULDU")
        adaylar_yaz(y, [aday()])
        bekle("tek satır -> denetle 0", kos(KONTROL, ["denetle", y]), 0)

        # --- tekrar ---
        kl = os.path.join(d, "kl")
        os.makedirs(kl)
        adaylar_yaz(os.path.join(kl, "adaylar.tsv"), [aday()])
        bekle("tekrar: aynı ürün no'lu link (parametreli) -> DAHA ONCE GORULDU",
              kos(KONTROL, ["--klasor", kl, "tekrar", "https://www.trendyol.com/baska-ad-p-100?boutiqueId=1"]), 1, "DAHA ONCE GORULDU")
        bekle("tekrar: yeni ürün -> YENI", kos(KONTROL, ["--klasor", kl, "tekrar", "https://www.trendyol.com/y-p-999"]), 0, "YENI")

        # --- kota ---
        kt = os.path.join(d, "kota")
        t0 = "2026-11-23T10:00:00"
        bekle("kota: ilk arama kaydı -> 0", kos(KONTROL, ["--klasor", kt, "kota", "kaydet", "arama", "terim1"], {"BAZAAR_SIMDI": t0}), 0)
        bekle("kota: 15 sn dolmadan ikinci istek -> BEKLE (4)",
              kos(KONTROL, ["--klasor", kt, "kota", "kaydet", "arama", "terim2"], {"BAZAAR_SIMDI": "2026-11-23T10:00:05"}), 4, "BEKLE")
        for i in range(2, 16):
            kos(KONTROL, ["--klasor", kt, "kota", "kaydet", "arama", "t%d" % i], {"BAZAAR_SIMDI": "2026-11-23T10:%02d:00" % i})
        bekle("kota: 16. arama -> günlük tavan (4)",
              kos(KONTROL, ["--klasor", kt, "kota", "kaydet", "arama", "fazla"], {"BAZAAR_SIMDI": "2026-11-23T11:00:00"}), 4, "TAVAN")
        bekle("kota durum: tavan dolu -> 4", kos(KONTROL, ["--klasor", kt, "kota", "durum"], {"BAZAAR_SIMDI": "2026-11-23T11:00:00"}), 4)
        bekle("kota: ertesi gün sayaç sıfırlanır -> 0",
              kos(KONTROL, ["--klasor", kt, "kota", "kaydet", "arama", "yeni-gun"], {"BAZAAR_SIMDI": "2026-11-24T10:00:00"}), 0)
        kt2 = os.path.join(d, "kota2")
        kos(KONTROL, ["--klasor", kt2, "kota", "kilit", "CAPTCHA"], {"BAZAAR_SIMDI": t0})
        bekle("kota: kilit yazılınca istek -> 3",
              kos(KONTROL, ["--klasor", kt2, "kota", "kaydet", "urun", "x"], {"BAZAAR_SIMDI": "2026-11-23T12:00:00"}), 3, "KİLİTLİ")
        bekle("kota: kilit ertesi gün kalkar -> 0",
              kos(KONTROL, ["--klasor", kt2, "kota", "kaydet", "urun", "x"], {"BAZAAR_SIMDI": "2026-11-24T12:00:00"}), 0)

        # --- viral (veritabanı yok) ---
        v = os.path.join(d, "v.tsv")
        adaylar_yaz(v, [aday()])
        bekle("viral: veritabanı yok -> hepsi dogrulanamadi, çıkış 0", kos(KONTROL, ["viral", "--db", os.path.join(d, "yok.db"), v]), 0, "dogrulanamadi")
        with open(v, encoding="utf-8") as f:
            satir = list(csv.reader(f, delimiter="\t"))[1]
        kontrol("viral: viral_db sütunu dogrulanamadi yazıldı", satir[ALANLAR.index("viral_db")] == "dogrulanamadi", satir)

        # --- sinama ---
        s1 = os.path.join(d, "s1.tsv")
        s2 = os.path.join(d, "s2.tsv")
        adaylar_yaz(s1, [aday(), aday(no="2", trendyol_link="https://www.trendyol.com/x-p-101", urun="B"),
                         aday(no="3", trendyol_link="https://www.trendyol.com/x-p-102", urun="C")])
        adaylar_yaz(s2, [aday(), aday(no="2", trendyol_link="https://www.trendyol.com/x-p-101", urun="B"),
                         aday(no="3", trendyol_link="https://www.trendyol.com/x-p-102", urun="C")])
        bekle("sinama: okunan değerler aynı -> 3/3 tuttu", kos(KONTROL, ["sinama", s1, "--kontrol", s2]), 0, "3/3")
        adaylar_yaz(s2, [aday(), aday(no="2", trendyol_link="https://www.trendyol.com/x-p-101", urun="B", alis_tl="400"),
                         aday(no="3", trendyol_link="https://www.trendyol.com/x-p-102", urun="C")])
        bekle("sinama: biri tutmadı (alış 200 → 400) -> çıkış 1", kos(KONTROL, ["sinama", s1, "--kontrol", s2]), 1, "TUTMADI")
        bekle("sinama: rastgele satır seçimi çıkış 0", kos(KONTROL, ["sinama", s1, "--tohum", "1"]), 0)

        # --- kullanım ---
        bekle("bilinmeyen alt komut -> kullanım hatası (2)", kos(KONTROL, ["yok"]), 2)

    kalan = sonuc.count(False)
    print("TOPLAM: %d test, %d kaldi" % (len(sonuc), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
