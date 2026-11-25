# Araç kaydı · OCR (K2 yazım kapısı) — 2026-11-25

ARAÇ: rapidocr-onnxruntime 1.4.4 · PyPI · kaynak github.com/RapidAI/RapidOCR
Güvenilirlik: RapidAI organizasyonu, 86 sürüm; ad betiğin import satırından kopyalandı (rapidocr_onnxruntime).
Yetki: yalnız yerel dosya okur; ağ/hesap/sır yok. Ayrı sanal ortam: ~/.local/share/viral-urun-ekibi/ocr-venv (Python 3.12, 240 MB). Sistem Python'una dokunulmadı.
Ön koşul: Tesseract YOK (makinede Homebrew yok) → Türkçe harf (İ Ö Ş Ğ Ü Ç) doğrulaması yapılamaz.
Kullanım: `~/.local/share/viral-urun-ekibi/ocr-venv/bin/python scripts/sinav_kos.py 05-gorsel <klasör>`

## Kırma testi (b-zor galeri-2, görseldeki yazı "KLEBEBLATT ABZIEHEN")
| Beklenen metin | Sonuç | Doğru mu |
|---|---|---|
| KLEBEBLATT ABZIEHEN (doğru) | 0 GEÇTİ | ✅ |
| HAARE ENTFERNEN (tamamen farklı) | 1 KALDI | ✅ |
| KLEBEBLAT ABZIEHN (2 harf eksik) | 0 GEÇTİ | ❌ yazım hatası kaçıyor |
| KLEBEBLATT ANZIEHEN (1 harf, anlam ters) | 0 GEÇTİ | ❌ |
| TR görsel (SOĞUKKEN SİYAH) | 1 KALDI ("gözle") | ölçülemez — Tesseract yok |

## Hüküm
K2 artık **yazı var/yok ve fazla yazı** ölçer; **yazım hatası ölçmez** (benzerlik eşiği %90). Kırma tutmadı → yazım kısmı ölçülmemiş sayılır.
Açık işler: (1) Latin metinde eşleşmeyi birebir yap (eşik sıkılaştırma = ayrı kalibrasyon işi, kırma testi yukarıdaki 2 satır), (2) TR için Tesseract + tur verisi (Homebrew ya da başka kurulum yolu, ayrı onay), (3) TR "gözle" sonucu KALDI değil olculemedi raporlanmalı.

## 05 tur1 K2 sonucu (bu araçla)
b-zor (DE) 6/6 GEÇTİ · c-tuzak (US) 6/6 GEÇTİ · a-kolay (TR) KALDI = Türkçe harf doğrulanamadı (gerçek hata değil).
