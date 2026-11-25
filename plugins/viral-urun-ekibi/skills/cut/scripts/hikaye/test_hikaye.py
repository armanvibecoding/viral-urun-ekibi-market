#!/usr/bin/env python3
"""Hikâye hattı uçtan uca testi (kredisiz, ağsız): sentetik stok klip + sentetik ürün PNG + sentetik müzik → 25 sn video.

  python3 test_hikaye.py [--hf]     --hf: HyperFrames ile gerçek render (Node 22+, ağ gerekir); yoksa render adımı "atlandı" yazılır
                                    ve yazısız ffmpeg birleştirme kullanılır — ses, ölçüm ve görüntü kapıları yine koşar.
Kırma testleri: fiyatlı metin, kanca yok, eksik klip dosyası → hikaye_kur çıkış 2 olmalı.
Çıkış 0 = hepsi geçti.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw

BURADA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURADA)
from _arac import FF, CUT, sure as medya_sure  # noqa: E402

sonuc = []


def kontrol(ad, ok, ayrinti=""):
    sonuc.append(bool(ok))
    print(("GEÇTİ " if ok else "KALDI ") + ad + ("" if ok else " | " + str(ayrinti)[:300]))


def muzik_yaz(yol, sr=48000, sure=40.0, drop=22.88):
    t = np.arange(int(sure * sr)) / sr
    nota = lambda f: np.sin(2 * np.pi * f * t)  # noqa: E731
    pad = (nota(220) + nota(277.2) + nota(329.6)) / 3
    zarf = np.where(t < drop, 0.05, 0.30)
    zarf = np.convolve(zarf, np.ones(2400) / 2400, mode="same")
    bas = nota(55) * np.where(t < drop, 0.0, 0.22)
    vurus = np.zeros_like(t)
    for b in np.arange(drop, sure, 0.5):  # drop sonrası ritim: delik sayılmasın diye zarf altı sürekli pad
        i = int(b * sr)
        vurus[i:i + 3000] += np.sin(2 * np.pi * 90 * t[:3000]) * np.exp(-t[:3000] * 40) * 0.25
    x = pad * zarf + bas + vurus
    x = np.stack([x, x * 0.98], 1)
    x /= np.abs(x).max() / 0.8
    with wave.open(yol, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def kur(d):
    os.makedirs(os.path.join(d, "stok"), exist_ok=True)
    os.makedirs(os.path.join(d, "muzik"), exist_ok=True)
    klip = os.path.join(d, "stok", "klip1.mp4")
    subprocess.run([FF, "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=1920x1080:r=30:d=22", "-vf", "hue=h=t*20,format=yuv420p", "-c:v", "libx264", "-crf", "20", klip], check=True)
    im = Image.new("RGBA", (400, 560), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((60, 20, 340, 540), radius=60, fill=(231, 192, 143, 255))
    im.save(os.path.join(d, "stok", "urun.png"))
    muzik_yaz(os.path.join(d, "muzik", "parca.wav"))
    a = json.load(open(os.path.join(BURADA, "ayar-ornek.json"), encoding="utf-8"))
    a["ses"].update({"giris_hedef": 18, "drop_oncesi_db": -12})  # sentetik müzik gerçek parçadan daha düz: drop kontrastı ayarla büyütülür
    import shutil
    shutil.copy(os.path.join(BURADA, "on-uretim-karti-ornek.json"), os.path.join(d, "on-uretim-karti.json"))
    yol = os.path.join(d, "ayar.json")
    json.dump(a, open(yol, "w"), ensure_ascii=False, indent=1)
    return yol, a


def kos(*c, **kw):
    return subprocess.run([str(x) for x in c], capture_output=True, text=True, **kw)


def main():
    hf = "--hf" in sys.argv
    with tempfile.TemporaryDirectory(prefix="hikaye_test_") as d:
        yol, a = kur(d)
        # kırma testleri (hikaye_kur --dogrula + tam kurulum kapıları)
        k = copy.deepcopy(a)
        k["sahneler"][1]["ana"] = "Only 29 USD today / *buy* *now*"
        p = os.path.join(d, "kir_fiyat.json"); json.dump(k, open(p, "w"))
        r = kos(sys.executable, os.path.join(BURADA, "hikaye_kur.py"), p, "--dogrula")
        kontrol("kırma: fiyatlı metin → çıkış 2", r.returncode == 2 and "fiyat" in r.stdout, r.stdout + r.stderr)
        k = copy.deepcopy(a)
        k["on_uretim_karti"] = "yok.json"
        p = os.path.join(d, "kir_kart.json"); json.dump(k, open(p, "w"))
        r = kos(sys.executable, os.path.join(BURADA, "hikaye_kur.py"), p, "--dogrula")
        kontrol("kırma: ön-üretim kartı yok → hat çalışmaz, çıkış 2", r.returncode == 2 and "ön-üretim kartı" in r.stdout, r.stdout + r.stderr)
        k = copy.deepcopy(a)
        del k["on_uretim_karti"]
        p = os.path.join(d, "kir_kart2.json"); json.dump(k, open(p, "w"))
        r = kos(sys.executable, os.path.join(BURADA, "hikaye_kur.py"), p, "--dogrula")
        kontrol("kırma: ayarda kart alanı yok → çıkış 2", r.returncode == 2 and "ön-üretim kartı" in r.stdout, r.stdout + r.stderr)
        k = copy.deepcopy(a)
        k["sahneler"][0]["bas"] = 1.0
        p = os.path.join(d, "kir_kanca.json"); json.dump(k, open(p, "w"))
        r = kos(sys.executable, os.path.join(BURADA, "hikaye_kur.py"), p, "--dogrula")
        kontrol("kırma: kanca ilk karede değil → çıkış 2", r.returncode == 2 and "kanca" in r.stdout, r.stdout + r.stderr)
        k = copy.deepcopy(a)
        k["klipler"][0]["dosya"] = "stok/yok.mp4"
        p = os.path.join(d, "kir_klip.json"); json.dump(k, open(p, "w"))
        r = kos(sys.executable, os.path.join(BURADA, "hikaye_kur.py"), p, "--dogrula")
        kontrol("kırma: eksik klip dosyası → çıkış 2", r.returncode == 2 and "klip 0" in r.stdout, r.stdout + r.stderr)
        r = kos(sys.executable, os.path.join(BURADA, "hikaye_kur.py"), yol, "--dogrula")
        kontrol("geçerli ayar --dogrula → çıkış 0", r.returncode == 0, r.stdout + r.stderr)
        # uçtan uca
        ek = [] if hf else ["--sessiz-ffmpeg"]
        r = kos(sys.executable, os.path.join(BURADA, "uret.py"), yol, *ek)
        print(r.stdout[-1200:], r.stderr[-600:])
        kontrol("uret.py çıkış 0", r.returncode == 0, r.stdout[-400:] + r.stderr[-400:])
        v = os.path.join(d, "TESLIM", a["ad"] + ".mp4")
        kontrol("TESLIM videosu var", os.path.exists(v))
        if os.path.exists(v):
            kontrol("süre 25,0 ± 0,1 sn", abs(medya_sure(v) - 25.0) <= 0.1, medya_sure(v))
            o = kos(sys.executable, os.path.join(CUT, "ses_olc.py"), v, "--drop", "18.4", "--muzik_stem", os.path.join(d, "ses", "stem_" + a["ad"], "muz_teslim.wav"), "--kapi")
            kontrol("ses_olc --kapi çıkış 0", o.returncode == 0, o.stdout[-500:] + o.stderr[-300:])
            try:  # teslim kodlaması (AAC yeniden kodlama) sonrası true peak ≤ −1 dBTP (sınav 03 tur1: −0,7 çıkıyordu)
                tp = json.loads(o.stdout)["true_peak_dbtp"]
            except Exception:  # noqa: BLE001
                tp = None
            kontrol("teslim true peak ≤ −1,0 dBTP (AAC sonrası)", tp is not None and tp <= -1.0, tp)
            g = kos(sys.executable, os.path.join(CUT, "kurgu_kontrol.py"), "--goruntu", v, "--kesimler", ",".join(str(x) for x in a["kesimler"]), "--yalniz-goruntu")
            kontrol("kurgu_kontrol --goruntu GEÇTİ (çıkış 0)", g.returncode == 0, g.stdout[-400:] + g.stderr[-300:])
            for dosya in ("_pano_4fps.jpg", "_pano10.jpg", "_kontrol.jpg"):
                kontrol("pano " + dosya, os.path.exists(os.path.join(d, "TESLIM", a["ad"] + dosya)))
        # VO'lu ses adımı: sentetik konuşma (5 Hz hece) + müzik duck −10 dB; kapı müzik katmanında (ses_olc --vo) ölçer
        voyol = os.path.join(d, "ses", "vo1.wav")
        subprocess.run([FF, "-v", "error", "-y", "-f", "lavfi", "-i", "aevalsrc='0.5*sin(2*PI*300*t)*gt(sin(2*PI*5*t),0)':s=48000:d=3", voyol], check=True)
        av = json.load(open(yol, encoding="utf-8"))
        av["ses"]["vo"] = [{"dosya": "ses/vo1.wav", "bas": 6.0}]
        av["ses"]["vo_duck_db"] = -10
        yol_vo = os.path.join(d, "ayar_vo.json")
        json.dump(av, open(yol_vo, "w"))
        r2 = kos(sys.executable, os.path.join(BURADA, "ses.py"), yol_vo)
        kontrol("VO + duck −10 dB: ses.py çıkış 0 (ses_olc --vo müzik katmanında)", r2.returncode == 0, r2.stdout[-500:] + r2.stderr[-300:])
        kontrol("hf/index.html yazıldı ve kanca bas=0", os.path.exists(os.path.join(d, "hf", "index.html")) and 'data-start="0"' in open(os.path.join(d, "hf", "index.html")).read())
        if not hf:
            print("NOT: HyperFrames render ATLANDI (ffmpeg yedeği kullanıldı); gerçek render için: python3 test_hikaye.py --hf")
    kalan = sonuc.count(False)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
    sys.exit(1 if kalan else 0)


if __name__ == "__main__":
    main()
