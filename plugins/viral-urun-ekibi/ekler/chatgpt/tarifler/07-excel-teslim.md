# Tarif 07 — Excel teslim · betiksiz ChatGPT sürümü

## Amaç
Ürün listesini 3 sayfalı, doğrulanmış tek biçimli Excel olarak teslim etmek.

## Adımlar
1. 12 alanlı tablo: urun · link · ilgi · ilgi_sayi · alis · satis · para · marj_kat · karar · neden · kaynak · tarih. `karar` yalnız SAT · SAT (koşullu) · İZLE · ELE.
2. Kod yorumlayıcıda (openpyxl varsa) üç sayfa yaz: **Ürünler** (10 sütun; sıralama SAT, SAT (koşullu), İZLE, ELE; her grupta ilgi büyükten küçüğe; karar renkleri SAT C6EFCE, koşullu E2F0D9, İZLE FFEB9C, ELE FFC7CE) · **Ayrıntı** (ham tablo, dondurulmuş + filtreli) · **Nasıl okunur**.
3. Yazdıktan sonra dosyayı yeniden aç ve say: satır sayısı = girdi, sayfa sayısı = 3, karar sütununda izin dışı değer yok. Tutmazsa dosyayı verme.
4. Dosyayı indirilebilir olarak ver (tek dosya; klasör değil). Kod yorumlayıcı yoksa `.csv` ver ve nedenini söyle.

**Pazar:** para sütunu pazar para birimi (TRY/USD/EUR).

## Kalite çıtası
Tam 3 sayfa · yazıdan sonra yeniden okunup ölçülmüş · sıralama doğru · karar değerleri izinli · indirilebilir tek dosya.

## Kendi çıktını şu 10 maddeyle denetle
1. 12 alan eksiksiz. 2. Karar değerleri izinli. 3. 3 sayfa var. 4. Ürünler sayfası 10 sütun. 5. Sıralama doğru. 6. Renkler doğru. 7. Ayrıntı dondurulmuş+filtreli. 8. Dosya yeniden açıldı, satır sayısı eşit. 9. Tek dosya (klasör değil). 10. Özet satırı: "N ürün (SAT a / SAT-koşullu b / İZLE c / ELE d)" sohbette.

## Bitti tanımı
İndirilebilir dosya + özet satırı + ölçüm sonucu.
