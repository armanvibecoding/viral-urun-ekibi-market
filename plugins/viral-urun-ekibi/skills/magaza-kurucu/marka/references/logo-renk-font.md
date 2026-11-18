# Logo brifi, renk ve font

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 71, 97, 124, 144, 264–265, 441–443. 0.3.0: logo üretimi kapandı, yerine brif + canlı metin logo + yükleme yuvası (eski kurallar repo `docs/ESKIDI.md`). Renk rolleri ve font listesi `01-kurallar.md` → TEMA KISITLARI'nda.

---

- Marka kimliği: renk paleti (5 HEX, kontrast kontrolü yapılmış), body fontu (listeden), ses tonu, slogan; rakiplerden ayrışma 1 satır
- Görsel kilidi (0.3.4): 5 HEX ve görsel başlık yazı tipi tarifi (A/B + 1 satır tarif, ör. "dar, yüksek kontrastlı serif, Regular 400") bu adımda seçilip DEVAM KARTI'na yazılmadan `gorseller` adımı görsel üretmez; DEVAM KARTI'na ayrıca "Görsel zemini: #HEX" yazılır: bütün galeri ve banner görsellerinin tek zemini (`tasarim-dili.md` §9–10).
- Görsel kilidi (0.3.5): görsel zemini açık ya da koyu olabilir; açık/pastel ürün açık pastel zemine konmaz, koyu zemin seçilir. Görsel metni ve vurgu ürünün renginden olmaz. Görsel başlık varsayılanı D: dar grotesk BÜYÜK HARF SemiBold; serif (A) yalnız kullanıcı isterse.
- Görsel kilidi (0.3.6, test13: krem zemin + fuşya vurgu pembe ürünü yuttu): zemin/vurgu kararı BU adımda verilir. Ürünün baskın rengi pembe, pastel ya da açık (beyaz, bej, krem) ise görsel zemini KOYU nötr tek HEX'tir (ör. petrol #0F2B2E, antrasit #1E2226, lacivert #14213D); krem/pastel zemin yalnız koyu üründe. Vurgu ürünün baskın renginden OLMAZ (pembe ürün → fuşya/vişne vurgu YOK): ürünün ikinci tonu (ör. altın) ya da nötr. Görsel metni koyu zeminde kemik beyazı, ikincil metin soluk gri. Görsel başlık fontu adıyla yazılır: "Barlow Condensed SemiBold ya da Oswald benzeri dar grotesk"; Poppins/Montserrat/geniş geometrik = RED. Görsel ↔ site tek yazı sistemi (0.4.0): aynı aile sitenin başlık fontu olur (`type_heading_font`). DEVAM KARTI'na "Tipografi" satırı: `Başlık: Barlow Condensed 600 · barlow_condensed_n6 | Gövde: Inter 400 · inter_n4` ve "Görsel renkleri" satırı: zemin, metin, ikincil metin, kart (zeminin bir ton açığı), vurgu HEX + ürün rengi adı. `gorseller` adımında `duzelt.py zemin` her görselde zorunlu.

## Logo: üretim değil, brif
- **Varsayılan (0.3.6): yalnız ikon, yazısız, şeffaf PNG.** `gorseller` adımında hazır şablonla (`istemler/logo-ikon.md`) ChatGPT görsel aracıyla üretilir: en fazla 1–2 şekil, 32 px'te okunur, düz tek renk (Nike/Target/Airbnb gibi), ürünün geometrisinden tek fikir cümlesi, "transparent background PNG, alfa kanallı"; ürün fotoğrafı eklenmez; kodla çizilmez. Bu adımda yalnız fikir cümlesi + logo HEX'i (açık ve koyu zeminde görünen tek ton) seçilip DEVAM KARTI'na yazılır.
- **Canlı metin logo yalnız kullanıcı isterse:** o zaman logo ayarı boş kalır; tema header'da mağaza adını canlı metin olarak yazar.
- **Yükleme yuvası:** kullanıcının logosu varsa `<marka>-logo.png` (şeffaf PNG; koyu zemin sürümü varsa o da) ve `<marka>-favicon.png` adıyla sohbete ekler ya da Admin › İçerik › Dosyalar'a yükler; `shopify-kurulum` T10'da ayara bağlar. Yalnız ikon (yazısız) yüklenirse tema header'da mağaza adını göstermez: bunu kullanıcıya tek satırla söyle.
- **Brif (yalnız kullanıcı tasarımcıya yaptırmak isterse):** kullanıcıya Markdown madde listesi olarak verilir, kod bloğunda DEĞİL (tasarımcı ya da vektör araç için). Aşağıdaki şablon alanları ve sırayı tanımlar:
```
LOGO BRİFİ — <marka adı>
Ürün: <1 satır>  ·  Pazar: <ülke>  ·  Ses tonu: <2–3 kelime>
İşaret: ürünle ilgili tek işaret; ürünün biçiminden, dokusundan ya da kullanım anından türer
        (soyut geometri, hap, uygulama ikonu karosu, harf monogramı değil)
Biçim: yalnız ikon, yazısız; tek renk düz; gradyan, gölge, çerçeve yok
Renk: <metin HEX> (açık zeminde) · ters sürüm <arka plan HEX> (koyu zeminde)
Teslim: SVG + şeffaf PNG (1024 px) + favicon kare 512 px (32 px'te okunur)
Kaçın: rakip işaretlerine benzerlik (<3 rakip adı>), ince detay, birden fazla fikir
Referans: beğendiğin 2–3 logo örneğini ekle (yoksa tasarımcıdan 3 yön iste)
Not: yalnız ikon yüklenirse header'da mağaza adı görünmez; ad için ikon + yazı kilidi de iste.
```

## Dosya adları ve ayarlar
| Logo (varsayılan: `gorseller` adımında üretilen yalnız ikon, şeffaf PNG; ya da kullanıcının dosyası) | `<marka>-logo.png` | ayar `logo` (koyu zemin sürümü varsa `logo_inverse`); dosya yoksa boş kalır, header mağaza adını canlı metin yazar |
| Favicon (isteğe bağlı; kullanıcı yükler; kare, ≥ 32 px) | `<marka>-favicon.png` | ayar `favicon`; dosya yoksa boş kalır |

| `color_palette.background` / `.foreground` / `.color1` / `.color2` / `.color3` | Arka plan / Metin / Ana / İkincil (AÇIK yüzey) / Vurgu, `#RRGGBB` (kontrast kontrolünden sonra; metin/ikincil ≥ 7:1) |
| `type_heading_font` + `type_accent_font` | Görsel başlık ailesiyle aynı (0.4.0): varsayılan `barlow_condensed_n6` |
| `type_body_font` + `type_subheading_font` | Aynı aile: `<aile>_n4` + `<aile>_n5` (varsayılan `inter_n4`, `inter_n5`) |
| `logo`, `logo_inverse`, `favicon` | `shopify://shop_images/<dosya>`; dosya yoksa yazılmaz |
