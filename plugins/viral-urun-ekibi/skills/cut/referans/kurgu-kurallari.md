# Kurgu kuralları ve ayar dosyası

Kaynak: ~100 milyon izlenen ürün videosunun ölçümü (süre, yazı, CTA) + 30 videoluk gerçek AI serisinde ölçülen hatalar.
Gerekçeler ve kanıt numaraları: `<eklenti kökü>/skills/studio/referans/kurgu-ve-yasaklar.md`.

## Ayar dosyası (is/NN/kurgu/VNN.json — yollar BU dosyaya göre göreli)
```json
{
  "planlar": [["../klipler/V01_S1.mp4", 0, 4.0], ["../klipler/V01_S2.mp4", 0.4, 4.0], ["../klipler/V01_S3.mp4", 0, 3.6]],
  "kanca": "Kedim bunu görünce aklı gitti",
  "cta_kelime": "PİYANO",
  "cta_plan": -1,
  "yazi_konum": "oto",
  "kanca_gizle": [],
  "sfx": [{"dosya": "../ses/tik.wav", "sn": 5.2, "db": -6, "hizala": true}],
  "klip_sesi_db": 0,
  "qc_izin": [],
  "cikti": "V01.mp4"
}
```
| Alan | Anlam |
|---|---|
| `planlar` | [klip, başlangıç sn, bitiş sn]. Hatalı uç burada kırpılır. Her planda ekranda 2–4 sn. |
| `kanca` | metin ya da plan başına liste (`null` = o planda yazı yok; K11 kart akışı: `["The problem", "Vs…", "The solution"]`). `" / "` satır sonu. |
| `cta` / `cta_kelime` | `cta` yoksa kelime + pazar: TR `Yorumlara "KELİME" yaz, linki DM'den atayım` · yurt dışı `Comment "WORD" and I'll DM you the link`. |
| `cta_plan` | CTA'nın başladığı plan (varsayılan son). Betik en az 3 sn olmasını zorlar. |
| `yazi_konum` | `oto` (her planın orta karesinde en az kenar/detay olan bant: ust/orta/alt) · `ust` · `orta` · `alt` · piksel. |
| `kanca_gizle` | yakın planda ürün yazısının üstüne binmesin diye kancasız planlar. |
| `sfx` | kullanıcının telifsiz ses dosyası; `hizala: true` = plan saniyesinin ±1,2 sn'sindeki gerçek ses yükselişine oturur. |
| `qc_izin` | ölçüm işaretledi ama 4 fps panoda doğal hareket görülen plan numaraları (0'dan). Gerekçeyi DURUM'a yaz. |
| `pazar`, `font`, `min_yukseklik` | isteğe bağlı geçersiz kılma (varsayılan: KARARLAR.md, otomatik font, 1280). |

## Süre ve kesme
- Toplam 8–15 sn, hedef 10–12 (milyonların medyanı 12 sn; bu aralıkta kısaltmak tek başına kazandırmaz).
- Tek sahne şablonunda (S1) kesmesiz; 2–3 klip aynı kadrajda devam eder.
- Son kare ilk kareye bağlanıyorsa döngü (tekrar izlenme).

## Yazı
- Kanca beyaz, kalın sans-serif, siyah kontur, 1–3 satır; 40 karakter altı 72 px, üstü 64 px; CTA 56 px, kancanın hemen altında.
- Yazı ürünü ve çıkış noktasını örtmez: ürünün en büyük olduğu karede kontrol (kontrol karesi). Ürün alt yarıdaysa yazı üstte.
- Alt %20 (Instagram açıklama alanı) ve sağ %15 (düğmeler) boş.
- Emoji fontta kutucuk olur → videoya koyma, caption'a taşı. Koyu emoji koyu zeminde kaybolur.
- Türkçe büyük harf elle yazılır (`upper()` "i"yi "I" yapar); font test karesinde İ ve ı'yı kontrol et.
- Yazısız (K13) videoda yalnız caption'da CTA.
- Fiyat: ICE-01 (`ortak/kurallar.md`). Ekran yazısı merak/ikna/kimlik taşır;
  ölçü/ağırlık/renk listesi yazı değildir (`studio/referans/kanca-kutuphanesi.md` §1b Ekran yazısı).

## Ses
- Klibin kendi gerçek sesi esas. Efekt: kullanıcının kendi telifsiz dosyası; ürün sesi gerçek basış/olay anına (hizala).
- Lisanslı popüler müzik yok. Konuşma/seslendirme yok (kurallar ses düzeyinde dinlenebilir videoya göre).
- Müzik girişi: SES-01 (`ortak/kurallar.md`; kapı `ses_olc.py --muzik_stem --kapi`).
- Hedef −14 LUFS; tek geçişli normalleştirme videolar arasında 8 dB fark bıraktı → betik ölç-kazanç-ölç döngüsü yapar.
- Seri halinde videoları art arda dinlemek mümkün değilse LUFS satırlarını karşılaştır (±1 içinde olmalı).

## Klip kalite kapısı — neden 4 fps
Gerçek seride saniyede ~1,5 kareye bakılan 30 videonun 17'sinde sonradan hata çıktı: yanlış parçaya basınca sonuç,
kimse dokunmadan ürün çalışması, ışınlanma, hayvanın yavaşça cins değiştirmesi. Ölçüm (sıçrama) ışınlanma ve gizli
kesmeyi yakalar; yavaş dönüşümü yalnız 4 fps pano yakalar. İkisi birlikte zorunlu.
Kök sebepler: başlangıç karesi (pati havadaysa yanlış yere iner) · prompt (belirsiz yön, AUDIO satırındaki olmayan olay) ·
video modeli (kesme/dönüşüm → kırp ya da yeniden üret).

## Hızlı (viral) kurgu ve ses kuralları (SKILL.md'den taşındı)
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
- **Ön-kontrol kapısı (kurgudan sonra, jüriden önce):** `hizli_kurgu.py ayar.json --katı` (okunma UYARI'sı = çıkış 1),
  sonra `kurgu_kontrol.py ayar.json --video VIDEO.mp4` → çıkış 0 olmadan jüriye gönderme. Klip içerikleri
  `klipler/klip_etiket.json`dan okunur (biçim betiğin başında; yeni klip = yeni etiket satırı, bilinmeyen "bilinmiyor").
  Betik ölçülebilir kuralları alır; kanca gücü, gerçekçilik, ritim yargısı kör jüride kalır.
- Teslimden önce kör jüri (`juri.py pano --mod teslim` → `video-juri` 3 kopya → `juri.py birlestir`; akış `captain` "Hüküm hattı")
  videoyu gerçek viral referanslarla yan yana puanlar; `gecti: true` olmadan teslim yok. Kalırsa kök nedeni `video-elestirmen` yazar.
  Teslim geçişinin tek kapısı: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/captain/scripts/kapi.py" yayin is/NN --proje . --kopyala`
  (teknik, kurgu, görüntü, ses, iddia, hüküm, defter, sözleşme); çıkış 0 olmadan `teslim/` klasörüne video konmaz.

Kurallar (ayrıntı `referans/kurgu-kurallari.md`):
- Kanca beyaz kalın, siyah konturlu, 1–3 satır; konum "oto" en boş bandı seçer (alt %20 ve sağ %15 hariç).
- Emoji videoya girmez (betik çıkarır, uyarır) → caption'a taşı. Türkçe büyük harfi elle yaz; kodda `upper()` kullanma.
- Font: betik Türkçe harfleri (çğıİöşü) ölçerek seçer; ilk kurulumda font test karesine bak.
- Ses: klibin gerçek sesi + sentetik efekt: `ses_tasarla.py --sfx tik@sn,vurus@sn` (tık = dokunuş, vuruş = değişim);
  **efekt dosyası istenmez.** Kullanıcı kendi efektini verirse `sfx` + `hizala: true` gerçek ses anına oturtur. Hedef −14 LUFS.
- **Ses tasarımcısı (ses_tasarla'dan önce):** `ses-tasarimcisi` ajanı ayar dosyasından efekt planı (sn · efekt · dB · neden)
  çıkarır ve komutu üretir: dosya efekti `--sfx_dosya "ad.mp3@sn:dB" --sfx_klasor is/NN/sfx/kaynak` (lisans `sfx/LISANS.md`'de),
  sentetik `boom/whoosh`, drop reçetesi `--riser <drop−0,2>:1.0:-18 --sessizlik_vurusu 0.2`. Kapılar: 10 sn'de ≤ 5 efekt,
  `drop_tuttu`, **müzik girişi** (SES-01).
  Önce/sonra `ses_olc.py VIDEO --drop sn --muzik_stem <stem>/muz.wav --kapi`. Yöntem: `referans/ses-tasarimi.md`.
- **Elle miks betiği** (ses_tasarla dışı) yazılırsa müzik stem'i ayrı wav olarak kaydedilir ve aynı kapıdan geçer.
- **Drop karışımda ölçülür:** müzik dosyasındaki drop yetmez; klip sesi (rölanti, söküm) drop'u bastırır. `ses_tasarla.py`
  drop'tan önceki 1,7 sn'de klip sesini `--drop_oncesi_db` (varsayılan −8) kadar kısar ve drop anındaki artışı ölçer;
  < `--drop_esik_db` (6 dB) ise `hedef_tuttu: false`. Geçmezse −12/−16 dene ya da drop öncesi planların `ses_db`'sini kıs.
- **Müzik videoda olmalı** (müziksiz teslim yok). Kaynak (Aşama 0'da izni alınmış): kullanıcının dosyası ya da Pixabay.
  Pixabay (ölçülmüş): arama sayfasını `fetch` et (`pixabay.com/music/search/<tür>/`) → ilk parça sayfasını `fetch` et →
  içindeki `cdn.pixabay.com/download/audio/...mp3` bağlantısını al → `curl -L -o is/NN/muzik/<ad>.mp3 <bağlantı>`.
  Parça adı, sanatçı, sayfa linki ve lisans notu (Content ID riski) teslim raporuna. Telifli şarkı indirilmez; yayında
  platformun kendi ses kütüphanesinden eklenebilir. Drop'u ölç (0,1 sn enerji sıçraması) ve "önce/sonra" kesimine hizala.
- Ana ses anı (egzoz, tık, patlama) müziğin üstüne çıkar: `ses_tasarla.py` (sidechain ile müziği o anda kısar,
  bas + doygunluk + mekân yankısı; tepe −1 dBTP). Abartı gerçekçiliği bozmamalı: clipping yok.
- Toplam 10–15 sn; tek sahne şablonunda kesme yok; son kare ilk kareye bağlanabiliyorsa döngü kur.
