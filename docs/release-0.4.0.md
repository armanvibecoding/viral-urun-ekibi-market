# Sürüm 0.4.0 — yayın notu

Tarih: 2026-11-23 · Eklenti sürümü 0.4.0 · Mağaza modülü 0.6.0

## Kullanıcıya görünen değişiklikler

1. **Beceriler kod adı aldı:** Captain, Radar, Spy, Hunter, Builder, Studio, Cut. Eski beceri adları (8 tane; liste `ortak/ad-haritasi.tsv`'de ve CHANGELOG'un "Kaldırılacak" bölümünde) bu sürümde yönlendirme olarak çalışır; 0.5.0'da kalkar. Eski ajan adları çalışmaz; oturum başında harita (`ortak/ad-haritasi.tsv`) uyarısı gelir.
2. **Yeni beceri Bazaar:** Trendyol'da ilgi gören, henüz viral olmamış ucuz ürünü bulur; günlük tavanlı yalnız-oku tarama, net marj, tedarik ve fiyat şeffaflığı riski. Eşiklerin yarısı varsayımdır (ilk 20 üründe karar DENEME); `tr-oranlari.tsv` değerleri boş açılır, kurucu doldurur.
3. **Tek Excel şablonu:** Radar, Spy, Hunter, Bazaar aynı 3 sayfalı, 10 sütunlu dosyayı üretir. Radar Excel'inden Marka Skorları, Rakip & Notlar ve Özet sayfaları çıktı (`.md` dosyalarında duruyor).
4. **Mağaza 3 aşama:** ① Plan (araştırma, teklif, marka, site metinleri) · ② Görseller · ③ Site. Adım sayısı 8 → 9; site metinleri artık görsellerden önce yazılır, görsel metinleri Aşama 1'de kilitlenir. Teklif ayrı beceri olmaktan çıktı, Builder'ın `teklif` bölümü oldu.
5. **Kadro 27 → 17 ajan:** mağaza rolleri 20 → 10 (Atlas, Muse, Copy, Forge, Sentinel, Panel, Director, Architect, Probe, Shopper); ürün ve video rolleri 7 (Scout, Skeptic, Decoder, Story, Jury, Fixer, Mixer). Kör jüri ve kök neden rolleri ayrı kaldı. Birleşen rollerin brief'inde `mod:` satırı zorunludur.

## Geriye uyumluluk

| Ne | Durum |
|---|---|
| `/viral-urun-ekibi:<eski beceri adı>` | çalışır (yönlendirme) |
| `.ekip/` ve `is/` dosyaları, `urun-paketi.json` vb. (`surum` "2") | aynen okunur |
| Eski DEVAM KARTI (`Düzen` satırı yok) | çalışır: karttaki "Sıradaki" bölümden devam, eski adım numarası çevrilir |
| `is/kesfet/kesfet-urunler.xlsx` | aynı yol, yeni düzen |
| ChatGPT paketi | yeni ZIP eskisinin yerine yüklenir; yönlendirmeler pakette yok |

Güncelledikten sonra oturumu yeniden başlat (eski sürüm önbelleği iki ad kümesini birlikte gösterebilir).

## Ölçülmeyenler ve bilinen sınırlar

- Yönlendirme dosyalarındaki `disable-model-invocation` alanı `claude plugin validate` ile geçti; gerçek çalışma davranışı (modelin listesinden çıkma) ayrıca ölçülmedi.
- Bazaar eşikleri 5 ürünlük elle denemeden ve varsayımlardan gelir; Trendyol'da tarama temposu ölçülmedi.
- Kurucunun bilgisayarındaki yerel ajan kopyaları (`firsat-avcisi-mcp`, `kanit-savcisi-mcp`) depo dışıdır, eski adla kalır: `scout-mcp`, `skeptic-mcp` olarak yeniden adlandırılacak (Captain'e ayrı iş).

## Yayın adımları (kurucu onayıyla; bu belge yayın yapmaz)

1. `sh scripts/paketle.sh` → `dist/viral-urun-ekibi-CLAUDE-v0.4.0.zip`, `dist/viral-urun-ekibi-CHATGPT-v0.4.0.zip`.
2. Dal birleştirme, etiket ve Releases yüklemesi kurucu kararıdır.
