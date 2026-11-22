#!/usr/bin/env python3
"""marj_hesap.py ve ivme_olc.py kirma testleri. Gecici klasorde sahte veri kurar, betikleri cagirir.
Kullanim: python3 kirma_testi.py   -> hepsi gecerse cikis 0, biri bile tutmazsa 1."""
import os
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
MARJ = os.path.join(BURADA, "marj_hesap.py")
IVME = os.path.join(BURADA, "ivme_olc.py")
MB = "urun,pazar,para,satis_fiyati,urun_maliyeti,kargo,gumruk_orani_yuzde,tarife_kalemi,araci_sabit,odeme_yuzde,odeme_sabit,iade_orani_yuzde,iade_birim_maliyet,teslim_gun,kaynak_notu\n"
IB = "urun,pazar,olcum,tarih,reklam_sayisi,yorum_sayisi,bsr,trendyol_degerlendirme,tiktok_satilan,yeni_magaza,perakende_satici,akraba_kanit,kaynak_notu\n"
SONUC = []


def kos(betik, args, icerik, klasor, ad="girdi.csv"):
    yol = os.path.join(klasor, ad)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(icerik)
    p = subprocess.run([sys.executable, betik] + [a.replace("{G}", yol) for a in args],
                       capture_output=True, text=True, cwd=klasor)
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

    for ad, tamam, kod, bk in SONUC:
        print(f"{'GECTI' if tamam else 'KALDI'} | {ad} | cikis {kod} (beklenen {bk})")
    kalan = sum(1 for x in SONUC if not x[1])
    print(f"TOPLAM: {len(SONUC)} test, {kalan} kaldi")
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
