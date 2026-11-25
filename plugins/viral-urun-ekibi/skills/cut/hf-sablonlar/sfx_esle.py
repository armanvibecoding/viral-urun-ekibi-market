#!/usr/bin/env python3
"""SFX eşleme (kredisiz, yerel): HyperFrames olaylarını (hf/olaylar.json) ses_tasarla `--sfx_dosya` / `--riser` dizgisine çevirir.

Eşleme (mixer hiyerarşisi: ikincil −6…−9 · UI −10…−14 · riser ≤ −22; seviyeler tepe dBFS, son −14 LUFS normalizasyonundan önce):
  kesme (whip)      → whoosh        whoosh-short.mp3   −9    hareket başlangıcından 0,05 sn önce
  kesme (punch)     → whoosh (kısa) whoosh-short.mp3   −12   kırpma 0–0,35
  açılış (0. sn)    → pop           pop.mp3            −4    ilk karedeki yazı: diegetik açılış olayı (müzik rampada; kapı ≥ −6 dB ister)
  yazı girişi       → pop           pop.mp3            −13   şablon başına bir kez (kelime başına değil)
  CTA rozeti        → bubble        bubble.wav         −11   (sentetik)
  kanıt anı         → sparkle/ding  sparkle.mp3 −4 (drop darbesi katmanı) · ping.mp3 −9 (sayaç bitişi = ding)
  şok (tepki)       → darbe         impact-bass-2.mp3  −8    kırpma 0–1,2
  açılış öncesi     → riser         sentetik `--riser`  −22  kanıt anından 0,25 sn önce BİTER (drop kontrastını silmez)
Yoğunluk: herhangi 10 sn penceresinde ≤ max10 efekt (varsayılan 6); fazlası öncelik sırasıyla elenir (punch < yazı < tekrar CTA < whip < riser < CTA < kanıt < şok < açılış).
Lisans kaydı: hf-sablonlar/LISANS-SFX.md.  Kullanım: python3 sfx_esle.py olaylar.json [--sure 8 --max10 6]  → JSON (sfx, riser, plan, elenen)
"""
import json
import os
import shutil
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
EKLENTI = os.path.dirname(os.path.dirname(os.path.dirname(BURADA)))
PIXABAY = os.path.join(EKLENTI, "skills", "media-use", "audio", "assets", "sfx")

# ad → (dosya, tepe dB, kırpma "bas-bit" ya da "")
KART = {
    "whoosh": ("lib_whoosh-short.mp3", -9, ""),
    "whoosh_kisa": ("lib_whoosh-short.mp3", -12, "0-0.35"),
    "pop": ("lib_pop.mp3", -13, "0-0.5"),
    "acilis": ("lib_pop.mp3", -4, "0-0.5"),      # 0. saniye diegetik ses olayı: ses_olc kapısı ilk 0,5 sn tepe ≥ −6 dB ister
    "bubble": ("bubble.wav", -11, ""),
    "sparkle": ("lib_sparkle.mp3", -4, "0-1.4"),
    "ding": ("lib_ping.mp3", -9, "0-1.1"),
    "sok": ("lib_impact-bass-2.mp3", -8, "0-1.2"),
}
ONCELIK = {"acilis": -1, "cta2": 4.5, "sok": 0, "kanit": 1, "cta": 2, "riser": 3, "whip": 4, "yazi": 5, "punch": 6}   # küçük = önemli


def klasor_hazirla(hedef):
    """Lisanslı Pixabay efektlerini (eklentide paketli) hedef klasöre lib_<ad>.mp3 olarak kopyalar."""
    os.makedirs(hedef, exist_ok=True)
    for ad, (dosya, _, _) in KART.items():
        if dosya.startswith("lib_"):
            kaynak = os.path.join(PIXABAY, dosya[4:])
            if not os.path.exists(kaynak):
                raise SystemExit("HATA: efekt kaynağı yok: %s" % kaynak)
            if not os.path.exists(os.path.join(hedef, dosya)):
                shutil.copy(kaynak, os.path.join(hedef, dosya))
    return hedef


def _tur(o):
    if o["tur"] == "kesme":
        return o.get("tip", "whip")
    return o["tur"]


def esle(olaylar, sure, drop=None, max10=6, riser=True):
    """olaylar: [{t, tur, ...}] → {"sfx": 'dosya@sn:dB[:bas-bit],…', "riser": 'bit:sure:dB'|None, "plan": [...], "elenen": [...]}"""
    ev = []
    for o in olaylar:
        k = _tur(o)
        t = float(o["t"])
        if k == "whip":
            ev.append({"t": max(0.0, t - 0.05), "k": "whip", "ad": "whoosh"})
        elif k == "punch":
            ev.append({"t": max(0.0, t), "k": "punch", "ad": "whoosh_kisa"})
        elif k == "yazi":
            if t < 0.5 and not any(e["k"] == "acilis" for e in ev):
                ev.append({"t": t + 0.02, "k": "acilis", "ad": "acilis"})
            else:
                ev.append({"t": t + 0.02, "k": "yazi", "ad": "pop"})
        elif k == "cta":
            ev.append({"t": t + 0.02, "k": "cta2" if any(e["k"] in ("cta", "cta2") for e in ev) else "cta", "ad": "bubble"})
        elif k == "sok":
            ev.append({"t": t, "k": "sok", "ad": "sok"})
        elif k == "kanit":
            ev.append({"t": t, "k": "kanit", "ad": "ding" if o.get("ses") == "ding" else "sparkle"})
    if drop is not None and not any(e["k"] == "kanit" and abs(e["t"] - drop) < 0.6 for e in ev):
        ev.append({"t": float(drop), "k": "kanit", "ad": "sparkle"})
    rs = None
    if riser and drop is not None and drop >= 1.2:
        sr = min(0.9, drop - 0.6)
        rs = (round(drop - 0.25, 2), round(sr, 2), -22)
        ev.append({"t": rs[0] - rs[1], "k": "riser", "ad": "riser"})
    ev = [e for e in ev if e["t"] < sure - 0.05]
    # aynı anda (±0,12 sn) iki efekt: önemlisi kalır
    ev.sort(key=lambda e: (ONCELIK[e["k"]], e["t"]))
    kalan, elenen = [], []
    for e in ev:
        if any(abs(e["t"] - x["t"]) < 0.12 for x in kalan):
            elenen.append(dict(e, neden="aynı anda önemli efekt var"))
        else:
            kalan.append(e)
    # kayan 10 sn pencere kapısı
    while True:
        kalan.sort(key=lambda e: e["t"])
        bozuk = [e for e in kalan if sum(1 for x in kalan if e["t"] <= x["t"] < e["t"] + 10.0) > max10]
        if not bozuk:
            break
        aday = max((x for x in kalan if any(e["t"] <= x["t"] < e["t"] + 10.0 for e in bozuk)), key=lambda x: (ONCELIK[x["k"]], x["t"]))
        kalan.remove(aday)
        elenen.append(dict(aday, neden="10 sn penceresinde > %d efekt" % max10))
    riser_kaldi = any(e["k"] == "riser" for e in kalan)
    parca = []
    for e in sorted(kalan, key=lambda e: e["t"]):
        if e["k"] == "riser":
            continue
        dosya, db, kirp = KART[e["ad"]]
        parca.append("%s@%.2f:%s%s" % (dosya, e["t"], db, (":" + kirp) if kirp else ""))
    return {"sfx": ",".join(parca), "riser": ("%.2f:%.2f:%d" % rs) if (rs and riser_kaldi) else None,
            "plan": sorted(kalan, key=lambda e: e["t"]), "elenen": elenen}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    arg = lambda a, v: float(sys.argv[sys.argv.index(a) + 1]) if a in sys.argv else v  # noqa: E731
    sure = arg("--sure", 8.0)
    print(json.dumps(esle(d["olaylar"], sure, d.get("drop"), int(arg("--max10", 6))), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
