# Logo · Yalnız ikon, yazısız, şeffaf PNG (hazır istem şablonu, 0.3.6)

**HAZIR İSTEM.** İstemi sen YAZMAZSIN. `İSTEM BAŞI` ile `İSTEM SONU` arasındaki metni al, YALNIZ `{…}` yer tutucularını DEVAM KARTI'ndan doldur, gerisini KELİMESİ KELİMESİNE görsel aracına ver. Kısaltma, özetleme, yeniden yazma YASAK. Tek çağrı = tek işaret. İstemi kullanıcıya gösterme; isterse `.txt` dosyası olarak ver.

- Varsayılan logo budur: **yalnız ikon, yazısız, şeffaf PNG.** Marka adını canlı metin olarak header'a yazdırmak yalnız kullanıcı isterse.
- Ne zaman: Adım 5'in başında, G1'den ÖNCE. 1 işaret üret, göster; kullanıcı beğenmezse `{LOGO_FİKRİ}` değiştirilip en fazla 2 yeni yön.
- Ekler: YOK. Ürün fotoğrafı EKLENMEZ (gerçekçi çizime kayar); bu yüzden bu şablonda ürün kilidi yoktur.
- Onaylı işaret galeri ve banner görsellerine KONMAZ (YASAKLAR: marka adı ya da logo).
- Kontrol (Python): köşe pikseli alfa 0; 32 px'e küçültünce okunuyor; yazı/harf yok; tek renk. İhlal varsa göstermeden 1 kez yeniden üret.
- Teslim: `<marka>-logo.png` (şeffaf) ve aynı işaretten kare `<marka>-favicon.png` (512 px).

## Yer tutucular (yalnız bunlar değişir)
- `{NE_SATIYOR}`: tek satır (ör. `profesyonel pet kuaför makası satıyor (kavisli, dişli makas)`)
- `{LOGO_FİKRİ}`: ürünün geometrisinden TEK fikir cümlesi (ör. `tek bir kavisli yay ve iç kenarında 5 eşit, dikdörtgen diş çentiği`); harf, monogram, soyut blob değil
- `{LOGO_HEX}`: açık ve koyu zeminde de görünen tek ton (ad + HEX); DEVAM KARTI'ndaki logo rengi

=== İSTEM BAŞI ===
Bir marka için YALNIZ İKONDAN oluşan logo işareti tasarla. Yazı, harf, marka adı YOK.
Marka: {NE_SATIYOR}.
FİKİR: {LOGO_FİKRİ}. Tek parça dolu şekil; uçları yuvarlatılmış; kalınlığı eşit.
STİL: Nike, Target, Airbnb, Apple işaretleri gibi düz, tek renk, geometrik, akılda kalan; en fazla 1–2 şekil; 32 pikselde bile okunur; ince çizgi, detay, gölge, degrade, 3B, parlama, doku YOK. Gerçekçi ürün çizimi DEĞİL, illüstrasyon DEĞİL, clipart DEĞİL. Çerçeve, daire, rozet, kalkan içinde DEĞİL.
RENK: tek renk {LOGO_HEX}, düz dolgu.
ÇIKTI: kare 1:1, ŞEFFAF arka plan (transparent background PNG, alfa kanallı); işaret ortada, tuvalin yaklaşık %60'ı; mockup, kartvizit, birden fazla varyasyon YOK. Tek işaret.
=== İSTEM SONU ===
