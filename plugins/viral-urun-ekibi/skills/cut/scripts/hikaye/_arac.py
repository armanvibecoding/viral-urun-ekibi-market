"""Hikâye hattı ortak yardımcıları: ffmpeg/ffprobe bulma (cut/scripts/ffaraclar.py), PATH'e ekleme, komut çalıştırma."""
import os
import subprocess
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
CUT = os.path.dirname(BURADA)            # skills/cut/scripts
sys.path.insert(0, CUT)
import ffaraclar as _F  # noqa: E402

try:
    FF = _F.ffmpeg_bul()
except SystemExit as _e:   # ffaraclar kurulum talimatıyla çıkar; traceback yerine net Türkçe hata
    print("HATA: ffmpeg bulunamadı. Kur: " + _F.kurulum_talimati(), file=sys.stderr)
    sys.exit(3)
FP = _F.ffprobe_bul()   # yoksa None: süre/bilgi `ffmpeg -i` çıktısından okunur
os.environ["PATH"] = os.path.dirname(FF) + os.pathsep + os.environ.get("PATH", "")
SFX = os.environ.get("HIKAYE_SFX") or os.path.join(os.path.expanduser("~"), ".cache", "viral-urun-ekibi", "sfx")


def sfx_hazirla():
    """Sentetik efektleri (numpy; kendi üretimimiz, lisans gerekmez) ilk kullanımda önbelleğe (~/.cache/viral-urun-ekibi/sfx) üretir."""
    if not os.path.exists(os.path.join(SFX, "pop.wav")):
        subprocess.run([sys.executable, os.path.join(BURADA, "sfx", "sentez.py")], check=True, env=dict(os.environ, SFX_CIKTI=SFX))
    return SFX


def calis(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def _ffmpeg_i(yol):
    r = subprocess.run([FF, "-hide_banner", "-i", yol], capture_output=True, text=True)
    return r.stderr


def sure(yol):
    """Saniye cinsinden süre: ffprobe varsa o, yoksa `ffmpeg -i` çıktısındaki Duration."""
    import re
    if FP:
        r = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", yol], capture_output=True, text=True)
        try:
            return float(r.stdout.strip())
        except ValueError:
            pass
    m = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", _ffmpeg_i(yol))
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0


def akis_bilgi(yol):
    """'1080x1920 30 fps' gibi kısa video akışı özeti (ffprobe gerekmez)."""
    import re
    m = re.search(r"Video:.*?(\d{2,5}x\d{2,5}).*?(\d+(?:\.\d+)?) fps", _ffmpeg_i(yol))
    return "%s %s fps %.1fs" % (m.group(1), m.group(2), sure(yol)) if m else "%.1fs" % sure(yol)
