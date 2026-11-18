# Üretim promptları: onaylı görsel tasarım dili (genel şablonlar)

Durum: ONAYLI (kullanıcı, 2026-11-16/17; sürüm 0.3.0). Kaynak: `tasarim-dili.md` (çekirdek), SESSA test5 galeri istemleri (v2/v3), test7 mobil banner istemleri. Slot koordinatları yaklaşık yerleşim tarifidir; kabulde px ölçülmez (`kabul-kontrolu.md`). SESSA'ya özgü değerler yer tutucuya çevrildi; SESSA değerleri her yer tutucunun yanında örnek olarak durur.

## 0. Kararlar (tek kural seti)
- **0.3.5 (önce bunu oku): `ortak-istem-bloklari.md`.** Önce yalnız G1 üretilir ve onaylatılır; sonraki her görsel Ek 1 ürün + Ek 2 onaylı G1 ile üretilir. Üç ortak blok (ÜRÜN KİLİDİ, SİSTEM, YASAKLAR) bir kez doldurulur, her isteme aynen eklenir. Başlık satır satır ve harf yüksekliği tuval yüzdesiyle verilir; varsayılan başlık tipografisi dar grotesk BÜYÜK HARF (TİPOGRAFİ D). Aşağıdaki şablonlarla çelişen yerde o dosya geçerlidir.
- **Galeri 8 kare (G1–G8), grafik ve yazılı.** G1 poster: somut fayda başlığı + en fazla 1 kısa alt satır (ürün satırı). G2–G8 yazılı grafik serbest. S1–S5 site görselleri yazısız.
- **Feed notu (bilgi):** Shopify kanalları ürünün 1. medyasını feed'e gönderir; G1 yazılıysa feed'e de yazılı gider. Yazısız ayrı feed görseli istenirse kullanıcıya sorulur.
- **Masaüstü banner metinli (0.3.5);** tipografi görselin içinde: etiket + dev başlık + alt metin + buton solda, ürün sağda. Sol yarısı boş "sakin alan" banner üretilmez (kullanıcı: "banner niye boş").
- **Mobil banner metinli;** tipografi görselin içinde tasarlanır (M2 düzeni).
- **Zemin hilesi ve kenar payı:** görsel zemini = konacağı yüzeyin zemini (aynı hex); ürün hiçbir kenara değmez, her kenarda en az %6 boş zemin. Yakın plan karede de ürün kadrajdan taşmaz.
- **Reddedilenler (üretme):** insanlı yaşam tarzı paneller; referansı 1-1 kopyalamak; AI süsleri (taş, traverten, mermer, bitki, leke, parlama); kodla çizilmiş görsel; kodla çizilmiş logo; çizgi ikonlu özellik kartı (G2).
- **Logo:** varsayılan yalnız ikon, yazısız, şeffaf PNG (`istemler/logo-ikon.md`; 1–2 şekil, 32 px'te okunur). Canlı metin logo yalnız kullanıcı isterse.
- **0.3.6 HAZIR İSTEM:** G1, G2, G3, G4, G5, B1, B2 ve logo için istem `istemler/` klasöründe hazırdır ve kelimesi kelimesine kullanılır; bu dosyadaki aynı kodlu şablonlar yalnız açıklamadır. G6–G8 ve S1–S5 için buradaki DÜZEN kullanılır, üç ortak blok `ortak-istem-bloklari.md` §2–4'ten aynen alınır.
- **0.3.4 kilitleri (`tasarim-dili.md` §9; metin kuralı `01-kurallar.md` Görsel metni):** 5 HEX + başlık yazı tipi tarifi DEVAM KARTI'nda yoksa prompt kurulmaz; lojistik/kampanya yazısı ("Ücretsiz kargo" vb.) hiçbir görselde yok; bütün galeri ve bannerlar TEK ve AYNI zemin HEX'inde (`{RENK_ZEMIN}`; açık ya da koyu olabilir, görselden görsele değişmez, bölünmüş zemin yok; üretimden sonra `duzelt.py zemin` ile sabitlenir; farklı zemin RED); süs çizgisi, numara etiketi ("DETAY 01"), "detay" kelimesi, büyüteç dairesi yok; ürün kadrajın ≥ %55'i; her üretimden sonra Ref 1 ile renk/biçim karşılaştırması.
- **Tek görsel = tek prompt = tek mesaj.** Çoklu istekte kolaj, yanlış oran ve ürün kayması ölçüldü. Her görsel orijinal ürün fotoğrafından üretilir.

## 1. Yer tutucular
Plan (Adım 4) onaylanınca bir kez doldur; bütün promptlarda aynı değer kullanılır (tek şablon sistemi).

| Yer tutucu | Ne | SESSA örneği |
|---|---|---|
| `{MARKA}` | Ambalajdaki marka adı (yalnız ambalajda görünür) | SESSA |
| `{URUN_ADI}` | Ürünün kısa adı | ağız bandı |
| `{AMBALAJ_TARIFI}` | Ref 1'den okunan ambalaj: malzeme, renk (≈hex), biçim, ön yüz baskısı birebir | mat kraft, kum-bej (≈#CBB5A0) kilitli poşet; üstte yatay kilit şeridi; ön yüzde lacivert ince serif 'SESSA', altında 'Ağız Bandı · 30 gece', altında ince pas çizgi |
| `{URUN_TARIFI}` | Ürünün kendisi: biçim, oran, parça sayısı, ayırt edici detay | bej (≈#CEB498) dokuma bant; iki ucu yarım daire uzun oval; en/boy 1,9 (7,5 × 4 cm), 2,2'den uzun değil; ortada uzun eksene paralel, bant boyunun %16'sı kadar yarık |
| `{DOKU_TARIFI}` | Yakın planda görünen yüzey | ince pamuk tela, düzenli bez ayağı örgü, kısa kenarda 60–80 iplik; çuval bezi gibi kaba değil |
| `{DURUS_KURALI}` | Ürünün zeminde nasıl durduğu, en sık bozulan hâli | kâğıt inceliğinde; zemine yapışık düz yatar, kenar kalınlığı görünmez; asla dik durmaz, hiçbir şeye yaslanmaz |
| `{URUN_YASAK}` | Modelin ürüne yaptığı tipik bozulma | dik duran, kalın kenarlı, köpük ya da karton görünümlü bant; labirent, yazı ya da hiyeroglif benzeri doku |
| `{SADAKAT_LISTESI}` | Adım 4.1'deki 5–10 madde | — |
| `{REF_DIZILIM}` | Ref 1'deki dizilim (kopyalanmaz) | dik poşet + arkada şeffaf taşıyıcı + önde gevşek bant |
| `{RENK_ZEMIN}` | Görsel zemini (DEVAM KARTI "görsel zemini"; açık ya da koyu, ürünle güçlü kontrast); G1–G8, B1 ve B2'de TEK ve AYNI HEX; S görsellerinde konacağı bölümün zemini | #F2EEE8 |
| `{RENK_METIN}` | Metin + koyu panel, tek değer (marka "metin") | #14304F |
| `{RENK_KOYU_YASAK}` | Metin renginin modelin kaydığı daha koyu hâli | #0A2540 ve daha koyusu (siyaha yakın lacivert) |
| `{RENK_KART}` / `{RENK_KART_KENAR}` | Açık kart (marka "ikincil") / 2 px kenar | #FAF8F5 / #E3DCD2 |
| `{RENK_IKINCIL_ACIK}` / `{RENK_IKINCIL_KOYU}` | İkincil metin: açık zeminde / koyu zeminde (≥ 4,5:1) | #5B6B7D / #B9C3CF |
| `{RENK_AYIRICI}` | Tablo çizgisi (metin renginin %20'si) | #C6C8C9 |
| `{RENK_VURGU}` + `{VURGU_ADI}` | Tek doygun aksan (marka "vurgu"); görselde tam 1 öğe | #B5533C, pas |
| `{TIPO}` | Varsayılan D (dar grotesk BÜYÜK HARF, §4); A serif ya da B tek grotesk yalnız kullanıcı isterse | D |
| `{EK_STIL}` | Bu mağazanın onaylı G1'i (G1 dışındaki bütün görsellerde Ek 2); G1'in kendisinde §3a paket stil çapası | `stil-capasi/g1-poster.jpg` |

Renk türetme: metin = ambalajın en koyu baskı rengi; zemin = ürünle güçlü kontrastlı tek HEX, açık ya da koyu (açık/pastel ürün açık pastel zemine konmaz; koyu zemin seçilir); metin ve vurgu ürünün renginden OLMAZ; kart = zeminden 2–8 RGB açık; vurgu = ambalajdaki tek doygun aksan. Kontrastları Python ile ölç (metin ≥ 4,5:1; ürün–zemin ≥ 1,5:1; vurgu koyu zemine konmaz). Marka skill'inin 5 HEX'i: arka plan → `{RENK_ZEMIN}`, metin → `{RENK_METIN}`, ikincil → `{RENK_KART}`, vurgu → `{RENK_VURGU}`; "ana" (buton) rengi görselde yalnız mobil banner butonunda, metin renginden farklıysa.

## 2. Niş anahtarı
0.3.5: `{TIPO}` sütunu yalnız kullanıcı serif/tek grotesk isterse geçerlidir; varsayılan her nişte D (dar grotesk BÜYÜK HARF). Zemin açık ya da koyu tek HEX. "G2 ikon ızgarası" geçen yerde makro fotoğraf kartları kullanılır.
| Niş | `{TIPO}` | Zemin | Galeri sırası → şablon |
|---|---|---|---|
| Sağlık | A | `{RENK_ZEMIN}` (tek HEX) | G1 poster → G2 makro kartlar → G3 nasıl çalışır → G4 dev sayı → G5 kullanım → G6 kutu + ölçü → G7 karşılaştırma → G8 zaman çizelgesi |
| Güzellik | A (krem/sıcak) · B (cihaz, klinik-beyaz) | `{RENK_ZEMIN}` (tek HEX) | G1 → G4 düzeni fayda kartı (ürün büyük ve sağda, kenara değmez; sol kolonda 3–4 madde) → G3 mekanizma/içerik → G4 kanıt (yalnız yazılı raporla; yoksa sayısız doku makrosu) → G5 → G6 boy/süre ya da kutu → G7 ya da G2 "kimin için" → G8 rutin. Önce/sonra ÜRETİLMEZ |
| Gadget | B | `{RENK_ZEMIN}` (tek HEX) | G1 → G3 tek mekanizma (başlık 2–4 kelime) → G2 ikon ızgarası ya da G3 işaret çizgileri → G4 sayı + kaynak notu (yalnız gerçek kaynak; yoksa ölçü) → G6 ölçü/kapasite → G7 sınıfa karşı → G6 düzeni kutu içeriği → G5 kullanım. İnsansız; ölçek yazısız bir nesneyle |
| Ev | B (serif yalnız tek vurgu) | `{RENK_ZEMIN}` (tek HEX; beyaz ya da açık gri) | G1 packshot + yazısız ölçek nesnesi → G8 düzeni vaat + 3–4 fayda (bölünmüş) → G3 mekanizma → G7 → G4 ölçü/varyant → G5 düzeni temizlik/bakım (ZORUNLU) → G2 kullanım alanları → G6 kutu |
| Moda | B (dar büyük harf serbest) | Tek açık gri #F1F1F1–#F8F8F8 | Önce alt tip. Bedenli giyim model ister: kullanıcıya tek satırla sor. Yazı yalnız işlev iddiasında (kapasite, kumaş, malzeme); estetik üründe kare yazısız packshot/makro |

Takviyede karşılaştırma karesi yerine G6 önerilir (Bilgi notu, `tasarim-dili.md` §8).

## 3. Birleştirme sırası (her prompt, 12 blok, eksiksiz)
ROL → ÜRÜN KİLİDİ → STİL ÇAPASI → RENK (+ slot eki) → TİPOGRAFİ (A ya da B) → IZGARA → SLOT DÜZENİ → AÇI → METİNLER → YASAKLAR → ÇIKTI → DÜZELTME.
Bir blok eksikse gönderme. Yön/stil adı, bölüm adı, hex ve px görsele yazılmaz (YASAKLAR'da). Ekler: Ek 1 = ürün fotoğrafı (her zaman, orijinal). Ek 2–3 = `{EK_STIL}`; mağazada henüz onaylı görsel yoksa §3a'daki paket stil çapası. Web'den bulunan görsel ek olarak konmaz.

### 3a. Paket stil çapası (`assets/stil-capasi/`)
Kullanıcının onayladığı test12 kareleri (koyu petrol zemin, makas). **Çapadan yalnız tipografi hiyerarşisi (dev dar başlık, küçük etiket, gövde oranı) ve boşluk ritmi alınır; rengi ve ürünü ALMA: renk DEVAM KARTI'ndan, ürün Ek 1'den.** Çapadaki zemin rengi, makas, metinler ve düzen kopyalanmaz.

| Dosya | Ne zaman |
|---|---|
| `g1-poster.jpg` | G1'de Ek 2 (mağazanın ilk karesi) |
| `g2-makro-kartlar.jpg` | G2'de Ek 3 (kart düzeni: üstte makro fotoğraf, altta etiket) |
| `g3-isaret-cizgileri.jpg` | G3'te Ek 3 |
| `b1-masaustu.jpg` | B1'de Ek 3 |
| `b2-mobil.jpg` | B2'de Ek 3 |

G1 onaylandıktan sonra bütün görsellerde Ek 2 = onaylı G1'dir (`ortak-istem-bloklari.md` §1); paket çapası en çok Ek 3 olur. Skill dosyası görsel aracına ek olarak geçmiyorsa STİL ÇAPASI bloğunun "ek yok" cümlesi kullanılır.

## 4. Ortak bloklar

**ROL.** `Sen üst düzey bir DTC marka ajansında sanat yönetmenisin. YALNIZ 1 görsel üret: kolaj, ızgara, yan yana varyasyon ya da mockup çerçevesi değil. Ekler: Ek 1 = ürün fotoğrafı[, Ek 2–3 = bu mağazanın onaylı görselleri].`

**ÜRÜN KİLİDİ.** `Ek 1 ürünün TEK doğru kaynağıdır; ürünü birebir koru. Ambalaj: {AMBALAJ_TARIFI}. Ürün: {URUN_TARIFI}. {DURUS_KURALI}. Doku: {DOKU_TARIFI}; yakın planda tek tek seçilir; yüzeyde yazıya, labirente ya da karalamaya benzeyen desen YOK. Korunacaklar: {SADAKAT_LISTESI}. Ambalajı yeniden tasarlama, rengini değiştirme, üstüne yazı ekleme ya da çıkarma. Ek 1'deki DİZİLİMİ ({REF_DIZILIM}), KAMERA AÇISINI, KADRAJI ve GÖLGE YÖNÜNÜ KOPYALAMA; bu görselin dizilimi aşağıdaki AÇI satırıdır.` Ürünsüz karede (G7) sona ekle: `Bu görselde ürün fotoğrafı YOK; ikonlar ürünün geometrisinden çizilir.`

**STİL ÇAPASI.** G1'de (Ek 2 = paket çapası): `Ek 2 başka bir markanın onaylı karesidir. Ondan YALNIZ tipografi hiyerarşisini (dev dar başlık, küçük etiket, gövde oranı) ve boşluk ritmini al. Rengini, zeminini, ürününü, metinlerini, düzenini ve açısını ALMA; renkler aşağıdaki RENK bloğundan, ürün Ek 1'den.` Diğer görsellerde (Ek 2 = onaylı G1): `Ek 2 = aynı markanın onaylı galeri karesi: ondan YALNIZ yazı tipi sistemini, renkleri, boşluk ritmini ve kalite seviyesini al; düzenini, metinlerini ve ürünün açısını KOPYALAMA.` Ek yoksa: `Seviye: üst düzey marka ajansı galeri karesi; grafik, insansız, ürün odaklı; başlık büyük ve kendinden emin.`

**RENK.** `RENK (yalnız bunlar): Zemin {RENK_ZEMIN}, düz ve kesintisiz; görselin konacağı yüzeyle aynı renk; bu mağazanın bütün galeri ve banner görsellerinde birebir aynı HEX. Metin rengi tek değer {RENK_METIN}: harflerin içi tam bu ton; {RENK_KOYU_YASAK} YOK. Açık zeminde ikincil metin {RENK_IKINCIL_ACIK}; koyu zeminde {RENK_IKINCIL_KOYU}. Açık kart {RENK_KART}, kenar 2 px {RENK_KART_KENAR}, gölgesiz. {VURGU_ADI} {RENK_VURGU} yalnız tek bir öğede; koyu zemine konmaz. Kart ve panel yüzeyleri düz: köşeden köşeye renk farkı yok; renkten renge degrade, vinyet, radyal parlama yok.` Slot eki: hangi metin hangi tonda + `{VURGU_ADI} öğesi: YALNIZ <slotta yazan öğe> (ambalajın kendi baskısı sayılmaz).`

**TİPOGRAFİ D (varsayılan, 0.3.5; her niş).** `Başlıklar DAR (condensed) grotesk, BÜYÜK HARF, SemiBold; Barlow Condensed / Oswald ailesine benzer uzun-dar harfler; harf aralığı sıkı, satır aralığı 0,95; başlık büyük ve kendinden emin, tasarımın ana öğesi. Gövde ve açıklamalar: sade grotesk (Inter benzeri) Regular, cümle düzeni. Küçük etiketler: aynı grotesk Medium, BÜYÜK HARF, harf aralığı geniş (+%12). Başka yazı tipi YOK; serif YOK; italik YOK; el yazısı YOK. Bütün metinler tek sol hatta hizalı. Türkçe harfler birebir doğru: İ, ı, ğ, ş, ç, ö, ü (büyük harfte i → İ, ı → I). Yazım hatası olan görsel REDdedilir.` D'de vurgu kelimesi italik yapılmaz; vurgu tek küçük öğedir. A ve B yalnız kullanıcı açıkça isterse.

**TİPOGRAFİ A (sağlık, sıcak güzellik).** `Ölçüler büyük harf yüksekliğidir (cap), yanında yaklaşık font boyu. Başlık ve kart/etiket başlıkları: DAR, uzun oranlı, yüksek kontrastlı serif, Regular 400 (Instrument Serif / GT Super Display / Editorial New benzeri); dikey sap kalınlığı cap'in en fazla %11'i; Medium, SemiBold, Bold, Black ve kalın kama serif YASAK; harf aralığı −%1, satır aralığı 1,0–1,05. Vurgu kelimesi aynı serifin italiği 400; görselde tek. Diğer her yazı tek grotesk (Inter benzeri): gövde 400, etiket ve eyebrow 500. Başka font YOK.`

**TİPOGRAFİ B (gadget, ev, moda, cihaz güzellik).** `Ölçüler cap'tir. Bütün yazı tek grotesk aile (Inter / Figtree / Söhne benzeri): başlık en fazla SemiBold 600 (700 ve üstü YASAK), kart/etiket başlığı 500, gövde 400, eyebrow 500. İtalik YOK; vurgu yalnız tek {VURGU_ADI} öğesiyle. Serif yalnız ambalajın kendi logosunda yaşar. Başka font YOK.` (Moda: başlıkta dar büyük harf varyantı serbest.)

İki tipografiye de eklenir: `Metin düz vektör gibi temiz: doku, kabartma, baskı izi, hale YOK. Türkçe harfler (ı, İ, ş, ğ, ü, ö, ç) birebir; büyük harfte i → İ, ı → I. BOY: başlık harf yüksekliği G1 ve bannerlarda tuvalin %9–11'i, bilgi karelerinde %6–8; başlık satır satır verilir. Küçük metin boyları üst sınırdır: alt başlık cap 34; kart/etiket başlığı cap 48; kart gövdesi ve ikon etiketi cap 30; meta, ürün satırı ve eyebrow cap 26 (en küçük metin 26). Eyebrow: BÜYÜK HARF, harf aralığı +%10, grotesk 500, ikincil tonda; serif DEĞİL, koyu DEĞİL, kalın DEĞİL; başlığın 24 px üstünde, aynı sol hatta; hap ya da kutu içinde DEĞİL. Başlık 2–4 kısa satır, yetim kelime yok; her satır METİNLER'de ayrı tırnakla, '/' ile verilir.`

**IZGARA (kare 1254×1254).** `DIŞ ÇERÇEVE BOŞ: dört kenardan tuvalin en az %6'sı boş zemindir; hiçbir yazı, kart, tablo, çizgi, ikon ya da ürün bu çerçeveye girmez; metin ve kartlar x 88–1166, y 88–1166 içinde. Ürün hiçbir kenara değmez ve kadrajdan taşmaz; yakın planda bile ürünün çevresinde zemin görünür. Ürün BÜYÜK: ürünün ana öğe olduğu karede ürün (grubu) tuvalin en az bir ekseninde %55'ini kaplar; kadrajın yarısı boş zemin kalmaz. İnce/uzun ürün çapraz konmaz: dike yakın (dikeyden 8–12° eğik), boyu tuval yüksekliğinin %80'i; yatay bannerda yataydan 10°. En az bir değer ayrıntısı (doku, dikiş, mekanizma, malzeme) net. 12 kolon (68 px, oluk 24 px). Bütün metin satırları aynı sol hatta (±2 px). Metin ile ürün arası en az 50 px; metin ürünün üstüne binmez. Çizgiler 2 px. 3×3 bölmede boş hücre yok. Işık tek kaynak, sağ üstten; gölge sola ve aşağı, opaklık %15–25, tabandan en fazla %8.`

**YASAKLAR.** `insan, el, yüz, dudak, yatak sahnesi; taş/kaide, kuru çiçek, bitki, yaprak, organik leke şekli, kumaş drape, bokeh, ışık hüzmesi, parlama, yansıma havuzu, mermer, traverten, ahşap masa, zemin–duvar çizgisi; renkten renge degrade, vinyet, radyal parlama, sistem dışı renk, {RENK_KOYU_YASAK}; 3D, emoji ya da dolu siluet ikon; ok, dalga, rüzgâr, ışıma, hareket ve parıltı çizgisi; hap içine alınmış etiket, rozet, mühür, yıldız puan, yüzde, 'klinik', hekim, basın logosu; kargo, teslimat, iade, garanti, indirim, kampanya ya da fiyat yazısı ('Ücretsiz kargo', 'Kapıda ödeme', '%20 indirim' vb.); süs çizgisi, başlık altı renkli çizgi, numara ya da sıra etiketi ('DETAY 01', '01/08'), 'detay' kelimesi, büyüteç dairesi, yakınlaştırma balonu; {RENK_ZEMIN} dışında zemin rengi; {URUN_YASAK}; kart ya da satır içinde dikey ayraç çizgisi; kenara %6'dan yakın ya da kadrajdan taşan her öğe (ürün dahil); METİNLER bölümünde olmayan HER yazı. Bu prompttaki ölçüleri, renk kodlarını, bölüm adlarını ya da herhangi bir stil/yön adını görsele YAZMA. Ambalajın kendi baskısı dışında '{MARKA}' yazma.`

**ÇIKTI (kare).** `Tek görsel, kare 1:1, 1254×1254 px. Kolaj, çerçeve, dış beyaz pay, filigran yok.`

**DÜZELTME (her promptta, en sonda).**
```
DÜZELTME (geçmiş turlarda en sık bozulanlar; KESİN uygula):
- Doku: {DOKU_TARIFI}; ince, düzenli, sık. Labirent, yazı ya da hiyeroglif benzeri desen YOK. Kalınlık gerçek ürün kadar; karton ya da köpük kalınlığı YOK. Oran {URUN_TARIFI}'ndeki gibi.
- Duruş: {DURUS_KURALI}. Yassı ürün asla dik durmaz; zemine düz yatar, kamera yukarıdan 30–60° (ya da 90° kuşbakışı) bakar; ambalajın önüne değil yanına konur.
- Metin rengi tam {RENK_METIN} (daha koyuya kaçmasın); ikincil metin {RENK_IKINCIL_ACIK}.
- Kenar boşluğu: her kenarda tuvalin en az %6'sı boş zemin; ürün dahil hiçbir öğe bu çerçeveye girmez, ürün kenarda kesilmez.
- Ürün rengi ve biçimi Ek 1 ile aynı: renk kaydırma, 'güzelleştirme' YOK. Ürün büyük (tuvalin en az bir ekseninde %55), çapraz değil.
- Zemin tam {RENK_ZEMIN}; başka zemin rengi YOK.
- Süs çizgisi, numara etiketi ('DETAY 01'), 'detay' kelimesi, büyüteç dairesi YOK; {VURGU_ADI} yalnız tek öğede. Kargo/iade/garanti/indirim yazısı YOK.
```
Yeniden üretimde altına ekle: `- Bu görselin önceki denemesi şu yüzden reddedildi: <kabul kontrolündeki kritik madde>; bunu KESİN düzelt.`

## 5. Banner şablonları

### B1 Masaüstü banner (metinli, 0.3.5; tipografi görselin içinde)
- RENK: `Zemin düz {RENK_ZEMIN} (galeriyle aynı HEX); her köşede aynı; aydınlanma, hale YOK. {VURGU_ADI} YALNIZ küçük etiketin solundaki küçük dolu kare nokta.`
- DÜZEN: `Web sitesi ana sayfa MASAÜSTÜ BANNER; çok geniş yatay, oran 12:5. Sol %45 metin bloğu, sol hizalı, dikeyde ortalı: küçük etiket; altında dev başlık 2 satır (harf yüksekliği tuval yüksekliğinin %10–12'si); altında tek satır alt metin (ikincil renk); altında buton (dolu, köşeleri hafif yuvarlak dikdörtgen; yazısı dar grotesk BÜYÜK HARF SemiBold). Sağ %55: ürün BÜYÜK; ince/uzun ürün yataya yakın (yataydan 10° eğik, boyu tuval genişliğinin %50'si), diğer ürün dik ve tuval yüksekliğinin %75'i. Ürün metne, butona ve kenarlara değmez. Boş, sönük alan kalmaz.`
- METİNLER: `Küçük etiket: "{ETIKET}"` · `Başlık (2 satır): "{SATIR_1}" / "{SATIR_2}"` · `Alt metin: "{ALT_METIN}"` (doğrulanmış özellik) · `Buton: "{BUTON}"`. Kargo/iade/garanti DEĞİL.
- ÇIKTI: `Tek görsel, yatay 12:5 (ör. 1942×809). Üstte ve altta bant, dış çerçeve YOK; zemin tuvalin tamamını doldurur.` Teslimde 1920×800'e kırp.
- Kurulum notu: görselde yazı vardır; `e-hero-b` H1'i görseldeki başlıkla çelişmez.

### B2 Mobil banner (tipografi görselin içinde)
- ROL'e ekle: `Mobil ana sayfa BANNER'ı tasarla, dikey 4:5. Bu bir TASARIM: tipografi görselin içinde ve tasarımın parçası; yazıyı görselin altına ayrı bloğa alma. Ek 2–3'ün tipografi ve renk sistemini al (kopyalama değil, aynı sistem).`
- ÜRÜN KİLİDİ'ne ekle: `Ürün büyük ve kendinden emin; gerçekçi stüdyo gölgesi; hiçbir kenara değmez. Küçük ürün + boş zemin YASAK.`
- TİPOGRAFİ (yerine): `Küçük etiket = aralıklı büyük harf grotesk; başlık = {TIPO} başlık fontu, dev, 2–3 satır (harf yüksekliği tuvalin %8–9'u) ({TIPO}=A ise "{VURGU_KELIME}" italik); alt metin = temiz grotesk; buton = hap biçimli düz buton (hap yalnız butonda); en altta küçük ürün satırı. Sol hizalı, kenarlardan tuval genişliğinin %8'i boş, düzenli ritim. Boş, sönük alan yok; dengeli dolu.`
- METİNLER: `Etiket: "{ETIKET}"` (ürün adı · miktar, büyük harf) · `Başlık: "{BASLIK}"` (≤ 6 kelime) · `Alt metin: "{ALT_METIN}"` (≤ 8 kelime, doğrulanmış özellik) · `Buton: "{BUTON}"` · `Ürün satırı: "{URUN_SATIRI}"` (yalnız doğrulanmış ürün gerçeği; kargo/iade/garanti DEĞİL; yoksa basılmaz). SESSA: "AĞIZ BANDI · 30 GECE" / "Sessiz geceler başlasın." / "Nefes alan dokuma kumaş, ortada hava aralığı." / "Hemen al" / "30 bant · kilitli poşet".
- RENK eki: `{VURGU_ADI} yalnız başlıktaki vurgu kelimesi; süs çizgisi YOK.`
- SLOT DÜZENİ (0.3.4: yalnız M2 kullanılır; M1 ve M3 koyu zemin kullandığı için KAPALI, tek zemin HEX'i kuralı):
  - **M1 tam koyu zemin (KAPALI):** `Düz {RENK_METIN} zemin. Üst %42 metin bloğu (etiket ve alt metin {RENK_IKINCIL_KOYU}, başlık {RENK_KART}, buton {RENK_KART} zeminli {RENK_METIN} yazılı, ürün satırı); alt %58 ürün büyük: ambalaj ortada-sağda, 2 ürün önünde zemine yatık.` (Vurgu kelimesi koyu zeminde yalnız kontrastı ≥ 4,5:1 ise vurgu renginde; değilse M1'de vurgu öğesi yok.)
  - **M2 tek zemin:** `Düz {RENK_ZEMIN} zemin. Üst %45 metin bloğu ({RENK_METIN} başlık, buton {RENK_METIN} zeminli {RENK_KART} yazılı); alt %58 ürün büyük, yumuşak stüdyo ışığı ve gölge.`
  - **M3 bölünmüş zemin (KAPALI):** `Üst %50 {RENK_ZEMIN} (metin bloğu burada, {RENK_METIN} yazılar), alt %50 düz {RENK_METIN} panel; ambalaj iki rengin sınırına oturur (üst kenarı açık bölgeye taşar), 2 ürün koyu panelde önde yatık. Ürün satırı koyu panelin en altında, {RENK_KART} renginde.`
- AÇI: masaüstünden farklı olmak zorunda. `Kamera 35° yukarıdan; ambalaj 15° sağa dönük; ürünler zemine düz yatık, birbirine binmez, ambalaja en az 40 px uzak.`
- ÇIKTI: `Tek görsel, dikey 4:5 (yaklaşık 1122×1402 px).` Teslimde 1080×1350'ye ölçekle/kırp. Masaüstünün kırpılmışı olmaz.
- Kurulum notu: bu görselde yazı vardır; tema hero'sunun canlı metni mobilde ikinci kez basılmamalı (`shopify-kurulum` aşamasında kontrol et).

## 6. Galeri şablonları (kare 1254×1254)
Her slotta yalnız farklı bloklar yazılı; geri kalanı §4. Açılar galeri içinde çakışmaz; plan tablosundaki "Poz/açı" sütunu bu AÇI satırlarından gelir. Metin limitleri: başlık ≤ 5 kelime, alt başlık ≤ 12, kart gövdesi ≤ 6, görsel toplamı ≤ 40 kelime; kart başlığı ≤ 14 karakter. Bilgi karelerinde (G2–G8) eyebrow zorunlu.

### G1 Ana görsel (asimetrik afiş; ÖNCE bu üretilir ve onaylatılır)
- DÜZEN: `Kare 1:1, e-ticaret ürün galerisi AFİŞ karesi. Asimetrik. SOL %58: dev başlık, 2–4 satır, alt alta, sol hizalı; başlık bloğu tuval yüksekliğinin yaklaşık yarısını kaplar (her satırın harf yüksekliği tuvalin yaklaşık %10'u). Altında 1–2 satırlık açıklama (ikincil renk). Sol altta tek satır teknik bilgi (küçük etiket stili, ikincil renk, aralarında orta nokta). SAĞ %42: ürün BÜYÜK; ince/uzun ürün neredeyse dik (dikeyden 8–12° eğik, boyu tuval yüksekliğinin %80'i, kamera kuşbakışı); diğer ürün tuval yüksekliğinin %70'i. Ürün başlığa ve kenara değmez. Boş, sönük alan kalmaz; yazı bloğu ile ürün aynı ağırlıkta.`
- RENK eki: `{VURGU_ADI} öğesi: YALNIZ tek küçük öğe (ör. teknik satırdaki bir nokta).`
- METİNLER: `Başlık (N satır): "{SATIR_1}" / "{SATIR_2}" / …` (somut fayda = alıcının sonucu, 2–5 kelime; soyut sıfat yığını değil) · `Açıklama: "{ACIKLAMA}"` (≤ 12 kelime) · `Teknik satır: "{URUN_SATIRI}"` (≤ 3 madde, yalnız doğrulanmış ürün gerçeği: ölçü, malzeme, içerik; kargo/iade/garanti DEĞİL; doğrulanmadıysa basılmaz). Örnek: "YUVARLAK" / "HATLARA" / "YUMUŞAK" / "BİTİŞ." · "7,25 İNÇ  ·  JP440C ÇELİK  ·  AYARLANABİLİR VİDA".

### G2 Ürün özellikleri: makro fotoğraf kartları (0.3.5; çizgi ikon KULLANILMAZ)
Kullanıcı: "ikonlar kötü". Kartlarda ikon yerine ürünün ilgili parçasının gerçek makro fotoğrafı durur. Örnek: `assets/stil-capasi/g2-makro-kartlar.jpg`.
- DÜZEN: `Kare 1:1, ÖZELLİK KARTLARI karesi. Üstte sol hizalı başlık, 2 satır, büyük. Altında 3 sütun × 2 satır = 6 eşit kart; kart yüzeyi zeminden bir ton açık (koyu zeminde zeminin bir ton açığı, açık zeminde {RENK_KART}), köşeleri hafif yuvarlak, gölgesiz, aralarında eşit dar boşluk; ızgara başlıkla aynı sol hatta. Her kartın üst %60'ında İKON YOK; onun yerine BU ürünün ilgili parçasının gerçek, keskin, stüdyo MAKRO FOTOĞRAFI (Ek 1'deki ürünün aynısı, aynı renk ve kaplama), kartın içinde ortalı: 1) {PARCA_1 yakın planı}; 2) {PARCA_2}; 3) {PARCA_3}; 4) {PARCA_4}; 5) {PARCA_5}; 6) {PARCA_6}. Kartın alt kısmında etiket (başlık fontu, BÜYÜK HARF) ve altında tek satır açıklama (gövde fontu, ikincil renk). {VURGU_ADI} YALNIZ bir kartın etiketinde.`
- Kart 1 ürünün tamamı olabilir (ölçü kartı); diğer 5 kart ÜRÜN KİLİDİ'ndeki parçaların yakın planıdır. Çizgi ikon, piktogram, illüstrasyon YOK. Bu karede ÜRÜN KİLİDİ bloğu aynen kalır (ürünsüz kare değildir).
- METİNLER: başlık 2 satır ("ALTI AYRINTI," / "TEK MAKAS."), 6 × `Kart n: "{ETIKET}" — "{ACIKLAMA}"` (etiket ≤ 14 karakter, açıklama ≤ 5 kelime; yalnız doğrulanmış özellik).

### G3 Nasıl çalışır (işaret çizgileri)
- RENK eki: `Başlık ve etiket başlıkları {RENK_METIN}; eyebrow ve etiket gövdeleri {RENK_IKINCIL_ACIK}; işaret çizgileri 2 px {RENK_METIN}. {VURGU_ADI} öğesi: YALNIZ "{ETIKET_A}" çizgisinin ürün üzerindeki 14 px dolu uç noktası.`
- SLOT DÜZENİ: `1) Eyebrow x=88, cap üst y=112. 2) Başlık x=88, cap y 162–238. 3) Tek ürün, ambalajsız, merkez (627, 700), görünen genişlik 760 px; sol ve sağ kenardan en az 240 px uzak. 4) Üç etiket (etiket başlığı + 20 px altında tek satır gövde): a ortalı x 627, cap üst y=318; b sol hizalı x=247, cap üst y=990; c sağ hizalı, satır sonu x=1007, cap üst y=990. 5) İşaret çizgileri 2 px, yalnız dikey, kırılımsız; parçadaki ucunda 12 px nokta; etiketten 16 px önce biter; kesişmez.`
- AÇI: `Kamera 35° yukarıdan; ürünün uzun ekseni yatayla 8° saat yönünde; ürün zemine düz yatar; işaretlenen 3 detay net. Işık sağ üstten, sola kısa temas gölgesi %15–20.`
- METİNLER: eyebrow ("NASIL ÇALIŞIR"), başlık ("Bandın yapısı.", vurgu "yapısı"), 3 etiket "ad / tek satır gövde" (SESSA: "Orta yarık / Hava için dar açıklık.").

### G4 Dev sayı (makro)
- RENK eki: `Sayı ve birim {RENK_METIN}; eyebrow ve açıklama {RENK_IKINCIL_ACIK}. {VURGU_ADI} öğesi: YALNIZ birim kelimesi.`
- SLOT DÜZENİ: `Sol kolon x 88–600; bütün sol öğelerin sol kenarı tam x=88. 1) Eyebrow cap üst y=362. 2) Sayı: rakam üstü y=412, tabanı y=712 (cap 300). 3) Birim kelimesi cap üst y=744 (genişliği sayının en fazla yarısı). 4) Açıklama tek satır, cap üst y=850, ≤ 22 karakter. Sağ: ürünün makro yakın planı x 640'tan başlar, y 380–900; sol blokla arası ≥ 50 px.`
- AÇI: `Makro: kamera 30° yukarıdan, çok yakın; ürünün uzun ekseni yatayla 12° (sağ ucu aşağıda). Ayırt edici detay kadrajda; ürün büyük ve yakın ama sağ, üst ve alt kenara değmez (çevresinde en az %6 zemin). Doku tek tek seçilir.`
- METİNLER: eyebrow ("PAKET"), sayı ("30"), birim ("gece"), açıklama ("Poşette 30 ayrı bant."). Sayı yalnız etiketten/ölçüden doğrulanabilir (uydurma veri yok); yoksa ölçü yaz.

### G5 Kullanım adımları (insansız, 3 satır kart)
- RENK eki: `Satır kartları {RENK_KART} + 2 px {RENK_KART_KENAR}. Başlık, adım numaraları ve adım adları {RENK_METIN}; eyebrow ve açıklamalar {RENK_IKINCIL_ACIK}. {VURGU_ADI} öğesi: YALNIZ başlıktaki vurgu kelimesi.`
- SLOT DÜZENİ: `1) Eyebrow x=88, cap üst y=112. 2) Başlık x=88, cap y 162–238. 3) Üç kart TAM x 88–1166, 260 px yüksek, köşe 24 px, iç boşluk 42 px: y 314–574, 598–858, 882–1142; aralık 24 px. 4) Kartta soldan sağa: adım numarası (x=130, cap 76), ürün durumu görseli (x 240–560, ≤ 180 px, dikey ortalı), metin bloğu (x=620'den: adım adı ≤ 12 karakter + 20 px altında açıklama ≤ 22 karakter). Kartta dikey ayraç çizgisi YOK.`
- AÇI: `Her satır farklı durum ve açı; üçü birbirine benzemez. Örnek: 1) ürün koruma kâğıdının/kutusunun üstünde, 45°; 2) ürün tek başına tam önden 0°; 3) ürün 60° yukarıdan, bir ucu 25° kalkık. İnsan, el, yüz YOK.`
- METİNLER: eyebrow ("KULLANIM"), başlık ("Üç adımda hazır.", vurgu "adımda"), 3 × (numara · ad · açıklama). Ev nişinde aynı düzen "temizlik/bakım" karesidir.

### G6 Kutu içeriği + ölçü (kuşbakışı)
- RENK eki: `Başlık, ölçü çizgileri ve değerleri {RENK_METIN}; eyebrow ve alt liste {RENK_IKINCIL_ACIK}. {VURGU_ADI} öğesi: YALNIZ başlıktaki vurgu kelimesi.`
- SLOT DÜZENİ: `1) Eyebrow ve başlık üst solda (y 112 / 162–238). 2) Ambalaj solda x 88–508, y 380–900, sol kenarı tam x=88. 3) Ön ürün x 600–1020, y 420–644, oranı ürünün gerçek oranı TAM; uzun ekseni yatay. 4) İki ürün daha altında y 700–940, 24 px aşağı ve 16 px sağa kaydırılmış yelpaze, zemine yapışık. 5) Ölçü çizgileri yalnız ön üründe: yatay y=388, x 600–1020; dikey x=1052, y 420–644; 2 px, uçlarda 16 px dik kısa çizgi, ok başı YOK; değer çizgiden 16 px uzakta; dikey değer x 1068–1152 içinde. Çizgilerin uçları ürünün uçlarıyla TAM hizalı. 6) Alt liste x=88, cap üst y=1060, tek satır, '·' ayraçlı.`
- AÇI: `Tam kuşbakışı (90°, düz flat lay). Ambalaj sırtüstü yatık, ön yüzü yukarıda ve okunur, saat yönünün tersine 6° dönük. Işık sağ üstten; her nesnenin sola kısa gölgesi %15–20.`
- METİNLER: eyebrow ("KUTU İÇERİĞİ"), başlık ("Poşetin içinde.", vurgu "içinde"), ölçü değerleri Türkçe ondalık virgülüyle ("7,5 cm", "4 cm"), alt liste ("30 ağız bandı · 1 kilitli poşet"). Ölçüler ürün etiketinden ya da ölçümden.

### G7 Karşılaştırma (sınıfa karşı tablo)
- RENK eki: `Tablo kartı {RENK_KART} + 2 px {RENK_KART_KENAR}, gölgesiz; satır ayırıcıları 2 px {RENK_AYIRICI}. Başlık, satır adları, sütun başlıkları, tikler ve değerler {RENK_METIN}; eyebrow ve '—' {RENK_IKINCIL_ACIK}. {VURGU_ADI} öğesi: YALNIZ başlıktaki vurgu kelimesi. Kırmızı ✕ ve yeşil ✓ YOK.`
- SLOT DÜZENİ: `1) Eyebrow ve başlık üst solda. 2) Tablo kartı TAM x 88–1166, y 320–1092, köşe 24 px. 3) Satır adı sütunu x 130–600 (sol hizalı, cap 48); 2. sütun merkezi x=760; 3. sütun merkezi x=1010; sütun başlıkları cap üst y=372, grotesk 500 (kalın değil); en sağdaki yazı x 1124'ü geçmez. 4) 4 satır × 150 px; ayırıcılar y 440 / 590 / 740 / 890, x 130–1124. 5) Var = 40×40 px kutuda 2 px ince tik (dairesiz); yok = kısa '—'.`
- AÇI: `Bu görselde ürün fotoğrafı yok.`
- METİNLER: eyebrow ("KARŞILAŞTIRMA"), başlık ("Flasterden farkı.", vurgu "farkı"), sütun başlıkları ("Bu bant" / "{SINIF_ADI}"), 4 satır (3 × tik/—, 1 × değer/değer). Varsayılan sınıf adı; rakip marka adı yalnız kullanıcı isterse (Bilgi notu, `tasarim-dili.md` §8).

### G8 Zaman çizelgesi (bölünmüş, makro)
- RENK eki: `Zemin {RENK_ZEMIN}, tuvalin tamamında kesintisiz (sol bölge ayrı panel DEĞİL). Başlık, adım adları, çizgi ve halkalar {RENK_METIN}; eyebrow ve açıklamalar {RENK_IKINCIL_ACIK}. {VURGU_ADI} öğesi: YALNIZ ilk halkanın dolgusu.`
- SLOT DÜZENİ: `Sol bölge x 75–514: ürünün yakın planı, hiçbir kenara değmeden. Sağ kolon x 562–1166; sağdaki her şey x=562'den başlar. 1) Eyebrow cap üst y=112. 2) Başlık 2 satır, cap üstleri y=162 ve y=275. 3) Dikey 2 px çizgi x=576, y 476–1044; 3 halka (dış çap 28 px, çizgi 3 px) merkezleri y 500 / 760 / 1020; ilk halka {RENK_VURGU} dolu (28 px, daha büyük değil). 4) Her adım x=632'den: adım adı (≤ 10 karakter, cap üst halka merkezinin 24 px üstü) + 20 px altında iki satır açıklama.`
- AÇI: `Makro, kamera 15° yukarıdan, çok yakın; ürünün uzun ekseni dikey; ürün sol, üst ve alt kenara değmez (çevresinde en az %6 zemin); ayırt edici detay kadrajda, gerçek oranında. Ürünün sağ kenarı ile metin kolonu arasında boş zemin. Doku ince, kaba değil.`
- METİNLER: eyebrow ("ALIŞMA"), başlık ("İlk ay / nasıl geçer?", vurgu "geçer?"), 3 adım ("İlk gece" / "1. hafta" / "1. ay" + iki satır açıklama). Varsayılan deneyim dili; sağlık ya da sonuç dili kullanıcı isterse yazılır ve mesaja Bilgi notu eklenir (`tasarim-dili.md` §8).

## 7. Teslim
- Dosya adları (T3): `<marka>-urun-1..8.jpg` (galeri 8 kare), `<marka>-banner-masaustu.jpg` (1920×800), `<marka>-banner-mobil.jpg` (1080×1350).
- Kabul ve düzeltme: `kabul-kontrolu.md`.
