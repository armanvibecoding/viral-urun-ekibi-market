#!/usr/bin/env python3
"""Niş × pazar sorgu kuyruğu — kaldığı yerden devam, günlük tavan, engelde gün kilidi.

  python3 kuyruk.py uret  --db is/meta/reklam.db --pazar US,DE,TR [--nis evcil,mutfak] [--yol mcp|chrome|ikisi] [--hepsi]
        nisler.md'den kuyruk üretir (tekrar çalıştırmak güvenli; var olan satır değişmez). ELE nişi girmez.
        mcp: niş başına 1 sorgu (ilk ürün terimi). chrome: ilk 2 ürün + 1 kimlik terimi. --hepsi: tüm U+K terimleri.
        IT/NL'de yerel terim yoksa US İngilizce terimi `dil=EN-yedek` ile girer.
  python3 kuyruk.py al    --db ... --yol mcp [--tavan 150] [--bekle 20]
  python3 kuyruk.py al    --db ... --yol chrome --kok is/meta [--tavan 30]
        Sıradaki sorguyu AÇAR ve sayaca yazar; çıktısı JSON (mcp: çağrı parametreleri + kayıt dosyası yolu,
        chrome: Ad Library URL'si). chrome yolunda kota bekçisi `nis_kelime.py kaydet`tir (tek sayaç).
  python3 kuyruk.py engel --db ... --yol mcp --id 12 --sebep "rate limit mesajı"     # o gün o yol KİLİTLENİR
  python3 kuyruk.py hata  --db ... --yol mcp --id 12 --sebep "araç hata verdi"        # o gün o yol KİLİTLENİR
  python3 kuyruk.py durum --db ...

Çıkış kodları: 0 tamam · 1 yanlış girdi · 3 KİLİT/ENGEL — bugün bu yol durur · 4 günlük tavan doldu ·
5 çok hızlı (çıktıdaki sn kadar bekle) · 6 kuyrukta bekleyen sorgu yok.
Tavan ve bekleme yalnız DÜŞÜRÜLEBİLİR (varsayılanın üstü reddedilir); yükseltmek kurucu kararıdır.
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)
import ortak as o  # noqa: E402
import nis_kelime as nk  # noqa: E402
import toplayici_ortak as t  # noqa: E402

MCP_ARAC = "mcp__meta-official__ads_library_search"


def uret(c, pazarlar, nisler, yol, hepsi, sozluk):
    eklenen = 0
    yollar = ["mcp", "chrome"] if yol == "ikisi" else [yol]
    hedef_nisler = [n for n in sozluk if not n.startswith("_") and not sozluk[n]["ele"]]
    if nisler:
        for n in nisler:
            if n not in sozluk or n.startswith("_"):
                raise o.VeriHatasi("niş bilinmiyor: %s" % n)
            if sozluk[n]["ele"]:
                raise o.VeriHatasi("%s ELE KAPISI nişi: kuyruğa girmez" % n)
        hedef_nisler = nisler
    for p in pazarlar:
        if p not in t.PAZARLAR:
            raise o.VeriHatasi("pazar geçersiz: %s (%s)" % (p, ",".join(t.PAZARLAR)))
    oncelik = 0
    for nis in hedef_nisler:
        terim = sozluk[nis]["terim"]
        for p in pazarlar:
            us, ks, dil = terim.get((p, "U"), []), terim.get((p, "K"), []), "yerel"
            if not us:
                us, ks, dil = terim.get(("US", "U"), []), terim.get(("US", "K"), []), "EN-yedek"
            for y in yollar:
                if hepsi:
                    sec = [("U", x) for x in us] + [("K", x) for x in ks]
                elif y == "mcp":
                    sec = [("U", x) for x in us[:1]]
                else:
                    sec = [("U", x) for x in us[:2]] + [("K", x) for x in ks[:1]]
                for i, (aile, sorgu) in enumerate(sec):
                    cur = c.execute("INSERT OR IGNORE INTO kuyruk(pazar,nis,aile,sorgu,yol,dil,oncelik) VALUES (?,?,?,?,?,?,?)",
                                    (p, nis, aile, sorgu, y, dil, oncelik * 10 + i))
                    eklenen += cur.rowcount
        oncelik += 1
    c.commit()
    toplam = c.execute("SELECT COUNT(*) FROM kuyruk").fetchone()[0]
    print("kuyruk: %d yeni sorgu eklendi · toplam %d" % (eklenen, toplam))


def _sifirla_eski(c, yol, bugun):
    """Önceki günlerden kalan acik/engel → bekliyor; hata → deneme hakkı varsa bekliyor (ertesi gün)."""
    c.execute("UPDATE kuyruk SET durum='bekliyor' WHERE yol=? AND durum IN ('acik','engel') AND (son_tarih IS NULL OR son_tarih<?)",
              (yol, bugun))
    c.execute("UPDATE kuyruk SET durum='bekliyor' WHERE yol=? AND durum='hata' AND deneme<? AND son_tarih<?",
              (yol, t.HATA_DENEME, bugun))
    c.commit()


def al(c, yol, tavan, bekle, kok, nisler_yolu):
    bugun = t.bugun_str()
    if tavan > t.TAVAN[yol]:
        raise o.VeriHatasi("tavan %d > varsayılan %d: yükseltmek kurucu kararıdır (beceri metnine yazılır)" % (tavan, t.TAVAN[yol]))
    if bekle < t.BEKLE_SN[yol]:
        raise o.VeriHatasi("bekleme %d sn < en az %d sn: düşürülemez" % (bekle, t.BEKLE_SN[yol]))
    sebep = t.kilitli_mi(c, yol, bugun)
    if sebep:
        print("KİLİT — bugün %s yolu duruyor: %s. Yarın kaldığı yerden devam." % (yol, sebep))
        sys.exit(3)
    _sifirla_eski(c, yol, bugun)
    cagrilar = c.execute("SELECT zaman FROM cagri WHERE tarih=? AND yol=? ORDER BY zaman", (bugun, yol)).fetchall()
    if len(cagrilar) >= tavan:
        print("TAVAN: bugün %d/%d %s sorgusu yapıldı. Yarın devam." % (len(cagrilar), tavan, yol))
        sys.exit(4)
    if cagrilar:
        gecen = (t.simdi() - dt.datetime.fromisoformat(cagrilar[-1]["zaman"])).total_seconds()
        if gecen < bekle:
            print(json.dumps({"bekle_sn": int(bekle - gecen) + 1}))
            sys.exit(5)
    acik = c.execute("SELECT id FROM kuyruk WHERE yol=? AND durum='acik' AND son_tarih=?", (yol, bugun)).fetchone()
    if acik:
        raise o.VeriHatasi("açık sorgu var (id=%d): önce işle (`toplanan_isle.py`) ya da `engel`/`hata` yaz" % acik["id"])
    r = c.execute("SELECT * FROM kuyruk WHERE yol=? AND durum='bekliyor' ORDER BY deneme, oncelik, id LIMIT 1", (yol,)).fetchone()
    if not r:
        print("kuyruk boş: %s yolunda bekleyen sorgu yok (`uret` ile ekle)" % yol)
        sys.exit(6)
    if yol == "chrome":
        if not kok:
            raise o.VeriHatasi("chrome yolu --kok ister (kota bekçisi nis_kelime.py kaydet)")
        arg = [sys.executable, os.path.join(BURASI, "nis_kelime.py"), "--nisler", nisler_yolu, "kaydet", "--kok", kok,
               "--ulke", r["pazar"], "--aile", r["aile"], "--nis", r["nis"], "--sorgu", r["sorgu"], "--siralama", "yeni"]
        p = subprocess.run(arg, capture_output=True, text=True)
        if p.returncode != 0:
            print((p.stdout + p.stderr).strip())
            sys.exit(p.returncode)
    zaman = t.simdi().isoformat(timespec="seconds")
    c.execute("INSERT INTO cagri(tarih,zaman,yol,kuyruk_id) VALUES (?,?,?,?)", (bugun, zaman, yol, r["id"]))
    c.execute("UPDATE kuyruk SET durum='acik', son_tarih=? WHERE id=?", (bugun, r["id"]))
    c.commit()
    cikti = {"id": r["id"], "yol": yol, "pazar": r["pazar"], "nis": r["nis"], "aile": r["aile"], "sorgu": r["sorgu"],
             "dil": r["dil"], "sayac": "%d/%d" % (len(cagrilar) + 1, tavan)}
    if yol == "mcp":
        cikti["arac"] = MCP_ARAC
        cikti["parametre"] = {"countries": [r["pazar"]], "search_terms": r["sorgu"], "ad_active_status": "ACTIVE",
                              "ad_type": "ALL", "limit": 50}
        cikti["kaydet"] = "mcp/%s-%s-%d.json" % (bugun, r["pazar"], r["id"])
        cikti["sonra"] = "toplanan_isle.py mcp --db <db> --id %d <kaydet>" % r["id"]
    else:
        cikti["url"] = nk.meta_url(r["pazar"], r["sorgu"], r["aile"], "yeni")
        cikti["sonra"] = "meta_topla.js → meta_aktar.js → ham/ → toplanan_isle.py chrome --db <db> --id %d <ham>" % r["id"]
    print(json.dumps(cikti, ensure_ascii=False))


def isaretle(c, yol, kid, durum, sebep):
    r = c.execute("SELECT * FROM kuyruk WHERE id=?", (kid,)).fetchone()
    if not r:
        raise o.VeriHatasi("kuyrukta id=%d yok" % kid)
    if r["yol"] != yol:
        raise o.VeriHatasi("id=%d %s yoluna ait, %s değil" % (kid, r["yol"], yol))
    c.execute("UPDATE kuyruk SET durum=?, deneme=deneme+?, son_tarih=?, notlar=? WHERE id=?",
              (durum, 1 if durum == "hata" else 0, t.bugun_str(), sebep[:300], kid))
    t.kilitle(c, yol, "%s (id=%d): %s" % (durum.upper(), kid, sebep))
    print("%s yazıldı (id=%d) — bugün %s yolu KİLİTLİ, yarın kaldığı yerden." % (durum.upper(), kid, yol))
    sys.exit(3)


def durum(c):
    bugun = t.bugun_str()
    print("# %s" % bugun)
    for y in t.YOLLAR:
        n = c.execute("SELECT COUNT(*) FROM cagri WHERE tarih=? AND yol=?", (bugun, y)).fetchone()[0]
        k = t.kilitli_mi(c, y, bugun)
        print("%-6s bugün %d/%d çağrı · %s" % (y, n, t.TAVAN[y], ("KİLİTLİ: " + k) if k else "açık"))
    print("\npazar\tyol\tbekliyor\tacik\ttamam\tengel\thata")
    for r in c.execute("""SELECT pazar, yol, SUM(durum='bekliyor') b, SUM(durum='acik') a, SUM(durum='tamam') t,
                          SUM(durum='engel') e, SUM(durum='hata') h FROM kuyruk GROUP BY pazar, yol ORDER BY pazar, yol"""):
        print("\t".join(str(x) for x in r))
    n = c.execute("SELECT COUNT(*) FROM reklam").fetchone()[0]
    print("\nreklam (tekil): %d" % n)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nisler", default=nk.VARSAYILAN_NISLER)
    alt = ap.add_subparsers(dest="komut")
    u = alt.add_parser("uret")
    u.add_argument("--db", required=True)
    u.add_argument("--pazar", required=True)
    u.add_argument("--nis", default="")
    u.add_argument("--yol", default="mcp", choices=["mcp", "chrome", "ikisi"])
    u.add_argument("--hepsi", action="store_true")
    a = alt.add_parser("al")
    a.add_argument("--db", required=True)
    a.add_argument("--yol", required=True, choices=t.YOLLAR)
    a.add_argument("--tavan", type=int)
    a.add_argument("--bekle", type=int)
    a.add_argument("--kok")
    for ad in ("engel", "hata"):
        e = alt.add_parser(ad)
        e.add_argument("--db", required=True)
        e.add_argument("--yol", required=True, choices=t.YOLLAR)
        e.add_argument("--id", type=int, required=True)
        e.add_argument("--sebep", required=True)
    d = alt.add_parser("durum")
    d.add_argument("--db", required=True)
    x = ap.parse_args()
    if not x.komut:
        ap.print_help()
        sys.exit(1)
    try:
        c = t.baglan(x.db)
        if x.komut == "uret":
            sozluk = nk.nisler_oku(x.nisler)
            uret(c, [p.strip().upper() for p in x.pazar.split(",") if p.strip()],
                 [n.strip() for n in x.nis.split(",") if n.strip()], x.yol, x.hepsi, sozluk)
        elif x.komut == "al":
            al(c, x.yol, x.tavan if x.tavan is not None else t.TAVAN[x.yol],
               x.bekle if x.bekle is not None else t.BEKLE_SN[x.yol], x.kok, x.nisler)
        elif x.komut in ("engel", "hata"):
            isaretle(c, x.yol, x.id, x.komut, x.sebep)
        else:
            durum(c)
    except o.VeriHatasi as e:
        o.hata_cik(str(e))


if __name__ == "__main__":
    main()
