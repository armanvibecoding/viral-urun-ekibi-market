# hf-sablonlar — kanca + tipografi + geçiş + SFX paketi (0.6.0)

22 sahne türü: 6 temel şablon + TR/AB referans paketi (uzman_kutu, tek_kelime, altyazi, iki_katman, son_kart, dev_fiyat) + donusum + geçiş/kapanış paketi (urun_gecisi, dip_gecis, kapanis). Kaynak id'leri aşağıda (saha S24 = Keşfet turları G…; REF = referans seti 0.6 TR/AB reklamları TR01–TR06, AB01–AB05; dış hesap içeriği depoya kopyalanmaz, yalnız id + kural).

HyperFrames ile Reels/Keşfet videosunun yazı, geçiş ve ses katmanı. Kredisiz, ağsız üretim (render yerel Chrome). Kurallar ve ölçüler: `../referans/tipografi-ve-kanca-gorseli.md`.

| Dosya | İş |
|---|---|
| `tipografi.py` | 6 yazı şablonu + `donusum` + klip geçişleri (`klipler`) + ses olayı kaydı. `hikaye/bloklar.py` içe aktarır; ayar JSON'unda `"tur": "<şablon>"` |
| `sablon.css` | şablon stilleri (güvenli alan, kontur, kutu, rozet) |
| `ornekler/<şablon>/` | her şablonun bağımsız HyperFrames kompozisyonu (`index.html`) + parametre sözlüğü (`sahne.json`); `ornek_uret.py` ile yeniden üretilir, `npx hyperframes check` hata 0 (check sonrası `ornekler/*/.hyperframes/` silinir: yerel yol içerir, anonimlik kapısı yakalar) |
| `sfx_esle.py`, `LISANS-SFX.md` | olay → efekt eşleme, yoğunluk kapısı, lisans kaydı |
| `muzik_sentez.py` | demo/test müziği (numpy, drop'lu) |
| `sablon_test.py` | kırma testleri (kanca 3 satır/8 kelime, CTA güvenli alan, dönüşüm, SFX yoğunluğu) |

## Şablon parametreleri (hepsi: `bas`, `sure`, `top`, `renk`)
| Şablon | Parametreler |
|---|---|
| `ig_kutu`, `kalin_kontur` | `metin` (`/` satır, `*vurgu*`), `vurgu` [liste], `boy`, `adim` (0,08–0,12), `ilk_kare` (None → kancada hepsi) |
| `karaoke` | `metin`, `zamanlar` [kelime başına sn] ya da `adim` |
| `tepki` | `ust` ("Im sorry but"), `buyuk` ("WHAT?!"), `slam` (dev kelimenin gecikmesi) |
| `ig_kutu` ek | `vurgu_stil` (`kutu`\|`renk`), `emoji`, `buyuk_harf`, `dil` (`tr`: i→İ) |
| `uzman_kutu` | `metin`, `vurgu`, `dil` (hep BÜYÜK HARF, siyah kutu) |
| `tek_kelime` | `metin`, `adim` (≥ 0,3 sn), `renkler`, `top` (560–1100), `ok` (kırmızı ok), `dil` |
| `altyazi` | `metin`, `top` (varsayılan 1080; satırlar y ≤ 1330'da biter) |
| `iki_katman` | `kanca` {sablon, …}, `altyazi_ayar` {metin, top} |
| `son_kart` | `pazar` (TR\|DE\|AB\|US), `rozet`, `ikinci`, `dugme`, `anahtar` (US), `top` (öğe yığını y ≤ 1330'da biter) |
| `dev_fiyat` | `metin` ("−23€"), `renk`, `cikartma` ("−15%"), `boy` |
| `cta_rozet` | `anahtar` ("DOG"), `on` ("Comment"), `alt` (isteğe bağlı), `renk` |
| `sayac` | `deger`, `sonek` ("%"), `onek`, `etiket`, `sayim` |
| `ikili_kiyas` | `soru` (tek '?', ≤ 7 kelime; ≥ 3 kelime otomatik 2 satıra bölünür, `boy` 116 → telefonda okunur, `sigdir` 820 px'e sığdırır), `sol_etiket`, `sag_etiket`, `kazanan` (`sol`\|`sag`\|None), `cevap_an` (mutlak sn; varsayılan %70) — iki video alanı çağıranın klibi; çerçeve = orta çizgi + iki etiket (y ≤ 1330) + üstte soru |
| `deneme_sayaci` | `toplam` (2–10), `adimlar` (toplam adet MUTLAK sn, artan, yayın aralığında), `kural` (tek satır, ≤ 7 kelime) — '0/N → N/N' atlayan sayaç, son adım yeşil |
| `urun_gecisi` | `gorsel` (ürün PNG/JPG/SVG yolu ya da None), `kick`, `ust1`, `ust2` (`*` yok; ust2 vurgu rengi), `alt`, `gecis` (0,7 sn), `w`, `ust`, `bg` — `bas` ≥ `gecis` (sahne bas−gecis'te başlar: önceki klibin son 0,7 sn'si üstüne opacity 0→1, ilk 1 sn scale 1,06→1 + parlaklık 0,6→1, yazılar geçişten 0,3 sn sonra); tek yazı katmanı |
| `dip_gecis` | `z` (kesim sn, ≥ `once`), `once` (0,35: kesimden önce kararma), `ac` (0,6: açılış), `yogunluk` (0,7), `renk` — yazısız; sert kesmeyi yumuşatır |
| `kapanis` | `logo` (PNG/JPG/SVG yolu; yoksa HATA), `marka`, `alt_satir`, `yazi` (isteğe bağlı CTA, ≤ 7 kelime), `yumusak` (px; >0 → logo/alt satıra odak yumuşatma + 1,4 sn kararma), `kapan_sn` (0,8), `top_yazi`, `top_logo` — logo daire maske fade+scale; en çok 2 yazı katmanı; son `kapan_sn` siyaha fade. Görseller `varliklari_kopyala` ile `assets/img/`e gider (depoya logo konmaz) |
| `donusum` | `pencereler` [[0,2.2],[2.2,3.9],…], `kanca` {sablon, …}, `cta` {sablon, …} |
Klip öğesi (ayar `klipler[i]`): `dosya`, `ss`, `hiz`, `z0/z1` + `tur`: `bolunmus` (`dosya2`, `etiket1`, `etiket2`) · `donuk`. Geçişler: ayar `gecisler` = kesim başına `whip | punch | kesim`.
`ses.sfx_otomatik: true` → SFX olaylardan eşlenir (`sfx_max` varsayılan 6, `giris_hedef` kısa döngüde 8, hikâyede 11).

## Şablon → dayandığı referans id'si
| Şablon | Referans | Çıkarılan kural |
|---|---|---|
| `ig_kutu` (vurgu_stil `kutu`) | S24 G1x04, G2x03 | satır başına beyaz kutu, siyah yazı, üst-orta |
| `ig_kutu` (`vurgu_stil: renk` + `emoji`) | REF TR01, AB01, AB02 | beyaz kutu + TEK renkli (kırmızı) vurgu kelime + sonda emoji |
| `uzman_kutu` | REF TR03, TR05 | siyah (yarı saydam) kutu, beyaz KALIN BÜYÜK HARF; "uzman/acil" tonu; TR'de i→İ |
| `kalin_kontur` | S24 G3x07, G2x03; REF TR04 | kalın kontur, sarı vurgu, büyük harf seçeneği |
| `karaoke` | REF TR06, TR04 | satır görünür, kelimeler sırayla renk alır |
| `tek_kelime` | REF TR06, TR04 | ekranda tek kelime, sarı-beyaz dönüşümlü, BÜYÜK HARF, göğüs hizası, kırmızı ok |
| `altyazi`, `iki_katman` | REF TR04, AB01, AB04 | büyük kanca + küçük konuşma altyazısı birlikte (ikinci katman) |
| `tepki` | S24 G3x07 (51,4MN; ADAY, tek kanıt) | "Im sorry but WHAT?!" şaşkınlık; küçük cümle + dev kelime |
| `cta_rozet` | S24 G1x07, G2x03, G2x05, G3x05 | Comment "X" ekranda, kancayla dönüşümlü |
| `son_kart` TR | REF TR01, TR05 | son kare tek kırmızı teklif rozeti; metin mağazanın gerçek teklifi (varsayılan yok; "KAPIDA ÖDEME" yalnız mağaza sunuyorsa) |
| `son_kart` DE/AB | REF AB02, AB04, AB01 | kırmızı teklif rozeti ("−50% Nur HEUTE") + "GRATIS VERSAND" etiketi + düğme ("Jetzt bestellen"); teklif metni doğrulanmış olmalı |
| `son_kart` US | S24 G1x07, G2x03, G3x03 | Comment "X" ya da LINK IN BIO |
| `dev_fiyat` | REF AB04 | 1,5 sn'de dev kırmızı fiyat/indirim vuruşu + yuvarlak çıkartma; metin doğrulanmış teklif; hikâye hattında `fiyat_izin: true` ister |
| `sayac` | S24 G3x05 ("98%"), sahne S8 | kanıt/rakam sayımı |
| klip `bolunmus`, `donuk`, yakın çekim (`z0`) | S24 G1x08/G2x06 (dönüşüm), REF AB04 (ilk 1 sn dönüşüm), sahne S2/S9 | önce/sonra, sorun anı, yakın çekim kanca görselleri |
| `donusum` | S24 G2x03, G2x05, G1x07, G3x05; P02/P03 | kanca ↔ CTA dönüşümlü |
| `ikili_kiyas` | R1 (uzman yöntemi R74; üst 6/21, alt 0/20) | bölünmüş ekran + üstte tek soru; sonuç gerçek çekimle, cevap anında kazanan tarafa tik |
| `urun_gecisi`, `dip_gecis`, `kapanis` | müşteri video kitinden genelleştirilen geçiş/kapanış teknikleri (marka adı/logo çağıranın; örnekte jenerik yer tutucu) | ürün sahnesine çapraz geçiş · kesim öncesi dip kararma · logo+marka kapanışı ve son siyaha fade; ses tarafı: `ses_tasarla.py --son_fade 2.5 --son_fade_egri qsin` (müzik son 2,5 sn yumuşak; bayrak yoksa davranış değişmez) |
| `deneme_sayaci` | R2 (uzman yöntemi R74; üst 4/21, alt 1/20) | konuşmasız tek kurallı test + ilerleyen sayaç; adım zamanları gerçek sonuç anlarına bağlı |
Pazar notu: REF'te TR ve AB reklamları ABD Keşfet verisinden ayrı örneklenmiştir (TR veri zayıf: ilk testten sonra kalibre). `son_kart` pazar parametresiyle seçilir; metinleri pazarın dilinde çağıran verir.

## Kanca türü (K1–K15) → şablon
| Kanca | Şablon | Not |
|---|---|---|
| K1 Yasak "Don't show this to a X" | `kalin_kontur` (vurgu = kimlik) + `cta_rozet` | saha: kimlik kancası 14/19 |
| K2 Zorunluluk "Every X needs this" | `ig_kutu` | |
| K3 Hediye-yok kesik | `ig_kutu` (cümle "…" ile kesilir) | |
| K4 Bağlamlı hediye/tavsiye | `ig_kutu` | |
| K5 Alıntı-ironi | `ig_kutu` (tırnaklı) | |
| K6 Yetişkin parası ironisi | `kalin_kontur` | |
| K7 POV sorun anı | `ig_kutu` + klip `donuk` (sorun anı) | |
| K8 POV keşif | `ig_kutu` | demo 1 |
| K9 Sonuç/ihtiyaç cümlesi | `karaoke` ya da `kalin_kontur`; rakamlıysa `sayac` | |
| K10 Kimlik hitabı | `kalin_kontur` | |
| K11 Akış kartları (3 yazı) | `karaoke` / `ig_kutu` sırayla | |
| K12 Soru/merak | `karaoke` ya da `tepki` | demo 3 |
| K13 Yazısız | yazı şablonu yok; yalnız geçiş + SFX (CTA caption'da) | |
| K14 İtiraz/diyalog alıntısı | `ig_kutu` (tırnaklı itiraz) → `tepki` ya da `kalin_kontur` yanıt | |
| K15 Yorum-anahtar CTA, kancayla dönüşümlü | `donusum` (`kalin_kontur`/`ig_kutu` ↔ `cta_rozet`) | demo 1, 2 |
Kanıt/tatmin anı: `sayac` + yavaşlatılmış plan (S8, S7). Şaşkınlık kancası (ADAY, tek kanıt): `tepki`.

## Kullanım
```
python3 skills/studio/scripts/on_uretim_karti.py kontrol is/NN/hikaye/on-uretim-karti.json      # kart kapısı
python3 skills/cut/scripts/hikaye/uret.py is/NN/hikaye/ayar.json                                # kur → render → ses → pano → görüntü kapısı
python3 skills/cut/hf-sablonlar/sablon_test.py                                                  # paket testi
```
Ön koşul: Node 22+, ffmpeg + ffprobe PATH'te (`ffmpeg`/`ffprobe` adıyla; imageio ikilisi yalnız ffmpeg verir), Chrome (HyperFrames önbelleği).
Demo ayarları: bu klasörde yok (müşteri dışı demolar `_demo-0.6.0/` altında, depoya girmez); ayar biçimi `../scripts/hikaye/ayar-ornek.json` + yukarıdaki tablo.
