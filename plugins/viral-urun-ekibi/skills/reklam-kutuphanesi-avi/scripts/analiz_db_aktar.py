#!/usr/bin/env python3
"""Adaptör: reklam.db derin analiz kuyruğunu kullanıcı projesindeki analiz veritabanına (hesap/urun/video) yazar.

  python3 analiz_db_aktar.py --db is/meta/reklam.db --analiz-modul <proje>/veri/db.py --analiz-db <proje>/veri/analiz.db
                             [--pazar US] [--tum] [--deneme]

Analiz modülü (db.py) projede durur, eklentide değil: yolu `--analiz-modul` ya da REKLAMAVI_ANALIZ_MODUL ile verilir.
Modül yoksa çıkış 4 — veri reklam.db'de kalır, adaptör sonra bağlanır (başka bir şey yapılmaz).
Beklenen modül arayüzü: baglan(yol), kur(c), hesap_yaz(c, dict), urun_yaz(c, dict), video_yaz(c, dict),
isteğe bağlı urun_esle(ad, hesap, platform) ve kisa_ad(metin).
Eşleme: sayfa → hesap(platform=facebook) · başlık/ürün yolu → urun · reklam → video(reklam_mi=E,
kaynak_yontemi=meta-reklam-kutuphanesi, video_anahtari=meta-ad-<id>, kaynak_ref=<id>).
Varsayılan: yalnız derin=1 sayfaların reklamları (25k reklamın hepsi değil). --tum: puanlanan tüm Shopify sayfaları.
--deneme: hiçbir şey yazmaz, kaç satır yazılacağını basar.
Çıkış: 0 tamam · 1 yanlış girdi · 4 analiz modülü/DB bağlanamadı.
"""
import argparse
import importlib.util
import os
import re
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)
import ortak as o  # noqa: E402
import toplanan_isle as ti  # noqa: E402
import toplayici_ortak as t  # noqa: E402


def modul_yukle(yol):
    if not yol or not os.path.exists(yol):
        print("ADAPTÖR BAĞLANMADI: analiz modülü yok (%s). Veri reklam.db'de duruyor; modül hazır olunca tekrar çalıştır." % yol)
        sys.exit(4)
    spec = importlib.util.spec_from_file_location("analiz_db_modul", yol)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except Exception as e:
        print("ADAPTÖR BAĞLANMADI: modül yüklenemedi: %r" % e)
        sys.exit(4)
    eksik = [f for f in ("baglan", "kur", "hesap_yaz", "urun_yaz", "video_yaz") if not hasattr(m, f)]
    if eksik:
        print("ADAPTÖR BAĞLANMADI: modülde eksik işlev: %s" % ",".join(eksik))
        sys.exit(4)
    return m


def _kisa(m, s):
    if hasattr(m, "kisa_ad"):
        return m.kisa_ad(s)
    return re.sub(r"[^a-z0-9]+", "-", o.norm(s)).strip("-")[:60]


def aktar(c, m, analiz_db, pazar, tum, deneme):
    kosul = "shopify=1" + ("" if tum else " AND derin=1") + (" AND pazar=?" if pazar else "")
    secili = c.execute("SELECT * FROM puan WHERE " + kosul, (pazar,) if pazar else ()).fetchall()
    if not secili:
        raise o.VeriHatasi("aktarılacak sayfa yok (önce basari_puani.py hesapla; derin=1 Shopify sayfası gerekli)")
    birimler = {(r["pazar"], r["birim"]): r for r in secili}
    reklamlar = [r for r in c.execute("SELECT * FROM reklam") if (r["pazar"], ti.birim(r)) in birimler]
    if deneme:
        print("DENEME: %d sayfa (hesap) · %d reklam (video) yazılacaktı → %s" % (len(birimler), len(reklamlar), analiz_db))
        return
    ac = m.baglan(analiz_db)
    m.kur(ac)
    hesap_id = {}
    for (pz, b), p in birimler.items():
        kullanici = ("fbpage-" + b) if not b.startswith("sayfa:") else "fbpage-" + _kisa(m, b[6:])
        hesap_id[(pz, b)] = m.hesap_yaz(ac, {
            "platform": "facebook", "kullanici_adi": kullanici, "marka_adi": p["page_name"],
            "pazar": t.PAZAR_ANALIZ.get(pz, "bilinmiyor"), "pazar_ham": pz, "site": p["alan"],
            "kaynak": "reklam-kutuphanesi-avi"})
    n = 0
    for r in reklamlar:
        key = (r["pazar"], ti.birim(r))
        p = birimler[key]
        ad = r["baslik"] or (o.urun_yolu(r["hedef_yol"] or "").replace("-", " ")) or (r["govde"] or "")[:60] or ("reklam " + r["ad_id"])
        kullanici = "fbpage-" + key[1]
        if hasattr(m, "urun_esle"):
            uid, aile, esl = m.urun_esle(ad, hesap=kullanici, platform="facebook")
        else:
            uid, aile, esl = "a-" + _kisa(m, ad), None, "ad"
        m.urun_yaz(ac, {"urun_id": uid, "ad": ad, "aile": aile, "nis": r["nis"] or "bilinmiyor",
                        "nis_kaynak": "reklam-kutuphanesi-sorgu", "eslesme_kaynagi": esl})
        m.video_yaz(ac, {
            "video_anahtari": "meta-ad-" + r["ad_id"], "platform": "facebook", "url": r["snapshot_url"],
            "hesap_id": hesap_id[key], "urun_id": uid, "pazar": t.PAZAR_ANALIZ.get(r["pazar"], "bilinmiyor"),
            "nis": r["nis"] or "bilinmiyor", "yayin_tarihi": r["yayin_tarihi"], "okuma_tarihi": r["okuma_tarihi"],
            "reklam_mi": "E", "kaynak_yontemi": "meta-reklam-kutuphanesi", "kaynak_ref": r["ad_id"],
            "liste_karari": "derin-analiz puan=%s sira=%s" % (p["puan"], p["sira"])})
        n += 1
    ac.commit()
    print("aktarıldı: %d hesap · %d video → %s" % (len(birimler), n, analiz_db))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True)
    ap.add_argument("--analiz-modul", default=os.environ.get("REKLAMAVI_ANALIZ_MODUL"))
    ap.add_argument("--analiz-db", required=True)
    ap.add_argument("--pazar")
    ap.add_argument("--tum", action="store_true")
    ap.add_argument("--deneme", action="store_true")
    x = ap.parse_args()
    m = modul_yukle(x.analiz_modul)
    try:
        aktar(t.baglan(x.db), m, x.analiz_db, x.pazar.upper() if x.pazar else None, x.tum, x.deneme)
    except o.VeriHatasi as e:
        o.hata_cik(str(e))
    except Exception as e:  # analiz DB kısıt hatası vb.
        print("ADAPTÖR HATASI: %r" % e)
        sys.exit(4)


if __name__ == "__main__":
    main()
