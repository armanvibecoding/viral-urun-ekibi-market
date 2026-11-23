#!/usr/bin/env python3
"""Hikâye hattı ses adımı: sessiz render → +2 sn dolgu → müzik girişi düzleştirme (−30 dB'ye yakın rampa) → ses_tasarla → kırp →
isteğe bağlı seslendirme (VO) + müzik duck → −14 LUFS → ses_olc --kapi.

  python3 ses.py ayar.json [--video hf/renders/<ad>_sessiz.mp4]

ayar["ses"]: {"muzik": "muzik/x.mp3", "muzik_bas": 22.88 (müzik dosyasında drop sn), "drop": 18.4 (videoda drop sn),
  "giris_hedef": 8, "drop_oncesi_db": -8, "taban": 5, "tavan": 3.5, "fade_in": 1.75, "son_fade": 0.6, "muzik_db": 5,
  "sfx": "pop.wav@0.12:-3,tik.wav@2.5:-12", "sentetik": "vurus@18.4", "riser": "18.4:1.0:-12", "sfx_max": 8,
  "vo": [{"dosya": "ses/vo1.mp3", "bas": 0.3, "db": 0}], "vo_duck_db": -10}
Çıktı: TESLIM/<ad>.mp4 (+ ses/ses_olc_<ad>.json). Çıkış = ses_olc --kapi çıkışı.
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _arac import FF, CUT, SFX, sfx_hazirla  # noqa: E402

SR = 48000


def r(c):
    subprocess.run([str(x) for x in c], check=True)


def vo_karistir(girdi, cikti, vo, duck_db, sure):
    """Müziği VO altında duck eder (sidechain), VO'yu ekler, −14 LUFS'a çeker."""
    cmd = [FF, "-v", "error", "-y", "-i", girdi]
    for v in vo:
        cmd += ["-i", v["dosya"]]
    parca, etiket = [], []
    for k, v in enumerate(vo):
        ms = int(round(v.get("bas", 0) * 1000))
        parca.append("[%d:a]adelay=%d|%d,volume=%sdB[v%d]" % (k + 1, ms, ms, v.get("db", 0), k))
        etiket.append("[v%d]" % k)
    parca.append("%samix=inputs=%d:normalize=0[vot]" % ("".join(etiket), len(vo)))
    parca.append("[vot]asplit=2[vok][vosc]")
    oran = max(2.0, abs(duck_db) / 2.0)
    parca.append("[0:a][vosc]sidechaincompress=threshold=0.02:ratio=%.1f:attack=15:release=350:makeup=1[duck]" % oran)
    parca.append("[duck][vok]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7[son]")
    cmd += ["-filter_complex", ";".join(parca), "-map", "0:v", "-map", "[son]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(sure), cikti]
    r(cmd)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ayar = os.path.abspath(sys.argv[1])
    D = os.path.dirname(ayar)
    a = json.load(open(ayar, encoding="utf-8"))
    s = a["ses"]
    ad = a["ad"]
    sure = float(a["sure"])
    video = sys.argv[sys.argv.index("--video") + 1] if "--video" in sys.argv else "hf/renders/%s_sessiz.mp4" % ad
    kesmeler = ",".join(str(x) for x in a["kesimler"])
    os.makedirs(os.path.join(D, "ses"), exist_ok=True)
    sfx_klasor = sfx_hazirla()
    pad = os.path.join(D, "ses", ad + "_pad.mp4")
    r([FF, "-v", "error", "-y", "-i", os.path.join(D, video), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-vf", "tpad=stop_mode=clone:stop_duration=2",
       "-t", sure + 2, "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", pad])
    drop, muzik_bas = float(s["drop"]), float(s["muzik_bas"])
    giris_hedef = float(s.get("giris_hedef", 8.0))
    taban, tavan = float(s.get("taban", 5.0)), float(s.get("tavan", 3.5))
    raw = subprocess.run([FF, "-v", "error", "-i", os.path.join(D, s["muzik"]), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    n0 = int(muzik_bas * SR)
    bas0 = max(0, n0 - int((drop + 0.5) * SR))
    rms = lambda z: 10 * np.log10((z ** 2).mean() + 1e-12)  # noqa: E731
    once = rms(x[bas0:n0]) if n0 > bas0 else -99
    sonra = rms(x[n0:n0 + int(4 * SR)])
    fark = sonra - once
    G = max(-6.0, min(18.0, fark - giris_hedef))
    g = np.ones(len(x))
    g[:n0] = 10 ** (G / 20)
    cf = int(0.12 * SR)
    if n0 > cf:
        g[n0 - cf:n0] = np.linspace(10 ** (G / 20), 1, cf)
    y = x * g[:, None]
    if taban > 0 and n0 > SR:  # giriş düzleme: sessiz boşluk → sıçrama olmasın
        h = int(0.1 * SR)
        m = n0 // h
        e = 10 * np.log10((y[:m * h].reshape(m, h, 2) ** 2).mean((1, 2)) + 1e-12)
        med = np.median(e[max(0, m - int((drop + 0.5) * 10)):])
        kz = np.clip((med - taban) - e, 0, 30) - np.clip(e - (med + tavan), 0, 30)
        gg = np.interp(np.arange(n0), (np.arange(m) + 0.5) * h, 10 ** (kz / 20))
        y[:n0] *= gg[:, None]
    y /= max(1.0, np.abs(y).max() / 0.95)
    duz = os.path.join(D, "ses", "muzik_duz.wav")
    with wave.open(duz, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((y * 32767).astype("<i2").tobytes())
    komp = os.path.join(D, "ses", "muzik_komp.wav")
    r([FF, "-v", "error", "-y", "-i", duz, "-af", s.get("komp", "acompressor=threshold=-22dB:ratio=3.5:attack=8:release=220:makeup=4"), komp])
    print("müzik: giriş %.1f dB · drop sonrası %.1f dB · fark %.1f → giriş kazancı %+.1f dB" % (once, sonra, fark, G))
    uzun = os.path.join(D, "ses", ad + "_uzun.mp4")
    stem = os.path.join(D, "ses", "stem_" + ad)
    c = [sys.executable, os.path.join(CUT, "ses_tasarla.py"), "--video", pad, "--muzik", komp, "--muzik_bas", muzik_bas, "--drop_video_sn", drop,
         "--muzik_fade_in", s.get("fade_in", 1.75), "--patlama_db", 0, "--crackle_db", 0, "--rolanti_db", 0, "--yankı_db", -60,
         "--muzik_db", s.get("muzik_db", 5.0), "--kesmeler", kesmeler, "--sessizlik_vurusu", s.get("sessizlik_vurusu", 0.2),
         "--sfx_db", s.get("sfx_db", 0.0), "--sfx_dosya", s["sfx"], "--sfx_klasor", sfx_klasor, "--son_fade", s.get("son_fade", 0.6),
         "--sfx_max_10sn", s.get("sfx_max", 8), "--drop_oncesi_db", s.get("drop_oncesi_db", -8.0), "--drop_esik_db", s.get("drop_esik_db", 6.0),
         "--stem_klasoru", stem, "--cikti", uzun]
    if s.get("sentetik"):
        c += ["--sfx", s["sentetik"]]
    if s.get("riser"):
        c += ["--riser", s["riser"]]
    p = subprocess.run([str(z) for z in c], capture_output=True, text=True)
    with open(os.path.join(D, "ses", "ses_tasarla_%s.log" % ad), "w") as f:
        f.write(p.stdout + "\n" + p.stderr)
    print("ses_tasarla çıkış", p.returncode, (p.stdout.strip().splitlines() or [""])[-1][:300])
    if p.returncode != 0:
        sys.exit(p.returncode)
    cikti = os.path.join(D, "TESLIM", ad + ".mp4")
    os.makedirs(os.path.dirname(cikti), exist_ok=True)
    ara = cikti if not s.get("vo") else os.path.join(D, "ses", ad + "_vosuz.mp4")
    r([FF, "-v", "error", "-y", "-i", uzun, "-t", sure, "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-af", "afade=t=out:st=%.2f:d=0.25" % (sure - 0.25), "-movflags", "+faststart", ara])
    muz = os.path.join(stem, "muz_teslim.wav")
    r([FF, "-v", "error", "-y", "-i", os.path.join(stem, "muz.wav"), "-t", sure, muz])
    if s.get("vo"):
        vo = [dict(v, dosya=os.path.join(D, v["dosya"])) for v in s["vo"]]
        vo_karistir(ara, cikti, vo, float(s.get("vo_duck_db", -10)), sure)
    o = subprocess.run([sys.executable, os.path.join(CUT, "ses_olc.py"), cikti, "--drop", str(drop), "--muzik_stem", muz, "--kapi"], capture_output=True, text=True)
    with open(os.path.join(D, "ses", "ses_olc_%s.json" % ad), "w") as f:
        f.write(o.stdout)
    try:
        j = json.loads(o.stdout)
        print("ses_olc --kapi çıkış", o.returncode, {k: j.get(k) for k in ("I_lufs", "true_peak_dbtp", "drop_artis_db", "delikler", "sure_sn")},
              "giris tuttu:", (j.get("muzik_giris") or {}).get("tuttu"), "sicrama:", (j.get("drop_disi_sicrama") or {}).get("asan"))
    except Exception:
        print("ses_olc çıkış", o.returncode, o.stdout[-600:], o.stderr[-400:])
    sys.exit(o.returncode)


if __name__ == "__main__":
    main()
