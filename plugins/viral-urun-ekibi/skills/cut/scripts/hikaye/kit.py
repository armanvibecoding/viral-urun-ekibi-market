"""Hikâye hattı kiti: stok klibi 1080x1920@30'a hazırlar, kamera (zoom) sarmalayıcısı, index.html yazar."""
import os
import subprocess

from _arac import FF


def hazirla(src, dst, ss, sure, hiz=1.0, kirp=None, vf_ek="", zorla=False):
    """src'den ss'ten başlayıp (sure*hiz) sn kaynak alır, hız uygular, 1080x1920@30 yazar.
    kirp=(w,h,x,y) kaynak pikselinde; yoksa ortadan 9:16."""
    if os.path.exists(dst) and not zorla:
        return
    f = ["crop=%d:%d:%d:%d" % tuple(kirp)] if kirp else ["crop='min(iw,ih*9/16)':'min(ih,iw*16/9)'"]
    f.append("scale=1080:1920:flags=lanczos")
    if hiz != 1.0:
        f.append("setpts=PTS/%s" % hiz)
    f.append("fps=30")
    if vf_ek:
        f.append(vf_ek)
    cmd = [FF, "-v", "error", "-y", "-ss", str(ss), "-t", str(sure * hiz + 0.4), "-i", src, "-an",
           "-vf", ",".join(f), "-t", str(sure + 0.25), "-c:v", "libx264", "-crf", "15", "-preset", "medium",
           "-pix_fmt", "yuv420p", "-g", "15", "-movflags", "+faststart", dst]
    subprocess.run(cmd, check=True)


def vid(pid, f, bas, sure, z0=1.0, z1=1.05, origin="50% 45%", ease="none", track=0):
    p = (f'<div class="cam" id="{pid}cam" style="transform-origin:{origin}"><video id="{pid}" class="clip vid" src="assets/video/{f}" '
         f'data-start="{bas}" data-duration="{sure}" data-media-start="0" data-track-index="{track}" muted playsinline></video></div>')
    t = f'tl.fromTo("#{pid}cam",{{scale:{z0}}},{{scale:{z1},duration:{sure},ease:"{ease}"}},{bas});'
    return p, t


def yaz(K, P, T, css, sure):
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{css}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{sure}" data-width="1080" data-height="1920" data-fps="30">
{chr(10).join(P)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(T)}
window.__timelines["main"] = tl;
</script>
</body></html>
"""
    with open(os.path.join(K, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)


def tema_css(tema):
    """Tema değişkenleri (ayar 'tema'): renk ve yazı ailesi. Eksik anahtar varsayılanla tamamlanır."""
    v = {"navy": "#0A1030", "zemin": "#060a1e", "ivory": "#F6EFE6", "gold": "#E7C08F", "gold2": "#F2D3A6", "rose": "#D9A27E",
         "red": "#D8232F", "sari": "#F2C300", "serif": "'Playfair Display', serif", "sans": "'Inter', sans-serif"}
    v.update(tema or {})
    return ":root { " + " ".join("--%s:%s;" % (k, x) for k, x in v.items()) + " }\n"
