# Kabul kontrolü ve düzeltme (Adım 5, her görselden sonra)

Bu dosya tek kabul listesidir. Kalibre edilmemiş px puanı ve puan eşikli gösterim kapısı 0.3.0'da kaldırıldı; zevk kararını kullanıcı verir.

## 1. Sıra
1. Görsel gelir → 2. kritik 5 madde → 3. gerekiyorsa kenar/zemin betiği → 4. teslim ölçüsü → 5. kullanıcıya gösterim (§6).
- Her görsel ayrı mesajla üretilir; kolaj gelirse kritik 3 ❌.
- Her prompt orijinal Ref 1'i ek alır. Onaylı görseller ve `assets/stil-capasi/` yalnız stil çapasıdır; ürün her zaman Ref 1'den.

## 2. Kritik (tek ❌ = ret)
1. **Ürün kimliği:** görsel Ref 1 (tedarikçi fotoğrafı) ile yan yana karşılaştırılır: ana renk, ikinci renk, biçim, parça sayısı aynı; renk kayması (ör. mor-yeşil ürün pembe-altın çıkmış) ❌, RED ve yeniden üret. Renk varyantı belirsizse kullanıcıya tek soru. Sadakat listesi birebir; ambalaj rengi ve baskısı Ref 1 ile harf harf aynı; biçim, oran, doku, parça sayısı aynı. Ref 1'de ve promptta olmayan nesne yok (şeffaf tepsi, aksesuar, ikinci ürün, kaide, taş, bitki, insan, el). Tipik bozulmalar: yassı ürün dik duruyor, karton/köpük kalınlığında kenar, yazı ya da labirent benzeri doku, ambalaj yeniden tasarlanmış.
2. **Türkçe yazım ve fazla yazı:** METİNLER'deki metinle karakter karakter aynı (§4). Modelin eklediği slogan, hex, px, stil ya da bölüm adı ❌. Süs çizgisi, numara/sıra etiketi ("DETAY 01"), "detay" kelimesi, büyüteç dairesi, palet dışı renk ya da prompttaki yazı tipi tarifine uymayan başlık ❌ (`tasarim-dili.md` §9).
3. **Kolaj / oran:** tek görsel, istenen en-boy oranı.
4. **Uydurma veri:** doğrulanmamış sayı, yüzde, yıldız puan, rozet, mühür, "klinik", hekim, basın logosu; [DOĞRULA] işaretli bilgi. **Onaysız vaat:** görselde kargo, teslimat, iade, garanti, indirim, kampanya ya da fiyat yazısı ("Ücretsiz kargo" vb.) her zaman ❌; mağaza kuralı olsa bile (`01-kurallar.md` Görsel metni).
5. **Kenara değen ürün / boş kadraj / farklı zemin:** zemin rengi diğer galeri ve banner görselleriyle aynı HEX değilse ❌ (§3). Ürün (ya da kart, yazı) herhangi bir kenara %6'dan yakın ya da kenarda kesik (§3). Ürünün ana öğe olduğu karede (G1, G3, B2 ürün bölgesi, S1–S5) ürün tuvalin hiçbir ekseninde %55'e ulaşmıyorsa ya da ince/uzun ürün çapraz konup kadrajın yarısı boş kalmışsa ❌.

Rapor, görsel başına 1 satır: `G3 ✅ kritik 0 · sadakat 7/7` ya da `G1 ❌ 5: ürün sağ kenarda kesik`. Sonuç yalnız ✅ ya da ❌; ⚠️ ya da "kabul ama" yok. Galeri karelerinde sadakat sayısı her zaman yazılır.

Kritik olmayan sapmalar (parlama, bokeh, degrade, ikinci koyu ton, hizalama, yazı boyu, açı benzerliği) ret değildir: aynı satıra `not: …` olarak yazılır; kullanıcı numarayla isterse yeniden üretilir.

Başlık denetimi (üretimden ÖNCE, METİNLER doldurulurken): G1 başlığı somut fayda mı, 2–5 kelime mi; başka ürüne de yazılabilen soyut başlık ("Kontrollü form.") prompta girmez.

### 2a. 0.3.5 ek kontroller (`ortak-istem-bloklari.md`)
- İstemde üç ortak blok (ÜRÜN KİLİDİ, SİSTEM, YASAKLAR) aynen var mı; G1 dışındaki görselde Ek 2 = onaylı G1 mi. Yoksa gönderme.
- Başlık dar grotesk BÜYÜK HARF mi, satırları istemdeki kırılımla mı, harf yüksekliği G1/bannerda tuvalin ≈ %9–11'i mi (Python ile satır yüksekliğini ölç). İnce, küçük, silik başlık ❌ (kritik 2).
- Metin ya da çizgi ürünün renginde mi (pembe ürün + pembe yazı) ❌. Üretici gravürü/logosu üründe duruyor mu ❌ (kritik 1).
- Tuvalin yarısı boş mu (boş sol yarı, süs yayı) ❌ (kritik 5). G2'de çizgi ikon var mı ❌: kartlarda makro fotoğraf olmalı.
- Logo işareti üretildiyse: köşe alfa 0, yazı yok, 32 px'te okunuyor.
- Gösterilen = teslim edilen: kabul edilip gösterilen dosya sonradan değişmez; yeniden üretim `-v2` adıyla ve yalnız ❌ ya da kullanıcı isteğiyle.

### 2b. 0.3.6 bağlayıcı kontrol listesi (her görsel, gösterimden ÖNCE)
Görseli aç ve tek tek bak; rapor satırına 6 işaret yaz. Tek ❌ = görsel kullanıcıya GÖSTERİLMEZ, onaya sunulmaz: aynı şablonla, `{DÜZELTME}` satırına ret nedeni yazılarak 1 kez yeniden üretilir. İkinci deneme de ❌ ise dur, nedeni tek satırla söyle. Hatayı görüp yine de onaya sunmak YASAK.
1. **Yazım:** her kelime METİNLER ile harf harf aynı; İ/ı, ğ, ş, ç, ö, ü doğru; METİNLER'de olmayan yazı yok (girdi fotoğrafından taşınan yazı dahil).
2. **Ürün kilidi:** parça sayıları ve biçim Ek 1 ile aynı (ör. yalnız BİR bıçak dişli, kavis var, halkalar oval); gravür/üretici logosu yok; banner ve küçük karede de aynı.
3. **Tek zemin:** `duzelt.py zemin` çalıştı; dört köşe hedef HEX; degrade yok.
4. **Font:** başlık DAR grotesk, BÜYÜK HARF, tek renk, satır kırılımı istemdeki gibi. Geniş geometrik (Poppins/Montserrat benzeri), iki renkli başlık, ince ağırlıklı satır ❌.
5. **Yasak öğe:** çizgi ikon, hap etiket, ok, süs çizgisi, dalga, "detay" kelimesi, doğrulanmamış sıfat ("Konforlu Tutuş"), kargo/indirim yazısı, logo ❌.
6. **Kadraj:** tek görsel (kolaj/panel değil); ürün her kenarda ≥ %6 boş zemin, hiçbir kenarda kesik değil.

### 2c. 0.4.0 feed karesi G0 (`istemler/g0-feed.md`; galerinin 1. görseli, `<marka>-urun-0.jpg`)
Google Merchant Center ana görsel kuralı (support.google.com/merchants/answer/6324350): G0'da HİÇBİR yazı, rakam, rozet, logo, kenarlık yok; tek ürün, tek varyant; ürünün uzun kenarı tuvalin %75–86'sı (Google %75–90, bizim %7 kenar kuralıyla üst sınır %86); ≥ 1500 × 1500 px. Ölçüm: `duzelt.py zemin`den sonra zemin dışı piksellerin sınır kutusu / tuval. Tek ❌ = 1 kez yeniden üretim. Galerideki öbür kareler yazılı kalabilir; feed'e yalnız G0 gider. Görsel içi yazının aynısı sayfada HTML'de ya da alt metinde de bulunur (WCAG 1.4.5).

## 3. Kenar ve zemin (Python)
Kenar payı tek değerdir: her kenarda tuval kenarının en az %6'sı boş zemin.
Betiğin yeri (ChatGPT sandbox'ında skill klasörü değişebilir): `find / -name duzelt.py -path "*gorseller*" 2>/dev/null | head -1`; aşağıda `scripts/duzelt.py` bu yolu kasteder. Bulunamazsa skill'deki `scripts/duzelt.py` dosyasını oku ve çalışma klasörüne birebir yaz.
```python
from PIL import Image, ImageChops
im = Image.open("G5.png").convert("RGB"); w, h = im.size
bg = im.getpixel((4, 4))
m = ImageChops.difference(im, Image.new("RGB", im.size, bg)).convert("L").point(lambda v: 255 if v > 18 else 0)
x0, y0, x1, y1 = m.getbbox()
pay = min(x0 / w, y0 / h, (w - x1) / w, (h - y1) / h)
print("en küçük pay: %.3f" % pay, "KRİTİK 5 ❌" if pay < 0.06 else "✅")
```
- İçerik kenara değmiyor ama pay %6'dan azsa ve zemin düzse (köşeler ±3 RGB): `python scripts/duzelt.py kenar <girdi> <çıktı> <oran>` içeriği merkezden küçültür, kenarı zemin rengiyle doldurur. Oran `s = (1 − 2·0,06) / (1 − 2·m_min)`; m_min ölçülen en küçük pay (oran olarak). Ör. m_min 0,04 → s = 0,957. Betikten sonra yeniden ölç.
- Ürün kenarda kesikse betik kullanılmaz: yeniden üret.
- **Zemin hilesi:** görsel zemini, konacağı yüzeyin hex'inden ±3 RGB dışındaysa `python scripts/duzelt.py zemin <girdi> <çıktı> <#hex>`. Betik RED verirse (ürün kenara değiyor) yeniden üret.
- **Arka plan = bölüm zemini (0.4.1):** siteye konan ürün/kutu görselinin köşe HEX'i, konduğu bölümün zemin HEX'iyle birebir aynı değilse ❌ (kaydırınca görsel kenarı kutu gibi görünür). Düzeltme: `duzelt.py zemin`; RED verirse önce `duzelt.py kenar` ile kenar boşluğu, sonra yeniden `zemin`.
- **Yapay zekâ büyütme (0.4.1):** yazılı görselde Real-ESRGAN ve benzeri kullanılmaz (ince yazı içi boş çift çizgili harfe dönüyor); Lanczos ile ölçekle ya da yüksek çözünürlükte yeniden üret. Harfleri içi boş/çift çizgili görsel ❌.
- **Tek zemin HEX'i (0.3.4):** G1–G8, B1 ve B2 aynı zemin HEX'indedir (DEVAM KARTI "görsel zemini"). Her galeri ve banner görseli üretimden sonra köşe rengi ölçülür ve `duzelt.py zemin` ile o HEX'e sabitlenir. Zemini başka renkte gelen (koyu, renkli, bölünmüş) ve betikle sabitlenemeyen görsel RED: kritik 5 ❌, yeniden üret.

## 4. Türkçe metin: OCR + göz kontrolü
- OCR aracı varsa çalıştır; sonuç ne olursa olsun göz kontrolü ZORUNLU (OCR İ/ı ayrımını sık kaçırır).
- Metin bölgesini Python ile kırp, 2× büyüt, harf harf oku; METİNLER'deki metinle karakter karakter karşılaştır.
- Bak: **İ** (noktalı büyük) ↔ I · **ı** (noktasız küçük) ↔ i · ş, ğ, ç çengelleri · ü, ö noktaları · büyük harf satırında İ ("ÖZELLİKLER", "KUTU İÇERİĞİ") · '·' ayraç · ondalık virgül ("7,5 cm") · noktalama.
- Ambalaj baskısı Ref 1 ile harf harf aynı olmalı.
- Hata → yalnız o görsel yeniden üretilir. Kod yalnız tek harfi düzeltmek için kullanılabilir; başlığı ya da görseli kodla yeniden çizmek yok.

## 5. Yeniden üretim
- Yalnız reddedilen görsel; orijinal Ref 1'den; aynı prompt + DÜZELTME paragrafının altına ret nedeni satırı. Üretilmiş görseli düzenleyerek türetme yok.
- Turda tek değişken. Aynı görsel 2 denemede düzelmezse dur ve kullanıcıya söyle.
- Kabul edilenler teslim ölçüsüne getirilir: banner masaüstü 1920×800, mobil 1080×1350; galeri 1:1.

## 6. Kullanıcıya gösterim
- Kritik ✅ olan her görsel gösterilir; puan eşiği yok. Görselin altına rapor satırı.
- Bitince (`adim-5-gorsel-uretimi.md` son satırı) tek liste: dosya adı · ölçü · rapor satırı. Kullanıcı numara yazarsa o görsel yeniden üretilir; "devam" onaydır.
- Onaylanan görsellerin adları DEVAM KARTI'nın "Görseller" satırına yazılır; onaylı G1 sonraki bütün promptlara stil çapası (Ek 2) olur.
