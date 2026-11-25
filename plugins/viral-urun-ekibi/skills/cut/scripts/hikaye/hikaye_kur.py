#!/usr/bin/env python3
"""Hikâye videosu kurucu: ayar JSON → HyperFrames projesi (hf/index.html) + hazırlanmış stok klipler + zaman.json.

  python3 hikaye_kur.py ayar.json [--dogrula]       (--dogrula: yalnız ayar kapıları, dosya yazmaz)

Ayar şeması: bkz. ayar-ornek.json ve ortak/tarifler/02-hikaye-videosu-organik.md. Yollar ayar dosyasına göre göreli.
Kapılar (HATA → çıkış 2): ön-üretim kartı geçerli (ayar "on_uretim_karti"; yoksa hat çalışmaz) · kanca ilk karede (bas=0) · kesimler artan ve süre içinde · kesim aralığı başına klip ya da ürün sahnesi ·
görünür metinde fiyat/para birimi yok (ayar "fiyat_izin": true ile açılır) · stok klip dosyası var.
"""
import json
import os
import re
import subprocess
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURADA)
import bloklar as B  # noqa: E402
from kit import hazirla  # noqa: E402
from _arac import FF  # noqa: E402

HF_SURUM = os.environ.get("HF_SURUM", "0.9.65")
FIYAT = re.compile(r"(?:[$€£₺]\s?\d|\d\s?(?:TL|₺|USD|EUR|\$|€|dolar|lira)\b|\bfiyat|\bprice\b|%\s?\d+\s?(?:off|indirim))", re.I)


def ayar_oku(yol):
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def kart_kontrol(a, kok):
    """Ön-üretim kartı kapısı: kart yoksa/geçersizse hat çalışmaz (studio/scripts/on_uretim_karti.py)."""
    sys.path.insert(0, os.path.join(BURADA, "..", "..", "..", "studio", "scripts"))
    from on_uretim_karti import kart_kapisi
    yol = a.get("on_uretim_karti")
    ok, h = kart_kapisi(os.path.join(kok, yol) if yol else None)
    return ["ön-üretim kartı: " + x for x in h] if not ok else []


def dogrula(a, kok):
    hata = kart_kontrol(a, kok)
    sure = float(a["sure"])
    ks = [float(x) for x in a["kesimler"]]
    if ks != sorted(ks) or (ks and (ks[0] <= 0 or ks[-1] >= sure)):
        hata.append("kesimler artan olmalı ve 0 < kesim < sure")
    t_ = [0.0] + ks + [sure]
    if len(a["klipler"]) != len(t_) - 1:
        hata.append("klipler uzunluğu %d ≠ kesim aralığı %d (ürün/yazı sahnesi için null yaz)" % (len(a["klipler"]), len(t_) - 1))
    for i, k in enumerate(a["klipler"]):
        if k is None:
            continue
        for alan in ("dosya", "dosya2"):
            if k.get(alan) and not os.path.exists(os.path.join(kok, k[alan])):
                hata.append("klip %d dosyası yok: %s" % (i, k[alan]))
        if k.get("tur") == "bolunmus" and not k.get("dosya2"):
            hata.append("klip %d bölünmüş ekran: dosya2 gerekli" % i)
    kancalar = [s for s in a["sahneler"] if s.get("tur") in B.TP.KANCA_TURLERI]
    if not kancalar or float(kancalar[0].get("bas", 0)) > 0.05:
        hata.append("kanca ilk karede değil (kanca sahnesi bas=0 olmalı; kanca türleri: %s)" % ", ".join(B.TP.KANCA_TURLERI))
    gec = a.get("gecisler")
    if gec is not None:
        if len(gec) != len(ks):
            hata.append("gecisler uzunluğu %d ≠ kesim sayısı %d" % (len(gec), len(ks)))
        for g in gec:
            if g not in B.TP.GECIS_OV:
                hata.append("bilinmeyen geçiş %r (izinli: %s)" % (g, ", ".join(B.TP.GECIS_OV)))
    return hata, t_


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    yol = os.path.abspath(sys.argv[1])
    kok = os.path.dirname(yol)
    a = ayar_oku(yol)
    hata, t_ = dogrula(a, kok)
    if hata:
        for h in hata:
            print("HATA:", h)
        sys.exit(2)
    sure = float(a["sure"])
    B.sifirla()
    urun_ayar = a.get("urun") or {}
    doku = bool(a.get("doku"))
    hf = os.path.join(kok, "hf")
    for d in ("assets/img", "assets/video", "renders"):
        os.makedirs(os.path.join(hf, d), exist_ok=True)
    for d in ("ses", "muzik", "TESLIM"):
        os.makedirs(os.path.join(kok, d), exist_ok=True)
    # klipler: aralık i → t_[i]..t_[i+1]
    plan = []
    yeni = a.get("gecisler") is not None
    for i, kl in enumerate(a["klipler"]):
        if kl is None:
            continue
        s_ = round(t_[i + 1] - t_[i], 2)
        ek = 0.2 if yeni else 0.0     # geçişte giren klip kesimden önce başlar (örtüşme)
        if "--dogrula" not in sys.argv:
            tur = kl.get("tur", "klip")
            dst = os.path.join(hf, "assets/video/a%d.mp4" % i)
            if tur == "donuk":
                kare = os.path.join(hf, "assets/img/f%d.png" % i)
                subprocess.run([FF, "-v", "error", "-y", "-ss", str(kl.get("ss", 0)), "-i", os.path.join(kok, kl["dosya"]), "-frames:v", "1",
                                "-vf", "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=1080:1920:flags=lanczos", kare], check=True)
                subprocess.run([FF, "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", kare, "-t", str(s_ + 0.45), "-c:v", "libx264", "-crf", "15",
                                "-pix_fmt", "yuv420p", "-g", "15", "-movflags", "+faststart", dst], check=True)
            else:
                hazirla(os.path.join(kok, kl["dosya"]), dst, kl.get("ss", 0), s_ + ek, hiz=kl.get("hiz", 1.0), vf_ek=kl.get("filtre", ""), zorla=True)
                if tur == "bolunmus":
                    hazirla(os.path.join(kok, kl["dosya2"]), os.path.join(hf, "assets/video/a%db.mp4" % i), kl.get("ss2", 0), s_ + ek, hiz=kl.get("hiz2", 1.0),
                            vf_ek=kl.get("filtre2", ""), zorla=True)
        plan.append(("a%d" % i, "a%d.mp4" % i, t_[i], s_, 1.0 if i % 2 == 0 else 1.06, 1.07 if i % 2 == 0 else 1.0, "50% 45%"))
    if yeni:
        B.TP.klipler([dict(kl, i=i) for i, kl in enumerate(a["klipler"]) if kl is not None], t_, a["gecisler"], sure)
        B.TP.ust_perde(sure)
    else:
        B.klipler(plan)
        B.perde(0, sure, "perde")
    for s in a["sahneler"]:
        B.sahne(s, t_, urun_png="urun.png", urun_w=urun_ayar.get("genislik", 570), doku=doku)
    # fiyat kapısı
    if not a.get("fiyat_izin"):
        m = FIYAT.search(B.metinler())
        if m:
            hata.append("görünür metinde fiyat/para ifadesi: %r (organik videoda fiyat yok; bilinçli ise ayar 'fiyat_izin': true)" % m.group(0))
    if hata:
        for h in hata:
            print("HATA:", h)
        sys.exit(2)
    if "--dogrula" in sys.argv:
        print("ayar kapıları TAMAM (%d sahne, %d kesim aralığı)" % (len(a["sahneler"]), len(t_) - 1))
        return
    if urun_ayar.get("png"):
        import shutil
        shutil.copy(os.path.join(kok, urun_ayar["png"]), os.path.join(hf, "assets/img/urun.png"))
    if doku:
        import shutil
        shutil.copy(os.path.join(kok, a["doku"]), os.path.join(hf, "assets/img/doku.jpg"))
    # HyperFrames iskeleti
    with open(os.path.join(hf, "hyperframes.json"), "w") as f:
        json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
                   "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
                   "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
                   "media": {"autoProxy": True}, "authoringSkill": "hyperframes"}, f, indent=2)
    with open(os.path.join(hf, "package.json"), "w") as f:
        json.dump({"name": "hf", "private": True, "type": "module",
                   "scripts": {k: "npx --yes hyperframes@%s %s" % (HF_SURUM, k if k != "dev" else "preview") for k in ("dev", "check", "render", "publish")}}, f, indent=2)
    with open(os.path.join(hf, "meta.json"), "w") as f:
        json.dump({"id": "hf", "name": "hf"}, f)
    B.bitir(hf, sure, a["ses"]["drop"], t_[1:-1], a.get("tema"), a.get("ek_css", ""), doku)
    print("hf/index.html yazıldı · %.1f sn · %d kesim aralığı · kesimler %s" % (sure, len(t_) - 1, ",".join(str(x) for x in t_[1:-1])))


if __name__ == "__main__":
    main()
