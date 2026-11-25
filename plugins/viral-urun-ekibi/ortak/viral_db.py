#!/usr/bin/env python3
"""Sansürlü viral ürün tablosu (bilgi/viral-urunler.tsv) üstünde "zaten viral mi" kontrolü.

Eşleşme kuralı skills/hunter/trendyol/scripts/trendyol_kontrol.py `viral` komutuyla AYNIDIR (analiz.db yerine TSV'den):
  - yalnız hukum VIRAL-URUN / VIRAL-VIDEO satırları taranır;
  - VIRAL-URUN satırıyla ürün metni arasında >= 4 ortak sözcük (>= 4 harf, TR harfleri katlanmış) -> "ayni-urun-viral";
  - aksi halde aile sözcüklerinden biri satırın ad+aile sözcükleriyle kesişirse -> "aile-var";
  - yoksa "yok". Tablo yoksa "dogrulanamadi".
Kullanım (modül):  from viral_db import ara;  ara("cepli bebek taşıyıcı hoodie", aile="cepli-hoodie")
Kullanım (komut):  python3 viral_db.py "<ürün metni>" [aile]
"""
import csv
import json
import os
import re
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
VARSAYILAN_TSV = os.path.join(BURADA, "bilgi", "viral-urunler.tsv")
VIRAL_HUKUMLER = ("VIRAL-URUN", "VIRAL-VIDEO")


def fold(s):
    return (s or "").translate(str.maketrans("ıİşŞğĞüÜöÖçÇ", "iissgguuoocc")).lower()


def jeton(s, en_az=4):
    return {t for t in re.split(r"[^a-z0-9]+", fold(s)) if len(t) >= en_az}


def oku(tsv=None):
    yol = tsv or os.environ.get("VIRAL_DB_TSV") or VARSAYILAN_TSV
    if not os.path.isfile(yol):
        return None
    with open(yol, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def ara(urun_metni, aile=None, tsv=None):
    """-> {"durum": yok|aile-var|ayni-urun-viral|dogrulanamadi, "eslesen": [{urun_id, ad_jenerik, aile, hukum}...]}"""
    satirlar = oku(tsv)
    if satirlar is None:
        return {"durum": "dogrulanamadi", "eslesen": []}
    urun_j = jeton(urun_metni)
    aile_j = jeton((aile or "").replace("-", " "))
    sonuc, eslesen = "yok", []
    for r in satirlar:
        if r.get("hukum") not in VIRAL_HUKUMLER:
            continue
        ad_j = jeton(r.get("ad_jenerik"))
        kayit = {k: r.get(k, "") for k in ("urun_id", "ad_jenerik", "aile", "hukum")}
        if r["hukum"] == "VIRAL-URUN" and len(urun_j & ad_j) >= 4:
            return {"durum": "ayni-urun-viral", "eslesen": [kayit]}
        if aile_j and aile_j & (ad_j | jeton((r.get("aile") or "").replace("-", " "))):
            sonuc = "aile-var"
            eslesen.append(kayit)
    return {"durum": sonuc, "eslesen": eslesen}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    print(json.dumps(ara(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None), ensure_ascii=False, indent=1))
