#!/usr/bin/env python3
"""marj_hesap.py ve ivme_olc.py kirma testleri. Gecici klasorde sahte veri kurar, betikleri cagirir.
Kullanim: python3 kirma_testi.py   -> hepsi gecerse cikis 0, biri bile tutmazsa 1."""
import csv
import os
import re
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
MARJ = os.path.join(BURADA, "marj_hesap.py")
IVME = os.path.join(BURADA, "ivme_olc.py")
FIRSAT = os.path.join(BURADA, "firsat_kontrol.py")
MB = "urun,pazar,para,satis_fiyati,urun_maliyeti,kargo,gumruk_orani_yuzde,tarife_kalemi,araci_sabit,odeme_yuzde,odeme_sabit,iade_orani_yuzde,iade_birim_maliyet,teslim_gun,kaynak_notu\n"
IB = "urun,pazar,olcum,tarih,reklam_sayisi,yorum_sayisi,bsr,trendyol_degerlendirme,tiktok_satilan,yeni_magaza,perakende_satici,akraba_kanit,kaynak_notu\n"
SONUC = []


def kos(betik, args, icerik, klasor, ad="girdi.csv", env=None):
    yol = os.path.join(klasor, ad)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(icerik)
    p = subprocess.run([sys.executable, betik] + [a.replace("{G}", yol) for a in args],
                       capture_output=True, text=True, cwd=klasor,
                       env={**os.environ, "VUE_PROFIL": os.path.join(klasor, "yok-profil.tsv"), **(env or {})})  # hermetik: gerçek profil sızmaz
    return p.returncode, p.stdout + p.stderr


def bekle(ad, kod, cikti, beklenen_kod, icermeli=()):
    tamam = kod == beklenen_kod and all(x in cikti for x in icermeli)
    SONUC.append((ad, tamam, kod, beklenen_kod))
    if not tamam:
        print(f"--- {ad} cikti:\n{cikti}")


def main():
    with tempfile.TemporaryDirectory() as k:
        # 1) Marj: elle hesapla eslesme (ABD). Elle: gumruk 8*0.30=2.40; odeme 39.99*0.029+0.30=1.45971;
        #    iade 0.05*12=0.60; inis 8+4+2.40+1.50+1.45971+0.60=17.95971; kar 39.99-17.95971=22.03; carpan 2.23
        kod, c = kos(MARJ, ["{G}"], MB + "kedi rampasi,US,USD,39.99,8,4,30,1,1.50,2.9,0.30,5,12,6,test\n", k)
        bekle("marj elle-hesap ABD", kod, c, 0, ["inis 17.96", "kar 22.03", "carpan 2.23x", "P5=1", "P6=2"])
        # 2) Marj: AB esik alti 3 EUR/kalem + KDV 19 (elle: gumruk 0+3*2=6; net 34.95/1.19=29.37;
        #    odeme 34.95*0.025+0.25=1.12375; iade 0.10*8=0.80; inis 9+3+6+0+1.12+0.80=19.92; kar 9.45)
        kod, c = kos(MARJ, ["{G}"], MB + "organizer,DE,EUR,34.95,9,3,,2,0,2.5,0.25,10,8,12,test\n", k)
        bekle("marj AB esik-alti kalem ucreti", kod, c, 0, ["gumruk 6.00", "net 29.37", "inis 19.92", "kar 9.45", "P6=1"])
        # 3) Kirma: eksik sutun
        kod, c = kos(MARJ, ["{G}"], "urun,pazar,satis_fiyati\nx,US,10\n", k)
        bekle("marj eksik sutun -> 1", kod, c, 1, ["eksik sutun"])
        # 4) Kirma: sayi yerine metin
        kod, c = kos(MARJ, ["{G}"], MB + "x,US,USD,abc,8,4,30,1,1,2.9,0.3,5,12,6,\n", k)
        bekle("marj metin fiyat -> 1", kod, c, 1, ["sayi degil"])
        # 5) Kirma: ABD'de gumruk orani bos (esik yok)
        kod, c = kos(MARJ, ["{G}"], MB + "x,US,USD,30,8,4,,1,1,2.9,0.3,5,12,6,\n", k)
        bekle("marj ABD tarife bos -> 1", kod, c, 1, ["muafiyet esigi yok"])
        # 6) Kirma: varsayilani olmayan odeme/iade bos
        kod, c = kos(MARJ, ["{G}"], MB + "x,TR,TRY,599,150,40,0,1,0,,,,,3,\n", k)
        bekle("marj odeme/iade bos -> 1", kod, c, 1, ["oranlar dosyasinda da yok"])
        # 7) Kirma: para birimi pazarla uyusmuyor
        kod, c = kos(MARJ, ["{G}"], MB + "x,DE,USD,30,8,4,0,1,0,2,0.3,5,8,6,\n", k)
        bekle("marj para uyusmazligi -> 1", kod, c, 1, ["para USD"])
        # 8) Kirma: AB esik ustu urun, oran yok
        kod, c = kos(MARJ, ["{G}"], MB + "x,FR,EUR,400,160,10,,1,0,2,0.3,5,8,6,\n", k)
        bekle("marj AB esik ustu oran bos -> 1", kod, c, 1, ["gumruk_orani_yuzde zorunlu"])
        # 9) Uyari: dogrulanmamis oran kullanimi raporlanir (TR KDV)
        kod, c = kos(MARJ, ["{G}"], MB + "x,TR,TRY,599,150,40,0,1,0,3,0,8,120,3,\n", k)
        bekle("marj TR dogrulanmamis KDV uyarisi", kod, c, 0, ["UYARI", "TR.kdv_yuzde"])
        # 9b) Profil: TR'de kapıda ödeme %30 x 25 TL = 7,50 TL inişe eklenir; profil yoksa 0; ABD'yi etkilemez; bozuk profil -> 1
        pr = os.path.join(k, "p.tsv")
        satir_tr = MB + "x,TR,TRY,599,150,40,0,1,0,3,0,8,120,3,\n"
        kod0, c0 = kos(MARJ, ["{G}"], satir_tr, k)
        with open(pr, "w", encoding="utf-8") as f:
            f.write("anahtar\tdeger\ttarih\nkapida_odeme_orani_yuzde\t30\t2026-11-25\nkapida_ek_ucret\t25\t2026-11-25\n")
        kod1, c1 = kos(MARJ, ["{G}"], satir_tr, k, env={"VUE_PROFIL": pr})
        i0 = float(re.search(r"inis ([\d.]+)", c0).group(1))
        i1 = float(re.search(r"inis ([\d.]+)", c1).group(1))
        bekle("KIRMA marj TR profil kapida %30x25: inis +7,50 TL", 0 if kod0 == kod1 == 0 and abs((i1 - i0) - 7.5) < 0.011 and "kapida(profil) 7.50" in c1 and "kapida(profil)" not in c0 else 1, f"{i0} {i1}", 0)
        kod2, c2 = kos(MARJ, ["{G}"], MB + "kedi rampasi,US,USD,39.99,8,4,30,1,1.50,2.9,0.30,5,12,6,test\n", k, env={"VUE_PROFIL": pr})
        bekle("marj profil ABD'yi etkilemez", kod2, c2, 0, ["inis 17.96"])
        with open(pr, "w", encoding="utf-8") as f:
            f.write("anahtar\tdeger\ttarih\nkapida_odeme_orani_yuzde\t150\t2026-11-25\n")
        kod3, c3 = kos(MARJ, ["{G}"], satir_tr, k, env={"VUE_PROFIL": pr})
        bekle("KIRMA bozuk profil (kapida %150) -> 1", kod3, c3, 1, ["aralık dışı"])

        # 10) Ivme: sahte uc urun -> uc bant
        veri = IB + (
            "A erken,US,t0,2026-11-01,3,40,9000,,120,1,1,E,q1\n"
            "A erken,US,t7,2026-11-08,7,65,5200,,300,3,1,E,q1\n"
            "B bos,TR,t0,2026-11-01,0,0,,0,,0,0,E,q2\n"
            "B bos,TR,t7,2026-11-08,0,0,,0,,0,0,E,q2\n"
            "C doymus,US,t0,2026-11-01,40,900,150,,5000,4,8,E,q3\n"
            "C doymus,US,t7,2026-11-09,45,1100,140,,6000,5,9,E,q3\n")
        kod, c = kos(IVME, ["bant", "{G}"], veri, k)
        bekle("ivme uc urun uc bant", kod, c, 0,
              ["A erken | US | 7 gun | BANT: ERKEN DALGA", "B bos | TR | 7 gun | BANT: BOS", "C doymus | US | 8 gun | BANT: DOYMUS"])
        # 11) Kirma: t7 var t0 yok
        kod, c = kos(IVME, ["bant", "{G}"], IB + "X,US,t7,2026-11-08,3,,,,,,,E,\n", k)
        bekle("ivme t0 yok -> 1", kod, c, 1, ["t0 yok"])
        # 12) Kirma: 3 gunluk aralik
        kod, c = kos(IVME, ["bant", "{G}"], IB + "X,US,t0,2026-11-01,3,,,,,,,E,\nX,US,t7,2026-11-04,5,,,,,,,E,\n", k)
        bekle("ivme 3 gun -> 1", kod, c, 1, ["3 gun"])
        # 13) Kirma: reklam_sayisi bos + bozuk tarih + metin sayi
        kod, c = kos(IVME, ["bant", "{G}"], IB + "X,US,t0,2026-11-01,,,,,,,,E,\nY,US,t0,01.11.2026,2,,,,,,,E,\nZ,US,t0,2026-11-01,cok,,,,,,,E,\n", k)
        bekle("ivme bos/bozuk alanlar -> 1", kod, c, 1, ["reklam_sayisi zorunlu", "tarih YYYY-AA-GG", "tam sayi degil"])
        # 14) Kirma: eksik sutun
        kod, c = kos(IVME, ["bant", "{G}"], "urun,pazar\nX,US\n", k)
        bekle("ivme eksik sutun -> 1", kod, c, 1, ["eksik sutun"])
        # 15) bekleyen: t0'i 7 gun once olan listelenir, 2 gun once olan listelenmez
        kod, c = kos(IVME, ["bekleyen", "{G}", "--bugun", "2026-11-17"],
                     IB + "Eski,US,t0,2026-11-10,2,,,,,,,E,\nYeni,US,t0,2026-11-15,2,,,,,,,E,\n", k)
        bekle("ivme bekleyen listesi", kod, c, 0, ["OLCUM GUNU: Eski", "TOPLAM: 1"])
        bekle("ivme bekleyen yeni olani listelemez", 0, "" if "OLCUM GUNU: Yeni" in c else "ok", 0, ["ok"])

    # denetim #21: skeptic hükmü `SAT-KOŞULLU: <eksik tek kanıt>`: firsat_kontrol denetle ve excel_hazirla tanır
    with tempfile.TemporaryDirectory() as k2:
        TB = ("| ürün | link | satış | fiyat | dna | a | b | c | d | durum | not |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
              "| X | https://www.aliexpress.com/item/1005001234567890.html | 2300 sold (ürün sayfası) | 12.99 normal | 1111100 | 2 | 2 | 2 | 2 | %s | is/firsat/kanit/01.md |\n")
        # kurucu kararı 2026-11-25: SAT-KOŞULLU ayrı sınıf değil, eski yazım SAT sayılır (eksik kanıt = SAT kartı notu); hata vermez
        for durum, beklenen, parca in (("SAT-KOŞULLU: numune", 0, "0 sorun"), ("SAT-KOŞULLU", 0, "0 sorun"),
                                       ("SAT-KOŞULLU: numune ve alıcı videosu", 0, "0 sorun"), ("SAT", 0, "0 sorun")):
            kod, c = kos(FIRSAT, ["denetle", "{G}"], TB % durum, k2, "adaylar.md")
            bekle("firsat_kontrol denetle durum=%r" % durum, kod, c, beklenen, [parca])
        sys.path.insert(0, BURADA)
        import excel_hazirla as eh
        proje = os.path.join(k2, "proje")
        os.makedirs(os.path.join(proje, "is", "firsat", "kanit"))
        with open(os.path.join(proje, "is", "firsat", "kanit", "01.md"), "w", encoding="utf-8") as f:
            f.write("kanit\n")
        ad_ = os.path.join(k2, "a.md")
        for durum, beklenen, parca in (("SAT-KOŞULLU: numune — is/firsat/kanit/01.md", "SAT", "Kontrol et: numune"),
                                       ("SAT-KOŞULLU — is/firsat/kanit/01.md", "SAT", ""), ("SAT-KOŞULLU: numune", None, ""),
                                       ("İZLE — is/firsat/kanit/01.md", None, "")):
            with open(ad_, "w", encoding="utf-8") as f:
                f.write("| Ürün | Ali link | Ürün satışı | Normal fiyat | Durum | Zaten viral |\n|---|---|---|---|---|---|\n| X | https://www.aliexpress.com/item/1005001234567890.html | 2300 sold | 12.99 USD | %s | yok |\n" % durum)
            out = os.path.join(k2, "u.tsv")
            n = eh.hazirla(ad_, None, proje, out)
            with open(out, encoding="utf-8") as f:
                rows = list(csv.reader(f, delimiter="\t"))
            if beklenen is None:
                bekle("excel_hazirla durum=%r -> kullanıcıya gitmez (kanıtsız/İZLE satır yazılmaz)" % durum, 0 if n == 0 and len(rows) == 1 else 1, str(rows), 0)
            else:
                bekle("excel_hazirla durum=%r -> %s" % (durum, beklenen), 0 if n == 1 and rows[1][8] == beklenen and parca in rows[1][9] else 1,
                      str(rows[1:]), 0)

    # YALNIZ SAT (kurucu kararı 2026-11-25): (a)-(f)
    with tempfile.TemporaryDirectory() as k3:
        proje = os.path.join(k3, "proje")
        firsat = os.path.join(proje, "is", "firsat")
        os.makedirs(os.path.join(firsat, "kanit"))
        for n_ in ("01-iyi.md", "02-vetolu.md"):
            with open(os.path.join(firsat, "kanit", n_), "w", encoding="utf-8") as f:
                f.write("kanit\n")
        BASLIK = "| # | ürün | link | satış | fiyat | dna | a | b | c | d | zaten viral? | veto | marj (kat) | durum |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"

        def satir(no="1", urun="İyi ürün", fiyat="12.99 USD normal", dna="1111100", abcd="2 | 2 | 2 | 2", zaten="doğrulanamadı", veto="yok", marj="2.4",
                  durum="SAT — is/firsat/kanit/01-iyi.md", item="1005001234567890"):
            return "| %s | %s | https://www.aliexpress.com/item/%s.html | 2300 sold (ürün sayfası) | %s | %s | %s | %s | %s | %s | %s |\n" % (
                no, urun, item, fiyat, dna, abcd, zaten, veto, marj, durum)

        def denetle_md(*satirlar, ad="adaylar.md"):
            y = os.path.join(firsat, ad)
            with open(y, "w", encoding="utf-8") as f:
                f.write("# Adaylar\n\n" + BASLIK + "".join(satirlar))
            p = subprocess.run([sys.executable, FIRSAT, "denetle", y], capture_output=True, text=True)
            return p.returncode, p.stdout + p.stderr, y

        def ozet_md(y, *ek):
            p = subprocess.run([sys.executable, FIRSAT, "ozet", y] + list(ek), capture_output=True, text=True)
            return p.returncode, p.stdout + p.stderr

        kod, c, y = denetle_md(satir())
        bekle("(a) tüm ölçütler iyi ama zaten viral=doğrulanamadı -> SAT adayı, denetle 0", kod, c, 0, ["oneri: SAT adayi"])
        bekle("(a) ... ve not düşer: 'zaten viral doğrulanamadı' (eskiden İZLE'ye düşerdi)", 0 if "zaten viral doğrulanamadı" in c else 1, c, 0)
        kod, c = ozet_md(y)
        bekle("(a) özet: SAT satırı listelenir (1 SAT)", kod, c, 0, ["SAT 1/5", "İyi ürün"])
        kod, c, y = denetle_md(satir(marj=""))
        bekle("(b) marj/ROAS hesaplanmamış -> SAT adayı + not (engel değil)", kod, c, 0, ["oneri: SAT adayi", "marj hesaplanmadı"])
        kod, c, y = denetle_md(satir(marj="zarar"))
        bekle("(c) kanıtlı negatif katkı + durum SAT -> HATA (ELE)", kod, c, 1, ["oneri: ELE", "marj: kanıtlı negatif"])
        kod, c, y = denetle_md(satir(marj="0.8", durum="ELE"))
        bekle("(c) çarpan 0,8 + durum ELE -> tutarlı, denetle 0, oneri ELE", kod, c, 0, ["oneri: ELE"])
        kod, c, y = denetle_md(satir(veto="lisans-marka"))
        bekle("(d) veto + durum SAT -> HATA (ELE)", kod, c, 1, ["oneri: ELE", "veto: lisans-marka"])
        kod, c, y = denetle_md(satir(veto="yok"))
        bekle("(d) veto 'yok' -> SAT adayı", kod, c, 0, ["oneri: SAT adayi"])
        kod, c, y = denetle_md(satir(fiyat="Trendyol 399 TL"))
        bekle("(e) Trendyol fiyatı alış/fiyat alanına yazılmış -> denetim HATA", kod, c, 1, ["Trendyol perakende"])
        kod, c, y = denetle_md(satir(), satir(no="2", urun="Vetolu ürün", item="1005001234567891", veto="riskli-kargo", durum="ELE"),
                               satir(no="3", urun="Eski izle ürünü", item="1005001234567892", durum="İZLE — numune bekleniyor"))
        bekle("(f) karışık tablo denetle 0", kod, c, 0)
        kod, c = ozet_md(y, "--hedef", "5")
        bekle("(f) özet: İyi ürün var", kod, c, 0, ["İyi ürün"])
        bekle("(f) özette İZLE/ELE kelimesi ve elenen ürün adı yok",
              0 if not re.search(r"İZLE|IZLE|\bELE\b", c) and "Vetolu" not in c and "Eski izle" not in c else 1, c, 0)
        bekle("(f) hedef 5, 1 SAT -> '1 SAT buldum, sebep:' tek satır", 0 if len(re.findall(r"^1 SAT buldum, sebep: .+$", c, re.M)) == 1 else 1, c, 0)
        bekle("(f) özet <= 10 satır", 0 if len(c.strip().splitlines()) <= 10 else 1, c, 0)
        kod, c = ozet_md(y, "--hedef", "1")
        bekle("(f) hedef 1 ulaşıldı -> 'sebep' satırı yok", 0 if "sebep" not in c else 1, c, 0)
        # Excel hazırlayıcı: Ürünler yalnız SAT
        import excel_hazirla as eh2
        out = os.path.join(k3, "u3.tsv")
        n = eh2.hazirla(y, None, proje, out)
        with open(out, encoding="utf-8") as f:
            rows = list(csv.reader(f, delimiter="\t"))
        bekle("excel_hazirla: kullanıcı sayfasına yalnız SAT (1 satır) + 'Kontrol et' notu", 0 if n == 1 and rows[1][8] == "SAT" and "Kontrol et" in rows[1][9] and "zaten viral" in rows[1][9] else 1, str(rows), 0)
    for ad, tamam, kod, bk in SONUC:
        print(f"{'GECTI' if tamam else 'KALDI'} | {ad} | cikis {kod} (beklenen {bk})")
    kalan = sum(1 for x in SONUC if not x[1])
    print(f"TOPLAM: {len(SONUC)} test, {kalan} kaldi")
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
