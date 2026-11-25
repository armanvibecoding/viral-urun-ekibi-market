"""muzik_sentez kırma testi: drop artışı her tonik/bpm'de ≥ 7 dB (kapı 6 + pay); drop_payi kapatılırsa düşük tonik kalmalı."""
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np

BURA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURA)
import muzik_sentez as ms  # noqa: E402


def oku(yol):
    with wave.open(yol) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32767
    return x.reshape(-1, 2)[:, 0]


def uret(tonik, bpm):
    d = tempfile.mkdtemp()
    yol = os.path.join(d, "m.wav")
    out = subprocess.run([sys.executable, os.path.join(BURA, "muzik_sentez.py"), yol, "--sure", "16",
                          "--tonik", str(tonik), "--bpm", str(bpm)], capture_output=True, text=True, check=True).stdout
    drop = float(out.strip().splitlines()[-1].split("=")[1])
    return oku(yol), drop


def main():
    hata = 0
    for tonik in (48, 52, 57, 62):
        for bpm in (90, 104, 120):
            x, drop = uret(tonik, bpm)
            a = ms.drop_artis(x, drop)
            ok = a >= 7.0
            hata += not ok
            print("%s tonik=%d bpm=%d drop_artis=%.1f dB" % ("GEÇTİ" if ok else "KALDI", tonik, bpm, a))
    # kırma: düz (drop'suz) sinyal tek başına kapıdan kalır, pay fonksiyonu onu hedefe taşımalı
    y = np.sin(np.linspace(0, 2000, 16 * ms.SR)) * 0.3
    y[int(4 * ms.SR):] *= 1.2  # ~1,6 dB artış
    z = ms.drop_payi(y, 4.0)
    a0, a1 = ms.drop_artis(y, 4.0), ms.drop_artis(z, 4.0)
    ok = a0 < 6 and a1 >= ms.HEDEF_DROP_DB - 0.5
    hata += not ok
    print("%s kırma: düz sinüs %.1f → %.1f dB" % ("GEÇTİ" if ok else "KALDI", a0, a1))
    sys.exit(1 if hata else 0)


if __name__ == "__main__":
    main()
