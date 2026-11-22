#!/usr/bin/env python3
"""Reklamdan mağazaya ve AliExpress eşleme listesine geçiş.

  python3 magaza_gecis.py liste  --kok is/meta [--en-cok 15]
        Okunacak Shopify mağazalarını (önce OLCEKLENIYOR, sonra çok reklamlı TEST; son 7 günde okunmamış) basar.
        Son satır magaza_oku.js'e yapıştırılacak `window.__REKLAMAVI_MAGAZALAR = [...]` satırıdır.
        ALTALAN-LANDING / DİĞER birimler ayrıca "elle salt-okuma" listesi olarak basılır.
  python3 magaza_gecis.py aktar  --kok is/meta <magaza-dokumu.txt> [parça2.txt ...]
        meta_aktar.js (KAYNAK='magaza') çıktısını magazalar.tsv'ye yazar, etiketleri yeniden hesaplar.
        Biçim bozuk / parça eksik / adet tutmuyor → çıkış 1.
  python3 magaza_gecis.py esleme --kok is/meta
        OLCEKLENIYOR + genç (≤180 gün, ≤30 ürün) Shopify mağazalarının ana ürünlerinden is/meta/aliexpress-esleme.md yazar
        (kaynak META-<kutuphane_kodu>). AliExpress araması lider Chrome'dan, `hunter` akışıyla yapılır.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402
import kazanan_puan as kp  # noqa: E402
import nis_kelime as nk  # noqa: E402

MAGAZA_SATIR = ["alan", "durum", "urun_sayisi", "ilk_urun", "son_urun", "medyan_fiyat", "ana_urun",
                "ana_urun_eklenme", "ana_fiyat", "ana_cizili", "ana_handle"]


def liste(kok, en_cok):
    birimler = o.oku(kok, "birim")
    magazalar = {m["alan"]: m for m in o.oku(kok, "magaza")}
    bugun = o.bugun().date().isoformat()

    def taze(alan):
        m = magazalar.get(alan)
        return m and o.iso_mu(m["okuma_tarihi"]) and o.gun_farki(bugun, m["okuma_tarihi"]) < 7

    shop = [b for b in birimler if b["tip"] == "SHOPIFY" and not b["birim"].startswith("sayfa:") and not taze(b["birim"])]
    shop.sort(key=lambda b: (b["etiket"] != "OLCEKLENIYOR", b["etiket"] == "ESKI-KAZANAN", -int(b["reklam_sayisi"] or 0)))
    secilen = shop[:en_cok]
    print("# Shopify mağazaları (%d / %d aday) — magaza_oku.js ile:" % (len(secilen), len(shop)))
    for b in secilen:
        print("  %s %-12s %-35s reklam=%s kopya=%s" % (b["ulke"], b["etiket"], b["birim"], b["reklam_sayisi"], b["kopya_toplami"]))
    elle = [b for b in birimler if b["tip"] in ("ALTALAN-LANDING", "DİĞER") and b["etiket"] == "OLCEKLENIYOR"]
    if elle:
        print("# Elle salt-okuma (fiyat/teklif → teklif.tsv; marka/ürün adı yoksa eşleme yok):")
        for b in elle[:en_cok]:
            print("  %s %s %s reklam=%s" % (b["ulke"], b["tip"], b["birim"], b["reklam_sayisi"]))
    js = [{"alan": b["birim"], "yollar": [y for y in b["urun_yollari"].split(",") if y]} for b in secilen]
    print("window.__REKLAMAVI_MAGAZALAR = %s;" % json.dumps(js, ensure_ascii=False))


def dokum_oku(yollar):
    parcalar, taban = {}, None
    for yol in yollar:
        if not os.path.exists(yol):
            raise o.VeriHatasi("döküm yok: %s" % yol)
        guncel = None
        with open(yol, encoding="utf-8") as f:
            for no, s in enumerate(f.read().split("\n"), start=1):
                s = s.rstrip("\r")
                if not s.strip():
                    continue
                if s.startswith("#REKLAMAVI-MAGAZA"):
                    h = s.split("\t")
                    if h[0] != "#REKLAMAVI-MAGAZA v1":
                        raise o.VeriHatasi("%s:%d sürüm v1 değil" % (yol, no))
                    m = dict(p.split("=", 1) for p in h[1:] if "=" in p)
                    if not (o.iso_mu(m.get("okuma")) and o.sayi_mi(m.get("adet")) and re.fullmatch(r"\d+/\d+", m.get("parca", ""))):
                        raise o.VeriHatasi("%s:%d başlık eksik/bozuk (okuma, adet, parca)" % (yol, no))
                    i, n = [int(x) for x in m["parca"].split("/")]
                    t = (m["okuma"], int(m["adet"]), n)
                    if taban and t != taban:
                        raise o.VeriHatasi("%s:%d parça başka döküme ait" % (yol, no))
                    taban = t
                    if i in parcalar:
                        raise o.VeriHatasi("%s:%d parça %d iki kez" % (yol, no, i))
                    parcalar[i] = []
                    guncel = parcalar[i]
                    continue
                if guncel is None:
                    raise o.VeriHatasi("%s:%d başlıksız satır" % (yol, no))
                h = s.split("\t")
                if len(h) != len(MAGAZA_SATIR):
                    raise o.VeriHatasi("%s:%d %d alan var, %d bekleniyor" % (yol, no, len(h), len(MAGAZA_SATIR)))
                r = dict(zip(MAGAZA_SATIR, h))
                if not (r["durum"] in ("OK", "KAPALI") or r["durum"].startswith("HATA-")):
                    raise o.VeriHatasi("%s:%d durum geçersiz: %s" % (yol, no, r["durum"]))
                if r["durum"] == "OK" and not (o.sayi_mi(r["urun_sayisi"]) and o.iso_mu(r["ilk_urun"])):
                    raise o.VeriHatasi("%s:%d OK satırında ürün sayısı/ilk ürün tarihi yok" % (yol, no))
                guncel.append(r)
    if not taban:
        raise o.VeriHatasi("#REKLAMAVI-MAGAZA başlığı yok")
    okuma, adet, n = taban
    if sorted(parcalar) != list(range(1, n + 1)):
        raise o.VeriHatasi("parça eksik: elde %s, beklenen 1..%d" % (sorted(parcalar), n))
    satirlar = [r for i in sorted(parcalar) for r in parcalar[i]]
    if len(satirlar) != adet:
        raise o.VeriHatasi("başlık adet=%d ama %d satır" % (adet, len(satirlar)))
    return okuma, satirlar


def aktar(kok, yollar):
    okuma, satirlar = dokum_oku(yollar)
    mevcut = {m["alan"]: m for m in o.oku(kok, "magaza")}
    for r in satirlar:
        bos = o.GORUNMUYOR if r["durum"] == "OK" else ""
        mevcut[r["alan"]] = {
            "alan": r["alan"], "okuma_tarihi": okuma, "durum": r["durum"],
            "urun_sayisi": r["urun_sayisi"], "ilk_urun": r["ilk_urun"], "son_urun": r["son_urun"],
            "medyan_fiyat": r["medyan_fiyat"], "ana_urun": r["ana_urun"] or bos,
            "ana_urun_eklenme": r["ana_urun_eklenme"] or bos, "ana_fiyat": r["ana_fiyat"] or bos,
            "ana_cizili": r["ana_cizili"] or ("yok" if r["durum"] == "OK" else ""), "ana_handle": r["ana_handle"],
        }
    o.yaz(kok, "magaza", list(mevcut.values()))
    r, b = kp.hesapla(kok)
    o.yaz(kok, "reklam", r)
    o.yaz(kok, "birim", b)
    print("magazalar.tsv: %d satır yazıldı (OK %d) · etiketler yeniden hesaplandı" %
          (len(satirlar), sum(1 for x in satirlar if x["durum"] == "OK")))


def esleme(kok):
    birimler = o.oku(kok, "birim")
    reklamlar = o.oku(kok, "reklam")
    magazalar = {m["alan"]: m for m in o.oku(kok, "magaza")}
    try:
        ele_nis = {n for n, v in nk.nisler_oku().items() if v["ele"]}
    except o.VeriHatasi:
        ele_nis = {"kozmetik-saglik"}
    satirlar, ele_atlanan = [], []
    for b in birimler:
        m = magazalar.get(b["birim"])
        if b["etiket"] != "OLCEKLENIYOR" or b["tip"] != "SHOPIFY" or kp.magaza_genc_mi(m, b["son_okuma"]) != "E":
            continue
        if b["nis"] in ele_nis:
            ele_atlanan.append(b["birim"])
            continue
        rs = [r for r in reklamlar if r["ulke"] == b["ulke"] and kp.birim_anahtari(r) == b["birim"]]
        rs.sort(key=lambda r: (-(int(r["kopya"]) if o.sayi_mi(r["kopya"]) else 0), -(int(r["aktif_gun"]) if o.sayi_mi(r["aktif_gun"]) else 0)))
        kod = rs[0]["kutuphane_kodu"] if rs else "?"
        ele = ""
        satirlar.append("| META-%s | %s | %s | %s%s | %s | %s / %s | %s | https://%s/products/%s | _(lider yazar)_ | _(boş)_ | BEKLIYOR |" % (
            kod, b["ulke"], b["birim"], b["nis"], ele, m["ana_urun"], m["ana_fiyat"], m["ana_cizili"],
            m["ilk_urun"], b["birim"], m["ana_handle"]))
    yol = os.path.join(kok, "aliexpress-esleme.md")
    with open(yol, "w", encoding="utf-8") as f:
        f.write("# AliExpress eşleme listesi (%s)\n\n" % o.bugun().date().isoformat())
        f.write("Kaynak: `kazanan_puan.py` OLCEKLENIYOR + mağaza ≤%d gün ve ≤%d ürün (%s).\n" %
                (o.ESIK["magaza_yas_gun"], o.ESIK["magaza_urun"], o.ESIK_NOTU))
        f.write("Kimlik = form + ana parça + mekanizma (benzer ≠ aynı). Eşleşen ürün `is/firsat/adaylar.md`'ye kaynak `META-<kod>` ile girer;\n"
                "ELE-KAPISI nişi (kozmetik/sağlık) eşlenmez. Durum: BEKLIYOR → ESLESTI / BULUNAMADI / ELE.\n\n")
        f.write("| Kaynak | Ülke | Mağaza | Niş | Ana ürün | Fiyat / çizili | Mağaza ilk ürün | Ürün sayfası | 3–5 kelime İngilizce tanım | AliExpress linki | Durum |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
        f.write("\n".join(satirlar) + ("\n" if satirlar else "_(uygun mağaza yok — önce `liste` + magaza_oku.js + `aktar`)_\n"))
        if ele_atlanan:
            f.write("\nELE KAPISI nedeniyle eşlenmedi (sinyal olarak kayıtta): %s\n" % ", ".join(ele_atlanan))
    print("%s: %d satır (ELE kapısından atlanan %d)" % (yol, len(satirlar), len(ele_atlanan)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut")
    a = alt.add_parser("liste")
    a.add_argument("--kok", default="is/meta")
    a.add_argument("--en-cok", type=int, default=15)
    b = alt.add_parser("aktar")
    b.add_argument("--kok", default="is/meta")
    b.add_argument("dosyalar", nargs="+")
    c = alt.add_parser("esleme")
    c.add_argument("--kok", default="is/meta")
    x = ap.parse_args()
    try:
        if x.komut == "liste":
            liste(x.kok, x.en_cok)
        elif x.komut == "aktar":
            aktar(x.kok, x.dosyalar)
        elif x.komut == "esleme":
            esleme(x.kok)
        else:
            ap.print_help()
            sys.exit(1)
    except o.VeriHatasi as e:
        o.hata_cik(str(e))


if __name__ == "__main__":
    main()
