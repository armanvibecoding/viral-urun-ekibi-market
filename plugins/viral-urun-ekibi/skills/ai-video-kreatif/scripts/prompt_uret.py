#!/usr/bin/env python3
"""Başlangıç karesi (ChatGPT) ve klip (Flow / Omni) promptlarını ŞABLONDAN üretir — elle kopyalama yok.

Kilit metinleri (ürün, mekanizma, ekran) her prompta betik ekler; elle hatırlamaya bırakılmaz.
Kontroller (biri tutmazsa çıkış 1, dosya yazılmaz):
  - PRODUCT kilidinin tam metni her promptta birebir var mı (sayılır)
  - AUDIO ⊆ ACTION: AUDIO'daki her ses, ACTION'daki bir kelimeye bağlı mı (ses satırı görüntüye olay ekletir:
    "treat rolling" yazılan basışsız klipte model kendiliğinden mama döktü). Sesi sebebiyle yaz:
    "single piano note as the white key goes down". Ortam sesi "ambient" listesine yazılır.
  - Yasak görsel kelimeleri (8k, hyperrealistic, cinematic, masterpiece, perfect)
Uyarı: belirsiz yön kelimesi (under, near, around) — yeri adıyla tarif et.

Girdi: senaryolar.json (referans/senaryo-formati.md) + kilit.txt:
    PRODUCT: <İngilizce tek paragraf ürün kilidi>
    MECHANISM: <isteğe bağlı: sonuç YALNIZ nereden çıkar, neye basılmazsa olmaz>
    SCREEN: <isteğe bağlı: ekranlı üründe "screen stays one flat uniform color, no image/icon/text, no flicker">
    AVOID: <isteğe bağlı ek yasaklar, virgülle>
    WRONG: <isteğe bağlı: ürünün yanlış davranışı, Flow AVOID'a eklenir>
Kullanım:
  python3 prompt_uret.py senaryolar.json kilit.txt --cikti promptlar/ [--video 1 4 7]
  python3 prompt_uret.py senaryolar.json kilit.txt --kopyala 1 2 flow     (V01 sahne 2 Flow promptu panoya)
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

YASAK_GORSEL = ["8k", "hyperrealistic", "cinematic", "masterpiece", "perfect"]
BELIRSIZ = ["under", "near", "around", "beside"]
ORTAM = {"hum", "room", "tone", "ambience", "ambient", "wind", "rain", "traffic", "birds", "silence", "breeze",
         "background", "distant", "echo", "footsteps", "purring", "purr", "breathing"}
SES_DOLGU = {"sound", "sounds", "soft", "faint", "quiet", "loud", "gentle", "single", "short", "small", "little",
             "light", "sharp", "low", "high", "the", "and", "with", "from", "one", "two", "three", "few", "tiny",
             "click", "clicks", "clack", "thud", "tap", "taps", "rustle", "rustling", "noise", "of", "a", "an", "its",
             "as", "when", "goes", "down", "into", "onto", "out", "off", "each", "every", "then", "while"}


def kilit_oku(yol):
    k = {}
    with open(yol, encoding="utf-8") as f:
        for satir in f:
            m = re.match(r"\s*(PRODUCT|MECHANISM|SCREEN|AVOID|WRONG)\s*:\s*(.+)", satir)
            if m:
                k[m.group(1)] = (k.get(m.group(1), "") + " " + m.group(2).strip()).strip()
    if not k.get("PRODUCT"):
        sys.exit("kilit.txt içinde 'PRODUCT:' satırı yok")
    return k


def kelimeler(s):
    return re.findall(r"[a-z]+", (s or "").lower())


def ses_baglimi(ses, eylem):
    ek = kelimeler(eylem)
    icerik = [w for w in kelimeler(ses) if w not in SES_DOLGU and len(w) >= 3]
    if not icerik or set(icerik) & ORTAM:
        return True
    return any(any(e.startswith(w[:5]) or w.startswith(e[:5]) for e in ek if len(e) >= 3) for w in icerik)


def gorsel(v, si, s, k, ortak):
    p = s.get("prompt", {})
    al = lambda x: p.get(x) or v.get(x) or ortak.get(x)  # noqa: E731
    sat = []
    if si > 0:
        sat.append(f"CONTINUITY LOCK: same {al('who') or 'subject'}, same place, same light and the same product "
                   f"as the previous image in this chat.")
    sat += ["Generate ONE image. Vertical 9:16 phone-video still frame, photorealistic, looks like a real "
            "Instagram Reel shot on an iPhone.",
            f"SCENE: {p['scene']}",
            f"PRODUCT (copy exactly from the reference photo): {k['PRODUCT']}"]
    if k.get("SCREEN"):
        sat.append(f"SCREEN: {k['SCREEN']}")
    sat += [f"WHO: {al('who') or 'nobody'}",
            f"POSITION: {p.get('position', 'as described in SCENE')} — the interaction point is already touched "
            f"in this frame, nothing hovers in the air.",
            f"WHERE: {al('where')}", f"LIGHT: {al('light')}",
            "FRAMING: the product, the hand/paw and the exit point sit inside the middle 70% of the frame; the "
            "product fills at least one third of the frame; the top 25% of the frame shows only plain "
            "wall/background - no head, ears or product there; nothing important in the bottom 20% or the right "
            "15%. At most three subjects.",
            "TEXTURE: natural phone noise, a real lived-in place, one light source, not perfect.",
            "AVOID: any text or letters, watermark, brand logos, posters, licensed characters, extra fingers, "
            "distorted hands or paws, extra animals, traces of an event that has not happened yet, studio backdrop, "
            "studio lighting, bokeh, CGI render look" + (", " + k["AVOID"] if k.get("AVOID") else "") + "."]
    return "\n".join(sat)


def flow(v, s, k):
    p = s["prompt"]
    ses = p.get("audio", []) + p.get("ambient", [])
    sat = ["Make a 4-second vertical 9:16 video using the attached image as the exact first frame.",
           f"CAMERA: {p.get('camera', 'static, low, in front - no camera move')}.",
           f"ACTION: {p['action']} Only this one action happens.",
           "PRODUCT: stays identical - same shape, color, parts and text; it does not move by itself, grow, "
           "shrink or duplicate."]
    if k.get("MECHANISM"):
        sat.append(f"MECHANISM: {k['MECHANISM']}")
    if k.get("SCREEN"):
        sat.append(f"SCREEN LOCK: {k['SCREEN']} It stays exactly like this for all 4 seconds.")
    sat += ["LIGHT: unchanged from the image.",
            f"AUDIO: {', '.join(ses) if ses else 'natural room tone only'}. No dialogue. No music.",
            "AVOID: extra paws or hands, extra animals, on-screen text, subtitles, watermark, glow, light beams"
            + (", " + k["WRONG"] if k.get("WRONG") else "") + ".",
            f"PRODUCT LOCK: {k['PRODUCT']}",
            "ONE continuous shot: no cuts, no jumps, nothing vanishes or appears; people and animals keep the same "
            "look, breed, colors and markings for all 4 seconds."]
    return "\n".join(sat)


def panoya(metin):
    if sys.platform == "darwin" and shutil.which("pbcopy"):
        cmd = ["pbcopy"]
    elif os.name == "nt":
        cmd = ["clip"]
    elif shutil.which("xclip"):
        cmd = ["xclip", "-selection", "clipboard"]
    else:
        print(metin)
        return "pano aracı yok; metin yukarıda"
    subprocess.run(cmd, input=metin.encode("utf-16" if os.name == "nt" else "utf-8"), check=True)
    return "panoya kopyalandı"


def main():
    import json
    ap = argparse.ArgumentParser()
    ap.add_argument("senaryolar")
    ap.add_argument("kilit")
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--video", type=int, nargs="*")
    ap.add_argument("--kopyala", nargs=3, metavar=("VIDEO", "SAHNE", "TUR"))
    a = ap.parse_args()
    with open(a.senaryolar, encoding="utf-8") as f:
        d = json.load(f)
    k = kilit_oku(a.kilit)
    ortak = d.get("ortak", {})
    secili = a.video or ([int(a.kopyala[0])] if a.kopyala else None)
    V = [v for v in d["videolar"] if (secili is None and all("prompt" in s for s in v["sahneler"]))
         or (secili and v["no"] in secili)]
    if not V:
        sys.exit("prompt alanı dolu senaryo yok (--video ile seçtiklerinin sahnelerinde 'prompt' olmalı)")
    hata, uyari, uret = [], [], {}
    for v in V:
        for si, s in enumerate(v["sahneler"]):
            ad = f"V{v['no']:02d}_S{si + 1}"
            if "prompt" not in s or not s["prompt"].get("scene") or not s["prompt"].get("action"):
                hata.append(f"{ad}: prompt.scene / prompt.action eksik")
                continue
            g, fl = gorsel(v, si, s, k, ortak), flow(v, s, k)
            for ses in s["prompt"].get("audio", []):
                if not ses_baglimi(ses, s["prompt"]["action"]):
                    hata.append(f"{ad}: AUDIO '{ses}' ACTION'da yok — ya eylemi yaz ya sesi sil (ortam sesi ise 'ambient')")
            for w in YASAK_GORSEL:
                if re.search(rf"\b{w}\b", (s["prompt"].get("scene", "") + " " + s["prompt"]["action"]).lower()):
                    hata.append(f"{ad}: yasak görsel kelimesi '{w}'")
            for w in BELIRSIZ:
                if re.search(rf"\b{w}\b", (s["prompt"]["action"] + " " + s["prompt"].get("position", "")).lower()):
                    uyari.append(f"{ad}: belirsiz yön '{w}' — yeri adıyla tarif et")
            uret[ad] = (g, fl)
    sayi = sum(t.count(k["PRODUCT"]) for g, fl in uret.values() for t in (g, fl))
    if sayi != 2 * len(uret):
        hata.append(f"ürün kilidi {sayi}/{2 * len(uret)} promptta")
    for u in uyari:
        print("UYARI:", u)
    if hata:
        for h in hata:
            print("DUR:", h)
        sys.exit(1)
    if a.kopyala:
        ad = f"V{int(a.kopyala[0]):02d}_S{a.kopyala[1]}"
        if ad not in uret:
            sys.exit(f"{ad} yok")
        print(ad, a.kopyala[2], panoya(uret[ad][0 if a.kopyala[2].startswith("g") else 1]))
        return
    c = a.cikti or os.path.join(os.path.dirname(os.path.abspath(a.senaryolar)), "promptlar")
    os.makedirs(c, exist_ok=True)
    for ad, (g, fl) in uret.items():
        with open(os.path.join(c, ad + "_gorsel.txt"), "w", encoding="utf-8") as f:
            f.write(g + "\n")
        with open(os.path.join(c, ad + "_flow.txt"), "w", encoding="utf-8") as f:
            f.write(fl + "\n")
    print(f"{len(uret)} sahne × 2 prompt -> {c}  · ürün kilidi {sayi}/{2 * len(uret)} · AUDIO⊆ACTION geçti")


if __name__ == "__main__":
    main()
