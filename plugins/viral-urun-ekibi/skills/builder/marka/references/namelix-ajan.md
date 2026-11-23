# Namelix: ajanla otomatik ad bulma (AŞAMA 1/3 · ADIM 4/9 · Atlas)

Biçim: KARAKTER bloğu (1. satır eylem · 2. satır `AŞAMA 1/3 · ADIM 4/9 · Atlas` · ≤5 madde · kod bloğu yok · son satır `Sonraki:`).
Ölçüm: 2026-11-16, Playwright ile 6 koşu (hesap, giriş, captcha yok). ChatGPT ajan tarayıcısında denenmedi [DOĞRULA]; arayüz değişirse "Yedek yol".

## Ne zaman
- Marka adımının ilk işi budur. Tarayıcı aracın (Agent / web tarayıcısı) varsa Namelix'i SEN kullanırsın; kullanıcıyı siteye gönderme.
- Tarayıcı aracın yoksa ya da Namelix 30 sn içinde açılmazsa: "Yedek yol"a geç. Akışı durdurma, kullanıcıya soru sorma.
- Tarayıcı işi başlamadan kullanıcıya tek satır yaz: "Namelix'te 3 tura kadar ad üretiyorum, sonra 5 ad getireceğim."

## Hazırlık (tarayıcıyı açmadan)
1. Anahtar kelime: 4 İngilizce kelime, her biri tek kelime: 1 fayda (rest, glow), 1 duygu (calm, soft), 1 mekanizma kökü (nasal, skin), 1 kök/hece (somn, lumi, nova).
   - Ürünün adını yazma (tape, device, strip).
   - Blacklist'teki harfleri (w, q, x) ve dizileri (th, ph, ee, oo) içeren kelime kullanma: anahtar kelime blacklist'i ezer.
2. Açıklama (İngilizce, ≤200 karakter): `<ürün> that <fayda> for <kitle> in <ülke>; easy to pronounce in <dil> and English.` Yalnız doğrulanmış gerçeklerle.
3. Blacklist: `<ürün adı>, <sorun adı>, th, ph, w, q, x, ee, oo` (Türkiye dışı pazarda sondaki harf listesi o dilin okunuşuna göre değişir).

## Tur 1 (Brandable names + Medium)
1. Aç: `https://namelix.com/app/?keywords=<k1>+<k2>+<k3>+<k4>` (ana sayfayı atlar, sihirbazı açar).
2. "Brandable names" kartına tıkla, yeşil **Next**'e bas.
3. "Medium"a tıkla, **Next**'e bas (seçmek tek başına ilerletmez; seçim yoksa Next pasiftir).
4. Brand Info: "Brand keywords" kutusunda 4 kelimeyi kontrol et. "Business description" kutusuna açıklamayı yaz.
5. ⚙ sekmesi (Optional settings): "Blacklist words" kutusuna blacklist'i yaz. Uzunluk kaydırıcısına tıkla, `Home` tuşuna ve 4 kez `→` tuşuna bas; altta "9 letters" yazısını gör. ".com" yeşil kalsın, başka uzantı açma.
6. ⚙ sekmesinde Generate yoktur: **Brand Info** sekmesine dön, **Generate**'e bas. ~5–10 sn bekle; 30 kart gelir.
7. Bir kez sayfanın en altına kaydır (~80 karta çıkar). Üstteki kategori çiplerine tıklama.

## Kartı okuma
- Adı logodan OKUMA; logo fontları harfi bozar. Kartın üstüne gel, sol üstteki küçük düz yazıyı ad olarak al ("more info" panelinin başlığı da olur).
- Sağ üstte yeşil ✓ varsa .com boştur. ✓ yoksa .com doludur.
- Ad `.com` ile bitiyorsa ya da rozetinde `$` fiyatı varsa ("domain for sale") bu satılık alan adı ilanıdır: ELE.
- Tıklama: "logos" (Brandmark, ücretli), "domains" satın alma bağlantıları, Namecheap. Hiçbir satın alma, hesap ya da giriş sayfasına girme.

## Tur 2 ve 3
- Tur 2: ön elemeyi geçen en iyi 5 adın kalbine tıkla → "Create New Names" (form korunur) → Name Style **Auto** → Next → **High** → Next → Generate.
- Tur 3 (yalnız 5 geçerli aday çıkmadıysa): **Compound words** + **Low**.
- En çok 3 tur. Her turda ilk 30 kart + 1 kaydırma okunur.

## Ön eleme (biri tutmazsa aday çıkar)
Namelix blacklist'e ve uzunluğa kesin uymaz (tercih sayar); bütün filtreleri sonuçlara SEN uygularsın.
1. .com ✓ var ve satılık ilan değil.
2. Boşluk yok, en çok 9 harf, 2–3 hece.
3. Blacklist harfleri/dizileri yok; Türkiye için `c`, `j`, `y` (sonda), `ou`, `ea`, `oi` yok.
4. Ürünü ya da sorunu doğrudan söylemiyor (tape, bant, snore, horlama, nose-tape…).
5. Bildiğin bir markanın adı ya da yakın benzeri değil (ör. SomniFix, Somnox, Breathe Right). Emin değilsen elemek yerine "Risk" sütununa yaz.

## Puanlama (geçen adaylara, her ölçüt 0–2, toplam /10)
| Ölçüt | 2 | 1 | 0 |
|---|---|---|---|
| Telaffuz | Türkçe harf harf okunuş = İngilizce okunuş | Küçük fark | Farklı okunur |
| Türkçede anlam | Nötr ya da olumlu | Belirsiz çağrışım | Olumsuz/argo hece (pis, am, göt, sik, bok, piç, mal, kıç, sap…) |
| Uzunluk | 5–7 harf, 2 hece | 8–9 harf ya da 3 hece | Daha uzun |
| Çağrışım | Faydayı ya da kullanım yerini çağrıştırır, ürünü tarif etmez | Nötr | Ürünü tarif eder (tescil riski) |
| Ayırt edicilik | Rakip adlarına benzemez | Bir öneki/kökü paylaşır | Rakibe çok benzer |

En yüksek 5 aday için **"more info"** panelini aç: "AI feedback"i 1 satıra indirip "Neden" sütununda kullan, alan adı listesini kontrol et. Eşitlikte kısa olan ad önde.

## Çıktı (kullanıcıya tek mesaj, kod bloğu yok)
- 1. satır: `Marka adı için 1–5 arasından bir numara yaz. Önerim 1: <ad>.`
- 2. satır: `AŞAMA 1/3 · ADIM 4/9 · Atlas · senden ~30 sn · ✓1–3 ▶4 ○5–9`
- Tablo: `# | Ad | Neden (1 satır) | .com | Risk` (5 satır; önerilen ad 1. satırda, kalın, "önerim" etiketli).
- Tek satır: `Namelix: <tur> tur, <N> aday okundu, <M> ön elemeyi geçti.` (gerçek sayılar; saymadıysan yazma)
- Son satır: `Sonraki: numara yaz (10 sn). Kendi adın varsa onu yaz.`

Kullanıcı numara seçince SEN yaparsın (tarayıcıyla), sonucu tek satırda yazarsın:
1. TÜRKPATENT: https://www.turkpatent.gov.tr/arastirma-yap?form=trademark → Marka Adı = <ad>, "içinde geçen", sınıflar <SINIFLAR>
2. Instagram: https://www.instagram.com/<ad>/ · TikTok: https://www.tiktok.com/@<ad> (doluysa `<ad>.tr` / `<ad>official`, iki platformda aynısı)
3. .com.tr: https://www.trabis.gov.tr
Yapamadığın kontrolü "kontrol edilmedi" diye yaz ve DEVAM KARTI'nda "Bekleyen"e ekle. Benzer ad bulursan adı eleme: Bilgi notu (kullanıcının sorumluluğu).

## Dur ve yedek yola geç
- Captcha, "verify you are human", giriş isteyen ya da ödeme sayfası: hiçbir şey doldurma; yedek yola geç ve tek satır yaz: "Namelix doğrulama istedi, kendi listemle devam ediyorum."
- Namelix 30 sn içinde açılmazsa ya da Generate 60 sn içinde sonuç vermezse: yedek yol.

## Yedek yol (tarayıcı yok ya da Namelix açılmadı)
1. Aynı 4 anahtar kelime ve kurallarla 20 aday üret (uydurma kelime ya da bileşik; ≤9 harf).
2. Aynı ön eleme ve puanlama. .com sütunu: Shopify aracında `generate-domain-names` varsa en iyi 5 ad için `<ad>.com` kontrol et ve sonucu yaz. Araç yoksa "kontrol edilmedi" yaz, boş olduğunu iddia etme.
3. Aynı çıktı biçimi. Tablonun altına tek satır: "Namelix kullanılmadı: <neden>. İstersen Namelix'i kendin denemen için kısa adımları veririm ('adımlar' yaz)."
4. Kullanıcı "adımlar" yazarsa `namelix-sablonu.md` doldurulur ve numaralı kısa adımlar olarak verilir (kod bloğu değil; anahtar kelimeler ve açıklama satır içi kod).
- Shopify'ın `generate-business-names` aracını aday kaynağı olarak kullanma: tarif eden adlar veriyor (MouthSeal, QuietTape) ve bilinen markaları öneriyor (BreatheRight). Yalnız alan adı kontrolü için kullan.
