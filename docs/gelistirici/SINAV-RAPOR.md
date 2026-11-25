# Sınav seti raporu (2026-11-24)

Durum: 7/7 özellik klasörü + koşucu + kırma testi yeşil. COMMIT/PUSH yapılmadı.

## Değişen / eklenen dosyalar
- `plugins/viral-urun-ekibi/ortak/sinav/README.md` · `<özellik>/OLCUT.md` · `<özellik>/referanslar.tsv` · `<özellik>/vakalar/{a-kolay,b-zor,c-tuzak}/vaka.json` (7 özellik × 3 vaka = 21 vaka)
- `scripts/sinav_kos.py` (koşucu) · `scripts/sinav_kos_test.py` (kırma testi)
- `plugins/viral-urun-ekibi/ortak/tarifler/README.md` ("Her sürümden önce sinav_kos" bölümü)
- `plugins/viral-urun-ekibi/ekler/chatgpt/tarifler/sinav-kontrol-listesi.md` (yeni, elle liste) + aynı klasörün `README.md` son satırı
- Dokunulmadı: `skills/cut/hf-sablonlar/`, `tipografi-ve-kanca-gorseli.md`, hikaye/*.py (git'te görünen `M` hikaye dosyaları başka ajanın).

## Test çıkışları (24 Kas 2026)
| Komut | Sonuç |
|---|---|
| `python3 scripts/sinav_kos_test.py` | 69 test, 0 kaldı (çıkış 0; ≈4 dk, 03 gerçek hikâye hattını koşar) |
| `python3 scripts/sinav_kos_test.py --hizli` | 61 test, 0 kaldı (03 atlanır) |
| `python3 scripts/sozlesme_test.py` | 49/49 geçti |
| `python3 scripts/musteri_icerik_kontrol.py` | GEÇTİ |
| `python3 moduller/magaza-kurucu/tools/build.py --check` | SONUÇ: GEÇTİ (yalnız boyut uyarıları) |
| `python3 -m pytest -q moduller` | 72 geçti, 20 atlandı |
| `sh scripts/anonim_kontrol.sh` | 5 eşleşme, HEPSİ `docs/gelistirici/REFERANS-0.6.0-DURUM.md` (lider dosyası, benim değil); benim dosyalarımda eşleşme yok |
| `python3 -m pytest -q` (depo kökü) | ÖNCEDEN BOZUK, benim değişikliğim değil: `ortak/excel_test.py` toplama sırasında `openpyxl` yok diye `sys.exit(3)` → INTERNALERROR. `moduller` altı yeşil. |

## Kırma testinin kanıtladığı (özet)
- Her özellikte önce DOĞRU sentetik çıktı kapıları geçer, sonra tek bozma ilgili kapıyı KALDI yapar: süre 18/12 sn · yasaklı iddia (ayar, caption, kanca, VO, METINLER, sayfa, tablo) · ekranda fiyat · sessiz ses · müzik stem'i yok · telifli parça · ekransız vaka ekranlı ayarlı · 12 senaryo · 6 kanca · aynı aile art arda · kenar payı < %6 · yanlış B1 boyutu · SADAKAT ❌ · onaysız sayı iddiası · bozuk aday tablosu · zorunlu platform notu yok.
- Boş klasör, hiç olmayan klasör, eksik dosya → KALDI, çıkış 1.
- Mekanik kapılar yeşilken jüri referansı yoksa çıkış 3 (0 değil). Çıkış 0'ın ulaşılabilir olduğu da kanıtlı: sahte referans + 3 sahte KOR kopyasıyla 01 jüri GEÇTİ → çıkış 0; düşük puanda KALDI → çıkış 1. 04 ve 06'da jüri tanımsız olduğu için doğru çıktıda çıkış 0.

## Kararlar ve dürüst sınırlar (lider bilsin)
1. **Çıkış kodu:** 0 hepsi GEÇTİ · 1 KALDI var · 3 KALDI yok ama olculemedi/bekliyor var. Bugünkü gerçek hâl: hiçbir özellik 0 veremez, çünkü referans yuvaları boş/yetersiz (01–03, 05, 07) ya da ölçen betik yok (05, 07).
2. **c-tuzak ve IDD-01:** `ortak/kurallar.md` IDD-01 sağlık dilini "eleme sebebi değil" sayar. Senin kararın gereği sınav yine de "cures back pain" benzeri çıktıyı KALDI sayıyor (PLT-01, kişisel özellik/sağlık sonucu iddiası). Çelişki değil ayrı kapı; `ortak/sinav/README.md`'de yazılı. Bu vakayı gevşetmek sana ait karar.
3. **Jüri geçme şartı iki şartlı:** bizim toplam ≥ referans toplam medyanı − 1 **ve** `juri.py`'nin kendi eşikleri (≥ 7, alan ≥ 5, sonuncu değil). Yalnız göreli şart juri.py'den gevşek olurdu; yapmadım.
4. **Jüri uygulanmaz (gerekçeli):** 04 (jüri sesi dinleyemez) ve 06 (ürün kararı kanıt kapısı). Bunlar `uygulanmaz` yazar, kapıyı sessizce geçmez.
5. **05 gorsel:** ölçülenler boyut, zemin HEX ±3, kenar payı ≥ %6, G0 ürün %75–86, yasaklı metin. K1 sadakat betiksiz → `olculemedi` (SADAKAT.md'de ❌ varsa KALDI, temizse yine geçti sayılmaz). K2 OCR: `ocr_kontrol.py` + görsel yanında `<ad>.txt` varsa koşar; OCR motoru bu makinede kurulu olmayabilir (o zaman `olculemedi`). Testte K2 yolu yalnız "txt yok → olculemedi" olarak sınandı (OCR yok).
6. **07 site:** iddia kapısı gerçek (`paket.py iddia-kontrol`); hız/erişim/arama/dönüşüm dört kapısı için depoda ölçen betik yok → `olculemedi`.
7. **Pazar uyumu (jüri referansı):** ABD→ABD; AB/UK→AB/UK/ABD; TR→yalnız TR. Saha verisi TR'siz → her özellikte TR vakasının jüri kapısı TR referansı gelene kadar `olculemedi`.
8. **Vaka pazarları** özellikten özelliğe döner (US/TR/DE): 01 a=US b=TR c=DE · 02 a=TR b=DE c=US · 03 a=DE b=US c=TR · 04 = 01 gibi · 05 = 02 gibi · 06 = 03 gibi · 07 = 01 gibi. AB'yi `DE` temsil eder.
9. **Koşucu çıktı değişince:** jüri panosu bir kez hazırlanır; çıktı sonradan değişirse koşucu `bekliyor` verir ve `juri/` klasörünün silinmesini ister (eski kör kopyalar geçersiz).
10. 01 vakaları `format: dongu` (6–10,5 sn) varsayılan formatla kuruldu; 8–15 sn standart sürüm sınavda yok.

## Referans yuvaları (boş kalanlar) — lider dolduracak
`referanslar.tsv` kolonları: id, pazar, hesap, kaynak_url, olcum, tur, kare_panosu_yolu, not.
| Özellik | Durum |
|---|---|
| 01 ürün videosu | 7 satır dolu (ABD 6 + AB/FR 1; kareler `<referans-kok>/kareler/...` 4 hesap adı herkese açık, 3 satırda hesap ekranda okunmadı). **Eksik:** TR 0/3; AB için FR 1 + ABD kabul. `kaynak_url` hepsinde boş (Keşfet ızgarasından alındı, URL kaydedilmedi). `olcum` yayın günü `?`. |
| 02 kanca + senaryo | 7 satır dolu (tur=kanca; ABD 6 + FR 1). **Eksik:** TR 0/3, URL, yayın günü. |
| 03 hikâye videosu | boş başlık |
| 04 ses/müzik | boş başlık (jüri uygulanmaz; yuva ileride ses etiketi örnekleri için) |
| 05 görsel | boş başlık (tur=gorsel, nişe uygun ödüllü tasarım/ürün görselleri) |
| 06 ürün avı | boş başlık (jüri uygulanmaz) |
| 07 site | boş başlık (tur=site, 1440 ve 390 ekran görüntüleri) |
`kare_panosu_yolu` göreli yazıldı (`kareler/P01-tam`); koşucuya `--referans-kok <referans-kok>` verilir. Doğrulandı: 01 ve 02'deki 12 yolun hepsi o kökte var.

## Sonraki adım
Lider: 03, 05, 07 ve TR için referans satırlarını doldursun; sonra `scripts/sinav_kos.py 01-urun-videosu <çıktı>/01-urun-videosu --referans-kok …` ile ilk gerçek koşu. Gerçek çıktılar vaka klasörü şemasına (OLCUT.md "Çıktı klasörü şeması") konur.
