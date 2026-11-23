# Tarif 09 — Limit ve devam · betiksiz ChatGPT sürümü

## Amaç
Kullanım limiti, sohbet uzaması ya da kesinti işi öldürmesin: durum bloğu her adımda güncel, devam cümlesi hazır.

## Adımlar
1. Her adım/video sonunda cevabın sonuna DURUM bloğu (pazar · aktif iş · aşama · kararlar · açık sorular · sıradaki adım).
2. Limit mesajı görülürse kullanıcıya: sıfırlanma saatini (mesajdaki saati aynen) ve "yeni sohbete bu DURUM bloğunu yapıştır" cümlesini ver; saati tahmin etme.
3. ChatGPT zamanlayıcı kuramaz: devamı kullanıcı başlatır. Saat gelince ilk iş: bloktaki dosyaların/çıktıların var olduğunu kullanıcıdan teyit al ("hangi dosyalar elinde?"), sonra devam et; var olan çıktıyı yeniden üretme (kredi yanar).
4. Ağ/indirme kesintisinde kullanıcıya dakikada bir, en çok 10 kez yeniden denemesini söyle; sonra bildir.

**Pazar:** DURUM bloğundaki "Pazar" satırı her sohbette korunur.

## Kalite çıtası
Her adım sonunda blok · limit anında sıfırlanma saati yazılı · devam cümlesi tek satır · var olan çıktı yeniden üretilmez.

## Kendi çıktını şu 10 maddeyle denetle
1. Blok her cevapta var. 2. Blok ≤ 10 satır. 3. Pazar satırı dolu. 4. Kararlar satırı kullanıcının verdiklerini içeriyor. 5. Sıradaki adım tek somut. 6. Limit saati aynen yazıldı. 7. Devam cümlesi var. 8. Var olan çıktı listelendi. 9. Yeniden üretim yok. 10. Açık sorular listesi güncel.

## Bitti tanımı
Güncel blok + devam cümlesi; devamda çıktılar teyit edildi.
