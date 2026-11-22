# Ekip gelişim planı: her rol kendi yolundan (Fable) — 2026-11-19

**Sonuç:** Hiçbir rolün "işi iyi yaptı mı" sorusuna cevap veren bir sonuç ölçümü yok. Ölçülen tek şey ara doğruluk (sayı kaynağından doğru mu, kota doldu mu, süre tuttu mu). Bu yüzden her rol aynı yoldan "öğreniyor": kural ekleyerek. Öneri: her role kendi gerçeklik kaynağını bağlamak (avcıya 30 gün sonraki pazar, savcıya bırakılan ürünler, eleştirmene kurucu hükmü, sese kurucunun kulağı, stratejiste 48. saat paylaşımı, mağazaya sepete ekleme oranı) ve bunların hepsini tek bir hüküm defterinden beslemek.

Bu belge `GELISTIRME-ONERILERI-FABLE.md` üstüne kurulur; oradaki 15 öneri tekrarlanmadı, yalnız atıf yapıldı ("önceki Ö1" gibi).

Kapsam: yalnız okundu. Değişen tek dosya budur. Video izlenmedi, ses dinlenmedi. Sayılar dosyalardan ve veritabanından sayıldı (salt okunur sorgu).

Yol kısaltmaları: **A/** = `plugins/viral-urun-ekibi/` · **B/** = Mağaza Kurucu deposu · **K/** = kurucunun çalışma projesi (ürün avı + video işleri) · **S/** = K/ içindeki yetişkin wellness video serisi klasörü.

---

## 1. Yeni ölçümler (bu belgenin dayanağı)

| # | Ölçüm | Değer | Kaynak |
|---|---|---|---|
| 1 | Karnenin son satırı | 2026-11-08; sonraki 45 eleştiri çağrısı karnede yok; özet tablosu boş | K/`ekip/karne.md:3-4`, `:48` |
| 2 | Kurucunun bir işi KABUL ettiği kayıt | 0 satır. Ret kaydı en az 12 olay | K/`ekip/KARARLAR.md:8,11,17` · A/`ortak/bilgi/dersler.md:86,89,96,97,98,101,102,109,112` · K/`ekip/DERSLER.md:7,54` |
| 3 | Eleştirmenin "kanca" puanı | 45 satırda hep 6–8 (ort. 6,76; sapma 0,74). En az ayırt eden alan; kurucunun en sık ret sebebi | S/ altındaki 8 `puanlar.jsonl` |
| 4 | Eleştirmenin "ikna" puanı | 20 satırda ort. 7,35; kurucu aynı seriye "ikna etmiyor, hook yok" dedi | aynı dosyalar · K/`ekip/KARARLAR.md:11,17` |
| 5 | Aynı videonun iki kez okunduğu kayıt | 0. Okuma tarihi yalnız 3 gün (3–6 Kasım); yayın tarihi 0/628 | K/`veri/analiz.db` `video` tablosu |
| 6 | Aday ürünün sonradan yeniden ölçümü | 0. `ivme.csv` yok; 80 aday 8 Kasım'da değerlendirildi | K/ altında `find` · K/`firsat/aday-degerlendirme-2026-11-08.md` |
| 7 | Kanıt savcısı çıktısı | 0 dosya (`firsat/kanit/` yok), karnede satırı yok | K/`firsat/` · K/`ekip/karne.md` |
| 8 | Müzikte "Kurucu seçti:" satırı | 13 lisans dosyasında 0 | S/ altında grep |
| 9 | Viral video ses verisi | `muzik_turu` 116/116 "bilinmiyor"; derin analiz 0 satır | K/`veri/analiz.db` `video_analiz` |
| 10 | Yayın ölçümü | `olcum.csv` yok; reklam veritabanında 0 reklam (36 sorgu kuyrukta) | K/ altında `find` · K/`is/meta/reklam.db` |

**Madde 2 en önemlisi:** defter yalnız ret biriktiriyor. Ekip "ne yapmamalı"yı 12 kez öğrendi, "kurucu neyi sever"i bir kez bile kaydetmedi. Kural yığınının sebebi bu: ret → yasak → yeni kural.

---

## 2. Viral Ürün Ekibi: rol kartları

### 2.1 Fırsat avcısı (`firsat-avcisi` + iki tarama becerisi)

1. **İyi neyle ölçülür:** 30. gün isabet oranı = önerdiği adaylardan 30 gün sonra hedef pazarda büyüyenlerin payı. Bugün ölçülmüyor. Karne yalnız "3 sayı ürün sayfasıyla aynı mı" diye bakıyor (K/`ekip/karne.md:21,27,32`).
2. **En büyük zayıflık:** doğruluk ölçülüyor, isabet ölçülmüyor. 80 adayın hiçbiri yeniden okunmadı (ölçüm 6). Ayrıca AliExpress alt ajana kapandı (K/`ekip/DERSLER.md:49-52`); rol fiilen liderin tarayıcısından yürüyor.
3. **Gelişim mekanizması: geriye dönük test, iki yönlü.**
   - İleri test: 8 Kasım kaydı t0 sayılır. Açık 20 aday için bugün satış adedi + hedef pazarda aktif reklam sayısı yeniden okunur, `ivme.csv`'ye t0 ve t7 satırı girilir. Betik hazır: A/`skills/aliexpress-firsat/scripts/ivme_olc.py`. Sıklık: her Pazartesi `bekleyen` komutu.
   - Ters test: veritabanındaki 12 VIRAL-URUN ile 15 ZAYIF ürün adı gizlenip karıştırılır; avcının DNA puanı bunları ayırabiliyor mu? Ayıramıyorsa `viral-dna.md` ölçütleri yeniden ağırlıklanır. Uyarı: DNA bu ürünlerin bir kısmından türetildi; adil sınama için yeni toplanan ürünler gerekir (tahmin: ilk sonuç iyimser çıkar).
4. **Altın set:** 12 VIRAL-URUN + 15 ZAYIF (K/`veri/analiz.db` `v_viral_urun`) + 2 ders ürünü (mekanizması doğrulanmadan seçilen, büyük perakendede doymuş çıkan: A/`ortak/bilgi/firsat-gecmisi.md` özet tablosu). Hedef 50 + 50; kaynağı reklam veritabanı dolunca `kazanan_puan.py` etiketleri.
5. **Model:** tarama Sonnet (hacimli, kalıp). Puanlama betik. Haftalık geri test yorumu için tek Opus çağrısı.
6. **İlk 2 hafta:** (S) 20 açık adayı `ivme.csv`'ye gir, t7'yi oku. (M) `dna_geri_test.py`: gizli etiketle sıralama + ilk 10 isabeti.

### 2.2 Kanıt savcısı (`kanit-savcisi`)

1. **İyi neyle ölçülür:** SAT kararının 30 gün sonra ayakta kalma oranı (ürün bırakılmadı, harcanan kredi çöpe gitmedi). Bugün ölçülmüyor; rol bu projede hiç dosya üretmemiş (ölçüm 7).
2. **En büyük zayıflık:** en pahalı hata savcı devrede değilken yapıldı. Mekanizması doğrulanmamış ürüne 30 video, yaklaşık 1.200 kredi harcandı (K/`ekip/DERSLER.md:54-56`). SAT sonuçları yalnız düz yazı tablo.
3. **Gelişim mekanizması: ölüm sonrası dosyası.** Bırakılan her ürün için tek satır: "7 kontrolden hangisi bunu yakalardı?" (kontroller: A/`agents/kanit-savcisi.md:23-30`). Madde başına isabet sayılır; hiç yakalamayan kontrol sadeleşir, kaçıran kontrol sıkılaşır. Ek: geçmiş ürünler savcıya sonucu gizlenerek verilir (kör yeniden yargılama).
4. **Altın set:** üretime alınan 4 ürün (sonuçları belli) + 21 veto kararı + avcının ileri testinden çıkacak "ELE dendi ama büyüdü" ürünleri. Küçük set; ayda 2–3 ürün eklenir.
5. **Model:** Opus; yalnız son 3 adayda Fable. Para kararı, çağrı sayısı az.
6. **İlk 2 hafta:** (S) 4 geçmiş ürünle kör koşu, doğrulanmamış mekanizmayı yakalıyor mu? (S) kanıt şablonuna `sonuc_30gun` alanı.

### 2.3 Kreatif analisti (`kreatif-analisti`)

1. **İyi neyle ölçülür:** tutan desen oranı = ayrı tutulmuş videolarda yönü doğru çıkan desenlerin payı. Bugün ölçülmüyor; ölçülen şey desenin kaç notta geçtiği (A/`agents/kreatif-analisti.md:23`).
2. **En büyük zayıflık:** yalnız kazananlara bakıyor. Sıklık etki değildir: aynı kalıbın kopyaları 2–12 beğenide kaldı, kazanan oranı %2–8 (K/`ekip/DERSLER.md:18-19`). 116 analiz satırının 35'inde kanca türü "bilinmiyor".
3. **Gelişim mekanizması: aynı hesapta kazanan–kaybeden farkı.** Hesap başına ≥1 milyon izlenen video ile medyan altı video eşlenir; desen kazananda kaç kat sık? Veri: `v_video` görünümü (`izlenme_takipci`; 189 videoda hesaplanabilir). Reklam tarafında betik var (A/`skills/reklam-kutuphanesi-avi/scripts/desen_say.py`); organik için tek SQL yeter. Sıklık: her 100 yeni analiz satırında.
4. **Altın set:** 4 hesap × (5 kazanan + 10 kaybeden) = 60 video, derin katmanda analiz. Canlı izlenen ~210 video bu hesaplardan (K/`ekip/DERSLER.md:19`).
5. **Model:** Sonnet + SQL. Sayım model işi değil. Desen yorumu ayda bir Fable.
6. **İlk 2 hafta:** (S) mevcut 81 kodlu videoda kanca kodu × medyan izlenme/takipçi tablosu (n küçük, "deneme" etiketiyle). (M) 60'lık eşli set.

### 2.4 İçerik stratejisti (`icerik-stratejisti`)

1. **İyi neyle ölçülür:** yayınlanan videoda 48. saat paylaşım/izlenme oranı, kanca ailesi başına. Eşik hazır: %0,61 (A/`skills/ekip-lideri/scripts/yayin_olc.py` başlık yorumu). Bugün ölçülmüyor (ölçüm 10).
2. **En büyük zayıflık:** kapısı kota sayıyor, fikir kalitesini saymıyor (≥8 mekanizma, ≥6 şablon: A/`agents/icerik-stratejisti.md:33`). Kurucunun hükmü: "fikirler sıkıcı", "hook yok", "olay ne, anlamadım" (K/`ekip/KARARLAR.md:8,17` · A/`ortak/bilgi/dersler.md:109`). Model alanı boş (A/`agents/icerik-stratejisti.md:1-5`).
3. **Gelişim mekanizması, iki kademe.**
   - Yayın öncesi (bugün yapılabilir): kör kanca turnuvası. 10 kanca + ilk kare tarifi, veritabanındaki gerçek viral kancalarla (116 satırda `kanca_metni` dolu) adsız karıştırılır. Jüri "hangileri bizim" diye ayırabiliyorsa kanca zayıftır. Kalan 5'ten kurucu 2 seçer; seçim hüküm defterine gider.
   - Yayın sonrası: `PLAN.md`'deki kanca ailesi etiketi × `olcum.csv`. Betik ortalamayı zaten basıyor; eksik olan çıktının kanca kütüphanesine ağırlık olarak geri yazılması.
4. **Altın set:** 116 gerçek viral kanca (pozitif) + kurucunun reddettiği hikâyeler (negatif) + kurucunun el yazısı fikir notları (S/ altında 7 fotoğraf ve dökümü; şu an tek pozitif zevk örneği).
5. **Model:** hikâye bankası ve ilk 5 seçimi Fable; 30 senaryonun yazımı Sonnet.
6. **İlk 2 hafta:** (S) bir üründe kör kanca turnuvası. (S) `PLAN.md` şablonunda kanca ailesi sütununu zorunlu yap.

### 2.5 Video eleştirmeni (`video-elestirmen`)

1. **İyi neyle ölçülür:** kurucu hükmüyle uyum oranı; en kritik parça "GEÇTİ dedi, kurucu reddetti" sayısı. Bugün ölçülmüyor; kayıtta kurucu alanı yok (önceki Ö2).
2. **En büyük zayıflık:** kurucunun en çok önem verdiği iki alanda puan ayırt etmiyor (ölçüm 3 ve 4). Teslimde 24 satırın 10'u GEÇTİ; hükmü kayıtlı tek GEÇTİ videosu kurucu tarafından reddedildi (K/`ekip/KARARLAR.md:11`).
3. **Gelişim mekanizması: alan bazında ayırt edicilik testi.** Kalibrasyon seti (önceki Ö1, Ö2) kurulduktan sonra her alan için: kurucunun KABUL ve RET videolarında puan farkı var mı? Farkı sıfır olan alan cetvelden çıkar ya da yeniden yazılır. Sıklık: cetvel her değiştiğinde ve ayda bir.
4. **Altın set:** 20 video. Kurucunun hüküm verdiği en az 8 kendi videomuz + aynı nişten 12 gerçek viral. İlk sınav sorusu: jüri bizimkini virallerden ayırabiliyor mu?
5. **Model:** kör jüri Fable × 3 kopya; mekanik kontrol betik.
6. **İlk 2 hafta:** (S) geçmiş 12 ret olayını hüküm defterine gir. (M) 20'lik setle ilk uyum oranını yaz.

### 2.6 Ses tasarımcısı (`ses-tasarimcisi`)

1. **İyi neyle ölçülür:** kurucunun ilk dinlemede kabul ettiği miks oranı. Bugün ölçülmüyor (ölçüm 8).
2. **En büyük zayıflık:** rol dinleyemiyor (A/`agents/ses-tasarimcisi.md:11`); ölçüm doğru ama zevki ölçmüyor. Eleştirmenin ödüllendirdiği ani açılışı kurucu "kötü, bir anda açılıyor" diye reddetti (A/`ortak/bilgi/dersler.md:101`). Dinletme adımı kurucuyu bekliyor; cevap gelmeyince varsayılanla gidildi (K/`ekip/KARARLAR.md:16`).
3. **Gelişim mekanizması: kurucunun kulağından referans kütüphanesi.** Kurucunun seçtiği ve reddettiği her parça ölçülüp `ses/referans.tsv`'ye yazılır: tempo, ses yüksekliği, bas oranı, vokal var mı, giriş rampası süresi. Yeni adaylar bu profile uzaklığa göre sıralanır. Kurucuya 3 tam parça yerine 2 adet 10 saniyelik kesit gider; cevap tek kelime. Betik: A/`skills/video-kurgu/scripts/ses_olc.py`'ye `--parmak_izi` seçeneği.
4. **Altın set:** 15 parça = kurucunun reddettikleri + bir dinleme turunda seçeceği 5 + nişin 5 viral videosunun sesi (bu veri şu an yok: ölçüm 9).
5. **Model:** Sonnet. İş ölçüm okuyup komut üretmek; yargı kurucuda ve betik eşiklerinde.
6. **İlk 2 hafta:** (S) 6 kesitlik dinleme paketi, kurucunun 5 dakikası. (S) parmak izi seçeneği.

### 2.7 Kurgu ve hareketli tasarım (`video-kurgu` + HyperFrames becerileri; ajan dosyası yok)

1. **İyi neyle ölçülür:** kör jürinin "yapay görünüyor mu" sorusunda "hayır" oranı. Ara ölçüm: mekanik kapıdan ilk seferde geçme. Bugün ölçülmüyor.
2. **En büyük zayıflık:** kurucu hükmü "animasyon yok, tipografi kötü" (K/`ekip/KARARLAR.md:17`). Yön stok görüntü + kinetik tipografiye çevrildi ama beğenilen bir örnek henüz kayıtlı değil.
3. **Gelişim mekanizması: stil kartı.** Kurucunun beğendiği 10 hareketli tasarım klibinden ölçülen değerler (yazı ailesi, harf boyu/ekran oranı, giriş süresi, kesim aralığı) tek sayfaya yazılır; kurgu bu kartı okur, kural listesini değil. Yazı ailesi mağaza paketinden gelir (önceki Ö13).
4. **Altın set:** 10 referans klip (kurucu seçer) + kendi reddedilen 3 videomuz.
5. **Model:** uygulama Sonnet; stil kartının ilk yazımı Fable, bir kez.
6. **İlk 2 hafta:** (S) kurucudan 10 klip bağlantısı. (M) stil kartı + bir pilot video.

### 2.8 Ekip lideri (`ekip-lideri`)

1. **İyi neyle ölçülür:** kurucuya giden teslimin ilk seferde kabul oranı. Yan ölçüm: aynı geri bildirimin ikinci kez gelme sayısı (hedef 0).
2. **En büyük zayıflık:** karne elle tutuluyor ve 10 gün önce durdu (ölçüm 1). Kapılar yazıda (önceki Ö6).
3. **Gelişim mekanizması:** karneyi betik üretsin (bölüm 6). Lider yalnız "sonraki deneme" sütununu yazar.
4. **Altın set:** gerekmez; girdisi diğer rollerin defterleri.
5. **Model:** oturum modeli (kurucu kararı: lider en güçlü model, K/`ekip/KARARLAR.md:18`).
6. **İlk 2 hafta:** (S) `karne_uret.py`.

---

## 3. Mağaza Kurucu: küme kartları (25 rol, 5 küme)

Ortak durum: kör denemede ürün sayfası ilk ekranı 5,57 → 6,86 (B/`docs/EKIP-v2.md:9`). Gerçek satış ya da dönüşüm verisi hiçbir yerde yok; 0.4.0 gerçek koşuda denenmedi (B/`docs/EKIP-v2.md:106,122`).

| Küme | Roller | Sonuç metriği | Bugün | Kendine özgü mekanizma | Model |
|---|---|---|---|---|---|
| **M1 Jüri ve yönetim** | kor-elestirmen, tasarim-direktoru, seri-tutarlilik-denetcisi, gorsel-qa | Kör panoda bizim karenin sırası (1–4) | Tek deneme ölçüldü | Ekipteki en olgun döngü; eksiği kurucu hükmüyle kalibrasyon. Görev tanımlı (B/`.claude/agents/kor-elestirmen.md:29`), çıktısı depoda yok (doğrulanamadı) | Fable × 3 · yazım kontrolü Haiku |
| **M2 Marka ve yön** | marka-stratejisti, kreatif-direktor, nis-stil-mimari, referans-kuratoru, tipografi-sistemcisi, tasarim-dili, logo × 2 | Kurucunun 3 yönden seçtiğinin ilk turda onaylanması | Ölçülmüyor | İkili tercih defteri: "A yönü seçildi, B ve C elendi". Seçim puandan güvenilir veridir. Gerilim kayıtlı: kurucunun dili başarılı markaların ~%2'sinde (B/`docs/EKIP-v2.md:18,56`); bunu ancak satış verisi çözer | Fable (yön) · Opus (tipografi) |
| **M3 Üretim** | metin-yazari, prompt-muhendisi, gorsel-uretici, urun-kilidi-analisti | İlk üretimde kapıdan geçen görsel oranı | Kısmen (boş kart 8 denemede 1 temiz, B/`docs/EKIP-v2.md:135`) | İstem bloğu defteri: blok × geçti/kaldı. 20 üretimde hiç geçmeyen blok atılır | Opus (istem) · Sonnet (üretim) |
| **M4 Site denetçileri** | cro-ux-denetcisi, hiz-muhendisi, seo-aio-uzmani, erisilebilirlik-denetcisi, marka-sesi-denetcisi, site-bolum-mimari | Sepete ekleme oranı (oturum → sepet) | Ölçülmüyor; hız verisi yalnız laboratuvar (B/`docs/EKIP-v2.md:125`) | Denetim skoru ↔ gerçek davranış: her düzeltme tarihli; önceki ve sonraki 14 gün karşılaştırılır. Video bazında kaynak için UTM hazır (B/`src/ortak/arayuz-sozlesmesi.md:34`) | Sonnet + betik |
| **M5 Platform ve bakım** | platform-uyum-muhendisi, benchmark-kosucusu, kutuphane-bakimci | Gerçek koşuda uçtan uca tamamlanan adım oranı | 0.4.0 için koşu yok | Sürüm başına bir gerçek koşu, adım adım geçti/kaldı tablosu | Opus (koşu) · Sonnet (bakım) |

**M4 için dürüst sınır:** yeni mağazada sipariş sayısı düşük olur; dönüşüm oranıyla karşılaştırma haftalarca "veri yok" döner (tahmin). Bu yüzden metrik sepete ekleme oranı seçildi: aynı trafikte daha erken sinyal verir. Sipariş ancak yeterli hacim birikince eklenir.

**Altın set (küme başına):**
1. M1: kurucunun geçmişte hüküm verdiği 20 kare.
2. M2: seçilen ve elenen yön çiftleri, ilk 10 karar.
3. M3: geçen ve kalan 40 üretim, istemiyle birlikte.
4. M4: her denetim maddesi için bir "önce/sonra" ekran çifti.
5. M5: sürüm başına bir koşu kaydı.

**İlk 2 hafta:** (S) M2 ikili tercih defterini aç, geçmiş seçimleri gir. (M) 0.4.0 için bir gerçek koşu. (S) mağaza analitiğinden haftalık üç sayı: oturum, sepete ekleme, sipariş.

---

## 4. Roller arası geri besleme haritası

Okunuşu: "kaynak → öğrenen: hangi veriyle".

1. **Pazar (30. gün ölçümü) → Fırsat avcısı:** hangi adaylar büyüdü. → **Kanıt savcısı:** ELE dediği büyüdü mü, SAT dediği ayakta mı.
2. **Kanıt savcısı (bırakılan ürün dosyası) → Fırsat avcısı:** hangi eleyici en çok aday düşürüyor; avcı o tür adayı baştan getirmez.
3. **Kreatif analisti (kazanan–kaybeden farkı) → İçerik stratejisti:** hangi kanca ailesine ağırlık. → **Fırsat avcısı:** hangi mekanizma kodları gerçekten taşıyor.
4. **Yayın ölçümü (48. saat) → Stratejist, Eleştirmen, Ses:** kanca ailesi sonucu; eleştirmenin hangi alan puanı sonucu öngördü; hangi ses profili tuttu.
5. **Hüküm defteri (kurucu) → Kör jüri, Stratejist, Ses, Kurgu, M2:** kabul ve ret örnekleri (bölüm 5).
6. **Mağaza analitiği (sepete ekleme) → M4 denetçileri ve Teklif:** hangi düzeltme davranışı değiştirdi.
7. **Mağaza paketi → Kurgu:** yazı ailesi, renk, onaylı iddialar (önceki Ö13).

Bugün bu yedi oktan çalışan: yok. 1, 4 ve 6'nın betikleri hazır (`ivme_olc.py`, `yayin_olc.py`, UTM alanı), verisi girilmemiş.

---

## 5. Kurucunun zevkini öğrenme sistemi: tek hüküm defteri

**Sorun:** kurucunun her hükmü düz yazıya, oradan kurala dönüşüyor. 12 ret kaydı var, 0 kabul kaydı (ölçüm 2). Kuraldan zevk öğrenilmez; örnekten öğrenilir.

**Dosya:** `.ekip/hukum.jsonl`, satır başına bir karar. Tek yazan betik: `hukum_yaz.py`.

| Alan | İçerik |
|---|---|
| `tarih`, `tur` | video · kare · muzik · senaryo · urun · gorsel · sayfa · yon |
| `kimlik` | dosya yolu + içerik özetinin ilk 8 hanesi (dosya değişirse hüküm eskisine yapışmasın) |
| `hukum` | KABUL · RET · SECILDI · ELENDI |
| `karsi` | birlikte gösterilen diğer adayların kimlikleri (seçim satırlarında) |
| `etiket` | en çok 3, sabit sözlükten |
| `soz` | kurucunun cümlesi, aynen |
| `rol` | bu çıktıyı üreten roller |

**Etiket sözlüğü kurucunun kendi kelimelerinden** (K/`ekip/KARARLAR.md:8,11,17` · A/`ortak/bilgi/dersler.md:89,96-98,109`): `fake` · `hook-yok` · `sikici` · `anlasilmadi` · `muzik` · `tipografi` · `hareket-yok` · `tekrar` · `cok-hizli` · `ikna-etmiyor`. Yeni etiket ancak aynı söz ikinci kez gelince eklenir.

**Kurucu için kural: form yok.**
1. Kurucu her zamanki gibi serbest yazar.
2. Lider satırı ve etiketleri çıkarır, tek satırla teyit ister ("3 etiket: fake, hook-yok, tipografi. Doğru mu?").
3. Mümkün olan her yerde puan değil seçim sorulur: "A mı B mi?" Tek kelimelik cevap, en güvenilir veri.

**Pozitif örnek açığını kapatmak (en acil iş):**
1. Kurucu Instagram'da beğendiği 20 videoyu kaydeder ya da bağlantısını atar (10 dakika). Beğeni aracı projede zaten var (K/`begen`).
2. Her biri `KABUL` + tek kelime neden olarak deftere girer.
3. Kurucunun el yazısı fikir notları (S/ altında 7 fotoğraf) `senaryo · KABUL` olarak girilir.

**Besleme (kim, nasıl okur):**
1. **Kör jüri:** talimatına kural değil, defterden 6 çift örnek girer (3 KABUL, 3 RET, kareleriyle). Talimat bir sayfa kalır.
2. **Üreticiler (stratejist, ses, kurgu, M2):** işe başlarken "zevk kartı" okur: son 5 KABUL + son 5 RET, her biri tek satır. Betik üretir, en çok 1 sayfa.
3. **Eleştirmen kalibrasyonu:** defterdeki video satırları altın settir; uyum oranı karneye yazılır.
4. **Kural terfisi:** bir etiket 2 farklı üründe görülmeden eklenti kuralı olmaz (önceki Ö5).

**Sınır:** 20 satırın altında defter istatistik değil, örnek kümesidir. "Kurucunun zevkini öğrendi" iddiası ancak jüri, görmediği 10 hükmün en az 8'ini tutturunca yazılır (eşik öneridir, ölçülmedi).

---

## 6. Haftalık ekip karnesi

Betik üretir (`karne_uret.py`): `hukum.jsonl`, `puanlar.jsonl`, `ivme.csv`, `olcum.csv` ve mağaza analitiğinden okur. Veri yoksa hücreye "veri yok" yazar, sayı uydurmaz. Lider yalnız son sütunu doldurur. Rol başına bir satır, toplam bir ekran.

| Rol | Sonuç metriği | Bu hafta | Değişim | Örnek sayısı | Sonraki tek deneme |
|---|---|---|---|---|---|
| Fırsat avcısı | 30. gün isabet | veri yok | — | 0 / 20 aday yeniden okundu | 20 adayın t7 okuması |
| Kanıt savcısı | SAT ayakta kalma | veri yok | — | 0 kanıt dosyası | 4 geçmiş ürünle kör koşu |
| Kreatif analisti | Tutan desen oranı | veri yok | — | 81 kodlu video | Kanca kodu × izlenme tablosu |
| İçerik stratejisti | 48. saat paylaşım/izlenme | veri yok | — | 0 yayın | Kör kanca turnuvası |
| Eleştirmen / jüri | Kurucuyla uyum | veri yok | — | 1 kayıtlı eşleşme (uyumsuz) | 12 geçmiş hükmü deftere gir |
| Ses | İlk dinlemede kabul | veri yok | — | 0 seçim | 6 kesitlik dinleme paketi |
| Kurgu | "Yapay mı" → hayır oranı | veri yok | — | 0 | 10 referans klip |
| Lider | İlk seferde kabul | 0 / 3 (wellness serisi) | — | 3 teslim | Karne betiği |
| Mağaza (M1–M5) | Sepete ekleme oranı | veri yok | — | 0 hafta | Haftalık 3 sayı |

Yukarıdaki satırlar bugünün gerçek durumudur; tablo aynı zamanda başlangıç karnesidir. Kural: bir satır 3 hafta üst üste "veri yok" kalırsa o rolün gelişim işi durur ve kurucuya tek soru gider (veri mi gelecek, rol mü kapanacak).

---

## 7. Kaldırılması ya da birleştirilmesi gerekenler

1. **`video-elestirmen` → ikiye bölünür** (mekanik betik + kör jüri). Önceki Ö1; yeni kanıt ölçüm 3 ve 4.
2. **`teklif-ve-sayfa` ↔ Mağaza Kurucu'nun metin ve bölüm rolleri → tek sayfa hattı.** İkisi de ürün sayfası metni yazıyor (A/`skills/teklif-ve-sayfa/SKILL.md:9-10` · B/`docs/EKIP-v2.md:90-91`). Öneri: teklif araştırması A'da kalır, sayfa yazımı B'ye geçer, arada mağaza paketi.
3. **`kreatif-analisti` → kalıcı ajan olmaktan çıkar.** Sayım betiğe, yorum ayda bir tek çağrıya iner. Karnedeki son çağrısı 7 Kasım (K/`ekip/karne.md:35`).
4. **Fırsat avcısı ve kanıt savcısının yerel "-mcp" kopyaları → kaldırılır.** Asıl dosyalarda bağlayıcı satırı zaten var (A/`agents/firsat-avcisi.md:37`, A/`agents/kanit-savcisi.md:32`); iki kopya iki ayrı kural kaynağıdır.
5. **Mağaza Kurucu'da üç birleştirme adayı (tahmin; kullanım sıklığı kaydı olmadığı için kesin değil):** logo-arastirmaci + logo-tasarimci · referans-kuratoru + kutuphane-bakimci · hiz + erisilebilirlik + seo denetçileri → tek denetim betiği + bir yorumcu. Beş rolde model alanı boş.

Kaldırılmaması gereken: kanıt savcısı. Hiç çalışmamış görünmesi rolün gereksizliğini değil, atlandığını gösteriyor; en pahalı hata tam onun kontrol ettiği noktada oldu.

---

## 8. İlk iki hafta (sıralı, toplam 5 iş)

1. **Hüküm defteri + geçmiş 12 ret + kurucudan 20 beğeni** (S). Diğer her şeyin girdisi.
2. **Karne betiği** (S). Başlangıç karnesi bölüm 6'daki tablo.
3. **Avcı ileri testi:** 20 adayın t7 okuması (S). İlk gerçek isabet sayısı.
4. **Ses dinleme paketi + kör kanca turnuvası** (S + S). Kurucunun toplam 15 dakikası.
5. **Jüri kalibrasyonu:** 20'lik altın setle ilk uyum oranı (M).

Kurucudan istenen toplam zaman (tahmin): ilk hafta 30 dakika, sonra haftada 15 dakika.

---

## 9. Doğrulanmayanlar ve varsayımlar

1. "Kurucunun kabul kaydı 0" yalnız karar ve ders dosyalarına dayanır; sözlü ya da başka oturumda verilmiş onay olabilir.
2. Veritabanındaki `liste_karari` (AL 352, YEDEK 147, ELE 1) kimin kararı, kayıttan anlaşılmıyor; kurucununsa hazır bir pozitif zevk kaynağıdır. Sorulmalı.
3. Ters geri testin adil olup olmadığı (DNA ölçütlerinin aynı ürünlerden türetilmesi) sınanmadı.
4. Mağaza Kurucu'nun kalibrasyon ve kör deneme çıktıları depoda değil; yalnız özet belgedeki sayılar okundu.
5. Model önerileri işin türüne göredir; fiyat ve çağrı maliyeti ölçülmedi.
6. Bölüm 7 madde 5 ve bölüm 3'teki M4 sınırı tahmindir.
7. Bu belgedeki mekanizmaların hiçbiri denenmedi; "işe yarar" iddiası yok, yalnız "ölçülebilir hale getirir" iddiası var.
