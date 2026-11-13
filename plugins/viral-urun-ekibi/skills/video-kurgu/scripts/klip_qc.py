#!/usr/bin/env python3
"""AI klip kalite kapısı (Flow / Omni çıktısı). Kurgudan ÖNCE zorunlu.

1) ÇÖZÜNÜRLÜK: video yüksekliği < --min-yukseklik (varsayılan 1280 = 720p dikey) ise HATA.
   360p/düşük klip teslim videosuna girmez; 720p'yi yeniden indir ya da yeniden üret.
2) SIÇRAMA: ardışık kareler arası ortalama mutlak fark (64x112 gri, 24 fps). Fark, KLİBİN genel
   medyanının >= 3 katı VE >= 5,5 ise sıçrama (ışınlanma, nesne kaybolması, klip içi gizli kesme,
   ani kamera atlaması). AI sıçramaları 4-5 kareye yayıldığı için yerel pencere değil klip medyanı
   kullanılır. Eşikler 30 videoluk gerçek seride kalibre edildi (hatalı klipler 9-32 / temiz 1,9-3,6).
   YAKALAMAZ: yavaş dönüşüm (hayvanın cinsi/rengi yavaşça değişir) -> 4 fps panoya gözle bakmak zorunlu.
3) --pano: saniyede 4 kare, zaman damgalı pano (<klip>_qc.jpg). 1,5 fps pano gerçek seride
   30 videonun 17'sindeki hatayı kaçırdı; 4 fps altına inme.

Kullanım: python3 klip_qc.py <klip.mp4> [...] [--pano] [--min-yukseklik 1280]
Çıkış kodu 0 = hepsi temiz · 1 = en az bir klipte sıçrama ya da düşük çözünürlük (kurguya geçme).
"""
import argparse
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
from operator import sub

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ffaraclar as F  # noqa: E402

KW, KH = 64, 112
ORAN, MUTLAK = 3.0, 5.5


def kareler(yol):
    raw = subprocess.run([F.ffmpeg_bul(), "-v", "error", "-i", yol, "-vf", f"fps=24,scale={KW}:{KH},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    n = KW * KH
    return [raw[i * n:(i + 1) * n] for i in range(len(raw) // n)]


def sicramalar(yol):
    """[(saniye, fark, klip_medyani)] döndürür. Boş liste = sıçrama yok."""
    k = kareler(yol)
    if len(k) < 3:
        return []
    n = KW * KH
    d = [sum(map(abs, map(sub, a, b))) / n for a, b in zip(k, k[1:])]
    med = max(statistics.median(d), 0.5)
    bul, son = [], -99
    for i, v in enumerate(d):
        if v >= MUTLAK and v >= ORAN * med:
            if i - son > 6:  # aynı sıçramanın komşu kareleri tek kayıt
                bul.append(((i + 1) / 24, v, med))
            elif v > bul[-1][1]:
                bul[-1] = ((i + 1) / 24, v, med)
            son = i
    return bul


def pano(yol, fps=4, sutun=8):
    """Zaman damgalı kare panosu -> <klip>_qc.jpg (Pillow ile; font yolu kaçışı gerekmez)."""
    Image, ImageDraw, _, ImageFont = F._pil()
    gecici = tempfile.mkdtemp(prefix="qc_")
    try:
        F.calistir([F.ffmpeg_bul(), "-v", "error", "-y", "-i", yol, "-vf", f"fps={fps},scale=180:-2",
                    os.path.join(gecici, "k%04d.png")])
        dosyalar = sorted(x for x in os.listdir(gecici) if x.endswith(".png"))
        if not dosyalar:
            return None
        ilk = Image.open(os.path.join(gecici, dosyalar[0]))
        w, h = ilk.size
        satir = (len(dosyalar) + sutun - 1) // sutun
        tuval = Image.new("RGB", (w * sutun, h * satir), (0, 0, 0))
        try:
            fnt = ImageFont.truetype(F.font_bul(), 18)
        except SystemExit:
            fnt = ImageFont.load_default()
        for i, ad in enumerate(dosyalar):
            im = Image.open(os.path.join(gecici, ad)).convert("RGB")
            dr = ImageDraw.Draw(im)
            dr.rectangle([0, 0, 66, 24], fill=(0, 0, 0))
            dr.text((4, 2), f"{i / fps:.2f}s", font=fnt, fill=(255, 230, 0))
            tuval.paste(im, ((i % sutun) * w, (i // sutun) * h))
        cikti = os.path.splitext(yol)[0] + "_qc.jpg"
        tuval.save(cikti, quality=88)
        return cikti
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description="AI klip kalite kapısı")
    ap.add_argument("klipler", nargs="+")
    ap.add_argument("--pano", action="store_true", help="4 fps zaman damgalı pano üret")
    ap.add_argument("--min-yukseklik", type=int, default=1280)
    a = ap.parse_args()
    hata = 0
    for y in a.klipler:
        b = F.medya_bilgi(y)
        if b["h"] < a.min_yukseklik:
            hata = 1
            print(f"ÇÖZÜNÜRLÜK {y}: {b['w']}x{b['h']} (en az {a.min_yukseklik} yükseklik) — 720p'yi yeniden indir")
        s = sicramalar(y)
        if s:
            hata = 1
            for t, v, m in s:
                print(f"SIÇRAMA {y} @{t:.2f}s fark={v:.1f} klip_medyanı={m:.1f}")
        elif b["h"] >= a.min_yukseklik:
            print(f"temiz   {y}  {b['w']}x{b['h']} {b['sure']:.2f}sn")
        if a.pano:
            p = pano(y)
            print(f"pano    {p}  (her kareye bak: ürün kendi kendine çalışıyor mu, cins/renk değişiyor mu, fazladan uzuv)")
    sys.exit(hata)


if __name__ == "__main__":
    main()
