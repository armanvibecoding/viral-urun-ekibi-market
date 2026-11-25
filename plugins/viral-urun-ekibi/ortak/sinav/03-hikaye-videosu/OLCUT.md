# OLCUT · 03-hikaye-videosu · Hikâye videosu (organik, 25 sn)

Ölçüt dosyası: bu özelliğin sürümler arası **değişmeyen** sınavı. Vakalar (`vakalar/*/vaka.json`) sabittir; kapı eşiği bu dosyada değil çağrılan betiklerdedir ve **gevşetilmez** (eşik değişimi ancak ilgili betiğin kalibrasyonuyla, ayrı iş olarak). Koşucu: `python3 scripts/sinav_kos.py 03-hikaye-videosu <çıktı-klasörü>` (depo kökünden).

Tarif/sahip: `ortak/tarifler/02-hikaye-videosu-organik.md` (cut: `hikaye/uret.py`)

## Vakalar (sabit, jenerik ürünler)

| Vaka | Ürün | Pazar | Neden bu vaka |
|---|---|---|---|
| `a-kolay` | Isıyla renk değiştiren kupa | DE | kolay: değişim görüntüde zaten kanıt; metin iddiaya ihtiyaç duymaz |
| `b-zor` | Tüy toplayıcı rulo | US | zor: ekransız ürün, kanıt anı kurgunun içinde kurulmalı; problem-çözüm sırası bozulursa ürün anlaşılmaz |
| `c-tuzak` | Duruş düzeltici | TR | tuzak: işlev doğal olarak sağlık iddiasına kayar; çıktı iddiaya düşerse kalır (imâ yolu: omuzlar geride, dik duruş hissi) |

Her vakanın girdisi, beklenen kapıları ve yasaklı çıktı desenleri `vakalar/<vaka>/vaka.json`'dadır. Ürün bilgisi yalnız `girdi.dogrulanmis_bilgi`'dir; `dogrulanmamis_bilgi` çıktıda iddia olarak geçerse yasaklı sayılır (IDD-02).

## Çıktı klasörü şeması (her vaka klasöründe)

- ayar.json (hikâye ayarı; `kesimler`, `ses.drop`, `on_uretim_karti` alanı)
- on-uretim-karti.json (ayarın gösterdiği ad)
- stok/ (ayarın başvurduğu klipler ve ürün PNG'si; `--dogrula` dosya varlığına bakar)
- video.mp4 (25,0 sn, 1080×1920)
- muz_stem.wav (`ses/stem_<ad>/muz_teslim.wav` kopyası)
- caption.txt

## i. Mekanik kapılar

| Kapı | Betik / komut | Eşik (kaynak) |
|---|---|---|
| dosyalar | koşucu | beklenen dosyalar var |
| on_uretim_karti | `studio/scripts/on_uretim_karti.py kontrol` | çıkış 0; kart pazarı = vaka pazarı; format hikaye |
| hikaye_kur_dogrula | `cut/scripts/hikaye/hikaye_kur.py ayar.json --dogrula` | çıkış 0 (kart geçerli, kanca ilk karede, kesimler artan, fiyat/para birimi yok, klip dosyaları var) |
| sure / cozunurluk | koşucu | 25,0 sn ±0,1 · 1080×1920 |
| ses_kapi / ses_seviye | `ses_olc.py video.mp4 --muzik_stem muz_stem.wav --drop <ayar.ses.drop> --kapi` | çıkış 0 · −14 ±1 LUFS · tepe ≤ −1 dBTP · drop ≥ 6 dB |
| goruntu | `kurgu_kontrol.py --goruntu video.mp4 --kesimler <ayar.kesimler> --yalniz-goruntu` | çıkış 0 |
| kim_denetledi | koşucu (`KİM DENETLEDİ:` satırı, `ortak/rapor-sablonu.md`) | kapı raporunda bağımsız denetleyen rol adı; yok ya da `ÖZ-DENETİM` (denetleyen = ÜRETEN) → `olculemedi` (geçti sayılmaz) |
| yasakli / zorunlu_metin | koşucu | ayar, caption, kart metinlerinde yasaklı çıktı yok |

Bir vaka, bütün kapıları GEÇTİ ise geçer. `olculemedi` ve `bekliyor` geçti sayılmaz (çıkış 3). Boş ya da eksik klasör KALDI'dır.

## ii. Kör jüri şartı

Mod `teslim`; öge = `video.mp4`. `juri.py` hattı (kör jüri). Pano `scripts/sinav_kos.py` tarafından adsız hazırlanır (`juri/pano`, eşleşme `juri/_esleme.json` jüriye kapalı). `viral-urun-ekibi:jury` ajanı 3 bağımsız kopya çalışır (`juri/KOR-1.json … KOR-3.json`); koşucu yeniden koşunca hüküm verir.
**Geçme şartı (ikisi birden):** bizim çıktının jüri toplamı ≥ referansların toplam medyanı − 1 **ve** `juri.py birlestir` kendi kapısı GEÇTİ (toplam ≥ 7 · hiçbir alan < 5 · medyan sırada sonuncu değil; eşikler `juri.py`'dedir, burada gevşetilmez). ≥ 3 pazar-uyumlu referans yoksa kapı `olculemedi` kalır (sahte geçti yok). Pazar uyumu: ABD→ABD; AB/UK→AB/UK/ABD (eşik ABD'nin yarısı, `pazar-katmani.md`); TR→yalnız TR.

## iii. Referans yuvaları

`referanslar.tsv` kolonları: `id, pazar, hesap, kaynak_url, olcum(izlenme/yayın_gün), tur, kare_panosu_yolu, not`. `kare_panosu_yolu` depoya **göreli** yazılır (örn. `kareler/P01-tam`); koşucu `--referans-kok` (ya da `SINAV_REFERANS_KOK`) altında çözer. Yalnız herkese açık hesap adı ve ölçüm yazılır; kişi/müşteri adı yazılmaz.
Doldurma kuralı: ≥ 3 satır, vaka pazarıyla uyumlu (bkz. §ii), gerçekten izlenmiş, kareleri toplanmış videolar. TR için ≥ 3 satır yoksa TR vakasının jüri kapısı `olculemedi` kalır (saha verisi ABD'ye ayarlı, TR 0).
Durum: **boş başlık** — lider dolduracak.

## Ölçülemeyenler (dürüst sınır)

HyperFrames render kalitesi/animasyon pürüzü (kareler jüriye gider, betik ölçmez). Stok klibin lisansı (kaynak kaydı elle).
