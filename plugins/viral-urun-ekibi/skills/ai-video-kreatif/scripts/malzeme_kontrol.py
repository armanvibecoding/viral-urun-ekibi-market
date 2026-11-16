#!/usr/bin/env python3
"""Malzeme yeterliliği kapısı: video planı × klip planı × kredi tavanı. Kredi onayından ÖNCE koşar.

Neden: 30'luk seride özne (araç) başına 5 klip vardı; aynı aracın 3. videosu her araçta "kopya" diye
eleştiriden geçmedi ve tavan dolduğu için kurtarılamadı (dersler.md H/78, SKILL.md "Flow ve kredi").

Kurallar (özne = araç/sahne; V = o öznenin video sayısı):
 1) klip:   K >= 5 + 3*(V-2)  (en az 5)  -> 2 video 5 klip, 3 video 8 klip, 4 video 11 klip
 2) içerik: ekran/"sonra" içerik sayısı >= V (her videoya ayrı bir "sonra")
 3) ortak klip: en fazla 4 videoda ve ardışık iki videoda (no farkı 1) değil
 4) kredi:  (gerekli yeni klip) * kredi_klip * (1 + yedek) <= tavan   (720p = 12 kredi/klip, yedek 0,15)
Mevcut (önceden üretilmiş) klip kredi istemez.

Girdi: (a) 30-VIDEO-PLANI-v3.md biçiminde plan (araç tablosu "Ekran içerikleri" sütunlu, ortak tablo
"Kullanılan videolar" sütunlu, video tablosu "| No | Araç |"; "(A, 6 klip)" mevcut klip sayılır) ya da
(b) JSON:
  {"tavan": 800, "kredi_klip": 12, "yedek": 0.15,
   "araclar": {"C1": {"klip": 5, "icerik": 2, "mevcut": 0}, ...},
   "videolar": [{"no": 1, "arac": "C1"}, ...],
   "ortak": {"O1": [3, 11, 19, 26], ...}}
Çıkış 0 = yeterli · 1 = en az bir yetersiz ya da tavan aşıldı (alternatifler basılır) · 2 = girdi okunamadı.

Kullanım:
  python3 malzeme_kontrol.py 30-VIDEO-PLANI-v3.md --klip 5 --tavan 800
  python3 malzeme_kontrol.py plan.json
  bayraklar: --klip N (planlı klip, araç başına; JSON'daki değeri ezer) · --icerik N (en az içerik) ·
             --mevcut A=6 · --tavan X · --kredi-klip 12 · --yedek 0.15
"""
import argparse
import json
import math
import re
import sys

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def gerekli_klip(v):
    return max(5, 5 + 3 * (v - 2))


def _hucreler(satir):
    return [h.strip() for h in satir.strip().strip("|").split("|")]


def md_oku(metin):
    araclar, videolar, ortak = {}, [], {}
    tablo = None
    for satir in metin.splitlines():
        if not satir.strip().startswith("|"):
            tablo = None
            continue
        h = _hucreler(satir)
        if all(re.fullmatch(r":?-+:?", x or "-") for x in h):
            continue
        baslik = " ".join(h).lower()
        if "ekran içerik" in baslik:
            tablo = "arac"; continue
        if "kullanılan video" in baslik:
            tablo = "ortak"; continue
        if h[0].lower() == "no" and len(h) > 1 and h[1].lower().startswith("araç"):
            tablo = "video"; continue
        if tablo == "arac" and len(h) >= 5:
            icerik = [x for x in re.split(r"→|->", h[4]) if x.strip()]
            araclar[h[0]] = {"icerik": max(0, len(icerik) - 1), "ad": h[1]}
        elif tablo == "ortak" and len(h) >= 3:
            ortak[h[0]] = [int(x) for x in re.findall(r"\d+", h[2])]
        elif tablo == "video" and len(h) >= 2 and re.fullmatch(r"\d+", h[0]):
            videolar.append({"no": int(h[0]), "arac": h[1]})
    for kod, n in re.findall(r"\(([A-Z]\w*),\s*(\d+)\s*klip\)", metin):
        araclar.setdefault(kod, {"icerik": 0})
        araclar[kod]["mevcut"] = int(n)
        araclar[kod]["klip"] = int(n)
    return {"araclar": araclar, "videolar": videolar, "ortak": ortak}


def maliyet(klip, ka):
    return klip * ka["kredi_klip"] * (1 + ka["yedek"])


def en_cok_video(satirlar, ortak_yeni, ka):
    """Tavan içinde en çok video: önce her özne 2 video (5 klip), sonra +3 klip ile +1 video."""
    butce = ka["tavan"] / (ka["kredi_klip"] * (1 + ka["yedek"])) - ortak_yeni  # klip cinsinden
    secim = {}
    # kredi istemeyen (mevcut klipli) özneler önce
    for s in sorted(satirlar, key=lambda s: -s["mevcut"]):
        hedef = min(s["V"], 2)
        yeni = max(0, gerekli_klip(hedef) - s["mevcut"])
        if yeni <= butce + 1e-9:
            butce -= yeni
            secim[s["kod"]] = hedef
    ilerledi = True
    while ilerledi:
        ilerledi = False
        for s in satirlar:
            v = secim.get(s["kod"])
            if v is None or v >= s["V"]:
                continue
            ek = max(0, gerekli_klip(v + 1) - s["mevcut"]) - max(0, gerekli_klip(v) - s["mevcut"])
            if ek <= butce + 1e-9:
                butce -= ek
                secim[s["kod"]] = v + 1
                ilerledi = True
    return secim


def main():
    ap = argparse.ArgumentParser(description="Malzeme yeterliliği kapısı")
    ap.add_argument("plan")
    ap.add_argument("--klip", type=int)
    ap.add_argument("--icerik", type=int)
    ap.add_argument("--mevcut", action="append", default=[])
    ap.add_argument("--tavan", type=float)
    ap.add_argument("--kredi-klip", type=float)
    ap.add_argument("--yedek", type=float)
    a = ap.parse_args()

    try:
        metin = open(a.plan, encoding="utf-8").read()
        veri = json.loads(metin) if a.plan.lower().endswith(".json") else md_oku(metin)
    except Exception as e:
        print(f"Girdi okunamadı: {e}")
        return 2
    ka = {"tavan": a.tavan if a.tavan is not None else veri.get("tavan"),
          "kredi_klip": a.kredi_klip or veri.get("kredi_klip", 12),
          "yedek": a.yedek if a.yedek is not None else veri.get("yedek", 0.15)}
    if ka["tavan"] is None:
        print("Kredi tavanı yok: --tavan ver ya da JSON'a 'tavan' yaz.")
        return 2
    araclar, videolar, ortak = veri.get("araclar", {}), veri.get("videolar", []), veri.get("ortak", {})
    if not videolar:
        print("Video planı boş (video tablosu/listesi bulunamadı).")
        return 2
    for m in a.mevcut:
        kod, n = m.split("=")
        araclar.setdefault(kod, {})
        araclar[kod]["mevcut"] = int(n)

    sayac = {}
    for v in videolar:
        sayac.setdefault(v["arac"], []).append(int(v["no"]))
    hata = False
    satirlar = []
    for kod in sorted(sayac, key=lambda k: (k != "A", len(k), k)):
        bilgi = araclar.get(kod, {})
        mevcut = int(bilgi.get("mevcut", 0))
        klip = bilgi.get("klip") if mevcut and a.klip is None else (a.klip if a.klip is not None else bilgi.get("klip"))
        if klip is None:
            klip = mevcut
        klip = max(int(klip), mevcut)
        icerik = int(bilgi.get("icerik", 0))
        if a.icerik is not None:
            icerik = max(icerik, a.icerik)
        V = len(sayac[kod])
        kg = gerekli_klip(V)
        ok = klip >= kg and icerik >= V
        hata |= not ok
        satirlar.append({"kod": kod, "V": V, "klip": klip, "mevcut": mevcut, "kg": kg, "icerik": icerik,
                         "ok": ok, "ek": max(0, kg - klip), "yeni_plan": max(0, klip - mevcut),
                         "yeni_gerekli": max(0, max(kg, klip) - mevcut)})

    print(f"Malzeme kontrolü: {len(videolar)} video · {len(satirlar)} özne · {len(ortak)} ortak klip · "
          f"tavan {ka['tavan']:.0f} · {ka['kredi_klip']:.0f} kredi/klip · yedek %{ka['yedek']*100:.0f}\n")
    print("| Özne | Video (V) | Klip plan/gerekli | İçerik plan/gerekli | Ek klip | Ek kredi | Sonuç |")
    print("|---|---|---|---|---|---|---|")
    for s in satirlar:
        nedenler = []
        if s["klip"] < s["kg"]:
            nedenler.append("klip az")
        if s["icerik"] < s["V"]:
            nedenler.append(f"içerik +{s['V'] - s['icerik']}")
        sonuc = "✅ yeterli" if s["ok"] else "❌ yetersiz (" + ", ".join(nedenler) + ")"
        mev = f" (mevcut {s['mevcut']})" if s["mevcut"] else ""
        print(f"| {s['kod']} | {s['V']} | {s['klip']}/{s['kg']}{mev} | {s['icerik']}/{s['V']} | {s['ek']} | "
              f"{s['ek'] * ka['kredi_klip']:.0f} | {sonuc} |")

    ortak_yeni, ortak_ihlal = 0, 0
    print()
    for kod, nolar in sorted(ortak.items()):
        nolar = sorted(int(x) for x in nolar)
        sorun = []
        if len(nolar) > 4:
            sorun.append(f"{len(nolar)} videoda (>4)")
        ard = [f"{x:02d}-{y:02d}" for x, y in zip(nolar, nolar[1:]) if y - x == 1]
        if ard:
            sorun.append("ardışık " + ",".join(ard))
        if sorun:
            hata = True
            ortak_ihlal += 1
            print(f"❌ ortak {kod}: " + "; ".join(sorun))
        ortak_yeni += 1
    if ortak:
        print(f"Ortak klipler: {len(ortak)} adet, kural ihlali {ortak_ihlal}")

    yeni_plan = sum(s["yeni_plan"] for s in satirlar) + ortak_yeni
    yeni_gerekli = sum(s["yeni_gerekli"] for s in satirlar) + ortak_yeni
    k_plan, k_ger = maliyet(yeni_plan, ka), maliyet(yeni_gerekli, ka)
    print(f"\nPlanlanan: {yeni_plan} yeni klip × {ka['kredi_klip']:.0f} = {yeni_plan * ka['kredi_klip']:.0f} kredi "
          f"(+yedek = {math.ceil(k_plan)})")
    print(f"Gerekli:   {yeni_gerekli} yeni klip × {ka['kredi_klip']:.0f} = {yeni_gerekli * ka['kredi_klip']:.0f} kredi "
          f"(+yedek = {math.ceil(k_ger)}) · tavan {ka['tavan']:.0f} → "
          + ("✅ sığar" if k_ger <= ka["tavan"] else f"❌ {math.ceil(k_ger - ka['tavan'])} kredi aşar"))
    if k_ger > ka["tavan"]:
        hata = True

    if not hata:
        print("\nSONUÇ: ✅ malzeme yeterli — tavan onayı bu sayıyla istenebilir.")
        return 0

    secim = en_cok_video(satirlar, ortak_yeni, ka)
    nmax = sum(secim.values())
    icerik_eksik = sum(max(0, v - next(s["icerik"] for s in satirlar if s["kod"] == k)) for k, v in secim.items())
    kmax = sum(max(0, gerekli_klip(v) - next(s["mevcut"] for s in satirlar if s["kod"] == k))
               for k, v in secim.items()) + ortak_yeni
    print("\nSONUÇ: ❌ malzeme yetersiz. Seçenekler (kurucu karar verir — para kararı):")
    print(f"  1) {len(videolar)} video için {math.ceil(k_ger)} kredi (yedekli; {yeni_gerekli} klip) — "
          f"içerik eksiği varsa prompt'a ek ekran içeriği yazılır, kredi istemez.")
    print(f"  2) Tavan {ka['tavan']:.0f} ile en çok {nmax} video ({kmax} klip ≈ {math.ceil(maliyet(kmax, ka))} kredi): "
          + ", ".join(f"{k}×{v}" for k, v in secim.items())
          + (f" · ek ekran içeriği {icerik_eksik}" if icerik_eksik else ""))
    iki = sum(min(s["V"], 2) for s in satirlar)
    k_iki = sum(max(0, gerekli_klip(min(s["V"], 2)) - s["mevcut"]) for s in satirlar) + ortak_yeni
    print(f"  3) Özne başına en çok 2 video: {iki} video, {k_iki} klip ≈ {math.ceil(maliyet(k_iki, ka))} kredi.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
