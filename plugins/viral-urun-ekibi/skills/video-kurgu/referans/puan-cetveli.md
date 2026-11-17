# Video puan cetveli (teslim ve ön-üretim eleştirisi)

Amaç: aynı video, aynı eleştirmen ya da başka eleştirmen tarafından ±1 içinde aynı puanı alsın. Her alan puanı aşağıdaki
**gözlenebilir** çapalardan birine bağlanır; çapa dışı sıfat ("güzel", "zayıf") puan gerekçesi değildir.
Ara puan (4, 6, 8) yalnız iki çapanın ölçütleri karışık tutuyorsa verilir; hangi ölçütün tuttuğunu yaz.
Kanıt: 4 fps kare panosu (ilk 2 sn 10 fps) + `ses_olc.py VIDEO --drop <sn> --muzik_stem <müzik stem'i> --kapi` JSON'u.
Panoya bakmadan alan puanı yok. Müzik stem'i (`ses_tasarla.py --stem_klasoru` → `muz.wav`, ya da kurgucunun miks betiğinin
yazdığı müzik stem'i) yoksa kurgucudan iste; gelmezse ses alanı en fazla 5 ve raporda "müzik girişi ölçülemedi".
**Varsayılan hüküm KALIR.** 2026-11-17: bu cetvelle 7,0 GEÇTİ alan hikâye videosu kurucu tarafından reddedildi (müzik
12,6 sn'de bir anda açıldı, yazı bilgi veriyor ama ikna etmiyor, organikte fiyat, ürünün işlevi hissedilmiyor) → bu dört
kusur aşağıda ağır kusur ya da "İkna ve işlev" alanı olarak eklendi. Kurucunun reddettiği her GEÇTİ, çapa tablosuna satır olur.
Plan süreleri panodan değil ayar dosyasından okunur: `(bit − bas) / hiz` (`is/NN/kurgu/VNN.json`); 3 fps pano 0,86 sn'lik
planı "tek kare" gösterebilir (kalibrasyonda ölçüldü).

## Toplam kuralı (tek kural)
1. **Toplam = altı alanın düz ortalaması** (kanca, gerçekçilik, yazı, ritim, ses, ikna), en yakın 0,5'e yuvarlanır (6,25 → 6,5; 6,2 → 6,0).
2. **Ağır kusur tavanı:** aşağıdaki ağır kusurlardan biri varsa toplam en fazla 5 ve video KALIR. Ağır kusur kontratta
   (`KURALLAR.md`) yazmasa da düşürür.
3. Teslim geçer: toplam ≥ 7 **ve** hiçbir alan < 5 **ve** ağır kusur yok. Ön-üretim ayrıca ikna ≥ 6 ister.
4. Kontrat dışı kusur ("YENİ KURAL", ağır olmayan): alan puanı **kontrata göre** verilir; yeni kural ilgili alanı
   yalnız bilgi amaçlı `toplam_yeni`de **en fazla 1** düşürür. Geçti/kaldı kontrat puanlarından hesaplanır → yeni kural
   tek başına videoyu düşüremez; sonraki serinin `KURALLAR.md`'sine önerilir.

**Ağır kusurlar:** seçilen ≠ görünen (telefonda dokunulan karo, sonraki araç planında görünmüyor ya da başka içerik çıkıyor;
yalnız dokunuş gösteren videoda) · uydurma/doğrulanmamış iddia (fiyat, yasallık, su geçirmezlik, "herkes soruyor", kurulum süresi) · ürün/plaka/el
4 fps panoda ≥ 0,5 sn boyunca biçim değiştiriyor ya da eriyor · yasa dışı kullanım imâsı. Soru biçimindeki kanca ("Is this legal?") iddia değildir; cevabı ("It's legal") uydurmadır.
Ağır DEĞİL (gerçekçilik 5, kontrat K7/K8): video seçilmemiş içerikle bitiyor ya da seçilmeden yeni içerik beliriyor.

**Ağır kusurlar — 2026-11-17 kurucu geri bildiriminden (otomatik KALIR, kontrat sormaz):**
- **Ani müzik girişi:** `ses_olc.py --muzik_stem … --kapi` çıkış 3 — kural: açılış diegetik ses olayıyla (kutu tık, telefon titreşimi), müzik 0. sn'de −30 dB'den başlar, 1,5–2 sn'de yatak seviyesine çıkar; kapı (başlangıç ≤ −20 dB · rampa 1,2–3,0 sn · ilk 1 sn ≥ −30 dB · 3 sn basamak ≤ +10 dB · açılış olayı ≥ −6 dB). "Kısık/boğuk yatak, drop'ta tam müzik" tarifi bu kusurdur (ölçüldü: +22,2 dB).
- **Organik videoda fiyat:** organik (ücretsiz paylaşım) kreatifin ekranında fiyat, "$", "TL", indirim yüzdesi. Fiyat
  caption/bio/ürün sayfasındadır. Reklam kreatifinde karar pazar kartına bağlıdır (`pazar-katmani.md` §4).
- **İşlev hissedilmiyor:** "2. izleme testi" (İkna alanı) 3 çıkıyor — izleyici iki izlemede ürünün NE İŞE YARADIĞINI
  (doğrudan ya da imâyla) çıkaramıyor. Reklamı yasak kategoride açık söylenemiyorsa alt mesaj zorunlu: ses (ör. kısa
  titreşim/buzz efekti), imâlı yazı, görüntü (`ai-video-kreatif/referans/kurgu-ve-yasaklar.md` §İmâ yolu).
- **Hassas kategori platform kapısı** (`ai-video-kreatif/referans/kurgu-ve-yasaklar.md` §8.1): kelime kapısında tek
  isabet · imâ seviyesi 3 · anatomik biçimli ürün kadrajda ya da çalışan ürün yakın planı · vızıltı + nefes/inleme/yatakta beden · vızıltı
  görünür masum kaynaksız, > 3 kez ya da ürün yakın planıyla aynı anda (vızıltının kendisi serbest, kurucu talimatı).
- **Yazının çoğu özellik listesi:** yazı kartlarının yarısından fazlası ölçü/ağırlık/renk/malzeme ("121 mm · 30 g") →
  yazı alanı 3 (alan < 5 = KALIR). Tek ölçü kartı, ancak bir merak/ikna cümlesine bağlıysa izinli.

## Kanca (ilk 1,7 sn)
| Puan | Gözlenebilir ölçüt |
|---|---|
| 9 | İlk karede değişmiş ürün + bir olay (alev, dokunuş, söküm) + kanca yazısı tam; ilk 1,5 sn'de ikinci bir değişim (ekran içeriği ya da durum değişiyor; aynı içeriğin başka açısı sayılmaz). |
| 7 | İlk karede değişmiş ürün yakın ya da orta planda, kanca yazısı tam; olay ya da ikinci değişim yok. |
| 5 | Şunlardan biri: ürün (değişmiş ekran) ilk 0,9 sn'de görünmüyor · durağan stok geniş planla açılış · kancadaki nesne görüntüde yok · açılış karesi seride başka videonun açılışıyla aynı. |
| 3 | İlk 1,7 sn'de ürün yok **ve** olay yok; ya da sessiz/siyah açılış; ya da kanca yazısı kelime kelime beliriyor. |

## Gerçekçilik ve mantık
| Puan | Gözlenebilir ölçüt |
|---|---|
| 9 | Panonun hiçbir karesinde biçim/renk/yazı oynaması yok; ürün ışığı ve yansıması sahneyle uyumlu; plaka tüm planlarda aynı; seçilen = görünen. |
| 7 | Bozulma yok; yalnız brief'te kabul edilmiş sınır (ör. plaka ay etiketi planlar arasında değişiyor) ya da tek planlık ışık uyumsuzluğu. |
| 5 | Bir planda < 0,5 sn biçim oynaması (ör. ikon kenarı bir karede değişiyor) · bindirme kenarı taşıyor · video seçilmemiş içerikle bitiyor ya da seçilmeden yeni içerik beliriyor. |
| 3 | Ağır kusur (yukarıdaki liste): dokunulan ≠ hemen görünen, ≥ 0,5 sn dönüşüm/erime, plastik yüz/fazla parmak, uydurma iddia. |

## Yazı
| Puan | Gözlenebilir ölçüt |
|---|---|
| 9 | Her yazı ≤ 5 kelime ve ≤ 2 satır; hiçbir yazı plaka rakamı ya da ürün ekranı üstünde değil; yetim kelime yok; alt %20 ve sağ düğme sütunu (sağ %15 × alt yarı) boş; her yazının söylediği o planda görünüyor. |
| 7 | 9'un kurallarına uyuyor, ama bir yazı görüntüyle zayıf bağlı (ör. "Change it anytime" planında değişim gösterilmiyor) ya da ekranda < 0,5 s + 0,25 s/kelime kalıyor. |
| 5 | Şunlardan biri: bir yazı plakayı ya da ürün ekranını kapatıyor · yetim kelime (üst satır ≥ 3 kelime, alt satır tek kelime) · yazı görüntüyle çelişiyor ya da iddiası görünmüyor (ör. "Anything" + 2 ikon; telefonda alev seçilirken "Heart mode") · 3 satırlık kanca. |
| 3 | Yazı okunmuyor (kontrast/boyut) · emoji kutucuğu/bozuk harf · yazı ürün ekranını tamamen örtüyor. (İki 5-ölçütü birden = 4.) |

## Ritim
| Puan | Gözlenebilir ölçüt |
|---|---|
| 9 | Her plan ≥ 2 vuruş (140 BPM'de ≥ 0,85 sn, ayar dosyasından), önce/sonra kesimi drop'ta (flaşla), aynı klip aralığı iki kez kullanılmıyor, son kare ilk kareye bağlanıyor (döngü). |
| 7 | 9'dan bir ölçüt eksik (ör. döngü yok ya da bir plan tekrarı var); önce/sonra drop'ta. |
| 5 | Önce/sonra drop'a oturmuyor **ya da** < 2 vuruşluk plan var **ya da** aynı iki planın gidip gelmesi (A-B-A-B) videonun yarısını kaplıyor **ya da** yapı seride başka videonun kopyası. |
| 3 | 2 sn'den uzun durağan plan + önce/sonra anı yok; ya da toplam süre 8–15 sn dışında. |

## Ses (`ses_olc.py` ile ölçülür; dinlenemez — yalnız ölçüleni yaz)
| Puan | Gözlenebilir ölçüt |
|---|---|
| 9 | `muzik_giris.tuttu` ✓ (diegetik açılış, müzik −30 dB'den 1,5–2 sn rampa, ani basamak yok) · I = −14 ±1 LUFS, tepe ≤ −1 dBTP, delik yok, drop kullanıldıysa `drop_artis_db` 6–10 (vurgu efekt + kısa sessizlik vuruşuyla; müzik kendisi kısılıp açılmaz), drop dışında 0,1 sn RMS'te +10 dB'den büyük sıçrama yok, ana ses anı (`tepe_anlari`) görüntüdeki olayla ±0,1 sn (ölçülmediyse en fazla 8) · müzik seçim ölçütü (`ses-tasarimi.md` §2b) dosyada gerekçeli. |
| 7 | `muzik_giris.tuttu` ✓, I = −14 ±1, tepe ≤ −1, delik yok, drop dışı sıçrama ≤ +10 dB; müzik seçimi gerekçesi yok ya da tür ürünle zayıf bağlı. |
| 5 | Şunlardan biri: drop kullanılıp `drop_artis_db` < 6 · drop dışında (plan ortası ya da son 0,5 sn) > +10 dB sıçrama · I ±1 dışında (±2 içinde) · müzik stem'i ölçülemedi · "stok müzik" hissi (tür/duygu ürünle ve pazarla çelişiyor; gerekçeyle yaz). |
| 3 | Müzik yok · `muzik_giris` KALDI (ağır kusur) · delik (`delikler` dolu) · I ±2 dışında · tepe > 0 dBTP (kırpılma). |

## İkna ve işlev (2026-11-17; yazı + görüntü + ses birlikte)
**2. izleme testi (zorunlu):** videoyu ürünü bilmeyen hedef izleyici gibi iki kez izle (pano + ses ölçümü + yazı listesi).
Rapora iki cümle yaz: (1) "1. izlemede anladığım: …" (2) "2. izlemede anladığım ürün ve işlevi: …". İkinci cümle ürün
kartındaki gerçek işlevle örtüşmüyorsa ikna en fazla 3. Ayrıca **gönderim testi:** "Bunu kime gönderirim?" tek cümle
(ör. "bestie'me", "partnerime"); cevap yoksa ikna en fazla 7. Hassas kategoride **imâ seviyesi** (0–3, §8.1) yazılır.
| Puan | Gözlenebilir ölçüt |
|---|---|
| 9 | 2. izlemede işlev net (açık ya da imâ: ses + yazı + görüntüden en az ikisi aynı işleve işaret ediyor); yazıların çoğu merak/ikna/kimlik kalıbı (`kanca-kutuphanesi.md` §1b Ekran yazısı); en az bir itiraz/arzu cevaplanıyor; organikte fiyat yok; ABD hedefinde ≥ 1 ABD kültür unsuru görünür. |
| 7 | İşlev 2. izlemede anlaşılıyor (tek kanaldan); yazıların yarısı ikna kalıbı; fiyat yok; kültür unsuru zayıf ya da yok. |
| 5 | İşlev ancak caption okunursa anlaşılıyor · yazılar düz bilgi (özellik/ölçü) ağırlıklı ama liste değil · ABD hedefinde kültür unsuru yok. |
| 3 | 2. izlemede işlev anlaşılmıyor ya da yanlış anlaşılıyor (ör. yetişkin wellness ürünü "sadece kolye" okunuyor) · yazıların yarısından fazlası özellik listesi · organikte fiyat (ağır). |

## Çapa videoları (amblem serisi, 2026-11-16; soğuk ABD araç-modifiye izleyicisi)
Kök: `is/NN/teslim/` (ürün klasörü) (25/26/28: `bekleyen/` içindeki sürüm).
| Video | Son eleştiri | Cetvel (kanca/gerç/yazı/ritim/ses[/ikna] → toplam; amblem satırları ikna alanından önce) | Belirleyici kanıt |
|---|---|---|---|
| 01 M3 is-this-legal (tur-1 kontratı) | 7 GEÇTİ | 9/7/5/8/7 → 7,0 GEÇTİ | alev + X ekran ilk karede; "want" yetim (5,5 sn); tüm planlar ≥ 0,86 sn; drop +6,2 dB. Plaka-yazı ve kapanış kuralları o tarihte yoktu → YENİ KURAL |
| 01 (bugünkü kurallarla) | — | 9/5/4/8/7 → 6,5 KALIR | + 7,2 sn'de yazı plakada (yazı 4), gülen yüz seçilip X ile bitiyor (gerç 5) |
| 27 Maybach old-money | 7 GEÇTİ | 7/8/8/7/8 → 7,5 GEÇTİ | taç ilk karede, olay yok; plaka sabit; "Change it anytime" planında değişim yok; drop +10,5 dB |
| 25 M2 stock-to-anything | 6 KALDI | 5/5/6/5/8 → 6,0 KALDI | açılış 20'nin kapağı; yüzgeç 5,6 sn'de biçim oynatıyor; "Anything" + 2 ikon; 0,43 sn'lik planlar |
| 26 Golf flame-badge | 5 KALDI | 7/5/5/6/8 → 6,0 KALDI | alev seçilip hemen alev görünüyor ama video kalple bitiyor (gerç 5); "Heart mode" yazısı alev seçim planında |
| 28 Golf owners-need-this | 5 KALDI | 5/5/7/5/5 → 5,5 KALDI | ürün 1,8 sn'de; kalp seçilmeden beliriyor ve kalple bitiyor; alev/kalp A-B-A-B; son 0,3 sn +11,2 dB |
Sınama (2026-11-17): cetvel yazarı + çapa tablosunu görmeyen bağımsız kör puanlayıcı. İlk kör turda 01 "seçilmemiş
içerikle bitiyor = ağır" yüzünden 5'e düştü → kapanış kusuru ağırdan çıkarıldı (gerçekçilik 5), plan süresi ayar dosyasına bağlandı.
| H1 hikâye (yetişkin wellness, metafor; 2026-11-17, kalibresiz) | 7 GEÇTİ (5 alan) | 7/6/3/8/3/3 → 5,0 KALIR (bugünkü kurallarla) | kurucu reddetti: müzik 12,6 sn'de açılıyor (stem basamağı +22,2 dB, ağır); ad+fiyat kartı organikte (ağır); "Looks like jewelry / 121 mm · 30 g" bilgi kartları (yazı 3); 2. izlemede ürün "kolye" okunuyor, işlev yok (ikna 3) |
Yeni sektörde ilk seri: o sektörden 2 videoyu (biri geçen, biri kalan) bu tabloya ekle; çapa dışı sektörde puanı "kalibresiz" işaretle.
