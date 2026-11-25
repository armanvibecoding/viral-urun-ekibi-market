#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""copy_kontrol.py + beklenen_uret.py kırma testleri. Kullanım: python3 copy_kontrol_test.py → 0 hepsi geçerse, 1 biri tutmazsa.
Her kapı önce bozuk girdiyle ≠ 0 (kırma), sonra doğru girdiyle 0 görülür; beklenen_uret çıktısı elle yazılmış doğru beklenen dosyalarla bayt bayt aynı olmalı."""
import os
import subprocess
import sys
import tempfile

B = os.path.dirname(os.path.abspath(__file__))
CK, BU = os.path.join(B, "copy_kontrol.py"), os.path.join(B, "beklenen_uret.py")
sonuc = []


def kos(betik, *a):
    r = subprocess.run([sys.executable, betik] + list(a), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def bekle(ad, rc, beklenen, cikti, parca=None):
    ok = rc == beklenen and (parca is None or parca in cikti)
    sonuc.append(ok)
    print("%s %s → çıkış %d (beklenen %d)%s" % ("GEÇTİ" if ok else "KALDI", ad, rc, beklenen, "" if ok else "\n    " + cikti.strip()[-400:].replace("\n", "\n    ")))


def yaz(y, m):
    with open(y, "w", encoding="utf-8") as f:
        f.write(m)
    return y


def main():
    with tempfile.TemporaryDirectory() as k:
        kilit = yaz(os.path.join(k, "URUN-KILIDI.md"), "Bitiş kenarı çelik, ağız yuvarlak. Seramik kupa, 350 ml. Sıcak sıvı. Desen belirir, dökünce. Başlık bir kısa.\n")
        def m(metin, pazar="TR", *ek):
            return kos(CK, yaz(os.path.join(k, "METINLER.md"), metin), "--pazar", pazar, "--bilgi", kilit, *ek)
        rc, c = m("- galeri-1: SICAK SIVI DÖKÜNCE DESEN BELİRİR | alt satır: Seramik · 350 ml\n")
        bekle("doğru metin (TR)", rc, 0, c, "GEÇTİ")
        rc, c = m("- galeri-1: BU BAŞLIK ÇOK UZUN VE BEŞ KELİMEYİ AŞIYOR\n")
        bekle("başlık 8 kelime", rc, 1, c, "başlık 8 kelime")
        rc, c = m("### G1\n| alan | önerilen metin |\n|---|---|\n| etiket | ÇOK UZUN KART ETİKETİ |\n")
        bekle("etiket 21 karakter", rc, 1, c, "etiketi 21 karakter")
        rc, c = m("- galeri-2: KISA BAŞLIK | alt satır: bir iki üç dört beş altı yedi sekiz dokuz on onbir oniki onüç\n")
        bekle("açıklama 13 kelime", rc, 1, c, "açıklama 13 kelime")
        rc, c = m("- galeri-3: BAŞLIK BİR | alt satır: " + " ".join(["kelime"] * 12) + " | etiket: kart | buton: " + " ".join(["a"] * 30) + "\n")
        bekle("kare toplamı > 40 kelime", rc, 1, c, "kare toplamı")
        rc, c = m("- galeri-1: SICAK SIVI — DESEN\n")
        bekle("uzun tire", rc, 1, c, "uzun tire")
        rc, c = m("- galeri-1: SICAK SIVI!\n")
        bekle("ünlem", rc, 1, c, "ünlem")
        rc, c = m("- galeri-1: SICAK SIVI | alt satır: Seramik, 7.5 cm\n")
        bekle("TR ondalık nokta", rc, 1, c, "ondalık nokta")
        rc, c = m("- galeri-1: SICAK SIVi DÖKÜNCE\n")
        bekle("büyük harfli satırda küçük i (naif upper izi)", rc, 1, c, "küçük harf kalmış")
        rc, c = m("- galeri-1: BITIŞ KENARI ÇELIK\n")
        bekle("BITIŞ ↔ bilgi 'Bitiş': İ/I yanlış", rc, 1, c, "doğrulanmış bilgiye göre 'BİTİŞ'")
        rc, c = m("- galeri-1: BİTİŞ KENARI ÇELİK\n")
        bekle("BİTİŞ doğru (bilgiyle eşleşir)", rc, 0, c, "GEÇTİ")
        rc, c = m("- galeri-1: KUPA | alt satır: seramİk kupa\n")
        bekle("küçük harfli kelimede ortada büyük İ", rc, 1, c, "ortada büyük")
        rc, c = m("- galeri-1: BİLİNMEYEN KELİME\n")
        bekle("bilgide olmayan büyük harfli İ/I'li kelime: ölçülemedi (3), geçti değil", rc, 3, c, "ÖLÇÜLEMEYEN")
        rc, c = m("- galeri-1: THIS IS WRONG, NOT RIGHT\n", "US")
        bekle("US pazarında TR kuralları (İ/I, değil) uygulanmaz", rc, 0, c, "GEÇTİ")
        rc, c = m("# boş dosya\nyazı yok burada\n")
        bekle("yazı bulunamadı", rc, 2, c, "yazı bulunamadı")
        # beklenen_uret: elle yazılmış doğru dosyalarla bayt bayt aynı
        md = yaz(os.path.join(k, "M2.md"), "# METINLER\n- g0-feed: (yazı yok)\n- galeri-2: SICAK SIVI DÖKÜNCE DESEN BELİRİR\n- b1-masaustu, b2-mobil: SICAK SIVI DÖKÜNCE / DESEN BELİRİR | alt satır: Seramik · 350 ml\n")
        out = os.path.join(k, "g")
        rc, c = kos(BU, md, "--cikti", out)
        bekle("beklenen_uret yazdı", rc, 0, c, "4 beklenen")
        elle = {"g0-feed.txt": "", "galeri-2.txt": "SICAK SIVI DÖKÜNCE DESEN BELİRİR\n", "b1-masaustu.txt": "SICAK SIVI DÖKÜNCE\nDESEN BELİRİR\nSeramik · 350 ml\n",
                "b2-mobil.txt": "SICAK SIVI DÖKÜNCE\nDESEN BELİRİR\nSeramik · 350 ml\n"}
        farkli = [a for a, v in elle.items() if not os.path.isfile(os.path.join(out, a)) or open(os.path.join(out, a), encoding="utf-8").read() != v]
        sonuc.append(not farkli)
        print("%s beklenen_uret çıktısı = elle yazılmış beklenen dosyalar %s" % ("GEÇTİ" if not farkli else "KALDI", farkli or ""))
        yaz(md, "- galeri-1: A\n- galeri-1: B\n")
        rc, c = kos(BU, md, "--cikti", os.path.join(k, "g2"))
        bekle("beklenen_uret: aynı ad iki slotta", rc, 1, c, "aynı ad")
    kalan = sonuc.count(False)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
