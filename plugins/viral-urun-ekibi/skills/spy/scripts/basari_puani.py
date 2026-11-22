#!/usr/bin/env python3
"""Sayfa (mağaza) başına 0–100 başarı puanı + gerekçe; pazar başına en iyi N → derin analiz kuyruğu.

  python3 basari_puani.py hesapla --db is/meta/reklam.db [--pazar US,DE] [--en-iyi 300] [--cikti is/meta]
  python3 basari_puani.py liste   --db ... --pazar US [--ilk 20]

Puan (hepsi vekil sinyal; ağırlık ve eşikler DENEME — 4 hafta sonra kendi verimizle kalibre):
  A aktif gün      0–30  en uzun yayındaki reklam (bugün − delivery_start); ≥90 gün tam puan
  B varyant        0–20  sayfanın bizde görülen reklam sayısı (+ Chrome kopya sayısı − 1); ≥20 tam
  C çok mağaza     0–15  aynı başlık/ürün kaç FARKLI sayfada (≥5 sayfa tam) — trend işareti, doygunluk riski raporda
  D niş hacmi      0–10  sayfanın geldiği sorgunun tahmini toplamı (log ölçek; ≥100.000 tam)
  E mağaza         0–25  Shopify + yaş/ölçek: ≤180 gün ve ≤30 ürün 25 · ≤180 gün >30 ürün 18 · ≤365 gün 15 ·
                         daha eski 8 · Shopify ama yaş bilinmiyor 10
Derin analiz kuyruğuna YALNIZ shopify=1 girer. shopify=0 kayıtta kalır ("Shopify değil"); shopify bilinmiyorsa
"alan/Shopify bekliyor" yazılır ve kuyruğa girmez (önce `shopify_kontrol.py`).
Çıktı: `puan` tablosu + `<cikti>/derin-analiz-<pazar>.tsv`.
"""
import argparse
import math
import os
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)
import ortak as o  # noqa: E402
import toplanan_isle as ti  # noqa: E402
import toplayici_ortak as t  # noqa: E402

AGIRLIK_NOTU = "ağırlıklar DENEME (ölçülmedi)"
TSV_SUTUN = ["sira", "pazar", "birim", "sayfa", "alan", "nis", "puan", "reklam", "max_aktif_gun", "magaza_yas_gun",
             "urun_sayisi", "gerekce"]


def puanla(x, m):
    """x: sayfa özeti, m: magaza satırı ya da None → (puan, gerekce, shopify)."""
    g = []
    gun = x["max_gun"]
    a = round(30 * min(gun, 90) / 90) if gun is not None else 0
    g.append("A aktif %s gün=%d" % (gun if gun is not None else "?", a))
    varyant = x["reklam"] + max(0, (x["max_kopya"] or 1) - 1)
    b = round(20 * min(varyant, 20) / 20)
    g.append("B %d reklam/kopya=%d" % (varyant, b))
    k = x["baslik_yayilim"]
    cc = round(15 * min(k - 1, 4) / 4) if k > 1 else 0
    g.append("C başlık %d sayfada=%d%s" % (k, cc, " (doygunluk?)" if k >= 8 else ""))
    nt = x["nis_toplam"]
    d = round(10 * min(math.log10(nt), 5) / 5) if nt and nt > 1 else 0
    g.append("D niş~%s=%d" % (nt if nt is not None else "?", d))
    shp = m["shopify"] if m else None
    if shp == 1:
        yas, n = m["yas_gun"], m["urun_sayisi"]
        if yas is None:
            e, ne = 10, "yaş?"
        elif yas <= 180:
            e, ne = (25, "genç+küçük") if (n is not None and n <= 30) else (18, "genç")
        elif yas <= 365:
            e, ne = 15, "≤1 yıl"
        else:
            e, ne = 8, "eski"
        g.append("E Shopify %s (%s gün, %s ürün)=%d" % (ne, yas if yas is not None else "?", n if n is not None else "?", e))
    elif shp == 0:
        e = 0
        g.append("E Shopify değil=0")
    else:
        e = 0
        g.append("E alan/Shopify bekliyor=0")
    return a + b + cc + d + e, "; ".join(g), shp


def hesapla(c, pazarlar, en_iyi, cikti):
    bugun = t.bugun_str()
    oz = ti.sayfa_ozeti(c)
    magaza = {r["alan"]: r for r in c.execute("SELECT * FROM magaza")}
    for p in pazarlar:
        if p not in t.PAZARLAR:
            raise o.VeriHatasi("pazar geçersiz: %s" % p)
        satirlar = []
        for (pz, b), x in oz.items():
            if pz != p:
                continue
            m = magaza.get(x["alan"]) if x["alan"] else None
            puan, gerekce, shp = puanla(x, m)
            satirlar.append((puan, x, m, gerekce, shp))
        satirlar.sort(key=lambda s: (-s[0], -s[1]["reklam"], s[1]["birim"]))
        c.execute("DELETE FROM puan WHERE pazar=?", (p,))
        derin, sira = [], 0
        for puan, x, m, gerekce, shp in satirlar:
            secildi = shp == 1 and len(derin) < en_iyi
            if secildi:
                sira += 1
                derin.append((sira, puan, x, m, gerekce))
            c.execute("INSERT INTO puan VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (p, x["birim"], x["page_name"], x["alan"], x["nis"], puan, gerekce, shp, 1 if secildi else 0,
                       sira if secildi else None, bugun))
        c.commit()
        if cikti:
            os.makedirs(cikti, exist_ok=True)
            yol = os.path.join(cikti, "derin-analiz-%s.tsv" % p)
            o.tsv_yaz(yol, TSV_SUTUN, [{
                "sira": s, "pazar": p, "birim": x["birim"], "sayfa": x["page_name"] or o.GORUNMUYOR, "alan": x["alan"],
                "nis": x["nis"] or o.GORUNMUYOR, "puan": pu, "reklam": x["reklam"],
                "max_aktif_gun": x["max_gun"] if x["max_gun"] is not None else o.GORUNMUYOR,
                "magaza_yas_gun": m["yas_gun"] if m["yas_gun"] is not None else o.GORUNMUYOR,
                "urun_sayisi": m["urun_sayisi"] if m["urun_sayisi"] is not None else o.GORUNMUYOR, "gerekce": ge}
                for s, pu, x, m, ge in derin])
        bek = sum(1 for s in satirlar if s[4] is None)
        degil = sum(1 for s in satirlar if s[4] == 0)
        print("%s: %d sayfa puanlandı · derin analiz %d/%d · Shopify değil %d · alan/Shopify bekliyor %d · %s"
              % (p, len(satirlar), len(derin), en_iyi, degil, bek, AGIRLIK_NOTU))


def liste(c, pazar, ilk):
    print("sira\tpuan\tshopify\tsayfa\talan\tgerekce")
    for r in c.execute("SELECT * FROM puan WHERE pazar=? ORDER BY derin DESC, puan DESC LIMIT ?", (pazar, ilk)):
        print("\t".join(str(r[k]) if r[k] is not None else "-" for k in ("sira", "puan", "shopify", "page_name", "alan", "gerekce")))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut")
    h = alt.add_parser("hesapla")
    h.add_argument("--db", required=True)
    h.add_argument("--pazar", default=",".join(t.PAZARLAR))
    h.add_argument("--en-iyi", type=int, default=300)
    h.add_argument("--cikti")
    l_ = alt.add_parser("liste")
    l_.add_argument("--db", required=True)
    l_.add_argument("--pazar", required=True)
    l_.add_argument("--ilk", type=int, default=20)
    x = ap.parse_args()
    if not x.komut:
        ap.print_help()
        sys.exit(1)
    try:
        c = t.baglan(x.db)
        if x.komut == "hesapla":
            if not 1 <= x.en_iyi <= 2000:
                raise o.VeriHatasi("--en-iyi 1..2000 olmalı")
            hesapla(c, [p.strip().upper() for p in x.pazar.split(",") if p.strip()], x.en_iyi, x.cikti)
        else:
            liste(c, x.pazar.upper(), x.ilk)
    except o.VeriHatasi as e:
        o.hata_cik(str(e))


if __name__ == "__main__":
    main()
