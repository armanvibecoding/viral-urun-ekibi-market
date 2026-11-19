# Üretim kuralları (ai-video-kreatif: viral referans, hikâye bankası, kare, klip, Flow, görüntü kaynağı)

SKILL.md'den taşındı; içerik aynıdır. Kalıcı kuralların tek kaynağı `ortak/kurallar.md`'dir (kimlikle atıf).

## 1. Viral referans
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

## 2. Hikâye bankası
**Hikâye bankası (Aşama 1 sonu, sahne üretiminden önce):** `is/NN/hikaye-bankasi.md` — en az 10 hikâye/metafor adayı; her satır: tek cümle hikâye ·
izleyicinin kendini gördüğü an · ürünün işlevinin nasıl hissettirileceği (açık ya da imâ: ses/yazı/görüntü) · kaynak
(viral referans satırı ya da gerçek yorum/forum cümlesi) · pazar kültür unsuru · AI riski. Kör jüri ön-üretimde bankadan seçilen
hikâyelerin karelerini puanlar; senaryo yalnız bankadan seçilir. Bir sahne 2 kez yeniden üretilip tutmadıysa 3. üretim
yerine bankaya dön, başka hikâye seç (kredi ve tur israfı ölçüldü: aynı hikâyenin 5 serisi, 4 eleştiri turu).

## 3. Kare ve klip kuralları (en sık hata buradan çıkar)
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

## 4–5. Flow ve kredi (ölçülmüş)
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

## 6. Görüntü kaynağı önceliği
1. İnsan, sıvı, şehir/ofis gibi gerçekçiliği zor sahnelerde önce **gerçek stok video** (ticari lisanslı, atıfsız; lisans `LISANS.md`) ya da kurucunun kendi çekimi.
2. Ürün her zaman **gerçek ürün fotoğrafından** (kesim + hareketli tasarım) ya da ürün sadakati kanıtlı karelerden.
3. AI klip yalnız gerçek görüntünün bulunamadığı, hikâyeye özgü sahnede. Durgun AI fotoğrafı + itme, video yerine geçmez.
4. Her videoda hareketli tasarım katmanı zorunlu: kinetik tipografi (vuruşa oturan, hiyerarşili, vurgu kelimesi renkli), geçiş, ilerleme/sayaç ya da UI öğesi. Uygulandığı yer: `video-kurgu` **Aşama 8b** (HyperFrames becerileri; registry önce aranır). Düz beyaz altyazı kutusu tipografisi kullanılmaz.
