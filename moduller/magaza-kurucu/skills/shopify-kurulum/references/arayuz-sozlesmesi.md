# Arayüz sözleşmesi (sürüm 2): ekibin kolları arasında dosya alışverişi

Ekibin ürün kolu, mağaza kolu ve video kolu arasındaki tek bağ üç JSON dosyasıdır. Proje klasöründe yeri `is/NN-urun/magaza/`; ChatGPT'de sohbete eklenir. İki yüzeyde aynı biçim. Alan adları değişmez; yeni alan eklenirse `surum` artar, eski alan silinmez. Makine şeması ve betik: eklenti kökünde `sozlesme/sema.json`, `sozlesme/paket.py` (`dogrula`, `urun-yaz`, `magaza-oku`, `iddia-kontrol`, `video-yaz`, `video-sec`). Kullanım sırası: `ekip-koprusu.md`.

## Girdi: `urun-paketi.json` (ürün kolu üretir; isteğe bağlı)
Kullanıcı fotoğraf + ülke yerine bu dosyayı verirse `urun-analiz` onu okur, yalnız eksik alanları araştırır. Dosyadaki bilgi "doğrulanmış" sayılmaz; `kaynak` alanı olan özellik doğrulanmış sayılır.

| Alan | Tür | Not |
|---|---|---|
| `surum` | "1" ya da "2" | `teklif` alanı sürüm 2 ile geldi |
| `urun.ad` | metin | tedarikçideki ad |
| `urun.nis` | metin | `nis-guzellik`, `nis-gadget`, `nis-ev`, `nis-moda`, `nis-saglik`, `nis-pet` (TEKNİK EK T4.3); ürün kolunun niş kodu `sozlesme/nis-esleme.tsv` ile çevrilir |
| `urun.fotograflar` | liste | dosya adı ya da URL; ilki Ek 1 adayı |
| `urun.ozellikler` | liste | `{ "ad": "uzunluk", "deger": "120", "birim": "mm", "kaynak": "<URL>" }` |
| `urun.varyantlar` | liste | `{ "ad": "Siyah", "stok": true }` |
| `urun.tedarik_fiyati` | nesne | `{ "tutar": 11.4, "para": "USD" }` |
| `pazar` | nesne | `{ "ulke": "US", "dil": "en", "para": "USD" }` (ülke ISO 3166: İngiltere `GB`) |
| `rakipler` | liste | `{ "marka", "url", "fiyat" }` |
| `kanit` | liste | reklam/satış kanıtı: `{ "kaynak": "Meta Ads Library", "url", "tarih", "olcu": "aktif reklam 90+ gün" }` |
| `teklif` | nesne (sürüm 2) | `{ "kaynak": "teklif.tsv" ya da "sabit-kural", "fiyat", "para", "paketler": [{ "adet": 2, "indirim_yuzde": 10 }], "garanti", "kargo_vaadi" }`. Fiyatın TEK kaynağı: `teklif.tsv` ise onaylı değerdir; `sabit-kural` ise fiyatı `urun-analiz` önerir, paket 2'li %10, 3'lü %18 |

## Çıktı: `magaza-paketi.json` (`shopify-kurulum` sonunda üretilir)
DEVAM KARTI'nın makine okunur hâli. Video kolu altyazı, kapak ve son kareyi bununla mağazayla aynı sistemde kurar: aynı yazı ailesi, aynı renkler, yalnız onaylı iddialar.

| Alan | Örnek | Video tarafında kullanım |
|---|---|---|
| `surum` | "2" | |
| `marka` | `{ "ad", "slogan", "ses": { "sifatlar": [3], "degil": [3] } }` | seslendirme ve altyazı tonu |
| `renkler` | `{ "zemin": "#1E2226", "metin": "#F2F2EE", "ikincil": "#A9ADB2", "kart": "#2A2F34", "vurgu": "#E0B04A" }` | altyazı kutusu, kapak, son kare |
| `tipografi` | `{ "baslik": { "aile": "Barlow Condensed", "agirlik": 600, "handle": "barlow_condensed_n6", "buyuk_harf": true }, "govde": { "aile": "Inter", "handle": "inter_n4" } }` | altyazı ve kapak yazısı (Google Fonts'ta da aynı adla var) |
| `logo` | `{ "dosya": "<marka>-logo.png", "tur": "ikon" }` | son kare |
| `urun` | `{ "baslik", "handle", "url", "fiyat", "para", "varyantlar" }` | link, CTA |
| `onayli_metinler` | `{ "faydalar": [3], "g1_baslik": [...], "b2": {...}, "iddialar": [{ "metin", "kaynak", "bilgi_notu": true/false }] }` | yalnız bunlar söylenir; listede olmayan iddia videoya girmez (kapı: `paket.py iddia-kontrol`) |
| `gorseller` | `[{ "kod": "G0", "dosya": "<marka>-urun-0.jpg", "olcu": "1500x1500", "yazisiz": true }, …]` | G0 temiz ürün karesi video için ürün referansıdır |
| `magaza` | `{ "alan_adi", "tema_id", "pdp_url", "utm": "utm_source=<kanal>&utm_medium=video&utm_campaign=<marka>-<urun>", "tema_modu": "tam" ya da "temasiz" }` | reklam linki |

## Geri dönüş: `video-paketi.json` (video kolu üretir; isteğe bağlı)
`[{ "dosya", "olcu": "1080x1920", "sure_sn", "kullanim": "pdp-galeri|hero|reklam", "altyazi_dili" }]`. `shopify-kurulum` yalnız `pdp-galeri` ve `hero` olanları yükler: ürün videosu galerinin son sıralarına girer, G0'ın yerini almaz (feed görseli yazısız fotoğraftır; video "ölçek" karesinin yerini tutmaz, KANIT 1.2).

## Kurallar
- Sözleşme dışı alan okunmaz, yazılmaz. Eksik zorunlu alan varsa kullanıcıya tek satırla söylenir, uydurulmaz.
- Para, fiyat ve onaylı metin dosyadan birebir taşınır (DEVAM KARTI kuralı).
- Başka kolun görselini ya da metnini mağaza kolu yeniden üretmez; yalnız kendi kapılarından (yazım, ürün kilidi, feed kuralı) geçirir.
