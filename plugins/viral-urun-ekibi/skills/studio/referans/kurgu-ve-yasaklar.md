# Kurgu talimatı + yasaklar

> Kaynak notu: bu dosya ~100 milyon izlenen ürün videosunun saha incelemesinden (kayıt numaraları köşeli parantezde, ör. [058]) ve bir dış araştırmadan derlendi. Ham veri seti eklentiye dahil değildir; sayılar o ölçümün sonucudur.

Kurgu = Flow'dan (Gemini Omni) gelen 3–4 klibi (4 sn) `cut` becerisiyle (ffmpeg) ya da CapCut / Instagram editöründe birleştirmek.
Kaynak: 97 milyon kayıt (saha veri seti). Etiket: KURAL ≥3 · ADAY 2 · GÖZLEM 1.

## 0. Üretim kuralları (canlı izleme)
- **Kare = tek eylem, 4 sn.** Video 3 başlangıç karesi × 4 sn klip (12 sn). Tek 8 sn klipte eylem zinciri (bas → düş → ye) AI'da bozuluyor; her klip yalnız bir eylem.
- 🔴 **ÇIKIŞ NOKTASI NET GÖRÜNÜR:** AI üretim sorun değil; sorun izleyicinin ürünün NEREDEN çıktığını görememesi (piyano videolarında mama kedinin patisinin altından çıkıyormuş gibi göründü). Kurallar: (1) üretime başlamadan "mekanizma kartı" yaz — ne basılır, ürün hangi açıklıktan çıkar (satıcı görselinden; görseller çelişiyorsa en sık görüleni seç ve kartta yaz), (2) basış karesinde pati çıkış açıklığından UZAK bir tuşta (en dış tuş), açıklık kadrajda açık ve örtülmemiş, kamera önden-alçak, (3) her videoda en az bir kez çıkış açıklığının yakın planı (1–1,5 sn, ürünün açıklıktan çıktığı an), (4) video promptu: "treats emerge from the [açıklık] — visibly separate from the paw; the paw never covers or touches the opening", (5) 4 fps kontrolde ek soru: "ürün çıktığı karede açıklık görünüyor mu, ürün patiden/elden çıkıyor gibi mi?" — öyleyse RED.
- **Ürün mekanizması referanstan doğrulanır:** ürün nereden çıkar/ne hareket eder, ürün sayfasının açıklama görsellerinden okunur ve prompta yazılır ("treats come out ONLY at the front"). Mekanizmayı uydurma.
- **Kare kontrol listesi (RED ölçütü, her karede):** ürün yazısı/parça sayısı/renk birebir · ürün boyutu sabit · canlı: 4 bacak, 1 kuyruk, bozuk göz/ağız yok, 3 karede aynı hayvan · insan: 5 parmak, ekstra uzuv yok · ortam 3 karede aynı · arka planda marka/lisanslı karakter YOK (ChatGPT kendiliğinden Zelda/Mario posteri koydu → düzelttirildi).
- **Viral video ≠ bizim ürün:** kalıbı aldığın videodaki ürün ile tedarik ürünü aynı mı karşılaştır (ör. [hesap] siyah dik piyano ≠ AliExpress "PIANO FEEDER"). Video bizim tedarik ürünüyle çekilir.
- **Kazanan tip (canlı izleme ~210 video):** hayvan/kişi ürünle şakanın kendisi olduğu an · basit gerçek görünümlü POV · problemin en net karesi. Kalıp birebir kopyası (aynı hesapta tekrar) 2–12 beğenide kaldı → aynı fikir, yeni an.

- **Yazı ürünü örtmez** (2026-11-08, piyano örneği): CTA 1150 px'te tuşların üstüne bindi. Yazı katmanını son karelerde (özellikle ürün en büyük göründüğü an) kontrol et; ürün alt yarıdaysa CTA hook'un hemen altına (~460 px) gider. Kurgu: `cut` becerisi (ffmpeg + saydam PNG yazı katmanı).

### 0.1 Kalıcı kalite kapısı (2026-11-08, 30 piyano videosunda 17 hata sonrası)
Hata sınıfları ve kök sebebi (ölçüldü, saha dersi):
| Sınıf | Örnek | Kök sebep | Kalıcı önlem |
|---|---|---|---|
| Yanlış mekanizma (kapağa basınca mama) | v10, v22, v28, v08 | Başlangıç karesinde pati kapağın ÜSTÜNDE havada → Veo patiyi kapağa indirir | Basış klibinin başlangıç karesinde pati **zaten beyaz tuşun ön kenarına değiyor** olmalı. Kare kontrol listesine madde: "pati nerede?" |
| Mama yanlış yerden / kendiliğinden | v04, v28 k2 | Belirsiz "from under the keys"; basışsız klipte ses satırında "treat rolling" | Ürün kilidi + mekanizma kilidi **betik tarafından otomatik** eklenir (`prompt_uret.py`); basışsız klipte AUDIO satırında mama/tık sesi YAZILMAZ |
| Sıçrama (ışınlanma, nesne kaybolması, klip içi kesme) | v14, v25, v30, v22, v28 k1, v05 | Veo 4 sn'de ara kesme üretiyor | `klip_qc.py <klip>` (cut) kurgudan ÖNCE zorunlu; işaretlenen saniye kırpılır ya da klip yeniden üretilir |
| Yavaş morph (hayvan ırk/renk değiştiriyor) | v20, v21, v09 | Veo; ölçümle yakalanmıyor | `klip_qc.py --pano` → **4 fps** zaman damgalı pano, her kare gözle. 1,5 fps pano 17 hatanın çoğunu kaçırdı — YASAK |
| Ses seviyesi farkı (8 dB) | v05 vs v22 | loudnorm tek geçiş | `kurgu.py` ölç-düzelt döngüsü, hedef −14 LUFS; çıktıda ölç |

Mekanizma kilidi ÖRNEĞİ (piyano ürünü; her ürün için `kilit.txt` içinde `MECHANISM:` satırı olarak yazılır, betik her Flow promptuna ekler — elle yazma):
`KEY LOCK: the keys are the four white rectangles at the FRONT-BOTTOM of the product, below the "PIANO FEEDER" panel. A paw or nose presses ONLY a white key; it never touches, presses, rests on or pushes the clear red lid on top. Treats appear ONLY at the moment a white key goes down, from a narrow opening at floor level directly BELOW the white keys — never on top of or between the keys, never from the lid. If no key is pressed, no treat appears. ONE continuous shot: no cuts, no jumps, nothing vanishes or appears, the animal keeps the same breed, colors and markings for all 4 seconds.`


## 1. Süre ve kesme

- **Toplam 8–15 sn, hedef 10–12 sn** — KURAL (83/97 kayıt 8–15 sn; medyan 12). 20 sn ve üstü yalnız 13 kayıt.
  Eski "12–24 sn" aralığı daraltıldı.
  **Ölçüm (2026-11-07, içerik matematiği ölçümü §3):** 104 milyonun 90'ı 8–15 sn, medyan 12. Ama milyonların içinde süre izlenmeyi açıklamıyor
  (ρ=0,04, n=93; ≤12 sn 3,1MN vs >12 sn 3,2MN). Milyon-altı kayıtların uzun olması (medyan 24 sn) gözlem dönemine karışık (ρ(kayıt no, süre)=−0,58).
  → Aralık = kazananların tipik formu; kısaltmak tek başına kazandırmaz. Testte süre düşük öncelikli değişken; ≤8 sn (n=6) "deneme".
- **Klip başına ekranda 2–4 sn**: Omni'nin 5–6 sn klibinden en iyi 2–4 sn'yi al. Örnek akışlar: 4 sahne × ~3 sn [071], 4 sahne × ~2,5 sn [086], 3 sahne [131].
- **Tek sahne kesmesiz** 8–12 sn de milyon alıyor — KURAL (14): 014, 038, 060, 063, 066, 072, 085, 089, 090, 097, 105, 114, 117, 123.
  Gag/mekanizma ürününde kesme ekleme [123: gerçek tek kare 4,8MN vs çok sahneli AI 16,5B–52,4B].
- **Döngü:** son kare ilk kareye bağlanır — KURAL (9 kayıtta akışta açıkça "döngü"): 001, 056, 057, 058, 059, 072, 085, 089, 092.
  Yöntem: ilk kadraja dön, ürünü aynı yere bırak, sahneyi kesmesiz bitir.

## 2. Ekran yazısı

- **Üç seçenek** (videoya göre birini seç):
  1. Tek cümle, video boyunca sabit — KURAL (3): 061, 125, 129 (+ kanca kancası olan çoğu kayıt).
  2. Akış kartları `The problem → Vs… → The solution` / `The Concept → VS → The Result` — KURAL (16, D12).
  3. Yazısız — KURAL (20, D7). Problem/CTA caption'da.
- **Özellik cümlesi** yalnız İŞLEVİ söyleyen tek cümle olarak: "It's a life jacket with chin support...🛟🥺" [132] — ADAY.
  Ölçü/ağırlık/renk/malzeme kartları ("121 mm · 30 g · Rose gold") yazı DEĞİLDİR: bilgi verir, ikna etmez (2026-11-17
  kurucu reddi). Eski "özellik başına 1 yazı [001]" önerisi kaldırıldı. İkna kalıpları:
  `kanca-kutuphanesi.md` §1b Ekran yazısı. Fiyat: ICE-01.
- **İddia metni yazma:** yazılı teklif/"sturdy"/"fix" metinleri yazısız demoya kaybetti [102: 983–2.275 vs 5,1MN; 117: 2.461–3.590 vs 4MN] — ADAY (2).
- **Biçim (uygulama kuralı, kanıt değil):** üst-orta üçte bir; beyaz kalın sans-serif, ince siyah kontur; 1–2 satır + 1–2 emoji; alt %20 ve sağ %15 boş (Instagram arayüzü).
- Yazı AI'a ürettirilmez; editörde eklenir.

## 3. Ses

- **Konuşma yok** — KURAL (96/97; tek istisna GERÇEK-MARKA kurucu anlatımı [033]).
- **Doğal/ASMR ürün sesi** (klik, kâğıt, kum, kesme) — KURAL (10): 060, 066, 068, 076, 089, 095, 101, 102, 116, 130 (kayıtta açıkça ASMR / klik sesi / ses yok yazıyor).
  Omni klibindeki ortam sesini koru; müziği altına koy.
- **Müzik:** milyonlarda lisanslı popüler şarkılar var (070, 109 Adele; 076 Michael Jackson; 129 Bublé; 047 The Ronettes; 044 Dua Lipa) → **bizde YASAK** (yasak #3).
  Sahadan alınan ders şarkı değil **ton**: sezon neşesi, duygusal, enerjik. Meta Sound Collection / telifsiz kütüphaneden o tonda parça.
  (Web: işletme hesabı/reklamda lisanslı müzik kısıtı — https://www.foximusic.com/blog/instagram-reels-music-copyright-legal-guide/ · https://www.soundstripe.com/instagram — satıcı blogları, Meta resmi metni bulunamadı.)

## 4. CTA ve caption

| CTA | Etiket | Kanıt |
|---|---|---|
| `Comment "[KELİME]" for the link [emoji]` (ekranın ortasında ya da caption'da) | KURAL (36) | D5: 003, 005, 006, 036, 037, 040, 044, 047, 054, 056, 058, 063, 065, 072, 077, 078, 084, 085, 088, 091, 096, 099, 100, 103, 106, 107, 109, 110, 112, 114, 115, 119, 122, 126, 128, 132 |
| DM otomasyonu cümlesi: `…and I'll send you the link` / `we'll DM you the link` | KURAL (6) | 065, 077, 096, 103, 114, 126 (096 yorumları kapatıp DM) |
| `Send this to a [KİMLİK]` (paylaşım isteyen) | KURAL (8) | 078, 080, 081, 082, 083, 084, 086, 120 |
| Soru / seçim: `Which one is your favorite?`, `Who else would keep going? 👇`, `rate 1-10` | KURAL (3) | 062, 068, 092 |
| Emoji yorum: `Drop a [emoji] in the comments if…` | GÖZLEM (1) | 109 |
| Link in bio / site adı (CTA yok gibi) | çok kayıt | 001, 020, 051, 067, 069, 070, 073, 098, 123 … — milyon için yorum CTA'sı şart değil |

**Ölçüm (2026-11-07, içerik matematiği ölçümü §6):** yorum-kelime CTA'lı videolarda yorum/izlenme %0,016 (n=37), yorum istemeyenlerde %0,016 (n=50) → **1,01×**;
yorum/beğeni 1,08× (n=43/63), yalnız milyonda %0,78 vs %0,76. Yani `Comment "X"` yorum oranını ölçülebilir artırmıyor; işlevi **DM ile link dağıtımı**.
Paylaşım isteyen `Send this to a [KİMLİK]` (n=6: 080, 081, 082, 083, 086, 120) paylaşım/beğeni 1,26 vs tüm milyon 0,61 — ZAYIF, "deneme".
Soru CTA'sı (n=6: 049, 062, 068, 092, 109, 124) yorum/beğeni %2,32 vs %0,87 — ZAYIF, "deneme".
→ Karar: CTA'yı hedefe göre seç (link → Comment; paylaşım → Send this to; konuşma → soru). Yorum/izlenme karar metriği değil.

Kelime = ürünün özü ya da hayvan/eylem: SWIM [132], REX [103], SLEEP [099], CALM [119], PAW [115].
Caption: ilk satır CTA; ekranda yazı yoksa problem/fayda cümlesi caption'da [004, 094, 117].

## 5. Seri ve hesap

- **Aynı set, 5–10 kanca, ayrı videolar** — KURAL (60, D1). İzlenmesi en yüksek kancayı yeni sahnelerle tekrar et — KURAL (11, R2).
- **Yeni hesap da milyon alabilir:** 131 SkyPaw 3 gönderi / 1.218 takipçi, 3. videoda 1,4MN — GÖZLEM. Aynı kalıbı en az 3 kez dene.
- **Deneme sayısı (ölçüm, içerik matematiği ölçümü §2):** milyon görmüş 104 hesabın gönderi medyanı **110** [48–182]; ≤20 gönderide milyon 12/104, ≤50 gönderide 30/104.
  İzlenme/takipçi medyanı **308×** (74/91 ≥100×) → takipçi tabanı şart değil (ρ(takipçi, izlenme)=0,24).
  Aynı profilde kazanan video, diğer görünen videoların medyanının **4,7 katı** (n=27) → kazananı mutlak sayıyla değil hesap-içi katla seç.
  → 10 varyasyon = 1 parti; kazanan çıkmazsa yeni görüntüyle 2. parti (`olcum-ve-test-plani.md`). Başarısızlık oranı veride yok.
- **Kazanan ürün başka hesap/kimlikle tekrar milyon** — KURAL (5): kaplumbağa tulumu iki marka bağımsız [065 22,3MN, 096 11,7MN] · tünel yatak 3 marka [047 hesabı 5,5MN, 084, 120 5MN] · buzdolabı plak magneti İtalya→Noel kimliği [067 2,3MN, 127 3,5MN] · kardeş hesap ikinci ürün [047 Ek, thekittycapsule 10,5MN] · aynı ürün influencer'da [108 Ek, 46,4MN vs marka hesabı 1,6MN].
- **Affiliate/yaratıcı ağı** markanın kendi hesabından büyük olabilir — ADAY (2): 108 Ek (30×), 061 Ek ([hesap] 4,4MN, ücretli ortaklık).
- Niş topluluk sayfası dağıtım çarpanı — GÖZLEM (akış: [hesap]).

## 6. AI kullanımını belirtme (web)
- AB: gerçek gibi görünen AI video için açıklama zorunlu, 2 Ağustos 2026'dan beri (https://artificialintelligenceact.eu/article/50/).
- TR: tüketici davranışını etkileyen AI kullanımı reklamda belirtilir, yürürlük 1 Ağustos 2026 (https://www.alomaliye.com/2026/07/01/sosyal-medya-ve-indirim-reklamlarina-yeni-kurallar/amp/ — haber özeti).
- Meta "AI info" etiketi (https://www.meta.com/en-gb/help/artificial-intelligence/355108217670024/): otomatik olarak Meta'nın kendi araçlarıyla yapılan reklamlara konuyor; **üçüncü taraf araçla (Omni) yapılan reklamda etiket "olmayabilir"**, ticari reklam için self-beyan kutusu metinde yok [ARAŞTIRMA madde 2]. Omni çıktısında SynthID (engadget URL'si `sahne-sablonlari.md` §0).
- TikTok reklam: açıklanmamış AI içerik reddedilir/kısıtlanır (https://ads.tiktok.com/help/article/tiktok-ads-policy-misleading-and-false-content). YouTube Shorts: C2PA'da "tamamen üretken" içerikte etiket kalıcı (https://billo.app/blog/ai-labeling/) [ARAŞTIRMA madde 16].
- TR: kapsam özellikle **insandan ayırt edilemeyen AI dijital karakter**; ibare "açık ve ayırt edilebilir" olmalı → AI insanlı TR videosunda caption'a ek olarak **videonun içinde** kısa ibare (madde metni doğrulanmadı) [ARAŞTIRMA madde 18].
- Sahada: 128 Instagram "AI içeriği" etiketiyle 1,1MN aldı — etiket milyonu engellemedi (GÖZLEM).
- **Etiketin duygusal içerikteki bedeli:** hakemli çalışmada (~700 katılımcı) "AI ile üretildi" etiketi duygusal gönderide etkileşimi ~46 puan, "AI ile geliştirildi" ~24 puan düşürüyor (https://www.cbs.dk/en/articles/ai-labels-reduce-social-media-engagement) [ARAŞTIRMA madde 3]. Sahada tam AI gövde izlenme medyanı 2,1MN vs gerçek 4,0MN (içerik matematiği ölçümü §4c).
  → S4 (hayvan/bebek anı) ve S9 (huzur) için aynı kancayla iki versiyon: tam AI ve S10 hibrit (gerçek çekim + AI kanca). Etiket kapatılmaz.
→ **Kural:** "AI ile oluşturuldu" etiketini aç (organik); **her pazarda** caption'a kısa AI ibaresi (Meta reklamda etiketi kendisi koymayabilir); TR'de AI insan varsa videonun içinde de.

---

## 7. YASAKLAR — kayıtta milyon almış olsa da kit önermez

| # | Yasak | Milyonlarda görülen (kopyalanmaz) | Kitin jenerik karşılığı |
|---|---|---|---|
| 1 | **Lisanslı karakter / başka markanın adı-logosu** (çizgi film, oyun, süper kahraman, araba markası) | kahraman maskeli cüzdan [085], çizgi film parası kart kılıfı [097], oyun silahı difüzör [072], araba markası çizgili ceket [106], spor araba maketi duş başlığı [112], sezon karakteri figürü [088] | **kendi karakterin** (uydurma maskot, adsız "dragon", "space hero"), nesil/hobi kimliği ("90s kids", "gamers", "car guy"), jenerik "sports car" silueti |
| 2 | **Gerçek mağaza adı / uydurma iş birliği** ("RUN to [mağaza]", "[MAĞAZA] X [MARKA]", mağaza üniforması) | 056, 079, 086, 107 milyon; aynı kalıbın 10 hesapta düşük kalan versiyonları (N1) | mağaza sahnesi yok; gerekirse **"büyük mağaza rafı"** tabelasız, ≤2 sn [132, GÖZLEM] |
| 3 | **Lisanslı popüler müzik** | 044, 047, 070, 076, 109, 129 | telifsiz parça, aynı ton |
| 4 | **Reklamda izleyicinin sağlık durumunu söyleyen kanca (Meta kişisel özellik kuralı, PLT-01); bebek uyku güvenliği iddiası.** Sağlık ve sonuç dili ("ağrıyı geçirir", "Fix Foot Drop") yasak DEĞİL: yazılır, yumuşatılmaz, çıktıya "Bilgi notu (kullanıcının sorumluluğu)" eklenir (IDD-01, `ortak/kurallar.md`) | "POV: you have a torn ACL" [059], "POV: You have back pain and sciatica" [109], "Fix Foot Drop" (düşük) [117], anksiyete [119] | durum/an anlatan POV ("POV: 15 hours on the plane…" [099], "POV: No partner. No wall" [092]); sağlık ürününde yazısız takma demosu [117 kalıbı] (performans gözlemi: iddialı metinli sürüm düşük kaldı; yasak değil) |
| 5 | **Sahte otorite / uzman** ("vet recommended", beyaz önlüklü AI doktor) | 119 "Vet recommended this calming head wrap"; 059 AI doktor videoları (zaten düşük 2,3–17,3B) | sahibin kendi gözlemi ("My dog was shaking every time…") |
| 6 | **Sahte yorum / AI müşteri tanıklığı**, uydurma yıldız ekranı | — | gerçek alıcı yorumu (Loox/Judge.me) yalnız gerçekse |
| 7 | **Gerçek kişi / ünlü yüzü-adı** (karta konan ünlü fotoğrafı dahil) | 085 kart slotunda ünlü yüzleri | kendi model/AI karakterin, kullanıcının kendi fotoğrafı |
| 8 | **Uydurma sosyal kanıt / basın / indirim** ("250M+ views", "8000+ happy customers", sahte üstü çizili fiyat) | 014 bio, 047 bio; 49/65 sitede üstü çizili fiyat | yalnız ölçülmüş sayı; AB 30 gün, TR 10 gün kuralı |
| 9 | **Ürünün yapmadığını gösteren görüntü / uydurma özellik** ("%100 su geçirmez" ürün öyle değilse; IDD-02). Sonuç cümlesi ("kazayı önler") yasak değil, bilgi notuyla yazılır (IDD-01) | can yeleği [132] gibi güvenlik ürünlerinde risk | **AI görüntüsü de bir iddiadır:** efekt/ışık/boyut/hız gerçek ürünle aynı olmalı; ASA'ya göre ürün etkisini abartan AI görüntüsü yanıltıcıdır ve AI ibaresi bunu düzeltmez (https://www.rpclegal.com/snapshots/advertising-and-marketing/summer-2025/cap-issues-guidance-on-use-of-ai-in-ads/); LED ayakkabı vakasında AI parlaklığı abartmış (https://jingsourcing.com/fb-ai-product-marketing/). Fayda kanıtının yalnız gerçek çekimle verilmesi kullanıcı kararına açık (dış araştırma, açık soru 1) |
| 10 | **Kişiyi küçük düşüren / taciz eden prank** (gerçek yabancıya fiziksel şaka, kaba hareket ürünü) | 098 hava topu yabancılara, 100 trafikte orta parmak | AI-2 tepkisi zararsız ve kısa; gerçek kişiye fiziksel temas yok (kit kararı, saha kanıtı yok) |

Yasak listesi her video promptunun AVOID satırına ve her paketin son kontrolüne girer.

---

## 8. İmâ yolu — işlevi açıkça söylenemeyen ürün (reklamı yasak / hassas kategori)

Örnek kategori: yetişkin wellness ürünü, reklamı kısıtlı kişisel bakım ürünü. Platform kelimeyi ve bedeni yasaklar ama
izleyici ürünün NE OLDUĞUNU çıkaramazsa video ürün satmaz (2026-11-17: takı gibi görünen ürün videoda "sadece kolye"
okundu; kurucu: "ürünün asıl işlevi hissedilmiyor"). Kural: **açık söylenemeyen işlev, en az iki kanaldan imâ edilir.**
1. **Ses — vızıltıya İZİN VAR (kurucu talimatı 2026-11-17; "titreşim sesi asla" türü eski kural bunun yerine geçer):**
   platform görüntü+ses+metni birlikte değerlendirir, bu yüzden üç koşul zorunlu: (a) ses ekranda görünen masum bir
   nesneden gelir (ör. masadaki telefon), (b) motif videoda en fazla 3 kez, (c) vızıltı ürün yakın planıyla aynı anda olmaz ve ürün kadrajdayken HER karede (geçiş ve döngü kareleri dahil) kontrol arayüzü kapalı/seviye 0 gösterir (yoksa seçilen ≠ görünen); yükselen seviye → sessizlik → drop doruğu ürüne bağlanmaz (imâ 2); (d) imâ taşıyan son vızıltıda önceki vızıltıların kaynağı (telefon) kadrajda olmaz ve son vızıltı, ürünün içinde durduğu kutunun (ya da ürünün orta/uzak planda) kadrajda göründüğü planın İÇİNDE başlar (kutunun içi görünürse ürün içindedir); siyah/karanlık kare kaynak sayılmaz (kaynaksız = ağır kusur).
   Titreşim ürününde kısa buzz motifi (`cut/referans/ses-tasarimi.md` efekt kartı "Buzz"), 1–3 kez, ilk 5 sn'de bir
   kez, müziğin vuruşuna kilitli. Kaynak örnekleri: masadaki telefon, saat, kapalı kutu. Vızıltı + nefes/inleme/fısıltı
   ya da yatakta beden YOK.
2. **İmâlı yazı:** çift anlamlı ama tek başına masum cümle; yetişkin izleyici ikinci anlamı alır. Kalıplar:
   `It's not just a necklace.` · `It looks like jewelry. It isn't only jewelry.` · `Ask me what it does. 🤫` (emoji caption'da) ·
   `For the nights you…` · `Read the comments.` (yorumlarda soru → DM'de ürün sayfası). Yasak: açık kelime, beden, algospeak
   (yanlış yazılmış kelime), sağlık/etki iddiası, gizleme/sır dili (partnerden saklama).
3. **Görüntü metaforu:** işlevin kendisini değil sonucunu/ritmini gösteren nesne/hayvan/doğa (titreşen yüzey, telefonun masada titremesi,
   tabakta tıkırdayan obje, açılan çiçek; dalgalanan su/sıvı+cam AI'da üretilmez → gerçek çekim, `baslangic-karesi.md` §6 Sıvı modülü). Metafor işlevle aynı fiili taşımalı; taşımıyorsa (kabuğundan çıkan hayvan =
   "cesaret", işlev değil) ses ve yazı işlevi taşımak zorunda.
4. **Kontrol:** "2. izleme testi" (kör jüri `anlasilir` alanı; ICE-03) — ürünü bilmeyen hedef izleyici iki izlemede işlevi çıkarıyor mu. Çıkaramıyorsa
   ağır kusur (`cut/referans/agir-kusurlar.md`). Platform riski için caption'da da açık kelime yok; işlev ürün sayfasında.
5. Ürün kartına (`kart.md`) `işlev cümlesi:` (açık, iç kullanım) ve `imâ planı:` (ses · yazı · görüntü) satırları yazılır.

### 8.1 Platform sınırı (Instagram/Facebook öneri kuralları; dış araştırma 2026-11-17)
Üç ayrı ceza basamağı: **A. gönderi öneri dışı** (takipçi görür, Keşfet/Reels önermez — yetişkin ürün/hizmet *tanıtımı* ve
müstehcen içerik buraya düşer) · **B. hesap öneri dışı** (A'nın tekrarı ya da ad/biyografi/profil fotoğrafında uygunsuz öğe;
hiçbir içerik takipçi dışına gitmez) · **C. kaldırma / hesap kapanması** (çıplaklık, ima edilen cinsel aktivite — çizim ve AI
dahil, grafik cinsel dil, cinsel talep). Mizahi cinsel metafor kaldırılmaz ama 18+ ile sınırlanır (Keşfet'e gidemez).
Kaynak: https://www.facebook.com/help/1257205004624246 · https://transparency.meta.com/policies/community-standards/sexual-solicitation/
- **İmâ seviyesi (0–3; direktör `video-elestirmen` yazar):** 0 imâ yok (işlev hissedilmez → ağır kusur) · **1 obje/duygu/ilişki imâsı = hedef**
  · 2 yatak odası/ilişki-anı imâsı = yalnız deneme gönderisi (Trial Reels, ana grid değil) · 3 cinsel karşılaşma imâsı =
  YAYINLANMAZ (ağır kusur). Metafor ilişkiyi/duyguyu/nesneyi anlatır; yatakta ne olduğunu anlatmaz.
- **Kelime kapısı (ekran yazısı + caption + hashtag + ses dökümü):** ürün kategorisinin açık adı, anatomik kelime, "sex/toy/
  pleasure/NSFW/18+" ve bunların algospeak yazımları (s*x, seggs) YOK — algospeak tanınıyor ve fayda ölçülmedi. Tek isabet = KALIR.
  Ürünün pazar kartındaki/kart.md'deki yasak listesi esastır.
- **Biçim kapısı:** anatomik/fallik biçimli ürün kadraja hiç girmez; ürün çalışırken yakın plan yok; çıplak omuz + yatak,
  çarşaf altı, iç çamaşırı, şeffaf kumaş, ürün + çıplak/yatakta beden aynı karede yok. Takı görünümlü ürün kapalı giysi
  üstünde, boyunda takı olarak gösterilebilir (yüz yok, çalışırken yakın plan yok); obje görünümlü ürün obje olarak
  gösterilebilir. Gizlenen parça örtü/kumaş altında da biçim bırakmaz (şişkinlik, uzun çıkıntı yok): promptta örtü
  'flat and smooth', ürün yalnız görünen parçası kadar bir yuvada.
- **Ana konu testi:** videonun ana konusu "ürün tanıtımı" ise Keşfet önermez (basamak A) → hikâye/durum/duygu önde, ürün
  ipucu ikinci planda; ekranda fiyat, "shop now", indirim sayacı yok.
- **Hesap katmanı:** biyografi, kullanıcı adı, profil fotoğrafı ve link sayfasının ilk ekranı açık kelime taşımaz.
- **Tekrar sınırı:** 10 gönderide en çok 1 sınırda (imâ 2) deneme; hesap durumu (Account Status) haftalık kontrol; reddedilen
  içerik düzeltilmeden yeniden yüklenmez.

- Giyilebilir ürünün boyunda takılı göründüğü plan AI ile üretilmez (Flow politika reddi + sahte görünüm, 2026-11-18): kurucunun kendi telefon çekimi (yüz yok, 3 sn) ya da ürünün gerçek fotoğrafı kullanılır.
