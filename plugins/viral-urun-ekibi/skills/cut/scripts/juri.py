#!/usr/bin/env python3
"""Kör video jürisi: pano hazırlar, 3 bağımsız kopyanın puanını birleştirir, jüriyi GERÇEK PERFORMANSA karşı sınar.

"En iyi" kurucunun beğenisinden değil ölçülmüş performanstan öğrenilir: referanslar gerçekten izlenmiş viral videolardır,
jürinin değeri de "sıralaması gerçek performans sıralamasıyla ne kadar uyuşuyor" sorusuyla ölçülür (geriye dönük test).

  juri.py pano --cikti is/NN/juri/tur-1 --mod teslim|onuretim --bizim V03=is/NN/kurgu/V03.mp4 --referans R1 --referans R2 --referans R3
  juri.py pano --cikti is/NN/juri/tur-1 --mod teslim --bizim V03=… --referans-klasoru is/NN/referans   (analiz.db yok: indirdiğin ≥ 3 viral video bu klasörde)
  juri.py pano --cikti is/kalibrasyon/set-1 --mod kalibrasyon --tsv kalibrasyon.tsv
  juri.py birlestir is/NN/juri/tur-1 --kayit is/NN/elestiri/juri.jsonl --tur 1 [--proje .]
  juri.py kalibrasyon is/kalibrasyon/set-1 [--proje .]
  juri.py ayirt is/*/elestiri/juri.jsonl [puanlar.jsonl …]
  juri.py yapilamadi is/NN --video V03 --mod teslim --referans-sayisi 2 --neden "viral referans < 3"   (kapı KALDI olur; ilerlemek yalnız kullanıcının (mağaza sahibinin) açık aşım cümlesiyle: KARARLAR.md kapi-asimi)
  juri.py set --analiz-db <proje>/veri/analiz.db --cikti is/kalibrasyon/set-1 [--nis evcil] [--pazar ABD] [--adet 12]

pano       Her öge (video · kare klasörü · tek görsel) AYNI biçimde adsız pano görseline çevrilir: 20 kare, 5×4 ızgara, 1080×1536
           (video: ilk 2 sn 5 kare/sn + kalanından 10 eşit aralıklı kare). Video ögeleri (ve `--arayuz-maske` verilen ögeler) hesap adı +
           sayaç şeridi HER ögede, bizim dahil, aynı biçimde kapatılır; maskeden sonra OCR ile @hesap / 1.2M / beğeni kelimesi kalırsa
           PANO GEÇERSİZ (çıkış 1). Her kopyanın kendi klasörü (`<cikti>/kopya-<n>/`) ve kendi harf sırası vardır; eşleşme jürinin
           okuduğu dizinin DIŞINDA durur: `<cikti>.gizli/_esleme.json`. teslim ve onuretim modunda en az 3 gerçek viral referans şart
           (referanssız pano kör jüri değildir → çıkış 1).
birlestir  `kopya-<n>/KOR-<n>.json` dosyalarını okur (pano biçimi tek değilse PANO GEÇERSİZ) (en az 3 geçerli kopya; yoksa çıkış 1). Öge başına alan medyanı, toplam
           (alan medyanlarının ortalaması, 0,5'e yuvarlı) ve medyan sıra. Bütün ögelere aynı puanı veren (ayırt etmeyen)
           kopya geçersizdir. Bizim video GEÇER: toplam ≥ 7 · hiçbir alan < 5 · dururdum ≥ 6 · gonderirdim ≥ 6 · medyan sırada sonuncu değil.
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
import re
import shutil
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
# Denetim 2026-11-25 #5: ortalama telafi edici olmasın — durduran ve paylaştıran iki alanın tabanı (rapordaki değer 6)
ALAN_TABAN = {"dururdum": 6.0, "gonderirdim": 6.0}
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
# Denetim 2026-11-25 #1/#2: her öge AYNI biçimde (20 kare, 5×4 ızgara, 216×384 kare); video ögeleri ya da --arayuz-maske verilince
# hesap adı / beğeni sayacı şeridi HER ögede (bizim dahil) aynı biçimde kapatılır; eşleşme jürinin okuduğu dizinde DEĞİL
# (`<cikti>.gizli/_esleme.json`); her kopyanın kendi klasörü ve kendi harf sırası vardır (`<cikti>/kopya-<n>/`).
KARE_SAYISI, SUTUN, TILE_W, TILE_H = 20, 5, 216, 384
KOPYA_SAYISI = 3
OCR_VENV = os.path.expanduser("~/.local/share/viral-urun-ekibi/ocr-venv/bin/python")
SIZINTI_RE = (r"@\s?[A-Za-z0-9_.]{3,}", r"\b\d[\d.,]*\s?[KkMmBb]\b",
              r"\b\d[\d.,]*\s?[KkMmBb]?\s?(likes?|views?|followers?|comments?|shares?|beğeni|izlenme|takipçi|yorum)\b")
# Sayaç sözcüğü YALNIZ önünde sayı varsa sızıntıdır ("1,2K comments"); CTA "Comment \"KELİME\"" sızıntı değildir (rol sınavı 2026-11-25).


def ffmpeg():
    sys.path.insert(0, BURASI)
    import ffaraclar as F
    return F.ffmpeg_bul()


def esit_sec(liste, n):
    """Listeden eşit aralıklı tam n öğe (az ise tekrarlanır; çıktı uzunluğu HEP n)."""
    if not liste:
        return []
    if n == 1:
        return [liste[0]]
    return [liste[round(i * (len(liste) - 1) / (n - 1))] for i in range(n)]


def video_kareleri(yol):
    """İlk 2 sn 5 kare/sn (10 kare, kanca) + kalanından eşit aralıklı 10 kare. Dosya adı ve meta veri panoya taşınmaz."""
    import tempfile
    from PIL import Image
    ff = ffmpeg()
    with tempfile.TemporaryDirectory() as g:
        for ad, giris in (("a", ["-t", "2", "-i", yol, "-vf", "fps=5,scale=-2:384"]),
                          ("b", ["-ss", "2", "-i", yol, "-vf", "fps=4,scale=-2:384", "-frames:v", "80"])):
            subprocess.run([ff, "-v", "error", "-y"] + giris + ["-q:v", "3", os.path.join(g, ad + "_%03d.jpg")],
                           capture_output=True, text=True)
        a = sorted(glob.glob(os.path.join(g, "a_*.jpg")))
        b = sorted(glob.glob(os.path.join(g, "b_*.jpg")))
        if not a and not b:
            raise SystemExit("HATA: videodan kare çıkarılamadı: %s" % yol)
        sec = esit_sec(a, KARE_SAYISI // 2) + esit_sec(b or a, KARE_SAYISI // 2)
        return [Image.open(k).convert("RGB").copy() for k in sec]


def maskele(k):
    """Uygulama arayüzü performansı ve kimliği ele verir: üst %6 (hesap/başlık) + alt %20 (hesap adı, açıklama) + sağ %15'in
    %38'den aşağısı (beğeni/yorum/paylaşım sayaçları) kapatılır. Bizim ögeler de aynı maskeyi alır (biçim farkı sızıntısı olmaz);
    kurgu kontratı K5 zaten alt %20 + sağ %15'i boş bırakır."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(k)
    w, h = k.size
    d.rectangle([0, 0, w, int(h * 0.06)], fill=(0, 0, 0))
    d.rectangle([0, int(h * 0.80), w, h], fill=(0, 0, 0))
    d.rectangle([int(w * 0.85), int(h * 0.38), w, h], fill=(0, 0, 0))
    return k


def dikis_var(im, sutun):
    """Sütun sınırlarında görüntü kesintisi var mı (gerçek kare sayfası)? Düz manzara fotoğrafı bölünmesin diye."""
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    adim = max(1, h // 200)
    def fark(x):
        return sum(abs(px[x, y] - px[x - 1, y]) for y in range(0, h, adim)) / len(range(0, h, adim))
    ornek = sorted(fark(x) for x in range(2, w, max(1, w // 120)))
    taban = ornek[len(ornek) // 2] + 1.0
    dikis = 0
    for c in range(1, sutun):
        x0 = round(c * w / sutun)
        dikis += max(fark(x) for x in range(max(1, x0 - 2), min(w, x0 + 3))) >= 3 * taban
    return dikis * 2 >= sutun - 1  # sınırların en az yarısı keskin (benzer ardışık kare bir sınırı yumuşatabilir)


def sayfa_bol(im):
    """Yatay kare sayfası ise (dikey 9:16 hücrelerden ızgara) hücre listesi döner, değilse None.
    Hücrenin üst %9'u kırpılır: sayfa etiketleri ("0.4s / 11") süre ve biçim farkı sızdırır."""
    w, h = im.size
    if w <= h:
        return None
    en_iyi = None
    for satir in (1, 2, 3, 4):
        hh = h / satir
        sutun = round(w / (hh * 9 / 16))
        if sutun < 2:
            continue
        hata = abs((w / sutun) / hh - 9 / 16)
        if en_iyi is None or hata < en_iyi[0]:
            en_iyi = (hata, satir, sutun)
    if not en_iyi or en_iyi[0] > 0.06 or en_iyi[1] * en_iyi[2] < 4:
        return None
    _, satir, sutun = en_iyi
    if sutun > 8 or satir * sutun > 24 or not (en_iyi[0] < 0.01 or dikis_var(im, sutun)):  # tam 9:16 ızgara ya da keskin dikiş
        return None
    cw, ch = w / sutun, h / satir
    return [im.crop((int(c * cw), int(r * ch + ch * 0.09), int((c + 1) * cw), int((r + 1) * ch)))
            for r in range(satir) for c in range(sutun)]


def kareleri_al(yol):
    """(kare listesi tam KARE_SAYISI, tür, uyarı). tür: video | kare | tek."""
    from PIL import Image
    if os.path.isdir(yol):
        yollar = sorted(y for y in glob.glob(os.path.join(yol, "*")) if y.lower().endswith(GORSEL))
        # Rol sınavı 2026-11-25: kare klasöründe profil/sayfa ekran görüntüsü hesap adını sızdırıyordu → yalnız kare dosyaları.
        kare_adi = [y for y in yollar if re.match(r"^(k|kare|frame)[_-]?\d+\.", os.path.basename(y).lower())]
        yollar = kare_adi or [y for y in yollar if not re.match(r"^(profil|sayfa|p\d)", os.path.basename(y).lower())]
        if not yollar:
            raise SystemExit("HATA: klasörde görsel yok: %s" % yol)
        uy = "%d kare var, %d'ye tamamlandı (tekrarla)" % (len(yollar), KARE_SAYISI) if len(yollar) < KARE_SAYISI else ""
        return [Image.open(y).convert("RGB") for y in esit_sec(yollar, KARE_SAYISI)], "kare", uy
    if yol.lower().endswith(GORSEL):
        im = Image.open(yol).convert("RGB")
        hucreler = sayfa_bol(im)
        if hucreler:  # kare sayfası (ör. 5×2): hücrelere bölünür, pano içinde pano olmaz (rol sınavı 2026-11-25)
            return esit_sec(hucreler, KARE_SAYISI), "sayfa", "kare sayfası %d hücreye bölündü" % len(hucreler)
        return [im] * KARE_SAYISI, "tek", "tek görsel %d kez tekrarlandı" % KARE_SAYISI
    if os.path.isfile(yol):
        return video_kareleri(yol), "video", ""
    raise SystemExit("HATA: öge bulunamadı: %s" % yol)


def tile_yap(k, maske):
    from PIL import Image
    k = k.copy()
    k.thumbnail((TILE_W, TILE_H))
    t = Image.new("RGB", (TILE_W, TILE_H), (0, 0, 0))
    t.paste(k, ((TILE_W - k.width) // 2, (TILE_H - k.height) // 2))
    return maskele(t) if maske else t


def oge_panosu(yol, cikti, maske_zorla=False):
    """Öge → tek pano görseli (HER ZAMAN 5×4 ızgara, 1080×1536). Döner: (tür, maskelendi_mi, uyarı, sizinti_tile_yolları)."""
    from PIL import Image
    kareler, tur, uy = kareleri_al(yol)
    maske = True  # her öge aynı maskeyi alır: kare klasörü/sayfası da IG arayüzü taşıyabilir (rol sınavı 2026-11-25)
    tiles = [tile_yap(k, maske) for k in kareler]
    pano = Image.new("RGB", (TILE_W * SUTUN, TILE_H * (KARE_SAYISI // SUTUN)), (0, 0, 0))
    for i, t in enumerate(tiles):
        pano.paste(t, ((i % SUTUN) * TILE_W, (i // SUTUN) * TILE_H))
    pano.save(cikti, quality=88)
    return tur, maske, uy, [tiles[i] for i in (0, 6, 13, 19)]


def ocr_sizinti(tiles_listesi):
    """Maskeden sonra kalan hesap adı / sayaç metni var mı? [(ad, [tile])] → ({ad: [bulgu]}, durum). OCR yoksa durum 'olculemedi'."""
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        yollar = []
        for ad, tiles in tiles_listesi:
            for i, im in enumerate(tiles):
                y = os.path.join(t, "%s__%d.png" % (ad, i))
                im.resize((im.width * 3, im.height * 3)).save(y)
                yollar.append(y)
        kod = ("import sys,json\nfrom rapidocr_onnxruntime import RapidOCR\no=RapidOCR()\nout={}\n"
               "for y in sys.argv[1:]:\n    r=o(y)[0] or []\n    out[y]=[m for _,m,g in r if float(g)>=0.5]\nprint(json.dumps(out))\n")
        py = OCR_VENV if os.path.exists(OCR_VENV) else sys.executable
        r = subprocess.run([py, "-c", kod] + yollar, capture_output=True, text=True)
        if r.returncode != 0:
            return {}, "olculemedi"
        try:
            sonuc = json.loads(r.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            return {}, "olculemedi"
    bulgu = {}
    for y, metinler in sonuc.items():
        ad = os.path.basename(y).rsplit("__", 1)[0]
        for m in metinler:
            for desen in SIZINTI_RE:
                if re.search(desen, m, re.I):
                    bulgu.setdefault(ad, []).append(m)
                    break
    return bulgu, "tamam"


def esleme_yolu(dizin):
    """Eşleşme jürinin okuduğu dizinin DIŞINDA: `<dizin>.gizli/_esleme.json`. Eski düzen (dizin içinde) yalnız okunur."""
    yeni = os.path.join(os.path.normpath(dizin) + ".gizli", "_esleme.json")
    return yeni if os.path.exists(yeni) else os.path.join(dizin, "_esleme.json")


REFERANS_UZANTI = (".mp4", ".mov", ".webm", ".mkv", ".m4v", ".png", ".jpg", ".jpeg")


def pano(a):
    ogeler = []
    for b in a.bizim:
        ad, _, yol = b.partition("=")
        if not yol:
            raise SystemExit("HATA: --bizim AD=YOL biçiminde olmalı (ör. V03=is/07/kurgu/V03.mp4)")
        ogeler.append({"tur": "bizim", "ad": ad, "kaynak": yol, "perf": {}})
    referanslar = list(a.referans)
    if a.referans_klasoru:
        # analiz.db olmadan referans: kullanıcının indirdiği viral videolar/görseller/kare klasörleri (ad sırasıyla)
        if not os.path.isdir(a.referans_klasoru):
            raise SystemExit("HATA: --referans-klasoru bulunamadı: %s" % a.referans_klasoru)
        for ad in sorted(os.listdir(a.referans_klasoru)):
            yol = os.path.join(a.referans_klasoru, ad)
            if ad.startswith(".") or not (os.path.isdir(yol) or ad.lower().endswith(REFERANS_UZANTI)):
                continue
            referanslar.append(yol)
    for i, r in enumerate(referanslar, 1):
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
    for i, o in enumerate(ogeler, 1):
        o["id"] = "O%02d" % i
    tohum = a.tohum if a.tohum is not None else random.SystemRandom().randrange(10 ** 9)
    cikti = os.path.normpath(a.cikti)
    gizli = cikti + ".gizli"
    import tempfile
    sizinti_girdi, uyarilar = [], []
    esleme = {"mod": a.mod, "tohum": tohum, "olusturma": datetime.date.today().isoformat(), "kare_sayisi": KARE_SAYISI,
              "ogeler": {}, "kopyalar": {}}
    with tempfile.TemporaryDirectory() as gecici:
        for o in ogeler:
            tur, maske, uy, tiles = oge_panosu(o["kaynak"], os.path.join(gecici, o["id"] + ".jpg"), a.arayuz_maske)
            o.update({"kaynak_turu": tur, "maske": maske})
            if uy:
                uyarilar.append("%s: %s" % (o["id"], uy))
            sizinti_girdi.append((o["id"], tiles))
            esleme["ogeler"][o["id"]] = o
        # biçim sızıntısı (maske artık herkese aynı): durağan tek görsel (aynı kare 20 kez) hareketli ögelerin yanında hemen ayrılır
        if len({o["kaynak_turu"] == "tek" for o in ogeler}) > 1:
            print("PANO GEÇERSİZ: ögelerin bir kısmı tek durağan görsel (20 kez aynı kare), bir kısmı hareketli (biçim farkı sızar). "
                  "Referansı video, kare klasörü ya da kare sayfası olarak verin.", file=sys.stderr)
            return 1
        bulgu, ocr_durum = ocr_sizinti(sizinti_girdi)
        if bulgu:
            print("PANO GEÇERSİZ: maskeden sonra hesap adı/sayaç metni kaldı (kimlik ya da performans sızar):", file=sys.stderr)
            for k, v in sorted(bulgu.items()):
                print("  %s (%s): %s" % (k, esleme["ogeler"][k]["tur"], "; ".join(sorted(set(v))[:3])), file=sys.stderr)
            return 1
        esleme["ocr_sizinti_taramasi"] = ocr_durum
        kopya_n = max(1, a.kopya)
        for eski in glob.glob(os.path.join(cikti, "kopya-*")):
            shutil.rmtree(eski, ignore_errors=True)   # yalnız eski kopya klasörleri; çıktı klasörünün kendisi silinmez
        for n in range(1, kopya_n + 1):
            oidler = [o["id"] for o in ogeler]
            random.Random("%s-%d" % (tohum, n)).shuffle(oidler)
            kodlar = ["K%02d" % i for i in range(1, len(oidler) + 1)] if len(oidler) > 26 else [chr(65 + i) for i in range(len(oidler))]
            kd = os.path.join(cikti, "kopya-%d" % n)
            os.makedirs(os.path.join(kd, "pano"), exist_ok=True)
            esleme["kopyalar"][str(n)] = dict(zip(kodlar, oidler))
            for kod, oid in zip(kodlar, oidler):
                shutil.copy(os.path.join(gecici, oid + ".jpg"), os.path.join(kd, "pano", kod + ".jpg"))
            with open(os.path.join(kd, "BRIEF.md"), "w", encoding="utf-8") as f:
                f.write("# Kör jüri brifi · kopya %d\nMod: %s\nPano: `pano/` (%d öge: %s)\nBağlam: %s\n"
                        "Çıktı: yalnız bu klasöre `KOR-%d.json`. Başka kopya klasörünü ve `.gizli` eşleşme klasörünü AÇMA.\n"
                        % (n, a.mod, len(kodlar), ", ".join(kodlar), a.baglam or "ürün videosu, dikey kısa video akışı", n))
    os.makedirs(gizli, exist_ok=True)
    with open(os.path.join(gizli, "_esleme.json"), "w", encoding="utf-8") as f:
        json.dump(esleme, f, ensure_ascii=False, indent=1)
    for u in uyarilar:
        print("UYARI %s" % u)
    if ocr_durum == "olculemedi":
        print("UYARI: sayaç/hesap adı OCR taraması ÖLÇÜLEMEDİ (RapidOCR yok): maske uygulandı ama sızıntı denetlenmedi.")
    print("pano: %s/kopya-1..%d/pano (%d öge, %d referans, %d kare/öge, 5×4) · eşleşme jüriden ayrı: %s"
          % (cikti, kopya_n, len(ogeler), ref, KARE_SAYISI, os.path.join(gizli, "_esleme.json")))
    return 0


# ------------------------------------------------------------------ birleştir
def kor_dosyalari(dizin, es):
    """[(kopya no | None, yol)]. Yeni düzen: kopya-<n>/KOR-*.json. Eski düzen (eşleşme dizinin içindeyse): dizin/KOR-*.json."""
    out = [(int(m.group(1)), y) for y in sorted(glob.glob(os.path.join(dizin, "kopya-*", "KOR-*.json")))
           for m in [re.search(r"kopya-(\d+)", y)] if m]
    if not es.get("kopyalar"):
        out += [(None, y) for y in sorted(glob.glob(os.path.join(dizin, "KOR-*.json")))]
    return out


def kopyalari_oku(dizin, es):
    """Geçerli kopyalar (öge KİMLİKLERİ üzerinden; kopya başına harf sırası eşleşmeden çözülür) + geçersizlik nedenleri."""
    gecerli, gecersiz = [], []
    oidler = sorted(es["ogeler"])
    for no, yol in kor_dosyalari(dizin, es):
        ad = os.path.relpath(yol, dizin)
        harita = (es.get("kopyalar") or {}).get(str(no)) or {o: o for o in oidler}   # kod → öge kimliği
        kodlar = sorted(harita)
        try:
            d = json.load(open(yol, encoding="utf-8"))
        except ValueError as e:
            gecersiz.append("%s: JSON okunamadı (%s)" % (ad, e))
            continue
        p, sira = d.get("puanlar") or {}, d.get("sira") or []
        hata = []
        if sorted(p) != kodlar:
            hata.append("ögeler eksik/fazla (beklenen %s)" % ",".join(kodlar))
        elif sorted(sira) != kodlar:
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
            gecerli.append({"ad": ad, "puanlar": {harita[k]: {al: sayi(p[k][al]) for al in ALANLAR} for k in kodlar},
                            "sira": {harita[k]: sira.index(k) + 1 for k in kodlar}, "yapay": [harita[k] for k in d.get("yapay") or [] if k in harita]})
    return gecerli, gecersiz


def pano_gecerli(dizin, es):
    """Biçim denetimi: bütün pano görselleri aynı boyutta ve ızgara aynı mı (tek biçim). Boş liste = geçerli."""
    sorun, boyutlar = [], {}
    from PIL import Image
    for y in sorted(glob.glob(os.path.join(dizin, "kopya-*", "pano", "*.jpg"))):
        with Image.open(y) as im:
            boyutlar.setdefault(im.size, []).append(os.path.relpath(y, dizin))
    if len(boyutlar) > 1:
        sorun.append("pano görselleri farklı boyutta (%s) — bizim ile referans ayırt edilir" % ", ".join("%dx%d" % b for b in boyutlar))
    if len({bool(o.get("maske")) for o in es["ogeler"].values() if "maske" in o}) > 1:
        sorun.append("ögelerin bir kısmı maskeli, bir kısmı değil")
    if len({o.get("kaynak_turu") == "tek" for o in es["ogeler"].values() if "kaynak_turu" in o}) > 1:
        sorun.append("ögelerin bir kısmı tek durağan görsel, bir kısmı hareketli")
    return sorun


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
    yol = esleme_yolu(dizin)
    if not os.path.exists(yol):
        raise SystemExit("HATA: _esleme.json yok: %s (önce `juri.py pano`)" % dizin)
    return json.load(open(yol, encoding="utf-8"))


def birlestir(a):
    es = esleme_oku(a.dizin)
    kodlar = sorted(es["ogeler"])
    for sorun in pano_gecerli(a.dizin, es):
        print("PANO GEÇERSİZ: %s" % sorun, file=sys.stderr)
        return 1
    gecerli, gecersiz = kopyalari_oku(a.dizin, es)
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
        taban = [al for al, t in ALAN_TABAN.items() if x["medyan"][al] < t and al not in dusuk]
        if taban:
            nedenler.append("taban < %g: %s (durdurmayan/paylaştırmayan video ortalama telafisiyle geçmez)" % (ALAN_TABAN["dururdum"], ", ".join(taban)))
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
    gecerli, gecersiz = kopyalari_oku(a.dizin, es)
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


def yapilamadi(a):
    """Referans < 3 iken hüküm kaydına açık 'jüri yapılamadı' satırı yazar. GEÇİŞ DEĞİLDİR (gecti=false): kapi.py bunu KALDI sayar,
    ilerlemek yalnız KARARLAR.md'de kullanıcının (mağaza sahibinin) açık aşım cümlesiyle olur (denetim 2026-11-25 #2/#4)."""
    if a.referans_sayisi >= MIN_REFERANS:
        print("HATA: referans %d ≥ %d — jüri koşabilir, 'yapılamadı' yazılamaz" % (a.referans_sayisi, MIN_REFERANS), file=sys.stderr)
        return 1
    if not a.neden.strip():
        print("HATA: --neden boş olamaz", file=sys.stderr)
        return 1
    yol = os.path.join(a.is_dizin, "elestiri", "juri.jsonl")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "a", encoding="utf-8") as f:
        f.write(json.dumps({"video": a.video, "tur": 0, "mod": a.mod, "gecti": False, "juri": "yapilamadi",
                            "referans_sayisi": a.referans_sayisi, "neden": a.neden}, ensure_ascii=False) + "\n")
    print("kaydedildi: %s — kapı KALDI; ilerlemek için kullanıcının (mağaza sahibinin) açık cümlesi gerekir: `- TARİH | kapi-asimi | <kredi|yayin> <iş> hukum[@V]: \"<cümle>\"` (KARARLAR.md). Referans bulma ayrı iş (DURUM.md)" % yol)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut", required=True)
    p = alt.add_parser("pano")
    p.add_argument("--cikti", required=True); p.add_argument("--mod", choices=["teslim", "onuretim", "kalibrasyon"], required=True)
    p.add_argument("--bizim", action="append", default=[]); p.add_argument("--referans", action="append", default=[])
    p.add_argument("--referans-klasoru", help="analiz.db olmadan referans: klasördeki her video/görsel/kare alt klasörü bir referans olur (indirdiğin 3+ viral video)")
    p.add_argument("--tsv"); p.add_argument("--tohum", type=int); p.add_argument("--baglam")
    p.add_argument("--arayuz-maske", action="store_true",
                   help="video olmayan ögelerde (kare klasörü/görsel) de hesap adı + sayaç şeritlerini kapat; video ögeleri HER ZAMAN maskelenir")
    p.add_argument("--kopya", type=int, default=KOPYA_SAYISI, help="bağımsız jüri kopyası sayısı (her birine ayrı klasör ve harf sırası)")
    b = alt.add_parser("birlestir")
    b.add_argument("dizin"); b.add_argument("--kayit"); b.add_argument("--tur", type=int, default=1); b.add_argument("--proje", default=".")
    k = alt.add_parser("kalibrasyon")
    k.add_argument("dizin"); k.add_argument("--proje", default=".")
    y = alt.add_parser("ayirt")
    y.add_argument("dosyalar", nargs="+")
    s = alt.add_parser("set")
    s.add_argument("--analiz-db", required=True); s.add_argument("--cikti", required=True)
    s.add_argument("--nis"); s.add_argument("--pazar"); s.add_argument("--adet", type=int, default=12)
    yp = alt.add_parser("yapilamadi")
    yp.add_argument("is_dizin"); yp.add_argument("--video", required=True); yp.add_argument("--mod", choices=["teslim", "onuretim"], default="teslim")
    yp.add_argument("--referans-sayisi", type=int, required=True); yp.add_argument("--neden", required=True)
    a = ap.parse_args()
    return {"yapilamadi": yapilamadi, "pano": pano, "birlestir": birlestir, "kalibrasyon": kalibrasyon, "ayirt": ayirt, "set": set_kur}[a.komut](a)


if __name__ == "__main__":
    sys.exit(main())
