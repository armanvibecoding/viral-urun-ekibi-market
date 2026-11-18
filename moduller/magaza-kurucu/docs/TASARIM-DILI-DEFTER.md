# Tasarım dili defteri (geliştirme belgesi, pakette YOK)

> 0.3.0'dan beri çalışma zamanında okunmaz. Çalışma zamanı çekirdeği: `src/ortak/tasarim-dili.md` (≤ 8 KB, göreli tarifler). Bu defter SESSA (ağız bandı) üzerindeki px ölçümlerinin ve K1–K78 kurallarının kaydıdır; px puanlama ve "≥ 7 gösterim kapısı" kalibre edilmediği için çalışma zamanından çıkarıldı (`docs/ESKIDI.md`). Hukuki maddeler (K70, K77) bilgi notuna çevrildi; kenar kuralı tek değere indi (ürün hiçbir kenara değmez, her kenarda ≥ %6).

---

# Mağaza Kurucu tasarım dili (v1)

Tarih: 2026-11-16 · Sahibi: `tasarim-dili` ajanı · Okuyanlar: `prompt-muhendisi` (prompt yazar), `tasarim-direktoru` (kabul eder).

> **Plugin içinde okuyan model için:** Bu dosya `src/ortak/tasarim-dili.md`'nin kopyasıdır (gorseller ve marka skill'lerinde aynı). Hex, ürün ve metin örnekleri SESSA (ağız bandı) markasınındır; yeni marka için değerler `uretim-promptlari.md` yer tutucularıyla ve K10 türetme sırasıyla yeniden üretilir. `research/` yolları yalnız repo içi kaynak kaydıdır, pakette yoktur. Dosyanın sonundaki **karar güncellemeleri** önceki kuralların üstündedir.

Bu dosya tek doğru kaynaktır. Her kural ölçülebilir: px, hex, ağırlık, karakter ya da kelime sayısı. "Güzel olsun" türünden kural yoktur.

**Kaynaklar**
- `research/test4/cikti/ELESTIRI.md`: 30 kural, kritik 10 kusur, 14 teknik. Hepsinin bu dosyadaki karşılığı Ek A'da.
- Kütüphane: `research/kutuphane/{saglik,guzellik,moda,gadget,ev}/OZET.md` ve `*/KART.md` (25 marka; 5 niş tamam).
- Kullanıcının sevdiği iki örnek: `research/test2/ref/stil-hero.jpg` (SomniFix 01) ve `stil-kart.jpg` (Pulsetto lite-07).
- Reddedilen turlar: test2 (tipografi, banner ve renk sorunlu), test3 ("AI slop"), test4 (V1/V2; hiçbiri 7/10'u geçmedi).
- Hafıza: "Ürün görsel zevki" ve "Ürün görselini kodla çizme".
- Ürün referansı: `research/test1/cikti/G1-ana.png` (SESSA).

**Ölçü sözleşmesi**
- Kare tuval 1254×1254, masaüstü banner 1942×809 (12:5), mobil banner 1122×1402 (4:5). Bunlar ChatGPT Image'ın verdiği gerçek boyutlardır.
- Bütün ölçüler bu tuvallerde px cinsindendir. "Tuvalin %9'u" gibi font boyu mu harf yüksekliği mi belli olmayan ifade yazılmaz (test4 kökü).
- Yazı ölçüsü her zaman **cap yüksekliği** (büyük harf yüksekliği) olarak verilir. Yanında yaklaşık font boyu yazılır: font ≈ cap ÷ 0,70.
- Çizgi kalınlığı 1254 tuvalde **2 px**'tir. Bu, 627 px gösterimde 1 CSS px eder. "1 px çizgi" denince bu kastedilir. 1254 tuvalde gerçek 1 px, telefonda kaybolur.

Kurallar K1–K78 olarak numaralı (78 kural). Bunlara ek olarak 10 slot şablonu (S-B1, S-B2, S-G1…S-G8) ve logo kuralı (Ek B) var.

---

## 1. İlkeler

- **K1. İnsansız, grafik, ürün odaklı.** İnsan, el, yüz, model ve yatak sahnesi 0. İstisnalar niş farklarında (§8) yazılıdır ve kullanıcı onayı ister.
- **K2. Kaliteyi model getirir.** Görselin tamamını (sahne, ürün, yazı, ikon) ChatGPT Image üretir. Kod yalnız iki iş için kullanılır: OCR ile bozuk Türkçe harfi düzeltmek ve ölçü/kontrast ölçmek. PIL ile şablon çizilmez; kullanıcı bu yolu "muazzam ötesi kötü" bulmuştu.
- **K3. Referans ilkedir, kopya değildir.**
  - Ürün referansından yalnız kimlik alınır: ambalaj, logo, bant.
  - Dizilim, açı, kadraj, gölge yönü ve şeffaf taşıyıcı kopyalanmaz.
  - Stil örneklerinden yalnız kalite seviyesi ve sakinlik alınır; düzen, metin, marka ve renk alınmaz.
  - Test4'te aynı G1 dizilimi 6 görselin 4'ünde tekrarlanmıştı.
- **K4. Açı tekrarı yasak.** Her görselin promptunda ayrı bir AÇI satırı zorunludur: kamera yüksekliği (derece), ürünün dönüşü (derece), ürünün tuvaldeki yeri (px). Bir galeride aynı dizilim ve açı en fazla 1 kez kullanılır.
- **K5. Tek görsel = tek prompt = tek mesaj.** Çoklu istekte model kolaj, yanlış oran ve ürün kayması üretiyor: test4 `V2/` istenen kareler 3:2 kolaj olarak geldi, poşet beyaza döndü.
- **K6. Turda tek değişken.** Bir üretim turunda tek eksen değişir (tipografi, düzen ya da renk). Kalanı önceki turdan sabit kalır.
- **K7. Doğrulanabilir metin.** Görseldeki her sayı ve iddia ürün etiketinden, ölçüden ya da politikadan doğrulanabilir olmalıdır. Uydurma yüzde, kullanıcı sayısı, "klinik", hekim, basın ve rozet yok.
  - Kaynak/dipnot satırı yalnız gerçek ve yazılı bir kaynak varsa konur. Kaynak yoksa satır hiç basılmaz; boş yer bırakılmaz.
- **K8. Metin nereye gider.**
  - Banner görseli **metinsiz** üretilir. Banner metnini tema canlı HTML olarak yazar (`e-hero-b` H1).
  - Google/Meta feed'ine giden ürün görseli (feed G1) yazısızdır.
  - Mağaza galerisinin 1. görseline en fazla **1 gerçek** güven satırı ya da rozet konabilir (koordinatör kararı, 2026-11-16).
  - Galerinin geri kalanında yazılı grafik kare serbesttir. Eski "en fazla 1 açıklamalı görsel" kuralı iptal edildi: yazılı grafik galeri 5 nişte de norm ve kullanıcı bunu seviyor.
- **K9. Tek şablon sistemi.** Bir galerideki bütün kareler aynı kenar boşluğunu, aynı başlık konumunu, aynı font çiftini ve aynı renk rollerini kullanır. SomniFix 02–12 bunu yapıyor: başlık hep x=112/1600.

## 2. Renk sistemi

### 2a. Paleti üründen türetme (4 rol)

**K10. Türetme sırası:**
1. **Metin ve koyu panel:** ambalajdaki en koyu baskı rengi. Logo laciverti gibi; tek değer, ±4 RGB.
2. **Zemin:** ürün yüzeyiyle luminans kontrastı en az 1,5:1 olan, en açık sıcak nötr.
3. **İkincil yüzey (kart):** zeminden 2–8 RGB birimi açık nötr ve 2 px kenar çizgisi.
4. **Vurgu:** ambalajdaki tek doygun aksan rengi. Kullanım K16'da.

Bunlara ek olarak her zemin için bir ikincil metin tonu türetilir. Bu ton açık zeminde ≥4,5:1, koyu zeminde ≥4,5:1 kontrast vermelidir.

### 2b. SESSA paleti (ölçülmüş)

**K11.**

| Rol | Hex | Nerede | Kontrast (WCAG, ölçüldü) |
|---|---|---|---|
| Zemin | `#F2EEE8` | Açık kareler | Lacivert metin 11,61:1 |
| Metin + koyu panel + logo | `#14304F` | Başlık, gövde, durak kartı, logo | — |
| Açık kart | `#FAF8F5` | Tonlu zemin üstünde kart | Lacivert metin 12,65:1 |
| Kart kenarı | `#E3DCD2` | 2 px | — |
| İkincil metin (açık zeminde) | `#5B6B7D` | Gövde, meta, eyebrow | 4,73:1 krem · 5,15:1 açık kart |
| İkincil metin (lacivert zeminde) | `#B9C3CF` | Gövde, eyebrow | 7,52:1 |
| Ayırıcı çizgi | `#C6C8C9` | Lacivertin %20'si, krem üstünde | Yalnız çizgi |
| Vurgu (pas) | `#B5533C` | Görsel başına 1 öğe | 4,26:1 krem · 4,64:1 açık kart · **2,73:1 lacivert** |
| Ürün: kraft poşet | ≈ `#CBB5A0` | Ürünün kendisi | Krem 1,71 · açık kart 1,86 · lacivert 6,81 · `#E6DFD3` 1,49 ✗ |
| Ürün: bant | ≈ `#CEB498` | Ürünün kendisi | Krem 1,71 · lacivert 6,78 |

Ürün renkleri `test1/cikti/G1-ana.png`'den kutu ortalamasıyla ölçüldü.

### 2c. Renk kuralları

- **K12. Tek lacivert.** Metin, panel ve logo aynı `#14304F` (±4 RGB). Siyaha yakın lacivert (`#000A2C`–`#021E40`) ve ikinci bir mavi yasak. Test4'te 4 ayrı lacivert vardı.
- **K13. Kontrast eşikleri.**
  - Metin ≥ 4,5:1.
  - Cap ≥ 48 px başlık ≥ 3:1. Yine de hedef 4,5:1'dir.
  - Ürün ile arkasındaki zemin ≥ 1,5:1.
  - Kum ya da bej zemin ikincil metin taşıyamaz (3,42:1).
- **K14. Kraft ürün kum ya da bej zemine konmaz.**
  - Test4'te kraft kum panel üstünde 1,01:1 ve 1,14:1 ölçüldü.
  - İzinli zeminler: krem `#F2EEE8` (1,71), açık kart `#FAF8F5` (1,86), lacivert `#14304F` (6,81).
  - Banner ve kahraman görselde lacivert tercih edilir.
- **K15. Tonal metin hiyerarşisi.** Başlık tam tonda: açık zeminde `#14304F`, lacivert zeminde `#FAF8F5`. Gövde, meta ve eyebrow ikincil tonda: `#5B6B7D` ya da `#B9C3CF`. Bütün metnin tek tonda olması yasak.
- **K16. Pas: görsel başına tam 1 grafik öğe.**
  - Biçimi şunlardan biri: 48×4 px çizgi, 12–16 px dolu nokta ya da bir ikonun çizgisi.
  - Ton `#B5533C`, ±6 RGB.
  - Ürünün kendi baskısındaki pas çizgi bu sayıma girmez.
  - Metinsiz bannerda grafik pas öğesi 0'dır.
  - Lacivert zemin üstüne pas konmaz (2,73:1). Lacivert karede pas, açık kartın içine konur (4,64:1).
- **K17. Düz yüzey.** Kart ve panelde köşeden köşeye renk farkı ΔRGB ≤ 3. Renkten renge degrade, vinyet ve radyal parlama yasak.
- **K18. Doğal ışık düşüşü istisnası.**
  - Yalnız iki yerde serbest: banner sakin alanı ve ürünlü sahne zemini.
  - Aynı ton içinde en fazla 14 RGB birimi açıklık farkı, tek yönde: sağ üstten sola ve aşağıya.
  - Lacivertte izinli aralık `#14304F` → `#1F3D5C` (1,2:1). Kremde `#F2EEE8` → `#E8E2D8`.
- **K19. Kart rengi.** Ya tonlu zemin üstünde açık kart (`#FAF8F5` + 2 px `#E3DCD2`, zemin `#F2EEE8`; SomniFix 11 mantığı) ya da lacivert zemin üstünde açık kart (stil-kart mantığı). Açık zeminde koyu kum kart yasak; test4 V1-3/V2-3'te "çamurlu" duruyordu.
- **K20. Renk sayısı.** Bir görselde en fazla 4 sistem rengi kullanılır: zemin, lacivert, ikincil ton ve pas. Ürünün kendi renkleri bu sayıya dahil değildir.
- **K21. Durak kartı.** Galeride en fazla 1 koyu (lacivert) zeminli kare olur. 5 sağlık markasının 3'ünde bu ritim kırıcı var.

## 3. Tipografi sistemi

- **K22. Ölçü cap ile verilir.** Promptta şu biçimde yazılır: "büyük harf yüksekliği X px (yaklaşık font boyu Y px)". Küçük harfle başlayan satırda (ör. "gece") x yüksekliği değil, aynı fonttaki büyük harf yüksekliği esas alınır.
- **K23. Onaylı eşleşme A: serif başlık + grotesk gövde** (V2 temeli).
  - Başlık: dar (condensed), uzun oranlı, yüksek kontrastlı serif, **Regular 400**. Tarif: Instrument Serif / GT Super Display / Editorial New ailesi; SomniFix galeri başlığı seviyesi.
  - Gövde, etiket ve eyebrow: tek grotesk, Inter benzeri; 400 gövde, 500 etiket.
  - Bold, Black ve kalın kama serif yasak. V2'nin kalın serifi "kafe menüsü" gibi duruyordu.
- **K24. Onaylı eşleşme B: tek grotesk aile.**
  - Başlık en fazla SemiBold 600; 700 ve üstü yasak. V1 ExtraBold çıkmıştı.
  - Gövde 400, etiket 500.
  - Tarif: Inter / Figtree / Söhne benzeri; modada dar (condensed) büyük harf varyantı serbest.
- **K25. Eşleşmeyi niş anahtarı ve ambalaj seçer.**
  - Sağlık: A.
  - Güzellik: krem/sıcak estetikte A; cihaz ve klinik-beyaz estetikte B.
  - Gadget: B. Galeri başlığı 5/5 sans ölçüldü.
  - Moda: B. Serif 0/5.
  - Ev: B (ayrıntı §8). Ev galerileri 5/5 sans ölçüldü; serif yalnız tek vurgu olarak.
  - Ürünün ambalaj logosu serifse ve niş B ise başlık B'de kalır; serif yalnız logoda yaşar.
  - SESSA: A.
- **K26. Ölçek (1254 kare tuval).** A ve B'de aynı ölçek kullanılır.

| Kod | Rol | Cap (px) | Yaklaşık font (px) | Aile / ağırlık | Satır aralığı | Harf aralığı |
|---|---|---|---|---|---|---|
| T0 | Dev sayı | 300 | 430 | Başlık ailesi 400 | 1,0 | −%2 |
| T1 | Başlık | 76 | 108 | Başlık ailesi 400 (A) / 600 (B) | 1,0–1,05 | −%1 |
| T2 | Alt başlık | 34 | 48 | Grotesk 400 | 1,35 | 0 |
| T3 | Kart/satır başlığı, etiket başlığı | 48 | 69 | Başlık ailesi 400 (A) / 500 (B) | 1,1 | 0 |
| T4 | Kart gövdesi, ikon etiketi | 30 | 42 | Grotesk 400 (gövde) / 500 (ikon etiketi) | 1,35 | 0 |
| T5 | Meta, güven satırı, eyebrow, dipnot | 26 | 37 | Grotesk 400 (eyebrow 500) | 1,3 | 0 (eyebrow +%10) |

  Oranlar ELESTIRI kural 9'u sağlar:
  - T2 = T1 × 0,45.
  - T5 = T2 × 0,76 ≈ 0,75.
  - T3 = T4 × 1,6.
  - Eyebrow, kuralda T4 × 0,8 = 24 px'tir. Bu, K28'deki 26 px alt sınırın altına düştüğü için 26 px'e çekildi; alt sınır önceliklidir.
- **K27. Banner ölçeği.** Banner görselinde yazı yoktur (K8). Tema H1'i HTML olarak yazar. İleride metinli banner gerekirse başlık cap'i tuval yüksekliğinin %8'i olur (1942×809'da 65 px); diğer roller aynı oranla ölçeklenir.
- **K28. En küçük metin.** Cap ≥ 26 px (1254'te). 360 px telefonda bu ≥ 7,5 px eder.
- **K29. Dikey ritim.**
  - Başlık → alt başlık: 0,5 × T1 cap = 38 px.
  - Alt başlık → meta: 1,0 × T1 cap = 76 px.
  - Eyebrow → başlık: 24 px.
  - Grup içi boşluk, gruplar arası boşluğun yarısıdır.
- **K30. Satır kırılımı.**
  - Başlık en fazla 2 satırdır; her satırda en az 2 kelime olur. Yetim kelime yok.
  - Kart başlığı ve ikon etiketi tek satır, ≤ 14 karakter.
  - Gövde ya tek satır olur ya da her satırda en az 2 kelime olacak şekilde kırılır.
  - Satır kırılım yeri promptta "/" ile verilir.
- **K31. Kelime limitleri.**
  - Başlık ≤ 5 kelime.
  - Alt başlık ≤ 12 kelime.
  - Kart gövdesi ≤ 6 kelime.
  - Görselin toplamı ≤ 40 kelime (SomniFix 40–87; kullanıcı sadeyi seçti).
- **K32. Tek italik vurgu.** Başlıkta en fazla 1 kelime (en fazla 2) başlık serifinin italik 400'ü ile yazılır. Görsel başına 1. Örnekler: SomniFix "Unlock *greater sleep*", Grande "The *Perfect* Size". B eşleşmesinde italik yok.
- **K33. Eyebrow etiketi.**
  - Büyük harf, +%10 harf aralığı, T5 (26 px cap), grotesk 500, ikincil ton.
  - Başlığın 24 px üstünde ve aynı sol hatta durur.
  - Bilgi karelerinde (G2–G8) zorunlu; G1'de ve bannerda yok.
  - Hap ya da kutu içine alınmaz; test3'teki hap etiketler "slop" bulundu.
- **K34. Marka adı yalnız logo çiziminde.** Görselde marka adı yalnız ambalajdaki logo çiziminde görünür. Başlık ve gövde metninde marka adı geçmez; geçmesi gerekiyorsa logo çizimiyle yazılır. Test4'te "SESSA?" iki ayrı fontla yazılmıştı.
- **K35. Temiz yazı.** Metin düz vektör gibi olur: doku, kabartma, kâğıt baskı izi ve hale yok. Türkçe harfler (ı, İ, ş, ğ, ü, ö, ç) birebir doğru yazılır.
- **K36. Ayraç noktası.** "·" işaretinin iki yanında 1 em boşluk olur. Bir satırda en fazla 3 madde.

## 4. Izgara

- **K37. Kare (1254×1254).**
  - Kenar boşluğu dört yönde 88 px (SomniFix 112/1600 = %7). İçerik alanı x 88–1166.
  - 12 kolon: kolon 68 px, oluk 24 px.
  - İlk metnin cap üstü y=112'de başlar.
- **K38. Masaüstü banner (1942×809).** Yatay kenar 117 px, dikey kenar 97 px. 12 kolon: kolon 120 px, oluk 24 px.
- **K39. Mobil banner (1122×1402).** Kenar dört yönde 80 px. 12 kolon: kolon 58 px, oluk 24 px.
- **K40. Boşluk birimi.** 8 px. İzinli değerler: 8 / 16 / 24 / 32 / 48 / 64 / 88 / 120.
- **K41. Sol hat.** Bütün metin satırları aynı x'te başlar (±2 px). Serifin optik taşması için en fazla 3 px tolerans var. Test4'te 5–8 px kayma ölçüldü.
- **K42. Metin–ürün mesafesi.** En az 50 px. Metin ürünün üstüne binmez.
- **K43. Kenar teğeti yasak.** Ürün ya kadrajdan en az %15 taşar ya da kenara en az 88 px uzak durur. 1–87 px yakınlık yasak.
- **K44. Ölü bölge yasak.** Tuval 3×3'e bölünür (hücre 418 px). Hiçbir hücre %100 boş kalmaz. Boş hücre kaçınılmazsa kompozisyon simetrik kurulur (S-G1 düzeni).
- **K45. Ürün ölçeği.**
  - Ana görselde (G1) ürün grubu yüksekliği 778–878 px (%62–70).
  - Banner ürün grubu, tuval yüksekliğinin %70–75'i olur; üst ve alt boşluk eşittir (±10 px).
  - Makro karelerde ürün kadrajdan en az %15 taşar.
- **K46. Hizalama.**
  - Ortalı düzen yalnız G1 (simetrik poster), ikon kartı ızgarası (stil-kart) ve logoda.
  - Diğer bütün kareler sol hizalı.
  - "Her şeyi ortalamak yasak" kuralı ana görsel için kaldırıldı; kullanıcının sevdiği SomniFix 01 tamamen ortalı.
- **K47. Makro kotası.** 8 karelik galeride en az 2 kare makro olur: ürün kadrajdan taşacak kadar yakın, iplik ya da doku seçilir. Turun en iyi sonucu (V2-3) makroydu.

## 5. Slot şablonları

Kare ölçüleri 1254×1254 içindir. Her slotta şunlar yazılıdır: amaç, düzen şeması, öğeler, ölçüler, yazı limitleri, açı kuralı. Galeri sırası sağlık nişi içindir; diğer nişlerin sırası §8'de.

**K48.** Her slot promptu bu şablonun ölçülerini px olarak taşır. Slotun açı satırı galerideki diğer slotlarla çakışmaz (K4).

### S-B1 Masaüstü banner (1942×809, metinsiz)

- **Amaç:** Ana sayfa ilk ekranı. Metni tema yazar.
- **Zemin:** Lacivert `#14304F`. Sağ üstten gelen ışıkla ürün çevresinde `#1F3D5C`'ye açılır (K18).
- **Sol bölge (x 0–874):** Sakin alan. Öğe yok ama boş da değil: ton/ışık geçişi var, en koyu ton sol kenarda.
- **Sağ bölge:** Ürün grubu.
  - Yükseklik 582 px (%72), y 113–695: üst ve alt boşluk eşit.
  - x 1100–1825; sağ kenar boşluğu 117 px.
- **Pas:** grafik pas öğesi 0 (K16).
- **Yazı limiti:** 0 karakter. Ürünün kendi baskısı dışında yazı, logo ve ikon yok.

```
┌──────────────────────────────────────────────────────┐ 809
│ ░░ koyu ton ░░░░░░░░ → ışık geçişi →    ┌──ürün───┐  │
│ (sakin alan, x 0–874)                   │ grubu   │  │ y 113
│                                         │ %72 h   │  │
│                                         └─────────┘  │ y 695
└──────────────────────────────────────────────────────┘
 0                    874            1100          1825 1942
```

### S-B2 Mobil banner (1122×1402, metinsiz)

- **Zemin:** Masaüstüyle aynı lacivert ve aynı ışık yönü.
- **Üst bölge (y 0–491, %35):** Sakin alan; ton geçişi var, öğe yok.
- **Ürün grubu:** y 571–1290 (719 px), x 80–1042 içinde ortalı.
- **Açı:** Masaüstünden farklı olmak zorunda (K4).

```
┌──────────────┐ 0
│ sakin alan   │
│ ton geçişi   │ 491
│              │ 571
│  ┌ürün────┐  │
│  │ grubu  │  │
│  └────────┘  │ 1290
└──────────────┘ 1402
```

### S-G1 Ana görsel, simetrik poster

- **Amaç:** Mağaza G1. Feed G1 ayrı, yazısız packshot'tır (K8).
- **Zemin:** krem `#F2EEE8`.
- **Başlık:** T1, ortalı, cap üst y=112. Tek satır, ≤ 4 kelime, ≤ 20 karakter.
- **Pas:** 48×4 px çizgi, ortalı, y=244.
- **Ürün:** grubu y 284–1062 (778 px), yatayda ortalı.
- **Güven satırı:** T5, ortalı, cap üst y=1112, ikincil ton. Tam 1 satır, ≤ 3 madde, yalnız gerçek bilgi. Bu, K8'deki "en fazla 1 güven satırı"dır.

```
┌───────────────────────────┐
│      Başlık (T1, ortalı)  │ y 112–188
│           ──              │ y 244 pas
│        ┌────────┐         │ y 284
│        │ ürün   │         │
│        │ ortada │         │
│        └────────┘         │ y 1062
│ madde · madde · madde (T5)│ y 1112
└───────────────────────────┘
```

### S-G2 Durak kartı: lacivert zeminde ikon kartları (stil-kart mantığı)

- **Zemin:** `#14304F`, düz.
- **Eyebrow:** cap üst y=200, ortalı, `#B9C3CF`.
- **Başlık:** T1, ortalı, `#FAF8F5`, cap y 250–326.
- **Kartlar:** 3×2, her biri 343×300 px. Satırlar y 430–730 ve 754–1054. Aralık yatayda da dikeyde de 24 px. Kolonlar x 88–431, 455–798, 822–1165.
- **Kart içi:** `#FAF8F5`, köşe 10 px. 75 px ikon + 32 px boşluk + T4 etiket (500); blok kartta yatay ve dikey ortalı.
- **Ürün:** yok.
- **Pas:** ikonlardan birinin çizgisi.

```
┌─────────────────────────────┐
│         EYEBROW             │ 200
│     Başlık (T1, ortalı)     │ 250–326
│ ┌─────┐ ┌─────┐ ┌─────┐     │ 430
│ │ ikon│ │ ikon│ │ ikon│     │
│ │etkt │ │etkt │ │etkt │     │ 730
│ └─────┘ └─────┘ └─────┘     │ 754
│ ┌─────┐ ┌─────┐ ┌─────┐     │
│ └─────┘ └─────┘ └─────┘     │ 1054
└─────────────────────────────┘
```

### S-G3 Nasıl çalışır: işaret çizgili tek bant

- **Zemin:** krem.
- **Metin:** Eyebrow cap üst y=112; başlık T1 cap y 162–238. İkisi de x=88'de, sol hizalı.
- **Ürün:** Tek bant grafik nesne olarak; poşet yok. Merkez (627, 700), görünen genişlik 760 px. Ürünün kendisi kahramandır (teknik 1).
- **Etiketler:** 3 adet. Her biri T3 başlık + T4 tek satır gövde. Her etiket parçaya 2 px lacivert çizgiyle bağlanır; çizgilerden birinin ucunda 14 px pas nokta olur.
  - a: üstte ortalı, cap üst y=318.
  - b: altta solda, x=247, cap üst y=990.
  - c: altta sağda, sağ hizalı, bitiş x=1007, cap üst y=990.

```
┌─────────────────────────────┐
│ EYEBROW / Başlık            │ 112–238
│        Etiket a             │ 318
│           │                 │
│   ╭───────●───────╮         │ bant
│   ╰──│─────────│──╯         │
│      │         │            │
│ Etiket b    Etiket c        │ 990
└─────────────────────────────┘
```

### S-G4 Dev sayı kartı

- **Zemin:** krem.
- **Sol kolon (x 88–600):**
  - Eyebrow, cap üst y=362.
  - T0 sayı, cap y 412–712.
  - T1 birim kelimesi, cap üst y=744.
  - 48×4 pas çizgi, y=850.
  - T2 tek satır, cap üst y=882, ≤ 22 karakter.
- **Sağ:** Makro ürün, x 640'tan başlar ve sağ kenardan en az %15 taşar.
- **Sayı kuralı:** Yalnız doğrulanabilir sayı (K7).

```
┌─────────────────────────────┐
│ EYEBROW            ╭────────┼─ (taşma)
│ 30                 │ makro   │
│ gece               │ ürün    │
│ ──                 ╰────────┼─
│ tek satır                    │
└─────────────────────────────┘
```

### S-G5 Kullanım adımları (insansız, grafik)

- **Zemin:** krem.
- **Metin:** Eyebrow cap üst y=112; başlık cap y 162–238. Altında 48×4 pas çizgi, y=262.
- **Satır kartları:** 3 adet, x 88–1166, her biri 260 px yüksek. y 314–574, 598–858, 882–1142.
- **Kart:** `#FAF8F5` + 2 px `#E3DCD2`, köşe 24 px, iç boşluk 42 px.
- **Kart içi:**
  - Adım numarası: T1, x=130.
  - Ürün durumu görseli: x 240–560 içinde, ≤ 180 px yüksek.
  - Metin bloğu: x 620'den başlar; T3 adım adı (≤ 12 karakter) + T4 tek satır (≤ 22 karakter).
- **Açı:** Her satırdaki ürün görseli farklı açıda.

```
┌─────────────────────────────┐
│ EYEBROW / Başlık / ──       │
│ ┌ 1 │ [ürün durumu] │ Ad    ┐│ 314
│ └───┴───────────────┴ gövde ┘│
│ ┌ 2 │ ...                   ┐│ 598
│ ┌ 3 │ ...                   ┐│ 882–1142
└─────────────────────────────┘
```

### S-G6 Kutu içeriği + ölçü

- **Zemin:** krem.
- **Metin:** Eyebrow ve başlık üst solda; pas çizgi y=262.
- **Kamera:** tam kuşbakışı (90°) flat lay.
  - Poşet solda yatık: x 88–508, y 380–900.
  - Ön bant x 600–1020, y 420–644, üstünde ölçü çizgileri.
  - İki bant daha, altında 24 px kaydırılmış yelpaze: y 700–940.
- **Ölçü çizgileri:**
  - Yatay: bandın 32 px üstünde, değeri ortada.
  - Dikey: x=1052, değeri yanında; değer x 1068–1152.
- **Liste:** T4, cap üst y=1060, x=88, "·" ayraçlı.

```
┌─────────────────────────────┐
│ EYEBROW / Başlık / ──       │
│ ┌──────┐   |──7,5 cm──|     │ 388
│ │ poşet│   ╭────────╮ ┬     │
│ │ yatık│   ╰────────╯ ┴ 4 cm│
│ └──────┘   ╭╭╭──────╮       │
│ 30 ağız bandı · 1 kilitli poşet │ 1060
└─────────────────────────────┘
```

### S-G7 Karşılaştırma (sınıfa karşı)

- **Zemin:** krem.
- **Metin:** Eyebrow ve başlık üst solda; pas çizgi y=262.
- **Tablo kartı:** `#FAF8F5` + 2 px `#E3DCD2`, köşe 24 px, x 88–1166, y 320–1092.
  - Sütun başlıkları T4 500, cap y 372–402.
  - Satır adı sütunu x 130–600, T3.
  - "Bu ürün" sütun merkezi x=760; sınıf sütun merkezi x=1010.
  - 4 satır, her biri 150 px. Satır ayırıcıları 2 px `#C6C8C9`, y 440 / 590 / 740 / 890.
  - Var: ince çizgi tik (40 px kutu, lacivert). Yok: "—" (ikincil ton). Metin değer: T4.
- **Ad kuralı:** Rakip marka adı yazılmaz. Sınıf adı kullanılır ("düz flaster", "geleneksel defter").

```
┌─────────────────────────────┐
│ EYEBROW / Başlık / ──       │
│ ┌───────────────────────┐   │ 320
│ │           Bu   Sınıf  │   │
│ │ Satır 1    ✓     —    │   │
│ │ Satır 2    ✓     —    │   │
│ │ Satır 3    ✓     —    │   │
│ │ Satır 4  değer  değer │   │
│ └───────────────────────┘   │ 1092
└─────────────────────────────┘
```

### S-G8 Zaman çizelgesi (bölünmüş)

- **Sol bölge (x 0–514, %41):** Ürün makrosu, kenardan kenara. Üst ve alt kenardan en az %15 taşar.
- **Sağ kolon (x 562–1166):**
  - Eyebrow cap üst y=112.
  - Başlık 2 satır, cap y 162–238 ve 275–351.
- **Çizelge:**
  - Dikey 2 px çizgi, x=580, y 476–1044.
  - 3 halka: dış çap 28 px, 3 px çizgi; merkezler y 500 / 760 / 1020. İlk halka dolu pas.
  - Etiketler x=632: T3 adım adı + T4 iki satır gövde.
- **Dil:** Yalnız deneyim dili; sonuç ya da sağlık vaadi yok.

```
┌───────────┬─────────────────┐
│ ╲ makro   │ EYEBROW         │
│  ╲ ürün   │ Başlık / 2. satır│
│   ╲       │ ● İlk gece      │ 500
│ (taşar)   │ │  gövde        │
│           │ ○ 1. hafta      │ 760
│           │ ○ 1. ay         │ 1020
└───────────┴─────────────────┘
```

## 6. Bileşenler

- **K49. Kart geometrisi.**
  - Köşe yarıçapı = kart genişliğinin %3'ü, en fazla 24 px.
  - İç boşluk dört yönde eşit: kart genişliğinin %8'i. Kart 2:1'den uzunsa kısa kenarın %16'sı.
  - Kartlar arası yatay ve dikey boşluk eşit: 24 px.
  - Gölge yok. Kartta ayraç çizgisi yok.
- **K50. Taban çizgisi.** Aynı satırdaki kartlarda başlık ve gövde aynı taban çizgisine oturur.
- **K51. Kart içi düzen.** İkon kartında ikon ve etiket yatay ve dikey ortalı (stil-kart). Bilgi kartında içerik sol hizalı. Başlık sığmıyorsa ikon başlığın üstüne çıkar; yan yana durmaz.
- **K52. İkon çizimi.**
  - Yalnız çizgi (outline); çizgi kalınlığı ikon kutusunun %4'ü (75 px kutuda 3 px).
  - Dolgu, dolu siluet, ışıma, hareket çizgisi, ok, dalga, rüzgâr ve parıltı yasak.
  - Bir sette boy farkı ±%5; tek renk.
  - Test4'te dolu sakal silueti emoji gibi duruyordu.
- **K53. İkon boyu.** İkon kutusu = ikon etiketinin cap'i × 2,5. T4 30 px için 75 px.
- **K54. İkon metaforu üründen türer.** SESSA sözlüğü:

  | Kavram | İkon |
  |---|---|
  | Dokuma kumaş | Kare içinde 3×3 iplik ızgarası |
  | Hava aralığı | Stadyum biçimli bant + ortada yatay yarık |
  | Oval kesim | İki ucu yarım daire dikdörtgen |
  | Tek kullanım | Tek bant + yanında "1" rakamı |
  | Kilitli poşet | Poşet silueti + üstte yatay kilit şeridi |
  | Gece | Hilal ay |
  | Ölçü | İki ucu dik kısa çizgili ölçü çizgisi |

  Klişe yasak: dalga = "nefes", ok = "hava", takvim = "30".
- **K55. İşaret çizgisi (callout).**
  - Parçadan etikete 2 px lacivert düz çizgi; yalnız yatay ya da dikey, en fazla 1 adet 90° kırılım.
  - Parça üstündeki ucunda 12 px dolu nokta (lacivert ya da tek pas öğesi).
  - Çizgi etiketten 16 px önce biter. Çizgiler kesişmez.
  - Etiket = T3 başlık + T4 gövde.
  - Örnekler: SomniFix 08, Purest 06, Pulsetto fitm-01.
- **K56. Ölçü çizgisi.**
  - 2 px lacivert çizgi; iki ucunda 16 px dik kısa çizgi. Ok başı yok.
  - Değer T4, çizgiden 16 px uzakta; "7,5 cm" biçiminde, Türkçe ondalık virgülüyle.
  - Ürün kenarından 32 px uzakta durur. Örnek: Wavytalk 04.
- **K57. Dev sayı.** T0 sayı + altında T1 birim kelimesi + T2 tek satır açıklama. Sayının yanında yıldız ya da dipnot işareti yalnız gerçek kaynak varsa bulunur. Örnekler: SomniFix 11, Grande 05, Peace Out 06.
- **K58. Ayırıcı çizgi.** 2 px `#C6C8C9` (lacivertin %20'si). Yalnız tablo satırları arasında ve kart dışı bölüm ayrımında kullanılır.
- **K59. Tablo.** Satır yüksekliği 150 px. Var = ince çizgi tik; yok = "—". Kırmızı ✕ ve yeşil ✓ yok; renk sistemde yok.
- **K60. Zaman çizelgesi.** 2 px dikey çizgi; halka 28 px dış çap, 3 px çizgi. En fazla 4 adım. Adım adı ≤ 10 karakter.
- **K61. Güven satırı.** T5, ikincil ton, "·" ayraçlı, ≤ 3 madde. Yalnız politika ve gerçek bilgi: kargo, iade, gönderim yeri. Sayı içeriyorsa sayı gerçek olmalı.
- **K62. Kaynak/dipnot satırı.** T5, alt kenardan 88 px yukarıda, sol hizalı. **Yalnız gerçek, yazılı kaynak varsa** basılır (K7). SESSA'da şu an yok.
- **K63. Satın alma kutusu güven satırı (sitede).** Sepete Ekle butonunun hemen altına bitişik, tek satır: `Ücretsiz kargo · 14 gün iade`. Sayılar gerçek politikadan gelir. Butona bitişik güven satırı ev nişinde 3/5, gadget'ta 4/5 ölçüldü.
- **K64. Ürün gerçekçiliği.**
  - Bant kâğıt inceliğindedir; kenar kalınlığı kısa kenarın %0,3'ünü geçmez, köşeler hafif kalkık olabilir.
  - Doku düzenli yatay ve dikey iplik ızgarasıdır; makroda tek tek iplikler görünür (V2-3 seviyesi).
  - Yazıya ya da labirente benzeyen desen ve köpük ped kalınlığı yasak.
- **K65. Işık.** Tek kaynak sağ üstte. Gölge sola ve aşağıya düşer; opaklık %15–25; ürün tabanından en fazla %8 uzanır. Bütün nesnelerin gölgesi aynı yönde.

## 7. Yasaklar

- **K66. Süs:** taş/kaide, kuru çiçek, bitki, yaprak, organik leke şekli, kumaş drape, bokeh, ışık hüzmesi, parlama, yansıma havuzu, mermer, ahşap masa, zemin–duvar çizgisi.
- **K67. İkon:** 3D, emoji, dolu siluet, ok, dalga, rüzgâr, ışıma ve hareket çizgisi.
- **K68. Renk:** renkten renge degrade, vinyet, radyal parlama, ikinci mavi, siyaha yakın lacivert, sistem dışı renk. Kraft ürün kum ya da bej zeminde.
- **K69. Metin:**
  - İstenmeyen yazı, yüzde, rozet, mühür, yıldız puan, "klinik", hekim, basın logosu.
  - Stil ya da yön adı, renk kodu, px değeri, tuval ölçüsü görsele yazılmaz.
  - Hap içine alınmış etiket.
- **K70. İddia:** sağlık sonucu ("horlamayı keser", "daha iyi uyku", "sessiz uyku"), hastalık adı, tanıklık, üstünlük ("ilk", "tek", "orijinal"), rakip marka adı. Kaynak: `saglik/somnifix/KART.md` §6 iddia tablosu.
- **K71. Kompozisyon:**
  - Referans dizilimini kopyalamak.
  - Aynı açıyı tekrarlamak.
  - Poşeti her karede tekrarlamak: galeride poşet en fazla 2 karede (G1 + kutu içeriği) yer alır; diğer karelerde kahraman bandın kendisidir.
  - Kolaj; çoklu görsel isteği.
  - Ürüne yazının binmesi; kenar teğeti; ölü bölge.
- **K72. İnsan:** insan, el, yüz, yatak sahnesi, uyuyan kişi (K1).

## 8. Niş farkları

Galeri her nişte 8 karedir. Feed G1 yazısızdır; mağaza G1'inde en fazla 1 gerçek güven satırı olur (K8). Grafik kare kotası niş OZET'lerindeki ölçüme göre belirlenir.

- **K73. Niş tablosu.**

| Niş | Tipografi (K25) | Zemin | Grafik kota | İnsan | Galeri sırası (G1→G8) | Kaynak |
|---|---|---|---|---|---|---|
| **Sağlık** | A | Krem + en fazla 1 lacivert durak kartı | 8/8 grafik | 0 | Poster → durak/ikon kartları → nasıl çalışır (işaret çizgisi) → dev sayı → kullanım adımları → kutu + ölçü → karşılaştırma → zaman çizelgesi (deneyim dili) | `saglik/OZET.md` §2a, §5/4; SomniFix 9/17 grafik |
| **Güzellik** | A (krem/sıcak) ya da B (cihaz/klinik) | Açık 4/5; koyu yalnız cihaz "teknoloji" bloğunda | ≥ 6/8 | Bilgi kartları insansız; önce/sonra **üretilmez** | Packshot/poster → fayda kartı (ürün taşar + 3–4 madde) → mekanizma/içerik makrosu → kanıt (yalnız raporla; yoksa doku makrosu) → 3 adım kullanım → boy/süre ya da kutu → karşılaştırma ya da "kimin için" → rutin/aile | `guzellik/OZET.md` §2.1, §4/2 |
| **Gadget** | B | Tek zemin ailesi, en fazla 2: ya hep açık ya hep koyu degrade. Bizde degrade yerine düz koyu (K17) | ≥ %70; 4 Batılı markada %84 | El yalnız ölçek için; yüz yok | Ürün → tek mekanizma (başlık 2–4 kelime) → işaret çizgileri ya da ikon ızgarası (biri zorunlu) → ekran/uygulama (yalnız gerçek entegrasyon) → sayı + altında kaynak notu (yalnız gerçek kaynak) ya da ölçü → ölçü/kapasite → sınıfa karşı karşılaştırma → kutu içeriği | `gadget/OZET.md` §1a–1b, §2 |
| **Moda** | B (dar büyük harf serbest) | Tek açık gri: `#F1F1F1`–`#F8F8F8` | Yalnız işlev iddiasında yazı (kapasite, kumaş, garanti); estetik üründe 0 | Bedene oturan giyim: model zorunlu (29/29). Ayakkabı, takı, aksesuar: 0/48 | Alt tipe göre A/B/C/D tarifleri (`moda/OZET.md` §2). Aksesuar kullanıcı zevkine tam uyar | `moda/OZET.md` §2–4 |
| **Ev** | B; serif yalnız tek vurgu | Beyaz ya da açık gri; en fazla 1 koyu kart | 4 markada 7/9, 12/16, 8/16 grafik | El ya da yüzsüz; bizde grafik kullanım | Packshot + **ölçek nesnesi** (yazısız) → vaat + 3–4 fayda (bölünmüş, sol panel %40) → mekanizma → sınıfa karşı kıyas → ölçü/boy/varyant → **temizlik/bakım kolaylığı** → kullanım → varyant/kutu | `ev/OZET.md` (a)–(b) |

- **K74. Ev slotu.** Ev galerisinde "temizlik/bakım kolaylığı" karesi zorunludur. Ev alıcısının itirazı "nasıl temizlenir, ne kadar dayanır" sorusudur; 5 markanın 4'ünde var. Teknik ev ürününde "Not:" beklenti dipnotu galeride yer alır ("Bu üründe kamera yok").
- **K75. Gadget sayısı.** Galeride rakam varsa altında kaynak notu olur (4/5 marka). Kaynak yoksa rakam yerine ölçü yazılır (K7).
- **K76. Moda alt tipi.** Önce alt tip belirlenir. Model gerektiren alt tipte (bedenli giyim) K1 istisnası kullanıcıya tek satırla sorulur.
- **K77. Sınıfa karşı karşılaştırma.** Bütün nişlerde karşılaştırma bir ürün sınıfına karşı yapılır ("düz flaster", "spor salonu tartısı"). Rakip marka adı yasaktır. Takviyede karşılaştırma hiç yapılmaz.

## 9. Kabul kontrol listesi (direktör)

**K78.** Her görsel bu listeden geçer. Tek ❌ = 7/10 altı = kullanıcıya gösterilmez. Ölçüm PIL ve göz ile yapılır.

| # | Kontrol | Ölçüm | Eşik |
|---|---|---|---|
| 1 | Ürün kimliği | Referansla yan yana | Ambalaj rengi, logo, "Ağız Bandı · 30 gece", pas çizgi, bant biçimi ve yarık birebir |
| 2 | Açı tekrarı | Galerideki diğer karelerle | Aynı dizilim ve açı yok; G1-ana dizilimi yok |
| 3 | Kenar boşluğu | Piksel | Kare 88 ±4 px; banner 117 / 97 px |
| 4 | Sol hat | Satır başlarının x'i | ±2 px (serif +3) |
| 5 | Başlık cap | Piksel | 76 ±4 px; ağırlık 400 (A) / ≤ 600 (B) |
| 6 | Oranlar | Cap'ler | T2/T1 0,40–0,45 · T5/T2 ≈ 0,75 · T3/T4 = 1,6 |
| 7 | En küçük metin | Cap | ≥ 26 px |
| 8 | Kırılım | Göz | Başlık ≤ 2 satır, yetim yok; kart başlığı tek satır |
| 9 | Metin–ürün | Piksel | ≥ 50 px, bindirme yok |
| 10 | Kenar teğeti | Piksel | ≥ 88 px ya da ≥ %15 taşma |
| 11 | Ölü bölge | 3×3 hücre | Boş hücre 0 (simetrik G1 hariç) |
| 12 | Lacivert | Metin çekirdeği | `#14304F` ±4 RGB |
| 13 | Kontrast | WCAG | Metin ≥ 4,5; ürün–zemin ≥ 1,5 |
| 14 | Pas | Öğe sayısı | Tam 1 (banner 0); ±6 RGB |
| 15 | Düz yüzey | Köşe–köşe | ΔRGB ≤ 3 (ışık düşüşü izinli alanda ≤ 14) |
| 16 | İkon seti | Göz + piksel | Yalnız çizgi; boy ±%5; yasak metafor yok |
| 17 | Kart geometrisi | Piksel | Boşluklar 24 px eşit; iç boşluk eşit; taban hizası |
| 18 | Bant gerçekçiliği | Makro kırpıntı | İplik ızgarası; yazı/labirent deseni yok; kâğıt inceliği |
| 19 | Işık | Gölge yönü | Tek kaynak sağ üst; gölge sola, ≤ %8 |
| 20 | Metin | OCR | Yalnız prompttaki Türkçe metin, birebir; fazladan yazı 0 |
| 21 | İddia | Metin | K7 ve K70'e uygun |
| 22 | Yasak süs | Göz | K66–K72'den 0 |
| 23 | Oran ve tekillik | Dosya | İstenen en-boy oranı, tek görsel, kolaj değil |
| 24 | Telefon testi | 360 px'e küçült | Bütün metin okunur |

---

## Ek A. ELESTIRI.md izlenebilirlik (hepsi işlendi)

**(b) 30 kural → dil kuralı**

| ELESTIRI | Dil | ELESTIRI | Dil | ELESTIRI | Dil |
|---|---|---|---|---|---|
| 1 kenar | K37–K39 | 11 kırılım | K30 | 21 taban hizası | K50 |
| 2 sol hat | K41 | 12 marka adı | K34 | 22 ikon çizimi | K52 |
| 3 dikey ritim | K29 | 13 eyebrow | K33 | 23 ikon boyu | K53, K51 |
| 4 metin–ürün | K42 | 14 tek lacivert | K12 | 24 ikon metaforu | K54 |
| 5 kenar teğeti | K43 | 15 ikincil ton | K11, K15 | 25 kompozisyon çeşitliliği | K4, K71 |
| 6 ölü bölge | K44 | 16 ürün–zemin | K13, K14 | 26 ürün ölçeği | K45 |
| 7 cap ölçüsü | K22, K26 | 17 pas | K16 | 27 bant gerçekçiliği | K64 |
| 8 başlık serifi | K23, K26 | 18 düz yüzey | K17 | 28 ışık | K65 |
| 9 boy oranları | K26 | 19 kart rengi | K19 | 29 banner metinsiz | K8, S-B1, S-B2 |
| 10 en küçük metin | K28 | 20 kart geometrisi | K49 | 30 logo | Ek B |

**(a) Kritik 10 kusur → önlem**

| # | Kusur | Önlem |
|---|---|---|
| 1 | Referans kopyası | K3, K4, K71 + promptta açı satırı |
| 2 | Ürün zemine karışıyor | K13, K14 |
| 3 | Bant gerçek değil | K64 |
| 4 | Tipografi spek dışı | K23–K26 |
| 5 | Izgara yok | K37–K41 |
| 6 | Çakışma ve sıkışma | K42, K43 |
| 7 | İkon seti tutarsız | K52–K54 |
| 8 | Ölü bölge | K44 |
| 9 | Tonal hiyerarşi yok | K12, K15 |
| 10 | Metin bannera gömülü | K8, K27 |

Prompt kökleri:
- "%9 belirsiz" → K22 ve ölçü sözleşmesi.
- "1,5 px ölçeksiz" → ölçü sözleşmesi (2 px).
- "ortalama yasağı" → K46.
- "çoklu istem" → K5.

**(d) 14 teknik → dil**

| # | Teknik | Dil karşılığı |
|---|---|---|
| 1 | Ürünü grafik nesne yapmak | S-G3, S-G4, K71 |
| 2 | İşaret çizgisi | K55, S-G3 |
| 3 | Dev sayı | K57, S-G4 |
| 4 | Eyebrow | K33 |
| 5 | Tonal metin | K15 |
| 6 | İtalik vurgu | K32 |
| 7 | Açık kart + tonlu zemin | K19, S-G5, S-G7 |
| 8 | Kaynak satırı | K62 (yalnız gerçek kaynakla) |
| 9 | Makro taşma | K47, S-G4, S-G8 |
| 10 | Tek şablon | K9 |
| 11 | Simetrik ana görsel | S-G1, K46 |
| 12 | Karşılaştırma + zaman çizelgesi | S-G7, S-G8 |
| 13 | Özellik kutucukları | S-G2. Hap yerine ikon kartı (K33: hap yasak) |
| 14 | Canlı metinli hero | K8, S-B1, S-B2 (tema `e-hero-b`) |

## Ek B. Logo kuralı (ASKIDA: kullanıcı onayı bekliyor, uygulanmaz)

Güncel durum: logo yalnız ikon (yazısız) olacak; ikon + yazı kilitleri ve kodla birleştirilmiş logo reddedildi. Aşağıdaki maddeler SESSA test5 kaydıdır, kural değildir.


- Logo, ambalajdaki logo çiziminin aynısıdır: ince, yüksek kontrastlı serif, Regular. Yeni bir logo türetilmez.
- Harf aralığı optik olarak eşittir. Çiftler arası fark ≤ %10 ve harfler asla birbirine değmez: her çiftte en az sap kalınlığının 1,5 katı boşluk olur.
- Sunum karesinde (1254) logo genişliği 564 px (%45); geometrik merkezin 25 px (%2) üstünde durur.
- Efekt, çerçeve, kart, slogan ve ® yok. Zemin `#F2EEE8`, logo `#14304F`.
- Küçük boy (favicon) ayrı turda üretilir.

## Ne kaldı
- v1, test5 üretimi ve direktör eleştirisiyle sınanacak. Ölçülen sapmalar v2'ye girecek.
- Ev tipografisi: koordinatör "ev = serif varsayılan" dedi, ama `ev/OZET.md` galeri başlıklarını 5/5 sans ölçtü. v1 ölçüme uydu (K25, ev = B). Karar koordinatörde.
- ~~`uretim-promptlari.md` genel şablonlara çevrilmedi.~~ Çevrildi (2026-11-16, sürüm 0.2.0): `skills/gorseller/references/uretim-promptlari.md`.
- Instrument Serif'in Türkçe glifleri (İ, ş, ğ) gerçek render ile denenmedi.


## K78 karar güncellemesi (2026-11-16, koordinatör — direktör önerisi C1)
Kabul kontrol listesi iki sınıfa ayrıldı:
- **KRİTİK (tek ❌ = ret):** ürün kimliği bozuk (ambalaj, logo, bant şekli/dokusu), Türkçe yazım hatası ya da istenmeyen metin, yasak süs (taş, bitki, leke, parlama, 3D ikon), sistem dışı renk (yasak aralık), uydurma iddia/yüzde, kolaj.
- **ÖLÇÜ (puan düşürür, ret değil):** px koordinat ve kenar boşluğu sapmaları ±%15'e kadar −0,5 puan; ±%15 üstü −1 puan. Görsel model px'i birebir tutmuyor (test5: sapma 16–87 px).
Gösterim eşiği: kritik ❌ yok VE puan ≥ 7.
Logo: görsel modelle üretilir (kullanıcı: "fontla değil, düz logo"); genişlik/yerleşim kodla düzeltilebilir (kırp + tuvalin %45'ine ortala).

## Karar güncellemesi 2 (2026-11-16, kullanıcı onayı — sürüm 0.2.0)
- **Onaylandı:** test5 galeri ürün görselleri ("baya iyi"): grafik, insansız, yazılı galeri G1–G8 bu dosyanın ölçüleriyle. Kaynak prompttaki "galeride yazı yok" kuralı (4.3, kabul kapısı madde 6) galeri G2–G8 için bu dil ile değişti; feed G1 yine yazısız (K8).
- **Onaylandı:** test7 mobil banner: tipografi görselin İÇİNDE, tasarımın parçası (etiket, serif başlık + tek italik kelime, alt metin, hap buton, güven satırı; sol hizalı, kenar %8). Bu, S-B2 "metinsiz" ve K8'in mobil banner kısmının yerine geçer. Yazıyı görselin altına ayrı bloğa almak ve küçük ürün + boş zemin reddedildi. Düzenler M1/M2/M3: `uretim-promptlari.md`.
- **Değişmedi:** masaüstü banner metinsiz üretilir, metni tema canlı HTML olarak yazar (S-B1, K8).
- **Reddedildi (yasak):** insanlı yaşam tarzı paneller; referansı 1-1 kopyalamak; AI süsleri (taş, bitki, leke, parlama); kodla çizilmiş görsel (PIL şablon); kodla birleştirilmiş logo.
- **Logo:** yalnız ikon (yazısız), onay bekliyor. Ek B ve K78 güncellemesindeki logo satırı askıda.
- **Uygulanan direktör önerileri (test5 v2 ELESTIRI):** bant/yassı ürün asla dik durmaz, poşetin önüne değil yanına düz yatar; her promptta DÜZELTME paragrafı (ince sık doku, yatık ürün, kenar %7, vurgu çizgisi ≤ %4, metin rengi tam değer); düz zeminli karede kenar sapması kodla küçültülerek düzeltilir (`scripts/duzelt.py kenar`), ürün kadrajdan taşıyorsa uygulanmaz.
