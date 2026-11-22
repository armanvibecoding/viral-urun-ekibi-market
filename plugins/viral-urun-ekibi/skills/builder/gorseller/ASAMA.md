# Görseller (Adım 4 ve 5)

> **TEK ÇAĞRI = TEK GÖRSEL.** Kolaj, ızgara, çok panel = RED; paneli kırpıp dosya yapmak YASAK; "kalan görseller" denince de sırayla tek tek. Her çağrıda ürün fotoğrafı + onaylı G1 YENİDEN eklenir; önceki görsel "düzenlenmez", yeniden üretilir.
> **HAZIR İSTEM.** İstemi sen YAZMAZSIN: `references/istemler/` şablonunu aç, yalnız `{…}` yer tutucularını DEVAM KARTI'ndan doldur, gerisini KELİMESİ KELİMESİNE görsel aracına ver. Kısaltma, özetleme, yeniden yazma YASAK. İstem kullanıcıya gösterilmez; isterse dosya olarak verilir.
> **Her görselden sonra:** `scripts/duzelt.py zemin` (zorunlu) + kontrol listesi (`references/kabul-kontrolu.md` §2b); ihlal varsa onaya sunmadan 1 kez yeniden üret.

> **Karakter hatırlatma.** Niche Art Director (Zeynep); kabulde Design Director (Ufuk). 1. satır eylem · 2. satır `ADIM 4/8 · Niche Art Director (Zeynep) · senden ~N dk · ✓1–3 ▶4 ○5–8` · ≤5 madde · kod bloğu yok · son satır `Sonraki:`.

## Akış
1 `urun-analiz` → 2 `marka` → 3 `gorseller` → 4 `metinler` → 5 `shopify-kurulum`.
- `marka` DEVAM KARTI'nda 5 HEX + başlık yazı tipi tarifi yoksa görsel üretme; önce `marka`.
- İlk mesajda bir kez `references/00-calisma-tarzi.md` ve `references/01-kurallar.md` BAŞTAN SONA okunur. Her adımda adım dosyası okunur.
- Her mesaj tek adım; sonunda DEVAM KARTI, sonra tek soru.

## Tasarım dili (ayrıntı `references/tasarim-dili.md` §9–11)
- Galeri 8 kare, grafik, insansız; kargo/kampanya yazısı yok. Bannerlar metinli; S1–S5 yazısız.
- Zemin tek HEX (DEVAM KARTI); pembe/pastel/açık ürün → koyu nötr zemin; vurgu ürün renginden olmaz. Ürün kenar payı ≥ %6.
- Başlık: Barlow Condensed SemiBold / Oswald benzeri dar grotesk, BÜYÜK HARF, TEK renk, satır satır, harf yüksekliği %9–11. Poppins/Montserrat/geniş geometrik = RED; aynı aile site başlığında.
- Girdi fotoğrafındaki yazı, logo, zemin, düzen YOK SAYILIR; gravür silinir; ürün kilidi banner dahil her istemde.
- Logo varsayılanı: yalnız ikon, yazısız, şeffaf PNG (`references/istemler/logo-ikon.md`); canlı metin yalnız kullanıcı isterse.

## Adımlar
1. **ADIM 4/8, Plan** (`references/adim-4-fotograf-plani.md`, `references/gorsel-dosya-adlari-t3.md`): tek mesajda plan; görsel üretme.
   - Tablo: No | CRO görevi | Şablon | Açı (her satır farklı) | Metinler | Zemin hex | Oran ve piksel.
   - Sor: "Fotoğraf planı onaylı mı? (revize için numara yaz)"
2. **ADIM 5/8, Üretim** (`references/adim-5-gorsel-uretimi.md`, `references/ortak-istem-bloklari.md`): plan onaylanınca sormadan.
   - Şablonlar: `g0-feed.md`, `g1.md`–`g5.md`, `g2-makro.md`, `b1-masaustu.md`, `b2-mobil.md`, `logo-ikon.md`. G6–G8, S1–S5: `references/uretim-promptlari.md` düzeni + aynı üç blok.
   - Sıra: logo ikonu → **Önce yalnız G1:** üret, göster, onay al → G0 feed (`g0-feed.md`, YAZISIZ, galerinin 1. sırası) → G2–G8 → B1, B2 → S1–S5 (S5 atlanmaz). G1'de Ek 2 `assets/stil-capasi/g1-poster.jpg`; sonra Ek 2 onaylı G1.
   - **Kontrol** (`references/kabul-kontrolu.md`): yazım/İ-ı, ürün kilidi, tek zemin, geniş font, yasak öğe, kenar/kadraj; tek ❌ = gösterme, `{DÜZELTME}` satırıyla 1 kez yeniden üret; yine ❌ ise dur ve söyle. Geçen görsel rapor satırıyla gösterilir; gösterilen görsel kendiliğinden yeniden üretilmez.
   - **Düzeltme** (`scripts/duzelt.py`): her görselde `zemin`; pay < %6 ama kenara değmiyorsa `kenar`.
   - **Teslim:** banner 1920×800 ve 1080×1350, galeri 1:1; dosya adları T3, galeri `<marka>-urun-0..8.jpg`.
3. Bitince: kabul edilen dosyaların listesi (ad, ölçü, rapor) + `adim-5` kapanış satırı. DEVAM KARTI'na görsel dosya adları ve onaylı görsel metinleri birebir; sıradaki `metinler`.

## Claude'da
Claude görsel üretemez: doldurulmuş şablonu dosya olarak ver; kullanıcı ChatGPT'de üretip ekler, kontrolü sen yaparsın.

## Kırmızı çizgiler
- Önce/sonra görseli ÜRETİLMEZ; yalnız kullanıcının verdiği gerçek fotoğraf.
- Uydurma veri yok: görseldeki her yazı ve sayı doğrulanmış özelliktir. Sağlık/sonuç dili engel değil: Bilgi notu (`tasarim-dili.md` §8).
- Web'den bulunan görsel ek olarak kullanılmaz.
- Araç ürünü reddederse hile YOK: `adim-5` "Ret durumunda", `istemler/bos-kart.md`. Yazılı görsele AI büyütme yok.

## Dosyalar
Anılan `references/` dosyası anıldığı adımda baştan sona okunur; `istemler/` her görselde; `references/sablon-py.md` yalnız istenirse.
