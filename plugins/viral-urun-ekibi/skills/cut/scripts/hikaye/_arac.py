"""Hikâye hattı ortak yardımcıları: ffmpeg/ffprobe bulma (cut/scripts/ffaraclar.py), PATH'e ekleme, komut çalıştırma."""
import os
import subprocess
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
CUT = os.path.dirname(BURADA)            # skills/cut/scripts
sys.path.insert(0, CUT)
import ffaraclar as _F  # noqa: E402

FF = _F.ffmpeg_bul()
FP = _F.ffprobe_bul() or "ffprobe"
os.environ["PATH"] = os.path.dirname(FF) + os.pathsep + os.environ.get("PATH", "")
SFX = os.environ.get("HIKAYE_SFX") or os.path.join(os.path.expanduser("~"), ".cache", "viral-urun-ekibi", "sfx")


def sfx_hazirla():
    """Sentetik efektleri (numpy; kendi üretimimiz, lisans gerekmez) ilk kullanımda önbelleğe (~/.cache/viral-urun-ekibi/sfx) üretir."""
    if not os.path.exists(os.path.join(SFX, "pop.wav")):
        subprocess.run([sys.executable, os.path.join(BURADA, "sfx", "sentez.py")], check=True, env=dict(os.environ, SFX_CIKTI=SFX))
    return SFX


def calis(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def sure(yol):
    r = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", yol], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0
