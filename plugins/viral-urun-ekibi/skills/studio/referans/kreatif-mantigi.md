# Kreatif mantığı — milyon izlenen videolar neden izlendi

> Kaynak notu: bu dosya ~100 milyon izlenen ürün videosunun saha incelemesinden (kayıt numaraları köşeli parantezde, ör. [058]) ve bir dış araştırmadan derlendi. Ham veri seti eklentiye dahil değildir; sayılar o ölçümün sonucudur.

Kaynak: saha veri setinde **`milyon: true` olan 104 kayıt** (001–139) + saha notları. §1 ve oran ölçümleri ilk 97 kayıtla yapıldı; 133–139 kural kanıtlarına işlendi.
`milyon: false` kayıtlar (011, 012, 035, 039, 041, 042, 043, 045, 046, 048, 049, 050) **kural kaynağı değildir**; yalnız karşı-örnek olarak anılır.
Köşeli parantez = kayıt numarası. Etiket: **KURAL** ≥3 milyon kayıt · **ADAY** 2 · **GÖZLEM** 1.
Sayılar notlardan aynen alındı (B = bin, MN/M = milyon).

---

## 1. Veri tabanı neye benziyor

| Ölçü | Değer | Kaynak |
|---|---|---|
| Milyon kayıt | 97 (85 DROP-MARKA, 11 GERÇEK-MARKA, 1 BELİRSİZ) | saha.json `tip` |
| Pazar | ABD + ABD/global 79 · AB/UK 12 [014, 051, 055, 062, 065, 068, 069, 077, 089, 101, 104, 111] · TR 1 [125] · LatAm 1 [093] · Global 2 | saha.json `pazar` |
| Süre | medyan **12 sn**; 83/97 kayıt 8–15 sn; 20 sn ve üstü 13 kayıt | `sure_sn` |
| Paylaşım/beğeni | medyan 0,56 (94 kayıtla); paylaşım ≥ beğeni 23 kayıt | `paylasim`, `begeni` |
| Üretim | gerçek çekim 66 · AI ağırlıklı gövde 24 · gerçek + AI/VFX karışık 7 | `format` (aşağıda §4) |
| Yorum-kelime CTA | 36 kayıt | `cta` |
| **2026-11-07 ölçüm** (116 kayıt, 104 milyon; içerik matematiği ölçümü) | beğeni/izlenme %1,82 [1,01–2,91] n=89 · paylaşım/izlenme %1,07 [0,61–1,93] n=91 · yorum/izlenme %0,016 n=90 · paylaşım/beğeni 0,61 n=101 · izlenme/takipçi 308× n=91 · gönderi 110 n=104 · süre 12 sn, 90/104 8–15 sn | içerik matematiği ölçümü |

Uyarı: bu veri Keşfet'te **görünen** kazananlardır. Aynı kalıbı deneyip görünmeyen hesapların oranı bilinmiyor; o yüzden hesap-içi karşılaştırmalar (§3) en değerli kanıttır.
Sayıyla: 12 milyon-altı kaydın yalnız 2'sinde etkileşimle eşleşen izlenme var (012, 048) → "milyon vs altı" oran karşılaştırması yapılamaz. Milyonların içinde süre izlenmeyi açıklamıyor (ρ=0,04); oranlar izlenme büyüklüğünden bağımsız (ρ(izlenme, paylaşım/izlenme)=−0,06).

---

## 2. Çekirdek kurallar (kanıt sayısına göre)

| # | Kural | Etiket | Kanıt |
|---|---|---|---|
| R1 | **Aynı ürün, aynı çekim seti, çok kanca.** Hesap aynı ürünü onlarca videoda farklı ekran yazısıyla atıyor; milyonu algoritma seçiyor. | KURAL (60) | D1: 001, 005, 014, 020, 047, 052–056, 058–069, 073–076, 078, 085, 088–090, 092, 093, 095–097, 099–101, 105–110, 112, 114–116, 119, 121, 122, 124–130, 132 |
| R2 | **Kazanan kalıp tekrar milyon alıyor.** Aynı kanca/kadraj ikinci, üçüncü kez milyon. | KURAL (11) | 122 'Babe/Me' 4× 1,2–2,2MN · 053 25,6/3,8/1,2MN · 114 20,1/15/8,5/6,1MN · 113 27,8/5,2/1,8MN · 112 26,3/21/2,3MN · 119 9,9/5,1/2,7MN · 085 30,2/2,7/1,2MN · 073 7,5/3,1/2,8/1MN · 054 32,7/6,1/1,9/1,4MN · 061 13,3/10,2/5,5MN · 055 9/3,6/3,5MN |
| R3 | **Ürün/görüntü kancayı yener.** Aynı hesapta, aynı set ve kancayla ürün değişince sonuç 30–1000 kat değişiyor. | KURAL (4) | 082, 091, 098, 103 (§3 tablo B) |
| R4 | **Kısa:** 8–15 sn. İlk saniyede ürün ya da problem görünür. | KURAL (83/97) | `sure_sn` |
| R5 | **Ürünün kendisi dönüşüyor / karakter gibi davranıyor** (katlı→açık, peluş↔bebek, ışık yanıyor, parça parça tamamlanıyor). | KURAL (25) | D15: 030, 038, 053, 057, 058, 065, 069, 075, 080, 081, 083, 085, 087, 089, 090, 093, 096, 101, 103, 113, 115, 123, 127, 128, 131 |
| R6 | **Yazısız da milyon olur:** görüntü 2 sn'de anlaşılıyorsa ekran yazısı gerekmez, problem/CTA caption'da. | KURAL (20) | D7: 004, 006, 038, 053, 057, 060, 062, 065, 085, 089, 090, 093, 094, 095, 101, 102, 114, 117, 123, 130 |
| R7 | **Tek sahne, kesmesiz** 8–12 sn döngü — gag ya da mekanizma ürünlerinde. | KURAL (17) | 014, 038, 060, 063, 066, 072, 085, 089, 090, 097, 105, 114, 117, 123, 134, 135, 138 |
| R8 | **Problem/Concept → Vs… → Sonuç** üç kartlı akış. | KURAL (17) | D12: 036, 040, 044, 047, 074, 075, 076, 077, 080, 084, 100, 112, 116, 120, 126, 131, 137 |
| R9 | **Kimlik kancası** (yasak / zorunluluk / hitap) — ama tek başına yetmiyor (R13). | KURAL (44) | D3: 001, 003, 006, 020, 037, 040, 047, 053–057, 059, 064, 066, 067, 070–073, 078, 079, 081–083, 086–088, 096–098, 103, 106, 107, 112, 113, 121, 122, 124, 131, 132, 133, 136, 139 |
| R10 | **Alıntı-ironi kancası** ('Them/Babe: …' → 'Me:', '[X] are hard to gift', 'It's just a …'). | KURAL (7) | 054, 086, 098, 113, 122, 127, 135 |
| R11 | **Yorum-kelime CTA** ('Comment "KELİME"'), çoğu DM otomasyonlu. Ölçüm: yorum oranını artırmıyor (yorum/izlenme 1,01×, n=37/50) → işlevi link dağıtımı, erişim değil. | KURAL (36) | D5 (bkz. `kurgu-ve-yasaklar.md` §4) |
| R12 | **Bağlam dışı / kamusal yerde kullanım** (ürün beklenmedik yerde: direksiyon, trafik, kasa, ofis, AVM). | KURAL (16) | D9: 006, 063, 069, 073, 075, 081, 087, 088, 091, 097, 098, 100, 115, 123, 129, 134 |
| R13 | **Kanıt deneyi / işkence testi:** görünmez faydayı abartılı testle göster. Ölçüm: paylaşım/izlenme %0,32 vs %1,15 — izletir, paylaştırmaz; kimlik kancasıyla eşle. | KURAL (13) | D14: 014, 052, 061, 066, 077, 092, 102, 104, 106, 108, 111, 114, 118 |
| R14 | **Paylaşım istenir:** 'Send this to a [KİMLİK]' CTA'lı videolarda paylaşım beğeniye yakın ya da fazla. | KURAL (8) | 078, 080, 081, 082, 083, 084, 086, 120 (086: 1MN paylaşım / 954B beğeni) |
| R15 | **Topluluk / kültür kimliği** (diaspora, fandom, meslek, hobi). | KURAL (15) | D11: 051, 054, 055, 059, 067, 068, 072, 076, 083, 097, 101, 106, 112, 124, 127 |
| R16 | **Sezon çerçevesi** (Noel, Cadılar Bayramı, havai fişek). | KURAL (11) | D8: 005, 064, 071, 081, 088, 110, 119, 122, 127, 129, 139 |
| R17 | **Kurulum/montaj demosu** (sök→tak→çalıştır). | ADAY (2) | 111, 118 (ikisi de GERÇEK-MARKA) |
| R18 | **Kurucu anlatımı.** | GÖZLEM (1) | 033 (GERÇEK-MARKA) — kit önermez |

### Okuma: üç iş
- **Durdur (0–1 sn):** ürün kullanım anında ya da tek bakışta anlaşılan tuhaf görüntü (dev ayak terlik [123], maskeli köpek [075], iskeletli kedi [057]). Yazı yoksa da durduruyor (R6).
- **İzlet (1–12 sn):** "sonra ne olacak?" — dönüşüm (R5), Vs… geçişi (R8), tamamlanma (zırh parça parça [093], kumun süzülmesi [102]), ya da kesmesiz komik tepki [063].
- **Paylaştır:** kimlik adı (R9, R15), ironi (R10), 'Send this to' (R14), hediye. Paylaşım ≥ beğeni olan 23 kaydın 17'sinde ekranda ya da CTA'da kimlik / hediye / alıntı / izleyicinin acısı var [003, 040, 071, 072, 079, 081, 082, 083, 084, 086, 088, 098, 109, 121, 124, 131, 132]; 4'ünde başka metin (POV rahatlama 089, POV keşif 108, fiyat 125, ironi 129); 2'si yazısız demo [102, 117] → paylaşım çoğunlukla bir kişiyi çağıran metinle geliyor, ama şart değil.

---

## 3. NE İŞE YARAMIYOR — hesap-içi karşılaştırmalar

Aynı hesap, aynı ürün (B tablosunda: aynı set, farklı ürün). Sayılar notlardan aynen.

### A. Aynı ürün — biri milyon, diğeri düşük

| Kayıt | Milyon olan | Düşük kalan | Ders |
|---|---|---|---|
| 047 | gerçek araç-içi problem çekimi 1,3MN (gerçek çekimler 320B–1,3MN) | AI market/polis sahneli 1,7B–7B | AI mağaza/polis sahnesi düşük |
| 070 | üretici ham demo videosu 1,4MN | AI 'Car owners RUN to [mağaza]' 3–10B | aynı |
| 071 | 4 mekânda kullanım montajı 1,2MN | AI market şaşkınlığı 12–16B · 'RUN to [mağaza]' 5B · 'DON'T show this to a dog dad' 35,8B | aynı + yasak kancası tek başına yetmedi |
| 072 | sade ürün demosu (su→buhar→ışık) 1,1MN | kurucu-yüzlü AI/sahne versiyonları 1,8–2B | AI "kişi" sahnesi düşük |
| 080 | karton Concept → Result 4MN | AI market + 'perfect dog gift doesn't exi-' 1.445 · 'Babe stop buying dumb stuff' 385–1.445 | aynı |
| 083 | sade AI: hayvanlar ürünü kullanıyor 1MN | sahte kafe/fast-food kalabalık AI 436–1.705 | AI kalabalık düşük |
| 086 | kullanım anları + tek kısa mağaza karesi 32,8MN | sahte mağaza ekip kalabalığı AI 3.967–5.275 (biri 195B) | kalabalık baskınsa düşük |
| 107 | unboxing + kullanım + kısa raf reveal 2MN / 955B | aynı format başka mağaza adıyla 2.796–29,5B | mağaza sahnesi şansa bağlı |
| 120 | gece kamerası problem→çözüm 5MN | AI 'RUN to [pet mağazası]' 292–296 · 'He was shivering…' 292 | — |
| 123 | gerçek POV tek kare 4,8MN | AI metro/mağaza/kuyumcu/polis 16,5B–52,4B · AI + 'perfect gift for your husband doesn't exi-' 18,2B | gag ürünü süsleme istemez |
| 059 | gerçek POV, yalnız bacak 17,4MN | AI "doktor" videoları (beyaz önlük) 2,3–17,3B | sahte otorite düşük |
| 094 | yazısız AI "çözülmüş hayat" 1,1MN | gerçek UGC yorgun-anne videoları 2–3,6B | bebek kategorisinde AI sonuç sahnesi kazandı (karşı yön) |
| 065 | AI morph (bebek↔peluş) 22,3MN | aynı AI dünyası diğer videolar 21B–223B | AI seti tek başına yetmez; morph anı taşıdı |
| 006 | tulum direksiyonda (bağlam dışı) 15,8MN | bebekli "doğru" kullanım videoları 4–6B | bağlam dışı > doğru kullanım |
| 063 | kesmesiz gerçek köpek tepkisi 15MN | torba-açma 'DO NOT show' versiyonları "tutmadı" (sayı yok) | gerçek tepki > kanca |
| 064 | parti/kalabalık telefonla çekiyor sahnesi 2,2MN | 'Don't let a small Dog Mom see this', 'Send this to a Small Dog Mom' 5–12B | — |
| 075 | Concept → VS → Result 3,1MN | 'The perfect Halloween dog mask doesn't exist' 5,6B · 'The perfect gift for your dog' 802 | düz hediye kancası düşük |
| 081 | AI insan korku/prank tepkisi 3,7MN | 'DON'T let your DOG see this' 2–3,5B · 'POV: Your dog hates walking when it snows' 3,1B | tepki > yasak kancası |
| 084 | gece kamerası problem→çözüm 1MN | 'He was shivering from the cold…' 6,7B · kedi versiyonu 528 (sonra Ek: kedi gece kamerası 2,8MN) | kalıp kazandı, cümle değil |
| 085 | yazısız tek sahne 30,2MN | 'DO NOT let your dad see this' 7,5B (fan-yasak versiyonu 2,7MN) | yazısız gag en büyük |
| 087 | 'POV: You have adult money' + AI gag 7,7MN | 'DO NOT let a Dog mom see this' 2,9–6,4B · 'The Problem…' 13,5B | ironi > yasak |
| 088 | 'Do NOT send this to a [karakter] lover' 2,5MN | 'If you're a [karakter] lover you NEED this' 3.821 · 'adult money' 32,1B | aynı ürün, kanca 650× fark |
| 099 | 'POV: 15 hours on the plane…' 3,2MN | 'The perfect gift for your passenger queen' (araba sahnesi) 2.068 | acı anı > düz hediye |
| 100 | 'The best thing I've bought with my adult money' 19,8MN | unboxing 'instead of therapy for my road rage' 21,7B–206B | — |
| 102 | yazısız mekanizma demosu 5,1MN | yazılı Black Friday / 'Sturdy and well-made' 983–2.275 | yazı/teklif metni düşük |
| 104 | köpek kendi burun izini kokluyor 3,2MN | kit unboxing 597B · yüzük 64,6B | hayvan-ürün etkileşimi > unboxing |
| 106 | çekiç/ateş işkencesi + su testi 4,6MN | 'No one likes [marka] clothing', 'Its just some rain jacket' 12,3B–139B | test > kanca |
| 110 | 'Secret Santa idea for a cheese lover in the US' 4,7MN | 'Gift idea for a cheese lover' 31,4B · 'Stocking stuffer idea…' 23,2B | sezon kelimesi + ülke etiketi farkı |
| 111 | kurulum demosu 1,6MN | güzellik yüzü videoları 1.172–8.422 | — |
| 116 | 'Travel bottles in 2026' (2025 vs 2026) 2,7MN | diğer kancalar 1.654–68,9B | — |
| 117 | yazısız takma demosu 4MN | metinli 'Fix Foot Drop…' 2.461–3.590 | sağlık iddialı metin düşük |
| 118 | kurulum demosu 1,8MN / 1,5MN | POV hırsız sahnesi 980 | korku senaryosu < kolay kurulum |
| 119 | 'My dog has anxiety attacks every time it fireworks' 5,1MN | 'The problem… Vs…' (yağmur şemsiyesi) 3.791–435B | — |
| 126 | 'Normal office chair vs… The kloud' 9,3MN | 'Not your regular office chair' 23,7B | karşılaştırma sahnesi > iddia |
| 127 | "It's just a fridge magnet..." 3,5MN | 'EVERY Christmas LOVER Needs One' 2.266 · 'POV: Me every time I open the fridge' 2.171 | alıntı-ironi > zorunluluk |
| 131 | AI 'The concept 🤢 → VS → The result' 1,4MN (yeni hesap, 3. video) | aynı kalıbın ilk iki denemesi 29,4B · 4.129 | aynı kalıp 3 denemede milyon — tekrar dene |
| 132 | 2 sn jenerik raf + 3 kullanım sahnesi 2,6MN | AI 'RUN TO [mağaza]' ekip/kalabalık reveal 4.645–19,1B · 'The perfect gift for small dog owners' 45,6B | N1 + N4 |
| 128 | 'Perfect gift for bathing you dog doesn't exi…' 1,1MN | 'Live alone? Here's how I bathe my big dog' 173B · 'Bathing one dog is hard… imagine two' 18,8B · 'DON'T let DOG moms see this' 565 | — |

### B. Aynı set/kanca — ürün değişince

| Kayıt | Milyon | Düşük | Ders |
|---|---|---|---|
| 082 | aynı AI ev + kadın, köpek bezi 3,1MN | aynı set, başka ürün: 'Don't let DOG LOVERS see this' 125B · 'Small dog owners this is for you' 222B | ürün > kanca |
| 091 | göbek çantası AI havaalanı prank 14,7MN | aynı hesabın pet hoodie AI uçak videoları 2–22B | aynı |
| 098 | hava topu gerçek prank 2,4MN | yeni ürün aynı 'Perfect Gift' kancasıyla 2–6B | aynı |
| 103 | dinozor bebek tulumu AI 1,5MN | AI prank, başka ürün 3–5B | aynı |

### C. Bu tablolardan çıkan "işe yaramıyor" kuralları

| # | İşe yaramıyor | Etiket | Kanıt |
|---|---|---|---|
| N1 | **AI mağaza / kalabalık / ekip / kafe sahnesinin baskın olduğu video.** | KURAL (10 milyon hesap + akış) | 047, 070, 071, 080, 083, 086, 107, 120, 123, 132 · akış: [hesap] AI mağaza 1,9B–9,3B |
| N2 | **Yasak/zorunluluk kancasının tek başına taşıması.** Aynı ürünün 'DO NOT show / Every X needs' versiyonu düşük kaldı; milyonu görüntü getirdi. | KURAL (9) | 063, 064, 071, 081, 085, 087, 088, 127, 128 |
| N3 | **Ürünü anlatan / iddia eden ekran metni** (teklif, "sturdy", "fix …") yazısız demoya kaybetti. | ADAY (2) | 102, 117 |
| N4 | **Düz hediye kancası ("perfect gift for your dog")**, bağlamsız. | KURAL (4) | 075 (802), 099 (2.068), 110 (31,4B), 132 (45,6B) |
| N5 | **Sahte uzman / kurucu yüzlü AI kişi.** | ADAY (2) | 059, 072 |
| N6 | **Kanca bombardımanı tek başına.** Aynı AI karakteri 6 kez farklı kancayla atmak milyon getirmedi. | GÖZLEM (milyon dışı akış) | [hesap] 6× en iyi 502B · [hesap] 6× 18,9B–204B · [hesap] (071 şablon kopyası) en iyi 33,1B · [hesap] problem→vs en iyi 211B |

---

## 4. AI kullanımı — hangi AI sahnesi milyon aldı, hangisi düşük kaldı

Sınıflama `format`/`akis` alanından; "muhtemel AI" göz yargısıdır (şüpheli nokta).

**AI ağırlıklı gövdeyle milyon (29):** 058, 064, 065, 071, 074, 075, 079, 080, 081, 082, 083, 086, 087, 089, 091, 094, 099, 103, 115, 119, 120, 124, 131, 132, 133, 134, 137, 138, 139
**Gerçek + AI/VFX karışık milyon (7):** 040, 056, 078, 084, 096, 107, 128

### Milyon alan AI sahne tipleri
| Tip | Ne | Etiket | Kanıt |
|---|---|---|---|
| AI-1 | **Gerçekte çekilemeyen hayvan/bebek eylemi:** köpekler top sürüyor, bebek peluşa dönüşüyor, köpek poşetlerle alışveriş, peluş eller bebeği pışpışlıyor, hayvanlar yatağın kollarında uyuyor. | KURAL (9) | 058 17,5MN · 065 22,3MN · 080 4MN · 082 3,1MN · 083 1MN · 087 7,7MN · 089 2MN · 103 1,5MN · 131 1,4MN (kediler ejderha yatakta) |
| AI-2 | **Yabancıların tepkisi gag'i onaylıyor:** insanlar korkup kaçıyor, gülüyor, polis/K9 şüpheyle bakıyor, kalabalık telefonla çekiyor. Tepki kısa, ürün her karede. | KURAL (6) | 064 2,2MN · 075 3,1MN · 081 3,7MN · 087 7,7MN · 091 14,7MN · 115 2MN |
| AI-3 | **Gece / güvenlik kamerası estetiğinde problem karesi** (REC, IR gri) → çözüm. | KURAL (3 + 2 Ek) | 074 1,1MN · 084 1MN · 120 5MN · Ek: 047 hesabı tünel yatak 5,5MN, 084 kedi 2,8MN |
| AI-4 | **Giyilen/taşınan ürünün 3–4 mekânda kullanım montajı** (park, ev, kafe, yolculuk). | KURAL (6) | 056 2,3MN · 071 1,2MN · 079 1,1MN · 086 32,8MN · 124 1,4MN · 132 2,6MN (havuz, nehir) |
| AI-5 | **İdealize sonuç / huzur karesi** (aile dinleniyor, uçakta/araçta derin uyku, oda gökyüzüne dönmüş). | KURAL (6) | 078 1,4MN · 094 1,1MN · 099 3,2MN · 119 5,1MN · 133 6,4MN (araç içi, tek AI araç kanıtı) · 138 4,1MN |
| AI-6 | Gerçek çekim üstüne VFX katmanı (hologram, patlama). | GÖZLEM (1) | 040 1,6MN |

### Düşük kalan AI sahne tipleri
| Tip | Ne | Kanıt |
|---|---|---|
| AI-X1 | Mağaza açılışı / raf / ekip / kalabalık kuyruğu baskın | N1: 047, 070, 071, 080, 083, 086, 107, 120, 123, 132 |
| AI-X2 | Ürünü kamusal alanda göstermek, ama ürün kendi başına zaten komikse | 123 (gerçek POV 4,8MN vs AI 16,5B–52,4B) · **karşı-kanıt** 134: aynı jenerik ürün, AI market kuyruğu, kimse fark etmiyor 20,9MN → kesin değil, ADAY |
| AI-X3 | Sahte uzman / kurucu yüzü | 059 (2,3–17,3B), 072 (1,8–2B) |
| AI-X4 | Aynı AI dünyası, morph/tepki anı olmadan | 065 (diğerleri 21B–223B), akış [hesap], [hesap] |

### Karar kuralı (sahne başına sor)
1. Bu sahne **telefonla çekilebilir mi?** Evet ve ürün kendini anlatıyorsa → gerçek-görünümlü sade POV yaz (AI süsleme yok) [123, 085, 063].
2. Çekilemiyorsa ve **hayvan/bebek/ürün bir şey yapıyorsa** (AI-1) ya da **yabancı tepkisi** gerekiyorsa (AI-2) → AI'nın en güçlü kullanımı.
3. Sahne **mağaza/raf/kalabalık kuyruk** ise → yazma [N1]. Mağaza karesi milyonlarda yalnız ≤2 sn, gövde ürün kullanımıyken görüldü: gerçek marka adıyla [079, 086, 107] (bize yasak) ve bir kez **markasız büyük mağaza koridorunda** [132, GÖZLEM]. İstersen yalnız jenerik raf, ≤2 sn, 'deneme' etiketiyle.
4. Problem karesi gerçekçi olmalıysa → gece/güvenlik kamerası estetiği (AI-3).

Not: DERSLER 2026-11-04 KARŞI-KANIT maddesi (058 gövdesi AI, 17,5MN) bu tabloyla doğrulandı: "AI gövde düşük izlenir" kuralı kaldırıldı, yerine N1 + AI-1…AI-5 geldi.

**Format sayıları (2026-11-07, içerik matematiği ölçümü §4c; anahtar kelime sınıflaması):** gerçek 73 kayıt izlenme 4,0MN (n=57), paylaşım/beğeni 0,49 · tam AI 30 kayıt 2,1MN (n=26), 0,94 · karma 13 kayıt 1,8MN (n=10), paylaşım/izlenme %1,60 (en yüksek). Aynı gözlem döneminde (kayıt ≥074) fark sürüyor: 4,0MN vs 2,6MN. → AI gövde milyon alır ama izlenme tavanı gerçeğin altında, paylaşımı yüksek; karma/hibrit (S10) test edilir.

---

## 5. Teklif tarafı (videonun dışında, mağaza fiyat verisi)

65 milyon kaydın sitesi okundu:
- **Fiyat:** USD gösteren 50 sitede medyan **$46,97** (aralık $10–$349). Bantlar: <$30 16 · $30–60 19 · $60–100 9 · ≥$100 6.
- **Üstü çizili karşılaştırma fiyatı** 49/65 sitede var (yasal sınır için `pazar-katmani.md`).
- **Ürün yeni:** ürün eklenme tarihi 48/65'te 2026-07 ve sonrası, 34/65'te 2026-09 ve sonrası → milyon videolar çoğunlukla ürün sayfası 0–4 aylıkken.
- **Mağaza dar:** 39/65 mağazada ≤5 ürün, 13'ünde tek ürün.
- **Uygulamalar:** Kaching (paket/bundle) 20 · ReConvert 9 · Zendrop 8 · UpCart 8 · yorum uygulaması Loox 18, Judge.me 10, Trustoo 3.
Bu alanın anlamı `excel betiği` sütun başlıklarından alındı (n = mağaza ürün sayısı, tar = ürün eklenme).

---

## 6. Sektör kanıt tablosu — bu ürünün sektöründe ne kadar kanıt var

Sayım: saha notlarının tamamı (114 not, 001–139), her nota TEK ana sektör; "AI gövde" = AI ağırlıklı gövde, "karma" = gerçek + AI/VFX.
Yeni not eklenince tablo yeniden sayılır (elle güncellenen sayı eskir, `ortak/bilgi/dersler.md` #67).

| Sektör | Not | AI gövde / karma | Örnek | Durum |
|---|---|---|---|---|
| Evcil hayvan | 30 | 17 / 2 | 058, 063, 081, 086, 120, 131 | kanıtlı |
| Bebek (giyim/bakım/taşıma) | 10 | 6 / 2 | 004, 065, 089, 094, 096, 103 | kanıtlı |
| Giyim/ayakkabı (yetişkin) | 8 | 3 / 0 | 062, 106, 123, 134 | kanıtlı (AI sınırda) |
| Ev/yatak odası/dekor | 7 | 0 / 1 | 020, 053, 061, 078 | KANITSIZ SEKTÖR |
| Araç/motosiklet aksesuarı | 7 | 1 / 0 | 037, 070, 088, 100, 133 | KANITSIZ SEKTÖR |
| Banyo/kişisel bakım | 6 | 0 / 0 | 001, 036, 055, 111 | KANITSIZ SEKTÖR |
| Teknoloji/gadget | 6 | 0 / 1 | 095, 107, 114, 118, 136 | KANITSIZ SEKTÖR |
| Sağlık/ortopedi | 6 | 2 / 0 | 059, 109, 117, 139 | KANITSIZ SEKTÖR (reklamda sağlık POV'u platform riski, PLT-01) |
| Mutfak | 5 | 0 / 0 | 060, 067, 110, 121, 127 | KANITSIZ SEKTÖR |
| Aksesuar/cüzdan/takı | 5 | 0 / 0 | 085, 097, 101, 130, 135 | KANITSIZ SEKTÖR |
| Oyuncak/şaka (yetişkin) | 5 | 0 / 1 | 040, 073, 098, 129 | KANITSIZ SEKTÖR |
| Fitness/spor | 5 | 0 / 0 | 003, 035, 092, 105 | KANITSIZ SEKTÖR |
| Mobilya (büyük) | 3 | 0 / 0 | 108, 113, 126 | KANITSIZ SEKTÖR |
| Çocuk oyuncak/aktivite | 3 | 1 / 0 | 012, 069, 122 | KANITSIZ SEKTÖR |
| Seyahat | 3 | 2 / 0 | 099, 116, 138 | KANITSIZ SEKTÖR |
| Hediye/kişiye özel | 3 | 0 / 1 | 041, 042, 090 | KANITSIZ SEKTÖR |
| Kültür/din topluluğu | 2 | 0 / 0 | 051, 054 | KANITSIZ SEKTÖR |
| Kozmetik, bahçe/kamp, temizlik | 0 | — | — | KANITSIZ SEKTÖR (sıvı/doku: gerçek çekim, `baslangic-karesi.md` §6) |

**KANITSIZ SEKTÖR** = sektörde AI gövdeli not < 3. AI kanıtının 23/32'si evcil + bebekten geliyor; buradaki şablonlar
(S4, S5, S6, M7–M9) başka sektöre taşındığında tutup tutmadığı ölçülmedi. Sonuçları:
1. Viral referans 5 değil **10 video** izlenir (`SKILL.md` "Viral referans").
2. Senaryoların **≥ %50'si** viral referansta ≥3 videoda görülen desenden kurulur; evcil/bebek kökenli şablon tek başına iskelet olmaz.
3. İlk parti küçük (`olcum-ve-test-plani.md` §7); kazanan oranı bu tabloya not olarak geri yazılır.
