#!/usr/bin/env python3
"""juri.py kırma testi (sentetik veri; model çağrısı, ffmpeg ve internet gerekmez; Pillow gerekir).

Kullanım: python3 juri_test.py  → hepsi geçerse 0. Her kural önce geçen girdide, sonra kırılmış girdide ölçülür.
"""
import json
import os
import subprocess
import sys
import tempfile

BURASI = os.path.dirname(os.path.abspath(__file__))
JURI = os.path.join(BURASI, "juri.py")
SONUC = []
ALAN = ["dururdum", "anlasilir", "gercek", "yazi", "ritim", "gonderirdim"]


def kos(*a):
    r = subprocess.run([sys.executable, JURI] + list(a), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def bekle(ad, sonuc, kod, icermeli=(), icermemeli=()):
    k, c = sonuc
    ok = k == kod and all(x in c for x in icermeli) and not any(x in c for x in icermemeli)
    SONUC.append((ad, ok))
    if not ok:
        print("--- %s (çıkış %s, beklenen %s)\n%s" % (ad, k, kod, c))


def gorsel(yol, renk):
    from PIL import Image
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    Image.new("RGB", (216, 384), renk).save(yol)
    return yol


def kopya(dizin, no, puan, sira, yapay=()):
    """puan: {kod: sayı} (bütün alanlara aynı sayı + alan sırasına göre küçük oynama)."""
    d = {"puanlar": {k: {al: max(0, min(10, v - (i % 2))) for i, al in enumerate(ALAN)} for k, v in puan.items()},
         "sira": sira, "yapay": list(yapay)}
    with open(os.path.join(dizin, "KOR-%d.json" % no), "w", encoding="utf-8") as f:
        json.dump(d, f)


def temizle(dizin):
    for f in os.listdir(dizin):
        if f.startswith("KOR-"):
            os.remove(os.path.join(dizin, f))


def bizim_kodu(dizin):
    es = json.load(open(os.path.join(dizin, "_esleme.json"), encoding="utf-8"))
    return next(k for k, o in es["ogeler"].items() if o["tur"] == "bizim"), sorted(es["ogeler"]), es


def main():
    kok = tempfile.mkdtemp(prefix="juri_test_")
    os.makedirs(os.path.join(kok, ".ekip"))
    biz = gorsel(os.path.join(kok, "g", "biz.png"), (200, 40, 40))
    refs = [gorsel(os.path.join(kok, "g", "r%d.png" % i), (40, 40 * i, 200)) for i in range(1, 4)]
    p = os.path.join(kok, "tur-1")
    ref_arg = [x for r in refs for x in ("--referans", r)]
    bekle("pano: referanssız -> 1 (kör jüri değildir)", kos("pano", "--cikti", p, "--mod", "teslim", "--bizim", "V01=" + biz), 1, ["en az 3 gerekli"])
    bekle("pano: 2 referans -> 1", kos("pano", "--cikti", p, "--mod", "teslim", "--bizim", "V01=" + biz, *ref_arg[:4]), 1)
    bekle("pano: 3 referans -> 0", kos("pano", "--cikti", p, "--mod", "teslim", "--bizim", "V01=" + biz, *ref_arg, "--tohum", "7"), 0, ["4 öge, 3 referans"])
    b, kodlar, es = bizim_kodu(p)
    brief = open(os.path.join(p, "BRIEF.md"), encoding="utf-8").read()
    SONUC.append(("pano: brif ve pano dosya adları kimliği ele vermiyor",
                  "V01" not in brief and "biz" not in brief and sorted(os.listdir(os.path.join(p, "pano"))) == [k + ".jpg" for k in kodlar]))
    oteki = [k for k in kodlar if k != b]
    kayit = os.path.join(kok, "juri.jsonl")

    # bizim video en iyi → GEÇER
    for n in (1, 2, 3):
        kopya(p, n, {b: 9, oteki[0]: 8, oteki[1]: 7, oteki[2]: 5}, [b] + oteki)
    bekle("birlestir: 3 kopya, bizim üstte -> 0 GEÇTİ", kos("birlestir", p, "--kayit", kayit, "--proje", kok), 0, ["GEÇTİ V01", "kalibrasyon: ölçülmedi", "hüküm DENEME"])
    r = json.loads(open(kayit, encoding="utf-8").read().splitlines()[-1])
    SONUC.append(("birlestir: kayıt satırı (gecti, mod, medyan, kalibrasyon) yazıldı",
                  r["gecti"] is True and r["mod"] == "teslim" and r["kopya"] == 3 and r["kalibrasyon"]["durum"] == "ölçülmedi" and set(r["medyan"]) == set(ALAN)))
    # kırma: 2 kopya
    os.remove(os.path.join(p, "KOR-3.json"))
    bekle("kırma: 2 kopya -> 1 (tek/iki kopya hüküm değil)", kos("birlestir", p), 1, ["en az 3 bağımsız kopya"])
    # kırma: bizim sonuncu
    temizle(p)
    for n in (1, 2, 3):
        kopya(p, n, {b: 7, oteki[0]: 10, oteki[1]: 9, oteki[2]: 8}, oteki + [b])
    bekle("kırma: bizim bütün referansların gerisinde -> 1", kos("birlestir", p, "--kayit", kayit), 1, ["KALDI V01", "hepsinin gerisinde"])
    # kırma: toplam düşük
    temizle(p)
    for n in (1, 2, 3):
        kopya(p, n, {b: 6, oteki[0]: 10, oteki[1]: 5, oteki[2]: 4}, [oteki[0], b, oteki[1], oteki[2]])
    bekle("kırma: toplam < 7 -> 1", kos("birlestir", p), 1, ["KALDI V01", "toplam"])
    # medyan: bir kopya sapsa da hüküm değişmez
    temizle(p)
    kopya(p, 1, {b: 9, oteki[0]: 8, oteki[1]: 7, oteki[2]: 5}, [b] + oteki)
    kopya(p, 2, {b: 9, oteki[0]: 8, oteki[1]: 7, oteki[2]: 5}, [b] + oteki)
    kopya(p, 3, {b: 3, oteki[0]: 10, oteki[1]: 9, oteki[2]: 8}, oteki + [b])
    bekle("medyan: bir kopya düşük verse de 2/3 çoğunluk -> 0, 'jüri bölündü' yazılır", kos("birlestir", p), 0, ["GEÇTİ V01", "jüri bölündü"])
    # kırma: ayırt etmeyen kopya geçersiz
    temizle(p)
    kopya(p, 1, {b: 9, oteki[0]: 8, oteki[1]: 7, oteki[2]: 5}, [b] + oteki)
    kopya(p, 2, {b: 9, oteki[0]: 8, oteki[1]: 7, oteki[2]: 5}, [b] + oteki)
    kopya(p, 3, {k: 7 for k in kodlar}, [b] + oteki)
    bekle("kırma: bütün ögelere aynı puanı veren kopya geçersiz -> 1", kos("birlestir", p), 1, ["ayırt etmiyor", "GEÇERSİZ KOPYA"])
    # kırma: eksik sıra / eksik öge
    temizle(p)
    for n in (1, 2, 3):
        kopya(p, n, {b: 9, oteki[0]: 8, oteki[1]: 7, oteki[2]: 5}, [b] + oteki[:2])
    bekle("kırma: sıralama eksik -> 1", kos("birlestir", p), 1, ["sıra bütün ögelerin"])

    # kalibrasyon: performansı bilinen 10 gerçek video (sentetik sayılar)
    tsv = os.path.join(kok, "kal.tsv")
    with open(tsv, "w", encoding="utf-8") as f:
        f.write("kimlik\tyol\tizlenme\ttakipci\tpaylasim\tkaydetme\n")
        for i in range(10):
            gorsel(os.path.join(kok, "g", "k%d.png" % i), (i * 20, 100, 100))
            f.write("vid%d\tg/k%d.png\t%d\t1000\t%d\t%d\n" % (i, i, (i + 1) * 100000, (i + 1) * 900, (i + 1) * 300))
    kd = os.path.join(kok, "kal")
    bekle("pano kalibrasyon: 10 öge -> 0", kos("pano", "--cikti", kd, "--mod", "kalibrasyon", "--tsv", tsv, "--tohum", "3"), 0)
    es = json.load(open(os.path.join(kd, "_esleme.json"), encoding="utf-8"))
    kodlar = sorted(es["ogeler"])
    perf = {k: int(es["ogeler"][k]["ad"][3:]) for k in kodlar}                # 0..9, büyük = iyi performans
    iyi_sira = sorted(kodlar, key=lambda k: -perf[k])

    def jurile(puan_fn, sira, sabit_alan=None):
        temizle(kd)
        for n in (1, 2, 3):
            d = {"puanlar": {k: {al: (7 if al == sabit_alan else puan_fn(k)) for al in ALAN} for k in kodlar}, "sira": sira, "yapay": []}
            json.dump(d, open(os.path.join(kd, "KOR-%d.json" % n), "w"))
    jurile(lambda k: 1 + perf[k], iyi_sira)
    bekle("kalibrasyon: performansla aynı sıralayan jüri -> 0 UYUMLU (ρ = 1)", kos("kalibrasyon", kd, "--proje", kok), 0, ["ρ = 1.0", "UYUMLU", "n = 10"])
    kal = [json.loads(s) for s in open(os.path.join(kok, ".ekip", "juri-kalibrasyon.jsonl"), encoding="utf-8")]
    SONUC.append(("kalibrasyon: .ekip/juri-kalibrasyon.jsonl'a yazıldı", kal[-1]["hukum"] == "UYUMLU" and kal[-1]["n"] == 10))
    jurile(lambda k: 10 - perf[k], iyi_sira[::-1])
    bekle("kırma: performansın tersini sıralayan jüri -> 1 UYUMSUZ", kos("kalibrasyon", kd, "--proje", kok), 1, ["UYUMSUZ", "performansı öngörmüyor"])
    jurile(lambda k: 1 + perf[k], iyi_sira, sabit_alan="dururdum")
    bekle("kırma: hep 7 verilen alan 'ayırt etmiyor' diye işaretlenir", kos("kalibrasyon", kd, "--proje", kok), 0, ["| dururdum | 0.00 | 7–7 |", "ayırt etmiyor"])
    # son kalibrasyon hükmün yanına yazılır
    temizle(p)
    b, kodlar4, _ = bizim_kodu(p)
    ot = [k for k in kodlar4 if k != b]
    for n in (1, 2, 3):
        kopya(p, n, {b: 9, ot[0]: 8, ot[1]: 7, ot[2]: 5}, [b] + ot)
    bekle("birlestir: son kalibrasyon UYUMLU ise hüküm DENEME notu basılmaz", kos("birlestir", p, "--proje", kok), 0, ["kalibrasyon: UYUMLU"], ["hüküm DENEME"])
    # veri yetersiz: 5 öge
    tsv2 = os.path.join(kok, "kal2.tsv")
    with open(tsv2, "w", encoding="utf-8") as f:
        f.write("kimlik\tyol\tizlenme\ttakipci\n" + "".join("vid%d\tg/k%d.png\t%d\t1000\n" % (i, i, (i + 1) * 1000) for i in range(5)))
    kd2 = os.path.join(kok, "kal2")
    kos("pano", "--cikti", kd2, "--mod", "kalibrasyon", "--tsv", tsv2)
    es2 = json.load(open(os.path.join(kd2, "_esleme.json"), encoding="utf-8")); k2 = sorted(es2["ogeler"])
    for n in (1, 2, 3):
        json.dump({"puanlar": {k: {al: 1 + int(es2["ogeler"][k]["ad"][3:]) for al in ALAN} for k in k2},
                   "sira": sorted(k2, key=lambda k: -int(es2["ogeler"][k]["ad"][3:])), "yapay": []}, open(os.path.join(kd2, "KOR-%d.json" % n), "w"))
    bekle("kırma: n = 5 -> 3 VERİ YETERSİZ (ρ = 1 olsa da hüküm yok)", kos("kalibrasyon", kd2), 3, ["VERİ YETERSİZ", "hüküm değildir"])
    # performans verisi olmayan set: uydurulmaz
    tsv3 = os.path.join(kok, "kal3.tsv")
    with open(tsv3, "w", encoding="utf-8") as f:
        f.write("kimlik\tyol\n" + "".join("vid%d\tg/k%d.png\n" % (i, i) for i in range(8)))
    kd3 = os.path.join(kok, "kal3")
    kos("pano", "--cikti", kd3, "--mod", "kalibrasyon", "--tsv", tsv3)
    es3 = json.load(open(os.path.join(kd3, "_esleme.json"), encoding="utf-8")); k3 = sorted(es3["ogeler"])
    for n in (1, 2, 3):
        json.dump({"puanlar": {k: {al: 3 + i for al in ALAN} for i, k in enumerate(k3)}, "sira": k3[::-1], "yapay": []}, open(os.path.join(kd3, "KOR-%d.json" % n), "w"))
    bekle("kırma: performans ölçütü olmayan set -> 3 (uydurulmaz)", kos("kalibrasyon", kd3), 3, ["VERİ YETERSİZ", "uydurulmaz"])
    # ayırt edicilik: eski puan kaydı
    pj = os.path.join(kok, "puanlar.jsonl")
    with open(pj, "w", encoding="utf-8") as f:
        for i in range(10):
            f.write(json.dumps({"puanlar": {"kanca": 6 + (i % 2), "ritim": 3 + i % 6}}) + "\n")
    bekle("ayirt: dar aralıklı alan işaretlenir, geniş olan işaretlenmez", kos("ayirt", pj), 0, ["| kanca | 10 | 6.50 | 0.50 | 6–7 | ayırt etmiyor |", "| ritim |"])
    bekle("ayirt: veri yoksa 'veri yok' (3)", kos("ayirt", os.path.join(kok, "yok.jsonl")), 3, ["veri yok"])
    bekle("set: veritabanı yoksa VERİ YOK (3)", kos("set", "--analiz-db", os.path.join(kok, "yok.db"), "--cikti", kok), 3, ["VERİ YOK"])

    for ad, ok in SONUC:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    kalan = sum(1 for _, ok in SONUC if not ok)
    print("klasör:", kok)
    print("TOPLAM: %d test, %d kaldı" % (len(SONUC), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
