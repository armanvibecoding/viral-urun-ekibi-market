# TEKNİK EK T0–T2: tuzaklar, denetim, tanımlar

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 229–256. Metin birebir taşındı; kurallar değiştirilmedi.

---

TEKNİK EK — ANA TEMA HARİTASI VE MCP KALIPLARI
Araç: Shopify Admin GraphQL (MCP). Alan adlarından emin değilsen önce şema sorgusu yap. Her mutation'da `userErrors` iste ve boş olduğunu kontrol et.

T0. Ölçülmüş tuzaklar
- Tema yüklendikten sonra `theme(id) { processing files(filenames: ["templates/product.nis-<niş>.json", "templates/index.json"]) { nodes { filename size } } }` ile dosyaları doğrula. `processing: true` ise bekle ve tekrar sorgula. İşlem bittiği hâlde `product.nis-<niş>.json` yoksa yüklenen zip eskidir (eski sürümde ürün şablonları metafield tanımı olmadan yüklenince Shopify tarafından atlanıyordu): kullanıcıdan bu paketteki güncel temiz zip'i yeni tema olarak yeniden yüklemesini iste, şablonu kendin YAZMA.
- MCP yapamaz: birincil dil ve dil yayını, mağaza adı, ödeme yöntemi, tema yayını (`themePublish`), tema dosyası silme (`themeFilesDelete`), vitrin şifresi. Bunlar Admin işi.
- `productSet` liste alanlarını (files, variants, metafields) eşitler: güncellemede mevcut id'leri listeye koymazsan silinir. Var olan üründe `productSet`'e `seo` gönderme: `global.title_tag` / `description_tag` metafield'larıyla çakışıp INVALID_METAFIELD verir. Kurulu üründe galeri değişikliği yalnız medya işlemleriyle yapılır: `productCreateMedia` (ya da `productUpdate` + `media`) → `productDeleteMedia` → `productReorderMedia`.
- Shopify politikaları kullanılmaz (bağlantıda `write_legal_policies` izni de yok): `shopPolicyUpdate` deneme, kullanıcıdan politika yapıştırması isteme. Yasal metinler yayında sayfa olarak açılır (T7, T8).
- `menuUpdate` öğe listesinin tamamını yeniden yazar.
- Aynı handle'lı sayfa varsa yeni sayfa açma (`-1` eki alır, link kırılır); `pageUpdate` kullan.
- İndirim yüzdesi kesirdir: %15 → `0.15`, %100 → `1.0`. Tarihler UTC: TR 00:00 = önceki gün `21:00:00Z`.
- Abonelik yoksa (`sellingPlanGroups(first:1)` boş) indirimde `appliesOnSubscription` / `appliesOnOneTimePurchase` gönderme: `INVALID` döner.
- Otomatik indirim sınırı 25 (`discountNodesCount(query:"method:automatic status:active,scheduled")`).
- Şablonlar büyüktür: ürün şablonu 85–114 KB (girintisiz 42–55 KB), `index.json` 46 KB (girintisiz 24 KB). `themeFilesUpsert` her yazmada dosyanın TAMAMINI ister, yani sen her yazmada dosyayı baştan sona yeniden göndermek zorundasın. Ölçülmüş hata: bir kullanıcı sohbetinde model büyük şablonu kısaltarak "yeniden yazdı"; ana sayfada 12 bölümden 4'ü, ürün sayfasında 13 bölümden 2'si kaldı. Bu yüzden: şablonu yalnız T4.5 tarifiyle yaz; dosyanın tamamını tek seferde eksiksiz gönderemiyorsan YAZMA, dur ve tema editörü listesine geç. Okuyamadığın dosyayı tahminle ya da sıfırdan ASLA yazma.
- Büyük dosyanın gövdesi okumada `content` yerine kısa ömürlü `url` olarak gelebilir (`... on OnlineStoreThemeFileBodyUrl { url }`); o adresi indirip oku.
- Yedek ve geri dönüş için `themeFilesCopy(themeId, files: [{ srcFilename, dstFilename }])` kullan: içerik sohbetten geçmez, sunucuda kopyalanır, bölüm kaybı olamaz.
- Tema görsel değeri: `shopify://shop_images/<dosya-adı>` (dosya URL'sinin son parçası, `?v=` hariç).

T1. Denetim sorgusu
`shop { name currencyCode taxesIncluded }`, `shopLocales { locale primary published }`, `themes(first:20) { nodes { id name role processing } }`, `products(first:20) { nodes { id handle status templateSuffix } }`, `pages(first:50) { nodes { id handle templateSuffix isPublished } }`, `menus(first:10) { nodes { id handle title items { title type } } }`, `shop { shopPolicies { type url } }`, `locations(first:10) { nodes { id isActive address { countryCode city } } }`, `deliveryProfiles(first:5) { nodes { id default } }`, `publications(first:20) { nodes { id catalog { title } } }`, `sellingPlanGroups(first:1) { nodes { id } }`. Beklenen: `shopLocales` içinde pazarın dili `primary: true, published: true`; TR'de `currencyCode: TRY` (para biçimine bakma, isteme), başka pazarda o pazarın para birimi. ABD'de `currencyCode: USD` ve `taxesIncluded: false` beklenir; AB ve Birleşik Krallık'ta `taxesIncluded: true`. Lokasyon adresini kullanıcıdan isteme.

T2. Tanımlar (hepsi `access: { storefront: PUBLIC_READ }`; varsa tekrar kurma, tipi farklıysa dur)
Önce metaobject tanımları (`metaobjectDefinitionCreate`), dönen id'lerle metafield tanımları (`metafieldDefinitionCreate`; referans doğrulaması `{ name: "metaobject_definition_id", value: "<id>" }`).
- Metaobject `mt_review` (displayNameKey `author`, `capabilities.publishable.enabled: true`): author single_line_text_field*, date date*, rating number_integer (min 1, max 5), body multi_line_text_field*, image file_reference (Image), verified_buyer boolean, sponsored boolean.
- Metaobject `mt_volume_offer` (displayNameKey `title`): title single_line_text_field*, tiers json*, scope single_line_text_field* (choices `["product","collection"]`), collection collection_reference, starts_at date_time, ends_at date_time, discount_ids list.single_line_text_field*, applies_on_subscription boolean.
- PRODUCT `mt_theme`: reviews list.metaobject_reference (→ mt_review), campaign_start date, campaign_end date, campaign_limited_qty number_integer (min 1), volume_offer metaobject_reference (→ mt_volume_offer), light_color color, specs json, benefit_1 / benefit_2 / benefit_3 single_line_text_field.
- PRODUCTVARIANT `mt_theme`: pack_size number_integer (min 1), light_color color, lowest_price_10d number_decimal.
(* = required.) Doğrulama: PRODUCT altında en az 10, PRODUCTVARIANT altında 3 tanım.
