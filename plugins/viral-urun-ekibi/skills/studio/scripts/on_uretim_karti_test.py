#!/usr/bin/env python3
"""on_uretim_karti.py kırma testi (ağsız, ffmpeg'siz). Çıkış 0 = hepsi geçti."""
import copy
import json
import os
import subprocess
import sys
import tempfile

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
from on_uretim_karti import dogrula, sablon  # noqa: E402

sonuc = []


def t(ad, ok):
    sonuc.append(bool(ok))
    print(("GEÇTİ " if ok else "KALDI ") + ad)


iyi = sablon("US")
t("geçerli ABD kartı", dogrula(iyi) == [])
for pz in ("UK", "DE", "FR", "ES", "TR"):
    t("şablon %s geçerli" % pz, dogrula(sablon(pz)) == [])


def boz(ad, f, parca):
    k = copy.deepcopy(iyi)
    f(k)
    h = dogrula(k)
    t("kırma: %s → HATA" % ad, any(parca in x for x in h))


boz("bilinmeyen pazar", lambda k: k.update(pazar="XX"), "pazar")
boz("var olmayan kanca ailesi", lambda k: k.update(kanca_ailesi="K99"), "kanca_ailesi")
boz("uydurma kanıt numarası", lambda k: k.update(kanit=["[9999]"]), "kanıt")
boz("kanıt yok", lambda k: k.update(kanit=[]), "kanit boş")
boz("var olmayan sahne şablonu", lambda k: k.update(sahne_sablonu="S99"), "sahne_sablonu")
boz("döngüde tatmin anı yok", lambda k: k.update(tatmin_ani=""), "tatmin_ani")
boz("müzik dayanağı yok", lambda k: k.update(muzik={"karar": "x"}), "muzik")
boz("ilk 1 sn boş", lambda k: k.update(ilk_1sn=""), "ilk_1sn")
tr = sablon("TR")
k = copy.deepcopy(tr); k["kanca_metni"] = "bu çok uzun bir kanca metni olmamalı hiç ama hiç"
t("kırma: TR kancası > 8 kelime → HATA", any("8" in x for x in dogrula(k)))
k = copy.deepcopy(tr); k.pop("tr_veri_zayif")
t("kırma: TR'de veri-zayıf uyarısı yok → HATA", any("tr_veri_zayif" in x for x in dogrula(k)))
k = sablon("DE"); k.pop("esik")
t("kırma: AB'de eşik notu yok → HATA", any("esik" in x for x in dogrula(k)))

with tempfile.TemporaryDirectory() as d:
    # hizli_kurgu kutulu: kart olmadan çalışmaz, mesaj kartı söyler
    ay = os.path.join(d, "ayar.json")
    json.dump({"yazi_stil": "kutulu", "font": "x.ttf", "planlar": [], "cikti": "k.mp4"}, open(ay, "w"))
    r = subprocess.run([sys.executable, os.path.join(B, "..", "..", "cut", "scripts", "hizli_kurgu.py"), ay], capture_output=True, text=True)
    t("kırma: hizli_kurgu kutulu + kart yok → çıkış ≠ 0, 'ÖN-ÜRETİM KARTI'", r.returncode != 0 and "ÖN-ÜRETİM KARTI" in (r.stdout + r.stderr))
    json.dump(iyi, open(os.path.join(d, "kart.json"), "w"))
    json.dump({"yazi_stil": "kutulu", "on_uretim_karti": "kart.json", "font": "x.ttf", "planlar": [], "cikti": "k.mp4"}, open(ay, "w"))
    r = subprocess.run([sys.executable, os.path.join(B, "..", "..", "cut", "scripts", "hizli_kurgu.py"), ay], capture_output=True, text=True)
    t("geçerli kart: hizli_kurgu kart kapısını geçer", "ÖN-ÜRETİM KARTI" not in (r.stdout + r.stderr))
    r = subprocess.run([sys.executable, os.path.join(B, "on_uretim_karti.py"), "kontrol", os.path.join(d, "yok.json")], capture_output=True, text=True)
    t("kırma: kart dosyası yok → çıkış 1", r.returncode == 1)

print("TOPLAM: %d test, %d kaldı" % (len(sonuc), sonuc.count(False)))
sys.exit(1 if False in sonuc else 0)
