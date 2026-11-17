# Sahne şablonları — ChatGPT kare + Gemini Omni video (3–4 sahne × 4–6 sn)

> Kaynak notu: bu dosya ~100 milyon izlenen ürün videosunun saha incelemesinden (kayıt numaraları köşeli parantezde, ör. [058]) ve bir dış araştırmadan derlendi. Ham veri seti eklentiye dahil değildir; sayılar o ölçümün sonucudur.

Hat: her sahne → ChatGPT'de başlangıç karesi (`baslangic-karesi.md` §4) → aynı kare + video promptu Gemini Omni → 4–6 sn klip → kurgu.
Milyon videoların süresi medyan **12 sn**, 83/97'si 8–15 sn [R4]. Bu yüzden: 3–4 klip üret, kurguda her birini **2–4 sn**'ye kes, toplam **10–15 sn**.
Promptlar İngilizce (model için), açıklamalar Türkçe. Etiket: KURAL ≥3 · ADAY 2 · GÖZLEM 1. Kanıt numaraları saha veri seti.
Sayısal ölçüm (2026-11-07): içerik matematiği ölçümü — şablon seçerken §4 tablosu: yazısız (D7) ve dönüşen ürün (D15) izlenmede ~2×; kimlik kancası paylaşımda ~1,9×; kanıt deneyi (D14) paylaşımda düşük.

## 0. Ortak

**Sürüm ve maliyet (2026-11-07, dış araştırma notu §1a, madde 7):** kitin aracı artık **Gemini Omni Flash 1.2**. API: 720p $0,07/sn, 1080p $0,104/sn (https://aistudio.google.com/docs/pricing). 1.1 istekleri **3 Aralık 2026'dan itibaren 1.2'ye yönlendiriliyor**. 3–10 sn, uzatmayla 40 sn; sohbetle düzenleme ("keep everything else the same" + tek değişiklik; ~4 düzenlemeden sonra sıfırdan kur — https://morphic.com/resources/how-to/gemini-omni-flash-1-1-guide).
**Referans modu (madde 8):** 10'a kadar referans görsel verilebilir (ürün için en katı rol), ama referans ve ilk kare **aynı çağrıda kullanılamaz** → ürün çok kayıyorsa iki geçiş: önce referansla klip, sonra kareyi sabitle (https://runware.ai/docs/models/google-gemini-omni-flash-1-1/guides/reference-driven-video.md). Her referansa tek görev ver ("product only from image 1, room only from image 2").
**Yedek model (madde 6):** Omni'nin bağımsız ürün sadakati testi yok; bir bağımsız inceleme "fazla keskin, fizik tutarsız" diyor (https://curiousrefuge.com/blog/google-omni-review). Elle tutulan ürün sahnesinde 3 denemede kullanılabilir klip çıkmazsa aynı kareyle Kling 3.0 (1080p $0,112/sn) ya da Veo 3.1 Lite/Fast denenir. **Ücretli API = projenin bütçe kapısı + kullanıcı onayı**; kit bu çağrıyı yapmaz.
**Deneme bütçesi (madde 14):** kullanılabilir klip oranı ölçümlerde %30–100 (küçük ürün testi, https://kingy.ai/?p=929624); klip başına **en fazla 3 üretim** (araştırmanın planlama varsayımı, ölçülmüş değil); her yeniden üretimde tek değişken değiştir (https://morphic.com/resources/how-to/ai-video-troubleshooting). Oranı `olcum-ve-test-plani.md` §5 tablosuna yaz.
**Kota (madde 15):** Gemini uygulamasında 10 sn'lik video 5 saatlik kotanın ~%22'si → pencere başına ~3–5 klip (https://www.analyticsvidhya.com/blog/2026/06/gemini-omni-ai-video-generation/). Tek set × 10 kanca (~12 üretim) 1–2 gün; 10 farklı set haftalar.

**Gemini Omni (web, önceki tur doğrulaması — yeniden ölçülmedi):** Google I/O 2026'da duyuruldu; Gemini uygulaması, Google Flow ve YouTube Shorts'ta; görsel + metin + ses girdisi; çıktıda görünmez SynthID
(https://engadget.com/2176590/googles-gemini-omni-can-generate-anything-from-any-input-starting-with-video). Çağrı başına 3–10 sn, varsayılan 6; oran 16:9 / 9:16
(https://runware.ai/docs/models/google-gemini-omni-flash-1-1/guides/resolution-and-duration — üçüncü taraf; uygulamada farklıysa uygulamayı esas al).
Prompt yapısı (Veo rehberi, Omni'ye aynen geçtiği doğrulanmadı): özne + eylem + mekân + kamera + ışık; ses ayrı cümle; istenmeyen şey liste olarak
(https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide). Klip başına tek kamera hareketi (https://www.atlabs.ai/blog/the-ultimate-prompting-guide-for-veo-3-1 — üçüncü taraf).

**Video prompt kalıbı:**
```
Vertical 9:16, [4–6] seconds. Use the provided image as the first frame.
CAMERA: [handheld phone POV, static | slow push-in | slow follow | locked-off top-down | fixed security-camera angle] — one camera move only.
ACTION: [özne] [tek eylem, klip içinde başlayıp biten]. Promptta saniye yazılırsa kurgu saniyesinden geri hesaplanır: ileri `t_klip = (t_video − plan_bas) × hız`, ters `t_klip = süre − (t_video − plan_bas) × hız`; ters oynatılacak klipte eylem klibin SONUNA yakın yazılır (üretilen klibin durgun kuyruğu videonun başı olur, ≤ 0,8 sn).
PRODUCT: stays identical to the image — same shape, color, parts, logo; it does not morph or duplicate. Keep identical: [görünen parçaları tek tek say]. [Dönüşüm şablonunda: yalnız tarif edilen dönüşüm olur.] Any glow/effect matches the real product's brightness, size and speed.
LIGHT: unchanged from the image: [ışık].
AUDIO: [2–3 ortam sesi]. No dialogue. No music.
AVOID: on-screen text, subtitles, watermark, store signage, brand logos, warped logo, distorted label, garbled text, extra fingers, extra limbs or paws, impossible grip, shallow depth of field, sudden scene change.
```
Konuşma yok: milyonlarda konuşan tek video GERÇEK-MARKA kurucu anlatımı [033, GÖZLEM]. Müzik kurguda eklenir.

**Şablon seçimi (sırayla sor):**
1. Ürün 2 sn'de tek görüntüyle anlaşılıyor ve komik/tatmin edici mi? → **S1** (gerçek görünüm, süsleme yok) [123, 085].
2. Tanıdık bir problemi çözüyor mu? → **S2**; ürün tuhaf/fantezi ise → **S3**.
3. Hayvan/bebek giyiyor ya da içinde duruyor mu? → **S4** (dönüşüm/çekilemeyen eylem) ya da **S6** (çok mekân).
4. İnsanlar görünce güler/korkar/şaşırır mı? → **S5**.
5. Ürün açılıyor/yanıyor/tamamlanıyor mu? → **S7**. Faydası görünmez mi? → **S8**. Bir yerde uzun süre sıkıntıyı bitiriyor mu? → **S9**.
6. Fayda/etki gösterilecek ve elde gerçek numune var mı? → **S10** (AI kanca + gerçek kanıt). S4/S9 seçildiyse S10 versiyonunu da A/B olarak üret.

---

## S1 — Tek sahne gag / mekanizma — KURAL (17)
Kanıt: 014, 038, 060, 063, 066, 072, 085, 089, 090, 097, 105, 114, 117, 123, 134 (AI market kuyruğu, kimse fark etmiyor, 20,9MN), 135 (örtü reveal, gerçek), 138 (AI uçak, iki kişi uyuyor). Örnek sayılar: 085 30,2MN · 063 15MN · 114 6,1MN (profilde 20,1MN) · 123 4,8MN · 117 4MN.
Hesap-içi: aynı ürünün AI kamusal sahneli versiyonları 16,5B–52,4B [123]; yazılı versiyon 983–2.275 [102].
Yapı: **1 sahne, kesmesiz, 6–10 sn döngü.** Gerekirse aynı kadrajdan ikinci klip (devam) — kurguda birleştir. Yazı yok ya da tek satır.
Kanca: K13 yazısız / K8 POV keşif / K9 sonuç cümlesi.

**Örnek — kauçuk dişli halı tüy tarağı (kanıt 066 kalıbı, gerçek görünüm)**
Görsel:
```
Vertical 9:16 phone-video still frame, photorealistic, looks like a real Instagram Reel shot on an iPhone.
SCENE: a hand pushes a rubber-bristle carpet rake across a grey living-room rug; a thick clump of beige dog fur is already rolling up in front of the blade.
PRODUCT: rubber-bristle carpet rake with a short teal handle — match the attached product photo exactly.
WHO: only one adult hand and forearm, seen from a standing POV looking down.
WHERE: a real, slightly worn grey rug, a dog toy and the edge of a sofa leg visible.
LIGHT: soft window daylight from the left.
FRAMING: rake and fur pile in the middle 70%, top third is plain rug; nothing important in the bottom 20% or right 15%.
TEXTURE: natural phone noise, slight motion blur.
AVOID: any text, watermark, brand logos other than ours, extra fingers, studio backdrop, CGI render look.
```
Video:
```
Vertical 9:16, 6 seconds. Use the provided image as the first frame.
CAMERA: handheld phone POV looking down, static — one camera move only.
ACTION: the hand drags the rake toward the camera in three short strokes; the fur clump grows into a large fluffy pile.
PRODUCT: stays identical to the image — same shape, color, logo; it does not morph or duplicate.
LIGHT: unchanged from the image: soft window daylight.
AUDIO: rubber scraping on carpet, a dog's paws padding nearby. No dialogue. No music.
AVOID: on-screen text, subtitles, watermark, extra fingers, sudden scene change.
```
Yazı: yok ya da `POV: you found the perfect gift for a DOG MOM 😳` [066]. Caption: `Comment "FUR" and I'll send you the link`.

---

## S2 — Problem → Vs… → Çözüm (+ gece kamerası varyantı) — KURAL (16; gece kamerası 3 + 2 Ek)
Kanıt D12: 036, 040, 044, 047, 074, 075, 076, 077, 080, 084, 100, 112, 116, 120, 126, 137 (AI tren/uçak: problem ve yan koltukta zorlanan başka ebeveyn aynı karede). Gece kamerası: 074 1,1MN · 084 1MN · 120 5MN · Ek 047 hesabı 5,5MN · Ek 084 kedi 2,8MN.
Problem şartı (eski "komik-tehlike şart" kuralı daraltıldı): **tanıdık + tek bakışta anlaşılır** yeterli — üşüyen köpek [084], yatağı kapan kedi [120], kıllı lavabo [077], sıkıcı duş başlığı [112], dar ofis koltuğu [126], tehlikeli-komik kedi [047].

| Sahne | Klip | Kurguda | Görüntü | Yazı |
|---|---|---|---|---|
| 1 Problem | 5 sn | 2–3 sn | ürünsüz; gri/IR | `The problem 😭` |
| 2 Vs… | 4 sn | 2 sn | ürün açılıyor/seriliyor, el POV | `Vs…` |
| 3 Çözüm | 6 sn | 3–4 sn | ürün kullanımda, en sıcak/renkli kare | `The solution 🤩` |
| 4 (ops.) | 5 sn | 2–3 sn | çözümün 2. hali (iki hayvan / farklı açı) | CTA kartı |

**Örnek — tünel tipi peluş köpek yatağı (084/120 kalıbı)**
Sahne 1 görsel:
```
Vertical 9:16 still frame from a home security night-vision camera, grey infrared image, photorealistic, a small "REC" dot in the upper left corner only.
SCENE: a small short-haired dog curled up shivering on a bare bedroom floor next to an empty thin dog cushion at night.
WHO: tan short-haired small dog, seen from a high corner security-camera angle.
WHERE: a real bedroom, bed edge and a crumpled blanket visible.
LIGHT: grey night-vision infrared, slight noise.
FRAMING: dog in the middle 70%; top third calm; nothing important in the bottom 20% or right 15%.
AVOID: any other text, watermark, extra legs, distorted paws, color image.
```
Sahne 1 video:
```
Vertical 9:16, 5 seconds. Use the provided image as the first frame.
CAMERA: fixed security-camera angle, no movement.
ACTION: the dog shivers, lifts its head toward the camera, then tucks its nose under its paws again.
PRODUCT: none in this shot.
LIGHT: unchanged from the image: grey night-vision infrared.
AUDIO: faint room hum, a soft whimper. No dialogue. No music.
AVOID: on-screen text, subtitles, watermark, extra legs, color change, sudden scene change.
```
Sahne 2 görsel: `CONTINUITY LOCK: same dog, same bedroom. Vertical 9:16 phone-video still, warm lamp light. SCENE: POV hands unfold a plush beige tunnel-shaped dog bed with a sherpa lining onto the floor — match the attached product photo exactly; the dog watches from the side. AVOID: any text, watermark, extra fingers.`
Sahne 2 video: `Vertical 9:16, 4 seconds. Use the provided image as the first frame. CAMERA: handheld POV, static. ACTION: the hands lift the top flap open; the dog steps forward and sniffs the opening. PRODUCT: stays identical to the image. LIGHT: unchanged warm lamp. AUDIO: fabric rustle, dog sniffing. No dialogue. No music. AVOID: on-screen text, morphing product, extra fingers.`
Sahne 3 görsel: `CONTINUITY LOCK: same dog, same bed, same room. SCENE: the dog sleeps inside the tunnel bed, only its face peeking out from the soft opening, eyes half closed. LIGHT: warm bedside lamp, cozy. FRAMING: dog face and bed opening in the middle.`
Sahne 3 video: `Vertical 9:16, 6 seconds. Use the provided image as the first frame. CAMERA: slow push-in toward the dog's face. ACTION: the dog sighs, its eyes slowly close, the bed fabric rises gently with its breathing. PRODUCT: stays identical. LIGHT: unchanged warm lamp. AUDIO: soft breathing, quiet room tone. No dialogue. No music. AVOID: on-screen text, extra paws, morphing product.`
Yazı: `The problem… 😱` → `Vs…` → `The Solution 😍🐶` · CTA `Comment "DOG" if you need one` / `Send this to a dog mom` [084].

---

## S3 — Concept (karton prototip) → VS… → Result — KURAL (4 + 1 profil)
Kanıt: 036 8,1MN · 075 3,1MN · 080 4MN · 131 1,4MN (tamamen AI, yeni hesabın 3. videosu) · 112 profilde 'The concept…' 26,3MN. Hesap-içi: 080'de diğer kancalar 385–1.445; 075'te düz hediye 802–5,6B.
Yapı: 1 komik kötü prototip (bant, karton) → 2 gerçek ürün elde → 3 ürün çalışıyor, wow.

**Örnek — ışıklı ejderha başı duş başlığı (036 kalıbı, jenerik ejderha)**
Sahne 1 görsel:
```
Vertical 9:16 phone-video still frame, photorealistic, looks like a real Instagram Reel.
SCENE: a cheap cardboard dragon head with marker-drawn eyes is taped onto a chrome shower head with beige masking tape; a weak trickle of water drips from it.
WHO: nobody, close-up of the shower wall.
WHERE: a real grey-tiled bathroom, a shampoo bottle on the ledge (no label).
LIGHT: flat bathroom ceiling light.
FRAMING: taped prototype in the middle 70%; top third calm.
AVOID: any text or letters, watermark, brand logos, CGI render look.
```
Sahne 1 video: `Vertical 9:16, 4 seconds. Use the provided image as the first frame. CAMERA: handheld, static. ACTION: the wet cardboard sags and one piece of tape peels off. PRODUCT: none. LIGHT: unchanged. AUDIO: weak dripping water, tape crinkling. No dialogue. No music. AVOID: on-screen text, sudden scene change.`
Sahne 2 görsel: `CONTINUITY LOCK: same bathroom. SCENE: two hands hold the real dark-bronze dragon-head shower head close to the camera, open jaws, amber eyes — match the attached product photo exactly.`
Sahne 2 video: `Vertical 9:16, 4 seconds. CAMERA: slow push-in toward the dragon's mouth. ACTION: the hands rotate the head slightly to show the teeth. PRODUCT: stays identical. AUDIO: soft metallic tap. No dialogue. No music. AVOID: on-screen text, extra fingers, morphing product.`
Sahne 3 görsel: `CONTINUITY LOCK: same bathroom, lights off. SCENE: the mounted dragon head's eyes glow orange and a wide stream of water pours from its mouth; warm orange haze; the glow is the brightest point in the frame.`
Sahne 3 video: `Vertical 9:16, 6 seconds. CAMERA: static. ACTION: water flows from the dragon's mouth, the eyes pulse brighter twice. PRODUCT: stays identical; only its LEDs change brightness. LIGHT: dark room lit only by the product's glow. AUDIO: strong shower water, echo in a tiled room. No dialogue. No music. AVOID: on-screen text, fire, smoke.`
Yazı: `The Concept 🤢` → `VS…` → `The Result 🤯🐉` · CTA `Comment "DRAGON"`.

---

## S4 — AI: gerçekte çekilemeyen hayvan/bebek anı (AI-1) — KURAL (9)
Kanıt: 058 17,5MN · 065 22,3MN · 080 4MN · 082 3,1MN · 083 1MN · 087 7,7MN · 089 2MN · 103 1,5MN · 131 1,4MN.
Alt tip **peluş ↔ bebek reveal** (İ4): 065, 096 (11,7MN, karışık), 103 → KURAL (3).
Uyarı: aynı AI dünyası morph/eylem anı olmadan düşük [065 diğerleri 21B–223B]. Bebek ürünlerinde uyku güvenliği/sağlık iddiası yok (yasak #4).
**AI etiketi (ARAŞTIRMA madde 3):** duygusal gönderide "AI ile üretildi" etiketi etkileşimi ~46 puan düşürüyor (hakemli, ~700 katılımcı). Bu şablon tam bu kategoride → aynı kancayla bir de S10 (gerçek çekim + AI an) versiyonu üret; kazananı `olcum-ve-test-plani.md` ile seç.

**Örnek — dinozor bebek tulumu, "peluş sanılan bebek" (103 kalıbı)**
Sahne 1 görsel:
```
Vertical 9:16 phone-video still frame, photorealistic.
SCENE: on a white bed, what looks like a green plush triceratops toy lies face down — it is actually a baby wearing a triceratops onesie, seen from behind: spiky hood frill, soft tail, little padded feet.
PRODUCT: green bobble-texture triceratops baby onesie with horned hood and tail — match the attached product photo exactly.
WHERE: a real bedroom, rumpled white duvet, a pillow edge.
LIGHT: soft morning window light.
FRAMING: the onesie in the middle 70%; top third is plain duvet.
AVOID: any text, watermark, baby face visible in this frame, extra limbs, licensed characters, CGI look.
```
Sahne 1 video:
```
Vertical 9:16, 5 seconds. Use the provided image as the first frame.
CAMERA: handheld phone, static.
ACTION: the "plush toy" wiggles its tail, then rolls over and reveals a smiling baby face inside the hood who giggles at the camera.
PRODUCT: stays identical to the image — same colors, horns, tail; it does not morph.
LIGHT: unchanged soft morning light.
AUDIO: baby giggling, duvet rustle. No dialogue. No music.
AVOID: on-screen text, extra limbs, distorted face, sudden scene change.
```
Sahne 2: `CONTINUITY LOCK … SCENE: a parent's hand gently strokes the baby's cheek inside the hood, close-up.` · Video: `CAMERA: slow push-in. ACTION: the baby grabs the parent's finger and laughs. AUDIO: giggle, soft fabric.`
Sahne 3 (döngü): `CONTINUITY LOCK … SCENE: the baby crawls away from camera across the bed, looking again like a plush dinosaur from behind.` · Video: `CAMERA: static. ACTION: the baby crawls two steps and stops, tail swaying. AUDIO: soft giggle.`
Yazı: `Do NOT let DINOSAUR parents see this 🦕🥹` [103] ya da yazısız [065]. CTA `comment "REX" and I'll send you the link 🦕`.

---

## S5 — AI: yabancı tepkisi / kamusal gag (AI-2) — KURAL (6)
Kanıt: 064 2,2MN (kalabalık telefonla çekiyor) · 075 3,1MN (insanlar gülüyor) · 081 3,7MN (korku-prank) · 087 7,7MN (gülen insanlar) · 091 14,7MN (havaalanı göbek çantası) · 115 2MN (güvenlik + K9).
Şart: ürün **her karede**, tepki 1–2 sn; mekân **marka/tabela içermez**. Kalabalık/ekip baskın olursa düşüyor (N1: 083 436–1.705, 086 3.967–5.275).
Gerçek prank da çalışıyor [098, 2,4MN gerçek gizli kamera] — çekebiliyorsan gerçek tercih.

**Örnek — köpek için kırkayak kostümü (081 kalıbı, Cadılar Bayramı)**
Sahne 1 görsel:
```
Vertical 9:16 still frame from a doorbell camera, photorealistic, slight fisheye, a small timestamp area left empty (no readable text).
SCENE: a long dachshund wearing a segmented orange-and-brown centipede costume with many soft legs crawls through a half-open front door.
PRODUCT: plush centipede dog costume — match the attached product photo exactly.
WHERE: a real suburban porch, doormat, autumn leaves.
LIGHT: overcast daylight.
AVOID: any readable text, watermark, brand logos, extra dog heads, CGI look.
```
Sahne 1 video: `Vertical 9:16, 5 seconds. Use the provided image as the first frame. CAMERA: fixed doorbell-camera angle. ACTION: the costumed dog waddles inside, the costume's soft legs bouncing with each step. PRODUCT: stays identical. AUDIO: door creak, paws on wood, leaves. No dialogue. No music. AVOID: on-screen text, extra legs on the dog itself, sudden scene change.`
Sahne 2 görsel: `CONTINUITY LOCK: same dog, same costume. SCENE: in a backyard, an older man watering plants with a garden hose freezes and leans back as the costumed dog crawls out from behind a bush.`
Sahne 2 video: `Vertical 9:16, 5 seconds. CAMERA: handheld, static, medium shot. ACTION: the man jumps back one step, drops the hose, then bursts out laughing when he sees it is a dog. AUDIO: hose water, a startled gasp, laughter. No dialogue words. No music. AVOID: on-screen text, extra limbs.`
Sahne 3 görsel: `CONTINUITY LOCK … SCENE: close-up of the dog's face inside the costume hood with two soft antennae, sitting proudly on the lawn.` · Video: `CAMERA: slow push-in. ACTION: the dog tilts its head, antennae wobble. AUDIO: birds, soft panting.`
Yazı: `DON'T show this to a DOG MOM... 🫣🐶` · CTA `Send this to a dog mom` [081].

---

## S6 — AI: giyilen/taşınan ürün, 3–4 mekân montajı (AI-4) — KURAL (6)
Kanıt: 056 2,3MN · 071 1,2MN · 079 1,1MN · 086 32,8MN · 124 1,4MN · 132 2,6MN (havuz başı, havuz, nehir). Mesaj: "her yerde kullanılır".
**Mağaza karesi yok** (milyonlarda gerçek marka adıyla vardı [079, 086]; bize yasak, jenerik hali ölçülmedi). Mekânlar: park, ev, kafe, tren/uçak koltuğu, iş yeri.
Sahte "müşteri yorumu" söyleten kişi yok (yasak #5).

**Örnek — önünde köpek cebi olan hoodie (071/086 kalıbı)**
Sahne 1 görsel:
```
Vertical 9:16 phone-video still frame, photorealistic, selfie angle.
SCENE: a woman in her late 20s in an autumn park wears a cream hoodie with a round front pocket; a small white dog's head peeks out of the pocket.
PRODUCT: cream fleece hoodie with a round padded front pet pocket — match the attached product photo exactly.
WHO: woman, shoulder-length brown hair, small gold earrings; white small dog.
WHERE: real city park path, fallen leaves, a bench far behind.
LIGHT: low golden afternoon sun.
AVOID: any text, watermark, store signage, brand logos, extra fingers, extra dog heads.
```
Sahne 1 video: `Vertical 9:16, 5 seconds. Use the provided image as the first frame. CAMERA: selfie handheld, static. ACTION: the dog pops its head fully out of the pocket and licks her chin; she laughs. PRODUCT: stays identical. AUDIO: leaves crunching, light wind, laughter. No dialogue. No music. AVOID: on-screen text, extra paws, morphing hoodie.`
Sahne 2: `CONTINUITY LOCK … SCENE: same woman at home on a sofa under Christmas string lights, zipping the dog into the pocket.` · Video: `CAMERA: static. ACTION: she zips the pocket halfway, the dog settles in. AUDIO: zipper, soft dog sigh.`
Sahne 3: `CONTINUITY LOCK … SCENE: same woman seated in a café by the window, the dog's head out of the pocket looking at her cup (plain white cup, no logo).` · Video: `CAMERA: slow push-in. ACTION: the dog sniffs the steam, she smiles. AUDIO: café murmur, cup on saucer.`
Sahne 4: `… on a train seat, the dog asleep in the pocket.` · Video: `ACTION: the dog's ear twitches as the train sways. AUDIO: train rhythm.`
Yazı: `Every little DOG OWNER NEEDS this! 🫣🎅` [071] ya da `"Dog moms are hard to gift" / Me: 🤩` [086]. CTA `Send this to a dog mom!`.

---

## S7 — Ürünün kendisi dönüşüyor (reveal / ışık / tamamlanma) — KURAL (26)
Kanıt D15: 030, 038, 053, 057, 058, 065, 069, 075, 080, 081, 083, 085, 087, 089, 090, 093, 096, 101, 103, 113, 115, 123, 127, 128, 134, 135.
Alt tipler: sıradan görünüm → sürpriz işlev ("It's just a …" 127 3,5MN; Ek 067 aynı ürün 2,3MN) · katlı → açık (113 5,2MN, 128 1,1MN) · parça parça tamamlanma (093 13,3MN) · ışık kapanınca parlama (057 33,3MN).
Gerçek görünüm yeterli (bunların çoğu gerçek çekim); AI yalnız ürün hareketi için.

**Örnek — buzdolabı magneti mini plak çalar (127 kalıbı)**
Sahne 1 görsel:
```
Vertical 9:16 phone-video still frame, photorealistic, POV.
SCENE: a hand opens a home fridge door; on the outside of the door hang several small round vinyl-record magnets and a small square frame-shaped player.
PRODUCT: mini vinyl record fridge magnets (plain colored labels, no artist names) and a small wooden frame player — match the attached product photo exactly.
WHERE: a real kitchen, Christmas garland on the cabinet, a few drink cans inside the fridge (no logos).
LIGHT: warm kitchen light plus cold fridge light.
AVOID: any readable text, album art, artist names, brand logos, extra fingers.
```
Sahne 1 video: `Vertical 9:16, 4 seconds. Use the provided image as the first frame. CAMERA: handheld POV, static. ACTION: the fridge door closes, revealing the magnet collection at eye level. AUDIO: fridge door thud, quiet kitchen hum. No dialogue. No music. AVOID: on-screen text, morphing magnets.`
Sahne 2: `CONTINUITY LOCK … SCENE: close-up, fingers pick one mini record off the door.` · Video: `CAMERA: slow push-in. ACTION: the fingers slide the mini record into the frame player. AUDIO: magnetic click.`
Sahne 3: `CONTINUITY LOCK … SCENE: the frame player glows warm amber, the mini record spins.` · Video: `CAMERA: static. ACTION: the light turns on and the record starts spinning. AUDIO: soft click, then a gentle crackle (music added in edit). No dialogue.`
Yazı: `"It's just a fridge magnet..." 😤` [127] · CTA `30% OFF — link in bio` (yalnız gerçek indirimse).

---

## S8 — Kanıt deneyi / işkence testi — KURAL (13)
Kanıt D14: 014, 052, 061, 066, 077, 092, 102, 104, 106, 108, 111, 114, 118. Örnek: 106 işkence + su testi 4,6MN (kancalar 12,3B–139B) · 114 ateş körükleme 6,1MN / 20,1MN · 014 duman bombası 6,3MN (en iyi 31,1M).
Gerçek çekim tercih (AI'da sonuç "uydurma" görünür). Garanti cümlesi yazma ("%100 su geçirmez" → yasak #8 ruhu); görüntü kanıtlasın.
**Ölçüm:** D14 kayıtlarında paylaşım/izlenme %0,32 (n=13) vs diğerleri %1,15; paylaşım/beğeni 0,23 vs 0,66 (içerik matematiği ölçümü §4b). Kanıt deneyi izletir ama paylaşılmaz → S8'e mutlaka kimlik kancası (K1/K2/K10) ya da `Send this to` ekle; AI ile kanıt verilecekse S10'a geç.

**Örnek — su itici rüzgârlık (106 kalıbı, marka çizgisi yok)**
Sahne 1 görsel: `Vertical 9:16 phone-video still, photorealistic. SCENE: a vacuum-sealed flat package with a folded black windbreaker inside lies on a garage concrete floor; a hand holds a hammer above it. WHERE: real garage, tool wall blurred. LIGHT: single overhead garage bulb. AVOID: any text, brand logos or stripes from real brands, extra fingers.`
Sahne 1 video: `Vertical 9:16, 4 seconds. CAMERA: handheld POV, static. ACTION: the hammer hits the package twice; the package flexes but stays sealed. AUDIO: two dull thuds, garage echo. No dialogue. No music.`
Sahne 2: `CONTINUITY LOCK … SCENE: hands cut the package open and pull out the jacket.` · Video: `ACTION: the jacket unfolds with a snap. AUDIO: plastic tearing, fabric whoosh.`
Sahne 3: `CONTINUITY LOCK … SCENE: a man wearing the jacket in the garage, a hand pours a bottle of water over his shoulder.` · Video: `CAMERA: static. ACTION: water beads up and rolls off the fabric onto the floor. AUDIO: water splashing on concrete.`
Yazı: `DO NOT let a CAR GUY see this...` (K1) · CTA `Comment "JACKET"`.

---

## S9 — POV sorun anı → idealize sonuç (AI-5) — KURAL (6 AI-5; K7 kancası 5)
Kanıt: 099 3,2MN (uçakta 15 saat) · 094 1,1MN (çözülmüş aile anı) · 119 5,1MN (titreyen köpek → huzur) · 078 1,4MN (oda dönüşümü) · 133 araç yolcu koltuğunda yastıkla uyuyan kadın (profil 6,4MN) · 138 4,1MN (uçakta iki kişi uyuyor) · 139 1,2MN (masa altı ısıtıcı POV, gerçek-görünümlü AI) · K7: 053, 092, 099.
Hesap-içi: 094 gerçek yorgun-anne videoları 2–3,6B, AI huzur sahnesi 1,1MN. Sağlık durumu söyleyen POV yok (059/109 kit dışı).
**AI etiketi:** duygusal içerikte etiket etkileşimi düşürüyor (ARAŞTIRMA madde 3), ama 094 hesap-içi kanıtı ters yönde (AI huzur karesi 1,1MN, gerçek videolar 2–3,6B → ~300–550×) → karar verilmedi; tam AI ve S10 versiyonu A/B.

**Örnek — öne yaslanma seyahat yastığı (099 kalıbı)**
Sahne 1 görsel: `Vertical 9:16 phone-video still, photorealistic. SCENE: a tired man in an economy airplane seat at night, neck bent awkwardly, eyes open, cabin lights dimmed. WHERE: real economy cabin, seatback in front, blanket. LIGHT: dim blue cabin light. AVOID: any text, airline logos, extra fingers.`
Sahne 1 video: `Vertical 9:16, 4 seconds. CAMERA: static, from the aisle seat. ACTION: his head drops forward and jerks back up. AUDIO: engine hum, faint seatbelt chime. No dialogue. No music.`
Sahne 2: `CONTINUITY LOCK … SCENE: he inflates a grey ring-shaped forward-leaning travel pillow on the tray table — match the attached product photo exactly.` · Video: `ACTION: the pillow fills in three breaths. AUDIO: air puffs, engine hum.`
Sahne 3: `CONTINUITY LOCK … SCENE: dark cabin, he sleeps deeply hugging the pillow on the tray table while the passengers around him are awake.` · Video: `CAMERA: slow push-in. ACTION: he shifts slightly and keeps sleeping. AUDIO: engine hum, soft breathing.`
Yazı: `POV: 15 hours on the plane and I never moved once 😮‍💨✈️` [099] · CTA `Comment "SLEEP" if you need it now!`.

---

## S10 — Hibrit: AI kanca + gerçek kanıt — ADAY (saha karma n=13; dış vaka 1)
Ne zaman: ürünün faydası/etkisi gösterilecek (temizlik, ışık, su itme, sığma) **ve** elde gerçek ürün numunesi var. Duygusal şablonların (S4, S9) A/B eşi.
Kanıt: saha "karma" format (gerçek + AI/VFX) 13 kayıt — paylaşım/izlenme **%1,60** [%0,74–%2,60] (n=10), gerçek %1,02 (n=57), tam AI %1,15 (n=26); izlenme medyanı 1,8MN (n=10, ZAYIF) (içerik matematiği ölçümü §4c; kayıtlar 040, 042, 045, 047, 056, 058, 078, 084, 096, 107, 112, 119, 128).
Dış: 41,8MN mutfak temizleyici — AI kanca (abartılı kirli mutfak) → gerçek püskürt-sil çekimine geçiş [SATICI/ajans] (https://jingsourcing.com/fb-ai-product-marketing/); uygulayıcı yöntemi ~%50 gerçek çekim [ANEKDOT]; "AI ile geliştirildi" etiketi "AI ile üretildi"den daha az cezalandırılıyor (https://www.cbs.dk/en/articles/ai-labels-reduce-social-media-engagement). Kaynak: dış araştırma notu madde 13.
Yapı: **sahne 1–2 AI (≤5 sn toplam)** = çekilemeyen ya da abartılı problem/tepki anı (S2 gece kamerası, S5 tepki, S4 hayvan anı) → **sahne 3–4 gerçek telefon çekimi** = ürünün gerçekten çalıştığı an, gerçek hız ve parlaklıkta. Kurguda geçiş `Vs…` kartı ya da kesme.
Kural: kanıt sahnesi (ürün işini yaparken) asla AI değil. AI sahnesinde ürün ya hiç yok ya da hareketsiz.

**Örnek — köpek patisi temizleme kabı (kurgusal; S2 + S8 karışımı)**
Sahne 1 görsel (AI):
```
Vertical 9:16 phone-video still frame, photorealistic, looks like a grey night-vision home security camera (REC indicator is added later in edit).
SCENE: a muddy medium-sized dog walks across a light beige living-room rug, leaving dark paw prints. No product in the frame.
WHERE: a real living room, sofa edge and a shoe rack by the door.
LIGHT: grey IR night-vision.
FRAMING: dog and paw prints in the middle 70%; top third calm.
AVOID: any text or letters, watermark, brand logos, extra legs or paws, more than one dog, studio lighting, shallow depth of field, bokeh, CGI render look.
```
Sahne 1 video: `Vertical 9:16, 4 seconds. Use the provided image as the first frame. CAMERA: fixed security-camera angle — no movement. ACTION: the dog trots from the door to the sofa, each step leaves a new paw print. AUDIO: faint camera hum, paws on rug. No dialogue. No music. AVOID: extra paws, morphing dog, on-screen text.`
Sahne 2 (GERÇEK, telefonla çekilir): kapı önünde gerçek kap; köpeğin patisi kaba girer, el kabı 3 kez çevirir, pati çıkınca temiz. Çekim: telefon dikey, POV, tek kaynak ışık, kesmesiz 6–8 sn.
Sahne 3 (GERÇEK): temiz pati halıya basar, iz yok. 2–3 sn.
Yazı: `The problem 😭` → `Vs…` → `The solution 🤩` (K11) ya da `DO NOT show this to a DOG MOM with a white rug…` (K1) · CTA `Send this to a dog mom!` (paylaşım, deneme) ya da `Comment "PAW"`.
Caption: AI ibaresi ("Problem sahnesi AI ile oluşturuldu"); etiket açık.

---

## Bu kitte şablonu OLMAYANLAR (bilerek)
- **Mağaza perde açılışı / raf reveal / "RUN to [mağaza]"** [056, 079, 107]: milyonlar gerçek marka adıyla; N1 karşı-kanıtı güçlü (10 hesap). Jenerik "büyük mağaza rafı" yalnız bir kez milyonda görüldü [132: 2 sn raf + 3 kullanım sahnesi 2,6MN; aynı hesabın mağaza adlı kalabalık reveal'leri 4.645–19,1B] → GÖZLEM: ≤2 sn, sonra gövde tamamen ürün kullanımı, "deneme" etiketiyle.
  Görsel: `Vertical 9:16 photorealistic still. SCENE: a generic big-box store aisle, one shelf section stacked with our branded boxes — match the attached product photo. AVOID: any real store name, logo, uniform or signage; readable text other than our box logo.`
- **Kurucu anlatımı** [033, GÖZLEM, GERÇEK-MARKA] · **uzman/doktor AI** [059 düşük, yasak].
- **Kurulum demosu** [111, 118, ADAY]: istenirse S1 yapısıyla, adım başına 1 klip.
