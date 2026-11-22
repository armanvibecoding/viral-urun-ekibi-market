#!/usr/bin/env python3
"""Başlangıç karesi hazırlığı ve ürün karşılaştırması (Pillow; ffmpeg gerekmez).

1) Kırp/ölçekle:  python3 kare_hazirla.py girdi.png cikti.png [--referans orijinal.jpg]
   Ortadan 9:16 kırpar, 1080x1920'ye ölçekler; kaynak boyutu, kesilen payı ve md5'i yazar.
   md5 referansla aynıysa "YANLIŞ DOSYA" (üretilen değil, yüklediğin ek inmiştir) -> çıkış 1.
   Yanına <cikti>_onizleme.jpg (900 px) yazar: kırpılmış karede ürün/el/pati/çıkış noktası kesilmiş mi BAK.
2) Aynı ürün mü panosu:  python3 kare_hazirla.py --yan-yana orijinal.jpg uretilen.png pano.jpg [--bolge 0.2,0.5,0.8,0.9]
   İki görseli aynı yükseklikte yan yana koyar; --bolge (oran: x0,y0,x1,y1) verilirse o bölgeyi iki görselden
   2x büyütüp alta ekler (yazı/parça harf harf karşılaştırma). Oran ölçümü (ör. tuş genişliği / gövde genişliği)
   bu panoda piksel olarak yapılır; sapma > %10 = ❌. Göz kararı ✅ geçersiz.
"""
import argparse
import hashlib
import os
import sys

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow gerekli: python3 -m pip install pillow   (Windows: py -3 -m pip install pillow)")


def md5(yol):
    with open(yol, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def kirp(girdi, cikti, referans=None):
    im = Image.open(girdi).convert("RGB")
    w, h = im.size
    hedef = 9 / 16
    if w / h > hedef:
        nw = round(h * hedef)
        kutu = ((w - nw) // 2, 0, (w - nw) // 2 + nw, h)
    else:
        nh = round(w / hedef)
        kutu = (0, (h - nh) // 2, w, (h - nh) // 2 + nh)
    pay = 1 - (kutu[2] - kutu[0]) * (kutu[3] - kutu[1]) / (w * h)
    out = im.crop(kutu).resize((1080, 1920), Image.LANCZOS)
    os.makedirs(os.path.dirname(os.path.abspath(cikti)), exist_ok=True)
    out.save(cikti)
    on = os.path.splitext(cikti)[0] + "_onizleme.jpg"
    out.resize((506, 900), Image.LANCZOS).save(on, quality=85)
    oran = f"{w}x{h} ({w / h:.3f})"
    print(f"{girdi}: kaynak {oran} -> 1080x1920 · kırpılan pay %{pay * 100:.0f} · kutu {kutu}")
    print(f"önizleme: {on}  (ürün, el/pati ve çıkış noktası kadrajda mı, üst %25 boş mu — bak)")
    if abs(w / h - 2 / 3) > 0.02 and abs(w / h - 9 / 16) > 0.02:
        print("UYARI: kaynak ne 2:3 ne 9:16; kenarlar beklenenden çok kesilmiş olabilir")
    if referans and md5(girdi) == md5(referans):
        print("YANLIŞ DOSYA: indirilen görsel referansla birebir aynı (md5) — üretilen kareyi yeniden indir")
        sys.exit(1)


def yan_yana(a, b, cikti, bolge=None):
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    H = 900
    A = A.resize((round(A.width * H / A.height), H))
    B = B.resize((round(B.width * H / B.height), H))
    satirlar = [(A, B)]
    if bolge:
        x0, y0, x1, y1 = bolge
        za = A.crop((int(x0 * A.width), int(y0 * H), int(x1 * A.width), int(y1 * H)))
        zb = B.crop((int(x0 * B.width), int(y0 * H), int(x1 * B.width), int(y1 * H)))
        satirlar.append((za.resize((za.width * 2, za.height * 2)), zb.resize((zb.width * 2, zb.height * 2))))
    gw = max(x.width + y.width + 20 for x, y in satirlar)
    gh = sum(max(x.height, y.height) + 10 for x, y in satirlar)
    pano = Image.new("RGB", (gw, gh), (255, 255, 255))
    yy = 0
    for x, y in satirlar:
        pano.paste(x, (0, yy))
        pano.paste(y, (x.width + 20, yy))
        yy += max(x.height, y.height) + 10
    d = ImageDraw.Draw(pano)
    d.text((8, 8), "ORIJINAL", fill=(255, 0, 0))
    d.text((A.width + 28, 8), "URETILEN", fill=(255, 0, 0))
    pano.save(cikti, quality=90)
    print(f"pano: {cikti}  (parça sayısı, renk, yazı harf harf, oran — tabloya ✅/❌ yaz)")
    if md5(a) == md5(b):
        print("YANLIŞ DOSYA: iki görsel birebir aynı (md5)")
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dosyalar", nargs="*")
    ap.add_argument("--referans")
    ap.add_argument("--yan-yana", nargs=3, metavar=("ORIJINAL", "URETILEN", "PANO"))
    ap.add_argument("--bolge", help="x0,y0,x1,y1 (0-1 oran)")
    a = ap.parse_args()
    if a.yan_yana:
        b = [float(x) for x in a.bolge.split(",")] if a.bolge else None
        yan_yana(*a.yan_yana, bolge=b)
    elif len(a.dosyalar) == 2:
        kirp(a.dosyalar[0], a.dosyalar[1], a.referans)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
