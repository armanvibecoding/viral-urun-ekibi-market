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

## 6. Shopify reklam toplayıcı — iki veri yolu

### 6a. Meta resmi MCP aracı (`mcp__meta-official__ads_library_search`)
- **Kim çağırır:** lider (ana ajan). Betik çağırmaz; betik yalnız sırayı, sayacı ve kilidi tutar (`kuyruk.py al`).
- **Ne için:** hedefli niş araştırması — niş × pazar başına 1 sorgu: tahmini toplam (`estimated_total_count`) + ≤50 örnek.
  Aracın açıklaması "toplu veri çıkarma/kazıma için kullanma" der; bu yüzden tavan **150 çağrı/gün**, aralar **≥20 sn**.
- **Parametre:** `countries=[<pazar>]`, `search_terms`, `ad_active_status=ACTIVE`, `ad_type=ALL`, `limit=50` (en çok 50).
  Gerekirse `page_ids=[..]` ile tek sayfanın reklamları (aynı sayaçtan düşer).
- **Dönen alanlar:** id · page_id · page_name · ad_creative_link_title · ad_creation_time · ad_delivery_start_time (epoch sn) ·
  ad_snapshot_url · currency; üstte estimated_total_count. Yanıt `{"results": "<JSON metni>"}` sarmalıyla gelir — dosyaya
  **olduğu gibi** yazılır, `toplanan_isle.py mcp` açar.
- **Ölçülen sınırlar (2026-11-18, 3 çağrı):**
  - Hedef link / alan adı, reklam gövdesi, kopya sayısı **dönmüyor** → Shopify kontrolü için alan adı Chrome'dan gelir (§6c).
  - Sıralama en yeni reklam önde; gösterim sıralaması yok.
  - Çok kelimeli jenerik terim (ABD "dog bed", tırnaklı da) ~99 bin sonuç ve ilk 50'si alakasız (kitap/roman reklamı) döndü;
    ayırt edici tek kelime (DE "Katzenbaum") 7 sonuç, hepsi evcil hayvan. → MCP'de **ayırt edici terim** kullan; jenerik
    terimin sayımı niş hacmi diye okunmaz. Bu, terim listesinin MCP için ayrıca ayıklanması gerektiğini gösterir (öneri).
  - Erişim reklam hesabı ister (hesabı olmayan çağıran hata alır).
- **Hata/engel:** yanıtta `error`, "rate limit", "too many", "try again later" vb. → çıkış 3, o gün mcp yolu kilitli.

### 6b. Chrome: Reklam Kütüphanesi + TrendTrack Chrome eklentisi
- Toplama §3'teki yöntemle (yavaş kaydırma, `localStorage`, `get_page_text`); **≤30 sorgu/gün** kuralı korunur. Kota bekçisi
  tek: `nis_kelime.py kaydet` (`kuyruk.py al --yol chrome` onu çağırır). Bu tavanın yükseltilmesi kurucuya **öneri** olarak
  sunulur; ölçülmeden değiştirilmez (~45 ardışık aramada sessiz kısıt ölçülmüştü).
- **TrendTrack:** yalnız Chrome **eklentisi** kullanılır (kurucu kararı 2026-11-18). TrendTrack web sitesi ve ücretli kısmı
  kullanılmaz. Eklentinin kartlara koyduğu Shopify işareti/filtresi varsa **ipucudur**: "Only Shopify" filtresinin eksik
  bıraktığı daha önce ölçüldü → her alan ayrıca `shopify_kontrol.py` ile doğrulanır. Eklentinin gösterdiği satış/gelir tahmini
  kayda sayı olarak girmez (ölçüm değil).
- Döküm (`#REKLAMAVI v1`) hedef linki taşır → alan adı buradan gelir; `toplanan_isle.py chrome` işler.

### 6c. Alan adı çözme (MCP sayfaları için)
`shopify_kontrol.py bekleyen` en çok reklamı olan, alan adı bilinmeyen sayfaları ve birer `ad_snapshot_url` listeler.
Lider snapshot'ı Chrome'da açar, reklamın hedef linkini **okur** (tıklamaz, satın almaz), `alan-ekle` ile yazar.
Günde ≤60 snapshot, aralar ≥15 sn; doğrulama/giriş ekranı çıkarsa dur (`kuyruk.py engel --yol chrome`).

### 6d. Shopify kontrolü
Alan adı başına **tek** GET (`/products.json?limit=250`) — Shopify olup olmadığı ve en eski `created_at` (mağaza yaşı) aynı
istekten. Önbellek: `tamam` alana bir daha istek atılmaz. 429/5xx/zaman aşımı → 24 sa ertele (Retry-After daha uzunsa o);
bir koşuda 3× 429 → koşu durur. 401/403 → `hata`, yeniden denenmez. Dürüst User-Agent; tarayıcı taklidi yok.
products.json kapalı Shopify mağazası başlık/gövde iziyle (x-shopid, cdn.shopify.com) Shopify sayılır, yaşı `bilinmiyor` kalır.
§4'teki not geçerli: düz istek bazı mağazalarda 429 alır → o mağaza ertelenir; gerekirse kısa listede tarayıcıdan
`magaza_oku.js` ile okunur.
