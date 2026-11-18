# Boş kart · ret durumunda yedek (ürünsüz seri kartı) (hazır istem şablonu, 0.4.1)

**HAZIR İSTEM.** İstemi sen YAZMAZSIN. `İSTEM BAŞI` ile `İSTEM SONU` arasındaki metni al, YALNIZ `{…}` yer tutucularını DEVAM KARTI'ndan doldur, gerisini KELİMESİ KELİMESİNE görsel aracına ver. Kısaltma, özetleme, yeniden yazma, cümle çıkarma, çeviri YASAK. Tek çağrı = tek görsel. İstemi kullanıcıya gösterme; isterse `.txt` dosyası olarak ver.

- Ne zaman: YALNIZ görsel aracı ürünü içerik politikası nedeniyle reddettiğinde (ürün fotoğrafı eklenince ya da ürün tarif edilince ret; `adim-5-gorsel-uretimi.md` "Ret durumunda"). Ret yokken bu şablon kullanılmaz; ürün her zaman önce normal şablonla denenir.
- Ne üretir: serinin kart TASARIMI (zemin, başlık, açıklama, teknik satır); ürünün yeri BOŞ. Ürün sonradan gerçek fotoğraftan yerleştirilir. Tasarım görsel aracından, ürün gerçek fotoğraftan gelir; ürün kodla çizilmez, görsel aracına başka bir şey gibi anlatılmaz.
- Ekler: YOK. Ürün fotoğrafı da, stil çapası da eklenmez (ölçüm: ek vermeden istenen boş kart daha sık geçti; ekli denemelerde ret ya da kodla çizilmiş kart geldi).
- Dürüstlük: istem ne istediğini açıkça söyler (boş yerleşim kartı, ürün sonradan gerçek fotoğraftan eklenecek). Ürünü gizleyen, başka ürün gibi tanıtan, politikayı dolanmaya çalışan ifade eklenmez. Bu istem de reddedilirse en çok 2 kez daha dene, sonra dur ve kullanıcıya söyle.
- Üretimden sonra: kart kodla çizilmiş gibi mi (düz dikdörtgenler, sistem fontu, fotoğraf kalitesi yok) bak; öyleyse RED, yeniden üret. Sonra `scripts/duzelt.py zemin` → yazım kontrolü (`kabul-kontrolu.md` §2b 1, 3, 4, 5) → gerçek ürün fotoğrafının yerleştirilmesi (`adim-5-gorsel-uretimi.md` "Ret durumunda" adım 3–5).
- Dosya adı: yerleştirmeden sonra plandaki ad (`<marka>-urun-N.jpg`); boş kart ara dosyadır, teslim edilmez.

## Yer tutucular (yalnız bunlar değişir)
- `{BAŞLIK_SATIRLARI}`: plandaki başlık, satır satır, BÜYÜK HARF. Ürün adı, ürün türü ve kategori adı YAZILMAZ; nötr ve doğru bir başlık (ölçü, malzeme, kullanım süresi gibi doğrulanmış özellik). Yanlış ya da yanıltıcı başlık yazılmaz.
- `{AÇIKLAMA}`: en çok 2 satır, doğrulanmış özellik; ürün adı yok.
- `{TEKNİK_SATIR}`: tek satır ölçü/malzeme ("120 MM · SİLİKON" biçiminde); yoksa aynen `bu satır yok, hiçbir şey yazma`.
- `{BOŞ_ALAN}`: ürünün geleceği yer, aynen şunlardan biri: `tuvalin sağ %55'i` · `tuvalin alt %60'ı` · `tuvalin ortası, genişliğin %60'ı ve yüksekliğin %60'ı`
- `{YAZI_ALANI}`: boş alanın karşısı, aynen: `sol %38` · `üst %30` · `üst %22`
- `{ZEMİN_HEX}`, `{METİN_HEX}`, `{İKİNCİL_HEX}`, `{KART_HEX}`, `{VURGU_HEX}`, `{NİŞ_YASAKLARI}`, `{DÜZELTME}`: `g1.md` ile aynı değerler, karakter karakter

=== İSTEM BAŞI ===
Sen üst düzey bir marka ajansında sanat yönetmenisin. YALNIZ 1 görsel üret: kolaj, ızgara, yan yana varyasyon, çok panel ya da mockup çerçevesi değil. Bu bir BOŞ YERLEŞİM KARTIdır: bir ürün galerisi serisinin kart tasarımı. Kartta ürün YOK; ürün için ayrılan alan boş bırakılır ve oraya sonradan gerçek ürün fotoğrafı yerleştirilecek. Hiçbir ürün, nesne ya da ürün silüeti çizme. Görseli fotoğraf kalitesinde üret; kod ya da çizim aracıyla düz şekillerden kurma.

RENK (yalnız bunlar): Zemin {ZEMİN_HEX}; DÜZ ve kesintisiz tek renk, dört köşede aynı; degrade, vinyet, ışık lekesi, hale, doku YOK. Ana metin {METİN_HEX}. İkincil metin {İKİNCİL_HEX}. Kart yüzeyi {KART_HEX}. Tek vurgu rengi {VURGU_HEX} ve görselde yalnız TEK küçük öğede.
TİPOGRAFİ (bir marka sistemi; her görselde aynı): Başlıklar DAR (condensed) grotesk, BÜYÜK HARF, SemiBold; Barlow Condensed / Oswald ailesine benzer uzun-dar harfler (Barlow Condensed SemiBold ya da Oswald benzeri dar grotesk); harf aralığı sıkı, satır aralığı 0,95; başlık büyük ve kendinden emin, tasarımın ana öğesi. Başlık TEK renk: bütün satırlar ana metin renginde; iki renkli başlık, renkli kelime, ince ağırlıklı satır YOK. Başlık satır satır, METİNLER'deki kırılımla dizilir. Poppins, Montserrat ve benzeri geniş geometrik yazı tipi = RED; bu dar grotesk aile markanın tek başlık ailesidir, başka başlık ailesi KULLANILMAZ. Gövde ve açıklamalar: sade grotesk (Inter benzeri) Regular, cümle düzeni. Küçük etiketler: aynı grotesk Medium, BÜYÜK HARF, harf aralığı geniş (+%12). Başka yazı tipi YOK; serif YOK; italik YOK; el yazısı YOK. Bütün metinler tek sol hatta hizalı (aksi yazmıyorsa). Metin düz vektör gibi keskin. Türkçe harfler birebir doğru: İ, ı, ğ, ş, ç, ö, ü (büyük harfte i → İ, ı → I). Yazım hatası olan görsel REDdedilir.
IŞIK: temiz stüdyo ışığı; boş alanın alt üçte birinde, ortada, yalnız çok hafif, kısa, yumuşak bir temas gölgesi (oraya konacak ürünün zemine değdiği yer); başka gölge, yansıma, parlama YOK.

DÜZEN (kare 1:1, boş yerleşim kartı): Yazı alanı {YAZI_ALANI}; ürün alanı {BOŞ_ALAN}. Ürün alanı TAMAMEN BOŞ düz {ZEMİN_HEX} zemin: içinde ürün, nesne, silüet, çerçeve, kesik çizgi, yer tutucu kutu, artı işareti, "ürün buraya" yazısı YOK; yalnız IŞIK'ta tarif edilen hafif temas gölgesi. Yazı alanında başlık en üstte, harf yüksekliği tuvalin %9–11'i; altında açıklama; en altta teknik satır küçük etiket düzeninde. Yazılar ürün alanına taşmaz.
METİNLER (yalnız bunlar, birebir): Başlık: {BAŞLIK_SATIRLARI} · Açıklama: {AÇIKLAMA} · Teknik satır: {TEKNİK_SATIR}
ÇIKTI: tek görsel, kare 1:1, en az 1500 × 1500 piksel.



{DÜZELTME}
=== İSTEM SONU ===
