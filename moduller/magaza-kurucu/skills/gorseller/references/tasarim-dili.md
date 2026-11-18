# Tasarım dili: çalışma zamanı çekirdeği

Durum: ONAYLI dil (kullanıcı, 2026-11-16/17), sürüm 0.3.0. Ölçüler göreli tarif: görsel model px tutmuyor, oranı tutuyor. Prompt şablonları: `uretim-promptlari.md`. Kabul: `kabul-kontrolu.md`. SESSA px defteri pakette yok (repo `docs/TASARIM-DILI-DEFTER.md`).

## 1. İlkeler
- **İnsansız, grafik, ürün odaklı.** İnsan, el, yüz, model, yatak sahnesi yok. Tek istisna bedenli giyim: kullanıcıya tek satırla sorulur.
- **Kaliteyi görsel model getirir.** Görselin tamamını (ürün, zemin, yazı, ikon) ChatGPT görsel modeli üretir. Kod yalnız ölçer, kırpar, zemini boyar, tek bozuk harfi düzeltir. Kodla çizilmiş galeri ve kodla birleştirilmiş logo reddedildi.
- **Referans ilkedir, kopya değildir.** Ürün fotoğrafından yalnız ürünün kimliği alınır; dizilim, açı, kadraj, gölge yönü kopyalanmaz. Stil çapasından yalnız tipografi sistemi, renk rolleri, boşluk ritmi ve kalite seviyesi alınır; marka adı, ürün, metin, düzen ve nesneler alınmaz.
- **Her görsel ayrı mesaj:** tek prompt, tek görsel. Çoklu istekte kolaj, yanlış oran ve ürün kayması ölçüldü.
- **Açı tekrarı yok:** her görselin promptunda kendi AÇI satırı; galeride aynı dizilim ve açı bir kez.
- **Turda tek değişken:** yeniden üretimde yalnız reddedilen eksen değişir.
- **Uydurma veri yok:** görseldeki her sayı ve özellik ürün etiketinden ya da ölçüden gelir. Mağaza politikası (kargo, iade, garanti) görsele yazılmaz (§9).

## 2. Metin nereye gider
- **Galeri 8 kare (G1–G8).** G1 poster: somut fayda başlığı + ürün + en fazla 1 kısa alt satır (ürün satırı: doğrulanmış ürün gerçeği). G2–G8 yazılı grafik kare serbest (ikon kartı, nasıl çalışır, dev sayı, adımlar, ölçü, karşılaştırma, zaman çizelgesi).
- **Feed notu (bilgi):** Shopify, Google/Meta kanalına ürünün 1. medyasını gönderir; G1 yazılıysa feed'e de yazılı gider. Yazısız ayrı feed görseli istenirse kullanıcıya sorulur.
- **Masaüstü banner metinli (0.3.5).** Tipografi görselin içinde: etiket, dev başlık, alt metin, buton solda; ürün sağda. Sol yarısı boş banner reddedildi. `e-hero-b` H1 görseldeki başlıkla çelişmez.
- **Mobil banner metinli.** Tipografi görselin içinde, tasarımın parçası: küçük etiket, başlık, alt metin, hap buton, ürün satırı. Yazıyı görselin altına ayrı bloğa almak ve küçük ürün + boş zemin reddedildi.
- **S1–S5 site görselleri yazısız.**
- Marka adı yalnız ambalajın kendi baskısında görünür; başlık ve gövdede geçmez.

## 3. Renk
Marka paletinin rolleri görselde 4 role iner:
- **Metin (koyu panel):** ambalajın en koyu baskı rengi; tek değer. Modelin daha koyuya kayması ve ikinci bir koyu ton yasak.
- **Zemin:** tek HEX, açık ya da koyu; ölçüt ürünün zeminden güçlü ayrışması (luminans ≥ 1,5:1, Python ile). Açık/pastel ürün açık pastel zemine konmaz (pembe tüp + pembe-krem zemin soluk çıktı): koyu zemin seçilir. DEVAM KARTI'na "görsel zemini" olarak yazılır; site "arka plan" renginden farklı olabilir (§10).
- **Kart:** zeminden çok az açık, ince kenar çizgili, gölgesiz.
- **Vurgu:** ambalajdaki tek doygun aksan; görsel başına tam 1 öğe (başlıktaki vurgu kelimesi, nokta ya da tek ikon çizgisi; süs çizgisi değil); metin ve vurgu ürünün renginden olmaz (§10).
- Metin kontrastı ≥ 4,5:1; ikincil metin tonu açık ve koyu zemin için ayrı türetilir.
- Yüzeyler düz: renkten renge degrade, vinyet, radyal parlama yok. Görselde en fazla 4 sistem rengi (ürünün kendi renkleri hariç). Bütün galeri ve bannerlar tek zemin HEX'inde (§9).

## 4. Zemin hilesi ve kenar payı (tek değer)
- **Görsel zemini = konacağı yüzeyin zemini (aynı hex).** Sayfada ürün çerçevesiz, yüzeye oturmuş görünür. Bölüm görselinde (S1–S5) bölümün zemin rengi; galeride ve bannerlarda marka "arka plan" rengi, hepsinde TEK ve AYNI HEX (§9).
- **Ürün hiçbir kenara değmez: her kenarda en az %6 boş zemin.** Bu tek değerdir; yazı, kart, çizgi ve ikon da kenara %6'dan yakın durmaz. Yakın plan (makro) karede ürün büyük ve yakındır ama yine kadrajın içinde kalır; kenardan taşan ürün sayfada düz kesik kenar (kutu) bırakır.
- Kontrol: köşe rengi hedef hex'ten ±3 RGB içinde olmalı; değilse `scripts/duzelt.py zemin <girdi> <çıktı> <#hex>` kenara bağlı zemini boyar (betiği bulma: `find / -name duzelt.py 2>/dev/null | head -1`; `gorseller` skill'inde). Kenarda ürün varsa betik RED verir: yeniden üret.

## 5. Tipografi
- **D (varsayılan, 0.3.5, her niş):** başlık dar (condensed) grotesk, BÜYÜK HARF, SemiBold (Barlow Condensed / Oswald benzeri), satır aralığı 0,95, 2–4 kısa satır; gövde sade grotesk Regular; küçük etiket aynı grotesk Medium, BÜYÜK HARF, harf aralığı +%12. Serif, italik, el yazısı yok.
- **A (yalnız kullanıcı isterse):** başlık dar, uzun oranlı, yüksek kontrastlı serif, Regular 400 (Instrument Serif / Editorial New benzeri); vurgu kelimesi aynı serifin italiği, görselde tek. Diğer yazı tek grotesk (Inter benzeri). Bold ve kalın kama serif yok.
- **B (yalnız kullanıcı isterse):** tek grotesk aile; başlık en fazla SemiBold, italik yok.
- Niş anahtarını marka adımı seçer (`uretim-promptlari.md` §2) ve DEVAM KARTI'na yazar.
- **Hiyerarşi (göreli):** başlık tasarımın ana öğesidir: G1 ve bannerlarda harf yüksekliği tuvalin %9–11'i, bilgi karelerinde %6–8; başlık bloğu G1'de tuval yüksekliğinin yaklaşık yarısı. İnce, küçük, silik başlık reddedildi. En küçük metin 360 px'e küçültülünce okunur kalır.
- **Limitler:** başlık ≤ 5 kelime, 2–4 kısa satır, yetim kelime yok; kart başlığı tek satır, ≤ 14 karakter; görsel toplamı ≤ 40 kelime. Satırlar promptta ayrı ayrı, "/" ile verilir.
- **Eyebrow:** büyük harf, aralıklı grotesk, ikincil tonda; hap ya da kutu içinde değil; G2–G8'de var, G1'de ve bannerda yok.
- **Hizalama:** bütün kareler sol hizalı, bütün satırlar aynı sol hatta; tablo sütun başlıkları ortalı olabilir.
- Türkçe harfler birebir: büyük harfte i → İ, ı → I; ş, ğ, ç, ö, ü.

## 6. Bileşenler
- **İkon:** özellik kartlarında (G2) çizgi ikon KULLANILMAZ; yerine ürünün ilgili parçasının gerçek makro fotoğrafı (0.3.5, kullanıcı: "ikonlar kötü"). İkon yalnız başka çare yoksa: ince çizgi, tek renk, sette aynı kalınlık.
- **Kart:** gölgesiz, küçük köşe, iç boşluk eşit, kartlar arası boşluk eşit, kart içinde dikey ayraç yok.
- **İşaret çizgisi:** parçadan etikete düz ince çizgi, parçadaki ucunda küçük nokta, çizgiler kesişmez.
- **Ölçü çizgisi:** iki ucunda dik kısa çizgi, ok başı yok, değer Türkçe ondalık virgülüyle ("7,5 cm"), uçlar ürünün uçlarıyla hizalı.
- **Tablo:** ince satır ayırıcı; var = ince tik, yok = "—"; kırmızı ✕ ve yeşil ✓ yok.
- **Zaman çizelgesi:** dikey ince çizgi, en fazla 4 adım, deneyim dili.
- **Ürün satırı (G1, B2 alt satırı):** yalnız doğrulanmış ürün gerçeği (içerik, ölçü, malzeme), "·" ayraçlı, ≤ 3 madde; kargo, iade, garanti değil (§9).
- **Işık:** tek kaynak; gölgeler kısa, yumuşak, hepsi aynı yönde.

## 7. Yasaklar (kalite)
- **AI süsü:** taş, kaide, traverten, mermer, ahşap masa, kuru çiçek, bitki, yaprak, organik leke, kumaş drape, bokeh, ışık hüzmesi, parlama, yansıma havuzu, zemin–duvar çizgisi.
- **İkon ve grafik:** 3D, emoji, dolu siluet; ok, dalga, ışıma, hareket ve parıltı çizgisi; hap içine alınmış etiket.
- **Uydurma veri:** uydurma yüzde, kullanıcı sayısı, yıldız puan, rozet, mühür, "klinik", hekim, basın logosu, kaynaksız dipnot. Kaynak satırı yalnız gerçek, yazılı kaynak varsa.
- **Onaysız vaat ve klişe:** lojistik/kampanya yazısı ("Ücretsiz kargo" vb.; liste `01-kurallar.md` Görsel metni), süs çizgisi, numara etiketi ("DETAY 01"), büyüteç dairesi (§9).
- Görsele stil/yön adı, renk kodu, px değeri ya da prompt metni yazılmaz. Kolaj, çerçeve, dış beyaz pay yok.

## 8. Bilgi notları (kullanıcının sorumluluğu; engel değil)
Aşağıdakiler hiçbir görseli ya da metni reddettirmez, yumuşatılmaz; ilgili mesajın sonunda tek satır "Bilgi notu (kullanıcının sorumluluğu): …" olarak yazılır.
- Sağlık ya da sonuç dili ("daha iyi uyku", "horlamayı keser"), hastalık adı, üstünlük iddiası ("ilk", "tek").
- Karşılaştırmada rakip marka adı. Varsayılan tasarım sınıfa karşı karşılaştırmadır ("düz flaster"); rakip adı kullanıcı isterse yazılır. Takviyede karşılaştırma karesi yerine kutu/ölçü karesi önerilir.
- Ürünün tıbbi cihaz olabilmesi (EMS/TENS, ışık, ölçüm cihazı): kayıt belgesi kullanıcının işidir.

## 9. Görsel metni, tipografi kilidi, kadraj, ürün kayması (0.3.4, ilk gerçek koşudan)
- **Metin:** ne yazılır, ne yazılmaz: `01-kurallar.md` "Görsel metni" maddesi (tek kaynak). Özet: "Ücretsiz kargo" gibi lojistik/kampanya/garanti yazısı ASLA; başlık somut fayda; [DOĞRULA] bilgi yazılmaz.
- **Önce HEX ve yazı tipi, sonra görsel:** DEVAM KARTI'nda marka paleti (5 HEX) ve başlık yazı tipi tarifi (A/B + 1 satır tarif) yoksa görsel ÜRETİLMEZ; `marka` adımına dönülür. Her görsel promptunda HEX'ler (RENK bloğu) ve yazı tipi tarifi (TİPOGRAFİ bloğu) açıkça yazılır; boş yer tutucuyla ya da "marka renklerinde" gibi tarifle prompt gönderilmez. Palet dışı renk yok.
- **Tek hiyerarşi:** başlık > en fazla 1 kısa alt satır. Yarışan ikinci başlık, slogan ya da etiket yok. Bilgi karelerinde (G2–G8) eyebrow + başlık + karenin kendi içeriği.
- **Tek zemin HEX'i:** bütün galeri kareleri (G1–G8) ve bannerlar (B1, B2) TEK ve AYNI zemin HEX'ini kullanır; görselden görsele zemin rengi değişmez. HEX `marka` adımında seçilir ("görsel zemini"), her görsel promptunun RENK bloğunda birebir yazılır, üretimden sonra zemin hilesi aracıyla (`scripts/duzelt.py zemin`) o HEX'e sabitlenir. Farklı zeminli görsel RED. Bölünmüş zemin yok; zemin açık ya da koyu olabilir ama tektir.
- **Yasak** (kullanıcı açıkça istemedikçe): numara/etiket yazısı ("DETAY 01", "01/08") ve "detay" kelimesi, büyüteç dairesi ve yakınlaştırma balonu, süs çizgisi (başlık altı renkli çizgi dahil), jenerik çok kalın + çok ince sans karışımı.
- **Kadraj doluluğu:** ürünün ana öğe olduğu karelerde (G1, G3, B2 ürün bölgesi, S1–S5) ürün (grubu) tuvalin en az bir ekseninde ≥ %55'ini kaplar (G1'de %60–70); %6 kenar payı korunur; kadrajın yarısı boş zemin kalmaz. İnce/uzun ürün çapraz konmaz: uzun ekseni tuval kenarına paralel ya da en çok 20° eğik; kadraj dolmuyorsa daha yakın açı ya da ambalajıyla grup. Bilgi karelerinde ürün kendi slotunu doldurur.
- **Değer ayrıntısı:** her görselde en az bir değer ayrıntısı net görünür (doku, dikiş, mekanizma, malzeme yüzeyi, parça birleşimi).
- **Ürün kayması:** her üretimden sonra görsel tedarikçi fotoğrafıyla (Ref 1) yan yana karşılaştırılır: ana renk, ikinci renk, biçim, parça sayısı. Fark varsa RED, orijinalden yeniden üret. Renk varyantı belirsizse ya da araştırma metni fotoğrafla çelişiyorsa (metin "mor ve yeşil", fotoğraf pembe-altın) üretmeden önce kullanıcıya tek soru: "Hangi renk varyantını satıyoruz?"

## 10. 0.3.5: test12 dersleri + Lufella koşusu (üretim kalıbı)
Ayrıntı ve şablonlar: `gorseller` skill'inde `ortak-istem-bloklari.md`.
- **G1 önce:** önce yalnız G1 üretilir, kullanıcıya onaylatılır; sonraki her görsel `ürün fotoğrafı + onaylı G1` ekiyle üretilir (G1'den yalnız yazı tipi, renk, boşluk ritmi). Ayrı mesajlarda sistem böyle dağılmıyor.
- **Üç ortak blok:** ÜRÜN KİLİDİ, SİSTEM (renk + tipografi + ışık), YASAKLAR bir kez doldurulur, her isteme karakter karakter aynen eklenir; görsele özel yalnız DÜZEN + METİNLER + ÇIKTI.
- **Ürün kilidi parça parça:** en az 5 parça, her biri "X DEĞİL" karşıtıyla; "değişirse RED". Üretici gravürü/logosu için silme cümlesi: "yüzey DÜZ: gravür, logo, amblem, harf YOK (Ek 1'deki küçük gravürü SİL)".
- **Başlık satır satır + boy yüzdeyle:** her satır ayrı tırnakta; harf yüksekliği tuval yüzdesiyle (%9–11). Dar grotesk BÜYÜK HARF (D). Türkçe cümlesi her istemde: "büyük harfte i → İ, ı → I; yazım hatası = RED".
- **İnce-uzun ürün:** dike yakın (dikeyden 8–12°), boyu tuvalin %80'i; kalan alanı dev başlık doldurur. Çapraz ürün + ortalı küçük başlık yok.
- **Metin rengi ürünün renginden OLMAZ:** ürün rengi yalnız üründe; yazı nötr (kemik beyazı / koyu), tek vurgu ürünün ikinci tonu ya da nötr.
- **Tek zemin + `duzelt.py zemin`:** model HEX'i ±10 RGB kaydırır; her görsel üretimden hemen sonra betikle sabitlenir.
- **Stil çapası:** `assets/stil-capasi/` karelerinden yalnız tipografi hiyerarşisi ve boşluk ritmi alınır; renk DEVAM KARTI'ndan, ürün Ek 1'den.
- **G2 özellik kartları:** çizgi ikon yok; her kartın üst %60'ında parçanın gerçek makro fotoğrafı, altta etiket + tek satır açıklama; kart zemini ana zeminden bir ton açık.
- **Logo işareti (0.3.6: varsayılan):** yalnız ikon, yazısız, en fazla 1–2 şekil, 32 px'te okunur, düz tek renk, ürünün geometrisinden tek fikir; "transparent background PNG, alfa kanallı". Canlı metin logo yalnız kullanıcı isterse.
- **Gösterilen = teslim edilen:** gösterilmiş görsel kendiliğinden yeniden üretilmez, üstüne yazılmaz; Python işlemi gösterimden önce biter; kullanıcı soru sorarsa yalnız cevap verilir; bir yanıtta en fazla 4 görsel.

## 11. 0.3.6: hazır istem modu (test13, 0.3.5'in gerçek ChatGPT koşusu)
Model istemi kendi yazınca: krem/fuşya pastel zemin, geniş iki renkli başlık, kalan gravür, 9 görsellik kolaj + kırpma, iki bıçağı dişli ürün. Çözüm: istem pakette hazır.
- **Hazır istem:** `gorseller` skill'inde `istemler/` şablonları; model yalnız yer tutucuları DEVAM KARTI'ndan doldurur, gerisini kelimesi kelimesine görsel aracına verir. Kısaltma, özetleme, yeniden yazma yasak. İstem kullanıcıya gösterilmez; isterse dosya.
- **Tek çağrı = tek görsel:** kolaj, ızgara, panel kırpma RED; her görselde ürün fotoğrafı + onaylı G1 yeniden eklenir; önceki görsel düzenlenmez, yeniden üretilir.
- **Zemin/vurgu `marka` adımında:** pembe, pastel ya da açık renkli ürün → koyu nötr zemin (petrol, antrasit, lacivert); vurgu ürünün renginden olmaz; `duzelt.py zemin` her görselde zorunlu.
- **Tipografi adıyla:** başlık "Barlow Condensed SemiBold ya da Oswald benzeri dar grotesk"; Poppins/Montserrat/geniş geometrik = RED; başlık TEK renk, satır satır, harf yüksekliği tuvalin %9–11'i; aynı aile sitenin başlık fontudur (0.4.0, tek yazı sistemi).
- **Girdi fotoğrafı:** üstündeki yazı, logo, zemin ve düzen YOK SAYILIR; gravür silme cümlesi ve parça parça ürün kilidi (parça sayısı, kavis yönü, halka biçimi) banner dahil her şablonda; ürün kenar payı ≥ %6.
- **Kontrol bağlayıcı:** yazım/İ-ı, ürün kilidi, tek zemin, geniş font, yasak öğe, kadraj; ihlal varsa onaya sunmadan 1 kez yeniden üretim (`kabul-kontrolu.md` §2b).
- **Logo varsayılanı:** yalnız ikon, yazısız, şeffaf PNG; canlı metin yalnız kullanıcı isterse.

## 12. 0.4.0: kütüphane v2 ve kanıt tablosu (420 başarılı Shopify markası ölçüldü)
- **G0 feed karesi:** galerinin 1. görseli yazısız, tek ürün; ürünün uzun kenarı tuvalin %75–86'sı (`istemler/g0-feed.md`). Google Merchant Center ana görselde yazı/rozet/logo/kenarlığı yasaklıyor; ölçülen başarılı markaların %68'inin ilk görseli zaten eklenmiş yazısız düz ürün, ürün kareyi medyan %80 dolduruyor. Beyaz zemin şartı yok: galeri zemini kullanılır.
- **Tek yazı sistemi:** görsel başlık ailesi = sitenin başlık fontu (`type_heading_font`, varsayılan `barlow_condensed_n6`).
- **Galeri karışımı (192 kare, gözle):** insanlı %39, düz ürün %28, yazılı grafik kart %27, sahne %7. Bizim insansız grafik kart dilimiz başarılı markalarda nadir (galerisi okunan 172 markanın ≈ %2'si; koyu zeminli kare %16): bu bir farklılaşma tercihidir, ölçülmüş başarı kalıbı değil.
- **Ölçek:** alıcıların %42'si boyutu görselden anlamaya çalışıyor (Baymard): insanlı kare yerine insansız ölçek kartı (ürün + aynı boy cetvel + ölçü sütunları; pazar ABD/İngiltere ise metrik + imperial).

