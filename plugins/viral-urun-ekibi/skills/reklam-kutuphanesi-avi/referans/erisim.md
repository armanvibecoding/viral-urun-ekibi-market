# Erişim, tarayıcı ve güvenli sınırlar

## 1. Kim tarar
Tarama yalnız **lider** oturumunda, Claude in Chrome ile yapılır. Alt ajana tarayıcı işi verilmez (alt ajanlarda
Chrome erişimi ölçülerek yok bulundu). Alt ajana yalnız kayıt dosyaları (TSV) üzerinden sentez/çürütme verilir.

## 2. Tarayıcı seçimi
1. `list_connected_browsers` → birden çok tarayıcı bağlıysa **kullanıcının asıl bilgisayarındaki** Chrome seçilir
   (varsayılan yanlış olanı seçebilir; ilk iş budur).
2. Meta Reklam Kütüphanesi **girişsiz** açılır (hesap gerekmez). Mümkünse **ayrı Chrome profili, Facebook girişi yok**:
   önceki turda sessiz kısıtın hesaba bağlı olabileceği gözlendi. Girişsiz çalıştığı henüz **ölçülmedi** → ilk turda
   kontrol sorgusunun dolu dönüp dönmediği `aramalar.tsv`'ye yazılır; bu, ölçümün kendisidir.
3. Gizli pencere, IP/VPN değiştirme, bot tespitini aşma, CAPTCHA çözme **yok**. Doğrulama/giriş/"şüpheli etkinlik"
   ekranı çıkarsa dur, okunan kadarı kaydedilir, kullanıcıya bildirilir.

## 3. Meta Reklam Kütüphanesi kuralları
| Kural | Değer | Neden |
|---|---|---|
| Günlük sorgu | ≤30 (kontrol + alan sorguları dahil) | ~45 ardışık aramadan sonra sessiz kısıt ölçüldü |
| Sorgu arası | ≥15 sn | aynı ölçüm |
| Kaydırma | 4–7 sn aralık, oturum ≤1 saat | uzun oturum kısıta katkı yaptı |
| Kontrol sorgusu | oturum başında + her 0 kartlık sonuçtan sonra | kısıt hata vermez, "Hiçbir reklam eşleşmiyor" der |
| Kısıt görülünce | o gün Meta'ya dokunulmaz; sonuç "doğrulanamadı" | kısıt 30+ dk sürdü, tüm aramaları kapsadı |
| Sıralama | genç mağaza: "en yeniler" (`relevancy_monthly_grouped`, ~4× verimli) · olgun kazanan: toplam gösterim | ilk TR turu |

Kotayı betik tutar: her sorgu açılmadan **önce** `nis_kelime.py kaydet`; kayıtsız taranan ham dosyayı `meta_kayit.py` reddeder.

### URL kalıbı (`nis_kelime.py gun` üretir)
```
https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=<ÜLKE>&q="<ifade>"
  &search_type=keyword_exact_phrase&media_type=video&sort_data[mode]=<total_impressions|relevancy_monthly_grouped>&sort_data[direction]=desc
```
Mağaza ölçeği (alan sorgusu): `q=<alan adı>&search_type=keyword_unordered&media_type=all` → ekrandaki "~N sonuç" = aktif reklam
(jenerik kelimeli alan adlarında şişer; not düşülür).

### Toplama ve okuma (javascript_tool)
- `javascript_tool` çıktısı ~1.000 karakterde kesilir ve ~45 sn'de zaman aşar → veri `localStorage`'a yazılır, ayrı okunur.
- `scripts/meta_topla.js` dosyasını Read ile oku, metnin **üstüne** ayar satırını ekleyip tek çağrıda çalıştır:
  `window.__REKLAMAVI_AYAR = {nis: 'evcil', aile: 'U'};` (S sorgusunda `nis: '-'`, `aile: 'S'`).
- Döngü arka planda sürer; durum: `localStorage.getItem('__reklamavi_durum')` (`bitti: true` olana kadar 1–2 dk arayla bak).
  Sekme arka plandaysa zamanlayıcı yavaşlar (~30 sn/tur) — toplama sekmesi önde kalsın.
- Bitince **aynı alan adında 2. sekme** aç (ör. `facebook.com/ads/library/`), `meta_aktar.js`'i çalıştır
  (`window.__REKLAMAVI_PARCA = 1;` üstte) → `get_page_text` → metni olduğu gibi `is/meta/ham/<tarih>-<ülke>-<sorgu>-1.txt`'ye yaz.
  Başlıktaki `parca=1/N` N>1 ise 2..N için tekrarla. Alternatif: `window.__REKLAMAVI_INDIR = true;` tek dosyayı İndirilenler'e
  kaydeder (izin isterse kullanıcıya sorulur); dosya `is/meta/ham/`'a taşınır.
- Kopyalama hatası sessiz geçmez: başlıktaki `kart=N` ile satır sayısı ya da parça listesi tutmazsa `meta_kayit.py` çıkış 1 verir.
- İlk turda **seçici sınaması**: kayıttan sonra ilk 5 kartın Kütüphane Kodu, sayfa adı, tarih ve kopya sayısı ekrandakiyle elle
  karşılaştırılır. Tutmazsa `meta_topla.js` seçicileri düzeltilmeden devam edilmez (meta_kayit, kartların yarısından çoğunda
  tarih okunamazsa zaten uyarır).

## 4. Shopify mağaza okuma
- `/products.json?limit=250` resmi belgede yok, kapatılabilir; resmi uç `/products/<handle>.js`. Yalnız kısa listedeki mağazalar,
  sırayla, 8–15 sn arayla (`magaza_oku.js`). Herhangi bir Shopify mağaza sekmesinden diğer mağazalara CORS açık (ölçüldü);
  curl/düz istek 429 alır — betikten değil tarayıcıdan okunur.
- En eski `created_at` ≈ katalog yaşı; ürün silinip yeniden eklendiyse genç görünür. **Mağaza yaşı ≠ ürün yaşı.**
- Şifre sayfası / 401 / 404 = KAPALI. Eski alan adının yeni markaya yönlenmesi ürün değişimi sinyalidir (not düşülür).

## 5. Instagram / TikTok (bu skill'in ana işi değil)
Yalnız kullanıcının **ayrı Chrome profilindeki kendi hesabıyla** ve yalnız **bak / kaydır / oku**: beğeni, takip, yorum, kaydetme,
mesaj yok. Tek sekme, öğe başına ≥5–10 sn, oturum ≤1 saat, günde ≤2 oturum, toplu kazıma yok. Platform şartları izinsiz otomatik
toplamayı yasaklar; giriş yapılmış hesapla otomasyon hesabı riske sokar — hangi hızın "işlem engeli"ne yol açtığı **doğrulanmadı**.
Meta kütüphanesinde ölçeklenen reklamın kreatifi Ad Library oynatıcısında izlenir; Instagram'a gitmek gerekmez.
