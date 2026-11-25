#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yerel web ölçümü: üretilen HTML'de Lighthouse (hız / Core Web Vitals) + axe-core (WCAG 2.2 AA). Probe `hiz` ve `erisim` modlarının ölçen betiği.

  python3 web_olcum.py kontrol                         araç kurulu mu, sürümler sabit mi, Chrome var mı (çıkış 0 ya da 3)
  python3 web_olcum.py kur                             araçları AYRI klasöre, sürümleri SABİT kurar (global kurulum yok; --ignore-scripts)
  python3 web_olcum.py hiz|erisim|hepsi HEDEF [HEDEF…] [--kosu 3] [--json YOL]
        HEDEF: .html dosyası · .html'li klasör (üst düzey) · http(s) URL (canlı mağaza).
        Dosya/klasör yerel 127.0.0.1 sunucusundan açılır ve çıktıda "yerel" etiketiyle yazılır; URL "canlı" etiketini alır.
        "yerel" ölçüm laboratuvar ölçümüdür: ağ, üçüncü taraf uygulama, gerçek görsel ve alan verisi (CrUX) YOKTUR; canlı mağaza
        sayısı yerine geçmez, yalnız üretilen HTML'in kendi kusurunu yakalar.

Kapılar (eşik gevşetilmez; Google "iyi" sınırı ve WCAG 2.2 AA):
  hiz     Lighthouse mobil profili (390 px, 4× CPU, yavaş 4G benzetimi), --kosu koşunun MEDYANI:
          LCP ≤ 2500 ms · CLS ≤ 0,1 · TBT ≤ 200 ms (INP laboratuvarda ölçülemez; TBT onun vekilidir, raporda öyle yazılır)
  erisim  axe-core, etiketler wcag2a/2aa/21a/21aa/22aa, 390 px ve 1440 px: tek ihlal = KALDI (kontrast, alt metin, etiket, hedef boyutu…).
          axe'in "incomplete" (insan bakışı gerekir) sonuçları UYARI olarak yazılır, geçti yerine sayılmaz ama KALDI da yapmaz.
Çıkış: 0 hepsi GEÇTİ · 1 en az bir KALDI · 3 ölçülemedi (araç/Chrome yok ya da ölçüm çalışmadı; geçti sayılmaz) · 2 kullanım.

Araçlar (arac-ekle kapısı, 2026-11-25): lighthouse@13.6.0 (GoogleChrome/lighthouse), axe-core@4.14.0 (dequelabs/axe-core),
puppeteer-core@25.18.1 (Lighthouse'un kendi bağımlılığı; tarayıcı indirmez), hepsi `~/.local/share/viral-urun-ekibi/web-olcum/` altında
(WEB_OLCUM_DIZIN ile değişir). Chrome: CHROME_PATH ya da macOS/Linux standart yolları.
"""
import argparse
import functools
import http.server
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import threading

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BURASI = os.path.dirname(os.path.abspath(__file__))
DIZIN = os.environ.get("WEB_OLCUM_DIZIN") or os.path.join(os.path.expanduser("~"), ".local", "share", "viral-urun-ekibi", "web-olcum")
SABIT = {"lighthouse": "13.6.0", "axe-core": "4.14.0", "puppeteer-core": "25.18.1"}
ESIK = {"lcp_ms": 2500.0, "cls": 0.1, "tbt_ms": 200.0}
GENISLIKLER = (390, 1440)
CHROME_ADAYLAR = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium",
                  "google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
OLCULEMEDI, GECTI, KALDI = "olculemedi", "GEÇTİ", "KALDI"


def chrome_yolu():
    c = os.environ.get("CHROME_PATH")
    if c:
        return c if os.path.isfile(c) else None
    for a in CHROME_ADAYLAR:
        y = a if os.path.isabs(a) else shutil.which(a)
        if y and os.path.isfile(y):
            return y
    return None


def node_surumu():
    n = shutil.which("node")
    if not n:
        return None, "node yok (Node 22.19+ gerekir)"
    try:
        v = subprocess.run([n, "--version"], capture_output=True, text=True, timeout=20).stdout.strip().lstrip("v")
        sayilar = tuple(int(x) for x in v.split(".")[:3])
    except (OSError, ValueError, subprocess.SubprocessError):
        return None, "node sürümü okunamadı"
    if sayilar < (22, 19, 0):
        return None, "node %s çok eski (Lighthouse 13: ≥ 22.19)" % v
    return n, v


def kurulu_surum(paket):
    y = os.path.join(DIZIN, "node_modules", *paket.split("/"), "package.json")
    try:
        with open(y, encoding="utf-8") as f:
            return json.load(f).get("version")
    except (OSError, ValueError):
        return None


def araclar():
    """(tamam, [eksik/sorun açıklamaları])."""
    sorun = []
    n, v = node_surumu()
    if not n:
        sorun.append(v)
    if not chrome_yolu():
        sorun.append("Chrome/Chromium bulunamadı (CHROME_PATH ile yol ver)")
    for p, s in SABIT.items():
        k = kurulu_surum(p)
        if k is None:
            sorun.append("%s kurulu değil (%s): python3 web_olcum.py kur" % (p, DIZIN))
        elif k != s:
            sorun.append("%s sürümü %s, sabit sürüm %s (sürüm sabit tutulur; `kur` ile düzelt)" % (p, k, s))
    return (not sorun), sorun


def kur():
    n, v = node_surumu()
    npm = shutil.which("npm")
    if not n or not npm:
        print("YAPILAMAZ: %s" % (v if not n else "npm yok"))
        return 3
    os.makedirs(DIZIN, exist_ok=True)
    pj = os.path.join(DIZIN, "package.json")
    if not os.path.isfile(pj):
        with open(pj, "w", encoding="utf-8") as f:
            json.dump({"name": "web-olcum", "private": True, "version": "1.0.0",
                       "description": "viral-urun-ekibi yerel Lighthouse + axe ölçümü (sürüm sabit)"}, f)
    r = subprocess.run([npm, "install", "--save-exact", "--ignore-scripts", "--no-audit", "--no-fund"] + ["%s@%s" % kv for kv in SABIT.items()],
                       cwd=DIZIN, capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-600:])
    tamam, sorun = araclar()
    for s in sorun:
        print("SORUN:", s)
    return 0 if tamam else 3


class _Sessiz(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def sunucu_ac(klasor):
    h = functools.partial(_Sessiz, directory=klasor)
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def hedefleri_coz(hedefler):
    """[(etiket, ad, klasör ya da None, yol/url)]: URL → canlı; dosya/klasör → yerel."""
    out = []
    for h in hedefler:
        if re.match(r"^https?://", h):
            out.append(("canlı", h, None, h))
        elif os.path.isdir(h):
            dosyalar = sorted(f for f in os.listdir(h) if f.lower().endswith((".html", ".htm")))
            for f in dosyalar:
                out.append(("yerel", f, os.path.abspath(h), f))
        elif os.path.isfile(h):
            out.append(("yerel", os.path.basename(h), os.path.dirname(os.path.abspath(h)), os.path.basename(h)))
        else:
            raise SystemExit("HATA: hedef yok: %s" % h)
    if not out:
        raise SystemExit("HATA: ölçülecek .html bulunamadı: %s" % ", ".join(hedefler))
    return out


def lighthouse_kos(url):
    lh = os.path.join(DIZIN, "node_modules", ".bin", "lighthouse")
    with tempfile.TemporaryDirectory() as t:
        cikti = os.path.join(t, "lh.json")
        env = dict(os.environ, CHROME_PATH=chrome_yolu() or "")
        r = subprocess.run([lh, url, "--output=json", "--output-path=" + cikti, "--only-categories=performance", "--quiet",
                            "--chrome-flags=--headless=new --disable-gpu", "--max-wait-for-load=45000"],
                           capture_output=True, text=True, env=env, timeout=240)
        if r.returncode != 0 or not os.path.isfile(cikti):
            raise RuntimeError("lighthouse çıkış %d: %s" % (r.returncode, " ".join((r.stdout + r.stderr).split())[-240:]))
        with open(cikti, encoding="utf-8") as f:
            d = json.load(f)
    a = d["audits"]
    if d.get("runtimeError"):
        raise RuntimeError("lighthouse runtimeError: %s" % d["runtimeError"].get("message", "")[:200])
    return {"lcp_ms": a["largest-contentful-paint"]["numericValue"], "cls": a["cumulative-layout-shift"]["numericValue"],
            "tbt_ms": a["total-blocking-time"]["numericValue"], "skor": (d["categories"]["performance"].get("score")),
            "benchmark": d.get("environment", {}).get("benchmarkIndex"), "surum": d.get("lighthouseVersion")}


def hiz_olc(url, kosu):
    kayitlar = [lighthouse_kos(url) for _ in range(kosu)]
    med = {k: statistics.median(x[k] for x in kayitlar) for k in ESIK}
    nedenler = []
    if med["lcp_ms"] > ESIK["lcp_ms"]:
        nedenler.append("LCP %.0f ms > %.0f" % (med["lcp_ms"], ESIK["lcp_ms"]))
    if med["cls"] > ESIK["cls"]:
        nedenler.append("CLS %.3f > %g" % (med["cls"], ESIK["cls"]))
    if med["tbt_ms"] > ESIK["tbt_ms"]:
        nedenler.append("TBT %.0f ms > %.0f (INP vekili)" % (med["tbt_ms"], ESIK["tbt_ms"]))
    return {"durum": KALDI if nedenler else GECTI, "kosu": kosu, "medyan": med, "nedenler": nedenler,
            "lighthouse": kayitlar[0]["surum"], "benchmark": kayitlar[0]["benchmark"],
            "kayitlar": [{k: x[k] for k in ("lcp_ms", "cls", "tbt_ms")} for x in kayitlar]}


def axe_kos(url, genislik):
    node = shutil.which("node")
    r = subprocess.run([node, os.path.join(BURASI, "web_olcum_axe.mjs"), DIZIN, chrome_yolu(), url, str(genislik)],
                       capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        raise RuntimeError("axe çıkış %d: %s" % (r.returncode, " ".join((r.stdout + r.stderr).split())[-240:]))
    return json.loads(r.stdout.strip().splitlines()[-1])


def erisim_olc(url):
    ihlal, incomplete, surum = [], [], None
    for g in GENISLIKLER:
        d = axe_kos(url, g)
        surum = d["axe"]
        for v in d["ihlaller"]:
            ihlal.append(dict(v, genislik=g))
        for v in d["incomplete"]:
            incomplete.append(dict(v, genislik=g))
    return {"durum": KALDI if ihlal else GECTI, "axe": surum, "etiketler": "wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa",
            "ihlaller": ihlal, "gozle_bakilacak": incomplete}


def olc(hedefler, mod, kosu):
    tamam, sorun = araclar()
    if not tamam:
        return [{"etiket": "-", "ad": "-", "durum": OLCULEMEDI, "neden": "; ".join(sorun)}]
    sonuc = []
    servisler = {}
    try:
        for etiket, ad, klasor, yol in hedefleri_coz(hedefler):
            if klasor:
                if klasor not in servisler:
                    servisler[klasor] = sunucu_ac(klasor)
                url = "http://127.0.0.1:%d/%s" % (servisler[klasor].server_address[1], yol)
            else:
                url = yol
            k = {"etiket": etiket, "ad": ad}
            try:
                if mod in ("hiz", "hepsi"):
                    k["hiz"] = hiz_olc(url, kosu)
                if mod in ("erisim", "hepsi"):
                    k["erisim"] = erisim_olc(url)
            except (RuntimeError, subprocess.SubprocessError, OSError, ValueError, KeyError) as e:
                k["hata"] = "%s: %s" % (type(e).__name__, str(e)[:300])
            sonuc.append(k)
    finally:
        for s in servisler.values():
            s.shutdown()
    return sonuc


def kapi_durumu(sonuc, kapi):
    """kapi: hiz | erisim → GEÇTİ/KALDI/olculemedi (tek hedefte bile ölçülemeyen varsa ölçülemedi, KALDI hepsinden önce)."""
    d = []
    for k in sonuc:
        if k.get("durum") == OLCULEMEDI or k.get("hata"):
            d.append(OLCULEMEDI)
        elif kapi in k:
            d.append(k[kapi]["durum"])
    if KALDI in d:
        return KALDI
    if OLCULEMEDI in d or not d:
        return OLCULEMEDI
    return GECTI


def yazdir(sonuc, mod):
    for k in sonuc:
        if k.get("durum") == OLCULEMEDI:
            print("ÖLÇÜLEMEDİ: %s" % k["neden"])
            continue
        print("[%s] %s" % (k["etiket"], k["ad"]))
        if k.get("hata"):
            print("  ÖLÇÜLEMEDİ: %s" % k["hata"])
        if "hiz" in k:
            h = k["hiz"]
            m = h["medyan"]
            print("  hiz     %-6s LCP %.0f ms · CLS %.3f · TBT %.0f ms (medyan %d koşu, Lighthouse %s, benchmark %s)%s"
                  % (h["durum"], m["lcp_ms"], m["cls"], m["tbt_ms"], h["kosu"], h["lighthouse"], h["benchmark"],
                     " — " + "; ".join(h["nedenler"]) if h["nedenler"] else ""))
        if "erisim" in k:
            e = k["erisim"]
            print("  erisim  %-6s axe %s: %d ihlal kuralı%s" % (e["durum"], e["axe"], len(e["ihlaller"]),
                  "" if not e["ihlaller"] else " — " + "; ".join("%s×%d (%s, %d px)" % (v["kural"], v["adet"], v["etki"], v["genislik"]) for v in e["ihlaller"][:6])))
            for v in e["ihlaller"][:3]:
                for o in v["ornek"][:1]:
                    print("          · %s: %s" % (v["kural"], (o["secici"] + " " + o["ozet"])[:200]))
            if e["gozle_bakilacak"]:
                print("          UYARI: axe 'incomplete' (gözle bakılacak, geçti sayılmaz): %s"
                      % ", ".join(sorted({v["kural"] for v in e["gozle_bakilacak"]})))
    etiketler = sorted({k.get("etiket", "-") for k in sonuc} - {"-"}) or ["-"]
    ozet = " · ".join("%s: %s" % (kp, kapi_durumu(sonuc, kp)) for kp in (("hiz", "erisim") if mod == "hepsi" else (mod,)))
    print("WEB ÖLÇÜM (%s) %s" % ("/".join(etiketler), ozet))


def cikis_kodu(sonuc, mod):
    d = [kapi_durumu(sonuc, kp) for kp in (("hiz", "erisim") if mod == "hepsi" else (mod,))]
    return 1 if KALDI in d else (3 if OLCULEMEDI in d else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("komut", choices=["kontrol", "kur", "hiz", "erisim", "hepsi"])
    ap.add_argument("hedef", nargs="*")
    ap.add_argument("--kosu", type=int, default=3, help="hız ölçümünde koşu sayısı (medyan); varsayılan 3")
    ap.add_argument("--json", help="ayrıntılı sonucu bu dosyaya yaz")
    a = ap.parse_args()
    if a.komut == "kur":
        return kur()
    if a.komut == "kontrol":
        tamam, sorun = araclar()
        print("WEB ÖLÇÜM ARAÇLARI: %s (%s)" % ("TAMAM" if tamam else "EKSİK", DIZIN))
        for s in sorun:
            print("  EKSİK:", s)
        return 0 if tamam else 3
    if not a.hedef:
        ap.error("hedef gerekli (.html, klasör ya da URL)")
    if a.kosu < 1:
        ap.error("--kosu en az 1")
    sonuc = olc(a.hedef, a.komut, a.kosu)
    yazdir(sonuc, a.komut)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"mod": a.komut, "esik": ESIK, "sonuc": sonuc}, f, ensure_ascii=False, indent=2)
    return cikis_kodu(sonuc, a.komut)


if __name__ == "__main__":
    sys.exit(main())
