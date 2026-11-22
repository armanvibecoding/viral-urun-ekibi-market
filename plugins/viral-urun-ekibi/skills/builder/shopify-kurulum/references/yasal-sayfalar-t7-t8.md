# TEKNİK EK T7–T8: sayfalar ve yasal metinler

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 423–434. Metin birebir taşındı; kurallar değiştirilmedi.

---

T7. Sayfalar (`pageCreate(page: { title, handle, templateSuffix, isPublished: true, body })`; gövde boş olmaz, boş sayfanın linki basılmaz)
| Sayfa | handle | templateSuffix |
| S.S.S. | `sss` | `faq` |
| Hakkımızda | `hakkimizda` | `about` |
| İletişim | `iletisim` | `contact` |
| Mesafeli Satış Sözleşmesi (gövde iki bölüm: önce "Ön Bilgilendirme Formu", sonra "Mesafeli Satış Sözleşmesi"; taraflar, ürün ve fiyat, ödeme, teslimat, cayma hakkı ve istisnaları, iade süreci, uyuşmazlık) | `mesafeli-satis-sozlesmesi` | — |
| Teslimat ve İade (Ücretsiz Kargo ve Hızlı Kargo tutarları T9 ile aynı; teslim süresi bilinmiyorsa "Teslimat tahmini ödeme adımında gösterilir"; 14 gün cayma, iade adımları (İletişim formu), para iadesi yasal süre içinde; bilinmeyen tutar ve süre yazılmaz) | `teslimat-ve-iade` | — |
| Gizlilik / KVKK (toplanan veriler, amaç, hukuki sebep, aktarım, saklama, çerezler, KVKK md.11 haklar, başvuru: İletişim sayfası) | `gizlilik-ve-kvkk` | — |
| Ölçü Rehberi (yalnız moda, gerçek tablo varsa) | `olcu-rehberi` | — |
Handle'lar sabittir; footer ve sepet onay kutusu sayfayı handle ile bulur. Footer "Yasal Bilgiler" sütunu: Mesafeli Satış Sözleşmesi, Teslimat ve İade, Gizlilik / KVKK, İletişim (sayfası olmayan görünmez). Bütün sayfalar `isPublished: true`. Başka pazarda (global) handle'lar: `refund-policy`, `shipping-policy`, `privacy-policy`, `terms-of-service`, `imprint`, AB'de `withdraw` (cayma), hub `legal` (templateSuffix `legal`); S.S.S. `faq`, Hakkımızda `about`, İletişim `contact`.

T8. Shopify politikaları KULLANILMAZ, boş kalır. Tema footer'daki, sepet onay kutusundaki, ürün sayfasındaki ve metin içindeki `/policies/...` linklerini T7'deki yayında sayfalara kendisi çevirir; sayfa yoksa link basılmaz. Bu yüzden yasal sayfa handle'ları T7'deki gibi aynen kullanılır.
