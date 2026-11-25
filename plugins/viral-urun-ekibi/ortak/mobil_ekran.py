#!/usr/bin/env python3
"""Mobil ekran alma yardımcısı: sayfayı GENİŞ pencerede, 390 px genişliğinde bir iframe içinde açıp o iframe'i keser.

Neden (2026-11-25 sınav 07): headless Chrome'da `--window-size=390,…` pencereyi en az ~500 px yapar; sayfa 500 px düzenle çizilip 390 px'e
KIRPILIR ve görüntüde yazı sağdan kesilir (yatay taşma gibi görünür; yöntem hatası). Doğru yöntem: geniş pencere + 390 px iframe.

  python3 mobil_ekran.py ekran SAYFA.html|URL CIKTI.png [--genislik 390] [--yukseklik 844]
        iframe'i keser, CIKTI.png yazar. Sayfanın kendi yatay taşması (scrollWidth > genişlik) varsa çıkış 1.
  python3 mobil_ekran.py kontrol SAYFA.html EKRAN.png
        Verilen mobil ekran görüntüsü doğru yöntemle alınmış mı: aynı sayfa iframe'le yeniden çizilir, ortalama piksel farkı
        > 6 ise "MOBİL EKRAN YANLIŞ ALINMIŞ" (çıkış 1). Kırma ölçümü: yanlış (500 px düzenle kırpılmış) 12,5 · doğru 0,0.
Çıkış: 0 tamam · 1 taşma/yanlış ekran · 2 kullanım/ortam hatası (Chrome yok → ölçülemedi) · yöntem sonucu uydurmaz.
Chrome yolu: ortam değişkeni CHROME_YOLU, yoksa macOS'taki Google Chrome, yoksa PATH'te google-chrome/chromium, yoksa Windows'ta
%ProgramFiles%, %ProgramFiles(x86)% ya da %LOCALAPPDATA% altındaki Google\\Chrome\\Application\\chrome.exe.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

FARK_ESIK = 6.0


def windows_adaylari():
    """Windows Chrome kurulum yolları (ortam değişkenlerinden; yoksa boş). Sabit C:\\ yolu varsayılmaz."""
    out = []
    for ort in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        k = os.environ.get(ort)
        if k:
            out.append(os.path.join(k, "Google", "Chrome", "Application", "chrome.exe"))
    return out


def chrome():
    adaylar = [os.environ.get("CHROME_YOLU", ""), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
               shutil.which("google-chrome") or "", shutil.which("chromium") or "", shutil.which("chromium-browser") or ""]
    adaylar += windows_adaylari() + [shutil.which("chrome") or ""]
    return next((a for a in adaylar if a and os.path.exists(a)), None)


def adres(s):
    return s if re.match(r"^https?://|^file://", s) else "file://" + os.path.abspath(s)


def sarmal(sayfa, genislik, yukseklik, dizin):
    yol = os.path.join(dizin, "sarmal.html")
    with open(yol, "w", encoding="utf-8") as f:
        f.write('<!doctype html><html><body style="margin:0;background:#fff"><iframe id="f" src="%s" width="%d" height="%d" '
                'style="border:0;display:block"></iframe><script>document.getElementById("f").onload=function(){try{'
                'document.body.setAttribute("data-sw",this.contentDocument.documentElement.scrollWidth)}catch(e){'
                'document.body.setAttribute("data-sw","yok")}}</script></body></html>' % (adres(sayfa), genislik, yukseklik))
    return yol


def al(sayfa, cikti, genislik=390, yukseklik=844):
    """(kare_yolu, scrollWidth ya da None). Chrome yoksa SystemExit(2)."""
    ch = chrome()
    if not ch:
        print("OLCULEMEDI: Chrome bulunamadı (CHROME_YOLU ver).", file=sys.stderr)
        raise SystemExit(2)
    from PIL import Image
    with tempfile.TemporaryDirectory() as t:
        sarmal_yol = sarmal(sayfa, genislik, yukseklik, t)
        ortak = [ch, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", "--hide-scrollbars",
                 "--window-size=%d,%d" % (max(1440, genislik + 100), max(900, yukseklik + 56))]
        dom = subprocess.run(ortak + ["--virtual-time-budget=4000", "--dump-dom", "file://" + sarmal_yol], capture_output=True, text=True, timeout=120).stdout
        m = re.search(r'data-sw="(\d+|yok)"', dom)
        sw = int(m.group(1)) if m and m.group(1).isdigit() else None
        ham = os.path.join(t, "ham.png")
        subprocess.run(ortak + ["--virtual-time-budget=4000", "--screenshot=" + ham, "file://" + sarmal_yol], capture_output=True, timeout=120)
        if not os.path.exists(ham):
            print("OLCULEMEDI: ekran görüntüsü alınamadı.", file=sys.stderr)
            raise SystemExit(2)
        Image.open(ham).convert("RGB").crop((0, 0, genislik, yukseklik)).save(cikti)
    return cikti, sw


def ekran(a):
    _, sw = al(a.sayfa, a.cikti, a.genislik, a.yukseklik)
    print("mobil ekran: %s (%dx%d iframe) · sayfa scrollWidth %s" % (a.cikti, a.genislik, a.yukseklik, sw if sw is not None else "okunamadı"))
    if sw is not None and sw > a.genislik:
        print("TASMA: sayfa %d px genişliğinde çizildi, %d px'e sığmıyor (yatay taşma = gerçek düzen hatası)" % (sw, a.genislik))
        return 1
    return 0


def kontrol(a):
    from PIL import Image
    import numpy as np
    verilen = Image.open(a.ekran).convert("RGB")
    w, h = verilen.size
    with tempfile.TemporaryDirectory() as t:
        ref, sw = al(a.sayfa, os.path.join(t, "ref.png"), w, h)
        fark = float(np.abs(np.asarray(verilen, dtype=float) - np.asarray(Image.open(ref).convert("RGB"), dtype=float)).mean())
    print("mobil ekran kontrolü: %s ↔ iframe yeniden çizimi · ortalama fark %.2f (eşik %.1f) · scrollWidth %s" % (a.ekran, fark, FARK_ESIK, sw))
    if sw is not None and sw > w:
        print("TASMA: sayfa %d px > %d px" % (sw, w))
        return 1
    if fark > FARK_ESIK:
        print("MOBİL EKRAN YANLIŞ ALINMIŞ: görüntü doğru 390 px düzeninden farklı (pencere ≥ 500 px düzenle çizilip kırpılmış olabilir); "
              "`mobil_ekran.py ekran` ile yeniden al.")
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut", required=True)
    e = alt.add_parser("ekran")
    e.add_argument("sayfa"); e.add_argument("cikti"); e.add_argument("--genislik", type=int, default=390); e.add_argument("--yukseklik", type=int, default=844)
    k = alt.add_parser("kontrol")
    k.add_argument("sayfa"); k.add_argument("ekran")
    a = ap.parse_args()
    return {"ekran": ekran, "kontrol": kontrol}[a.komut](a)


if __name__ == "__main__":
    sys.exit(main())
