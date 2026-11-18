#!/usr/bin/env python3
"""Bitmiş videonun sesini ölç (ses tasarımcısı / eleştirmen için): LUFS, true peak, LRA, drop artışı, ses delikleri.

Kullanım:
  python3 ses_olc.py VIDEO.mp4 [--drop 3.429] [--delik_db -45] [--delik_sn 0.25] [--muzik_stem MUZIK.wav --kapi]

drop_artis_db: ses_tasarla.py ile aynı tanım — drop sonrası 0,43 sn RMS / drop öncesi (−0,6 … −0,05 sn) RMS.
delikler: 50 ms pencerelerde RMS < delik_db olan, delik_sn'den uzun aralıklar (kanca sessizliği, kesim boşluğu).
tepe_anlari: en yüksek 5 kısa-dönem (50 ms) RMS anı — "ana ses anı neresi" sorusuna cevap.
muzik_giris (yalnız --muzik_stem ile; stem = müziğin VİDEO ZAMAN ÇİZGİSİNE yerleştirilmiş hâli, efektsiz).
Kural (2026-11-17 kurucu): açılış diegetik ses olayıyla; müzik −30 dB'den başlar, 1,5–2 sn'de yatak seviyesine çıkar,
ortada "bir anda açılma" yok. yatak = stem'in 1 sn pencere RMS medyanı.
  baslangic_db   : ilk 0,1 sn RMS − yatak. Eşik ≤ −20 (hedef −30; parçanın güçlü notası için 10 dB pay).
  rampa_sn       : 0,5 sn pencere RMS'in ilk kez (yatak − 3 dB)'e ulaştığı an (pencere ortası). Eşik 1,5–3,0 sn.
                   Ölçüldü: dB-doğrusal 1,5/1,75/2,0 sn rampa → 1,3–1,6 sn; rampasız 0,25; doğrusal genlik 1,5 sn → 0,65–1,4.
  ilk_sn_db      : ilk 1 sn RMS − yatak. Eşik ≥ −30 → ilk saniye sessiz değil (−30 dB rampanın ortalaması ≈ −20).
  maks_basamak_db: RMS[t, t+3] − RMS[t−3, t] en büyüğü (0,05 sn adım). Eşik ≤ +10.
                   Kalibrasyon: kısık+boğuk yatak → drop'ta tam müzik tarifi +22,2 dB (KALDI); aynı parça 0'dan rampayla
                   +7,2 dB (parçanın kendi dinamiği; GEÇTİ). 1 sn pencere parçanın cümle dinamiğinde (+10,5) yanlış alarm verdi.
  acilis_olayi_db: (VIDEO karışımında) ilk 0,5 sn'nin en yüksek 50 ms RMS'i − karışımın 1 sn medyanı. Eşik ≥ −6 →
                   açılışta duyulur bir diegetik ses olayı var (müzik o sırada −30 dB'de).
  tuttu          : hepsi birden.
drop_disi_sicrama (her zaman): ardışık 0,1 sn RMS pencereleri arası artış; muaf ilk 0,5 sn, drop ±0,5 sn ve −45 dB altından
  dönüş. `asan` = +10 dB'yi aşanlar (puan cetveli Ses 5-ölçütü; 2026-11-18 eleştirmen reçetesi: alan yoktu, elle ölçülüyordu).
--kapi çıkışları: 3 = müzik girişi tutmadı ya da ses deliği var (delikler dolu) · 4 = drop dışı sıçrama > +10 dB · 0 = temiz.
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


GIRIS_ESIK = {"baslangic_db": -20.0, "rampa_min_sn": 1.5, "rampa_max_sn": 3.0, "ilk_sn_db": -30.0,
              "maks_basamak_db": 10.0, "acilis_olayi_db": -6.0}


def _enerji(x, sr):
    h = int(0.05 * sr)
    n = len(x) // h
    return (np.asarray(x[: n * h], np.float64).reshape(n, h) ** 2).mean(1)


def _db(v):
    return 10 * np.log10(v + 1e-12)


def acilis_olayi(karisim, sr=SR):
    """Karışımın ilk 0,5 sn'sindeki en yüksek 50 ms RMS − karışımın 1 sn medyanı (dB)."""
    en = _enerji(karisim, sr)
    if len(en) < 20:
        return None
    return float(_db(en[:10]).max() - np.median(_db(np.convolve(en, np.ones(20) / 20, mode="valid"))))


def muzik_giris(x, sr=SR, esik=None, karisim=None):
    """x: mono müzik stem'i (video zaman çizgisinde); karisim: isteğe bağlı mono video sesi (açılış olayı için)."""
    e = dict(GIRIS_ESIK, **(esik or {}))
    en = _enerji(x, sr)
    if len(en) < 60:
        return {"tuttu": False, "neden": "stem 3 sn'den kısa"}
    c1 = np.convolve(en, np.ones(20) / 20, mode="valid")  # 1 sn
    yatak = float(np.median(_db(c1)))
    bas = float(_db(en[:2].mean()) - yatak)
    q = np.convolve(en, np.ones(10) / 10, mode="valid")  # 0,5 sn
    u = np.nonzero(_db(q) >= yatak - 3)[0]
    rampa = float(u[0] * 0.05 + 0.25) if len(u) else float(len(en) * 0.05)
    ilk = float(_db(c1[0]) - yatak)
    W = 60  # 3 sn
    c3 = np.convolve(en, np.ones(W) / W, mode="valid")
    adim = [(float(_db(c3[i]) - _db(c3[i - W])), i * 0.05) for i in range(W, len(c3))]
    mb, mbs = max(adim) if adim else (0.0, 0.0)
    r = {"baslangic_db": round(bas, 1), "rampa_sn": round(rampa, 2), "ilk_sn_db": round(ilk, 1),
         "maks_basamak_db": round(mb, 1), "basamak_sn": round(mbs, 2), "esik": e}
    neden = []
    if bas > e["baslangic_db"]:
        neden.append(f"müzik −30 dB'den başlamıyor (ilk 0,1 sn {bas:+.1f} dB > {e['baslangic_db']})")
    if not e["rampa_min_sn"] <= rampa <= e["rampa_max_sn"]:
        neden.append(f"rampa {rampa:.2f} sn ({e['rampa_min_sn']}–{e['rampa_max_sn']} dışında; hedef 1,5–2 sn dB-doğrusal)")
    if ilk < e["ilk_sn_db"]:
        neden.append(f"ilk 1 sn müzik yok/çok kısık ({ilk:+.1f} dB < {e['ilk_sn_db']})")
    if mb > e["maks_basamak_db"]:
        neden.append(f"{mbs:.2f} sn'de ani açılma (+{mb:.1f} dB > +{e['maks_basamak_db']}, 3 sn pencere)")
    if karisim is not None:
        ao = acilis_olayi(karisim, sr)
        r["acilis_olayi_db"] = None if ao is None else round(ao, 1)
        if ao is None or ao < e["acilis_olayi_db"]:
            neden.append(f"açılışta diegetik ses olayı yok (ilk 0,5 sn tepe {ao if ao is None else round(ao, 1)} dB < {e['acilis_olayi_db']})")
    r["tuttu"] = not neden
    if neden:
        r["neden"] = "; ".join(neden)
    return r


SICRAMA_ESIK = 10.0


def drop_disi_sicrama(x, drop=0.0, sr=SR):
    """Ardışık 0,1 sn RMS pencereleri arası artış (dB). Muaf: ilk 0,5 sn (diegetik açılış olayı), drop ±0,5 sn,
    önceki pencere −45 dB altı (bilinçli sessizlikten dönüş). Eşik +10 dB (puan cetveli Ses 5-ölçütü)."""
    h = int(0.1 * sr)
    n = len(x) // h
    z = 20 * np.log10(np.sqrt((np.asarray(x[: n * h], np.float64).reshape(n, h) ** 2).mean(1)) + 1e-9)
    adim = []
    for k in range(1, n):
        t = k * 0.1
        if t < 0.5 or (drop > 0 and abs(t - drop) <= 0.5) or z[k - 1] < -45:
            continue
        adim.append({"sn": round(t, 1), "db": round(float(z[k] - z[k - 1]), 1)})
    adim.sort(key=lambda d: -d["db"])
    return {"maks": adim[0] if adim else None, "asan": [d for d in adim if d["db"] > SICRAMA_ESIK],
            "esik_db": SICRAMA_ESIK}


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
    ap.add_argument("--kapi", action="store_true", help="müzik girişi/delik → çıkış 3; drop dışı sıçrama > +10 dB → çıkış 4")
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
    rapor["drop_disi_sicrama"] = drop_disi_sicrama(x, a.drop)
    if a.muzik_stem:
        rapor["muzik_giris"] = muzik_giris(oku_mono(FF, a.muzik_stem), karisim=x)
    print(json.dumps(rapor, ensure_ascii=False, indent=1))
    if a.kapi:
        k3 = []
        if a.muzik_stem and not rapor["muzik_giris"]["tuttu"]:
            k3.append("müzik girişi tutmadı — " + rapor["muzik_giris"]["neden"])
        if delikler:
            k3.append(f"ses deliği: {delikler}")
        ds = rapor["drop_disi_sicrama"]
        if k3:
            print("KAPI: " + " · ".join(k3), file=sys.stderr)
            sys.exit(3)
        if ds["asan"]:
            print(f"KAPI: drop dışı 0,1 sn sıçrama > +{SICRAMA_ESIK:.0f} dB: {ds['asan']} — müzik stem'ine kompresör "
                  "(ses-tasarimi §1.5); --muzik_db normalizasyondan sonra etkisizdir", file=sys.stderr)
            sys.exit(4)


if __name__ == "__main__":
    main()
