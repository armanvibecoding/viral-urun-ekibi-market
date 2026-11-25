#!/usr/bin/env python3
"""ocr_kontrol.py kırma testi (denetim 2026-11-25 #6; ARAC-OCR.md): Latin metinde 1 harflik hata KALDI, doğru metin GEÇTİ,
Türkçe harfli öğe Tesseract'sız OLCULEMEDI (çıkış 2) verir, KALDI değil. RapidOCR ortamı yoksa ATLANIR (ölçülmedi sayılır).
Kullanım: python3 ocr_kontrol_test.py   (OCR ortamı: ~/.local/share/viral-urun-ekibi/ocr-venv/bin/python)"""
import os
import subprocess
import sys
import tempfile

BURASI = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.expanduser("~/.local/share/viral-urun-ekibi/ocr-venv/bin/python")
FONTLAR = ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def kart(yol, satirlar):
    from PIL import Image, ImageDraw, ImageFont
    f = next((x for x in FONTLAR if os.path.exists(x)), None)
    im = Image.new("RGB", (1080, 1080), "#1E2226")
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(f, 64) if f else ImageFont.load_default()
    for i, s in enumerate(satirlar):
        d.text((60, 200 + i * 220), s, font=font, fill="#F2F2EE")
    im.save(yol)


def kos(py, gorsel, beklenen, dil):
    return subprocess.run([py, os.path.join(BURASI, "ocr_kontrol.py"), gorsel, beklenen, "--dil", dil], capture_output=True, text=True).returncode


def main():
    py = VENV if os.path.exists(VENV) else sys.executable
    try:
        subprocess.run([py, "-c", "import rapidocr_onnxruntime"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, OSError):
        print("ATLANDI: RapidOCR yok (bu kapı bu koşuda ÖLÇÜLMEDİ)")
        return 0
    t = tempfile.mkdtemp(prefix="ocr_test_")
    g = os.path.join(t, "latin.png")
    kart(g, ["KLEBEBLATT ABZIEHEN"])
    tr = os.path.join(t, "tr.png")
    kart(tr, ["SOĞUKKEN SİYAH"])
    sonuc = [
        ("doğru Latin metin -> 0 GEÇTİ", kos(py, g, "KLEBEBLATT ABZIEHEN", "en") == 0),
        ("kırma: 2 harf eksik (KLEBEBLAT ABZIEHN) -> 1 KALDI (eski %90 eşiği geçiriyordu)", kos(py, g, "KLEBEBLAT ABZIEHN", "en") == 1),
        ("kırma: 1 harf anlam ters (ANZIEHEN) -> 1 KALDI", kos(py, g, "KLEBEBLATT ANZIEHEN", "en") == 1),
        ("kırma: tamamen farklı metin -> 1 KALDI", kos(py, g, "HAARE ENTFERNEN", "en") == 1),
    ]
    tesseract = subprocess.run(["which", "tesseract"], capture_output=True).returncode == 0
    if tesseract:
        print("ATLANDI: Tesseract kurulu; TR olculemedi testi bu makinede anlamsız")
    else:
        sonuc.append(("TR harfli öğe, Tesseract yok -> 2 olculemedi (KALDI değil)", kos(py, tr, "SOĞUKKEN SİYAH", "tr") == 2))
    for ad, ok in sonuc:
        print(("GEÇTİ " if ok else "KALDI ") + ad)
    kalan = sum(1 for _, ok in sonuc if not ok)
    print("TOPLAM: %d test, %d kaldı" % (len(sonuc), kalan))
    return 1 if kalan else 0


if __name__ == "__main__":
    sys.exit(main())
