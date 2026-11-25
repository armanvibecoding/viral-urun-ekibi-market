#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mixer için TASLAK ses planı (denetim 2026-11-25 #24, V3): anları ayar dosyasından betik çıkarır, Mixer yalnız onaylar/düzeltir.

  python3 ses_plan.py ayar.json [--drop-sn 3.43] [--muzik-bas 8.0] [--md PLAN.md] [--json PLAN.json]

ayar.json = hizli_kurgu biçimi (planlar[bas, bit, gecis: kesim|flas|punch], yazilar[], cta{plan}). Betik yalnız ayardan türetilebilen anları yazar:
  kanca (0 sn) · her `flas` (drop/değişim adayı) · her `punch` (whoosh adayı) · yazı değişimleri (tık adayı) · CTA başlangıcı.
Drop saniyesi: `--drop-sn` verilirse o; verilmezse ayardaki İLK `flas` başlangıcı (kaynak: "tahmin: ilk flas"), flas yoksa süre/2 ("tahmin: süre/2");
tahmin "ölçülmedi" demektir, Mixer `ses_olc.py` ile doğrular. Müzikteki drop saniyesi (`--muzik-bas`) betikçe UYDURULMAZ: verilmezse komutta
`<MUZIK_DROP_SN>` kalır ve komut "çalıştırılamaz" işaretlenir.
Kurallar (agents/mixer.md): 10 sn'de ≤ 5 efekt (öncelik: drop > kanca > riser > punch > flas dışı > yazı tıkı; fazlası listeden düşer ve raporda sayılır) ·
hiyerarşi dB (drop −3, ikincil darbe −6…−9, tık −12, riser −16) · riser drop'tan 0,2 sn önce biter · sessizlik vuruşu 0,2 · ilk 0,5 sn'de bir ses olayı ·
efektler görüntüdeki eyleme bağlı (kesim geçişine efekt YOK; yazı tıkı yalnız yazı değişiminde).
Çıkış: 0 plan yazıldı · 1 ayar geçersiz · 2 kullanım. Aynı girdi → aynı çıktı.
"""
import argparse
import json
import os
import sys

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

MAX_10SN, PENCERE = 5, 10.0
ONCELIK = {"boom": 0, "kanca": 1, "riser": 2, "whoosh": 3, "tik": 4}
DB = {"boom": -3.0, "kanca": -9.0, "riser": -16.0, "whoosh": -9.0, "tik": -12.0}


def anlar(ayar):
    t, sinirlar = 0.0, []
    for i, p in enumerate(ayar.get("planlar") or []):
        if not isinstance(p, dict) or "bas" not in p or "bit" not in p or float(p["bit"]) <= float(p["bas"]):
            raise ValueError("planlar[%d]: bas/bit eksik ya da bit <= bas" % i)
        s = round(float(p["bit"]) - float(p["bas"]), 3)
        sinirlar.append({"no": i + 1, "bas": round(t, 3), "sure": s, "gecis": p.get("gecis", "kesim"), "yazi": p.get("yazi") or ""})
        t += s
    if not sinirlar:
        raise ValueError("planlar boş")
    return sinirlar, round(t, 3)


def plan(ayar, drop_sn=None, muzik_bas=None):
    sinirlar, toplam = anlar(ayar)
    flaslar = [p for p in sinirlar if p["gecis"] == "flas"]
    if drop_sn is not None:
        drop, kaynak = float(drop_sn), "verilen (--drop-sn)"
    elif flaslar:
        drop, kaynak = flaslar[0]["bas"], "tahmin: ilk flas — ölçülmedi, ses_olc.py ile doğrula"
    else:
        drop, kaynak = round(toplam / 2, 2), "tahmin: süre/2 — ölçülmedi, ses_olc.py ile doğrula"
    adaylar = [{"sn": 0.0, "tur": "whoosh", "oncelik": ONCELIK["kanca"], "neden": "kanca sesi: ilk 0,5 sn'de ses olayı (sessiz açılış yok)", "efekt": "kanca"}]
    adaylar.append({"sn": round(drop, 2), "tur": "boom", "oncelik": ONCELIK["boom"], "neden": "drop/vurgu anı (en yüksek efekt)", "efekt": "boom"})
    adaylar.append({"sn": round(max(drop - 1.2 - 0.2, 0.0), 2), "tur": "riser", "oncelik": ONCELIK["riser"],
                    "neden": "drop'tan 0,2 sn önce BİTEN yükseliş (1,2 sn)", "efekt": "riser", "bitis": round(max(drop - 0.2, 0.0), 2)})
    for p in sinirlar:
        if p["gecis"] == "punch":
            adaylar.append({"sn": p["bas"], "tur": "whoosh", "oncelik": ONCELIK["whoosh"], "neden": "punch geçişi (hareketli geçiş)", "efekt": "whoosh"})
        elif p["gecis"] == "flas" and abs(p["bas"] - drop) > 0.05:
            adaylar.append({"sn": p["bas"], "tur": "boom", "oncelik": ONCELIK["whoosh"], "neden": "ikincil flaş değişimi (drop değil)", "efekt": "boom2"})
    for z in ayar.get("yazilar") or []:
        if isinstance(z, dict) and "bas" in z and float(z["bas"]) > 0.3:
            adaylar.append({"sn": round(float(z["bas"]), 2), "tur": "tik", "oncelik": ONCELIK["tik"], "neden": "yazı değişimi: %s" % (z.get("yazi") or "")[:30], "efekt": "tik"})
    secilen, dusen = [], []
    def en_yogun(liste):
        return max([len([y for y in liste if w <= y["sn"] < w + PENCERE]) for w in [x["sn"] for x in liste]] or [0])
    for a in sorted(adaylar, key=lambda x: (x["oncelik"], x["sn"])):
        if any(abs(x["sn"] - a["sn"]) < 0.15 and x["tur"] == a["tur"] for x in secilen):
            dusen.append((a, "aynı anda aynı efekt"))
        elif en_yogun(secilen + [a]) > MAX_10SN:
            dusen.append((a, "10 sn'de ≤ %d efekt kuralı" % MAX_10SN))
        else:
            secilen.append(a)
    secilen.sort(key=lambda x: (x["sn"], x["oncelik"]))
    for a in secilen:
        a["tepe_db"] = DB["boom"] if a["efekt"] == "boom" else (-7.0 if a["efekt"] == "boom2" else DB[a["tur"] if a["efekt"] != "kanca" else "kanca"])
    sfx = ",".join("%s@%.2f" % (a["tur"], a["sn"]) for a in secilen if a["tur"] in ("tik", "boom", "whoosh"))
    riser = next((a for a in secilen if a["tur"] == "riser"), None)
    komut = ["python3", "ses_tasarla.py", "--video", "<VNN_sessiz.mp4>", "--drop_video_sn", "%.2f" % drop, "--muzik_bas", "%s" % (muzik_bas if muzik_bas is not None else "<MUZIK_DROP_SN>")]
    if sfx:
        komut += ["--sfx", sfx]
    if riser:
        komut += ["--riser", "%.2f:1.2:%g" % (riser["bitis"], DB["riser"] - 2)]
    komut += ["--sessizlik_vurusu", "0.2", "--sfx_max_10sn", str(MAX_10SN), "--cikti", "<VNN_ses.mp4>"]
    return {"sure_sn": toplam, "drop_sn": round(drop, 2), "drop_kaynak": kaynak, "efektler": secilen,
            "dusen": [{"sn": a["sn"], "tur": a["tur"], "neden": n} for a, n in dusen], "komut": " ".join(komut),
            "komut_calistirilabilir": not any("<" in k for k in komut),
            "efekt_sayisi": len(secilen), "en_yogun_10sn": en_yogun(secilen)}


def md(p):
    s = ["# Ses planı (TASLAK — Mixer onaylar; kulakla dinlenmedi, ölçülmedi)", "",
         "Süre %.2f sn · drop %.2f sn (%s) · efekt %d · en yoğun 10 sn: %d (en çok %d)" % (p["sure_sn"], p["drop_sn"], p["drop_kaynak"], p["efekt_sayisi"], p["en_yogun_10sn"], MAX_10SN), "",
         "| sn | efekt | tepe dB | neden |", "|---|---|---|---|"]
    for a in p["efektler"]:
        s.append("| %.2f | %s | %g | %s |" % (a["sn"], a["tur"], a["tepe_db"], a["neden"]))
    if p["dusen"]:
        s += ["", "Kuraldan düşen adaylar: " + "; ".join("%.2f sn %s (%s)" % (d["sn"], d["tur"], d["neden"]) for d in p["dusen"])]
    s += ["", "Taslak komut (%s): `%s`" % ("çalıştırılabilir" if p["komut_calistirilabilir"] else "ÇALIŞTIRILAMAZ: <…> alanları ölçümle doldurulacak", p["komut"])]
    return "\n".join(s) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ayar")
    ap.add_argument("--drop-sn", type=float)
    ap.add_argument("--muzik-bas", type=float)
    ap.add_argument("--md")
    ap.add_argument("--json")
    a = ap.parse_args()
    try:
        ayar = json.load(open(a.ayar, encoding="utf-8"))
        p = plan(ayar, a.drop_sn, a.muzik_bas)
    except (OSError, ValueError) as e:
        print("HATA: %s" % e)
        return 1
    m = md(p)
    print(m, end="")
    if a.md:
        open(a.md, "w", encoding="utf-8", newline="\n").write(m)
    if a.json:
        json.dump(p, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
