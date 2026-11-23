#!/usr/bin/env python3
"""Yerel alıcı: tarayıcı sayfasındaki veriyi (ör. ElevenLabs <audio> data: URI) yerel dosyaya yazar. Yalnız 127.0.0.1.

  python3 alici.py <klasör> [port=8765]
Sayfadan (javascript_tool):  fetch("http://127.0.0.1:8765/vo01.mp3", {method:"POST", body: audioEl.src})
  - gövde `data:<tür>;base64,<veri>` ise çözülüp <klasör>/<yol adı> olarak yazılır (ikili dosya);
  - değilse metin olarak yazılır. Klasör dışına yazmaz (yol adı yalnız dosya adı olabilir).
ChatGPT sayfası localhost bağlantısını CSP ile engeller; ElevenLabs engellemez. Chrome çoklu indirmeyi sessizce kestiği için indirme düğmesi yerine bu yöntem.
"""
import base64
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

KLASOR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else sys.exit(__doc__)
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
os.makedirs(KLASOR, exist_ok=True)


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
        ad = os.path.basename(self.path.split("?")[0]) or "gelen.bin"
        if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", ad):
            self.send_response(400)
            self.end_headers()
            return
        gov = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        m = re.match(rb"data:[^;,]*;base64,(.*)", gov, re.S)
        veri = base64.b64decode(m.group(1)) if m else gov
        with open(os.path.join(KLASOR, ad), "wb") as f:
            f.write(veri)
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(b"ok")
        print("yazıldı", ad, len(veri), "bayt", flush=True)

    def log_message(self, *a):
        pass


print("alıcı 127.0.0.1:%d → %s (Ctrl+C ile kapat)" % (PORT, KLASOR), flush=True)
HTTPServer(("127.0.0.1", PORT), H).serve_forever()
