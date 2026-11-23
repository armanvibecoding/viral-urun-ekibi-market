#!/usr/bin/env python3
"""Pexels video stok aracı (lisans: pexels.com/license — ücretsiz, ticari serbest, atıf gerekmez; tanınabilir kişi kötü ışıkta gösterilemez
→ yüzsüz planlar seç). Her indirilen klip için klasör/LISANS-ham.tsv'ye satır yazılır (tarif 02 lisans kaydı).

Çalışma klasörü: --calisma (varsayılan ./stok_calisma). Arama sonucu dosyaları: <calisma>/px/*.txt, biçim:
  #<sorgu>!<id>~<slug>~<önizleme dosya adı>~<hd dosya adı>!<id>~...        (dosya adı = videos.pexels.com/video-files/<id>/<dosya>)

  stok_px.py api <sorgu> [adet]                  → Pexels API (ücretsiz anahtar: env PEXELS_API_KEY) ile arar, px/api_*.txt yazar
  stok_px.py alici [port]                        → Chrome yöntemi için yerel alıcı (127.0.0.1:8765): sayfa içi fetch sonucu POST edilir → px/chrome_*.txt
  stok_px.py liste                               → sorgular ve aday sayıları
  stok_px.py on <sorgu> [adet] [atla]            → 3 sütunlu önizleme panosu (klip başına 4 kare) → <calisma>/on/_<sorgu>_<atla>.jpg
  stok_px.py al <klasör> <id> ...                → HD klibi indirir + LISANS-ham.tsv satırı
Chrome yöntemi: pexels.com sekmesinde (kullanıcının açık oturumu, giriş yok) arama sayfasını aç; sayfa içi fetch ile sonuçları yukarıdaki biçime çevirip
alıcıya POST et (curl doğrudan 403 alır). Anahtar varsa `api` daha sağlamdır.
"""
import concurrent.futures as cf
import glob
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _arac import FF, sure, akis_bilgi  # noqa: E402

args = sys.argv[1:]
CAL = "stok_calisma"
if "--calisma" in args:
    i = args.index("--calisma")
    CAL = args[i + 1]
    del args[i:i + 2]
UA = {"User-Agent": "Mozilla/5.0"}


def yukle():
    Q, V, cur = {}, {}, None
    for f in sorted(glob.glob(os.path.join(CAL, "px", "*.txt"))):
        for l in open(f, encoding="utf-8").read().split("!"):
            if l.startswith("#"):
                cur = l[1:]
                Q.setdefault(cur, [])
            elif l.count("~") == 3 and cur is not None:
                i, s, a, h = l.strip().split("~")
                V[i] = (s, a, h)
                if i not in Q[cur]:
                    Q[cur].append(i)
    return Q, V


def get(u, p):
    if os.path.exists(p) and os.path.getsize(p) > 1000:
        return
    open(p, "wb").write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120).read())


def api(sorgu, adet):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        sys.exit("PEXELS_API_KEY yok (pexels.com/api ücretsiz). Anahtarsız yol: Chrome yöntemi (başlıktaki açıklama).")
    u = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": sorgu, "orientation": "portrait", "per_page": adet})
    j = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": key, "User-Agent": "Mozilla/5.0"}), timeout=60).read())
    parcalar = ["#" + sorgu]
    for v in j.get("videos", []):
        f = sorted([x for x in v.get("video_files", []) if x.get("file_type") == "video/mp4"], key=lambda x: x.get("width", 0))
        if not f:
            continue
        ad = lambda x: x["link"].rsplit("/", 1)[-1]  # noqa: E731
        sd = next((x for x in f if x.get("width", 0) >= 360), f[0])
        hd = next((x for x in reversed(f) if x.get("width", 0) <= 1080), f[-1])
        slug = v["url"].rstrip("/").rsplit("/", 1)[-1]
        parcalar.append("%s~%s~%s~%s" % (v["id"], slug, ad(sd), ad(hd)))
    os.makedirs(os.path.join(CAL, "px"), exist_ok=True)
    p = os.path.join(CAL, "px", "api_%s.txt" % "".join(c if c.isalnum() else "_" for c in sorgu))
    open(p, "w", encoding="utf-8").write("!".join(parcalar))
    print(p, len(parcalar) - 1, "aday")


def alici(port):
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class H(BaseHTTPRequestHandler):
        def _cors(self):
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

        def do_OPTIONS(self):
            self.send_response(204)
            self._cors()
            self.end_headers()

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            gov = self.rfile.read(n).decode("utf-8", "ignore")
            os.makedirs(os.path.join(CAL, "px"), exist_ok=True)
            ad = "chrome_%d.txt" % len(glob.glob(os.path.join(CAL, "px", "chrome_*.txt")))
            open(os.path.join(CAL, "px", ad), "w", encoding="utf-8").write(gov)
            self.send_response(200)
            self._cors()
            self.end_headers()
            self.wfile.write(b"ok")
            print("alındı", ad, len(gov), "bayt", flush=True)

        def log_message(self, *a):
            pass
    print("alıcı 127.0.0.1:%d (Ctrl+C ile kapat)" % port, flush=True)
    HTTPServer(("127.0.0.1", port), H).serve_forever()


def main():
    if not args:
        sys.exit(__doc__)
    k = args[0]
    if k == "api":
        return api(args[1], int(args[2]) if len(args) > 2 else 15)
    if k == "alici":
        return alici(int(args[1]) if len(args) > 1 else 8765)
    Q, V = yukle()
    if k == "liste":
        for q in Q:
            print(q, len(Q[q]))
    elif k == "on":
        from PIL import Image, ImageDraw
        q = args[1]
        n = int(args[2]) if len(args) > 2 else 12
        at = int(args[3]) if len(args) > 3 else 0
        ids = Q[q][at:at + n]
        od = os.path.join(CAL, "on")
        os.makedirs(od, exist_ok=True)

        def bir(i):
            p = os.path.join(od, "px_%s.mp4" % i)
            j = os.path.join(od, "px_%s.jpg" % i)
            try:
                get("https://videos.pexels.com/video-files/%s/%s" % (i, V[i][1]), p)
                d = sure(p) or 6.0
                subprocess.run([FF, "-v", "error", "-y", "-i", p, "-vf", "fps=4/%f,scale=90:160:force_original_aspect_ratio=increase,crop=90:160,tile=4x1" % d, "-frames:v", "1", j])
                return i, j, d
            except Exception:
                return i, None, 0
        with cf.ThreadPoolExecutor(6) as ex:
            R = [r for r in ex.map(bir, ids) if r[1] and os.path.exists(r[1])]
        kol = 3
        sat = (len(R) + kol - 1) // kol
        m = Image.new("RGB", (kol * 366, sat * 164), (30, 30, 30))
        dr = ImageDraw.Draw(m)
        for k2, (i, j, d) in enumerate(R):
            x, y = (k2 % kol) * 366, (k2 // kol) * 164
            m.paste(Image.open(j).convert("RGB"), (x, y))
            dr.rectangle((x, y, x + 120, y + 12), fill=(0, 0, 0))
            dr.text((x + 2, y), "%s %ds" % (i, d), fill=(255, 255, 0))
        o = os.path.join(od, "_%s_%d.jpg" % (q.replace(" ", "_"), at))
        m.save(o, quality=72)
        print(o)
        print(" ".join("%s:%s" % (i, V[i][0][:28]) for i, _, _ in R))
    elif k == "al":
        d = args[1]
        os.makedirs(d, exist_ok=True)
        for i in args[2:]:
            p = os.path.join(d, "px_%s.mp4" % i)
            yeni = not os.path.exists(p)
            get("https://videos.pexels.com/video-files/%s/%s" % (i, V[i][2]), p)
            w = akis_bilgi(p)
            if yeni:
                open(os.path.join(d, "LISANS-ham.tsv"), "a", encoding="utf-8").write("px_%s.mp4\thttps://www.pexels.com/video/%s/\tPexels License\t%s\n" % (i, V[i][0], w))
            print(i, os.path.getsize(p) // 1024, "KB", w, V[i][0])
    else:
        sys.exit(__doc__)


main()
