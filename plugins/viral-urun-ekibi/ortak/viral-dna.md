# Viral ürün DNA'sı (ortak bilgi)

Bu dosya, Instagram'da **sıfırdan patlamış** ürünlerin ortak özelliklerini ölçüt hâline getirir.
`aliexpress-firsat` becerisi adayları bu ölçütle süzer; `ai-video-kreatif` kanca seçerken buna bakar.

**Kaynak:** 114 saha notu (Instagram Reels, her not tek video; 102'si ≥1 milyon izlenmeli) + 70 marka
sitesinin fiyat taraması. Parantezdeki sayılar not numarasıdır (ör. "063" = 63 numaralı not).
Notların kendisi eklentide yok; numaralar kanıt izidir. Hesaplar adla anılmaz.
**Kural:** bir desen en az 3 notla desteklenmiyorsa desen sayılmaz; 2 notluk gözlemler "aday" diye ayrı yazılır.
Akraba ürün seçerken yalnız marka gibi davranan hesaplar örnek alınır → `${CLAUDE_PLUGIN_ROOT}/ortak/marka-skoru.md`.

---

## 1. Kapılar (üçü de geçmezse aday puanlanmaz → ELE)

| Kapı | Soru | Kanıt |
|---|---|---|
| K1 Gösterilebilirlik | Ürünün faydası veya şakası **3 saniyede, tek planda** gösterilebiliyor mu? | 001, 006, 020, 052, 063, 085, 102 — milyonluk videoların süresi 8–25 sn, medyan 12 sn; fayda ilk karelerde görünüyor |
| K2 Kanıtlı akraba | Aynı acıyı/şakayı çözen, milyon almış bir ürün var mı? (§3 mekanizma tablosundan kod + not no) | Aynı jenerik ürün farklı markalarda tekrar milyon aldı: cepli hoodie 056, 071, 086, 115, 137 · hayvan bebek tulumu 065, 096, 103 · dev ayak terlik 123, 134 · retro ahize 107, 136 · öne eğilen seyahat yastığı 099, 138 |
| K3 Veto yok | §4'teki eleyici risklerden biri var mı? | §4 |

## 2. DNA ölçütleri (her biri 1 puan, toplam 0–7) — eşik: **≥ 4/7**

| # | Ölçüt | Nasıl bakılır (AliExpress ürün sayfası / fotoğraf) | Kanıt notları |
|---|---|---|---|
| V1 | **Tek karede, yazısız anlaşılan dönüşüm, reveal veya görsel şaka** | Ürün fotoğrafına yazıyı kapatıp bak: "bu ne?" sorusu tek bakışta cevaplanıyor mu? İki net hâl (kapalı/açık, peluş/bebek, karanlık/galaksi) var mı? | 006, 020, 057, 063, 065, 085, 090, 102, 123 |
| V2 | **Ürünün öznesi bir canlı** (evcil hayvan veya bebek ürünün içinde/üstünde, "şakanın kendisi" oluyor) | Fotoğrafta hayvan/bebek ürünü giyiyor, içine giriyor, taşınıyor mu? | 005, 006, 057, 058, 063, 065, 081, 084, 086, 096 |
| V3 | **Bir kimliğe bağlanabiliyor** ve kimlik değiştirerek yeniden satılabiliyor (köpek annesi, gitarist, araba tutkunu, din/ülke, meslek) | Aynı gövde başka desen/disk/baskıyla başka topluluğa satılabilir mi? | 054, 067, 076, 078, 083, 124, 127; aynı ürün iki kimlikle milyon: 067 ↔ 127 |
| V4 | **"Birine gönder" tetikleyicisi:** şaka, hediye ya da ortak acı | İzleyici bunu kime atar? Cevap bir kişi/grup ise 1 puan. | Paylaşımın beğeniyi geçtiği notlar: 071, 084, 086, 098, 125, 129, 131, 134, 135 |
| V5 | **Sezon kancası** (Noel, Cadılar Bayramı, kış, bayram, Ramazan) | Önümüzdeki 8 haftada bir özel gün/sezon var mı? | 005, 064, 071, 081, 088, 110, 122, 127, 139 |
| V6 | **Teklif bandı:** satış fiyatı 25–70 $ (TR: pazarın karşılığı) ve maliyetin ≥3 katı | AliExpress **normal** fiyatı + kargo → hedef satış fiyatı | Site taraması (70 site): ana ürün medyan 47 $, çeyrekler 30–69 $; 54/70 sitede üstü çizili fiyat, medyan %40 indirim. TR'de fiyat bizzat kanca: 049 (1.699 TL), 125 ("kargo dahil 199 TL") |
| V7 | **Jenerik tedarik:** AliExpress/1688'de birden çok satıcıda var, patentli/tek üretici ürünü değil | Aynı ürünü farklı satıcı fotoğraflarıyla bul (benzer ≠ aynı) | Notlarda "jenerik" diye işaretlenen ürünler: 052, 054, 066, 069, 070, 075, 084, 099, 114, 121 (toplam 48 not) |

**Eşik nereden?** Kaynak çalışmada 7 maddelik bu liste milyonluk ürünlerden türetildi ve "en az 4" ile kullanıldı.
Ölçülmüş zayıflık: gerçek aday listesinde adayların çoğu 5–7/7 aldı → **DNA puanı kapıdır, sıralama değildir.**
Sıralama `aliexpress-firsat` becerisindeki sıra puanıyla (mekanizma gücü + doygunluk + marj + üretilebilirlik) yapılır.

## 3. Mekanizma tablosu (izleyici neden durdu / neden paylaştı)

Her milyonluk not tek bir birincil mekanizmaya atandı. Medyan izlenme = notun açılan videosu. p/b = paylaşım ÷ beğeni.

| Kod | Mekanizma | Notlar | Medyan izlenme | p/b medyan | Ürünün taşıması gereken özellik |
|---|---|---|---|---|---|
| M3 | Obje başka bir şeye benziyor (görsel şaka) | 038, 063, 083, 085, 112, 123, 134, 135 | 9,9 MN | 0,45 | Tanıdık bir nesnenin (yiyecek, araba, ayak) birebir formu; yazı gerekmez |
| M2 | Canlıyı karaktere çevirme | 006, 057, 058, 064, 065, 075, 081, 087, 096, 103 | 9,7 MN | 0,52 | Giyilebilir kılık; canlının yüzü açıkta; vücut şekliyle şekil oyunu (063, 081: sosis köpeği) |
| M4 | Görünmeyeni görünür yapma | 014, 052, 066, 077, 102 | 5,1 MN | 0,22 | Sonuç fiziksel yığın/iz bırakıyor; önce-sonra tek planda |
| M5 | Jenerik ürün + kimlik/kültür/ritüel | 051, 054, 067, 068, 076, 101, 106, 127, 131 | 4,5 MN | 0,31 | Deseni/diski/baskısı değiştirilebilir gövde |
| M13 | Mekanizma merakı (nasıl çalışıyor?) | 060, 093, 095, 111, 114, 118 | 4,5 MN | 0,27 | Görünür hareket eden parça veya akış |
| M10 | Beden rahatlaması (POV acı/uyku/yol) | 053, 059, 061, 099, 109, 117, 124, 126, 133, 138, 139 | 4,1 MN | 0,46 | Rahatlama tek pozda görülüyor — ⚠️ sağlık iddiası yazılmaz |
| M11 | Küçük sürtünme → 3 saniyede çözüm | 001, 003, 055, 092, 108, 110, 116, 121, 125, 130 | 3,6 MN | **0,91** | Tek elde, tek adım; "bilmediğin ihtiyaç" |
| M14 | Zararsız kaba şaka / prank | 088, 091, 098, 100, 129 | 2,5 MN | **1,44** | Kurbanın tepkisi görülebiliyor; zarar yok |
| M12 | Ekransız aile oyunu hediyesi | 040, 073, 105, 122 | 2,4 MN | 0,77 | Birden çok kişi aynı anda kullanıyor |
| M1 | Anlık dönüşüm (oda/ürün) | 020, 036, 037, 062, 069, 070, 078, 113 | 2,3 MN | 0,49 | Açık/kapalı iki net hâl; karanlıkta ışık |
| M7 | Canlıyı bedende taşıma | 056, 071, 079, 086, 115, 137 | 2,1 MN | **0,89** | Canlının yüzünü çerçeveleyen açıklık, eller serbest |
| M8 | Evcil hayvan: problem → huzur | 005, 044, 047, 074, 080, 082, 084, 119, 120, 128, 132 | 2,1 MN | **0,84** | Problem anı tek planda (gece kamerası 084, 120); son kare hayvan yuvasında |
| M9 | Bebek uykusu/huzuru | 004, 089, 094 | 2,0 MN | 0,93 | ⚠️ bebek güvenliği iddiası yasak |
| M6 | Nesil nostaljisi | 072, 097, 107, 136 | 1,6 MN | **0,90** | Bir nesle ait ikonik form + bugünkü işlev |
| (aday) | Müşterinin kendi hayvanı ürüne basılıyor | 090, 104 | — | — | Yalnız 2 not → desen sayılmaz |

**Okuma:** En çok izlenen M3 + M2 (ikisi de yazısız tek kare şaka). En çok paylaşılan M14, M11, M6, M7, M8.
M4 ve M13 izleniyor ama az paylaşılıyor → organik yayılım için tek başına zayıf.

## 4. Eleyiciler (biri varsa ELE — "riskli ama güzel" diye geçilmez)

| Risk | Kanıt notları | Ne yapılır |
|---|---|---|
| Lisanslı karakter / marka görünümü (Batman, Porsche, BMW, Grinch, çizgi film parası, oyun silahı) | 072, 083, 085, 087, 088, 093, 097, 106, 112, 133, 135 | Ürün logosuz ve karakterden bağımsız değilse ELE. Kendi karakteriyle aynı mekanizma aranabilir. |
| Sağlık/tedavi iddiasına dayanan fayda | 059, 109, 117, 119 | Fayda iddiasız gösterilemiyorsa ELE |
| Bebek uyku/güvenlik iddiası | 004, 089, 094 | Güvenlik iddiası gerektiriyorsa ELE; çocuk ürünü sertifika ister |
| Kargo riski: sıvı, cam, pil ağırlıklı, ateş, hacimli/ağır | (kaynak aday değerlendirmesi: ateş çukuru, ferrofluid şişe, squat makinesi elendi) | ELE ya da kullanıcıya açık risk olarak sor |

## 5. Karşı-kanıtlar ve sınırlar (ölçüt yazarken unutulmaz)

- **Ürün değişimi kancadan büyük:** aynı video şablonu bir üründe 2–22 bin, başka üründe 3–15 milyon aldı (082, 091; ayrıca 098, 103). → DNA'ya uymayan ürün iyi kancayla kurtulmaz.
- **Kalıp kopyası garanti değil:** aynı ürün ve aynı kancayla çekilen ikinci video 12 beğenide kaldı (063); bir hesabın 13 videosunda 1 milyon çıktı (084). Ölçülen kazanan oranı ~%2–8 → ürün seçimi, video sayısının yerini tutmaz.
- **Kazanan an:** ürünün sonucunun ya da hayvanın ürünle "o şeye dönüştüğü" anın yakın planı (063 köpek ekmeğin içinde, 084 köpek tünel yatakta, 066 tüy yığını). Ürün böyle bir an üretemiyorsa V1/V2 puanı verilmez.
- **Elektrikli ürünler:** milyonluk kayıtların ~31'inde var ama en çok izlenen M2+M3 grubunda yalnız 1 tane (112). Elektrikli aday M1/M13/M11'e oturmalı.
- **Satış ölçülmedi:** bu DNA izlenme ve paylaşım üzerinden kuruldu; "çok satar" demez, "gösterilirse durdurur" der.
- **Pazar farkı:** kaynakların çoğu ABD. TR notları azdır (039, 041, 049, 125); TR'de fiyat ve sosyal kanıt dili öne çıkıyor (039: "4500+ yorum", 049 ve 125: fiyat ekranda).
