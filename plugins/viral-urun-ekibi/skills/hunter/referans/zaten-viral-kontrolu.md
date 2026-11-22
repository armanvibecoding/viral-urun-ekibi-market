# "Zaten viral mi?" kontrolü (pazara göre)

Ne zaman okunur: aday listesi çıktıktan sonra (akış adım 4). Amaç: seçilen pazarda bu ürün zaten büyütülmüş mü?
Tanım: `ortak/sozluk.md` → "Tutmamış", "Zaten viral". Her satıra üç sonuçtan biri yazılır: **tutmamış · zaten viral · doğrulanamadı**.

## 1. Pazara göre mağaza kontrolü
| Pazar | Nereye bakılır | Nasıl |
|---|---|---|
| **TR** | Trendyol | `https://www.trendyol.com/sr?q=<terim>&os=1` → ilk ~36 kart: toplam sonuç, aynı ürün var mı (fotoğrafla), en çok değerlendirmeli 3 kart, yaklaşık fiyat. Aynı ürün ≤100 değerlendirme ya da yok → tutmamış. |
| **ABD** | Amazon + TikTok Shop | Amazon aramasında aynı ürün, değerlendirme sayısı, satıcı sayısı, fiyat. TikTok Shop'ta aynı ürünün satış sayısı. Ek doygunluk sinyali: Walmart/Target'ta aynı ürün birçok satıcıdaysa marj baskısı (kaynak turda bir aday bu yüzden düştü: AliExpress 22 $, Walmart'ta aynı ürün 23–38 $, ≥5 satıcı). |
| **Diğer** | O ülkenin en büyük pazar yeri + Amazon'un o ülke sitesi | Aynı yöntem. Hangi sitenin bakılacağını kullanıcıya bir kez sor, KARARLAR.md'ye yaz. |

- Trendyol ve Amazon düz istekte (curl/WebFetch) çoğunlukla engel/captcha verir → tarayıcıdan açılır. Açılamazsa "doğrulanamadı".
- WebSearch özetinde Amazon çoğu zaman görünmez → "Amazon'da yok" denmez, **"bulunamadı"** denir.
- Yokluk ≠ talep yok. Pazar mağazasında hiç olmaması fırsat da olabilir, talep yokluğu da; karar kanıt dosyasında verilir.

## 2. Video kontrolü (≥500 bin izlenme var mı?)
- WebSearch: `"<ürün mekanizması>" tiktok OR instagram`, `"<ürün>" viral`, `"<ürün>" site:tiktok.com`.
- Aynı ürünün ≥500 bin izlenmeli videosu bulunursa → **zaten viral** (ELE). Benzer ürünün videosu sayılmaz (benzer ≠ aynı); not olarak yazılır.
- Instagram/TikTok'ta yalnız izle, ara, profil oku. Takip, yorum, mesaj, kaydetme yok.

## 3. Meta Reklam Kütüphanesi (aktif reklam sayısı)
- Tarayıcıdan, hesap gerekmeden:
  `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=<TR|US>&q="<ifade>"&search_type=keyword_exact_phrase&media_type=all`
- Pazarda aynı ürün için aktif reklam ≤3 → tutmamış koşulu sağlanır.
- **Sessiz sınırlama (ölçüldü):** uzun oturum + art arda çok arama sonrası her arama "eşleşen reklam yok" döner, hata mesajı çıkmaz.
  Kural: aramalar ≥15 sn arayla, oturumda ≤30. Boş sonuçta bilinen dolu bir sorguyla (ör. büyük bir markanın adı) kontrol et; o da boşsa o gün Meta'ya dokunma, sonucu "doğrulanamadı" yaz.
- Rakip mağaza yaşı gerekirse: Shopify mağazasında `/products.json?limit=250` → en eski `created_at` ≈ katalog yaşı. Mağaza yaşı ≠ ürün yaşı.

## 4. Yasaklar
- TrendTrack ve benzeri ücretli "casus" araçlar kullanılmaz (ekip kararı). Ücretli araç gerekiyorsa kullanıcıya sorulur, onay KARARLAR.md'ye yazılır.
- Bot korumasını aşma (gizli sekme, IP değiştirme, CAPTCHA çözme) yok.

## 5. Satıra yazılacak
`Zaten viral?` sütunu: sonuç + en güçlü kanıt (ör. `tutmamış — Trendyol 0 aynı ürün, Meta TR 0 reklam (kontrol sorgusu dolu), video bulunamadı`).

- Meta taraması varsa: `is/meta/sayfalar.tsv` etiketine bak (`spy`); ivme bandı (`ivme_olc.py`) "doymuş" ise ELE, "erken dalga" ise öncelik.
