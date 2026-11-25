#!/usr/bin/env python3
"""analiz.db -> plugins/viral-urun-ekibi/ortak/bilgi/viral-urunler.tsv (SANSÜRLÜ, deterministik).

Kullanım: python3 scripts/bilgi_paketi.py <analiz.db> [--cikti DOSYA]

Beyaz liste: yalnız aşağıdaki sütunlar çıkar. url, hesap, hesap_id, kaynak_ref, not_dosyasi, sayilar_ham, yorum metni,
reklam_mi ve ham urun_id (hesap adı taşıyabilir) ASLA alınmaz. Ürün kimliği ad kökünden türetilen kısa özettir.
Aynı db -> bayt bayt aynı dosya (sıralı, saat yok; 'guncelleme' db içindeki en yeni kayıt tarihidir).
"""
import hashlib
import os
import re
import sqlite3
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EKLENTI = os.path.join(KOK, "plugins", "viral-urun-ekibi")
VARSAYILAN_CIKTI = os.path.join(EKLENTI, "ortak", "bilgi", "viral-urunler.tsv")
KATALOG = os.path.join(EKLENTI, "ortak", "bilgi", "urun-katalogu.md")

SUTUNLAR = ["urun_id", "ad_jenerik", "aile", "nis", "pazarlar", "video_sayisi", "hesap_sayisi", "viral_hesap_sayisi",
            "en_yuksek_izlenme", "toplam_izlenme", "medyan_izlenme_takipci", "ilk_gorulme", "son_gorulme", "hukum",
            "guncelleme"]

# Büyük harfli ama marka olmayan sözcükler (ürün tarifinde kalır).
JENERIK_BUYUK = {"noel", "baba", "cadılar", "bayramı", "sevgililer", "günü", "anneler", "yılbaşı", "halloween", "kış",
                 "yaz", "usb", "led", "uv", "rgb", "tv", "ai", "3d", "rfid", "usb-c", "pet", "diy", "abd", "tr", "pvc",
                 "pu", "xl", "xxl", "hdmi", "wifi", "gps", "pil", "mp3", "uhd", "fm", "ip", "no", "ve", "ile", "bir"}

BILINEN_MARKA = {"apple", "samsung", "nike", "lego", "disney", "pokemon", "mario", "ryobi", "ikea", "xiaomi", "sony", "dyson",
                 "stanley", "hello", "kitty", "barbie", "minecraft", "tesla", "bmw", "mercedes", "porsche", "lamborghini",
                 "airpods", "android", "google", "amazon", "netflix", "tiktok", "instagram", "youtube", "spotify", "starbucks",
                 "nintendo", "playstation", "xbox", "pandora", "bluey", "labubu", "stitch", "grogu", "yoda", "hamilton"}


def fold(s):
    return (s or "").translate(str.maketrans("ıİşŞğĞüÜöÖçÇ", "iissgguuoocc")).lower()


def katalog_marka_jetonlari():
    """urun-katalogu.md son sütunundaki @hesap ve alan adı gövdelerinden marka benzeri jetonlar (>=5 harf)."""
    jetonlar = set()
    if not os.path.isfile(KATALOG):
        return jetonlar
    with open(KATALOG, encoding="utf-8") as f:
        for satir in f:
            if not satir.startswith("| "):
                continue
            hucre = satir.rstrip("\n").rstrip("|").split("|")[-1]
            adaylar = re.findall(r"@([A-Za-z0-9_.]+)", hucre)
            adaylar += [m.group(1) for m in re.finditer(r"([A-Za-z0-9-]+)\.(?:com|store|shop|co|net|org|app|me|io|de|es|tr)\b", hucre)]
            for a in adaylar:
                for t in re.split(r"[^a-z0-9]+", a.lower()):
                    if len(t) >= 5 and not t.isdigit():
                        jetonlar.add(t)
    return jetonlar


def jenerik_kelime_kumesi(adlar, esik=6):
    """Çok sayıda üründe geçen sözcük jeneriktir; marka jetonu sayılmaz."""
    sayac = {}
    for ad in adlar:
        for t in set(re.split(r"[^a-z0-9]+", fold(ad))):
            if t:
                sayac[t] = sayac.get(t, 0) + 1
    return {t for t, n in sayac.items() if n >= esik}


def jenerik_ad(ad, marka_jetonlari, yaygin):
    s = (ad or "").replace("\t", " ").replace("\n", " ")
    s = s.split(" — ")[0]
    s = re.sub(r"\([^)]*\)?", " ", s)          # parantez içi (iç referans, marka, kod) atılır
    s = re.sub(r"\s[-–]\s.*$", "", s)          # " - ..." kuyruğu
    kelimeler = s.split()
    cikti = []
    for i, k in enumerate(kelimeler):
        cekirdek = re.sub(r"^[^\wçğıöşüÇĞİÖŞÜ]+|[^\wçğıöşüÇĞİÖŞÜ]+$", "", k)
        if not cekirdek:
            continue
        f = fold(cekirdek)
        jeton = re.sub(r"[^a-z0-9]", "", f)
        if "@" in k or "http" in f or "www" in f or "/" in k and re.search(r"\.[a-z]{2,}", f):
            continue
        marka = False
        if f in JENERIK_BUYUK or f.rstrip("'sı") in JENERIK_BUYUK:
            marka = False
        elif re.search(r"[A-Za-zÇĞİÖŞÜçğıöşü]", cekirdek) and re.search(r"\d", cekirdek) and re.search(r"[A-ZÇĞİÖŞÜ]", cekirdek):
            marka = True                         # model kodu: AJ350A, Tina2C
        elif re.search(r"[a-zçğıöşü][A-ZÇĞİÖŞÜ]", cekirdek) or f.split("'")[0] in BILINEN_MARKA:
            marka = True                         # camelCase (iPhone, MagSafe, ShowerDock) ya da bilinen marka
        elif len(cekirdek) >= 2 and cekirdek.isupper():
            marka = True                         # HP, DIY dışı tamamen büyük harf
        elif i > 0 and cekirdek[0].isupper():
            marka = True                         # cümle ortasında özel ad
        elif i == 0 and cekirdek[0].isupper() and jeton in marka_jetonlari:
            marka = True
        if jeton and jeton in marka_jetonlari and jeton not in yaygin:
            marka = True
        if not marka:
            cikti.append(k)
    s = " ".join(cikti)
    s = re.sub(r"\b(ile|ve|gibi|tipi|ayn[ıi]|markalı|marka)\b\s*$", "", s, flags=re.I).strip(" ,;:-–'\"")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def urun_kodu(urun_id):
    return "v" + hashlib.sha256(("viral-urunler|" + (urun_id or "")).encode("utf-8")).hexdigest()[:8]


def tarih(s):
    s = (s or "").strip()
    return s[:10] if re.match(r"^\d{4}-\d{2}-\d{2}", s) else ""


def sayi_txt(v):
    if v is None:
        return ""
    if isinstance(v, float):
        return ("%.2f" % v).rstrip("0").rstrip(".")
    return str(int(v)) if isinstance(v, int) else str(v)


def uret(db_yolu):
    c = sqlite3.connect("file:%s?mode=ro" % db_yolu, uri=True)
    satirlar = c.execute(
        "SELECT urun_id, ad, aile, nis, hesap_sayisi, video_sayisi, viral_hesap_sayisi, toplam_izlenme, en_yuksek_izlenme,"
        " medyan_izlenme_takipci, hukum FROM v_viral_urun ORDER BY urun_id").fetchall()
    toplu = {}
    for uid, pazarlar, ilk, son, gunc in c.execute(
            "SELECT urun_id, group_concat(DISTINCT CASE WHEN pazar IN ('bilinmiyor','') THEN NULL ELSE pazar END),"
            " min(COALESCE(NULLIF(yayin_tarihi,''), NULLIF(okuma_tarihi,''), substr(guncelleme,1,10))),"
            " max(COALESCE(NULLIF(yayin_tarihi,''), NULLIF(okuma_tarihi,''), substr(guncelleme,1,10))),"
            " max(guncelleme) FROM video GROUP BY urun_id"):
        toplu[uid] = (pazarlar, ilk, son, gunc)
    c.close()
    marka = katalog_marka_jetonlari()
    yaygin = jenerik_kelime_kumesi([r[1] for r in satirlar])
    cikti = []
    for (uid, ad, aile, nis, hs, vs, vhs, ti, eyi, med, hukum) in satirlar:
        pazarlar, ilk, son, gunc = toplu.get(uid, (None, None, None, None))
        pz = "|".join(sorted({p.strip() for p in (pazarlar or "").split(",") if p.strip()}))
        cikti.append([urun_kodu(uid), jenerik_ad(ad, marka, yaygin), aile or "", nis or "", pz, sayi_txt(vs), sayi_txt(hs),
                      sayi_txt(vhs), sayi_txt(eyi), sayi_txt(ti), sayi_txt(med), tarih(ilk), tarih(son), hukum or "", tarih(gunc)])
    cikti.sort(key=lambda r: r[0])
    kodlar = [r[0] for r in cikti]
    if len(set(kodlar)) != len(kodlar):
        raise SystemExit("HATA: ürün kodu çakışması")
    return cikti


def yaz(satirlar, yol):
    govde = "\t".join(SUTUNLAR) + "\n" + "".join("\t".join(h.replace("\t", " ").replace("\n", " ") for h in r) + "\n" for r in satirlar)
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(govde)


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    db = argv[1]
    cikti = VARSAYILAN_CIKTI
    if "--cikti" in argv:
        cikti = argv[argv.index("--cikti") + 1]
    if not os.path.isfile(db):
        print("HATA: db yok: %s" % db)
        return 2
    satirlar = uret(db)
    os.makedirs(os.path.dirname(cikti), exist_ok=True)
    yaz(satirlar, cikti)
    print("%d ürün -> %s" % (len(satirlar), cikti))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
