#!/usr/bin/env python3
"""Haftalık niş raporu.

  python3 haftalik_rapor.py --kok is/meta [--gun 7]
        → is/meta/nis-raporu-<tarih>.md : pazar × niş başına en güçlü 3 mağaza, en güçlü 5 kreatif, ivme (gün 0 → gün 7),
          sorgu/sınırlama özeti ve "yeni kelime adayı" (kazanan reklam gövdelerinde ≥3 farklı reklamda geçen 2–3 kelimelik ifade).
Reddeder (çıkış 1): kayıt şeması bozuk (kayit_denetle) ya da son N günde hiç reklam yok.
Rapor kısa tutulur; ham tablo dosyalarda kalır.
"""
import argparse
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402
import kazanan_puan as kp  # noqa: E402
import kayit_denetle as kd  # noqa: E402

DURAK = set("""ve ile bu bir için da de en çok daha her the and for with your you our to of a in on is are this that it
und der die das mit für ein eine le la les de des et pour avec un une el la los las y con para un una del al
kargo shipping free ücretsiz""".split())


def ivme(gecmis, ulke, birim, bugun, gun):
    s = sorted((g for g in gecmis if g["ulke"] == ulke and g["birim"] == birim), key=lambda g: g["tarih"])
    if len(s) < 2:
        return "tek ölçüm"
    son = s[-1]
    eski = [g for g in s if o.gun_farki(son["tarih"], g["tarih"]) >= gun]
    if not eski:
        return "tek hafta"
    e = eski[-1]
    d = int(son["reklam_sayisi"]) - int(e["reklam_sayisi"])
    return "%+d reklam (%s→%s)" % (d, e["tarih"], son["tarih"])


def kelime_adaylari(reklamlar):
    say = collections.Counter()
    for r in reklamlar:
        t = re.findall(r"[^\W\d_]+", o.norm(r["govde_ilk200"]))
        gor = set()
        for n in (2, 3):
            for i in range(len(t) - n + 1):
                g = t[i:i + n]
                if g[0] in DURAK or g[-1] in DURAK or all(x in DURAK for x in g):
                    continue
                gor.add(" ".join(g))
        say.update(gor)
    return [(g, n) for g, n in say.most_common(20) if n >= 3][:8]


def rapor(kok, gun):
    hatalar = kd.denetle(kok)
    if hatalar:
        raise o.VeriHatasi("kayıt bozuk, önce düzelt: %s" % hatalar[0])
    bugun = o.bugun().date().isoformat()
    reklamlar = [r for r in o.oku(kok, "reklam") if o.gun_farki(bugun, r["okuma_tarihi"]) < gun]
    if not reklamlar:
        raise o.VeriHatasi("son %d günde reklam kaydı yok — rapor üretilmez" % gun)
    birimler = o.oku(kok, "birim")
    gecmis = o.oku(kok, "gecmis")
    aramalar = [a for a in o.oku(kok, "arama") if o.gun_farki(bugun, a["tarih"]) < gun]
    magazalar = {m["alan"]: m for m in o.oku(kok, "magaza")}
    import nis_kelime as nk
    try:
        ele = {n for n, v in nk.nisler_oku().items() if v["ele"]}
    except o.VeriHatasi:
        ele = {"kozmetik-saglik"}
    y = ["# Niş raporu — %s (son %d gün)" % (bugun, gun), "",
         "Sorgu: %d · sınırlama: %d · gerçek sıfır: %d · reklam: %d · %s. Sinyaller vekildir (satış değil)." % (
             sum(1 for a in aramalar if a["aile"] in o.SORGU_AILELERI),
             sum(1 for a in aramalar if a["durum"] == "SINIRLAMA"),
             sum(1 for a in aramalar if a["durum"] == "GERCEK-SIFIR"), len(reklamlar), o.ESIK_NOTU), ""]
    gruplar = collections.defaultdict(list)
    for r in reklamlar:
        gruplar[(r["ulke"], r["nis"])].append(r)
    for (ulke, nis) in sorted(gruplar):
        rs = gruplar[(ulke, nis)]
        anahtarlar = {kp.birim_anahtari(r) for r in rs}
        bs = [b for b in birimler if b["ulke"] == ulke and b["birim"] in anahtarlar]
        bs.sort(key=lambda b: (b["etiket"] != "OLCEKLENIYOR", b["etiket"] != "ESKI-KAZANAN", -int(b["reklam_sayisi"] or 0)))
        y.append("## %s · %s%s — %d reklam, %d mağaza" % (o.PAZAR_AD.get(ulke, ulke), nis, " ⚠ELE KAPISI (ürün önerilmez)" if nis in ele else "", len(rs), len(bs)))
        for b in bs[:3]:
            m = magazalar.get(b["birim"], {})
            yas = ("mağaza ilk ürün %s, %s ürün" % (m.get("ilk_urun"), m.get("urun_sayisi"))) if m.get("durum") == "OK" else "mağaza okunmadı"
            y.append("- **%s** %s · %s · reklam %s (alan sorgusu %s) · kopya %s · ilk reklam %s · %s · ivme: %s" % (
                b["etiket"], b["birim"], b["tip"], b["reklam_sayisi"], b["alan_sorgu"] or "—", b["kopya_toplami"],
                b["ilk_baslangic"], yas, ivme(gecmis, ulke, b["birim"], bugun, gun)))
        kaz = [r for r in rs if r["etiket"] in ("OLCEKLENIYOR", "ESKI-KAZANAN")]
        kaz.sort(key=lambda r: -(int(r["kopya"]) * int(r["aktif_gun"])))
        if kaz:
            y.append("- Kazanan kreatif (%d):" % len(kaz))
            for r in kaz[:5]:
                y.append("  - %s · %s gün · %s kopya · %s · izlendi=%s · \"%s\"" % (
                    r["kutuphane_kodu"], r["aktif_gun"], r["kopya"], r["sayfa_adi"], r["izlendi"], r["govde_ilk200"][:90]))
        else:
            y.append("- Kazanan kreatif yok (eşik: ≥%d gün ve ≥%d kopya)." % (o.ESIK["kreatif_aktif_gun"], o.ESIK["kreatif_kopya"]))
        y.append("")
    kaz_hepsi = [r for r in reklamlar if r["etiket"] in ("OLCEKLENIYOR", "ESKI-KAZANAN")]
    aday = kelime_adaylari(kaz_hepsi)
    y.append("## Yeni kelime adayı (kazanan gövdelerde ≥3 reklamda) → nisler.md'ye elle değerlendirip ekle")
    y.append(", ".join("`%s` (%d)" % a for a in aday) if aday else "_(yok — kazanan gövde sayısı yetersiz)_")
    yol = os.path.join(kok, "nis-raporu-%s.md" % bugun)
    with open(yol, "w", encoding="utf-8") as f:
        f.write("\n".join(y) + "\n")
    return yol, len(gruplar)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kok", default="is/meta")
    ap.add_argument("--gun", type=int, default=7)
    a = ap.parse_args()
    try:
        yol, n = rapor(a.kok, a.gun)
    except o.VeriHatasi as e:
        o.hata_cik(str(e))
    print("%s yazıldı (%d pazar×niş grubu)" % (yol, n))


if __name__ == "__main__":
    main()
