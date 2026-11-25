#!/usr/bin/env python3
"""senaryo_kontrol.py kırma testi (ağsız, ffmpeg'siz). Çıkış 0 = hepsi geçti.
Geçerli küçük senaryo → 0; her kural bozulunca çıkış ≠ 0 (ya da UYARI satırı) olmalı."""
import copy
import json
import os
import subprocess
import sys
import tempfile

B = os.path.dirname(os.path.abspath(__file__))
KONTROL = os.path.join(B, "senaryo_kontrol.py")
sonuc = []


def t(ad, ok):
    sonuc.append(bool(ok))
    print(("GEÇTİ " if ok else "KALDI ") + ad)


def video(no, kanca, soru, eylemler):
    return {"no": no, "mekanizma": "M%d" % no, "sablon": "S%d" % (no + 1), "an": "an %d farklı bir an" % no, "kanca": kanca, "aile": "K%d" % no,
            "kimlik": False, "giris": "giriş %d" % no, "ortam": "ortam %d" % no, "ozne": "özne %d" % no,
            "sahneler": [{"eylem": e} for e in eylemler], "etkilesim_sahne": 2, "sonuc_sahne": 2, "cta": "Yorumlara PİYANO yaz",
            "neden": "neden %d" % no, "kanca_sorusu": soru, "cevap_an": 10, "kanca_onceki": "eski " + kanca}


IYI = {"urun": "Test ürünü", "pazar": "TR", "marka": "Kedibahçe",
       "videolar": [
           video(1, "Kedi tüyü tek hamlede çıkar mı?", "Tüy tek hamlede çıkar mı?", ["Fırça halıya değer", "Tüy fırçaya toplanır", "Fırça temiz kalır"]),
           video(2, "Bu leke silinir mi?", "Leke silinir mi?", ["Kahve döküldü yazısı", "Bez lekeye gider", "Leke yok olur sonuç"]),
           video(3, "Su mu kahve mi yağ mı?", "Yağ da çıkar mı?", ["Su damlar kumaşa", "Kahve damlar kumaşa", "Yağ damlar silinir"]),
           video(4, "Hangisi önce kurudu?", "Hangisi kurudu?", ["İki havlu ıslanır", "Biri üründe asılır", "Ürünlü havlu kurur"]),
       ]}


def kos(d):
    with tempfile.TemporaryDirectory() as k:
        yol = os.path.join(k, "senaryolar.json")
        with open(yol, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
        r = subprocess.run([sys.executable, KONTROL, yol], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr


def boz(f):
    d = copy.deepcopy(IYI)
    f(d)
    return d


rc, o = kos(IYI)
t("geçerli senaryo çıkış 0", rc == 0)
if rc:
    print(o)

# R4: markayla / biz / we / our / yeni koleksiyon ile başlayan kanca
for ad, kanca in (("marka adı", "Kedibahçe fırçası tüyü çıkarır mı?"), ("BİZ", "Biz yeni fırçayı çıkardık"), ("bizim", "Bizim fırça tüyü alır"),
                  ("we", "We made a brush"), ("our", "Our new brush"), ("yeni koleksiyon", "Yeni koleksiyon geldi"), ("new collection", "New collection is here")):
    rc, o = kos(boz(lambda d, kanca=kanca: d["videolar"][0].__setitem__("kanca", kanca)))
    t("R4 kırma: %s ile başlayan kanca → çıkış ≠ 0" % ad, rc != 0 and "R4" in o)
rc, o = kos(boz(lambda d: d["videolar"][0].__setitem__("kanca", "Kedinin tüyü Kedibahçe ile gider mi?")))
t("R4 ortada geçen marka adı serbest", rc == 0)

# A: kanca_sorusu / cevap_an zorunlu, aralık UYARI
rc, o = kos(boz(lambda d: d["videolar"][1].pop("kanca_sorusu")))
t("A kırma: kanca_sorusu yok → çıkış ≠ 0", rc != 0 and "kanca_sorusu" in o)
rc, o = kos(boz(lambda d: d["videolar"][1].pop("cevap_an")))
t("A kırma: cevap_an yok → çıkış ≠ 0", rc != 0 and "cevap_an" in o)
rc, o = kos(boz(lambda d: d["videolar"][1].__setitem__("cevap_an", 2)))
t("A: cevap_an süre×0,4'ten önce → UYARI (çıkış 0)", rc == 0 and "UYARI" in o and "cevap_an" in o)
rc, o = kos(boz(lambda d: d["videolar"][1].__setitem__("cevap_an", 13)))
t("A: cevap_an süreden sonra → UYARI", rc == 0 and "UYARI" in o and "cevap_an" in o)
rc, o = kos(boz(lambda d: d["videolar"][1].__setitem__("sure", 30)))
t("A: sure alanı sahne×4'e baskın (10 sn < 30×0,4 → UYARI)", rc == 0 and "cevap_an" in o and "UYARI" in o)

# B: soru zinciri
rc, o = kos(boz(lambda d: d["videolar"][2].__setitem__("zincir", ["Su?", "Kahve?", "Yağ?"])))
t("B kırma: 12 sn videoda 3 halka → çıkış ≠ 0", rc != 0 and "zincir" in o)
rc, o = kos(boz(lambda d: d["videolar"][2].__setitem__("zincir", ["Su?", "Kahve?"])))
t("B: 2 halka serbest", rc == 0)
rc, o = kos(boz(lambda d: d["videolar"][2].update({"sure": 30, "zincir": ["a?", "b?", "c?"], "cevap_an": 20})))
t("B: 30 sn hikâyede 3 halka serbest", rc == 0)

# C: sıkılaştırma
rc, o = kos(boz(lambda d: d["videolar"][0].pop("kanca_onceki")))
t("C: kanca_onceki yok → UYARI", rc == 0 and "kanca_onceki" in o)
rc, o = kos(boz(lambda d: d["videolar"][3].__setitem__("kanca", "Hangisi 10 saniyede kurudu?")))
t("C: kancada sayı + sayi_kaniti yok → UYARI", rc == 0 and "sayi_kaniti" in o)

sys.exit(0 if all(sonuc) else 1)
