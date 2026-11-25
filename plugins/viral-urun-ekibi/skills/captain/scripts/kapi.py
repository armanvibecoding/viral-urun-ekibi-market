#!/usr/bin/env python3
"""Tek zorlayıcı kapı: iki geçişi mekanik kapılardan tek komutla geçirir. Kapı yazıda değil, burada.

  python3 kapi.py kredi is/NN-urun [--proje .]                 ön-üretim → kredi (Flow üretimi istenmeden ÖNCE)
  python3 kapi.py yayin is/NN-urun [--proje .] [--video V01 …] [--kopyala]   teslim → yayın (kullanıcıya göndermeden ÖNCE)
  python3 kapi.py liste                                        geçiş başına kapı adları (kapının kendisini say)

Kapılar (her biri kendi betiğini koşturur; betik yoksa ya da girdi dosyası yoksa kapı KALDI sayılır, "temiz" denmez):
  kredi   senaryo      is/NN/senaryolar.json → studio/scripts/senaryo_kontrol.py çıkış 0
          kontrat      is/NN/kurgu/KURALLAR.md alan denetimi: İmza (tarihli) + İzleyici dolu, K1/K2/K9/K10 var, <…> yer tutucu yok
          hukum        son ön-üretim hükmü her videoda gecti=true (is/NN/elestiri/juri.jsonl; yoksa puanlar.jsonl)
          kredi-onayi  .ekip/KARARLAR.md'de tarihli `| kredi |` ya da `| bütçe |` satırı (tavan onayı)
          defter       .ekip/GERI-BILDIRIM.md var ve geri_bildirim_kontrol.py çıkış 0
  yayin   (video başına, is/NN/kurgu/VNN.mp4 + VNN.json)
          teknik@V     1080×1920, ses izi var, −14 ± 1 LUFS
          kurgu@V      hizli_kurgu biçimli ayarda kurgu_kontrol.py AYAR --video → 0 (kurgu.py biçiminde UYGULANMAZ)
          goruntu@V    kurgu_kontrol.py --goruntu → 0 (kesim dışı sıçrama / son 2 sn gürültü)
          ses@V        ses_olc.py --kapi --muzik_stem is/NN/ses/stem_VNN/muz.wav → 0 (stem yoksa KALDI: müzik girişi ölçülemedi)
          iddia@V      mağaza paketi varsa ortak/paket.py iddia-kontrol → 0 (uydurma veri; sağlık dili yalnız bilgi notu)
          lisans@V     videodaki her klibin etiketi ve kaynağı var; ürün klipleri KAYNAK.tsv satırına bağlı ve o satırda lisans
                       (kurucu|uretim|stok|yazili) + kullanim=yayin + yapay_mi + bakildi dolu; boş sütun / `kullanma` = KALDI (karar kullanıcıda, kayıt kapıda)
          hukum@V      son teslim hükmü gecti=true (juri.jsonl; yoksa puanlar.jsonl)
          (iş başına)  defter (yukarıdaki) · sozlesme: magaza-paketi.json varsa paket.py dogrula magaza --tam → 0 (eksik[] dolu / fiyat 0 / yer tutucu / kaynaksız marka adı = KALDI; denetim #17)
  "jüri yapılamadı" kaydı (referans < 3) GEÇİŞ DEĞİLDİR: hukum kapısı KALDI olur, ilerlemek yalnız kullanıcının (mağaza sahibinin) açık aşım cümlesiyle (AŞILDI).
  UYGULANMAZ yalnız kapının konusu o işte yoksa yazılır (mağaza kurulmamış, ayar kurgu.py biçiminde); ölçülemeyen = KALDI.

Aşım (kapı kaldı ama yine de ilerlemek): YALNIZ kullanıcının (mağaza sahibinin) açık kararıyla, kapı başına bir satır, .ekip/KARARLAR.md'de:
  - YYYY-AA-GG | kapi-asimi | <kredi|yayin> <iş klasörü adı> <kapı adı>: "<kullanıcının cümlesi, aynen>"
  Tarih bugünden ileri olamaz; cümle tırnak içinde ve ≥ 10 karakter; kapı adı tam eşleşir (ör. ses@V03). "Hepsi" yok.
  Aşılan kapı raporda AŞILDI görünür ve kayda geçer; lider bu satırı kullanıcı söylemeden yazamaz (sahte aşım = uydurma karar).

--kopyala (yalnız yayin, yalnız geçince): videoları is/NN/teslim/ altına betik kopyalar; elle kopyalama yok.
Kayıt: her koşu .ekip/kapi.jsonl'a bir satır (karne_uret.py okur). Çıkış: 0 geçti (aşım dahil) · 1 kaldı · 2 kullanım hatası.
"""
import argparse
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BURASI = os.path.dirname(os.path.abspath(__file__))
EKLENTI = os.path.abspath(os.path.join(BURASI, "..", "..", ".."))
CUT_BETIK = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")), "skills", "cut", "scripts")
BETIK = {
    "senaryo": os.path.join(EKLENTI, "skills", "studio", "scripts", "senaryo_kontrol.py"),
    "kurgu": os.path.join(EKLENTI, "skills", "cut", "scripts", "kurgu_kontrol.py"),
    "ses": os.path.join(EKLENTI, "skills", "cut", "scripts", "ses_olc.py"),
    "defter": os.path.join(BURASI, "geri_bildirim_kontrol.py"),
    "paket": os.path.join(EKLENTI, "ortak", "paket.py"),
}
if not os.path.exists(BETIK["paket"]):  # ChatGPT paketinde ortak/ → skills/ekip-bilgi/references/
    BETIK["paket"] = os.path.join(EKLENTI, "skills", "ekip-bilgi", "references", "paket.py")
GECTI, KALDI, YOK, ASILDI = "GEÇTİ", "KALDI", "UYGULANMAZ", "AŞILDI"
KAPILAR = {
    "kredi": ["senaryo", "kontrat", "hukum", "kredi-onayi", "defter"],
    "yayin": ["teknik@V", "kurgu@V", "goruntu@V", "ses@V", "iddia@V", "lisans@V", "hukum@V", "defter", "sozlesme"],
}
ASIM_RE = re.compile(r"^\s*-\s*(\d{4}-\d{2}-\d{2})\s*\|\s*kapi-asimi\s*\|\s*(kredi|yayin)\s+(\S+)\s+(\S+?)\s*:\s*[\"“](.+)[\"”]\s*$")


def kos(komut):
    """(çıkış kodu, son satırlar). Betik yoksa 127 (kapı kalır)."""
    if not os.path.exists(komut[1]):
        return 127, "betik yok: %s" % komut[1]
    try:
        r = subprocess.run(komut, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        return 124, "zaman aşımı (600 sn)"
    cikti = (r.stdout + "\n" + r.stderr).strip().splitlines()
    onemli = [s for s in cikti if re.search(r"HATA|KAPI|KALDI|❌|✗|Traceback|Error", s)] or cikti
    return r.returncode, " / ".join(s.strip() for s in onemli[-3:])[:400]


def betik_kapisi(komut, ad):
    kod, ozet = kos(komut)
    return (GECTI, "çıkış 0") if kod == 0 else (KALDI, "%s çıkış %d: %s" % (ad, kod, ozet))


def son_hukumler(is_dizin, mod):
    """{video: satır} — juri.jsonl öncelikli; yoksa puanlar.jsonl. (None, neden) dosya yoksa/bozuksa."""
    for ad in ("juri.jsonl", "puanlar.jsonl"):
        yol = os.path.join(is_dizin, "elestiri", ad)
        if not os.path.exists(yol):
            continue
        son = {}
        try:
            with open(yol, encoding="utf-8") as f:
                for satir in f:
                    if satir.strip():
                        r = json.loads(satir)
                        if r.get("mod") == mod:
                            son[str(r.get("video"))] = r
        except (ValueError, OSError) as e:
            return None, "%s okunamadı: %s" % (ad, e)
        return son, ad
    return None, "hüküm kaydı yok (elestiri/juri.jsonl ya da puanlar.jsonl)"


def kalici_recete_var(is_dizin):
    yol = os.path.join(is_dizin, "elestiri", "puanlar.jsonl")
    if not os.path.exists(yol):
        return False
    with open(yol, encoding="utf-8") as f:
        return any(str(x).strip().upper().startswith("KALICI") for s in f if s.strip()
                   for x in (json.loads(s).get("recete") or []))


def k_defter(proje, is_dizin):
    defter = os.path.join(proje, ".ekip", "GERI-BILDIRIM.md")
    if not os.path.exists(defter):
        ek = " — puanlar.jsonl'da KALICI reçete var, hiçbiri deftere girmemiş" if kalici_recete_var(is_dizin) else ""
        return KALDI, "defter yok: .ekip/GERI-BILDIRIM.md (yok = ölçülemedi, temiz değil)%s" % ek
    return betik_kapisi([sys.executable, BETIK["defter"], defter, "--eklenti", EKLENTI], "geri_bildirim_kontrol")


def k_hukum(is_dizin, mod, video=None):
    son, kaynak = son_hukumler(is_dizin, mod)
    if son is None:
        return KALDI, kaynak
    if video is not None:
        r = son.get(video) or son.get(video.lstrip("V")) or son.get(video.lstrip("V").lstrip("0"))
        if r is None:
            return KALDI, "%s: %s için %s hükmü yok" % (kaynak, video, mod)
        kal = (r.get("kalibrasyon") or {}).get("durum")
        if r.get("juri") == "yapilamadi":   # referans < 3: iş durmaz, "jüri yapılamadı" notuyla teslim (juri.py yapilamadi yazar)
            n, neden = r.get("referans_sayisi"), str(r.get("neden") or "").strip()
            if not isinstance(n, int) or n >= 3 or not neden:
                return KALDI, "%s: 'jüri yapılamadı' kaydı geçersiz (referans_sayisi < 3 ve neden dolu olmalı; referans ≥ 3 ise jüri koşar)" % kaynak
            # Denetim 2026-11-25 #2/#4: "yapılamadı" artık geçiş değil, KALDI; yalnız kullanıcının açık aşım cümlesiyle ilerler (AŞILDI görünür)
            return KALDI, "JÜRİ YAPILAMADI (referans %d < 3): %s — kullanıcının (mağaza sahibinin) açık aşım cümlesi şart (KARARLAR.md kapi-asimi), referanssız jüri notla geçmez" % (n, neden[:120])
        if r.get("gecti") is True:
            return GECTI, "%s tur %s gecti=true%s" % (kaynak, r.get("tur"), " · jüri kalibrasyonu: %s (hüküm DENEME)" % kal if kal and kal != "UYUMLU" else "")
        return KALDI, "%s tur %s gecti=false (toplam %s)" % (kaynak, r.get("tur"), r.get("toplam", r.get("medyan")))
    if not son:
        return KALDI, "%s: %s modunda satır yok" % (kaynak, mod)
    kalan = sorted(v for v, r in son.items() if r.get("gecti") is not True or r.get("juri") == "yapilamadi")
    return (KALDI, "%s: son %s hükmü KALDI olan video: %s" % (kaynak, mod, ", ".join(kalan))) if kalan else \
        (GECTI, "%s: %d videonun son %s hükmü gecti=true" % (kaynak, len(son), mod))


def k_kredi_onayi(proje):
    yol = os.path.join(proje, ".ekip", "KARARLAR.md")
    if not os.path.exists(yol):
        return KALDI, "KARARLAR.md yok (kredi tavanı onayı ölçülemedi)"
    with open(yol, encoding="utf-8") as f:
        for s in f:
            m = re.match(r"^\s*-\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]+)\|\s*(.+)$", s)
            if m and re.search(r"kredi|bütçe|butce", m.group(2), re.I) and re.search(r"\d", m.group(3)):
                return GECTI, "onay satırı: %s" % s.strip()[:120]
    return KALDI, "KARARLAR.md'de tarihli ve tutarlı `| kredi |` / `| bütçe |` satırı yok"


KONTRAT_ZORUNLU = ("K1", "K2", "K9", "K10")   # iskelet · kanca · ses · malzeme (cut/referans/KURALLAR-sablon.md)
YER_TUTUCU = re.compile(r"<[^<>|]{0,60}>|TODO")


def yer_tutucu_var(c):
    """Kod aralığı (`...`) içindeki <arg> komut bağımsız değişkenidir, yer tutucu sayılmaz."""
    return bool(YER_TUTUCU.search(re.sub(r"`[^`]*`", "", c)))


def k_kontrat(yol):
    """Kontrat kapısı = ALAN denetimi (denetim 2026-11-25 #5): satır sayısı kanıt değildir.
    Şart: `İmza:` (tarihli) ve `İzleyici:` satırları dolu · zorunlu K1/K2/K9/K10 satırları var · her K satırında
    Alan/Kural/Eşik/Nasıl ölçülür dolu ve `<…>` yer tutucu kalmamış · en az 5 K satırı."""
    if not os.path.exists(yol):
        return KALDI, "kontrat yok: kurgu/KURALLAR.md"
    metin = open(yol, encoding="utf-8").read()
    eksik = []
    for ad, desen in (("İmza", r"^\s*İmza\s*:\s*(.*)$"), ("İzleyici", r"^\s*İzleyici\s*:\s*(.*)$")):
        m = re.search(desen, metin, re.M)
        if not m or not m.group(1).strip():
            eksik.append("`%s:` satırı yok/boş" % ad)
        elif yer_tutucu_var(m.group(1)):
            eksik.append("`%s:` satırında yer tutucu kaldı" % ad)
        elif ad == "İmza" and not re.search(r"\d{4}-\d{2}-\d{2}", m.group(1)):
            eksik.append("`İmza:` satırında tarih (YYYY-AA-GG) yok")
    satirlar = {}
    for ln in metin.splitlines():
        h = [c.strip() for c in ln.strip().strip("|").split("|")]
        if ln.lstrip().startswith("|") and len(h) >= 5 and re.fullmatch(r"K\d+|K\.\.", h[0]):
            if h[0] != "K..":
                satirlar[h[0]] = h
    for k in KONTRAT_ZORUNLU:
        if k not in satirlar:
            eksik.append("zorunlu %s satırı yok" % k)
    if len(satirlar) < 5:
        eksik.append("K satırı %d < 5" % len(satirlar))
    for k, h in satirlar.items():
        bos = [n for n, c in zip(("alan", "kural", "eşik", "ölçüm"), h[1:5]) if not c]
        if bos:
            eksik.append("%s boş alan: %s" % (k, "/".join(bos)))
        elif any(yer_tutucu_var(c) for c in h[1:5]):
            eksik.append("%s yer tutucu (<…>) kaldı" % k)
    if eksik:
        return KALDI, "kontrat alanları eksik (kurgu/KURALLAR.md): " + "; ".join(eksik[:6])
    return GECTI, "kurgu/KURALLAR.md alanları dolu (%d K satırı)" % len(satirlar)


def kredi_kapilari(proje, is_dizin, _a):
    s = []
    sj = os.path.join(is_dizin, "senaryolar.json")
    s.append(("senaryo", *(betik_kapisi([sys.executable, BETIK["senaryo"], sj], "senaryo_kontrol") if os.path.exists(sj)
                           else (KALDI, "dosya yok: senaryolar.json"))))
    kontrat = os.path.join(is_dizin, "kurgu", "KURALLAR.md")
    s.append(("kontrat", *k_kontrat(kontrat)))
    s.append(("hukum", *k_hukum(is_dizin, "onuretim")))
    s.append(("kredi-onayi", *k_kredi_onayi(proje)))
    s.append(("defter", *k_defter(proje, is_dizin)))
    return s


def videolar(is_dizin, secim):
    hepsi = sorted(os.path.splitext(os.path.basename(y))[0] for y in glob.glob(os.path.join(is_dizin, "kurgu", "V*.mp4"))
                   if re.fullmatch(r"V\d+[A-Za-z]?", os.path.splitext(os.path.basename(y))[0]))
    return [v for v in hepsi if not secim or v in secim], hepsi


def k_teknik(video):
    sys.path.insert(0, os.path.join(EKLENTI, "skills", "cut", "scripts"))
    try:
        import ffaraclar as F
        m = F.medya_bilgi(video)
        if (m["w"], m["h"]) != (1080, 1920):
            return KALDI, "çözünürlük %sx%s (1080x1920 olmalı)" % (m["w"], m["h"])
        if not m.get("ses"):
            return KALDI, "ses izi yok (müziksiz/sessiz teslim yok)"
        lufs = F.lufs_olc(video)
        if abs(lufs + 14) > 1.0:
            return KALDI, "ses %.1f LUFS (−14 ± 1 olmalı)" % lufs
        return GECTI, "1080x1920 · %.2f sn · %.1f LUFS" % (m["sure"], lufs)
    except Exception as e:  # ölçülemeyen = kaldı
        return KALDI, "ölçülemedi: %r" % (e,)


def k_lisans(is_dizin, ayar_yolu):
    """Lisans kapısı (denetim 2026-11-25 #10): klip → etiket → KAYNAK.tsv satırı → lisans sütunları. Kapı yazıda değil kayıtta."""
    if CUT_BETIK not in sys.path:
        sys.path.insert(0, CUT_BETIK)
    import malzeme_kaynak as M
    if not os.path.exists(ayar_yolu):
        return KALDI, "ayar dosyası yok: klip listesi okunamadı (lisans ölçülemedi)"
    try:
        ayar = json.load(open(ayar_yolu, encoding="utf-8"))
    except ValueError as e:
        return KALDI, "ayar okunamadı: %s" % e
    kok = os.path.dirname(ayar_yolu)
    klipler = []
    for p in ayar.get("planlar", []):
        yol = p.get("klip") if isinstance(p, dict) else (p[0] if p else None)
        if yol:
            klipler.append(os.path.normpath(os.path.join(kok, yol)))
    if not klipler:
        return KALDI, "ayarda klip yok: lisans ölçülemedi"
    etiket = {}
    for d in sorted({os.path.dirname(k) for k in klipler}):
        y = os.path.join(d, "klip_etiket.json")
        if os.path.exists(y):
            try:
                etiket.update(json.load(open(y, encoding="utf-8")).get("klipler", {}))
            except ValueError:
                return KALDI, "klip_etiket.json okunamadı: %s" % y
    kyol = M.bul(is_dizin)
    satirlar = M.oku(kyol) if kyol else []
    sorun, urun = [], 0
    for k in dict.fromkeys(klipler):
        ad = os.path.splitext(os.path.basename(k))[0]
        e = etiket.get(ad)
        if not e:
            sorun.append("%s: klip_etiket.json'da yok (kaynak ve lisans bilinmiyor)" % ad)
            continue
        metin = e.get("malzeme") or e.get("kaynak") or ""
        if not metin.strip():
            sorun.append("%s: etikette kaynak yok" % ad)
        elif e.get("tur") in M.URUN_TURLERI:
            urun += 1
            if not kyol:
                sorun.append("%s: KAYNAK.tsv yok (lisans kaydı yok)" % ad)
                continue
            es = M.esle(satirlar, metin, os.path.basename(kok))
            if not es:
                sorun.append("%s: kaynağı KAYNAK.tsv'de yok" % ad)
            else:
                for r in es:
                    if not M.kullanilabilir(r):
                        sorun.append("%s: %s 'kullanma' işaretli" % (ad, r.get("dosya")))
                    for x in M.lisans_sorunu(r):
                        sorun.append("%s → %s: %s" % (ad, r.get("dosya"), x))
    if sorun:
        return KALDI, "lisans kaydı eksik (%d sorun): %s" % (len(sorun), " / ".join(dict.fromkeys(sorun))[:360])
    return GECTI, "%d klip kayıtlı kaynaktan, %d ürün klibinin lisansı yayın için tamam (%s)" % (len(dict.fromkeys(klipler)), urun, os.path.basename(kyol) if kyol else "KAYNAK.tsv gerekmedi")


def yayin_kapilari(proje, is_dizin, a):
    s = []
    secili, hepsi = videolar(is_dizin, a.video)
    mp = os.path.join(is_dizin, "magaza", "magaza-paketi.json")
    if not secili:
        s.append(("teknik@V", KALDI, "kurgu/ altında teslim videosu yok (VNN.mp4)%s"
                  % (" — istenen: %s, bulunan: %s" % (a.video, hepsi) if a.video else "")))
    for v in secili:
        video = os.path.join(is_dizin, "kurgu", v + ".mp4")
        ayar = os.path.join(is_dizin, "kurgu", v + ".json")
        s.append(("teknik@" + v, *k_teknik(video)))
        if not os.path.exists(ayar):
            for ad in ("kurgu@", "goruntu@"):
                s.append((ad + v, KALDI, "ayar dosyası yok: kurgu/%s.json (kesimler ve yazılar ölçülemedi)" % v))
            d = {}
        else:
            try:
                d = json.load(open(ayar, encoding="utf-8"))
            except ValueError as e:
                d = None
                for ad in ("kurgu@", "goruntu@"):
                    s.append((ad + v, KALDI, "ayar okunamadı: %s" % e))
            if d is not None:
                hizli = bool(d.get("planlar")) and isinstance(d["planlar"][0], dict)
                if hizli:
                    komut = [sys.executable, BETIK["kurgu"], ayar, "--video", video]
                    s.append(("kurgu@" + v, *betik_kapisi(komut, "kurgu_kontrol")))
                else:
                    s.append(("kurgu@" + v, YOK, "ayar kurgu.py biçiminde (plan kuralları hizli_kurgu ayarında ölçülür)"))
                s.append(("goruntu@" + v, *betik_kapisi([sys.executable, BETIK["kurgu"], ayar, "--goruntu", video, "--yalniz-goruntu"], "kurgu_kontrol --goruntu")))
        stem = os.path.join(is_dizin, "ses", "stem_" + v, "muz.wav")
        if not os.path.exists(stem):
            s.append(("ses@" + v, KALDI, "müzik stem'i yok: ses/stem_%s/muz.wav (müzik girişi ölçülemedi; müziksiz teslim yok)" % v))
        else:
            komut = [sys.executable, BETIK["ses"], video, "--muzik_stem", stem, "--kapi"]
            if isinstance(d, dict) and d.get("drop_sn") is not None:
                komut += ["--drop", str(d["drop_sn"])]
            s.append(("ses@" + v, *betik_kapisi(komut, "ses_olc --kapi")))
        if not os.path.exists(mp):
            s.append(("iddia@" + v, YOK, "mağaza paketi yok (onaylı iddia listesi mağaza kurulunca gelir)"))
        elif not os.path.exists(ayar):
            s.append(("iddia@" + v, KALDI, "ayar dosyası yok: ekran yazıları okunamadı"))
        else:
            s.append(("iddia@" + v, *betik_kapisi([sys.executable, BETIK["paket"], "iddia-kontrol", mp, ayar], "paket.py iddia-kontrol")))
        s.append(("lisans@" + v, *k_lisans(is_dizin, ayar)))
        s.append(("hukum@" + v, *k_hukum(is_dizin, "teslim", v)))
    s.append(("defter", *k_defter(proje, is_dizin)))
    s.append(("sozlesme", *(betik_kapisi([sys.executable, BETIK["paket"], "dogrula", "magaza", mp, "--tam"], "paket.py dogrula magaza --tam")
                            if os.path.exists(mp) else (YOK, "mağaza paketi yok"))))
    return s


def asimlar(proje, gecis, is_ad):
    """{kapı adı: (tarih, cümle)} — yalnız biçimi ve tarihi geçerli satırlar. Geçersizler ayrı listede (sessizce yutulmaz)."""
    yol = os.path.join(proje, ".ekip", "KARARLAR.md")
    gecerli, gecersiz = {}, []
    if not os.path.exists(yol):
        return gecerli, gecersiz
    bugun = datetime.date.today()
    with open(yol, encoding="utf-8") as f:
        for no, s in enumerate(f, 1):
            if "kapi-asimi" not in s:
                continue
            m = ASIM_RE.match(s.rstrip("\n"))
            if not m:
                gecersiz.append("KARARLAR.md:%d biçim tutmuyor (- TARİH | kapi-asimi | geçiş iş kapı: \"cümle\")" % no)
                continue
            tarih, g, isad, kapi, cumle = m.groups()
            try:
                t = datetime.date.fromisoformat(tarih)
            except ValueError:
                gecersiz.append("KARARLAR.md:%d tarih geçersiz: %s" % (no, tarih))
                continue
            if t > bugun:
                gecersiz.append("KARARLAR.md:%d ileri tarihli aşım (%s)" % (no, tarih))
            elif len(cumle.strip()) < 10:
                gecersiz.append("KARARLAR.md:%d kullanıcının cümlesi yok ya da < 10 karakter" % no)
            elif g == gecis and isad == is_ad:
                gecerli[kapi] = (tarih, cumle.strip())
    return gecerli, gecersiz


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gecis", choices=["kredi", "yayin", "liste"])
    ap.add_argument("is_dizin", nargs="?")
    ap.add_argument("--proje", default=".")
    ap.add_argument("--video", action="append", default=[], help="yalnız bu video(lar) (yayin); varsayılan kurgu/ altındaki hepsi")
    ap.add_argument("--kopyala", action="store_true", help="geçince videoları is/NN/teslim/ altına kopyala (yalnız yayin)")
    a = ap.parse_args()
    if a.gecis == "liste":
        for g, liste in KAPILAR.items():
            print("%s (%d): %s" % (g, len(liste), " · ".join(liste)))
        return 0
    if not a.is_dizin or not os.path.isdir(a.is_dizin):
        print("HATA: iş klasörü yok: %s" % a.is_dizin, file=sys.stderr)
        return 2
    proje = os.path.abspath(a.proje)
    is_dizin = os.path.abspath(a.is_dizin)
    is_ad = os.path.basename(is_dizin.rstrip(os.sep))
    sonuc = (kredi_kapilari if a.gecis == "kredi" else yayin_kapilari)(proje, is_dizin, a)

    # kapının kendisini say: listedeki her kapı türü en az bir kez koşmuş olmalı (sessizce düşen kapı = kaldı)
    kosan = {ad.split("@")[0] for ad, _, _ in sonuc}
    for beklenen in KAPILAR[a.gecis]:
        if beklenen.split("@")[0] not in kosan:
            sonuc.append((beklenen, KALDI, "kapı koşmadı (ölçülecek girdi yok ya da betik hatası) — ölçülmeyen kapı yeşil sayılmaz"))

    gecerli, gecersiz = asimlar(proje, a.gecis, is_ad)
    satirlar = []
    for ad, durum, mesaj in sonuc:
        if durum == KALDI and ad in gecerli:
            tarih, cumle = gecerli[ad]
            satirlar.append({"kapi": ad, "durum": ASILDI, "mesaj": mesaj, "asim": {"tarih": tarih, "soz": cumle}})
        else:
            satirlar.append({"kapi": ad, "durum": durum, "mesaj": mesaj})
    kalan = [x for x in satirlar if x["durum"] == KALDI]
    asilan = [x for x in satirlar if x["durum"] == ASILDI]
    hukum = "KALDI" if kalan else ("AŞIMLA GEÇTİ" if asilan else "GEÇTİ")

    print("KAPI %s · %s · %d kapı" % (a.gecis, is_ad, len(satirlar)))
    for x in satirlar:
        print("  %-10s %-14s %s" % (x["durum"], x["kapi"], x["mesaj"]))
        if x["durum"] == ASILDI:
            print("             ↳ kullanıcı kararı %s: \"%s\" (KARARLAR.md; kullanıcı söylemediyse sahte aşımdır)" % (x["asim"]["tarih"], x["asim"]["soz"]))
    for g in gecersiz:
        print("  UYARI      geçersiz aşım satırı yok sayıldı: %s" % g)
    print("SONUÇ: %s — geçen %d · kalan %d · aşılan %d · uygulanmaz %d"
          % (hukum, sum(x["durum"] == GECTI for x in satirlar), len(kalan), len(asilan), sum(x["durum"] == YOK for x in satirlar)))
    if kalan:
        print("Kalan kapı düzeltilmeden %s. Aşmak yalnız kullanıcının (mağaza sahibinin) açık kararıyla (kapı başına bir satır):"
              % ("kredi istenmez" if a.gecis == "kredi" else "teslim ve yayın yok"))
        for x in kalan:
            print("  - %s | kapi-asimi | %s %s %s: \"<kullanıcının cümlesi>\"" % (datetime.date.today().isoformat(), a.gecis, is_ad, x["kapi"]))

    if a.gecis == "yayin" and a.kopyala:
        if kalan:
            print("KOPYALANMADI: kapı kaldı; teslim klasörüne video gitmez.")
        else:
            hedef = os.path.join(is_dizin, "teslim")
            os.makedirs(hedef, exist_ok=True)
            for v in videolar(is_dizin, a.video)[0]:
                shutil.copy2(os.path.join(is_dizin, "kurgu", v + ".mp4"), os.path.join(hedef, v + ".mp4"))
                print("teslim: %s" % os.path.join(hedef, v + ".mp4"))

    ekip = os.path.join(proje, ".ekip")
    if os.path.isdir(ekip):
        with open(os.path.join(ekip, "kapi.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"tarih": datetime.datetime.now().isoformat(timespec="seconds"), "gecis": a.gecis, "is": is_ad,
                                "sonuc": hukum, "kapilar": satirlar}, ensure_ascii=False) + "\n")
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
