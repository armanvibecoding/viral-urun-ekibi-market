#!/usr/bin/env python3
"""30 senaryonun kod kontrolü + tablo üretimi. Elle "kontrol ettim" yerine ölçüm.

Girdi: is/NN-urun/senaryolar.json (biçim: referans/senaryo-formati.md).
Çıktı: senaryolar.md (tablo) + senaryolar.csv (Excel açar) aynı klasöre; ekrana sayılarla rapor.
Çıkış kodu 0 = geçti · 1 = en az bir ❌ (düzelt, tekrar koş).

Kontroller:
 1) etkileşim sahnesi no <= sonuç sahnesi no (SEBEP -> SONUÇ)
 2) aynı sahne eylemi > 3 senaryoda = ❌
 3) iki senaryonun birleşik sahne metni benzerliği (difflib) > 0,8 = ❌
 4) "an" tekrarı = ❌
 5) kimlik kelimeli kanca <= 15 (30 senaryoda; oranla ölçeklenir)
 6) dağılım (>= 30 senaryoda): >= 8 mekanizma, >= 6 şablon, >= 6 kanca ailesi, hiçbir şablon > 6,
    aynı aile art arda yok, >= 3 yazısız (K13)
 7) sahne sayısı 3-4 (S1 tek sahne gag: 2-3)
 8) TR pazarında kanca <= 8 kelime ve kalıp yasakları; K13'te kanca boş
 9) çeşitlilik: `giris` (ilk klip/ilk kare kimliği) ve `ortam` her videoda zorunlu; aynı giriş > 2 videoda = ❌,
    aynı ortam > 6 videoda = ❌; `ozne` (araç/renk/hayvan gibi) varsa aynı özne ardışık iki videoda = ❌
10) organik seride (varsayılan; kökte "kreatif": "reklam" değilse) kanca/CTA/`yazilar` içinde fiyat ($12, 199 TL, ₺, €, "% off") = ❌
11) ABD pazarında her videoda `kultur` (görünen ABD kültür unsuru) alanı zorunlu
    (10–11: 2026-11-17 kurucu geri bildirimi — "organikte fiyat anlamsız", "ABD kültür unsuru zorunlu")
Kullanım: python3 senaryo_kontrol.py is/04-urun/senaryolar.json
"""
import csv
import difflib
import json
import os
import re
import sys
from collections import Counter

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TR_YASAK = ["keşfedin", "hayatınızı değiştirecek", "sizler için", "hemen sipariş verin", "mükemmel", "kaliteli",
            "tanışın", "işte", "artık", "—"]
TR_KIMLIK = r"\b(annesi|annesine|anneleri|babası|babaları|sahibi|sahipleri|severler|sevenler|anne|baba)\b"
EN_KIMLIK = r"\b(moms?|dads?|owners?|lovers?|guys?|girls?|parents?|people)\b"


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", (s or "").lower())).strip()


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    yol = sys.argv[1]
    with open(yol, encoding="utf-8") as f:
        d = json.load(f)
    pazar = (d.get("pazar") or "").upper()
    organik = (d.get("kreatif") or "organik").lower() != "reklam"
    FIYAT = re.compile(r"([$€£₺]\s?\d)|(\d[\d.,]*\s?(tl|usd|eur|dollars?)\b)|(\d+\s?%\s?off)|(\bfiyat)", re.I)
    V = d["videolar"]
    n = len(V)
    hata, uyari = [], []

    for v in V:
        no = v.get("no")
        sh = v.get("sahneler", [])
        alt, ust = (2, 3) if v.get("sablon") == "S1" else (3, 4)
        if not alt <= len(sh) <= ust:
            hata.append(f"V{no}: {len(sh)} sahne ({v.get('sablon')} için {alt}-{ust})")
        e, s = v.get("etkilesim_sahne"), v.get("sonuc_sahne")
        if e and s and e > s:
            hata.append(f"V{no}: etkileşim sahnesi {e} > sonuç sahnesi {s} (sonuç sebepten önce)")
        k = (v.get("kanca") or "").strip()
        if organik:
            for metin_ in [k, v.get("cta") or ""] + list(v.get("yazilar") or []):
                if FIYAT.search(metin_ or ""):
                    hata.append(f"V{no}: organik videoda fiyat: '{metin_[:50]}' (fiyat caption/bio'da; reklamsa kökte \"kreatif\": \"reklam\")")
        if pazar in ("US", "ABD", "USA") and not norm(v.get("kultur")):
            hata.append(f"V{no}: ABD videosunda 'kultur' alanı boş (görünen ABD kültür unsuru: ortam/an/dil/takvim)")
        if v.get("aile") == "K13" and k:
            hata.append(f"V{no}: K13 yazısız ama kanca var")
        if pazar == "TR" and k:
            kel = len(re.sub(r"[^\w\sçğıöşüÇĞİÖŞÜ]", " ", k).split())
            if kel > 8:
                hata.append(f"V{no}: kanca {kel} kelime (TR en fazla 8)")
            for y in TR_YASAK:
                if y in k.lower() or y in (v.get("cta") or "").lower():
                    hata.append(f"V{no}: yasak kalıp '{y}'")

    eylem_say = Counter()
    for v in V:
        for e_ in {norm(s.get("eylem")) for s in v.get("sahneler", [])}:
            eylem_say[e_] += 1
    for e_, c in eylem_say.items():
        if e_ and c > 3:
            hata.append(f"aynı sahne eylemi {c} senaryoda: '{e_[:60]}'")

    metin = {v["no"]: " ".join(norm(s.get("eylem")) for s in v.get("sahneler", [])) for v in V}
    benzer = 0
    for i in range(n):
        for j in range(i + 1, n):
            a, b = metin[V[i]["no"]], metin[V[j]["no"]]
            r = difflib.SequenceMatcher(None, a, b).ratio()
            if r > 0.8:
                benzer += 1
                hata.append(f"V{V[i]['no']} ~ V{V[j]['no']} benzerlik {r:.2f} (> 0,80)")

    an_say = Counter(norm(v.get("an")) for v in V)
    for a, c in an_say.items():
        if a and c > 1:
            hata.append(f"'an' {c} kez tekrar: '{a[:60]}'")

    kimlik_re = TR_KIMLIK if pazar == "TR" else EN_KIMLIK
    kimlik = sum(1 for v in V if v.get("kimlik") or re.search(kimlik_re, (v.get("kanca") or "").lower()))
    sinir = max(1, round(15 * n / 30))
    if kimlik > sinir:
        hata.append(f"kimlik kelimeli kanca {kimlik} (en fazla {sinir})")

    mek = Counter(m.strip() for v in V for m in re.split(r"[+,/]", v.get("mekanizma", "")) if m.strip())
    sab = Counter(v.get("sablon") for v in V)
    aile = Counter(v.get("aile") for v in V)
    ard = [f"V{V[i]['no']}-V{V[i + 1]['no']}" for i in range(n - 1) if V[i].get("aile") == V[i + 1].get("aile")]
    if n >= 30:
        if len(mek) < 8:
            hata.append(f"mekanizma çeşidi {len(mek)} (en az 8; ürüne uyan azsa raporda söyle)")
        if len(sab) < 6:
            hata.append(f"şablon çeşidi {len(sab)} (en az 6)")
        if len(aile) < 6:
            hata.append(f"kanca ailesi çeşidi {len(aile)} (en az 6)")
        for s_, c in sab.items():
            if c > 6:
                hata.append(f"şablon {s_} {c} kez (en fazla 6)")
        if aile.get("K13", 0) < 3:
            hata.append(f"yazısız (K13) {aile.get('K13', 0)} (en az 3)")
    else:
        uyari.append(f"{n} senaryo: dağılım kontrolleri (6) yalnız >= 30 senaryoda uygulanır")
    if ard:
        hata.append("aynı kanca ailesi art arda: " + ", ".join(ard))

    # ---- çeşitlilik: giriş, ortam, özne ----
    for alan in ("giris", "ortam"):
        eksik = [f"V{v.get('no')}" for v in V if not norm(v.get(alan))]
        if eksik:
            hata.append(f"'{alan}' alanı boş: " + ", ".join(eksik[:10]))
    for alan, sinir_ in (("giris", 2), ("ortam", 6)):
        say = Counter(norm(v.get(alan)) for v in V if norm(v.get(alan)))
        for deger, c in say.items():
            if c > sinir_:
                hata.append(f"aynı {alan} {c} videoda (en fazla {sinir_}): '{deger[:50]}'")
    oz = [(v.get("no"), norm(v.get("ozne"))) for v in V]
    for (n1, o1), (n2, o2) in zip(oz, oz[1:]):
        if o1 and o1 == o2:
            hata.append(f"aynı özne art arda: V{n1}-V{n2} '{o1[:40]}'")
    giris_n = len({norm(v.get("giris")) for v in V if norm(v.get("giris"))})
    ortam_n = len({norm(v.get("ortam")) for v in V if norm(v.get("ortam"))})

    # ---- tablo ----
    kok = os.path.splitext(yol)[0]
    bas = ["No", "Mekanizma", "Şablon", "Giriş", "Ortam", "Özne", "An", "Kanca", "Aile", "Sahneler", "Etkileşim", "Sonuç",
           "CTA", "Neden çalışır"]
    satirlar = [[v.get("no"), v.get("mekanizma"), v.get("sablon"), v.get("giris"), v.get("ortam"), v.get("ozne"),
                 v.get("an"), v.get("kanca") or "(yazısız)",
                 v.get("aile"), " → ".join(s.get("eylem", "") for s in v.get("sahneler", [])),
                 v.get("etkilesim_sahne"), v.get("sonuc_sahne"), v.get("cta"), v.get("neden")] for v in V]
    with open(kok + ".md", "w", encoding="utf-8") as f:
        f.write(f"# {d.get('urun', '')} — {n} senaryo ({pazar or 'pazar ?'})\n\n")
        f.write("| " + " | ".join(bas) + " |\n|" + "---|" * len(bas) + "\n")
        for r in satirlar:
            f.write("| " + " | ".join(str(x if x is not None else "").replace("|", "/") for x in r) + " |\n")
    with open(kok + ".csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(bas)
        w.writerows(satirlar)

    print(f"{n} senaryo · mekanizma {len(mek)} · şablon {len(sab)} (en çok {max(sab.values()) if sab else 0}) · "
          f"aile {len(aile)} · K13 {aile.get('K13', 0)} · kimlik kancası {kimlik}/{sinir} · benzer çift {benzer} · "
          f"giriş {giris_n} · ortam {ortam_n}")
    print(f"tablo: {kok}.md  ve  {kok}.csv")
    for u in uyari:
        print("UYARI:", u)
    for h in hata:
        print("❌", h)
    print("SONUÇ:", "GEÇTİ" if not hata else f"{len(hata)} hata — düzelt, tekrar koş")
    sys.exit(1 if hata else 0)


if __name__ == "__main__":
    main()
