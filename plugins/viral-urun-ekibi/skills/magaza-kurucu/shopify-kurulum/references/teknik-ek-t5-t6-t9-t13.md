# TEKNİK EK T5, T6, T9–T13: ürün, indirim, kargo, ayarlar, koleksiyon, menü

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 410–421 ve 436–463. 0.3.0: galeri 8 medya, T10 ikincil kontrastı ≥ 7, logo yalnız dosya varsa (repo `docs/ESKIDI.md`). T7–T8 `yasal-sayfalar-t7-t8.md`'de.

---

T5. Ürün (`productSet(input:, synchronous: true)`)
Alanlar: `title`, `handle` (Latin, kısa), `descriptionHtml`, `vendor`, `productType`, `status: ACTIVE`, `templateSuffix: "nis-<niş>"`, `tags`, `seo { title description }`, `files: [{ originalSource, contentType: IMAGE, alt }]` ×8 (`<marka>-urun-1..8`, sırayla), `productOptions`, `variants`, `metafields`.
- Varyant: her varyantta `price`, `inventoryItem: { tracked: false }` (stok takibi yok; ürün hep satılabilir), `inventoryPolicy: CONTINUE`. Ölçülü üründe (ml, g) `showUnitPrice: true` + `unitPriceMeasurement`.
- Beden/renk: seçenek `Beden` (ve `Renk`; pazar dilinde); her kombinasyon bir varyant. `Paket` seçeneği açılmaz, `pack_size` yazılmaz.
- Tek varyant: `productOptions` gönderilmez; tek varyant `optionValues: [{ optionName: "Title", name: "Default Title" }]` (reddedilirse `productOptions: [{ name: "Title", values: [{ name: "Default Title" }] }]` ekle).
- Ürün metafield'ları (yalnız gerçek veri): `mt_theme.benefit_1..3` (single_line_text_field), `mt_theme.specs` (json, `[{"k":"Hacim","v":"330 ml"}]`).
- `compareAtPrice` yalnız gerçek fiyat geçmişiyle (o zaman varyanta `mt_theme.lowest_price_10d` de yazılır).
Sonra `publishablePublish(id, input: [{ publicationId: <Online Store> }])`. Doğrulama: varyant sayısı (kombinasyon ya da 1), 8 medya `READY` ve kare (kabul edilen galeri 8'den azsa o sayı; eksikleri "bekleyen"e yaz), `status: ACTIVE`, `publishedOnPublication(publicationId:)` true.

T6. Adet indirimi (her üründe; varsayılan 2 adet %10, 3 adet %18)
Önce kota kontrolü (T0). Kademe başına bir `discountAutomaticBasicCreate`: `title` (müşteri görür, pazar dilinde; ör. "2'li Paket %10", "3'lü Paket %18"), `context: { all: ALL }`, `startsAt` (şimdi), `endsAt` gönderme (süresiz), `combinesWith` üçü `true`, `minimumRequirement: { quantity: { greaterThanOrEqualToQuantity: "2" } }`, `customerGets: { value: { percentage: 0.10 }, items: { products: { productsToAdd: [<ürün gid>] } } }`. Üst kademe aynı ürüne daha yüksek eşikle (3 → `0.18`); Shopify aynı satıra en iyi indirimi uygular. Biri hata verirse oluşanları sil ve dur. Dönen `summary` beklenen oranı söylemiyorsa dur.
Sonra `metaobjectUpsert(handle: { type: "mt_volume_offer", handle: "kademe-<ürün-handle>" })`: title, tiers (JSON string, indirimlerle aynı min/pct/sıra: `[{"min":2,"pct":10,"badge":"recommended"},{"min":3,"pct":18,"badge":"best"}]`), scope `product`, starts_at, discount_ids (oluşan indirim id'leri, JSON string), applies_on_subscription `"false"`. Sonra `metafieldsSet`: ürün `mt_theme.volume_offer` = kayıt id'si. Tema "1 Adet / 2'li Paket / 3'lü Paket" satırlarını bu kayıttan çizer; beden/renk seçimi aynı kalır, indirim farklı bedenlerin toplam adedine uygulanır.

T9. Kargo (`deliveryProfileUpdate`, varsayılan profil). Önce `deliveryProfiles(first: 5) { nodes { id default profileLocationGroups { locationGroup { id } locationGroupZones(first: 20) { nodes { zone { id countries { code { countryCode } } } methodDefinitions(first: 20) { nodes { id name active } } } } } } }`. TR bölgesi yoksa `locationGroupsToUpdate: [{ id: <grup>, zonesToCreate: [{ name: "Türkiye", countries: [{ code: TR, includeAllProvinces: true }], methodDefinitionsToCreate: [{ name: "Ücretsiz Kargo", active: true, rateDefinition: { price: { amount: "0", currencyCode: TRY } } }] }] }]`. Aynı listeye her zaman ikinci yöntem: `{ name: "Hızlı Kargo", active: true, rateDefinition: { price: { amount: "300", currencyCode: TRY } } }`. TR bölgesi varsa `zonesToUpdate` ile güncelle; silinecek eski yöntemleri önce bana göster. Başka pazarda aynı kalıp: bölge = o ülke(ler), "Ücretsiz Kargo" 0 ve "Hızlı Kargo" 10 (USD, EUR ya da GBP; başka para biriminde 10 USD'nin yuvarlanmış karşılığı), adlar pazar dilinde. Bölgede başka tutarlı eski yöntem varsa bu iki yönteme eşitle. Shopify kargo için lokasyon adresi isterse satıcıdan adres İSTEME: kargoyu "bekleyen" olarak yaz, DEVAM KARTI'na "Ayarlar › Lokasyonlar'a mağaza adresini girin, sonra 'kargo' yazın" ekle ve devam et.

T10. Tema ayarları (`config/settings_data.json`)
Oku → yorumu ayır → `current` bir metinse (ör. `"Tr"`) önce `presets["Tr"]` nesnesini `current`'a kopyala → yalnız aşağıdaki anahtarları yaz (iç içe `color_palette`'te yalnız 5 alt anahtar) → yorumu geri ekle → tekrar oku. Listede olmayan ayar YASAK.
| Ayar | Değer |
| `color_palette.background` / `.foreground` / `.color1` / `.color2` / `.color3` | Arka plan / Metin / Ana / İkincil (AÇIK yüzey) / Vurgu, `#RRGGBB` (kontrast kontrolünden sonra; metin/ikincil ≥ 7:1) |
| `type_heading_font` + `type_accent_font` | Görsellerin başlık ailesi (0.4.0): varsayılan `barlow_condensed_n6` (yedek `oswald_n6`); DEVAM KARTI "Tipografi" satırındaki handle birebir |
| `type_body_font` + `type_subheading_font` | Aynı aile: `<aile>_n4` + `<aile>_n5` (varsayılan `inter_n4`, `inter_n5`) |
| `logo`, `logo_inverse`, `favicon` | `shopify://shop_images/<dosya>`; yalnız kullanıcı dosyayı verdiyse, yoksa yazılmaz (header mağaza adını yazar) |
| `mt_buy_product` | Ana ürün handle'ı (menü ve `e-mini.product` ile aynı) |
| `mt_brand_description` | 1–2 cümle, doğrulanmış |
| `mt_market_mode` | Türkiye `tr`, başka pazar `global` |
| `mt_legal_company`, `mt_legal_address`, `mt_legal_phone`, `mt_legal_email`, `mt_legal_tax_id`, `mt_legal_mersis`, `mt_legal_tax_office`, `mt_legal_kep` | Yalnız gerçek bilgi; bilinmeyen `""` |
| `mt_etbis_url`, `mt_etbis_image` | Yalnız gerçek ETBİS kaydı |
| (yalnız TR) `mt_consent_enabled` `true`, `mt_consent_precontract_page` boş bırak (ön bilgilendirme mesafeli sayfasında), `mt_consent_distance_page` `mesafeli-satis-sozlesmesi`, `mt_consent_version` | Sayfalar kurulduktan sonra |
| `mt_consent_shipping_text` | Tek kargo metni; T9 ile birebir (TR: "Türkiye'nin her yerine ücretsiz kargo. Hızlı kargo 300 TL.") |
| `mt_consent_payment_text` | Mağaza gerçeği: taksit varsa "Kabul edilen ödeme yöntemleri ve taksit seçenekleri ödeme adımında listelenir.", yoksa "Kabul edilen ödeme yöntemleri ödeme adımında listelenir." |
| `mt_cart_trust_return_text`, `mt_cart_trust_return_page` | Boşsa iade politikası |
| `mt_cod_enabled`, `mt_cod_fee` | Yalnız Shopify'da kapıda ödeme açıksa |
| `mt_installments_tr`, `mt_installments_min`, `mt_installments_label` | Yalnız sağlayıcının gerçek oranları; gıda ve kozmetikte boş |
| `mt_whatsapp_number`, `mt_whatsapp_label`, `mt_whatsapp_message`, `mt_whatsapp_floating` | Numara yoksa boş (buton görünmez) |
| `mt_express_checkout_tr` | `false` (sepet onayı açıkken `true` olamaz) |
| `empty_state_collection` | T11 koleksiyonunun handle'ı |

T11. Arama koleksiyonu: `collectionCreate(input: { title: "Ürünler", handle: "urunler", products: [<ana ürün gid>] })` → `publishablePublish(id, input: [{ publicationId: <Online Store> }])` → handle `empty_state_collection`'a.

T12. Menüler: `menus` ile `main-menu` ve `footer` id'lerini al; ikisine `menuUpdate(id, title, items)` ile aynı 5 öğe: `{ title: "Anasayfa", type: FRONTPAGE, url: "/" }`, `{ title: "Satın Al", type: PRODUCT, resourceId: <ürün gid> }`, `{ title: "S.S.S.", type: PAGE, resourceId: <sss> }`, `{ title: "Hakkımızda", type: PAGE, resourceId: <hakkimizda> }`, `{ title: "İletişim", type: PAGE, resourceId: <iletisim> }`. Başlık: `main-menu` → "Ana menü", `footer` → "Menü" (footer sütun başlığı olur). Başka pazarda öğe ve başlıklar o pazarın dilinde. Yasal Bilgiler sütunu menü değildir; tema T7 sayfalarından kendisi kurar.

T13. Ürün T5'te AKTİF ve Online Store'da yayında kurulur; ayrı yayın adımı yok. Vitrin şifresi ve tema yayını kullanıcının işidir.
