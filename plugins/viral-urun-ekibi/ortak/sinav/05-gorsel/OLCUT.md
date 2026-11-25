# OLCUT · 05-gorsel · Ürün/mağaza görselleri (ChatGPT ile üretilen set)

Ölçüt dosyası: bu özelliğin sürümler arası **değişmeyen** sınavı. Vakalar (`vakalar/*/vaka.json`) sabittir; kapı eşiği bu dosyada değil çağrılan betiklerdedir ve **gevşetilmez** (eşik değişimi ancak ilgili betiğin kalibrasyonuyla, ayrı iş olarak). Koşucu: `python3 scripts/sinav_kos.py 05-gorsel <çıktı-klasörü>` (depo kökünden).

Tarif/sahip: `skills/builder/gorseller/references/kabul-kontrolu.md`, `ortak/roller/sentinel/*.md`, `ortak/roller/panel`

## Vakalar (sabit, jenerik ürünler)

| Vaka | Ürün | Pazar | Neden bu vaka |
|---|---|---|---|
| `a-kolay` | Isıyla renk değiştiren kupa | TR | kolay: değişim görüntüde zaten kanıt; metin iddiaya ihtiyaç duymaz |
| `b-zor` | Tüy toplayıcı rulo | DE | zor: ekransız ürün, kanıt anı kurgunun içinde kurulmalı; problem-çözüm sırası bozulursa ürün anlaşılmaz |
| `c-tuzak` | Duruş düzeltici | US | tuzak: işlev doğal olarak sağlık iddiasına kayar; çıktı iddiaya düşerse kalır (imâ yolu: omuzlar geride, dik duruş hissi) |

Her vakanın girdisi, beklenen kapıları ve yasaklı çıktı desenleri `vakalar/<vaka>/vaka.json`'dadır. Ürün bilgisi yalnız `girdi.dogrulanmis_bilgi`'dir; `dogrulanmamis_bilgi` çıktıda iddia olarak geçerse yasaklı sayılır (IDD-02).

## Çıktı klasörü şeması (her vaka klasöründe)

- stil.json ({"zemin": "#RRGGBB"} tek zemin HEX'i)
- gorseller/g0-*.png (feed karesi, ≥ 1500×1500, yazısız)
- gorseller/galeri-*.png (≥ 3, 1:1)
- gorseller/b1-*.png (1920×800) · gorseller/b2-*.png (1080×1350)
- gorseller/<görsel adı>.txt (görselin içindeki beklenen yazı; OCR kapısı için; yazısız görselde boş dosya)
- METINLER.md (görsellerde geçen bütün yazı) · URUN-KILIDI.md · SADAKAT.md (sentinel raporu, varsa)

## i. Mekanik kapılar

| Kapı | Betik / komut | Eşik (kaynak) |
|---|---|---|
| dosyalar | koşucu | beklenen dosyalar var |
| K3_tuval_olcu | koşucu (Pillow; `kabul-kontrolu.md` §3 formülü) | boyutlar (galeri 1:1, B1 1920×800, B2 1080×1350, G0 ≥ 1500² ve ürün uzun kenarı %75–86) · dört köşe zemin HEX ±3 · her kenarda boş pay ≥ %6 |
| K2_yazim_ocr | `builder/gorseller/scripts/ocr_kontrol.py <görsel> <ad>.txt` | çıkış 0 (eksik/fazla yazı yok). OCR motoru kurulu değilse `olculemedi` (göz kontrolü sentinel `yazim`) |
| K1_sadakat | (betik yok) | `olculemedi`: ürün sadakati gözle (sentinel `kilit`); SADAKAT.md'de ❌ varsa KALDI, temiz olsa da geçti sayılmaz |
| kim_denetledi | koşucu (`KİM DENETLEDİ:` satırı, `ortak/rapor-sablonu.md`) | kapı raporunda bağımsız denetleyen rol adı; yok ya da `ÖZ-DENETİM` (denetleyen = ÜRETEN) → `olculemedi` (geçti sayılmaz) |
| yasakli / zorunlu_metin | koşucu | METINLER.md ve görsel yan dosyalarında kargo/indirim/garanti/klinik/yüzde/sağlık iddiası yok (K4, kritik 4) |

Bir vaka, bütün kapıları GEÇTİ ise geçer. `olculemedi` ve `bekliyor` geçti sayılmaz (çıkış 3). Boş ya da eksik klasör KALDI'dır.

## ii. Kör jüri şartı

Mod `teslim`; öge = `gorseller/` klasörü (referanslar `tur=gorsel`). `juri.py` hattı (kör jüri). Pano `scripts/sinav_kos.py` tarafından adsız hazırlanır (`juri/pano`, eşleşme `juri/_esleme.json` jüriye kapalı). `viral-urun-ekibi:jury` ajanı 3 bağımsız kopya çalışır (`juri/KOR-1.json … KOR-3.json`); koşucu yeniden koşunca hüküm verir.
**Geçme şartı (ikisi birden):** bizim çıktının jüri toplamı ≥ referansların toplam medyanı − 1 **ve** `juri.py birlestir` kendi kapısı GEÇTİ (toplam ≥ 7 · hiçbir alan < 5 · medyan sırada sonuncu değil; eşikler `juri.py`'dedir, burada gevşetilmez). ≥ 3 pazar-uyumlu referans yoksa kapı `olculemedi` kalır (sahte geçti yok). Pazar uyumu: ABD→ABD; AB/UK→AB/UK/ABD (eşik ABD'nin yarısı, `pazar-katmani.md`); TR→yalnız TR.
Görselin zevk rubriği için `panel` ajanı (7 boyut) ek kanıttır; geçti/kaldı hükmü `juri.py` medyanındandır.

## iii. Referans yuvaları

`referanslar.tsv` kolonları: `id, pazar, hesap, kaynak_url, olcum(izlenme/yayın_gün), tur, kare_panosu_yolu, not`. `kare_panosu_yolu` depoya **göreli** yazılır (örn. `kareler/P01-tam`); koşucu `--referans-kok` (ya da `SINAV_REFERANS_KOK`) altında çözer. Yalnız herkese açık hesap adı ve ölçüm yazılır; kişi/müşteri adı yazılmaz.
Doldurma kuralı: ≥ 3 satır, vaka pazarıyla uyumlu (bkz. §ii), gerçekten izlenmiş, kareleri toplanmış videolar. TR için ≥ 3 satır yoksa TR vakasının jüri kapısı `olculemedi` kalır (saha verisi ABD'ye ayarlı, TR 0).
Durum: **boş başlık** — lider dolduracak.

## Ölçülemeyenler (dürüst sınır)

K1 ürün sadakati, K2'nin göz kontrolü ve yapay görünüm işaretleri betikle ölçülmez; bu iki kapı `olculemedi` olduğu sürece 05 çıkışı 0 olamaz.
