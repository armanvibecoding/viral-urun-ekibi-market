# OLCUT · 04-ses-muzik · Ses, efekt ve müzik

Ölçüt dosyası: bu özelliğin sürümler arası **değişmeyen** sınavı. Vakalar (`vakalar/*/vaka.json`) sabittir; kapı eşiği bu dosyada değil çağrılan betiklerdedir ve **gevşetilmez** (eşik değişimi ancak ilgili betiğin kalibrasyonuyla, ayrı iş olarak). Koşucu: `python3 scripts/sinav_kos.py 04-ses-muzik <çıktı-klasörü>` (depo kökünden).

Tarif/sahip: `cut/referans/ses-tasarimi.md`, `agents/mixer.md`, `ortak/kurallar.md` SES-01/SES-02

## Vakalar (sabit, jenerik ürünler)

| Vaka | Ürün | Pazar | Neden bu vaka |
|---|---|---|---|
| `a-kolay` | Isıyla renk değiştiren kupa | US | kolay: değişim görüntüde zaten kanıt; metin iddiaya ihtiyaç duymaz |
| `b-zor` | Tüy toplayıcı rulo | TR | zor: ekransız ürün, kanıt anı kurgunun içinde kurulmalı; problem-çözüm sırası bozulursa ürün anlaşılmaz |
| `c-tuzak` | Duruş düzeltici | DE | tuzak: işlev doğal olarak sağlık iddiasına kayar; çıktı iddiaya düşerse kalır (imâ yolu: omuzlar geride, dik duruş hissi) |

Her vakanın girdisi, beklenen kapıları ve yasaklı çıktı desenleri `vakalar/<vaka>/vaka.json`'dadır. Ürün bilgisi yalnız `girdi.dogrulanmis_bilgi`'dir; `dogrulanmamis_bilgi` çıktıda iddia olarak geçerse yasaklı sayılır (IDD-02).

## Çıktı klasörü şeması (her vaka klasöründe)

- video.mp4 (karışmış)
- muz_stem.wav (müziğin video zaman çizgisine yerleştirilmiş hâli)
- ses.json ({"drop_sn": <videodaki drop saniyesi>})
- LISANS.md (müzik + efekt lisans kaydı; "Kurucu seçti: <tarih>, söz kapısı: temiz | enstrümantal" satırı)
- vo.txt (seslendirme varsa dökümü; yasaklı taramasına girer)

## i. Mekanik kapılar

| Kapı | Betik / komut | Eşik (kaynak) |
|---|---|---|
| dosyalar | koşucu | beklenen dosyalar var |
| ses_kapi | `ses_olc.py video.mp4 --muzik_stem muz_stem.wav --drop <ses.json drop_sn> --kapi` | çıkış 0 (SES-01: başlangıç ≤ −20 dB · rampa 1,5–3 sn · basamak ≤ +10 dB · açılış olayı ≥ −6 dB; delik yok; drop dışı sıçrama ≤ +10 dB) |
| ses_seviye | koşucu (ses_olc JSON'u) | −14 ±1 LUFS · tepe ≤ −1 dBTP · drop artışı ≥ 6 dB |
| sure | koşucu | 6–25 sn |
| lisans_kaydi | koşucu | söz kapısı satırı · kaynak (URL/kullanıcının dosyası/sentetik) · lisans adı · telifli parça adı yok (SES-02; sahada gördüğümüz tanınmış parçalar kara listede) |
| kim_denetledi | koşucu (`KİM DENETLEDİ:` satırı, `ortak/rapor-sablonu.md`) | kapı raporunda bağımsız denetleyen rol adı; yok ya da `ÖZ-DENETİM` (denetleyen = ÜRETEN) → `olculemedi` (geçti sayılmaz) |
| yasakli / zorunlu_metin | koşucu | vo.txt/LISANS.md gibi metinlerde yasaklı çıktı yok |

Bir vaka, bütün kapıları GEÇTİ ise geçer. `olculemedi` ve `bekliyor` geçti sayılmaz (çıkış 3). Boş ya da eksik klasör KALDI'dır.

## ii. Kör jüri şartı

**Uygulanmaz.** Jüri (`jury`) ve mixer sesi dinleyemez; kör jüri panosu ses içermez. Yerine ölçüm kapıları (yukarıda) + kullanıcının kulak onayı (teslim notuna yazılır). Bu bilinçli bir boşluktur: ses kalitesinin zevk kapısı yoktur.

## iii. Referans yuvaları

`referanslar.tsv` kolonları: `id, pazar, hesap, kaynak_url, olcum(izlenme/yayın_gün), tur, kare_panosu_yolu, not`. `kare_panosu_yolu` depoya **göreli** yazılır (örn. `kareler/P01-tam`); koşucu `--referans-kok` (ya da `SINAV_REFERANS_KOK`) altında çözer. Yalnız herkese açık hesap adı ve ölçüm yazılır; kişi/müşteri adı yazılmaz.
Doldurma kuralı: ≥ 3 satır, vaka pazarıyla uyumlu (bkz. §ii), gerçekten izlenmiş, kareleri toplanmış videolar. TR için ≥ 3 satır yoksa TR vakasının jüri kapısı `olculemedi` kalır (saha verisi ABD'ye ayarlı, TR 0).
Durum: **boş başlık** — lider dolduracak.

## Ölçülemeyenler (dürüst sınır)

Müziğin hit/tanınma gücü (müzik verisi ölçülmedi, `muzik-kutuphanesi.md`); sesin 'TikTok yerlisi' hissi; efekt kaynağının gerçek lisansı (kayıt var mı bakılır, kaynak sayfa elle doğrulanır).
