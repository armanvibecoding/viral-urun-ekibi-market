#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sınav koşucusu: bir özelliğin sabit 3 vakasının çıktısını mekanik kapılardan geçirir, yasaklı çıktıyı tarar,
kör jüri panosunu hazırlar ve SONUC.md yazar. Her sürümden önce koşulur (ortak/tarifler/README.md).

  python3 scripts/sinav_kos.py <ozellik> <cikti_klasoru> [--referans-kok KLASOR] [--vaka a-kolay ...] [--sonuc YOL]
  python3 scripts/sinav_kos.py --liste
  python3 scripts/sinav_kos.py --hepsi <cikti_koku> [--tur tur3] [--referans-kok KLASOR]   7 sınavın hepsi, tek satır özet + çıkış kodu
                   (<cikti_koku>/<özellik>/<tur>/<vaka>/; tur verilmezse her özelliğin en son turu; çıktısı olmayan özellik KALDI)

<ozellik>        01-urun-videosu · 02-kanca-senaryo · 03-hikaye-videosu · 04-ses-muzik · 05-gorsel · 06-urun-avi · 07-site
                 (yalnız önek de olur: 01)
<cikti_klasoru>  içinde vaka klasörleri: a-kolay/ b-zor/ c-tuzak/ (her birinde özelliğin çıktısı; beklenen dosyalar
                 plugins/viral-urun-ekibi/ortak/sinav/<ozellik>/vakalar/<vaka>/vaka.json "beklenen.dosyalar")
--referans-kok   referanslar.tsv'deki göreli `kare_panosu_yolu` değerlerinin çözüleceği klasör (ya da ortam değişkeni
                 SINAV_REFERANS_KOK). Referans yolları depoya mutlak yazılmaz.

Kapı durumları: GEÇTİ · KALDI · olculemedi (ölçen betik/araç yok ya da referans yuvası boş: sahte geçti verilmez) ·
bekliyor (jüri panosu hazır, kör kopyalar henüz puanlamadı) · uygulanmaz (gerekçesi OLCUT.md'de).
Çıkış: 0 = bütün vakaların bütün kapıları GEÇTİ · 1 = en az bir KALDI · 3 = KALDI yok ama olculemedi/bekliyor var.
Eşikler bu dosyada DEĞİL, çağrılan betiklerde ve vaka.json'dadır; bu dosya eşik gevşetmez, yalnız betikleri çağırır.
"""
import argparse
import csv
import datetime
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EKL = os.path.join(KOK, "plugins", "viral-urun-ekibi")
SINAV = os.environ.get("SINAV_KOK") or os.path.join(EKL, "ortak", "sinav")  # SINAV_KOK yalnız kırma testi için
CUT = os.path.join(EKL, "skills", "cut", "scripts")
STUDIO = os.path.join(EKL, "skills", "studio", "scripts")
TRENDYOL = os.path.join(EKL, "skills", "hunter", "trendyol", "scripts")
HUNTER = os.path.join(EKL, "skills", "hunter", "scripts")
GORSEL = os.path.join(EKL, "skills", "builder", "gorseller", "scripts")
ORTAK = os.path.join(EKL, "ortak")
OZELLIKLER = ["01-urun-videosu", "02-kanca-senaryo", "03-hikaye-videosu", "04-ses-muzik", "05-gorsel", "06-urun-avi", "07-site"]
GECTI, KALDI, OLCULEMEDI, BEKLIYOR, UYGULANMAZ = "GEÇTİ", "KALDI", "olculemedi", "bekliyor", "uygulanmaz"
METIN_UZANTI = (".json", ".md", ".txt", ".tsv", ".csv", ".srt")
# Çıktının içinde taranmayan dosyalar: girdi/ölçüm/pano dosyaları (yasaklı sözcük orada meşru olabilir).
TARAMA_HARIC = ("vaka.json", "magaza-paketi.json", "klip_etiket.json", "_esleme.json", "BRIEF.md", "SONUC.md", "stil.json",
                # Ölçüm/denetim raporları: içindeki yüzde ölçümdür (ör. "ürün kadrajın %58'i"), müşteriye giden iddia değil.
                "KAPI.md", "SADAKAT.md", "URUN-KILIDI.md", "OCR.md", "ELESTIRI.md", "SONUC-HEPSI.md")

# IDD-02 (uydurma veri) için her vakaya uygulanan genel desenler; vaka.json "izinli" listesindeki metin muaf.
GENEL_YASAKLI = [
    (r"\b\d{1,3}\s?%|%\s?\d{1,3}\b", "uydurma yüzde/istatistik (IDD-02)"),
    (r"clinically (proven|tested)|klinik(?:\s+olarak)?\s+(kanıtlanmış|test)|klinisch (bewiesen|getestet)", "uydurma klinik kanıt (IDD-02)"),
    (r"doctor[- ]recommended|doctors? (love|recommend)|doktor(lar)? (önerir|tavsiye)|ärztlich empfohlen", "belgesiz uzman onayı (IDD-02)"),
    (r"\bonly \d+ left\b|\bson \d+ (adet|ürün)\b|nur noch \d+|stokla?r? tükeniyor|selling out|countdown", "sahte kıtlık/geri sayım (IDD-02)"),
    (r"\b(#1|no\.? ?1|number one)\b|en çok satan|bestseller|best[- ]seller", "kanıtsız en iyi/çok satan iddiası (IDD-02)"),
    (r"\b(\d[\d.,]*\s?(k|bin|m)?\+?\s?(happy )?(customers|müşteri|kunden|reviews|yorum|bewertungen))\b", "uydurma müşteri/yorum sayısı (IDD-02)"),
]

sys.path.insert(0, ORTAK)
sys.path.insert(0, CUT)


def G(kapi, durum, ayrinti=""):
    return {"kapi": kapi, "durum": durum, "ayrinti": " ".join(str(ayrinti).split())[:400]}


def kos(cmd, cwd=None, timeout=900):
    try:
        r = subprocess.run([str(x) for x in cmd], capture_output=True, text=True, cwd=cwd, timeout=timeout)
        return r.returncode, (r.stdout or ""), (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "", "zaman aşımı"
    except OSError as e:
        return 127, "", str(e)


def py(betik, *arg, cwd=None):
    return kos([sys.executable, betik] + list(arg), cwd=cwd)


def oku_json(yol):
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def son(s, n=240):
    s = " ".join(s.split())
    return s[-n:]


# ------------------------------------------------------------------ ortak kapılar
def k_dosyalar(c):
    eksik = []
    for ad in c["vaka"]["beklenen"].get("dosyalar", []):
        p = os.path.join(c["d"], ad)
        if ad.endswith("/"):
            if not (os.path.isdir(p) and os.listdir(p)):
                eksik.append(ad + " (boş/yok)")
        elif not (os.path.isfile(p) and os.path.getsize(p) > 0):
            eksik.append(ad + " (boş/yok)")
    return [G("dosyalar", KALDI if eksik else GECTI, "eksik: " + ", ".join(eksik) if eksik else "tamam")]


def metinler(c):
    haric = set(TARAMA_HARIC) | set(c["vaka"]["beklenen"].get("tarama_haric", []))
    out = []
    for yol in sorted(glob.glob(os.path.join(c["d"], "**", "*"), recursive=True)):
        rel = os.path.relpath(yol, c["d"])
        if not os.path.isfile(yol) or not yol.lower().endswith(METIN_UZANTI):
            continue
        if os.path.basename(yol) in haric or rel.split(os.sep)[0] in ("juri", "varyasyon") or rel in haric:
            continue
        try:
            with open(yol, encoding="utf-8") as f:
                out.append((rel, f.read()))
        except (OSError, UnicodeDecodeError):
            pass
    return out


def k_yasakli(c):
    """Yasaklı çıktı taraması: genel (IDD-02) + vakaya özel desenler. Tek eşleşme = KALDI."""
    v = c["vaka"]
    izinli = [x.lower() for x in v.get("izinli", [])]
    desenler = [(d, n) for d, n in GENEL_YASAKLI] + [(d, "vaka yasağı: " + v["beklenen"].get("yasakli_neden", "yasaklı çıktı"))
                                                      for d in v.get("yasakli", [])]
    bulunan = []
    for rel, metin in metinler(c):
        for d, neden in desenler:
            for m in re.finditer(d, metin, re.I):
                parca = metin[max(0, m.start() - 20): m.end() + 20].replace("\n", " ")
                if any(i in parca.lower() for i in izinli):
                    continue
                bulunan.append("%s: «%s» → %s" % (rel, m.group(0), neden))
                break
    if not metinler(c):
        return [G("yasakli", OLCULEMEDI, "taranacak metin dosyası yok")]
    return [G("yasakli", KALDI if bulunan else GECTI, "; ".join(bulunan[:4]) if bulunan else "yasaklı çıktı yok")]


def k_zorunlu(c):
    z = c["vaka"]["beklenen"].get("zorunlu", [])
    if not z:
        return []
    corpus = "\n".join(m for _, m in metinler(c))
    yok = [d for d in z if not re.search(d, corpus, re.I)]
    return [G("zorunlu_metin", KALDI if yok else GECTI, ("çıktıda yok: " + ", ".join(yok)) if yok else "tamam")]


def k_ayar_beklenen(c, ayar, ad="ayar"):
    sorun = []
    for k, b in c["vaka"]["beklenen"].get("ayar", {}).items():
        d = ayar.get(k)
        if isinstance(b, str) and b.startswith("!"):
            if d == b[1:]:
                sorun.append("%s=%r olmamalı" % (k, d))
        elif d != b:
            sorun.append("%s=%r (beklenen %r)" % (k, d, b))
    return [G(ad + "_beklenen", KALDI if sorun else GECTI, "; ".join(sorun) if sorun else "tamam")] if c["vaka"]["beklenen"].get("ayar") else []


def k_kart(c, yol, ad="on_uretim_karti"):
    if not os.path.isfile(yol):
        return [G(ad, KALDI, "kart dosyası yok: " + os.path.basename(yol))]
    rc, o, e = py(os.path.join(STUDIO, "on_uretim_karti.py"), "kontrol", yol)
    sonuc = [G(ad, GECTI if rc == 0 else KALDI, son(o + e))]
    try:
        kart = oku_json(yol)
    except ValueError:
        return sonuc
    sorun = []
    if kart.get("pazar") != c["vaka"]["pazar"]:
        sorun.append("kart pazarı %r ≠ vaka pazarı %r" % (kart.get("pazar"), c["vaka"]["pazar"]))
    for k, b in c["vaka"]["beklenen"].get("kart", {}).items():
        if k == "tatmin_ani_dolu":
            if b and not str(kart.get("tatmin_ani") or "").strip():
                sorun.append("kartta tatmin_ani/kanıt anı boş")
        elif kart.get(k) != b:
            sorun.append("kart.%s=%r (beklenen %r)" % (k, kart.get(k), b))
    sonuc.append(G(ad + "_vaka", KALDI if sorun else GECTI, "; ".join(sorun) if sorun else "pazar ve kart beklentisi tamam"))
    return sonuc


def medya(yol):
    import ffaraclar as F
    return F.medya_bilgi(yol)


def k_sure_cozunurluk(c, video):
    b = c["vaka"]["beklenen"]
    out = []
    try:
        m = medya(video)
    except SystemExit as e:
        return [G("sure", OLCULEMEDI, "ffmpeg yok: %s" % e)]
    except Exception as e:  # noqa: BLE001
        return [G("sure", KALDI, "video okunamadı: %s" % e)]
    lo, hi = b["sure_sn"]
    out.append(G("sure", GECTI if lo - 0.1 <= m["sure"] <= hi + 0.1 else KALDI, "%.2f sn (beklenen %s–%s)" % (m["sure"], lo, hi)))
    if b.get("cozunurluk"):
        w, h = b["cozunurluk"]
        out.append(G("cozunurluk", GECTI if (m["w"], m["h"]) == (w, h) else KALDI, "%sx%s (beklenen %sx%s)" % (m["w"], m["h"], w, h)))
    return out


def k_ses(c, video, stem, drop=None, drop_gerekli=True):
    """ses_olc.py --kapi (müzik girişi, delik, sıçrama) + −14 ±1 LUFS + tepe ≤ −1 dBTP + drop artışı ≥ 6 dB."""
    if not os.path.isfile(stem):
        return [G("ses_kapi", KALDI, "müzik stem'i yok (SES-02 müziksiz teslim yok): " + os.path.basename(stem))]
    cmd = [video, "--muzik_stem", stem, "--kapi"] + (["--drop", str(drop)] if drop else [])
    rc, o, e = py(os.path.join(CUT, "ses_olc.py"), *cmd)
    out = [G("ses_kapi", GECTI if rc == 0 else KALDI, "çıkış %d %s" % (rc, son(e)))]
    try:
        r = json.loads(o)
    except ValueError:
        return out + [G("ses_seviye", KALDI, "ses_olc çıktısı okunamadı")]
    sorun = []
    if abs(r["I_lufs"] + 14.0) > 1.0:
        sorun.append("%.1f LUFS (−14 ±1)" % r["I_lufs"])
    if r["true_peak_dbtp"] > -1.0:
        sorun.append("tepe %.1f dBTP (> −1)" % r["true_peak_dbtp"])
    if drop_gerekli and drop:
        if r.get("drop_artis_db") is None or r["drop_artis_db"] < 6.0:
            sorun.append("drop artışı %s dB (< 6)" % r.get("drop_artis_db"))
    out.append(G("ses_seviye", KALDI if sorun else GECTI, "; ".join(sorun) if sorun else "LUFS %.1f · tepe %.1f dBTP · drop %s dB" % (
        r["I_lufs"], r["true_peak_dbtp"], r.get("drop_artis_db"))))
    return out


def k_goruntu(c, video, kesimler=None, ayar=None):
    cmd = [os.path.join(CUT, "kurgu_kontrol.py"), "--goruntu", video]
    if kesimler is not None:
        cmd += ["--kesimler", ",".join(str(x) for x in kesimler), "--yalniz-goruntu"]
    elif ayar:
        cmd.insert(1, ayar)
    rc, o, e = kos([sys.executable] + cmd)
    return [G("goruntu", GECTI if rc == 0 else KALDI, "çıkış %d %s" % (rc, son(o + e)))]


# ------------------------------------------------------------------ jüri
def referanslar(ozellik):
    yol = os.path.join(SINAV, ozellik, "referanslar.tsv")
    if not os.path.isfile(yol):
        return []
    with open(yol, encoding="utf-8", newline="") as f:
        return [s for s in csv.DictReader(f, delimiter="\t") if (s.get("id") or "").strip() and not (s["id"].startswith("#"))]


PAZAR_UYUM = {"US": {"US"}, "TR": {"TR"}, "DE": {"DE", "UK", "FR", "ES", "US"}, "UK": {"UK", "DE", "FR", "ES", "US"},
              "FR": {"DE", "UK", "FR", "ES", "US"}, "ES": {"DE", "UK", "FR", "ES", "US"}}


def juri_modulu():
    ad = os.path.join(CUT, "juri.py")
    sp = importlib.util.spec_from_file_location("juri_mod", ad)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def k_juri(c, bizim_yol, mod, tur):
    """Kör jüri şartı: bizim çıktı + ≥3 referans; medyan toplam ≥ referans medyanı − 1 (juri.py'nin kendi eşikleri de geçerli).
    Pano yoksa hazırlanır (bir kez; yeniden koşuda eşleşme DEĞİŞTİRİLMEZ); KOR-<n>.json kopyalar gelince hüküm verilir."""
    jd = os.path.join(c["d"], "juri")
    pazar = c["vaka"]["pazar"]
    adaylar = [r for r in referanslar(c["ozellik"]) if (r.get("tur") or "").strip() == tur and (r.get("pazar") or "").strip() in PAZAR_UYUM.get(pazar, {pazar})
               and (r.get("kare_panosu_yolu") or "").strip()]
    J = juri_modulu()
    if not os.path.isfile(J.esleme_yolu(jd)):
        kok = c["args"].referans_kok or os.environ.get("SINAV_REFERANS_KOK")
        cozulen = []
        for r in adaylar:
            y = r["kare_panosu_yolu"].strip()
            yol = y if os.path.isabs(y) else (os.path.join(kok, y) if kok else None)
            if yol and os.path.exists(yol):
                cozulen.append((r["id"], yol))
        if len(cozulen) < 3:
            return [G("juri", OLCULEMEDI, "referans yuvası dolu değil: pazar %s için %d/3 çözülen kare panosu (referanslar.tsv'yi doldur; "
                      "--referans-kok %s)" % (pazar, len(cozulen), "verilmedi" if not kok else "verildi"))]
        if not os.path.exists(bizim_yol):
            return [G("juri", KALDI, "jüriye girecek çıktı yok: " + os.path.basename(bizim_yol))]
        os.makedirs(jd, exist_ok=True)
        cmd = [os.path.join(CUT, "juri.py"), "pano", "--cikti", jd, "--mod", mod, "--bizim", "SINAV=" + bizim_yol,
               "--baglam", "sınav vakası (%s), adsız pano" % c["ozellik"]]
        if tur in ("video", "kanca"):   # referanslar uygulama ekran kaydı: hesap adı/sayaç şeridi bizim dahil HER ögede kapanır (#1)
            cmd.append("--arayuz-maske")
        for _, y in cozulen:
            cmd += ["--referans", y]
        rc, o, e = kos([sys.executable] + cmd)
        if rc:
            return [G("juri", KALDI, "juri.py pano çıkış %d %s" % (rc, son(o + e)))]
    def en_yeni(y):
        if os.path.isdir(y):
            return max([os.path.getmtime(x) for x in glob.glob(os.path.join(y, "**", "*"), recursive=True) if os.path.isfile(x)] or [0])
        return os.path.getmtime(y) if os.path.exists(y) else 0
    if en_yeni(bizim_yol) > os.path.getmtime(J.esleme_yolu(jd)) + 1:
        return [G("juri", BEKLIYOR, "çıktı panodan sonra değişmiş: eski kör kopyalar geçersiz; `%s` klasörünü sil ve yeniden koş (pano yeniden hazırlanır)" % jd)]
    try:
        es = J.esleme_oku(jd)
        kodlar = sorted(es["ogeler"])
        gecerli, gecersiz = J.kopyalari_oku(jd, es)
    except SystemExit as e:
        return [G("juri", KALDI, str(e))]
    if len(gecerli) < J.MIN_KOPYA:
        return [G("juri", BEKLIYOR, "pano hazır (%s/kopya-1..3/pano); %d/%d geçerli bağımsız kör kopya (kopya-<n>/KOR-<n>.json) — jüri ajanını 3 kez, her biri kendi klasörüyle çalıştır%s" % (
            jd, len(gecerli), J.MIN_KOPYA, ("; geçersiz: " + "; ".join(gecersiz[:2])) if gecersiz else ""))]
    oz = J.ozetle(gecerli, kodlar)
    bizim = [k for k in kodlar if es["ogeler"][k]["tur"] == "bizim"]
    ref = sorted(oz[k]["toplam"] for k in kodlar if es["ogeler"][k]["tur"] == "referans")
    if not bizim or len(ref) < 3:
        return [G("juri", KALDI, "pano bizim/referans yapısı bozuk")]
    import statistics
    med = statistics.median(ref)
    t = oz[bizim[0]]["toplam"]
    rc, o, e = py(os.path.join(CUT, "juri.py"), "birlestir", jd, "--tur", "1", "--proje", c["d"])
    nedenler = []
    if t < med - 1.0:
        nedenler.append("toplam %.1f < referans medyanı %.1f − 1" % (t, med))
    if rc != 0:
        nedenler.append("juri.py kendi kapısı KALDI: " + son(o + e, 160))
    return [G("juri", KALDI if nedenler else GECTI, "; ".join(nedenler) if nedenler else "toplam %.1f ≥ referans medyanı %.1f − 1; juri.py GEÇTİ" % (t, med))]


# ------------------------------------------------------------------ 07 site: iç dil / kanıt anı sızıntısı, mobil ekran
KANIT_SIZINTI = [
    (r"^\s*#{1,6}\s*(the moment|der moment|le moment|el momento|the proof|proof moment|kanıt(\s+anı)?|beweis(moment)?)\s*$", "bölüm başlığı iç terim (kanıt anı)"),
    (r"\bkanıt anı\b|\bkanit_ani\b|\bproof moment\b|\bBeweismoment\b", "iç terim: kanıt anı"),
    (r"(?:^|[.!?\n])\s*Kanıt\b", "cümle 'Kanıt' etiketiyle başlıyor (iç dil)"),
]


def k_kanit_sizinti(c):
    """Vaka `girdi.kanit_ani` bir ÇEKİM TALİMATIDIR (görsel brif); site metnine cümlesiyle ya da iç etiketiyle ('Kanıt', 'Der Moment') girerse KALDI.
    Denetim 2026-11-25 #6: bu kapı yokken 07 tur1 b-zor ve c-tuzak iç dille geçmişti."""
    metin = {rel: m for rel, m in metinler(c) if rel.split(os.sep)[0] == "site"}
    if not metin:
        return [G("kanit_ani_sizinti", OLCULEMEDI, "site/*.md yok")]
    bulunan = []
    for rel, m in metin.items():
        for d, neden in KANIT_SIZINTI:
            mm = re.search(d, m, re.I | re.M)
            if mm:
                bulunan.append("%s: «%s» → %s" % (rel, mm.group(0).strip()[:40], neden))
    ani = (c["vaka"].get("girdi") or {}).get("kanit_ani") or ""
    govde = re.sub(r"\s+", " ", " ".join(metin.values()).lower())
    for parca in re.split(r"[;:()=]|, ", ani.lower()):
        parca = re.sub(r"\s+", " ", parca).strip(" .")
        if len(parca.split()) >= 4 and parca in govde:
            bulunan.append("vaka kanit_ani cümlesi site metninde aynen: «%s»" % parca[:60])
    return [G("kanit_ani_sizinti", KALDI if bulunan else GECTI, "; ".join(bulunan[:4]) if bulunan else "kanıt anı cümlesi/iç terim sitede yok")]


def k_mobil_ekran(c):
    """ekran/<ad>.html + <ad>-390.png çiftleri `mobil_ekran.py kontrol` ile: geniş pencerede 390 px iframe düzeniyle aynı mı (yöntem hatası/taşma → KALDI)."""
    ciftler = [(h, os.path.splitext(h)[0] + "-390.png") for h in sorted(glob.glob(os.path.join(c["d"], "ekran", "*.html")))]
    ciftler = [(h, p) for h, p in ciftler if os.path.isfile(p)]
    if not ciftler:
        return [G("mobil_ekran", OLCULEMEDI, "ekran/ altında <ad>.html + <ad>-390.png çifti yok (mobil ekran ölçülemedi)")]
    sonuc = []
    for h, p in ciftler:
        rc, o, e = py(os.path.join(ORTAK, "mobil_ekran.py"), "kontrol", h, p)
        sonuc.append((os.path.basename(p), rc, next((l for l in (o + e).splitlines() if l.startswith(("MOBİL", "TASMA", "OLCULEMEDI"))), son(o + e, 100))[:100]))
    if any(rc == 1 for _, rc, _ in sonuc):
        return [G("mobil_ekran", KALDI, "; ".join("%s: %s" % (a, m) for a, rc, m in sonuc if rc == 1)[:300])]
    if any(rc != 0 for _, rc, _ in sonuc):
        return [G("mobil_ekran", OLCULEMEDI, "Chrome yok ya da ekran alınamadı: " + sonuc[0][2])]
    return [G("mobil_ekran", GECTI, "%d mobil ekran 390 px iframe düzeniyle aynı" % len(sonuc))]


def k_web_olcum(c):
    """hiz_cwv + erisim_wcag (denetim #22): üretilen HTML'de yerel Lighthouse + axe (ortak/web_olcum.py). Hedef: <vaka>/canli-url.txt (ilk satır, canlı
    mağaza varsa) yoksa ekran/*.html ve site/*.html ('yerel' etiketi: laboratuvar ölçümü, canlı mağaza ve alan verisi yerine geçmez).
    Araç/Chrome yoksa ya da HTML yoksa olculemedi (sahte geçti yok). Koşu sayısı: SINAV_WEB_KOSU (varsayılan 3, hız medyanı)."""
    d = c["d"]
    hedefler, etiket = [], "yerel"
    canli = os.path.join(d, "canli-url.txt")
    if os.path.isfile(canli):
        satirlar = [x.strip() for x in open(canli, encoding="utf-8") if x.strip() and not x.startswith("#")]
        hedefler, etiket = [x for x in satirlar if x.startswith(("http://", "https://"))], "canlı"
    if not hedefler:
        hedefler = sorted(glob.glob(os.path.join(d, "ekran", "*.html")) + glob.glob(os.path.join(d, "site", "*.html")))
        etiket = "yerel"
    ad_hiz, ad_erisim = "hiz_cwv", "erisim_wcag"
    if not hedefler:
        yok = "ölçülecek HTML yok (ekran/*.html ya da site/*.html; canlı mağaza varsa canli-url.txt): ölçülemedi"
        return [G(ad_hiz, OLCULEMEDI, yok), G(ad_erisim, OLCULEMEDI, yok)]
    kosu = os.environ.get("SINAV_WEB_KOSU", "3")
    out = []
    for kapi, mod in ((ad_hiz, "hiz"), (ad_erisim, "erisim")):
        rc, o, e = py(os.path.join(ORTAK, "web_olcum.py"), mod, *hedefler, "--kosu", kosu)
        ozet = " | ".join(l.strip() for l in o.splitlines() if l.strip().startswith(("hiz ", "erisim ", "ÖLÇÜLEMEDİ", "WEB ÖLÇÜM")) )
        durum = {0: GECTI, 1: KALDI}.get(rc, OLCULEMEDI)
        out.append(G(kapi, durum, "[%s] çıkış %d %s" % (etiket, rc, son(ozet or (o + e), 330))))
    return out


# ------------------------------------------------------------------ üreten ≠ denetleyen (denetim #2/#4: ortak/rapor-sablonu.md)
RAPOR_DESENLERI = ("SADAKAT.md", "KAPI.md", "OCR.md", "DUZELTME.md", "ELESTIRI*.md", "KOR-*.md", "SES-*.md", "HIZ.md", "ERISIM.md", "ARAMA.md")
KIM_DENETLEDI = re.compile(r"^[\s>*_`#-]*K[İIi]M\s+DENETLED[İIi][\s*_`]*[:：]\s*(.*?)\s*$", re.I | re.M)
URETEN = re.compile(r"^[\s>*_`#-]*(?:ÜRETEN|URETEN)[\s*_`]*[:：]\s*(.*?)\s*$", re.I | re.M)


def _buyuk(x):
    return x.replace("i", "İ").replace("ı", "I").upper().replace("Ö", "O").replace("İ", "I").replace("Ü", "U").replace("Ş", "S").replace("Ğ", "G").replace("Ç", "C")


def k_denetleyen(c):
    """Kapı raporlarında (SADAKAT/KAPI/OCR/ELESTIRI/KOR/SES…) `KİM DENETLEDİ:` satırı: yok ya da `ÖZ-DENETİM` (ya da denetleyen = ÜRETEN) → olculemedi
    (üreten kendi işini ölçmüş olamaz: 05 tur1 SADAKAT ✅'lerini üreten ajan yazmıştı); bağımsız rol adı varsa GEÇTİ. Rapor dosyası yoksa kapı yok (uygulanmaz)."""
    d = c["d"]
    dosyalar = sorted({y for p in RAPOR_DESENLERI for y in glob.glob(os.path.join(d, p)) + glob.glob(os.path.join(d, "*", p))})
    if not dosyalar:
        return []
    sorun, iyi = [], []
    for y in dosyalar:
        rel = os.path.relpath(y, d)
        with open(y, encoding="utf-8", errors="replace") as f:
            metin = f.read()
        m = KIM_DENETLEDI.search(metin)
        if not m or not m.group(1).strip():
            sorun.append("%s: KİM DENETLEDİ satırı yok" % rel)
            continue
        kim = m.group(1).strip()
        u = URETEN.search(metin)
        if re.search(r"OZ[- ]?DENETIM", _buyuk(kim)) or (u and _buyuk(u.group(1)).strip() == _buyuk(kim).strip()):
            sorun.append("%s: ÖZ-DENETİM (üreten = denetleyen)" % rel)
        else:
            iyi.append("%s: %s" % (rel, kim[:30]))
    if sorun:
        return [G("kim_denetledi", OLCULEMEDI, "bağımsız denetleyen kayıtlı değil — %s (geçti sayılmaz; üreten ölçmez)" % "; ".join(sorun[:4]))]
    return [G("kim_denetledi", GECTI, "%d raporda bağımsız denetleyen: %s" % (len(iyi), "; ".join(iyi[:3])))]


# ------------------------------------------------------------------ özellik kapıları
def f01(c):
    d, v = c["d"], c["vaka"]
    out = k_dosyalar(c)
    if out[0]["durum"] == KALDI:
        return out
    ayar_yol = os.path.join(d, "ayar.json")
    ayar = oku_json(ayar_yol)
    out += k_kart(c, os.path.join(d, "on_uretim_karti.json"))
    out += k_ayar_beklenen(c, ayar)
    cmd = [ayar_yol, "--video", os.path.join(d, "video.mp4")]
    mp = os.path.join(d, "magaza-paketi.json")
    if os.path.isfile(mp):
        cmd += ["--magaza-paketi", mp]
    rc, o, e = py(os.path.join(CUT, "kurgu_kontrol.py"), *cmd)
    out.append(G("kurgu_kontrol", GECTI if rc == 0 else KALDI, son("\n".join(s for s in (o + e).splitlines() if s.startswith(("HATA", "özet"))) or o + e)))
    out += k_goruntu(c, os.path.join(d, "video.mp4"), ayar=ayar_yol)
    out += k_ses(c, os.path.join(d, "video.mp4"), os.path.join(d, "muz_stem.wav"), ayar.get("drop_sn", 3.429))
    out += k_sure_cozunurluk(c, os.path.join(d, "video.mp4"))
    # ICE-01: organik videoda ekranda fiyat yok (yalnız ekrana basılan metin: ayar yazıları)
    if v.get("kreatif", "organik") == "organik":
        import paket
        fiyat = re.compile(r"([$€£₺]\s?\d)|(\d[\d.,]*\s?(tl|usd|eur|dollars?)\b)|(\d+\s?%\s?(off|indirim))|(\bfiyat)", re.I)
        ihlal = [m for _, m in paket.ayar_yazilari(ayar) if fiyat.search(m)]
        out.append(G("ice01_fiyat", KALDI if ihlal else GECTI, ("ekranda fiyat: %s" % ihlal[:2]) if ihlal else "ekranda fiyat yok"))
    out += k_yasakli(c) + k_zorunlu(c)
    out += k_juri(c, os.path.join(d, "video.mp4"), "teslim", "video")
    return out


def f02(c):
    d = c["d"]
    out = k_dosyalar(c)
    if out[0]["durum"] == KALDI:
        return out
    out += k_kart(c, os.path.join(d, "on_uretim_karti.json"))
    with tempfile.TemporaryDirectory(prefix="sinav02_") as t:  # betikler yanına dosya yazar: çıktıyı kirletme
        for ad in ("senaryolar.json", "kancalar.json", "ayar.json", "on_uretim_karti.json"):
            if os.path.isfile(os.path.join(d, ad)):
                shutil.copy(os.path.join(d, ad), t)
        sen = oku_json(os.path.join(t, "senaryolar.json"))
        n = len(sen.get("videolar", []))
        lo = c["vaka"]["beklenen"].get("senaryo_adedi", 30)
        rc, o, e = py(os.path.join(STUDIO, "senaryo_kontrol.py"), os.path.join(t, "senaryolar.json"))
        out.append(G("senaryo_kontrol", GECTI if rc == 0 else KALDI, son("\n".join(s for s in o.splitlines() if s.startswith("❌") or s.startswith("SONUÇ")) or o + e)))
        out.append(G("senaryo_adedi", GECTI if n >= lo else KALDI, "%d senaryo (en az %d)" % (n, lo)))
        if sen.get("pazar") and sen["pazar"] != c["vaka"]["pazar"]:
            out.append(G("senaryo_pazar", KALDI, "senaryolar.json pazar %r ≠ vaka %r" % (sen["pazar"], c["vaka"]["pazar"])))
        rc, o, e = py(os.path.join(CUT, "kanca_varyasyon.py"), os.path.join(t, "ayar.json"), os.path.join(t, "kancalar.json"))
        out.append(G("kanca_varyasyon", GECTI if rc == 0 else KALDI, son(o + e)))
    out += k_yasakli(c) + k_zorunlu(c)
    out += k_juri(c, os.path.join(d, "onuretim"), "onuretim", "kanca")
    return out


def f03(c):
    d = c["d"]
    out = k_dosyalar(c)
    if out[0]["durum"] == KALDI:
        return out
    ayar_yol = os.path.join(d, "ayar.json")
    ayar = oku_json(ayar_yol)
    kart_ad = ayar.get("on_uretim_karti") or "on-uretim-karti.json"
    out += k_kart(c, os.path.join(d, kart_ad))
    rc, o, e = py(os.path.join(CUT, "hikaye", "hikaye_kur.py"), ayar_yol, "--dogrula")
    out.append(G("hikaye_kur_dogrula", GECTI if rc == 0 else KALDI, "çıkış %d %s" % (rc, son(o + e))))
    video = os.path.join(d, "video.mp4")
    out += k_sure_cozunurluk(c, video)
    out += k_ses(c, video, os.path.join(d, "muz_stem.wav"), (ayar.get("ses") or {}).get("drop"))
    out += k_goruntu(c, video, kesimler=ayar.get("kesimler", []))
    out += k_yasakli(c) + k_zorunlu(c)
    out += k_juri(c, video, "teslim", "video")
    return out


def f04(c):
    d = c["d"]
    out = k_dosyalar(c)
    if out[0]["durum"] == KALDI:
        return out
    ses = oku_json(os.path.join(d, "ses.json"))
    out += k_ses(c, os.path.join(d, "video.mp4"), os.path.join(d, "muz_stem.wav"), ses.get("drop_sn"), drop_gerekli=True)
    out += k_sure_cozunurluk(c, os.path.join(d, "video.mp4"))
    lis = open(os.path.join(d, "LISANS.md"), encoding="utf-8").read()
    sorun = []
    if not re.search(r"Kurucu seçti:.*söz kapısı:\s*(temiz|enstrümantal)", lis, re.I):
        sorun.append("\"Kurucu seçti: <tarih>, söz kapısı: temiz | enstrümantal\" satırı yok")
    if not re.search(r"https?://|kullanıcının dosyası|sentetik", lis, re.I):
        sorun.append("kaynak (URL / kullanıcının dosyası / sentetik) yok")
    if not re.search(r"CC0|SFX Free|Mixkit|Pixabay|kullanıcının dosyası|sentetik|royalty|lisans", lis, re.I):
        sorun.append("lisans adı yok")
    for k in c["vaka"].get("telifli_parca", []):
        if re.search(k, lis, re.I):
            sorun.append("telifli parça kaydı: %s (SES-02)" % k)
    out.append(G("lisans_kaydi", KALDI if sorun else GECTI, "; ".join(sorun) if sorun else "tamam"))
    out += k_yasakli(c) + k_zorunlu(c)
    out.append(G("juri", UYGULANMAZ, "jüri sesi dinleyemez (OLCUT.md §ii); ses kapısı ölçümdür, kulak onayı kullanıcıdadır"))
    return out


def f05(c):
    from PIL import Image, ImageChops
    d = c["d"]
    out = k_dosyalar(c)
    if out[0]["durum"] == KALDI:
        return out
    stil = oku_json(os.path.join(d, "stil.json"))
    hexz = stil["zemin"].lstrip("#")
    hedef = tuple(int(hexz[i:i + 2], 16) for i in (0, 2, 4))
    gdir = os.path.join(d, "gorseller")
    olcu = c["vaka"]["beklenen"]["gorsel_olcusu"]
    sorun, sayi = [], {k: 0 for k in olcu}
    for yol in sorted(glob.glob(os.path.join(gdir, "*"))):
        ad = os.path.basename(yol).lower()
        if not ad.endswith((".png", ".jpg", ".jpeg")):
            continue
        tip = next((k for k in olcu if ad.startswith(k)), None)
        if tip is None:
            sorun.append("%s: ad galeri-/g0-/b1-/b2- ile başlamıyor" % ad)
            continue
        sayi[tip] += 1
        im = Image.open(yol).convert("RGB")
        w, h = im.size
        o = olcu[tip]
        if o.get("kare") and w != h:
            sorun.append("%s: 1:1 değil (%dx%d)" % (ad, w, h))
        if o.get("boyut") and [w, h] != o["boyut"]:
            sorun.append("%s: %dx%d (beklenen %s)" % (ad, w, h, "x".join(map(str, o["boyut"]))))
        if o.get("min_kenar") and min(w, h) < o["min_kenar"]:
            sorun.append("%s: %dx%d < %d px" % (ad, w, h, o["min_kenar"]))
        koseler = [im.getpixel(p) for p in ((4, 4), (w - 5, 4), (4, h - 5), (w - 5, h - 5))]
        if any(max(abs(a - b) for a, b in zip(k, hedef)) > 3 for k in koseler):
            sorun.append("%s: köşe rengi zemin HEX'inden ±3 dışında (K3)" % ad)
        fark = ImageChops.difference(im, Image.new("RGB", im.size, hedef)).convert("L").point(lambda x: 255 if x > 18 else 0)
        bb = fark.getbbox()
        if not bb:
            sorun.append("%s: boş kadraj (içerik yok)" % ad)
            continue
        pay = min(bb[0] / w, bb[1] / h, (w - bb[2]) / w, (h - bb[3]) / h)
        if pay < 0.06:
            sorun.append("%s: kenar payı %.3f < 0,06 (kritik 5)" % (ad, pay))
        if tip == "g0":
            uzun = max((bb[2] - bb[0]) / w, (bb[3] - bb[1]) / h)
            if not 0.75 <= uzun <= 0.86:
                sorun.append("%s: G0 ürün uzun kenarı %%%.0f (beklenen %%75–86)" % (ad, uzun * 100))
    for k, o in olcu.items():
        if sayi[k] < o.get("en_az", 1):
            sorun.append("%s: %d dosya (en az %d)" % (k, sayi[k], o.get("en_az", 1)))
    out.append(G("K3_tuval_olcu", KALDI if sorun else GECTI, "; ".join(sorun[:5]) if sorun else "boyut · zemin HEX ±3 · kenar payı ≥ %6 tamam"))
    # K2 yazım: ocr_kontrol.py (yan dosya <ad>.txt = beklenen metin); OCR motoru yoksa olculemedi
    ocr_rc, ocr_say, ocr_not = [], 0, []
    for yol in sorted(glob.glob(os.path.join(gdir, "*.txt"))):
        gorsel = next((g for g in glob.glob(os.path.splitext(yol)[0] + ".*") if g.lower().endswith((".png", ".jpg", ".jpeg"))), None)
        if not gorsel:
            continue
        rc, o, e = py(os.path.join(GORSEL, "ocr_kontrol.py"), gorsel, yol)
        ocr_rc.append(rc)
        ocr_say += 1
        if rc: ocr_not.append("%s→%d" % (os.path.basename(gorsel), rc))
    if not ocr_say:
        out.append(G("K2_yazim_ocr", OLCULEMEDI, "görsel yanında beklenen metin dosyası (<ad>.txt) yok"))
    elif 1 in ocr_rc:
        out.append(G("K2_yazim_ocr", KALDI, "OCR eksik/fazla yazı: " + ", ".join(ocr_not)))
    elif 2 in ocr_rc:
        out.append(G("K2_yazim_ocr", OLCULEMEDI, "OCR çalışmadı ya da Türkçe harf (İ Ö Ş Ğ Ü Ç) doğrulanamadı (Tesseract yok): hata bulunmadı ama ölçülemedi; gözle kontrol sentinel `yazim` işi"))
    else:
        out.append(G("K2_yazim_ocr", GECTI, "%d görsel OCR ile beklenen metne uydu (göz kontrolü yine de gerekir)" % ocr_say))
    rapor = os.path.join(d, "SADAKAT.md")
    if os.path.isfile(rapor) and "❌" in open(rapor, encoding="utf-8").read():
        out.append(G("K1_sadakat", KALDI, "SADAKAT.md'de ❌ var (sentinel raporu)"))
    else:
        out.append(G("K1_sadakat", OLCULEMEDI, "ürün sadakati betikle ölçülmez (sentinel `kilit` gözle); rapor temiz olsa da geçti sayılmaz"))
    out += k_yasakli(c) + k_zorunlu(c)
    out += k_juri(c, gdir, "teslim", "gorsel")
    return out


def f06(c):
    d, v = c["d"], c["vaka"]
    out = k_dosyalar(c)
    if out[0]["durum"] == KALDI:
        return out
    tr = v["pazar"] == "TR"
    with tempfile.TemporaryDirectory(prefix="sinav06_") as t:
        if tr:
            kopya = os.path.join(t, "adaylar.tsv")
            shutil.copy(os.path.join(d, "adaylar.tsv"), kopya)
            rc, o, e = py(os.path.join(TRENDYOL, "trendyol_kontrol.py"), "denetle", kopya)
            out.append(G("trendyol_denetle", GECTI if rc == 0 else KALDI, "çıkış %d %s" % (rc, son(o + e))))
        else:
            kopya = os.path.join(t, "adaylar.md")
            shutil.copy(os.path.join(d, "adaylar.md"), kopya)
            rc, o, e = py(os.path.join(HUNTER, "firsat_kontrol.py"), "denetle", kopya)
            out.append(G("firsat_denetle", GECTI if rc == 0 else KALDI, "çıkış %d %s" % (rc, son(o + e))))
    metin = open(os.path.join(d, "adaylar.tsv" if tr else "adaylar.md"), encoding="utf-8").read()
    anahtar = v["beklenen"]["urun_anahtar"]
    out.append(G("vaka_urunu_listede", GECTI if re.search(anahtar, metin, re.I) else KALDI, "aranan: %s" % anahtar))
    out += k_yasakli(c) + k_zorunlu(c)
    out.append(G("juri", UYGULANMAZ, "ürün kararı kanıt kapısıdır (denetle + kanıt dosyası); zevk jürisi yok (OLCUT.md §ii)"))
    return out


def f07(c):
    d = c["d"]
    out = k_dosyalar(c)
    if out[0]["durum"] == KALDI:
        return out
    metinler_ = sorted(glob.glob(os.path.join(d, "site", "*.md")))
    rc, o, e = py(os.path.join(ORTAK, "paket.py"), "iddia-kontrol", os.path.join(d, "magaza-paketi.json"), *metinler_)
    out.append(G("iddia_kontrol", GECTI if rc == 0 else KALDI, "çıkış %d %s" % (rc, son(o + e))))
    out += k_yasakli(c) + k_zorunlu(c)
    # #17: sözleşme kapısı: fiyat 0 / yer tutucu / kaynaksız marka adı KALDI; dürüst `null + eksik[]` geçer ama site tamam sayılmaz (olculemedi)
    rc, o, e = py(os.path.join(ORTAK, "paket.py"), "dogrula", "magaza", os.path.join(d, "magaza-paketi.json"))
    eksik = next((l.strip() for l in o.splitlines() if "EKSİK:" in l), "")
    out.append(G("paket_sozlesme", KALDI if rc else (OLCULEMEDI if eksik else GECTI),
                 "çıkış %d %s" % (rc, son(("; ".join(l.strip() for l in o.splitlines() if l.startswith("HATA")) or eksik or o + e), 300))))
    out += k_kanit_sizinti(c) + k_mobil_ekran(c)
    out += k_web_olcum(c)
    for kapi, kim in (("arama_merchant", "probe `arama`: arama/Merchant/yapay zekâ araması (canlı sayfa gerekir)"),
                      ("donusum_kullanilabilirlik", "shopper `donusum`: müşteri gözü denetimi (ajan yargısı; betik yok)")):
        out.append(G(kapi, OLCULEMEDI, "ölçen betik depoda yok — " + kim))
    out += k_juri(c, os.path.join(d, "ekran"), "teslim", "site")
    return out


KAPILAR = {"01-urun-videosu": f01, "02-kanca-senaryo": f02, "03-hikaye-videosu": f03, "04-ses-muzik": f04,
           "05-gorsel": f05, "06-urun-avi": f06, "07-site": f07}


# ------------------------------------------------------------------ koşu
def vaka_durumu(kapilar):
    d = [k["durum"] for k in kapilar]
    if KALDI in d:
        return KALDI
    if OLCULEMEDI in d:
        return OLCULEMEDI
    if BEKLIYOR in d:
        return BEKLIYOR
    return GECTI


def ozellik_coz(ad):
    for o in OZELLIKLER:
        if o == ad or o.startswith(ad.rstrip("-") + "-") or o.split("-")[0] == ad:
            return o
    sys.exit("HATA: bilinmeyen özellik %r (seçenekler: %s)" % (ad, ", ".join(OZELLIKLER)))


def vakalari_oku(ozellik):
    yollar = sorted(glob.glob(os.path.join(SINAV, ozellik, "vakalar", "*", "vaka.json")))
    if not yollar:
        sys.exit("HATA: vaka yok: %s" % os.path.join(SINAV, ozellik, "vakalar"))
    return [(os.path.basename(os.path.dirname(y)), oku_json(y)) for y in yollar]


def sonuc_yaz(yol, ozellik, cikti, sonuclar, genel):
    ref = referanslar(ozellik)
    dolu = [r for r in ref if (r.get("kare_panosu_yolu") or "").strip()]
    s = ["# Sınav sonucu · %s" % ozellik, "",
         "Tarih: %s · çıktı klasörü: `%s` · koşucu: `scripts/sinav_kos.py`" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), cikti),
         "Genel durum: **%s** (0 = hepsi GEÇTİ · 1 = KALDI var · 3 = KALDI yok ama olculemedi/bekliyor var)" % genel, "",
         "| Vaka | Pazar | Durum |", "|---|---|---|"]
    for vid, v, kapilar in sonuclar:
        s.append("| %s | %s | **%s** |" % (vid, v["pazar"], vaka_durumu(kapilar)))
    for vid, v, kapilar in sonuclar:
        s += ["", "## %s (%s · %s)" % (vid, v.get("urun", ""), v["pazar"]), "", "| Kapı | Durum | Ayrıntı |", "|---|---|---|"]
        for k in kapilar:
            s.append("| %s | %s | %s |" % (k["kapi"], k["durum"], k["ayrinti"].replace("|", "/")))
    s += ["", "## Referans yuvaları", "",
          "`referanslar.tsv`: %d satır, %d tanesinde `kare_panosu_yolu` dolu." % (len(ref), len(dolu)),
          "Jüri en az 3 pazar-uyumlu, tür-uyumlu, yolu çözülen referans ister; eksikse kapı `olculemedi` kalır."]
    with open(yol, "w", encoding="utf-8") as f:
        f.write("\n".join(s) + "\n")


def kos_ozellik(a, ozellik, cikti, sonuc_yolu=None, sessiz=False):
    """Bir özelliğin vakalarını koşar, SONUC.md yazar. Döner: (çıkış 0/1/3, [(vaka, durum)], sonuclar)."""
    sonuclar = []
    for vid, v in vakalari_oku(ozellik):
        if a.vaka and vid not in a.vaka:
            continue
        d = os.path.join(cikti, vid)
        c = {"ozellik": ozellik, "vaka": v, "d": d, "args": a}
        if not os.path.isdir(d) or not os.listdir(d):
            kapilar = [G("cikti", KALDI, "vaka çıktısı yok ya da klasör boş: %s (boş klasör geçti sayılmaz)" % d)]
        else:
            try:
                kapilar = KAPILAR[ozellik](c)
                kapilar += k_denetleyen(c)
            except Exception as e:  # noqa: BLE001 — çalışmayan kapı KALDI'dır, sessizce geçmez
                kapilar = [G("koşucu_hatası", KALDI, "%s: %s" % (type(e).__name__, e))]
        sonuclar.append((vid, v, kapilar))
    if not sonuclar:
        sys.exit("HATA: koşacak vaka seçilmedi")
    durumlar = [vaka_durumu(k) for _, _, k in sonuclar]
    cikis = 1 if KALDI in durumlar else (0 if all(x == GECTI for x in durumlar) else 3)
    genel = {0: "GEÇTİ", 1: "KALDI", 3: "TAMAMLANMADI (olculemedi/bekliyor)"}[cikis]
    yol = os.path.abspath(sonuc_yolu) if sonuc_yolu else os.path.join(cikti, "SONUC.md")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    sonuc_yaz(yol, ozellik, cikti, sonuclar, genel)
    if not sessiz:
        for vid, v, kapilar in sonuclar:
            print("%s · %s: %s" % (ozellik, vid, vaka_durumu(kapilar)))
            for k in kapilar:
                if k["durum"] != GECTI:
                    print("  %-26s %-11s %s" % (k["kapi"], k["durum"], k["ayrinti"][:160]))
        print("GENEL: %s · çıkış %d · %s" % (genel, cikis, yol))
    return cikis, [(vid, vaka_durumu(k)) for vid, _, k in sonuclar], sonuclar


def tur_klasoru(kok, ozellik, tur=None):
    """<kök>/<özellik>/<tur>: tur verilmediyse en son tur klasörü (tur1 < tur2 < tur3); tur klasörü yoksa <kök>/<özellik> kendisi."""
    ozel = os.path.join(kok, ozellik)
    if tur:
        return os.path.join(ozel, tur)
    turlar = sorted(x for x in glob.glob(os.path.join(ozel, "tur*")) if os.path.isdir(x))
    return turlar[-1] if turlar else ozel


def hepsi(a):
    """7 sınavı tek komutta koşar (sürüm öncesi regresyon). Tek satır özet + çıkış kodu: 0 hepsi GEÇTİ · 1 KALDI var · 3 KALDI yok ama olculemedi/bekliyor var."""
    kok = os.path.abspath(a.hepsi)
    ozet, satirlar, cikislar = [], [], []
    for o in OZELLIKLER:
        d = tur_klasoru(kok, o, a.tur)
        if not os.path.isdir(d):
            cikis, durumlar = 1, [("cikti", KALDI)]
            satirlar.append("%s: KALDI (çıktı klasörü yok: %s)" % (o, os.path.relpath(d, kok)))
        else:
            cikis, durumlar, _ = kos_ozellik(a, o, d, os.path.join(d, "SONUC-HEPSI.md"), sessiz=True)   # önceki SONUC.md (elle turlanmış kayıt) ezilmez
            satirlar.append("%s: %s (%s) %s" % (o, {0: "GEÇTİ", 1: "KALDI", 3: "TAMAMLANMADI"}[cikis], os.path.relpath(d, kok),
                                               " ".join("%s=%s" % (v, d_) for v, d_ in durumlar)))
        cikislar.append(cikis)
    genel = 1 if 1 in cikislar else (0 if all(c == 0 for c in cikislar) else 3)
    for s_ in satirlar:
        print("  " + s_)
    print("HEPSİ: %d özellik · GEÇTİ %d · KALDI %d · ölçülemedi/bekliyor %d · çıkış %d" % (
        len(OZELLIKLER), cikislar.count(0), cikislar.count(1), cikislar.count(3), genel))
    return genel


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ozellik", nargs="?")
    ap.add_argument("cikti", nargs="?")
    ap.add_argument("--referans-kok")
    ap.add_argument("--vaka", action="append")
    ap.add_argument("--sonuc")
    ap.add_argument("--liste", action="store_true")
    ap.add_argument("--hepsi", metavar="CIKTI_KOKU", help="7 özelliği tek komutta koş: <kök>/<özellik>/<tur>/<vaka>/ (tur: en son turN)")
    ap.add_argument("--tur", help="--hepsi ile: tur klasörü adı (ör. tur3); verilmezse her özelliğin en son turu")
    a = ap.parse_args()
    if a.liste:
        for o in OZELLIKLER:
            print(o, "·", ", ".join(v for v, _ in vakalari_oku(o)))
        return 0
    if a.hepsi:
        return hepsi(a)
    if not a.ozellik or not a.cikti:
        ap.error("özellik ve çıktı klasörü gerekli (ya da --hepsi <çıktı kökü>)")
    cikis, _, _ = kos_ozellik(a, ozellik_coz(a.ozellik), os.path.abspath(a.cikti), a.sonuc)
    return cikis


if __name__ == "__main__":
    sys.exit(main())
