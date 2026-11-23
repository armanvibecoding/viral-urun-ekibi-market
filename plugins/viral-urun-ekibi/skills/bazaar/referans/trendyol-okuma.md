# Trendyol sayfa okuma

Ne zaman okunur: tarama adımında, `scout` brief'i yazılırken.

1. Arama: `https://www.trendyol.com/sr?q=<terim>`, sıralama "çok değerlendirilenler". Her arama öncesi `kota kaydet arama <terim>`.
2. Sonuç kartlarından en çok değerlendirilen ilk 10 ürün seçilir; her ürün sayfası öncesi `tekrar <link>` ve `kota kaydet urun <link>`.
3. Ürün sayfasından okunur (yalnız görünen değer; okunamayan alan boş bırakılır, tahmin yazılmaz):
   ad · link · güncel fiyat (alış_tl) · değerlendirme sayısı · puan · "diğer satıcılar" sayısı · satıcı adı · ana görsele bakıldı mı.
4. Sayıları olduğu gibi yaz ("10.314" → 10314, "4,1" → 4,1); betik ondalık virgülü ve nokta binliği okur.
5. Mekanizma (viral-dna.md) ve aile (örn. `tirnak-makasi`) alanlarını doldur; aile, viral veritabanı eşlemesinde kullanılır.
6. Her aday `okuma_tarihi` ile yazılır. Aynı link ikinci kez eklenmez.
7. Engel ya da CAPTCHA görünürse: dur, `kota kilit CAPTCHA`, okunanı kaydet.
