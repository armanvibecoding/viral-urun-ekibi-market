# Ortak istem blokları (0.3.6): HAZIR İSTEM modu

Kaynak: test12 (ince-uzun metal ürün, koyu zemin, 7 görsel + logo; kullanıcı beğendi) ve test13 (0.3.5'in gerçek ChatGPT koşusu: model istemi kendi yazınca pastel zemin, geniş iki renkli başlık, kalan gravür, kolaj, iki bıçağı dişli ürün çıktı). Bu dosya `uretim-promptlari.md` ile çelişirse BU DOSYA geçerlidir.

## 0. HAZIR İSTEM kuralı (0.3.6; en üst kural)
- **İstemi sen YAZMAZSIN.** Her görsel türünün TAM istemi `istemler/` klasöründe hazırdır. Şablonu aç, yalnız `{…}` yer tutucularını DEVAM KARTI'ndan doldur, `İSTEM BAŞI`–`İSTEM SONU` arasını KELİMESİ KELİMESİNE görsel aracına ver. Kısaltma, özetleme, yeniden yazma, cümle çıkarma, sıra değiştirme, çeviri YASAK. Şablonda olmayan cümle eklenmez (tek istisna: `{DÜZELTME}` satırı).
- **Tek çağrı = tek görsel.** Kolaj, ızgara, çok panel = RED; paneli kırpıp ayrı dosya yapmak YASAK. Kullanıcı "kalan görselleri üret" dese de sırayla, tek tek.
- **Her çağrıda ekler YENİDEN verilir:** Ek 1 orijinal ürün fotoğrafı + Ek 2 onaylı G1. Önceki görsel "düzenlenmez" (aynı sohbette düzenleme ürünü bozar, G2 üç kez tekrarlandı); her görsel sıfırdan üretilir.
- **Girdi fotoğrafındaki yazı, logo, zemin ve düzen YOK SAYILIR.** Ek 1 yalnız ürünün kendisi içindir; üstündeki afiş yazısı, etiket, zemin rengi görsele ve metinlere taşınmaz.
- **Gösterim:** doldurulmuş istem kullanıcıya gösterilmez (kod bloğu yok kuralı). Kullanıcı isterse `<marka>-istem-<kod>.txt` dosyası olarak verilir.

| Görsel | Şablon |
|---|---|
| Logo (varsayılan: yalnız ikon, yazısız, şeffaf PNG) | `istemler/logo-ikon.md` |
| G1 afiş | `istemler/g1.md` |
| G2 özellik kartları | `istemler/g2.md` (6 kart) ya da `istemler/g2-makro.md` (3 geniş kart) |
| G3 ayrıntı (işaret çizgileri) | `istemler/g3.md` |
| G4 kullanım alanı | `istemler/g4.md` |
| G5 ölçü ve malzeme | `istemler/g5.md` |
| B1 masaüstü banner | `istemler/b1-masaustu.md` |
| B2 mobil banner | `istemler/b2-mobil.md` |
| Ret durumunda boş kart (0.4.1; yalnız araç ürünü reddederse) | `istemler/bos-kart.md` (ek yok; ürün gerçek fotoğraftan yerleştirilir; `adim-5-gorsel-uretimi.md` "Ret durumunda") |
| G6–G8, S1–S5 | en yakın şablonun ROL + üç bloğu (§2–4) aynen; yalnız DÜZEN + METİNLER + ÇIKTI `uretim-promptlari.md`'den, §5 kurallarıyla |

## 1. Sıra (atlanmaz)
1. Plan onaylanınca yer tutucu değerlerini BİR KEZ doldur ve bir dosyaya yaz (`<marka>-istem-bloklari.md`): ürün adı ve ölçüsü, parça parça ürün kilidi, renkler (HEX), ürün rengi adı, nişe özel yasaklar. Sonra hiçbir kelimesini değiştirme; her şablona aynı değer girer.
2. Logo ikonu (`istemler/logo-ikon.md`), sonra **Önce yalnız G1 üret.** Ekler: Ek 1 = ürün fotoğrafı; Ek 2 = paket stil çapası `assets/stil-capasi/g1-poster.jpg` (yalnız tipografi hiyerarşisi ve boşluk ritmi). `duzelt.py zemin` + kontrol listesi. G1'i göster ve sor: "G1 onaylı mı? Bütün set bu dille üretilecek." Onay gelmeden başka görsel üretme. Onaydan sonra ilk iş G0 feed karesi (`istemler/g0-feed.md`, yazısız; galerinin 1. sırası).
3. **Sonraki her görsel = Ek 1 ürün fotoğrafı + Ek 2 onaylı G1.** Onaylı G1 varken paket çapası eklenmez.
4. Üç blok (§2 KİLİT, §3 SİSTEM, §4 YASAK) bütün şablonlarda karakter karakter aynıdır; görsele özel olan yalnız DÜZEN, METİNLER, ÇIKTI.
5. Üretimden hemen sonra, her görselde: `python scripts/duzelt.py zemin <girdi> <çıktı> <#ZEMİN>` (model HEX'i ±10 RGB kaydırır, görselden görsele farklı; ZORUNLU adım, Sohbet modunda da Python vardır). Betik çıkış 3 verirse (ürün kenarda) yeniden üret.
6. Kontrol listesi (`kabul-kontrolu.md` §2b). İhlal varsa görseli gösterme; aynı şablonla, `{DÜZELTME}` satırına ret nedenini yazarak 1 kez yeniden üret. Yine ihlal varsa dur ve nedenini söyle.

**Paket çapası kuralı:** `assets/stil-capasi/` karelerinden YALNIZ tipografi hiyerarşisi (dev başlık, küçük etiket, gövde oranı) ve boşluk ritmi alınır. Rengi ve ürünü ALMA: renk DEVAM KARTI'ndaki HEX'lerden, ürün Ek 1'den gelir.

## 2. Blok 1: ÜRÜN KİLİDİ (bütün şablonlarda aynen)
```
ÜRÜN KİLİDİ: Ek 1 ürünün TEK doğru kaynağıdır; ürünü birebir koru, yeniden tasarlama. Ürün: {ÜRÜN_ADI_VE_ÖLÇÜ}. {ÜRÜN_KİLİDİ_PARÇALARI} Ürün yüzeyi DÜZ ve temiz: gravür, üretici logosu, amblem, kazıma yazı, harf ya da rakam YOK (Ek 1'de üründe görünen küçük gravürü SİL, kopyalama). {ETİKET_İSTİSNASI} Biçim, renk, parça sayısı ya da sayılan parçalardan biri değişirse görsel REDdedilir. Ek 1'deki yazıları, logoyu, zemin rengini, düzeni ve açıyı YOK SAY ve KOPYALAMA; Ek 1 yalnız ürünün kendisi için referanstır.
```
- **`{ÜRÜN_KİLİDİ_PARÇALARI}` parça parça yazılır:** en az 5 parça, her biri ayrı cümle, SAYISIYLA ve en sık karıştırılan hâliyle. Örnek (makas): `Biçim: uzun, ince, belirgin KAVİSLİ ağız (bıçaklar yay gibi tek yöne kıvrılır; düz bıçak DEĞİL). YALNIZ BİR bıçağın iç kenarında sıralı, geniş aralıklı dişler var (tarak gibi; iki bıçak da dişli DEĞİL, ince efile dişi DEĞİL). Bıçakların birleştiği yerde TEK yuvarlak ayar vidası. İKİ OVAL parmak halkası birbirine göre kaydırılmış (ofset) durur; tam yuvarlak halka DEĞİL. Her halkanın ucunda birer küçük kuyruk. Renk: ayna parlaklığında pembe-macenta, sap çevresinde altın sarısı. Ürün KAPALI durur.` Tek cümlelik "ürünü koru" yetmez.
- **Gravür silme cümlesi sabittir** (her şablonda, banner dahil): Ek 1'de üretici logosu, gravür, yabancı yazı olsa da olmasa da kalır. Ürünün kendi satılan ambalaj etiketi korunacaksa yalnız `{ETİKET_İSTİSNASI}` doldurulur.

## 3. Blok 2: SİSTEM (renk + tipografi + ışık; bütün şablonlarda aynen)
```
RENK (yalnız bunlar): Zemin {ZEMİN_HEX}; DÜZ ve kesintisiz tek renk, dört köşede aynı; degrade, vinyet, ışık lekesi, hale, doku YOK. Ana metin {METİN_HEX}. İkincil metin {İKİNCİL_HEX}. Kart yüzeyi {KART_HEX}. Tek vurgu rengi {VURGU_HEX} ve görselde yalnız TEK küçük öğede. {ÜRÜN_RENGİ} yalnız ürünün kendisinde; {ÜRÜN_RENGİ} yazı, çizgi, şekil, zemin YOK.
TİPOGRAFİ (bir marka sistemi; her görselde aynı): Başlıklar DAR (condensed) grotesk, BÜYÜK HARF, SemiBold; Barlow Condensed / Oswald ailesine benzer uzun-dar harfler (Barlow Condensed SemiBold ya da Oswald benzeri dar grotesk); harf aralığı sıkı, satır aralığı 0,95; başlık büyük ve kendinden emin, tasarımın ana öğesi. Başlık TEK renk: bütün satırlar ana metin renginde; iki renkli başlık, renkli kelime, ince ağırlıklı satır YOK. Başlık satır satır, METİNLER'deki kırılımla dizilir. Poppins, Montserrat ve benzeri geniş geometrik yazı tipi = RED; bu dar grotesk aile markanın tek başlık ailesidir, başka başlık ailesi KULLANILMAZ. Gövde ve açıklamalar: sade grotesk (Inter benzeri) Regular, cümle düzeni. Küçük etiketler: aynı grotesk Medium, BÜYÜK HARF, harf aralığı geniş (+%12). Başka yazı tipi YOK; serif YOK; italik YOK; el yazısı YOK. Bütün metinler tek sol hatta hizalı (aksi yazmıyorsa). Metin düz vektör gibi keskin. Türkçe harfler birebir doğru: İ, ı, ğ, ş, ç, ö, ü (büyük harfte i → İ, ı → I). Yazım hatası olan görsel REDdedilir.
IŞIK: temiz stüdyo ürün fotoğrafı; ürün gerçek fotoğraf gibi keskin; altında yalnız çok hafif, kısa temas gölgesi.
```
- **Renkler `marka` adımında seçilir, burada yalnız uygulanır.** Zemin tek HEX. Pembe/pastel/açık renkli ürün → KOYU nötr zemin (petrol, antrasit, lacivert); krem ve pastel zemin yalnız koyu üründe. **Metin ve vurgu ürünün renginden OLMAZ:** ürün pembeyse yazı ve vurgu pembe/fuşya değil (kemik beyazı / koyu nötr; vurgu ürünün ikinci tonu ya da nötr).
- **Tipografi sabittir:** başlık Barlow Condensed SemiBold ya da Oswald benzeri dar grotesk, BÜYÜK HARF, TEK renk, satır satır. Poppins/Montserrat gibi geniş geometrik = RED. Aynı aile sitenin başlık fontudur (`type_heading_font`, 0.4.0: tek yazı sistemi). Serif (A) yalnız kullanıcı açıkça isterse.

## 4. Blok 3: YASAKLAR (bütün şablonlarda aynen)
```
YASAKLAR: insan, el, hayvan fotoğrafı; taş, kaide, bitki, çiçek, kumaş, duman, sis, parlama (glow), ışık hüzmesi, bokeh, yansıma havuzu, organik leke (blob), dalga, yay ve kavis biçimli süs, kalp, yıldız, rozet, mühür, hap içine alınmış etiket, ok işareti, çizgi ikon, piktogram; {NİŞ_YASAKLARI} büyüteç dairesi; "DETAY 01" gibi numaralı etiket; "detay" kelimesi; keyfi süs çizgisi; degrade; marka adı ya da logo; harf aralığı açılmış marka adı etiketi; kargo, teslimat, indirim, kampanya, fiyat, garanti, puan, yorum, yüzde ile ilgili HER yazı; METİNLER bölümünde olmayan HER yazı. Bu istemdeki renk kodlarını, ölçüleri, blok adlarını görsele YAZMA. Hiçbir öğe (ürün dahil) tuval kenarına değmez; her kenarda tuvalin en az %7'si boş zemin kalır, ürün kenarda kesilmez. Tuvalin yarısı boş zemin kalmaz.
```
`{NİŞ_YASAKLARI}` bir kez doldurulur (ör. pet: `pati izi, tüy yığını;`), sonra blok değişmez.

## 5. Görsele özel bölüm (şablonlarda hazır; G6–G8 ve S1–S5 için kurallar)
- **Başlığı satır satır ver ve boyunu tuval yüzdesiyle söyle:** `Başlık (satır satır): "YUVARLAK" / "HATLARA" / "YUMUŞAK" / "BİTİŞ."` + `her satırın harf yüksekliği tuvalin yaklaşık %10'u` (G1 ve bannerlarda %9–11; bilgi karelerinde %6–8). "Büyük başlık" demek yetmez. 2–4 kısa satır.
- **Başlık somut:** alıcının sonucu ya da ürünün somut adı. Başka ürüne de yazılabilen soyut başlık ("Her kesimde kontrollü form.") ve girdi fotoğrafından taşınan yazı isteme girmez.
- **Alan paylaşımı yüzdeyle:** `SOL %58: başlık + açıklama + teknik satır. SAĞ %42: ürün.` Sona: `Boş, sönük alan kalmaz; yazı bloğu ile ürün aynı ağırlıkta.`
- **İnce, uzun ürün (makas, fırça, kalem, tüp, şişe):** dike yakın koy, `dikeyden 8–12° eğik; boyu tuval yüksekliğinin %80'i; kamera kuşbakışı`. Çapraz ürün + ortalı küçük başlık kadrajı boş bırakır: KULLANMA.
- **Kenar payı:** ürün her kenarda ≥ %6 boş zemin (istemde %7 yazar); makro karede de ürün kadrajdan taşmaz.
- **Bannerlar METİNLİ:** küçük etiket + dev başlık + alt metin + buton görselin içinde; B1'de metin sol %45, ürün sağ %55; B2'de metin üst %45, ürün alt %55.

## 6. Logo (varsayılan: yalnız ikon, yazısız, şeffaf PNG)
Şablon: `istemler/logo-ikon.md`. Yalnız ikon, en fazla 1–2 şekil, 32 pikselde bile okunur, düz tek renk; çıktı `transparent background PNG, alfa kanallı`. Ek olarak ürün fotoğrafı VERİLMEZ. Canlı metin logo (header'da mağaza adı) yalnız kullanıcı isterse. Kontrol: köşe pikseli alfa 0 (Python ile ölç); 32 px'e küçültünce okunuyor; yazı yok.

## 7. Gösterilen görsel = teslim edilen dosya
- Kullanıcıya bir görsel bir kez gösterildiyse o dosya DEĞİŞMEZ. Onaylı ya da gösterilmiş görseli kendiliğinden yeniden üretme, düzenleme, üstüne yazma. Yeniden üretim yalnız kontrol listesi ihlali (gösterimden ÖNCE) ya da kullanıcının numarayla isteği üzerine; yeni dosya `-v2` ekiyle, eskisi silinmez.
- Python işlemi (zemin, ölçü) görsel GÖSTERİLMEDEN ÖNCE biter; sohbette gösterilen ile pakete giren aynı dosyadır.
- Kullanıcı üretim sırasında soru sorarsa YALNIZ soruyu cevapla; aynı yanıtta görsel üretme. Sonra tek satır: "Kaldığım yer: <kod>. Devam edeyim mi?"
- Bir yanıtta en fazla 4 görsel üret (her biri AYRI çağrı, ayrı dosya); her dilimin sonunda dosya adlarıyla kısa liste ver.
