# Mağaza Kurucu modülü (sürüm 0.5.0)

Viral Ürün Ekibi eklentisinin mağaza kurma kolunun KAYNAĞI. Kullanıcıya giden beceri buradan üretilir:
`plugins/viral-urun-ekibi/skills/magaza-kurucu/` (elle düzenlenmez; `tools/build.py` yazar).

| Klasör | Ne |
|---|---|
| `skills/<aşama>/` | 5 aşamanın kaynağı: `urun-analiz`, `marka`, `gorseller`, `metinler`, `shopify-kurulum` (her SKILL.md ≤ 5.120 bayt) |
| `src/tek/SKILL.md` | beceri girişi (aşama yönlendiricisi). Ekibin tek lideri `ekip-lideri` becerisidir; bu dosya yalnız aşamaları sıralar |
| `src/ortak/` | birden çok aşamanın paylaştığı dosyalar (derleme aşama klasörlerine kopyalar) |
| `config/tema.json` | tam modda yüklenecek tema zip'inin kaydı (zip depoda yok; yoksa temasız mod) |
| `kaynak/KAYNAK-PROMPT.md` | aşamalara bölünen kaynak metnin anlık kopyası (`tests/test_kaynak_kapsam.py` kapsamı ölçer) |
| `tools/build.py` | eşitle + doğrula + birleşik beceriyi yaz; `--check` hiçbir şey yazmadan doğrular |
| `skills/gorseller/scripts/ocr_kontrol.py` | görseldeki yazıyı onaylı metinle karşılaştırır (RapidOCR; Türkçe harf için Tesseract `tur`, `OCR_TESSDATA`) |
| `tests/` | `python3 -m pytest moduller/magaza-kurucu/tests` |

## Komutlar (depo kökünden)
```
python3 moduller/magaza-kurucu/tools/build.py          # kopyaları eşitle, birleşik beceriyi ve dist zip'ini yaz
python3 moduller/magaza-kurucu/tools/build.py --check  # yalnız doğrula (çıkış 0 = geçti)
python3 -m pytest -q moduller/magaza-kurucu/tests
```
Köprü dosyaları (`urun-paketi.json`, `magaza-paketi.json`, `video-paketi.json`): anlatım `src/ortak/arayuz-sozlesmesi.md`,
şema ve betik `plugins/viral-urun-ekibi/sozlesme/`.

Tek başına ChatGPT becerisi (`dist/chatgpt/magaza-kurucu.zip`) aynı kaynaktan üretilir; ekip lideri ve köprü betiği o pakette yoktur.
