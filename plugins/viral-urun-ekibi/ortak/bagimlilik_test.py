#!/usr/bin/env python3
"""numpy/Pillow korumalı içe aktarma kırma testi: paket yokken betik ham ImportError yerine
"kurulum eksik: ... pip install ..." yazar ve çıkış 3 verir; paket varken (gerçek ortam) bu mesaj çıkmaz.
Çıkış 0 = hepsi geçti."""
import os
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# (betik, hangi paket yoksa düşmeli)
BETIKLER = [
    ("skills/studio/scripts/ekran_tasi.py", "numpy"), ("skills/cut/scripts/ses_olc.py", "numpy"),
    ("skills/cut/scripts/hizli_kurgu.py", "PIL"), ("skills/cut/scripts/hikaye/ses.py", "numpy"),
    ("skills/cut/scripts/hikaye/sfx/sentez.py", "numpy"), ("skills/cut/scripts/hikaye/kes.py", "numpy"),
    ("skills/cut/scripts/hikaye/pano.py", "PIL"), ("skills/cut/scripts/ses_tasarla.py", "numpy"),
    ("skills/cut/scripts/kurgu_kontrol.py", "numpy"), ("skills/builder/gorseller/scripts/duzelt.py", "PIL"),
    ("skills/builder/gorseller/scripts/sablon.py", "PIL"), ("skills/cut/hf-sablonlar/muzik_sentez.py", "numpy"),
]
sonuc = []
SFX_TMP = tempfile.mkdtemp(prefix="bagimlilik_sfx_")


def t(ad, ok, ayrinti=""):
    sonuc.append(bool(ok))
    print(("GEÇTİ " if ok else "KALDI ") + ad + ("" if ok else " | " + str(ayrinti)[:300]))


def kos(betik, pythonpath=None):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env["SFX_CIKTI"] = SFX_TMP  # sentez.py argümansız çalışır ve wav yazar: depoya değil geçici klasöre
    if pythonpath:
        env["PYTHONPATH"] = pythonpath
    return subprocess.run([sys.executable, os.path.join(KOK, betik), "--yardim-yok"], capture_output=True, text=True,
                          env=env, cwd=tempfile.gettempdir(), timeout=60)


with tempfile.TemporaryDirectory() as d:
    # paketi gizleyen sahte modüller: import anında ImportError
    for ad in ("numpy", "PIL"):
        os.makedirs(os.path.join(d, ad))
        with open(os.path.join(d, ad, "__init__.py"), "w") as f:
            f.write("raise ImportError('gizli test', name=%r)\n" % ad)
    for betik, paket in BETIKLER:
        r = kos(betik, d)
        cikti = r.stdout + r.stderr
        t("KIRMA %s: %s yok -> çıkış 3 + 'kurulum eksik' + pip komutu, ham Traceback yok" % (betik.split("/")[-1], paket),
          r.returncode == 3 and "kurulum eksik" in cikti and "pip install" in cikti and "Traceback" not in cikti,
          "çıkış %d: %s" % (r.returncode, cikti))
        r2 = kos(betik)
        t("paket varken %s 'kurulum eksik' demez" % betik.split("/")[-1], "kurulum eksik" not in r2.stdout + r2.stderr,
          r2.stdout + r2.stderr)
import shutil
shutil.rmtree(SFX_TMP, ignore_errors=True)
kalan = sonuc.count(False)
print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
sys.exit(1 if kalan else 0)
