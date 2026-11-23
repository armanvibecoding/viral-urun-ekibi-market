# teklif.tsv şeması

Ne zaman okunur: rakip sayfası okunurken ve `bizim` satırı yazılırken. Başlık: `assets/teklif.tsv` (sekmeyle ayrılmış).
Denetim: `teklif_kontrol.py sema` — eksik sütun, bilinmeyen değer, kanıtsız çizili fiyat, `bizim` satırında yasak ifade → çıkış 1.

| Sütun | Ne yazılır | Kural |
|---|---|---|
| `tur` | `rakip` (gözlem) · `bizim` (tasarım) | zorunlu |
| `tarih` | okuma/tasarım günü `YYYY-AA-GG` | zorunlu (fiyatlar gün içinde oynar) |
| `pazar` | `US` `TR` `UK` `DE` `FR` `ES` | zorunlu |
| `urun` | kısa ürün adı | zorunlu |
| `kaynak_url` | rakip iniş sayfası | `rakip`'te http(s) zorunlu · `bizim`'de `-` |
| `para` | US USD · TR TRY · UK GBP · DE/FR/ES EUR | pazarla uyuşmalı |
| `fiyat` | tekli satış fiyatı (KDV dahil gösterilen) | sayı > 0 |
| `karsilastirma_fiyati` | üstü çizili fiyat | `yok` ya da fiyattan **büyük** sayı |
| `karsilastirma_kaniti` | çizili fiyatın gerçek olduğuna kanıt (ör. "2026-10-01..30 arası 49,90 satıldı, sipariş kaydı") | `bizim` + çizili fiyat varsa zorunlu |
| `paket` | `1x` · `2x:-15%` · `3x:-25%` · `bundle:<ne>` (`;` ile) | boş olamaz (`yok`/`gorulmedi`) |
| `garanti` | `30 gün para iadesi` · `koşulsuz iade 14 gün` … | boş olamaz |
| `kargo_vaadi` | `ücretsiz` · `ücretsiz>50` · `kargo dahil` · teslim günü | boş olamaz |
| `odeme_yontemleri` | `;` ile: `kart` `kapida` `havale` `taksit` `paypal` `klarna` `afterpay` `shop_pay` `apple_pay` `google_pay` `fatura` `bizum` `diger` · ya da `gorulmedi` | bilinmeyen değer → hata |
| `sosyal_kanit_turu` | `;` ile: `yok` `gercek_yorum_uygulamasi` `alici_foto` `alici_video` `ugc_izinli` `basin` `sertifika` `satis_sayaci` `uydurma_supheli` · ya da `gorulmedi` | `uydurma_supheli` yalnız `rakip`'te |
| `aciliyet` | `rakip`: gördüğün aynen (ör. "geri sayım 10 dk, son 3 ürün") · `bizim`: `yok` ya da `kampanya_bitis:YYYY-AA-GG` | `bizim`+TR → yalnız `yok` |
| `itiraz_yanitlari` | sayfada cevaplanan itirazlar (`;` ile kısa: "beden?; kargo süresi?; iade?") | boş olamaz |
| `upsell` | sepette/ödemede/teşekkür sayfasında ek teklif | boş olamaz |
| `ilk_ekran` | ilk ekranda ne var (video/gif/foto/fayda başlığı) | boş olamaz |
| `not` | serbest; yorum uygulaması adı + görünen sayı, SSS var mı | — |

**Gözlem ve tasarım ayrımı:** yasak ifade taraması yalnız `bizim` satırına uygulanır. Rakibin "son 3 ürün"ünü yazmak gözlemdir,
kendi teklifine koymak ihlaldir. `gorulmedi` = sayfada aradım bulamadım; `yok` = sayfada açıkça yok.
