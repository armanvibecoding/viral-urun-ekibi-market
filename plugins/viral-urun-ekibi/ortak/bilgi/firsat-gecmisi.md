# Fırsat geçmişi — değerlendirilen adaylar ve kararlar

"Bu ürünü daha önce değerlendirdik mi?", "neden elendi?", "hangi aday hâlâ açık?" sorularında buraya bak.
Kaynak: AliExpress ürün sayfaları (satış adedi yalnız ürün sayfasından okundu), Walmart/Target/Chewy/Amazon web araması, Trendyol ilk ~36 kart.
Fiyatlar okunduğu gündeki AliExpress fiyatıdır (gün içinde oynar); "$1.09" yeni-müşteri teklifidir, çarpan hep normal fiyattan hesaplandı.

## Karar anahtarı
- **SAT** = içerik üretimine alındı. **İZLE** = güçlü ama doğrulanacak şey var (numune, fiyat, hukuk, sezon). **ELE** = veto ya da doymuş/düşük marj.
- **Veto** (puanlanmadan ELE): lisanslı karakter/marka, sağlık/tıbbi iddiaya dayanan kanca, çocuk ürünü sertifikası (CPSIA), ağır/hacimli kargo, lityum pil, sıvı+cam, ateş/yanma, büyük marka ürününün kendisi, tasarım/patent benzerliği.
- **Puan (0–11):** A viral mekanizma 0–3 · B girilebilirlik 0–3 (3 = ABD büyük perakendede aynısı yok) · C marj 0–3 (≥3× = 3, 2–3× = 2, 1,5–2× = 1) · D AI ile üretilebilirlik 0–2.
- **Kaynak kodu:** Y = canlı izleme turu (katalogda `Y` satırı) · W = mekanizma benzerliğiyle bulunan AliExpress adayı · V = viral mekanizma (M1–M15) taramasıyla bulunan aday.
- "masa başı" = doygunluk o gün aranmadı, kategori bilgisine göre verildi → zayıf kanıt.

## Üretime alınan / plan yazılan ürünler (özet)
| Ürün | Durum | Neden seçildi | Ne oldu |
|---|---|---|---|
| Evcil hayvan piyanosu (tuşa basınca mama düşen oyuncak, AliExpress $22.18, 11 sold, 4,0★/1 yorum) | SAT → 30 video üretildi | 17,5MN kaynak video; ABD büyük perakendede jenerik bulunamadı; orijinal markalı ürüne göre belirgin ucuz görünür; hayvan "şakanın kendisi" | Mekanizma (mama nereden çıkıyor) doğrulanmadan üretildi; satıcı videosu da AI'dı → bir süre bırakıldı, sonra "AI sorun değil, çıkış noktası net görünsün" kuralıyla 29 video düzeltildi. Ayrıntı: `uretim-deneyimi.md` |
| Arcade joystick ışık anahtarı kapağı ($3.22, bu satıcı 94 / toplam 490 satış, 4,9★/53) | SAT → örnek video planı | Çarpan 6,2× ($19.99, 2'li $29.99), gamer kimliği, tek POV çekim | Yedek ilk ürün; düşük bilet → 2'li paket şart |
| Köpekbalığı ağızlı kedi yuvası ($22.09, 169 sold, 4,4★/5) | İZLE → 10 varyasyon test planı | Hot dog yatak gag'inin (15MN) akrabası, tek karede anlaşılır | Sonra Walmart'ta 23–38$ arası ≥5 satıcı bulundu → çarpan ~2×, "bize özel değil" |
| Araç amblemi yerine takılan dijital ekran (orijinal $279.95) | Plan (30 video), ürün açık | Ürün kendisi dönüşüyor + car guy kimliği | Dropship edilebilir jenerik muadil bulunamadı; tek otomobil markasına özgü; ABD ışık yasası riski → plan ürün-bağımsız yazıldı, muadil bulunmadan üretilmez |

## Tüm değerlendirilen adaylar (80)

Sıra = kaynak dosyadaki sıra. Bağlantı ve fiyat yalnız ürün sayfası açılan adaylarda dolu.

| Kaynak | Aday | A/B/C/D = toplam | Karar | Gerekçe | AliExpress linki | Fiyat · satış · puan |
|---|---|---|---|---|---|---|
| Y1 | Evcil hayvan fotoğraflı kesik portre hediye (POD) | 3/1/2/1 = 7 | ELE | M15 ve paylaşım güçlü ama Etsy'de kişiye özel evcil hayvan süsü çok; AliExpress değil POD. | — | — |
| Y2 | Grinch bebek tulumu | — | ELE (veto) | Lisanslı karakter (Dr. Seuss) + bebek giysisi çocuk güvenliği sertifikası (CPSIA) | — | — |
| Y3 | Diz dostu squat makinesi | — | ELE (veto) | Ağır/hacimli kargo | — | — |
| Y4 | Şarkı söyleyen kuş müzik kutusu (replika) | 2/2/0/1 = 5 | ELE | AliExpress'te mekanik kuş yok (yalnız kuş sesi hoparlörü); Walmart'ta 19$ replika var. | — | — |
| Y5 | Yaşlı adam yüzü baskılı balaclava | 3/2/3/1 = 9 | İZLE (ilk 8) | 15,4MN, tek karede dönüşüm + meslek kimliği; ABD perakendede baskılı versiyon bulunamadı ama AliExpress'te onlarca satıcı. | https://www.aliexpress.us/item/3256813224578403.html | $4.42 (çizili $8.84) · bu satıcı 125, **toplam 10,000+**, 4,9/1373 |
| Y6 | Kitaplık görünümlü duvar saati | 2/2/0/1 = 5 | ELE | AliExpress'te aynı ürün bulunamadı; Walmart'ta kitap temalı saat 17–26$. | — | — |
| Y7 | Kapüşonlu Noel giyilebilir battaniye | 2/0/2/2 = 6 | ELE | Giyilebilir battaniye ABD'de doymuş kategori (masa başı). | — | — |
| Y8 | Hediye paketi kâğıdı kesici | 2/0/1/2 = 5 | ELE | 36,9MN ama ucuz ve yaygın (masa başı), bilet çok düşük. | — | — |
| Y9 | Bağdaş ofis sandalyesi | — | ELE (veto) | Ağır/hacimli kargo | — | — |
| Y10 + Y11 | Kapı basket potası çamaşır filesi | 2/0/2/2 = 6 | ELE | Walmart 19,99$ (Bundaloo), Target 29,99$, Hammacher 19,95$ → doymuş; AliExpress kart 11,49$. | — | — |
| Y12 | Yapışkanlı kapı kolu kilidi | 1/0/1/1 = 3 | ELE | Ucuz jenerik, masa başı elendi. | — | — |
| Y13 | Grinch bagaj bebeği | — | ELE (veto) | Lisanslı karakter; jenerik "bagaj Noel Baba" AliExpress'te bulunamadı | — | — |
| Y14 | Havasız 3D basketbol topu | — | ELE (veto) | Wilson Airless tasarım/patent riski; 3D baskı üretimi | — | — |
| Y15 | Pati izi kil + çerçeve kiti | 2/0/1/1 = 4 | ELE | Walmart'ta pati/burun izi kitleri 3–9$; AliExpress çerçeve kiti kart 9,75$. | — | — |
| Y16 | Ahtapot kafa masaj aleti | — | ELE (veto) | Kanca sağlık iddiasına dayalı ("migraines") | — | — |
| Y17 | Laptop ek ekranı | 1/0/1/1 = 3 | ELE | Elektronik, doymuş kategori (masa başı). | — | — |
| Y20 | Burun izi hatıra kalıbı | 2/1/2/1 = 6 | ELE | M15 güçlü ama burun/pati izi kitleri Walmart'ta ucuz; silikon kalıp Etsy'de ~34$. | — | — |
| Y21 | Şemsiye porselen çay süzgeci | 2/1/1/1 = 5 | ELE | ASMR iyi ama kırılgan porselen, düşük bilet (masa başı). | — | — |
| Y22 | İkiye ayrılan sırt çantası | 2/1/0/1 = 4 | ELE | Jenerik tedarik bulunamadı; kategori Peak Design/Gregory (~400$) elinde. | — | — |
| Y23 | Katlanır köpek küveti | 2/0/2/1 = 5 | ELE | Walmart'ta 15–117$ arası çok sayıda. | — | — |
| Y24 | Karanlıkta parlayan çizim matı | — | ELE (veto) | Çocuk oyuncağı → sertifika (CPSIA) | — | — |
| Y25 | Silikon parmak fidget kaydırıcı | 2/1/1/2 = 6 | ELE | Çok ucuz fidget, masa başı. | — | — |
| Y26 | Fişe takılan pamuk ped koku yayıcı | 1/1/1/1 = 4 | ELE | Ürün tipi belirsiz (kaynakta "tahmini"); tedarik aranmadı. | — | — |
| Y28 | Isıtmalı omuz şalı | 2/1/2/2 = 7 | ELE | Paylaşım beğeninin 3 katı ama Walmart'ta 14–30$ arası çok sayıda; AliExpress kart 16,73$. | — | — |
| Y29 | Isıtmalı ofis sandalyesi minderi | 2/1/1/2 = 6 | ELE | Walmart 20–48$; AliExpress kart 28,09$, 220V varyant riski. | — | — |
| Y31 | Uzak mesafe dokunmatik bileklik | — | ELE (veto) | Büyük marka ürünü (Bond Touch, Totwoo 140$+) + uygulama; AliExpress'te jenerik karşılık yok | — | — |
| Y32 | Orta parmak şaka kutusu | 3/0/1/2 = 6 | ELE | M14 paylaşım gücü yüksek ama Walmart/eBay'de 6–12$, AliExpress kart 1–4$. | — | — |
| Y33 | Nail Morph oje baskı makinesi | — | ELE (veto) | Marka cihaz, pahalı elektronik | — | — |
| Y34 | Horlama durdurucu | — | ELE (veto) | Sağlık iddiası | — | — |
| Y35 | Luxafor meşgul ışığı | — | ELE (veto) | Büyük marka ürünü | — | — |
| Y37 | Evcil hayvan piyanosu (tuşa basınca ödül) | 3/3/2/1 = 9 | SAT — üretime alındı (30 video) | 17,5MN, hayvanın kendisi şakanın merkezi; ABD büyük perakendede jenerik bulunamadı, orijinali 150$ (Indiegogo 2024). | https://www.aliexpress.us/item/3256812774901618.html | $22.18 (çizili $65.68) · **11 sold**, 4,0/1 yorum |
| Y39 | Duvar gözlem kovanı | — | ELE (veto) | Canlı hayvan + hacimli/kırılgan | — | — |
| Y40 | Pembe retro yuvarlak tuşlu klavye | 2/0/2/1 = 5 | ELE | 59,4MN ama retro klavye Amazon'da yaygın (masa başı); AI tuş/yazı bozar. | — | — |
| Y42 | Simli şişede bebek squishy | — | ELE (veto) | Çocuk ürünü + sıvı dolu | — | — |
| Y43 | Mini pençe makinesi anahtarlık | 2/2/1/1 = 6 | ELE | AliExpress kart 1–11$, bilet çok düşük. | — | — |
| Y46 | Gitar penası zımbası | 2/2/3/2 = 9 | İZLE (ilk 8) | Gitarist kimliği + nostalji kıyası; ABD'de yalnız niş marka (Pick Punch 25–40$), AliExpress 8,25$. | https://www.aliexpress.us/item/2251832777619739.html | $8.25 · **39 sold**, 5,0/3 |
| Y47 | Arcade joystick ışık anahtarı kapağı | 2/2/3/2 = 9 | SAT — örnek video planı yazıldı | Gamer kimliği, POV ürün-elde; Walmart'ta joystick versiyonu bulunamadı, AliExpress 3,22$ / 490 toplam satış. | https://www.aliexpress.us/item/3256813102555746.html | $3.22 (çizili $7.77) · bu satıcı 94, **toplam 490**, 4,9/53 |
| Y49 | Mini damlalık sprey şişe | 2/0/1/2 = 5 | ELE | Hack videosu, ürün seyahat şişesi (doymuş, masa başı). | — | — |
| Y50 | Hesap makinesi boyama kalemi | 1/1/1/1 = 4 | ELE | Ürün tipi belirsiz; tedarik aranmadı. | — | — |
| Y51 | Hızlı buz çözme tepsisi + fanlı kapak | 2/0/1/2 = 5 | ELE | 141MN talep sinyali ama defrost tepsisi Amazon'da çok yaygın (masa başı). | — | — |
| Y54 | Şarjlı telefon kılıfı | — | ELE (veto) | Lityum pil kargo + model uyumu | — | — |
| Y58 | Otomatik nail-art yazıcı (lisanslı baskı) | — | ELE (veto) | Lisanslı karakter baskısı (Y33 ailesi) | — | — |
| W1 | Köpekbalığı ağızlı kedi yuvası | 3/1/1/2 = 7 | İZLE — 10 varyasyonluk test planı yazıldı; sonra ABD'de doymuş bulundu | Tek karede gag ama Walmart'ta 23–38$ arası en az 5 satıcı; AliExpress 22,09$ → çarpan ~2×. | https://www.aliexpress.us/item/3256808218224559.html | $22.09 (çizili $45.08) · **169 sold**, 4,4/5 |
| W2 | Noel ağacı duvar kedi tırmalaması | 2/1/0/2 = 5 | ELE | Walmart'ta Diceymbol duvar ağacı 9,59$; AliExpress 30,89$ Walmart'tan pahalı. | https://www.aliexpress.us/item/3256813390263713.html | $30.89 · ürün satışı görünmedi (mağaza 132 sold, 4,7) · görünmedi |
| W3 | Döner kollu futbol antrenörü | 2/1/0/1 = 4 | ELE | AliExpress 57,79$; Target/SKLZ benzerleri daha ucuz, ağır. | https://www.aliexpress.us/item/3256813379598258.html | $57.79 (çizili $165.11) · ürün satışı görünmedi (mağaza 156 sold, 4,4) · görünmedi |
| W4 | Terlik (clog) kedi yatağı | — | ELE (veto) | Crocs ticari görünümü (IP) | https://www.aliexpress.us/item/3256813015543092.html | $35.59 (çizili $74.15) · ürün satışı görünmedi (mağaza 5,000+ sold, 4,2) · görünmedi |
| W5 | Kaplumbağa kabuğu evcil sırt çantası | 3/1/3/2 = 9 | İZLE (ilk 8) | En güçlü akraba (kaplumbağa reveal ~50MN), çarpan 3,2× ama Rubie's (büyük kostüm markası) 15–23$'a satıyor. | https://www.aliexpress.us/item/3256810162037016.html | $7.88 normal ($1.09 yeni müşteri) · bu satıcı 10, **toplam 172**, 4,9/33 |
| W6 | Gotik kedi ağacı + tabut yatak | 2/2/1/1 = 6 | ELE | Hacimli mobilya, Cadılar Bayramı geçti. | https://www.aliexpress.us/item/3256813267655936.html | $51.29 (çizili $205.17) · ürün satışı görünmedi (mağaza 113 sold); ABD deposu · yorum yok |
| W7 | Dumansız masaüstü ateş çukuru | — | ELE (veto) | Ateş/yanma riski + Solo Stove tasarım benzerliği | https://www.aliexpress.us/item/3256811598208556.html | $32.04 yeni müşteri (çizili $89.44) · 11 sold · 5,0 / 2 yorum |
| W8 | Şeffaf retro kasetçalar | 2/2/1/1 = 6 | ELE | Nostalji iyi, çarpan ~1,6×; gövdede "Walkman" yazısı. | https://www.aliexpress.us/item/3256812429344789.html | $48.39 (çizili $87.98) · 4 sold · 5,0 / 1 yorum |
| W9 | Akıllı zikir yüzüğü | 2/1/3/1 = 7 | ELE | Çarpan 4× (7,57$) ama iQibla Zikr Ring marka/patent benzerliği. | https://www.aliexpress.us/item/3256808739857665.html | $1.09 yeni müşteri / normal $7.57 · 161 sold · 4,1 / 19 yorum |
| W10 | 3D baskı kaslı kol evcil kostümü | 3/2/2/1 = 8 | ELE | Mekanizma güçlü ama ürün puanı **1,5★ / 5 yorum** → kalite yüzünden ilk 10'a alınmadı. | https://www.aliexpress.us/item/3256811769066315.html | $1.09 yeni müşteri / normal $13.77 · 46 sold · **1,5 / 5 yorum** |
| W11 | Seyahat ayak hamağı | 2/0/1/2 = 5 | ELE | Amazon'da yaygın (masa başı), düşük bilet. | https://www.aliexpress.us/item/3256808801146090.html | $10.25 (çizili $22.78) · 193 sold · 4,9 / 7 yorum |
| W12 | Onsen fıçısı keçe kedi yatağı | 3/2/2/2 = 9 | İZLE (ilk 8) | "Kedi sıcak küvette" gag'i tek karede; Walmart/Amazon'da aynısı bulunamadı (ArkPet kendi sitesinde 45,99$). | https://www.aliexpress.us/item/3256813202949254.html | $13.99 erken-kuş ("only 1 left"; çizili $34.97) · ürün satışı görünmedi (mağaza 5,000+) |
| W13 | Kızak evcil yatak | 2/1/1/2 = 6 | ELE | Walmart'ta kızak/Noel yatakları 13–30$; AliExpress 22,99$. | https://www.aliexpress.us/item/3256813215843836.html | kart $22.99 · **satış: kart, doğrulanmadı** (sayfa açılmadı) · — |
| V1 | Muz kedi başlığı | 2/0/2/2 = 6 | ELE | Walmart'ta 3–8$. | https://www.aliexpress.us/item/3256806928758914.html | $6.43 normal ($1.09 yeni müşteri) · 10 sold · yorum yok |
| V2 | Bal kavanozu kedi yuvası | 3/1/1/2 = 7 | ELE | Hot dog yatak gag'i ama Chewy NonoPets 22,99$, Walmart 23,99$+ satıyor. | https://www.aliexpress.us/item/3256812739411544.html | $23.34 normal ($14.84 yeni) · **7 sold** |
| V3 | Sırtlıklı katlanır seccade | 2/2/3/1 = 8 | İZLE (ilk 8) | Kimlik hediyesi (M5); ABD'de yalnız niş İslami mağazalar 35–55$; AliExpress 13,25$. | https://www.aliexpress.us/item/3256811581873567.html | $13.25 (çizili $31.55) · **2 sold** (mağaza 113) |
| V4 | UV idrar lekesi feneri | 2/0/2/2 = 6 | ELE | Amazon'da çok yaygın (masa başı). | https://www.aliexpress.us/item/3256804515598467.html | $5.09 normal ($1.09 yeni) · 23 sold · yorum yok |
| V5 | Kameralı kulak temizleyici | — | ELE (veto) | Tıbbi cihaz/sağlık iddiası | https://www.aliexpress.us/item/3256812854393320.html | $4.61 (çizili $36.52) · toplam 123 (bu satıcı 16) · 4,9 / 11 |
| V6 | Yağmur bulutu nemlendirici | 2/0/2/1 = 5 | ELE | 2023'te viral olmuş, doymuş (masa başı). | https://www.aliexpress.us/item/3256808056888671.html | $18.70 (çizili $57.40) · 29 sold · 3,0 / 1 |
| V7 | Tırtıl çocuk uyku tulumu | — | ELE (veto) | Çocuk uyku ürünü (güvenlik sertifikası) | https://www.aliexpress.us/item/3256812729625880.html | $49.29 (çizili $98.58) · ürün satışı görünmedi (mağaza 4,000+) · mağaza 4,1 |
| V8 | Kumandalı osuruk makinesi | 2/0/1/2 = 5 | ELE | Amazon'da yaygın (masa başı). | https://www.aliexpress.us/item/3256812998490828.html | $12.55 (çizili $15.30) · 3 sold ("100K+ benzer") · yorum yok |
| V9 | Havuz köpekbalığı kumandalı tekne | 2/1/1/1 = 5 | ELE | Yaz ürünü, pil + su. | https://www.aliexpress.us/item/3256808428560872.html | $23.40 (çizili $52.00) · 0 sold (mağaza 1,000+, 4,8) · — |
| V10 | Otomatik pati yıkama kabı | 2/1/2/1 = 6 | ELE | Walmart'ta 16–25$ arası çok sayıda. | https://www.aliexpress.us/item/3256810520671417.html | $16.19 (çizili $39.97) · toplam 179 (bu satıcı 48) · 4,9 / 8 |
| V11 | Kapsül cam kedi tüneği | 2/1/1/2 = 6 | ELE | Cam tüneği kategorisi yaygın (masa başı); vantuz düşme riski. | https://www.aliexpress.us/item/3256812605281414.html | $32.49 · ürün satışı görünmedi ("100K+ benzer") · — |
| V12 | Isıtmalı masa matı | 2/1/2/2 = 7 | ELE | Amazon'da yaygın (masa başı). | https://www.aliexpress.us/item/3256810067988086.html | $16.59 (çizili $24.76) · 62 sold · 5,0 / 4 |
| V13 | Balık ağzı terlik | 3/0/1/2 = 6 | ELE | Coddies vb. Walmart'ta 14–24$; AliExpress 14,95$. | https://www.aliexpress.us/item/3256807386287968.html | $14.95 (çizili $25.77) · 6 sold · yorum yok |
| V14 | Kanepe kolu bardaklık-tepsi | 2/0/2/2 = 6 | ELE | Amazon'da yaygın (masa başı). | https://www.aliexpress.us/item/3256809072381512.html | $14.28 (çizili $24.50) · 23 sold · 5,0 / 3 |
| V15 | Ferrofluid şişesi | — | ELE (veto) | Sıvı + cam, kırılgan kargo | https://www.aliexpress.us/item/3256808546752766.html | $23.96 (çizili $57.62) · 37 sold · yorum yok |
| V16 | Retro pager kulaklık kılıfı | 2/0/2/1 = 5 | ELE | elago "Pager" kılıfı Amazon'da 13–17$. | https://www.aliexpress.us/item/3256807402467000.html | $5.30 normal ($1.09 yeni) · 13 sold · 5,0 / 2 |
| V17 | Masa üstü curling oyunu | 2/1/1/2 = 6 | ELE | Normal fiyat 21,42$ → çarpan <2×. | https://www.aliexpress.us/item/3256810032450463.html | $21.42 normal ($1.09 yeni) · 29 sold · 5,0 / 3 |
| V18 | İnek desenli peluş evcil taşıma askısı | 2/2/2/2 = 8 | İZLE (ilk 8) | "My cat is a cow" kimliği (M7); peluş askı Walmart'ta 10–30$ var ama inek desenlisi bulunamadı. | https://www.aliexpress.us/item/3256807703930666.html | $13.63 normal ($3.63 yeni) · **57 sold**, 5,0/8 |
| V19 | Toz toplama jeli | 2/0/1/2 = 5 | ELE | Bilinen kategori. | https://www.aliexpress.us/item/3256804052784755.html | $10.48 (çizili $10.73) · 6 sold (kategori kartlarında 2,000+) · yorum yok |
| V20 | Ezan saatli Kuran lamba | 2/0/2/1 = 5 | ELE | Kuran hoparlör lamba Amazon'da yaygın (masa başı); içerik telifi. | https://www.aliexpress.us/item/3256812184448623.html | $19.66 (çizili $56.31) · toplam 25 (bu satıcı 26) · 5,0 / 1 |
| V21 | Istakoz köpek kostümü | 2/0/2/2 = 6 | ELE | Chewy Frisco 19,99$, PetSmart 19,99$; ürün sayfası bugün açılmadı. | https://www.aliexpress.us/item/3256813198349071.html | $9.15 (çizili $15.00) · ürün satışı görünmedi (mağaza 5,000+, 4,7) · — |
| V22 | Hazine sandığı aurora projektörü | 2/1/1/1 = 5 | ELE | Walmart'ta "Secret Projector" kategorisi var; normal fiyat 27,56$. | https://www.aliexpress.us/item/3256813361646358.html | $27.56 normal ($6.85 erken kuş) · 0 sold (mağaza 10,000+, 4,8) · — |
| V23 | Boyun traksiyon hamağı | — | ELE (veto) | Tıbbi iddia (traksiyon) | https://www.aliexpress.us/item/3256813297102578.html | $11.25 · ürün satışı görünmedi (mağaza 1,000+) · — |
| V24 | Kalorifer peteği kedi yatağı | 2/1/1/2 = 6 | ELE | Walmart 16,57$'dan başlıyor; ABD evlerinin çoğunda petek yok. | https://www.aliexpress.us/item/3256808606864654.html | $28.99 (çizili $42.01) · 33 sold · 4,5 / 4 |
| V25 | Kapı altı rüzgar şeridi | 2/0/1/2 = 5 | ELE | Yaygın (masa başı), düşük bilet. | https://www.aliexpress.us/item/3256810277226452.html | $12.57 normal ($1.09 yeni) · 23 sold · 4,0 / 2 |

## Ek tablolar

### Trendyol'da winner aileleri (aynı ürün var mı, ne kadar doymuş)

| Aile (yurt dışı kanıt) | Trendyol arama | Sonuç | İlk 36 kartta yorum | Aynı ürün var mı? | Okuma |
|---|---|---|---|---|---|
| Galaksi projektörü (Galix 66MN) | galaksi projektör | 1.934 | 19.290 | **Var, çok satıcı** (astronot projektör 3.078–3.775 yorum; 12 diskli projektör ~950 TL) | **Doymuş.** TR'de Galaxora reklamda 1.699 TL; Trendyol'da 400–1.400 TL. Fiyat rekabeti sert |
| Tüy toplama (FurFree 32MN) | tüy toplama eldiveni | 1.745 | 11.004 | **Var** (gırgır tüy toplayıcı 1.400 yorum, 115–199 TL) | Doymuş, ucuz. Meta'da pawpeo.com.tr 389 TL ile yeni giriyor |
| Hayvan cepli hoodie (Pawcket 32MN) | kedi cepli sweatshirt | 402 | 579 | Var ama zayıf (kanguru cepli kedi-köpek hoodie, en çok 99 yorum, ~300–400 TL) | **Yarı boş:** ürün var, talep/marka zayıf → markalı + videolu giriş alanı |
| Hayvan bebek tulumu (Ma Tortue 22MN) | kaplumbağa bebek tulum | 1.032 | 1.780 | **Kabuklu peluş kaplumbağa tulumu ilk 36'da yok** (baskılı/figürlü tulumlar var) | **Boşluk.** Meta'da tosbikdunyasitr (Ekim 2026, 1.139 TL) yeni başladı — ilk rakip |
| Tünel/uyku tulumu kedi yatağı (PawDozy 5MN) | kedi tünel yatak · kedi uyku tulumu | 1.010 · 1.051 | 5.189 · 9.639 | Tünel = oyun tüneli; uyku tulumu tipi yok, kedi evleri var | **Kısmi boşluk:** "giyilebilir/uyku tulumu" formu yok |
| Hot dog / şekilli köpek yatağı (Weeniebedzzz 15MN) | sosis köpek yatağı | **1** | 0 | **Yok** | **Net boşluk** (yurt dışı 15MN) |
| Dev ayak terlik (GoofToes 20,9MN) | dev ayak terlik | 86 | 10 | **Yok** (süet terlikler çıkıyor) | **Net boşluk**; şaka/hediye ürünü |
| Batman maskeli cüzdan (Justice Pocket 30MN) | batman maskeli cüzdan | 53.044 (genel cüzdan) | — | Yok | Boşluk ama ⚠️ Batman = lisans/IP riski → jenerik "süper kahraman maske" versiyonu gerekir |
| Öne eğilen seyahat yastığı (NapNest/CloudRide) | öne eğilmeli seyahat yastığı | 945 | 12.158 | Klasik boyun yastığı doymuş; öne eğilen tip ilk kartlarda yok | Kısmi boşluk (form farkı) |
| Kedi dinozor iskelet kostümü (ForgeBruze 33MN) | kedi dinozor kostümü | 995 | 2.375 | **Yok** (çocuk kostümleri çıkıyor) | **Net boşluk**; sezon (Cadılar Bayramı) |
| Müzikli magnet plak (Vinyl Verse/Xmas Mag) | buzdolabı magnet müzik çalar plak | 494 | 3.486 | Yalnız fotoğraflı magnet | Boşluk; ⚠️ müzik lisansı engeli (AliExpress raporu) |
| Latte art damga (Kitty Café Club, 2026-11-06) | latte art kahve damgası | 64 | — | **Yok** (fincan takımları çıkıyor) | Boşluk; Meta'da jormaria.com 2026-11-05'te 1.499 TL ile girdi — ABD'den 1 gün sonra |
| Retro telefon ahizesi (Long Hello/3 marka) | retro telefon ahizesi cep | 29 | 54 | Yok (masaüstü telefonlar) | Net boşluk |
| Kilim desenli oto paspas (Orientalis 13MN) | kilim desenli oto paspas | 66 | 230 | Yok (PVC muşamba) | Net boşluk (AliExpress'te de yalnız benzeri var) |

### AliExpress adaylarının Trendyol kontrolü (ilk ~36 kart)

| # | Aday | Trendyol araması | Sonuç | Aynı ürün? | Okuma |
|---|---|---|---|---|---|
| 1 | Köpekbalığı ağızlı kedi yuvası | köpekbalığı kedi yuvası | 9.877 (genel kedi yatağı) | Yok — ilk kartlar düz peluş yatak/kedi evi | **Boşluk** (kategori talebi büyük: ilk 36 kartta 18.807 yorum) |
| 2 | Noel ağacı duvar kedi tırmalaması | duvar kedi tırmalama noel ağacı | 1.014 | Yok — klasik tırmalama tahtası (2.570 yorum) | **Boşluk**, sezonluk |
| 3 | Döner kollu futbol antrenörü | futbol antrenör döner kollu top | 180 | Yok — "akıllı futbol topu" (en çok 16 yorum) | **Boşluk**, talep zayıf görünüyor |
| 4 | Terlik şeklinde kedi yatağı | terlik şeklinde kedi yatağı | 473 | Yok — kedi desenli insan terliği | **Boşluk** |
| 5 | Kaplumbağa kabuğu evcil sırt çantası | kaplumbağa kabuğu evcil hayvan çanta | 5.276 (taşıma çantası) | Yok — astronot kedi çantası doymuş (3.857 yorum) | **Boşluk** (taşıma çantası talebi kanıtlı) |
| 6 | Tabut kedi yatağı | tabut kedi yatağı | 255 | Yok | Boşluk (Cadılar Bayramı TR'de zayıf) |
| 7 | Dumansız masaüstü ateş çukuru | dumansız masaüstü ateş çukuru | 25 | Yalnız biyoetanol masaüstü şömine (≤8 yorum) | **Boşluk**; ⚠️ yanıcı |
| 8 | Şeffaf retro kasetçalar | şeffaf kasetçalar bluetooth | 139 | Yok — gramofon görünümlü hoparlör 851 yorum | Kısmi boşluk (nostalji talebi var) |
| 9 | Akıllı zikir yüzüğü (OLED) | akıllı zikir yüzüğü | 1.020 | Var — parmak zikirmatik 15–199 TL (1.047 yorum); OLED akıllı yüzük ilk kartlarda yok | **Doymuş ucuz segment**; premium akıllı yüzük boşluk olabilir |
| 10 | Kaslı kol evcil kostüm | kedi köpek kaslı kol kostüm | 9.183 (genel kıyafet) | Yok | Boşluk |
| 11 | Seyahat ayak hamağı | seyahat ayak hamağı | **2** | Var, 0 yorum (620 TL) | **Net boşluk** |
| 12 | Onsen fıçı kedi yatağı | fıçı kedi yatağı keçe | 508 | Yok (kutu şekilli/keçe ped) | Boşluk |
| 13 | Kızak köpek yatağı | kızak şeklinde köpek yatağı | 11.068 (genel) | Yok | Boşluk, sezonluk |

### Winner ailelerinin AliExpress tedarik özeti (çarpan = site medyanı / AliExpress normal fiyatı)

| Aile | AliExpress medyan | Site medyan | Çarpan | TR gönderim | Not |
|---|---|---|---|---|---|
| 1 Cepli hoodie | $20.85 (n=5) | ≈$59.5 (n=3) | ≈2,9× | kontrol edilmedi (bir ürün TR vitrininde TL fiyatla var) | AYNI; en çok satan 800+ sold ama 3,8★ |
| 2 Kaplumbağa bebek tulumu | — (AYNI yok) | ≈$81 (n=2) | hesaplanamaz | — | bulunamadı; 6 terim + Alibaba/1688 araması; OEM gerekir |
| 3 Tünel/uyku tulumu yatak | $11.19 (n=3) | $34.95 (n=3) | ≈3,1× | kontrol edilmedi | AYNI; Purr Dock bu aileden çıkarıldı (konsol koltuğu) |
| 4 Komik kostüm | $16.28 (n=3) | ≈$36.7 (n=5) | ≈2,3× (ürün bazında 3,7–3,9×) | kontrol edilmedi | Dino ve kırkayak AYNI, Noel ağacı BENZER; satış ≤13 |
| 5 Şekilli yatak (hot dog) | $20.69 (n=2) | $29.99 (n=1) | ≈1,45× | kontrol edilmedi | marj zayıf, hacimli kargo; Dog Tap/SleepJedi aranmadı |
| 6 Galaksi projektörü | $6.38 (n=2) | ≈$37.5 (n=2) | **≈5,9×** | kontrol edilmedi | 4,9★ / 166 yorum, 1.000+ toplam satış; CE kontrolü |
| 7 Magnet plak | $35.69 (n=3) | ≈$100.5 (n=2) | ≈2,8× | kontrol edilmedi | AYNI (NFC); satış 2–22 |
| 8 Tüy toplama (eldiven) | $3.42 normal (n=1) / $8.82 (4'lü) | $14.99 (n=1) | **≈4,4×** | kontrol edilmedi | 4,000+ sold, 4,6★ / 687 yorum; düşük bilet |
| 9 Şaka ürünleri | $12.52 (n=4) | ≈$31 (n=2 eşleşen) | ≈2,5× | kontrol edilmedi | LED el, göbek çantası, ayak terlik AYNI; IP'li olanlar aranmadı |
| 10 Ağrı/destek (dizlik) | $12.61 (n=3) | $44.95 (n=1) | ≈3,6× | kontrol edilmedi | ⚠️ sağlık iddiası yasak |
| B1 Magnet plak TR | $33.89 | $140.99 (Vinyl Verse) | ≈4,2× | kontrol edilmedi | asıl engel müzik lisansı |
| B2 Cepli hoodie TR | $20.85 | ≈$59.5 | ≈2,9× | **var** (1 ürün, TL fiyat) | aile 1 ile aynı |
| B3 Kilim paspas | $28.82 (Fars, BENZER) | okunamadı | hesaplanamaz | kontrol edilmedi | kilim deseni bulunamadı; POD veya yerel üretim |
| B4 Tünel yatak TR | $11.19 | $34.95 | ≈3,1× | kontrol edilmedi | aile 3 ile aynı |

### Kanıtlı ürün aileleri (≥2 bağımsız markada milyon)

| Aile | Markalar (izlenme) | Neden çalışıyor |
|---|---|---|
| **Hayvan cepli / taşıyıcı hoodie** | Pookie 056 (2,3MN anne-bebek), Ginger Paws 071 (1,2MN köpek), Pawcket 086 (**32,8MN** kedi), HuggieCat 115 (2MN), Kitty Capsule Purr Pouch 047 (site ana ürünü) | Eller serbest + sevimli yüz çerçevesi + hediye. 5 marka, 4 kitle (anne/köpek/kedi/koca) |
| **Hayvan şeklinde bebek tulumu** | SnugShells 006 (15,8MN), Ma Tortue 065 (**22,3MN**), BabyTurtle 096 (11,7MN), Elumi 103 (1,5MN dinozor), Tortubebe (500 listesi) | "Peluş sanıyorsun → bebek" reveal'i. Hayvanı değiştirip yeni marka |
| **Tünel / uyku tulumu evcil yatak** | Pawnest 005 (2,1MN), Lulla Paw 084 (1MN + 2,8MN), PawDozy 120 (5MN) — *düzeltme 2026-11-07: Purr Dock 047 araç konsolu kedi koltuğu, bu aileden çıkarıldı* | Gece kamerası "problem" → hayvan yuvada. Site fiyatı 25–65$; 3'ü Zendrop |
| **Komik evcil hayvan kostümü** | ForgeBruze 057 (33,3MN dino iskelet), Hoop Hound 058 (17,5MN), Little Tree Pups 064, CentiPaws 081 (3,7MN), SassyPup 087 (7,7MN), WoofSmile 075 (3,1MN) | Sezon (Cadılar Bayramı/Noel) + AI ile insan tepkisi. 25–60$ |
| **Şekilli / komik evcil yatak** | Weeniebedzzz 063 (15MN hot dog), Dog Tap 080 (4MN), SleepJedi 083 (1MN araba) | Hayvan cinsiyle kelime oyunu (sosis köpeği = hot dog) |
| **Yıldız / galaksi projektörü** | Galix 020 (**66,4MN**), Galaxora TR 049, Star Bella 078 (1,4MN), Galix 2. hesap (5,4MN) | Karanlık odada anlık dönüşüm; TR'de 1.699 TL |
| **Müzikli magnet plak** | Vinyl Verse 067 (2,3MN İtalyan), Xmas Mag 127 (3,5MN Noel) | Aynı ürün, farklı kültür veya sezon kimliği |
| **Tüy/kir toplama** | FurFree 052 (32MN eldiven), Indigo 066 (2MN süpürge), 4FurBaby 102 (5,1MN kum eleği) | Görünmeyen kiri görünür yapan tatmin videosu |
| **Şaka / prank ürünleri** | Flip Buddy 100 (19,8MN), Justice Pocket 085 (30,2MN), Cozypet göbek çantası 091 (14,7MN), BigFooties 123 (4,8MN), Air Cannon 098 (2,4MN), SprayBandit 088 (2,5MN), Annoying Present 129 (1,1MN), Krabby Pay 097 (5,9MN) | Paylaşım > beğeni; "yetişkin parası" ironisi; 25–65$ |
| **Ağrı / destek** | KneeRx 059 (17,4MN), Corevia 109 (2,2MN), Velunor 117 (4MN), SoftStep 124 (1,4MN) | "POV: [ağrı]" kimlik kancası. ⚠️ Sağlık iddiası yazılmamalı |

### Milyon getiren mağazaların teklif profili (70 site)

| Ölçüt | Değer | Kaynak |
|---|---|---|
| Ana ürün fiyatı (USD/EUR/CAD) | medyan **47**, çeyrekler **30 – 69** | 70 site |
| Üstü çizili fiyat gösteren | **54 / 70**, medyan indirim **%40** | 70 site |
| Tek ürün mağazası (≤3 ürün) | **34 / 73** | products.json |
| Ana ürün Ağustos 2026 ve sonrası eklenmiş | **49 / 73** | created_at |
| Kaching (paket/miktar indirimi) | **25** site | HTML |
| Zendrop izi (dropship kanıtı) | **10**: Hydrovara, Pawnest, Nightra, Sorellan, Lulla Paw, Gadgets Stark, PawDozy, MagSeal, MerryDoodle, SoftStep | HTML |
| Yorum uygulaması | Loox 21 · Judge.me 11 · **yok 42** | HTML |
| Fiyat bandı → medyan izlenme | <25$: 2,3MN · 25–40: 2,7 · 40–60: 3,3 · 60–100: 3,2 · 100+: 5,05 | 52 eşleşme |

### Viral mekanizmalar (104 milyon kayıt, kayıt başına tek mekanizma)

| Kod | Mekanizma | Tanım (izleyici neden durdu/paylaştı) | n | Etiket | Kanıt kayıt no | Medyan izlenme | p/b medyan (p≥b) | Gerekli ürün özelliği |
|---|---|---|---|---|---|---|---|---|
| M3 | Obje başka bir şeye benziyor (görsel gag) | Ürünün kendisi bir şaka: "bu gerçekten X mi?" diye durduruyor, şakayı paylaştırıyor | 8 | DESEN | 038, 063, 083, 085, 112, 123, 134, 135 | **9,9 MN** | 0,45 (3/8) | Tanıdık bir nesnenin (yiyecek, araba, ayak, maske) birebir formu; tek karede anlaşılır, yazı gerekmez |
| M2 | Canlıyı karaktere çevirme | Bebek/evcil hayvan bir karaktere dönüşüyor (kaplumbağa, dinozor, kırkayak, basketbolcu) → sevimlilik + absürt | 10 | DESEN | 006, 057, 058, 064, 065, 075, 081, 087, 096, 103 | **9,7 MN** | 0,52 (1/10) | Giyilebilir kılık; canlının yüzü açıkta kalıyor; vücut şekliyle kelime/şekil oyunu yapılabiliyor (sosis köpeği = kırkayak) |
| M4 | Görünmeyeni görünür yapma | Kir, tüy, duman, toz testle ortaya çıkıyor → tatmin + "benimki de böyle mi?" | 5 | DESEN | 014, 052, 066, 077, 102 | 5,1 MN | 0,22 (1/5) | Sonucu fiziksel bir yığın/iz olarak bırakıyor; önce-sonra tek planda |
| M5 | Jenerik ürün + kimlik/kültür/ritüel | Sıradan cihaz bir topluluğun ritüeline/kültürüne giydiriliyor (Kuran, abdest, İtalyan şarkısı, Fars halısı, havacılık) | 9 | DESEN | 051, 054, 067, 068, 076, 101, 106, 127, 131 | 4,5 MN | 0,31 (1/9) | İçerik/desen değiştirilebilir jenerik gövde (disk, baskı, desen) → aynı ürün farklı kimlikle tekrar satılır |
| M13 | Mekanizma merakı / ASMR | "Nasıl çalışıyor?" — mekanizma kendisi seyirlik (manyetik demlik, zırh montajı, termal yazıcı, jet fan) | 6 | DESEN | 060, 093, 095, 111, 114, 118 | 4,5 MN | 0,27 (0/5) | Görünür hareket eden parça veya akış; sesli/sessiz tek sahnede tamamlanıyor |
| M10 | Beden rahatlaması (POV acı/uyku/yol) | "POV: [ağrı/sıcak basma/uçakta 15 saat]" — izleyici kendi bedenini tanıyor | 11 | DESEN | 053, 059, 061, 099, 109, 117, 124, 126, 133, 138, 139 | 4,1 MN | 0,46 (4/11) | Bedene takılan/sarılan ürün; rahatlama tek pozda görülüyor (şişme, sarma, ısınma) — ⚠️ sağlık iddiası riski |
| M11 | Küçük sürtünme → zekice çözüm | Herkesin yaşadığı ufak dert 3 saniyede çözülüyor (duşta telefon, açık poşet, seyahat şişesi) | 10 | DESEN | 001, 003, 055, 092, 108, 110, 116, 121, 125, 130 | 3,6 MN | **0,91** (4/10) | Tek elde, tek adımda kullanım; ucuz; "bilmediğin ihtiyaç" çerçevesi |
| M1 | Anlık dönüşüm (ortam/ürün) | Tek tuşla oda, cam, ayakkabı, masa başka bir şeye dönüşüyor | 9 | DESEN | 020, 030, 036, 037, 062, 069, 070, 078, 113 | 3,2 MN | 0,43 (0/8) | Açık/kapalı iki net hal; karanlıkta ışık veya fiziksel açılma |
| M9 | Bebek uykusu/huzuru | Uykusuz ebeveynin acısı → huzurla uyuyan bebek | 4 | DESEN | 004, 033, 089, 094 | 3,0 MN | 0,79 (1/4) | Bebeğin çevresini saran yumuşak ürün — ⚠️ bebek güvenliği iddiası yasak |
| M14 | Zararsız kaba şaka / prank | Yabancının tepkisi veya "kaba ama komik" intikam (orta parmak LED, hava topu, fıskiye) | 5 | DESEN | 088, 091, 098, 100, 129 | 2,5 MN | **1,44** (3/5) | Uzaktan/gizli tetik; kurbanın tepkisi görülebiliyor; zarar vermiyor |
| M12 | Ekransız oyun/hareket hediyesi | Aile/çocuk ekran yerine birlikte oynuyor → ebeveyn suçluluğunu çözen hediye | 4 | DESEN | 040, 073, 105, 122 | 2,4 MN | 0,77 (1/4) | Birden çok kişinin aynı anda kullandığı, ışık/ses/hareket veren oyun |
| M7 | Canlıyı bedende taşıma | Kedi/köpek/bebek göğüste cepten başını çıkarıyor: eller serbest + sevimli yüz çerçevesi | 6 | DESEN | 056, 071, 079, 086, 115, 137 | 2,1 MN | **0,89** (3/6) | Canlının yüzünü çerçeveleyen açıklık; eller serbest |
| M8 | Evcil hayvan şefkati: problem → huzur | Hayvan üşüyor/tehlikede/kaos çıkarıyor (gece kamerası) → ürünle huzurlu | 11 | DESEN | 005, 044, 047, 074, 080, 082, 084, 119, 120, 128, 132 | 2,1 MN | **0,84** (3/11) | Problem anı tek planda gösterilebiliyor; hayvanın "yuvasına girdiği" son kare |
| M6 | Nesil nostaljisi | "80'ler çocuğu / BO2 fanı / SpongeBob" — eski bir objeyi modern işleve taşıyor | 4 | DESEN | 072, 097, 107, 136 | 1,6 MN | **0,90** (2/4) | Bir nesle ait ikonik form (ahize, oyun silahı, çizgi film parası) + bugünkü işlev |
| M15 | Evcil hayvanın kendisi ürüne | Müşterinin kendi hayvanı ürüne basılıyor/dökülüyor (kravat, burun izi kolye) | 2 | ADAY | 090, 104 | 6,8 MN | 0,38 (0/2) | Kişiye özel üretim (POD/kalıp kiti) |

### Açık aday listesi (TR satırı dahil)

| # | Ürün | Ali link | Ali satış | Ali fiyat | Trendyol (lider doldurur) | DNA skoru | Akraba viral ürün (not no) | Neden tutabilir | Durum |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Köpekbalığı ağızlı kapalı kedi yuvası | https://www.aliexpress.us/item/3256808218224559.html | 169 sold (sayfa) · 4,4/5 | $22.09 (çizili $45.08) | Yok (9.877 genel kedi yatağı) → boşluk | winner 6/7 (1,2,3,4,5,7) | 063, 083, 131 | Hot dog yatak gag'inin köpekbalığı hali; tek kare reveal, risk düşük | AÇIK |
| 2 | Noel ağacı/Noel Baba duvar kedi tırmalaması | https://www.aliexpress.us/item/3256813390263713.html | ürün satışı görünmedi (mağaza 132) | $30.89 | Yok (klasik tırmalama) → boşluk | winner 6/7 (2,3,4,5,6,7) | 005, 064 | "Kedi Noel ağacını deviriyor" problem→çözüm; Noel zamanlaması şimdi | AÇIK |
| 3 | Ağırlıklı tabanlı döner kollu futbol antrenörü | https://www.aliexpress.us/item/3256813379598258.html | ürün satışı görünmedi (mağaza 156) | $57.79 (çizili $165.11) | Yok (akıllı top, ≤16 yorum) → boşluk | winner 6/7 (2,3,4,5,6,7) | 092, 105 | "No partner. No wall" kalıbı + çocuk Noel hediyesi; yüksek bilet | AÇIK |
| 4 | Dev terlik (clog) şeklinde Noel kedi yatağı | https://www.aliexpress.us/item/3256813015543092.html | ürün satışı görünmedi (mağaza 5,000+) | $35.59 (çizili $74.15) | Yok → boşluk | winner 7/7 | 063, 123/134, 005 | Dev ayak terlik + kedi + Noel; ⚠️ Crocs görünüm riski, kısmen keşfedilmiş | AÇIK |
| 5 | Kaplumbağa kabuğu evcil sırt çantası | https://www.aliexpress.us/item/3256810162037016.html | toplam 173 (sayfa) · 4,9/33 | $7.88 normal ($1.09 yeni müşteri) | Yok (astronot çanta doymuş) → boşluk | winner 5/7 (1,2,3,5,7) | 006, 065, 096 | Kaplumbağa reveal ailesinin evcil hali; bilet düşük → paket | AÇIK |
| 6 | Gotik kedi ağacı + tabut yatak | https://www.aliexpress.us/item/3256813267655936.html | ürün satışı görünmedi (mağaza 113) | $51.29 | Yok → boşluk | winner 6/7 (2,3,4,5,6,7) | 057, 131 | "Goth cat mom" kimliği; ⚠️ hacimli, Cadılar Bayramı geçti | AÇIK |
| 7 | Dumansız masaüstü ateş çukuru | https://www.aliexpress.us/item/3256811598208556.html | 11 sold (sayfa) · 5,0/2 | $32.04 yeni müşteri (çizili $89.44) | Yalnız biyoetanol şömine (≤8 yorum) → boşluk | winner 7/7 | 110, 014 | Duman yok testi + kış hediyesi; ⚠️ ateş riski, Solo Stove benzeri | AÇIK |
| 8 | Şeffaf retro kasetçalar (BT+FM) | https://www.aliexpress.us/item/3256812429344789.html | 4 sold (sayfa) · 5,0/1 | $48.39 (çizili $87.98) | Yok (gramofon hoparlör 851 yorum) → kısmi | winner 5/7 (2,3,4,5,7) | 107, 136, 067 | 90'lar nostaljisi kimliği; ⚠️ "Walkman" ibaresi, elektronik | AÇIK |
| 9 | Akıllı zikir/tesbih yüzüğü (OLED) | https://www.aliexpress.us/item/3256808739857665.html | 161 sold (sayfa) · 4,1/19 | $7.57 normal ($1.09 yeni müşteri) | Ucuz zikirmatik doymuş (1.047 yorum); OLED yüzük yok | winner 6/7 (2,3,4,5,6,7) | 054, 051 | "Muslims are too hard to gift" kancası; ⚠️ kategori keşfedilmiş (iQibla), pil | AÇIK |
| 10 | 3D baskı kaslı kol evcil kostümü | https://www.aliexpress.us/item/3256811769066315.html | 46 sold (sayfa) · 1,5/5 | $13.77 normal ($1.09 yeni müşteri) | Yok → boşluk | winner 5/7 (1,2,3,5,7) | 058, 087 | Sahte uzuv gag'i + yabancı tepkisi; ⚠️ kalite 1,5★ | AÇIK |
| 11 | Kalorifer peteğine asılan peluş kedi yatağı | https://www.aliexpress.us/item/3256808606864654.html | 33 sold (sayfa) · 4,5/4 | $28.99 (çizili $42.01) | | winner 7/7 | 005, 120, 084 | M8 gece kamerası problem→yuva kalıbı; kış sezonu, TR'de petek yaygın | AÇIK |
| 12 | Bal kavanozu şeklinde kedi yuvası | https://www.aliexpress.us/item/3256812739411544.html | 7 sold (sayfa) · yorum yok | $14.84 (normal $23.34) | | winner 6/7 (1,2,3,4,5,7) | 063, 083 | M3 yiyecek formu gag'i (hot dog yatak ailesi), yazısız tek kare | AÇIK |
| 13 | Tırtıl şeklinde çocuk uyku tulumu | https://www.aliexpress.us/item/3256812729625880.html | ürün satışı görünmedi (mağaza 4,000+) | $49.29 (çizili $98.58) | | winner 6/7 (1,2,3,5,6,7) | 065, 081, 006 | M2 çocuk→hayvan yanılsaması + Noel hediyesi; ⚠️ AI görünümlü foto, numune şart | AÇIK |
| 14 | Istakoz kılığı köpek/kedi kostümü | https://www.aliexpress.us/item/3256813198349071.html | ürün satışı görünmedi (mağaza 5,000+) | $9.15 (çizili $15.00) | | winner 6/7 (1,2,3,4,5,7) | 057, 081, 064 | M2 evcil karakter kostümü, bilinen ailelerin dışında yeni karakter | AÇIK |
| 15 | Hazine sandığı aurora/galaksi projektörü | https://www.aliexpress.us/item/3256813361646358.html | 0 sold (sayfa; mağaza 10,000+) | $27.56 normal ($6.85 erken kuş) | | winner 6/7 (1,3,4,5,6,7) | 020, 078 | M1 "kapağı aç → oda dönüşür" reveal'i üründe; Noel hediyesi | AÇIK |
| 16 | Sırtlıklı katlanır seccade | https://www.aliexpress.us/item/3256811581873567.html | 2 sold (sayfa; mağaza 113) | $13.25 (çizili $31.55) | | winner 6/7 (2,3,4,5,6,7) | 054, 051 | M5 ritüel kimliği + yaşlıya hediye; Ramazan ~Şubat 2027; ⚠️ filigranlı foto | AÇIK |
| 17 | Ezan saatli Kuran lamba-hoparlör | https://www.aliexpress.us/item/3256812184448623.html | toplam 25 (sayfa) · 5,0/1 | $19.66 (çizili $56.31) | | winner 6/7 (1,2,3,4,5,6) | 054, 051 | M5; Kuran çalar (054, 32,7MN) akrabası; ⚠️ kategori AliExpress'te yaygın, elektronik | AÇIK |
| 18 | İnek desenli peluş çapraz evcil taşıma askısı | https://www.aliexpress.us/item/3256807703930666.html | 57 sold (sayfa) · 5,0/8 | $13.63 normal ($3.63 yeni müşteri) | | winner 6/7 (1,2,3,4,5,7) | 086, 079, 056 | M7 yüz çerçevesi + eller serbest; cepli hoodie ailesinin çanta hali | AÇIK |
| 19 | Havuz şakası kumandalı köpekbalığı tekne | https://www.aliexpress.us/item/3256808428560872.html | 0 sold (sayfa; mağaza 1,000+) | $23.40 (çizili $52.00) | | winner 6/7 (1,2,3,4,5,7) | 098, 100 | M14 prank (en yüksek p/b 1,44); ⚠️ yaz ürünü, pil+su | AÇIK |
| 20 | Muz şeklinde peluş kedi başlığı | https://www.aliexpress.us/item/3256806928758914.html | 10 sold (sayfa) · yorum yok | $6.43 normal ($1.09 yeni müşteri) | | winner 5/7 (1,2,3,5,7) | 057, 064 | M2 "banana cat" meme'i; bilet düşük → paket | AÇIK |
| 21 | Kruvasan şeklinde kedi tüneli + yatağı (TR) | AliExpress US'te bulunamadı (6 arama, 2026-11-10) | — | — | Trendyol 1 ilan: Pet Luxe 969 TL, 1 yorum (3,0★), menşei CN · KUSVA PET 2.997 TL · TR Meta aktif reklam 0 (kontrol sorgusu "kedi yatağı" dolu) · webde kruvasan kedi tüneli videosu bulunamadı | winner 6/7 (1,2,3,4,5,7; tedarik doğrulanmadı) | 063 hot dog yatak 15MN, M3 | "Croissant cat / cat loaf" meme kültürü + tünelden kafa çıkarma, yazısız tek kare; kış yuvası | AÇIK — tedarik (1688) + numune kalitesi |

## "Tutmamış ama tutabilir" tanımı (ölçülebilir)
- **Tutmamış:** AliExpress'te ≤1.000 satış **ve** Trendyol'da ≤100 değerlendirme (ya da hiç yok) **ve** IG/TikTok'ta bu ürünün ≥500B izlenmeli videosu yok **ve** TR'de aktif Meta reklamı ≤3.
- **Tutabilir:** DNA eşiğini geçer + en az bir kanıtlı akraba ürün (aynı acı/wow'u çözen, sosyal medyada patlamış ürün, not numarasıyla).

## Winner ürün kontrol listesi (verilerden türetildi — en az 4'ü)
1. Tek karede anlaşılan dönüşüm veya reveal (peluş→bebek, oda→galaksi, kir→yığın).
2. Belirli bir kimliğe bağlanabilir; aynı ürün kimlik değiştirerek yeniden satılabilir.
3. Paylaşım ≥ beğeni potansiyeli: "bunu birine gönder" (hediye, şaka, ortak acı).
4. Fiyat 25–70$ (paket indirimi + çizili fiyatla anlamlı).
5. Jenerik tedarik (AliExpress/Zendrop'ta var).
6. Sezon kancası (Noel, Cadılar Bayramı, kış).
7. Sessiz izlenebilir: yazısız ya da tek yazıyla anlaşılır.

## TR boşluk hipotezleri (kanıt değil, test edilecek)
- **Müzikli magnet plak + TR kimliği** (Türk sanat müziği / 90'lar pop seti): aynı ürün İtalyan ve Noel kimliğiyle 2 kez milyon aldı. Tedarik var (NFC programlanabilir mini plak çalar, $33.89). Asıl engel: **müzik telifi/lisansı**.
- **Hayvan cepli hoodie + TR kedi annesi:** 5 markada milyon, TR'de görülmedi; Trendyol'da ürün var ama talep/marka zayıf (en çok 99 yorum) → markalı + videolu giriş alanı. Bir AliExpress ilanı TR'ye TL fiyatla gönderiliyor.
- **Kilim desenli araba paspası:** İran halısı versiyonu 13MN; AliExpress'te kilim deseni bulunamadı (yalnız Fars/Bohem benzeri) → baskı-isteğe-bağlı ya da yerel üretim.
- **Tünel kedi yatağı + TR gece kamerası kalıbı:** 3 markada kanıtlı, tedarik $9.70–15.87, çarpan ≈3,1×.
- **Kruvasan şeklinde kedi tüneli (TR):** AliExpress US'te 6 aramada bulunamadı; Trendyol'da 1 ilan (969 TL, 1 yorum) + 2.997 TL bir ilan; TR Meta aktif reklam 0 → tedarik (1688) ve numune kalitesi açık.
- TR Meta'da yeni girenler görüldü (Ekim–Kasım): kabuklu kaplumbağa bebek tulumu (1.139 TL), latte art damga (1.499 TL, ABD'den 1 gün sonra), tüy toplayıcı (389 TL).

## Mekanizma → AliExpress arama terimi örnekleri
Arama terimi ürün adından değil mekanizmadan üretilir:
- M2 canlıyı karaktere çevirme: pet costume food shaped funny · lobster costume dog cat · baby pea pod sleeping bag
- M3 obje başka şeye benziyor: sushi shaped pet bed · fish shaped slippers funny · object shaped dog bed pun
- M4 görünmeyeni görünür yapma: pet urine detector uv flashlight · car cleaning gel slime dust
- M5 kimlik/ritüel: portable prayer mat travel pocket · ramadan lantern quran speaker light
- M7 canlıyı bedende taşıma: pet carrier chest bag hands free small dog
- M8 evcil hayvan problem→huzur: radiator cat bed hanging · cat window perch suction cup bubble · dog paw cleaner cup
- M10 beden rahatlaması: heated mouse pad hand warmer
- M11 küçük dert→zekice çözüm: couch armrest cup holder tray silicone · door draft stopper under door
- M12 ekransız oyun: tabletop hockey game family fast
- M14 prank: remote control prank toy adult
- Diğer denenenler: coffin cat bed · turtle shell costume for dog cat · airplane footrest hammock · smart tasbih ring · shark pet bed · christmas tree cat scratcher · solo soccer kick trainer · retro cassette player bluetooth · bathtub shaped pet bed

## Aramada elenen aileler (aday değil)
- Çamaşır makinesi tüy topu (kartta 410.000+ satış — doymuş), tortilla bebek battaniyesi (2019'dan beri viral), sahte kollu köpek kostümleri (lisanslı korku karakteri), muz/ananas kedi yatağı (eski viral), 500 oyunlu retro konsollar (ROM/IP riski), dışkı şakaları (ucuz/bayağı), balık nakışlı terlik (fotoğraf balık şeklinde değil).
