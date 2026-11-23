# Tarif 06 — Trendyol ve AliExpress avı · betiksiz ChatGPT sürümü

## Amaç
TR'de satılabilir ürün bulmak: Trendyol'da kanıtlanmış, henüz viral olmamış, AliExpress'ten temin edilebilir ürünler. Çıktı: **5 niş × 5 ürün** tablosu + tek gerekçeli öneri. Sayfaları **kullanıcı açar** (Trendyol düz isteği engeller; tarayıcı otomasyonu burada yok) ve ürün sayfası metnini/ekran görüntüsünü yükler.

## Adımlar
0. **Oran turu (bir kez, oran tablosu boşsa):** komisyon, ödeme (ör. %2,49 + 0,25 TL), kargo, KDV oranlarını web aramasıyla **kaynak URL'siyle** yaz. Kaynak bulunamayan oran BOŞ kalır; oran uydurma; boş oranla marj hesaplanamaz → ürün en çok "SAT (koşullu)".
1. 5 niş seç (viral mekanizmalardan: ürün adı değil mekanizma); niş başına Trendyol arama terimi yaz; kullanıcı sayfaları açıp yükler.
2. Her aday için **ürün SAYFASINDAN** oku (arama kartı yetmez): yorum sayısı, puan, fiyat, satıcı, varyant. Görmediğini yazma: `doğrulanamadı`.
3. **Estetik filtre:** görünüşü ucuz/estetiği zayıf ürünü ele (ör. sıradan telefon standı tipi). Soru: "Videosu ilk 2 saniyede dikkat çeker mi, fotoğrafı pahalı durur mu?" Hayırsa ELE + gerekçe.
4. AliExpress tedarik (kullanıcı sayfayı yükler): **"This seller: N | Total sales: M" ayrı yazılır** (satıcının satışı ≠ ürünün toplam satışı); sayfanın altındaki öneri/benzer ürün sayılarını ALMA; 1-1 aynı ürün görselle doğrulanır.
5. Marj: net gelir = satış / (1 + KDV); maliyet = alış + kargo + ödeme + iade; çarpan = net gelir / maliyet. Oran yoksa hesaplama, "marj hesaplanamadı" yaz.
6. Viral kontrol (Instagram/TikTok/Meta kütüphanesi, kullanıcı bakar): doğrulanamazsa `doğrulanamadı`.
7. **Sınama 3/3** (talep var · tedarik/marj tutuyor · viral değil/çürütülemedi); 3/3 geçmeyen SAT olamaz.
8. Etiketler: **SAT** · **SAT (koşullu)** (marj ya da viral doğrulanamadı, diğer ölçütler güçlü; neden sütunu hangisi eksik) · **İZLE** · **ELE**.
9. Çıktı: 5 × 5 tablo (ürün · link · yorum · puan · alış · satış · çarpan · karar · neden) + tek öneri: "Önerim: X — çünkü …. İtirazın yoksa onunla devam ediyorum."

**Pazar:** TR; TR verisi zayıf, eşikler `deneme`/`varsayım`, ilk 20 üründen sonra kalibre. Eşikler (başlangıç): yorum 150–3000 SAT adayı, puan ≥ 4,2, satıcı ≤ 5, alış 100–600 TL, satış/alış ≥ 2,2 ve satış ≥ 399 TL.

## Kalite çıtası
5 niş × 5 ürün (eksik niş belirtilir) · her satırda ürün sayfası linki · sayılar ürün sayfasından · AliExpress satıcı/toplam ayrı · öneri bölümü sayısı yok · her kararda gerekçe · uydurma oran/sayı yok.

## Kendi çıktını şu 10 maddeyle denetle
1. 5 niş × 5 ürün var (eksik varsa söylendi). 2. Her satırda ürün sayfası linki. 3. Sayılar sayfadan, arama kartından değil. 4. AliExpress "This seller" ve "Total sales" ayrı sütunda. 5. Öneri bölümü sayısı alınmadı. 6. Estetik filtre uygulandı, elenenlerin gerekçesi yazılı. 7. Oran kaynaklı ya da boş; uydurma yok. 8. SAT'ların hepsi 3/3. 9. SAT (koşullu)'larda eksik koşul yazılı. 10. Tek gerekçeli öneri + "itirazın yoksa devam" cümlesi var.

## Bitti tanımı
Tablo (indirilebilir .xlsx/.csv ya da sohbette) + tek öneri + 10 maddelik denetim. ChatGPT'de uygulanabilirlik: sayfaları kullanıcı yüklerse tam uygulanır; yüklemezse yalnız web araması bulgularıyla "doğrulanamadı" işaretli taslak çıkar.
