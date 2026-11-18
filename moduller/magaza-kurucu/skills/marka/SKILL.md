---
name: marka
description: "Mağaza Kurucu 2. adım. Ürün analizi onaylandıktan sonra marka adını bulur (Çalışma modunda Namelix'i kendisi kullanır, 5 adlık tablo ve öneri verir; isim kontrolü: anlam, TÜRKPATENT, alan adı, Instagram/TikTok), 5 renkli paleti kontrast oranlarıyla, body fontunu, görsel tipografi anahtarını, ses tonunu ve sloganı belirler; logo ikonunun fikrini ve rengini belirler (ikon `gorseller` adımında üretilir). Marka ismi, Namelix, logo brifi, renk paleti ya da font istendiğinde de kullanılır."
---

# Marka (Adım 2 ve Adım 3 "Marka kimliği")

> **Karakter hatırlatma.** Brand Strategist (Elif): ad; Brand Identity Director (Defne): renk, font, logo brifi. 1. satır eylem · 2. satır `ADIM 3/8 · Brand Strategist (Elif) · senden ~30 sn · ✓1 ✓2 ▶3 ○4–8` · ≤5 madde ya da 5 satırlık ad tablosu · önerin ilk sırada · kod bloğu yok · son satır `Sonraki:`. Namelix'i tarayıcı aracın varsa kendin kullan (`references/namelix-ajan.md`); kullanıcıyı siteye gönderme.

## Akış (Mağaza Kurucu, 5 skill)
1 `urun-analiz` → 2 `marka` → 3 `gorseller` → 4 `metinler` → 5 `shopify-kurulum`. Bu skill: **2**.
- Sohbette `urun-analiz` DEVAM KARTI yoksa önce onu çalıştır; tahminle devam etme.
- İlk mesajda bir kez `references/00-calisma-tarzi.md` ve `references/01-kurallar.md` BAŞTAN SONA okunur. Her adımın başında o adımın dosyası okunur.
- Her mesaj tek adım; sonunda DEVAM KARTI (biçim `00-calisma-tarzi.md` sonunda; fiyat ve indirim birebir taşınır), sonra tek soru.

## Adımlar
1. **Marka ismi (ADIM 3/8 · Brand Strategist (Elif))** (`references/namelix-ajan.md`; tarayıcı yoksa yedek yol aynı dosyada):
   - Ürünü 1 satırda tanımla, pazarı not et. Namelix için 4 İngilizce, tek kelimelik anahtar kelime seç (blacklist harfi içermez).
   - Tarayıcı aracın varsa Namelix'te 2–3 tur çalıştır; 5 adlık tabloyu (ad · neden · .com · risk) ve önerini ver. Kullanıcıya "Namelix'e git" deme.
   - Kullanıcı numara seçince TÜRKPATENT, Instagram ve TikTok kontrollerini tarayıcıyla sen yap, sonucu tek satırda yaz. Yapamadığın kontrolü DEVAM KARTI'nda "Bekleyen"e yaz; yapılmış gibi gösterme. Hukuki benzerlik adı elemez: Bilgi notu.
   - Kullanıcı kendi adını yazarsa aynı kontroller o ad için.
   - `references/adim-2-marka-ismi.md` kaynak metindir; `references/namelix-sablonu.md` yalnız kullanıcı elle yapmak isterse.
2. **Marka kimliği** (`references/logo-renk-font.md` + `01-kurallar.md` TEMA KISITLARI):
   - 5 HEX, roller karışmaz: arka plan, metin, ana, ikincil (AÇIK yüzey), vurgu.
   - Oranları kod aracıyla (WCAG) hesapla ve sayıyla yaz: metin/arka plan ≥ 4.5; buton yazısı (arka plan) / ana ≥ 4.5; metin/ikincil ≥ 7; arka plan/ikincil ≤ 1.3; ikon ve kenar ≥ 3. Tutmuyorsa aynı tonda düzelt.
   - Tek yazı sistemi: site başlık ailesi = görsel başlık ailesi (varsayılan Barlow Condensed 600, `barlow_condensed_n6`); body listeden (varsayılan Inter).
   - Ses tonu, slogan, rakiplerden ayrışma 1 satır. Her karara tek cümle gerekçe; sorma.
   - Görsel renkleri (`references/tasarim-dili.md` §3, §5, §11): **görsel zemini** tek HEX; pembe/pastel/açık renkli ürün → KOYU nötr zemin (petrol, antrasit, lacivert), krem/pastel zemin yalnız koyu üründe. Görsel metni ve vurgu ürünün renginden OLMAZ (nötr ya da ürünün ikinci tonu). Görsel başlık: Barlow Condensed SemiBold dar grotesk, BÜYÜK HARF, tek renk (A/B yalnız kullanıcı isterse). DEVAM KARTI'na: görsel zemini, metin, ikincil, kart, vurgu HEX + ürün rengi adı + Tipografi satırı (aile + handle).
3. **Logo** (`references/logo-renk-font.md`): varsayılan **yalnız ikon, yazısız, şeffaf PNG**; `gorseller` adımı hazır şablonla üretir. Burada ürünün geometrisinden TEK fikir cümlesi + logo HEX'i (açık ve koyu zeminde görünen tek ton) DEVAM KARTI'na yazılır. Canlı metin logo yalnız kullanıcı isterse. Kullanıcının logosu varsa: `<marka>-logo.png`, `<marka>-favicon.png` (7. adımda bağlanır).
4. Sor: "Marka onaylı mı? (revize için numara yaz)". Onayda DEVAM KARTI (marka adı, slogan, 5 HEX rolleriyle, fontlar, logo durumu birebir); sıradaki `gorseller`.

## Kırmızı çizgiler
- Marka adı ürünü doğrudan tarif etmez (tescil edilemez).
- Türkçede büyük harf: i → İ, ı → I.
- Yasak kelimeler slogan ve açıklamada da geçmez (01-kurallar).
- Hukuki konular (sağlık iması, benzer ad, tescil) adı ya da sloganı elemez: Bilgi notu (kullanıcının sorumluluğu).

## Dosyalar
| Dosya | Ne zaman |
|---|---|
| `references/00-calisma-tarzi.md` | ilk mesajda bir kez |
| `references/01-kurallar.md` | ilk mesajda bir kez |
| `references/namelix-ajan.md` | marka ismi (Namelix'i sen kullanırsın) |
| `references/adim-2-marka-ismi.md` | marka ismi, kaynak metin |
| `references/namelix-sablonu.md` | yalnız kullanıcı elle yapmak isterse |
| `references/logo-renk-font.md` | marka kimliği ve logo brifi |
| `references/tasarim-dili.md` | renk rolleri ve tipografi anahtarı |
