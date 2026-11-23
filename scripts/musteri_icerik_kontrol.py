#!/usr/bin/env python3
"""Müşteri içeriği kapısı: public depoda müşteri/ortak senaryosundan kalan cümle olmasın.
Desen listesi bu dosyadadır (JENERİK ipuçları; müşteri/marka adı yazılmaz). Çıkış 0 temiz · 1 eşleşme.
Kapıyı kırarak sınar: python3 scripts/musteri_icerik_kontrol.py --kendini-sina"""
import os, re, subprocess, sys, tempfile
DESEN = re.compile(r"lighthouse|signal gets lost|right connection|finds the boat|hibernat|stage fright|locked door|desert bloom|find your signal|body is ready", re.I)
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BU = os.path.relpath(os.path.abspath(__file__), KOK)

def tara(kok):
    dosyalar = subprocess.run(["git", "-C", kok, "ls-files"], capture_output=True, text=True).stdout.split("\n")
    bul = []
    for f in dosyalar:
        if not f or f == BU or f.startswith("dist/"):
            continue
        try:
            for n, s in enumerate(open(os.path.join(kok, f), encoding="utf-8"), 1):
                if DESEN.search(s):
                    bul.append("%s:%d" % (f, n))
        except (OSError, UnicodeDecodeError):
            pass
    return bul

if "--kendini-sina" in sys.argv:
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["git", "init", "-q", d], check=True)
        open(os.path.join(d, "a.txt"), "w").write("temiz satır\n")
        subprocess.run(["git", "-C", d, "add", "a.txt"], check=True)
        t1 = tara(d) == []
        open(os.path.join(d, "a.txt"), "w").write("When the lighthouse takes long\n")
        subprocess.run(["git", "-C", d, "add", "a.txt"], check=True)
        t2 = tara(d) == ["a.txt:1"]
    print("temiz → boş: %s · bozuk → yakalandı: %s" % (t1, t2))
    sys.exit(0 if t1 and t2 else 1)
b = tara(KOK)
for x in b:
    print("MÜŞTERİ İÇERİĞİ:", x)
print("müşteri içeriği kapısı:", "GEÇTİ" if not b else "KALDI (%d)" % len(b))
sys.exit(1 if b else 0)
