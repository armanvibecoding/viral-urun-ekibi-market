# Üretim deneyimi — içerik planı yazılan 4 ürün

"Şu ürüne 30 video yaz", "hangi kanca/şablonu seçeyim", "AI klip neden bozuldu" sorularında buraya bak.
Ürünler: (1) köpekbalığı ağızlı kedi yuvası, (2) arcade joystick ışık anahtarı kapağı, (3) evcil hayvan mama piyanosu, (4) araç amblemi yerine takılan dijital ekran.
Kod kısaltmaları (K = kanca ailesi, S = sahne şablonu, İ = ilk kare tipi, M = viral mekanizma, D = desen) `ai-video-kreatif` becerisinin referans dosyalarındaki anlamdadır. Sayılar kaynak planlardan aynen alındı; kendi ürünümüzün satış/izlenme sonucu **ölçülmedi** (yayına çıkmadı).

## 0. Ortak üretim hattı (dört üründe de aynı)
| Adım | Ne | Öğrenilen |
|---|---|---|
| 0 | **Mekanizma kartı + ürün kilidi** | Ürün ne yapar, ne hareket eder, ürün/mama hangi açıklıktan çıkar → satıcının açıklama görsellerinden yazılır. Görseller çelişiyorsa en sık görüleni seç ve karta yaz. Ürün kilidi (renk, parça sayısı, yazı, boyut, "Keep identical: …") her prompta kelimesi kelimesine girer. |
| 1 | **Temiz referans görsel** | Tedarikçi fotoğrafı yazılı/kolajlı/filigranlı ya da başka markanın logosunu taşıyorsa önce düz zeminde, yazısız, tek ürünlü "clean pack shot" üret; sonraki her kare buna bakar. Logo taşıyan referansı modele yükleme — logoyu sızdırır. |
| 2 | **ChatGPT: 3 başlangıç karesi** (9:16) | Aynı sohbette K1→K2→K3, ikinci kareden itibaren `CONTINUITY LOCK` satırı. Tekrar eden karakter için önceki videonun karesini 3. görsel olarak yükle ("Image 3 = the SAME animal") → tutarlılık tuttu. |
| 3 | **Google Flow (Veo / Omni Flash 1.2): 3 × 4 sn klip** | Her klip TEK eylem, tek kamera hareketi. 8 sn'lik tek klipte eylem zinciri (bas → düş → ye) bozuluyor. Klip başına ≤3 deneme, her denemede tek değişken. 720p = 12 kredi/klip; 360p kullanılmaz. |
| 4 | **Kalite kontrol** | Her klip 4 kare/sn zaman damgalı panoyla gözle; ayrıca sıçrama ölçümü (klip medyanına göre). 1,5 kare/sn pano hataların çoğunu kaçırdı. |
| 5 | **Kurgu (ffmpeg)** | Klipler art arda → üstte sabit kanca yazısı (saydam PNG) → CTA → SFX → iki geçişli ses normalizasyonu (hedef −14 LUFS, çıktıda ölç) → MP4. Son kare ilk kareye bağlanır (döngü). |
| 6 | **Caption** | Sonunda "🎥 Made with AI" + Instagram "AI ile oluşturuldu" etiketi açık. CTA tek kelime (`Comment "KELİME"`), işlevi DM ile link dağıtmak. |

---

## 1. Köpekbalığı ağızlı kedi yuvası (ABD + TR test planı)
- **Ürün:** peluş, kapalı kedi yuvası; kedi köpekbalığının ağzından girip ağzından bakar. AliExpress $22.09 (çizili $45.08), 169 sold, 4,4★/5 yorum.
- **Neden seçildi:** hot dog köpek yatağı (15MN, tek sabit çekim) ile aynı "nesne-şekilli yatak = tek kare gag" mekanizması; tünel/kapalı yatak ailesi 3 markada milyon.
- **Kimlik:** CAT MOM (kedi annesi) ya da ona hediye alan. 4 kimlik kovası (evcil, hobi, ilişki-ironi, yetişkin parası) + Secret Santa bağlamı.
- **Teklif (tahmin, ölçülmedi):** ABD $44.99 (bant 39.99–49.99), sahte çizili fiyat yerine gerçek 2'li paket indirimi, ücretsiz kargo, fiyat videoda değil caption/bio'da. TR 1.199–1.499 TL kargo dahil, kapıda ödeme önerisi → kapıda ödeme AliExpress'ten doğrudan gönderimle uyumsuz, yerel stok gerekir (para kararı → kullanıcı onayı).
- **İlk versiyon reddedildi:** 3 sahneli hikâye + Noel ("The shark got my cat") milyonluk videolara benzemiyordu. İkinci versiyon kaydedilmiş milyon karelerine bakılarak yazıldı: 4 kısa plan (~2,5 sn), her planda değişen üst yazı, gece kamerası problem planı, insan uyurken hayvan üründe.
- **Test matrisi (10 varyasyon, tek değişken):** V1 kontrol (K2 "Every CAT MOM NEEDS this!") · V2 K5 alıntı-ironi · V3 K11 problem→Vs→çözüm kartları · V4 yazısız · V5 ABD Secret Santa / TR fiyat kancası · V6 K8 POV keşif · V7 ilk kare problem · V8 süre 8 sn · V9 CTA "Send this to a CAT MOM" · V10 hibrit (AI problem + gerçek telefon çekimi). Aynı klip seti iki pazarda kullanılır, yalnız yazı/caption dili değişir → üretim saniyesi pazar sayısıyla artmaz.
- **Bozulma riski ve önlem:** AI köpekbalığının ağzını açıp kapatabilir, "kediyi yiyor" gibi oynatabilir, boyutu büyütebilir → her video promptunda "the mouth is soft fabric and never moves, opens, closes or bites", klip kontrolünde bu hareket = RED.
- **Ürün kilidi hatası:** görmeden yazılan tarif ("kuyruk yüzgeci, açık karın") yanlıştı; tedarikçi fotoğrafıyla düzeltildi (köpekbalığı BAŞI + beyaz oluklu gövde + yan yüzgeç + solungaç çizgileri). Ders: ürün fotoğrafını görmeden kilit yazma.
- **Tahmini maliyet:** API 720p 66 sn × $0,07 = $4,62 (numuneli) · numunesiz $6,72 · 1080p $9,98 · kötü durumda ~$20. Abonelik yoluyla ek ücret yok ama 1–2 gün.
- **Sonuç:** son değerlendirmede ABD'de Walmart'ta aynı tip 23–38$ arası ≥5 satıcı bulundu → çarpan ~2×, "müşteri daha ucuzunu bulur" riski; ilk ürün olarak seçilmedi.

### Senaryo 1 — "PawDozy kalıbı" (ABD, 10 sn, 4 plan)
| Sn | Üst yazı | Görüntü |
|---|---|---|
| 0–2,5 | `The problem vs…😳` | Gece kamerası (siyah-beyaz IR, tavan köşesinden): çift uyuyor, kedi yastığa çıkıp kadının yüzüne yatıyor. Ürün yok. |
| 2,5–5 | `✨The solution✨` | Sabah, beyaz kapitone nevresim, kadın yan yatmış uyuyor; yastığın yanında köpekbalığı yuvası, kedinin yüzü ağzından bakıyor. |
| 5–7,5 | `✨The solution✨` | Yakın: bir el yuvanın içindeki yumuşak minderi bastırıyor, peluş doku görünüyor; köpekbalığı ağzı hareketsiz. |
| 7,5–10 | `Comment "SHARK" if you need one 🦈` | Yatakta gri + mavi iki yuva yan yana, ikisinden de bir kedi bakıyor (2'li alım mesajı) → 2. plana döngü. |

Caption: `Send this to a cat mom 🐈🦈 #cat #catmom #catsofinstagram` + `🎥 Made with AI`. Ses: lisanslı müzik yok; telifsiz yumuşak parça + mırlama.

### Senaryo 2 — V01 kontrol videosu (S1 tek sahne, 12 sn, K2)
| Ekranda sn | Klip | Görüntü (tek eylem) |
|---|---|---|
| 0–4 | A | Kedinin yüzü köpekbalığının ağzından bakıyor (İ3 tuhaf görüntü); yavaşça iki kez göz kırpıyor, kulağı seğiriyor, çenesini peluş dişlere dayıyor. |
| 4–8 | B | Yuva boş, kedi 30 cm sağda; dişleri kokluyor, ağızdan içeri giriyor, içeride dönüp yüzü ağızdan bakıyor. |
| 8–12 | D | Kedi içeride kıvrılmış uyuyor → gözlerini açıp başını kaldırıyor, A'nın ilk pozunda bitiyor (döngü). |

- Ekran yazısı: üst-orta, 0–12 sn `Every CAT MOM NEEDS this! 🦈🐱` (TR deneme: `Her KEDİ ANNESİNİN buna ihtiyacı var! 🦈🐱`); 6–9 sn küçük kart `Comment "SHARK" for the link 🦈` / `"YUVA" yaz, link DM'de 🦈`.
- Caption EN: `Comment "SHARK" and I'll send you the link 🦈 / Your cat finally gets swallowed by a (very soft) shark. / Free shipping · price & bundle at the link in bio. / 🤖 Video made with AI. The shark bed shown is the real product we sell.`
- Ses: klibin ortam sesi (mırlama, peluş hışırtısı) + telifsiz neşeli parça; "Baby Shark", Jaws motifi yasak.
- Klip A başlangıç karesi promptu (özet): `Vertical 9:16 phone-video still frame, photorealistic… SCENE: the cat's face peeks out of the open mouth of a plush shark-shaped cat bed… PRODUCT: [ürün kilidi] — match the attached product photo exactly… WHO: one adult orange tabby… low ground angle… WHERE: real lived-in living room… LIGHT: soft window daylight from the left. FRAMING: main subject in the middle 70%, product ≥1/3 of frame, top third calm for a caption, nothing important in the bottom 20% or right 15%. AVOID: any text, logos, licensed characters, cartoon shark face, realistic sharp teeth, a second cat, human hands, extra paws, studio lighting, bokeh, CGI look.`
- Klip A video promptu: `Vertical 9:16, 5 seconds. Use the provided image as the first frame. CAMERA: locked-off low ground angle, static. ACTION: the cat blinks slowly twice, one ear twitches, then it rests its chin on the felt teeth. PRODUCT: stays identical… The mouth is soft fabric and never moves, opens, closes or bites. AUDIO: soft purring, quiet room tone. No dialogue. No music. AVOID: on-screen text, the shark mouth moving, the bed changing size or color, a second cat, extra paws, sudden scene change.`

---

## 2. Arcade joystick ışık anahtarı kapağı (ABD, tek POV)
- **Ürün:** duvar anahtarı kapağı; kırmızı toplu joystick yukarı-aşağı kayıp alttaki düz anahtarı iter, düğmeler süs. AliExpress $3.22 (çizili $7.77), bu satıcı 94 / toplam 490 satış, 4,9★/53. Önerilen satış $19.99 (2'li $29.99), çarpan 6,2×.
- **Kaynak kalıp:** 2,3MN'lik tek POV video (parmak joystick'i itiyor, ışık yanıyor). Kazanan tip: basit POV ürün-elde + tek "aha" anı. Kimlik kancası en büyük çarpan ("DO NOT show this to a CARGUY" 93,6MN gözlemi).
- **Seçilen:** S1 tek çekim, kesme yok; yazı tek satır, üstte, video boyunca sabit (hot dog yatak kalıbı); kimlik: 90'lar gamer'ı.
- **Risk:** AI tuş/yazı bozar (kapaktaki "arcade game" yazısı, düğme sayısı) → başlangıç karesinde yazı ve düğme sayısı (2 beyaz + 2 mavi) birebir kontrol; joystick yana dönerse, ışık gecikirse RED. Düşük bilet → 2'li paket şart.
- **Durum:** yedek ilk ürün; örnek video planı yazıldı. Kaynakta yalnız **bir** tam senaryo var (ikincisi —).

### Senaryo 1 — "Joystick'i it, oda aydınlansın" (8 sn, tek POV çekim)
| Sn | Görüntü | Ses |
|---|---|---|
| 0–2 | Gece, karanlık yatak odası; duvarda arcade kapağı, koridordan gelen loş ışık. Bir el kadraja giriyor. | sessiz oda |
| 2–4 | İşaret parmağı + başparmak kırmızı topu tutuyor, joystick'i aşağıdan yukarı itiyor — "klik". | net mekanik klik |
| 4–6 | Tavan lambası anında yanıyor, oda aydınlanıyor (oyun konsolları, posterler görünüyor). | 8-bit "coin" sesi (telifsiz) |
| 6–8 | El joystick'i bırakıyor, kapak yakın planda; son kare ilk kareye döngü (ışık tekrar söner). | — |

- Üst yazı (sabit): `DO NOT show this to a 90s GAMER… 🕹️😳` · alt küçük yazı (6–8 sn): `Comment "ARCADE" 👾`
- Caption: `Comment "ARCADE" and I'll send you the link 🕹️ #gamer #gamingsetup #90skid #giftsforhim` + `🎥 Made with AI`
- Başlangıç karesi promptu: `Vertical 9:16 photo taken with an iPhone at night in a dark bedroom. On a plain light wall, at shoulder height, there is a light switch cover that looks EXACTLY like the attached product photo: white face with red and blue stripes, the printed words "arcade game", a red ball-top joystick on the left, two white and two blue round buttons, a "COIN" slot, blue side edge. Keep its shape, colors, text and parts identical. A man's hand is about to grab the red joystick. Only dim warm light from the hallway. Gaming posters and a game console shelf barely visible in the dark. Realistic phone photo, natural noise, everything in focus. AVOID: bokeh, shallow depth of field, cinematic lighting, extra buttons, changed text, extra fingers, watermark.`
- Flow promptu (8 sn): `The hand grabs the red ball joystick and pushes it straight UP along its slot with a clear click; the switch cover itself never moves, bends or changes; at that exact moment the ceiling light turns on and the bedroom becomes brightly lit, revealing gaming posters and a console shelf; the hand lets go. Handheld phone camera, real home footage, no cuts. Sound: room silence, a sharp mechanical click, then a short retro 8-bit coin sound.`
- Kurgu: 1080×1920, üst sabit yazı (beyaz, kalın, ince siyah kontur, güvenli alan üst %14), 6. sn'den alt CTA, kapak = 2. sn karesi.

### Senaryo 2 — —

---

## 3. Evcil hayvan mama piyanosu (ABD, 30 video üretildi)
- **Ürün:** yerde duran kırmızı-siyah oyuncak; şeffaf kırmızı kapak, içte beyaz spiral; önde pati desenli 4 beyaz + 3 siyah tuş; tuşa basınca önden mama düşer. AliExpress $22.18 (çizili $65.68), 11 sold, 4,0★/1 yorum. Satış fiyatı tedarik fiyatının yaklaşık 2,5–3 katı kuruldu; gerçek olmayan çizili fiyat kullanılmadı.
- **Neden seçildi:** 17,5MN kaynak video; hayvan "şakanın kendisi"; AI'ın gerçekte çekilemeyen sevimli hayvan eylemini iyi ürettiği alan. ⚠️ Kaynak videodaki ürün (siyah dik mini piyano) ≠ bizim tedarik ürünü — kalıp alınır, ürün bizimki çekilir.
- **Seri yapısı:** 30 video × 12 sn (3 kare × 4 sn), 16 güne yayıldı. 22 karakter (14 kedi + 8 köpek), her karakter kendi içinde tutarlı. İlk 10 video = 5 kanca ailesi × 2 (K9/K8 POV, K1 yasak-kimlik, K5 alıntı-ironi, K13 yazısız, K11 akış kartları); hediye kancaları tek başına zayıf (%0,44) olduğu için kimlik/sezonla eşlenip Şükran/Black Friday haftasına kondu. CTA tüm seride tek kelime (yorumlara ürünle ilgili tek kelime). Video 02 KONTROL; diğerleri ona karşı tek değişkenle.
- **Kanca dağılımı:** K1 ×4 · K5 ×4 · K13 ×3 · K11 ×3 · K9/K8 ×4 · K10 ×2 · K7 ×2 · K12 ×2 · K2, K3, K4, K6, prank, "Send this to" ×1.
- **Yasak kontrolü 30 videoda:** sağlık/davranış tedavisi iddiası yok ("slow eating", "anxiety" yazılmadı), veteriner/uzman yok, sahte yorum/sayı/indirim/stok yok, logo/lisanslı karakter yok, sahte önce-sonra yok, müzik yok (yalnız telifsiz SFX: piyano notaları, mama tıkırtısı, mırlama).
- **Neler bozuldu (87 kare + 87 klip):**
  - Boş hazne: ChatGPT şeffaf hazneyi boş çizdi → mama boş hazneden çıkıyor gibi. Çözüm: promptta "compartment is half filled with small round brown dry kibble".
  - Erken mama: basılmadan önceki karede yerde mama vardı → K1'de zemin boş olmalı.
  - Çift hayvan: hayvan ürünün arkasındayken öndeki tuşa kadraj dışından pati uzandı (imkânsız anatomi).
  - Yazı bozulması: düzenleme isteği ürün yazısını bozdu ("FEDER") → her düzenlemeden sonra yazıyı kırpıp yakından oku.
  - Yanlış mekanizma: başlangıç karesinde pati kapağın üstünde havadaydı → Veo patiyi kapağa indirdi, kapaktan mama çıktı. Prompt düzeltmesi yetmedi; kare "pati beyaz tuşun ön kenarında" diye yeniden üretildi.
  - AUDIO satırı olay ekletir: basışsız klipte "one treat still rolling" yazınca kimse basmadan mama döküldü; "page edge fluttering" nota kâğıdını uçurdu.
  - Sıçrama / morph: köpek 0,75–1,75 sn'de başka ırka dönüştü, yavru 1,0 sn'de ışınlandı, gece kamerasında ürün kırmızıya döndü → üçü de kırpmayla kurtarıldı. 1,5 kare/sn panoyla "84/87 temiz" dendi; 4 kare/sn panoda 30 videonun 17'sinde hata çıktı.
  - Yazı ürünü örttü: CTA 1150 px'te tuşların üstüne bindi; 3 satıra taşan kancada CTA son satırın üstüne bindi → CTA, kanca yazısının hemen altına akıtıldı.
  - Ses: tek geçiş normalizasyon videolar arası −13,4…−21,6 LUFS bıraktı → iki geçiş, hedef −14.
  - SFX zamanı: Veo sesi basış anında +12…+36 dB sıçrıyor; nota plan saniyesine değil bu sıçramaya (±1,2 sn) oturtuldu — plan saniyesiyle fark 0,1–1,0 sn çıktı.
  - Eşleme: indirilen klip adları sıra taşımıyor → her klibin ilk karesi tüm başlangıç kareleriyle küçük boyutta karşılaştırıldı (87/87 net eşleşti).
- **Neden bırakıldı, neden geri döndü:** satıcının ürün videosu AI'dı (ürün sahneden sahneye renk değiştiriyor, mama bir sahnede yandan fışkırıyor), sayfa "self-playing" diyor, 1 yazısız yorum, benzer ilanlar 6 ve 1 satış. Bizim "mama tuşların altından çıkar" kilidimiz bir AI ürün görseline dayanıyordu → yüksek Flow kredisiyle 30 video doğrulanmamış mekanizmayla üretildi. Ürün bir süre bırakıldı; sonra kural "AI sorun değil, **çıkış noktası net görünsün**" diye yeniden yazıldı ve 29 video düzeltildi: pati çıkış açıklığından uzak (en dış) tuşta, açıklık kadrajda açık, her videoda en az bir kez açıklığın 1–1,5 sn yakın planı.

### Senaryo 1 — Video 01 "I taught my cat to play the piano" (12 sn)
| Sn | Kare | Görüntü (tek eylem) | Ses |
|---|---|---|---|
| 0–4 | K1 | Gündüz oturma odası, ahşap zemin. Ürün yerde. Bir el şeffaf kapağı açıp kuru mamayı hazneye döküyor. Turuncu tekir kedi yanında oturmuş, merakla izliyor. | mama tıkırtısı |
| 4–8 | K2 | Yakın, zemin hizası: kedi sağ ön patisini kaldırıp pati desenli beyaz bir tuşa basıyor → kısa piyano notası → tuşların önünden 3–4 mama tanesi yere düşüyor. | tek nota + mama tıkırtısı |
| 8–12 | K3 | Kedi düşen mamayı yiyor, sonra başını kaldırıp kameraya bakıyor, patisini tekrar tuşa koyuyor (döngü → K2). | iki nota, mırlama |

- Üst yazı (sabit): `I taught my cat to play the piano 🎹😭` · alt (8–12 sn): `Comment "<KELİME>" 🐾`
- Caption: `Comment "<KELİME>" and I'll send you the link 🎹🐱 #catsofinstagram #catmom #catgifts` + `🎥 Made with AI`
- Kare RED listesi: ürün yazısı okunur, 4 beyaz + 3 siyah tuş, şeffaf kırmızı kapak + beyaz spiral, ürün kediden küçük · mama yalnız tuşların önünden · kedi 4 bacak 1 kuyruk, 3 karede aynı kedi · insan 5 parmak, yüz yok · ortam 3 karede aynı · bokeh/sinematik ışık/logo/lisanslı karakter/ürünün kendi kendine çalması yok.

### Senaryo 2 — Video 02 "Konser piyanisti" (K1 yasak-kimlik, KONTROL)
- Karakter: tombul gri British Shorthair, bakır gözlü. Kanca (üstte sabit, 0–12 sn): `DO NOT show this to a CAT MOM… 🫣🎹` · CTA (8–12 sn, kancanın hemen altı): `Comment "<KELİME>" 🐾` · Caption: `Comment "<KELİME>" and I'll send you the link 🎹🐱 She practices every day. #catmom #catsofinstagram #cattoys · 🎥 Made with AI` · Kazanırsa aynı görüntüyle geçiş kancası: `Every CAT MOM NEEDS this! 🐱🎹`
- **K1 (0–4 sn)** — kedi ürünün önünde konser piyanisti gibi dik oturuyor, ön patiler birleşik, tuşlara bakıyor. Video: sağ ön patiyi kaldırıp tuşların üstünde havada tutuyor, henüz basmıyor.
- **K2 (4–8 sn)** — zemin hizası yakın: sağ ön pati ikinci beyaz tuşta. Video: tuşa bir kez basıyor, kısa nota, 3–4 mama yalnız önden yere yuvarlanıyor.
- **K3 (8–12 sn)** — sol patiyle dördüncü tuşa basarken başı geriye, gözler yarı kapalı "müziği hissediyor" pozu; önde birkaç mama. Video: poz korunuyor, baş bir kez yana sallanıyor, çok yavaş itme.
- SFX: 0–4 sn oda sesi · 5,0 sn nota E4 · 5,3–6,3 sn mama tıkırtısı (ahşap) · 8,4 sn nota C5 (2 sn sönüm) · 9,5–12 sn hafif mırlama (−12 dB). Seviyeler: Veo sesi 0 dB, nota −3, mama −6, ortam −18.
- K1 görsel promptu (tam): `Vertical 9:16 phone-video still frame, photorealistic, looks like a real Instagram Reel shot on an iPhone. SCENE: the grey cat sits upright and very straight in front of the product, facing the keys like a concert pianist about to play, front paws together, looking down at the keys. PRODUCT: Low rectangular pet treat toy standing on the floor, exactly like attached image 1 (the RED product; attached image 2 only shows where treats come out — ignore its blue color): red front body on a black base; on top a tall transparent red-tinted lid with a slanted top like a piano lid, a white horizontal spiral auger and round paw-print shapes visible inside it; a red front panel with small vent slits and the white text "PIANO FEEDER"; four big white keys, each with a raised paw print, and three short black keys between them; a small round button on the left side and a tiny switch on the right side. About 20 x 20 cm, clearly smaller than the animal. Treats come out ONLY at the front, below the keys, onto the floor. One single product, nothing else on it, no extra keys, no other text. WHO: a chunky grey British Shorthair cat with round copper eyes and a thick plush coat. Animal anatomy correct: four legs, one tail, normal eyes and mouth. WHERE: a real cozy living room in the US, light oak floor, beige rug edge, a sofa leg and a houseplant pot in the background. LIGHT: soft window daylight from the left. FRAMING: main subject in the middle 70%; the product fully visible, at least one third of the frame, "PIANO FEEDER" readable; top third calm (plain wall or floor) for a caption; nothing important in the bottom 20% or right 15%. TEXTURE: natural phone noise, slight motion blur, real lived-in home, not perfect. AVOID: any extra text, letters, captions or watermark (only the "PIANO FEEDER" text on the product), store signage, brand logos, licensed characters or posters, extra legs, extra paws or tails, distorted eyes or mouth, extra fingers or hands, human face, a second product, a bigger product, studio backdrop, studio lighting, shallow depth of field, bokeh, anamorphic flare, glow or sparkle effects, CGI render look.`
- K1 Flow promptu (tam): `Vertical 9:16, 4 seconds. Use the provided image as the first frame. CAMERA: static handheld phone at floor level, slight sway — one camera move only. ACTION: the cat slowly lifts its right front paw and holds it in the air above the keys, like a pianist preparing; it does not press yet. Only this one action happens. PRODUCT: stays identical to the image… It never moves by itself, never grows, never duplicates. Only the pressed key goes down. Treats appear ONLY at the front, below the keys, and fall onto the floor; nothing comes out of the lid or the sides. LIGHT: unchanged from the image. AUDIO: quiet room tone, faint street noise outside. No dialogue. No music. AVOID: on-screen text, subtitles, watermark, brand logos, extra paws or limbs, morphing animal, morphing or resizing product, treats coming from the lid or sides, the product playing by itself, glow effects, sudden scene change, dialogue, music.`
- K2/K3 promptları aynı kalıp; başa `CONTINUITY LOCK: same animal(s) (…), same room, same light, same RED product exactly as in attached image 1` eklenir, yalnız SCENE / ACTION / CAMERA / AUDIO satırları değişir. Sonradan her Flow promptunun sonuna betikle "KEY LOCK" eklendi (tuşlar önde-altta; pati yalnız beyaz tuşa basar, kapağa asla; mama yalnız tuş indiği anda tuşların altındaki dar açıklıktan; tuşa basılmazsa mama yok; tek kesintisiz çekim, hayvan 4 sn boyunca aynı ırk/renk).

---

## 4. Araç amblemi yerine takılan dijital ekran (ABD, 30 video planı)
- **Ürün:** amblem yerine takılan, ince siyah çerçeveli yuvarlak ekran; uygulamadan animasyon yüklenir. Orijinal $279.95 (+$50 boya eşleme), 12V, IP69. **Dropship edilebilir jenerik muadil bulunamadı** (3 aramada yalnız esnek LED arka cam panelleri ve ışıklı marka amblemleri — ekran değil, çoğu başka markanın logosu). Uyumluluk listesi tek bir otomobil markasına özgü.
- **Neden plan yazıldı:** ürün kendisi dönüşüyor/karakter oluyor (D15 izlenmede ~2×), "sıradan rozet sandın" sürprizi (K5 "It's just a …"), gece + ürün ışığı ilk kare, car guy kimlik kovası.
- **En önemli teknik karar:** AI'a ekranda hiçbir görüntü **çizdirilmez**. Başlangıç karesinde ekran kapalı siyah cam ya da düz tek renk; animasyonlar (radar, göz, alev, kalp, geri sayım… 20 özgün animasyon) kurguda dairesel maskeyle bindirilir. Kamera yalnız sabit / yavaş itme / yavaş kayma (doğrusal hareket iki ölçümle takip edilebilir). Disk konumu ilk ve son kareden ölçülür; bindirme diskten >3 px taşarsa klip yeniden üretilir ya da kırpılır.
- **Referans görsel yüklenmedi:** kaynak karelerin hepsinde başka markanın logosu/model yazısı var → model sızdırır. Geometri basit olduğu için metinden temiz paket çekimi üretildi.
- **Kanca planı:** her aile ≤3 video (K1, K5, K8, K11, K12, K13 ×3; K2, K7, K10 ×2; K3, K4, K6, K9, prank, kurulum ×1). Düz hediye kancası yok; K3/K4 kimlik + bağlamla. CTA `Comment "BADGE"` (marka adı değil, ürünü anlatan kelime). Kanca ≤8 kelime. Video çiftlerinin metin benzerliği en çok 0,31 (eşik 0,80).
- **İlk 5 test videosu** (en düşük AI riski + farklı aile): V01 yazısız radar · V17 "araban göz kırpıyor" POV · V28 gündüz vs gece kartları · V12 "kedi neden kaçtı" gece kamerası · V02 "It's just a badge". Kazanan eşiği (48. saat): paylaşım/izlenme ≥ %0,61 ve beğeni/izlenme ≥ %1,01.
- **Kredi:** 90 klip × 12 = 1.080 taban; %30 yeniden deneme payıyla tavan 1.416 (pay varsayım, ölçülmedi).
- **Yasal/IP riskleri:** hiçbir karede otomobil markası/model/logo yok ("generic white coupe, no badges"); plaka boş beyaz; araç hiç hareket etmiyor (park/show); kırmızı-mavi yanıp sönme yok (polis ışığı çağrışımı, eyalet yasakları); caption: `Display shown parked/for show. Check your local lighting laws.`; plaka karartma ürünü gösterilmez; su testi muadilde doğrulanmadan üretilmez.

### Senaryo 1 — V01 "Radar modu" (K13 yazısız, S1 tek sahne)
| Sahne | Ne olur (4 sn, tek eylem) | Ekran bindirmesi (kurguda) |
|---|---|---|
| 1 (0–4) | Loş beton otoparkta aracın arkası, tampon hizasından, 2 m; amblem yeşil yanıyor. | yeşil radar taraması |
| 2 (4–8) | Daha yakın: bagaj kapağı + amblem kadrajın ortası. | radar (kesintisiz) |
| 3 (8–12) | Makro: amblem beyaz boya üstünde, çerçeve keskin. | radar, son 1 sn ilk kareye döngü |
- Ekran yazısı yok; CTA yalnız caption: `Comment "BADGE" 👇 I'll DM you the link` + ortak caption sonu. Ses: garaj uğultusu + her taramada alçak sonar "ping" (−12 dB); lisanslı müzik yok. Risk: ekran yeşilinin parlama halesi → bindirmeden önce kare ışığına göre renk eşle.

### Senaryo 2 — V02 "Alt tarafı bir amblem" (K5 alıntı-ironi, S7 ürün dönüşür)
| Sahne | Ne olur (4 sn, tek eylem) | Ekran bindirmesi |
|---|---|---|
| 1 (0–4) | Gün batımı sokak; gri kapüşonlu genç sırttan, arabanın bir adım arkasında, kapalı (siyah) amblemi süzüyor. | yok (ekran kapalı) |
| 2 (4–8) | Bagaj yakın: amblem düz mavi yanıyor. | mavi zemin + beyaz şimşek ikonu, 0–0,6 sn açılış |
| 3 (8–12) | Aynı genç eğilmiş, ellerini dizlerine koymuş, irkilip geri çekiliyor. | şimşek → 2. sn'de göz animasyonu (göz ona bakar) |
- Ekran yazısı: üstte sabit `"It's just a badge" 😒` (0–4 sn) → `Me: 🤩` satırı eklenir (4–12 sn). CTA son 3 sn `Comment "BADGE" 👇`. Ses: sokak ambiyansı; 0:04'te kısa whoosh + ekran-açılma blip (−8 dB), telifsiz minimal ritim (−18 dB). Risk: gencin yüzü 3. karede profil; bozulursa sırttan yeniden üret.
- Sahne 1 görsel promptu (özet): `…SCENE: a young man in a grey hoodie, seen from behind, stands one step behind the parked car… looking at the plain black round badge. PRODUCT (the only aftermarket part): one round digital display badge about 7.5 cm across, flush-mounted at the exact center of the trunk lid… no text, letters or logo… never moves, grows, duplicates or detaches. SCREEN: switched off — plain uniform glossy black glass… CAR: a generic modern white two-door sports coupe with no recognizable make or model… no manufacturer badges… blank white plate. LIGHT: warm low sunset light from the left.`

---

## 5. Mağaza ve marka kurulumundan genel dersler (tek ürün Shopify, ABD)
- **Marka adı:** 20 aday ölçüldü; alan adının 404 dönmesi "boşta" demek değil (kayıtlı olabilir) → kayıt bilgisini ve aynı mal sınıfında **sesçe yakın tescilli marka** olup olmadığını kontrol et (adaylardan biri aynı mal sınıfındaki benzer bir tescil yüzünden elendi). Tek hayvana bağlı isim genişlemez.
- **Fiyat:** çizili (compare-at) fiyatı gerçek değilse boş bırak; indirim yerine gerçek 2'li paket ("save $X").
- **Görseller:** tedarikçi görsellerinden sağlık iddiası taşıyanlar ("Reduce Choking Risk, Gentle Digestion", "Food-Grade, Non-Toxic") ve farklı renk varyantları kullanılmadı. Görsel yükleme sırası kayabiliyor → önizlemede kontrol.
- **Teslimat süresi** üç yerde aynı yazılmalı (ürün sayfası, kargo sayfası, SSS): "1–3 iş günü işlem · 8–20 iş günü teslim" gibi dürüst aralık.
- **Mobil:** 390 px'te "Sepete ekle" ilk ekranın altında kaldı (~875 px, görünür alan ~750 px); yapışkan sepet butonu yalnız butonu geçince çıkıyor → görsel oranını küçült ya da yapışkan butonu açılışta göster.
- **Shopify deneme planında video dosyası yüklenemiyor** → ürün videosu plan seçilince eklenir.
- **Ödeme:** Shopify Payments Türkiye'de yok; ABD/AB şirketi yoksa PayPal vb. + ek komisyon. Vergi, alan adı, piksel, test siparişi, numune ayrı karar.
- Kullanıcının doldurması gereken alanlar (yasal ad, adres, destek e-postası, iade adresi, iade kargosunu kim öder) yer tutucu olarak bırakılır, uydurulmaz.
- AI kedi kareleri gerçek müşteri gibi sunulmaz; numune gelince kendi çekimle değiştirilir. Yorum uygulamasına yalnız gerçek alıcı yorumu.
