# Geliştirme önerileri (bağımsız inceleme, Fable) — 2026-11-18

**Sonuç:** Ekip kural yazmayı öğrenmiş, kurucunun zevkini öğrenmemiş. Son seride 12 teslim eleştirisinin 0'ı geçti, puan 5,0–6,5 bandında dönüp durdu, aynı 18 saatte tek üründen 46 kalıcı kural çıktı. En büyük kazanç yeni kural değil: eleştirmeni ikiye bölmek, kapıları zorlayıcı yapmak ve kural terfisini yavaşlatmak.

Kapsam: yalnız okundu, hiçbir dosya değiştirilmedi (bu dosya dışında). Video izlenmedi, ekibin betikleri koşturulmadı (yalnız bu dosya için anonimlik kontrolü koştu: temiz); bütün sayılar dosyalardan sayıldı. `docs/BIRLESME-ANALIZI.md` inceleme bittikten sonra oluştu; yalnız özeti (§0) okundu, çelişki görülmedi. Öneri 13 oradaki 4. maddeyle aynı bulguya dayanır; taşıma planı ve anonimlik engeli o belgededir, burada tekrarlanmadı.

Yol kısaltmaları: **A/** = `plugins/viral-urun-ekibi/` · **B/** = Mağaza Kurucu deposu · **P/** = kurucunun video projesindeki `v6-uclu/` klasörü (yetişkin wellness serisi, A–B–C videoları).

---

## 1. Beş soruya kısa cevap

1. **Kendini geliştirme döngüsü öğreniyor mu?** Hayır, biriktiriyor. Kural ekleniyor (17 Kasım'dan beri +225 / −28 satır) ama kuralın işe yaradığı hiçbir yerde ölçülmüyor; pazar verisi (`olcum.csv`) hiç girilmemiş.
2. **Eleştirmen sert ve ölçülebilir mi?** Sert, ama yanlış şeyi ölçüyor. Kontrat ayrıntısında titiz (1,85 sn süre eksiği), kurucunun asıl ret sebebinde kör (kurucu "hook yok" dediği videoya kanca 6, ikna 8 vermiş).
3. **Talimat bütçesi şişmiş mi?** Evet. Şartname ≤ 120 satır ve ≤ 40 talimat diyor; üç ana beceri 126–146 satır ve satırlar uzatılarak 1.340–1.860 kelimeye çıkmış. Eleştirmen işe başlamadan yaklaşık 9.000 kelime kural okuyor.
4. **ChatGPT tasarımı?** B'ninki ölçülmüş ve sıkı (≤ 5.120 bayt, tek yönlendirici, testli). A'nınki otomatik çeviri: beceri başına 6–17 KB, temel varsayımı "doğrulanmadı" diye işaretli.
5. **Güçlü model nerede değer?** Az sayıda, yüksek kaldıraçlı yargıda: kör zevk jürisi, hikâye seçimi, kök neden kararı, kural budama. Tarama, ölçüm ve komut üretiminde gereksiz.

---

## 2. Ölçülen tablo (önerilerin dayanağı)

| Ölçüm | Değer | Kaynak |
|---|---|---|
| Teslim eleştirisi geçen / toplam | 0 / 12 (hepsi 5,0–6,5) | P/`{A,B,C}/elestiri/puanlar.jsonl` |
| Ön-üretimde geçip teslimde kalan | A: 7,5 → 5,5 ve 6,0 · B: 7,0 → 5,0–6,0 | aynı dosyalar |
| Ön-üretimde KALDI alıp yine üretilen | C (gerçekçilik 6 < 7, `gecti: false`) → 24 kredi harcandı | P/`C/elestiri/ELESTIRI-onuretim-C-tur2.md:4`, P/`C/DURUM.md` kredi defteri |
| 18 saatte kalıcı reçete | 46 (tek ürün, 3 video) | `puanlar.jsonl` `recete` alanı |
| Aynı kuralın yazıldığı dosya | müzik girişi (−30 dB): 10 dosya, 26 kez · organikte fiyat: 17 dosya | A/ altında grep |

---

## 3. Öneriler (etkiye göre sıralı, 15 madde)

### Grup 1 — Eleştirmen (en yüksek etki)

**1. Eleştirmeni ikiye böl: mekanik kapı betiği + kör zevk jürisi.** Maliyet: M
- Sorun: tek ajan hem kontrat uyumunu hem zevki ölçüyor; dikkatinin çoğu ölçülebilir ayrıntıya gidiyor.
- Kanıt: son turda düşüren sebepler "süre 18,75 > 18,0", "pil %15 → %30", "kauçuk halka" (P/`B/elestiri/ELESTIRI-teslim-B-v2-tur2.md:5`); kurucunun sebebi "fake, AI slop, animasyon yok, tipografi kötü, hook yok" (A/`ortak/bilgi/dersler.md:112`). Aynı videoda kanca 6, ikna 8.
- Değişiklik: (a) süre, LUFS, yazı konumu, kelime sayısı gibi her ölçülebilir madde `kurgu_kontrol.py`'ye; ajan bunları puanlamaz. (b) Zevk için B'deki `kor-elestirmen` deseni: bitmiş video + aynı kategoriden 3 gerçek viral referans (`viral-referans.md`'den) adsız yan yana, 3 bağımsız kopya, medyan. Jüri kontratı, üretici notunu ve önceki puanı görmez (B/`.claude/agents/kor-elestirmen.md:7-9`).
- Etki: jüri kurucunun sorduğu soruyu sorar ("hangisi sahte duruyor, hangisinde dururdum"); kural sayısı 9.000 kelimeden bir sayfaya iner.

**2. Kurucu hükmünü veri yap, eleştirmeni ona karşı sına.** Maliyet: S–M
- Sorun: kurucu reddi düz yazı olarak derse dönüşüyor; eleştirmenin kurucuyla ne sıklıkta uyuştuğu bilinmiyor.
- Kanıt: `puan_kaydet.py` kaydında kurucu alanı yok (A/`skills/video-kurgu/scripts/puan_kaydet.py:99-102`); kalibrasyon tek satır elle eklenmiş (A/`skills/video-kurgu/referans/puan-cetveli.md:118`).
- Değişiklik: `puanlar.jsonl`'a `kurucu: KABUL|RET` + en çok 3 etiket. Kurucunun hüküm verdiği videolar "altın set" olur; cetvel ya da jüri talimatı her değiştiğinde altın set yeniden puanlanır, uyum oranı yazılır. Uyum düşerse değişiklik geri alınır.
- Etki: "eleştirmen daha iyi oldu mu" sorusu ilk kez sayıyla cevaplanır.

**3. Eleştirmeni bağımsız tut: önceki puanı ve kendi imzaladığı kontratı okumasın.** Maliyet: S
- Sorun: aynı ajan kontratı yazıyor, sonra o kontrata göre yargılıyor; her turda önce eski puanını okuyor.
- Kanıt: A/`agents/video-elestirmen.md:39` (kontratı imzalar), `:47` (önce `puanlar.jsonl` satırını oku).
- Değişiklik: tur karşılaştırmasını betik yapsın (zaten Δ hesaplıyor); ajan kör puanlasın, fark sonradan gösterilsin.
- Etki: çapalanma azalır; turlar arası sabit kalan puan gerçek sabitlik olur.

**4. Alan düzeyinde oynamayı kapıya bağla, öğrenme betiklerine kırma testi yaz.** Maliyet: S
- Sorun: gerekçe yalnız toplam 1,5'ten fazla oynarsa isteniyor; alan 2–3 puan oynayınca geçiyor.
- Kanıt: B-ANA ritim 5 → 3 ve B-GÜVENLİ gerçekçilik 5 → 7 gerekçe alanı boş kaydedilmiş (A'da ritim 3 → 6 gerekçeliydi, ama gönüllü); kural A/`skills/video-kurgu/scripts/puan_kaydet.py:94`. `kendini_test.py` içinde `puan_kaydet` ve `geri_bildirim_kontrol` geçmiyor.
- Değişiklik: herhangi bir alanda |Δ| ≥ 2 ise gerekçe zorunlu; iki betik için kırma testi.
- Etki: ekibin kendi kuralı ("kırılmayan kapı yeşil sayılmaz") öğrenme döngüsüne de uygulanır.

### Grup 2 — Öğrenme döngüsü

**5. Kural terfisini iki basamaklı yap; tek örnekten eklenti kuralı çıkmasın.** Maliyet: M
- Sorun: her geri bildirim ve her kalıcı reçete aynı turda eklentiye işleniyor.
- Kanıt: A/`skills/ekip-lideri/SKILL.md:99` ("aynı turda eklentiye işle"). Sonuç: genel beceride tek ürünün kuralları — plaka, rozet, "telefon karosu = araç ekranı" (A/`skills/video-kurgu/SKILL.md:89-97`), genel cetvelde "plaka tüm planlarda aynı" (A/`skills/video-kurgu/referans/puan-cetveli.md:64`). B bunu yasaklamış: "yalnız 2+ görselde doğrulanan kural; tek örnekten kural çıkarma" (B/`.claude/agents/tasarim-direktoru.md:26`).
- Değişiklik: yeni kural önce ürün kontratına (`is/NN/kurgu/KURALLAR.md`) ya da `.ekip/DERSLER.md`'ye girer. Eklentiye terfi koşulu: ikinci bir üründe ya da 2+ videoda yeniden görülmesi + kapsam etiketi (sektör, pazar, format).
- Etki: kural artışı yavaşlar; herkese açık eklentiye tek markanın özel kuralları sızmaz.

**6. Kapıları yazıdan betiğe taşı; aşım yalnız kurucu kararıyla.** Maliyet: S
- Sorun: üç kapı da metinde "geçmeden gitmez" diyor, pratikte geçilmeden gidilmiş.
- Kanıt: (a) C ön-üretimde KALDI, üretim yapıldı. (b) 0/12 teslim geçti, üç video teslim klasöründe (P/`TESLIM-UCLU/`). (c) Geri bildirim kapısı defter yokken yeşil dönüyor (A/`skills/ekip-lideri/scripts/geri_bildirim_kontrol.py:26-28`); projede defter yok, 46 kalıcı reçete var.
- Değişiklik: tek `kapi.py`: Flow öncesi son ön-üretim satırı `gecti: true` değilse çıkış 1; teslim klasörüne kopyalamayı betik yapar; `puanlar.jsonl`'da KALICI varken defter yoksa çıkış 1. Aşım: KARARLAR'da tarihli `kapi-asimi` satırı (kurucunun cümlesiyle).
- Etki: "kaldı ama gitti" durumu ya engellenir ya da kayıtlı bir kurucu kararı olur.

**7. Tur sayısını sınırla, kök neden sınıfı ve tek değişkenli emir getir.** Maliyet: S–M
- Sorun: her turda 5–10 düzeltme birden yapılıyor, yeni kusur doğuyor, puan yakınsamıyor.
- Kanıt: C dört turda 5,5 → 6,5 → 5,5 → 5,5; B-v2 6,0 → 5,5, raporda "düzeltme yeni kusur getirdi" (P/`B/elestiri/ELESTIRI-teslim-B-v2-tur2.md:17`). B'deki kural: en çok 3 tur, iki tur üst üste artış < 0,3 ise dur ve "tavan" yaz; kök neden tek sınıf (B/`.claude/agents/tasarim-direktoru.md:16-25`).
- Değişiklik: aynı kuralı videoya uyarla. Sınıflar: kurgu · kare · hikâye · malzeme · tavan. "Hikâye" ya da "malzeme" çıkarsa kurgu turu açılmaz, hikâye bankasına dönülür.
- Etki: 12 eleştiri turunun yaklaşık yarısı açılmazdı (tahmin; ölçülmedi).

**8. Krediden önce kredisiz animatik; zevk jürisi onu puanlasın.** Maliyet: M
- Sorun: ön-üretim kapısı teslim sonucunu öngörmüyor; senaryo ve durgun kare puanlanıyor, ritim ve ses yok.
- Kanıt: A 7,5 → 5,5; B 7,0 → 5,5. Ön-üretim 6 sn klip varsaydı, gerçek 4,03 sn çıktı (A/`ortak/bilgi/dersler.md:111`).
- Değişiklik: kareler + yazı zamanlaması + seçilen müzikle kaba kurgu (ffmpeg ya da HyperFrames, 0 kredi). Kör jüri bunu referanslarla karşılaştırır; geçerse kredi tavanı istenir.
- Etki: süre, ritim, tipografi ve müzik kusurları kredi harcanmadan görünür.

**9. Pazar verisini döngüye bağla.** Maliyet: S (betik), veri kurucudan
- Sorun: öğrenmenin tek kaynağı eleştirmen ve kurucunun gözü; izlenme ve paylaşım hiç girmemiş.
- Kanıt: proje ağacında `olcum.csv` yok; `yayin_olc.py` eleştirmen puanlarını okumuyor (içinde `puanlar` geçmiyor).
- Değişiklik: `yayin_olc.py --puanlar` ile video bazında birleştir; "alan puanı ↔ 48. saat paylaşım/izlenme" tablosu. 10 ölçülmüş videodan sonra hangi alanın sonucu öngördüğü yazılır.
- Etki: cetvel zevke değil sonuca göre ayarlanır. Veri gelene kadar bu madde boş kalır; dürüst durum budur.

### Grup 3 — Talimat bütçesi

**10. Satır sınırını bayt sınırına çevir, derleme kapısına bağla.** Maliyet: M
- Sorun: şartname kendi sınırını tutmuyor; satır sınırı uzun satırla aşılıyor.
- Kanıt: `docs/SARTNAME.md:17` (≤ 120 satır, ≤ 40 talimat), `:60` ("tarih içeren kural yazma"). Gerçek: `video-kurgu` 146 satır / 1.840 kelime, `ai-video-kreatif` 143 / 1.856, `ekip-lideri` 126 / 1.341; cetvelde 9, yasaklar dosyasında 9 tarihli kural. B'de sınır betikte: `SKILL_MAX_BAYT = 5120` (B/`tools/build.py:34`), beş becerinin hepsi altında.
- Değişiklik: birleşik eklentide B'nin `build.py --check` düzeni; SKILL.md ≤ 5 KB, referans ≥ 10 KB uyarı.
- Etki: bütçe aşımı derlemede yakalanır, elle sayılmaz.

**11. Ürüne özgü kuralları sektör eklerine taşı; her kural tek yerde yaşasın.** Maliyet: M
- Sorun: aynı kural çok dosyada; değiştirmek için 10 dosya düzenlemek gerekiyor, biri unutulunca çelişki doğuyor.
- Kanıt: bölüm 2 tablosu (10 ve 17 dosya). Ekip bunun bedelini bir kez ödemiş: eski cümle silinmediği için ajan çelişkiyi eskisinden okudu (A/`skills/ekip-lideri/SKILL.md:99-101`).
- Değişiklik: `referans/sektor/arac-aksesuar.md`, `referans/sektor/hassas-kategori.md`; çekirdek dosyalar sektörsüz. Kural kimliği (ör. `SES-01`) tek kaynakta, diğer dosyalar yalnız kimliğe atıf yapar. Betiğe çevrilen kuralın metni tek satıra iner.
- Etki: eleştirmenin okuma yükü ürüne göre yarıdan aza iner (tahmin).

**12. Kural defteri ve aylık budama.** Maliyet: S başlangıç, sonra tur başına S
- Sorun: kurallar yalnız ekleniyor; hangisinin hâlâ işe yaradığı bilinmiyor.
- Kanıt: +225 / −28 satır; liderin öz denetim listesi tasarım gereği sınırsız büyüyor (A/`skills/ekip-lideri/SKILL.md:77`). B aynı sorunu yaşayıp çözmüş: 43 KB kural defteri çalışma zamanından çıkarıldı, çekirdek ≤ 8 KB (B/`docs/ESKIDI.md:42`).
- Değişiklik: `docs/KURAL-DEFTERI.tsv` (kimlik · kaynak · kapsam · kapı var mı · son tetiklenme). Ayda bir güçlü modelle budama: 30 gün tetiklenmeyen ya da kapıya çevrilmiş kural metinden çıkar, `ESKIDI.md`'ye yazılır.
- Etki: bütçe sabit kalır; silinen kuralın izi kaybolmaz.

### Grup 4 — Birleşme ve ChatGPT

**13. Dosya sözleşmesini iki yönde uygula.** Maliyet: M
- Sorun: B sözleşmeyi yazmış, A tarafında karşılığı yok.
- Kanıt: B/`docs/EKIP-v2.md:128` ("öbür plugin'lerde henüz uygulanmadı"); alanlar B/`src/ortak/arayuz-sozlesmesi.md:5-34`.
- Değişiklik: `aliexpress-firsat` SAT kararında `urun-paketi.json` yazar; `video-kurgu` Aşama 8b `magaza-paketi.json`'dan yazı ailesini, renkleri ve yalnız `onayli_metinler.iddialar` listesini okur.
- Etki: kurucunun "tipografi kötü" şikâyeti mağazayla aynı yazı sistemi kullanılarak kökten ele alınır; uydurma iddia kapısı tek listeye bağlanır.

**14. ChatGPT sürümünü çeviriyle değil tek kaynaktan derle; önce gerçek koşuyla sına.** Maliyet: M–L
- Sorun: A'nın paketi metin dönüştürme ile üretiliyor; beceriler büyük, temel varsayım sınanmamış.
- Kanıt: çıktı SKILL.md'leri 6–17 KB (`dist/chatgpt/…/skills/*/SKILL.md`); her birine 1,9–3,1 KB aynı not ekleniyor (13 dosya); "kod yorumlayıcının paket dosyalarını görüp görmediği doğrulanmadı" (`docs/chatgpt_paketi_yap.sh:105`). Altı rol becerisi aynı sohbette uygulanıyor, yani "üretici kendini puanlamaz" kuralı (A/`skills/ekip-lideri/SKILL.md:73`) ChatGPT'de tutmuyor.
- Değişiklik: B deseni — tek yönlendirici + aşama dosyaları, ortak not tek dosyada. Roller aşama içine girer. Eleştiri ayrı yeni sohbette yapılır: kullanıcıya "kör eleştiri kartı" (video + referanslar + bir sayfa talimat) verilir. Yayından önce bir ürünle uçtan uca ChatGPT koşusu.
- Etki: iki yüzeyde aynı davranış; "doğrulanmadı" satırları kapanır.

**15. Birleşmeden önce iki çelişkiyi kurucu çözsün, oturum kancasını sustur.** Maliyet: S
- Sorun: iki eklentinin iddia politikası zıt; kanca ilgisiz projelerde de konuşuyor.
- Kanıt: A sağlık/sonuç iddiasını yasaklıyor (A/`ortak/bilgi/dersler.md:76`); B "hukuk danışmanın sorumluluğu, eklenti engellemez" diyor (B/`docs/ESKIDI.md:15`). Kanca `.ekip/` yokken de üç satır basıyor: çıkış satırı 9'da, yazdırma 6–8'de (A/`hooks/durum-yukle.sh:6-9`). ADHD kuralları iki ayrı metin (A/`ortak/adhd-kurallari.md`, B/`src/ortak/00-calisma-tarzi.md:6-36`).
- Değişiklik: tek iddia politikası (kurucu kararı, KARARLAR'a); kancada `.ekip/` kontrolü en başa; mesaj biçimi tek dosya.
- Etki: birleşik eklenti kendi içinde çelişmez; diğer projelerde bağlam kirlenmez.

---

## 4. Kaldırılmalı

1. **Genel becerilerdeki ürüne özgü maddeler** — A/`skills/video-kurgu/SKILL.md:89-97` (plaka, rozet, telefon karosu), cetveldeki amblem çapaları (`puan-cetveli.md:106-117`). Sektör ekine taşınır (öneri 11).
2. **Tarihli anlatı cümleleri kural dosyalarından** — "2026-11-17 kurucu: …" türü 30'dan fazla satır. Kural kalır, hikâyesi `dersler.md`'de durur (şartname zaten yasaklıyor).
3. **Commit edilmiş kopyalar** — A/`ekler/proje-paketi/yuklenecek/` altındaki 5 bilgi dosyası `ortak/bilgi/` ile bayt bayt aynı (2.107 satır). Derlemede üretilsin, depoda durmasın.
4. **ChatGPT paketindeki 6 rol becerisi** — aynı sohbette rol değiştirmek bağımsızlık sağlamıyor; aşama içine alınır (öneri 14).
5. **Eleştirmenin "önce eski puanını oku" talimatı** — A/`agents/video-elestirmen.md:47` (öneri 3).

Ayrıca değerlendirilecek (kesin "kaldır" değil):
- **Gömülü HyperFrames paketi** (4 beceri, 222 dosya, yaklaşık 3,7 MB; henüz commit edilmemiş). CLI kendi becerilerini kurabiliyor (`--skip-skills` bayrağı bunun için var, A/`skills/video-kurgu/SKILL.md:118`). Gömmek sürümü sabitler ama güncelleme ve imza bakımını size bırakır. Öneri: gömme yerine kurulum kontrolünde sürüm sabitleme; karar kurucunun.
- **B'deki 25 geliştirme rolü**: çalışma zamanına girmiyor, zararı yok. Birleşik depoda A'nın 6 çalışma zamanı ajanıyla aynı klasöre konmasın (`.claude/agents/` geliştirme, `agents/` çalışma zamanı ayrımı korunmalı).
- **`README` içindeki elle sayılar**: bilgi rehberi "68 ders" diyor (A/`ortak/bilgi/README.md:27`), dosyada 85 numaralı ders var.

---

## 5. Model seçimi

Fiyat bu incelemede ölçülmedi; tablo işin türüne ve çağrı sayısına göre. Son seride eleştirmen 18 kez çağrıldı; kör jüri 3 kopya çalışır, bu yüzden tur sınırı (öneri 7) ile birlikte uygulanmalı.

| Rol | Şimdi | Öneri | Gerekçe |
|---|---|---|---|
| Kör zevk jürisi (yeni; ön-üretim animatiği ve teslim) | opus (tek eleştirmen) | **fable**, 3 kopya | Kurucunun zevkini öngörmek en zor ve en pahalı hata; B aynı işte fable kullanıyor |
| Kök neden / dur-devam kararı (yeni) | lider yapıyor | **fable**, tur başına 1 çağrı | Tek çağrı bir sonraki 3–4 turu belirliyor |
| Hikâye bankası + ilk 5 senaryo seçimi | belirtilmemiş (`icerik-stratejisti`) | **fable** (seçim), sonnet (30 senaryonun yazımı) | "Hook yok, sıkıcı" kusuru burada doğuyor; 30 satır üretim kalıp işi |
| Kanıt savcısı (SAT kararı) | opus | opus; yalnız kısa listeye fable | Para kararı; aday başına değil, son 3 adayda güçlü model |
| Kural budama, birleşik plan, sözleşme tasarımı | — | **fable**, ayda bir / sürüm başına | Seyrek, geniş bağlam, yanlışı pahalı |
| Ses tasarımcısı | opus | sonnet | İş ölçüm okuyup komut üretmek; yargı betik eşiklerinde |
| Kreatif analisti (desen sayımı) | opus | sonnet + sayımı betik yapsın | Sayma işi model işi değil |
| Fırsat avcısı (tarama) | sonnet | sonnet | Hacimli, kalıp |
| Mekanik uyum kontrolü, OCR/yazım | opus eleştirmenin içinde | betik; gerekiyorsa haiku | Deterministik; modelle yapmak hem pahalı hem tutarsız |
| Ekip lideri (ana oturum) | oturum modeli | oturum modeli | Yönlendirme ve hafıza; ağır yargıyı alt ajana verir |

---

## 6. Doğrulanmayanlar ve varsayımlar

1. Kurucunun 18 Kasım'daki "hook yok" geri bildirimini B'nin ilk teslim sürümüne verdiği, KARARLAR satırının tarihinden ve sırasından çıkarıldı; hangi dosyayı izlediği kayıtlı değil.
2. Eleştirmen o videoları da KALDI saymıştı. Yani hüküm kurucuyla aynı, sebep farklı; "eleştirmen yanlış geçirdi" iddiası yalnız 17 Kasım'daki 7,0 GEÇTİ videosu için kayıtlı.
3. "Tur sayısı yarıya iner" ve "okuma yükü yarıdan aza iner" tahmindir.
4. Kör jürinin videoda işe yarayacağı B'deki görsel sonuçlarından (5,57 → 6,86) aktarılmış bir beklentidir; videoda denenmedi.
5. ChatGPT davranışına dair hiçbir şey bu incelemede çalıştırılmadı.

---

## 7. İlk üç adım

1. Öneri 6: `kapi.py` + kırma testi (yarım gün; mevcut verilerle hemen sınanır: C'nin ön-üretim satırı çıkış 1 vermeli).
2. Öneri 1 ve 2: mevcut üç teslim videosu + kurucunun hükümleriyle kör jüri denemesi; uyum oranını yaz.
3. Öneri 5: `ekip-lideri` §5b madde 2'yi "önce ürün kontratına, terfi 2. örnekte" diye değiştir; bugünkü 46 reçeteyi bu kurala göre ayır.
