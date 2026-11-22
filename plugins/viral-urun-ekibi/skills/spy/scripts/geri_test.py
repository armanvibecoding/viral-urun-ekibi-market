#!/usr/bin/env python3
"""Kırma testi 1 — gerçek veriyle geri test.

  python3 geri_test.py <eski-ozet.tsv> [--boz]

Girdi: önceki elle toplamanın mağaza özeti (sütunlar: alan_adi, sayfa, tip, reklam_sayisi, kopya_toplami, ilk_baslangic,
son_baslangic, urun_sluglari; '#' satırları yorum). Ham localStorage dökümü saklanmadığı için özetten SENTETİK ham üretilir
(Meta kart biçiminde: Türkçe tarih metni, l.facebook.com sarmalı, utm, kopya metni, 2 parça) → meta_kayit.py kaydet →
sayfalar.tsv her satırı özetle birebir karşılaştırılır (reklam sayısı, kopya toplamı, ilk/son başlangıç, tip, sayfa adı).
--boz: en çok reklamlı satırdan bir kart düşürülür → karşılaştırma TUTMAMALI (çıkış 1). Kapı kırılmazsa yeşil sayılmaz.
Sınır: bu test meta_kayit.py'nin hesabını ve tip/tarih/link çözümlemesini sınar; meta_topla.js'in sayfadan okumasını SINAMAZ.
"""
import argparse
import os
import subprocess
import sys
import tempfile
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o  # noqa: E402

BURASI = os.path.dirname(os.path.abspath(__file__))
TR_AY = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]


def tr_tarih(iso):
    y, a, g = iso.split("-")
    return "%d %s %s tarihinde yayınlanmaya başladı" % (int(g), TR_AY[int(a) - 1], y)


def ham_yaz(yol_taban, meta, kartlar, parca=1):
    """kartlar: [[kod, sayfa, tarih_metni, kopya_metni, kart_tam, link, cta, medya, govde], ...] → parça dosyaları."""
    n = max(1, parca)
    boy = (len(kartlar) + n - 1) // n if kartlar else 0
    yollar = []
    for i in range(n):
        parcasi = kartlar[i * boy:(i + 1) * boy] if boy else []
        baslik = "\t".join(["#REKLAMAVI v1"] + ["%s=%s" % (k, meta[k]) for k in ("ulke", "sorgu", "nis", "aile", "siralama", "baslangic")]
                           + ["kart=%d" % len(kartlar), "parca=%d/%d" % (i + 1, n)])
        yol = "%s-%d.txt" % (yol_taban, i + 1)
        with open(yol, "w", encoding="utf-8") as f:
            f.write(baslik + "\n" + "\n".join("\t".join(str(x) for x in k) for k in parcasi) + "\n")
        yollar.append(yol)
    return yollar


def ozet_oku(yol):
    sut = ["alan_adi", "sayfa", "tip", "reklam_sayisi", "kopya_toplami", "ilk_baslangic", "son_baslangic", "urun_sluglari"]
    satirlar = []
    with open(yol, encoding="utf-8") as f:
        for s in f:
            if s.startswith("#") or not s.strip():
                continue
            h = s.rstrip("\n").split("\t")
            h += [""] * (len(sut) - len(h))
            satirlar.append(dict(zip(sut, h[:len(sut)])))
    if not satirlar:
        raise o.VeriHatasi("özet boş: %s" % yol)
    return satirlar


def sentetik(ozet, boz):
    kartlar, kod = [], 900000000000000
    en_cok = max(range(len(ozet)), key=lambda i: int(ozet[i]["reklam_sayisi"]))
    for i, r in enumerate(ozet):
        R, K = int(r["reklam_sayisi"]), int(r["kopya_toplami"])
        if R == 1 and r["ilk_baslangic"] != r["son_baslangic"]:
            raise o.VeriHatasi("tutarsız özet satırı: %s (1 reklam, iki farklı tarih)" % r["alan_adi"])
        sluglar = [x for x in r["urun_sluglari"].split(",") if x] or [""]
        for j in range(R):
            if boz and i == en_cok and j == R - 1:
                continue
            kod += 1
            tarih = r["son_baslangic"] if j == R - 1 else r["ilk_baslangic"]
            kopya = 1 + (K - R if j == 0 else 0)
            if r["tip"] == "SHOPIFY":
                hedef = "https://%s/products/%s?utm_source=facebook&utm_medium=paid" % (r["alan_adi"], sluglar[j % len(sluglar)])
            else:
                hedef = "https://%s/?fbclid=x" % r["alan_adi"]
            link = "https://l.facebook.com/l.php?u=" + urllib.parse.quote(hedef, safe="") + "&h=AT0x"
            kartlar.append([str(kod), r["sayfa"] or "-", tr_tarih(tarih),
                            ("%d reklam bu kreatifi ve metni kullanıyor" % kopya) if kopya > 1 else "",
                            "1", link, "Şimdi Alışveriş Yap", "video", "Kapıda ödeme ile hemen sipariş ver"])
    return kartlar, ozet[en_cok]


def calistir(ozet_yolu, boz):
    ozet = ozet_oku(ozet_yolu)
    kok = tempfile.mkdtemp(prefix="geri-test-")
    okuma = "2026-11-07"
    env = dict(os.environ, REKLAMAVI_SIMDI=okuma + "T10:00:00")
    o.yaz(kok, "arama", [
        {"tarih": okuma, "saat": "09:59:00", "ulke": "TR", "nis": "-", "aile": "KONTROL", "sorgu": "trendyol",
         "siralama": "gosterim", "kart": "30", "durum": "TAMAM", "ham_dosya": ""},
        {"tarih": okuma, "saat": "10:00:00", "ulke": "TR", "nis": "-", "aile": "S", "sorgu": "kapıda ödeme",
         "siralama": "gosterim", "kart": "", "durum": "ACIK", "ham_dosya": ""}])
    kartlar, ust = sentetik(ozet, boz)
    meta = {"ulke": "TR", "sorgu": "kapıda ödeme", "nis": "-", "aile": "S", "siralama": "gosterim", "baslangic": okuma + "T10:00"}
    yollar = ham_yaz(os.path.join(kok, "ham"), meta, kartlar, parca=2)
    p = subprocess.run([sys.executable, os.path.join(BURASI, "meta_kayit.py"), "kaydet", "--kok", kok] + yollar,
                       env=env, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stdout + p.stderr)
        return 1, kok
    birim = {b["birim"]: b for b in o.oku(kok, "birim")}
    tutmayan = []
    for r in ozet:
        b = birim.get(r["alan_adi"])
        if not b:
            tutmayan.append("%s: birim yok" % r["alan_adi"])
            continue
        beklenen = (r["reklam_sayisi"], r["kopya_toplami"], r["ilk_baslangic"], r["son_baslangic"], r["tip"], r["sayfa"] or "-")
        bulunan = (b["reklam_sayisi"], b["kopya_toplami"], b["ilk_baslangic"], b["son_baslangic"], b["tip"], b["sayfa_adi"])
        if beklenen != bulunan:
            tutmayan.append("%s: beklenen %s bulunan %s" % (r["alan_adi"], beklenen, bulunan))
    bu = birim.get(ust["alan_adi"], {})
    print("en çok reklamlı satır: %s · beklenen %s aktif / %s kopya · bulunan %s / %s · etiket %s" % (
        ust["alan_adi"], ust["reklam_sayisi"], ust["kopya_toplami"], bu.get("reklam_sayisi"), bu.get("kopya_toplami"), bu.get("etiket")))
    print("özet satırı %d · tutan %d · tutmayan %d · birim toplamı %d" % (len(ozet), len(ozet) - len(tutmayan), len(tutmayan), len(birim)))
    for t in tutmayan[:10]:
        print("  TUTMADI " + t)
    return (1 if tutmayan else 0), kok


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ozet")
    ap.add_argument("--boz", action="store_true")
    a = ap.parse_args()
    try:
        kod, _ = calistir(a.ozet, a.boz)
    except o.VeriHatasi as e:
        o.hata_cik(str(e))
    sys.exit(kod)
