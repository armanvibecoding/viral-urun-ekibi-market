#!/usr/bin/env python3
"""trendyol_kontrol.py: Hunter · Trendyol kaynağı yardımcısı (yalnız Python 3 standart kütüphanesi).

Alt komutlar (--klasor varsayılan: is/firsat/trendyol):
  kota durum|kaydet <arama|urun> <hedef>|iade <arama|urun> <hedef>|sonuc <ok|bos|429|403|captcha> [hedef]|kilit [sebep]
                                                          engel sinyali (429/403/captcha/art arda 3 boş sayfa) → kilit; günlük sayı yalnız üst güvenlik sınırı;
                                                          tekrar eden hedef ve iade edilen (başarısız/hatalı) istek kotaya sayılmaz (kota.tsv)
  tekrar <link ya da ad>                                  adaylar.tsv ve elenenler.tsv'de daha önce görüldü mü
  denetle <adaylar.tsv> [--elenenlere-yaz] [--marj-sonuc marj-sonuc.tsv]
                                                          şema + eşikler → her satıra on_karar yazar (SAT-ADAYI ya da ELE; İZLE yok).
                                                          ELE yalnız KANITLI engel: veto · kanıtlı negatif katkı (marj) · kanıtlı doygunluk
                                                          · eşiğin altında talep. Okunamayan/ölçülemeyen ölçüt engel DEĞİL: neden sütununa
                                                          "Kontrol et: ..." notu olur (SAT kartında "ilk testte kontrol et")
  ozet <adaylar.tsv> [--hedef N] [--sebep METIN]          kullanıcı özeti: YALNIZ SAT (kanıt dosyası olanlar); N varsayılan 5;
                                                          N'e ulaşılamazsa tek satır "k SAT buldum, sebep: ..."
  viral [--db <analiz.db>] <adaylar.tsv>                  viral_db sütununu doldurur (db yoksa eklentinin ortak/bilgi/viral-urunler.tsv tablosu)
  sinama <adaylar.tsv> [--n 3] [--tohum N] [--kontrol OKUNAN.tsv]
                                                          rastgele satırları yeniden okutur / okunanla karşılaştırır

Eşikler koddan değil referans/esikler.tsv dosyasından okunur; danışanın .ekip/isletme-profili.tsv dosyası (kat_min, satis_tl_min) bunun üstüne yazar
(`--profil DOSYA` ile başka dosya; profil yoksa eklenti varsayılanı ve çıktıda "PROFIL: yok" satırı). Saat testi için TRENDYOL_SIMDI=YYYY-AA-GGTSS:DD:SS.
Çıkış: 0 tamam · 1 veri hatası (ya da DAHA ONCE GORULDU, sinama tutmadı) · 2 kullanım · 3 kilit · 4 günlük tavan ya da bekleme.
"""
import csv
import datetime
import glob
import os
import random
import re
import sqlite3
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BURADA, "..", "..", "..", "..", "ortak"))
import profil as profil_mod  # noqa: E402  (danışanın işletme profili: .ekip/isletme-profili.tsv)

PROFIL_YOLU = None  # --profil ile verilirse; yoksa profil.yol_bul()
PROFIL_NOTU = []    # esik üstüne yazan profil anahtarları (denetle çıktısında "profil kullanıldı" satırı)
ESIK_YOLU = os.path.join(BURADA, "..", "referans", "esikler.tsv")
# 19 alan = eski şema (kabul edilir); 22 alan = + rakip_tl (Trendyol'daki satış fiyatı, rakip/hedef) · alis_kaynak (alışın tedarikçi
# kaynağı: AliExpress/1688 linki) · veto (lisans-marka / tehlikeli / riskli-kargo ...). alis_tl ASLA Trendyol perakende fiyatı değildir.
TEMEL_ALANLAR = ["no", "urun", "trendyol_link", "alis_tl", "yorum", "puan", "satici_sayisi", "satici", "gorsel_bakildi",
                 "mekanizma", "aile", "viral_db", "viral_video", "meta_reklam", "onerilen_satis_tl", "on_karar", "karar",
                 "neden", "okuma_tarihi"]
EK_ALANLAR = ["rakip_tl", "alis_kaynak", "veto"]
# Tedarikçi ÜRÜN sayfası (arama sonucu değil): AliExpress /item/<no> · 1688 /offer/<no> ya da detail.1688.com
URUN_SAYFASI = re.compile(r"aliexpress\.[a-z.]+/item/\d+|1688\.com/offer/\d+|detail\.1688\.com/|alibaba\.com/product-detail/", re.I)
ALANLAR = TEMEL_ALANLAR + EK_ALANLAR
KOTA_ALANLAR = ["tarih", "saat", "tur", "hedef", "kilit", "sonuc"]
VIRAL_DEGERLER = ["yok", "aile-var", "ayni-urun-viral", "dogrulanamadi"]
SIRA = {"SAT": 0, "İZLE": 1, "ELE": 2}
OLUMSUZ_VETO = ("", "yok", "-", "hayir", "hayır", "temiz")
# Skeptic hükmü `SAT-KOŞULLU: <eksik tek kanıt>` (denetim #21): Trendyol kaynağının "SAT (koşullu)" kararıyla aynı şey, iki yazım da kabul
KOSULLU_RE = re.compile(r"^\s*SAT\s*[-–]?\s*\(?\s*KO[SŞ]ULLU\s*\)?\s*(?:[:：]\s*(?P<eksik>.*?))?\s*$", re.I)


def kosullu_eslesme(karar):
    return KOSULLU_RE.match(karar or "")


def sat_ailesi(karar):
    """SAT, 'SAT (koşullu)', 'SAT-KOŞULLU: x' hepsi SAT'tır; koşullu ayrı sınıf değil, eksik kanıt SAT kartında not olur."""
    k = (karar or "").strip()
    return k == "SAT" or k == "SAT (koşullu)" or bool(kosullu_eslesme(k))
DOGRULANAMADI = "dogrulanamadi"


def simdi():
    s = os.environ.get("TRENDYOL_SIMDI")
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
    profil_uygula(out)
    return out


def profil_uygula(out):
    """Danışanın profili eklenti varsayılanının ÜSTÜNE yazar: kat_min → kat.sat · satis_tl_min → satis_tl_min.sat.
    Profil yoksa eşik dosyası aynen kalır. Bozuk profil ValueError (ProfilHatasi) verir, sessiz geçilmez."""
    del PROFIL_NOTU[:]
    p = profil_mod.oku(PROFIL_YOLU)
    if "kat_min" in p:
        out["kat"] = dict(out["kat"], sat=">=%g" % p["kat_min"], izle="", durum="profil")
        PROFIL_NOTU.append("kat_min=%g" % p["kat_min"])
    if "satis_tl_min" in p:
        out["satis_tl_min"] = dict(out["satis_tl_min"], sat="%g" % p["satis_tl_min"], durum="profil")
        PROFIL_NOTU.append("satis_tl_min=%g" % p["satis_tl_min"])


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


def satir_karari(r, esik, marj=None, marj_verildi=False):
    """Döner: (on_karar, [ölçüt notları], [kontrol notları], [ELE sebepleri]).
    YALNIZ SAT (kurucu kararı 2026-11-25): on_karar SAT-ADAYI ya da ELE. ELE yalnız KANITLI engeldir:
    veto · kanıtlı negatif katkı (marj) · kanıtlı doygunluk (satıcı, Meta, aynı ürün viral) · eşiğin altında talep (yorum/puan) · kat < eşik.
    dogrulanamadi / boş / ölçülemeyen ölçüt satırı DÜŞÜRMEZ: kontrol notu olur."""
    notlar, kontrol, ele = [], [], []
    for ad, alan, tam, etiket in (("yorum", "yorum", True, "yorum sayısı okunamadı"), ("puan", "puan", False, "puan okunamadı"),
                                  ("satici_sayisi", "satici_sayisi", True, "satıcı sayısı okunamadı"),
                                  ("meta_reklam", "meta_reklam", True, "Meta reklam sayısı okunamadı")):
        v = sayi(r[alan], tam)
        if v is None:
            notlar.append("%s=dogrulanamadi not" % ad)
            kontrol.append(etiket)
        elif olcut_karari(esik[ad], v) == "SAT":
            notlar.append("%s=%g SAT" % (ad, v))
        else:
            notlar.append("%s=%g ELE" % (ad, v))
            ele.append("%s %g (SAT bandı %s dışı)" % (ad, v, esik[ad]["sat"]))
    # alis_tl = TEDARİKÇİ alışı (AliExpress/1688 aynı ürün); Trendyol perakende fiyatı değil. Eşik bandı yok: engel kat'tır.
    alis, satis, rakip = sayi(r["alis_tl"]), sayi(r["onerilen_satis_tl"]), sayi(r.get("rakip_tl", ""))
    kaynak = (r.get("alis_kaynak") or "").strip()
    if alis is not None and kaynak and not URUN_SAYFASI.search(kaynak):
        # Canlı rol sınavı 2026-11-25: arama sonucu/benzer ürün fiyatı alis_tl'ye yazılmış, kat 0,47 → ELE olmuştu.
        # Aynı ürünün tedarikçi SAYFASI yoksa alış kanıt değildir: kat ölçülmez, ELE verilmez.
        notlar.append("kat=dogrulanamadi not")
        kontrol.append("alış aynı ürünün tedarikçi sayfasından değil (arama/benzer ürün): kat ölçülemedi")
        alis = None
    elif alis is None:
        notlar.append("kat=dogrulanamadi not")
        kontrol.append("tedarikçi bulunamadı (alış ve kat ölçülemedi)")
    if alis is None:
        pass
    elif not satis:
        notlar.append("kat=dogrulanamadi not")
        kontrol.append("hedef satış fiyatı yazılmamış (kat ölçülemedi)")
    else:
        kat = satis / alis if alis else 0
        k = olcut_karari(esik["kat"], kat)
        if k == "SAT" and satis < float(esik["satis_tl_min"]["sat"]):
            notlar.append("kat=%.2f ELE" % kat)
            ele.append("hedef satış %g TL (SAT için en az %s TL)" % (satis, esik["satis_tl_min"]["sat"]))
        elif k != "SAT":
            notlar.append("kat=%.2f ELE" % kat)
            ele.append("kat %.2f (SAT bandı %s dışı)" % (kat, esik["kat"]["sat"]))
        else:
            notlar.append("kat=%.2f SAT" % kat)
    fiyat = satis or rakip
    if alis is None and fiyat and fiyat < float(esik["satis_tl_min"]["sat"]):
        # canlı rol sınavı 2026-11-25: kat ölçülemediğinde satış alt sınırı da denetlenmiyordu (324 TL ürün notsuz SAT oldu)
        kontrol.append("satış fiyatı %g TL, SAT için en az %s TL: set/paketle fiyatı yükselt" % (fiyat, esik["satis_tl_min"]["sat"]))
    if rakip and satis and rakip < satis:
        kontrol.append("Trendyol'da aynı ürün %g TL, hedef satışın (%g TL) altında" % (rakip, satis))
    viral = (r["viral_db"] or "").strip() or DOGRULANAMADI
    e = esik["viral_db"]
    if viral == e["ele"]:
        notlar.append("viral_db=%s ELE" % viral)
        ele.append("aynı ürün zaten viral")
    elif viral in e["sat"].split("|"):
        notlar.append("viral_db=%s SAT" % viral)
    else:
        notlar.append("viral_db=%s not" % viral)
        kontrol.append("viral doğrulanamadı (viral veritabanı yok; vekil: Meta reklam + satıcı sayısı)")
    # Instagram/TikTok girişsiz bakılamadıysa engel DEĞİL: karar analiz.db + Meta ile verilir.
    if (r.get("viral_video") or "").strip().lower().startswith("dogrulanamadi"):
        notlar.append("ig_tt=dogrulanamadi-giris RİSK: Instagram/TikTok girişsiz bakılamadı, karar analiz.db + Meta ile")
        kontrol.append("Instagram/TikTok bakılamadı")
    veto = (r.get("veto") or "").strip()
    if veto.lower() not in OLUMSUZ_VETO:
        notlar.append("veto=%s ELE" % veto)
        ele.append("veto: %s" % veto)
    # marj (tr_marj.py sonucu): kanıtlı negatif katkı → ELE; marka ROAS yok → not; ROAS hesabı tr_marj.py'de kalır
    if marj_verildi:
        if not marj:
            kontrol.append("marj hesaplanmadı (tr_marj.py)")
        else:
            try:
                katki = float(marj.get("katki", ""))
            except ValueError:
                katki = None
            km = (marj.get("karar_marj") or "").strip()
            if (katki is not None and katki <= 0) or marj.get("basabas_roas", "").strip() == "zarar":
                notlar.append("marj=zarar ELE")
                ele.append("marj: net katkı ≤ 0")
            elif km == "ELE":
                notlar.append("marj_roas=%s ELE" % km)
                ele.append("marj: marka ROAS başabaşın altında")
            elif km == "İZLE":
                notlar.append("marj_roas=sınırda not")
                kontrol.append("marka ROAS başabaşa yakın (sınırda)")
            elif km in ("", DOGRULANAMADI):
                notlar.append("marj_roas=dogrulanamadi not")
                kontrol.append("marka ROAS yok (başabaş ROAS doğrulanamadı)")
            else:
                notlar.append("marj_roas=%s SAT" % km)
    return ("ELE" if ele else "SAT-ADAYI"), notlar, kontrol, ele


NOT_RE = re.compile(r"\s*(?:Kontrol et|ELE sebebi):.*$")


def neden_yaz(neden, on_karar, kontrol, ele):
    """Betiğin yazdığı bölüm her koşuda yeniden üretilir; ajanın yazdığı gerekçe korunur."""
    temel = NOT_RE.sub("", neden or "").strip()
    ek = ""
    if on_karar == "ELE" and ele:
        ek = "ELE sebebi: " + "; ".join(ele)
    elif kontrol:
        ek = "Kontrol et: " + "; ".join(kontrol)
    return ((temel + " ") if temel and ek else temel) + ek


def marj_oku(klasor, yol=None):
    """marj-sonuc.tsv → ({urun.lower(): satır}, verildi). Dosya yoksa ({}, False)."""
    yol = yol or os.path.join(klasor, "marj-sonuc.tsv")
    if not os.path.isfile(yol):
        return {}, False
    satirlar = tsv_oku(yol)
    if not satirlar:
        return {}, True
    return {r.get("urun", "").strip().lower(): r for r in (dict(zip(satirlar[0], s)) for s in satirlar[1:])}, True


def kanit_var(klasor, no):
    n = re.sub(r"\D", "", no or "").zfill(2)
    kd = os.path.join(os.path.dirname(os.path.abspath(klasor)), "kanit")
    return bool(glob.glob(os.path.join(kd, n + "-*.md")))


def nihai(r, klasor):
    """Kullanıcıya gidecek tek hüküm: SAT | KANIT-BEKLIYOR | ELE | DISI. Kullanıcıya yalnız SAT gider."""
    karar = (r["karar"] or "").strip()
    if karar == "ELE" or (not karar and r["on_karar"] == "ELE") or r["on_karar"] == "ELE":
        return "ELE"
    if karar and not sat_ailesi(karar):
        return "DISI"          # eski İZLE vb.: denetim kaydında kalır, kullanıcıya gitmez
    if not karar and r["on_karar"] != "SAT-ADAYI":
        return "DISI"
    return "SAT" if kanit_var(klasor, r["no"]) else "KANIT-BEKLIYOR"


def link_anahtari(link):
    m = re.search(r"-p-(\d+)", link or "")
    if m:
        return "p" + m.group(1)
    return re.sub(r"[?#].*$", "", (link or "").strip().lower()).rstrip("/")


class Liste(list):
    alanlar = TEMEL_ALANLAR


def adaylari_oku(yol):
    if not os.path.isfile(yol):
        raise ValueError("dosya yok: %s" % yol)
    satirlar = tsv_oku(yol)
    if not satirlar:
        raise ValueError("dosya boş: %s" % yol)
    baslik = [h.strip() for h in satirlar[0]]
    if baslik not in (TEMEL_ALANLAR, ALANLAR):
        raise ValueError("başlık tam bu %d (ya da ek alanlı %d) alan olmalı (sekme ayraçlı): %s" % (
            len(TEMEL_ALANLAR), len(ALANLAR), ", ".join(ALANLAR)))
    out = Liste()
    out.alanlar = baslik
    for i, s in enumerate(satirlar[1:], 2):
        if len(s) > len(baslik):
            raise ValueError("satır %d: %d alan var (en çok %d)" % (i, len(s), len(baslik)))
        d = dict.fromkeys(ALANLAR, "")
        d.update(zip(baslik, [h.strip() for h in s + [""] * (len(baslik) - len(s))]))
        out.append(d)
    return out


# ------------------------------------------------------------------ kota
def kota_yolu(klasor):
    return os.path.join(klasor, "kota.tsv")


def kota_oku(klasor):
    y = kota_yolu(klasor)
    if not os.path.isfile(y):
        return []
    satirlar = tsv_oku(y)
    return [dict(zip(KOTA_ALANLAR, s + [""] * 6)) for s in satirlar[1:]]


def kota_ekle(klasor, tur, hedef, kilit="", sonuc=""):
    os.makedirs(klasor, exist_ok=True)
    y = kota_yolu(klasor)
    yeni = not os.path.isfile(y)
    n = simdi()
    with open(y, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        if yeni:
            w.writerow(KOTA_ALANLAR)
        w.writerow([n.date().isoformat(), n.time().strftime("%H:%M:%S"), tur, hedef, kilit, sonuc])


def kota_say(satirlar):
    """Bugünkü satırlardan etkin istek anahtarları: (tur, hedef). iade satırı anahtarı düşürür; aynı hedefin tekrarı ikinci kez sayılmaz."""
    etkin = {}
    for r in satirlar:
        if r["tur"] in ("arama", "urun"):
            etkin[(r["tur"], r["hedef"].strip().lower())] = r["sonuc"] != "iade"
    return {t: sum(1 for (tt, _), v in etkin.items() if tt == t and v) for t in ("arama", "urun")}, etkin


def kota(klasor, args):
    komutlar = ("durum", "kaydet", "kilit", "iade", "sonuc")
    if not args or args[0] not in komutlar:
        print("kullanım: kota durum | kaydet <arama|urun> <hedef> | iade <arama|urun> <hedef> | sonuc <ok|bos|429|403|captcha> [hedef] | kilit [sebep]")
        return 2
    esik = esikleri_oku()
    # Günlük sayı sabit kota değil, üst güvenlik sınırıdır (varsayim). Asıl durma ölçütü: engel sinyali (kota sonuc).
    tavan = {"arama": int(esik["kota_arama_gunluk"]["sat"]), "urun": int(esik["kota_urun_gunluk"]["sat"])}
    bekleme = int(esik["kota_bekleme_sn"]["sat"])
    bugun = simdi().date().isoformat()
    bugunku = [r for r in kota_oku(klasor) if r["tarih"] == bugun]
    kilitli = [r for r in bugunku if r["kilit"]]
    say, etkin = kota_say(bugunku)
    if args[0] == "kilit":
        kota_ekle(klasor, "kilit", "", " ".join(args[1:]) or "engel")
        print("KILIT YAZILDI: bugün Trendyol'a dokunulmaz")
        return 0
    if args[0] == "sonuc":
        if len(args) < 2 or args[1] not in ("ok", "bos", "429", "403", "captcha"):
            print("kullanım: kota sonuc <ok|bos|429|403|captcha> [hedef]")
            return 2
        kota_ekle(klasor, "sonuc", " ".join(args[2:]), "", args[1])
        if args[1] in ("429", "403", "captcha"):
            kota_ekle(klasor, "kilit", "", "engel sinyali: " + args[1])
            print("ENGEL SİNYALİ (%s): kilit yazıldı, bugün Trendyol'a dokunulmaz" % args[1])
            return 3
        son = [r["sonuc"] for r in bugunku if r["tur"] == "sonuc"] + [args[1]]
        art_arda = 0
        for v in reversed(son):
            if v != "bos":
                break
            art_arda += 1
        if art_arda >= 3:
            kota_ekle(klasor, "kilit", "", "boş sonuç sayfası art arda %d" % art_arda)
            print("ENGEL SİNYALİ (boş sonuç art arda %d): kilit yazıldı" % art_arda)
            return 3
        print("SONUÇ KAYDEDİLDİ: %s (art arda boş: %d/3)" % (args[1], art_arda))
        return 0
    if args[0] == "durum":
        print("bugün %s: arama %d (üst sınır %d) · ürün sayfası %d (üst sınır %d) · kilit: %s" % (
            bugun, say["arama"], tavan["arama"], say["urun"], tavan["urun"], kilitli[-1]["kilit"] if kilitli else "yok"))
        if kilitli:
            return 3
        return 4 if any(say[t] >= tavan[t] for t in tavan) else 0
    if len(args) < 3 or args[1] not in tavan:
        print("kullanım: kota %s <arama|urun> <hedef>" % args[0])
        return 2
    tur, hedef = args[1], " ".join(args[2:])
    anahtar = (tur, hedef.strip().lower())
    if args[0] == "iade":
        if not etkin.get(anahtar):
            print("İADE YOK: %s %s bugün sayılmış bir kayıt değil" % (tur, hedef))
            return 1
        kota_ekle(klasor, tur, hedef, "", "iade")
        print("İADE EDİLDİ: %s %s kotadan düşüldü (%d)" % (tur, hedef, say[tur] - 1))
        return 0
    if kilitli:
        print("KİLİTLİ: %s" % kilitli[-1]["kilit"])
        return 3
    if etkin.get(anahtar):
        print("TEKRAR: %s %s bugün zaten kayıtlı, kotaya sayılmadı (aynı terimi iki kez arama)" % (tur, hedef))
        return 0
    if say[tur] >= tavan[tur]:
        print("GÜNLÜK ÜST SINIR DOLDU: %s %d/%d" % (tur, say[tur], tavan[tur]))
        return 4
    istekler = [r for r in bugunku if r["tur"] in tavan]
    if istekler:
        son = datetime.datetime.fromisoformat(istekler[-1]["tarih"] + "T" + istekler[-1]["saat"])
        gecen = (simdi() - son).total_seconds()
        if gecen < bekleme:
            print("BEKLE: son istekten %d sn geçti, en az %d sn gerekir" % (gecen, bekleme))
            return 4
    kota_ekle(klasor, tur, hedef)
    print("KAYDEDİLDİ: %s %d (üst sınır %d)" % (tur, say[tur] + 1, tavan[tur]))
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
def denetle(yol, elenenlere_yaz=False, marj_yolu=None):
    try:
        esik = esikleri_oku()
        satirlar = adaylari_oku(yol)
    except ValueError as e:
        print("HATA: %s" % e)
        return 1
    genis = "alis_kaynak" in satirlar.alanlar
    hata, uyari = [], []
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
                          ("meta_reklam", True), ("onerilen_satis_tl", False), ("rakip_tl", False)):
            try:
                sayi(r[alan], tam)
            except ValueError:
                hata.append("satır %d: %s sayı değil: %r" % (i, alan, r[alan]))
        if r["viral_db"] and r["viral_db"] not in VIRAL_DEGERLER:
            hata.append("satır %d: viral_db %r; izinli: %s" % (i, r["viral_db"], ", ".join(VIRAL_DEGERLER)))
        # alis_tl = tedarikçi alışı. Trendyol perakende fiyatı rakip_tl'dedir (hedef satış ve rakip fiyatı), ASLA alis_tl'de değil.
        if r["alis_tl"].strip():
            try:
                a_, rk_ = sayi(r["alis_tl"]), sayi(r["rakip_tl"])
            except ValueError:
                a_, rk_ = None, None
            if a_ is not None and rk_ is not None and abs(a_ - rk_) < 0.005:
                hata.append("satır %d: alis_tl (%g) rakip_tl ile aynı: alis_tl Trendyol perakende fiyatı olamaz; alış tedarikçiden (AliExpress/1688 aynı ürün), yoksa boş bırak" % (i, a_))
            if re.search(r"trendyol", r["alis_kaynak"], re.I):
                hata.append("satır %d: alis_kaynak Trendyol: alis_tl Trendyol perakende fiyatı olamaz; tedarikçi (AliExpress/1688) kaynağı yaz ya da alis_tl'yi boş bırak" % i)
            elif genis and not r["alis_kaynak"].strip():
                hata.append("satır %d: alis_tl dolu ama alis_kaynak boş: alis_tl tedarikçiden gelir (Trendyol perakende fiyatı olamaz); kaynak linkini yaz" % i)
        if r["karar"] == "İZLE":
            uyari.append("satır %d: karar İZLE eski sınıf (kurucu kararı 2026-11-25: yalnız SAT ve ELE); denetim kaydında kalır, kullanıcıya gitmez" % i)
        elif r["karar"] and r["karar"] != "ELE" and not sat_ailesi(r["karar"]):
            hata.append("satır %d: karar %r; izinli: SAT / ELE (SAT-KOŞULLU: <ilk testte kontrol edilecek> eski yazım olarak SAT sayılır)" % (i, r["karar"]))
    if hata:
        for h in hata:
            print("HATA: " + h)
        return 1
    for u in uyari:
        print("UYARI: " + u)
    marj, marj_verildi = marj_oku(os.path.dirname(os.path.abspath(yol)), marj_yolu)
    if marj_yolu and not marj_verildi:
        print("HATA: --marj-sonuc dosyası yok: %s" % marj_yolu)
        return 1
    elenen = []
    for r in satirlar:
        r["on_karar"], notlar, kontrol, ele = satir_karari(r, esik, marj.get(r["urun"].lower()), marj_verildi)
        if r["on_karar"] == "ELE" and sat_ailesi(r["karar"]):
            hata.append("%s: karar %r ama kanıtlı engel var (%s); SAT yazılamaz" % (r["urun"], r["karar"], "; ".join(ele)))
        r["neden"] = neden_yaz(r["neden"], r["on_karar"], kontrol, ele)
        print("%-3s %-40s %-10s %s" % (r["no"], r["urun"][:40], r["on_karar"], " · ".join(n for n in notlar if not n.endswith("SAT"))))
        if r["on_karar"] == "ELE":
            elenen.append((r, ele))
    if hata:
        for h in hata:
            print("HATA: " + h)
        return 1
    tsv_yaz(yol, satirlar.alanlar, [[r[a] for a in satirlar.alanlar] for r in satirlar])
    if elenenlere_yaz and elenen:
        klasor = os.path.dirname(os.path.abspath(yol))
        ey = os.path.join(klasor, "elenenler.tsv")
        eski = tsv_oku(ey)[1:] if os.path.isfile(ey) else []
        var = {link_anahtari(s[0]) for s in eski if s}
        bugun = simdi().date().isoformat()
        for r, ele in elenen:
            if link_anahtari(r["trendyol_link"]) not in var:
                eski.append([r["trendyol_link"], "; ".join(ele) or "on_karar ELE", bugun])
        tsv_yaz(ey, ["link", "sebep", "tarih"], eski)
    toplam = len(satirlar)
    say = {k: sum(1 for r in satirlar if r["on_karar"] == k) for k in ("SAT-ADAYI", "ELE")}
    print("denetle: %d aday · SAT-ADAYI %d · ELE %d (kullanıcıya yalnız SAT gider; bilinmeyen ölçüt engel değil, 'Kontrol et' notu olur)" % (toplam, say["SAT-ADAYI"], say["ELE"]))
    if PROFIL_NOTU:
        print("PROFIL: danışanın işletme profili kullanıldı (%s)" % ", ".join(PROFIL_NOTU))
    else:
        print("PROFIL: yok ya da ilgili alan yok → eklenti varsayılanı kullanıldı (kat >= %s, satış >= %s TL); kendi değerini .ekip/isletme-profili.tsv'ye yaz"
              % (esik["kat"]["sat"].replace(">=", ""), esik["satis_tl_min"]["sat"]))
    deneme = [k for k, e in esik.items() if e["durum"] in ("varsayim", "deneme", "varsayilan")]
    if deneme:
        kanitli = len([f for f in os.listdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(yol))), "kanit"))]) \
            if os.path.isdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(yol))), "kanit")) else 0
        print("%d/20 kanıt: eşikler DENEME (%d ölçüt varsayım ya da denemedir)" % (kanitli, len(deneme)))
    return 0


# ------------------------------------------------------------------ ozet
def ozet(yol, args):
    """Kullanıcı özeti: YALNIZ SAT. Elenen/izlenen satır, sayı ve ürün adı basılmaz (denetim dosyada kalır)."""
    hedef, sebep_arg = 5, None
    if "--hedef" in args:
        hedef = int(args[args.index("--hedef") + 1])
    if "--sebep" in args:
        sebep_arg = args[args.index("--sebep") + 1]
    try:
        esik = esikleri_oku()
        satirlar = adaylari_oku(yol)
    except ValueError as e:
        print("HATA: %s" % e)
        return 1
    klasor = os.path.dirname(os.path.abspath(yol))
    marj, marj_verildi = marj_oku(klasor)
    sat, bekleyen, sebepler = [], 0, {}
    for r in satirlar:
        h = nihai(r, klasor)
        _, _, kontrol, ele = satir_karari(r, esik, marj.get(r["urun"].lower()), marj_verildi)
        if h == "SAT":
            sat.append((r, kontrol))
        elif h == "KANIT-BEKLIYOR":
            bekleyen += 1
        elif h == "ELE":
            for e in ele or ["yazılı karar eşiği geçmedi"]:
                anahtar = re.split(r"\s[\d(]", e)[0].split(":")[0].strip()
                sebepler[anahtar] = sebepler.get(anahtar, 0) + 1
    print("SAT %d/%d · %d aday tarandı" % (len(sat), hedef, len(satirlar)))
    if sat:
        print("Etiket sözlüğü: SAT = kanıt dosyası var ve kanıtlı engel yok (satış garantisi DEĞİL; ilk test şart).")
        print("  'ilk testte kontrol et' = ölçülemeyen ölçüt; engel değil, ilk testte bak.")
        print("  Alış = tedarikçi fiyatı; Trendyol fiyatı yalnız hedef satışı/rakip fiyatını gösterir.")
    for n, (r, kontrol) in enumerate(sat[:8], 1):
        puan = r["puan"]
        parca = ["%d. %s" % (n, r["urun"]), "%s yorum · %s puan" % (r["yorum"] or "?", puan or "?")]
        a, sa = sayi(r["alis_tl"]), sayi(r["onerilen_satis_tl"])
        if a and sa:
            parca.append("alış %g TL (tedarikçi) → satış %g TL (%.1f×)" % (a, sa, sa / a))
        elif sa:
            parca.append("satış %g TL (tedarikçi alışı yok)" % sa)
        if kontrol:
            parca.append("ilk testte kontrol et: " + "; ".join(kontrol))
        print(" · ".join(parca))
    if len(sat) > 8:
        print("+%d SAT daha: urunler.xlsx" % (len(sat) - 8))
    if bekleyen:
        print("%d aday kanıt dosyası bekliyor (kanıt yazılınca SAT olarak görünür)" % bekleyen)
    if len(sat) < hedef:
        sebep = sebep_arg or (", ".join(k for k, _ in sorted(sebepler.items(), key=lambda x: -x[1])[:2]) + " eşiği geçmedi"
                              if sebepler else "tarama sınırı ya da engel sinyali")
        print("%d SAT buldum, sebep: %s" % (len(sat), sebep))
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
    if db and os.path.isfile(db):
        try:
            c = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
            viraller = c.execute("SELECT ad, aile, hukum FROM v_viral_urun WHERE hukum IN ('VIRAL-URUN','VIRAL-VIDEO')").fetchall()
            c.close()
        except sqlite3.Error as e:
            print("UYARI: veritabanı okunamadı (%s): hepsi dogrulanamadi" % e)
    else:
        # Danışanda analiz.db yok: eklentiyle gelen sansürlü tablo (ortak/bilgi/viral-urunler.tsv) kullanılır.
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "ortak"))
        try:
            import viral_db
            tablo = viral_db.oku()
        except ImportError:
            tablo = None
        if tablo is None:
            print("UYARI: veritabanı yok (%s) ve eklenti tablosu yok: hepsi dogrulanamadi" % (db or "-"))
        else:
            viraller = [(r.get("ad_jenerik", ""), r.get("aile", ""), r.get("hukum", "")) for r in tablo
                        if r.get("hukum") in ("VIRAL-URUN", "VIRAL-VIDEO")]
            print("BİLGİ: analiz.db yok; eklenti tablosu kullanıldı (%d viral satır)" % len(viraller))
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
            # Canlı rol sınavı 2026-11-25: tek ortak kelime ("köpek") köpek kostümünü 23 köpek yatağıyla "aile" sayıyordu.
            # Aile = aile adı birebir aynı ya da aile adının BÜTÜN kelimeleri viral satırda geçiyor.
            if aile_j and ((aile or "").strip() == r["aile"].strip() or aile_j <= hedef):
                sonuc = "aile-var"
        r["viral_db"] = sonuc
        print("%-3s %-40s %s" % (r["no"], r["urun"][:40], sonuc))
    tsv_yaz(yol, satirlar.alanlar, [[r[a] for a in satirlar.alanlar] for r in satirlar])
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
    print("sonra: trendyol_kontrol.py sinama <adaylar.tsv> --kontrol <okunan.tsv>")
    for r in sec:
        print("- %s | %s | alis %s · yorum %s · puan %s" % (r["urun"], r["trendyol_link"], r["alis_tl"], r["yorum"], r["puan"]))
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    args = argv[1:]
    klasor = os.path.join("is", "firsat", "trendyol")
    if "--profil" in args:
        i = args.index("--profil")
        global PROFIL_YOLU
        PROFIL_YOLU = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
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
            marj_yolu = None
            if "--marj-sonuc" in rest:
                i = rest.index("--marj-sonuc")
                marj_yolu = rest[i + 1]
                del rest[i:i + 2]
            return denetle(rest[0], "--elenenlere-yaz" in rest, marj_yolu)
        if komut == "ozet" and rest:
            return ozet(rest[0], rest[1:])
        if komut == "viral":
            db = None
            if "--db" in rest:
                i = rest.index("--db")
                db = rest[i + 1]
                del rest[i:i + 2]
            if rest:
                return viral(db, rest[0])
        if komut == "sinama" and rest:
            return sinama(rest[0], rest[1:])
    except (ValueError, OSError) as e:  # ProfilHatasi de ValueError'dır
        print("HATA: %s" % e)
        return 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
