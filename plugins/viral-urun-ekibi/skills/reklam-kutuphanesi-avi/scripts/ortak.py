"""reklam-kutuphanesi-avi ortak yardımcıları (yalnız stdlib, Python 3.8+).

Tek kaynak: TSV şemaları, eşikler (DENEME), ülke/aile listeleri, tarih ve link çözümleme.
Okunamayan alan her zaman GORUNMUYOR yazılır; 0 yazılmaz.
"""
import csv
import datetime as dt
import os
import re
import sys
import urllib.parse

GORUNMUYOR = "görünmüyor"
ULKELER = ["US", "TR", "GB", "DE", "FR", "ES", "IT", "NL"]  # Meta ülke kodları (UK = GB); IT/NL ürün terimi yok → İngilizce yedek
PAZAR_AD = {"US": "ABD", "TR": "Türkiye", "GB": "Birleşik Krallık", "DE": "Almanya", "FR": "Fransa", "ES": "İspanya",
            "IT": "İtalya", "NL": "Hollanda"}
AILELER = ["U", "S", "K", "KONTROL", "ALAN"]            # Ü=ürün tipi, S=dropship sinyali, K=kimlik/kanca
SORGU_AILELERI = ["U", "S", "K"]
SIRALAMALAR = {"gosterim": "total_impressions", "yeni": "relevancy_monthly_grouped"}
TIPLER = ["SHOPIFY", "ALTALAN-LANDING", "PAZARYERI", "DİĞER", "LİNKSİZ"]
ETIKETLER_REKLAM = ["OLCEKLENIYOR", "ESKI-KAZANAN", "TEST", "BILINMIYOR"]
ETIKETLER_BIRIM = ["OLCEKLENIYOR", "ESKI-KAZANAN", "TEST"]

GUNLUK_KOTA = 30          # günde en çok sorgu (kontrol + alan sorguları dahil)
MIN_ARALIK_SN = 15        # iki sorgu kaydı arası en az

# ---- EŞİKLER: hepsi DENEME (kaynak: araç satıcısı sezgisi + ilk TR turu); 4 hafta sonra kendi verimizle kalibre ----
ESIK = {
    "kreatif_aktif_gun": 30,     # reklam ≥30 gündür yayında
    "kreatif_kopya": 3,          # "N reklam bu kreatifi kullanıyor" ≥3
    "eski_gun": 180,             # bundan eski reklam/mağaza "eski kazanan"
    "birim_aktif_reklam": 10,    # mağaza başına aktif reklam ≥10
    "magaza_yas_gun": 180,       # mağaza (en eski ürün) ≤6 ay
    "magaza_urun": 30,           # ≤30 ürün
    "pencere_gun": 7,            # birim sayımında aynı haftanın okumaları birlikte sayılır
}
ESIK_NOTU = "eşikler DENEME (ölçülmedi, 4 hafta sonra kalibre)"

REKLAM_SUTUN = ["kutuphane_kodu", "okuma_tarihi", "ulke", "nis", "sorgu", "aile", "siralama", "sayfa_adi",
                "ilk_yayin", "aktif_gun", "kopya", "govde_ilk200", "cta", "hedef_alan", "hedef_yol", "tip",
                "medya", "izlendi", "not_no", "etiket"]
BIRIM_SUTUN = ["ulke", "birim", "sayfa_adi", "tip", "nis", "reklam_sayisi", "kopya_toplami", "ilk_baslangic",
               "son_baslangic", "max_aktif_gun", "kazanan_kreatif", "alan_sorgu", "son_okuma", "urun_yollari", "etiket"]
ARAMA_SUTUN = ["tarih", "saat", "ulke", "nis", "aile", "sorgu", "siralama", "kart", "durum", "ham_dosya"]
MAGAZA_SUTUN = ["alan", "okuma_tarihi", "durum", "urun_sayisi", "ilk_urun", "son_urun", "medyan_fiyat",
                "ana_urun", "ana_urun_eklenme", "ana_fiyat", "ana_cizili", "ana_handle"]
GECMIS_SUTUN = ["tarih", "ulke", "birim", "reklam_sayisi", "kopya_toplami"]
ALAN_SUTUN = ["tarih", "ulke", "alan", "sonuc"]
TEKLIF_SUTUN = ["alan", "okuma_tarihi", "fiyat", "cizili", "paket", "kargo_esigi", "garanti", "yorum_app",
                "yorum_sayisi", "sss", "odeme", "ilk_ekran"]

DOSYA = {
    "reklam": ("reklamlar.tsv", REKLAM_SUTUN),
    "birim": ("sayfalar.tsv", BIRIM_SUTUN),
    "arama": ("aramalar.tsv", ARAMA_SUTUN),
    "magaza": ("magazalar.tsv", MAGAZA_SUTUN),
    "gecmis": ("sayfa_gecmis.tsv", GECMIS_SUTUN),
    "alan": ("alan_olcek.tsv", ALAN_SUTUN),
    "teklif": ("teklif.tsv", TEKLIF_SUTUN),
}


class VeriHatasi(Exception):
    """Yanlış/eksik girdi — betik çıkış 1 verir."""


def hata_cik(mesaj, kod=1):
    print("HATA: " + mesaj, file=sys.stderr)
    sys.exit(kod)


# ------------------------------------------------------------------ zaman
def bugun():
    s = os.environ.get("REKLAMAVI_SIMDI")  # testler için: "2026-11-07T10:00:00"
    return (dt.datetime.fromisoformat(s) if s else dt.datetime.now())


def iso_mu(s):
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", s or ""))


def gun_farki(son, ilk):
    return (dt.date.fromisoformat(son) - dt.date.fromisoformat(ilk)).days


AYLAR = {}
for _i, _adlar in enumerate([
    "oca ocak jan january janv janvier januar ene enero",
    "şub şubat sub subat feb february févr fevr février fevrier februar febrero",
    "mar mart march mars märz marz marzo",
    "nis nisan apr april avr avril abr abril",
    "may mayıs mayis mai mayo",
    "haz haziran jun june juin juni junio",
    "tem temmuz jul july juil juillet juli julio",
    "ağu ağustos agu agustos aug august août aout ago agosto",
    "eyl eylül eylul sep sept september septembre sep septiembre",
    "eki ekim oct october okt oktober octobre oct octubre",
    "kas kasım kasim nov november novembre noviembre",
    "ara aralık aralik dec december dez dezember déc dec décembre decembre dic diciembre",
], start=1):
    for _a in _adlar.split():
        AYLAR[_a] = _i


def tarih_coz(metin):
    """Meta kart tarih metnini ISO tarihe çevirir. Çözemezse None.
    Örn: '21 Ağu 2026 tarihinde yayınlanmaya başladı' · 'Started running on Aug 21, 2026' · '21.08.2026'."""
    if not metin:
        return None
    t = metin.strip().lower().replace(",", " ")
    m = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", t)
    if m:
        g, a, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return _gecerli(y, a, g)
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", t)
    if m:
        return _gecerli(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    kel = re.findall(r"[^\W\d_]+\.?|\d+", t)
    kel = [k.rstrip(".") for k in kel]
    for i, k in enumerate(kel):
        if k in AYLAR:
            ay = AYLAR[k]
            once = kel[i - 1] if i > 0 else ""
            sonra = kel[i + 1] if i + 1 < len(kel) else ""
            sonra2 = kel[i + 2] if i + 2 < len(kel) else ""
            if once.isdigit() and sonra.isdigit() and len(sonra) == 4:      # 21 ağu 2026
                return _gecerli(int(sonra), ay, int(once))
            if sonra.isdigit() and sonra2.isdigit() and len(sonra2) == 4:   # aug 21 2026
                return _gecerli(int(sonra2), ay, int(sonra))
            if i >= 2 and once == "de" and kel[i - 2].isdigit() and sonra == "de" and sonra2.isdigit():  # 21 de ago de 2026
                return _gecerli(int(sonra2), ay, int(kel[i - 2]))
    return None


def _gecerli(y, a, g):
    try:
        return dt.date(y, a, g).isoformat()
    except ValueError:
        return None


def kopya_coz(metin):
    """'3 reklam bu kreatifi ve metni kullanıyor' / '3 ads use this creative and text' → 3. Yoksa None."""
    if not metin:
        return None
    m = re.search(r"(\d+)\s*(reklam|ads?|anzeigen|publicités|publicites|anuncios)\b", metin, re.I)
    return int(m.group(1)) if m else None


# ------------------------------------------------------------------ link / tip
PAZARYERLERI = ("trendyol.", "hepsiburada.", "n11.", "amazon.", "etsy.", "ebay.", "temu.", "aliexpress.",
                "shopier.", "ciceksepeti.", "pttavm.", "walmart.", "otto.de", "cdiscount.", "zalando.", "shein.")
SOSYAL = ("instagram.", "facebook.", "fb.me", "m.me", "wa.me", "whatsapp.", "tiktok.", "youtube.", "t.me", "linktr.ee")
ALTALAN_DISI = {"www", "shop", "store", "m", "magaza", "en", "tr", "de", "fr", "es", "uk", "us", "eu", "app"}


def link_coz(link):
    """l.facebook.com/l.php?u=... sarmalını açar; (alan, yol) döner. Link yoksa ('', '')."""
    if not link or link == GORUNMUYOR:
        return "", ""
    u = link.strip()
    for _ in range(3):
        p = urllib.parse.urlparse(u if "://" in u else "https://" + u)
        if p.netloc.endswith("facebook.com") and p.path.startswith("/l.php"):
            q = urllib.parse.parse_qs(p.query).get("u")
            if not q:
                return "", ""
            u = q[0]
            continue
        break
    p = urllib.parse.urlparse(u if "://" in u else "https://" + u)
    alan = p.netloc.lower().split("@")[-1].split(":")[0]
    if alan.startswith("www."):
        alan = alan[4:]
    return alan, p.path or "/"


def tip_bul(alan, yol):
    if not alan:
        return "LİNKSİZ"
    if alan.endswith(".myshopify.com") or "/products/" in yol:
        return "SHOPIFY"
    if any(alan.startswith(p) or ("." + p) in alan for p in PAZARYERLERI):
        return "PAZARYERI"
    if any(alan.startswith(s) or ("." + s) in alan for s in SOSYAL):
        return "DİĞER"
    parca = alan.split(".")
    ikili_tld = len(parca) >= 3 and parca[-2] in ("com", "co", "net", "org") and len(parca[-1]) == 2
    kok_uzunluk = 3 if ikili_tld else 2
    if len(parca) > kok_uzunluk and parca[0] not in ALTALAN_DISI and yol.count("/") <= 2:
        return "ALTALAN-LANDING"
    return "DİĞER"


def urun_yolu(yol):
    m = re.search(r"/products/([^/?#]+)", yol or "")
    return m.group(1) if m else ""


# ------------------------------------------------------------------ TSV
def tsv_oku(yol, sutunlar, zorunlu=False):
    if not os.path.exists(yol):
        if zorunlu:
            raise VeriHatasi("dosya yok: %s" % yol)
        return []
    with open(yol, encoding="utf-8", newline="") as f:
        satirlar = [s for s in f.read().split("\n") if s.strip() and not s.startswith("#")]
    if not satirlar:
        return []
    baslik = satirlar[0].split("\t")
    if baslik != sutunlar:
        raise VeriHatasi("%s başlığı şemaya uymuyor.\n  beklenen: %s\n  bulunan : %s"
                         % (yol, "\t".join(sutunlar), "\t".join(baslik)))
    sonuc = []
    for no, s in enumerate(satirlar[1:], start=2):
        h = s.split("\t")
        if len(h) != len(sutunlar):
            raise VeriHatasi("%s satır %d: %d alan var, %d bekleniyor" % (yol, no, len(h), len(sutunlar)))
        sonuc.append(dict(zip(sutunlar, h)))
    return sonuc


def tsv_yaz(yol, sutunlar, satirlar):
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    gecici = yol + ".tmp"
    with open(gecici, "w", encoding="utf-8", newline="") as f:
        f.write("\t".join(sutunlar) + "\n")
        for r in satirlar:
            f.write("\t".join(temiz(r.get(c, "")) for c in sutunlar) + "\n")
    os.replace(gecici, yol)


def temiz(v):
    return str(v).replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()


def dosya_yolu(kok, ad):
    return os.path.join(kok, DOSYA[ad][0])


def oku(kok, ad):
    return tsv_oku(dosya_yolu(kok, ad), DOSYA[ad][1])


def yaz(kok, ad, satirlar):
    tsv_yaz(dosya_yolu(kok, ad), DOSYA[ad][1], satirlar)


def sayi_mi(v):
    return bool(re.fullmatch(r"\d+", v or ""))


def norm(s):
    """Dil-bağımsız küçük harf: Türkçe İ/I/ı farkı eşleşmeyi bozmasın."""
    return (s or "").replace("İ", "i").replace("I", "i").lower().replace("ı", "i").replace("̇", "")
