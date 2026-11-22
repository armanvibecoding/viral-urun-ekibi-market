#!/usr/bin/env python3
"""Kör video jürisi: pano hazırlar, 3 bağımsız kopyanın puanını birleştirir, jüriyi GERÇEK PERFORMANSA karşı sınar.

"En iyi" kurucunun beğenisinden değil ölçülmüş performanstan öğrenilir: referanslar gerçekten izlenmiş viral videolardır,
jürinin değeri de "sıralaması gerçek performans sıralamasıyla ne kadar uyuşuyor" sorusuyla ölçülür (geriye dönük test).

  juri.py pano --cikti is/NN/juri/tur-1 --mod teslim|onuretim --bizim V03=is/NN/kurgu/V03.mp4 --referans R1 --referans R2 --referans R3
  juri.py pano --cikti is/kalibrasyon/set-1 --mod kalibrasyon --tsv kalibrasyon.tsv
  juri.py birlestir is/NN/juri/tur-1 --kayit is/NN/elestiri/juri.jsonl --tur 1 [--proje .]
  juri.py kalibrasyon is/kalibrasyon/set-1 [--proje .]
  juri.py ayirt is/*/elestiri/juri.jsonl [puanlar.jsonl …]
  juri.py set --analiz-db <proje>/veri/analiz.db --cikti is/kalibrasyon/set-1 [--nis evcil] [--pazar ABD] [--adet 12]

pano       Her öge (video · kare klasörü · tek görsel) adsız bir pano görseline çevrilir: video ise ilk 2 sn 5 kare/sn +
           kalanı 2 kare/sn. Kare uygulama ekran görüntüsüyse `--arayuz-maske` şart (beğeni/yorum sayacı performansı ele verir). Harfler karıştırılır; eşleşme `_esleme.json`'da kalır (jüri bu dosyayı AÇMAZ). teslim ve
           onuretim modunda en az 3 gerçek viral referans şart (referanssız pano kör jüri değildir → çıkış 1).
birlestir  `KOR-<n>.json` dosyalarını okur (en az 3 geçerli kopya; yoksa çıkış 1). Öge başına alan medyanı, toplam
           (alan medyanlarının ortalaması, 0,5'e yuvarlı) ve medyan sıra. Bütün ögelere aynı puanı veren (ayırt etmeyen)
           kopya geçersizdir. Bizim video GEÇER: toplam ≥ 7 · hiçbir alan < 5 · medyan sırada sonuncu değil.
           Eşikler DENEME'dir; kalibrasyon verisi geldikçe değişir (değişiklik kalibrasyonla gerekçelenir).
kalibrasyon  Performansı bilinen gerçek videolardan kurulu panoda: jüri toplamı ↔ performans puanı Spearman ρ, alan başına
           yayılım (std) ve ρ. n < 8 → VERİ YETERSİZ (çıkış 3, hüküm yok). ρ ≥ 0,5 UYUMLU (0) · 0,2–0,5 ZAYIF (1) ·
           < 0,2 UYUMSUZ (1). std < 1,0 alan "ayırt etmiyor", ρ < 0,2 alan "performansı öngörmüyor" diye işaretlenir.
           Sonuç `.ekip/juri-kalibrasyon.jsonl`'a eklenir; birlestir her hükmün yanına son kalibrasyonu yazar.
ayirt      Hüküm kayıtlarında (juri.jsonl `medyan` ya da eski puanlar.jsonl `puanlar`) alan başına n · ort · std · aralık.
set        analiz veritabanından (salt okunur) performansı ölçülmüş videoları üst/orta/alt dilimden eşit seçer;
           `kalibrasyon.tsv` yazar. Kareleri lider toplar (yol sütunu), sonra `pano --mod kalibrasyon`. Reklam ve mağaza
           ölçütleri (aktif_gun, varyant, sepete_ekleme_orani) aynı TSV'ye sütun olarak elle eklenebilir.

Performans puanı (tek tanım, `perf_siralama`): ögelerin ≥ %80'inde dolu olan ölçütlerin sıra ortalaması —
izlenme/takipçi (yoksa izlenme) · (kaydetme + paylaşım)/izlenme · yorumda satın alma niyeti oranı · reklamın yayında
kalma süresi (gün) ve varyant sayısı · mağazada sepete ekleme oranı. Ölçütü olmayan öge hesaptan düşer ("veri yok");
değer uydurulmaz.
Çıkış: 0 tamam/geçti/uyumlu · 1 kaldı/uyumsuz/geçersiz girdi · 2 kullanım hatası · 3 veri yetersiz.
"""
import argparse
import csv
import datetime
import glob
import json
import math
import os
import random
import sqlite3
import statistics
import subprocess
import sys

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BURASI = os.path.dirname(os.path.abspath(__file__))
ALANLAR = ["dururdum", "anlasilir", "gercek", "yazi", "ritim", "gonderirdim"]
ALAN_ACIKLAMA = {
    "dururdum": "ilk kare + ilk 1,5 sn: kaydırırken durur muydum",
    "anlasilir": "ürün ve ne işe yaradığı ilk izlemede anlaşılıyor mu",
    "gercek": "yapaylık izi yok (ışık, el, yüz, ürün biçimi, bindirme kenarı)",
    "yazi": "ekran yazısı: işçilik + ikna (bilgi kartı değil)",
    "ritim": "plan çeşitliliği ve akış; boş ya da tekrar eden plan yok",
    "gonderirdim": "birine gönderme / kaydetme isteği",
}
PERF_OLCUT = ["izlenme_takipci", "etkilesim_orani", "niyet_orani", "aktif_gun", "varyant", "sepete_ekleme_orani"]
MIN_KOPYA, MIN_REFERANS, MIN_N = 3, 3, 8
GECME = {"toplam": 7.0, "alan": 5.0}
GORSEL = (".jpg", ".jpeg", ".png", ".webp")


def yuvarla(x):
    return math.floor(x * 2 + 0.5) / 2


def sayi(x):
    try:
        return float(str(x).strip().replace(",", "."))
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------ performans
def perf_degerleri(p):
    """Ham satırdan türetilmiş ölçütler (yalnız verisi olanlar)."""
    d = {}
    iz, tk = sayi(p.get("izlenme")), sayi(p.get("takipci"))
    if iz is not None and tk:
        d["izlenme_takipci"] = iz / tk
    elif sayi(p.get("izlenme_takipci")) is not None:
        d["izlenme_takipci"] = sayi(p["izlenme_takipci"])
    elif iz is not None:
        d["izlenme"] = iz
    kp = [sayi(p.get(k)) for k in ("kaydetme", "paylasim")]
    if iz and any(v is not None for v in kp):
        d["etkilesim_orani"] = sum(v for v in kp if v is not None) / iz
    for k in ("niyet_orani", "aktif_gun", "varyant", "sepete_ekleme_orani"):
        if sayi(p.get(k)) is not None:
            d[k] = sayi(p[k])
    return d


def siralar(degerler):
    """Büyük değer = iyi → sıra 1. Eşitler ortalama sıra alır."""
    sirali = sorted(degerler.items(), key=lambda kv: -kv[1])
    out, i = {}, 0
    while i < len(sirali):
        j = i
        while j + 1 < len(sirali) and sirali[j + 1][1] == sirali[i][1]:
            j += 1
        for k in range(i, j + 1):
            out[sirali[k][0]] = (i + j) / 2 + 1
        i = j + 1
    return out


def perf_siralama(ogeler):
    """{kod: perf dict} → ({kod: bileşik sıra}, kullanılan ölçütler, düşen kodlar). Küçük sıra = iyi."""
    turev = {k: perf_degerleri(p or {}) for k, p in ogeler.items()}
    n = len(turev)
    birincil = "izlenme_takipci" if sum("izlenme_takipci" in d for d in turev.values()) >= 0.8 * n else "izlenme"
    adaylar = [birincil] + [o for o in PERF_OLCUT if o != "izlenme_takipci"]
    kullan = [o for o in adaylar if n and sum(o in d for d in turev.values()) >= 0.8 * n]
    if not kullan:
        return {}, [], sorted(turev)
    kalan = {k: d for k, d in turev.items() if all(o in d for o in kullan)}
    olcut_sira = {o: siralar({k: d[o] for k, d in kalan.items()}) for o in kullan}
    bilesik = {k: sum(olcut_sira[o][k] for o in kullan) / len(kullan) for k in kalan}
    return bilesik, kullan, sorted(set(turev) - set(kalan))


def spearman(a, b):
    """a, b: {kod: değer} (büyük = iyi her ikisinde de aynı yönde olmalı). Ortak kodlarda ρ; n < 3 ise None."""
    ortak = sorted(set(a) & set(b))
    if len(ortak) < 3:
        return None, len(ortak)
    ra, rb = siralar({k: a[k] for k in ortak}), siralar({k: b[k] for k in ortak})
    xa, xb = [ra[k] for k in ortak], [rb[k] for k in ortak]
    ma, mb = sum(xa) / len(xa), sum(xb) / len(xb)
    pay = sum((x - ma) * (y - mb) for x, y in zip(xa, xb))
    payda = math.sqrt(sum((x - ma) ** 2 for x in xa) * sum((y - mb) ** 2 for y in xb))
    return (None if payda == 0 else round(pay / payda, 3)), len(ortak)


# ------------------------------------------------------------------ pano
def ffmpeg():
    sys.path.insert(0, BURASI)
    import ffaraclar as F
    return F.ffmpeg_bul()


def video_panosu(yol, cikti):
    """İlk 2 sn 5 kare/sn + kalan 2 kare/sn (toplam en çok 30 kare). Dosya adı ve meta veri panoya taşınmaz."""
    import tempfile
    ff = ffmpeg()
    with tempfile.TemporaryDirectory() as g:
        for ad, giris in (("a", ["-t", "2", "-i", yol, "-vf", "fps=5,scale=-2:384"]),
                          ("b", ["-ss", "2", "-i", yol, "-vf", "fps=2,scale=-2:384", "-frames:v", "20"])):
            subprocess.run([ff, "-v", "error", "-y"] + giris + ["-q:v", "3", os.path.join(g, ad + "_%03d.jpg")],
                           capture_output=True, text=True)
        kareler = sorted(glob.glob(os.path.join(g, "*.jpg")))
        if not kareler:
            raise SystemExit("HATA: videodan kare çıkarılamadı: %s" % yol)
        gorsel_panosu(kareler, cikti)


MASKE = False  # --arayuz-maske: ekran görüntüsü kaynaklı karede beğeni/yorum/paylaşım sayaçlarını kapatır


def maskele(k):
    """Uygulama arayüzündeki sayaçlar performansı ele verir (kör jüri sızıntısı): sağ %18 şeridin alt %60'ı ve alt %7 kapatılır."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(k)
    w, h = k.size
    d.rectangle([int(w * 0.82), int(h * 0.40), w, h], fill=(0, 0, 0))
    d.rectangle([0, int(h * 0.93), w, h], fill=(0, 0, 0))
    return k


def gorsel_panosu(yollar, cikti):
    from PIL import Image
    kareler = [Image.open(y).convert("RGB") for y in yollar[:30]]
    if MASKE:
        kareler = [maskele(k) for k in kareler]
    if len(kareler) == 1:
        k = kareler[0]
        k.thumbnail((1080, 1920))
        k.save(cikti, quality=88)
        return
    w, h, sutun = 216, 384, 5
    satir = math.ceil(len(kareler) / sutun)
    pano = Image.new("RGB", (w * min(sutun, len(kareler)), h * satir), (0, 0, 0))
    for i, k in enumerate(kareler):
        k.thumbnail((w, h))
        pano.paste(k, ((i % sutun) * w + (w - k.width) // 2, (i // sutun) * h + (h - k.height) // 2))
    pano.save(cikti, quality=88)


def oge_panosu(yol, cikti):
    if os.path.isdir(yol):
        yollar = sorted(y for y in glob.glob(os.path.join(yol, "*")) if y.lower().endswith(GORSEL))
        if not yollar:
            raise SystemExit("HATA: klasörde görsel yok: %s" % yol)
        gorsel_panosu(yollar, cikti)
    elif yol.lower().endswith(GORSEL):
        gorsel_panosu([yol], cikti)
    elif os.path.isfile(yol):
        video_panosu(yol, cikti)
    else:
        raise SystemExit("HATA: öge bulunamadı: %s" % yol)


def pano(a):
    global MASKE
    MASKE = bool(a.arayuz_maske)
    ogeler = []
    for b in a.bizim:
        ad, _, yol = b.partition("=")
        if not yol:
            raise SystemExit("HATA: --bizim AD=YOL biçiminde olmalı (ör. V03=is/07/kurgu/V03.mp4)")
        ogeler.append({"tur": "bizim", "ad": ad, "kaynak": yol, "perf": {}})
    for i, r in enumerate(a.referans, 1):
        ogeler.append({"tur": "referans", "ad": "R%d" % i, "kaynak": r, "perf": {}})
    if a.tsv:
        kok = os.path.dirname(os.path.abspath(a.tsv))
        with open(a.tsv, encoding="utf-8-sig", newline="") as f:
            for s in csv.DictReader(f, delimiter="\t"):
                yol = (s.get("yol") or "").strip()
                if not yol:
                    print("ATLANDI %s: yol boş (kare toplanmamış)" % s.get("kimlik"))
                    continue
                perf = {k: v for k, v in s.items() if k not in ("kimlik", "yol", "url", "not") and (v or "").strip()}
                ogeler.append({"tur": "referans", "ad": s["kimlik"], "kaynak": yol if os.path.isabs(yol) else os.path.join(kok, yol),
                               "perf": perf})
    ref = sum(o["tur"] == "referans" for o in ogeler)
    if a.mod in ("teslim", "onuretim"):
        if not a.bizim:
            raise SystemExit("HATA: %s modunda --bizim gerekli" % a.mod)
        if ref < MIN_REFERANS:
            print("HATA: %d gerçek viral referans var, en az %d gerekli. Referanssız pano kör jüri değildir "
                  "(kaynak: is/NN/viral-referans.md'deki videoların kareleri)." % (ref, MIN_REFERANS), file=sys.stderr)
            return 1
    elif ref < MIN_N:
        print("UYARI: kalibrasyon panosunda %d öge var; %d altı VERİ YETERSİZ sayılır." % (ref, MIN_N))
    if len(ogeler) > 26:
        kodlar = ["K%02d" % i for i in range(1, len(ogeler) + 1)]
    else:
        kodlar = [chr(65 + i) for i in range(len(ogeler))]
    tohum = a.tohum if a.tohum is not None else random.SystemRandom().randrange(10 ** 9)
    random.Random(tohum).shuffle(ogeler)
    os.makedirs(os.path.join(a.cikti, "pano"), exist_ok=True)
    esleme = {"mod": a.mod, "tohum": tohum, "olusturma": datetime.date.today().isoformat(), "ogeler": {}}
    for kod, o in zip(kodlar, ogeler):
        oge_panosu(o["kaynak"], os.path.join(a.cikti, "pano", kod + ".jpg"))
        esleme["ogeler"][kod] = o
    with open(os.path.join(a.cikti, "_esleme.json"), "w", encoding="utf-8") as f:
        json.dump(esleme, f, ensure_ascii=False, indent=1)
    with open(os.path.join(a.cikti, "BRIEF.md"), "w", encoding="utf-8") as f:
        f.write("# Kör jüri brifi\nMod: %s\nPano: `pano/` (%d öge: %s)\nBağlam: %s\n"
                "Çıktı: `KOR-<kopya no>.json` (bu klasöre). `_esleme.json` AÇILMAZ.\n"
                % (a.mod, len(kodlar), ", ".join(kodlar), a.baglam or "ürün videosu, dikey kısa video akışı"))
    print("pano: %s/pano (%d öge, %d referans) · eşleşme gizli: _esleme.json" % (a.cikti, len(kodlar), ref))
    return 0


# ------------------------------------------------------------------ birleştir
def kopyalari_oku(dizin, kodlar):
    """Geçerli kopyalar + geçersizlik nedenleri."""
    gecerli, gecersiz = [], []
    for yol in sorted(glob.glob(os.path.join(dizin, "KOR-*.json"))):
        ad = os.path.basename(yol)
        try:
            d = json.load(open(yol, encoding="utf-8"))
        except ValueError as e:
            gecersiz.append("%s: JSON okunamadı (%s)" % (ad, e))
            continue
        p, sira = d.get("puanlar") or {}, d.get("sira") or []
        hata = []
        if sorted(p) != sorted(kodlar):
            hata.append("ögeler eksik/fazla (beklenen %s)" % ",".join(kodlar))
        elif sorted(sira) != sorted(kodlar):
            hata.append("sıra bütün ögelerin tek tek sıralaması değil")
        else:
            for k in kodlar:
                for al in ALANLAR:
                    v = sayi(p[k].get(al))
                    if v is None or not 0 <= v <= 10:
                        hata.append("%s.%s 0–10 değil" % (k, al))
            if not hata and len(kodlar) >= 3:
                duz = [al for al in ALANLAR if len({sayi(p[k][al]) for k in kodlar}) == 1]
                if len(duz) > len(ALANLAR) / 2:
                    hata.append("ayırt etmiyor: %d alanda bütün ögelere aynı puan (%s)" % (len(duz), ", ".join(duz)))
        if hata:
            gecersiz.append("%s: %s" % (ad, "; ".join(hata[:4])))
        else:
            gecerli.append({"ad": ad, "puanlar": {k: {al: sayi(p[k][al]) for al in ALANLAR} for k in kodlar},
                            "sira": {k: sira.index(k) + 1 for k in kodlar}, "yapay": d.get("yapay") or []})
    return gecerli, gecersiz


def ozetle(gecerli, kodlar):
    oz = {}
    for k in kodlar:
        med = {al: statistics.median(c["puanlar"][k][al] for c in gecerli) for al in ALANLAR}
        oz[k] = {"medyan": med, "toplam": yuvarla(sum(med.values()) / len(med)),
                 "ham_toplam": sum(med.values()) / len(med),
                 "sira": statistics.median(c["sira"][k] for c in gecerli),
                 "sira_yayilim": max(c["sira"][k] for c in gecerli) - min(c["sira"][k] for c in gecerli),
                 "yapay_oy": sum(k in c["yapay"] for c in gecerli)}
    return oz


def son_kalibrasyon(proje):
    yol = os.path.join(proje or ".", ".ekip", "juri-kalibrasyon.jsonl")
    if not os.path.exists(yol):
        return {"durum": "ölçülmedi"}
    satirlar = [json.loads(s) for s in open(yol, encoding="utf-8") if s.strip()]
    if not satirlar:
        return {"durum": "ölçülmedi"}
    s = satirlar[-1]
    return {"durum": s["hukum"], "rho": s.get("rho"), "n": s.get("n"), "tarih": s.get("tarih")}


def esleme_oku(dizin):
    yol = os.path.join(dizin, "_esleme.json")
    if not os.path.exists(yol):
        raise SystemExit("HATA: _esleme.json yok: %s (önce `juri.py pano`)" % dizin)
    return json.load(open(yol, encoding="utf-8"))


def birlestir(a):
    es = esleme_oku(a.dizin)
    kodlar = sorted(es["ogeler"])
    gecerli, gecersiz = kopyalari_oku(a.dizin, kodlar)
    for g in gecersiz:
        print("GEÇERSİZ KOPYA %s" % g)
    if len(gecerli) < MIN_KOPYA:
        print("KALDI: %d geçerli kopya var, en az %d bağımsız kopya gerekli (tek kopya hüküm değildir)." % (len(gecerli), MIN_KOPYA),
              file=sys.stderr)
        return 1
    oz = ozetle(gecerli, kodlar)
    n = len(kodlar)
    kal = son_kalibrasyon(a.proje)
    print("JÜRİ %s · %d kopya · %d öge · kalibrasyon: %s" % (es["mod"], len(gecerli), n,
          kal["durum"] if kal["durum"] == "ölçülmedi" else "%s (ρ %s, n %s)" % (kal["durum"], kal.get("rho"), kal.get("n"))))
    print("| Öge | Kim | " + " | ".join(ALANLAR) + " | Toplam | Medyan sıra |\n|---|---|" + "---|" * (len(ALANLAR) + 2))
    for k in sorted(kodlar, key=lambda x: oz[x]["sira"]):
        o = es["ogeler"][k]
        print("| %s | %s | %s | %.1f | %s |" % (k, o["ad"] if o["tur"] == "bizim" else "referans",
              " | ".join("%g" % oz[k]["medyan"][al] for al in ALANLAR), oz[k]["toplam"], "%g" % oz[k]["sira"]))
    bizimkiler = [k for k in kodlar if es["ogeler"][k]["tur"] == "bizim"]
    kalan = 0
    en_iyi_ref = max((oz[k]["toplam"] for k in kodlar if es["ogeler"][k]["tur"] == "referans"), default=None)
    for k in bizimkiler:
        o, x = es["ogeler"][k], oz[k]
        nedenler = []
        if x["toplam"] < GECME["toplam"]:
            nedenler.append("toplam %.1f < %.1f" % (x["toplam"], GECME["toplam"]))
        dusuk = [al for al in ALANLAR if x["medyan"][al] < GECME["alan"]]
        if dusuk:
            nedenler.append("alan < %g: %s" % (GECME["alan"], ", ".join(dusuk)))
        if x["sira"] >= n:
            nedenler.append("gerçek viral referansların hepsinin gerisinde (medyan sıra %g/%d)" % (x["sira"], n))
        gecti = not nedenler
        kalan += not gecti
        kayit = {"video": o["ad"], "tur": a.tur, "mod": es["mod"], "kaynak": "kor-juri", "kopya": len(gecerli),
                 "medyan": x["medyan"], "toplam": x["toplam"], "sira": x["sira"], "oge_sayisi": n,
                 "en_iyi_referans": en_iyi_ref, "fark": None if en_iyi_ref is None else round(x["toplam"] - en_iyi_ref, 1),
                 "sira_yayilim": x["sira_yayilim"], "yapay_oy": "%d/%d" % (x["yapay_oy"], len(gecerli)),
                 "gecti": gecti, "nedenler": nedenler, "kalibrasyon": kal,
                 "tarih": datetime.datetime.now().isoformat(timespec="seconds")}
        print("%s %s: toplam %.1f · medyan sıra %g/%d · en iyi referansa fark %s · yapay oyu %s%s%s"
              % ("GEÇTİ" if gecti else "KALDI", o["ad"], x["toplam"], x["sira"], n, kayit["fark"], kayit["yapay_oy"],
                 " · jüri bölündü (sıra yayılımı %d)" % x["sira_yayilim"] if x["sira_yayilim"] > 2 else "",
                 "" if gecti else " — " + "; ".join(nedenler)))
        if a.kayit:
            os.makedirs(os.path.dirname(os.path.abspath(a.kayit)), exist_ok=True)
            with open(a.kayit, "a", encoding="utf-8") as f:
                f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
    if kal["durum"] != "UYUMLU":
        print("NOT: jüri performansa karşı %s; hüküm DENEME sayılır (`juri.py kalibrasyon`)." % kal["durum"])
    return 1 if kalan else 0


# ------------------------------------------------------------------ kalibrasyon / ayırt edicilik
def alan_tablosu(satirlar_alan):
    """{alan: [değerler]} → [(alan, n, ort, std, min, max)]"""
    out = []
    for al, v in satirlar_alan.items():
        if v:
            out.append((al, len(v), sum(v) / len(v), statistics.pstdev(v) if len(v) > 1 else 0.0, min(v), max(v)))
    return out


def kalibrasyon(a):
    es = esleme_oku(a.dizin)
    kodlar = sorted(es["ogeler"])
    gecerli, gecersiz = kopyalari_oku(a.dizin, kodlar)
    for g in gecersiz:
        print("GEÇERSİZ KOPYA %s" % g)
    if len(gecerli) < MIN_KOPYA:
        print("KALDI: %d geçerli kopya, en az %d gerekli." % (len(gecerli), MIN_KOPYA), file=sys.stderr)
        return 1
    oz = ozetle(gecerli, kodlar)
    perf, olcutler, dusen = perf_siralama({k: es["ogeler"][k].get("perf") for k in kodlar})
    if not perf:
        print("VERİ YETERSİZ: ögelerin performans ölçütü yok (izlenme, takipçi, kaydetme…); uydurulmaz.", file=sys.stderr)
        return 3
    perf_iyi = {k: -v for k, v in perf.items()}  # büyük = iyi
    rho, n = spearman({k: oz[k]["ham_toplam"] for k in perf}, perf_iyi)
    rho_sira, _ = spearman({k: -oz[k]["sira"] for k in perf}, perf_iyi)
    alanlar = []
    for al in ALANLAR:
        v = [oz[k]["medyan"][al] for k in perf]
        r, _ = spearman({k: oz[k]["medyan"][al] for k in perf}, perf_iyi)
        std = statistics.pstdev(v) if len(v) > 1 else 0.0
        alanlar.append({"alan": al, "std": round(std, 2), "rho": r, "aralik": [min(v), max(v)],
                        "isaret": ([] if std >= 1.0 else ["ayırt etmiyor"]) + ([] if (r is not None and r >= 0.2) else ["performansı öngörmüyor"])})
    if n < MIN_N or rho is None:
        hukum, kod = "VERİ YETERSİZ", 3
    elif rho >= 0.5:
        hukum, kod = "UYUMLU", 0
    elif rho >= 0.2:
        hukum, kod = "ZAYIF", 1
    else:
        hukum, kod = "UYUMSUZ", 1
    print("KALİBRASYON · %d kopya · n = %d (veri yok: %d) · ölçütler: %s" % (len(gecerli), n, len(dusen), ", ".join(olcutler)))
    print("jüri toplamı ↔ performans: ρ = %s · jüri sırası ↔ performans: ρ = %s → %s" % (rho, rho_sira, hukum))
    print("| Alan | Yayılım (std) | Aralık | ρ (performans) | İşaret |\n|---|---|---|---|---|")
    for x in alanlar:
        print("| %s | %.2f | %g–%g | %s | %s |" % (x["alan"], x["std"], x["aralik"][0], x["aralik"][1], x["rho"], ", ".join(x["isaret"]) or "—"))
    if hukum == "VERİ YETERSİZ":
        print("n < %d: bu sayı hüküm değildir; jüri talimatı bu sonuca göre değiştirilmez." % MIN_N)
    ekip = os.path.join(a.proje or ".", ".ekip")
    if os.path.isdir(ekip):
        with open(os.path.join(ekip, "juri-kalibrasyon.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"tarih": datetime.date.today().isoformat(), "set": os.path.basename(os.path.abspath(a.dizin)),
                                "n": n, "kopya": len(gecerli), "olcutler": olcutler, "rho": rho, "rho_sira": rho_sira,
                                "hukum": hukum, "alanlar": alanlar, "veri_yok": dusen}, ensure_ascii=False) + "\n")
    return kod


def ayirt(a):
    alan = {}
    n = 0
    for yol in a.dosyalar:
        if not os.path.exists(yol):
            print("dosya yok: %s" % yol, file=sys.stderr)
            continue
        for s in open(yol, encoding="utf-8"):
            if s.strip():
                r = json.loads(s)
                puan = r.get("medyan") or r.get("puanlar") or {}
                n += 1
                for k, v in puan.items():
                    if sayi(v) is not None:
                        alan.setdefault(k, []).append(sayi(v))
    if not alan:
        print("veri yok: hiçbir dosyada puan satırı bulunamadı")
        return 3
    print("AYIRT EDİCİLİK · %d satır\n| Alan | n | Ort | Std | Aralık | İşaret |\n|---|---|---|---|---|---|" % n)
    for al, k, ort, std, mn, mx in sorted(alan_tablosu(alan), key=lambda x: x[3]):
        print("| %s | %d | %.2f | %.2f | %g–%g | %s |" % (al, k, ort, std, mn, mx, "ayırt etmiyor" if std < 1.0 else "—"))
    return 0


# ------------------------------------------------------------------ set
def set_kur(a):
    if not os.path.exists(a.analiz_db):
        print("VERİ YOK: analiz veritabanı bulunamadı: %s" % a.analiz_db, file=sys.stderr)
        return 3
    c = sqlite3.connect("file:%s?mode=ro" % os.path.abspath(a.analiz_db), uri=True)
    c.row_factory = sqlite3.Row
    kosul, deger = ["v.izlenme IS NOT NULL", "h.takipci > 0"], []
    if a.nis:
        kosul.append("v.nis = ?"); deger.append(a.nis)
    if a.pazar:
        kosul.append("v.pazar = ?"); deger.append(a.pazar)
    satirlar = [dict(r) for r in c.execute(
        "SELECT v.video_anahtari AS kimlik, v.url, v.nis, v.izlenme, h.takipci, v.begeni, v.yorum, v.paylasim, v.kaydetme "
        "FROM video v JOIN hesap h ON h.hesap_id = v.hesap_id WHERE " + " AND ".join(kosul), deger)]
    if len(satirlar) < MIN_N:
        print("VERİ YETERSİZ: ölçütü dolu %d video var (en az %d). Filtreyi genişlet ya da veri topla." % (len(satirlar), MIN_N), file=sys.stderr)
        return 3
    satirlar.sort(key=lambda r: -r["izlenme"] / r["takipci"])
    adet = min(a.adet, len(satirlar))
    dilim = max(1, adet // 3)
    orta = len(satirlar) // 2
    secim = satirlar[:dilim] + satirlar[orta - dilim // 2: orta - dilim // 2 + dilim] + satirlar[-(adet - 2 * dilim):]
    gorulen, tekil = set(), []
    for r in secim:
        if r["kimlik"] not in gorulen:
            gorulen.add(r["kimlik"]); tekil.append(r)
    os.makedirs(a.cikti, exist_ok=True)
    sutun = ["kimlik", "yol", "url", "nis", "izlenme", "takipci", "begeni", "yorum", "paylasim", "kaydetme", "aktif_gun", "varyant"]
    with open(os.path.join(a.cikti, "kalibrasyon.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=sutun, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in tekil:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in sutun})
    print("set: %d video (üst/orta/alt dilim) → %s/kalibrasyon.tsv · `yol` sütununa her videonun kare klasörünü yaz, sonra "
          "`juri.py pano --mod kalibrasyon --tsv …`" % (len(tekil), a.cikti))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut", required=True)
    p = alt.add_parser("pano")
    p.add_argument("--cikti", required=True); p.add_argument("--mod", choices=["teslim", "onuretim", "kalibrasyon"], required=True)
    p.add_argument("--bizim", action="append", default=[]); p.add_argument("--referans", action="append", default=[])
    p.add_argument("--tsv"); p.add_argument("--tohum", type=int); p.add_argument("--baglam")
    p.add_argument("--arayuz-maske", action="store_true",
                   help="ekran görüntüsünden alınan karelerde sayaçları (beğeni/yorum/paylaşım) kapat — sayaç performansı ele verir")
    b = alt.add_parser("birlestir")
    b.add_argument("dizin"); b.add_argument("--kayit"); b.add_argument("--tur", type=int, default=1); b.add_argument("--proje", default=".")
    k = alt.add_parser("kalibrasyon")
    k.add_argument("dizin"); k.add_argument("--proje", default=".")
    y = alt.add_parser("ayirt")
    y.add_argument("dosyalar", nargs="+")
    s = alt.add_parser("set")
    s.add_argument("--analiz-db", required=True); s.add_argument("--cikti", required=True)
    s.add_argument("--nis"); s.add_argument("--pazar"); s.add_argument("--adet", type=int, default=12)
    a = ap.parse_args()
    return {"pano": pano, "birlestir": birlestir, "kalibrasyon": kalibrasyon, "ayirt": ayirt, "set": set_kur}[a.komut](a)


if __name__ == "__main__":
    sys.exit(main())
