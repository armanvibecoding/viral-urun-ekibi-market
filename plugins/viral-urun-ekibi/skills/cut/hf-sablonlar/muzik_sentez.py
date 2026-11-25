#!/usr/bin/env python3
"""Demo/test müziği üretici (numpy; kendi üretimimiz, lisans gerekmez): pad + hat'li giriş, bar sınırında DROP (kick+bas+clap+arp).

  python3 muzik_sentez.py cikti.wav [--sure 40] [--bpm 104] [--drop_bar 4] [--tonik 57]
Çıktının son satırı: "drop_sn=<saniye>" (ayar "muzik_bas" değeri). Gerçek yayında platform kütüphanesinden/lisanslı parça kullanılır;
bu üretici stok-hissi vermeden demoların ses kapılarını sınamak içindir. Kulakla dinlenmedi; ses_olc ile ölçülür.
Ölçüm notu (sınav 04, 2026-11-24): drop artışı (ses_tasarla drop_artis_db, eşik ≥ 6) tonikle değişir: tonik 57 → 6,1–6,9 dB; tonik 52 → 4,0–5,0 dB (düşük bas kulak/ölçüm penceresinde az yükselir). Kapıdan geçen demo için --tonik 57 kullan; eşik gevşetilmez.
"""
import sys
import wave

try:
    import numpy as np
except ImportError as _hata:  # ham ImportError yerine anlaşılır mesaj, çıkış 3 (kurulum eksik)
    print("kurulum eksik: '%s' paketi bulunamadı. Kur: python3 -m pip install --user numpy (Windows: py -3 -m pip install --user numpy)" % (_hata.name or "numpy"), file=sys.stderr)
    sys.exit(3)

SR = 48000


def arg(a, v):
    return type(v)(sys.argv[sys.argv.index(a) + 1]) if a in sys.argv else v


HEDEF_DROP_DB = 8.0   # kapı ≥ 6 dB (ses_olc/ses_tasarla); klip sesi + efekt karışımda oranı düşürür → 2 dB pay


def drop_artis(x, drop):
    """ses_olc.py ile aynı tanım: drop sonrası 0,43 sn RMS / drop öncesi (−0,6 … −0,05 sn) RMS, dB."""
    rr = lambda s: float(np.sqrt(np.mean(s ** 2)) + 1e-12)  # noqa: E731
    i = int(drop * SR)
    return 20 * np.log10(rr(x[i:i + int(0.43 * SR)]) / rr(x[i - int(0.6 * SR):i - int(0.05 * SR)]))


def drop_payi(x, drop, hedef=HEDEF_DROP_DB):
    """Drop artışı hedefin altındaysa drop öncesi son 0,6 sn'yi yumuşak rampayla kısar ("nefes" boşluğu).
    Tonikten bağımsız kapı payı sağlar (sınav 04: tonik 52 → 4–5 dB çıkıyordu)."""
    if drop * SR < SR or drop * SR + 0.43 * SR > len(x):
        return x
    a = drop_artis(x, drop)
    if a >= hedef:
        return x
    g = 10 ** ((a - hedef) / 20) * 0.97
    i = int(drop * SR)
    b0, b1 = i - int(1.0 * SR), i - int(0.6 * SR)
    zarf = np.ones(len(x))
    zarf[b0:b1] = np.linspace(1.0, g, b1 - b0)
    zarf[b1:i] = g
    return x * zarf


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out = sys.argv[1]
    sure, bpm, drop_bar, tonik = arg("--sure", 40.0), arg("--bpm", 104.0), arg("--drop_bar", 4), arg("--tonik", 57)
    N = int(sure * SR)
    x = np.zeros(N)
    rng = np.random.default_rng(11)
    beat = 60.0 / bpm
    bar = 4 * beat
    drop = drop_bar * bar
    hz = lambda m: 440.0 * 2 ** ((m - 69) / 12.0)  # noqa: E731

    def yerles(t0, s, g=1.0):
        i = int(t0 * SR)
        if i >= N:
            return
        s = s[: N - i]
        x[i:i + len(s)] += g * s

    def tt(d):
        return np.arange(int(d * SR)) / SR

    def pad(f, d, g):
        u = tt(d)
        s = sum(np.sin(2 * np.pi * f * (1 + dt) * u + ph) for dt, ph in ((0, 0), (0.004, 1.3), (-0.004, 2.1)))
        s += 0.4 * sum(np.sin(2 * np.pi * 2 * f * (1 + dt) * u) for dt in (0.002, -0.002))
        z = np.minimum(u / 0.25, 1) * np.minimum((d - u) / 0.4, 1)
        return g * s * z / 6

    def kick(g=1.0):
        u = tt(0.32)
        return g * np.sin(2 * np.pi * (48 + 110 * np.exp(-u * 28)) * u) * np.exp(-u * 11)

    def clap(g=1.0):
        u = tt(0.2)
        n = rng.standard_normal(len(u))
        n = n - np.convolve(n, np.ones(8) / 8, "same")
        return g * n * (np.exp(-u * 30) + 0.6 * np.exp(-np.maximum(u - 0.012, 0) * 38))

    def hat(g=1.0):
        u = tt(0.07)
        n = rng.standard_normal(len(u))
        n = n - np.convolve(n, np.ones(4) / 4, "same")
        return g * n * np.exp(-u * 70)

    def bas(f, d, g):
        u = tt(d)
        return g * np.sin(2 * np.pi * f * u) * np.minimum(u / 0.01, 1) * np.minimum((d - u) / 0.05, 1)

    def pluck(f, g):
        u = tt(0.3)
        return g * (np.sin(2 * np.pi * f * u) + 0.3 * np.sin(2 * np.pi * 2 * f * u)) * np.exp(-u * 11)

    # Am7 – Fmaj7 – C – G (tonik = A3 = 57), bar başına bir akor
    akorlar = [(0, 3, 7, 10), (-4, 0, 3, 7), (3, 7, 10, 14), (-2, 2, 5, 9)]
    kok = [0, -4, 3, -2]
    for b in range(int(sure / bar) + 1):
        t0 = b * bar
        ak = akorlar[b % 4]
        for m in ak:
            yerles(t0, pad(hz(tonik + m), bar + 0.3, 0.55 if t0 < drop else 0.40))
        for k in range(8):                                   # giriş ve drop sonrası kapalı hat
            yerles(t0 + k * beat / 2, hat(0.16 if t0 < drop else 0.22), 1.0)
        if t0 >= drop:
            for k in range(4):
                yerles(t0 + k * beat, kick(0.95))
            yerles(t0 + beat, clap(0.45))
            yerles(t0 + 3 * beat, clap(0.45))
            for k in range(8):
                yerles(t0 + k * beat / 2, bas(hz(tonik - 24 + kok[b % 4]), beat / 2 * 0.9, 0.5))
                yerles(t0 + k * beat / 2 + beat / 4, pluck(hz(tonik + 12 + ak[k % 4]), 0.16))
        elif b == drop_bar - 1:                              # drop öncesi son bar: yükselen hat kaldırımı
            for k in range(8):
                yerles(t0 + bar - 0.25 + k * 0.03, hat(0.12 + 0.02 * k))
    x = drop_payi(x, drop)
    x /= max(1.0, np.abs(x).max() / 0.9)
    y = np.stack([x, np.roll(x, 40)], 1)                      # hafif stereo genişlik (≈0,8 ms)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((y * 32767).astype("<i2").tobytes())
    print("drop_sn=%.3f" % drop)


if __name__ == "__main__":
    main()
