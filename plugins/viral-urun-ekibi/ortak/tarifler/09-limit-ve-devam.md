# Tarif 09 — Limit ve devam

## Amaç
Kullanım limiti, bağlam dolması ya da ağ kesintisi işi öldürmesin: durum dosyada, devam zamanı kurulu, saat gelince doğrulayarak sürer.

## Girdi
Çalışan iş + `DURUM.md` (proje köküne ya da `.ekip/DURUM.md`).

## Adımlar
1. **Her video/adım sonunda** `DURUM.md` güncelle: ne bitti (dosya yoluyla), ne sırada (tek somut komut), kapı çıkış kodları, harcanan kredi, açık sorular.
2. Limit mesajı görülünce: sıfırlanma saatini mesajdan oku, `DURUM.md` başına yaz: `LİMİT: <saat> sıfırlanır · devam komutu: …`.
3. Devam zamanlayıcısı kur: `schedule` becerisi (tek seferlik) ya da `CronCreate` ile sıfırlanma saatinden 2–5 dk sonrasına, istem: "DURUM.md'yi oku, ilk açık adımdan devam et". Zamanlayıcı kurulamıyorsa kullanıcıya tek satır: saat ve devam cümlesi.
4. Saat geçince lider kendisi doğrular: `DURUM.md`'deki son çıktı dosyaları gerçekten var mı (`ls`), son kapı çıktısı 0 mı; sonra devam eder. "Bitti" iddiası ölçülmeden kabul edilmez.
5. Ağ kesintisi (push/indirme): dakikada bir, en çok 10 kez arka planda yeniden dene; sonra kullanıcıya bildir.
6. Bağlam dolmadan önce `DURUM.md` ve (varsa) `.ekip/DERSLER.md` güncel olmalı; oturum yeniden başladığında ilk iş DURUM.md okumak.

## Kalite çıtası
Her adım sonunda DURUM.md ≤ 60 sn önce güncellenmiş · limit anında sıfırlanma saati yazılı · devam komutu tek satır, çalıştırılabilir · var olan çıktılar yeniden üretilmez (dosya varsa atla).

## Kapılar
Devam sonrası ilk iş: son kapı çıktısı yeniden okunur (çıkış 0) · çıktı dosyaları `ls` ile doğrulanır.

## Sık hata ve düzeltmesi
- Durum yalnız sohbette → dosyaya yaz; sohbet kaybolur.
- Devam ederken var olan video yeniden üretildi (kredi yandı) → önce `ls`, dosya varsa atla.
- Sıfırlanma saati tahmin edildi → mesajdaki saati aynen yaz, tahmin etme.

## Bitti tanımı
`DURUM.md` güncel + zamanlayıcı kurulu (ya da kullanıcıya devam satırı verildi) + saat geçince doğrulama notu eklendi.
