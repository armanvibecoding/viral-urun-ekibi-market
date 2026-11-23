#!/usr/bin/env python3
"""Mixkit stok aracı (v8). Lisans her klibin kendi sayfasından okunur; 'Restricted' olan listelenmez/indirilmez.
  mk.py tara <terim> [sayfa]        → Free lisanslı klipler: id · süre · çözünürlükler · slug
  mk.py on <çıktı.jpg> <id> ...     → 360p önizlemeden klip başına 6 karelik şerit (tek görsel)
  mk.py al <klasör> <id> ...        → 1080p (yoksa 720p) indirir, klasör/LISANS-ham.tsv'ye satır ekler"""
import sys, re, os, subprocess, concurrent.futures as cf, urllib.request
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
import sys as _s
_s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _arac import FF, FP
SP = os.environ.get("STOK_CALISMA", "stok_calisma")
os.makedirs(SP, exist_ok=True)
def get(u, bin=False):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60).read()
    return r if bin else r.decode("utf-8", "ignore")
def sayfa(slug):
    try: h = get("https://mixkit.co/free-stock-video/%s/" % slug)
    except Exception as e: return slug, "HATA", "", ""
    lis = "Restricted" if "Restricted License" in h else ("Free" if "Stock Video Free License" in h else "?")
    d = re.search(r'"duration":"PT(\d+)M(\d+)S"', h); sure = int(d.group(1))*60+int(d.group(2)) if d else 0
    coz = ",".join(sorted(set(re.findall(r'\b(\d{3,4}x\d{3,4})\b', h)) - {"180x180"}))
    return slug, lis, sure, coz
def slug_bul(i):
    # id'den slug: arama gerekmeden yönlendirme yok → önbellek dosyası
    for l in open(SP + "/mk_slug.tsv") if os.path.exists(SP + "/mk_slug.tsv") else []:
        a, b = l.strip().split("\t")
        if a == str(i): return b
    return None
k = sys.argv[1]
if k == "tara":
    t = sys.argv[2]; pg = sys.argv[3] if len(sys.argv) > 3 else "1"
    h = get("https://mixkit.co/free-stock-video/%s/%s" % (t, "" if pg == "1" else "?page=" + pg))
    sl = sorted(set(re.findall(r'free-stock-video/([a-z0-9-]+-\d+)/', h)))
    with cf.ThreadPoolExecutor(2) as ex: R = list(ex.map(sayfa, sl))
    with open(SP + "/mk_slug.tsv", "a") as f:
        for s, lis, sure, coz in R: f.write("%s\t%s\n" % (s.rsplit("-", 1)[1], s))
    n = 0
    for s, lis, sure, coz in R:
        if lis == "Free": print(s.rsplit("-", 1)[1], "%ss" % sure, coz, s.rsplit("-", 1)[0]); n += 1
    print("# %s: %d klip, %d Free" % (t, len(R), n))
elif k == "on":
    out = sys.argv[2]; ids = sys.argv[3:]; os.makedirs(SP + "/on", exist_ok=True); rows = []
    def bir(i):
        p = SP + "/on/%s.mp4" % i
        if not os.path.exists(p):
            for q in ("360", "720", "1080"):
                try: d = get("https://assets.mixkit.co/videos/%s/%s-%s.mp4" % (i, i, q), True); open(p, "wb").write(d); break
                except Exception: pass
        j = SP + "/on/%s.jpg" % i
        d = float(subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout or 6)
        subprocess.run([FF, "-v", "error", "-y", "-i", p, "-vf", "fps=6/%f,scale=-2:150,tile=6x1" % d, "-frames:v", "1", j])
        return j
    with cf.ThreadPoolExecutor(8) as ex: js = list(ex.map(bir, ids))
    from PIL import Image, ImageDraw
    ims = [Image.open(j).convert("RGB") for j in js]; W = max(i.width for i in ims)
    m = Image.new("RGB", (W, sum(i.height for i in ims))); y = 0
    for i, im in zip(ids, ims):
        m.paste(im, (0, y)); ImageDraw.Draw(m).text((4, y + 2), str(i), fill=(255, 255, 0)); y += im.height
    m.save(out, quality=80); print(out, m.size)
elif k == "al":
    d = sys.argv[2]; os.makedirs(d, exist_ok=True)
    for i in sys.argv[3:]:
        s = slug_bul(i); 
        if not s: print(i, "slug yok (önce tara)"); continue
        _, lis, sure, coz = sayfa(s)
        if lis != "Free": print(i, "LİSANS", lis, "→ indirilmedi"); continue
        p = os.path.join(d, "mx_%s.mp4" % i)
        if not os.path.exists(p):
            for q in ("1080", "720"):
                try: open(p, "wb").write(get("https://assets.mixkit.co/videos/%s/%s-%s.mp4" % (i, i, q), True)); break
                except Exception as e: q = None
            if not q: print(i, "indirilemedi"); continue
            open(os.path.join(d, "LISANS-ham.tsv"), "a").write("mx_%s.mp4\t%s\tMixkit Stock Video Free License (sayfadan okundu %s)" % __import__("datetime").date.today().isoformat() + "\t%sp\t%ss\n" % (i, s, q, sure))
        print(i, "tamam", os.path.getsize(p) // 1024, "KB", s)
