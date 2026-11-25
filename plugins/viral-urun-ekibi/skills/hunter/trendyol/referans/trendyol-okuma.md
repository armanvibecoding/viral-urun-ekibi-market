# Trendyol sayfa okuma

Ne zaman okunur: tarama adımında, `scout` brief'i yazılırken.

1. Arama: `https://www.trendyol.com/sr?q=<terim>`, sıralama "çok değerlendirilenler". Her arama öncesi `kota kaydet arama <terim>`.
2. Sonuç kartlarından en çok değerlendirilen ilk 10 ürün seçilir. "Çok değerlendirilenler" sıralamasında bile en üstte **değerlendirme sayısı görünmeyen kartlar** (öne çıkarılmış/kuponlu) gelir — bunlar sıralamaya ait değildir, atlanır (saha 2026-11-24: "duruş düzeltici" aramasında ilk 4 kart). Değerlendirme sayısı kartta `4.4 (19465)` biçiminde okunur; her ürün sayfası öncesi `tekrar <link>` ve `kota kaydet urun <link>`.
3. Ürün sayfasından okunur (yalnız görünen değer; okunamayan alan boş bırakılır, tahmin yazılmaz):
   ad · link · **Trendyol güncel satış fiyatı** · değerlendirme sayısı · puan · "diğer satıcılar" sayısı · satıcı adı · ana görsele bakıldı mı.
   **Fiyat kaynakları ayrıdır:** Trendyol'da okunan fiyat bizim **hedef satış/rakip fiyatımızdır**: `rakip_tl` (okunan fiyat) ve `onerilen_satis_tl` (hedef satış); ASLA `alis_tl` değil. `alis_tl` tedarikçiden gelir (AliExpress/1688'de AYNI ürün, `alis_kaynak` sütununa link); `alis_kaynak` AYNI ürünün tedarikçi SAYFASIDIR (`aliexpress.com/item/<no>`, `1688.com/offer/<no>`); arama sonucu ya da benzer ürünün fiyatı `alis_tl`'ye yazılmaz (yazılırsa `denetle` kat'ı ölçmez, not düşer). Bulunamazsa `alis_tl` boş kalır, notu "tedarikçi bulunamadı" olur ve kat ölçütü `dogrulanamadi` = SAT kartında not (engel değil).
4. Sayıları olduğu gibi yaz ("10.314" → 10314, "4,1" → 4,1); betik ondalık virgülü ve nokta binliği okur.
5. Mekanizma (viral-dna.md) ve aile (örn. `tirnak-makasi`) alanlarını doldur; aile, viral veritabanı eşlemesinde kullanılır.
6. Her aday `okuma_tarihi` ile yazılır. Aynı link ikinci kez eklenmez.
7. Engel ya da CAPTCHA görünürse: dur, `kota kilit CAPTCHA`, okunanı kaydet.
