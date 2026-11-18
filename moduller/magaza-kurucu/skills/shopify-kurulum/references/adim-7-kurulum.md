Biçim: KARAKTER bloğu (1. satır eylem · 2. satır `ADIM 7/8 · Store Architect (Baran)` · ≤5 madde · kod bloğu yok · son satır `Sonraki:`).

# Adım 7/8 Mağaza kurulumu (MCP)

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 190–213. 0.3.0: galeri 8 kare, logo yükleme yuvası, DEVAM KARTI biçimi `00-calisma-tarzi.md` (eski hâli repo `docs/ESKIDI.md`).

---

ADIM 7/8 — MAĞAZA KURULUMU (MCP)
Onayımı alınca uygula. Bu adımda yalnız İKİ kez durursun: 7.2 listesinden sonra (benim elle yapacaklarım) ve en sonda DEVAM KARTI'yla. "Yaptım" deyince 7.3'ten 7.9'a kadar hepsini TEK yanıtta, aralarda soru sormadan ve onay beklemeden yap. Her işlemden sonra 1 satır durum yaz (ne yapıldı + id). Ön koşulu eksik olan maddeyi (ör. lokasyon adresi gerekli ve yok → kargo) atla, sona "bekleyen" olarak yaz ve sonraki maddeye geç. Yalnız sonraki adımları da bozan bir hata olursa dur; nedenini ve tek düzeltme önerini yaz. Araç sınırı yanıtı keserse kaldığın maddeyi yaz; "devam" deyince oradan sürdür.
7.1 Metafield ve metaobject tanımlarını (T2) MCP ile HEMEN kur ve sorguyla doğrula; benden bir şey isteme. Aynı yanıtta Adım 5'te kabul edilen bütün görselleri MCP ile Admin › İçerik › Dosyalar'a T3 adlarıyla YÜKLE (Shopify bağlantısının dosya yükleme aracı; yoksa `stagedUploadsCreate` + `fileCreate`) ve T3 sorgusuyla hepsi `READY` olana kadar doğrula. Bağlantının yükleme aracı hata verirse aynı yanıtta `stagedUploadsCreate` + `fileCreate` ile dene. O da olmazsa kurulumu DURDURMA: yükleyemediklerini HEMEN tek zip olarak ver, 7.2 listesine "Dosyalar'a yükle (Admin › İçerik › Dosyalar › Dosya yükle; adları değiştirmeden)" maddesi ekle; "yaptım" denince T3 sorgusuyla bul ve kullan.
7.2 Benim yapacaklarım: önce kontrol et (T1); eksik olanları TEK listede iste ve dur, "yaptım" deyince tekrar doğrula. Liste:
   Pazara göre değerler (listeyi YALNIZ seçilen pazarın değerleriyle yaz, diğerlerini gösterme):
   | Pazar | Dil | Para birimi | Para biçimi | Fiyat |
   | Türkiye | Türkçe | TRY | Shopify varsayılanı, değiştirme | KDV dahil |
   | ABD | English | USD | Shopify varsayılanı (${{amount}}), değiştirme | vergi hariç (vergi ödeme sayfasında eklenir) |
   | AB ülkesi | o ülkenin dili | EUR | Shopify varsayılanı | KDV dahil |
   | Birleşik Krallık | English | GBP | Shopify varsayılanı | KDV dahil |
   Başka ülke: o ülkenin dili ve para birimi, Shopify varsayılan biçimi.
   - DİL: Ayarlar › Diller'de pazarın dilini ekle, BİRİNCİL dil yap ve yayınla (ABD'de English zaten birincilse bu madde yok). Bunu unutma: dil seçili değilse tema metinleri ve ödeme sayfası yanlış dilde çıkar.
   - Para birimi: pazarın para birimi (ilk satıştan önce; mağaza zaten o para birimindeyse bu madde yok). Para BİÇİMİ hiçbir pazarda istenmez ve kontrol edilmez: Türkiye'de açılan mağaza TRY ve Türk biçimiyle gelir; `{{amount}}TL` gibi varsayılan biçim olduğu gibi kalır.
   - Mağaza adı (marka adı).
   - Logo (`gorseller` adımında üretilen ikon ya da kullanıcının kendi logosu): dosya varsa `<marka>-logo.png` (ve varsa `<marka>-favicon.png`) adıyla Admin › İçerik › Dosyalar'a yükle ya da sohbete ekle. Yoksa bu maddeyi atla: header mağaza adını canlı metin yazar.
   "Yaptım" deyince T1'i tekrar çalıştır. Dil ve para birimi de tutmuyorsa yalnız eksik maddeleri tekrar iste.
   - Tema (7.1 tanımları kurulduktan sonra): temiz Ana Tema zip'ini yükle: Admin › Online Mağaza › Temalar › İçe aktar › Zip dosyası yükle. YAYINLAMA.
7.3 Ürün (T5): AKTİF, stok takibi yok, 9 galeri fotoğrafı (`<marka>-urun-0..8`, bu sırayla; 0 = yazısız feed karesi, ürünün ana görseli), `templateSuffix` (niş), varyantlar, fayda ve etiket metafield'ları; Online Store'da yayınla.
7.4 Adet indirimi (T6).
7.5 Sayfalar (T7): S.S.S., Hakkımızda, İletişim ve 3 yasal sayfa (Mesafeli Satış Sözleşmesi, Teslimat ve İade, Gizlilik / KVKK). Yasal metinler YALNIZ sayfadır ve hepsi YAYINDA açılır (`isPublished: true`; gizli ya da taslak sayfa oluşturma). Shopify politikalarına (Ayarlar › Politikalar) dokunma, benden de isteme; boş kalırlar, tema yasal linkleri sayfalara bağlar (T8). Sepet onay kutusu (mt_consent_enabled) Mesafeli Satış Sözleşmesi SAYFASINA bağlıdır (ön bilgilendirme o sayfanın içindedir); sayfa oluştuysa 7.8'de aç.
7.6 Kargo (T9).
7.7 Arama koleksiyonu (T11).
7.8 Tema ayarları (T10) ve şablon içerikleri (T4 haritası, Adım 6 tabloları): `themeFilesUpsert` ile, YALNIZ T4.5 tarifiyle (önce `themeFilesCopy` yedeği, sonra Python'la yama, harita kontrolü, eksiksiz yazım, tekrar okuma). Şablonu ASLA sıfırdan yazma; bölüm ve blok silinmez, kod dosyalarına (`.liquid`, `snippets/`, `assets/`, `locales/`) yazılmaz, hiçbir dosya silinmez (T4 kuralları). Her şablonu yazdıktan sonra bölüm adları, tipleri ve blok sayıları T4.0 haritasıyla aynı olmalı; değilse yedeği `themeFilesCopy` ile geri kopyala ve dur. Tema dosyası yazmadan önce bir kez hedef temanın `role` değerini sorgula: `UNPUBLISHED` değilse dur. MCP tema dosyası yazamazsa ya da yazım kesilirse dur; bana tema editöründe tıklanacak yerleri bölüm bölüm ver.
7.9 Menüler (T12).
Bitince DEVAM KARTI ver (biçim `00-calisma-tarzi.md`; yeni sohbette kaldığımız yerden sürdürmek için): mağaza, pazar, tema id, ürün handle ve gid, marka adı, 5 renk + font, yüklenen dosya adları, yüklenmeyen sayfalar ve nedeni, bekleyen işler. Sonra "devam yaz".
