#!/usr/bin/env python3
"""Kayıt şeması doğrulayıcı — is/meta altındaki tüm TSV'leri denetler.

  python3 kayit_denetle.py [--kok is/meta]      # temizse çıkış 0, hata listesiyle çıkış 1

Denetlenen: başlık = şema · ülke/aile/tip/etiket listede · Kütüphane Kodu sayı ve tekil · tarihler ISO ya da 'görünmüyor' ·
aktif_gun = okuma − ilk yayın · kopya ≥1 tamsayı ya da 'görünmüyor' (0 YASAK: okunamayan alan 0 değildir) ·
sayfalar toplamı reklamlarla tutuyor · etiketler betiğin hesabıyla aynı (elle etiket yok) · aramalarda günlük kota.
"""
import argparse
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402
import kazanan_puan as kp  # noqa: E402


def denetle(kok):
    h = []
    try:
        reklamlar = o.oku(kok, "reklam")
        birimler = o.oku(kok, "birim")
        aramalar = o.oku(kok, "arama")
        o.oku(kok, "magaza")
        o.oku(kok, "gecmis")
        o.oku(kok, "alan")
        o.oku(kok, "teklif")
    except o.VeriHatasi as e:
        return [str(e)]
    goruldu = set()
    for i, r in enumerate(reklamlar, start=2):
        y = "reklamlar.tsv:%d" % i
        if not o.sayi_mi(r["kutuphane_kodu"]):
            h.append("%s Kütüphane Kodu sayı değil" % y)
        if r["kutuphane_kodu"] in goruldu:
            h.append("%s Kütüphane Kodu tekrar: %s" % (y, r["kutuphane_kodu"]))
        goruldu.add(r["kutuphane_kodu"])
        if r["ulke"] not in o.ULKELER:
            h.append("%s ülke geçersiz: %s" % (y, r["ulke"]))
        if r["aile"] not in o.SORGU_AILELERI:
            h.append("%s aile geçersiz: %s" % (y, r["aile"]))
        if r["tip"] not in o.TIPLER:
            h.append("%s tip geçersiz: %s" % (y, r["tip"]))
        if r["etiket"] not in o.ETIKETLER_REKLAM:
            h.append("%s etiket geçersiz: %s" % (y, r["etiket"]))
        if r["izlendi"] not in ("E", "H"):
            h.append("%s izlendi E/H olmalı" % y)
        if not o.iso_mu(r["okuma_tarihi"]):
            h.append("%s okuma_tarihi ISO değil" % y)
        ilk, gun, kop = r["ilk_yayin"], r["aktif_gun"], r["kopya"]
        if ilk != o.GORUNMUYOR and not o.iso_mu(ilk):
            h.append("%s ilk_yayin ISO ya da '%s' olmalı: %r" % (y, o.GORUNMUYOR, ilk))
        if ilk == o.GORUNMUYOR and gun != o.GORUNMUYOR:
            h.append("%s ilk yayın görünmüyor ama aktif_gun=%s yazılmış" % (y, gun))
        if o.iso_mu(ilk) and o.iso_mu(r["okuma_tarihi"]):
            beklenen = o.gun_farki(r["okuma_tarihi"], ilk)
            if gun != str(beklenen):
                h.append("%s aktif_gun %s ≠ okuma−ilk yayın %d" % (y, gun, beklenen))
        if kop != o.GORUNMUYOR and not (o.sayi_mi(kop) and int(kop) >= 1):
            h.append("%s kopya ≥1 tamsayı ya da '%s' olmalı: %r (0 yazılmaz)" % (y, o.GORUNMUYOR, kop))
        for alan in ("sayfa_adi", "govde_ilk200", "cta", "medya"):
            if r[alan] == "":
                h.append("%s %s boş — okunamadıysa '%s' yazılır" % (y, alan, o.GORUNMUYOR))
    say = collections.Counter((r["ulke"], kp.birim_anahtari(r)) for r in reklamlar)
    for i, b in enumerate(birimler, start=2):
        y = "sayfalar.tsv:%d" % i
        if b["etiket"] not in o.ETIKETLER_BIRIM:
            h.append("%s etiket geçersiz: %s" % (y, b["etiket"]))
        if not o.sayi_mi(b["reklam_sayisi"]) or int(b["reklam_sayisi"]) > say.get((b["ulke"], b["birim"]), 0):
            h.append("%s reklam_sayisi %s, reklamlar.tsv'de bu birimin %d satırı var" %
                     (y, b["reklam_sayisi"], say.get((b["ulke"], b["birim"]), 0)))
        if b["alan_sorgu"] and not o.sayi_mi(b["alan_sorgu"]):
            h.append("%s alan_sorgu sayı değil" % y)
    gun_say = collections.Counter(a["tarih"] for a in aramalar)
    for t, n in gun_say.items():
        if n > o.GUNLUK_KOTA:
            h.append("aramalar.tsv %s günü %d sorgu (kota %d)" % (t, n, o.GUNLUK_KOTA))
    for a in aramalar:
        if a["aile"] not in o.AILELER or a["ulke"] not in o.ULKELER:
            h.append("aramalar.tsv geçersiz aile/ülke: %s %s" % (a["aile"], a["ulke"]))
    if not h:
        h += kp.denetle(kok)
    return h


def calistir(kok):
    h = denetle(kok)
    if h:
        print("KAYIT HATASI (%d):" % len(h))
        for s in h[:60]:
            print("  " + s)
        return 1
    print("kayıt temiz: %s" % kok)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kok", default="is/meta")
    sys.exit(calistir(ap.parse_args().kok))
