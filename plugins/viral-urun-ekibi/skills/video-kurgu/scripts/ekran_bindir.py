#!/usr/bin/env python3
"""Ürün üstündeki ekran/yazı/logo içeriğini kurguda bindirir (AI'a ÇİZDİRİLMEZ; AI ekranı 4 sn içinde bozar).

Başlangıç karesinde ekran kapalı siyah cam ya da düz tek renk üretilir; Flow promptunda "SCREEN LOCK"
(renk 4 sn sabit) yazılır. Bu betik animasyonu (video ya da görsel) daire/dikdörtgen maskeyle ekranın içine koyar.
Kamera yalnız sabit / yavaş doğrusal hareket olmalı: konum ve boyut ilk kare -> son kare arasında doğrusal
enterpolasyonla izlenir. Koordinatlar KLİBİN kendi pikselinde (ilk/son kareyi PNG çıkarıp ölç).

Kullanım:
  python3 ekran_bindir.py klip.mp4 anim.mp4 cikti.mp4 --x0 360 --y0 520 --d0 180 [--x1 .. --y1 .. --d1 ..]
        [--sekil daire|dikdortgen] [--en-boy 1.0] [--parlaklik 0.0] [--gri]
  --kareler klip.mp4   -> ölçüm için <klip>_ilk.png ve <klip>_son.png çıkarır, başka bir şey yapmaz.
Sonra ZORUNLU: klip_qc.py <cikti> --pano ile her karede bindirme ekranın içinde mi, kenardan taşıyor mu bak.
"""
import argparse
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ffaraclar as F  # noqa: E402


def maske(yol, w, h, sekil, yumusak=2):
    Image, ImageDraw, ImageFilter, _ = F._pil()
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    kutu = [yumusak, yumusak, w - 1 - yumusak, h - 1 - yumusak]
    (d.ellipse if sekil == "daire" else d.rectangle)(kutu, fill=255)
    m.filter(ImageFilter.GaussianBlur(yumusak / 2)).save(yol)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("klip")
    ap.add_argument("anim", nargs="?")
    ap.add_argument("cikti", nargs="?")
    ap.add_argument("--kareler", action="store_true")
    ap.add_argument("--x0", type=float)
    ap.add_argument("--y0", type=float)
    ap.add_argument("--d0", type=float, help="ekranın iç genişliği (çerçeve hariç), px")
    ap.add_argument("--x1", type=float)
    ap.add_argument("--y1", type=float)
    ap.add_argument("--d1", type=float)
    ap.add_argument("--sekil", choices=["daire", "dikdortgen"], default="daire")
    ap.add_argument("--en-boy", type=float, default=1.0, help="yükseklik/genişlik (dikdörtgen ekran)")
    ap.add_argument("--parlaklik", type=float, default=0.0, help="-0.3..0.3: karedeki ışığa eşle")
    ap.add_argument("--gri", action="store_true", help="gece/IR kamerası sahnesi")
    a = ap.parse_args()
    ff = F.ffmpeg_bul()
    b = F.medya_bilgi(a.klip)

    if a.kareler:
        kok = os.path.splitext(a.klip)[0]
        F.calistir([ff, "-v", "error", "-y", "-ss", "0", "-i", a.klip, "-frames:v", "1", kok + "_ilk.png"])
        F.calistir([ff, "-v", "error", "-y", "-sseof", "-0.1", "-i", a.klip, "-frames:v", "1", kok + "_son.png"])
        print(f"{kok}_ilk.png  {kok}_son.png  ({b['w']}x{b['h']}) — ekran merkezi (x,y) ve iç genişliği ölç")
        return
    if not (a.anim and a.cikti and a.x0 is not None and a.y0 is not None and a.d0):
        sys.exit("anim, cikti, --x0 --y0 --d0 gerekli (önce --kareler ile ölç)")
    x1 = a.x1 if a.x1 is not None else a.x0
    y1 = a.y1 if a.y1 is not None else a.y0
    d1 = a.d1 or a.d0
    T = max(b["sure"], 0.1)
    S = int(max(a.d0, d1)) // 2 * 2 + 2
    SH = int(S * a.en_boy) // 2 * 2
    gec = tempfile.mkdtemp(prefix="bindir_")
    try:
        mp = os.path.join(gec, "maske.png")
        maske(mp, S, SH, a.sekil)
        resim = os.path.splitext(a.anim)[1].lower() in (".png", ".jpg", ".jpeg", ".webp")
        anim_gir = ["-loop", "1", "-t", f"{T:.3f}", "-i", a.anim] if resim else ["-stream_loop", "-1", "-i", a.anim]
        renk = f",eq=brightness={a.parlaklik}" if a.parlaklik else ""
        renk += ",hue=s=0" if a.gri else ""
        dw = f"(({a.d0})+(({d1})-({a.d0}))*t/{T:.3f})"
        xe = f"(({a.x0})+(({x1})-({a.x0}))*t/{T:.3f})"
        ye = f"(({a.y0})+(({y1})-({a.y0}))*t/{T:.3f})"
        fl = [
            f"[1:v]fps=30,scale={S}:{SH},format=rgba{renk}[a]", "[2:v]format=gray[m]", "[a][m]alphamerge[am]",
            f"[am]scale=w='trunc({dw}/2)*2':h='trunc({dw}*{a.en_boy}/2)*2':eval=frame[s]",
            f"[0:v][s]overlay=x='{xe}-w/2':y='{ye}-h/2':eval=frame:shortest=1[o]"]
        son = "o"
        fl.append(f"[{son}]format=yuv420p[v]")
        F.calistir([ff, "-v", "error", "-y", "-i", a.klip] + anim_gir + ["-loop", "1", "-t", f"{T:.3f}", "-i", mp,
                   "-filter_complex", ";".join(fl), "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "17",
                   "-preset", "medium", "-c:a", "copy", "-t", f"{T:.3f}", a.cikti])
    finally:
        shutil.rmtree(gec, ignore_errors=True)
    m = F.medya_bilgi(a.cikti)
    print(f"tamam: {a.cikti}  {m['w']}x{m['h']} {m['sure']:.2f} sn — şimdi: klip_qc.py {a.cikti} --pano ile taşma kontrolü")


if __name__ == "__main__":
    main()
