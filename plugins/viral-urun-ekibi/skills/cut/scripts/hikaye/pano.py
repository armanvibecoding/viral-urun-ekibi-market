#!/usr/bin/env python3
"""Pano araçları (kare kare bakmak için; 4 fps altına inme).

  pano.py video <video.mp4> <çıktı_önek> ["t1 t2 t3 ..."]   → _pano_4fps.jpg · _pano_ilk2sn_10fps.jpg · _kontrol.jpg · _pano10.jpg
  pano.py serit <çıktı.jpg> <klip> ...                      → her klip için saniyede 1 kare şerit (en çok 16 sn)
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _arac import FF  # noqa: E402


def ff(*a):
    subprocess.run([FF, "-v", "error", "-y"] + [str(x) for x in a], check=True)


def video(v, o, kareler=""):
    ff("-i", v, "-vf", "fps=4,scale=180:320,drawtext=text='%{pts\\:hms}':x=3:y=3:fontsize=15:fontcolor=yellow:box=1:boxcolor=black,tile=13x8", "-frames:v", 1, o + "_pano_4fps.jpg")
    ff("-t", 2, "-i", v, "-vf", "fps=10,scale=270:480,drawtext=text='%{pts\\:hms}':x=4:y=4:fontsize=20:fontcolor=yellow:box=1:boxcolor=black,tile=10x2", "-frames:v", 1, o + "_pano_ilk2sn_10fps.jpg")
    ff("-i", v, "-vf", "fps=1/2.5,scale=324:576,tile=5x2", "-frames:v", 1, o + "_pano10.jpg")
    ts = kareler.split()
    if ts:
        with tempfile.TemporaryDirectory() as d:
            yollar = []
            for i, t in enumerate(ts):
                p = os.path.join(d, "k%d.png" % i)
                ff("-ss", t, "-i", v, "-frames:v", 1, "-vf", "scale=405:720", p)
                yollar.append(p)
            m = Image.new("RGB", (405 * len(yollar), 720))
            for k, p in enumerate(yollar):
                m.paste(Image.open(p).convert("RGB"), (405 * k, 0))
            m.save(o + "_kontrol.jpg", quality=88)


def serit(cikti, klipler):
    with tempfile.TemporaryDirectory() as d:
        m = Image.new("RGB", (1440, 160 * len(klipler)))
        dr = ImageDraw.Draw(m)
        for k, f in enumerate(klipler):
            j = os.path.join(d, "s%d.jpg" % k)
            ff("-t", 16, "-i", f, "-vf", "fps=1,scale=90:160:force_original_aspect_ratio=increase,crop=90:160,tile=16x1", "-frames:v", 1, j)
            m.paste(Image.open(j).convert("RGB"), (0, 160 * k))
            dr.rectangle((0, 160 * k, 150, 160 * k + 12), fill=(0, 0, 0))
            dr.text((2, 160 * k), os.path.basename(f), fill=(255, 255, 0))
        m.save(cikti, quality=72)


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "video":
        video(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
    elif len(sys.argv) >= 4 and sys.argv[1] == "serit":
        serit(sys.argv[2], sys.argv[3:])
    else:
        sys.exit(__doc__)
