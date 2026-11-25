#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/sinav_kos.py kırma testi: koşucunun KALDI/olculemedi verdiğini ve sahte geçti vermediğini kanıtlar.

  python3 scripts/sinav_kos_test.py [--hizli]      # çıkış 0 = hepsi geçti; --hizli: 03 (≈1 dk gerçek hikâye hattı) atlanır

Yöntem (her özellik için): önce DOĞRU sentetik çıktı kurulur ve kapıların yeşil olduğu görülür (kırılmayan kapı yeşil sayılmaz),
sonra tek bozma yapılır ve ilgili kapının KALDI'ya döndüğü görülür. Ayrıca: boş klasör, eksik klasör, eksik dosya → KALDI (çıkış 1);
mekanik kapılar yeşilken jüri/ölçen betik yoksa çıkış 3 (0 değil); jüri hattı sahte referans + sahte KOR kopyalarıyla uçtan uca
(GEÇTİ → çıkış 0, düşük puan → KALDI). Gerçek referans verisi kullanılmaz; geçici klasörde çalışır, depoya yazmaz.
"""
import copy
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EKL = os.path.join(KOK, "plugins", "viral-urun-ekibi")
CUT = os.path.join(EKL, "skills", "cut", "scripts")
KOS = os.path.join(KOK, "scripts", "sinav_kos.py")
sys.path.insert(0, CUT)
import ffaraclar as F  # noqa: E402

HIZLI = "--hizli" in sys.argv
sonuc = []
PAZAR = {"a-kolay": None, "b-zor": None, "c-tuzak": None}  # vaka.json'dan okunur


def t(ad, ok, ayrinti=""):
    sonuc.append(bool(ok))
    print(("GEÇTİ " if ok else "KALDI ") + ad + ("" if ok else "\n      " + str(ayrinti).strip().replace("\n", "\n      ")[:700]))


def yaz(yol, veri):
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(veri if isinstance(veri, str) else json.dumps(veri, ensure_ascii=False, indent=1))


def web_olcum_hazir():
    r = subprocess.run([sys.executable, os.path.join(EKL, "ortak", "web_olcum.py"), "kontrol"], capture_output=True, text=True)
    return r.returncode == 0


def vaka_pazar(oz, vaka):
    p = os.path.join(EKL, "ortak", "sinav", oz, "vakalar", vaka, "vaka.json")
    return json.load(open(p, encoding="utf-8"))["pazar"]


def kos(oz, cikti, *ek, env=None):
    e = dict(os.environ)
    e.pop("SINAV_REFERANS_KOK", None)   # dış ortamdaki referans kökü "referans yokken olculemedi" testlerini bozmasın; gereken test env ile verir
    e.update(env or {})
    r = subprocess.run([sys.executable, KOS, oz, cikti] + list(ek), capture_output=True, text=True, env=e)
    sonuc_md = os.path.join(cikti, "SONUC.md")
    md = open(sonuc_md, encoding="utf-8").read() if os.path.exists(sonuc_md) else ""
    return r.returncode, r.stdout + r.stderr, md


def kapi(md, vaka, ad):
    """SONUC.md'den vaka bölümünde kapı durumunu oku."""
    bol = md.split("## %s " % vaka)[1].split("\n## ")[0] if ("## %s " % vaka) in md else ""
    m = re.search(r"^\| %s \| ([^|]+) \|" % re.escape(ad), bol, re.M)
    return m.group(1).strip() if m else None


def hepsi_yesil(md, vaka, haric=("juri",)):
    bol = md.split("## %s " % vaka)[1].split("\n## ")[0]
    satirlar = re.findall(r"^\| ([^|]+) \| ([^|]+) \|", bol, re.M)
    return [(k.strip(), d.strip()) for k, d in satirlar if k.strip() not in ("Kapı", "---") and k.strip() not in haric and d.strip() != "GEÇTİ"]


# ------------------------------------------------------------------ sentetik medya
def ffmpeg(*a):
    F.calistir([F.ffmpeg_bul(), "-v", "error", "-y"] + [str(x) for x in a])


def video_tabani(d):
    """9 sn, 1080×1920, 30 fps; ses_tasarla ile müzik girişi/drop/−14 LUFS kapılarından geçen sentetik video + stem."""
    os.makedirs(os.path.join(d, "klipler"), exist_ok=True)
    for ad, renk, fr in (("S1", "0x2a6f97", 330), ("S2", "0x7a3e9d", 440)):
        ffmpeg("-f", "lavfi", "-i", "color=c=%s:s=1080x1920:r=30:d=3,noise=alls=10:allf=t,eq=brightness='0.35*sin(2*PI*t)':eval=frame" % renk,
               "-f", "lavfi", "-i",   # eq: ilk 2 sn'de belirgin değişim şart (kurgu_kontrol ilk2sn)
               "sine=frequency=%d:duration=3" % fr, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
               os.path.join(d, "klipler", ad + ".mp4"))
    yaz(os.path.join(d, "l.txt"), "file 'klipler/S1.mp4'\nfile 'klipler/S2.mp4'\nfile 'klipler/S1.mp4'\n")
    ffmpeg("-f", "concat", "-safe", "0", "-i", os.path.join(d, "l.txt"), "-c", "copy", os.path.join(d, "ham.mp4"))
    ffmpeg("-f", "lavfi", "-i", "aevalsrc='0.3*sin(2*PI*220*t)*(0.7+0.3*sin(2*PI*2*t))':s=48000:d=20", os.path.join(d, "muzik.wav"))
    r = subprocess.run([sys.executable, os.path.join(CUT, "ses_tasarla.py"), "--video", os.path.join(d, "ham.mp4"), "--muzik",
                        os.path.join(d, "muzik.wav"), "--muzik_bas", "6.0", "--drop_video_sn", "3.0", "--patlama_db", "0", "--crackle_db", "0",
                        "--kesmeler", "yok", "--sfx", "vurus@3.0,tik@0.1", "--sfx_db", "-3", "--sessizlik_vurusu", "0.2",
                        "--drop_oncesi_db", "-16", "--stem_klasoru", os.path.join(d, "stem"), "--cikti", os.path.join(d, "video.mp4")],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit("video tabanı kurulamadı: " + r.stdout[-400:] + r.stderr[-400:])
    shutil.copy(os.path.join(d, "stem", "muz.wav"), os.path.join(d, "muz_stem.wav"))


def kart(pazar, tatmin="tek hamlede temizlenen yüzey", fmt="dongu"):
    sys.path.insert(0, os.path.join(EKL, "skills", "studio", "scripts"))
    import on_uretim_karti as K
    k = K.sablon(pazar)
    k["format"] = fmt
    if fmt == "dongu":
        k["tatmin_ani"] = tatmin
    else:
        k.pop("tatmin_ani", None)
    k["kanca_metni"] = {"TR": "Bunu görünce şaşıracaksın", "DE": "Das solltest du sehen", "US": "You need to see this"}[pazar]
    return k


CAPTION = {"US": "Watch it happen. Link in bio.", "TR": "Bunu izle. Link biyografide.", "DE": "Schau genau hin. Link in der Bio."}


def vaka_01(kok, vaka, taban):
    d = os.path.join(kok, vaka)
    shutil.copytree(taban, d, ignore=shutil.ignore_patterns("stem", "ham.mp4", "muzik.wav", "l.txt"))
    pazar = vaka_pazar("01-urun-videosu", vaka)
    yaz(os.path.join(d, "on_uretim_karti.json"), kart(pazar))
    yaz(os.path.join(d, "klipler", "klip_etiket.json"), {"klipler": {"S1": {"arac": None, "tur": "urun", "icerik": "urun_a"},
                                                                  "S2": {"arac": None, "tur": "urun", "icerik": "urun_b"}}, "araclar": {}})
    kanca = kart(pazar)["kanca_metni"]
    ayar = {"format": "dongu", "font": "font/x.ttf", "cikti": "video.mp4", "drop_sn": 3.0, "tatmin_ani": {"bas": 3.0, "bit": 4.5},
            "planlar": [{"klip": "klipler/S1.mp4", "bas": 0, "bit": 3.0, "yazi": kanca}, {"klip": "klipler/S2.mp4", "bas": 0, "bit": 3.0},
                        {"klip": "klipler/S1.mp4", "bas": 0, "bit": 3.0}],
            "cta": {"satir1": "Comment LINK", "satir2": "and I'll DM you", "plan": 2}}
    if vaka != "a-kolay":
        ayar["urun_tipi"] = "ekransiz"
    yaz(os.path.join(d, "ayar.json"), ayar)
    yaz(os.path.join(d, "caption.txt"), CAPTION[pazar])
    return d


def kare_klasoru(yol, n=2, renk=(90, 60, 40)):
    from PIL import Image, ImageDraw
    os.makedirs(yol, exist_ok=True)
    for i in range(n):
        im = Image.new("RGB", (216, 384), renk)
        ImageDraw.Draw(im).rectangle((20 + i * 30, 50, 120 + i * 30, 300), fill=(200, 180, 60))
        im.save(os.path.join(yol, "k%d.jpg" % i))


# ------------------------------------------------------------------ 02 senaryo üretici (senaryo_kontrol'den geçer)
def _kelime(tohum, j):
    """Her senaryo sahnesi için birbirinden ayrışan sahte kelime (senaryo_kontrol benzerlik ≤ 0,8 kapısı için)."""
    import random
    r = random.Random(tohum * 31 + j)
    return "".join(r.choice("abcdefghijklmnoprstuvyz") for _ in range(r.randint(4, 8)))


def senaryolar(pazar, adet=30):
    isimler = ["kupa", "tabak", "kutu", "lamba", "saksı", "çanta", "kitap", "fincan", "şemsiye", "defter", "bisiklet", "gitar", "perde",
               "ayna", "radyo", "sandalye", "battaniye", "vazo", "terlik", "saat", "cüzdan", "bardak", "tepsi", "sepet", "çatal",
               "kalem", "yastık", "halı", "mum", "anahtar"]
    fiiller = ["kaldırır", "çevirir", "açar", "kapatır", "sallar", "iter", "çeker", "tutar", "bırakır", "kaydırır", "döker", "sıkar",
               "büker", "katlar", "yuvarlar", "fırlatır", "toplar", "gizler", "gösterir", "ölçer", "tartar", "boyar", "siler", "kurutur",
               "bağlar", "çözer", "yıkar", "doldurur", "boşaltır", "sayar"]
    yerler = ["mutfakta", "balkonda", "salonda", "garajda", "bahçede", "çatıda", "banyoda", "ofiste", "atölyede", "terasta"]
    mek = ["M%d" % (1 + i % 9) for i in range(adet)]
    sab = ["S%d" % (1 + i % 10) for i in range(adet)]
    desen = ["K1", "K2", "K13", "K3", "K4", "K13", "K5", "K6", "K13", "K7"]
    v = []
    for i in range(adet):
        aile = desen[i % 10]
        sahne = lambda k: {"eylem": " ".join(_kelime(i * 10 + k, j) for j in range(5)),
                           "prompt": {"scene": "s%d" % i, "action": "a%d" % i}}
        n_sahne = 2 if sab[i] == "S1" else 3
        v.append({"no": i + 1, "mekanizma": mek[i], "sablon": sab[i], "an": "an numarası %d %s" % (i, isimler[i]), "kanca": "" if aile == "K13" else "Bakın %s %d" % (isimler[i], i),
                  "aile": aile, "kimlik": False, "giris": "giriş %d" % (i // 2), "ortam": "ortam %d" % (i % 6), "ozne": "özne %d" % (i % 2 + 10 * (i % 3)),
                  "sahneler": [sahne(k) for k in range(n_sahne)], "etkilesim_sahne": 1, "sonuc_sahne": n_sahne,
                  "kanca_sorusu": "Bu gerçekten işe yarıyor mu %d?" % i, "cevap_an": n_sahne * 4 - 1,
                  "cta": "Yorumlara LINK yaz", "neden": "n", "kultur": "pazar günü ev ortamı"})
    # özne ardışık aynı olmasın
    for i, x in enumerate(v):
        x["ozne"] = "özne %d" % i
    return {"urun": "sınav", "pazar": pazar, "cta_kelime": "LINK", "videolar": v}


def vaka_02(kok, vaka):
    d = os.path.join(kok, vaka)
    pazar = vaka_pazar("02-kanca-senaryo", vaka)
    yaz(os.path.join(d, "on_uretim_karti.json"), kart(pazar))
    yaz(os.path.join(d, "senaryolar.json"), senaryolar(pazar))
    fam = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9", "K10"]
    yaz(os.path.join(d, "kancalar.json"), [{"id": "V%02d" % (i + 1), "aile": fam[i], "yazi": "Kanca sözü numara %d" % i, "vurgu": "sözü", "kanit": ["[001]"]} for i in range(10)])
    yaz(os.path.join(d, "ayar.json"), {"pazar": pazar, "font": "x.ttf", "cikti": "k.mp4", "yazilar": [{"bas": 0, "bit": 2, "yazi": "x"}], "planlar": []})
    kare_klasoru(os.path.join(d, "onuretim"))
    return d


# ------------------------------------------------------------------ 05 görsel
def vaka_05(kok, vaka, bozuk=None):
    from PIL import Image, ImageDraw
    d = os.path.join(kok, vaka)
    zemin = (0xF2, 0xEE, 0xE8)
    yaz(os.path.join(d, "stil.json"), {"zemin": "#F2EEE8"})
    yaz(os.path.join(d, "METINLER.md"), "# Metinler\n- G1: Sıcakla belirir\n")
    yaz(os.path.join(d, "URUN-KILIDI.md"), "# Ürün kilidi\n- tek parça\n")

    def gorsel(ad, w, h, oran):
        im = Image.new("RGB", (w, h), zemin)
        bw, bh = int(w * oran), int(h * oran)
        if ad.startswith("g0"):
            bw, bh = int(w * 0.80), int(h * 0.80)
        if bozuk == "kenar" and ad.startswith("galeri-1"):
            bw, bh = int(w * 0.97), int(h * 0.97)
        x0, y0 = (w - bw) // 2, (h - bh) // 2
        ImageDraw.Draw(im).rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=30, fill=(40, 80, 120))
        os.makedirs(os.path.join(d, "gorseller"), exist_ok=True)
        im.save(os.path.join(d, "gorseller", ad))
    gorsel("g0-feed.png", 1500, 1500, 0.8)
    for i in (1, 2, 3):
        gorsel("galeri-%d.png" % i, 1080, 1080, 0.6)
    gorsel("b1-masaustu.png", 1920, 800, 0.7)
    gorsel("b2-mobil.png", 1080, 1350, 0.6)
    return d


# ------------------------------------------------------------------ 06 / 07
BAZAAR_ALANLAR = ("no urun trendyol_link alis_tl yorum puan satici_sayisi satici gorsel_bakildi mekanizma aile viral_db viral_video "
                  "meta_reklam onerilen_satis_tl on_karar karar neden okuma_tarihi").split()


def vaka_06(kok, vaka):
    d = os.path.join(kok, vaka)
    pazar = vaka_pazar("06-urun-avi", vaka)
    ad = {"a-kolay": "Isıyla renk değiştiren kupa", "b-zor": "Tüy toplayıcı rulo", "c-tuzak": "Duruş düzeltici bant"}[vaka]
    neden = "Mekanizma görüntüde kanıtlanır; PLT-01 platform riski: iddia yok, imâ yolu." if vaka == "c-tuzak" else "Mekanizma görüntüde kanıtlanır."
    if pazar == "TR":
        satir = dict.fromkeys(BAZAAR_ALANLAR, "")
        satir.update(no="1", urun=ad, trendyol_link="https://www.trendyol.com/x-p-100", alis_tl="200", yorum="500", puan="4,5", satici_sayisi="3",
                     meta_reklam="1", onerilen_satis_tl="500", viral_db="yok", neden=neden, okuma_tarihi="2026-11-23")
        yaz(os.path.join(d, "adaylar.tsv"), "\t".join(BAZAAR_ALANLAR) + "\n" + "\t".join(satir[a] for a in BAZAAR_ALANLAR) + "\n")
    else:
        yaz(os.path.join(d, "adaylar.md"), "| ürün | link | satış | fiyat | dna | a | b | c | d | durum | not |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
            "| %s | https://www.aliexpress.com/item/1005001234567890.html | 2300 sold (ürün sayfası) | 12.99 normal | 1111100 | 2 | 2 | 1 | 1 | İZLE | %s |\n" % (ad, neden))
    return d


def vaka_07(kok, vaka):
    d = os.path.join(kok, vaka)
    shutil.copy(os.path.join(EKL, "ortak", "sozlesme", "ornek", "magaza-paketi.json"), os.path.join(d if os.path.isdir(d) else (os.makedirs(d) or d), "magaza-paketi.json"))
    yaz(os.path.join(d, "site", "ana-sayfa.md"), "# Ana sayfa\nGünlük kullanım için sade bir ürün.\n")
    yaz(os.path.join(d, "site", "urun-sayfasi.md"), "# Ürün sayfası\nSıcak sıvıyla desen belirir.\n")
    kare_klasoru(os.path.join(d, "ekran"))
    return d


def ses_tabani_04(kok, vaka, taban):
    d = os.path.join(kok, vaka)
    os.makedirs(d, exist_ok=True)
    for ad in ("video.mp4", "muz_stem.wav"):
        shutil.copy(os.path.join(taban, ad), d)
    yaz(os.path.join(d, "ses.json"), {"drop_sn": 3.0})
    yaz(os.path.join(d, "LISANS.md"), "Kurucu seçti: 2026-11-24, söz kapısı: enstrümantal\n\n| dosya | kaynak | lisans |\n|---|---|---|\n| muz_stem.wav | sentetik (kendi üretimimiz) | sentetik, lisans gerekmez |\n")
    yaz(os.path.join(d, "vo.txt"), "Seslendirme yok.\n")
    return d


def mutasyon(oz, kok, vaka, ad, degistir, kapi_adi, beklenen_durum="KALDI", tum=False):
    """kok kopyasında tek bozma yap, koş, ilgili kapının beklenen durumda olduğunu ve çıkışın 1 olduğunu kanıtla."""
    with tempfile.TemporaryDirectory(prefix="sinav_mut_") as m:
        shutil.copytree(os.path.join(kok, vaka), os.path.join(m, vaka))
        degistir(os.path.join(m, vaka))
        rc, cikti, md = kos(oz, m, "--vaka", vaka)
        d = kapi(md, vaka, kapi_adi)
        t("kırma %s: %s → %s %s, çıkış 1" % (oz, ad, kapi_adi, beklenen_durum), d == beklenen_durum and rc == 1, "kapı=%r rc=%s\n%s" % (d, rc, cikti[-500:]))


def main():
    with tempfile.TemporaryDirectory(prefix="sinav_test_") as T:
        taban = os.path.join(T, "taban")
        os.makedirs(taban)
        print("video tabanı kuruluyor (ffmpeg)…")
        video_tabani(taban)

        # ================= 01 =================
        k1 = os.path.join(T, "o01")
        for v in PAZAR:
            vaka_01(k1, v, taban)
        rc, o, md = kos("01", k1)
        for v in PAZAR:
            kal = hepsi_yesil(md, v)
            t("01 doğru çıktı %s: jüri dışı bütün kapılar GEÇTİ" % v, not kal, kal)
            t("01 doğru çıktı %s: jüri referansı yokken kapı olculemedi (sahte geçti yok)" % v, kapi(md, v, "juri") == "olculemedi", kapi(md, v, "juri"))
        t("01 doğru çıktı + referans yok → çıkış 3 (0 değil)", rc == 3, rc)

        def uzat(d):
            ffmpeg("-stream_loop", "1", "-i", os.path.join(d, "video.mp4"), "-c", "copy", os.path.join(d, "x.mp4"))
            shutil.move(os.path.join(d, "x.mp4"), os.path.join(d, "video.mp4"))
        mutasyon("01", k1, "a-kolay", "süre 18 sn", uzat, "sure")
        def yasakli_ayar(d):
            a = json.load(open(os.path.join(d, "ayar.json"), encoding="utf-8"))
            a["planlar"][0]["yazi"] = "Clinically proven, unbreakable"
            yaz(os.path.join(d, "ayar.json"), a)
        mutasyon("01", k1, "a-kolay", "yasaklı iddia (ayar yazısı)", yasakli_ayar, "yasakli")
        def fiyat_ayar(d):
            a = json.load(open(os.path.join(d, "ayar.json"), encoding="utf-8"))
            a["cta"]["satir2"] = "only 199 TL today"
            yaz(os.path.join(d, "ayar.json"), a)
        mutasyon("01", k1, "a-kolay", "ekranda fiyat (ICE-01)", fiyat_ayar, "ice01_fiyat")
        def sessiz(d):
            ffmpeg("-i", os.path.join(d, "video.mp4"), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", os.path.join(d, "x.mp4"))
            shutil.move(os.path.join(d, "x.mp4"), os.path.join(d, "video.mp4"))
        mutasyon("01", k1, "b-zor", "sessiz ses", sessiz, "ses_kapi")
        mutasyon("01", k1, "c-tuzak", "caption'da 'cures back pain'", lambda d: yaz(os.path.join(d, "caption.txt"), "This band cures back pain. Link in bio."), "yasakli")
        mutasyon("01", k1, "b-zor", "müzik stem'i yok (SES-02)", lambda d: os.remove(os.path.join(d, "muz_stem.wav")), "dosyalar")
        def urun_tipi(d):
            a = json.load(open(os.path.join(d, "ayar.json"), encoding="utf-8"))
            a.pop("urun_tipi", None)
            yaz(os.path.join(d, "ayar.json"), a)
        mutasyon("01", k1, "b-zor", "ekransız vaka ekranlı ayarlandı", urun_tipi, "ayar_beklenen")

        # boş / eksik klasör
        bos = os.path.join(T, "bos")
        os.makedirs(os.path.join(bos, "a-kolay"))
        rc, o, md = kos("01", bos)
        t("boş vaka klasörü → KALDI, çıkış 1", rc == 1 and kapi(md, "a-kolay", "cikti") == "KALDI", o)
        rc, o, md = kos("01", os.path.join(T, "yok-hic"))
        t("hiç olmayan çıktı klasörü → çıkış 1 (geçti yok)", rc == 1 and "Genel durum: **KALDI**" in md, o)

        # jüri hattı uçtan uca: sahte referans + sahte KOR kopyaları (gerçek referans verisi kullanılmaz)
        sk = os.path.join(T, "sinav-kok")
        shutil.copytree(os.path.join(EKL, "ortak", "sinav"), sk)
        rk = os.path.join(T, "refkok")
        satir = []
        for i, pz in enumerate(["US", "US", "US", "TR", "TR", "TR", "DE", "DE", "DE"]):
            kare_klasoru(os.path.join(rk, "kareler", "R%d" % i), renk=(40 + 20 * (i % 5), 90, 130))
            satir.append("S%02d\t%s\t\t\t1000000/?\tvideo\tkareler/R%d\tsahte" % (i, pz, i))
        yaz(os.path.join(sk, "01-urun-videosu", "referanslar.tsv"), "id\tpazar\thesap\tkaynak_url\tolcum\ttur\tkare_panosu_yolu\tnot\n" + "\n".join(satir) + "\n")
        env = {"SINAV_KOK": sk}
        rc, o, md = kos("01", k1, "--referans-kok", rk, env=env)
        t("jüri: referanslar dolu → pano hazırlandı, kapı bekliyor (çıkış 3)", all(kapi(md, v, "juri") == "bekliyor" for v in PAZAR) and rc == 3, md[-800:])

        def kor_yaz(oz_dir, bizim_puan):
            for v in PAZAR:
                jd = os.path.join(oz_dir, v, "juri")
                es = json.load(open(os.path.join(jd + ".gizli", "_esleme.json"), encoding="utf-8"))   # eşleşme jüri dizininin dışında (#1)
                oidler = sorted(es["ogeler"])
                bizim = [k for k in oidler if es["ogeler"][k]["tur"] == "bizim"][0]
                refler = [k for k in oidler if k != bizim]
                alanlar = ["dururdum", "anlasilir", "gercek", "yazi", "ritim", "gonderirdim"]
                for n in (1, 2, 3):
                    ters = {oid: kod for kod, oid in es["kopyalar"][str(n)].items()}
                    p = {ters[bizim]: {a: bizim_puan + (i % 2) for i, a in enumerate(alanlar)}}
                    for j, r in enumerate(refler):
                        p[ters[r]] = {a: 6 + ((i + j) % 2) for i, a in enumerate(alanlar)}
                    sira = [ters[bizim]] + [ters[r] for r in refler] if bizim_puan >= 7 else [ters[r] for r in refler] + [ters[bizim]]
                    yaz(os.path.join(jd, "kopya-%d" % n, "KOR-%d.json" % n), {"puanlar": p, "sira": sira})
        kor_yaz(k1, 8)
        rc, o, md = kos("01", k1, "--referans-kok", rk, env=env)
        t("jüri: yüksek puanlı 3 kör kopya → bütün vakalar GEÇTİ, çıkış 0 (0 ulaşılabilir)", rc == 0 and all(kapi(md, v, "juri") == "GEÇTİ" for v in PAZAR), o + md[-600:])
        kor_yaz(k1, 3)
        rc, o, md = kos("01", k1, "--referans-kok", rk, env=env)
        t("jüri: düşük puan → KALDI, çıkış 1", rc == 1 and all(kapi(md, v, "juri") == "KALDI" for v in PAZAR), o + md[-600:])

        # ================= 02 =================
        k2 = os.path.join(T, "o02")
        for v in PAZAR:
            vaka_02(k2, v)
        rc, o, md = kos("02", k2)
        for v in PAZAR:
            kal = hepsi_yesil(md, v)
            t("02 doğru çıktı %s: jüri dışı bütün kapılar GEÇTİ" % v, not kal, kal)
        t("02 doğru çıktı + referans yok → çıkış 3", rc == 3, rc)
        def az_senaryo(d):
            s = json.load(open(os.path.join(d, "senaryolar.json"), encoding="utf-8"))
            s["videolar"] = s["videolar"][:12]
            yaz(os.path.join(d, "senaryolar.json"), s)
        mutasyon("02", k2, "a-kolay", "12 senaryo (30 şart)", az_senaryo, "senaryo_adedi")
        def kanca_yasak(d):
            k = json.load(open(os.path.join(d, "kancalar.json"), encoding="utf-8"))
            k[0]["yazi"] = "This cures back pain fast"
            yaz(os.path.join(d, "kancalar.json"), k)
        mutasyon("02", k2, "c-tuzak", "kancada 'cures back pain'", kanca_yasak, "yasakli")
        def az_kanca(d):
            k = json.load(open(os.path.join(d, "kancalar.json"), encoding="utf-8"))
            yaz(os.path.join(d, "kancalar.json"), k[:6])
        mutasyon("02", k2, "b-zor", "6 kanca (10 şart)", az_kanca, "kanca_varyasyon")
        def ayni_aile(d):
            s = json.load(open(os.path.join(d, "senaryolar.json"), encoding="utf-8"))
            s["videolar"][1]["aile"] = s["videolar"][0]["aile"]
            yaz(os.path.join(d, "senaryolar.json"), s)
        mutasyon("02", k2, "a-kolay", "aynı kanca ailesi art arda", ayni_aile, "senaryo_kontrol")

        # ================= 03 =================
        if not HIZLI:
            k3 = os.path.join(T, "o03")
            h = os.path.join(T, "h3")
            sys.path.insert(0, os.path.join(CUT, "hikaye"))
            import test_hikaye as TH
            yol, a = TH.kur(h)
            r = subprocess.run([sys.executable, os.path.join(CUT, "hikaye", "uret.py"), yol, "--sessiz-ffmpeg"], capture_output=True, text=True)
            t("03 gerçek hikâye hattı (uret.py) çıkış 0", r.returncode == 0, r.stdout[-300:] + r.stderr[-300:])
            if r.returncode == 0:
                for v in PAZAR:
                    d = os.path.join(k3, v)
                    shutil.copytree(os.path.join(h, "stok"), os.path.join(d, "stok"))
                    shutil.copy(os.path.join(h, "TESLIM", a["ad"] + ".mp4"), os.path.join(d, "video.mp4"))
                    shutil.copy(os.path.join(h, "ses", "stem_" + a["ad"], "muz_teslim.wav"), os.path.join(d, "muz_stem.wav"))
                    shutil.copy(os.path.join(h, "ayar.json"), os.path.join(d, "ayar.json"))
                    pz = vaka_pazar("03-hikaye-videosu", v)
                    yaz(os.path.join(d, "on-uretim-karti.json"), kart(pz, fmt="hikaye"))
                    yaz(os.path.join(d, "caption.txt"), CAPTION[pz])
                rc, o, md = kos("03", k3)
                for v in PAZAR:
                    kal = hepsi_yesil(md, v)
                    t("03 doğru çıktı %s: jüri dışı bütün kapılar GEÇTİ" % v, not kal, kal)
                t("03 doğru çıktı + referans yok → çıkış 3", rc == 3, rc)
                mutasyon("03", k3, "a-kolay", "süre 12 sn", lambda d: (ffmpeg("-i", os.path.join(d, "video.mp4"), "-t", "12", "-c", "copy", os.path.join(d, "x.mp4")), shutil.move(os.path.join(d, "x.mp4"), os.path.join(d, "video.mp4"))), "sure")
                def fiyatli(d):
                    a2 = json.load(open(os.path.join(d, "ayar.json"), encoding="utf-8"))
                    a2["sahneler"][1]["ana"] = "Only 29 USD today"
                    yaz(os.path.join(d, "ayar.json"), a2)
                mutasyon("03", k3, "b-zor", "ekranda fiyat", fiyatli, "hikaye_kur_dogrula")
                mutasyon("03", k3, "c-tuzak", "caption'da sağlık iddiası", lambda d: yaz(os.path.join(d, "caption.txt"), "Tedavi eder, bel ağrısını geçirir."), "yasakli")
        else:
            print("NOT: 03 atlandı (--hizli)")

        # ================= 04 =================
        k4 = os.path.join(T, "o04")
        for v in PAZAR:
            ses_tabani_04(k4, v, taban)
        rc, o, md = kos("04", k4)
        for v in PAZAR:
            kal = hepsi_yesil(md, v)
            t("04 doğru çıktı %s: bütün kapılar GEÇTİ (jüri uygulanmaz)" % v, not kal and kapi(md, v, "juri") == "uygulanmaz", kal)
        t("04 doğru çıktı → çıkış 0 (jüri bu özellikte tanımsız, sahte kapı yok)", rc == 0, o)
        mutasyon("04", k4, "a-kolay", "sessiz video (ses deliği)", sessiz, "ses_kapi")
        mutasyon("04", k4, "b-zor", "müzik stem'i yok", lambda d: os.remove(os.path.join(d, "muz_stem.wav")), "dosyalar")
        mutasyon("04", k4, "c-tuzak", "telifli parça kaydı", lambda d: yaz(os.path.join(d, "LISANS.md"), "Kurucu seçti: 2026-11-24, söz kapısı: temiz\nWham! Last Christmas, kaynak https://example.org, lisans Mixkit\n"), "lisans_kaydi")
        mutasyon("04", k4, "c-tuzak", "VO'da 'cures back pain'", lambda d: yaz(os.path.join(d, "vo.txt"), "This cures back pain."), "yasakli")
        mutasyon("04", k4, "a-kolay", "lisans kaydı: söz kapısı satırı yok", lambda d: yaz(os.path.join(d, "LISANS.md"), "kaynak sentetik\n"), "lisans_kaydi")

        # ================= 05 =================
        k5 = os.path.join(T, "o05")
        for v in PAZAR:
            vaka_05(k5, v)
        rc, o, md = kos("05", k5)
        for v in PAZAR:
            kal = [x for x in hepsi_yesil(md, v) if x[0] not in ("K2_yazim_ocr", "K1_sadakat")]
            t("05 doğru çıktı %s: K3 ve metin kapıları GEÇTİ" % v, not kal, kal)
            t("05 doğru çıktı %s: K1 sadakat olculemedi (betik yok, sahte geçti yok)" % v, kapi(md, v, "K1_sadakat") == "olculemedi")
        t("05 doğru çıktı → çıkış 3 (0 değil)", rc == 3, rc)
        mutasyon("05", k5, "a-kolay", "kenar payı < %6", lambda d: (shutil.rmtree(d), vaka_05(os.path.dirname(d), os.path.basename(d), bozuk="kenar")), "K3_tuval_olcu")
        mutasyon("05", k5, "b-zor", "yanlış B1 boyutu", lambda d: __import__("PIL.Image", fromlist=["Image"]).new("RGB", (1900, 800), (0xF2, 0xEE, 0xE8)).save(os.path.join(d, "gorseller", "b1-masaustu.png")), "K3_tuval_olcu")
        mutasyon("05", k5, "c-tuzak", "METINLER'de klinik/yüzde iddiası", lambda d: yaz(os.path.join(d, "METINLER.md"), "- Klinik olarak kanıtlanmış, %98 memnuniyet\n"), "yasakli")
        mutasyon("05", k5, "a-kolay", "SADAKAT.md'de ❌", lambda d: yaz(os.path.join(d, "SADAKAT.md"), "G1 ❌ parça sayısı yanlış\n"), "K1_sadakat")
        # denetim #2/#4: üreten ≠ denetleyen. KİM DENETLEDİ yok ya da ÖZ-DENETİM → kim_denetledi olculemedi; bağımsız rol adı → GEÇTİ
        def kd_dene(ad, metin, beklenen):
            with tempfile.TemporaryDirectory(prefix="sinav_kd_") as m_:
                shutil.copytree(os.path.join(k5, "a-kolay"), os.path.join(m_, "a-kolay"))
                yaz(os.path.join(m_, "a-kolay", "SADAKAT.md"), metin)
                rc_, cikti_, md_ = kos("05", m_, "--vaka", "a-kolay")
                t("05 SADAKAT.md %s → kim_denetledi %s" % (ad, beklenen), kapi(md_, "a-kolay", "kim_denetledi") == beklenen, cikti_[-400:] + md_[-500:])
        kd_dene("KİM DENETLEDİ satırı yok", "G1 ✅ ürün sadık\n", "olculemedi")
        kd_dene("KİM DENETLEDİ: ÖZ-DENETİM", "G1 ✅ ürün sadık\nKİM DENETLEDİ: ÖZ-DENETİM\n", "olculemedi")
        kd_dene("ÜRETEN: forge, KİM DENETLEDİ: forge", "ÜRETEN: forge\nG1 ✅ ürün sadık\nKİM DENETLEDİ: forge\n", "olculemedi")
        kd_dene("KİM DENETLEDİ: sentinel (bağımsız)", "ÜRETEN: forge\nG1 ✅ ürün sadık\nKİM DENETLEDİ: sentinel\n", "GEÇTİ")

        # ================= 06 =================
        k6 = os.path.join(T, "o06")
        for v in PAZAR:
            vaka_06(k6, v)
        rc, o, md = kos("06", k6)
        for v in PAZAR:
            kal = hepsi_yesil(md, v)
            t("06 doğru çıktı %s: bütün kapılar GEÇTİ (jüri uygulanmaz)" % v, not kal, kal)
        t("06 doğru çıktı → çıkış 0", rc == 0, o)
        def bozuk_06(d):
            for f in ("adaylar.tsv", "adaylar.md"):
                p = os.path.join(d, f)
                if os.path.exists(p):
                    s = open(p, encoding="utf-8").read()
                    s = s.replace("https://www.trendyol.com/x-p-100", "x-p-100").replace("2300 sold (ürün sayfası) | 12.99 normal | 1111100", "kart | yeni müşteri 1 | 1000000")
                    yaz(p, s)
        mutasyon("06", k6, "a-kolay", "hunter denetle: arama kartından satış + yeni müşteri fiyatı (DE vaka)", bozuk_06, "firsat_denetle")
        mutasyon("06", k6, "c-tuzak", "trendyol denetle bozuk satır (TR vaka)", bozuk_06, "trendyol_denetle")
        def iddia_06(d):
            for f in ("adaylar.tsv", "adaylar.md"):
                p = os.path.join(d, f)
                if os.path.exists(p):
                    yaz(p, open(p, encoding="utf-8").read().replace("Mekanizma", "Bu ürün bel ağrısını tedavi eder; Mekanizma"))
        mutasyon("06", k6, "c-tuzak", "tabloda 'tedavi eder'", iddia_06, "yasakli")
        mutasyon("06", k6, "c-tuzak", "platform riski notu (zorunlu) yok", lambda d: [yaz(os.path.join(d, f), open(os.path.join(d, f), encoding="utf-8").read().replace("PLT-01 platform riski: ", "")) for f in ("adaylar.tsv", "adaylar.md") if os.path.exists(os.path.join(d, f))], "zorunlu_metin")

        # ================= 07 =================
        k7 = os.path.join(T, "o07")
        for v in PAZAR:
            vaka_07(k7, v)
        rc, o, md = kos("07", k7)
        for v in PAZAR:
            t("07 doğru çıktı %s: iddia kapısı GEÇTİ, hız/erişim/arama/dönüşüm olculemedi" % v,
              kapi(md, v, "iddia_kontrol") == "GEÇTİ" and all(kapi(md, v, x) == "olculemedi" for x in ("hiz_cwv", "erisim_wcag", "arama_merchant", "donusum_kullanilabilirlik")), md[-900:])
        t("07 doğru çıktı → çıkış 3 (olculemedi; sahte geçti yok)", rc == 3, rc)
        for v in PAZAR:
            t("07 doğru çıktı %s: sözleşme kapısı GEÇTİ (ornek paket: ad kaynaklı, fiyat dolu)" % v, kapi(md, v, "paket_sozlesme") == "GEÇTİ", md[-700:])
        # denetim #17: fiyat 0 / yer tutucu görsel / kaynaksız marka adı → paket_sozlesme KALDI; dürüst null + eksik[] → olculemedi (sahte geçti yok)
        def paket_boz(d, **kw):
            pj = os.path.join(d, "magaza-paketi.json")
            p_ = json.load(open(pj, encoding="utf-8"))
            for yol, deger in kw.items():
                a_, b_ = yol.split("__") if "__" in yol else (yol, None)
                if b_ is None:
                    p_[a_] = deger
                elif deger == "__sil__":
                    p_[a_].pop(b_, None)
                else:
                    p_[a_][b_] = deger
            yaz(pj, p_)
        mutasyon("07", k7, "b-zor", "mağaza paketinde fiyat 0 (yer tutucu)", lambda d: paket_boz(d, urun__fiyat=0), "paket_sozlesme")
        mutasyon("07", k7, "a-kolay", "mağaza paketinde 'yok-yer-tutucu.jpg' görseli", lambda d: paket_boz(d, gorseller=[{"kod": "G0", "dosya": "yok-yer-tutucu.jpg"}]), "paket_sozlesme")
        mutasyon("07", k7, "c-tuzak", "mağaza paketinde marka adının kaynağı yok (uydurma ad)", lambda d: paket_boz(d, marka__ad_kaynak="__sil__"), "paket_sozlesme")
        with tempfile.TemporaryDirectory(prefix="sinav_eksik_") as m:
            shutil.copytree(os.path.join(k7, "a-kolay"), os.path.join(m, "a-kolay"))
            paket_boz(os.path.join(m, "a-kolay"), urun__fiyat=None, urun__para=None, eksik=["urun.fiyat", "urun.para"])
            rc, cikti, md4 = kos("07", m, "--vaka", "a-kolay")
            t("07 fiyat null + eksik[] (dürüst eksik): paket_sozlesme olculemedi (KALDI da GEÇTİ de değil), çıkış 3", kapi(md4, "a-kolay", "paket_sozlesme") == "olculemedi" and rc == 3, cikti[-400:])
        # denetim #22: yerel Lighthouse + axe (hiz_cwv / erisim_wcag); ekran/*.html varsa ölçülür, yoksa olculemedi
        yok_html = [kapi(md, v, x) for v in PAZAR for x in ("hiz_cwv", "erisim_wcag")]
        t("07 ekranda HTML yok → hiz_cwv/erisim_wcag olculemedi (sahte geçti yok)", all(x == "olculemedi" for x in yok_html), yok_html)
        if web_olcum_hazir():
            HTML = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mug</title></head>'
                    '<body style="background:#ffffff;color:#111111"><main><h1>Heat mug</h1><p style="color:%s">Pour hot liquid.</p></main>%s</body></html>')
            os.environ["SINAV_WEB_KOSU"] = "1"
            with tempfile.TemporaryDirectory(prefix="sinav_web_") as w:
                shutil.copytree(os.path.join(k7, "a-kolay"), os.path.join(w, "a-kolay"))
                yaz(os.path.join(w, "a-kolay", "ekran", "ana-sayfa.html"), HTML % ("#111111", ""))
                rc, cikti, md3 = kos("07", w, "--vaka", "a-kolay")
                t("07 temiz HTML: hiz_cwv + erisim_wcag GEÇTİ ('yerel' etiketiyle)", kapi(md3, "a-kolay", "hiz_cwv") == "GEÇTİ" and kapi(md3, "a-kolay", "erisim_wcag") == "GEÇTİ" and "[yerel]" in md3, md3[-900:])
            mutasyon("07", k7, "a-kolay", "ekran HTML'inde açık gri kontrast (1,91:1)", lambda d: yaz(os.path.join(d, "ekran", "ana-sayfa.html"), HTML % ("#bbbbbb", "")), "erisim_wcag")
            mutasyon("07", k7, "b-zor", "ekran HTML'i ana iş parçacığını 3 sn kilitliyor", lambda d: yaz(os.path.join(d, "ekran", "ana-sayfa.html"), HTML % ("#111111", "<script>var t=Date.now();while(Date.now()-t<3000){}</script>")), "hiz_cwv")
            os.environ.pop("SINAV_WEB_KOSU", None)
        else:
            print("ATLANDI web ölçüm testleri: Lighthouse/axe/Chrome yok (hiz_cwv/erisim_wcag bu koşuda ÖLÇÜLMEDİ)")
        mutasyon("07", k7, "a-kolay", "sayfada onaysız sayı iddiası", lambda d: yaz(os.path.join(d, "site", "urun-sayfasi.md"), "30 kg taşır, %98 memnuniyet\n"), "iddia_kontrol")
        mutasyon("07", k7, "c-tuzak", "sayfada 'cures back pain'", lambda d: yaz(os.path.join(d, "site", "ana-sayfa.md"), "This band cures back pain.\n"), "yasakli")
        # denetim 2026-11-25 #6/#12: kanıt anı / iç dil sızıntısı (07 tur1 b-zor ve c-tuzak kaçağı) ve mobil ekran taşması
        for v in PAZAR:
            t("07 doğru çıktı %s: kanıt anı sızıntı kapısı GEÇTİ" % v, kapi(md, v, "kanit_ani_sizinti") == "GEÇTİ", md[-600:])
        mutasyon("07", k7, "c-tuzak", "site metninde '## Der Moment' iç başlığı", lambda d: yaz(os.path.join(d, "site", "ana-sayfa.md"), "# Ana sayfa\n## Der Moment\nSchultern zurück.\n"), "kanit_ani_sizinti")
        mutasyon("07", k7, "a-kolay", "site metninde '## The moment' iç başlığı", lambda d: yaz(os.path.join(d, "site", "ana-sayfa.md"), "# Home\n## The moment\nHot liquid goes in.\n"), "kanit_ani_sizinti")
        mutasyon("07", k7, "b-zor", "site metni 'Kanıt, sayfanın kendisidir.' ile başlıyor", lambda d: yaz(os.path.join(d, "site", "urun-sayfasi.md"), "# Ürün\nRuloyu gezdirirsin. Kanıt, sayfanın kendisidir.\n"), "kanit_ani_sizinti")
        mutasyon("07", k7, "b-zor", "vaka kanit_ani cümlesi (çekim talimatı) aynen sitede", lambda d: yaz(os.path.join(d, "site", "urun-sayfasi.md"), "# Ürün\nRuloyu koltukta tek hamlede gezdirmek yeter.\n"), "kanit_ani_sizinti")
        CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(CH):
            html = ("<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><body style='margin:0;font:28px sans-serif'>"
                    "<p style='padding:0 16px'>Bu satır yeterince uzun bir paragraf olarak yazıldı ve dar ekranda alt satıra sarmalıdır.</p>"
                    "<div style='background:#cde;height:200px;margin:16px'></div>")

            def mobil_iyi(d):
                yaz(os.path.join(d, "ekran", "x.html"), html)
                subprocess.run([sys.executable, os.path.join(EKL, "ortak", "mobil_ekran.py"), "ekran", os.path.join(d, "ekran", "x.html"), os.path.join(d, "ekran", "x-390.png")], capture_output=True)

            def mobil_yanlis(d):   # eski hata: pencere 390 istenir, Chrome ≥ 500 px düzenle çizer ve kırpar
                yaz(os.path.join(d, "ekran", "x.html"), html)
                subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=390,844", "--screenshot=" + os.path.join(d, "ekran", "x-390.png"),
                                "file://" + os.path.join(d, "ekran", "x.html")], capture_output=True)
            with tempfile.TemporaryDirectory(prefix="sinav_mob_") as m:
                shutil.copytree(os.path.join(k7, "a-kolay"), os.path.join(m, "a-kolay"))
                mobil_iyi(os.path.join(m, "a-kolay"))
                rc, cikti, md2 = kos("07", m, "--vaka", "a-kolay")
                t("07 mobil ekran doğru yöntemle (iframe) alındı -> mobil_ekran GEÇTİ", kapi(md2, "a-kolay", "mobil_ekran") == "GEÇTİ", cikti[-400:])
            mutasyon("07", k7, "a-kolay", "mobil ekran eski yöntemle (pencere 390, kırpılmış düzen)", mobil_yanlis, "mobil_ekran")
        else:
            print("ATLANDI mobil ekran testleri: Chrome yok (bu kapı bu koşuda ÖLÇÜLMEDİ)")

        # ================= --hepsi (denetim #11): 7 sınav tek komut, tek satır özet + çıkış kodu =================
        with tempfile.TemporaryDirectory(prefix="sinav_hepsi_") as hk:
            e = dict(os.environ)
            r = subprocess.run([sys.executable, KOS, "--hepsi", hk], capture_output=True, text=True, env=e)
            t("--hepsi: boş kök -> 1, 7 özelliğin hepsi KALDI (çıktısı olmayan sınav yeşil sayılmaz)",
              r.returncode == 1 and "HEPSİ: 7 özellik · GEÇTİ 0 · KALDI 7" in r.stdout, r.stdout[-500:])
            if os.path.isdir(os.path.join(T, "o04")):
                os.symlink(os.path.join(T, "o04"), os.path.join(hk, "04-ses-muzik"))
                r = subprocess.run([sys.executable, KOS, "--hepsi", hk], capture_output=True, text=True, env=e)
                t("--hepsi: yalnız 04 çıktısı var -> 04 GEÇTİ, öbürleri KALDI, çıkış 1 (hepsi geçmeden 0 yok)",
                  r.returncode == 1 and "04-ses-muzik: GEÇTİ" in r.stdout and "GEÇTİ 1 · KALDI 6" in r.stdout, r.stdout[-700:])
                t("--hepsi: önceki SONUC.md ezilmez (SONUC-HEPSI.md yazılır)", os.path.exists(os.path.join(T, "o04", "SONUC-HEPSI.md")))

    kalan = sonuc.count(False)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
