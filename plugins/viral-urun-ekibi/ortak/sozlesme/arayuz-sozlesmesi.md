# Arayüz sözleşmesi (0.4.0, şema 0.4.2): öbür plugin'lerle dosya alışverişi

Mağaza Kurucu tek başına da çalışır. Ürün bulan ve video yapan plugin'lerle birleşince aradaki tek bağ iki JSON dosyasıdır. Dosya ChatGPT'de sohbete eklenir, Claude'da yol olarak verilir; iki yüzeyde aynı biçim. Alan adları değişmez; yeni alan eklenirse `surum` artar, eski alan silinmez.

## Girdi: `urun-paketi.json` (ürün bulan plugin üretir; isteğe bağlı)
Danışman fotoğraf + ülke yerine bu dosyayı eklerse `urun-analiz` onu okur, yalnız eksik alanları araştırır. Dosyadaki bilgi "doğrulanmış" sayılmaz; `kaynak` alanı olan özellik doğrulanmış sayılır.

| Alan | Tür | Not |
|---|---|---|
| `surum` | "1" | zorunlu |
| `urun.ad` | metin | tedarikçideki ad; zorunlu |
| `urun.nis` | metin | `nis-guzellik`, `nis-gadget`, `nis-ev`, `nis-moda`, `nis-saglik` … (TEKNİK EK T4.3) |
| `urun.fotograflar` | liste | dosya adı ya da URL; ilki Ek 1 adayı; en az 1 (zorunlu) |
| `urun.ozellikler` | liste | `{ "ad": "uzunluk", "deger": "120", "birim": "mm", "kaynak": "<URL>" }` |
| `urun.varyantlar` | liste | `{ "ad": "Siyah", "stok": true }` |
| `urun.tedarik_fiyati` | sayı + para birimi | `{ "tutar": 9.4, "para": "USD" }` |
| `pazar` | nesne | `{ "ulke": "US", "dil": "en", "para": "USD" }`; `ulke` zorunlu |
| `rakipler` | liste | `{ "marka", "url", "fiyat" }` |
| `kanit` | liste | reklam/satış kanıtı: `{ "kaynak": "Meta Ads Library", "url", "tarih", "olcu": "aktif reklam 90+ gün" }` |

## Çıktı: `magaza-paketi.json` (`shopify-kurulum` sonunda üretilir)
DEVAM KARTI'nın makine okunur hâli. Video yapan plugin altyazı, kapak ve son kareyi bununla mağazayla aynı sistemde kurar: aynı yazı ailesi, aynı renkler, yalnız onaylı iddialar.

| Alan | Örnek | Video tarafında kullanım |
|---|---|---|
| `surum` | "1" | |
| `marka` | `{ "ad", "slogan", "ses": { "sifatlar": [3], "degil": [3] } }` | seslendirme ve altyazı tonu |
| `renkler` | `{ "zemin": "#1E2226", "metin": "#F2F2EE", "ikincil": "#A9ADB2", "kart": "#2A2F34", "vurgu": "#E0B04A" }` | altyazı kutusu, kapak, son kare |
| `tipografi` | `{ "baslik": { "aile": "Barlow Condensed", "agirlik": 600, "handle": "barlow_condensed_n6", "buyuk_harf": true }, "govde": { "aile": "Inter", "handle": "inter_n4" } }` | altyazı ve kapak yazısı (Google Fonts'ta da aynı adla var) |
| `logo` | `{ "dosya": "<marka>-logo.png", "tur": "ikon" }` | son kare |
| `urun` | `{ "baslik", "handle", "url", "fiyat", "para", "varyantlar" }` | link, CTA |
| `onayli_metinler` | `{ "faydalar": [3], "g1_baslik": [...], "b2": {...}, "iddialar": [{ "metin", "kaynak", "bilgi_notu": true/false }] }` | yalnız bunlar söylenir; listede olmayan iddia videoya girmez |
| `gorseller` | `[{ "kod": "G0", "dosya": "<marka>-urun-0.jpg", "olcu": "1500x1500", "yazisiz": true }, …]` | G0 temiz ürün karesi video için ürün referansıdır |
| `magaza` | `{ "alan_adi", "tema_id", "pdp_url", "utm": "utm_source=<kanal>&utm_medium=video&utm_campaign=<marka>-<urun>" }` | reklam linki |

## Geri dönüş: `video-paketi.json` (video plugin'i üretir; isteğe bağlı)
`[{ "dosya", "olcu": "1080x1920", "sure_sn", "kullanim": "pdp-galeri|hero|reklam", "altyazi_dili" }]`. `shopify-kurulum` yalnız `pdp-galeri` ve `hero` olanları yükler: ürün videosu galerinin son sıralarına girer, G0'ın yerini almaz (feed görseli yazısız fotoğraftır; video "ölçek" karesinin yerini tutmaz, KANIT 1.2).

## Makine okunur şema, örnek, doğrulama (0.4.2)
Bu dosyanın yanındaki `sozlesme/` klasörü sözleşmenin tek kaynağıdır ve iki plugin'de bayt bayt aynıdır (`OZET.json` = dosya özetleri):
- `sozlesme/urun-paketi.schema.json`, `magaza-paketi.schema.json`, `video-paketi.schema.json`: zorunlu alan, tür ve biçim buradan okunur (tablolarla çelişirse şema geçerlidir).
- `sozlesme/ornek/`: üç dosyanın geçerli örneği (aynı ürün, uçtan uca).
- `sozlesme/paket_dogrula.py` (yalnız standart Python; kod aracında çalışır, yol tutmazsa `find / -name paket_dogrula.py`):
  - gelen dosya okunmadan ÖNCE: `python paket_dogrula.py urun <dosya>` (ya da `video <dosya>`),
  - `magaza-paketi.json` yazıldıktan SONRA: `python paket_dogrula.py magaza <dosya>`,
  - üçü birlikte: `python paket_dogrula.py zincir <urun> <magaza> [<video>]` (para birimi, varyant, altyazı dili tutarlılığı).
- HATA varsa dosya kullanılmaz ve teslim edilmez: hata satırı danışmana tek satırla söylenir. UYARI engel değildir. Kod aracı yoksa şema elle uygulanır ve "doğrulayıcı çalıştırılmadı" denir.

## Dosya yerleri
- ChatGPT / claude.ai: dosya sohbete eklenir; çıktı indirilebilir dosya olarak verilir.
- Claude Code (iki plugin aynı klasörde): `is/NN-urun-adi/urun-paketi.json` → `is/NN-urun-adi/magaza-paketi.json` → `is/NN-urun-adi/teslim/video-paketi.json`. `is/` yoksa çalışma klasörünün kökü.

## Kurallar
- Sözleşme dışı alan okunmaz, yazılmaz. Eksik zorunlu alan varsa danışmana tek satırla söylenir, uydurulmaz.
- Para, fiyat ve onaylı metin dosyadan birebir taşınır (DEVAM KARTI kuralı).
- Başka plugin'in görselini ya da metnini Mağaza Kurucu yeniden üretmez; yalnız kendi kapılarından (yazım, ürün kilidi, feed kuralı) geçirir.
