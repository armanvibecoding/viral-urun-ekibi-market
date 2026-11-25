#!/usr/bin/env python3
"""kanca_varyasyon.py kırma testi (ffmpeg'siz; --render yok)."""
import json
import os
import subprocess
import sys
import tempfile

B = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(B, "kanca_varyasyon.py")
sonuc = []


def t(ad, ok):
    sonuc.append(bool(ok))
    print(("GEÇTİ " if ok else "KALDI ") + ad)


def kos(d, kanc, ek=()):
    json.dump(kanc, open(os.path.join(d, "k.json"), "w"))
    return subprocess.run([sys.executable, S, os.path.join(d, "ayar.json"), os.path.join(d, "k.json")] + list(ek), capture_output=True, text=True)


def liste(n, **ov):
    l = [{"id": "V%02d" % (i + 1), "aile": "K1", "yazi": "DO NOT show this to a fan %d" % i, "vurgu": "fan", "kanit": ["[037]"]} for i in range(n)]
    for i, o in ov.items():
        l[int(i)].update(o)
    return l


with tempfile.TemporaryDirectory() as d:
    json.dump({"yazi_stil": "kutulu", "font": "x.ttf", "cikti": "k.mp4", "yazilar": [{"bas": 0, "bit": 2, "yazi": "x"}], "planlar": []}, open(os.path.join(d, "ayar.json"), "w"))
    r = kos(d, liste(10))
    t("10 kanca → 10 ayar + plan + kayıt, çıkış 0", r.returncode == 0 and all(os.path.exists(os.path.join(d, "varyasyon_V%02d.json" % i)) for i in range(1, 11))
      and os.path.exists(os.path.join(d, "varyasyon", "yayin-plani.md")) and os.path.exists(os.path.join(d, "varyasyon", "kayit.tsv")))
    v = json.load(open(os.path.join(d, "varyasyon_V03.json")))
    t("yalnız kanca değişti (font/stil aynı, yazı V03'ünki)", v["yazilar"][0]["yazi"].endswith("fan 2") and v["yazi_stil"] == "kutulu" and v["cikti"].endswith("V03.mp4"))
    t("kırma: 9 kanca → çıkış 1", kos(d, liste(9)).returncode == 1)
    t("kırma: aynı kanca yazısı iki kez → çıkış 1", kos(d, liste(10, **{"1": {"yazi": "DO NOT show this to a fan 0"}})).returncode == 1)
    t("kırma: kütüphanede olmayan kanıt → çıkış 1", kos(d, liste(10, **{"2": {"kanit": ["[9999]"]}})).returncode == 1)
    t("kırma: var olmayan aile → çıkış 1", kos(d, liste(10, **{"2": {"aile": "K77"}})).returncode == 1)
    t("K14 ve K15 (S24 aileleri) kütüphanede başlıklı: kabul edilir", kos(d, liste(10, **{"0": {"aile": "K14", "kanit": ["[S24-G1x06]"]}, "1": {"aile": "K15", "kanit": ["[S24-G1x07]"]}})).returncode == 0)
    json.dump({"pazar": "TR", "font": "x.ttf", "cikti": "k.mp4", "yazilar": [{"bas": 0, "bit": 2, "yazi": "x"}], "planlar": []}, open(os.path.join(d, "ayar.json"), "w"))
    t("kırma: TR'de 9+ kelimelik kanca → çıkış 1", kos(d, liste(10, **{"0": {"yazi": "bu kanca TR için fazla uzun bir cümle oldu gerçekten"}})).returncode == 1)

print("TOPLAM: %d test, %d kaldı" % (len(sonuc), sonuc.count(False)))
sys.exit(1 if False in sonuc else 0)
