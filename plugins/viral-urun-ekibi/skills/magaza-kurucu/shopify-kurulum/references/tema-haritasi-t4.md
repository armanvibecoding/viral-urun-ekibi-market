# TEKNİK EK T4–T4.4: şablon haritası

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 273–363. 0.3.0: hukuki tek satır bilgi notuna çevrildi (repo `docs/ESKIDI.md`).

İçindekiler:
- T4 Şablon haritası: yol yazımı, yazılabilir dosyalar, yazma kuralı
- T4.0 Bölüm haritası (ana sayfa 12 bölüm; ürün sayfası niş başına)
- T4.1 Ana sayfa (`templates/index.json`)
- T4.2 Ürün sayfası satın alma kutusu
- T4.3 Ürün sayfası alt bölümleri
- T4.4 Sayfa şablonları (Hakkımızda, İletişim, S.S.S., 404, koleksiyon, sepet, footer)

---

T4. Şablon haritası (`themeFilesUpsert`)
Yol yazımı: `bölüm/blok/altblok.ayar` = JSON'da `sections.<bölüm>.blocks.<blok>.blocks.<altblok>.settings.<ayar>`; `bölüm.ayar` = `sections.<bölüm>.settings.<ayar>`. `N` = 1, 2, 3…
Kod dosyaları DOKUNULMAZ: `sections/*.liquid`, `blocks/`, `snippets/`, `assets/`, `layout/`, `locales/` ve `config/settings_schema.json` okunabilir ama ASLA yazılmaz; `themeFilesDelete` ASLA kullanılmaz. Yazılabilecek dosyalar YALNIZ şunlardır: `templates/*.json`, `sections/footer-group.json`, `sections/mt-cart-drawer-group.json`, `config/settings_data.json`. Bir bölüm ya da blok "gereksiz", "boş" ya da "bozuk" görünse bile silinmez, yerine yenisi yazılmaz. Gizlemek gerekiyorsa yalnız `"disabled": true` yapılır.
Yazma kuralı: şablonu sıfırdan yazmak, bölüm ya da blok silmek ve yeni bölüm eklemek YASAK. Bölüm sayıları T4.0'dadır (ana sayfa 12, ürün sayfası nişe göre 12–15); hepsi kalır, verisi olmayan boş bırakılır. Her şablon T4.5 tarifiyle yazılır: önce `themeFilesCopy` ile yedek alınır, dosya okunur ve kod aracında (Python) ayrıştırılır, YALNIZ tablodaki ayarlar ve bölümün `disabled` alanı değişir, bölüm/blok haritası kontrol edilir, dosya GİRİNTİSİZ (tek satır) yazılır, tekrar okunup yeniden kontrol edilir. Girintisiz yazım dosyayı yarıya indirir; Shopify kabul eder. `order`, `block_order`, `type`, `name`, anahtarlar ve tasarım ayarları (`mt_kalip`, `font*`, `width*`, `padding-*`, `gap`, `color*`, `background*`, `border*`, `*_radius`, `*_alignment*`, `custom_*`) değişmez. Tek istisna: S.S.S. `faq` bölümüne yeni `question` / `category` bloğu eklenebilir (`block_order` sonuna, adı `Soru · <soru>`).
Satın alma kutusu: bütün niş şablonlarında `volume_tiers` açık gelir (adet indirimi, T6), `gift` kapalı gelir ve kapalı kalır. `sub` bloğu yalnız abonelik varsa açılır.
Metin (`.text`) HTML'dir: başlık `<h2>…</h2>` / `<h3>…</h3>`, kart başlığı `<p><strong>…</strong></p>`, paragraf `<p>…</p>`. Boş = `""` (boş metin vitrinde hiçbir şey basmaz). `{{ closest.product.title }}` gibi dinamik kaynaklara dokunma. Değer tipleri: ürün → handle; sayfa → handle; link → `shopify://pages/<handle>` / `shopify://products/<handle>` / `/policies/<tip>`; görsel → `shopify://shop_images/<dosya>`; ikon → bloğun seçeneklerinden biri. İletişim linki sabit yazılmaz (temada bloktan gelir).
Temiz paketin `index.json`'u boş başlangıçtır; ana sayfa için niş kopyası gerekmez. Ürün sayfası şablonu ürünün `templateSuffix`'inden gelir (`product.nis-<niş>.json`); yazacağın dosya odur.

T4.0 Bölüm haritası (temiz paketteki hâli; sayılar alt bloklar dahil toplam blok sayısıdır; (K) = kapalı gelir)
Bir bölümü "üretmek" burada şu demek: bölüm ve blokları zaten şablonda var. Sen yalnız T4.1–T4.4 tablolarındaki ayarların değerini yazarsın, gerekirse `disabled`'ı değiştirirsin. Yeni bölüm, yeni blok ya da yeni dosya oluşturmazsın; blok silmezsin, `order` ve `block_order` sırasını değiştirmezsin. Yazmadan önce ve yazdıktan sonra bölüm adları, tipleri ve blok sayıları bu haritayla aynı olmalı.
Ana sayfa `templates/index.json` (12 bölüm, bütün nişlerde aynı):
| Sıra | Bölüm | Tip | Blok | İşi |
| 1 | `e-hero-a` | `hero` | 0 | Banner görseli (masaüstü + mobil) |
| 2 | `e-hero-b` | `section` | 5 | H1 vaat, puan satırı, satın al butonu |
| 3 | `e-serit` | `section` | 20 | 4'lü güven şeridi (kargo, iade, ödeme, destek) |
| 4 | `e-mini` | `featured-product-information` | 13 | Ana sayfada satın alma kutusu |
| 5 | `n-pc` | `section` | 12 | Sorun → çözüm |
| 6 | `e-fayda3` | `section` | 16 | Görselli 3 fayda kartı |
| 7 | `e-spec` | `media-with-content` | 5 | Etiket / teknik bilgiler |
| 8 | `n-ugc` | `media-with-content` | 4 | Müşteri videosu (veri yoksa gizli) |
| 9 | `e-yorum` | `mt-reviews` | 0 | Gerçek yorumlar (yoksa gizli) |
| 10 | `e-kars` | `section` | 7 | Karşılaştırma tablosu (veri yoksa gizli) |
| 11 | `e-hikaye` | `media-with-content` | 5 | Marka hikâyesi |
| 12 | `e-garanti` | `section` | 5 | Son çağrı ve iade güvencesi |
Ürün sayfası `templates/product.nis-<niş>.json` (sıra aynen böyle; parantezde tip ve blok sayısı):
- G güzellik (13): `main` (product-information, 41) · `e-serit` (section, 20) · `n-neden` (section, 20, K) · `e-faydayan` (media-with-content, 19) · `n-os` (section, 2, K) · `n-sonuc` (section, 15) · `n-icerik` (section, 19) · `e-zaman` (section, 20) · `e-kars` (section, 7, K) · `e-sss` (section, 10) · `e-yorum` (mt-reviews, 0) · `e-oneri` (product-recommendations, 7) · `n-abone` (section, 2, K)
- S sağlık (15): `main` (product-information, 43) · `e-serit` (section, 20) · `n-pc` (section, 3) · `n-neden` (section, 20, K) · `e-faydayan` (media-with-content, 19) · `n-otorite` (section, 15) · `n-sonuc` (section, 15) · `n-icermez` (section, 15, K) · `n-uzman` (media-with-content, 4, K) · `e-zaman` (section, 20) · `e-kars` (section, 7, K) · `e-sss` (section, 10) · `e-yorum` (mt-reviews, 0) · `e-oneri` (product-recommendations, 7) · `n-abone` (section, 2, K)
- D gadget (13): `main` (product-information, 41) · `e-serit` (section, 20) · `n-nasil` (section, 15) · `n-neden` (section, 20, K) · `e-faydayan` (media-with-content, 19) · `e-spec` (media-with-content, 5) · `e-zaman` (section, 20) · `e-kars` (section, 7, K) · `n-ugc` (media-with-content, 4, K) · `e-sss` (section, 10) · `e-yorum` (mt-reviews, 0) · `e-oneri` (product-recommendations, 7) · `n-abone` (section, 2, K)
- E ev (13): `main` (product-information, 41) · `e-serit` (section, 20) · `n-neden` (section, 20, K) · `e-faydayan` (media-with-content, 19) · `e-spec` (media-with-content, 5) · `n-bakim` (section, 15) · `e-zaman` (section, 20) · `e-kars` (section, 7, K) · `n-otorite` (section, 3, K) · `e-sss` (section, 10) · `e-yorum` (mt-reviews, 0) · `e-oneri` (product-recommendations, 7) · `n-abone` (section, 2, K)
- M moda (12): `main` (product-information, 42) · `e-serit` (section, 20) · `n-neden` (section, 20, K) · `e-faydayan` (media-with-content, 19) · `e-hikaye` (media-with-content, 4) · `e-spec` (media-with-content, 5) · `e-zaman` (section, 20) · `n-otorite` (section, 3, K) · `e-yorum` (mt-reviews, 0) · `e-sss` (section, 10) · `e-oneri` (product-recommendations, 7) · `n-abone` (section, 2, K)
Okuduğun şablon bu haritadan farklıysa (bölüm eksik, tip farklı, blok sayısı düşük) o dosyaya YAZMA: dur ve "Şablon bozuk; temiz Ana Tema zip'ini yeniden yükleyin" de.

T4.1 Ana sayfa (`templates/index.json`). Sıra: e-hero-a → e-hero-b → e-serit → e-mini → n-pc → e-fayda3 → e-spec → n-ugc → e-yorum → e-kars → e-hikaye → e-garanti.
| Bölüm | Doldur | Boşken |
| `e-hero-a` Banner | `e-hero-a.image_1`, `.image_1_mobile`, `.link` = `shopify://products/<handle>` | Görsel yoksa basılmaz |
| `e-hero-b` Vitrin şeridi | `e-hero-b/sol/baslik.text` = `<h1>…</h1>` (sayfanın tek H1'i); `e-hero-b/cta.product`, `e-hero-b/cta.label` | H1 boşsa ürün adı basılır |
| `e-serit` Güven şeridi | `e-serit/cN/i.icon`, `e-serit/cN/m/b.text` (`<p><strong>`), `e-serit/cN/m/s.text` (alt metin ya da politika linki; yalnız c1–c3), `e-serit/c4/m/s.label` (c4 iletişim linki; `text` yok). Hücreler: c1 kargo, c2 iade, c3 ödeme, c4 destek | Politika yoksa link gizli |
| `e-mini` Mini satın alma | `e-mini.product` = ürün handle'ı (ZORUNLU); `e-mini/product-details/delivery.transit_min`, `.transit_max`, `.cutoff_hour` = ürün sayfasıyla aynı | Ürün yoksa basılmaz |
| `n-pc` Problem → çözüm | `n-pc/bas/h.text` (`<h2>`), `n-pc/bas/p.text`; a1 = sorun, a2 = çözüm: `n-pc/adimlar/aN/s.text` (üst etiket), `/h.text` (`<h3>`), `/p.text` | Gizli |
| `e-fayda3` 3 fayda kartı | `e-fayda3/bas/h.text`, `e-fayda3/bas/l.text`; `e-fayda3/kartlar/fN/g.image` (dikey görsel, isteğe bağlı), `/h.text` (`<h3>`), `/p.text`. Üç kartın üçü de başlık + metinle dolmalı | Gizli |
| `e-spec` Etiket bilgileri | `e-spec/content/h.text`, `/p.text`, `e-spec/content/liste.rows` (her satır "Ad: değer"); `e-spec/media.image` isteğe bağlı | Gizli |
| `n-ugc` Müşteri videosu | `n-ugc/media.media_type` = `video`, `n-ugc/media.video`; `n-ugc/content/h.text`, `/p.text`. Yalnız gerçek, izinli video | Gizli |
| `e-yorum` Yorumlar | `e-yorum.product`, `e-yorum.heading`. Veri: `mt_theme.reviews` (yalnız gerçek yorum) | Gizli |
| `e-kars` Karşılaştırma | `e-kars/bas/h.text`, `/p.text`; `e-kars/cmp.col_1..3`, `.caption`, `.footnote`, `.mode` (`own_models` / `method`), `.highlight`; `e-kars/cmp/rN.label`, `.value_N` (`yes`/`no`/`text`), `.text_N` (r1–r3). Rakip marka adı yok | Gizli |
| `e-hikaye` Marka hikâyesi | `e-hikaye/content/h.text`, `/p.text`, `e-hikaye/content/b.label`, `.link` = `shopify://pages/hakkimizda`; `e-hikaye/media.image` isteğe bağlı | Gizli |
| `e-garanti` Son çağrı | `e-garanti/panel/h.text` (`<h2>`), `/p.text`, `e-garanti/panel/cta.product`, `e-garanti/panel/i.icon` | Politika yoksa link gizli |

T4.2 Ürün sayfası satın alma kutusu (`main/product-details/…`). Ürün adı, açıklama, fiyat, varyant, galeri ürün verisinden gelir; `title`, `price`, `variants`, `buy`, `breadcrumb`, `info/about`, `info/shipping`, `payments` bloklarına dokunma.
- `volume_tiers`: adet indirimi kutusu; veri `mt_theme.volume_offer` (T6). `.layout` `list` kalır, `.option_name` `Paket` kalır. `.eyebrow`, `.heading`, `.subheading` boşsa tema pazar dilinde varsayılanı yazar (TR: "Birlikte al, avantajı büyüt" / "Size en uygun paketi seçin" / alt metin kademelerden); yalnız marka sesine göre değiştirmek istersen yaz.
- `return_line` (satın al butonunun altı): `.text` inline HTML, ör. `<strong>14 gün iade</strong> · Kanuni istisnalar saklıdır.`; süre iade sayfasıyla aynı; boş = basılmaz. Başka pazarda o pazarın iade kuralı.
- `delivery`: `.transit_min`, `.transit_max`, `.processing_days`, `.cutoff_hour`. Süre bilinmiyorsa `.transit_max` = `0` yaz (tahmin satırı kapanır; alanı boş bırakma, varsayılan 3 "1–3 iş günü" basar). `.shipping_tr` boş kalır (kargo metni tek kaynak: ayar `mt_consent_shipping_text`). `.shipping_tr_express` yalnız gerçek hızlı kargoda.
- `benefits`: şablona dokunma; veri `mt_theme.benefit_1..3`.
- `payment_info`: `.show_cod` = ayar `mt_cod_enabled`; `.show_installments` gıda ve kozmetikte `false`.
- `sub`: `.enabled` yalnız abonelik uygulaması ve satış planı varsa `true`.
- `addons`: `.product_N`, `.label_N` yalnız gerçek eklenti ürünüyle.
- `info/how/t.text`: "Nasıl kullanılır" (`<p>`).
- `size_guide` (moda): link `/pages/olcu-rehberi` sabit; ölçü tablosu sayfası açılmadıysa `.text` = `""` (atlanamaz; yoksa 404).

T4.3 Ürün sayfası alt bölümleri. Şablon: G güzellik, S sağlık, D gadget, E ev, M moda; (K) = o şablonda kapalı gelir, gerçek veri varsa doldur ve `disabled: false` yap.
| Bölüm | Şablon | Doldur | Boşken |
| `e-serit` Güven şeridi | hepsi | `e-serit/cN/i.icon`, `/t/h.text`, `/t/s.text` (c1–c4). Her hücrenin ikonu içeriğine uygun seçilir (kargo → kamyon, iade → ok, ödeme → kilit/kart, kumaş/malzeme → yaprak ya da etiket, süre → saat) | Boş hücre gizlenmez: gerçek bilgiyle yaz ya da bölümü kapat |
| `n-neden` Neden buradan | hepsi (K) | `n-neden/bas/h.text`, `/p.text`; `n-neden/grid/pN/i.icon`, `/h.text`, `/p.text` (p1–p4) | Boş kart gizli |
| `e-faydayan` Görsel + 3 fayda | hepsi | `e-faydayan/media.image` (galeriden farklı); `e-faydayan/content/h.text`; `e-faydayan/content/liste/mN/i.icon`, `/t/h.text`, `/t/p.text` | Boş madde gizli; hepsi boşsa kapat |
| `e-zaman` Siparişten kapına | hepsi | `e-zaman/bas/h.text`, `/p.text`; `e-zaman/adimlar/aN/s.text`, `/h.text`, `/p.text` (a1–a4). Süreler `delivery` ve iade politikasıyla aynı | Boş adım gizli |
| `e-spec` Özellikler / Kutuda ne var | D E M | Veri `mt_theme.specs`; `e-spec/content/h.text`, `/p.text`; görsel isteğe bağlı. Görsel yok diye kapatma | Veri yoksa gizli |
| `e-kars` Karşılaştırma | G S D E (K) | T4.1'deki gibi (r1–r3). Sağlık beyanı karşılaştırması: Bilgi notu (kullanıcının sorumluluğu) | Etiketsiz satır gizli |
| `e-sss` S.S.S. | hepsi | `e-sss/sol/h.text`; `e-sss/acc/qN.heading`, `e-sss/acc/qN/t.text` (q1–q3) | Gizlenmez: gerçek bilgiyle yaz ya da kapat |
| `e-yorum` Yorumlar | hepsi | Veri `mt_theme.reviews` | Gizli |
| `e-oneri` Öneriler | hepsi | `e-oneri/h/t.text`, `e-oneri/h/l.text`. Tek ürünlü mağazada boş görünüyorsa `disabled: true` | Ürün yoksa gizli |
| `n-abone` Abonelik | hepsi (K) | `n-abone/h.text`, `/p.text`; `sub.enabled` ile birlikte açılır | Kapalı |
| `n-os` Önce/sonra | G (K) | `n-os/h.text`; `n-os/cmp.before_image`, `.after_image` (yalnız gerçek fotoğraf) | Kapalı |
| `n-sonuc` Kullandıkça ne beklenir | G S | `n-sonuc/bas/h.text`; `n-sonuc/adimlar/aN/s.text` (dönem adı, sayı yok), `/h.text`, `/p.text` | Boş adım gizli |
| `n-icerik` İçerik kartları | G | `n-icerik/bas/h.text`; `n-icerik/grid/pN/i.icon`, `/h.text`, `/p.text` (ana içerik, liste, cilt tipi, kullanım). G'de etiket bilgisi buraya ve ürün açıklamasına yazılır; S'de yalnız ürün açıklamasına | Boş kart gizli |
| `n-pc` Problem / ihtiyaç | S | `n-pc/bas/h.text`, `/p.text` | Metin yoksa kapat |
| `n-otorite` Kanıt / Test-sertifika / Basında | S; E M (K) | `n-otorite/bas/h.text` (+ S'de `grid/pN/…`: test adı, tarih, kurum; E M'de `bas/p.text`) | Kaynak yoksa kapat |
| `n-icermez` İçermez şeridi | S (K) | `n-icermez/bas/h.text`; `grid/pN/h.text`, `/p.text`. Yalnız etikette yazan bilgi | Kapalı |
| `n-uzman` Uzman görüşü | S (K) | `n-uzman/media.image`; `n-uzman/content/h.text`, `/p.text`. Gerçek, izinli | Kapalı |
| `n-nasil` Nasıl çalışır | D | `n-nasil/bas/h.text`; `n-nasil/adimlar/aN/s.text`, `/h.text`, `/p.text` | Boş adım gizli |
| `n-ugc` Kullanım videosu | D (K) | T4.1'deki gibi | Kapalı |
| `n-bakim` Kullanım ve bakım | E | `n-bakim/bas/h.text`; `n-bakim/adimlar/aN/s.text`, `/h.text`, `/p.text` | Boş adım gizli |
| `e-hikaye` Malzeme ve üretim | M | `e-hikaye/media.image`; `e-hikaye/content/h.text`, `/p.text` | Metin yoksa kapat |
Teslim süresi ya da kesim saati değişirse (bilinmiyorsa da) şu yerler birlikte yazılır: ürün `delivery`, ana sayfa `e-mini/product-details/delivery`, `e-zaman/adimlar/a2–a4/s.text` ve `a3/p.text`, ürün sayfası `e-serit/c4/t/s.text`, `n-neden/grid/p3/p.text` (açıksa), `e-sss/acc/q1/t.text`, Hakkımızda `degerler/kartlar/d2/p.text`, S.S.S. `q_teslim.answer`. Süre yoksa "ürün sayfasında yazar" diyen cümle kalmaz.

T4.4 Sayfa şablonları
- Hakkımızda (`page.about`): `sayfa-bas` (H1 = sayfa adı; giriş = ayar `mt_brand_description`); `gorsel` geniş görsel 21:9 KAPALI (`gorsel/gorsel.image` verilirse aç); `neden` = sayfa gövdesi (gerçek hikâye; gövdede başlık etiketi yok, başlık yalnız `neden/h.text`'te, ikisi aynı cümle olmaz) + `neden/h.text`; `degerler`: başlık `<h2>Alışveriş bilgileri</h2>` ve 3 kart başlığı sabit, yalnız `degerler/kartlar/dN/p.text` yazılır; `e-garanti/panel/h.text`, `/p.text`, `cta.label`.
- İletişim (`page.contact`): gövde = kısa giriş; `ilet-form/panel/form.mt_subject_options` (virgüllü konu listesi).
- S.S.S. (`page.faq`): sayfa GÖVDESİ yalnız 1 cümlelik giriştir ("Sık sorulan soruların yanıtları aşağıda."); soru-cevaplar gövdeye YAZILMAZ, yalnız `faq` bölümüne. `faq/<kategori>.title`; `faq/<soru>.question`, `.answer` (`<p>`). Mağazaya uymayan hazır sorunun cevabı `""` (cevabı boş soru basılmaz). Taksit sorusu: gıda ve kozmetikte taksit yok. `sss-yardim/panel/metin/h.text`, `/p.text`, `sss-yardim/panel/buton.label`.
- `404`: `main/title.text`, `main/text.text`, `main/actions/buy.label`.
- Koleksiyon (`collection`): `lander.products` (önce ana ürün); `ozellik/cN/i.icon`, `/m/b.text`, `/m/s.text` (c1–c3 = ana sayfa güven şeridi c1–c3).
- Sepet (`cart`): `cart-section/mt_cart_upsell.enabled`, `.products`, `.heading` (yalnız gerçek tamamlayıcı ürün). Çekmece: `sections/mt-cart-drawer-group.json` → `cart_drawer/upsell.products`, `.heading`.
- Footer (`sections/footer-group.json`): `footer/newsletter/newsletter_text.text`, `utilities/social.instagram_url` ve diğer `*_url` (yalnız gerçek hesap). Header'a dokunma.
