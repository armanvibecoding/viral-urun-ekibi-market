#!/usr/bin/env python3
"""7 gunluk talep ivmesi: ayni urunun t0 ve t7 sinyalleri -> ERKEN DALGA / BOS / DOYMUS bandi.

Kullanim:
  ivme_olc.py bant     IVME.csv [--esikler ESIK.tsv]
  ivme_olc.py bekleyen IVME.csv [--bugun YYYY-AA-GG]     (t7 olcum gunu gelmis urunleri listeler)

Sutunlar (sablon/ivme.csv): urun, pazar, olcum (t0|t7), tarih, reklam_sayisi, yorum_sayisi, bsr,
  trendyol_degerlendirme, tiktok_satilan, yeni_magaza, perakende_satici, akraba_kanit (E|H), kaynak_notu
reklam_sayisi zorunlu (Meta Reklam Kutuphanesi, hedef pazar, aktif). Diger sinyaller bos olabilir = olculmedi.
Esikler kodda degil: referans/ivme-esikleri.tsv (oneri, olculmedi).

Bant kurali (t7 degerleriyle):
  DOYMUS      perakende_satici >= doymus_satici_min  veya  reklam_sayisi >= doymus_reklam_min
  BOS         reklam_sayisi = 0 ve olculen diger talep sinyallerinin hepsi 0 (yorum, trendyol, tiktok, yeni_magaza)
  ERKEN DALGA akraba_kanit = E ve erken_reklam_min <= reklam_sayisi <= erken_reklam_max ve en az bir sinyalde artis
              (reklam/yorum/trendyol/tiktok/yeni_magaza artar ya da BSR sayisi duser)
  BELIRSIZ    hicbiri (gerekce yazilir)
P3: artis 2 · sabit 1 · dusus ya da olculemedi 0.  P4: DOYMUS 0 · BOS/BELIRSIZ 1 · ERKEN DALGA 2.
Cikis: 0 = tamam, 1 = veri hatasi, 2 = kullanim hatasi.
"""
import csv
import datetime as dt
import os
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
ESIK_DOSYASI = os.path.join(BURADA, "..", "referans", "ivme-esikleri.tsv")
PAZARLAR = {"US", "TR", "UK", "DE", "FR", "ES"}
SUTUNLAR = ["urun", "pazar", "olcum", "tarih", "reklam_sayisi", "yorum_sayisi", "bsr", "trendyol_degerlendirme",
            "tiktok_satilan", "yeni_magaza", "perakende_satici", "akraba_kanit", "kaynak_notu"]
ARTAN = ["reklam_sayisi", "yorum_sayisi", "trendyol_degerlendirme", "tiktok_satilan", "yeni_magaza"]
TALEP = ["yorum_sayisi", "trendyol_degerlendirme", "tiktok_satilan", "yeni_magaza"]
SAYISAL = ARTAN + ["bsr", "perakende_satici"]


def esik_oku(yol):
    e = {}
    with open(yol, encoding="utf-8", newline="") as f:
        for s in csv.DictReader(f, delimiter="\t"):
            e[s["anahtar"].strip()] = int(s["deger"].strip())
    gerekli = {"min_gun", "max_gun", "erken_reklam_min", "erken_reklam_max", "doymus_reklam_min", "doymus_satici_min"}
    if not gerekli.issubset(e):
        raise ValueError(f"{yol}: eksik esik: {', '.join(sorted(gerekli - set(e)))}")
    return e


def oku(yol):
    hatalar = []
    with open(yol, encoding="utf-8-sig", newline="") as f:
        ornek = f.read(2048)
        f.seek(0)
        ayrac = "\t" if ornek.count("\t") > ornek.count(",") else ","
        r = csv.DictReader(f, delimiter=ayrac)
        eksik = [c for c in SUTUNLAR if c not in (r.fieldnames or [])]
        if eksik:
            return None, [f"eksik sutun: {', '.join(eksik)} (sablon/ivme.csv basligini kullan)"]
        kayit = {}
        for i, s in enumerate(r, 2):
            et = f"satir {i}"
            urun = (s["urun"] or "").strip()
            pazar = (s["pazar"] or "").strip().upper()
            olcum = (s["olcum"] or "").strip().lower()
            if not urun:
                hatalar.append(f"{et}: urun bos")
                continue
            if pazar not in PAZARLAR:
                hatalar.append(f"{et}: bilinmeyen pazar '{s['pazar']}'")
                continue
            if olcum not in ("t0", "t7"):
                hatalar.append(f"{et}: olcum t0 ya da t7 olmali ('{s['olcum']}')")
                continue
            try:
                tarih = dt.date.fromisoformat((s["tarih"] or "").strip())
            except ValueError:
                hatalar.append(f"{et}: tarih YYYY-AA-GG olmali ('{s['tarih']}')")
                continue
            d = {"_satir": i, "tarih": tarih, "akraba": (s["akraba_kanit"] or "").strip().upper()}
            if d["akraba"] not in ("E", "H"):
                hatalar.append(f"{et}: akraba_kanit E ya da H olmali")
                continue
            bozuk = False
            for a in SAYISAL:
                m = (s[a] or "").strip().replace(".", "").replace(",", "")
                if m == "":
                    d[a] = None
                    continue
                if not m.isdigit():
                    hatalar.append(f"{et}: {a} tam sayi degil ('{s[a]}'); olculmediyse bos birak")
                    bozuk = True
                    continue
                d[a] = int(m)
            if bozuk:
                continue
            if d["reklam_sayisi"] is None:
                hatalar.append(f"{et}: reklam_sayisi zorunlu (Meta Reklam Kutuphanesi, aktif, hedef pazar)")
                continue
            anahtar = (urun.lower(), pazar)
            kayit.setdefault(anahtar, {"urun": urun, "pazar": pazar})
            if olcum in kayit[anahtar]:
                hatalar.append(f"{et}: {urun}/{pazar} icin ikinci {olcum} satiri (ilki satir {kayit[anahtar][olcum]['_satir']})")
                continue
            kayit[anahtar][olcum] = d
    return kayit, hatalar


def bant_hesapla(u, e):
    t0, t7 = u["t0"], u["t7"]
    artis, dusus = [], []
    for a in ARTAN:
        if t0[a] is not None and t7[a] is not None:
            if t7[a] > t0[a]:
                artis.append(a)
            elif t7[a] < t0[a]:
                dusus.append(a)
    if t0["bsr"] is not None and t7["bsr"] is not None:
        if t7["bsr"] < t0["bsr"]:
            artis.append("bsr(iyilesti)")
        elif t7["bsr"] > t0["bsr"]:
            dusus.append("bsr(kotulesti)")
    reklam = t7["reklam_sayisi"]
    satici = t7["perakende_satici"]
    if (satici is not None and satici >= e["doymus_satici_min"]) or reklam >= e["doymus_reklam_min"]:
        bant, neden = "DOYMUS", f"reklam {reklam}, perakende satici {satici if satici is not None else '-'}"
    elif reklam == 0 and all((t7[a] or 0) == 0 for a in TALEP):
        bant, neden = "BOS", "hedef pazarda reklam ve talep sinyali yok; yalniz akraba kaniti cok gucluyse IZLE"
    elif t7["akraba"] == "E" and e["erken_reklam_min"] <= reklam <= e["erken_reklam_max"] and artis:
        bant, neden = "ERKEN DALGA", f"reklam {reklam}, artis: {', '.join(artis)}"
    else:
        eksik = []
        if t7["akraba"] != "E":
            eksik.append("akraba kaniti yok")
        if not artis:
            eksik.append("7 gunde artis yok")
        if not (e["erken_reklam_min"] <= reklam <= e["erken_reklam_max"]):
            eksik.append(f"reklam {reklam} erken araliginda degil ({e['erken_reklam_min']}-{e['erken_reklam_max']})")
        bant, neden = "BELIRSIZ", "; ".join(eksik) or "-"
    p3 = 2 if artis else (0 if dusus or not any(t0[a] is not None and t7[a] is not None for a in SAYISAL) else 1)
    p4 = {"DOYMUS": 0, "ERKEN DALGA": 2}.get(bant, 1)
    return bant, neden, p3, p4


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if len(argv) < 3 or argv[1] not in ("bant", "bekleyen"):
        print(__doc__)
        return 2
    komut, yol = argv[1], argv[2]
    if not os.path.isfile(yol):
        print(f"HATA: dosya yok: {yol}")
        return 1
    try:
        e = esik_oku(argv[argv.index("--esikler") + 1] if "--esikler" in argv else ESIK_DOSYASI)
    except (OSError, ValueError, KeyError) as x:
        print(f"HATA: esik dosyasi: {x}")
        return 1
    kayit, hatalar = oku(yol)
    if kayit is None:
        print(f"HATA: {hatalar[0]}")
        return 1
    if not kayit and not hatalar:
        print("HATA: veri satiri yok")
        return 1

    if komut == "bekleyen":
        bugun = dt.date.fromisoformat(argv[argv.index("--bugun") + 1]) if "--bugun" in argv else dt.date.today()
        n = 0
        for u in kayit.values():
            if "t0" in u and "t7" not in u:
                gun = u["t0"]["tarih"] + dt.timedelta(days=e["min_gun"])
                if gun <= bugun:
                    print(f"OLCUM GUNU: {u['urun']} ({u['pazar']}) — t0 {u['t0']['tarih']}, t7 en erken {gun}")
                    n += 1
        print(f"TOPLAM: {n} urun t7 olcumu bekliyor")
        for h in hatalar:
            print(f"HATA {h}")
        return 1 if hatalar else 0

    for u in kayit.values():
        if "t7" in u and "t0" not in u:
            hatalar.append(f"{u['urun']} ({u['pazar']}): t7 var, t0 yok")
            continue
        if "t7" not in u:
            print(f"{u['urun']} | {u['pazar']} | OLCUM BEKLIYOR (yalniz t0: {u['t0']['tarih']})")
            continue
        fark = (u["t7"]["tarih"] - u["t0"]["tarih"]).days
        if not (e["min_gun"] <= fark <= e["max_gun"]):
            hatalar.append(f"{u['urun']} ({u['pazar']}): t0-t7 arasi {fark} gun ({e['min_gun']}-{e['max_gun']} olmali)")
            continue
        bant, neden, p3, p4 = bant_hesapla(u, e)
        print(f"{u['urun']} | {u['pazar']} | {fark} gun | BANT: {bant} | {neden} | P3={p3} P4={p4}")
    for h in hatalar:
        print(f"HATA {h}")
    print(f"TOPLAM: {len(kayit)} urun, {len(hatalar)} hata (esikler oneri, olculmedi)")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
