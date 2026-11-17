---
name: video-kurgu
description: AI klipleri (Flow/Omni ya da çekim) ffmpeg ile kurgular — klip kalite kontrolü (sıçrama ölçümü + 4 fps pano), kırpma, ekran içeriği bindirme, ekran üstü kanca/CTA yazısı, efekt ve −14 LUFS ses, kontrol karesi, caption ve teslim paketi. "Klipleri kurgula", "videoyu birleştir", "yazı ekle", "ses ekle", "klipleri kontrol et", "kurgu yap", "teslim et", "final videoyu çıkar" isteklerinde çağır.
---

# Video kurgu

Klipten teslim edilebilir MP4'e: 1080×1920, 30 fps, H.264 + AAC, +faststart, 8–15 sn. Kullanıcıyla dil **Türkçe**;
ekran yazısı ve CTA **pazarın dilinde** (`.ekip/KARARLAR.md`'deki son `| pazar |` satırı; betik kendisi okur).
Betikler `${CLAUDE_SKILL_DIR}/scripts/` altında; Python komutu: macOS/Linux `python3`, Windows `py -3` (Windows'ta `python3` yazmak Microsoft Store'u açar).
Gereken: Python 3.8+, Pillow, ffmpeg (PATH ya da `imageio-ffmpeg` paketi). Kurulum: `${CLAUDE_SKILL_DIR}/referans/kurulum.md`.
İlk kullanımda öz-testi koştur (kredi harcamaz): `python3 "${CLAUDE_SKILL_DIR}/scripts/kendini_test.py" --klasor kurgu_testi`
→ son satırlar GEÇTİ ve `ara_kare_10sn.png`'de Türkçe harfler doğru olmalı.

## Hafıza protokolü
- Aşama kaydı `is/NN-urun-adi/DURUM.md`: aşama 7 (klip kontrolü), 8 (kurgu), 9 (teslim); video başına QC/Kurgu/Teslim
  sütunları. Her video bitince güncelle; `.ekip/DURUM.md` "Sıradaki adım"ı yaz.
- Kırpma kararları, `qc_izin` istisnaları ve gerekçeleri `is/NN/kurgu/VNN.json` içinde kalır (ayar dosyası = kayıt).
- Tekrarlanan klip hatası (aynı kök sebep ikinci kez) `.ekip/DERSLER.md`'ye bir satır.
- Oturum kesilirse: DURUM'daki ilk "—" hücresinden devam; var olan `kurgu/VNN.mp4` yeniden üretilmez.

## Aşama 7 — Klip kontrolü (kurgudan ÖNCE, atlanamaz)
```
python3 "${CLAUDE_SKILL_DIR}/scripts/klip_qc.py" is/NN/klipler/V01_S*.mp4 --pano
```
- Çıkış 1 = sıçrama (ışınlanma, nesne kaybı, gizli kesme) ya da yükseklik < 1280 (720p altı) → kurguya geçme.
- Ölçüm yavaş dönüşümü yakalamaz: her klibin `_qc.jpg` panosunu (saniyede 4 kare) **her karesiyle** aç ve bak:
  ürün kendi kendine çalışıyor/büyüyor/renk değiştiriyor mu · sonuç yanlış yerden ya da el/patiden çıkıyor mu ·
  hayvan/kişi cins, renk, yüz değiştiriyor mu · fazladan uzuv · ürün yazısı bozuluyor mu. 4 fps altına inme.
- Hata klibin başında/sonundaysa → kırp (ayar dosyasında saniye aralığı). Ortadaysa → kök sebebi (kare / prompt /
  AUDIO satırı) yaz, `ai-video-kreatif` aşama 6'ya dön (kredi tavanı içinde). "Yeterince iyi" yok.
- Ölçüm işaretledi ama panoda doğal hareket görüyorsan (hızlı kafa çevirme) plan numarasını `qc_izin`'e ekle ve gerekçeyi yaz.

## Ekran / yazı içeren ürünler (istisna, kurgudan önce)
Ekran içeriği karede üretilir, değişim kesimdedir (`ai-video-kreatif` "Kare ve klip kuralları"). Bindirme yalnız karede
üretilemeyen hareketli içerik içindir ve elips/perspektif, cam yansıması, kumlanma eşlemesi ister:
`ekran_bindir.py klip --kareler` ile ilk/son kareyi çıkar, ekran merkezini ve iç genişliğini ölç, sonra
`ekran_bindir.py klip anim.mp4 cikti.mp4 --x0 --y0 --d0 [--x1 --y1 --d1]`. Ardından çıktıya tekrar `klip_qc.py --pano`:
her karede bindirme ekranın içinde mi. Yöntem ve ayarlar: `${CLAUDE_SKILL_DIR}/referans/ekran-bindirme.md`.

## Aşama 8 — Kurgu
1. `is/NN/kurgu/VNN.json` ayar dosyasını yaz (alanlar `kurgu.py` başındaki açıklamada ve `referans/kurgu-kurallari.md`).
2. Koştur: `python3 "${CLAUDE_SKILL_DIR}/scripts/kurgu.py" is/NN/kurgu/VNN.json --proje .`
   Betik kapıları kendisi uygular (720p altı, sıçrama); geçmezse kurgu yapılmaz.
3. Çıktı satırını oku: süre 8–15 sn, 1080×1920, −14 ±1 LUFS. Değilse düzelt.
4. `VNN_kontrol.jpg`'ye bak (her planın ortası + son kare): yazı okunuyor mu, ürünü/çıkış noktasını örtüyor mu,
   CTA son ≥ 3 sn'de ve kancanın hemen altında mı. Örtüyorsa `yazi_konum` ya da `kanca_gizle` ile yeniden koştur.
**Viral (hızlı) kurgu — varsayılan reklam kurgusu:** `hizli_kurgu.py ayar.json` (alanlar betiğin başında).
- Kanca = videonun **en güçlü anı ilk karede** (alev, değişim, sonuç); olayın ortasından aç, ilk karede ses de olsun.
  Ölü/kapalı ürünle ya da sessiz açma. Kanca yazısı ilk karede tam görünür (kelime kelime değil).
- Planlar müziğin vuruşuna oturur: plan = 2 ya da 4 vuruş (140 BPM'de 0,857 / 1,714 sn), **2 vuruştan kısa plan yok**
  (0,43 sn'lik montaj "çok hızlı" bulundu); toplam 12–15 sn.
- Yazılar planlara değil zaman çizelgesine bağlanır (`yazilar`: bas/bit sn): bir yazı birkaç kesim boyunca kalır.
  Ekranda en az 0,5 sn + kelime başına 0,25 sn (betik uyarır); en fazla 5 kelime, CTA ikinci satırı ≤ 5 kelime.
  "Önce/sonra" geçişi beyaz flaşla, yakın plan girişleri zoom punch ile. Son plan ilk plana bağlanır (döngü).
- Yazı: platformun yerli görünümü — **TikTok Sans Bold** (OFL, Google Fonts `ofl/tiktoksans`), cümle düzeni
  (büyük harf değil), 96–104 px, ince kontur (`kontur_oran` 0,06) + yumuşak gölge, cümlede tek vurgu kelimesi renkli.
  Montserrat ExtraBold büyük harf "reklam gibi" bulunup beğenilmedi. Konum plan başına: ürünü örtmez; alt %20 ve sağ %15 boş.
- "Polisten sakla" gibi yasa dışı kullanımı ima eden yazı yok.
- Çok sahneli videoda isteğe bağlı satış iskeleti (GÖZLEM, tek ürün): `referans/noropazarlama.md`. Tek sahne ve yazısız videolar iskeletsiz.
- Kontrol/uygulama planı neden-sonuç gösterir: önceki hal → dokunuş → sonuç; dokunuş öncesinde sonucun izi olan kesit
  kullanılmaz, kırpım sonucu kadraj dışında bırakmaz. Dokunuşa ve sonuca ses: `ses_tasarla.py --sfx tik@sn,vurus@sn`.
- **Ön-kontrol kapısı (kurgudan sonra, eleştirmenden önce):** `hizli_kurgu.py ayar.json --katı` (okunma UYARI'sı = çıkış 1),
  sonra `kurgu_kontrol.py ayar.json --video VIDEO.mp4` → çıkış 0 olmadan eleştirmene gönderme. Klip içerikleri
  `klipler/klip_etiket.json`dan okunur (biçim betiğin başında; yeni klip = yeni etiket satırı, bilinmeyen "bilinmiyor").
  Betik ölçülebilir kuralları alır; kanca gücü, gerçekçilik, ritim yargısı eleştirmende kalır.
- Teslimden önce `video-elestirmen` ajanı (soğuk izleyici, teslim modu) videoyu puanlar; ≥ 7/10 olmadan teslim yok.

Kurallar (ayrıntı `referans/kurgu-kurallari.md`):
- Kanca beyaz kalın, siyah konturlu, 1–3 satır; konum "oto" en boş bandı seçer (alt %20 ve sağ %15 hariç).
- Emoji videoya girmez (betik çıkarır, uyarır) → caption'a taşı. Türkçe büyük harfi elle yaz; kodda `upper()` kullanma.
- Font: betik Türkçe harfleri (çğıİöşü) ölçerek seçer; ilk kurulumda font test karesine bak.
- Ses: klibin gerçek sesi + sentetik efekt: `ses_tasarla.py --sfx tik@sn,vurus@sn` (tık = dokunuş, vuruş = değişim);
  **efekt dosyası istenmez.** Kullanıcı kendi efektini verirse `sfx` + `hizala: true` gerçek ses anına oturtur. Hedef −14 LUFS.
- **Ses tasarımcısı (ses_tasarla'dan önce):** `ses-tasarimcisi` ajanı ayar dosyasından efekt planı (sn · efekt · dB · neden)
  çıkarır ve komutu üretir: dosya efekti `--sfx_dosya "ad.mp3@sn:dB" --sfx_klasor is/NN/sfx/kaynak` (lisans `sfx/LISANS.md`'de),
  sentetik `boom/whoosh`, drop reçetesi `--riser <drop−0,2>:1.0:-18 --sessizlik_vurusu 0.2`. Kapılar: 10 sn'de ≤ 5 efekt,
  `drop_tuttu`, **müzik girişi** (açılış diegetik ses; müzik 0. sn'de −30 dB'den 1,5–2 sn rampa; kısık yatak + drop'ta tam müzik YASAK — ağır kusur).
  Önce/sonra `ses_olc.py VIDEO --drop sn --muzik_stem <stem>/muz.wav --kapi`. Yöntem: `referans/ses-tasarimi.md`.
- **Elle miks betiği** (ses_tasarla dışı) yazılırsa müzik stem'i ayrı wav olarak kaydedilir ve aynı kapıdan geçer.
- **Drop karışımda ölçülür:** müzik dosyasındaki drop yetmez; klip sesi (rölanti, söküm) drop'u bastırır. `ses_tasarla.py`
  drop'tan önceki 1,7 sn'de klip sesini `--drop_oncesi_db` (varsayılan −8) kadar kısar ve drop anındaki artışı ölçer;
  < `--drop_esik_db` (6 dB) ise `hedef_tuttu: false`. Geçmezse −12/−16 dene ya da drop öncesi planların `ses_db`'sini kıs.
- **Yazı ürünü/plakayı kapatmaz:** yakın planda (kirp ≥ 1,3 ya da rozet/plaka kadrajın alt yarısında) yazı konumu ≤ 0,15.
  Panoda her yazının altında plaka rakamı ya da ürün ekranı varsa düzelt.
- **Telefon karosu = araç ekranı:** telefonda dokunulan içerik, sonraki her planda araç ekranında aynı içerik olarak kalır;
  aracın içerikleri arasında yoksa telefon planı kullanılmaz. Ekranda dokunuş yoksa `tik` sesi yok.
- **Ürün ilk 0,9 sn'de görünür** (2. tur eleştiri: geçen videoların hepsi değişmiş ekranı ilk karede ya da < 0,9 sn'de gösterdi;
  durağan stok plan en fazla 0,86 sn ve ilk plan değil). Söküm klibi sökülen rozetin logosunu göstermiyorsa söküm kancası kullanılmaz.
- **İlk 1,7 sn kancayı görüntüyle kanıtlar:** durağan stok geniş plan ile açma. Ya sonuç önce (değişmiş ekran yakın), ya
  rozete punch (kirp ≥ 1,4), ya söküm/kutu eylemi. Ortak klipteki ikon/araç rengi bu araçla uyuşmuyorsa ≤ 0,9 sn ve ilk
  plan olmaz. Kancadaki nesne ("star", "pump", "walk over") görüntüde yoksa kanca değişir.
- **Müzik videoda olmalı** (müziksiz teslim yok). Kaynak (Aşama 0'da izni alınmış): kullanıcının dosyası ya da Pixabay.
  Pixabay (ölçülmüş): arama sayfasını `fetch` et (`pixabay.com/music/search/<tür>/`) → ilk parça sayfasını `fetch` et →
  içindeki `cdn.pixabay.com/download/audio/...mp3` bağlantısını al → `curl -L -o is/NN/muzik/<ad>.mp3 <bağlantı>`.
  Parça adı, sanatçı, sayfa linki ve lisans notu (Content ID riski) teslim raporuna. Telifli şarkı indirilmez; yayında
  platformun kendi ses kütüphanesinden eklenebilir. Drop'u ölç (0,1 sn enerji sıçraması) ve "önce/sonra" kesimine hizala.
- Ana ses anı (egzoz, tık, patlama) müziğin üstüne çıkar: `ses_tasarla.py` (sidechain ile müziği o anda kısar,
  bas + doygunluk + mekân yankısı; tepe −1 dBTP). Abartı gerçekçiliği bozmamalı: clipping yok.
- Toplam 10–15 sn; tek sahne şablonunda kesme yok; son kare ilk kareye bağlanabiliyorsa döngü kur.

## Aşama 9 — Teslim
`is/NN/teslim/` altına: MP4 + kontrol karesi + caption metni (+ istenirse kareler, klipler, senaryo tablosu .zip).
Caption, hashtag, AI etiketi, DM otomasyonu, 48. saat ölçüm eşikleri: `${CLAUDE_SKILL_DIR}/referans/teslim.md`.
Teslim raporu: yeniden üretilen/kırpılan klipler (saniyesiyle), harcanan kredi, kalan kusurlar, varsayımlar.
Sesi dinleyemediysen bunu açıkça yaz.

## Sınırlar
- Kontrol etmediğin klibi "temiz" ilan etme; "bitti" = dosya + ölçüm satırı + kontrol karesine bakıldı.
- Başka markanın logosu, lisanslı karakter, sahte fiyat/yorum/indirim videoya girmez (aksesuar istisnası: kullanıcı kararı, KARARLAR.md).
- Yeniden üretim kredi harcar: `ai-video-kreatif` kredi kuralı geçerli (tek seferlik tavan onayı, KARARLAR.md).
- ChatGPT'de tek başına kurgu isteyen kullanıcıya: `${CLAUDE_PLUGIN_ROOT}/ekler/chatgpt/video-kurgu.md`.
