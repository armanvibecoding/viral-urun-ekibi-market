#!/usr/bin/env python3
"""Kazanan puanlayıcı — etiketi YALNIZ bu betik verir (elle yazılmaz).

Kullanım:
  python3 kazanan_puan.py [--kok is/meta]            # reklamlar.tsv + sayfalar.tsv etiketlerini yeniden hesaplar ve yazar
  python3 kazanan_puan.py [--kok is/meta] --denetle  # yazılı etiket ≠ hesaplanan → listeler, çıkış 1
  python3 kazanan_puan.py [--kok is/meta] --liste    # en güçlü birimleri basar

Reklam (kreatif) etiketi:
  aktif_gun veya kopya görünmüyor → BILINMIYOR
  aktif_gun ≥ 30 ve kopya ≥ 3 → aktif_gun > 180 ise ESKI-KAZANAN, değilse OLCEKLENIYOR
  diğer → TEST
Birim (mağaza = hedef alan adı; linksizse sayfa adı) etiketi:
  sinyal = max(taranan aktif reklam, alan sorgusu "~N sonuç") ≥ 10  VEYA  ≥1 kazanan kreatif
  sinyal yok → TEST
  sinyal var + (mağaza ilk ürünü > 180 gün ya da > 30 ürün ya da ilk reklam > 180 gün) → ESKI-KAZANAN
  sinyal var + genç ya da yaşı henüz okunmamış → OLCEKLENIYOR
Tüm eşikler DENEME (ortak.ESIK).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402


def reklam_etiketi(r):
    g, k = r.get("aktif_gun", ""), r.get("kopya", "")
    if not (o.sayi_mi(g) and o.sayi_mi(k)):
        return "BILINMIYOR"
    g, k = int(g), int(k)
    if g >= o.ESIK["kreatif_aktif_gun"] and k >= o.ESIK["kreatif_kopya"]:
        return "ESKI-KAZANAN" if g > o.ESIK["eski_gun"] else "OLCEKLENIYOR"
    return "TEST"


def magaza_genc_mi(m, okuma):
    """'E' / 'H' / '?' (okunmamış ya da kapalı)."""
    if not m or m.get("durum") != "OK" or not o.iso_mu(m.get("ilk_urun")) or not o.sayi_mi(m.get("urun_sayisi")):
        return "?"
    yas = o.gun_farki(okuma, m["ilk_urun"])
    return "E" if (yas <= o.ESIK["magaza_yas_gun"] and int(m["urun_sayisi"]) <= o.ESIK["magaza_urun"]) else "H"


def birim_etiketi(b, magaza):
    olcek = int(b["reklam_sayisi"]) if o.sayi_mi(b["reklam_sayisi"]) else 0
    if o.sayi_mi(b.get("alan_sorgu", "")):
        olcek = max(olcek, int(b["alan_sorgu"]))
    kk = int(b["kazanan_kreatif"]) if o.sayi_mi(b.get("kazanan_kreatif", "")) else 0
    if not (olcek >= o.ESIK["birim_aktif_reklam"] or kk >= 1):
        return "TEST"
    genc = magaza_genc_mi(magaza, b["son_okuma"])
    eski_reklam = o.iso_mu(b["ilk_baslangic"]) and o.gun_farki(b["son_okuma"], b["ilk_baslangic"]) > o.ESIK["eski_gun"]
    if genc == "H" or eski_reklam:
        return "ESKI-KAZANAN"
    return "OLCEKLENIYOR"


def hesapla(kok):
    """(reklamlar, birimler) — etiketleri hesaplanmış kopyalar."""
    reklamlar = o.oku(kok, "reklam")
    birimler = o.oku(kok, "birim")
    magazalar = {m["alan"]: m for m in o.oku(kok, "magaza")}
    yeni_r = []
    for r in reklamlar:
        r2 = dict(r)
        r2["etiket"] = reklam_etiketi(r)
        yeni_r.append(r2)
    kazanan = {}
    for r in yeni_r:
        if r["etiket"] in ("OLCEKLENIYOR", "ESKI-KAZANAN"):
            kazanan[(r["ulke"], birim_anahtari(r))] = kazanan.get((r["ulke"], birim_anahtari(r)), 0) + 1
    yeni_b = []
    for b in birimler:
        b2 = dict(b)
        b2["kazanan_kreatif"] = str(kazanan.get((b["ulke"], b["birim"]), 0))
        b2["etiket"] = birim_etiketi(b2, magazalar.get(b["birim"]))
        yeni_b.append(b2)
    return yeni_r, yeni_b


def birim_anahtari(r):
    return r["hedef_alan"] if r.get("hedef_alan") else "sayfa:" + r.get("sayfa_adi", "")


def denetle(kok):
    reklamlar, birimler = o.oku(kok, "reklam"), o.oku(kok, "birim")
    h_r, h_b = hesapla(kok)
    farklar = []
    for a, b in zip(reklamlar, h_r):
        if a["etiket"] != b["etiket"]:
            farklar.append("reklam %s: yazılı=%s hesaplanan=%s" % (a["kutuphane_kodu"], a["etiket"], b["etiket"]))
    for a, b in zip(birimler, h_b):
        if a["etiket"] != b["etiket"] or a["kazanan_kreatif"] != b["kazanan_kreatif"]:
            farklar.append("birim %s/%s: yazılı=%s hesaplanan=%s" % (a["ulke"], a["birim"], a["etiket"], b["etiket"]))
    return farklar


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kok", default="is/meta")
    ap.add_argument("--denetle", action="store_true")
    ap.add_argument("--liste", action="store_true")
    a = ap.parse_args()
    try:
        if a.denetle:
            f = denetle(a.kok)
            if f:
                print("ELLE DEĞİŞTİRİLMİŞ / ESKİ ETİKET (%d):" % len(f))
                for s in f[:50]:
                    print("  " + s)
                print("Düzeltme: elle yazma; `kazanan_puan.py --kok %s` yeniden hesaplasın." % a.kok)
                sys.exit(1)
            print("etiketler tutarlı (%s)" % o.ESIK_NOTU)
            return
        r, b = hesapla(a.kok)
        o.yaz(a.kok, "reklam", r)
        o.yaz(a.kok, "birim", b)
        say = {}
        for x in b:
            say[x["etiket"]] = say.get(x["etiket"], 0) + 1
        print("birim etiketleri: %s · %s" % (say, o.ESIK_NOTU))
        if a.liste:
            b.sort(key=lambda x: (x["etiket"] != "OLCEKLENIYOR", -int(x["reklam_sayisi"] or 0)))
            for x in b[:15]:
                print("  %s %-12s %-35s reklam=%s kopya=%s kazanan_kreatif=%s" % (
                    x["ulke"], x["etiket"], x["birim"][:35], x["reklam_sayisi"], x["kopya_toplami"], x["kazanan_kreatif"]))
    except o.VeriHatasi as e:
        o.hata_cik(str(e))


if __name__ == "__main__":
    main()
