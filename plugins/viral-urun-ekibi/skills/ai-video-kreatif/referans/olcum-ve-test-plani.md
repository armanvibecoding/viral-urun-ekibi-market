# Ölçüm ve test planı — bir ürün için 10 varyasyon

> Kaynak notu: bu dosya ~100 milyon izlenen ürün videosunun saha incelemesinden (kayıt numaraları köşeli parantezde, ör. [058]) ve bir dış araştırmadan derlendi. Ham veri seti eklentiye dahil değildir; sayılar o ölçümün sonucudur.

Amaç: aynı ürün için 10 organik Reels videosu atıp hangisinin büyütüleceğine **sayıyla** karar vermek.
Eşiklerin kaynağı: içerik matematiği ölçümü (116 kayıt, 104 milyon). Veride olmayan eşik uydurulmadı; o satırlarda **"ilk testten sonra kalibre et"** yazıyor.

> **Eşiklerin sınırı:** saha oranları milyon videoların **ömür boyu** sayıları ve yalnız kazananlar (başarısız videolar veride yok). Yani eşik "bu video milyon profiline benziyor mu" sorusunu cevaplar, "bu video milyon olacak mı" sorusunu değil. İlk 24–48 saatteki oranın ömür boyu oranla aynı olduğu ölçülmedi.

---

## 1. Değişkenler ve 10 videonun dağılımı

Tek değişken kuralı: her test videosu kontrol videosundan (V1) **yalnız bir** şeyle ayrılır. Kanca kurguda değiştiği için en ucuz değişkendir ve en çok yeri o alır.

| Video | Değişen | Ne yapılır | Neden bu değişken (kanıt) |
|---|---|---|---|
| **V1 kontrol** | — | Seçilen şablon (S1–S10), 12 sn, kimlik kancası (K1/K2), `Comment "[KELİME]"` | 12 sn = milyon medyanı; kimlik kancası paylaşım/izlenmede en yüksek aile (%1,41, n=32) |
| V2 | kanca | K5 alıntı-ironi | paylaşım/izlenme %1,23 (n=15) |
| V3 | kanca | K11 akış kartları (Problem → Vs… → Solution) | problem→VS %0,76 (n=19); izlenme 2,7MN |
| V4 | kanca | K13 yazısız (CTA caption'da) | D7 izlenme 5,1MN vs 2,5MN (n=22) |
| V5 | kanca | K10 kimlik hitabı ya da K4 bağlamlı hediye + kimlik (sezonda) | hediye tek başına %0,44 (n=13) → mutlaka kimlikle |
| V6 | kanca | K7/K8 POV | POV %0,71 (n=11) — düşük beklenti, kontrol amaçlı |
| V7 | **ilk kare** | V1 ile aynı klipler, sıra değişik: ilk kare İ2 problem anı ↔ İ1 kullanım anı (V1 hangisiyle açıldıysa öteki) | `baslangic-karesi.md` §1: iki tip de KURAL; hangisinin üstün olduğu veride ölçülmedi |
| V8 | **süre** | V1'in 8 sn kurgusu (en iyi 3 kesme) | ≤8 sn kovası n=6, paylaşım/izlenme %2,77 — ZAYIF; milyonlarda süre izlenmeyi açıklamıyor (ρ=0,04) → düşük öncelik, tek video |
| V9 | **CTA** | V1 + `Send this to a [KİMLİK]` (Comment yerine) | paylaşım CTA'lı 6 kayıtta paylaşım/beğeni 1,26 vs 0,61 — ZAYIF; Comment CTA yorum oranını artırmıyor (1,01×) |
| V10 | **format** | S10 hibrit (AI kanca + gerçek kanıt) — gerçek numune yoksa: başka bir şablonla ikinci klip seti | karma format paylaşım/izlenme %1,60 (n=10); tam AI izlenme 2,1MN vs gerçek 4,0MN |

Not: her hücre n=1. Tek videonun sonucu gürültülüdür; bu yüzden karar tek video için değil, **eşik + hesap-içi kat** ile verilir ve kazanan ikinci partide tekrar edilerek doğrulanır (R2: kazanan kalıp tekrar milyon alıyor, 11 hesap).

Üretim: V1–V6, V8, V9 aynı klip seti (tek set; dış araştırma notu §5 Senaryo A: ~72 sn üretim ≈ $5 Omni 720p API **ya da** abonelikte 1–2 gün kota). V7 aynı klipler. V10 ek set ya da gerçek çekim.

## 2. Metrikler — ne ölçülür, nereden

| Metrik | Hesap | Karar metriği mi | Neden |
|---|---|---|---|
| **3 sn tutma** | Instagram Insights (izleyicinin ilk 3 sn'yi geçme oranı / atlama oranı) | evet, ama **eşik yok** | sahada bu alan yok → **ilk testten sonra kalibre et**: 10 videonun medyanı = hesabın kendi tabanı; tabanın altındaki kanca/ilk kare zayıf |
| **paylaşım / izlenme** | gönderilme ÷ oynatma | **evet (ana)** | milyon: %1,07 [%0,61 – %1,93], P10 %0,21 (n=91) |
| **beğeni / izlenme** | beğeni ÷ oynatma | evet | milyon: %1,82 [%1,01 – %2,91], P10 %0,75 (n=89) |
| yorum / izlenme | yorum ÷ oynatma | **hayır** | milyon %0,016, dağılım çok dar; yorum-kelime CTA farkı 1,01× → ayırt etmiyor |
| yorumdaki CTA kelimesi sayısı | "Comment X" yazan yorum adedi | hayır (satış sinyali) | link isteyen kişi sayısı; DM'le gönderilen link tıklamasıyla birlikte kaydet |
| izlenme / takipçi | oynatma ÷ yayın anındaki takipçi | bilgi | milyon medyanı 308×; yeni hesapta her video bu çarpanla okunur |
| **hesap-içi kat** | video izlenmesi ÷ aynı partideki diğer 9 videonun medyan izlenmesi | **evet** | milyon hesaplarda kazanan video, profildeki diğerlerinin medyanının **4,7 katı** [0,97 – 14,5] (n=27) |

**Pazar düzeltmesi:** AB/UK videolarında paylaşım/beğeni medyanı 0,27 (n=15), ABD'de 0,69 (n=94) → AB'de paylaşım eşiği ABD'den düşük olmalı; AB için ayrı paylaşım eşiği veride yeterli değil (n=13) → AB'de karar **beğeni/izlenme + hesap-içi kat** ile, paylaşım eşiği **ilk testten sonra kalibre et**. TR: eşik yok (1 milyon kaydı) → **ilk testten sonra kalibre et**.

## 3. Karar eşikleri

**Ölçüm noktaları:** yayından 24 s, 48 s ve 7 gün sonra (tablo §4). Karar 48. saatte verilir; 7. gün kalibrasyon içindir.

**Minimum izlenme (yöntem kuralı, saha verisi değil):** oran ancak sayılabilir olay biriktiğinde anlamlıdır. Eşik %0,61 paylaşım/izlenmede ~10 paylaşım için ≈ 1.640 izlenme gerekir (10 olayda Poisson göreli hatası ≈ ±%32). → **≥ 2.000 izlenme altındaki videoda oran kararı verilmez** ("veri yok" sayılır, öldürülmez).

| Karar | Koşul (48. saat, ≥2.000 izlenme) | Kaynak |
|---|---|---|
| **DEVAM — büyüt/tekrarla** | paylaşım/izlenme ≥ **%0,61** **ve** beğeni/izlenme ≥ **%1,01** (milyonların alt çeyreği) — **ya da** izlenme ≥ **4,7 ×** partideki diğer videoların medyanı | §1, §2 ölçümleri |
| **GÜÇLÜ** | paylaşım/izlenme ≥ **%1,07** (milyon medyanı) | §1 |
| **BEKLE** | yalnız biri geçiyor, ya da izlenme < 2.000 → 7. günde yeniden bak | yöntem |
| **ÖLDÜR (bu varyant)** | paylaşım/izlenme < **%0,21** **ve** beğeni/izlenme < **%0,75** (ikisi de milyonların en kötü %10'unda) | §1 P10 |
| **Parti kararı** | 10 videonun hiçbiri DEVAM değilse → **görüntüyü değiştir** (şablon / ilk kare), kancayı değil; yeni klip setiyle 2. parti | N2 + D7/D15 izlenme ~2× (içerik matematiği ölçümü §4) |
| **Ürün kararı** | kaç parti sonra ürün bırakılır: **veriden türetilemez** (başarısız hesaplar veride yok) → kullanıcı belirler. Referans: milyon görmüş hesapların gönderi medyanı 110, %12'si ≤20 gönderide milyon gördü | §2 |
| **3 sn tutma** | **ilk testten sonra kalibre et**: 10 videonun medyanının altında kalan ve paylaşım eşiğini de geçemeyen kanca/ilk kare bir sonraki partiye alınmaz | veri yok |

Kazanan seçilince: aynı kanca + **yeni sahne** (R2), aynı görüntü + 3 yeni kanca (R1). Bir varyant iki partide de DEVAM aldıysa kalıp "doğrulandı" sayılır.

## 4. Kayıt tablosu (her video bir satır)

| Video | Değişken | Şablon | Kanca (aile) | İlk kare (İ1–İ7) | Süre | CTA | Format | Pazar | Yayın tarihi/saat | Takipçi (yayında) | 24s izlenme | 48s izlenme | 48s beğeni | 48s yorum | 48s paylaşım | 48s repost | 3 sn tutma | CTA kelimesi yorumu | 7g izlenme | pay/iz | beğ/iz | hesap-içi kat | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V1 | kontrol | | | | 12 | Comment | | | | | | | | | | | | | | | | | |

Hesap: `pay/iz = 48s paylaşım ÷ 48s izlenme`; `hesap-içi kat = video 48s izlenme ÷ diğer 9 videonun 48s izlenme medyanı`.
İlk partiden sonra: 48 s oranı ile 7 g oranını karşılaştır; fark büyükse karar noktasını 7. güne taşı ve bu dosyayı güncelle (tarihli).

## 5. Üretim kaydı — kullanılabilir klip oranı

| Klip | Model / sürüm | Deneme no | Değiştirilen tek değişken | Kullanılabilir mi | Hata türü (el / ürün şekli / yazı / fizik / özne karışması) |
|---|---|---|---|---|---|

- Klip başına en fazla **3 deneme** (araştırmanın planlama varsayımı; ölçümler %30–100 arası: https://kingy.ai/?p=929624). Her denemede tek değişken değiştir (https://morphic.com/resources/how-to/ai-video-troubleshooting).
- Oran = kullanılabilir ÷ toplam üretim. Elle tutulan ürün sahnelerinde oran **%30'un altına** düşerse: önce referans modu iki geçiş (`sahne-sablonlari.md` §0), sonra yedek model (Kling 3.0 / Veo 3.1) — ücretli API, **kullanıcı onayı + projenin bütçe kapısı**.
- Maliyet planı: tek set × 10 kanca ≈ $5–10 API; 10 farklı set ≈ $50+ (Omni 720p) (dış araştırma notu §5). Abonelikte kota ~3–5 klip / 5 saat.

## 6. Bu planın ölçemediği
- Satış: organik izlenmeden siparişe dönüşüm sahada yok. DM link tıklaması + mağaza oturumu ayrıca kaydedilmeli (eşik: **ilk testten sonra kalibre et**).
- Ücretli reklam: CTR/CPA eşikleri bu veriden çıkmaz (saha organik Reels).
- Paylaşım CTA'sı (V9) ve ≤8 sn (V8) kanıtları n=6 — sonuçları "deneme" olarak okunur.
