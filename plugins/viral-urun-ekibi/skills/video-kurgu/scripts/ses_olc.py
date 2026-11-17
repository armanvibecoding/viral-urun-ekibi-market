#!/usr/bin/env python3
"""Bitmiş videonun sesini ölç (ses tasarımcısı / eleştirmen için): LUFS, true peak, LRA, drop artışı, ses delikleri.

Kullanım:
  python3 ses_olc.py VIDEO.mp4 [--drop 3.429] [--delik_db -45] [--delik_sn 0.25] [--muzik_stem MUZIK.wav --kapi]

drop_artis_db: ses_tasarla.py ile aynı tanım — drop sonrası 0,43 sn RMS / drop öncesi (−0,6 … −0,05 sn) RMS.
delikler: 50 ms pencerelerde RMS < delik_db olan, delik_sn'den uzun aralıklar (kanca sessizliği, kesim boşluğu).
tepe_anlari: en yüksek 5 kısa-dönem (50 ms) RMS anı — "ana ses anı neresi" sorusuna cevap.
muzik_giris (yalnız --muzik_stem ile; stem = müziğin VİDEO ZAMAN ÇİZGİSİNE yerleştirilmiş hâli, efektsiz):
  ilk_sn_db      : ilk 1 sn RMS − stem medyanı (1 sn pencereler). Eşik ≥ −20 → müzik ilk kareden duyulur.
  acilis_db      : ilk 0,25 sn RMS − ilk 3 sn'nin 1 sn medyanı. Eşik ≤ −6 → tam seviyeyle "pat" diye açılmaz (fade-in ≥ ~1 sn).
  maks_basamak_db: RMS[t, t+3] − RMS[t−3, t] en büyüğü (0,05 sn adım). Eşik ≤ +10 → ortada "bir anda açılma" yok.
                   Kalibrasyon (2026-11-17): kısık+boğuk yatak → drop'ta tam müzik tarifi +22,2 dB (KALDI); aynı parça
                   0'dan 1,5 sn fade-in ile +7,2 dB (parçanın kendi dinamiği; GEÇTİ). 1 sn pencere parçanın kendi
                   cümle dinamiğini (+10,5) yakalayıp yanlış alarm verdi → 3 sn.
  tuttu          : üçü birden. --kapi verilirse tuttu=false → çıkış 3.
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


GIRIS_ESIK = {"ilk_sn_db": -20.0, "acilis_db": -6.0, "maks_basamak_db": 10.0}


def muzik_giris(x, sr=SR, esik=None):
    """x: mono müzik stem'i (video zaman çizgisinde). Dönen sözlük JSON'a yazılabilir."""
    e = dict(GIRIS_ESIK, **(esik or {}))
    h = int(0.05 * sr)
    n = len(x) // h
    if n < 60:
        return {"tuttu": False, "neden": "stem 3 sn'den kısa"}
    en = (np.asarray(x[: n * h], np.float64).reshape(n, h) ** 2).mean(1)
    db = lambda v: 10 * np.log10(v + 1e-12)
    c1 = np.convolve(en, np.ones(20) / 20, mode="valid")  # 1 sn pencereler
    med = float(np.median(db(c1)))
    ilk = float(db(c1[0]) - med)
    acilis = float(db(en[:5].mean()) - np.median(db(c1[:41])))
    W = 60  # 3 sn
    c3 = np.convolve(en, np.ones(W) / W, mode="valid")
    bas = [(float(db(c3[i]) - db(c3[i - W])), i * 0.05) for i in range(W, len(c3))]
    mb, mbs = max(bas) if bas else (0.0, 0.0)
    r = {"ilk_sn_db": round(ilk, 1), "acilis_db": round(acilis, 1), "maks_basamak_db": round(mb, 1),
         "basamak_sn": round(mbs, 2), "esik": e}
    r["tuttu"] = bool(ilk >= e["ilk_sn_db"] and acilis <= e["acilis_db"] and mb <= e["maks_basamak_db"])
    if not r["tuttu"]:
        neden = []
        if ilk < e["ilk_sn_db"]:
            neden.append(f"ilk 1 sn müzik yok/çok kısık ({ilk:+.1f} dB < {e['ilk_sn_db']})")
        if acilis > e["acilis_db"]:
            neden.append(f"müzik tam seviyeyle açılıyor (ilk 0,25 sn {acilis:+.1f} dB > {e['acilis_db']}; fade-in ekle)")
        if mb > e["maks_basamak_db"]:
            neden.append(f"{mbs:.2f} sn'de ani açılma (+{mb:.1f} dB > +{e['maks_basamak_db']}, 3 sn pencere)")
        r["neden"] = "; ".join(neden)
    return r


def oku_mono(FF, yol):
    tmp = tempfile.mkdtemp(prefix="olc_")
    ham = os.path.join(tmp, "ham.f32")
    subprocess.run([FF, "-hide_banner", "-y", "-i", yol, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", ham],
                   capture_output=True)
    x = np.fromfile(ham, np.float32).astype(np.float64)
    shutil.rmtree(tmp, ignore_errors=True)
    return x


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--drop", type=float, default=0.0, help="drop'un videodaki saniyesi (0 = ölçme)")
    ap.add_argument("--delik_db", type=float, default=-45.0)
    ap.add_argument("--delik_sn", type=float, default=0.25)
    ap.add_argument("--muzik_stem", help="video zaman çizgisindeki müzik stem'i (ses_tasarla --stem_klasoru → muz.wav)")
    ap.add_argument("--kapi", action="store_true", help="muzik_giris tutmazsa çıkış 3")
    a = ap.parse_args()
    FF = ffmpeg_yolu()
    r = subprocess.run([FF, "-hide_banner", "-i", a.video, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind("Summary:"):]
    sayi = lambda k: float(re.search(k + r"\s+(-?[\d.]+|-inf)", s).group(1).replace("-inf", "-120"))
    tp = float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf)", s).group(1).replace("-inf", "-120"))
    rapor = {"video": a.video, "I_lufs": sayi("I:"), "LRA": sayi("LRA:"), "true_peak_dbtp": tp}

    x = oku_mono(FF, a.video)
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
    if a.muzik_stem:
        rapor["muzik_giris"] = muzik_giris(oku_mono(FF, a.muzik_stem))
    print(json.dumps(rapor, ensure_ascii=False, indent=1))
    if a.kapi and a.muzik_stem and not rapor["muzik_giris"]["tuttu"]:
        print("KAPI: müzik girişi tutmadı — " + rapor["muzik_giris"]["neden"], file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
