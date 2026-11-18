# Ses tasarımı — araştırma özeti, kurallar, efekt kartları

> 2026-11-16 araştırması (ses tasarımcısı üyesi için). Kaynaklar §6. Ölçümler dijital amblem serisi (30 video) üzerinde;
> hiçbir yargı kulakla verilmedi, hepsi `ses_tasarla.py` / `ses_olc.py` çıktısı.

## 1. Araştırma bulguları (kaynaklı)
1. **Ses açık izleniyor, ses satıyor.** TikTok/Kantar: kullanıcıların %88'i sesi deneyimin merkezi sayıyor; sesli reklamda "durup
   bakma" %73 ve yalnız TikTok'ta sesli reklam hem satın alma niyetini hem marka beğenisini kaldırıyor [K1, K2]. Ama tasarım
   **önce sessizde çalışır** (yazı + görüntü), ses destektir [B1].
2. **Kanca sesi ilk 1–2 sn'de.** Örüntü kıran efekt ilk 2 sn'de (whoosh/darbe/scratch); reklam kılavuzu bunu ~%12 kanca
   artışına bağlıyor (kendi verisi, kontrollü değil) [B1]. Sessiz açılış yok.
3. **Efekt yerleşimi = anlatı dönüm noktası:** problem→çözüm, fayda, CTA; her kesime değil [B1, F1]. Whoosh görsel hareketi olan
   geçişte, darbe jump-cut'ta, bas drop vurguda [F1]. Yoğunluk: 10 sn'de ≤ 4–5; "üçüncü-dördüncü tekrar"dan sonra ses
   bayatlar, "bir makine yapmış" hissi [A1].
4. **Drop öncesi boşluk (the cut):** drop'tan önce 1–2 vuruş sessizlik ya da yalnız riser/reverb kuyruğu; "sessizlik anında
   dikkatin %100'ü sende" [M1, M2, M3]. Ölçüldü: 0,2 sn kesme drop kontrastını +5,5 → +7,0 dB (yalnız kesme), darbeyle +14 dB'ye
   çıkarıyor. **Riser, drop'a kadar sürerse kontrastı siler** (+1,2 dB); kesmeden önce bitse bile −18 dB'de 4,6, −22 dB'de ≈ −1,5 dB bedel.
5. **Seviye:** hedef −14 LUFS; efektler ana ses/konuşmaya göre −5…−10 dB; telefon hoparlöründe test; clipping yok [B1].
   Drop dışı 0,1 sn sıçrama > +10 dB (`ses_olc.py` `drop_disi_sicrama`, `--kapi` çıkış 4) seviyeyle değil müzik stem'ine
   kompresörle düzeltilir; `--muzik_db` son normalizasyondan sonra etkisizdir (2026-11-18 ölçüldü).
6. **Meme sesleri:** Vine Boom 2012 Bluezone örnek kütüphanesinden, Vine'da 2014 (King Bach) yayıldı, 2020–22 ironik "loud =
   funny" kodu, "aşırı kullanım" algısı var [V1]; açık lisansı yok, Remotion bile "CC0 gibi serbest bir lisansla yayımlanmamış"
   diyor [V2]. Record scratch "Yep, that's me" kalıbı The Who "Baba O'Riley" ile anılır → şarkı yok, jenerik scratch var [R1].
   Meme sesi tek klipte 1–2 kez; "yığmak şakayı zayıflatır" [V3].
7. **Lisans ve platform:** TikTok işletme hesabı yalnız Ticari Müzik Kütüphanesi'ni (1 M+ parça ve efekt) görür; trend sesler
   tanıtım içeriğinde kullanılamaz; Temmuz 2025'te şartlar sıkılaştı; Sony–DSW davası (2025) emsal [T1, T2, T3]. Instagram
   işletme hesabı Meta Sound Collection ile sınırlı; efektler de orada [I1]. Serbest kaynak: Mixkit SFX Free (ticari + atıfsız)
   [L1], Freesound CC0 [L2], Pixabay Content License [L3]. **Yol:** dosya olarak yalnız açık lisanslı/sentetik; trend ses
   gerekiyorsa yayın anında platform kütüphanesinden eklenir (kurucu kararı).
8. **Araç videolarında kalıp:** motor + lastik + hava-whoosh katmanları; whoosh araç kameraya en yakınken tepe yapar; bas
   gürleme tiz lastik sesinden önce gelir [C1, C2]; en güçlü an (alev) drop'tan 0,5 sn sonra düşerse "kayık" hissi [C3].

## 2. Kurallar (ses tasarımcısı bunlara göre plan yazar)
- **Müzik ilk kareden, ani giriş yok (2026-11-17 kurucu: "müzik bir anda açılıyor"; ağır kusur).** Açılış diegetik ses olayıyla
  (kutu tık, telefon titreşimi); müzik 0. sn'de −30 dB'den başlar ve 1,5–2 sn'de dB-doğrusal rampayla yatak seviyesine
  çıkar (`ses_tasarla.py --muzik_fade_in 1.75`, varsayılan). "Kısık/boğuk
  (alçak geçiren) yatak + drop'ta tam müzik" YASAK — ölçüldü: 3 sn pencerede +22,2 dB basamak, kurucu reddetti. Kapı:
  `ses_olc.py VIDEO --muzik_stem muz.wav --kapi` çıkış 0 (başlangıç ≤ −20 dB · rampa 1,5–3,0 sn (fade 1,5–2 sn; parçanın kendi girişi ölçümü 3 sn'ye kadar uzatabilir) · ilk 1 sn ≥ −30 dB · 3 sn basamak ≤ +10 dB · açılış olayı ≥ −6 dB).
  Elle miks betiği yazan kurgucu müzik stem'ini ayrı dosyaya yazar (yoksa ölçülemez → eleştirmen ses ≤ 5).
- Herhangi bir 10 sn penceresinde (kayan pencere; 0–10/10–20 kovası değil) ≤ 5 efekt (betik kapısı `--sfx_max_10sn`); aynı anda
  katmanlanan sesler tek efekt dosyasında birleştirilir; 12–15 sn videoda 4–6. Kanca ilk 0,5 sn'de ses olayı (diegetik efekt; müzik altta −30 dB rampada). Delik yok (`ses_olc.py delikler: []`).
- Hiyerarşi (tepe, son seviyeden önce): drop darbesi −3…−6 · ikincil −6…−9 · UI/scratch −10…−14 · riser ≤ −22 (ya da yok).
- Drop (vurgu) reçetesi: müzik zaten çalarken `--sessizlik_vurusu 0.2` + drop'ta darbe (`boom@` ya da bas-drop dosyası);
  vurguyu efekt ve 0,2 sn boşluk taşır, müziğin seviyesi değil. `drop_artis_db` 6–10. Riser isteğe bağlı, kesmeden önce biter.
- Meme darbesi punchline'la aynı karede; komedi dışı videoda yok. Komedi duraklaması: scratch + 0,1–0,2 sn müzik kesme (`--sessizlik`).
- Gerçekçi efekt görüntüye bağlı: dokunuş yoksa tık yok; whoosh yalnız hareketli geçiş/punch'ta. Olay sesi hareketin İLK
  GÖRÜNÜR karesine ±0,1 sn oturur; plan saniyesi ya da senaryo değil, görüntü (4 fps/10 fps pano) esas alınır.
- **Ürünün işlevi sesle hissettirilir** (imâ yolu): işlevi ekranda söylenemeyen üründe (reklamı yasak kategori) işlevin
  sesi alt mesajdır — ör. kısa titreşim/buzz (bkz. efekt kartı "Buzz"), görüntüdeki hareketle ±0,1 sn (aynı klip aralığı tekrar ya da farklı hızla kullanılıyorsa olay anı yeniden hesaplanır:
  t_çıkış = bas_çıkış + (t_kaynak − bas_kaynak)/hız; o aralıktaki görünen olaylar da sese bağlanır), videoda 1–3 kez,
  ilk 5 sn içinde en az bir kez. Ses ürünü açıkça tarif etmez; izleyici 2. izlemede çıkarır (eleştirmen "2. izleme testi").
- Müzik drop'u bastırılmaz: `drop_tuttu: true` ve önce/sonra `drop_artis_db` yazılır; en yüksek an (`tepe_anlari`) punchline/drop olmalı.

## 2b. Müzik seçim ölçütü (seçim gerekçesi `muzik/LISANS.md` altına 3 satır)
1. **Duygu = ürünün vaadi:** ürün kartındaki "kim alır, neden" cümlesinden bir duygu kelimesi çıkar (ör. merak, rahatlama,
   özgüven, oyunbaz, lüks, gerilim) ve parçanın tür/temposunu buna bağla. "Gizem/suspense pizzicato" gibi jenerik stok
   kalıpları duyguyla gerekçelenmeden seçilmez (2026-11-17 kurucu: "müzik kötü").
2. **Pazar:** hedef pazarın o kategorideki organik videolarında duyulan türe yakın (pazar kartı §10; ABD'de trend ses
   gerekiyorsa yayın anında platform kütüphanesinden — dosya olarak yalnız açık lisanslı).
3. **Açılış:** parçanın ilk 3 sn'si videonun duygusuna uyuyor (girişi sessiz/uzun intro olan parça ofsetle kırpılır;
   parçanın kendi içinde +10 dB'den büyük ani bölüm geçişi varsa o bölüm videoya düşmez; parçanın kendi bas/bölüm girişi kullanılıyorsa o an videonun TEK drop'udur (`--drop` o saniyeye verilir), ikinci vurgu efekttir ve +6 dB'yi aşmaz — kapı yakalar).
   Hikâye türüne göre başlangıç (dış araştırma 2026-11-17, ölçülmedi): duygusal/metafor → lo-fi R&B / neo-soul, sıcak Rhodes,
   70–90 BPM · deadpan mizah → minimal ya da sessizlik + tek darbe (espri karesinden önce 0,3–0,5 sn boşluk) · lüks/obje →
   sultry pop / trip-hop pad, 80–95 BPM · sezon → kamu malı melodinin minör/lo-fi yorumu (kayıt değil, kendi üretimimiz).
   Açılış: 0,0 sn'de diegetik ses olayı (kutu tık, telefon titreşimi), müzik altta rampa; bitiş: müzik kesilmez, son 1,5 sn'de iner.
   Lisans: işletme hesabında platform ses koleksiyonu (uygulama içinde) ya da lisans belgesi klasörde duran ticari/açık
   lisanslı parça; telifli trend şarkı dosya olarak YOK.
4. **Kurucu dinler:** her videoda 3 aday parça `muzik/aday1-3` olarak indirilir ve kurucuya dinletilir; seçimi kurucu yapar.
   Ölçüm (tempo/spektrum) yalnız ön eleme içindir, seçim değildir. Yetişkin/arzu ürününde duygu "after dark": yavaş (60–85 BPM),
   bas ağır, nefesli vokal dokusu, sultry R&B/pop; inleme/nefes örneği YOK (platform kapısı).
   **Kapı:** `muzik/LISANS.md`'de "Kurucu seçti: <tarih>, söz kapısı: temiz | enstrümantal" satırı yoksa `ses_tasarla.py`
   çalıştırılmaz (ses tasarımcısı ve kurgucu bu satırı arar); satırsız teslimde eleştirmen ses alanına en fazla 4 verir.
5. **Stok hissi testi:** parça adında/etiketinde "corporate, upbeat background, inspiring, suspense" geçiyorsa ve 1. madde
   gerekçesi yoksa seçilmez. Ön elemede tür/BPM/enstrüman satırıyla karşılaştırılır; son seçim 4. maddeye göre kurucunun kulağıyla.

## 3. Efekt kartları (kütüphane: ürün klasörü `sfx/kaynak/`, lisans `sfx/LISANS.md`)
| Efekt | Dosya / sentetik | Ne zaman | Seviye | Dikkat |
|---|---|---|---|---|
| Whoosh (hızlı) | mixkit_1490, 1492 | hareketli geçiş, zoom punch; kesimden 0,10–0,15 sn önce başlar | −12 | durağan kesimde kullanma |
| Swoosh (kısa) | mixkit_1461, 166 | yazı/CTA girişi | −13 | |
| Boom (vine-boom benzeri) | `--sfx boom@` sentetik · CC0 alternatif freesound_826217 (kırp 0–1,2) | punchline, 1–2 kez | −6 | ironi bilinçli, yetişkin alıcıya 1 kez |
| Bas drop | freesound_475005 | müzik drop'u + flaş | −6 | sessizlik vuruşuyla birlikte |
| Büyük darbe | mixkit_788 (kırp 0–1,2), 1143 (whoosh→darbe) | sinematik reveal | −6 | kuyruğu uzun, 10 sn'de 1 |
| Record scratch | mixkit_704 (kırp 0–0,9), 710; freesound_431780 | "dur, ne?" anı, kanca | −8…−12 | müziği 0,1–0,2 sn kes |
| UI tık | mixkit_2577, 3124; sentetik `tik@` | telefon/ekran dokunuşu | −12 | ekranda dokunuş yoksa yok |
| Kamera | mixkit_1133 | "kaydet / fotoğraf" anı | −12 | |
| Bildirim | mixkit_2354 | yorum/CTA vurgusu | −14 | reklamda "sahte bildirim" hissi riski |
| Riser | `--riser bit:1.0:-22`; freesound_832275 (son 1–2 sn) | drop öncesi | ≤ −22 | kontrast bedeli ölçülü (§1.4) |
| Kalabalık "ooh" | freesound_264376 (CC0) | reveal tepkisi | −14 | sahte izleyici tepkisi gibi durur; seyrek |
| Vuruş | sentetik `vurus@` | rozet/ekran değişimi | −6…−9 | |
| Buzz (titreşim) | sentetik: 150–200 Hz gövde + 1–3 kHz masa/kasa tıkırtısı (telefon hoparlörü 200 Hz altını zayıf verir; miks telefonda dinlenerek sınanır), motif kısa-kısa-uzun ≈ 0,12 · 0,12 · 0,45 sn; ya da CC0 "phone vibrate" | işlevi titreşim olan ürünün imâsı; müziğin vuruşuna kilitli, ≤ 3 kez | −10…−14 | görünür kaynağı masum nesne (masadaki telefon, kapalı kutu); ürün yakın planıyla aynı anda YOK; nefes/inleme ile YOK (`kurgu-ve-yasaklar.md` §8.1) |

## 4. Kullanılamayan popüler meme sesleri
Vine Boom orijinali (lisanssız örnek) · "Oh no no no" (Capone şarkısı) · Bruh · Emotional damage · Sad violin · Curb Your
Enthusiasm · Directed by Robert B. Weide · Taco Bell bong · FBI open up · Windows XP · Metal Gear alert · Dramatic sting
(film kaydı) — telif/marka/kişilik hakkı. Yalnız platform kütüphanesinden, yayın anında.

## 5. Araç komutları (özet; tam liste `ses_tasarla.py --help`)
`--sfx tik|vurus|boom|whoosh@sn` · `--sfx_dosya "ad.mp3@sn:dB[:bas-bit]" --sfx_klasor sfx/kaynak` · `--riser bit:sure:dB` ·
`--sessizlik_vurusu 0.2` · `--sessizlik "a-b"` · `--sfx_max_10sn 5` · `--muzik_fade_in 1.75` · `--stem_klasoru` ·
ölçüm `ses_olc.py VIDEO --drop sn --muzik_stem muz.wav --kapi`.
Geri uyumluluk (2026-11-16): eski komut **bit-bit aynı** sesti (md5 1bab00e90c73). 2026-11-17'den beri müzikli komutlar
varsayılan −30 dB'den 1,75 sn rampa alır ve müzik girişi kapısından geçer → müzikli eski çıktılar artık birebir aynı değildir (bilinçli). Örnek dosyalar ve önce/sonra:
`is/NN/teslim/ses-ornek/SES-ORNEK.md` (ürün klasöründe).

## 6. Kaynaklar
- K1 https://ads.tiktok.com/business/en-US/blog/kantar-report-how-brands-are-making-noise-and-driving-impact-with-sound-on-tiktok
- K2 https://www.socialmediatoday.com/news/tiktok-shares-new-insights-into-the-importance-of-sound-for-marketing-promo/601569
- B1 https://benly.ai/learn/ad-creative/sound-design-video-ads · F1 https://fish.audio/blog/using-sound-effects-for-short-form-content
- A1 https://futuregoldmedia.com/goldmineblog/annoying-tiktok-trends
- M1 https://blog.faderpro.com/creativity/silence-in-music-production/ · M2 https://medium.com/betterism/8-simple-tricks-edm-artists-use-to-make-their-drops-sound-more-powerful-79b50413fb75 · M3 https://theghostproduction.com/how-to-build-drops
- V1 https://knowyourmeme.com/memes/vine-boom-sound-effect · V2 https://www.remotion.dev/docs/sfx/vine-boom · V3 https://voxbooster.com/blog/soundboard-meme-audios-vine-boom-sfx/
- R1 https://knowyourmeme.com/memes/record-scratch-freeze-frame
- T1 https://www.soundstripe.com/blogs/tiktok-music-library-explained · T2 https://legismusic.com/tiktoks-july-2025-music-licensing-changes · T3 https://www.foximusic.com/blog/commercial-music-licensing-tiktok-guide/
- I1 https://www.soundstripe.com/blogs/instagram-music-library
- L1 https://mixkit.co/llm-info/ (Free License: ticari, atıfsız; yeniden satış yok) · L2 https://freesound.org/help/faq/ · L3 https://pixabay.com/service/license-summary/
- C1 https://krotos.studio/blog/car-driving-sfx · C2 https://sfxengine.com/blog/car-driving-by-sound-effect · C3 https://resources.oreateai.com/resources/how-to-create-high-energy-car-edits-that-actually-go-viral
- Nörosinema (kesme-dikkat; ses bulgusu zayıf/karışık): https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2025.1719407/full
