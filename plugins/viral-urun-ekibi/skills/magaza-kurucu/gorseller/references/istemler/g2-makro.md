# G2 · Özellik kartları (3 geniş makro kart) (hazır istem şablonu, 0.3.6)

**HAZIR İSTEM.** İstemi sen YAZMAZSIN. `İSTEM BAŞI` ile `İSTEM SONU` arasındaki metni al, YALNIZ `{…}` yer tutucularını DEVAM KARTI'ndan doldur, gerisini KELİMESİ KELİMESİNE görsel aracına ver. Kısaltma, özetleme, yeniden yazma, cümle çıkarma, çeviri YASAK. Tek çağrı = tek görsel. İstemi kullanıcıya gösterme; isterse `.txt` dosyası olarak ver.

- Ne zaman: doğrulanmış özellik/parça 3–5 ise (`g2.md` yerine).
- Ekler (her çağrıda YENİDEN eklenir): Ek 1 = orijinal ürün fotoğrafı · Ek 2 = onaylı G1 (önceki görsel "düzenlenmez"; her görsel yeniden üretilir)
- Üretimden sonra: `scripts/duzelt.py zemin` → kontrol listesi (`kabul-kontrolu.md` §2b); ihlal varsa göstermeden 1 kez yeniden üret (`{DÜZELTME}` dolu).

## Yer tutucular (yalnız bunlar değişir)
- `{BAŞLIK_SATIRLARI}`: 2 satır, BÜYÜK HARF, tırnak içinde ` / ` ile (ör. `"ALTI AYRINTI," / "TEK MAKAS."`)
- `{MAKRO_PARÇALARI}`: 3 numaralı madde, her biri BU ürünün gerçek bir parçası (ör. `1) ürünün tamamı yatay, küçük, uçtan uca; 2) bıçağın çelik yüzeyine yakın plan; …`)
- `{KART_METİNLERİ}`: 3 satır, her biri `Kart N: "ETİKET" — "tek satır açıklama"`; yalnız doğrulanmış özellik; "konforlu", "şık" gibi doğrulanmamış sıfat yok
- `{VURGU_KARTI}`: vurgunun düşeceği kartın numarası (tek rakam)
- `{ÜRÜN_ADI_VE_ÖLÇÜ}`: ürünün somut adı + doğrulanmış ölçü (ör. `7,25 inç profesyonel pet kuaför makası`)
- `{ÜRÜN_KİLİDİ_PARÇALARI}`: `<marka>-istem-bloklari.md` dosyasındaki parça parça kilit (≥ 5 cümle: biçim ve kıvrım yönü, parça SAYILARI, "X DEĞİL" karşıtları, renk/yüzey, duruş); her şablonda karakter karakter aynı
- `{ETİKET_İSTİSNASI}`: ürünün kendi satılan ambalaj etiketi korunacaksa aynen `İstisna: ürünün kendi ambalaj etiketi Ek 1 ile harf harf aynı kalır.`; yoksa yer tutucuyu sil
- `{ZEMİN_HEX}`: DEVAM KARTI "Görsel zemini" (ad + HEX, ör. `koyu petrol #0F2B2E`)
- `{METİN_HEX}`: görsel ana metin rengi (ad + HEX)
- `{İKİNCİL_HEX}`: görsel ikincil metin rengi (ad + HEX)
- `{KART_HEX}`: zeminin bir ton açığı/koyusu kart yüzeyi (HEX)
- `{VURGU_HEX}`: tek vurgu (ad + HEX); ürünün baskın renginden OLMAZ
- `{ÜRÜN_RENGİ}`: ürünün baskın renginin adı, büyük harfle başlar (ör. `Pembe`)
- `{NİŞ_YASAKLARI}`: nişe özel yasak öğeler, sonunda noktalı virgül (ör. `pati izi, tüy yığını;`); yoksa sil
- `{DÜZELTME}`: ilk denemede sil; yeniden üretimde aynen `DÜZELTME (önceki deneme bu yüzden REDdedildi; KESİN düzelt): <ret nedeni>`

=== İSTEM BAŞI ===
Sen üst düzey bir marka ajansında sanat yönetmenisin. YALNIZ 1 görsel üret: kolaj, ızgara, yan yana varyasyon, çok panel ya da mockup çerçevesi değil. Ek 1 = ürün fotoğrafı (yalnız ürün referansı; içindeki yazı, logo, zemin ve düzen YOK SAYILIR). Ek 2 = aynı markanın onaylı galeri karesi: ondan YALNIZ yazı tipi sistemini, renkleri, boşluk ritmini ve kalite seviyesini al; düzenini, metinlerini ve ürünün açısını KOPYALAMA.

ÜRÜN KİLİDİ: Ek 1 ürünün TEK doğru kaynağıdır; ürünü birebir koru, yeniden tasarlama. Ürün: {ÜRÜN_ADI_VE_ÖLÇÜ}. {ÜRÜN_KİLİDİ_PARÇALARI} Ürün yüzeyi DÜZ ve temiz: gravür, üretici logosu, amblem, kazıma yazı, harf ya da rakam YOK (Ek 1'de üründe görünen küçük gravürü SİL, kopyalama). {ETİKET_İSTİSNASI} Biçim, renk, parça sayısı ya da sayılan parçalardan biri değişirse görsel REDdedilir. Ek 1'deki yazıları, logoyu, zemin rengini, düzeni ve açıyı YOK SAY ve KOPYALAMA; Ek 1 yalnız ürünün kendisi için referanstır.

RENK (yalnız bunlar): Zemin {ZEMİN_HEX}; DÜZ ve kesintisiz tek renk, dört köşede aynı; degrade, vinyet, ışık lekesi, hale, doku YOK. Ana metin {METİN_HEX}. İkincil metin {İKİNCİL_HEX}. Kart yüzeyi {KART_HEX}. Tek vurgu rengi {VURGU_HEX} ve görselde yalnız TEK küçük öğede. {ÜRÜN_RENGİ} yalnız ürünün kendisinde; {ÜRÜN_RENGİ} yazı, çizgi, şekil, zemin YOK.
TİPOGRAFİ (bir marka sistemi; her görselde aynı): Başlıklar DAR (condensed) grotesk, BÜYÜK HARF, SemiBold; Barlow Condensed / Oswald ailesine benzer uzun-dar harfler (Barlow Condensed SemiBold ya da Oswald benzeri dar grotesk); harf aralığı sıkı, satır aralığı 0,95; başlık büyük ve kendinden emin, tasarımın ana öğesi. Başlık TEK renk: bütün satırlar ana metin renginde; iki renkli başlık, renkli kelime, ince ağırlıklı satır YOK. Başlık satır satır, METİNLER'deki kırılımla dizilir. Poppins, Montserrat ve benzeri geniş geometrik yazı tipi = RED; bu dar grotesk aile markanın tek başlık ailesidir, başka başlık ailesi KULLANILMAZ. Gövde ve açıklamalar: sade grotesk (Inter benzeri) Regular, cümle düzeni. Küçük etiketler: aynı grotesk Medium, BÜYÜK HARF, harf aralığı geniş (+%12). Başka yazı tipi YOK; serif YOK; italik YOK; el yazısı YOK. Bütün metinler tek sol hatta hizalı (aksi yazmıyorsa). Metin düz vektör gibi keskin. Türkçe harfler birebir doğru: İ, ı, ğ, ş, ç, ö, ü (büyük harfte i → İ, ı → I). Yazım hatası olan görsel REDdedilir.
IŞIK: temiz stüdyo ürün fotoğrafı; ürün gerçek fotoğraf gibi keskin; altında yalnız çok hafif, kısa temas gölgesi.

DÜZEN (kare 1:1, ÖZELLİK KARTLARI karesi): Üstte sol hizalı başlık, 2 satır, büyük (harf yüksekliği tuvalin %6–8'i). Altında alt alta 3 eşit, tam genişlikte yatay kart; kartlar kart yüzeyi renginde, köşeleri hafif yuvarlak, gölgesiz, aralarında eşit dar boşluk; kartlar başlıkla aynı sol hatta. Bu karede yanda ayrı büyük ürün fotoğrafı YOK. Her kartın sol %45'inde İKON YOK, onun yerine BU ürünün ilgili parçasının gerçek, keskin, stüdyo MAKRO FOTOĞRAFI (Ek 1'deki ürünün aynısı, aynı renk ve yüzey), kart kenarına değmeden: {MAKRO_PARÇALARI}. Kartın sağ %55'inde, dikeyde ortalı etiket (dar grotesk BÜYÜK HARF SemiBold, ana metin rengi) ve altında tek satır açıklama (sade grotesk Regular, ikincil renk). Vurgu rengi: YALNIZ {VURGU_KARTI}. kartın etiketinde.
METİNLER (yalnız bunlar, birebir):
Başlık (satır satır): {BAŞLIK_SATIRLARI}
{KART_METİNLERİ}
ÇIKTI: tek görsel, kare 1:1.

YASAKLAR: insan, el, hayvan fotoğrafı; taş, kaide, bitki, çiçek, kumaş, duman, sis, parlama (glow), ışık hüzmesi, bokeh, yansıma havuzu, organik leke (blob), dalga, yay ve kavis biçimli süs, kalp, yıldız, rozet, mühür, hap içine alınmış etiket, ok işareti, çizgi ikon, piktogram; {NİŞ_YASAKLARI} büyüteç dairesi; "DETAY 01" gibi numaralı etiket; "detay" kelimesi; keyfi süs çizgisi; degrade; marka adı ya da logo; harf aralığı açılmış marka adı etiketi; kargo, teslimat, indirim, kampanya, fiyat, garanti, puan, yorum, yüzde ile ilgili HER yazı; METİNLER bölümünde olmayan HER yazı. Bu istemdeki renk kodlarını, ölçüleri, blok adlarını görsele YAZMA. Hiçbir öğe (ürün dahil) tuval kenarına değmez; her kenarda tuvalin en az %7'si boş zemin kalır, ürün kenarda kesilmez. Tuvalin yarısı boş zemin kalmaz.

{DÜZELTME}
=== İSTEM SONU ===
