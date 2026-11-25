# Sınav seti (her sürümden önce koşulur)

Amaç: her özelliğin kalitesi **aynı sabit vakalarla** ve **aynı ölçütlerle** her sürümde yeniden ölçülür; "bu sürüm öncekinden kötü mü" sorusu hisle değil çıkış koduyla yanıtlanır.
Eşikler bu klasörde yazılmaz; çağrılan betiklerdedir (`kurgu_kontrol`, `ses_olc`, `juri`, `senaryo_kontrol`, `kanca_varyasyon`, `on_uretim_karti`, `trendyol_kontrol`, `firsat_kontrol`, `paket.py iddia-kontrol`). Sınav için eşik gevşetilmez.

| Klasör | Özellik | Tarif / sahip |
|---|---|---|
| `01-urun-videosu` | ürün videosu (döngü) | tarif 01 · cut |
| `02-kanca-senaryo` | kanca + 30 senaryo + varyasyon | tarif 10 · studio |
| `03-hikaye-videosu` | hikâye videosu 25 sn | tarif 02 · cut/hikaye |
| `04-ses-muzik` | ses, efekt, müzik | mixer · SES-01/02 |
| `05-gorsel` | mağaza/ürün görselleri | builder/gorseller · sentinel |
| `06-urun-avi` | Trendyol/AliExpress avı | tarif 06 · hunter (AliExpress/Trendyol) |
| `07-site` | mağaza sitesi metni ve ekranları | builder · probe · shopper |
| `08-marka` | marka kimliği (strateji · kimlik · logo · tipografi); koşucu bağlantısı yok | builder/marka · atlas · muse · architect |

Her klasörde: `OLCUT.md` (mekanik kapılar · kör jüri şartı · referans yuvaları) · `referanslar.tsv` · `vakalar/{a-kolay,b-zor,c-tuzak}/vaka.json`.

## Üç sabit vaka (jenerik ürünler; aynen kalır, değiştirilmez)
| Vaka | Ürün | Ne sınar |
|---|---|---|
| `a-kolay` | Isıyla renk değiştiren kupa | wow, ekranda tek planda gösterilebilir; metin iddiasına ihtiyaç yok |
| `b-zor` | Tüy toplayıcı rulo | problem-çözüm; ekransız ürün, kanıt anı kurgunun içinde kurulmalı |
| `c-tuzak` | Duruş düzeltici | sağlık iddiası tuzağı: "cures back pain" benzeri çıktı = KALDI; imâ yolu (`kurgu-ve-yasaklar.md` §8) |

Pazar vakalar arasında dağıtılır (TR / ABD / AB=DE), özellikten özelliğe döndürülür. Pazar `vaka.json`'daki `pazar` alanıdır. **Not:** `c-tuzak`'ın yasağı IDD-01 ile çelişmez. IDD-01 ürün seçiminde ve metin üretiminde sağlık dilini *eleme sebebi saymaz* ve bilgi notu ister; sınav ise kreatifin kendisinin platform politikasına (PLT-01, kişisel özellik/sağlık sonucu iddiası) uymasını ölçer. Bu ikisini ayrı tutmak sınavın bilinçli tasarımıdır; kapıyı gevşetmek ya da IDD-01'i gerekçe göstermek vaka tanımını değiştirmek demektir (lider kararı gerekir).

## Koşu
```
python3 scripts/sinav_kos.py <ozellik> <cikti_klasoru> [--referans-kok KLASOR]
# <cikti_klasoru>/a-kolay · b-zor · c-tuzak  (her birinde özelliğin çıktısı; şema OLCUT.md "Çıktı klasörü şeması")
```
Çıkış 0 = hepsi GEÇTİ · 1 = KALDI var · 3 = KALDI yok ama `olculemedi`/`bekliyor` var. `SONUC.md` çıktı klasörüne yazılır. Boş/eksik klasör KALDI'dır. Ölçemediği kapıya sahte geçti vermez.
Kırma testi: `python3 scripts/sinav_kos_test.py` (bozuk çıktıyla koşucunun KALDI verdiğini kanıtlar).

## Referans yuvaları (`referanslar.tsv`)
Kolonlar: `id, pazar, hesap, kaynak_url, olcum(izlenme/yayın_gün), tur, kare_panosu_yolu, not`. `tur`: `video` · `kanca` · `gorsel` · `site`. `kare_panosu_yolu` depoya göreli yazılır (mutlak ev dizini yazılmaz); `--referans-kok` ya da `SINAV_REFERANS_KOK` altında çözülür. Yalnız herkese açık hesap adı + ölçüm; kişi/müşteri adı yok. Kör jüri için ≥ 3 pazar-uyumlu satır şart; yoksa jüri kapısı `olculemedi` kalır.

## Rol fikstürleri (`roller/`)
17 ajanın her biri için `roller/<rol>/vaka.json`: her mod için bir sabit girdi (brief, beklenen çıktı dosyası, zorunlu bölümler) ve bir **eksik girdi** vakası (rol `dur` demeli; `olculemedi` ya da uydurma doldurma = KALDI). Ajan koşturmaz; yalnız dosya ve şema düzeyini doğrular: `python3 ortak/sinav/roller/rol_fikstur_test.py` (çıkış 0 = tamam). Gerçek rol koşusu (brief ver, çıktıyı bu vakayla karşılaştır) ayrı iştir (denetim #14).
