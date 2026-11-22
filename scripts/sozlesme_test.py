#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arayüz sözleşmesi testi + uçtan uca kuru deneme (görsel/video üretmeden, geçici klasörde).

  python3 scripts/sozlesme_test.py        # çıkış 0 = hepsi geçti

Zincir: ürün bulundu -> paket.py urun-yaz -> urun-paketi.json -> (Mağaza Kurucu; burada örnek magaza-paketi.json)
        -> paket.py magaza-oku -> marka-kilidi.md -> paket.py video-yaz -> video-paketi.json -> zincir doğrulaması.
Kırma testleri: bozuk girdi çıkış 1 vermeli ve dosya yazılmamalı.
Ek bölüm (birleşmede yerel köprüden taşındı): sürüm 2 (teklif, tema_modu), fiyatın tek kaynağı (teklif.tsv > sabit kural),
niş eşlemesi, marj/kanıt dosyasından okuma, iddia kapısı (paket.py + kurgu_kontrol.py), video-sec, belge tablosu = şema.
"""
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORTAK = os.path.join(KOK, "plugins", "viral-urun-ekibi", "ortak")
PAKET = os.path.join(ORTAK, "paket.py")
SOZ = os.path.join(ORTAK, "sozlesme")
EKLENTI = os.path.dirname(ORTAK)
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


def yaz(klasor, ad, veri):
    y = os.path.join(klasor, ad)
    with open(y, "w", encoding="utf-8") as f:
        f.write(veri if isinstance(veri, str) else json.dumps(veri, ensure_ascii=False))
    return y


def teklif_satir(baslik, **k):
    v = {"tur": "bizim", "tarih": "2026-11-17", "pazar": "US", "urun": "katlanır kedi rampası", "kaynak_url": "-", "para": "USD",
         "fiyat": "39.99", "karsilastirma_fiyati": "yok", "karsilastirma_kaniti": "yok", "paket": "1x;2x:-15%",
         "garanti": "30 gün para iadesi", "kargo_vaadi": "ücretsiz, 5-8 iş günü", "odeme_yontemleri": "kart;shop_pay",
         "sosyal_kanit_turu": "alici_foto", "aciliyet": "yok", "itiraz_yanitlari": "kargo süresi?; iade?",
         "upsell": "2x paket", "ilk_ekran": "mekanizma videosu", "not": "-"}
    v.update(k)
    return "\t".join(v[c] for c in baslik.strip().split("\t")) + "\n"


def yerel_testler(k):
    """Birleşmede yerel köprüden (eski plugins/viral-urun-ekibi/sozlesme/kirma_testi.py) taşınan kapılar."""
    dog = os.path.join(SOZ, "paket_dogrula.py")
    u = json.loads(oku(os.path.join(SOZ, "ornek", "urun-paketi.json")))
    m = json.loads(oku(os.path.join(SOZ, "ornek", "magaza-paketi.json")))
    v2 = dict(copy.deepcopy(u), surum="2", teklif={"kaynak": "sabit-kural", "paketler": [{"adet": 2, "indirim_yuzde": 10}]})
    kod, c = kos(dog, "urun", yaz(k, "u-v2.json", v2))
    test("sürüm 2 + teklif geçerli", kod == 0, c)
    kod, c = kos(dog, "urun", yaz(k, "u-v1t.json", dict(v2, surum="1")))
    test("kırma: sürüm 1 + teklif -> çıkış 1", kod == 1 and "surum 2 ile geldi" in c, c)
    b = copy.deepcopy(v2); b["teklif"]["kaynak"] = "tahmin"
    kod, c = kos(dog, "urun", yaz(k, "u-tk.json", b))
    test("kırma: teklif.kaynak geçersiz -> çıkış 1", kod == 1, c)
    b = copy.deepcopy(u); b["urun"]["fotograflar"] = []
    kod, c = kos(dog, "urun", yaz(k, "u-foto.json", b))
    test("kırma: fotoğraf yok -> çıkış 1", kod == 1, c)
    b = copy.deepcopy(m); b["surum"] = "2"; b["magaza"]["tema_modu"] = "temasiz"
    kod, c = kos(dog, "magaza", yaz(k, "m-tm.json", b))
    test("sürüm 2 + tema_modu temasiz geçerli", kod == 0, c)
    b["magaza"]["tema_modu"] = "yarim"
    kod, c = kos(dog, "magaza", yaz(k, "m-tm2.json", b))
    test("kırma: tema_modu geçersiz -> çıkış 1", kod == 1, c)
    b["magaza"]["tema_modu"] = "tam"; b["surum"] = "1"
    kod, c = kos(dog, "magaza", yaz(k, "m-tm3.json", b))
    test("kırma: sürüm 1 + tema_modu -> çıkış 1", kod == 1 and "surum 2 ile geldi" in c, c)
    b = copy.deepcopy(m); del b["onayli_metinler"]["iddialar"]
    kod, c = kos(PAKET, "dogrula", "magaza", yaz(k, "m-id.json", b))
    test("kırma: paket.py dogrula iddialar silindi -> çıkış 1", kod == 1 and "iddialar" in c, c)

    # urun-yaz: ekibin dosyalarından paket; fiyatın TEK kaynağı
    tb = oku(os.path.join(EKLENTI, "skills", "teklif-ve-sayfa", "sablon", "teklif.tsv"))
    mb = oku(os.path.join(EKLENTI, "skills", "aliexpress-firsat", "sablon", "marj.csv"))
    rakip = teklif_satir(tb, tur="rakip", kaynak_url="https://www.ornek-magaza.example/products/rampa", fiyat="44.95")
    teklif = yaz(k, "teklif.tsv", tb + rakip + teklif_satir(tb))
    marj = yaz(k, "marj.csv", mb.rstrip("\n") + "\nkatlanır kedi rampası,US,USD,39.99,11.40,4.2,0,-,0,2.9,0.3,5,6,8,ornek\n")
    kanit = yaz(k, "kanit.md", "# 01 kedi rampası\nTarih: 2026-11-10\n- Meta reklam: https://reklam-kutuphanesi.example/ads/123 aktif 94 gün\n"
                               "- Rakip: https://www.ornek-magaza.example/products/rampa 44,95 USD\n- https://yalniz-url.example/x\n")
    cikti = os.path.join(k, "is", "magaza", "urun-paketi.json")
    ortak = ["urun-yaz", "--cikti", cikti, "--ad", "katlanır kedi rampası", "--nis-kodu", "evcil", "--foto", "tedarikci-1.jpg",
             "--marj-csv", marj, "--kanit-md", kanit, "--ozellik", "uzunluk|120|cm|https://tedarikci.example/item/1001"]
    kod, c = kos(PAKET, *ortak, "--pazar", "ABD", "--teklif-tsv", teklif)
    test("urun-yaz (bizim satırı var) -> çıkış 0, sürüm 2", kod == 0 and "teklif kaynağı: teklif.tsv" in c and "rakip 1" in c and "kanıt 2" in c, c)
    p = json.loads(oku(cikti)) if os.path.isfile(cikti) else {}
    tamam = (p.get("surum") == "2" and p.get("teklif") == {
        "kaynak": "teklif.tsv", "fiyat": 39.99, "para": "USD", "paketler": [{"adet": 1, "indirim_yuzde": 0}, {"adet": 2, "indirim_yuzde": 15}],
        "garanti": "30 gün para iadesi", "kargo_vaadi": "ücretsiz, 5-8 iş günü"}
        and p["urun"]["nis"] == "nis-pet" and p["pazar"] == {"ulke": "US", "dil": "en", "para": "USD"}
        and p["urun"]["tedarik_fiyati"] == {"tutar": 11.4, "para": "USD"}
        and p["rakipler"][0] == {"marka": "ornek-magaza.example", "url": "https://www.ornek-magaza.example/products/rampa", "fiyat": 44.95}
        and p["kanit"][0]["tarih"] == "2026-11-10" and all(x.get("olcu") for x in p["kanit"]))
    test("urun-yaz içeriği birebir (fiyat, paket, niş, pazar, tedarik, rakip, kanıt; ölçüsüz URL alınmaz)", tamam, json.dumps(p, ensure_ascii=False))
    teklif2 = yaz(k, "teklif2.tsv", tb + rakip)
    kod, c = kos(PAKET, *ortak, "--pazar", "US", "--teklif-tsv", teklif2)
    p = json.loads(oku(cikti)) if os.path.isfile(cikti) else {}
    test("bizim satırı yok -> sabit kural: 2'li %10, 3'lü %18, fiyat yazılmaz",
         kod == 0 and p.get("teklif") == {"kaynak": "sabit-kural", "paketler": [{"adet": 1, "indirim_yuzde": 0},
                                                                              {"adet": 2, "indirim_yuzde": 10}, {"adet": 3, "indirim_yuzde": 18}]}, c)
    kod, c = kos(PAKET, "fiyat", "--teklif-tsv", teklif, "--pazar", "DE")
    test("fiyat: başka pazarın bizim satırı sayılmaz", kod == 0 and "sabit-kural" in c, c)
    kod, c = kos(PAKET, *ortak[:5], "--nis-kodu", "bilinmez", "--foto", "a.jpg", "--pazar", "US")
    test("niş kodu tabloda yok -> nis-gadget + UYARI", kod == 0 and "nis-gadget yazıldı" in c, c)
    os.remove(cikti)
    kod, c = kos(PAKET, "urun-yaz", "--cikti", cikti, "--ad", "x", "--foto", "a.jpg", "--pazar", "Mars")
    test("kırma: tanınmayan pazar -> çıkış != 0, dosya yazılmadı", kod != 0 and not os.path.exists(cikti), c)

    # magaza-oku --cikti-dizin + iddia kapısı
    mp = os.path.join(SOZ, "ornek", "magaza-paketi.json")
    kd = os.path.join(k, "kurgu")
    kod, c = kos(PAKET, "magaza-oku", mp, "--cikti", os.path.join(k, "kilit.md"), "--cikti-dizin", kd)
    ayar = json.loads(oku(os.path.join(kd, "video-ayar.json"))) if os.path.isfile(os.path.join(kd, "video-ayar.json")) else {}
    test("magaza-oku --cikti-dizin: video-ayar.json mağazayla aynı yazı/renk/iddia/link",
         kod == 0 and ayar.get("renkler", {}).get("vurgu") == m["renkler"]["vurgu"]
         and ayar.get("yazi", {}).get("baslik_aile") == m["tipografi"]["baslik"]["aile"]
         and ayar.get("iddialar") == [i["metin"] for i in m["onayli_metinler"]["iddialar"]]
         and ayar.get("link", "").endswith("?" + m["magaza"]["utm"])
         and oku(os.path.join(kd, "onayli-iddialar.txt")).count("\n") == 1 + len(m["onayli_metinler"]["iddialar"]), c)
    iyi = yaz(k, "iyi.json", {"yazilar": [{"bas": 0, "bit": 2, "yazi": "Cama vantuzla tutunur, delme yok"},
                                         {"bas": 2, "bit": 4, "yazi": "15 KG'A KADAR TAŞIR"}],
                             "planlar": [{"klip": "a.mp4", "yazi": "bunu izle"}],
                             "cta": {"plan": 1, "satir1": m["urun"]["baslik"], "satir2": str(m["urun"]["fiyat"])}})
    kod, c = kos(PAKET, "iddia-kontrol", mp, iyi)
    test("iddia-kontrol: onaylı iddia + fiyat + iddiasız yazı -> 0", kod == 0 and "GEÇTİ" in c, c)
    kotu = yaz(k, "kotu.json", {"yazilar": [{"bas": 0, "bit": 2, "yazi": "30 kg taşır"}]})
    kod, c = kos(PAKET, "iddia-kontrol", mp, kotu)
    test("kırma: listede olmayan sayı iddiası -> 1", kod == 1 and "30 kg taşır" in c and "onaylı listede yok" in c, c)
    kotu2 = yaz(k, "altyazi.txt", "# altyazı\nCama vantuzla tutunur\nVeteriner onaylı, eklem ağrısını geçirir\n")
    kod, c = kos(PAKET, "iddia-kontrol", mp, kotu2)
    test("kırma: listede olmayan uydurma otorite (veteriner onaylı; metin dosyası) -> 1", kod == 1 and "altyazi.txt:3" in c, c)
    # Sağlık/sonuç dili ENGEL DEĞİL (kurucu kararı): metin geçer, bilgi notu basılır; uydurma veri yine kalır.
    NOT = "Bilgi notu (kullanıcının sorumluluğu):"
    saglik = yaz(k, "saglik.txt", "Cama vantuzla tutunur\nEklem ağrısını geçirir, duruşu iyileştirir\n")
    kod, c = kos(PAKET, "iddia-kontrol", mp, saglik)
    test("iddia-kontrol: sağlık cümlesi geçer + bilgi notu -> 0",
         kod == 0 and NOT in c and "saglik.txt:2" in c and "0 ihlal, 1 bilgi notu" in c and "GEÇTİ" in c, c)
    kod, c = kos(PAKET, "iddia-kontrol", mp, yaz(k, "temiz.txt", "Cama vantuzla tutunur\nbunu izle\n"))
    test("iddia-kontrol: sağlık dili yoksa bilgi notu basılmaz -> 0", kod == 0 and NOT not in c, c)
    karma = yaz(k, "karma.txt", "Ağrıyı geçirir\n%90 daha az ağrı\n")
    kod, c = kos(PAKET, "iddia-kontrol", mp, karma)
    test("kırma: sağlık cümlesi + uydurma istatistik -> 1 (istatistik kalır, sağlık not)",
         kod == 1 and "karma.txt:2" in c and "HATA: [iddia]" in c and NOT in c and "1 ihlal, 1 bilgi notu" in c, c)
    kotu3 = yaz(k, "fiyat.json", {"cta": {"satir1": "Şimdi 499"}})
    kod, c = kos(PAKET, "iddia-kontrol", mp, kotu3)
    test("kırma: mağazadakinden farklı fiyat -> 1", kod == 1 and "499" in c, c)
    kk = os.path.join(EKLENTI, "skills", "video-kurgu", "scripts", "kurgu_kontrol.py")
    kod, c = kos(kk, iyi, "--magaza-paketi", mp, "--yalniz-iddia")
    test("kurgu_kontrol --magaza-paketi onaylı ayar -> 0", kod == 0 and "GEÇTİ" in c, c)
    kod, c = kos(kk, kotu, "--magaza-paketi", mp, "--yalniz-iddia")
    test("kırma: kurgu_kontrol --magaza-paketi onaysız iddia -> 1", kod == 1 and "[iddia]" in c and "30 kg taşır" in c, c)
    sagj = yaz(k, "saglik.json", {"yazilar": [{"bas": 0, "bit": 2, "yazi": "Bel ağrısını geçirir"}]})
    kod, c = kos(kk, sagj, "--magaza-paketi", mp, "--yalniz-iddia")
    test("kurgu_kontrol --magaza-paketi sağlık cümlesi geçer + bilgi notu -> 0",
         kod == 0 and "[saglik-sonuc]" in c and NOT in c and "GEÇTİ" in c, c)

    # video-yaz --cikti + video-sec
    teslim = os.path.join(k, "teslim2")
    os.makedirs(teslim)
    vc = os.path.join(k, "is", "magaza", "video-paketi.json")
    kod, c = kos(PAKET, "video-yaz", teslim, "--cikti", vc, "--olcum", "V01.mp4=1080x1920:14.2",
                 "--olcum", "V02.mp4=1080x1920:12", "--pdp", "V02", "--dil", "en")
    test("video-yaz --cikti magaza/ klasörüne -> 0", kod == 0 and os.path.isfile(vc) and "mağazaya yüklenecek: 1" in c, c)
    kod, c = kos(PAKET, "video-sec", vc)
    test("video-sec yalnız pdp-galeri/hero", kod == 0 and "pdp-galeri\tV02.mp4" in c and "1 / 2" in c, c)
    b = json.loads(oku(vc)); b[0]["kullanim"] = "tiktok"
    kod, c = kos(PAKET, "video-sec", yaz(k, "v-bozuk.json", b))
    test("kırma: video kullanım geçersiz -> 1", kod == 1, c)

    # belge tablosu = şema (tek kaynak kayması)
    metin = oku(os.path.join(SOZ, "arayuz-sozlesmesi.md"))
    bolum = {"urun": metin.split("## Girdi:")[1].split("## Çıktı:")[0], "magaza": metin.split("## Çıktı:")[1].split("## Geri dönüş:")[0]}
    for tur, b in bolum.items():
        sm = json.loads(oku(os.path.join(SOZ, "%s-paketi.schema.json" % tur)))["properties"]
        anlatim = set(re.findall(r"^\| `([a-z_.]+)` \|", b, re.M))
        ust = set(sm) | ({"urun." + x for x in sm["urun"]["properties"]} if tur == "urun" else set())
        if tur == "urun":
            ust.discard("urun")
        eksik, fazla = sorted(anlatim - ust), sorted(ust - anlatim)
        test("%s-paketi: belge tablosu = şema (%d alan)" % (tur, len(anlatim)), not eksik and not fazla and len(anlatim) >= 9,
             "şemada olmayan %s · tabloda olmayan %s" % (eksik, fazla))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    # 1) Kopya güncel mi (OZET.json; yan klasörde Mağaza Kurucu deposu varsa bayt bayt)
    kod, cikti = kos(os.path.join(KOK, "scripts", "sozlesme_esitle.py"), "--kontrol")
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
        yerel_testler(gecici)
    finally:
        shutil.rmtree(gecici, ignore_errors=True)

    gecen = sum(1 for _, ok in sonuc if ok)
    print("SONUÇ: %d/%d test geçti" % (gecen, len(sonuc)))
    return 0 if gecen == len(sonuc) else 1


if __name__ == "__main__":
    sys.exit(main())
