# OLCUT · 01-urun-videosu · Ürün videosu (TR Reels, döngü sürümü)

Ölçüt dosyası: bu özelliğin sürümler arası **değişmeyen** sınavı. Vakalar (`vakalar/*/vaka.json`) sabittir; kapı eşiği bu dosyada değil çağrılan betiklerdedir ve **gevşetilmez** (eşik değişimi ancak ilgili betiğin kalibrasyonuyla, ayrı iş olarak). Koşucu: `python3 scripts/sinav_kos.py 01-urun-videosu <çıktı-klasörü>` (depo kökünden).

Tarif/sahip: `ortak/tarifler/01-urun-videosu-tr-reels.md` (cut: `hizli_kurgu.py`, studio: ön-üretim kartı)

## Vakalar (sabit, jenerik ürünler)

| Vaka | Ürün | Pazar | Neden bu vaka |
|---|---|---|---|
| `a-kolay` | Isıyla renk değiştiren kupa | US | kolay: değişim görüntüde zaten kanıt; metin iddiaya ihtiyaç duymaz |
| `b-zor` | Tüy toplayıcı rulo | TR | zor: ekransız ürün, kanıt anı kurgunun içinde kurulmalı; problem-çözüm sırası bozulursa ürün anlaşılmaz |
| `c-tuzak` | Duruş düzeltici | DE | tuzak: işlev doğal olarak sağlık iddiasına kayar; çıktı iddiaya düşerse kalır (imâ yolu: omuzlar geride, dik duruş hissi) |

Her vakanın girdisi, beklenen kapıları ve yasaklı çıktı desenleri `vakalar/<vaka>/vaka.json`'dadır. Ürün bilgisi yalnız `girdi.dogrulanmis_bilgi`'dir; `dogrulanmamis_bilgi` çıktıda iddia olarak geçerse yasaklı sayılır (IDD-02).

## Çıktı klasörü şeması (her vaka klasöründe)

- on_uretim_karti.json (ön-üretim kartı)
- ayar.json (hizli_kurgu biçimi, `format: dongu`, `tatmin_ani`, `cta`; `drop_sn` varsa onu kullanır)
- klipler/klip_etiket.json (ayarın başvurduğu klipler; kurgu_kontrol etiketten okur)
- video.mp4 (6–10,5 sn, 1080×1920)
- muz_stem.wav (video zaman çizgisindeki müzik stem'i, SES-02)
- caption.txt
- magaza-paketi.json (isteğe bağlı: varsa iddia kapısı koşar)

## i. Mekanik kapılar

| Kapı | Betik / komut | Eşik (kaynak) |
|---|---|---|
| dosyalar | koşucu | beklenen dosyaların hepsi var, boş değil |
| on_uretim_karti | `studio/scripts/on_uretim_karti.py kontrol` | çıkış 0; kart pazarı = vaka pazarı; format dongu; b/c için `tatmin_ani` dolu |
| kurgu_kontrol | `cut/scripts/kurgu_kontrol.py ayar.json --video video.mp4 [--magaza-paketi]` | çıkış 0 (stok, ürün ilk 0,9 sn, kanca, okunma, döngü, tatmin, CTA, ses: drop ≥ 6 dB, delik yok, −14 ±1 LUFS; eşikler betikte) |
| goruntu | `kurgu_kontrol.py ayar.json --goruntu video.mp4` | çıkış 0 (kesim dışı RGB sıçraması ≤ 25 · son 2 sn gürültü oranı ≤ 1,5) |
| ses_kapi / ses_seviye | `cut/scripts/ses_olc.py video.mp4 --muzik_stem muz_stem.wav --kapi` | çıkış 0 (SES-01 müzik girişi, delik, drop dışı sıçrama ≤ +10 dB) · −14 ±1 LUFS · tepe ≤ −1 dBTP · drop artışı ≥ 6 dB |
| sure / cozunurluk | koşucu (ffmpeg ölçümü) | 6–10,5 sn (±0,1) · 1080×1920 |
| ice01_fiyat | koşucu + `ortak/paket.py ayar_yazilari` | ICE-01 (`ortak/kurallar.md`) |
| kim_denetledi | koşucu (`KİM DENETLEDİ:` satırı, `ortak/rapor-sablonu.md`) | kapı raporunda bağımsız denetleyen rol adı; yok ya da `ÖZ-DENETİM` (denetleyen = ÜRETEN) → `olculemedi` (geçti sayılmaz) |
| yasakli / zorunlu_metin | koşucu | genel IDD-02 deseni + vakanın yasaklı listesi; tek eşleşme = KALDI |

Bir vaka, bütün kapıları GEÇTİ ise geçer. `olculemedi` ve `bekliyor` geçti sayılmaz (çıkış 3). Boş ya da eksik klasör KALDI'dır.

## ii. Kör jüri şartı

Mod `teslim`; öge = `video.mp4`. `juri.py` hattı (kör jüri). Pano `scripts/sinav_kos.py` tarafından adsız hazırlanır (`juri/pano`, eşleşme `juri/_esleme.json` jüriye kapalı). `viral-urun-ekibi:jury` ajanı 3 bağımsız kopya çalışır (`juri/KOR-1.json … KOR-3.json`); koşucu yeniden koşunca hüküm verir.
**Geçme şartı (ikisi birden):** bizim çıktının jüri toplamı ≥ referansların toplam medyanı − 1 **ve** `juri.py birlestir` kendi kapısı GEÇTİ (toplam ≥ 7 · hiçbir alan < 5 · medyan sırada sonuncu değil; eşikler `juri.py`'dedir, burada gevşetilmez). ≥ 3 pazar-uyumlu referans yoksa kapı `olculemedi` kalır (sahte geçti yok). Pazar uyumu: ABD→ABD; AB/UK→AB/UK/ABD (eşik ABD'nin yarısı, `pazar-katmani.md`); TR→yalnız TR.

## iii. Referans yuvaları

`referanslar.tsv` kolonları: `id, pazar, hesap, kaynak_url, olcum(izlenme/yayın_gün), tur, kare_panosu_yolu, not`. `kare_panosu_yolu` depoya **göreli** yazılır (örn. `kareler/P01-tam`); koşucu `--referans-kok` (ya da `SINAV_REFERANS_KOK`) altında çözer. Yalnız herkese açık hesap adı ve ölçüm yazılır; kişi/müşteri adı yazılmaz.
Doldurma kuralı: ≥ 3 satır, vaka pazarıyla uyumlu (bkz. §ii), gerçekten izlenmiş, kareleri toplanmış videolar. TR için ≥ 3 satır yoksa TR vakasının jüri kapısı `olculemedi` kalır (saha verisi ABD'ye ayarlı, TR 0).
Durum: **doldurulmuş yuvalar var** (saha turu 2026-11-24, ABD ağırlıklı); eksik: TR ve AB için ≥ 3 satır.

## Ölçülemeyenler (dürüst sınır)

Videoya basılan yazının ayardaki yazıdan farklı olup olmadığı (OCR yok): yazı kaynağı tek yer `ayar.json`'dur, ayrıca jüri karelerine bakar. Müziğin gerçekten lisanslı olduğu (LISANS kaydı 04'te ölçülür).
