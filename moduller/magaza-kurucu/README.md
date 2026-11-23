# Mağaza Kurucu modülü (sürüm 0.6.0)

Viral Ürün Ekibi eklentisinin mağaza kurma kolunun KAYNAĞI. Kullanıcıya giden beceri buradan üretilir:
`plugins/viral-urun-ekibi/skills/builder/` (elle düzenlenmez; `tools/build.py` yazar).

| Klasör | Ne |
|---|---|
| `skills/<bölüm>/` | 3 aşama, 6 bölümün kaynağı (sıra: `urun-analiz`, `teklif`, `marka`, `metinler`, `gorseller`, `shopify-kurulum`; her SKILL.md ≤ 5.120 bayt) |
| `src/tek/SKILL.md` | beceri girişi (bölüm yönlendiricisi). Ekibin tek lideri `captain` becerisidir; bu dosya yalnız bölümleri sıralar |
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
şema, örnek ve doğrulayıcı `src/ortak/sozlesme/` (kaynak; eklentideki kopya `plugins/viral-urun-ekibi/ortak/sozlesme/`,
`python3 scripts/sozlesme_esitle.py` ile eşitlenir), yazıcı-okuyucu betik `plugins/viral-urun-ekibi/ortak/paket.py`.

Tek başına ChatGPT becerisi (`dist/chatgpt/builder.zip`) aynı kaynaktan üretilir; ekip lideri ve köprü betiği o pakette yoktur.
