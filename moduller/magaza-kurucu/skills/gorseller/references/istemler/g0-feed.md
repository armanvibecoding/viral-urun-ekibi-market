# G0 · Feed karesi (yazısız ana görsel) (hazır istem şablonu, 0.4.0)

**HAZIR İSTEM.** İstemi sen YAZMAZSIN. `İSTEM BAŞI` ile `İSTEM SONU` arasındaki metni al, YALNIZ `{…}` yer tutucularını DEVAM KARTI'ndan doldur, gerisini KELİMESİ KELİMESİNE görsel aracına ver. Kısaltma, özetleme, yeniden yazma, cümle çıkarma, çeviri YASAK. Tek çağrı = tek görsel. İstemi kullanıcıya gösterme; isterse `.txt` dosyası olarak ver.

- Neden: Shopify ürününün İLK görseli Google Merchant Center'a `image_link` olarak gider. Google bu görselde yazı, rozet, fiyat, "ücretsiz kargo", eklenmiş logo ve kenarlık YASAKLIYOR; ürün karenin %75–90'ını kaplamalı; ≥ 1500 px öneriliyor (support.google.com/merchants/answer/6324350; kanıt tablosu repo `research/kutuphane-v2/KANIT.md` 4.3). Yazılı afiş (G1) bu yüzden 2. sıraya geçer. Beyaz zemin şartı YOK: galerinin zemin HEX'i kullanılır.
- Ne zaman: G1 onaylandıktan hemen sonra, G2'den önce.
- Ekler (her çağrıda YENİDEN eklenir): Ek 1 = orijinal ürün fotoğrafı · Ek 2 = onaylı G1 (önceki görsel "düzenlenmez"; her görsel yeniden üretilir)
- Üretimden sonra: `scripts/duzelt.py zemin` → kontrol listesi (`kabul-kontrolu.md` §2b ve §2c: yazı yok, ürünün uzun kenarı tuvalin %75–86'sı); ihlal varsa göstermeden 1 kez yeniden üret (`{DÜZELTME}` dolu).
- Dosya adı: `<marka>-urun-0.jpg`; ürün medyasında 1. sıra (T3).

## Yer tutucular (yalnız bunlar değişir)
- `{ÜRÜN_DURUŞU}`: ürün ince-uzunsa aynen `neredeyse dik, dikeyden 12° eğik; kamera tam üstten (kuşbakışı)`; değilse aynen `dik, önden hafif üç çeyrek açı; kamera göz hizasında`
- `{ÜRÜN_ADI_VE_ÖLÇÜ}`, `{ÜRÜN_KİLİDİ_PARÇALARI}`, `{ETİKET_İSTİSNASI}`, `{ZEMİN_HEX}`, `{METİN_HEX}`, `{İKİNCİL_HEX}`, `{KART_HEX}`, `{VURGU_HEX}`, `{ÜRÜN_RENGİ}`, `{NİŞ_YASAKLARI}`, `{DÜZELTME}`: `g1.md` ile aynı değerler, karakter karakter

=== İSTEM BAŞI ===
Sen üst düzey bir marka ajansında sanat yönetmenisin. YALNIZ 1 görsel üret: kolaj, ızgara, yan yana varyasyon, çok panel ya da mockup çerçevesi değil. Ek 1 = ürün fotoğrafı (yalnız ürün referansı; içindeki yazı, logo, zemin ve düzen YOK SAYILIR). Ek 2 = aynı markanın onaylı galeri karesi: ondan YALNIZ yazı tipi sistemini, renkleri, boşluk ritmini ve kalite seviyesini al; düzenini, metinlerini ve ürünün açısını KOPYALAMA.

ÜRÜN KİLİDİ: Ek 1 ürünün TEK doğru kaynağıdır; ürünü birebir koru, yeniden tasarlama. Ürün: {ÜRÜN_ADI_VE_ÖLÇÜ}. {ÜRÜN_KİLİDİ_PARÇALARI} Ürün yüzeyi DÜZ ve temiz: gravür, üretici logosu, amblem, kazıma yazı, harf ya da rakam YOK (Ek 1'de üründe görünen küçük gravürü SİL, kopyalama). {ETİKET_İSTİSNASI} Biçim, renk, parça sayısı ya da sayılan parçalardan biri değişirse görsel REDdedilir. Ek 1'deki yazıları, logoyu, zemin rengini, düzeni ve açıyı YOK SAY ve KOPYALAMA; Ek 1 yalnız ürünün kendisi için referanstır.

RENK (yalnız bunlar): Zemin {ZEMİN_HEX}; DÜZ ve kesintisiz tek renk, dört köşede aynı; degrade, vinyet, ışık lekesi, hale, doku YOK. Ana metin {METİN_HEX}. İkincil metin {İKİNCİL_HEX}. Kart yüzeyi {KART_HEX}. Tek vurgu rengi {VURGU_HEX} ve görselde yalnız TEK küçük öğede. {ÜRÜN_RENGİ} yalnız ürünün kendisinde; {ÜRÜN_RENGİ} yazı, çizgi, şekil, zemin YOK.
TİPOGRAFİ (bir marka sistemi; her görselde aynı): Başlıklar DAR (condensed) grotesk, BÜYÜK HARF, SemiBold; Barlow Condensed / Oswald ailesine benzer uzun-dar harfler (Barlow Condensed SemiBold ya da Oswald benzeri dar grotesk); harf aralığı sıkı, satır aralığı 0,95; başlık büyük ve kendinden emin, tasarımın ana öğesi. Başlık TEK renk: bütün satırlar ana metin renginde; iki renkli başlık, renkli kelime, ince ağırlıklı satır YOK. Başlık satır satır, METİNLER'deki kırılımla dizilir. Poppins, Montserrat ve benzeri geniş geometrik yazı tipi = RED; bu dar grotesk aile markanın tek başlık ailesidir, başka başlık ailesi KULLANILMAZ. Gövde ve açıklamalar: sade grotesk (Inter benzeri) Regular, cümle düzeni. Küçük etiketler: aynı grotesk Medium, BÜYÜK HARF, harf aralığı geniş (+%12). Başka yazı tipi YOK; serif YOK; italik YOK; el yazısı YOK. Bütün metinler tek sol hatta hizalı (aksi yazmıyorsa). Metin düz vektör gibi keskin. Türkçe harfler birebir doğru: İ, ı, ğ, ş, ç, ö, ü (büyük harfte i → İ, ı → I). Yazım hatası olan görsel REDdedilir.
IŞIK: temiz stüdyo ürün fotoğrafı; ürün gerçek fotoğraf gibi keskin; altında yalnız çok hafif, kısa temas gölgesi.

DÜZEN (kare 1:1, FEED karesi: galerinin İLK görseli; Google Merchant Center ve sosyal katalog bu kareyi ürünün ana görseli olarak kullanır): YALNIZ ürün, tek ürün, tek renk varyantı; ürünle birlikte satılmayan hiçbir nesne YOK. Ürün ortada, {ÜRÜN_DURUŞU}; ürünün uzun kenarı tuvalin en az %75'ini, en çok %86'sını kaplar (Google aralığı %75–90; her kenarda en az %7 boşluk kuralıyla üst sınır %86); ürünün tamamı net ve kesilmemiş. Bu karede HİÇBİR yazı, rakam, etiket, rozet, logo, çerçeve, kenarlık, ikon, çizgi, kart YOK. Zemin düz {ZEMİN_HEX} (galerinin diğer kareleriyle aynı); ışık ve gölge diğer karelerle aynı.
METİNLER (yalnız bunlar, birebir): BU KAREDE HİÇBİR YAZI YOK.
ÇIKTI: tek görsel, kare 1:1, en az 1500 × 1500 piksel.

YASAKLAR: insan, el, hayvan fotoğrafı; taş, kaide, bitki, çiçek, kumaş, duman, sis, parlama (glow), ışık hüzmesi, bokeh, yansıma havuzu, organik leke (blob), dalga, yay ve kavis biçimli süs, kalp, yıldız, rozet, mühür, hap içine alınmış etiket, ok işareti, çizgi ikon, piktogram; {NİŞ_YASAKLARI} büyüteç dairesi; "DETAY 01" gibi numaralı etiket; "detay" kelimesi; keyfi süs çizgisi; degrade; marka adı ya da logo; harf aralığı açılmış marka adı etiketi; kargo, teslimat, indirim, kampanya, fiyat, garanti, puan, yorum, yüzde ile ilgili HER yazı; METİNLER bölümünde olmayan HER yazı. Bu istemdeki renk kodlarını, ölçüleri, blok adlarını görsele YAZMA. Hiçbir öğe (ürün dahil) tuval kenarına değmez; her kenarda tuvalin en az %7'si boş zemin kalır, ürün kenarda kesilmez. Tuvalin yarısı boş zemin kalmaz.

{DÜZELTME}
=== İSTEM SONU ===
