# Tarif 06 — Trendyol ve AliExpress avı

## Amaç
TR pazarında satılabilir ürün bulmak: Trendyol'da kanıtlanmış ama henüz viral olmamış, AliExpress'ten temin edilebilir ürünler. Çıktı: **N SAT bulana kadar** (varsayılan N=5) yalnız SAT'lı Excel + tek gerekçeli öneri.

## Girdi
Niş/ilgi alanı ipuçları (yoksa viral-DNA'dan) · TR oran tablosu (`hunter/trendyol/referans/tr-oranlari.tsv`; boşsa tarif tur 0: "oran turu") · açık macOS Chrome (giriş yok, salt-okuma).

## Adımlar
0. **Oranlar:** `tr-oranlari.tsv` kaynaklı varsayılanlarla dolu (KDV, sanal POS, kargo, iade, reklam payı; kapıda ödeme 0). Oran turu yalnız kullanıcı kendi oranını verdiğinde ya da kayıt eskidiğinde yinelenir; kaynak sırası kullanıcı > kaynaklı > varsayım. Uydurma oran yazılmaz.
0b. **Tohum:** ilk turda en az 5 farklı niş, niş başına ≤ 5 aday.
1. Aday toplama: Trendyol arama/liste sayfalarından aday ürünler. **Arama kartı yetmez**: ürün SAYFASINA gir, yorum sayısı, puan, fiyat, satıcı, varyantları oradan oku.
2. Estetik filtre: görünüşü ucuz/estetiği zayıf ürünler elenir (ör. sıradan telefon standı tipi, plastik/jenerik görünüm). Soru: "Bu ürünün videosu ilk 2 saniyede dikkat çeker mi, fotoğrafı pahalı durur mu?" Hayırsa ELE, gerekçesiyle.
3. AliExpress tedarik (`alis_tl` KAYNAĞI; Trendyol fiyatı alış değil hedef satış/rakip fiyatıdır, `rakip_tl`): ürün sayfasında "This seller: N | Total sales: M" ayrımı — **satıcının** satışı (N) ile **ürünün toplam** satışı (M) ayrı yazılır; sayfanın altındaki öneri/benzer ürün bölümündeki sayılar ALINMAZ. Fiyat ve kargo sayfadan, 1-1 aynı ürün olduğu görselle doğrulanır.
4. Marj: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/hunter/trendyol/scripts/tr_marj.py" …` (oran tablosu doluysa).
5. Viral kontrolü: ürün zaten viral mi (analiz.db + Meta Reklam Kütüphanesi; Instagram/TikTok salt-okuma). Instagram/TikTok giriş istiyorsa `dogrulanamadi-giris` + risk notu yazılır, SAT'ı engellemez; Meta de yapılamazsa engel değil, kart notu (viral veritabanı yokken vekil: Meta reklam sayısı + satıcı sayısı).
6. **Sınama 3/3:** her SAT adayı için 3 bağımsız kontrol (talep var · tedarik/marj tutuyor · viral değil/çürütülemedi); 3/3 geçmeyen SAT olamaz.
7. Karar: **SAT** (3/3; okunamayan ölçüt engel değil, `neden` sütunu "Kontrol et: …" yazar) ya da **ELE** (yalnız kanıtlı engel). İZLE ve "SAT (koşullu)" yok; kullanıcıya yalnız SAT gider.
8. 5 niş × 5 ürün tablosu → `ortak/excel_yaz.py` (tarif 07).
9. Rapor: yalnız SAT ürünleri (`trendyol_kontrol.py ozet`); N'e ulaşılamazsa tek satır "k SAT buldum, sebep: …"; son satır: "Ben olsam: <SAT ürün> — <1 gerekçe> — risk: <1 risk>" (SAT varsa).

Pazar: bu tarif TR içindir; TR verisi zayıf (1 milyon kayıt), eşikler `esikler.tsv`'de `deneme`/`varsayim` durumunda ve ilk 20 üründen sonra kalibre edilir. ABD/AB ürün avı için `radar`/`hunter`.

## Kalite çıtası
5 niş × 5 ürün (eksik niş belirtilir) · her satırda ürün sayfası linki · satış sayıları ürün sayfasından (arama kartından değil) · AliExpress satıcı/toplam ayrımı yazılı · öneri bölümü sayısı yok · her kararda gerekçe · uydurma oran/sayı yok.

## Kapılar
`hunter/trendyol/scripts/trendyol_kontrol.py` 0 · `excel_yaz.py` doğrulaması 0 · `hunter/trendyol/scripts/kirma_testi.py` 0.

## Sık hata ve düzeltmesi
- Arama kartındaki "1B+ satış" ile ürün sayfası farklı → sayfadakini yaz.
- AliExpress'te "Total sales" satıcı sanıldı → iki sayıyı ayrı sütunda tut.
- SAT çıkmıyor → ELE sebeplerine bak (`ELE sebebi:` notları); okunamayan ölçüt zaten engel değil; eşiği gevşetme, N'e ulaşana kadar aramaya devam et ya da "k SAT buldum, sebep: …" de.

## Bitti tanımı
Excel + 1 tek öneri; her SAT için 3/3 kanıtı dosyada; DURUM.md güncel.
