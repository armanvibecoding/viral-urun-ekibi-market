#!/usr/bin/env python3
"""MCP JSON'unu ve Chrome dökümünü ortak reklam kaydına çevirir; reklam id ile tekilleştirir.

  python3 toplanan_isle.py mcp    --db is/meta/reklam.db --id 12 is/meta/mcp/<dosya>.json
        `kuyruk.py al --yol mcp` ile AÇILMIŞ sorgunun sonucunu işler. Kabul edilen biçimler:
        aracın ham çıktısı {"results": "<json metni>", ...} ya da iç nesne {"estimated_total_count": N, "ads": [...]}.
  python3 toplanan_isle.py chrome --db ... [--id 7] is/meta/ham/<dosya>-1.txt [...-2.txt]
        meta_aktar.js dökümü (#REKLAMAVI v1). Hedef link → alan adı buradan gelir (MCP alan adı VERMEZ).
  python3 toplanan_isle.py ozet   --db ... [--pazar US] [--ilk 30]
        sayfa başına reklam sayısı, en uzun aktif gün, alan adı; aynı başlığın kaç sayfada geçtiği.

Kapılar (çıkış kodu):
  1 — dosya yok / JSON bozuk / şema dışı (ads listesi yok, id sayı değil) / sorgu kuyrukta açık değil (kota dışı).
      Bozuk dosyada kuyruk satırı 'hata' olur ve o gün mcp yolu KİLİTLENİR.
  3 — yanıtta hata/engel izi (error alanı, rate limit, "too many", "temporarily blocked", "try again later"):
      kuyruk 'engel', o gün yol KİLİTLİ. Atlatma, tekrar deneme yok.
"""
import argparse
import collections
import json
import os
import re
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)
import ortak as o  # noqa: E402
import nis_kelime as nk  # noqa: E402
import meta_kayit as mk  # noqa: E402
import toplayici_ortak as t  # noqa: E402

ENGEL_IZI = re.compile(r"rate.?limit|too many|temporarily blocked|try again later|request limit|limit reached|"
                       r"throttl|blocked|checkpoint|captcha|#4\b|#17\b|#613\b|code\W+(4|17|32|613)\b", re.I)


class Engel(Exception):
    pass


def mcp_coz(metin):
    """Ham metin → (tahmini_toplam, ads). Bozuksa VeriHatasi, engel iziyse Engel."""
    try:
        d = json.loads(metin)
    except ValueError as e:
        raise o.VeriHatasi("JSON bozuk: %s" % e)
    if isinstance(d, dict) and "results" in d and isinstance(d["results"], str):
        if ENGEL_IZI.search(d["results"]) and not d["results"].lstrip().startswith("{"):
            raise Engel(d["results"][:200])
        try:
            d = json.loads(d["results"])
        except ValueError as e:
            raise o.VeriHatasi("results alanı JSON değil: %s" % e)
    if not isinstance(d, dict):
        raise o.VeriHatasi("beklenen nesne, gelen %s" % type(d).__name__)
    if "error" in d or "errors" in d:
        raise Engel(json.dumps(d.get("error") or d.get("errors"), ensure_ascii=False)[:200])
    if "ads" not in d or not isinstance(d["ads"], list):
        metin_k = json.dumps(d, ensure_ascii=False)[:200]
        if ENGEL_IZI.search(metin_k):
            raise Engel(metin_k)
        raise o.VeriHatasi("'ads' listesi yok (anahtarlar: %s)" % ",".join(sorted(d)))
    toplam = d.get("estimated_total_count")
    if toplam is not None and not isinstance(toplam, int):
        raise o.VeriHatasi("estimated_total_count sayı değil: %r" % toplam)
    ads = []
    for i, a in enumerate(d["ads"], start=1):
        if not isinstance(a, dict) or not re.fullmatch(r"\d+", str(a.get("id", ""))):
            raise o.VeriHatasi("reklam %d: id yok ya da sayı değil" % i)
        ads.append(a)
    return toplam, ads


def _yaz(c, r):
    """Tekil yaz: aynı ad_id ikinci kez gelirse yalnız okuma_tarihi ve boş alanlar tazelenir."""
    c.execute("""INSERT INTO reklam(ad_id,page_id,page_name,pazar,nis,sorgu,baslik,govde,olusturma,yayin_tarihi,
                 snapshot_url,hedef_alan,hedef_yol,kopya,kaynak,kuyruk_id,ilk_gorulme,okuma_tarihi)
                 VALUES (:ad_id,:page_id,:page_name,:pazar,:nis,:sorgu,:baslik,:govde,:olusturma,:yayin_tarihi,
                 :snapshot_url,:hedef_alan,:hedef_yol,:kopya,:kaynak,:kuyruk_id,:okuma_tarihi,:okuma_tarihi)
                 ON CONFLICT(ad_id) DO UPDATE SET okuma_tarihi=excluded.okuma_tarihi,
                   page_id=COALESCE(reklam.page_id, excluded.page_id),
                   hedef_alan=COALESCE(NULLIF(reklam.hedef_alan,''), excluded.hedef_alan),
                   hedef_yol=COALESCE(NULLIF(reklam.hedef_yol,''), excluded.hedef_yol),
                   kopya=COALESCE(excluded.kopya, reklam.kopya),
                   govde=COALESCE(NULLIF(reklam.govde,''), excluded.govde),
                   yayin_tarihi=COALESCE(reklam.yayin_tarihi, excluded.yayin_tarihi)""", r)


def isle_mcp(c, kid, yol):
    q = c.execute("SELECT * FROM kuyruk WHERE id=?", (kid,)).fetchone()
    if not q:
        raise o.VeriHatasi("kuyrukta id=%d yok" % kid)
    if q["yol"] != "mcp" or q["durum"] != "acik" or q["son_tarih"] != t.bugun_str():
        raise o.VeriHatasi("id=%d bugün açılmış bir mcp sorgusu değil (durum=%s) — kayıtsız çağrı kabul edilmez" % (kid, q["durum"]))
    try:
        if not os.path.exists(yol):
            raise o.VeriHatasi("dosya yok: %s" % yol)
        with open(yol, encoding="utf-8") as f:
            toplam, ads = mcp_coz(f.read())
    except Engel as e:
        c.execute("UPDATE kuyruk SET durum='engel', notlar=? WHERE id=?", (str(e), kid))
        t.kilitle(c, "mcp", "ENGEL (id=%d): %s" % (kid, e))
        print("ENGEL — yanıtta hata/sınır izi: %s\nBugün mcp yolu KİLİTLİ; yarın kaldığı yerden." % e)
        sys.exit(3)
    except o.VeriHatasi as e:
        c.execute("UPDATE kuyruk SET durum='hata', deneme=deneme+1, notlar=? WHERE id=?", (str(e)[:300], kid))
        t.kilitle(c, "mcp", "HATA (id=%d): %s" % (kid, e))
        raise
    okuma = t.bugun_str()
    yeni = 0
    for a in ads:
        once = c.execute("SELECT 1 FROM reklam WHERE ad_id=?", (str(a["id"]),)).fetchone()
        _yaz(c, {"ad_id": str(a["id"]), "page_id": str(a.get("page_id") or "") or None,
                 "page_name": a.get("page_name") or None, "pazar": q["pazar"], "nis": q["nis"], "sorgu": q["sorgu"],
                 "baslik": a.get("ad_creative_link_title") or None, "govde": None,
                 "olusturma": t.epoch_tarih(a.get("ad_creation_time")),
                 "yayin_tarihi": t.epoch_tarih(a.get("ad_delivery_start_time")),
                 "snapshot_url": a.get("ad_snapshot_url") or None, "hedef_alan": None, "hedef_yol": None,
                 "kopya": None, "kaynak": "mcp", "kuyruk_id": kid, "okuma_tarihi": okuma})
        yeni += 0 if once else 1
    c.execute("UPDATE kuyruk SET durum='tamam', tahmini_toplam=?, gelen=?, dosya=? WHERE id=?", (toplam, len(ads), yol, kid))
    c.commit()
    print("mcp id=%d %s/%s: %d reklam (%d yeni) · tahmini toplam %s" % (kid, q["pazar"], q["sorgu"], len(ads), yeni,
                                                                       toplam if toplam is not None else "görünmüyor"))


def isle_chrome(c, kid, yollar, nisler_yolu):
    meta, kartlar = mk.ham_oku(yollar)
    if kid is not None:
        q = c.execute("SELECT * FROM kuyruk WHERE id=?", (kid,)).fetchone()
        if not q or q["yol"] != "chrome" or q["durum"] != "acik":
            raise o.VeriHatasi("id=%s açık bir chrome sorgusu değil" % kid)
        if q["pazar"] != meta["ulke"] or q["sorgu"] != meta["sorgu"]:
            raise o.VeriHatasi("döküm başlığı (%s/%s) kuyruk satırıyla (%s/%s) tutmuyor" % (meta["ulke"], meta["sorgu"], q["pazar"], q["sorgu"]))
    sozluk = nk.nisler_oku(nisler_yolu)
    okuma = t.bugun_str()
    yeni = 0
    for k in kartlar:
        s = mk.kart_satiri(k, meta, okuma, sozluk)
        once = c.execute("SELECT 1 FROM reklam WHERE ad_id=?", (s["kutuphane_kodu"],)).fetchone()
        _yaz(c, {"ad_id": s["kutuphane_kodu"], "page_id": None,
                 "page_name": None if s["sayfa_adi"] == o.GORUNMUYOR else s["sayfa_adi"],
                 "pazar": meta["ulke"], "nis": s["nis"], "sorgu": meta["sorgu"],
                 "baslik": None, "govde": None if s["govde_ilk200"] == o.GORUNMUYOR else s["govde_ilk200"],
                 "olusturma": None, "yayin_tarihi": None if s["ilk_yayin"] == o.GORUNMUYOR else s["ilk_yayin"],
                 "snapshot_url": "https://www.facebook.com/ads/library/?id=" + s["kutuphane_kodu"],
                 "hedef_alan": s["hedef_alan"] or None, "hedef_yol": s["hedef_yol"] or None,
                 "kopya": int(s["kopya"]) if o.sayi_mi(s["kopya"]) else None,
                 "kaynak": "chrome", "kuyruk_id": kid, "okuma_tarihi": okuma})
        yeni += 0 if once else 1
    if kid is not None:
        c.execute("UPDATE kuyruk SET durum='tamam', gelen=?, dosya=? WHERE id=?", (len(kartlar), ",".join(yollar), kid))
    c.commit()
    print("chrome %s/%s: %d kart (%d yeni)" % (meta["ulke"], meta["sorgu"], len(kartlar), yeni))


def birim(r):
    """Sayfa kimliği: MCP page_id; Chrome'da page_id yok → 'sayfa:<ad>'."""
    if r["page_id"]:
        return r["page_id"]
    return "sayfa:" + o.norm(r["page_name"] or "?")


def sayfa_ozeti(c, pazar=None):
    """{(pazar, birim): {...}} — basari_puani.py da bunu kullanır."""
    bugun = t.bugun_str()
    sql = "SELECT * FROM reklam" + (" WHERE pazar=?" if pazar else "")
    rs = c.execute(sql, (pazar,) if pazar else ()).fetchall()
    alan_eslem = {r["page_id"]: r["alan"] for r in c.execute("SELECT page_id, alan FROM sayfa_alan")}
    toplamlar = {r["id"]: r["tahmini_toplam"] for r in c.execute("SELECT id, tahmini_toplam FROM kuyruk")}
    baslik_sayfa = collections.defaultdict(set)
    for r in rs:
        bn = t.baslik_norm(r["baslik"] or r["govde"] or "")
        if len(bn) >= 8:
            baslik_sayfa[(r["pazar"], bn)].add(birim(r))
    oz = {}
    for r in rs:
        b = birim(r)
        x = oz.setdefault((r["pazar"], b), {"pazar": r["pazar"], "birim": b, "page_name": r["page_name"], "reklam": 0,
                                            "max_gun": None, "max_kopya": None, "alanlar": collections.Counter(),
                                            "nisler": collections.Counter(), "baslik_yayilim": 1, "nis_toplam": None,
                                            "snapshot": r["snapshot_url"]})
        x["reklam"] += 1
        if r["yayin_tarihi"]:
            g = o.gun_farki(bugun, r["yayin_tarihi"])
            x["max_gun"] = g if x["max_gun"] is None else max(x["max_gun"], g)
        if r["kopya"]:
            x["max_kopya"] = max(x["max_kopya"] or 0, r["kopya"])
        alan = r["hedef_alan"] or alan_eslem.get(r["page_id"] or "")
        if alan:
            x["alanlar"][alan] += 1
        if r["nis"]:
            x["nisler"][r["nis"]] += 1
        bn = t.baslik_norm(r["baslik"] or r["govde"] or "")
        if len(bn) >= 8:
            x["baslik_yayilim"] = max(x["baslik_yayilim"], len(baslik_sayfa[(r["pazar"], bn)]))
        tt = toplamlar.get(r["kuyruk_id"])
        if tt is not None:
            x["nis_toplam"] = max(x["nis_toplam"] or 0, tt)
    for x in oz.values():
        x["alan"] = x["alanlar"].most_common(1)[0][0] if x["alanlar"] else None
        x["nis"] = x["nisler"].most_common(1)[0][0] if x["nisler"] else None
    return oz


def ozet(c, pazar, ilk):
    oz = sayfa_ozeti(c, pazar)
    sirali = sorted(oz.values(), key=lambda x: (-x["reklam"], -(x["max_gun"] or 0)))
    print("pazar\tbirim\tsayfa\treklam\tmax_aktif_gun\tmax_kopya\tbaslik_kac_sayfada\talan")
    for x in sirali[:ilk]:
        print("\t".join(str(v if v is not None else o.GORUNMUYOR) for v in (
            x["pazar"], x["birim"], x["page_name"], x["reklam"], x["max_gun"], x["max_kopya"], x["baslik_yayilim"], x["alan"])))
    print("# %d sayfa · %d reklam" % (len(oz), sum(x["reklam"] for x in oz.values())))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nisler", default=nk.VARSAYILAN_NISLER)
    alt = ap.add_subparsers(dest="komut")
    m = alt.add_parser("mcp")
    m.add_argument("--db", required=True)
    m.add_argument("--id", type=int, required=True)
    m.add_argument("dosya")
    ch = alt.add_parser("chrome")
    ch.add_argument("--db", required=True)
    ch.add_argument("--id", type=int)
    ch.add_argument("dosyalar", nargs="+")
    z = alt.add_parser("ozet")
    z.add_argument("--db", required=True)
    z.add_argument("--pazar")
    z.add_argument("--ilk", type=int, default=30)
    x = ap.parse_args()
    if not x.komut:
        ap.print_help()
        sys.exit(1)
    try:
        c = t.baglan(x.db)
        if x.komut == "mcp":
            isle_mcp(c, x.id, x.dosya)
        elif x.komut == "chrome":
            isle_chrome(c, x.id, x.dosyalar, x.nisler)
        else:
            ozet(c, x.pazar, x.ilk)
    except o.VeriHatasi as e:
        o.hata_cik(str(e))


if __name__ == "__main__":
    main()
