#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arayüz sözleşmesi testi + uçtan uca kuru deneme (görsel/video üretmeden, geçici klasörde).

  python3 docs/sozlesme_test.py        # çıkış 0 = hepsi geçti

Zincir: ürün bulundu -> paket.py urun-yaz -> urun-paketi.json -> (Mağaza Kurucu; burada örnek magaza-paketi.json)
        -> paket.py magaza-oku -> marka-kilidi.md -> paket.py video-yaz -> video-paketi.json -> zincir doğrulaması.
Kırma testleri: bozuk girdi çıkış 1 vermeli ve dosya yazılmamalı.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORTAK = os.path.join(KOK, "plugins", "viral-urun-ekibi", "ortak")
PAKET = os.path.join(ORTAK, "paket.py")
SOZ = os.path.join(ORTAK, "sozlesme")
sonuc = []


def kos(*arg):
    r = subprocess.run([sys.executable] + list(arg), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout + r.stderr


def test(ad, kosul, ayrinti=""):
    sonuc.append((ad, bool(kosul)))
    print("%s  %s%s" % ("GEÇTİ" if kosul else "KALDI", ad, "" if kosul else "\n      " + ayrinti.strip().replace("\n", "\n      ")))


def oku(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    # 1) Kopya güncel mi (OZET.json; yan klasörde Mağaza Kurucu deposu varsa bayt bayt)
    kod, cikti = kos(os.path.join(KOK, "docs", "sozlesme_esitle.py"), "--kontrol")
    test("sözleşme kopyası kaynağıyla aynı", kod == 0, cikti)

    # 2) Örnekler ve örnek zincir
    for tur in ("urun", "magaza", "video"):
        kod, cikti = kos(os.path.join(SOZ, "paket_dogrula.py"), tur, os.path.join(SOZ, "ornek", "%s-paketi.json" % tur))
        test("örnek %s-paketi.json geçerli" % tur, kod == 0, cikti)
    kod, cikti = kos(os.path.join(SOZ, "paket_dogrula.py"), "zincir",
                     *[os.path.join(SOZ, "ornek", "%s-paketi.json" % t) for t in ("urun", "magaza", "video")])
    test("örnek zincir geçerli", kod == 0, cikti)

    gecici = tempfile.mkdtemp(prefix="sozlesme-test-")
    try:
        urun_klasor = os.path.join(gecici, "is", "01-ornek-urun")
        teslim = os.path.join(urun_klasor, "teslim")
        os.makedirs(teslim)
        ornek_urun = json.loads(oku(os.path.join(SOZ, "ornek", "urun-paketi.json")))

        # 3) urun-yaz: örnek ürünün alanlarından aynı dosya çıkmalı
        u, p = ornek_urun["urun"], ornek_urun["pazar"]
        arg = [PAKET, "urun-yaz", "--cikti", os.path.join(urun_klasor, "urun-paketi.json"), "--ad", u["ad"],
               "--ulke", p["ulke"], "--dil", p["dil"], "--para", p["para"], "--nis", u["nis"],
               "--tedarik", "%s %s" % (u["tedarik_fiyati"]["tutar"], u["tedarik_fiyati"]["para"])]
        for f in u["fotograflar"]:
            arg += ["--foto", f]
        for o in u["ozellikler"]:
            arg += ["--ozellik", "|".join([o["ad"], str(o["deger"]), o.get("birim", ""), o.get("kaynak", "")])]
        for v in u["varyantlar"]:
            arg += ["--varyant", "%s|%s" % (v["ad"], "var" if v["stok"] else "yok")]
        for r in ornek_urun["rakipler"]:
            arg += ["--rakip", "|".join([r["marka"], r["url"], str(r["fiyat"])])]
        for k in ornek_urun["kanit"]:
            arg += ["--kanit", "|".join([k["kaynak"], k["url"], k["tarih"], k["olcu"]])]
        kod, cikti = kos(*arg)
        yazilan = os.path.join(urun_klasor, "urun-paketi.json")
        test("urun-yaz çıkış 0 ve dosya yazıldı", kod == 0 and os.path.isfile(yazilan), cikti)
        test("urun-yaz çıktısı örnekle aynı içerik", os.path.isfile(yazilan) and json.loads(oku(yazilan)) == ornek_urun,
             oku(yazilan) if os.path.isfile(yazilan) else "dosya yok")

        # 4) Kırma: zorunlu/biçim hatası -> çıkış 1, dosya yok
        bozuk = os.path.join(gecici, "bozuk.json")
        kod, cikti = kos(PAKET, "urun-yaz", "--cikti", bozuk, "--ad", "x", "--foto", "a.jpg", "--ulke", "Türkiye")
        test("kırma: ülke kodu yanlış -> çıkış 1, dosya yazılmadı", kod == 1 and not os.path.exists(bozuk), cikti)
        kod, cikti = kos(PAKET, "urun-yaz", "--cikti", bozuk, "--ad", "x", "--foto", "a.jpg", "--ulke", "TR", "--nis", "gadget")
        test("kırma: niş biçimi yanlış -> çıkış 1, dosya yazılmadı", kod == 1 and not os.path.exists(bozuk), cikti)
        kod, cikti = kos(PAKET, "urun-yaz", "--cikti", bozuk, "--ad", "x", "--foto", "a.jpg", "--ulke", "TR", "--tedarik", "dokuz dolar")
        test("kırma: tedarik fiyatı biçimi -> çıkış != 0, dosya yazılmadı", kod != 0 and not os.path.exists(bozuk), cikti)

        # 5) Mağaza Kurucu'nun çıktısı (örnek) -> magaza-oku -> marka kilidi
        magaza = os.path.join(urun_klasor, "magaza-paketi.json")
        shutil.copyfile(os.path.join(SOZ, "ornek", "magaza-paketi.json"), magaza)
        kod, cikti = kos(PAKET, "magaza-oku", magaza)
        kilit = os.path.join(urun_klasor, "marka-kilidi.md")
        test("magaza-oku çıkış 0 ve marka-kilidi.md yazıldı", kod == 0 and os.path.isfile(kilit), cikti)
        m = json.loads(oku(magaza))
        metin = oku(kilit) if os.path.isfile(kilit) else ""
        beklenen = ([m["marka"]["ad"], m["tipografi"]["baslik"]["aile"], m["magaza"]["pdp_url"] + "?" + m["magaza"]["utm"]]
                    + list(m["renkler"].values()) + m["onayli_metinler"]["faydalar"]
                    + [g["dosya"] for g in m["gorseller"] if g["kod"] == "G0"])
        eksik = [b for b in beklenen if b not in metin]
        test("marka kilidi: marka, yazı, 5 renk, link+utm, faydalar, G0 birebir", not eksik, "eksik: %r" % eksik)

        bozuk_m = dict(m, renkler=dict(m["renkler"], vurgu="altın"))
        bozuk_yol = os.path.join(gecici, "magaza-bozuk.json")
        with open(bozuk_yol, "w", encoding="utf-8") as f:
            json.dump(bozuk_m, f, ensure_ascii=False)
        kod, cikti = kos(PAKET, "magaza-oku", bozuk_yol, "--cikti", os.path.join(gecici, "kilit-bozuk.md"))
        test("kırma: bozuk renk -> çıkış 1, kilit yazılmadı",
             kod == 1 and not os.path.exists(os.path.join(gecici, "kilit-bozuk.md")), cikti)

        # 6) video-yaz (video üretmeden: ölçüm elle verilir) -> video-paketi.json + zincir
        kod, cikti = kos(PAKET, "video-yaz", teslim, "--olcum", "V01.mp4=1080x1920:12.4", "--olcum", "V02.mp4=1080x1920:9.8",
                         "--pdp", "V02", "--dil", "tr")
        vp = os.path.join(teslim, "video-paketi.json")
        test("video-yaz çıkış 0, zincir kontrolü yapıldı", kod == 0 and os.path.isfile(vp) and "yüklenecek video: V02.mp4" in cikti, cikti)
        test("video-yaz çıktısı örnekle aynı içerik",
             os.path.isfile(vp) and json.loads(oku(vp)) == json.loads(oku(os.path.join(SOZ, "ornek", "video-paketi.json"))),
             oku(vp) if os.path.isfile(vp) else "dosya yok")
        kod, cikti = kos(os.path.join(SOZ, "paket_dogrula.py"), "zincir", yazilan, magaza, vp)
        test("uçtan uca: üretilen 3 dosya zincirden geçti", kod == 0, cikti)

        os.remove(vp)
        kod, cikti = kos(PAKET, "video-yaz", teslim, "--olcum", "V01.mp4=1080x1920:12.4", "--pdp", "V09")
        test("kırma: olmayan video --pdp -> çıkış != 0, dosya yazılmadı", kod != 0 and not os.path.exists(vp), cikti)
        m2 = dict(m, urun=dict(m["urun"], para="USD"))
        with open(magaza, "w", encoding="utf-8") as f:
            json.dump(m2, f, ensure_ascii=False)
        kod, cikti = kos(PAKET, "video-yaz", teslim, "--olcum", "V01.mp4=1080x1920:12.4")
        test("kırma: para birimi uyuşmuyor -> zincir çıkış 1, dosya yazılmadı", kod == 1 and not os.path.exists(vp), cikti)
        bos = os.path.join(gecici, "bos-teslim")
        os.makedirs(bos)
        kod, cikti = kos(PAKET, "video-yaz", bos)
        test("kırma: boş teslim klasörü -> çıkış 1", kod == 1, cikti)
    finally:
        shutil.rmtree(gecici, ignore_errors=True)

    gecen = sum(1 for _, ok in sonuc if ok)
    print("SONUÇ: %d/%d test geçti" % (gecen, len(sonuc)))
    return 0 if gecen == len(sonuc) else 1


if __name__ == "__main__":
    sys.exit(main())
