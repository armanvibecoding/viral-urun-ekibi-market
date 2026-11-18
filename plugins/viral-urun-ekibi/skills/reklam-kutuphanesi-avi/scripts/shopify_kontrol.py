#!/usr/bin/env python3
"""Hedef alan adı Shopify mı, mağaza kaç günlük? — alan adı başına TEK istek, önbellekli, engelde durur.

  python3 shopify_kontrol.py bekleyen  --db is/meta/reklam.db [--pazar US] [--adet 20]
        Alan adı bilinmeyen sayfaları (MCP alan adı vermez) ön sıraya göre listeler: her biri için 1 snapshot URL'si.
        Lider bunu Chrome'da açar, reklamın hedef linkini okur → `alan-ekle`. Günde en çok 60 snapshot (ayrı sayaç).
  python3 shopify_kontrol.py alan-ekle --db ... --page-id 123 --alan ornek-dukkan.com   (ya da --dosya sayfa_alan.tsv)
  python3 shopify_kontrol.py kontrol   --db ... [--adet 50] [--bekle 10]
        Kontrol edilmemiş alanlar için `https://<alan>/products.json?limit=250` adresine TEK GET:
          200 + {"products": [...]}               → shopify=1, ürün sayısı, en eski created_at → mağaza yaşı
          başlık/gövdede Shopify izi (x-shopid, x-shopify-*, powered-by: Shopify, cdn.shopify.com, Shopify.theme)
                                                    → shopify=1, yaş bilinmiyor
          iz yok                                    → shopify=0 (kayıt tutulur, analiz kuyruğuna girmez)
          429 / 5xx / zaman aşımı                   → 'ertelendi' (24 sa ya da Retry-After); bir koşuda 3× 429 → koşu DURUR (çıkış 3)
          401/403                                   → 'hata', yeniden denenmez (koruma/engel: atlatma yok)
        Pazaryeri ve sosyal alanlara istek atılmaz (shopify=0). 'tamam' alana bir daha istek atılmaz.
  python3 shopify_kontrol.py liste     --db ...

İstek kimliği dürüsttür (tarayıcı taklidi yok): User-Agent `viral-urun-ekibi-shopify-kontrol/1.0`.
Testte hedef adres REKLAMAVI_SHOPIFY_TABAN ile değiştirilir (örn. http://127.0.0.1:8000/{alan}).
Çıkış: 0 tamam · 1 yanlış girdi · 3 çok 429 — bugün dur.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)
import ortak as o  # noqa: E402
import toplanan_isle as ti  # noqa: E402
import toplayici_ortak as t  # noqa: E402

UA = "viral-urun-ekibi-shopify-kontrol/1.0 (alan basina tek istek; 429'da durur)"
AZAMI_BAYT = 3 * 1024 * 1024
SNAPSHOT_GUNLUK = 60
SHOPIFY_IZ = re.compile(r"cdn\.shopify\.com|Shopify\.theme|myshopify\.com|shopify-section", re.I)
ALAN_DESEN = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$")


def alan_temiz(a):
    a = (a or "").strip().lower()
    if "://" in a or "/" in a:
        a, _ = o.link_coz(a)
    if a.startswith("www."):
        a = a[4:]
    if not ALAN_DESEN.match(a):
        raise o.VeriHatasi("alan adı geçersiz: %r" % a)
    return a


def bekleyen(c, pazar, adet):
    bugun = t.bugun_str()
    yapilan = c.execute("SELECT COUNT(*) FROM sayfa_alan WHERE tarih=? AND kaynak='chrome-snapshot'", (bugun,)).fetchone()[0]
    kalan = max(0, SNAPSHOT_GUNLUK - yapilan)
    oz = ti.sayfa_ozeti(c, pazar)
    adaylar = [x for x in oz.values() if not x["alan"] and not x["birim"].startswith("sayfa:")]
    adaylar.sort(key=lambda x: (-x["reklam"], -(x["max_gun"] or 0)))
    print("# snapshot kotası bugün %d/%d kullanıldı · aralar ≥15 sn · yalnız oku (tıklama/satın alma yok)" % (yapilan, SNAPSHOT_GUNLUK))
    print("pazar\tpage_id\tsayfa\treklam\tmax_gun\tsnapshot_url")
    for x in adaylar[:min(adet, kalan)]:
        print("\t".join(str(v) for v in (x["pazar"], x["birim"], x["page_name"], x["reklam"], x["max_gun"], x["snapshot"])))
    if not kalan:
        print("SNAPSHOT KOTASI DOLDU — yarın devam.")


def alan_ekle(c, ciftler, kaynak):
    bugun = t.bugun_str()
    for pid, alan in ciftler:
        if not re.fullmatch(r"\d+", pid or ""):
            raise o.VeriHatasi("page_id sayı değil: %r" % pid)
        a = alan_temiz(alan)
        c.execute("INSERT INTO sayfa_alan VALUES (?,?,?,?) ON CONFLICT(page_id) DO UPDATE SET alan=excluded.alan, "
                  "kaynak=excluded.kaynak, tarih=excluded.tarih", (pid, a, kaynak, bugun))
        c.execute("UPDATE reklam SET hedef_alan=? WHERE page_id=? AND (hedef_alan IS NULL OR hedef_alan='')", (a, pid))
    c.commit()
    print("%d sayfa → alan eşlendi" % len(ciftler))


def _adres(alan):
    taban = os.environ.get("REKLAMAVI_SHOPIFY_TABAN")
    kok = taban.format(alan=alan) if taban else "https://" + alan
    return kok.rstrip("/") + "/products.json?limit=250"


def getir(alan):
    """(kod, basliklar{küçük harf}, govde_metni, nihai_url). Ağ hatası: kod=None."""
    istek = urllib.request.Request(_adres(alan), headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(istek, timeout=15) as y:
            return y.status, {k.lower(): v for k, v in y.headers.items()}, y.read(AZAMI_BAYT).decode("utf-8", "replace"), y.geturl()
    except urllib.error.HTTPError as e:
        try:
            govde = e.read(AZAMI_BAYT).decode("utf-8", "replace")
        except Exception:
            govde = ""
        return e.code, {k.lower(): v for k, v in (e.headers or {}).items()}, govde, _adres(alan)
    except Exception as e:  # zaman aşımı, DNS, TLS
        return None, {}, "%s: %s" % (type(e).__name__, e), _adres(alan)


def yorumla(kod, bas, govde):
    """→ (durum, shopify, kanit, urun_sayisi, en_eski)."""
    if kod == 429 or kod is None or (kod and kod >= 500):
        return "ertelendi", None, "http %s" % kod if kod else govde[:120], None, None
    if kod in (401, 403):
        return "hata", None, "http %d — koruma/engel, atlatma yok" % kod, None, None
    if kod == 200:
        try:
            d = json.loads(govde)
        except ValueError:
            d = None
        if isinstance(d, dict) and isinstance(d.get("products"), list):
            tarihler = sorted(p.get("created_at", "")[:10] for p in d["products"] if isinstance(p, dict) and o.iso_mu(str(p.get("created_at", ""))[:10]))
            return "tamam", 1, "products.json", len(d["products"]), (tarihler[0] if tarihler else None)
    iz = [k for k in bas if k.startswith("x-shopify") or k == "x-shopid"]
    if "shopify" in bas.get("powered-by", "").lower():
        iz.append("powered-by")
    if SHOPIFY_IZ.search(govde or ""):
        iz.append("govde-izi")
    if iz:
        return "tamam", 1, "iz:" + ",".join(iz[:3]) + " (products.json yok/kapalı → yaş bilinmiyor)", None, None
    return "tamam", 0, "http %s, Shopify izi yok" % kod, None, None


def kontrol_listesi(c):
    simdi = t.simdi().isoformat(timespec="seconds")
    alanlar = {r[0] for r in c.execute("SELECT DISTINCT hedef_alan FROM reklam WHERE hedef_alan IS NOT NULL AND hedef_alan<>''")}
    alanlar |= {r[0] for r in c.execute("SELECT alan FROM sayfa_alan")}
    hazir = []
    for a in sorted(alanlar):
        m = c.execute("SELECT * FROM magaza WHERE alan=?", (a,)).fetchone()
        if m is None or m["durum"] == "bekliyor" or (m["durum"] == "ertelendi" and (m["ertele_bitis"] or "") <= simdi):
            hazir.append(a)
    return hazir


def kontrol(c, adet, bekle):
    if bekle < t.SHOPIFY_BEKLE_SN and not os.environ.get("REKLAMAVI_SHOPIFY_TABAN"):
        raise o.VeriHatasi("bekleme %d sn < en az %d sn: düşürülemez" % (bekle, t.SHOPIFY_BEKLE_SN))
    hazir = kontrol_listesi(c)
    sayac = {"istek": 0, "shopify": 0, "degil": 0, "ertelendi": 0, "hata": 0, "istek_yok": 0}
    cok429 = 0
    for a in hazir[:adet]:
        tip = o.tip_bul(a, "/")
        simdi = t.simdi()
        if tip in ("PAZARYERI",) or any(a.startswith(s) or ("." + s) in a for s in o.SOSYAL):
            c.execute("INSERT OR REPLACE INTO magaza(alan,durum,shopify,kanit,istek_sayisi,son_istek) VALUES (?,?,?,?,0,?)",
                      (a, "tamam", 0, "pazaryeri/sosyal — istek atılmadı", simdi.isoformat(timespec="seconds")))
            sayac["istek_yok"] += 1
            continue
        if sayac["istek"]:
            time.sleep(bekle)
        kod, bas, govde, nihai = getir(a)
        sayac["istek"] += 1
        durum, shp, kanit, n, eski = yorumla(kod, bas, govde)
        once = c.execute("SELECT istek_sayisi FROM magaza WHERE alan=?", (a,)).fetchone()
        istek = (once[0] if once else 0) + 1
        ertele = None
        if durum == "ertelendi":
            saat = t.SHOPIFY_ERTELE_SAAT
            ra = bas.get("retry-after", "")
            if ra.isdigit():
                saat = max(saat, int(ra) / 3600.0)
            ertele = (simdi + dt.timedelta(hours=saat)).isoformat(timespec="seconds")
            if istek >= t.HATA_DENEME:
                durum, kanit = "hata", kanit + " (%d. deneme — bırakıldı)" % istek
            if kod == 429:
                cok429 += 1
        yas = o.gun_farki(simdi.date().isoformat(), eski) if eski else None
        c.execute("""INSERT OR REPLACE INTO magaza(alan,durum,shopify,kanit,http_kodu,urun_sayisi,en_eski_urun,yas_gun,
                     istek_sayisi,son_istek,ertele_bitis,nihai_alan) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (a, durum, shp, kanit, kod, n, eski, yas, istek, simdi.isoformat(timespec="seconds"), ertele,
                   o.link_coz(nihai)[0] if nihai else None))
        c.commit()
        sayac["shopify" if shp == 1 else "degil" if shp == 0 else durum] += 1
        if cok429 >= t.SHOPIFY_429_DUR:
            print("DUR — bu koşuda %d alan 429 verdi. Kalan alanlar yarın; atlatma yok." % cok429)
            print(json.dumps(sayac, ensure_ascii=False))
            sys.exit(3)
    c.commit()
    print("kontrol: %s · kuyrukta kalan %d" % (json.dumps(sayac, ensure_ascii=False), max(0, len(hazir) - adet)))


def liste(c):
    print("alan\tdurum\tshopify\turun\ten_eski\tyas_gun\tistek\tkanit")
    for r in c.execute("SELECT * FROM magaza ORDER BY shopify DESC, yas_gun"):
        print("\t".join(str(r[k]) if r[k] is not None else o.GORUNMUYOR for k in
                        ("alan", "durum", "shopify", "urun_sayisi", "en_eski_urun", "yas_gun", "istek_sayisi", "kanit")))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut")
    b = alt.add_parser("bekleyen")
    b.add_argument("--db", required=True)
    b.add_argument("--pazar")
    b.add_argument("--adet", type=int, default=20)
    e = alt.add_parser("alan-ekle")
    e.add_argument("--db", required=True)
    e.add_argument("--page-id")
    e.add_argument("--alan")
    e.add_argument("--dosya", help="TSV: page_id<TAB>alan (başlıksız)")
    e.add_argument("--kaynak", default="chrome-snapshot")
    k = alt.add_parser("kontrol")
    k.add_argument("--db", required=True)
    k.add_argument("--adet", type=int, default=50)
    k.add_argument("--bekle", type=float, default=t.SHOPIFY_BEKLE_SN)
    s = alt.add_parser("liste")
    s.add_argument("--db", required=True)
    x = ap.parse_args()
    if not x.komut:
        ap.print_help()
        sys.exit(1)
    try:
        c = t.baglan(x.db)
        if x.komut == "bekleyen":
            bekleyen(c, x.pazar, x.adet)
        elif x.komut == "alan-ekle":
            if x.dosya:
                with open(x.dosya, encoding="utf-8") as f:
                    ciftler = [tuple(s.rstrip("\n").split("\t")[:2]) for s in f if s.strip()]
                if any(len(p) != 2 for p in ciftler):
                    raise o.VeriHatasi("dosya satırı 'page_id<TAB>alan' değil")
            elif x.page_id and x.alan:
                ciftler = [(x.page_id, x.alan)]
            else:
                raise o.VeriHatasi("--page-id + --alan ya da --dosya gerekli")
            alan_ekle(c, ciftler, x.kaynak)
        elif x.komut == "kontrol":
            kontrol(c, x.adet, x.bekle)
        else:
            liste(c)
    except o.VeriHatasi as ex:
        o.hata_cik(str(ex))


if __name__ == "__main__":
    main()
