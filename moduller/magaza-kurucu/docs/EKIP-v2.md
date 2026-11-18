# Ekip v2 (sürüm 0.4.0): neyin, neden değiştiği

Tarih: 2026-11-18. Kaynaklar: `research/kutuphane-v2/` (ölçülen kütüphane: `ANALIZ.md`, `markalar.jsonl/.csv`, `etiketler/`; kanıt tablosu: `KANIT.md`; yöntem ve sınırlar: `YONTEM.md`; elle doğrulama: `DOGRULAMA.md`).

## 1. Kısaca
- 420 başarılı Shopify markasının siteleri, ürün sayfaları, galerileri, tipografisi ve hızı ölçüldü; e-ticaret kullanılabilirlik ve platform kurallarından 55 maddelik kanıt tablosu çıkarıldı.
- Çalışma zamanına (ChatGPT ve Claude'da çalışan 5 aşama) üç büyük değişiklik girdi: **tek yazı sistemi** (sitenin başlık fontu = görsellerin başlık ailesi), **yazısız G0 feed karesi** (galerinin 1. görseli), **site denetimi** (hız, arama/feed, erişilebilirlik, satın alma kutusu). Öbür plugin'lerle birleşme için **arayüz sözleşmesi** eklendi.
- Geliştirme ekibi 15 rolden 25 role çıktı; her yeni rolün girdisi, ölçülebilir kontrol listesi, çıktısı ve testi var.
- Kör deneme (bir müşteri ürün sayfasıyla; malzeme repo dışında): ürün sayfası ilk ekranı eski 5,57 → v2 6,86 (kategori lideri Dame ile eşit, Maude 7,57). En büyük açık hâlâ ürün gerçekliği.

## 2. Ne ölçüldü, en önemli bulgular
**Örneklem:** 1.293 alan adlık liste (Shopify vaka çalışmaları ve blog, ecomm.design, Awwwards, Land-book, Siteinspire, büyüme listeleri + niş tohumu) → 465 tarandı, **420 marka ölçüldü** (376'sı Shopify; 16 niş: güzellik 99 · sağlık 64 · gıda 58 · ev 41 · diğer nişler 8–19). Ana sayfa 1440 px, ürün sayfası 1440 + 390 px, katalog (`products.json`), mobil hız (221 marka, laboratuvar). Galeri türleri otomatik sınıflayıcıyla değil, **gözle etiketlenmiş örneklemle** ölçüldü (sınıflayıcı %53 isabetli; `research/kutuphane-v2/DOGRULAMA.md`). Sınırlar: `YONTEM.md` (başarı satışla değil kaynakla tanımlı; Shopify `products.json` 158 markada hız sınırı verdi ve zorlanmadı → galeri verisi 175 markada).

| # | Bulgu (ölçülen) | Ekibe etkisi | Kanıt gücü |
|---|---|---|---|
| 1 | Galerinin 1. görseli: %68 eklenmiş yazısız düz ürün, %17 rozet/indirim/yazı, %9 insan; temiz karelerde ürün kareyi medyan %80 dolduruyor (n=144) | G0 feed karesi (yazısız, %75–86) | güçlü: Google kuralı + çoğunluk kalıbı |
| 2 | Galeri karışımı (192 kare): insanlı %39 ±7, düz ürün %28, yazılı grafik kart %27, sahne %7; kahraman ürün galerisi medyan 7 görsel (p25 4,5 · p75 10), %64'ü kare | Galeri G0 + 8 kare makul (p75 içinde); insan yerine insansız ölçek kartı | orta (örneklem) |
| 3 | Kullanıcının sevdiği dil (insansız, düz zemin, büyük başlık, gerçekçi ürün kartı) galerisi okunan 172 markanın yalnız ≈ %2'sinde ağırlıklı; koyu zeminli kare %16; sitede dar grotesk başlık %4, koyu gövde zemini %4 | Dil korunur ama "farklılaşma, ölçülmüş başarı kalıbı değil" diye etiketlenir; kör pano + kullanıcı karar verir | orta |
| 4 | Site tipografisi: başlık ve gövde aynı aile %55, kullanılan aile medyanı 2, başlık BÜYÜK HARF %17; en sık başlık aileleri Poppins ve Montserrat | Tek yazı sistemi (görsel = site), 2 aile; geniş geometrik yasağı bilinçli ayrışma | orta |
| 5 | Hız (aynı laboratuvar profili, 221 marka): hızlı %20 → toplam 1,0 MB, JS 0,42 MB, 9,5 alan adı; yavaş %20 → 2,6 MB, JS 1,1 MB, 18 alan adı. LCP ↔ toplam bayt Spearman 0,71, TTFB 0,09. LCP görselinin %16'sı hâlâ `lazy`, yalnız %56'sı `fetchpriority=high` | `site-denetimi` bayt bütçesi; `hiz-muhendisi` kapıları | orta (laboratuvar, alan verisi değil) |
| 6 | Ürün sayfası (343): mobilde sepete ekle ilk ekranda yalnız %18, yapışkan çubuk %51; başlık yanında yıldız %43; paket/adet indirimi %30; kargo/iade satırı %27; teslimat tahmini %7 | Mobil CTA kuralı; toplam maliyet satırı (Baymard: sepet terkinin 1. nedeni ek maliyet %40) | orta + güçlü (KANIT 7.6) |
| 7 | Ana sayfa: bölüm medyanı 9 (p25 7 · p75 12); hero %79, görsel-metin %73, ürün ızgarası %66 (3. sıra), yorum %39; duyuru şeridi %55 | `site-bolum-mimari` iskeleti ve bölüm sayısı aralığı | orta |
| 8 | Logo: kelime logosu %62, kombinasyon %13, yalnız ikon/monogram %9; %63'ü SVG | "Yalnız ikon" kararı azınlık: header'da ad görünürlüğü riski brife yazılır | orta |
| 9 | Arama/AI: Product JSON-LD %91 (aggregateRating %53); AI botlarını engelleyen %2; mağazaların %84'ünde Shopify'ın kendiliğinden ürettiği "Agent Instructions" llms.txt (Shop skill/UCP) | `seo-aio-uzmani`: ek "GEO" işi yok; feed ve yapılandırılmış veri tamlığı | güçlü (Google: ek şart yok) |

Kör deneme (bir müşteri ürün sayfasıyla; görseller ve panolar repo dışında): galeri kartı istemi eski 25/50 → v2 35/50; ürün sayfası ilk ekranı 3 bağımsız eleştirmen medyanı eski 5,57 → v2 6,86 (Dame 6,86, Maude 7,57). v2'yi tutan: ürün gerçekliği (CG/AI render 5–6 puan), mobilde fiyat/buton ilk ekranda değil, mor hızlı ödeme düğmesi.

## 2b. Kanıt tablosu (özet; tamamı `research/kutuphane-v2/KANIT.md`, 55 madde)
| Kural | Kaynak | Güç |
|---|---|---|
| Ana görselde yazı/rozet/logo/kenarlık yok, ürün %75–90, ≥ 1500 px önerilir | https://support.google.com/merchants/answer/6324350 | güçlü (platform kuralı) |
| CWV: LCP ≤ 2,5 sn, INP ≤ 200 ms, CLS ≤ 0,1 (75. yüzdelik) | https://web.dev/articles/vitals | güçlü (kılavuz) |
| LCP %31 iyileşme → satış +%8 (A/B) | https://web.dev/case-studies/vodafone | güçlü (deney) |
| LCP görseli lazy değil, `fetchpriority=high`, `image_url` boyutlu | https://shopify.dev/docs/storefronts/themes/best-practices/performance | güçlü (kılavuz) |
| Shopify kökenlerinin %76'sı CWV geçiyor | https://almanac.httparchive.org/en/2025/ecommerce | güçlü (büyük örneklem) |
| Kontrast 4,5:1 / 3:1, hedef 24 px | https://www.w3.org/TR/WCAG22/ | güçlü (standart) |
| EAA e-ticarete 28.06.2025'ten beri uygulanıyor (bilgi notu) | https://www.legislation.gov.uk/eudr/2019/882/article/31 | güçlü (hukuk metni) |
| AI Overviews/AI Mode için ek şart yok; llms.txt resmi değil | https://developers.google.com/search/docs/appearance/ai-features | güçlü (kılavuz) |
| Ürün yapılandırılmış verisi (merchant listing) | https://developers.google.com/search/docs/appearance/structured-data/merchant-listing | güçlü |
| Ürün sayfasında ilk eylem görsel (%56), boyut görselden anlaşılmaya çalışılıyor (%42) | https://baymard.com/blog/in-scale-product-images | orta |
| Masaüstünde küçük resim şeridi, mobilde kaydırma | https://baymard.com/blog/always-use-thumbnails-additional-images | orta |
| Yatay sekme yerine dikey bölümler | https://baymard.com/blog/avoid-horizontal-tabs | orta |
| Mobilde otomatik dönen slider yok | https://baymard.com/blog/homepage-carousel | orta |
| Sepet terki ortalama %70; 1. neden ek maliyet %40 | https://baymard.com/lists/cart-abandonment-rate | orta-güçlü |
| 5 yorum → satın alma olasılığı +%270; 4,0–4,7 yıldızda zirve | https://spiegel.medill.northwestern.edu/how-online-reviews-influence-sales/ | orta |
| Görselin AI olduğunu bilmek güveni düşürür (%60, öz-bildirim) | https://baymard.com/research-articles/ai-engagement-quantitative-ux-insights-2026 | orta |
| Shopify font kütüphanesinde Barlow Condensed (`barlow_condensed_n6`), Latin Extended-A | https://shopify.dev/docs/storefronts/themes/architecture/settings/fonts | güçlü (platform) |

Kanıtı bulunamayan yaygın inançlar (kural yazılmadı): "tam 7/8 görsel", "en fazla 3 font", "Merchant'ta beyaz zemin zorunlu", "yapışkan sepete ekle her zaman artırır", "güven rozeti %X artırır", "llms.txt görünürlük artırır", "mobilde 16 px zorunlu", "44 px hedef AA şartı".

## 2c. Kullanıcı zevki ↔ kanıt gerilimleri ve karar
| Gerilim | Karar |
|---|---|
| Baymard giyilen/sürülen üründe insan model öneriyor; kullanıcı insansız galeri istiyor | Galeri insansız kalır; boyut sorusu insansız ölçek kartıyla yanıtlanır; bedenli giyimde kullanıcıya tek satır sorulur (mevcut kural) |
| Yazılı afiş G1 kullanıcıya göre en iyi kare; Google ana görselde yazıyı yasaklıyor | Afiş korunur, 2. sıraya geçer; 1. sıraya yazısız G0 |
| Kullanıcının dili (koyu zemin, dar grotesk, grafik kart) başarılı markalarda nadir | Dil korunur; "farklılaşma" diye etiketlenir; başarı iddiası yazılmaz, kör pano ölçer |
| Kör denemede en büyük açık ürün gerçekliği (AI render) | Ölçülmeden kural yazılmadı; "Ne kaldı"daki deney |


## 3. Çalışma zamanında ne değişti (ChatGPT + Claude paketi)
| Değişiklik | Neden (kanıt) | Dosya |
|---|---|---|
| Sitenin başlık fontu = görsellerin başlık ailesi (Barlow Condensed 600, `barlow_condensed_n6`; gövde Inter) | Gerçek bir kurulumda görsel dar grotesk, site Poppins çıktı; kör denemede "galeri başlığı ürün adını eziyor, iki sistem" (eski 5,57). Tema `type_heading_font`'u zaten okuyor; kısıt bizim kuralımızdı. Kütüphanede başlık ↔ gövde aynı aile oranı ve başlık sınıfları: ANALIZ §3 | `src/ortak/01-kurallar.md` Fontlar, `skills/shopify-kurulum/references/teknik-ek-t5-t6-t9-t13.md` T10, `skills/marka/references/logo-renk-font.md`, ESKIDI E57 |
| G0 feed karesi: galerinin 1. görseli yazısız, tek ürün, uzun kenar tuvalin %75–86'sı, ≥ 1500 px; yazılı afiş 2. sıraya | Google Merchant Center `image_link` kuralı: yazı, rozet, fiyat, logo, kenarlık yasak; ürün %75–90 (KANIT 4.3, güçlü). Kütüphanede 1. görselin çoğunluğu eklenmiş yazısız (DOGRULAMA) | `skills/gorseller/references/istemler/g0-feed.md`, `kabul-kontrolu.md` §2c, `adim-4`, `adim-5`, T3 `urun-0`, `adim-7`, `adim-8` |
| Site denetimi (Adım 8) | CWV eşikleri ve Shopify LCP kuralları (KANIT 3.1, 3.6), WCAG 2.2 AA (5.1–5.3), sepet terki 1. nedeni ek maliyet (7.6), dikey bölümler (1.9), kör deneme: mobilde CTA ilk ekranda değil | `src/ortak/site-denetimi.md` (shopify-kurulum + metinler) |
| Arayüz sözleşmesi: `urun-paketi.json` girdi, `magaza-paketi.json` çıktı, `video-paketi.json` geri dönüş | Ürün bulan ve video yapan plugin'lerle birleşme; iki yüzeyde aynı dosya biçimi | `src/ortak/arayuz-sozlesmesi.md` (urun-analiz + shopify-kurulum), yönlendirici `src/tek/SKILL.md` |
| Şablonlarda tipografi cümlesi: "web sitesinin yazı tipi bu görselde KULLANILMAZ" → "bu dar grotesk aile markanın tek başlık ailesidir" | Görsel ve site artık aynı aile | `skills/gorseller/references/istemler/*.md`, `ortak-istem-bloklari.md` |
| DEVAM KARTI "Tipografi" satırı (aile + handle) ve `urun-0` | Aynı satırdan hem istem hem tema ayarı üretilir | `src/ortak/00-calisma-tarzi.md` |

## 4. Ekip (25 rol; `.claude/agents/`)
Yeni roller (10) **kalın**. Her rolde: girdi, ölçülebilir kontrol listesi, çıktı dosyası, test.

| Rol | İş | Ne zaman |
|---|---|---|
| marka-stratejisti | konumlama, rakip haritası (artık kütüphane sayılarıyla) | görselden önce |
| referans-kuratoru | üst düzey referans + kütüphane v2 havuzu | strateji sonrası |
| kreatif-direktor | 3 kimlik yönü; başlık ailesi Shopify kütüphanesinden ve iki yüzeyde aynı | yön |
| nis-stil-mimari | niş stil kartı; kütüphane oranları, zevk dilinin nadirliği | yeni niş |
| **tipografi-sistemcisi** | görsel ↔ site tek yazı sistemi, tema font ayarları | marka + her tur |
| tasarim-dili | çekirdek dil; yalnız kanıtlı kural çekirdeğe | sürüm |
| urun-kilidi-analisti | ürün kilidi, sadakat; G0 en sıkı kapı; yapay görünüm işaretleri | üretim öncesi/sonrası |
| metin-yazari | görsel içi metin; zayıf sayı başlık olmaz; metrik + imperial | istem öncesi |
| prompt-muhendisi | istem; G0, ölçek kartı, birim kilidi | üretim |
| gorsel-uretici | ChatGPT'de üretim (onaylı liste) | üretim |
| **gorsel-qa** | OCR ile yazım kapısı (RapidOCR + Tesseract `tur`), G0 kontrolü | her görsel |
| seri-tutarlilik-denetcisi | K2–K4, set tutarlılığı, kör pano | tur sonu |
| kor-elestirmen | kör puan; artık site bölümü ve istem panoları da | tur sonu |
| tasarim-direktoru | kök neden sınıfı + tek değişkenli emir; yeni sınıflar | tur sonu |
| logo-arastirmaci / logo-tasarimci | logo; kütüphanede kelime logosu %62 | marka |
| **site-bolum-mimari** | ana sayfa ve ürün sayfası bölüm planı (kütüphane kalıbı) | metinlerden önce |
| **marka-sesi-denetcisi** | site metni: uydurma iddia, yapay zekâ kalıbı, tekrar | metinler sonrası |
| **cro-ux-denetcisi** | Baymard kontrol listesi, satın alma kutusu, mobil CTA | kurulum sonrası |
| **hiz-muhendisi** | laboratuvar ölçümü, bayt bütçesi, LCP kuralları | kurulum sonrası |
| **seo-aio-uzmani** | feed görseli, JSON-LD, alt metin, AI arama | metinler + kurulum |
| **erisilebilirlik-denetcisi** | WCAG 2.2 AA kontrast/hedef/metin görseli | marka + kurulum |
| **platform-uyum-muhendisi** | ChatGPT ↔ Claude paket ve arayüz sözleşmesi | her sürüm |
| **kutuphane-bakimci** | kütüphaneyi yeniden tarar, eskimiş sayıları işaretler | çeyrekte bir |
| benchmark-kosucusu | gerçek ChatGPT koşusu; artık site ölçümleriyle | onaylı koşu |


## 5. İki yüzeyde çalışma (ChatGPT + Claude)
- **Çalışma zamanı ekibi aşama içindedir.** ChatGPT'de ve claude.ai sohbetinde alt ajan yok (plugin `agents/` claude.ai Chat'te yok sayılıyor; ChatGPT plugin'i ajan dosyası taşımıyor: `research/plan/YOL-HARITASI.md` §0). Bu yüzden yeni rollerin kullanıcıya dokunan işi aşama dosyalarına girdi: tipografi (marka adımı + T10), feed karesi (görseller), site denetimi (Adım 8), arayüz (urun-analiz + kurulum). `.claude/agents/` yalnız geliştirme ekibidir; pakete girmez.
- **Paket sınırları korunuyor:** her SKILL.md ≤ 5.120 bayt (marka 5.094, gorseller 5.078, shopify-kurulum 4.818, yönlendirici 4.915), `tools/build.py --check` geçiyor, 80 test + 35 alt test geçiyor (yeni: `tests/test_ocr_kontrol.py`). Yeni reference dosyaları `src/ortak/` tek kaynaktan kopyalanıyor.
- **ChatGPT:** yalnız Çalışma modu (test14: Sohbet modunda şablonlar okunmadı). Yükleme insan eliyle (Skills › Upload `magaza-kurucu.zip` ya da Plugins › arşiv). G0 istemi de tek çağrı = tek görsel kuralına uyuyor.
- **Claude:** görsel üretmez; G0 dahil istemler dosya olarak verilir. Shopify bağlayıcısıyla kurulum aynı.
- **Doğrulanmadı:** 0.4.0 gerçek ChatGPT Çalışma koşusunda henüz denenmedi (görsel üretimi kullanıcı onayı ister). `platform-uyum-muhendisi` ilk koşuda G0'ın yazısız gelip gelmediğini ve T10'da `type_heading_font` yazımını kayda geçirmeli.

## 6. Birleşme arayüzü (ürün bulan → Mağaza Kurucu → video)
```
ürün bulan plugin ──urun-paketi.json──▶ Mağaza Kurucu ──magaza-paketi.json──▶ video / AI video plugin'i
 (ad, niş, fotoğraflar, doğrulanmış      (marka, renk, tipografi aile+handle,      (altyazı ve kapak aynı aile ve renkle,
  özellik+kaynak, varyant, pazar,         onaylı metinler ve iddialar, G0 temiz     yalnız onaylı iddialar, UTM'li ürün linki)
  rakip, reklam kanıtı)                   ürün karesi, mağaza URL'leri + UTM)              │
                                    ◀──────────────video-paketi.json──────────────────────┘
                                     (pdp-galeri ve hero videoları kurulumda yüklenir; G0'ın yerini almaz)
```
- Alanlar ve kurallar: `src/ortak/arayuz-sozlesmesi.md`. Tek bağ dosyadır: ChatGPT'de sohbete eklenir, Claude'da yol olarak verilir; MCP ya da ortak veritabanı gerekmez.
- Sürümleme: `surum` alanı; alan eklenebilir, silinmez. Sözleşme değişikliği `platform-uyum-muhendisi` kontrol listesindedir.
- Video tarafı için kazanım: tipografi ailesi Google Fonts'ta da aynı adla var (Barlow Condensed, Inter), altyazı ve kapak mağazayla tek sistem olur; video yalnız `onayli_metinler.iddialar` listesini söyler.

## 7. Ne kaldı
1. **0.4.0 gerçek koşu:** ChatGPT Çalışma modunda bir ürünle uçtan uca (G0 yazısız mı geliyor, T10'da `type_heading_font` yazılıyor mu, Adım 8 site denetimi çalışıyor mu). Görsel üretimi kullanıcı onayı ister. Dağıtım zip'leri (`dist/`) yeniden üretilip yüklenmedi.
2. **Ürün gerçekliği deneyi:** G0/G1'de tedarikçinin gerçek fotoğrafını koruyan (yalnız zemin + ışık) üretim ile AI render'ı kör panoda karşılaştır; pilot ve kör deneme aynı açığı gösterdi.
3. **Kütüphane:** listenin 828 alan adı taranmadı; galeri verisi 175 markada (Shopify `products.json` hız sınırı, 158 marka). `kutuphane-bakimci` başka bir gün düşük hızla tamamlar. Niş başına n < 15 olan nişler için oran yazılmadı.
4. **Hız alan verisi yok:** PageSpeed/CrUX anahtarsız kota doluydu; sayılar laboratuvar. Bir API anahtarıyla 75. yüzdelik alan verisi eklenmeli.
5. **Galeri sınıflayıcı:** %53 isabet; yüz/beden algılayıcı indirilemedi. Oranlar gözle etiketli örneklemden; büyütmek için yeni etiket turu.
6. **Tema önerileri (onaysız dokunulmadı):** mobil ürün sayfasında galeri yüksekliği (≤ %60 ekran) ve hızlı ödeme düğmesinin renk çatışması tema ayarı/kodu gerektirebilir.
7. **Arayüz sözleşmesi** öbür plugin'lerde henüz uygulanmadı (ürün bulan tarafta `urun-paketi.json` üretimi, video tarafında `magaza-paketi.json` okuma).


## 0.4.1: gerçek koşudan üç ders

| Değişen | Neden (ölçülmüş) | Dosya |
|---|---|---|
| Ret durumunda dürüst yedek akış: boş kart (görsel aracından) + gerçek ürün fotoğrafı (yerleştirme) | Görsel aracı bazı ürün türlerini (ör. yetişkin wellness) ürün fotoğrafı ya da tarifiyle "cinsel içerik" diye reddetti; 3 dürüst yeniden ifade de ret. Hile ve başka araca geçiş yasak. Boş kart da 8 denemede 1 temiz geldi; ek vermeden istemek daha iyi geçti | `skills/gorseller/references/adim-5-gorsel-uretimi.md` "Ret durumunda", `istemler/bos-kart.md` |
| Arka plan = bölüm zemini: görsel zemin HEX'i bölüm zemin HEX'iyle birebir | Yakın tonda görselin kenarı sayfa kaydırılınca kutu gibi göründü | `adim-5`, `kabul-kontrolu.md` §3, `scripts/duzelt.py zemin` |
| Yazılı görselde yapay zekâ büyütme yok | Real-ESRGAN ince yazıyı içi boş çift çizgili harfe çevirdi | `adim-5`, `kabul-kontrolu.md` §3 |

Doğrulanmadı: `bos-kart.md` şablonu bu haliyle ChatGPT'de koşulmadı (istem sahadaki çalışan istemden genelleştirildi).
