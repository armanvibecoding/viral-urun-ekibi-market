#!/usr/bin/env python3
"""teklif_kontrol.py kirma testleri. Kullanim: python3 kirma_testi.py -> hepsi gecerse 0, biri tutmazsa 1."""
import os
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
BETIK = os.path.join(BURADA, "teklif_kontrol.py")
SABLON = os.path.join(BURADA, "..", "sablon")
BASLIK = open(os.path.join(SABLON, "teklif.tsv"), encoding="utf-8").read()
SONUC = []


def satir(**k):
    v = {"tur": "bizim", "tarih": "2026-11-17", "pazar": "US", "urun": "kedi rampasi", "kaynak_url": "-", "para": "USD",
         "fiyat": "39.99", "karsilastirma_fiyati": "yok", "karsilastirma_kaniti": "yok", "paket": "1x;2x:-15%",
         "garanti": "30 gun para iadesi", "kargo_vaadi": "ucretsiz, 5-8 is gunu", "odeme_yontemleri": "kart;shop_pay",
         "sosyal_kanit_turu": "alici_foto", "aciliyet": "yok", "itiraz_yanitlari": "kargo suresi?; iade?",
         "upsell": "2x paket", "ilk_ekran": "mekanizma videosu", "not": "-"}
    v.update(k)
    return "\t".join(v[c] for c in BASLIK.strip().split("\t")) + "\n"


RAKIP = satir(tur="rakip", kaynak_url="https://ornek-magaza.example/products/rampa", fiyat="44.95",
              karsilastirma_fiyati="89.90", karsilastirma_kaniti="gorulmedi", aciliyet="geri sayim 10 dk; only 3 left",
              sosyal_kanit_turu="gercek_yorum_uygulamasi;uydurma_supheli")


def kos(args, icerik=None, ad="teklif.tsv"):
    with tempfile.TemporaryDirectory() as k:
        yol = os.path.join(k, ad)
        if icerik is not None:
            with open(yol, "w", encoding="utf-8") as f:
                f.write(icerik)
        p = subprocess.run([sys.executable, BETIK] + [a.replace("{G}", yol) for a in args], capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr


def bekle(ad, sonuc, beklenen_kod, icermeli=()):
    kod, c = sonuc
    tamam = kod == beklenen_kod and all(x in c for x in icermeli)
    SONUC.append((ad, tamam, kod, beklenen_kod))
    if not tamam:
        print(f"--- {ad}:\n{c}")


def main():
    bekle("gecerli tablo (rakip sahte aciliyeti gozlem) -> 0", kos(["sema", "{G}"], BASLIK + RAKIP + satir()), 0, ["TOPLAM: 1 rakip, 1 bizim, 0 hata"])
    bekle("eksik sutun -> 1", kos(["sema", "{G}"], "tur\tfiyat\nbizim\t10\n"), 1, ["eksik sutun"])
    bekle("bizim 'son 3 urun' -> 1", kos(["sema", "{G}"], BASLIK + satir(pazar="DE", para="EUR", upsell="Son 3 ürün kaldı!")), 1, ["sahte kıtlık"])
    bekle("bizim 'Only 2 left' -> 1", kos(["sema", "{G}"], BASLIK + satir(ilk_ekran="Only 2 left in stock")), 1, ["yasak ifade"])
    bekle("bizim cizili fiyat kanitsiz -> 1", kos(["sema", "{G}"], BASLIK + satir(karsilastirma_fiyati="79.99")), 1, ["karsilastirma_kaniti yok"])
    bekle("cizili fiyat <= fiyat -> 1", kos(["sema", "{G}"], BASLIK + satir(karsilastirma_fiyati="30", karsilastirma_kaniti="x")), 1, ["buyuk degil"])
    bekle("TR bizim kampanya aciliyeti -> 1", kos(["sema", "{G}"], BASLIK + satir(pazar="TR", para="TRY", fiyat="599", aciliyet="kampanya_bitis:2026-12-01")), 1, ["TR teklifinde"])
    bekle("US bizim gercek kampanya tarihi -> 0", kos(["sema", "{G}"], BASLIK + satir(aciliyet="kampanya_bitis:2026-11-30")), 0)
    bekle("bizim uydurma_supheli -> 1", kos(["sema", "{G}"], BASLIK + satir(sosyal_kanit_turu="uydurma_supheli")), 1, ["uydurma_supheli"])
    bekle("para/pazar uyusmazligi -> 1", kos(["sema", "{G}"], BASLIK + satir(pazar="UK")), 1, ["GBP"])
    bekle("bilinmeyen odeme + bozuk tarih + metin fiyat -> 1",
          kos(["sema", "{G}"], BASLIK + satir(odeme_yontemleri="kart;kripto", tarih="17.11.2026", fiyat="ucuz")), 1,
          ["kripto", "tarih YYYY-AA-GG", "fiyat sayi"])
    bekle("rakip url yok -> 1", kos(["sema", "{G}"], BASLIK + satir(tur="rakip", kaynak_url="-")), 1, ["kaynak_url"])
    bekle("bos zorunlu alan -> 1", kos(["sema", "{G}"], BASLIK + satir(garanti="")), 1, ["garanti bos"])
    # tara
    bekle("tara: TR baski + uydurma sayi -> 1",
          kos(["tara", "--pazar", "TR", "{G}"], "# Sayfa\nKAÇIRMA! 1.250 mutlu müşteri\nStokta sadece 4 adet\n", "sayfa.md"), 1,
          ["TR baskı", "uydurma müşteri", "sahte kıtlık"])
    bekle("tara: DE/FR/ES kaliplari -> 1",
          kos(["tara", "{G}"], "Nur noch 3 verfügbar\nPlus que 2 en stock\nSolo quedan 5\n-80% de descuento\n", "x.md"), 1,
          ["(DE)", "(FR)", "(ES)", "sahte indirim"])
    bekle("tara: yer tutucu ve temiz metin -> 0",
          kos(["tara", "--pazar", "TR", "{G}"], "{GERCEK_YORUM_SAYISI} yorum · kargo dahil 599 TL · 14 gün koşulsuz iade\n", "t.md"), 0)
    bekle("tara: dosya yok -> 1", kos(["tara", "{G}"], None, "yok.md"), 1, ["dosya yok"])
    # magaza site metni kelimeleri (magaza kolunun kurali tek listede) + ISO pazar kodu
    bekle("tara: magaza site kelimeleri (dogal / cok satan / N bin musteri) -> 1",
          kos(["tara", "--pazar", "TR", "{G}"], "%100 Doğal içerik\nEn çok satan model\n12 bin müşteri\n", "site.md"), 1,
          ["kanıtsız nitelik", "kanıtsız satış üstünlüğü", "uydurma müşteri"])
    bekle("tara: 'dogalgaz' gibi kelime ici eslesme sayilmaz -> 0",
          kos(["tara", "--pazar", "TR", "{G}"], "Doğalgaz sobasının yanına konmaz. Ekonomik paket.\n", "site2.md"), 0)
    bekle("tara: --pazar GB = UK (kopru dosyalari ISO yazar) -> 0", kos(["tara", "--pazar", "GB"] + [os.path.join(SABLON, "sayfa-iskeleti.md")]), 0)
    # kendi sablonlarimiz temiz olmali (her pazar)
    sablonlar = [os.path.join(SABLON, d) for d in ("sayfa-iskeleti.md", "eposta-upsell.md")]
    for p in ("TR", "US", "UK", "DE", "FR", "ES"):
        bekle(f"sablonlar temiz ({p}) -> 0", kos(["tara", "--pazar", p] + sablonlar), 0)
    bekle("kullanim hatasi -> 2", kos(["tara", "--pazar", "XX", "a.md"]), 2)

    for ad, tamam, kod, bk in SONUC:
        print(f"{'GECTI' if tamam else 'KALDI'} | {ad} | cikis {kod} (beklenen {bk})")
    kalan = sum(1 for x in SONUC if not x[1])
    print(f"TOPLAM: {len(SONUC)} test, {kalan} kaldi")
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
