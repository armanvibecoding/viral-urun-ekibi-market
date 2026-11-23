#!/usr/bin/env python3
"""Hikâye videosu hattı: kur → render → ses → panolar → görüntü kapısı → TESLIM.

  python3 uret.py ayar.json [--sessiz-ffmpeg] [--kontrol-kareleri "0.05 1.5 4.5 ..."]

--sessiz-ffmpeg: HyperFrames render'ı atlanır ("atlandı" yazılır), hazırlanmış stok klipler ffmpeg ile birleştirilir (yazısız).
  Yalnız test/ön izleme içindir; teslim sürümü HyperFrames ile render edilir (Node 22+, npx hyperframes doctor).
Çıkış: 0 hepsi geçti · 2 ayar kapısı · 8 render · 3/ses_olc kodu · görüntü kapısı kodu.
"""
import json
import os
import shutil
import subprocess
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURADA)
from _arac import FF, CUT, sure as medya_sure  # noqa: E402

HF_SURUM = os.environ.get("HF_SURUM", "0.9.65")


def kos(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], **kw)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ayar = os.path.abspath(sys.argv[1])
    D = os.path.dirname(ayar)
    a = json.load(open(ayar, encoding="utf-8"))
    ad, sure = a["ad"], float(a["sure"])
    kk = sys.argv[sys.argv.index("--kontrol-kareleri") + 1] if "--kontrol-kareleri" in sys.argv else "0.05 1.5 4.5 7 10 13 17.5 20 23 %.1f" % (sure - 0.5)
    py = sys.executable
    if kos([py, os.path.join(BURADA, "hikaye_kur.py"), ayar]).returncode != 0:
        sys.exit(2)
    sessiz = os.path.join(D, "hf", "renders", ad + "_sessiz.mp4")
    if "--sessiz-ffmpeg" in sys.argv:
        print("HyperFrames render atlandı (--sessiz-ffmpeg): yazısız ffmpeg birleştirme kullanılıyor")
        liste = os.path.join(D, "hf", "renders", "liste.txt")
        t_ = [0.0] + [float(x) for x in a["kesimler"]] + [sure]
        with open(liste, "w") as f:
            for i in range(len(t_) - 1):
                k = os.path.join(D, "hf", "assets", "video", "a%d.mp4" % i)
                if not os.path.exists(k):  # ürün sahnesi: koyu zemin
                    k = os.path.join(D, "hf", "renders", "bos%d.mp4" % i)
                    kos([FF, "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x0A1030:s=1080x1920:r=30", "-t", round(t_[i + 1] - t_[i] + 0.25, 2),
                         "-c:v", "libx264", "-pix_fmt", "yuv420p", k], check=True)
                f.write("file '%s'\ninpoint 0\noutpoint %.2f\n" % (k, t_[i + 1] - t_[i]))
        kos([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-vf", "fps=30,format=yuv420p", "-t", sure, "-c:v", "libx264", "-crf", "17", sessiz], check=True)
    else:
        if not shutil.which("npx"):
            print("HATA: npx yok (Node 22+ gerekli). Test için --sessiz-ffmpeg.")
            sys.exit(8)
        with open(os.path.join(D, "hf", "renders", "render_%s.log" % ad), "w") as lg:
            r = kos(["npx", "--yes", "hyperframes@" + HF_SURUM, "render", "--output", "renders/%s_sessiz.mp4" % ad], cwd=os.path.join(D, "hf"), stdout=lg, stderr=subprocess.STDOUT)
        if r.returncode != 0:
            print("HATA: render başarısız, bkz hf/renders/render_%s.log" % ad)
            sys.exit(8)
    if kos([py, os.path.join(BURADA, "ses.py"), ayar]).returncode != 0:
        sys.exit(3)
    teslim = os.path.join(D, "TESLIM", ad + ".mp4")
    kos([py, os.path.join(BURADA, "pano.py"), "video", teslim, os.path.join(D, "TESLIM", ad), kk], check=True)
    kes = ",".join(str(x) for x in a["kesimler"])
    g = kos([py, os.path.join(CUT, "kurgu_kontrol.py"), "--goruntu", teslim, "--kesimler", kes, "--yalniz-goruntu"], capture_output=True, text=True)
    print((g.stdout.strip().splitlines() or [""])[-1])
    print("görüntü kapısı çıkış", g.returncode)
    d = medya_sure(teslim)
    print("süre %.3f sn" % d)
    if g.returncode != 0:
        sys.exit(g.returncode)
    if abs(d - sure) > 0.1:
        print("HATA: süre %.3f ≠ %.1f" % (d, sure))
        sys.exit(4)
    print("TAMAM", teslim)


if __name__ == "__main__":
    main()
