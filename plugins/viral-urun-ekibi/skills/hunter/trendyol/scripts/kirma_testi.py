#!/usr/bin/env python3
"""Trendyol kaynağı kırma testleri. Kullanım: python3 kirma_testi.py → hepsi geçerse 0, biri tutmazsa 1.

Her kapı önce bozuk girdiyle ≠ 0 görülür, sonra doğru girdiyle 0 (kırılmayan kapı yeşil sayılmaz).
"""
import csv
import os
import re
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
KONTROL = os.path.join(BURADA, "trendyol_kontrol.py")
MARJ = os.path.join(BURADA, "tr_marj.py")
ALANLAR = ("no urun trendyol_link alis_tl yorum puan satici_sayisi satici gorsel_bakildi mekanizma aile viral_db viral_video "
           "meta_reklam onerilen_satis_tl on_karar karar neden okuma_tarihi").split()
MARJ_SUTUN = ("urun,satis_fiyati,alis_fiyati,alis_kdv_dahil,fatura_kurumsal,kdv_yuzde,tedarik_kargo,musteri_kargo,odeme_yuzde,"
              "odeme_sabit,kapida_odeme_orani_yuzde,kapida_ek_ucret,iade_orani_yuzde,iade_birim_maliyet,reklam_payi_yuzde,kaynak_notu").split(",")
sonuc = []


def kos(betik, args, env=None):
    e = dict(os.environ)
    e["VUE_PROFIL"] = os.path.join(tempfile.gettempdir(), "trendyol-profil-yok", "isletme-profili.tsv")  # hermetik: gerçek profil sızmaz
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


def on_karar_tam(d, **k):
    """(çıktı, on_karar, neden) — eski 19 alanlı başlıkla."""
    y = os.path.join(d, "adaylar.tsv")
    adaylar_yaz(y, [aday(**k)])
    r = kos(KONTROL, ["denetle", y])
    with open(y, encoding="utf-8") as f:
        satir = list(csv.reader(f, delimiter="\t"))
    return r, satir[1][ALANLAR.index("on_karar")], satir[1][ALANLAR.index("neden")]


EK = ["rakip_tl", "alis_kaynak", "veto"]
GENIS = ALANLAR + EK
MARJ_CIKTI = ("urun net_gelir alis_net odeme iade maliyet katki carpan basabas_roas reklam net_kar marka_roas marka_payi karar_marj "
              "oran_kaynaklari").split()


def genis_yaz(yol, satirlar):
    with open(yol, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(GENIS)
        for s in satirlar:
            w.writerow([s.get(a, "") for a in GENIS])


def genis_aday(**k):
    r = aday()
    r.update(rakip_tl="", alis_kaynak="aliexpress.com/item/1005001", veto="")
    r.update(k)
    return r


def marj_sonuc_yaz(yol, urun="Test ürünü", katki="120.00", basabas="3.50", karar="dogrulanamadi"):
    with open(yol, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(MARJ_CIKTI)
        w.writerow([urun if c == "urun" else katki if c == "katki" else basabas if c == "basabas_roas" else karar if c == "karar_marj" else "" for c in MARJ_CIKTI])


def genis_karar(d, marj=None, **k):
    y = os.path.join(d, "adaylar.tsv")
    genis_yaz(y, [genis_aday(**k)])
    r = kos(KONTROL, ["denetle", y] + (["--marj-sonuc", marj] if marj else []))
    with open(y, encoding="utf-8") as f:
        satir = list(csv.reader(f, delimiter="\t"))
    if len(satir) < 2:
        return r, None, None
    return r, satir[1][GENIS.index("on_karar")], satir[1][GENIS.index("neden")]


def marj_yaz(yol, **k):
    r = dict(urun="Deneme", satis_fiyati="600", alis_fiyati="200", alis_kdv_dahil="E", fatura_kurumsal="E", kdv_yuzde="20",
             tedarik_kargo="10", musteri_kargo="30", odeme_yuzde="3", odeme_sabit="1", kapida_odeme_orani_yuzde="50",
             kapida_ek_ucret="10", iade_orani_yuzde="5", iade_birim_maliyet="100", reklam_payi_yuzde="10", kaynak_notu="test")
    r.update(k)
    with open(yol, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(MARJ_SUTUN)
        w.writerow([r[c] for c in MARJ_SUTUN])


def marj_sonuc(yol, oran=None):
    r = kos(MARJ, [yol, "--cikti", yol + ".sonuc"] + (["--oranlar", oran] if oran else []))
    d = None
    if os.path.exists(yol + ".sonuc"):
        with open(yol + ".sonuc", encoding="utf-8") as f:
            s = list(csv.reader(f, delimiter="\t"))
        d = dict(zip(s[0], s[1]))
    return r, d


def main():
    with tempfile.TemporaryDirectory(prefix="trendyol_test_") as d:
        # --- tr_marj: önce bozuk girdi (kırmızı), sonra doğru ---
        m = os.path.join(d, "marj.csv")
        bos = os.path.join(d, "bos-oran.tsv")
        with open(bos, "w", encoding="utf-8") as f:
            f.write("anahtar\tdeger\tdurum\ttarih\tkaynak\tnot\n")
        marj_yaz(m, odeme_yuzde="")
        r0 = kos(MARJ, [m, "--oranlar", bos])
        bekle("boş oran (oran dosyası da boş) -> yerleşik temkinli varsayılan, 'varsayim' etiketi, hesap durmaz", r0, 0, "varsayim")
        marj_yaz(m, odeme_yuzde="3")
        r, s = marj_sonuc(m, bos)
        bekle("tam girdi -> hesap tamam", r, 0)
        kontrol("elle hesaplanan katki 264.33, carpan 2.12, basabas ROAS 2.27, net kar 204.33",
                s and s["katki"] == "264.33" and s["carpan"] == "2.12" and s["basabas_roas"] == "2.27" and s["net_kar"] == "204.33", s)
        kontrol("marka ROAS yok -> karar_marj dogrulanamadi (sabit eşik yok)", s and s["karar_marj"] == "dogrulanamadi", s)
        for mr, bek in (("3.0", "SAT"), ("2.5", "İZLE"), ("2.27", "İZLE"), ("2.0", "ELE")):
            r2 = kos(MARJ, [m, "--oranlar", bos, "--marka-roas", mr, "--cikti", m + ".mr"])
            with open(m + ".mr", encoding="utf-8") as f:
                rr = list(csv.reader(f, delimiter="\t"))
            d2 = dict(zip(rr[0], rr[1]))
            kontrol("başabaş 2.27, marka ROAS %s -> %s" % (mr, bek), d2.get("karar_marj") == bek, d2)
        bekle("marka ROAS 0 -> HATA", kos(MARJ, [m, "--oranlar", bos, "--marka-roas", "0"]), 1, "pozitif")
        marj_yaz(m, fatura_kurumsal="H")
        r, s = marj_sonuc(m, bos)
        kontrol("kurumsal fatura yok -> KDV düşülmez (alis_net = alis)", s and s["alis_net"] == "200.00", s)
        marj_yaz(m, alis_fiyati="900")
        r, s = marj_sonuc(m, bos)
        kontrol("katkı <= 0 -> basabas_roas 'zarar', karar ELE", s and s["basabas_roas"] == "zarar" and s["karar_marj"] == "ELE", s)
        marj_yaz(m, reklam_payi_yuzde="")
        r, s = marj_sonuc(m, bos)
        kontrol("reklam payı boş -> net_kar hesaplanmaz", s and s["net_kar"] == "hesaplanmadi", s)
        marj_yaz(m, alis_kdv_dahil="X")
        bekle("alis_kdv_dahil E/H değil -> HATA", kos(MARJ, [m, "--oranlar", bos]), 1)

        # --- (i) kaynaklı oranlar (gerçek tr-oranlari.tsv) ---
        satir = os.path.join(d, "iyi.csv")
        marj_yaz(satir, urun="Iyi fixture", satis_fiyati="699", alis_fiyati="250", tedarik_kargo="0", kdv_yuzde="", odeme_yuzde="",
                 odeme_sabit="", musteri_kargo="", kapida_odeme_orani_yuzde="", kapida_ek_ucret="", iade_orani_yuzde="",
                 iade_birim_maliyet="", reklam_payi_yuzde="")
        r, s = marj_sonuc(satir)
        bekle("kaynaklı oranlarla boş hücreli satır -> hesap tamam (artık HATA yok)", r, 0, "kaynakli")
        kontrol("kaynaklı oranlarla net_kar hesaplandı (reklam payı varsayım 25)", s and s["net_kar"] != "hesaplanmadi", s)
        r, k = on_karar(d, yorum="500", puan="4,5", satici_sayisi="3", alis_tl="250", onerilen_satis_tl="699")
        kontrol("(i) iyi fixture (yorum 500, puan 4.5, satıcı 3, alış 250, satış 699) -> SAT-ADAYI", k == "SAT-ADAYI", k)
        # --- (iii) kapıda ödeme 0 -> kapıda ücret eklenmez ---
        marj_yaz(satir, urun="K0", kapida_odeme_orani_yuzde="", kapida_ek_ucret="", odeme_yuzde="3", odeme_sabit="1",
                 kdv_yuzde="20", musteri_kargo="30", iade_orani_yuzde="5", iade_birim_maliyet="100")
        r, s0 = marj_sonuc(satir)
        marj_yaz(satir, urun="K0", kapida_odeme_orani_yuzde="0", kapida_ek_ucret="500", odeme_yuzde="3", odeme_sabit="1",
                 kdv_yuzde="20", musteri_kargo="30", iade_orani_yuzde="5", iade_birim_maliyet="100")
        r, s1 = marj_sonuc(satir)
        kontrol("(iii) kapıda oranı 0 (dosyadan) ve 0 (satırdan, ek ücret 500) -> ödeme = 600*3% + 1 = 19.00, kapıda ücret yok",
                s0 and s1 and s0["odeme"] == "19.00" and s1["odeme"] == "19.00", (s0, s1))

        # --- denetle eşik sınırları ---
        r, k = on_karar(d)
        bekle("kusursuz aday -> denetle 0", r, 0)
        kontrol("kusursuz aday on_karar SAT-ADAYI", k == "SAT-ADAYI", k)
        for yorum, beklenen in (("150", "SAT-ADAYI"), ("149", "ELE"), ("50", "ELE"), ("49", "ELE"), ("3000", "SAT-ADAYI"), ("3001", "ELE")):
            r, k = on_karar(d, yorum=yorum)
            kontrol("eşik sınırı: yorum %s -> %s" % (yorum, beklenen), k == beklenen, k)
        for puan, beklenen in (("4,2", "SAT-ADAYI"), ("4,1", "ELE"), ("3,9", "ELE")):
            r, k = on_karar(d, puan=puan)
            kontrol("eşik sınırı: puan %s -> %s" % (puan, beklenen), k == beklenen, k)
        r, k = on_karar(d, onerilen_satis_tl="390", alis_tl="150")
        kontrol("kat 2.6 ama satış < 399 TL -> ELE (kanıtlı eşik)", k == "ELE", k)
        r, k = on_karar(d, satici_sayisi="")
        kontrol("okunamayan ölçüt (satıcı sayısı boş) -> engel değil, SAT-ADAYI (not düşer)", k == "SAT-ADAYI", k)
        r, k = on_karar(d, viral_db="ayni-urun-viral")
        kontrol("ayni-urun-viral -> ELE", k == "ELE", k)
        r, k = on_karar(d, viral_db="")
        kontrol("viral_db boş (doğrulanamadı), diğer ölçütler SAT -> SAT-ADAYI (eskiden SAT-KOSULLU)", k == "SAT-ADAYI", k)
        r, k = on_karar(d, viral_db="", yorum="100")
        kontrol("viral doğrulanamadı + yorum 100 (kanıtlı düşük talep) -> ELE", k == "ELE", k)
        r, k = on_karar(d, viral_db="", puan="3,9")
        kontrol("viral doğrulanamadı + puan 3,9 (ELE) -> ELE", k == "ELE", k)
        r, k = on_karar(d, onerilen_satis_tl="")
        kontrol("marj (kat) hesaplanamadı, diğer ölçütler SAT -> SAT-ADAYI", k == "SAT-ADAYI", k)
        # denetim #21: skeptic hükmü `SAT-KOŞULLU: <eksik tek kanıt>` tanınır; eksik kanıt yazılmamışsa HATA
        r, k = on_karar(d, karar="SAT-KOŞULLU: numune")
        bekle("karar 'SAT-KOŞULLU: numune' -> denetle 0 (tanınır)", r, 0)
        r, k = on_karar(d, karar="SAT-KOŞULLU")
        bekle("karar 'SAT-KOŞULLU' eksik kanıtsız -> artık HATA değil (SAT kartı notu)", r, 0)
        r, k = on_karar(d, karar="SAT-KOŞULLU", neden="Koşul: marj doğrulanamadı")
        bekle("karar 'SAT-KOŞULLU' + neden'de koşul -> denetle 0", r, 0)
        r, k = on_karar(d, karar="SATIR-KOŞULU")
        bekle("karar uydurma değer -> HATA", r, 1, "izinli")
        r, k = on_karar(d, viral_db="", satici_sayisi="")
        kontrol("viral + satıcı sayısı doğrulanamadı -> SAT-ADAYI (bilinmeyen engel değil)", k == "SAT-ADAYI", k)

        # --- YALNIZ SAT (kurucu kararı 2026-11-25): (a)-(f) ---
        r, k, n = on_karar_tam(d, viral_db="dogrulanamadi")
        kontrol("(a) tüm ölçütler iyi ama viral=dogrulanamadi -> SAT-ADAYI (eskiden İZLE/SAT-KOSULLU)", k == "SAT-ADAYI", k)
        kontrol("(a) viral doğrulanamadı SAT kartına NOT olur", "viral" in n.lower() and "Kontrol et" in n, n)
        mj = os.path.join(d, "m-test.tsv")
        marj_sonuc_yaz(mj, karar="dogrulanamadi")
        r, k, n = genis_karar(d, marj=mj)
        kontrol("(b) marka ROAS yok (karar_marj dogrulanamadi) -> SAT-ADAYI", k == "SAT-ADAYI", (k, r.stdout))
        kontrol("(b) ... ve not düşer: 'marka ROAS'", n is not None and "marka ROAS" in n, n)
        marj_sonuc_yaz(mj, karar="SAT")
        r, k, n = genis_karar(d, marj=mj)
        kontrol("(b) marka ROAS iyi -> SAT-ADAYI, ROAS notu yok", k == "SAT-ADAYI" and "ROAS" not in (n or ""), n)
        marj_sonuc_yaz(mj, katki="-12.50", basabas="zarar", karar="ELE")
        r, k, n = genis_karar(d, marj=mj)
        kontrol("(c) kanıtlı negatif katkı (katkı -12,50) -> ELE", k == "ELE", (k, r.stdout))
        kontrol("(c) ELE sebebi marj", n is not None and "marj" in n.lower(), n)
        r, k, n = genis_karar(d, veto="lisans-marka")
        kontrol("(d) veto (lisans/marka görünümü) -> ELE", k == "ELE", (k, r.stdout))
        r, k, n = genis_karar(d, veto="yok")
        kontrol("(d) veto 'yok' -> SAT-ADAYI", k == "SAT-ADAYI", k)
        r, k, n = genis_karar(d, alis_tl="", alis_kaynak="")
        kontrol("tedarikçi bulunamadı (alis_tl boş) -> SAT-ADAYI + 'tedarikçi' notu", k == "SAT-ADAYI" and "tedarikçi" in (n or ""), (k, n))
        # canlı rol sınavı 2026-11-25: arama sayfası/benzer ürün fiyatı alış sayılmaz (kat ELE'si kanıtsız olur)
        r, k, n = genis_karar(d, alis_tl="148", onerilen_satis_tl="450",
                              alis_kaynak="https://www.aliexpress.com/w/wholesale-turbo-julienne-peeler.html")
        kontrol("alis_kaynak arama sayfası (aynı ürün değil) + düşük kat -> SAT-ADAYI + 'arama/benzer' notu (ELE değil)",
                k == "SAT-ADAYI" and "benzer" in (n or ""), (k, n))
        r, k, n = genis_karar(d, alis_tl="300", onerilen_satis_tl="450", alis_kaynak="https://www.aliexpress.com/item/1005006.html")
        kontrol("alis_kaynak ürün sayfası + düşük kat (1,5) -> ELE (kapı hâlâ çalışır)", k == "ELE", (k, n))
        r, k, n = genis_karar(d, alis_tl="", alis_kaynak="", rakip_tl="324", onerilen_satis_tl="")
        kontrol("hedef satış boş + Trendyol 324 TL (< 399) -> SAT-ADAYI + 'set/paket' notu", k == "SAT-ADAYI" and "set/paket" in (n or ""), (k, n))
        r, k, n = genis_karar(d, alis_tl="", alis_kaynak="", rakip_tl="324", onerilen_satis_tl="324")
        kontrol("alış yok + hedef satış 324 TL (< 399) -> SAT-ADAYI + 'set/paket' notu", k == "SAT-ADAYI" and "set/paket" in (n or ""), (k, n))
        r, k, n = genis_karar(d, rakip_tl="400", onerilen_satis_tl="500")
        kontrol("Trendyol'da aynı ürün hedefin altında -> SAT-ADAYI + fiyat notu (ELE değil)", k == "SAT-ADAYI" and "Trendyol" in (n or ""), (k, n))
        for ad, ek in (("alis_tl == rakip_tl (Trendyol fiyatı alış alanına yazılmış)", dict(alis_tl="250", rakip_tl="250")),
                       ("alis_kaynak Trendyol", dict(alis_kaynak="https://www.trendyol.com/x-p-100")),
                       ("alis_tl dolu ama alis_kaynak boş (genişletilmiş başlık)", dict(alis_kaynak=""))):
            yy = os.path.join(d, "e.tsv")
            genis_yaz(yy, [genis_aday(**ek)])
            bekle("(e) %s -> denetim HATA" % ad, kos(KONTROL, ["denetle", yy]), 1, "Trendyol perakende")
        yy = os.path.join(d, "e.tsv")
        genis_yaz(yy, [genis_aday(alis_tl="200", rakip_tl="250")])
        bekle("(e) tedarikçi alışı + ayrı Trendyol fiyatı -> denetle 0", kos(KONTROL, ["denetle", yy]), 0)
        # (f) kullanıcı özeti yalnız SAT
        kok = os.path.join(d, "ozet")
        os.makedirs(os.path.join(kok, "trendyol"))
        os.makedirs(os.path.join(kok, "kanit"))
        open(os.path.join(kok, "kanit", "01-iyi-urun.md"), "w", encoding="utf-8").write("kanit\n")
        ay = os.path.join(kok, "trendyol", "adaylar.tsv")
        genis_yaz(ay, [genis_aday(no="1", urun="İyi ürün", trendyol_link="https://www.trendyol.com/a-p-1", viral_db=""),
                       genis_aday(no="2", urun="Zayıf talep ürünü", trendyol_link="https://www.trendyol.com/b-p-2", yorum="20"),
                       genis_aday(no="3", urun="Vetolu ürün", trendyol_link="https://www.trendyol.com/c-p-3", veto="riskli-kargo"),
                       genis_aday(no="4", urun="Eski izle ürünü", trendyol_link="https://www.trendyol.com/d-p-4", karar="İZLE")])
        bekle("(f) ozet öncesi denetle 0", kos(KONTROL, ["denetle", ay]), 0)
        r = kos(KONTROL, ["ozet", ay, "--hedef", "5"])
        c = r.stdout
        kontrol("(f) özet çıkış 0", r.returncode == 0, r.stdout + r.stderr)
        kontrol("(f) özette SAT ürünü var", "İyi ürün" in c, c)
        kontrol("(f) özette İZLE/ELE kelimesi ve elenen ürün adı yok",
                not re.search(r"İZLE|IZLE|\bELE\b", c) and "Zayıf talep" not in c and "Vetolu" not in c and "Eski izle" not in c, c)
        kontrol("(f) hedef 5, 1 SAT -> 'k SAT buldum, sebep:' tek satır", len(re.findall(r"^1 SAT buldum, sebep: .+$", c, re.M)) == 1, c)
        kontrol("(f) özet <= 10 satır", len(c.strip().splitlines()) <= 10, c)
        kontrol("(f) özette 3 satırlık etiket sözlüğü (SAT = kanıt var, garanti değil)", "Etiket sözlüğü: SAT" in c and "garantisi DEĞİL" in c, c)
        r = kos(KONTROL, ["ozet", ay, "--hedef", "1"])
        kontrol("(f) hedef 1 ulaşıldı -> 'SAT buldum, sebep' satırı yok", "sebep" not in r.stdout and "İyi ürün" in r.stdout, r.stdout)
        # excel hazırlayıcı: Ürünler yalnız SAT
        sys.path.insert(0, BURADA)
        import excel_hazirla as eh
        uy = os.path.join(d, "u.tsv")
        n_ = eh.hazirla(os.path.join(kok, "trendyol"), None, uy)
        with open(uy, encoding="utf-8") as f:
            ur = list(csv.reader(f, delimiter="\t"))
        kontrol("excel_hazirla: kullanıcı sayfasına yalnız SAT satırı (1 satır, karar SAT)", n_ == 1 and len(ur) == 2 and ur[1][8] == "SAT" and ur[1][0] == "İyi ürün", ur)
        kontrol("excel_hazirla: SAT kartında 'Kontrol et' notu (viral)", "Kontrol et" in ur[1][9] and "viral" in ur[1][9], ur[1][9])
        os.remove(os.path.join(kok, "kanit", "01-iyi-urun.md"))
        kontrol("(f) KIRMA SAT yoksa (kanıt dosyası silindi) sözlük basılmaz", "Etiket sözlüğü" not in kos(KONTROL, ["ozet", ay, "--hedef", "1"]).stdout)
        n_ = eh.hazirla(os.path.join(kok, "trendyol"), None, uy)
        kontrol("kanıt dosyası yoksa SAT kullanıcıya gitmez (0 satır)", n_ == 0, n_)

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
        bekle("kota: ilk arama kaydı -> 0", kos(KONTROL, ["--klasor", kt, "kota", "kaydet", "arama", "terim1"], {"TRENDYOL_SIMDI": t0}), 0)
        bekle("kota: 15 sn dolmadan ikinci istek -> BEKLE (4)",
              kos(KONTROL, ["--klasor", kt, "kota", "kaydet", "arama", "terim2"], {"TRENDYOL_SIMDI": "2026-11-23T10:00:05"}), 4, "BEKLE")
        # üst güvenlik sınırı 100 arama/gün (varsayım): kota.tsv'yi doğrudan doldur
        with open(os.path.join(kt, "kota.tsv"), "w", encoding="utf-8", newline="") as f:
            f.write("tarih\tsaat\ttur\thedef\tkilit\tsonuc\n")
            for i in range(100):
                f.write("2026-11-23\t09:%02d:%02d\tarama\tt%d\t\t\n" % (i // 60, i % 60, i))
        bekle("kota: 101. arama -> üst sınır (4)",
              kos(KONTROL, ["--klasor", kt, "kota", "kaydet", "arama", "fazla"], {"TRENDYOL_SIMDI": "2026-11-23T11:00:00"}), 4, "ÜST SINIR")
        bekle("kota durum: üst sınır dolu -> 4", kos(KONTROL, ["--klasor", kt, "kota", "durum"], {"TRENDYOL_SIMDI": "2026-11-23T11:00:00"}), 4)
        bekle("kota: ertesi gün sayaç sıfırlanır -> 0",
              kos(KONTROL, ["--klasor", kt, "kota", "kaydet", "arama", "yeni-gun"], {"TRENDYOL_SIMDI": "2026-11-24T10:00:00"}), 0)
        kt2 = os.path.join(d, "kota2")
        kos(KONTROL, ["--klasor", kt2, "kota", "kilit", "CAPTCHA"], {"TRENDYOL_SIMDI": t0})
        bekle("kota: kilit yazılınca istek -> 3",
              kos(KONTROL, ["--klasor", kt2, "kota", "kaydet", "urun", "x"], {"TRENDYOL_SIMDI": "2026-11-23T12:00:00"}), 3, "KİLİTLİ")
        bekle("kota: kilit ertesi gün kalkar -> 0",
              kos(KONTROL, ["--klasor", kt2, "kota", "kaydet", "urun", "x"], {"TRENDYOL_SIMDI": "2026-11-24T12:00:00"}), 0)

        # --- (iv) kota: tekrar, iade, engel sinyali ---
        kt3 = os.path.join(d, "kota3")
        e = lambda sn: {"TRENDYOL_SIMDI": "2026-11-23T10:00:%02d" % sn if sn < 60 else "2026-11-23T10:%02d:00" % (sn // 60)}
        kos(KONTROL, ["--klasor", kt3, "kota", "kaydet", "arama", "telefon kılıfı"], e(0))
        bekle("(iv) aynı terim tekrar -> TEKRAR, sayılmaz, bekleme de yok",
              kos(KONTROL, ["--klasor", kt3, "kota", "kaydet", "arama", "Telefon Kılıfı"], e(1)), 0, "TEKRAR")
        r = kos(KONTROL, ["--klasor", kt3, "kota", "durum"], e(2))
        kontrol("(iv) tekrar sonrası sayaç 1", "arama 1 " in r.stdout, r.stdout)
        bekle("kota iade: kayıtlı arama iade edilir", kos(KONTROL, ["--klasor", kt3, "kota", "iade", "arama", "telefon kılıfı"], e(3)), 0, "İADE EDİLDİ")
        r = kos(KONTROL, ["--klasor", kt3, "kota", "durum"], e(4))
        kontrol("(iv) iade sonrası sayaç 0 (yanlış satır hak yakmaz)", "arama 0 " in r.stdout, r.stdout)
        bekle("kota iade: sayılmamış kayıt iadesi -> 1", kos(KONTROL, ["--klasor", kt3, "kota", "iade", "arama", "yok"], e(5)), 1, "İADE YOK")
        bekle("iadeden sonra aynı terim yeniden kaydedilebilir", kos(KONTROL, ["--klasor", kt3, "kota", "kaydet", "arama", "telefon kılıfı"], e(30)), 0, "KAYDEDİLDİ")
        kt4 = os.path.join(d, "kota4")
        bekle("sonuc: boş sayfa 1/3 -> 0", kos(KONTROL, ["--klasor", kt4, "kota", "sonuc", "bos", "a"], e(0)), 0)
        bekle("sonuc: boş sayfa 2/3 -> 0", kos(KONTROL, ["--klasor", kt4, "kota", "sonuc", "bos", "b"], e(1)), 0)
        bekle("sonuc: art arda 3 boş sayfa -> kilit (3)", kos(KONTROL, ["--klasor", kt4, "kota", "sonuc", "bos", "c"], e(2)), 3, "kilit")
        kt5 = os.path.join(d, "kota5")
        kos(KONTROL, ["--klasor", kt5, "kota", "sonuc", "bos"], e(0))
        kos(KONTROL, ["--klasor", kt5, "kota", "sonuc", "ok"], e(1))
        kos(KONTROL, ["--klasor", kt5, "kota", "sonuc", "bos"], e(2))
        bekle("sonuc: araya ok girince boş sayacı sıfırlanır -> 0", kos(KONTROL, ["--klasor", kt5, "kota", "sonuc", "bos"], e(3)), 0)
        kt6 = os.path.join(d, "kota6")
        bekle("sonuc: HTTP 429 -> kilit (3)", kos(KONTROL, ["--klasor", kt6, "kota", "sonuc", "429"], e(0)), 3)
        bekle("429 sonrası istek -> KİLİTLİ (3)", kos(KONTROL, ["--klasor", kt6, "kota", "kaydet", "arama", "x"], e(40)), 3, "KİLİTLİ")

        # --- (ii) ig_tt dogrulanamadi-giris tek başına SAT'ı düşürmez ---
        r, k = on_karar(d, viral_video="dogrulanamadi-giris")
        kontrol("(ii) ig_tt dogrulanamadi-giris + diğer ölçütler SAT -> SAT-ADAYI (engel değil)", k == "SAT-ADAYI", k)
        kontrol("(ii) risk notu yazıldı", "ig_tt=dogrulanamadi-giris" in r.stdout, r.stdout)
        r, k = on_karar(d, viral_video="dogrulanamadi-giris", meta_reklam="")
        kontrol("(ii) (c) Meta de yapılamadı -> engel değil, SAT-ADAYI", k == "SAT-ADAYI", k)

        # --- viral: analiz.db yok -> eklenti tablosu (ortak/bilgi/viral-urunler.tsv) ---
        v = os.path.join(d, "v.tsv")
        adaylar_yaz(v, [aday(viral_db="")])
        bekle("viral: analiz.db yok -> eklenti tablosu kullanılır, çıkış 0", kos(KONTROL, ["viral", v]), 0, "eklenti tablosu")
        with open(v, encoding="utf-8") as f:
            satir = list(csv.reader(f, delimiter="\t"))[1]
        kontrol("viral: ilgisiz ürün -> yok (dogrulanamadi değil)", satir[ALANLAR.index("viral_db")] == "yok", satir)
        adaylar_yaz(v, [aday(urun="Kabartma maskeli deri cüzdan erkek")])
        kos(KONTROL, ["viral", v])
        with open(v, encoding="utf-8") as f:
            satir = list(csv.reader(f, delimiter="\t"))[1]
        kontrol("viral: tablodaki viral ürün -> ayni-urun-viral", satir[ALANLAR.index("viral_db")] == "ayni-urun-viral", satir)
        # canlı rol sınavı 2026-11-25: tek ortak kelime aile sayılmaz; aile adının bütün kelimeleri gerekir
        vt = os.path.join(d, "vt.tsv")
        with open(vt, "w", encoding="utf-8") as f:
            f.write("urun_id\tad_jenerik\taile\tnis\tpazarlar\tvideo_sayisi\thesap_sayisi\tviral_hesap_sayisi\ten_yuksek_izlenme\t"
                    "toplam_izlenme\tmedyan_izlenme_takipci\tilk_gorulme\tson_gorulme\thukum\tguncelleme\n"
                    "v1\tPeluş köpek yatağı\tpet-yatak\tpet\tTR\t1\t1\t1\t\t\t\t\t\tVIRAL-URUN\t\n"
                    "v2\tBasketbolcu köpek kostümü\tevcil-kostum\tpet\tTR\t1\t1\t1\t\t\t\t\t\tVIRAL-URUN\t\n")
        for urun_, aile_, bek in (("Leopar cepli köpek hoodie", "kopek-hoodie", "yok"),
                                  ("Koala peluş köpek tulumu", "kopek-kostumu", "aile-var"),
                                  ("Kapüşonlu köpek sweati", "pet-yatak", "aile-var")):
            adaylar_yaz(v, [aday(urun=urun_, aile=aile_, viral_db="")])
            kos(KONTROL, ["viral", v], {"VIRAL_DB_TSV": vt})
            with open(v, encoding="utf-8") as f:
                satir = list(csv.reader(f, delimiter="\t"))[1]
            kontrol("viral aile: %s (aile %s) -> %s" % (urun_, aile_, bek), satir[ALANLAR.index("viral_db")] == bek, satir[ALANLAR.index("viral_db")])
        adaylar_yaz(v, [aday()])
        bekle("viral: tablo da yok -> hepsi dogrulanamadi", kos(KONTROL, ["viral", "--db", os.path.join(d, "yok.db"), v],
              {"VIRAL_DB_TSV": os.path.join(d, "yok.tsv")}), 0, "dogrulanamadi")
        with open(v, encoding="utf-8") as f:
            satir = list(csv.reader(f, delimiter="\t"))[1]
        kontrol("viral: tablo yokken viral_db sütunu dogrulanamadi", satir[ALANLAR.index("viral_db")] == "dogrulanamadi", satir)

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

        # --- işletme profili (danışanın kendi kararı eklenti varsayılanının üstüne yazar) ---
        pr = os.path.join(d, "isletme-profili.tsv")
        pf = ["--profil", pr]
        y = os.path.join(d, "adaylar.tsv")
        adaylar_yaz(y, [aday(alis_tl="200", onerilen_satis_tl="500")])  # kat 2,5; satış 500
        r0 = kos(KONTROL, ["denetle", y])
        bekle("profil yok: eklenti varsayılanı (kat 2,5 >= 2,2) çıkış 0 + 'PROFIL: yok'", r0, 0, "PROFIL: yok")
        with open(y, encoding="utf-8") as f:
            kontrol("profil yok: kat 2,5 -> SAT-ADAYI", list(csv.reader(f, delimiter="\t"))[1][ALANLAR.index("on_karar")] == "SAT-ADAYI")
        with open(pr, "w", encoding="utf-8") as f:
            f.write("anahtar\tdeger\ttarih\nkat_min\t3\t2026-11-25\n")
        adaylar_yaz(y, [aday(alis_tl="200", onerilen_satis_tl="500")])
        bekle("profil kat_min=3: çıkış 0 + 'profili kullanıldı'", kos(KONTROL, ["denetle", y] + pf), 0, "profili kullanıldı")
        with open(y, encoding="utf-8") as f:
            satir = list(csv.reader(f, delimiter="\t"))[1]
        kontrol("KIRMA profil kat_min=3: aynı aday (kat 2,5) ELE olur", satir[ALANLAR.index("on_karar")] == "ELE", satir)
        with open(pr, "w", encoding="utf-8") as f:
            f.write("anahtar\tdeger\ttarih\nsatis_tl_min\t600\t2026-11-25\n")
        adaylar_yaz(y, [aday(alis_tl="200", onerilen_satis_tl="500")])
        kos(KONTROL, ["denetle", y] + pf)
        with open(y, encoding="utf-8") as f:
            satir = list(csv.reader(f, delimiter="\t"))[1]
        kontrol("KIRMA profil satis_tl_min=600: satış 500 ELE olur", satir[ALANLAR.index("on_karar")] == "ELE", satir)
        with open(pr, "w", encoding="utf-8") as f:
            f.write("anahtar\tdeger\ttarih\nkat_min\tabc\t2026-11-25\n")
        bekle("KIRMA bozuk profil (kat_min=abc) -> çıkış 1, sessiz geçilmez", kos(KONTROL, ["denetle", y] + pf), 1, "kat_min")
        os.remove(pr)
        # tr_marj: kapıda ödeme %30 + ek ücret profilden gelir -> katkı düşer; profil yoksa varsayılan (0)
        mj = os.path.join(d, "marj-profil.csv")
        marj_yaz(mj, kapida_odeme_orani_yuzde="", kapida_ek_ucret="")
        r_var = kos(MARJ, [mj], {"VUE_PROFIL": pr})
        bekle("tr_marj profil yok: eklenti varsayılanı + 'PROFIL: yok'", r_var, 0, "PROFIL: yok")
        with open(pr, "w", encoding="utf-8") as f:
            f.write("anahtar\tdeger\ttarih\nkapida_odeme_orani_yuzde\t30\t2026-11-25\nkapida_ek_ucret\t25\t2026-11-25\n")
        r_pro = kos(MARJ, [mj], {"VUE_PROFIL": pr})
        bekle("tr_marj profil kapıda %30 + 25 TL: çıkış 0 + 'PROFIL:' kullanıldı", r_pro, 0, "kapida_odeme_orani_yuzde")
        km = lambda r: float(re.search(r"katki ([-\d.]+)", r.stdout).group(1))
        kontrol("KIRMA tr_marj: profildeki kapıda ödeme katkıyı 7,50 TL düşürür (0,30 x 25)", abs((km(r_var) - km(r_pro)) - 7.5) < 0.01,
                (km(r_var), km(r_pro)))
        kontrol("tr_marj: oran_kaynaklari profil etiketini taşır", "profil" in r_pro.stdout, r_pro.stdout[-200:])

        # --- kullanım ---
        bekle("bilinmeyen alt komut -> kullanım hatası (2)", kos(KONTROL, ["yok"]), 2)

    kalan = sonuc.count(False)
    print("TOPLAM: %d test, %d kaldi" % (len(sonuc), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
