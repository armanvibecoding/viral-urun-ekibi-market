#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ses_plan.py kırma testleri. Kullanım: python3 ses_plan_test.py → 0 hepsi geçerse, 1 biri tutmazsa."""
import json
import os
import subprocess
import sys
import tempfile

B = os.path.dirname(os.path.abspath(__file__))
SP = os.path.join(B, "ses_plan.py")
sonuc = []


def kos(*a):
    r = subprocess.run([sys.executable, SP] + list(a), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def bekle(ad, ok, ayrinti=""):
    sonuc.append(bool(ok))
    print("%s %s%s" % ("GEÇTİ" if ok else "KALDI", ad, "" if ok else "\n    " + str(ayrinti)[-500:]))


def ayar(planlar, yazilar=()):
    return {"planlar": [dict({"klip": "k%d.mp4" % i, "bas": 0, "bit": s, "gecis": g}) for i, (s, g) in enumerate(planlar)], "yazilar": list(yazilar)}


def main():
    with tempfile.TemporaryDirectory() as k:
        def yaz(d):
            y = os.path.join(k, "a.json")
            json.dump(d, open(y, "w", encoding="utf-8"))
            return y
        # 12 sn: 1,7 kesim · 1,5 punch · 1,8 flas · 2 punch · 2 kesim · 3 punch
        y = yaz(ayar([(1.7, "kesim"), (1.5, "punch"), (1.8, "flas"), (2, "punch"), (2, "kesim"), (3, "punch")], [{"bas": 1.7, "bit": 3, "yazi": "A"}]))
        rc, c = kos(y, "--json", os.path.join(k, "p.json"))
        p = json.load(open(os.path.join(k, "p.json"), encoding="utf-8"))
        tur = {(round(a["sn"], 2), a["tur"]) for a in p["efektler"]}
        bekle("drop = ilk flas başlangıcı (3,2 sn), boom drop'ta", rc == 0 and p["drop_sn"] == 3.2 and (3.2, "boom") in tur, c)
        bekle("drop kaynağı 'tahmin' diye işaretli (uydurma kesinlik yok)", "tahmin" in p["drop_kaynak"], p["drop_kaynak"])
        bekle("kanca: 0. sn'de ses olayı", (0.0, "whoosh") in tur, tur)
        bekle("riser drop'tan 0,2 sn önce biter (3,0)", any(a["tur"] == "riser" and a["bitis"] == 3.0 for a in p["efektler"]), p["efektler"])
        bekle("kesim geçişine (7,0 sn) efekt yok", not any(a["sn"] == 7.0 for a in p["efektler"]), tur)
        bekle("yoğunluk ≤ 5 / 10 sn", p["en_yogun_10sn"] <= 5, p["en_yogun_10sn"])
        bekle("müzik drop'u verilmedi → komut ÇALIŞTIRILAMAZ (<MUZIK_DROP_SN>), uydurma yok", not p["komut_calistirilabilir"] and "<MUZIK_DROP_SN>" in p["komut"], p["komut"])
        rc2, c2 = kos(y, "--muzik-bas", "8.0", "--drop-sn", "3.43", "--json", os.path.join(k, "p2.json"))
        p2 = json.load(open(os.path.join(k, "p2.json"), encoding="utf-8"))
        bekle("müzik-bas + drop-sn verilince komut çalıştırılabilir (yalnız dosya yolları <…> kalır → hâlâ işaretli)", p2["drop_sn"] == 3.43 and "--muzik_bas 8.0" in p2["komut"] and "verilen" in p2["drop_kaynak"], p2["komut"])
        rc3, c3 = kos(y)
        bekle("aynı girdi → aynı çıktı", c3 == kos(y)[1])
        # kırma: 8 punch geçişi 8 sn'de → yoğunluk kuralı fazlayı düşürür
        y2 = yaz(ayar([(1, "punch")] * 8))
        rc, c = kos(y2, "--json", os.path.join(k, "p3.json"))
        p3 = json.load(open(os.path.join(k, "p3.json"), encoding="utf-8"))
        bekle("kırma: 8 punch / 8 sn → ≤ 5 efekt, fazlası düştü ve raporda sayıldı", p3["en_yogun_10sn"] <= 5 and len(p3["dusen"]) >= 3, (p3["en_yogun_10sn"], len(p3["dusen"])))
        # kırma: bozuk ayar
        y3 = yaz({"planlar": [{"klip": "x.mp4", "bas": 2, "bit": 1}]})
        rc, c = kos(y3)
        bekle("kırma: bit <= bas → çıkış 1", rc == 1 and "bit <= bas" in c, c)
        rc, c = kos(yaz({"planlar": []}))
        bekle("kırma: planlar boş → çıkış 1", rc == 1, c)
    kalan = sonuc.count(False)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
