#!/usr/bin/env python3
"""juri.py kırma testi (sentetik veri; model çağrısı, ffmpeg ve internet gerekmez; Pillow gerekir).

Kullanım: python3 juri_test.py  → hepsi geçerse 0. Her kural önce geçen girdide, sonra kırılmış girdide ölçülür.
"""
import glob
import json
import os
import shutil
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


def esleme(dizin):
    """Eşleşme jürinin dizininin DIŞINDA: <dizin>.gizli/_esleme.json (denetim 2026-11-25 #1)."""
    return json.load(open(os.path.join(os.path.normpath(dizin) + ".gizli", "_esleme.json"), encoding="utf-8"))


def kopya_ham(dizin, no, puanlar, sira, yapay=()):
    """puanlar: {öge kimliği: {alan: sayı}}; sira: [öge kimliği]. Kopya kendi klasörüne, kendi harfleriyle yazar."""
    ters = {oid: kod for kod, oid in esleme(dizin)["kopyalar"][str(no)].items()}
    d = {"puanlar": {ters[o]: v for o, v in puanlar.items()}, "sira": [ters[o] for o in sira], "yapay": [ters[o] for o in yapay]}
    kd = os.path.join(dizin, "kopya-%d" % no)
    with open(os.path.join(kd, "KOR-%d.json" % no), "w", encoding="utf-8") as f:
        json.dump(d, f)


def kopya(dizin, no, puan, sira, yapay=()):
    """puan: {öge kimliği: sayı} (bütün alanlara aynı sayı + alan sırasına göre küçük oynama)."""
    kopya_ham(dizin, no, {k: {al: max(0, min(10, v - (i % 2))) for i, al in enumerate(ALAN)} for k, v in puan.items()}, sira, yapay)


def temizle(dizin):
    for kd in glob.glob(os.path.join(dizin, "kopya-*")):
        for f in os.listdir(kd):
            if f.startswith("KOR-"):
                os.remove(os.path.join(kd, f))


def bizim_kodu(dizin):
    es = esleme(dizin)
    return next(k for k, o in es["ogeler"].items() if o["tur"] == "bizim"), sorted(es["ogeler"]), es


def ffmpeg_yolu():
    """ffmpeg klasörü: FFMPEG_DIZIN ortam değişkeni ya da PATH."""
    yol = os.environ.get("FFMPEG_DIZIN")
    if yol and os.path.exists(os.path.join(yol, "ffmpeg")):
        return yol
    w = shutil.which("ffmpeg")
    return os.path.dirname(w) if w else None


def main():
    kok = tempfile.mkdtemp(prefix="juri_test_")
    ff = ffmpeg_yolu()
    if ff:
        os.environ["PATH"] = ff + os.pathsep + os.environ["PATH"]
    os.makedirs(os.path.join(kok, ".ekip"))
    biz = gorsel(os.path.join(kok, "g", "biz.png"), (200, 40, 40))
    refs = [gorsel(os.path.join(kok, "g", "r%d.png" % i), (40, 40 * i, 200)) for i in range(1, 4)]
    p = os.path.join(kok, "tur-1")
    ref_arg = [x for r in refs for x in ("--referans", r)]
    bekle("pano: referanssız -> 1 (kör jüri değildir)", kos("pano", "--cikti", p, "--mod", "teslim", "--bizim", "V01=" + biz), 1, ["en az 3 gerekli"])
    bekle("pano: 2 referans -> 1", kos("pano", "--cikti", p, "--mod", "teslim", "--bizim", "V01=" + biz, *ref_arg[:4]), 1)
    bekle("pano: 3 referans -> 0", kos("pano", "--cikti", p, "--mod", "teslim", "--bizim", "V01=" + biz, *ref_arg, "--tohum", "7"), 0, ["4 öge, 3 referans", "eşleşme jüriden ayrı"])
    rk = os.path.join(kok, "rk")
    for i in range(1, 4):
        gorsel(os.path.join(rk, "ref%d.png" % i), (40, 40 * i, 200))
    p_rk = os.path.join(kok, "tur-rk")
    bekle("pano --referans-klasoru: 3 görsel (analiz.db yok) -> 0, 3 referans", kos("pano", "--cikti", p_rk, "--mod", "teslim", "--bizim", "V01=" + biz, "--referans-klasoru", rk, "--tohum", "7"), 0, ["4 öge, 3 referans"])
    rk2 = os.path.join(kok, "rk2")
    for i in range(1, 3):
        gorsel(os.path.join(rk2, "ref%d.png" % i), (40, 40 * i, 200))
    open(os.path.join(rk2, "not.txt"), "w").write("görsel değil")
    bekle("KIRMA --referans-klasoru: 2 referans (+ txt yok sayılır) -> 1 'en az 3'", kos("pano", "--cikti", os.path.join(kok, "tur-rk2"), "--mod", "teslim", "--bizim", "V01=" + biz, "--referans-klasoru", rk2), 1, ["en az 3 gerekli"])
    bekle("KIRMA --referans-klasoru: klasör yok -> 1", kos("pano", "--cikti", os.path.join(kok, "tur-rk3"), "--mod", "teslim", "--bizim", "V01=" + biz, "--referans-klasoru", os.path.join(kok, "yok")), 1, ["bulunamadı"])
    b, kodlar, es = bizim_kodu(p)
    # --- denetim #1: tek biçim, eşleşme ayrı dizin, kopya başına klasör ve harf sırası
    from PIL import Image
    boyutlar = {Image.open(y).size for y in glob.glob(os.path.join(p, "kopya-*", "pano", "*.jpg"))}
    SONUC.append(("pano: bütün ögeler/kopyalar tek biçimde (1080×1536, 5×4 ızgara, 20 kare)", boyutlar == {(1080, 1536)} and es["kare_sayisi"] == 20))
    SONUC.append(("pano: eşleşme jürinin okuduğu dizinde YOK (<cikti>.gizli içinde)",
                  not glob.glob(os.path.join(p, "**", "_esleme.json"), recursive=True) and os.path.exists(os.path.join(p + ".gizli", "_esleme.json"))))
    SONUC.append(("pano: kopya başına ayrı klasör (kopya-1..3, her birinde BRIEF + pano)",
                  sorted(os.path.basename(x) for x in glob.glob(os.path.join(p, "kopya-*"))) == ["kopya-1", "kopya-2", "kopya-3"]
                  and all(os.path.exists(os.path.join(p, "kopya-%d" % n, "BRIEF.md")) for n in (1, 2, 3))))
    SONUC.append(("pano: kopyaların harf sırası birbirinden farklı", len({tuple(sorted(es["kopyalar"][str(n)].items())) for n in (1, 2, 3)}) > 1))
    briefler = "".join(open(os.path.join(p, "kopya-%d" % n, "BRIEF.md"), encoding="utf-8").read() for n in (1, 2, 3))
    SONUC.append(("pano: brif ve pano dosya adları kimliği ele vermiyor",
                  "V01" not in briefler and "biz" not in briefler and all(
                      sorted(os.listdir(os.path.join(p, "kopya-%d" % n, "pano"))) == [k + ".jpg" for k in sorted(es["kopyalar"][str(n)])] for n in (1, 2, 3))))
    oteki = [k for k in kodlar if k != b]
    kayit = os.path.join(kok, "juri.jsonl")

    # bizim video en iyi → GEÇER
    for n in (1, 2, 3):
        kopya(p, n, {b: 9, oteki[0]: 8, oteki[1]: 7, oteki[2]: 5}, [b] + oteki)
    bekle("birlestir: 3 kopya, bizim üstte -> 0 GEÇTİ", kos("birlestir", p, "--kayit", kayit, "--proje", kok), 0, ["GEÇTİ V01", "kalibrasyon: ölçülmedi", "hüküm DENEME"])
    r = json.loads(open(kayit, encoding="utf-8").read().splitlines()[-1])
    SONUC.append(("birlestir: kayıt satırı (gecti, mod, medyan, kalibrasyon) yazıldı",
                  r["gecti"] is True and r["mod"] == "teslim" and r["kopya"] == 3 and r["kalibrasyon"]["durum"] == "ölçülmedi" and set(r["medyan"]) == set(ALAN)))
    # kırma: biçim farkı (bir pano başka boyutta) -> PANO GEÇERSİZ
    yol0 = sorted(glob.glob(os.path.join(p, "kopya-1", "pano", "*.jpg")))[0]
    yedek = open(yol0, "rb").read()
    Image.new("RGB", (216, 384), (9, 9, 9)).save(yol0)
    bekle("kırma: bir pano görseli farklı biçimde -> 1 PANO GEÇERSİZ", kos("birlestir", p, "--proje", kok), 1, ["PANO GEÇERSİZ"])
    open(yol0, "wb").write(yedek)
    # kırma: kopya klasörü dışına yazılan KOR dosyası sayılmaz
    shutil.copy(os.path.join(p, "kopya-1", "KOR-1.json"), os.path.join(p, "KOR-9.json"))
    os.remove(os.path.join(p, "kopya-3", "KOR-3.json"))
    bekle("kırma: kopya klasörü dışındaki KOR dosyası yok sayılır (2 kopya -> 1)", kos("birlestir", p), 1, ["en az 3 bağımsız kopya"])
    os.remove(os.path.join(p, "KOR-9.json"))
    # kırma: 2 kopya
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
    # denetim #3: dururdum/gonderirdim tabanı (toplam 8,6 ve hiçbir alan < 5: eski kural GEÇİRİRDİ)
    for ad, kusurlu in (("dururdum", "dururdum"), ("gonderirdim", "gonderirdim")):
        temizle(p)
        for n in (1, 2, 3):
            ham = {b: {al: (5.5 if al == kusurlu else 10) for al in ALAN}}
            for i, k in enumerate(oteki):
                ham[k] = {al: 7 - i for al in ALAN}
            kopya_ham(p, n, ham, [b] + oteki)
        bekle("kırma: toplam yüksek ama %s 5,5 (< 6) -> 1 KALDI taban" % ad, kos("birlestir", p), 1, ["KALDI V01", "taban < 6: " + ad], ["toplam 8"])
    temizle(p)
    for n in (1, 2, 3):
        ham = {b: {al: (6 if al in ("dururdum", "gonderirdim") else 9) for al in ALAN}}
        for i, k in enumerate(oteki):
            ham[k] = {al: 7 - i for al in ALAN}
        kopya_ham(p, n, ham, [b] + oteki)
    bekle("taban: dururdum = gonderirdim = 6 (tam eşik) -> 0 GEÇTİ", kos("birlestir", p), 0, ["GEÇTİ V01"])
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

    # denetim #1: sayaç/hesap adı sızıntısı -> PANO GEÇERSİZ (OCR gerekir; yoksa ölçülemedi diye ATLANIR, geçti sayılmaz)
    if os.path.exists(os.path.expanduser("~/.local/share/viral-urun-ekibi/ocr-venv/bin/python")):
        from PIL import ImageDraw, ImageFont
        sz = os.path.join(kok, "g", "sizinti.png")
        im = Image.new("RGB", (216, 384), (30, 30, 30))
        d = ImageDraw.Draw(im)
        try:
            f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        except OSError:
            f = ImageFont.load_default()
        d.text((10, 150), "@hesapadi", font=f, fill=(255, 255, 255))
        d.text((10, 200), "1.2M likes", font=f, fill=(255, 255, 255))
        im.save(sz)
        bekle("kırma: karede @hesap + sayaç metni kalmış -> 1 PANO GEÇERSİZ",
              kos("pano", "--cikti", os.path.join(kok, "tur-s"), "--mod", "teslim", "--bizim", "V01=" + biz,
                  "--referans", sz, "--referans", refs[0], "--referans", refs[1], "--tohum", "1"), 1, ["PANO GEÇERSİZ", "sayaç"])
    else:
        print("ATLANDI sızıntı OCR testi: OCR ortamı yok (bu kapı bu koşuda ÖLÇÜLMEDİ)")
    # video ögeleri maskelenir; maskeli ile maskesiz karışık pano geçersiz
    if ff:
        vid = os.path.join(kok, "g", "v.mp4")
        subprocess.run([os.path.join(ff, "ffmpeg"), "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc=size=270x480:rate=10:duration=4", vid], capture_output=True)
        if os.path.exists(vid):
            bekle("pano: video ögesi maskelenir ve 20 kareye normalize olur (1080×1536)",
                  kos("pano", "--cikti", os.path.join(kok, "tur-v"), "--mod", "teslim", "--bizim", "V01=" + vid,
                      "--referans", vid, "--referans", vid, "--referans", vid, "--tohum", "2"), 0)
            vb = glob.glob(os.path.join(kok, "tur-v", "kopya-1", "pano", "*.jpg"))
            im = Image.open(vb[0]).convert("RGB")
            SONUC.append(("pano: video karesinde üst %6 ve alt %20 siyah (maske)",
                          im.size == (1080, 1536) and im.getpixel((100, 10))[0] < 8 and im.getpixel((100, 360))[0] < 8 and im.getpixel((100, 200)) != (0, 0, 0)))
            bekle("kırma: bir ögesi video, ötekiler tek durağan görsel -> 1 PANO GEÇERSİZ",
                  kos("pano", "--cikti", os.path.join(kok, "tur-m"), "--mod", "teslim", "--bizim", "V01=" + vid,
                      "--referans", refs[0], "--referans", refs[1], "--referans", refs[2], "--tohum", "2"), 1, ["PANO GEÇERSİZ", "biçim farkı"])
            bekle("kırma: aynı karışım --arayuz-maske ile de geçersiz (durağan/hareketli farkı maskeyle kapanmaz) -> 1",
                  kos("pano", "--cikti", os.path.join(kok, "tur-m"), "--mod", "teslim", "--bizim", "V01=" + vid,
                      "--referans", refs[0], "--referans", refs[1], "--referans", refs[2], "--tohum", "2", "--arayuz-maske"), 1, ["biçim farkı"])
    else:
        print("ATLANDI video maske testleri: ffmpeg yok")
    # yapılamadı kaydı geçiş değildir
    i0 = os.path.join(kok, "is-y")
    os.makedirs(i0)
    bekle("yapilamadi: kayıt gecti=false yazılır (kapı KALDI sayar)", kos("yapilamadi", i0, "--video", "V01", "--referans-sayisi", "2", "--neden", "viral referans yok"), 0, ["(mağaza sahibinin) açık cümlesi"])
    SONUC.append(("yapilamadi: juri.jsonl satırı gecti=false", json.loads(open(os.path.join(i0, "elestiri", "juri.jsonl"), encoding="utf-8").read().splitlines()[-1])["gecti"] is False))

    # kalibrasyon: performansı bilinen 10 gerçek video (sentetik sayılar)
    tsv = os.path.join(kok, "kal.tsv")
    with open(tsv, "w", encoding="utf-8") as f:
        f.write("kimlik\tyol\tizlenme\ttakipci\tpaylasim\tkaydetme\n")
        for i in range(10):
            gorsel(os.path.join(kok, "g", "k%d.png" % i), (i * 20, 100, 100))
            f.write("vid%d\tg/k%d.png\t%d\t1000\t%d\t%d\n" % (i, i, (i + 1) * 100000, (i + 1) * 900, (i + 1) * 300))
    kd = os.path.join(kok, "kal")
    bekle("pano kalibrasyon: 10 öge -> 0", kos("pano", "--cikti", kd, "--mod", "kalibrasyon", "--tsv", tsv, "--tohum", "3"), 0)
    es = esleme(kd)
    kodlar = sorted(es["ogeler"])
    perf = {k: int(es["ogeler"][k]["ad"][3:]) for k in kodlar}                # 0..9, büyük = iyi performans
    iyi_sira = sorted(kodlar, key=lambda k: -perf[k])

    def jurile(puan_fn, sira, sabit_alan=None):
        temizle(kd)
        for n in (1, 2, 3):
            kopya_ham(kd, n, {k: {al: (7 if al == sabit_alan else puan_fn(k)) for al in ALAN} for k in kodlar}, sira)
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
    es2 = esleme(kd2); k2 = sorted(es2["ogeler"])
    for n in (1, 2, 3):
        kopya_ham(kd2, n, {k: {al: 1 + int(es2["ogeler"][k]["ad"][3:]) for al in ALAN} for k in k2},
                  sorted(k2, key=lambda k: -int(es2["ogeler"][k]["ad"][3:])))
    bekle("kırma: n = 5 -> 3 VERİ YETERSİZ (ρ = 1 olsa da hüküm yok)", kos("kalibrasyon", kd2), 3, ["VERİ YETERSİZ", "hüküm değildir"])
    # performans verisi olmayan set: uydurulmaz
    tsv3 = os.path.join(kok, "kal3.tsv")
    with open(tsv3, "w", encoding="utf-8") as f:
        f.write("kimlik\tyol\n" + "".join("vid%d\tg/k%d.png\n" % (i, i) for i in range(8)))
    kd3 = os.path.join(kok, "kal3")
    kos("pano", "--cikti", kd3, "--mod", "kalibrasyon", "--tsv", tsv3)
    es3 = esleme(kd3); k3 = sorted(es3["ogeler"])
    for n in (1, 2, 3):
        kopya_ham(kd3, n, {k: {al: 3 + i for al in ALAN} for i, k in enumerate(k3)}, k3[::-1])
    bekle("kırma: performans ölçütü olmayan set -> 3 (uydurulmaz)", kos("kalibrasyon", kd3), 3, ["VERİ YETERSİZ", "uydurulmaz"])
    # ayırt edicilik: eski puan kaydı
    pj = os.path.join(kok, "puanlar.jsonl")
    with open(pj, "w", encoding="utf-8") as f:
        for i in range(10):
            f.write(json.dumps({"puanlar": {"kanca": 6 + (i % 2), "ritim": 3 + i % 6}}) + "\n")
    bekle("ayirt: dar aralıklı alan işaretlenir, geniş olan işaretlenmez", kos("ayirt", pj), 0, ["| kanca | 10 | 6.50 | 0.50 | 6–7 | ayırt etmiyor |", "| ritim |"])
    bekle("ayirt: veri yoksa 'veri yok' (3)", kos("ayirt", os.path.join(kok, "yok.jsonl")), 3, ["veri yok"])
    bekle("set: veritabanı yoksa VERİ YOK (3)", kos("set", "--analiz-db", os.path.join(kok, "yok.db"), "--cikti", kok), 3, ["VERİ YOK"])

    # Rol sınavı 2026-11-25: kare sayfası pano içinde pano olmasın; düz yatay görsel bölünmesin; profil görüntüsü panoya girmesin
    from PIL import Image, ImageDraw
    sys.path.insert(0, BURA) if "BURA" in globals() else sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import juri as J
    sayfa = Image.new("RGB", (780, 554), (0, 0, 0))
    d = ImageDraw.Draw(sayfa)
    for i in range(10):
        x, y = (i % 5) * 156, (i // 5) * 277
        d.rectangle([x, y, x + 155, y + 276], fill=(30 + 20 * i, 200 - 15 * i, (90 * i) % 255))
    h = J.sayfa_bol(sayfa)
    SONUC.append(("sayfa_bol: 5×2 kare sayfası 10 hücreye bölünür", bool(h) and len(h) == 10))
    SONUC.append(("sayfa_bol: düz 1600×900 görsel bölünmez", J.sayfa_bol(Image.new("RGB", (1600, 900), (120, 80, 40))) is None))
    SONUC.append(("sayfa_bol: dikey 1080×1920 bölünmez", J.sayfa_bol(Image.new("RGB", (1080, 1920))) is None))
    kd = os.path.join(kok, "kare_profil")
    os.makedirs(kd, exist_ok=True)
    for ad in ("k01.png", "k02.png", "profil.png", "sayfa.jpg"):
        Image.new("RGB", (90, 160), (255, 0, 0) if ad.startswith(("profil", "sayfa")) else (0, 0, 255)).save(os.path.join(kd, ad))
    kk, _, _ = J.kareleri_al(kd)
    SONUC.append(("kareleri_al: profil/sayfa görüntüsü panoya girmez", all(k.getpixel((5, 5)) == (0, 0, 255) for k in kk)))

    for ad, ok in SONUC:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    kalan = sum(1 for _, ok in SONUC if not ok)
    print("klasör:", kok)
    print("TOPLAM: %d test, %d kaldı" % (len(SONUC), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
