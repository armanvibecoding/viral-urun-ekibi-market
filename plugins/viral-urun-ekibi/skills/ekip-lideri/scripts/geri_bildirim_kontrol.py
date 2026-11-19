#!/usr/bin/env python3
"""Geri bildirim defteri kapısı (.ekip/GERI-BILDIRIM.md) — teslimden ÖNCE koşulur.

Kullanım: python3 geri_bildirim_kontrol.py .ekip/GERI-BILDIRIM.md [--eklenti <eklenti kökü>]
Satır biçimi (tablo, şablon: referans/hafiza-sablonlari.md):
  | # | Tarih | Kaynak | Anahtar | Geri bildirim / kusur | İşlenen dosya:bölüm | Durum | Bildirildi |
Durum: AÇIK · İŞLENDİ · TEKRAR-DÜZELTİLDİ · REDDEDİLDİ (gerekçe "Geri bildirim" sütununda).
Kapı (çıkış 1, hepsi listelenir):
  - AÇIK satır var (geri bildirim/KALICI reçete henüz eklentiye işlenmedi).
  - İŞLENDİ/TEKRAR-DÜZELTİLDİ satırında dosya yok ya da dosya diskte yok (eklenti kökü ya da proje köküne göre).
  - İŞLENDİ satırı kurucuya bildirilmemiş (Bildirildi ≠ evet).
  - Aynı Anahtar ikinci kez görülmüş ama son satır TEKRAR-DÜZELTİLDİ değil ya da dosyası üretici dosya
    (agents/ ya da skills/) değil — tekrar eden kusur üreticinin talimatı yerinde düzeltilmeden kapanmaz.
  - Kural terfisi iki basamak (ortak/kurallar.md URE-02): anahtarın İLK satırında işlenen dosya eklenti dosyasıysa
    (agents/, skills/, ortak/, hooks/) "tek örnekten eklenti kuralı" — ilk örnek ürün kontratına (is/NN/kurgu/KURALLAR.md)
    ya da .ekip/DERSLER.md'ye yazılır; eklentiye ancak ikinci örnekte (TEKRAR-DÜZELTİLDİ) girer.
Çıkış 0 = temiz. Dosya yoksa bu betik çıkış 0 ve "defter yok" basar; geçiş kapısı kapi.py defter yokluğunu KALDI sayar.
"""
import argparse
import os
import sys


EKLENTI_KLASORLERI = ("agents/", "skills/", "ortak/", "hooks/")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("defter")
    ap.add_argument("--eklenti", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
    a = ap.parse_args()
    if not os.path.exists(a.defter):
        print(f"defter yok: {a.defter} (şablon: skills/ekip-lideri/referans/hafiza-sablonlari.md)")
        return 0
    proje = os.path.dirname(os.path.dirname(os.path.abspath(a.defter)))
    satirlar = []
    with open(a.defter, encoding="utf-8") as f:
        for no, s in enumerate(f, 1):
            h = [x.strip() for x in s.strip().strip("|").split("|")]
            if len(h) < 8 or not h[0].isdigit():
                continue
            satirlar.append({"no": no, "id": h[0], "anahtar": h[3].lower(), "metin": h[4], "dosya": h[5],
                             "durum": h[6].upper(), "bildirildi": h[7].lower()})
    hatalar = []
    for r in satirlar:
        d = r["durum"]
        if d.startswith("AÇIK") or d.startswith("ACIK"):
            hatalar.append(f"satır {r['no']} #{r['id']} AÇIK: {r['metin']}")
            continue
        if d.startswith("REDDED"):
            continue
        yol = r["dosya"].split(":", 1)[0].strip().strip("`")
        if not yol or yol in ("—", "-"):
            hatalar.append(f"satır {r['no']} #{r['id']} {d}: işlenen dosya yok")
        elif not any(os.path.exists(os.path.join(k, yol)) for k in (a.eklenti, proje)):
            hatalar.append(f"satır {r['no']} #{r['id']}: dosya diskte yok: {yol}")
        if not r["bildirildi"].startswith("evet"):
            hatalar.append(f"satır {r['no']} #{r['id']}: kurucuya bildirilmedi (Bildirildi = evet olmalı)")
    gorulen = {}
    for r in satirlar:
        gorulen.setdefault(r["anahtar"], []).append(r)
    for k, rr in gorulen.items():
        ilk = rr[0]
        yol = ilk["dosya"].split(":", 1)[0].strip().strip("`")
        if k and not ilk["durum"].startswith(("REDDED", "AÇIK", "ACIK")) and yol.startswith(EKLENTI_KLASORLERI):
            hatalar.append(f"satır {ilk['no']} #{ilk['id']} anahtar '{k}': tek örnekten eklenti kuralı ({yol}). İlk örnek ürün "
                           f"kontratına (is/NN/kurgu/KURALLAR.md) ya da .ekip/DERSLER.md'ye yazılır; eklentiye ikinci örnekte terfi eder")
    for k, rr in gorulen.items():
        if k and len(rr) >= 2:
            son = rr[-1]
            yol = son["dosya"].split(":", 1)[0].strip().strip("`")
            if not son["durum"].startswith("TEKRAR") or not yol.startswith(("agents/", "skills/")):
                hatalar.append(f"anahtar '{k}' {len(rr)}. kez (satır {son['no']}): son satır TEKRAR-DÜZELTİLDİ olmalı "
                               f"ve üretici dosyayı (agents/ ya da skills/) göstermeli — şu an: {son['durum']} · {yol or 'dosya yok'}")
    acik = sum(1 for r in satirlar if r["durum"].startswith(("AÇIK", "ACIK")))
    print(f"defter: {len(satirlar)} satır · açık {acik} · hata {len(hatalar)}")
    for h in hatalar:
        print("  ✗ " + h)
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
