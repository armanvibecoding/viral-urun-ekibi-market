#!/usr/bin/env python3
"""Yayın sonrası öğrenme döngüsü: 48. saat ölçümü -> video başına DEVAM / BEKLE / ÖLDÜR + kanca/giriş ortalaması.

Veri kurucudan gelir (Instagram/TikTok içgörüleri). Betik sayı uydurmaz, boş hücreyi "veri yok" sayar.
dersler.md'ye YAZMAZ: eklenecek 3-5 satırlık öneriyi ekrana basar; lider/kurucu onaylayıp ekler.

Girdi:
  olcum.csv  sütunlar: video,platform,saat,izlenme,ort_izlenme_sn,tutma_yuzde,begeni,yorum,cta_yorum,paylasim,kaydetme
             (şablon: ../sablon/olcum.csv; yalnız saat=48 satırları kullanılır, saat boşsa 48 sayılır)
  --plan PLAN.md  (şablon: ../sablon/yayin-PLAN.md) -> kanca ailesi, giriş türü, CTA kelimesi; eksik ölçüm sayımı

Eşikler (kaynak: ai-video-kiti/olcum-ve-test-plani.md §3, 48. saat; milyon görmüş videoların dağılımından):
  izlenme < 2000                        -> BEKLE (veri yok; 7. günde yeniden bak, öldürülmez)
  DEVAM : pay/iz >= %0,61 ve beğ/iz >= %1,01, ya da izlenme >= 4,7 × aynı platformdaki diğer videoların medyanı
          (pay/iz >= %1,07 ise "GÜÇLÜ" etiketi)
  ÖLDÜR : pay/iz < %0,21 ve beğ/iz < %0,75
  BEKLE : diğer her durum
  Tutma: partinin tutma medyanının altında kalıp paylaşım eşiğini de geçemeyen kanca/ilk kare sonraki partiye alınmaz.
  Parti: >= 10 ölçülmüş videonun hiçbiri DEVAM değilse -> görüntüyü değiştir (şablon/ilk kare), kancayı değil.
Çıkış 0 = rapor basıldı · 2 = girdi okunamadı.
Kullanım: python3 yayin_olc.py yayin/olcum.csv --plan yayin/PLAN.md
"""
import argparse
import csv
import statistics
import sys

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

MIN_IZ = 2000
PAY_DEVAM, BEG_DEVAM, PAY_GUCLU = 0.0061, 0.0101, 0.0107
PAY_OLDUR, BEG_OLDUR = 0.0021, 0.0075
KAT_DEVAM = 4.7


def sayi(x):
    """Sayı hücresi; '12400', '42,5' (Türkçe ondalık) ve '%42' kabul edilir. Binlik ayırıcı yazmayın."""
    x = (x or "").strip().replace("%", "").replace(" ", "")
    if "," in x:
        x = x.replace(".", "").replace(",", ".")
    try:
        return float(x)
    except ValueError:
        return None


def vno(x):
    x = (x or "").strip()
    return x.zfill(2) if x.isdigit() else x


def plan_oku(yol):
    plan = {}
    basliklar = None
    for satir in open(yol, encoding="utf-8"):
        if not satir.strip().startswith("|"):
            continue
        h = [c.strip() for c in satir.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in h):
            continue
        if basliklar is None:
            basliklar = [c.lower() for c in h]
            continue
        r = dict(zip(basliklar, h))
        anahtar = (vno(r.get("video")), (r.get("platform") or "").lower())
        plan[anahtar] = {"kanca": r.get("kanca ailesi") or "?", "giris": r.get("giriş türü") or "?",
                         "cta": r.get("cta kelimesi") or ""}
    return plan


def yuzde(x):
    return "—" if x is None else f"%{x * 100:.2f}"


def main():
    ap = argparse.ArgumentParser(description="48. saat yayın ölçümü kararı")
    ap.add_argument("olcum")
    ap.add_argument("--plan")
    a = ap.parse_args()
    try:
        satirlar = list(csv.DictReader(open(a.olcum, encoding="utf-8-sig")))
        plan = plan_oku(a.plan) if a.plan else {}
    except Exception as e:
        print(f"Girdi okunamadı: {e}")
        return 2

    vids = []
    for r in satirlar:
        saat = sayi(r.get("saat"))
        if saat is not None and saat != 48:
            continue
        iz = sayi(r.get("izlenme"))
        if iz is None:
            continue
        p = plan.get((vno(r["video"]), (r.get("platform") or "").lower()), {})
        v = {"video": vno(r["video"]), "platform": (r.get("platform") or "").lower(), "iz": iz,
             "beg": sayi(r.get("begeni")), "pay": sayi(r.get("paylasim")), "tutma": sayi(r.get("tutma_yuzde")),
             "cta": sayi(r.get("cta_yorum")), "kay": sayi(r.get("kaydetme")),
             "kanca": p.get("kanca", "?"), "giris": p.get("giris", "?")}
        v["pay_iz"] = v["pay"] / iz if v["pay"] is not None and iz else None
        v["beg_iz"] = v["beg"] / iz if v["beg"] is not None and iz else None
        vids.append(v)
    if not vids:
        print("48. saat ölçümü yok: olcum.csv'ye kurucu veri girmeli (uydurma veri kullanılmaz).")
        return 0

    tut_med = statistics.median([v["tutma"] for v in vids if v["tutma"] is not None] or [0]) or None
    for v in vids:
        digerleri = [w["iz"] for w in vids if w is not v and w["platform"] == v["platform"]]
        v["kat"] = v["iz"] / statistics.median(digerleri) if digerleri and statistics.median(digerleri) else None
        if v["iz"] < MIN_IZ:
            v["karar"], v["neden"] = "BEKLE", f"izlenme < {MIN_IZ} (veri yok, 7. gün)"
        elif v["pay_iz"] is None or v["beg_iz"] is None:
            v["karar"], v["neden"] = "BEKLE", "beğeni/paylaşım boş"
        elif (v["pay_iz"] >= PAY_DEVAM and v["beg_iz"] >= BEG_DEVAM) or (v["kat"] and v["kat"] >= KAT_DEVAM):
            v["karar"] = "DEVAM"
            v["neden"] = ("GÜÇLÜ, " if v["pay_iz"] >= PAY_GUCLU else "") + (
                "pay+beğ eşik" if v["pay_iz"] >= PAY_DEVAM and v["beg_iz"] >= BEG_DEVAM else f"izlenme {v['kat']:.1f}× medyan")
        elif v["pay_iz"] < PAY_OLDUR and v["beg_iz"] < BEG_OLDUR:
            v["karar"], v["neden"] = "ÖLDÜR", "pay ve beğeni P10 altında"
        else:
            v["karar"], v["neden"] = "BEKLE", "yalnız biri geçiyor"
        v["tutma_ele"] = (tut_med is not None and v["tutma"] is not None and v["tutma"] < tut_med
                          and (v["pay_iz"] is None or v["pay_iz"] < PAY_DEVAM))

    print(f"48. saat kararı — {len(vids)} video (eşik: ≥{MIN_IZ} izlenme; DEVAM pay/iz ≥%0,61 ve beğ/iz ≥%1,01 "
          f"ya da ≥4,7× medyan; ÖLDÜR pay/iz <%0,21 ve beğ/iz <%0,75)\n")
    print("| Video | Platform | Kanca | Giriş | İzlenme | pay/iz | beğ/iz | Tutma | CTA yorum | Karar | Neden |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for v in sorted(vids, key=lambda v: (v["video"], v["platform"])):
        tut = "—" if v["tutma"] is None else f"%{v['tutma']:.0f}" + (" ↓" if v["tutma_ele"] else "")
        print(f"| {v['video']} | {v['platform']} | {v['kanca']} | {v['giris']} | {v['iz']:.0f} | {yuzde(v['pay_iz'])} | "
              f"{yuzde(v['beg_iz'])} | {tut} | {'—' if v['cta'] is None else int(v['cta'])} | {v['karar']} | {v['neden']} |")

    def grupla(alan):
        g = {}
        for v in vids:
            g.setdefault(v[alan], []).append(v)
        out = []
        for k, vs in g.items():
            olc = [v for v in vs if v["iz"] >= MIN_IZ and v["pay_iz"] is not None and v["beg_iz"] is not None]
            out.append({"k": k, "n": len(vs), "n_olc": len(olc),
                        "iz": statistics.mean(v["iz"] for v in vs),
                        "pay": statistics.mean(v["pay_iz"] for v in olc) if olc else None,
                        "beg": statistics.mean(v["beg_iz"] for v in olc) if olc else None,
                        "devam": sum(v["karar"] == "DEVAM" for v in vs)})
        return sorted(out, key=lambda r: (r["pay"] is None, -(r["pay"] or 0)))

    gruplar = {}
    for alan, ad in (("kanca", "Kanca ailesi"), ("giris", "Giriş türü")):
        gruplar[alan] = grupla(alan)
        print(f"\n{ad} ortalaması (oranlar yalnız ≥{MIN_IZ} izlenmeli videolardan)")
        print(f"| {ad} | Video | Oranlı | Ort. izlenme | pay/iz | beğ/iz | DEVAM |")
        print("|---|---|---|---|---|---|---|")
        for r in gruplar[alan]:
            print(f"| {r['k']} | {r['n']} | {r['n_olc']} | {r['iz']:.0f} | {yuzde(r['pay'])} | {yuzde(r['beg'])} | {r['devam']} |")

    sayim = {k: sum(v["karar"] == k for v in vids) for k in ("DEVAM", "BEKLE", "ÖLDÜR")}
    print(f"\nÖzet: DEVAM {sayim['DEVAM']} · BEKLE {sayim['BEKLE']} · ÖLDÜR {sayim['ÖLDÜR']}")
    if plan:
        olculen = {(v["video"], v["platform"]) for v in vids}
        eksik = sorted(k for k in plan if k not in olculen)
        print(f"Planda olup 48s ölçümü olmayan: {len(eksik)}" + (f" ({', '.join(f'{a}/{b}' for a, b in eksik[:10])})" if eksik else ""))
        if len(eksik) >= 5:
            print("⚠ ≥5 video ölçülmedi → lider kurucuya tek soru sorar: '48. saat verilerini girebilir misin?'")
    if len(vids) >= 10 and sayim["DEVAM"] == 0:
        print("⚠ Parti kararı: ≥10 videodan hiçbiri DEVAM değil → görüntüyü (şablon/ilk kare) değiştir, kancayı değil.")

    print("\n--- dersler.md (H bölümü) için ÖNERİ — dosyaya yazılmadı, onaylanırsa elle eklenir ---")
    for alan, ad in (("kanca", "kanca ailesi"), ("giris", "giriş türü")):
        oranli = [r for r in gruplar[alan] if r["pay"] is not None]
        if len(oranli) >= 2:
            en, son = oranli[0], oranli[-1]
            az = " (n<3, tek seri — kesin değil)" if min(en["n_olc"], son["n_olc"]) < 3 else ""
            print(f"- 48s ölçümünde en iyi {ad} **{en['k']}** (pay/iz {yuzde(en['pay'])}, beğ/iz {yuzde(en['beg'])}, "
                  f"n={en['n_olc']}), en zayıf **{son['k']}** ({yuzde(son['pay'])}, n={son['n_olc']}){az}.")
    dv = [v["video"] + "/" + v["platform"] for v in vids if v["karar"] == "DEVAM"]
    ol = [v["video"] + "/" + v["platform"] for v in vids if v["karar"] == "ÖLDÜR"]
    if dv:
        print(f"- DEVAM: {', '.join(dv)} → aynı kanca + yeni sahne (R2) ve aynı görüntü + 3 yeni kanca (R1) üret.")
    if ol:
        print(f"- ÖLDÜR: {', '.join(ol)} → bu kanca/giriş birleşimi bir sonraki partiye alınmaz.")
    te = [v["video"] + "/" + v["platform"] for v in vids if v["tutma_ele"]]
    if te:
        print(f"- Tutma medyan (%{tut_med:.0f}) altında ve paylaşım eşiğinin altında: {', '.join(te)} → ilk kare değişir.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
