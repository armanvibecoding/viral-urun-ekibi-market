#!/usr/bin/env python3
"""Bitmiş videonun sesini ölç (ses tasarımcısı / eleştirmen için): LUFS, true peak, LRA, drop artışı, ses delikleri.

Kullanım:
  python3 ses_olc.py VIDEO.mp4 [--drop 3.429] [--delik_db -45] [--delik_sn 0.25]

drop_artis_db: ses_tasarla.py ile aynı tanım — drop sonrası 0,43 sn RMS / drop öncesi (−0,6 … −0,05 sn) RMS.
delikler: 50 ms pencerelerde RMS < delik_db olan, delik_sn'den uzun aralıklar (kanca sessizliği, kesim boşluğu).
tepe_anlari: en yüksek 5 kısa-dönem (50 ms) RMS anı — "ana ses anı neresi" sorusuna cevap.
Çıktı JSON; dosya değiştirilmez.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
import numpy as np

SR = 48000


def ffmpeg_yolu():
    yol = shutil.which("ffmpeg")
    try:
        import imageio_ffmpeg
        yol = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    if not yol:
        sys.exit("ffmpeg bulunamadı (imageio_ffmpeg ya da PATH)")
    return yol


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--drop", type=float, default=0.0, help="drop'un videodaki saniyesi (0 = ölçme)")
    ap.add_argument("--delik_db", type=float, default=-45.0)
    ap.add_argument("--delik_sn", type=float, default=0.25)
    a = ap.parse_args()
    FF = ffmpeg_yolu()
    r = subprocess.run([FF, "-hide_banner", "-i", a.video, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind("Summary:"):]
    sayi = lambda k: float(re.search(k + r"\s+(-?[\d.]+|-inf)", s).group(1).replace("-inf", "-120"))
    tp = float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf)", s).group(1).replace("-inf", "-120"))
    rapor = {"video": a.video, "I_lufs": sayi("I:"), "LRA": sayi("LRA:"), "true_peak_dbtp": tp}

    tmp = tempfile.mkdtemp(prefix="olc_")
    ham = os.path.join(tmp, "ham.f32")
    subprocess.run([FF, "-hide_banner", "-y", "-i", a.video, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", ham],
                   capture_output=True)
    x = np.fromfile(ham, np.float32).astype(np.float64)
    shutil.rmtree(tmp, ignore_errors=True)
    rapor["sure_sn"] = round(len(x) / SR, 3)
    rr = lambda v: np.sqrt(np.mean(v ** 2) + 1e-20)
    if a.drop > 0:
        d = int(a.drop * SR)
        on, son = x[max(0, d - int(0.6 * SR)):d - int(0.05 * SR)], x[d:d + int(0.43 * SR)]
        if len(on) > 0 and len(son) > 0:
            rapor["drop_sn"] = a.drop
            rapor["drop_artis_db"] = round(float(20 * np.log10(rr(son) / rr(on))), 1)
    h = int(0.05 * SR)
    n = len(x) // h
    z = 20 * np.log10(np.sqrt((x[: n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
    delikler, bas = [], None
    for j, v in enumerate(list(z) + [0]):
        if v < a.delik_db and bas is None:
            bas = j
        elif v >= a.delik_db and bas is not None:
            if (j - bas) * 0.05 >= a.delik_sn:
                delikler.append([round(bas * 0.05, 2), round(j * 0.05, 2)])
            bas = None
    rapor["delikler"] = delikler
    sira = np.argsort(z)[::-1]
    tepe, secilen = [], []
    for j in sira:
        if all(abs(j - k) > 6 for k in secilen):  # 300 ms aralıkla farklı anlar
            secilen.append(j)
            tepe.append({"sn": round(j * 0.05, 2), "rms_db": round(float(z[j]), 1)})
        if len(tepe) == 5:
            break
    rapor["tepe_anlari"] = tepe
    print(json.dumps(rapor, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
