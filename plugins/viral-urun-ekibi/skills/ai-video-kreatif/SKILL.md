---
name: ai-video-kreatif
description: Bir ürün için AI video kreatifi hazırlar — ürünü araştırır, ürün kartı ve kilit metni yazar, 30 senaryo (kanca, şablon, sahneler) üretir, ChatGPT'de başlangıç karelerini, Google Flow'da (Omni, 9:16, 4 sn) klipleri ürettirir. "Bu ürüne video yap", "30 senaryo yaz", "AI video kreatifi", "reels fikri", "başlangıç karesi", "Flow klibi üret", "kanca yaz" isteklerinde çağır. Kurgu, yazı, ses ve teslim için video-kurgu becerisine geçer.
---

# AI video kreatif

Ürün fotoğrafından 30 senaryoya ve ilk örnek videonun kliplerine kadar götürür. Kullanıcıyla dil **Türkçe**;
görsel/video promptları **İngilizce**; ekran yazısı ve CTA **pazarın dilinde** (pazar `.ekip/KARARLAR.md`'den okunur:
Türkiye → Türkçe, yurt dışı → İngilizce). Kullanıcı kod bilmeyebilir; terminal işini sen yaparsın.
Python komutu: macOS/Linux `python3`, Windows `py -3` (Windows'ta `python3` yazmak Microsoft Store'u açar).

## Hafıza protokolü (her aşamada)
- Her ürün `is/NN-urun-adi/` altında. Aşama kaydı `is/NN-urun-adi/DURUM.md`: aşama no (0–9), her videonun
  hangi aşamada olduğu (tablo), onaylı kredi tavanı ve harcanan kredi. Şablon:
  `${CLAUDE_PLUGIN_ROOT}/skills/ekip-lideri/referans/hafiza-sablonlari.md`.
- Her aşama bitince ürün `DURUM.md`'sini ve `.ekip/DURUM.md`'deki "Sıradaki adım"ı güncelle. Kullanıcı karar
  verdiği an (pazar, seçilen senaryo, kredi tavanı, CTA kelimesi) `.ekip/KARARLAR.md`'ye satır ekle.
- Oturum başında ya da "devam" denince önce ürün `DURUM.md`'sini oku, kaldığın aşamadan sürdür; biten aşamayı yeniden yapma.
- Uzun çıktı (kart, senaryo tablosu, prompt) dosyaya; sohbete 5–10 satır özet + dosya yolu.

## Aşamalar (ayrıntı: `${CLAUDE_SKILL_DIR}/referans/asamalar.md`)
| No | Aşama | Bitiş durumu (dosya) |
|---|---|---|
| 0 | Girdi + kapılar | ürün fotoğrafı `referans/` içinde; pazar, kredi tavanı, müzik izni, Flow hakları, Chrome indirme, logo/IP KARARLAR'da |
| 1 | Araştırma + ürün kartı + hikâye bankası | `kart.md` (sektör satırı + mekanizma kartı + işlev cümlesi) + `kilit.txt` + `viral-referans.md` + `hikaye-bankasi.md` |
| 2 | Temiz ürün görselleri | `referans/paket_*.png` + aynı-ürün panosu ve ölçüm tablosu |
| 3 | 30 senaryo | `senaryolar.json` + `senaryolar.md/.csv`, `senaryo_kontrol.py` çıkış 0 |
| 4 | Kare planı + promptlar | ilk 5 videonun `promptlar/VNN_SK_gorsel.txt` ve `_flow.txt` dosyaları |
| 5 | Başlangıç kareleri + ön-üretim eleştirisi | `kareler/VNN_SK.png` (1080×1920), kabul tablosu, `elestiri/ELESTIRI-on-uretim-*.md` GEÇTİ |
| 6 | Flow klipleri | `klipler/VNN_SK.mp4` (720p), harcanan kredi DURUM'da |
| 7–9 | Klip kontrolü, kurgu, teslim | `video-kurgu` becerisi |

**Aşama 0 tek turdur:** kullanıcıya gidecek bütün kapılar (pazar, kredi tavanı, müzik kaynağı izni, Flow "kullanım
hakları" onayı, Chrome çoklu indirme izni, logo/IP) burada tek mesajda sorulur ve KARARLAR.md'ye yazılır; sonrası
sorusuz akar (liste ve istisnalar: `asamalar.md` Aşama 0).

Aşama 1'de kartı **gerçek fotoğraf ve satıcı açıklamasından** yaz (AI görselden değil). Mekanizmanın bilinmeyen kısmını
gösterme; o anı atlayan sahne kur ve `[DOĞRULA]` etiketle. Kilit metni bir kez yazılır, her promptu betik üretir.

**Viral referans (Aşama 1 sonu, atlanamaz; alt ajan izlenme okuyamaz, bu iş liderde):**
1. **TikTok, ≥ 5 sorgu:** ürün adı + rakip marka/model adları + kategori sorguları ("<kategori> accessories you need",
   "<kategori> mod reveal"). `tiktok.com/search/video?q=<sorgu>`. Kart verisi toplanır (ölçülmüş yöntem): sayfada
   `a[href*="/video/"]` öğesinin 4 üst ebeveyninin `innerText`'i okunur; tarih satırından bir önceki değer izlenme,
   sonraki % değer izlenme oranıdır; her sorgunun satırları localStorage'da tek anahtarda biriktirilir (sayfa değişince kaybolmaz).
2. **En az 10 video İZLENİR** (izlenme sırasıyla, sorgulara dağıtarak); oynarken 2 sn'de bir `zoom` karesi.
3. **Meta Reklam Kütüphanesi satırı:** ürünün aktif reklam sayısı + en uzun süredir yayındaki 3 kreatifin kancası ve ilk
   karesi (uzun yayın = kârlı varsayımı ölçülmedi, "deneme" diye yaz).
`is/NN/viral-referans.md`: sorgular, toplanan kart sayısı, izlenen her video için hesap, izlenme, süre, kanca yazısı, plan
sırası, ürünün ekranda/elde nasıl göründüğü, ses; `Meta: N aktif, en uzun M gün` satırı. ≥3 videoda görülen desen
senaryoların iskeleti olur (KANITSIZ SEKTÖR'de senaryoların ≥ %50'si). Referans izlenmeden senaryo ve kare üretilmez.

**Hikâye bankası (Aşama 1 sonu, sahne üretiminden önce; 2026-11-17 kurucu: "sahneyi sürekli yeniden üretmek yerine
önce araştırma/hikâye bankası"):** `is/NN/hikaye-bankasi.md` — en az 10 hikâye/metafor adayı; her satır: tek cümle hikâye ·
izleyicinin kendini gördüğü an · ürünün işlevinin nasıl hissettirileceği (açık ya da imâ: ses/yazı/görüntü) · kaynak
(viral referans satırı ya da gerçek yorum/forum cümlesi) · pazar kültür unsuru · AI riski. Eleştirmen ön-üretimde
bankadan en güçlü 3'ü puanlar; senaryo yalnız bankadan seçilir. Bir sahne 2 kez yeniden üretilip tutmadıysa 3. üretim
yerine bankaya dön, başka hikâye seç (kredi ve tur israfı ölçüldü: aynı hikâyenin 5 serisi, 4 eleştiri turu).

Aşama 3 ağır iştir: `icerik-stratejisti` alt ajanına ver. Brief'te: `is/NN/kart.md`, `kilit.txt`, pazar, CTA kelimesi,
dağılım kuralları (`asamalar.md` §3), çıktı biçimi `${CLAUDE_SKILL_DIR}/referans/senaryo-formati.md`, betik klasörü
`${CLAUDE_SKILL_DIR}/scripts/` (ajan değişkeni bilmez, yolu açık yaz), durma ölçütü "`senaryo_kontrol.py` çıkış 0". Ana oturuma yalnız özet + dosya yolu döner. Sonra betiği **sen de** koştur (ajan çıktısı sınanır).

**Ön-üretim eleştirisi (Aşama 5 sonu, kredi onayından önce):** ilk 5 senaryo ve kareleri `video-elestirmen` ajanına
"ön-üretim" moduyla verilir; eşiği geçmeyen video Flow'a gitmez (eşikler ajan dosyasında).

Örnek video için en güçlü ve AI riski en düşük senaryoyu (mekanizması `[DOĞRULA]` olmayan) seç, gerekçeyi tek satır yaz.

## Betikler (`${CLAUDE_SKILL_DIR}/scripts/`)
- `senaryo_kontrol.py is/NN/senaryolar.json` — sebep→sonuç, tekrar, benzerlik (difflib > 0,8), dağılım, TR kanca kuralları,
  giriş/ortam/özne çeşitliliği; tablo yazar.
- `prompt_uret.py is/NN/senaryolar.json is/NN/kilit.txt --video 1 2 3` — görsel + Flow promptları; kilit sayımı ve
  AUDIO ⊆ ACTION kapısı. Tek promptu panoya: `--kopyala 1 2 flow`.
- `kare_hazirla.py <indirilen.png> is/NN/kareler/V01_S1.png --referans <orijinal>` — 9:16 kırp, 1080×1920, md5 kontrolü.
  `--yan-yana orijinal uretilen pano.jpg --bolge x0,y0,x1,y1` — aynı ürün mü panosu.
- `ekran_tasi.py k2.png k3.png CX CY R k3_hizali.png` — "sonra" karesinin ekran bölgesini "önce" karesine taşır (kadraj sabit).
- `chatgpt_indir.js`, `flow_yukle.js` — Claude in Chrome `javascript_tool` için (kullanım: `referans/flow-ve-chatgpt.md`).
Betik DUR/❌ verirse düzelt ve tekrar koştur; geçmeden sonraki aşamaya geçme.

## Kare ve klip kuralları (en sık hata buradan çıkar)
- Her kare ayrı görsel (kolaj değil), aynı video aynı ChatGPT sohbetinde; sahne 2+ `CONTINUITY LOCK` ile (betik ekler).
- Her kareyi isteğe karşı **ölçerek** kontrol et: ürün parça/renk/yazı, 4 bacak/5 parmak, aynı hayvan, etkileşim noktası
  karede hazır, olmamış olayın izi yok, logo/poster yok. Göz kararı ✅ yazma; ölçüm/pano dosyası yoksa ✅ geçersiz.
  ❌ olanı ORİJİNAL referanstan tek düzeltmeyle yeniden üret, en fazla 2 deneme; tutmazsa sonraki uygun senaryoya geç.
- **Ürün ekranı/ışığı karenin İÇİNDE üretilir** (görsel model hale, cam yansıması ve perspektifi kendisi yapar); klip
  promptunda `SCREEN LOCK` ile sabit tutulur, içerik değişimi **kesimde** olur (aynı kadraj, yeni içerik = önce/sonra).
  Sonradan düz daire bindirme sahte durur (perspektif taşması, yansımasız cam) — yalnız karede üretilemeyen hareket için,
  `video-kurgu` ekran bindirme kurallarıyla. Basit hareket (radar dönmesi) Flow'da istenebilir; 4 fps panoyla sına.
- **Gerçek bağlam:** ürün bir araca/eşyaya takılıyorsa o nesne gerçekçi ve tanınır olmalı (araçta model rozeti, gerçekçi
  plaka + uydurma numara). Boş plaka, logosuz/markasız sahne, plastik yüz AI işaretidir.
- **Kahraman karakter sabit:** hikâyenin kahramanı (hayvan ya da kişi) klip içinde ve klipler arasında tür, desen ya da
  renk değiştirmez. Her klibin ilk/orta/son karesi referans kırpımıyla yan yana konur (`kare_hazirla.py --yan-yana`);
  değişen klip kurguya girmez (kırp ya da tavan içinde yeniden üret).
- **Seri üretim (30 video): videoya değil sahneye klip üret.** Özneye (araç, hayvan, kişi) bağlı sahne yeniden
  kullanılamaz; her özne için ~5 klip: k1 kahraman giriş · k2 önce/stok · k3 sonra (k2 ile AYNI kadraj) · k4 başka açı,
  içerik 2 · k5 geniş kimlik planı. Özneden bağımsız sahneler (telefon dokunuşu, kutu açılışı, elde ürün, söküm/montaj
  makro, konnektör) **ortak klip**tir: 2–3 varyant (farklı el/kılıf/zemin), her biri ≤ 4 videoda, ardışık iki videoda değil.
  Her videoda özne, renk, ortam, giriş türü, kanca ve müzik türü farklı. Giriş türleri: egzoz/ses · söküm makro ·
  concept→result · hikâye POV yazısı · elde ürün/kutu · kapı/örtü reveal · sonuç önce. Plaka/etiket prompta yazılı
  sabitlenir; "dokun → değiş" için başlangıç + bitiş karesi. Örnek tablo: `referans/flow-ve-chatgpt.md` "Seri üretim".
- Ekran içeriği gerçek kullanıcıların koyduğu tarzda olur (viral referanstan): çoğunlukla siyah zemin, sade parlak ikon.
- Kare tipi, kamera, kanca, şablon kararları için: `referans/baslangic-karesi.md`, `sahne-sablonlari.md`,
  `kanca-kutuphanesi.md`, `kreatif-mantigi.md`, `pazar-katmani.md`; yasaklar `kurgu-ve-yasaklar.md` §7; tamamı tek blokta
  `sistem-promptu.md`; gerçek plan çıktısı biçimi `ornek-plan.md`; test/devam-öldür eşikleri `olcum-ve-test-plani.md`.
- Meme formatlı video (seride ≤ %30): `referans/meme-formatlari.md` — meme yalnız yazı/ritim/kavram olarak kendi klibimizle
  kurulur; film/şarkı/kişiye bağlı olan ve başka marka logosu yasak. Kullanmadan önce dosyadaki güncellik kontrolünü
  (§2: KYM son tarih + TikTok son 90 gün) uygula; ölü meme'i yalnız evrensel kalıp olarak kullan.

## Flow ve kredi (ölçülmüş)
- Model **Omni 1.2 Flash**, 9:16, x1, 4 sn, **720p = 12 kredi/klip**. 360p kullanılmaz. Pahalı model ayrı onay ister.
- **Tavan onayı Aşama 0'da bir kez** alınır: "N klip + en fazla R yeniden deneme = toplam en fazla X kredi (720p klip
  başı 12)". Tutarıyla KARARLAR.md'ye yazılır. Tavan içinde tekrar sorma; aşacaksan DUR. Kredi bilgisini her üretimde ekrandan da oku.
- **Tavanı istemeden önce malzeme kapısı:** `python3 "${CLAUDE_SKILL_DIR}/scripts/malzeme_kontrol.py" <video-planı.md|json> --klip N --tavan X`
  (özne başına K ≥ 5+3·(V−2), içerik ≥ V, ortak klip ≤4 video ve ardışık değil, kredi = klip×12×1,15). Çıkış 1 ise tavanı
  bu sayıyla isteme; betiğin bastığı seçenekleri ("N video için X kredi" / "tavanla en çok V video") kullanıcıya sun.
- **Araç/sahne başına klip sayısı video sayısını sınırlar:** 5 klip ≈ en çok 2 ayrışan video (ölçülen: 30'luk seride 3. video her araçta "kopya" diye kaldı). 3 video için ≥ 8 klip planla; ikonun klip içinde biçim/renk değiştirmediğini klip_qc + 8 fps kırpımla kontrol et.
- **Flow sohbetinde TEK kare = TEK klip.** Kareyi "İsteme ekle" ile tek ek olarak koy, tek klip iste. Ölçülen: 4 kareli istek
  ("en yeni 4 yükleme, içerikle eşle" ya da dosya adıyla) 4 klibin 3'ünü YANLIŞ kareden üretti, Flow cevabı doğru kimlikleri
  yazsa bile; tek ekli yöntem 5/5 doğru. Sohbet kutusu en fazla 2 ek tutar. Her klibin ilk karesini kaynak kareyle karşılaştır.
- Klip başına en fazla 3 deneme, her denemede tek değişiklik. İndirilen dosya adı sırayı taşımaz: klibi ilk karesine bakarak eşle.
- Yükleme yöntemi, giriş, kullanım hakları onayı, indirme: `${CLAUDE_SKILL_DIR}/referans/flow-ve-chatgpt.md`.
  Tarayıcı aracı yoksa promptları dosyadan kullanıcıya ver; o üretir, sen klipleri kontrol edersin.
- Klipler inince hemen `video-kurgu` aşama 7: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/video-kurgu/scripts/klip_qc.py" is/NN/klipler/*.mp4 --pano`.

## Sınırlar
- Uydurma yok: ürünün yapmadığını gösterme; sayı, yorum, indirim, stok, fiyat uydurma. Emin değilsen `[DOĞRULA]`.
- **Organik videoda ekranda fiyat yok** (ağır kusur); fiyat caption/bio/ürün sayfasında. Ekran yazısı ürünü listelemez,
  ikna eder (`kanca-kutuphanesi.md` §1b Ekran yazısı). İşlevi açık söylenemeyen ürün: `kurgu-ve-yasaklar.md` §8 İmâ yolu.
- Başka markanın logosu/ürün adı, lisanslı karakter/müzik, ünlü yüzü, sağlık/güvenlik iddiası, sahte otorite yok.
  İstisna: ürün belirli bir markanın aracına/ürününe takılan aksesuarsa (ör. araç amblemi) marka görünürlüğünü kullanıcı
  karar verir; risk ona söylenir ve karar KARARLAR.md'ye yazılır.
- Google/ChatGPT girişinde dur, kullanıcıya devret; şifre isteme, yazma. Ödeme ekranında dur.
- Kullanıcı ChatGPT'de kendi başına yapmak isterse: `${CLAUDE_PLUGIN_ROOT}/ekler/chatgpt/ai-video-kreatif.md`
  (Chrome eklentisi modunda ChatGPT Flow'a dosya yükleyemez; bulut tarayıcısında Google girişi kullanıcıdadır).

## Rapor (aşama sonunda, ≤6 satır)
Ne çıktı (dosya yolu) · kontrol sonucu (sayıyla) · harcanan/onaylı kredi · kalan kusurlar · sıradaki adım · varsa tek soru.

## Görüntü kaynağı önceliği (2026-11-18 kurucu geri bildirimi)
1. İnsan, sıvı, şehir/ofis gibi gerçekçiliği zor sahnelerde önce **gerçek stok video** (ticari lisanslı, atıfsız; lisans `LISANS.md`) ya da kurucunun kendi çekimi.
2. Ürün her zaman **gerçek ürün fotoğrafından** (kesim + hareketli tasarım) ya da ürün sadakati kanıtlı karelerden.
3. AI klip yalnız gerçek görüntünün bulunamadığı, hikâyeye özgü sahnede. Durgun AI fotoğrafı + itme, video yerine geçmez.
4. Her videoda hareketli tasarım katmanı zorunlu: kinetik tipografi (vuruşa oturan, hiyerarşili, vurgu kelimesi renkli), geçiş, ilerleme/sayaç ya da UI öğesi. Uygulandığı yer: `video-kurgu` **Aşama 8b** (HyperFrames becerileri; registry önce aranır). Düz beyaz altyazı kutusu tipografisi kullanılmaz.
