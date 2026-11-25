# Rol sınavı 2 + birleştirme raporu · 2026-11-25 (akşam)

Sonuç: 17 ajan 0.6 rol dosyalarıyla eksik girdi sınavından geçti (28 vakada 27 dur ya da dürüst kısmi; 1 vaka fikstür ↔ kural çelişkisi). 01/02 jürisi geçerli panolarla koşuldu. Ürün avı tek beceride birleşti, 8 eski ad silindi, mağaza kolunun kaynağı ile birleşik kopyası eşitlendi.

## 1. Kritik bulgu: kurulu eklenti 0.4.0
- `viral-urun-ekibi:*` ajan tipleri `~/.claude/plugins/cache/viral-urun-market/viral-urun-ekibi/0.4.0/` kopyasından çalışıyor. Depodaki 0.6 karakterleri o tiplerle sınanamaz.
- Öğlenki rol sınavı (ROL-SINAVI-RAPOR.md) rol TANIMLARI açısından 0.4.0'ı ölçtü (betikler ve ortak/ dosyaları depodan okundu).
- Bu sınavda her ajan, depodaki `agents/<rol>.md` okutularak ve frontmatter'daki modelle (`general-purpose` + model) çalıştırıldı.
- Danışanlar da büyük olasılıkla eski sürümde: 0.6 yayımlanana kadar düzeltmeler onlara ulaşmaz.

## 2. Eksik girdi sınavı (fikstür: `ortak/sinav/roller/*/vaka.json`, 28 vaka)
| Sonuç | Roller |
|---|---|
| ✅ dur / YAPILAMAZ, uydurma yok (24) | atlas ×3, copy site, decoder, director, fixer, forge ×2, jury, mixer, panel, probe ×3, scout, sentinel ×3, shopper ×2, skeptic, story, muse referans |
| ❌ → düzeltildi → ✅ (2) | copy görsel (URUN-KILIDI yokken kısmi metin yazdı) · architect tipografi (STIL-KARTI yokken varsayılan çift seçti) |
| ❌ → düzeltildi → ✅ (1) | muse logo (araştırma/brif yokken 12 yön + istem yazmıştı; yeniden sınamada YAPILAMAZ) |
| ⚠️ karar gerekli (1) | architect bölüm: fikstür "KANIT/kütüphane yok → dur" diyor; `magaza-ekibi.md` "kütüphane eksikliği işi durdurmaz" diyor. Ajan kurala uydu (veri isteyen bölümleri kapalı tuttu). |

Kök neden (3 hata): "Önce oku … yoksa gömülü sayı" kuralı ürün dosyalarını (URUN-KILIDI, STIL-KARTI, logo brifi) kütüphaneyle aynı sepete koyuyordu. Düzeltme: `agents/copy.md`, `ortak/roller/architect/tipografi.md`, `ortak/roller/muse/logo.md` içine "Zorunlu girdi (durma kuralı)" satırı.

Yöntem notu: jury ve panel kopyaları rol araçlarında olmayan Bash'i bir kez kullandı (sınav düzeneği `general-purpose` verdiği için). Gerçek eklenti tiplerinde araç listesi bunu engeller.

## 3. Jüri (3 kör kopya × 6 pano, geçerli panolarla)
| Sınav | a-kolay | b-zor | c-tuzak |
|---|---|---|---|
| 01 ürün videosu | GEÇTİ 7,0 | GEÇTİ 8,0 | KALDI 4,5 (13/13) |
| 02 kanca / ön-üretim | GEÇTİ 8,0 | KALDI 3,5 | KALDI 3,5 |

- İlk jüri turu geçersiz: `juri.py pano` referans kare sayfalarını (5×2) tek görsel sayıp 20 kez döşedi ("pano içinde pano"), kare klasörlerinden profil ekran görüntüsü (hesap adı) panoya girdi. Kopyalar okunamayan ögeyi puanlamayıp durdu ya da açıkça işaretledi.
- Düzeltme `skills/cut/scripts/juri.py`: `sayfa_bol` (dikiş + 9:16 ızgara algısı, hücre üst %9 etiket kırpılır), kare klasöründe yalnız `kNN` kareleri, her ögeye aynı maske. `juri_test.py` 42/42; düzeltme geri alınınca test KALDI (kırma tuttu). Eski KOR dosyaları `<referans-kok>/sinav-kosu/rol/_arsiv-juri-pano-hatasi-2026-11-25/`.
- Kalan: 01 c-tuzak (malzeme), 02 b-zor/c-tuzak için fixer kök nedeni. Referans kareleri düşük çözünürlüklü (kaynak sayfalar 155 px genişlik): biçim farkı riski not edildi.

## 3b. Fixer (gerçek girdi, eşleşme açıldıktan sonra)
| Vaka | Sınıf | Karar | Emir | Kredi |
|---|---|---|---|---|
| 01 c-tuzak | malzeme (kanıt planı kaynak videoda yok; 5 klip tek başsız stüdyo videosundan) | DUR | 2 (gerçek kanıt çekimi · omuz+bant kanca klibi) | 0; çekim/numune kurucu kararı (AI önce-sonra IDD-02 yasak) |
| 02 b-zor | hikâye (`ilk_1sn` olaysız; ürün karesi sonuç göstermiyor) | DUR, ön-üretim tur 2 | 3 | 0 Flow; 2 ChatGPT karesi |
| 02 c-tuzak | hikâye (kanca soru soruyor, cevap karesi yok; ICE-03) | DUR, ön-üretim tur 2 | 3 | 2 emir kredisiz; 1 emir gerçek çekim ya da 1 Flow klibi |

- Üç fixer da jüri bulgusunu körü körüne almadı: "CTA kesik" iddiasını kareden çürüttü (pano maskesi), "yapay" iddiasını gerçek tedarikçi çekimi diye `kare` sınıfından ayırdı.
- İkisi lider brifindeki hatayı yakaladı (b-zor ↔ c-tuzak eşik/sıra karışmıştı); KOR dosyalarından yeniden hesapladı, karar değişmedi.
- **Kapı adayı:** ön-üretim panosu 2 durağan kare × 10 tekrar → ritim ve cevap karesi ölçülemiyor; `ilk_1sn` ↔ senaryo `giris` uyumu kapıya çevrilmeli.

## 3c. Canlı Trendyol taraması (scout → denetle → skeptic → sınama → Excel)
- Klasör: `<referans-kok>/sinav-kosu/rol/06-canli/` · 2 niş (evcil kıyafet, mutfak soyacak) · 4 arama + 5 ürün sayfası, engel/CAPTCHA yok · ~10 dk.
- Sonuç: **SAT 2/5** (koala peluş köpek tulumu 850 TL · cepli leopar hoodie 324 TL), ELE 3 (lisanslı karakter veto · puan 2,8 · puan 4,1). skeptic ikisini de çürütemedi; AliExpress'te aynı ürünün sayfası bulunamadı (alış/marj "ilk testte kontrol et"). Lider sınaması 3/3 (yorum, puan, fiyat sayfadan okundu).
- Yakalanan ve düzeltilen 4 eklenti kusuru (hepsi kırma testli, Trendyol testleri 115 → 122):
  1. **Benzer ürün alışı ELE yaptı:** AliExpress arama sayfasındaki benzer ürünün fiyatı `alis_tl`'ye yazılmış, kat 0,47 → ELE. Artık `alis_kaynak` tedarikçi ÜRÜN sayfası değilse kat ölçülmez, not düşer.
  2. **Viral aile eşleşmesi gevşek:** tek ortak kelime ("köpek") köpek kostümünü 23 köpek yatağıyla aile sayıyordu (5/5 aday "aile-var"). Artık aile adının bütün kelimeleri gerekir (koala/köpek kostümü → gerçek "evcil-kostum" ailesi; hoodie ve soyacaklar → yok).
  3. **Satış alt sınırı kör nokta:** kat ölçülemeyince 399 TL alt sınırı hiç denetlenmiyordu; 324 TL ürün notsuz SAT oldu. Artık "set/paketle fiyatı yükselt" notu.
  4. **scout akış adımı atladı:** `viral` komutu koşulmadı, özet "viral veritabanı yok" dedi (tablo eklentide var). Lider koştu; brief'lerde 6a adımı zorunlu yazılmalı.
- Ek: muse'un araç listesinde tarayıcı yok → referans modunda görsel ölçemiyor (PANO kısmi kaldı).

## 3d. Marka sınavı 08 (elle; koşucu 08'i henüz tanımıyor)
a-kolay (kupa, TR) zinciri tamam: atlas strateji → muse referans → atlas kimlik → muse logo → architect tipografi → probe erişim; lider `magaza-paketi.json` yazdı.
| Kapı | Sonuç |
|---|---|
| dosyalar (5 md + paket) | GEÇTİ |
| paket_sozlesme | GEÇTİ (0 hata; dürüst `null`+`eksik[]`: ürün başlığı/fiyat/görsel/pdp → ölçüte göre `olculemedi`) |
| renk kontrastı | GEÇTİ (probe betikle; sözleşme renkleriyle lider yeniden ölçtü: kullanılan çiftlerin en düşüğü 4,60) |
| iddia / yasaklı (müşteri metni: ad, slogan, onaylı metin) | GEÇTİ (0) |
| iddia / yasaklı (iç belgeler marka/*.md) | ölçüm KUSURLU: 284 iddia + 20 yasaklı isabetin tamamı yanlış pozitif (`## 1.` başlığı `#1` desenine, "ödüllü demiyorum" olumsuzlamaya takılıyor) |
| kim_denetledi | erişim: probe (bağımsız) · diğerleri ÖZ-DENETİM → `olculemedi` |
| jüri | tanımsız (OLCUT ii) |
Ad: **Belir** · slogan "Sıcağı dök, siyah açılsın." · sicil/hesap adı kontrolü yapılmadı (kurucu).
Bulunan eklenti kusurları:
1. **Renk rolleri sözleşmeyle uyumsuz:** sözleşme `zemin, metin, ikincil, kart, vurgu` ister; atlas kimlik kuralında bu adlar yoktu (lider brifi de yanlış adlar verdi) → `kart` eksik, paket yazılamazdı. `ortak/roller/atlas/kimlik.md` düzeltildi.
2. **muse'da tarayıcı yok:** referans modunda görsel ölçülemiyor (PANO kısmi).
3. **08 OLCUT kapsamı:** iddia/yasaklı kapısı iç belgeleri tarıyor; koşucuya bağlanırken yalnız müşteri metnine (paket + KIMLIK örnek cümleleri) uygulanmalı (kurucu kararı; 05'teki KAPI.md yüzde sorunuyla aynı sınıf).
4. Tipografi durma kuralı (bu oturumda eklenen) marka adımında fazla sıkıydı: KIMLIK yazı ailesini de kaynak sayacak biçimde düzeltildi.
b-zor (DE) ve c-tuzak (US) da tamam (atlas strateji+kimlik tek çağrı · muse referans+logo · architect · probe):
| Vaka | Ad · slogan | Paket | Müşteri metni yasaklı | Kontrast (probe) | Not |
|---|---|---|---|---|---|
| a-kolay TR | Belir · "Sıcağı dök, siyah açılsın." | GEÇTİ | 0 | GEÇTİ 4,60 | sicil/hesap adı bakılmadı |
| b-zor DE | Blattwechsel · „Fellwechsel? Blattwechsel.“ | GEÇTİ | 0 | GEÇTİ 6,01 | blattwechsel.de kayıtlı; tarif edici ad → tescil riski; Barlow'da büyük ẞ yok (kural yazıldı) |
| c-tuzak US | Yokestay · "Shoulders back, under your shirt." | GEÇTİ | 0 | GEÇTİ 4,61 | tuzak geçildi: ağrı/omurga/hekim dili yok; iç belgelerdeki isabetler ajanın yasak listesi + rakip alıntıları |
- Sözleşme renk rolleri düzeltmesi tuttu: b ve c'de atlas ilk seferde `zemin/metin/ikincil/kart/vurgu` yazdı.
- Ortak sınır: muse tarayıcısız → pano görselleri ve kör pano kareleri `olculemedi` (3/3 vaka); 08 jürisi tanımsız; bağımsız denetim yalnız kontrastta.
- Vaka durumu (koşucu mantığıyla): 3/3 `olculemedi` (KALDI yok; olculemedi kapılar: kim_denetledi, jüri, eksik ürün alanları).

## 4. Birleştirme
1. **Mağaza kolu kaynak ↔ birleşik kopya:** `moduller/magaza-kurucu` (kaynak) ile `skills/builder` (üretilen) 12 dosyada ayrışmıştı; bugünkü düzeltmeler yalnız üretilen kopyadaydı, sonraki `build.py` silerdi. Ters eşitlendi, yönlendirici SKILL.md 5.120 bayt sınırına indirildi. `build.py --check` GEÇTİ, `pytest moduller/magaza-kurucu/tests` 72 geçti.
2. **8 eski ad silindi** (0.5.0'da kaldırılacağı yazıyordu): ai-video-kreatif, aliexpress-firsat, ekip-lideri, kesfet-urun-avi, magaza-kurucu, reklam-kutuphanesi-avi, teklif-ve-sayfa, video-kurgu. `ad-haritasi.tsv`'ye `alias` sütunu (`var` / `kaldirildi`); `ad_testi.py` d) kaldırılan adın klasörü geri gelirse KALDI (yeni kırma testi; kendini-sına 10/10).
3. **Ürün avı tek beceri:** `bazaar` → `hunter/trendyol/` (AKIS.md, scripts, referans, sablon); `bazaar_kontrol.py` → `trendyol_kontrol.py`, `BAZAAR_SIMDI` → `TRENDYOL_SIMDI`; hunter SKILL.md'ye "Kaynak seçimi" (AliExpress / Trendyol). `bazaar` bir sürüm için yönlendirme (0.7.0'da kalkar). Excel kaynak adları `aliexpress` / `trendyol`. Testler: Trendyol 115/115, AliExpress 43/43, Excel 76/76, bütçe GEÇTİ, anonim temiz, ChatGPT paketi üretildi (hunter + trendyol/ içinde, bazaar yok).

## 5. Bekleyen
- architect bölüm fikstür çelişkisi (kurucu kararı).
- 02 b-zor/c-tuzak ve 01 c-tuzak için fixer.
- Canlı Trendyol taraması (scout → skeptic → yalnız-SAT Excel) ve 08 marka sınavı.
- Sürüm 0.6.0 (commit + ZIP) yalnız kurucu isteyince.
