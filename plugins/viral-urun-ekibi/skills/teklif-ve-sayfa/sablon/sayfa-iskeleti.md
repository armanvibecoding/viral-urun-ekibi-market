# {URUN_ADI} — ürün sayfası taslağı ({PAZAR}, {TARIH})

> Taslak. Her iddia `[K: kanit/NN#bölüm]` ile kanıt dosyasına bağlanır; bağlanamayan cümle silinir.
> Sayılar yalnız gerçek kaynaktan; yoksa `{YER_TUTUCU}` kalır ve yayından önce kurucu doldurur.
> Sayfa metni hedef pazarın dilinde yazılır; bu iskelet yalnız sırayı ve her bölümün işini verir.

## 1. Hero (ilk ekran)
- Görsel: mekanizmayı tek planda gösteren video/gif (gerçek çekim ya da etiketli AI) `[K: …#6]`
- Başlık: tek somut fayda (kimin hangi sorunu) — sıfat değil sonuç
- Alt satır: 2–3 gerçek özellik (ölçü/malzeme/uyumluluk)
- Fiyat bloğu: `{FIYAT}` · çizili fiyat yalnız teklif.tsv'de kanıtlıysa · paket seçici (1x / 2x / 3x)
- Güven şeridi: kargo vaadi (`{TESLIM_GUN}` gün) · garanti · ödeme yöntemleri ikonları
- Satın al düğmesi

## 2. Video / gösterim
- 15–30 sn: problem → tek hamle çözüm (reklam videosunun uzun hâli). Gerçek kullanım; AI ise etiket.

## 3. Mekanizma — nasıl çalışıyor
- 3 adım, her adım bir görsel + tek cümle `[K: …#7]`
- "Kim için değil" satırı (iade riskini düşürür)

## 4. Özellikler ve ölçüler
- Tablo: ölçü, ağırlık, malzeme, kutu içeriği, uyumluluk (ürün sayfası / numune ölçümü)
- AB: GPSR bilgileri (üretici, AB sorumlu kişi, ürün tanımlayıcı, uyarılar)

## 5. Sosyal kanıt (yalnız gerçek)
- Yorum uygulaması bloğu: `{GERCEK_YORUM_SAYISI}` yorum · `{GERCEK_ORTALAMA_PUAN}` — doğrulanmış alıcı etiketiyle
- Alıcı fotoğraf/videoları (izinli UGC)
- Henüz gerçek yorum yoksa bu bölüm **çıkarılır**; yerine mekanizma videosu ve garanti öne alınır

## 6. İtiraz SSS
- `itiraz-sss.md`'den 5–8 soru; sıra: rakip yorumlarında en sık geçen önce

## 7. Garanti
- Garanti metni (teklif.tsv `garanti`) + iade adımları + iade süresi; kim öder

## 8. Kapanış
- Fiyat bloğunun tekrarı + paket seçici + satın al düğmesi
- Satıcı bilgisi / yasal bağlantılar (TR: mesafeli satış sözleşmesi, ön bilgilendirme · DE: Impressum)

## Bulunamayan veri
- (doldur: hangi iddia/sayı neden sayfaya girmedi)
