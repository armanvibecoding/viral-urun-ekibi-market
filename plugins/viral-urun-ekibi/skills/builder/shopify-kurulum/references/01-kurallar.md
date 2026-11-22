# Genel kurallar ve tema kısıtları

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 16–54. 0.3.0'da hukuki maddeler bilgi notuna çevrildi; eski hâlleri repo `docs/ESKIDI.md`'de.

---

GENEL KURALLAR
- Tasarım, renk, body fontu, niş, fiyat, fotoğraf konsepti ve hangi bölümlerin doldurulacağı kararlarını sen ver; bana sorma. Her kararın tek cümlelik gerekçesi olsun.
- Uydurma veri yok (kalite kuralı): doğrulanmamış özellik, sahte yorum, sahte sayı ya da puan, sahte indirim, sahte kıtlık, stok sayacı veya sahte şirket bilgisi yazılmaz. Emin olmadığın olguyu [DOĞRULA] diye işaretle. [DOĞRULA] işaretli olgu siteye yazılmaz.
- Görsel metni (0.3.4; görselin içine basılan yazı, tek kaynak bu madde):
  - Görsele lojistik, kampanya, indirim, fiyat, kargo, teslimat, iade ya da garanti yazısı ASLA yazılmaz. Yasak örnekler: "Ücretsiz kargo", "Kapıda ödeme", "Hızlı teslimat", "Aynı gün kargo", "%20 indirim", "2 al 1 öde", "14 gün iade", "2 yıl garanti". Bu bilgiler yalnız sitede canlı metindir (güven şeridi, S.S.S., sepet).
  - Görseldeki her yazı yalnız DEVAM KARTI'ndaki onaylı metinlerden ve doğrulanmış ürün gerçeklerinden gelir; [DOĞRULA] işaretli bilgi görsele yazılmaz.
  - G1 başlığı ürünün somut faydasıdır (alıcının elde ettiği sonuç), 2–5 kelime. Her görselin başlığı o görselin gösterdiği tek şeyi söyler.
  - Soyut sıfat yığını yok ("Kontrollü form.", "Her kesimde kontrollü form.", "Üstün kalite", "Kusursuz tasarım"). Sınama: başlık başka bir ürüne de yazılabiliyorsa boştur, yeniden yaz.
  - Numara/etiket yazısı yok: "DETAY 01", "01/08", "ÖZELLİK 2" gibi sıra etiketleri ve "detay" kelimesi görsele yazılmaz; büyüteç dairesi de çizilmez.
  - Jargon (ör. "chunker") yalnız hedef kitle profesyonelse ve yanında anlamı yazıyorsa kullanılır.
- Bilgi notu (kullanıcının sorumluluğu; engel değil): sağlık ve sonuç dili (ağrı giderir, tedavi eder, zayıflatır, cildi düzeltir vb.), hastalık adı, üstünlük iddiası, rakip marka adı, indirim ve reklam mevzuatı kullanıcının ve avukatının işidir. Bunlar yüzünden metin, slogan, marka adı ya da görsel elenmez, yumuşatılmaz; ilgili mesajın sonuna tek satır "Bilgi notu (kullanıcının sorumluluğu): …" yazılır. Ürün tıbbi cihaz olabilecekse (EMS/TENS, ışık tedavisi, ölçüm cihazı) ⚠️ bilgi notu yaz; kayıt belgesi istenmez. Kullanıcıya sormadan yeni hukuki yasak eklenmez.
- Müşteriye görünen tüm metinler hedef pazarın dilinde. Türkçede büyük harf yazarken i → İ, ı → I ("MİNİKANAT", "MINIKANAT" değil). Marka adı, pazar, renkler ve görsel dil süreç boyunca tutarlı.
- Sabit ticari kurallar (sorma, uygula):
  - Maliyet sorulmaz; fiyat rakip araştırmasına göre belirlenir.
  - Stok takibi yok: ürün her zaman satılabilir, stok sayısı ya da "son N ürün" yazılmaz.
  - Hediye kampanyası yok.
  - Her üründe adet indirimi var: 1 Adet (tekli fiyat), 2'li Paket %10, 3'lü Paket %18. Oranları araştırmaya göre değiştirebilirsin; gerekçesini yaz. 2'li "En çok tercih edilen", 3'lü en avantajlı rozetini alır. İndirim Shopify otomatik indirimiyle gerçekten uygulanır.
  - Varyant yalnız ürünün gerçek seçenekleridir (Beden, Renk); yoksa tek varyant. Paket varyantı açılmaz.
  - Ürün taslak değil, doğrudan AKTİF ve Online Store'da yayında oluşturulur. Vitrin şifresi ve tema yayını benim kararım.

TEMA KISITLARI (ilk adımdan itibaren geçerli)
Mağaza hazır **Ana Tema** ile kurulur. Bana ayrıca `Ana-Tema-temiz-*.zip` verilir (yüklenecek tema; içinde örnek ürün, fotoğraf ve metin yok). Bölüm anahtarları, ayar adları, metafield tanımları ve MCP kalıpları bu promptun sonundaki **TEKNİK EK**'tedir. Anahtar, ayar adı ve handle'ı YALNIZ oradan al; tahmin etme. Tablolarda geçmeyen hiçbir anahtara yazma.
- Pazar modu: Türkiye → tema `tr` modu (TRY, Türkçe, TR sözleşme onay kutusu). Başka pazar → `global` modu (o pazarın dili ve para birimi, AB/ABD yasal sayfaları). Global mod henüz canlı mağazada denenmedi: o pazarda Adım 8 sonunda bütün sayfaları ayrıca kontrol et.
- Sayfa düzeni ve bölüm sırası sabit. Bölüm silme, ekleme, taşıma; boşluk, köşe, hiza, yazı ölçeği, CSS değiştirme. Senin "sayfa düzeni kararın" hazır bölümlerden hangisinin doldurulacağıdır. Tasarımda değişen yalnız 5 renk + başlık fontu + body fontu.
  Bu kısıt sitenin tema ayarları içindir. Ürün görsellerinin tipografisi (niş anahtarı A/B) ve zemin rengi görselin içinde tasarlanır (`gorseller`); bunun için tema ayarı değiştirilmez.
- Renk: temanın 5 renk rolü şöyle kullanılır, roller karışmaz:
  - arka plan: sayfa zemini, açık ton
  - metin: koyu ana yazı rengi
  - ana: butonlar ve koyu vurgu yüzeyleri (koyu ton)
  - ikincil: AÇIK yüzey rengi (kart, şerit ve sepet çekmecesi zemini); arka plana yakın, çok açık bir ton. Koyu ikincil renk seçme. Ölçü: metin/ikincil ≥ 7:1 ve arka plan/ikincil ≤ 1.3:1 (ör. arka plan #FFF9F4 ise ikincil #F4ECEE gibi). Bu iki oranı planda sayıyla yaz; tutmuyorsa ikincili açılt. Tema kartları, şeritleri, son çağrı kutusunu, beden düğmelerini, footer'ı ve sepet çekmecesini bu renkle boyar; koyu ikincil bunların hepsini okunmaz yapar
  - vurgu: rozet, küçük etiket ve vurgu rengi Kontrast: metin/arka plan ≥ 4.5:1; ana renk üstündeki buton yazısı (arka plan rengi) ≥ 4.5:1; ikon ve kenar ≥ 3:1. Tutmuyorsa aynı tonda düzelt.
- Fontlar (0.4.0, tek yazı sistemi): sitenin başlık ailesi = görsellerin başlık ailesi. Varsayılan Barlow Condensed SemiBold (`type_heading_font` ve `type_accent_font` = `barlow_condensed_n6`; yedek Oswald `oswald_n6`); ikisi de Shopify font kütüphanesinde, Türkçe harfleri kapsar. Poppins, Montserrat ve benzeri geniş geometrik başlık ailesi kullanılmaz. Sayfada tek H1; ürün adı (H1) normal yazımla, BÜYÜK HARF yalnız görselde ve kısa etikette. Body fontu yalnız şu listeden: Inter (varsayılan), Inter Tight, Hanken Grotesk, DM Sans, Plus Jakarta Sans, Outfit. Neden: bir müşteri mağazasında (2026-11) görsel başlığı dar grotesk, site başlığı Poppins çıktı; iki ayrı marka gibi göründü (tema `type_heading_font` ayarını zaten okuyor).
- Niş: ürün sayfasının bölüm setini belirler (TEKNİK EK T4.3). Seç, 1 satır gerekçe yaz, sorma. `templateSuffix` birebir şunlardan biri:
  - `nis-guzellik`: kozmetik, cilt bakımı, güzellik cihazı
  - `nis-saglik`: takviye ve tüketilen wellness ürünü
  - `nis-gadget`: problem çözen cihaz (masaj, uyku, temizlik, ağrı cihazları dahil)
  - `nis-ev`: mutfak, ev gereci, set
  - `nis-moda`: takı, çanta, giyim, kostüm, bebek-çocuk giyim
  - Pet / evcil hayvan ekipmanı (tüy makası, tarak, tıraş makinesi, tasma, mama kabı) ve el aletleri: `nis-gadget`. Temada `nis-pet` şablonu yoktur; pet makası güzellik (`nis-guzellik`) DEĞİLDİR: `nis-guzellik` yalnız insanın kendi cildine/saçına kullandığı ürün içindir.
- Bilinmeyen alan boş kalır; tema boş bölümü vitrinde kendiliğinden gizler. Yer tutucu yazma ("Fayda 1", "örnek", "Lorem").
- Site metinlerinde şu kelimeler geçmez: "doğal", "organik", "temiz içerik", "eco", "çok satan", "en çok satan", "N bin müşteri" (ve pazar dilindeki karşılıkları). İstisna: adet indiriminin "En çok tercih edilen" rozeti temanın kendi metnidir.
- Ekip notu: bu kelimelerin makineyle denetlenen tek listesi ekibin `yasak-ifadeler.tsv` dosyasıdır (`ekip-koprusu.md` §4).
- Header: logo solda; ortada menü (Anasayfa, Satın Al, S.S.S., Hakkımızda, İletişim; bulunulan sayfa yuvarlak açık zeminle vurgulanır); sağda arama, hesap, sepet. Duyuru çubuğu yok. Tasarım temada hazır; yalnız menüyü kurarsın.
- Footer (temada hazır): logo | "Menü" sütunu (header menüsüyle aynı 5 öğe) | "Yasal Bilgiler" sütunu (Mesafeli Satış Sözleşmesi, Teslimat ve İade, Gizlilik / KVKK, İletişim) | "Bizden haber alın" bülten. Yasal sütun sayfalardan otomatik dolar; sayfası olmayan link görünmez.
- Yasal metinler YALNIZ 4 SAYFADIR (TEKNİK EK T7): Mesafeli Satış Sözleşmesi, Teslimat ve İade, Gizlilik / KVKK, İletişim. Başka yasal sayfa (çerez, künye, kullanım koşulları, ayrı ön bilgilendirme, işlem rehberi, "tüm yasal bilgiler") oluşturma.
- Yasal metinler GENEL TASLAKTIR: benden satıcı bilgisi (unvan, adres, telefon, e-posta, vergi no, MERSİS, KEP, ETBİS) İSTEME. Satıcı adı olarak mağaza adını kullan; iletişim için "İletişim sayfamızdaki form" de. Adres, telefon, e-posta, vergi no gibi bilgileri uydurma ve metne yazma; köşeli parantezli yer tutucu ([SATICI UNVANI] gibi) ya da [DOĞRULA] da bırakma. Metin bu bilgiler olmadan da eksiksiz ve okunur olmalı.
- Kargo (sabit, sorma): standart kargo HER ZAMAN ücretsizdir (0). Hızlı kargo: Türkiye'de 300 TL; başka pazarda 10 USD, 10 EUR ya da 10 GBP (pazarın para birimi; başka para biriminde 10 USD'nin yuvarlanmış karşılığı). Yöntem adları pazar dilinde "Ücretsiz Kargo" ve "Hızlı Kargo". Tutarlar her yerde birebir aynı: Shopify kargo yöntemleri (T9), temadaki kargo metni (`mt_consent_shipping_text`), güven şeridi, S.S.S., Teslimat ve İade sayfası.
- Satıcıdan bilgi İSTENMEZ: teslim süresi, kargo kesim saati, adres, telefon, ödeme ayrıntısı, ürünün fotoğraflarda görünmeyen teknik değerleri dahil. Bilinmeyen bilgi siteye yazılmaz: teslim tarihi satırı kapalı kalır (T4.2 `delivery`), süre yerine "Teslimat tahmini ödeme adımında gösterilir" yazılır; bilinmeyen özellik (pil süresi, konum, su dayanımı vb.) hiçbir metinde ve görselde geçmez.
- Canlı temaya yazma; her şey yayınsız Ana Tema üzerinde yapılır.
