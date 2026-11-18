#!/usr/bin/env python3
"""paket.py kırma testleri: her kapı önce GEÇERLİ girdiyle 0, sonra bozulmuş girdiyle 1 vermeli.
Kullanım: python3 kirma_testi.py -> hepsi tutarsa 0, biri tutmazsa 1."""
import copy
import json
import os
import subprocess
import sys
import tempfile

BURASI = os.path.dirname(os.path.abspath(__file__))
BETIK = os.path.join(BURASI, "paket.py")
ORNEK = os.path.join(BURASI, "ornek")
TEKLIF_BASLIK = open(os.path.join(BURASI, "..", "skills", "teklif-ve-sayfa", "sablon", "teklif.tsv"), encoding="utf-8").read()
MARJ_BASLIK = open(os.path.join(BURASI, "..", "skills", "aliexpress-firsat", "sablon", "marj.csv"), encoding="utf-8").read()
SONUC = []


def kos(*args):
    p = subprocess.run([sys.executable, BETIK] + list(args), capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def bekle(ad, sonuc, kod, icermeli=()):
    gelen, c = sonuc
    tamam = gelen == kod and all(x in c for x in icermeli)
    SONUC.append((ad, tamam, gelen, kod))
    if not tamam:
        print("--- %s:\n%s" % (ad, c))


def ornek(ad):
    return json.load(open(os.path.join(ORNEK, ad), encoding="utf-8"))


def yaz(k, ad, veri):
    y = os.path.join(k, ad)
    with open(y, "w", encoding="utf-8") as f:
        if isinstance(veri, str):
            f.write(veri)
        else:
            json.dump(veri, f, ensure_ascii=False)
    return y


def teklif_satir(**k):
    v = {"tur": "bizim", "tarih": "2026-11-17", "pazar": "US", "urun": "katlanır kedi rampası", "kaynak_url": "-", "para": "USD",
         "fiyat": "39.99", "karsilastirma_fiyati": "yok", "karsilastirma_kaniti": "yok", "paket": "1x;2x:-15%",
         "garanti": "30 gün para iadesi", "kargo_vaadi": "ücretsiz, 5-8 iş günü", "odeme_yontemleri": "kart;shop_pay",
         "sosyal_kanit_turu": "alici_foto", "aciliyet": "yok", "itiraz_yanitlari": "kargo süresi?; iade?",
         "upsell": "2x paket", "ilk_ekran": "mekanizma videosu", "not": "-"}
    v.update(k)
    return "\t".join(v[c] for c in TEKLIF_BASLIK.strip().split("\t")) + "\n"


def main():
    with tempfile.TemporaryDirectory() as k:
        # --- 1) şema: örnekler geçer, bozulanlar kalır ---
        for t in ("urun", "magaza", "video"):
            bekle("ornek %s-paketi -> 0" % t, kos("dogrula", t, os.path.join(ORNEK, t + "-paketi.json")), 0, ["GEÇERLİ"])
        u = ornek("urun-paketi.json")
        b = copy.deepcopy(u); del b["urun"]["ad"]
        bekle("urun.ad silindi -> 1", kos("dogrula", "urun", yaz(k, "u1.json", b)), 1, ["urun.ad: zorunlu alan eksik"])
        b = copy.deepcopy(u); del b["pazar"]
        bekle("pazar silindi -> 1", kos("dogrula", "urun", yaz(k, "u2.json", b)), 1, ["pazar: zorunlu alan eksik"])
        b = copy.deepcopy(u); b["pazar"]["ulke"] = "ABD"
        bekle("pazar ISO değil -> 1", kos("dogrula", "urun", yaz(k, "u3.json", b)), 1, ["biçime uymuyor"])
        b = copy.deepcopy(u); b["urun"]["uydurma_alan"] = "x"
        bekle("sözleşme dışı alan -> 1", kos("dogrula", "urun", yaz(k, "u4.json", b)), 1, ["sözleşme dışı alan"])
        b = copy.deepcopy(u); b["surum"] = "1"
        bekle("surum 1 + teklif alanı -> 1", kos("dogrula", "urun", yaz(k, "u5.json", b)), 1, ["surum 2 ile geldi"])
        b = copy.deepcopy(u); b["surum"] = "1"; del b["teklif"]
        bekle("surum 1 (teklifsiz, eski biçim) -> 0", kos("dogrula", "urun", yaz(k, "u6.json", b)), 0)
        b = copy.deepcopy(u); b["urun"]["fotograflar"] = []
        bekle("fotoğraf yok -> 1", kos("dogrula", "urun", yaz(k, "u7.json", b)), 1, ["en az 1"])
        m = ornek("magaza-paketi.json")
        b = copy.deepcopy(m); del b["onayli_metinler"]["iddialar"]
        bekle("iddialar silindi -> 1", kos("dogrula", "magaza", yaz(k, "m1.json", b)), 1, ["iddialar: zorunlu alan eksik"])
        b = copy.deepcopy(m); b["renkler"]["vurgu"] = "sarı"
        bekle("renk HEX değil -> 1", kos("dogrula", "magaza", yaz(k, "m2.json", b)), 1, ["renkler.vurgu"])
        b = copy.deepcopy(m); del b["tipografi"]["baslik"]["aile"]
        bekle("başlık ailesi silindi -> 1", kos("dogrula", "magaza", yaz(k, "m3.json", b)), 1, ["baslik.aile"])
        b = copy.deepcopy(m); b["magaza"]["tema_modu"] = "yarim"
        bekle("tema_modu geçersiz -> 1", kos("dogrula", "magaza", yaz(k, "m4.json", b)), 1, ["tema_modu"])
        v = ornek("video-paketi.json")
        b = copy.deepcopy(v); b[0]["kullanim"] = "tiktok"
        bekle("video kullanım geçersiz -> 1", kos("dogrula", "video", yaz(k, "v1.json", b)), 1, ["kullanim"])
        b = copy.deepcopy(v); del b[1]["sure_sn"]
        bekle("video süresi silindi -> 1", kos("dogrula", "video", yaz(k, "v2.json", b)), 1, ["sure_sn"])
        bekle("bozuk JSON -> 1", kos("dogrula", "urun", yaz(k, "bozuk.json", "{")), 1, ["JSON bozuk"])

        # --- 2) urun-yaz: A'nın dosyalarından paket; fiyatın TEK kaynağı ---
        rakip = teklif_satir(tur="rakip", kaynak_url="https://www.ornek-magaza.example/products/rampa", fiyat="44.95")
        teklif = yaz(k, "teklif.tsv", TEKLIF_BASLIK + rakip + teklif_satir())
        marj = yaz(k, "marj.csv", MARJ_BASLIK.rstrip("\n") + "\nkatlanır kedi rampası,US,USD,39.99,11.40,4.2,0,-,0,2.9,0.3,5,6,8,ornek\n")
        kanit = yaz(k, "kanit.md", "# 01 kedi rampası\nTarih: 2026-11-10\n- Meta reklam: https://reklam-kutuphanesi.example/ads/123 aktif 94 gün\n- Rakip: https://www.ornek-magaza.example/products/rampa 44,95 USD\n")
        cikti = os.path.join(k, "is", "urun-paketi.json")
        ortak = ["urun-yaz", "--cikti", cikti, "--ad", "katlanır kedi rampası", "--nis", "evcil", "--foto", "tedarikci-1.jpg",
                 "--marj-csv", marj, "--kanit-md", kanit, "--ozellik", "uzunluk=120|cm|https://tedarikci.example/item/1001"]
        bekle("urun-yaz (bizim satırı var) -> 0", kos(*ortak, "--pazar", "ABD", "--teklif-tsv", teklif), 0, ["teklif kaynağı: teklif.tsv", "rakip 1", "kanıt 2"])
        p = json.load(open(cikti, encoding="utf-8"))
        tamam = (p["teklif"] == {"kaynak": "teklif.tsv", "fiyat": 39.99, "para": "USD",
                                 "paketler": [{"adet": 1, "indirim_yuzde": 0}, {"adet": 2, "indirim_yuzde": 15}],
                                 "garanti": "30 gün para iadesi", "kargo_vaadi": "ücretsiz, 5-8 iş günü"}
                 and p["urun"]["nis"] == "nis-pet" and p["pazar"] == {"ulke": "US", "dil": "en", "para": "USD"}
                 and p["urun"]["tedarik_fiyati"] == {"tutar": 11.4, "para": "USD"}
                 and p["rakipler"][0] == {"marka": "ornek-magaza.example", "url": "https://www.ornek-magaza.example/products/rampa", "fiyat": 44.95}
                 and p["kanit"][0]["tarih"] == "2026-11-10")
        SONUC.append(("urun-yaz içeriği birebir (fiyat, paket, niş, pazar, tedarik, rakip, kanıt)", tamam, int(not tamam), 0))
        bekle("yazılan paket şemadan geçer -> 0", kos("dogrula", "urun", cikti), 0)
        teklif2 = yaz(k, "teklif2.tsv", TEKLIF_BASLIK + rakip)
        bekle("urun-yaz (bizim satırı YOK) -> sabit kural", kos(*ortak, "--pazar", "US", "--teklif-tsv", teklif2), 0, ["teklif kaynağı: sabit-kural"])
        p = json.load(open(cikti, encoding="utf-8"))
        tamam = p["teklif"] == {"kaynak": "sabit-kural", "paketler": [{"adet": 1, "indirim_yuzde": 0}, {"adet": 2, "indirim_yuzde": 10}, {"adet": 3, "indirim_yuzde": 18}]}
        SONUC.append(("sabit kural: 2'li %10, 3'lü %18, fiyat yazılmaz", tamam, int(not tamam), 0))
        bekle("fiyat komutu: başka pazarın bizim satırı sayılmaz", kos("fiyat", "--teklif-tsv", teklif, "--pazar", "DE"), 0, ["sabit-kural"])
        os.remove(cikti)
        bekle("urun-yaz fotoğrafsız -> 1, dosya yazılmaz", kos("urun-yaz", "--cikti", cikti, "--ad", "x", "--nis", "evcil", "--pazar", "US"), 1, ["YAZILMADI"])
        SONUC.append(("fotoğrafsız çağrıda dosya oluşmadı", not os.path.exists(cikti), int(os.path.exists(cikti)), 0))

        # --- 3) magaza-oku + iddia kapısı ---
        mp = os.path.join(ORNEK, "magaza-paketi.json")
        bekle("magaza-oku -> 0 + dosyalar", kos("magaza-oku", mp, "--cikti-dizin", os.path.join(k, "kurgu")), 0, ["Barlow Condensed", "patika-urun-0.jpg", "utm_source=instagram"])
        ayar = json.load(open(os.path.join(k, "kurgu", "video-ayar.json"), encoding="utf-8"))
        tamam = (ayar["renkler"]["vurgu"] == "#E0B04A" and ayar["yazi"]["baslik_aile"] == "Barlow Condensed"
                 and ayar["iddialar"] == ["120 cm uzunluk", "40 kg'a kadar taşır"]
                 and ayar["link"].endswith("?utm_source=instagram&utm_medium=video&utm_campaign=patika-rampa"))
        SONUC.append(("video-ayar.json mağazayla aynı yazı/renk/iddia/link", tamam, int(not tamam), 0))
        b = copy.deepcopy(m); del b["renkler"]
        bekle("magaza-oku eksik renk -> 1", kos("magaza-oku", yaz(k, "m5.json", b)), 1, ["renkler: zorunlu alan eksik"])
        iyi = yaz(k, "iyi.json", {"yazilar": [{"bas": 0, "bit": 2, "yazi": "Koltuğa zıplamadan çıkar"}, {"bas": 2, "bit": 4, "yazi": "40 KG'A KADAR TAŞIR"}],
                                   "planlar": [{"klip": "a.mp4", "yazi": "bunu izle"}], "cta": {"plan": 1, "satir1": "Patika Katlanır Kedi Rampası", "satir2": "39.99"}})
        bekle("onaylı iddia + fiyat + iddiasız yazı -> 0", kos("iddia-kontrol", mp, iyi), 0, ["GEÇTİ"])
        kotu = yaz(k, "kotu.json", {"yazilar": [{"bas": 0, "bit": 2, "yazi": "80 kg taşır"}]})
        bekle("listede olmayan sayı iddiası -> 1", kos("iddia-kontrol", mp, kotu), 1, ["80 kg taşır", "onaylı listede yok"])
        kotu2 = yaz(k, "altyazi.txt", "# altyazı\nKoltuğa zıplamadan çıkar\nVeteriner onaylı, eklem ağrısını geçirir\n")
        bekle("listede olmayan sonuç iddiası (metin dosyası) -> 1", kos("iddia-kontrol", mp, kotu2), 1, ["altyazi.txt:3"])
        kotu3 = yaz(k, "fiyat.json", {"cta": {"satir1": "Şimdi 19.99"}})
        bekle("mağazadakinden farklı fiyat -> 1", kos("iddia-kontrol", mp, kotu3), 1, ["19.99"])

        # kurgu ön-kontrol kapısı aynı kuralı kullanır (video-kurgu/scripts/kurgu_kontrol.py --magaza-paketi)
        kk = os.path.join(BURASI, "..", "skills", "video-kurgu", "scripts", "kurgu_kontrol.py")
        for ad, dosya, kod, icer in (("kurgu_kontrol --magaza-paketi onaylı ayar -> 0", iyi, 0, ["GEÇTİ"]),
                                     ("kurgu_kontrol --magaza-paketi onaysız iddia -> 1", kotu, 1, ["[iddia]", "80 kg taşır"])):
            r = subprocess.run([sys.executable, kk, dosya, "--magaza-paketi", mp, "--yalniz-iddia"], capture_output=True, text=True)
            bekle(ad, (r.returncode, r.stdout + r.stderr), kod, icer)

        # --- 4) video-yaz / video-sec ---
        vc = os.path.join(k, "video-paketi.json")
        bekle("video-yaz (elle ölçü) -> 0", kos("video-yaz", "--cikti", vc, "--video", "V01.mp4:reklam:en:1080x1920:14.2",
                                                 "--video", "V02.mp4:pdp-galeri:yok:1080x1920:12"), 0, ["mağazaya yüklenecek: 1"])
        bekle("video-sec yalnız pdp-galeri/hero", kos("video-sec", vc), 0, ["pdp-galeri\tV02.mp4", "1 / 2"])
        os.remove(vc)
        bekle("video-yaz geçersiz kullanım -> 1, dosya yazılmaz", kos("video-yaz", "--cikti", vc, "--video", "V01.mp4:tiktok:en:1080x1920:14.2"), 1, ["YAZILMADI"])
        SONUC.append(("geçersiz kullanımda dosya oluşmadı", not os.path.exists(vc), int(os.path.exists(vc)), 0))
        bekle("video-yaz ölçülemeyen dosya -> 1", kos("video-yaz", "--cikti", vc, "--video", os.path.join(k, "yok.mp4") + ":hero"), 1, ["okunamadı"])

    # --- 5) anlatım (arayuz-sozlesmesi.md) ile şema aynı alanları söylüyor mu (tek kaynak kayması) ---
    import re
    sema = json.load(open(os.path.join(BURASI, "sema.json"), encoding="utf-8"))
    sozlesme = os.path.join(BURASI, "..", "skills", "magaza-kurucu", "urun-analiz", "references", "arayuz-sozlesmesi.md")
    metin = open(sozlesme, encoding="utf-8").read()
    bolum = {"urun-paketi": metin.split("## Girdi:")[1].split("## Çıktı:")[0], "magaza-paketi": metin.split("## Çıktı:")[1].split("## Geri dönüş:")[0]}

    def var(s, yol):
        for parca in yol.split("."):
            s = s.get("alanlar", {}).get(parca)
            if s is None:
                return False
        return True
    for tur, b in bolum.items():
        anlatim = set(re.findall(r"^\| `([a-z_.]+)` \|", b, re.M))
        eksik = sorted(a for a in anlatim if not var(sema[tur], a))
        ust = set(sema[tur]["alanlar"]) | {"urun." + k for k in sema[tur]["alanlar"].get("urun", {}).get("alanlar", {})} if tur == "urun-paketi" else set(sema[tur]["alanlar"])
        anlatilmayan = sorted(a for a in ust if a not in anlatim and a != "urun")
        tamam = not eksik and not anlatilmayan and len(anlatim) >= 9
        SONUC.append(("%s: sözleşme tablosu = şema (%d alan)" % (tur, len(anlatim)), tamam, int(not tamam), 0))
        if not tamam:
            print("--- %s: şemada olmayan %s · tabloda olmayan %s" % (tur, eksik, anlatilmayan))

    kalan = [s for s in SONUC if not s[1]]
    for ad, tamam, gelen, kod in SONUC:
        print("%s  %s" % ("GEÇTİ" if tamam else "KALDI", ad))
    print("TOPLAM: %d test, %d kaldı" % (len(SONUC), len(kalan)))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
