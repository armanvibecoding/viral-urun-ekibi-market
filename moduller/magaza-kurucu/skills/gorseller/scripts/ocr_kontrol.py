# -*- coding: utf-8 -*-
"""Görsel içi yazıyı OCR ile okuyup beklenen metinle karşılaştırır (görsel QA, kapı K2).

  python scripts/ocr_kontrol.py <görsel> <beklenen.txt | "satır1|satır2"> [--dil tr|en] [--json]

Beklenen: her satır bir metin öğesi (başlık satırları ayrı ayrı yazılabilir). Karşılaştırma büyük/küçük
harfe duyarsız ama Türkçe harfe DUYARLI (İ≠I, ı≠i, ş≠s ...). Çıkış kodu: 0 = bütün öğeler bulundu ve
fazla yazı yok, 1 = eksik/yanlış öğe ya da fazla yazı, 2 = OCR çalışmadı.

Motor (karma): RapidOCR ana okuyucudur (küçük ve açık/koyu yazıda güçlü) ama Çince/İngilizce modeli
İ/Ö/Ş/Ğ/Ü/Ç'yi I/O/S/G/U/C okur. Bu yüzden Türkçe harf içeren öğe Tesseract 5 + `tur` verisiyle birebir
doğrulanır (dil verisi klasörü `OCR_TESSDATA` ortam değişkeniyle verilir; yoksa `TESSDATA_PREFIX`). Tesseract yoksa o öğe "gözle" kalır.
Eşleşme: Türkçe harfler katlanarak RapidOCR satırıyla ≥ %90; Türkçe harfli öğe Tesseract'ta birebir.
Beklenenle eşleşmeyen ≥ 3 harfli RapidOCR satırı "fazla yazı"dır (ör. girdi fotoğrafından taşınan logo).
"""
import argparse
import difflib
import json
import os
import re
import sys
import unicodedata

TR_UST = str.maketrans({"i": "İ", "ı": "I"})


def tr_upper(s):
    return s.translate(TR_UST).upper()


def norm(s, dil):
    s = unicodedata.normalize("NFC", s)
    s = tr_upper(s) if dil == "tr" else s.upper()
    s = re.sub(r"[\"“”'’`]", "", s)
    s = re.sub(r"[·•∙⋅|]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def ocr_satirlar(yol, buyut=False):
    """buyut=False: tam görsel tek geçiş. buyut=True: üst üste binen 5 yatay şerit, her biri 2×
    (küçük punto teknik satırlar tam görselde algılanmıyor; 2026-11-18 bir müşteri galerisinde ölçüldü)."""
    import numpy as np
    import cv2
    from rapidocr_onnxruntime import RapidOCR
    im = cv2.imdecode(np.fromfile(yol, dtype=np.uint8), cv2.IMREAD_COLOR)
    if im is None:
        raise RuntimeError("görsel okunamadı")
    ocr = RapidOCR()
    out = []
    h = im.shape[0]
    parcalar = [(0, h)] if not buyut else [(max(0, int(i * h / 5 - h * 0.04)), min(h, int((i + 1) * h / 5 + h * 0.04))) for i in range(5)]
    for y0, y1 in parcalar:
        kaynak = im[y0:y1]
        olcek = 2 if buyut else 1
        if buyut:
            kaynak = cv2.resize(kaynak, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        for kutu, metin, guven in (ocr(kaynak)[0] or []):
            if float(guven) >= 0.5:
                out.append({"metin": metin, "guven": round(float(guven), 2), "kutu": [[int(x / olcek), int(y / olcek + y0)] for x, y in kutu]})
    return out, im


TESS_EXE = [os.environ.get("OCR_TESSERACT", ""), "tesseract"]


def tesseract_bul(dil):
    import shutil
    exe = next((e for e in TESS_EXE if e and (os.path.exists(e) or shutil.which(e))), None)
    dd = os.environ.get("OCR_TESSDATA") or os.environ.get("TESSDATA_PREFIX") or ""
    gerek = ["tur", "eng"] if dil == "tr" else ["eng"]
    if exe and all(os.path.exists(os.path.join(dd, g + ".traineddata")) for g in gerek):
        return exe, dd, "+".join(gerek)
    return None


def tesseract_satirlar(yol, motor, buyut=False):
    import subprocess
    import tempfile
    from PIL import Image
    exe, dd, lang = motor
    kaynak = yol
    with tempfile.TemporaryDirectory() as t:
        if buyut:
            im = Image.open(yol).convert("RGB")
            im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
            kaynak = os.path.join(t, "b.png")
            im.save(kaynak)
        r = subprocess.run([exe, kaynak, "stdout", "-l", lang, "--tessdata-dir", dd, "--psm", "11"],
                           capture_output=True, text=True, encoding="utf-8")
    return [{"metin": l.strip(), "guven": None, "kutu": None} for l in r.stdout.splitlines() if l.strip()]


def yeniden_oku(im, kutu):
    import cv2
    from rapidocr_onnxruntime import RapidOCR
    xs = [p[0] for p in kutu]
    ys = [p[1] for p in kutu]
    h, w = im.shape[:2]
    pad = 12
    k = im[max(0, min(ys) - pad):min(h, max(ys) + pad), max(0, min(xs) - pad):min(w, max(xs) + pad)]
    k = cv2.resize(k, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    r = RapidOCR()(k)[0] or []
    return " ".join(m for _, m, g in r if float(g) >= 0.5)


def oran_hesap(nb, o):
    # OCR'ın O/0 karışıklığı yazım hatası sayılmaz (ikisi de O'ya eşlenir)
    nb, o = nb.replace("0", "O"), o.replace("0", "O")
    r = difflib.SequenceMatcher(None, nb, o).ratio()
    r = max(r, difflib.SequenceMatcher(None, nb.replace(" ", ""), o.replace(" ", "")).ratio())
    if nb and (nb in o or nb.replace(" ", "") in o.replace(" ", "")):
        r = 1.0
    return r


TR_OZEL = set("İıŞşĞğÜüÖöÇç")
KATLA = str.maketrans("İIŞĞÜÖÇ", "IISGUOC")


def katla(s):
    return s.translate(KATLA)


def en_iyi(nb, on):
    en, en_i = 0.0, None
    for i, o in enumerate(on):
        r = oran_hesap(nb, o)
        if r > en:
            en, en_i = r, i
    return en, en_i


def kontrol(yol, beklenen, dil):
    """Karma: RapidOCR ana okuyucu (küçük ve açık-koyu yazıda güçlü, Türkçe harfi göremez); Tesseract `tur`
    yalnız Türkçe harf içeren öğeyi birebir doğrular. Türkçe harfli öğe Tesseract'sız ya da Tesseract
    okuyamazsa "gözle" kalır (geçmiş sayılmaz)."""
    satirlar, im = ocr_satirlar(yol)
    on = [norm(s["metin"], dil) for s in satirlar]
    eksik = [b for b in beklenen if en_iyi(katla(norm(b, dil)), [katla(o) for o in on])[0] < 0.90]
    if eksik:  # küçük punto: 2× büyütülmüş şeritlerde ikinci geçiş
        ek, _ = ocr_satirlar(yol, buyut=True)
        satirlar = satirlar + [dict(x, ek=True) for x in ek if norm(x["metin"], dil) not in on]
        on = [norm(s["metin"], dil) for s in satirlar]
    motor = tesseract_bul(dil) if dil == "tr" else None
    ton = []
    if motor and any(set(b) & TR_OZEL for b in beklenen):
        ton = [norm(x["metin"], dil) for x in tesseract_satirlar(yol, motor) + tesseract_satirlar(yol, motor, buyut=True)]
    kullanilan = set()
    sonuc = []
    for b in beklenen:
        nb = norm(b, dil)
        en, en_i = en_iyi(katla(nb), [katla(o) for o in on])
        okunan = satirlar[en_i]["metin"] if en_i is not None else ""
        if not en >= 0.90 and en_i is not None and satirlar[en_i]["kutu"]:
            ikinci = yeniden_oku(im, satirlar[en_i]["kutu"])
            r2 = oran_hesap(katla(nb), katla(norm(ikinci, dil)))
            if r2 > en:
                en, okunan = r2, ikinci
        if en_i is not None and en >= 0.6:
            kullanilan.add(en_i)
        durum = "tamam" if en >= 0.90 else "hata"
        if durum == "tamam" and dil == "tr" and set(b) & TR_OZEL:
            # Türkçe harf: RapidOCR göremez; Tesseract birebir okumalı
            t_en, t_i = en_iyi(nb, ton) if ton else (0.0, None)
            if t_en >= 0.999:
                okunan = okunan + " | tesseract: " + ton[t_i]
            elif ton and t_i is not None and en_iyi(katla(nb), [katla(ton[t_i])])[0] >= 0.999:
                durum, okunan = "hata", "tesseract: " + ton[t_i]  # harfler aynı, Türkçe harf farklı = yazım hatası
            else:
                durum = "gozle"
        sonuc.append({"beklenen": b, "okunan": okunan, "oran": round(en, 2), "tamam": durum == "tamam", "durum": durum})
    nbs = [katla(norm(b, dil)) for b in beklenen]
    fazla = []
    for i in range(len(satirlar)):
        if satirlar[i].get("ek"):
            continue  # şerit geçişinin satırları yalnız eksik öğe aramak içindir; şerit kenarı yarım satır üretir
        if i in kullanilan or len(re.sub(r"[^\w]", "", satirlar[i]["metin"])) < 3:
            continue
        o = katla(on[i])
        if max(oran_hesap(nb, o) for nb in nbs) >= 0.8 or any(o in nb for nb in nbs):
            continue
        fazla.append(satirlar[i]["metin"])
    return sonuc, fazla, "rapidocr" + (" + tesseract " + motor[2] if ton else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gorsel")
    ap.add_argument("beklenen")
    ap.add_argument("--dil", default="tr", choices=["tr", "en"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if os.path.exists(a.beklenen):
        beklenen = [s.strip() for s in open(a.beklenen, encoding="utf-8") if s.strip()]
    else:
        beklenen = [s.strip() for s in a.beklenen.split("|") if s.strip()]
    try:
        sonuc, fazla, motor = kontrol(a.gorsel, beklenen, a.dil)
    except Exception as e:
        print("OCR çalışmadı:", e)
        return 2
    gecti = all(s["tamam"] for s in sonuc) and not fazla
    if a.json:
        print(json.dumps({"gecti": gecti, "motor": motor, "ogeler": sonuc, "fazla": fazla}, ensure_ascii=False, indent=1))
    else:
        for s in sonuc:
            isaret = {"tamam": "✅", "hata": "❌", "gozle": "👁 gözle (Türkçe harf doğrulanamadı)"}[s["durum"]]
            print(isaret, f"{s['oran']:.2f}", "beklenen:", s["beklenen"], "| okunan:", s["okunan"])
        for f in fazla:
            print("❌ fazla yazı:", f)
        print("motor:", motor)
        if "tesseract" not in motor and a.dil == "tr" and any(x["durum"] == "gozle" for x in sonuc):
            print("UYARI: RapidOCR Türkçe harfleri (İ Ö Ş Ğ Ü Ç) ayırt etmez; Türkçe harf kontrolü gözle yapılmalı ya da Tesseract tur kurulmalı.")
        print("K2", "GEÇTİ" if gecti else "KALDI (❌ öğeleri gözle doğrula: küçük puntoda OCR yanılabilir)")
    return 0 if gecti else 1


if __name__ == "__main__":
    sys.exit(main())
