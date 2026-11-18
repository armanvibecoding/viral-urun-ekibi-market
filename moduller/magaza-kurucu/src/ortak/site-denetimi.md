# Site denetimi (0.4.0): hız, arama/feed, erişilebilirlik, satın alma kutusu

Adım 8 QA'nın ikinci yarısı. Her madde ölçülür ya da gözle bakılır; sonuç ✅/❌ + tek düzeltme satırı. Kaynaklar repo `research/kutuphane-v2/KANIT.md` (madde no parantezde) ve 1.000+ başarılı Shopify markasının ölçüldüğü `research/kutuphane-v2/ANALIZ.md`. Tarayıcın yoksa listeyi kullanıcıya kontrol listesi olarak ver. Tema koduna dokunulmaz: düzeltme ayar, görsel dosyası ya da metindir.

## 1. Tipografi (görsel = site)
- Sitenin başlık ailesi (`type_heading_font`) DEVAM KARTI "Tipografi" satırındaki görsel başlık ailesiyle aynı (varsayılan `barlow_condensed_n6`). Ürün sayfasının ilk ekranında galeri görseli ile H1 yan yana bakıldığında iki ayrı aile görünüyorsa ❌.
- Yüklenen yazı ailesi ≤ 2 (başlık + gövde). "3 font kuralı" kanıtı yok; sınır performanstan gelir (6.5).

## 2. Hız (mobil, ana sayfa ve ürün sayfası)
- İlk ekrandaki en büyük görsel (LCP adayı) `loading="lazy"` DEĞİL; tema `image_url` ile boyutlandırıyor. Hero görseli ≤ 1920 px masaüstü, ≤ 1080 px mobil yüklenir (3.6).
- Hero'da otomatik oynayan video yok (varsa ⚠️: mobilde LCP'yi büyütür).
- Eklenen her uygulama (yorum, pop-up, sohbet) bir satırla raporlanır; amacı olmayan uygulama önerilmez (3.9).
- Bayt bütçesi (420 başarılı Shopify markasından 221'inin mobil laboratuvar ölçümü; en hızlı %20'nin medyanı): ana sayfa toplam ≤ 1,0 MB, JavaScript ≤ 0,45 MB, görsel ≤ 0,25 MB, farklı alan adı ≤ 10. En yavaş %20: 2,6 MB, 18 alan adı. LCP'yi en çok toplam bayt belirliyor (Spearman 0,71); sunucu yanıt süresi belirlemiyor (0,09). Her yeni uygulama bu bütçeden düşer.
- Hedef: Core Web Vitals "iyi" eşikleri LCP ≤ 2,5 sn, CLS ≤ 0,1, INP ≤ 200 ms (75. yüzdelik, alan verisi; 3.1). Yeni mağazada alan verisi yoktur: PageSpeed Insights laboratuvar sonucunu "laboratuvar" diye yaz.

## 3. Arama, feed ve yapay zekâ araması
- **Galerinin 1. görseli (G0) yazısız**, tek ürün, ürün karenin %75–90'ı, ≥ 1500 px (Google Merchant Center `image_link`; 4.3). Yazılı afiş 2. sıradadır.
- Ürün başlığı: ürün adı + ayırt edici özellik + varyant; BÜYÜK HARF değil. Meta açıklama somut (malzeme, ölçü, kullanım).
- Galerideki her görselin alt metni dolu; görselin içindeki yazı alt metinde de geçer (4.2, 5.2).
- Ürün yapılandırılmış verisi (tema üretir): fiyat, para birimi, stok, marka; `aggregateRating` yalnız gerçek yorum varsa (4.1).
- Yapay zekâ araması için ek şart yok (Google; 4.4). `llms.txt` resmi standart değil: istenirse eklenir, "görünürlük artırır" denmez (4.5). robots.txt'de alışveriş arama botlarını (OAI-SearchBot, Googlebot) kapatma.

## 4. Erişilebilirlik (WCAG 2.2 AA)
- Metin/zemin ≥ 4,5:1; büyük başlık ≥ 3:1; buton metni/buton ≥ 4,5:1 (5.1). Marka adımındaki oranlar sayfada da tutuyor mu, ölç.
- Dokunulan öğeler ≥ 24×24 px (5.3).
- Görseldeki bilgi sayfada metin olarak da var: banner yazısı H1/alt metinde, kart başlıkları açıklamada (5.2).
- Bilgi notu: AB'ye satışta Avrupa Erişilebilirlik Yasası 28.06.2025'ten beri e-ticarete uygulanıyor (mikro işletme istisnası var; 5.5). Karar kullanıcının.

## 5. Satın alma kutusu ve ürün sayfası
- Sepete ekle butonu mobilde (390 × 844) ilk ekranda ya da yapışkan çubukta görünüyor; galeri mobilde ekran yüksekliğinin ≤ %60'ı, fiyat ilk ekranda. Ölçüm: 390 px ekran görüntüsü (kör deneme 2026-11-18: üç eleştirmen de "mobilde fiyat ve buton ilk ekranda yok" diye puan kırdı).
- Hızlı ödeme düğmesi (mor "Buy with Shop") ana CTA ile renk çatışması yaratıyorsa ⚠️ olarak yaz; kapatmak kullanıcının kararı.
- Toplam maliyet açık: kargo ücreti/eşiği ve iade koşulu butonun hemen altında tek satır (sepet terkinin 1 numaralı nedeni ek maliyet, %40; 7.6).
- Galeri: masaüstünde küçük resim şeridi görünür, mobilde kaydırma çalışıyor; 10'dan az görselde hepsi görünür (1.5, 1.6).
- Bilgi blokları dikey açılır bölümler; yatay sekme yok (1.9).
- Yorum yoksa yıldız, "binlerce mutlu müşteri", basın logosu UYDURULMAZ. Yorum toplanınca: yorum sayısı satın almayı en çok ilk 5 yorumda artırıyor (7.1); puan sayısı ortalamadan önemli (7.3).
- Ölçek: alıcı boyutu görselden anlamaya çalışıyor (1.1): galeride ölçü kartı (G5 ya da ölçek kartı) var.

## Rapor
Tek tablo: Bölüm · Madde · Sonuç (✅/❌/⚠️) · Ölçülen değer · Düzeltme. Sonra yalnız kullanıcının yapması gerekenler.
