#!/usr/bin/env python3
"""bazaar_kontrol.py: Bazaar (Trendyol fırsat avı) yardımcısı (yalnız Python 3 standart kütüphanesi).

Alt komutlar (--klasor varsayılan: is/firsat/trendyol):
  kota durum|kaydet <arama|urun> <hedef>|kilit [sebep]   günlük tavan, istek aralığı, kilit (kota.tsv)
  tekrar <link ya da ad>                                  adaylar.tsv ve elenenler.tsv'de daha önce görüldü mü
  denetle <adaylar.tsv> [--elenenlere-yaz]                şema + eşikler → her satıra on_karar yazar
  viral --db <analiz.db> <adaylar.tsv>                    viral_db sütununu doldurur (db yoksa dogrulanamadi)
  sinama <adaylar.tsv> [--n 3] [--tohum N] [--kontrol OKUNAN.tsv]
                                                          rastgele satırları yeniden okutur / okunanla karşılaştırır

Eşikler koddan değil referans/esikler.tsv dosyasından okunur. Saat testi için BAZAAR_SIMDI=YYYY-AA-GGTSS:DD:SS.
Çıkış: 0 tamam · 1 veri hatası (ya da DAHA ONCE GORULDU, sinama tutmadı) · 2 kullanım · 3 kilit · 4 günlük tavan ya da bekleme.
"""
import csv
import datetime
import os
import random
import re
import sqlite3
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
ESIK_YOLU = os.path.join(BURADA, "..", "referans", "esikler.tsv")
ALANLAR = ["no", "urun", "trendyol_link", "alis_tl", "yorum", "puan", "satici_sayisi", "satici", "gorsel_bakildi",
           "mekanizma", "aile", "viral_db", "viral_video", "meta_reklam", "onerilen_satis_tl", "on_karar", "karar",
           "neden", "okuma_tarihi"]
KOTA_ALANLAR = ["tarih", "saat", "tur", "hedef", "kilit"]
VIRAL_DEGERLER = ["yok", "aile-var", "ayni-urun-viral", "dogrulanamadi"]
SIRA = {"SAT": 0, "İZLE": 1, "ELE": 2}
DOGRULANAMADI = "dogrulanamadi"


def simdi():
    s = os.environ.get("BAZAAR_SIMDI")
    return datetime.datetime.fromisoformat(s) if s else datetime.datetime.now()


def tsv_oku(yol):
    with open(yol, encoding="utf-8-sig", newline="") as f:
        satirlar = [r for r in csv.reader(f, delimiter="\t") if any(h.strip() for h in r)]
    return satirlar


def tsv_yaz(yol, baslik, satirlar):
    gecici = yol + ".tmp"
    with open(gecici, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(baslik)
        w.writerows(satirlar)
    os.replace(gecici, yol)


def esikleri_oku():
    if not os.path.isfile(ESIK_YOLU):
        raise ValueError("esikler.tsv yok: %s" % ESIK_YOLU)
    satirlar = tsv_oku(ESIK_YOLU)
    baslik = satirlar[0]
    out = {}
    for s in satirlar[1:]:
        r = dict(zip(baslik, s + [""] * (len(baslik) - len(s))))
        out[r["anahtar"]] = r
    return out


def sayi(metin, tam=False):
    """Boş → None. '199,90' → 199.9; '1.299,00' → 1299.0; '10.314' → 10314 (nokta binlik). Okunamayan → ValueError."""
    s = (metin or "").strip().replace(" ", "").replace("TL", "").replace("₺", "")
    if s == "" or s.lower() == DOGRULANAMADI:
        return None
    if tam:
        s = s.replace(".", "").replace(",", "")
    elif "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    return float(s)


def aralikta(deger, kural):
    """kural: 'a-b' | '>=x' | '<=x' | 'x' (tek değer)."""
    kural = (kural or "").strip()
    if not kural:
        return False
    if kural.startswith(">="):
        return deger >= float(kural[2:])
    if kural.startswith("<="):
        return deger <= float(kural[2:])
    m = re.fullmatch(r"(-?[\d.]+)-(-?[\d.]+)", kural)
    if m:
        return float(m.group(1)) <= deger <= float(m.group(2))
    return deger == float(kural)


def olcut_karari(esik, deger):
    """Sayısal ölçüt → SAT / İZLE / ELE. deger None ise çağıran DOGRULANAMADI sayar."""
    if aralikta(deger, esik["sat"]):
        return "SAT"
    if aralikta(deger, esik["izle"]):
        return "İZLE"
    return "ELE"


def satir_karari(r, esik):
    """Döner: (on_karar, [ölçüt notları])."""
    notlar, kararlar, adlar, dogr = [], [], [], []

    def ekle(ad, karar, ayrinti):
        kararlar.append(karar)
        adlar.append(ad)
        if ayrinti == "dogrulanamadi":
            dogr.append(ad)
        notlar.append("%s=%s %s" % (ad, ayrinti, karar))

    for ad, alan, tam in (("yorum", "yorum", True), ("puan", "puan", False), ("satici_sayisi", "satici_sayisi", True),
                          ("alis_tl", "alis_tl", False), ("meta_reklam", "meta_reklam", True)):
        v = sayi(r[alan], tam)
        if v is None:
            ekle(ad, "İZLE", "dogrulanamadi")
        else:
            ekle(ad, olcut_karari(esik[ad], v), "%g" % v)
    alis, satis = sayi(r["alis_tl"]), sayi(r["onerilen_satis_tl"])
    if alis and satis:
        kat = satis / alis
        k = olcut_karari(esik["kat"], kat)
        if k == "SAT" and satis < float(esik["satis_tl_min"]["sat"]):
            k = "İZLE"
        ekle("kat", k, "%.2f" % kat)
    else:
        ekle("kat", "İZLE", "dogrulanamadi")
    viral = (r["viral_db"] or "").strip() or DOGRULANAMADI
    e = esik["viral_db"]
    if viral in e["sat"].split("|"):
        ekle("viral_db", "SAT", viral)
    elif viral == e["ele"]:
        ekle("viral_db", "ELE", viral)
    else:
        ekle("viral_db", "İZLE", viral)
    en_kotu = max(kararlar, key=lambda k: SIRA[k])
    # SAT (koşullu): diğer ölçütlerin hepsi SAT; yalnız marj (kat) ve/veya viral doğrulanamadı → "SAT-KOSULLU" (neden sütunu hangisini yazar)
    if en_kotu == "İZLE" and dogr and set(dogr) <= {"kat", "viral_db"} and all(k == "SAT" or a in dogr for a, k in zip(adlar, kararlar)):
        return "SAT-KOSULLU", notlar
    return ("SAT-ADAYI" if en_kotu == "SAT" else en_kotu), notlar


def link_anahtari(link):
    m = re.search(r"-p-(\d+)", link or "")
    if m:
        return "p" + m.group(1)
    return re.sub(r"[?#].*$", "", (link or "").strip().lower()).rstrip("/")


def adaylari_oku(yol):
    if not os.path.isfile(yol):
        raise ValueError("dosya yok: %s" % yol)
    satirlar = tsv_oku(yol)
    if not satirlar:
        raise ValueError("dosya boş: %s" % yol)
    if [h.strip() for h in satirlar[0]] != ALANLAR:
        raise ValueError("başlık tam bu %d alan olmalı (sekme ayraçlı): %s" % (len(ALANLAR), ", ".join(ALANLAR)))
    out = []
    for i, s in enumerate(satirlar[1:], 2):
        if len(s) > len(ALANLAR):
            raise ValueError("satır %d: %d alan var (en çok %d)" % (i, len(s), len(ALANLAR)))
        out.append(dict(zip(ALANLAR, [h.strip() for h in s + [""] * (len(ALANLAR) - len(s))])))
    return out


# ------------------------------------------------------------------ kota
def kota_yolu(klasor):
    return os.path.join(klasor, "kota.tsv")


def kota_oku(klasor):
    y = kota_yolu(klasor)
    if not os.path.isfile(y):
        return []
    satirlar = tsv_oku(y)
    return [dict(zip(KOTA_ALANLAR, s + [""] * 5)) for s in satirlar[1:]]


def kota_ekle(klasor, tur, hedef, kilit=""):
    os.makedirs(klasor, exist_ok=True)
    y = kota_yolu(klasor)
    yeni = not os.path.isfile(y)
    n = simdi()
    with open(y, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        if yeni:
            w.writerow(KOTA_ALANLAR)
        w.writerow([n.date().isoformat(), n.time().strftime("%H:%M:%S"), tur, hedef, kilit])


def kota(klasor, args):
    if not args or args[0] not in ("durum", "kaydet", "kilit"):
        print("kullanım: kota durum | kaydet <arama|urun> <hedef> | kilit [sebep]")
        return 2
    esik = esikleri_oku()
    tavan = {"arama": int(esik["kota_arama_gunluk"]["sat"]), "urun": int(esik["kota_urun_gunluk"]["sat"])}
    bekleme = int(esik["kota_bekleme_sn"]["sat"])
    bugun = simdi().date().isoformat()
    bugunku = [r for r in kota_oku(klasor) if r["tarih"] == bugun]
    kilitli = [r for r in bugunku if r["kilit"]]
    say = {t: sum(1 for r in bugunku if r["tur"] == t) for t in tavan}
    if args[0] == "kilit":
        kota_ekle(klasor, "kilit", "", " ".join(args[1:]) or "engel")
        print("KILIT YAZILDI: bugün Trendyol'a dokunulmaz")
        return 0
    if args[0] == "durum":
        print("bugün %s: arama %d/%d · ürün sayfası %d/%d · kilit: %s" % (
            bugun, say["arama"], tavan["arama"], say["urun"], tavan["urun"], kilitli[-1]["kilit"] if kilitli else "yok"))
        if kilitli:
            return 3
        return 4 if any(say[t] >= tavan[t] for t in tavan) else 0
    if len(args) < 3 or args[1] not in tavan:
        print("kullanım: kota kaydet <arama|urun> <hedef>")
        return 2
    tur, hedef = args[1], " ".join(args[2:])
    if kilitli:
        print("KİLİTLİ: %s" % kilitli[-1]["kilit"])
        return 3
    if say[tur] >= tavan[tur]:
        print("GÜNLÜK TAVAN DOLDU: %s %d/%d" % (tur, say[tur], tavan[tur]))
        return 4
    istekler = [r for r in bugunku if r["tur"] in tavan]
    if istekler:
        son = datetime.datetime.fromisoformat(istekler[-1]["tarih"] + "T" + istekler[-1]["saat"])
        gecen = (simdi() - son).total_seconds()
        if gecen < bekleme:
            print("BEKLE: son istekten %d sn geçti, en az %d sn gerekir" % (gecen, bekleme))
            return 4
    kota_ekle(klasor, tur, hedef)
    print("KAYDEDİLDİ: %s %d/%d" % (tur, say[tur] + 1, tavan[tur]))
    return 0


# ------------------------------------------------------------------ tekrar
def tekrar(klasor, args):
    if not args:
        print("kullanım: tekrar <link ya da ad>")
        return 2
    sorgu = " ".join(args)
    link_mi = sorgu.lower().startswith("http")
    anahtar = link_anahtari(sorgu) if link_mi else sorgu.lower()
    bulundu = False
    for ad in ("adaylar.tsv", "elenenler.tsv"):
        y = os.path.join(klasor, ad)
        if not os.path.isfile(y):
            continue
        for i, s in enumerate(tsv_oku(y), 1):
            if any((link_anahtari(h) == anahtar) if link_mi else (anahtar in h.lower()) for h in s if (not link_mi or h.startswith("http"))):
                print("DAHA ONCE GORULDU: %s (%s:%d)" % (sorgu, ad, i))
                bulundu = True
    if not bulundu:
        print("YENI: %s" % sorgu)
    return 1 if bulundu else 0


# ------------------------------------------------------------------ denetle
def denetle(yol, elenenlere_yaz=False):
    try:
        esik = esikleri_oku()
        satirlar = adaylari_oku(yol)
    except ValueError as e:
        print("HATA: %s" % e)
        return 1
    hata = []
    gorulen = {}
    for i, r in enumerate(satirlar, 2):
        if not r["urun"]:
            hata.append("satır %d: urun boş" % i)
        if not r["trendyol_link"].lower().startswith("http"):
            hata.append("satır %d: trendyol_link http ile başlamıyor" % i)
        k = link_anahtari(r["trendyol_link"])
        if k in gorulen:
            hata.append("satır %d: DAHA ONCE GORULDU (satır %d ile aynı link)" % (i, gorulen[k]))
        gorulen[k] = i
        for alan, tam in (("alis_tl", False), ("yorum", True), ("puan", False), ("satici_sayisi", True),
                          ("meta_reklam", True), ("onerilen_satis_tl", False)):
            try:
                sayi(r[alan], tam)
            except ValueError:
                hata.append("satır %d: %s sayı değil: %r" % (i, alan, r[alan]))
        if r["viral_db"] and r["viral_db"] not in VIRAL_DEGERLER:
            hata.append("satır %d: viral_db %r; izinli: %s" % (i, r["viral_db"], ", ".join(VIRAL_DEGERLER)))
        if r["karar"] and r["karar"] not in ("SAT", "SAT (koşullu)", "İZLE", "ELE"):
            hata.append("satır %d: karar %r; izinli: SAT / SAT (koşullu) / İZLE / ELE" % (i, r["karar"]))
    if hata:
        for h in hata:
            print("HATA: " + h)
        return 1
    elenen = []
    for r in satirlar:
        r["on_karar"], notlar = satir_karari(r, esik)
        print("%-3s %-40s %-10s %s" % (r["no"], r["urun"][:40], r["on_karar"], " · ".join(n for n in notlar if not n.endswith("SAT"))))
        if r["on_karar"] == "ELE":
            elenen.append(r)
    tsv_yaz(yol, ALANLAR, [[r[a] for a in ALANLAR] for r in satirlar])
    if elenenlere_yaz and elenen:
        klasor = os.path.dirname(os.path.abspath(yol))
        ey = os.path.join(klasor, "elenenler.tsv")
        eski = tsv_oku(ey)[1:] if os.path.isfile(ey) else []
        var = {link_anahtari(s[0]) for s in eski if s}
        bugun = simdi().date().isoformat()
        for r in elenen:
            if link_anahtari(r["trendyol_link"]) not in var:
                eski.append([r["trendyol_link"], r["neden"] or "on_karar ELE", bugun])
        tsv_yaz(ey, ["link", "sebep", "tarih"], eski)
    toplam = len(satirlar)
    say = {k: sum(1 for r in satirlar if r["on_karar"] == k) for k in ("SAT-ADAYI", "SAT-KOSULLU", "İZLE", "ELE")}
    print("denetle: %d aday · SAT-ADAYI %d · SAT-KOSULLU %d · İZLE %d · ELE %d" % (toplam, say["SAT-ADAYI"], say["SAT-KOSULLU"], say["İZLE"], say["ELE"]))
    deneme = [k for k, e in esik.items() if e["durum"] in ("varsayim", "deneme")]
    if deneme:
        kanitli = len([f for f in os.listdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(yol))), "kanit"))]) \
            if os.path.isdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(yol))), "kanit")) else 0
        print("%d/20 kanıt: eşikler DENEME (%d ölçüt varsayım ya da denemedir)" % (kanitli, len(deneme)))
    return 0


# ------------------------------------------------------------------ viral
def fold(s):
    tr = str.maketrans("ıİşŞğĞüÜöÖçÇ", "iissgguuoocc")
    return (s or "").translate(tr).lower()


def jeton(s, en_az=4):
    return {t for t in re.split(r"[^a-z0-9]+", fold(s)) if len(t) >= en_az}


def viral(db, yol):
    try:
        satirlar = adaylari_oku(yol)
    except ValueError as e:
        print("HATA: %s" % e)
        return 1
    viraller = None
    if os.path.isfile(db):
        try:
            c = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
            viraller = c.execute("SELECT ad, aile, hukum FROM v_viral_urun WHERE hukum IN ('VIRAL-URUN','VIRAL-VIDEO')").fetchall()
            c.close()
        except sqlite3.Error as e:
            print("UYARI: veritabanı okunamadı (%s): hepsi dogrulanamadi" % e)
    else:
        print("UYARI: veritabanı yok (%s): hepsi dogrulanamadi" % db)
    for r in satirlar:
        if viraller is None:
            r["viral_db"] = DOGRULANAMADI
            continue
        urun_j = jeton(r["urun"])
        aile_j = jeton(r["aile"].replace("-", " "))
        sonuc = "yok"
        for ad, aile, hukum in viraller:
            ortak_ad = urun_j & jeton(ad)
            if hukum == "VIRAL-URUN" and len(ortak_ad) >= 4:
                sonuc = "ayni-urun-viral"
                break
            hedef = jeton(ad) | jeton((aile or "").replace("-", " "))
            if aile_j and aile_j & hedef:
                sonuc = "aile-var"
        r["viral_db"] = sonuc
        print("%-3s %-40s %s" % (r["no"], r["urun"][:40], sonuc))
    tsv_yaz(yol, ALANLAR, [[r[a] for a in ALANLAR] for r in satirlar])
    return 0


# ------------------------------------------------------------------ sinama
def sinama(yol, args):
    n, tohum, kontrol = 3, None, None
    if "--n" in args:
        n = int(args[args.index("--n") + 1])
    if "--tohum" in args:
        tohum = int(args[args.index("--tohum") + 1])
    if "--kontrol" in args:
        kontrol = args[args.index("--kontrol") + 1]
    try:
        satirlar = adaylari_oku(yol)
    except ValueError as e:
        print("HATA: %s" % e)
        return 1
    if kontrol:
        okunan = {link_anahtari(r["trendyol_link"]): r for r in adaylari_oku(kontrol)}
        tutan = 0
        secilen = [r for r in satirlar if link_anahtari(r["trendyol_link"]) in okunan]
        for r in secilen:
            o = okunan[link_anahtari(r["trendyol_link"])]
            a1, a2 = sayi(r["alis_tl"]), sayi(o["alis_tl"])
            y1, y2 = sayi(r["yorum"], True), sayi(o["yorum"], True)
            p1, p2 = sayi(r["puan"]), sayi(o["puan"])
            ok = None not in (a1, a2, y1, y2, p1, p2) and abs(a1 - a2) <= 0.05 * a1 and abs(y1 - y2) <= 0.10 * max(y1, 1) and abs(p1 - p2) <= 0.1
            tutan += 1 if ok else 0
            print("%s %s" % ("TUTTU " if ok else "TUTMADI", r["urun"]))
        print("sinama: %d/%d tuttu" % (tutan, len(secilen)))
        return 0 if secilen and tutan == len(secilen) and len(secilen) >= min(3, len(satirlar)) else 1
    rnd = random.Random(tohum)
    sec = rnd.sample(satirlar, min(n, len(satirlar)))
    print("Bu satırlar Trendyol ürün sayfasından yeniden okunur (alis_tl, yorum, puan); okunanı aynı başlıkla bir TSV'ye yaz,")
    print("sonra: bazaar_kontrol.py sinama <adaylar.tsv> --kontrol <okunan.tsv>")
    for r in sec:
        print("- %s | %s | alis %s · yorum %s · puan %s" % (r["urun"], r["trendyol_link"], r["alis_tl"], r["yorum"], r["puan"]))
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    args = argv[1:]
    klasor = os.path.join("is", "firsat", "trendyol")
    if "--klasor" in args:
        i = args.index("--klasor")
        klasor = args[i + 1]
        del args[i:i + 2]
    komut, rest = args[0], args[1:]
    try:
        if komut == "kota":
            return kota(klasor, rest)
        if komut == "tekrar":
            return tekrar(klasor, rest)
        if komut == "denetle" and rest:
            return denetle(rest[0], "--elenenlere-yaz" in rest)
        if komut == "viral" and "--db" in rest:
            i = rest.index("--db")
            db = rest[i + 1]
            del rest[i:i + 2]
            if rest:
                return viral(db, rest[0])
        if komut == "sinama" and rest:
            return sinama(rest[0], rest[1:])
    except (ValueError, OSError) as e:
        print("HATA: %s" % e)
        return 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
