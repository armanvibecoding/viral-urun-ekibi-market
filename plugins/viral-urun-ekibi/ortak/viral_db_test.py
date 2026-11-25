#!/usr/bin/env python3
"""viral_db.py testi: bilinen viral ürün -> ayni-urun-viral, ilgisiz -> yok, tablo yoksa dogrulanamadi. Çıkış 0 geçti, 1 kaldı."""
import os
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURADA)
import viral_db  # noqa: E402

hata = []
satirlar = viral_db.oku() or []
if len(satirlar) < 100:
    hata.append("viral-urunler.tsv yok ya da çok küçük (%d satır)" % len(satirlar))
virallar = [r for r in satirlar if r["hukum"] == "VIRAL-URUN" and len(viral_db.jeton(r["ad_jenerik"])) >= 4]
if not virallar:
    hata.append("test için VIRAL-URUN satırı yok")
else:
    r = virallar[0]
    s = viral_db.ara(r["ad_jenerik"])
    if s["durum"] != "ayni-urun-viral":
        hata.append("bilinen viral ürün %r -> %s (beklenen ayni-urun-viral)" % (r["ad_jenerik"], s["durum"]))
s = viral_db.ara("kuantum uzay gemisi muz soyucu kazan")
if s["durum"] != "yok":
    hata.append("ilgisiz ürün -> %s (beklenen yok)" % s["durum"])
# aile: ürün adı eşleşmez ama aile bilinen bir viral ürünle kesişir
vr = [r for r in satirlar if r["hukum"] in viral_db.VIRAL_HUKUMLER and r["aile"]]
if vr:
    s = viral_db.ara("tamamen ilgisiz sözcükler burada", aile=vr[0]["aile"])
    if s["durum"] != "aile-var":
        hata.append("aile=%s -> %s (beklenen aile-var)" % (vr[0]["aile"], s["durum"]))
# kırma: tablo yoksa yeşil olmamalı
if viral_db.ara("herhangi", tsv=os.path.join(tempfile.gettempdir(), "yok-boyle-bir-tsv.tsv"))["durum"] != "dogrulanamadi":
    hata.append("tablo yokken dogrulanamadi dönmedi")
# kırma: ürün sözcükleri bozulursa ayni-urun düşmeli
if virallar:
    bozuk = " ".join(w[::-1] for w in virallar[0]["ad_jenerik"].split())
    if viral_db.ara(bozuk)["durum"] == "ayni-urun-viral":
        hata.append("kırma tutmadı: bozuk metin ayni-urun-viral verdi")
for h in hata:
    print("KALDI: " + h)
print("viral_db_test: %s" % ("KALDI" if hata else "GEÇTİ"))
sys.exit(1 if hata else 0)
