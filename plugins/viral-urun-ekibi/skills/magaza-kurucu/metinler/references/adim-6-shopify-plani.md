Biçim: KARAKTER bloğu (1. satır eylem · 2. satır `ADIM 6/8 · Copywriter (Naz)` · ≤5 madde · kod bloğu yok · son satır `Sonraki:`).

# Adım 6/8 Shopify planı (site metinleri + yasal)

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 173–188. 0.3.0: banner metni ve logo satırı onaylı görsel diline göre güncellendi (repo `docs/ESKIDI.md`).

---

ADIM 6/8 — SHOPIFY PLANI (TEK MESAJ, ÇOK DETAYLI)
Bütün siteyi tek mesajda, siteye yazılacak SON metinlerle planla. Yeni araştırma yapma; Adım 3 Bulgularını kullan. Yalnız temanın hazır bölümlerini yaz (TEKNİK EK T4). Her blok için tablo:
Bölüm (anahtar) | Amaç | Başlık + metin (pazar dilinde, son hâli) | Görsel (no) | Durum
- Durum: "Doldur" (gerçek veri var), "Boş, gizli" (veri yok; tema gizler), "Aç" (kapalı gelen hazır bölüm, gerçek veri varsa), "Kapalı".
- Mobil ayrı planlanmaz: tema mobil düzeni kendisi yapar. Mobilde farklı olan yalnız banner görselidir: iki bannerda da tipografi görselin içindedir (Adım 4–5'te onaylanan B1 ve B2 metinleri); `e-hero-b` H1 + buton onlarla çelişmez. Tema vitrin şeridini mobilde gizleyemediği için H1 mobilde ikinci kez görünür: H1'i B2 başlığıyla çelişmeyecek, tekrar etmeyecek biçimde yaz ve planda 1 satır not düş.
Bloklar:
- A — Genel ve header: 5 renk + body font, logo/favicon (kullanıcının dosyası varsa; yoksa header'da mağaza adı canlı metin), ana menü (5 öğe), marka açıklaması (1–2 cümle), SEO başlık (≤60) / açıklama (≤155), gerçek sosyal medya linkleri.
- Görsel metni (0.3.4): görselin içindeki yazılar (G1–G8 başlıkları, B2 metinleri) DEVAM KARTI'ndaki onaylı hâliyle kalır; bu adımda yeniden yazılmaz. Yeniden üretim için görsel metni önerirsen `01-kurallar.md` "Görsel metni" maddesi geçerlidir: somut fayda başlığı, "Ücretsiz kargo" gibi lojistik/kampanya/garanti yazısı yok. Kargo, iade ve ödeme bilgisi yalnız site canlı metnindedir (güven şeridi, S.S.S., sepet).
- B — Anasayfa (sırasıyla): banner (B1/B2 + link), vitrin şeridi + tek H1, güven şeridi (4 hücre: kargo, iade, ödeme, destek), mini satın alma kutusu, problem→çözüm, 3 fayda kartı, etiket bilgileri, müşteri videosu, yorumlar (yalnız gerçek yorum), karşılaştırma (rakip marka adı yok), marka hikâyesi, son çağrı. Verisi olmayan "Boş, gizli".
- C — Ürün sayfası, yukarıdan aşağı: içerik yolu, başlık, fiyat ("KDV dahil" TR'de), varyant seçici (beden/renk düğmeleri), adet indirimi kutusu (üst etiket, başlık, alt metin; 1 Adet / 2'li Paket / 3'lü Paket satırları: toplam, üstü çizili tutar, adet fiyatı, rozet), adet + Sepete Ekle, iade satırı ("14 gün iade · Kanuni istisnalar saklıdır." ya da pazarın kuralı), 3 fayda maddesi (onay işaretli), akordeon (Nasıl kullanılır, Ürün açıklaması, Kargo ve iade), güven şeridi (4 hücre), sonra nişin alt bölümleri (T4.3).
- D — Sepet ve çekmece: kargo metni, ödeme metni, iade güven satırı; tamamlayıcı ürün önerisi yalnız gerçek ürünle. TR'de sepet onay kutusu (Ön Bilgilendirme Formu + Mesafeli Satış Sözleşmesi) zorunlu ve hazır; checkout Shopify'ındır.
- E — S.S.S. (kategoriler + soru-cevaplar, son hâliyle; kargo, iade, ödeme, beden/kullanım, iletişim), Hakkımızda ("Alışveriş bilgileri" başlığı ve 3 kart sabit, yalnız kart metinleri; marka hikâyesi sayfa gövdesine; S4 görseli), İletişim (form hazır; konu seçenekleri), koleksiyon şeridi, arama boş durumu, 404.
- F — Yasal sayfalar (T7, 4 sayfa): her sayfanın başlığı + 1 satır özeti. Tam metinler ayrı yanıtta, tek indirilebilir dosyada (`yasal-metinler.md`). Genel taslak; satıcı bilgisi isteme, yer tutucu bırakma. Yer tutuculu metin mağazaya YÜKLENMEZ. Hukuki onay benim.
- G — Kargo: sabit kural (Ücretsiz Kargo 0; Hızlı Kargo Türkiye'de 300 TL, başka pazarda 10 USD/EUR/GBP); teslim süresi ve kesim saati sorulmaz, bilinmiyorsa yazılmaz; adet indirimi kademeleri (T6).
- H — Footer: Menü sütunu, Yasal Bilgiler sütunu (sayfalardan otomatik), bülten başlığı ve metni.
Mesajın sonunda tek liste: "Senden gerekenler": isteğe bağlı, siteyi güçlendirecek bilgiler (gerçek sosyal hesaplar, gerçek yorum ya da video). Teslim süresi ve satıcı bilgisi bu listede YOK; yanıt gelmezse bekleme, devam et.
Planın sonunu "Yasal metinler için devam yaz" diye bitir; sonraki yanıtta `yasal-metinler.md`yi ver ve sor: "Plan ve yasal metinler onaylı mı? (revize için numara yaz)"
