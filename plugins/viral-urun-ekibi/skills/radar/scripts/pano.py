#!/usr/bin/env python3
"""pano.py KLASOR CIKTI.jpg — KLASOR/k01.png, k02.png ... karelerini tek kontakt sayfasında (en çok 4 sütun) birleştirir.

ffmpeg bulma sırası: PATH'teki ffmpeg → imageio_ffmpeg paketi → kurulum talimatı.
"""
import glob
import os
import shutil
import subprocess
import sys


def ffmpeg_bul():
    yol = shutil.which("ffmpeg")
    if yol:
        return yol
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def main():
    if len(sys.argv) < 3:
        sys.exit("kullanım: pano.py KLASOR CIKTI.jpg")
    klasor, cikti = sys.argv[1], sys.argv[2]
    n = len(glob.glob(os.path.join(klasor, "k[0-9][0-9].png")))
    if n == 0:
        sys.exit(f"HATA: {klasor} içinde k01.png gibi kare yok")
    ff = ffmpeg_bul()
    if not ff:
        sys.exit("HATA: ffmpeg yok. Kur: macOS 'brew install ffmpeg' · Windows 'winget install Gyan.FFmpeg' "
                 "· ya da 'python3 -m pip install imageio-ffmpeg'")
    sutun = min(n, 4)
    satir = (n + sutun - 1) // sutun
    r = subprocess.run([ff, "-loglevel", "error", "-y", "-framerate", "1", "-i", os.path.join(klasor, "k%02d.png"),
                        "-vf", f"scale=300:-1,tile={sutun}x{satir}", "-frames:v", "1", cikti])
    if r.returncode != 0 or not os.path.exists(cikti):
        sys.exit("HATA: kontakt sayfası yapılamadı")
    print(cikti, f"({n} kare)")


if __name__ == "__main__":
    main()
