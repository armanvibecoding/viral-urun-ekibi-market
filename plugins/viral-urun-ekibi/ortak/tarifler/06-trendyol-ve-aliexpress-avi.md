# Tarif 06 — Trendyol ve AliExpress avı

## Amaç
TR pazarında satılabilir ürün bulmak: Trendyol'da kanıtlanmış ama henüz viral olmamış, AliExpress'ten temin edilebilir ürünler. Çıktı: **5 niş × 5 ürün** Excel + tek gerekçeli öneri.

## Girdi
Niş/ilgi alanı ipuçları (yoksa viral-DNA'dan) · TR oran tablosu (`bazaar/referans/tr-oranlari.tsv`; boşsa tarif tur 0: "oran turu") · açık macOS Chrome (giriş yok, salt-okuma).

## Adımlar
0. **Oran turu** (yalnız tablo boşken, bir kez): komisyon, ödeme (ör. %2,49 + 0,25 TL), kargo, KDV oranlarını **kaynak URL'siyle** `tr-oranlari.tsv`'ye yaz. Kaynak bulunamayan oran BOŞ kalır; uydurma oran yazılmaz; boş oranla marj hesaplanamaz → ürün en çok "SAT (koşullu)".
1. Aday toplama: Trendyol arama/liste sayfalarından aday ürünler. **Arama kartı yetmez**: ürün SAYFASINA gir, yorum sayısı, puan, fiyat, satıcı, varyantları oradan oku.
2. Estetik filtre: görünüşü ucuz/estetiği zayıf ürünler elenir (ör. sıradan telefon standı tipi, plastik/jenerik görünüm). Soru: "Bu ürünün videosu ilk 2 saniyede dikkat çeker mi, fotoğrafı pahalı durur mu?" Hayırsa ELE, gerekçesiyle.
3. AliExpress tedarik: ürün sayfasında "This seller: N | Total sales: M" ayrımı — **satıcının** satışı (N) ile **ürünün toplam** satışı (M) ayrı yazılır; sayfanın altındaki öneri/benzer ürün bölümündeki sayılar ALINMAZ. Fiyat ve kargo sayfadan, 1-1 aynı ürün olduğu görselle doğrulanır.
4. Marj: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/bazaar/scripts/tr_marj.py" …` (oran tablosu doluysa).
5. Viral kontrolü: ürün zaten viral mi (Meta Reklam Kütüphanesi / TikTok arama, salt-okuma). Girişsiz doğrulanamıyorsa "doğrulanamadı" yazılır, uydurulmaz.
6. **Sınama 3/3:** her SAT adayı için 3 bağımsız kontrol (talep var · tedarik/marj tutuyor · viral değil/çürütülemedi); 3/3 geçmeyen SAT olamaz.
7. Karar etiketleri: **SAT** (3/3) · **SAT (koşullu)** (marj ya da viral doğrulanamadı ama diğer ölçütler güçlü; `neden` sütunu hangisinin eksik olduğunu yazar) · **İZLE** · **ELE**.
8. 5 niş × 5 ürün tablosu → `ortak/excel_yaz.py` (tarif 07).
9. Rapor: "Önerim: <ürün> — çünkü … İtirazın yoksa onunla devam ediyorum." (liste değil tek öneri; tarif captain'de).

Pazar: bu tarif TR içindir; TR verisi zayıf (1 milyon kayıt), eşikler `esikler.tsv`'de `deneme`/`varsayim` durumunda ve ilk 20 üründen sonra kalibre edilir. ABD/AB ürün avı için `radar`/`hunter`.

## Kalite çıtası
5 niş × 5 ürün (eksik niş belirtilir) · her satırda ürün sayfası linki · satış sayıları ürün sayfasından (arama kartından değil) · AliExpress satıcı/toplam ayrımı yazılı · öneri bölümü sayısı yok · her kararda gerekçe · uydurma oran/sayı yok.

## Kapılar
`bazaar/scripts/bazaar_kontrol.py` 0 · `excel_yaz.py` doğrulaması 0 · `bazaar/scripts/kirma_testi.py` 0.

## Sık hata ve düzeltmesi
- Arama kartındaki "1B+ satış" ile ürün sayfası farklı → sayfadakini yaz.
- AliExpress'te "Total sales" satıcı sanıldı → iki sayıyı ayrı sütunda tut.
- Hepsi İZLE çıkıyor (oran yok) → oran turunu yap; kaynak yoksa "SAT (koşullu)" etiketiyle ilerle.

## Bitti tanımı
Excel + 1 tek öneri; her SAT için 3/3 kanıtı dosyada; DURUM.md güncel.
