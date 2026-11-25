#!/usr/bin/env python3
"""kurgu_kontrol.py yeni kapıları: ilk 2 sn kare farkı (`ilk2sn`) ve klip ↔ KAYNAK.tsv eşleşmesi (`malzeme`).
Her kural önce kusurlu girdide KALDI, sonra iyi girdide GEÇTİ verir (denetim 2026-11-25 #6, #12). ffmpeg gerekir (yoksa ATLANIR: ölçülmedi).
Kullanım: python3 kurgu_kontrol_test.py → hepsi geçerse 0."""
import json
import os
import subprocess
import sys
import tempfile

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)
SONUC = []


def ffmpeg():
    import ffaraclar as F
    try:
        return F.ffmpeg_bul()
    except SystemExit:
        yol = os.path.join(os.environ.get("FFMPEG_DIZIN", ""), "ffmpeg")
        return yol if os.path.exists(yol) else None


def video(ff, yol, dinamik):
    if dinamik:   # her 0,4 sn'de gri tonu çok farklı renk
        renkler = ["white", "black", "green", "blue", "red", "white", "black"]
        girdi = []
        for r in renkler:
            girdi += ["-f", "lavfi", "-i", "color=c=%s:s=216x384:r=10:d=0.4" % r]
        cmd = [ff, "-v", "error", "-y"] + girdi + ["-filter_complex", "concat=n=%d:v=1:a=0" % len(renkler), "-pix_fmt", "yuv420p", yol]
    else:         # 3 sn düz renk
        cmd = [ff, "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=red:s=216x384:r=10:d=3", "-pix_fmt", "yuv420p", yol]
    subprocess.run(cmd, check=True, capture_output=True)


def kos(d, *ek):
    r = subprocess.run([sys.executable, os.path.join(BURASI, "kurgu_kontrol.py"), os.path.join(d, "ayar.json"), "--json"] + list(ek),
                       capture_output=True, text=True)
    try:
        j = json.loads(r.stdout)
    except ValueError:
        return {"hatalar": [{"kural": "PARSE", "mesaj": r.stdout + r.stderr}], "uyarilar": []}
    return j


def kural(j, tur, ad):
    return [x for x in j[tur] if x["kural"] == ad]


def kur(kok, ad, kaynak_metin, tur="urun_elde", kaynak_tsv=None):
    d = os.path.join(kok, ad)
    os.makedirs(os.path.join(d, "klipler"))
    json.dump({"klipler": {"u1": {"arac": None, "tur": tur, "icerik": "tuy_rulo", "kaynak": kaynak_metin}}, "araclar": {}},
              open(os.path.join(d, "klipler", "klip_etiket.json"), "w", encoding="utf-8"))
    json.dump({"planlar": [{"klip": "klipler/u1.mp4", "bas": 0, "bit": 1.714}, {"klip": "klipler/u1.mp4", "bas": 3, "bit": 4.714}],
               "yazilar": [{"bas": 0.0, "bit": 1.7, "yazi": "Tüy mü var?"}]}, open(os.path.join(d, "ayar.json"), "w", encoding="utf-8"))
    if kaynak_tsv is not None:
        open(os.path.join(d, "KAYNAK.tsv"), "w", encoding="utf-8").write(kaynak_tsv)
    return d


def t(ad, ok, ayrinti=""):
    SONUC.append((ad, ok))
    if not ok:
        print("--- %s\n%s" % (ad, ayrinti))


TSV = ("vaka\tdosya\tkaynak\tcekim\tkullanilacak_aralik\tnot\n"
       "b-zor\tae-111.mp4\tx\tgercek\t0-4 sn\t-\n"
       "b-zor\tae-333.mp4\tx\tyapay\tkullanma (gercek kapisi)\t-\n"
       "a-kolay\tae-222.mp4\tx\tgercek\t0-4 sn\t-\n")


def main():
    kok = tempfile.mkdtemp(prefix="kurgu_kontrol_test_")
    ff = ffmpeg()
    # --- klip ↔ malzeme (ffmpeg gerekmez)
    d = kur(kok, "b-zor", "tedarikçi ilan videosu ae-111.mp4 17.6s", kaynak_tsv=TSV)
    t("malzeme: ürün klibi KAYNAK.tsv'deki dosyadan -> HATA yok (GEÇTİ)", not kural(kos(d), "hatalar", "malzeme"), kos(d))
    d = kur(kok, "b-zor2", "stok Pexels (LISANS.md)", kaynak_tsv=TSV)
    j = kos(os.path.join(kok, "b-zor2"))
    t("kırma: 'ürün' etiketli klip stoktan (KAYNAK.tsv'de yok) -> malzeme HATA", len(kural(j, "hatalar", "malzeme")) == 1, j)
    # başka vakanın klibi: dizin adı vaka adı (b-zor) → ae-222 a-kolay'a ait
    ayri = os.path.join(kok, "v2"); os.makedirs(ayri)
    d = kur(ayri, "b-zor", "tedarikçi ilan videosu ae-222.mp4 9.0s", kaynak_tsv=TSV)
    j = kos(d)
    t("kırma: başka vakanın klibi (yanlış ürün) -> malzeme HATA", len(kural(j, "hatalar", "malzeme")) == 1, j)
    ayri = os.path.join(kok, "v3"); os.makedirs(ayri)
    d = kur(ayri, "b-zor", "tedarikçi ilan videosu ae-333.mp4 9.0s", kaynak_tsv=TSV)
    j = kos(d)
    t("kırma: 'kullanma' işaretli kaynak -> malzeme HATA", len(kural(j, "hatalar", "malzeme")) == 1, j)
    ayri = os.path.join(kok, "v4"); os.makedirs(ayri)
    d = kur(ayri, "b-zor", "", kaynak_tsv=TSV)
    t("kırma: etikette kaynak hiç yok -> malzeme HATA", len(kural(kos(d), "hatalar", "malzeme")) == 1)
    ayri = os.path.join(kok, "v5"); os.makedirs(ayri)
    d = kur(ayri, "b-zor", "stok Pexels", tur="stok", kaynak_tsv=TSV)
    t("stok etiketli klip KAYNAK.tsv istemez -> GEÇTİ", not kural(kos(d), "hatalar", "malzeme"))
    ayri = os.path.join(kok, "v6"); os.makedirs(ayri)
    d = kur(ayri, "b-zor", "tedarikçi ae-111.mp4")
    j = kos(d)
    t("KAYNAK.tsv yok -> UYARI (ölçülemedi), HATA değil", len(kural(j, "uyarilar", "malzeme")) == 1 and not kural(j, "hatalar", "malzeme"), j)
    j = kos(d, "--malzeme-zorunlu")
    t("kırma: KAYNAK.tsv yok + --malzeme-zorunlu -> HATA", len(kural(j, "hatalar", "malzeme")) == 1, j)
    # --- ilk 2 sn
    if not ff:
        print("ATLANDI ilk2sn testleri: ffmpeg yok (bu kapı bu koşuda ÖLÇÜLMEDİ)")
    else:
        for ad, dinamik, bek in (("durağan 3 sn düz renk", False, True), ("0,4 sn'de bir değişen renkler", True, False)):
            ayri = os.path.join(kok, "i" + str(dinamik)); os.makedirs(ayri)
            d = kur(ayri, "b-zor", "ae-111.mp4", kaynak_tsv=TSV)
            v = os.path.join(d, "video.mp4")
            video(ff, v, dinamik)
            j = kos(d, "--video", v)
            hata = bool(kural(j, "hatalar", "ilk2sn"))
            t("%s: ilk2sn %s" % (ad, "HATA (kırma)" if bek else "yok (GEÇTİ)"), hata == bek, j)
    for ad, ok in SONUC:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    kalan = sum(1 for _, ok in SONUC if not ok)
    print("TOPLAM: %d test, %d kaldı" % (len(SONUC), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
