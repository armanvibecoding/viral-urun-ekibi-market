# Tipografi, kanca görseli, geçiş ve SFX kuralları (0.6.0 paketi)

Kaynak: saha sentezi (28 video ilk 8 sn + 4 tam izlenen hit; `studio/referans/kanca-kutuphanesi.md` K1–K15, `sahne-sablonlari.md`). Uygulama: `hf-sablonlar/` (şablonlar, SFX eşleme, müzik üretici, testler).
Ölçüler 1080×1920. Kural dışı örnek bulursan kuralı değil kanıtı güncelle (kanıt numarası ile).

## 1. Kanca yazısı (ilk kare = küçük resim)
| Kural | Ölçü | Kapı |
|---|---|---|
| İlk karede (0,0 sn) tam kanca okunur | tüm kelimeler `opacity 1`; pop = kelime sırasıyla zıplama (1,0→1,22→1,0, 0,05+0,08 sn) | `tipografi.py` (`_pop`); `sablon_test.py::test_kanca_ilk_karede_gorunur` |
| Uzunluk | ≤ 2 satır, ≤ 7 kelime (TR ≤ 8, ön-üretim kartı kapısı) | `kanca_kapisi()` HATA (SystemExit) |
| Konum | üst-orta 1/3: `top` 300 px (yazı bloğu y 240–700); üst 220 px ve alt 420 px boş; sağ 130 px boş (IG sağ sütun) | `.tx{left:110px;width:780px}`; `cta_rozet` `top+330 > 1500` HATA |
| Kelime girişi | 80–120 ms aralık (`adim` 0,08–0,12; varsayılan 0,10) | parametre |
| Vurgu | tek anahtar kelime (en çok bir öbek) renkli: `#FFE600` sarı ya da `#22C55E` yeşil; `*kelime*` / `*iki kelime*` | `satirlar()` |
| Yazı tipi | Montserrat 800/900 (HyperFrames'te paketli); beyaz + siyah kontur 14 px + gölge YA DA beyaz kutu siyah yazı | `sablon.css` |
| Satır sarması | yok: yazı boyu en uzun satıra göre kendini küçültür (`sigdir`, ≈ 0,62 em/karakter) | otomatik |
| Okunma | yazı ekranda ≥ 0,5 sn + 0,3 sn/kelime (HyperFrames craft `line_unread` tabanı) | `hyperframes check` |
| Ürünü örtme | yazı üst 1/3'te; ürün orta 1/3'te; üst degrade perde `ustperde` (0,58→0) kontrastı korur | `ust_perde()` |

## 2. Altı yazı şablonu (parametre: metin, vurgu, renk, top, boy, süre)
| Şablon | Ne zaman | Hareket | SFX olayı |
|---|---|---|---|
| `ig_kutu` | IG-yerli his; kimlik/POV/hediye kancaları | satır başına beyaz kutu, vurgu kelime renkli kutu | açılış/yazı → pop |
| `kalin_kontur` | arka plan kalabalık, sarı vurgu; K1/K10 | kalın kontur + gölge | pop |
| `karaoke` | sonuç/akış cümlesi, K11/K12; yazısız hit'te anlatı | satır soluk, kelimeler sırayla renk + 1,14× | pop |
| `tepki` | şaşkınlık/şok ("Im sorry but WHAT?!") | küçük cümle 0. karede, dev kelime 3×→1× çarpar + 14 px sarsıntı | darbe (impact) |
| `cta_rozet` | yorum-anahtar CTA (K15) | yeşil rozet pop + zıplayan ok; `top` ≤ 1170 | bubble |
| `sayac` | kanıt/rakam (S8, "98% …") | 0→N sayım 0,9 sn, bitişte elastik çarpma | ding (ping) |
`donusum(pencereler, kanca, cta)`: kanca ↔ CTA dönüşümlü (saha 8 kanıt); ilk pencere 0. sn; ayrı bitiş kartı yok. Kanca dışı yazılar 0,12 sn yumuşak girer (büyük beyaz kutunun tek karede belirmesi görüntü kapısında sıçrama sayılır — ölçüldü).
Fiyat/para birimi ve ima edilen tıbbi sonuç yazılmaz (hikâye hattı fiyat kapısı + iddia kapısı geçerli); `sayac` rakamı yer tutucu olamaz, doğrulanmış iddiadır.

## 3. Kurgu ritmi
- Plan 1,3–2 sn (6–10 sn döngü: 3–6 plan; 25 sn hikâye: 8–10 plan, plan 2–3 sn). Aynı klibin ikinci kullanımı serbest.
- **Tek tatmin/kanıt anı** yavaşlatılır: `hiz` 0,55–0,6 + yavaş itme (`z0 1.0 → z1 1.1`), ≥ 1,4 sn; riser bu andan 0,25 sn önce biter; SFX = sparkle.
- **Döngü**: son plan = ilk plan (aynı klip; son karesi ilk karenin kaynak karesine bağlanır: `ss` = ilk plan `ss` − plan süresi; `z0/z1` ters). Son yazı kanca ya da CTA'dır.
- **Geçiş** (`gecisler`, kesim başına): `whip` = giren klip yandan itilir (x ±950, 0,16 sn, power3), ışık süzmesi (`streak`); `punch` = çıkan klip 1,22× yakınlaşır (0,12 sn), giren 1,22×→1× (0,28 sn expo.out); `kesim` = düz. Hepsi GSAP; videonun CSS filtresi yok. Bir videoda en çok 1/3 düz kesim; whip ve punch dönüşümlü. `data-motion-blur` AÇILMAZ: hareketli klip/karakter katmanında sızıntı yapar (tuzak); bulanıklık yerine süzme (`streak`) kullanılır.
- Registry karşılıkları (elle yazmadan önce arandı, 2026-11-24): `whip-pan-cut`, `zoom-through-transition`, `caption-highlight`, `caption-kinetic-slam`, `number-pop-in`. Üretim hattı tek dosyalı ve deterministik olduğundan aynı reçete GSAP ile `tipografi.py`'de; Studio'da elle düzenlenecek tekil sahnede registry bloğu tercih edilir.

## 4. Kanca görseli (ilk kare) — 3 kalıp
Ürün ya da sonuç ilk karede · yüksek kontrast · tek odak · yazıyla çakışmaz (yazı üst 1/3, odak orta 1/3).
| Kalıp | Klip ayarı | Not |
|---|---|---|
| Önce/sonra bölünmüş ekran | `"tur": "bolunmus", "dosya", "dosya2", "etiket1", "etiket2"` | 540 px yarım ekran, 12 px ayraç, etiket y 820; etiket karşıtlığı (COLD/HOT, BEFORE/AFTER); gerçek ürün klibi ile ölçülü (stok demo yalnız yerleşimi gösterir) |
| Aşırı yakın çekim | `"z0": 1.35–1.4, "z1": 1.0` (ya da kaynakta yakın plan) | doku/sonuç; kaynak ≥ 1080p (4K stok seçildi: 9:16 kırpma keskin kalır) |
| "Sorun anı" donmuş kare | `"tur": "donuk", "ss": <saniye>` | kare dondurulur, kırmızı vinyet (0,25 sn) + yavaş itme; metin sorunu söyler (K7/S9) |
Kaynak seçimi: stok klibi dikeye kırparken özneyi kırpma merkezine al (`crop x` oranı); özne 9:16 dışında kalırsa klip değişir.

## 5. SFX eşleme (kredisiz, yerel; `hf-sablonlar/sfx_esle.py`, lisans `LISANS-SFX.md`)
| Olay | Efekt | Tepe | Kural |
|---|---|---|---|
| 0. sn yazı | pop (açılış) | −4 dB | ses_olc kapısı: açılış olayı ≥ −6 dB, hiç elenmez |
| kesme (whip) | whoosh-short | −9 | hareket başlangıcından 0,05 sn önce |
| kesme (punch) | whoosh-short (0–0,35 sn) | −12 | |
| yazı girişi | pop | −13 | şablon başına bir kez |
| CTA | bubble (sentetik) | −11 | ikinci CTA düşük öncelik |
| kanıt anı | sparkle (drop darbesi) / ping (sayaç) | −4 / −9 | |
| şok | impact-bass | −8 | |
| riser | sentetik `--riser` | −22 | kanıt anından 0,25 sn önce biter |
Yoğunluk: kayan 10 sn pencerede ≤ 6 efekt (ayar `sfx_max`); fazlası öncelikle elenir (punch < yazı < tekrar CTA < whip < riser < CTA < kanıt < şok < açılış). Elenenler `ses/sfx_plan_<ad>.json` içinde nedeniyle yazılır.
Müzik: `ses.py` ayarı `giris_hedef` drop kontrastını belirler. Ölçüldü (sentetik müzik): kısa döngüde 8, 25 sn hikâyede 11 → `ses_olc --kapi` geçer; döngüde ≥ 9 müzik rampasını 3 sn'nin dışına taşır (kapı kalır). Efektler müzikten sonra −14 LUFS'a normalize edilir; ölçüm: `ses_olc.py --kapi`.
Gerçek yayında müzik platform kütüphanesinden/lisanslı dosyadır; `muzik_sentez.py` yalnız demo ve kapı testi içindir (kulakla dinlenmedi).

## 6. Render sonrası kare kontrolü (her video)
1. `uret.py` çıktısı: `TESLIM/<ad>_pano10.jpg` (10 kare, kısa videoda süre/10 arayla), `_kontrol.jpg`, `_pano_ilk2sn_10fps.jpg`, `_pano_4fps.jpg`. Hepsine bak.
2. Bak: kırpılma (yazı kenara/IG sütununa taşıyor mu) · çakışma (CTA ↔ etiket ↔ ayraç) · ilk kare tam kanca mı · son kare ilk kareyle bağlanıyor mu · whip karelerinde siyah boşluk var mı · bulanıklık sızıntısı (`data-motion-blur` yok).
3. Kapılar: `kurgu_kontrol.py --goruntu VIDEO --kesimler <başlar> --yalniz-goruntu` (çıkış 0) · `ses_olc.py VIDEO --drop <sn> --muzik_stem …/muz_teslim.wav --kapi` (çıkış 0) · `npx hyperframes check --json` (hata 0; `timeline_track_too_dense`/`nested_structure` uyarıları üretici yapısından gelir, kabul).

## 7. TR / AB referans paketi — KALİTE SÜZGECİNDEN GEÇMİŞ (REF TR01–TR06, AB01–AB05; 2026-11-24)
Kaynak: Meta Reklam Kütüphanesi (aktif + uzun yayın). **Süzgeç sonucu:** kanıt vekili (gün + sayfa reklam sayısı) zanaatı ayırt etmiyor; 12 referanstan tam ÖĞRET 1 (AB03), dar ÖĞRET 3 (AB01 kanca+son kart, AB02 kutu açma, AB04 dönüşüm kancası), YALNIZ-DESEN 4 (TR01, TR04, TR06, AB05), AT 4 (TR02, TR03, TR05, ANTİ). Aşağıdakiler bu yüzden "kanıtlı kural" değil, etiketiyle verilir. Referanstan BİÇİM alınır, METİN/TEKLİF kopyalanmaz.
1. **Açılış** (dayanak AB02, AB03, AB04, TR01): ilk 0,5 sn'de ürün kadrajda ve hareket halinde; yazı en geç 0,5 sn'de. Yüz şart değil.
2. **Yazı** (ilke, kanıtlı kural değil): varsayılan kutulu/yüksek kontrastlı, tek mesajlı yazı → `ig_kutu`. `tek_kelime`/`karaoke` yalnız seslendirme varsa. `uzman_kutu` ("acil" siyah kutu) varsayılan DEĞİL (dayanakları AT). Konum platform güvenli alanından: kart öğeleri y ≤ 1330'da biter.
3. **Altyazı** (koşullu): konuşma varsa altyazı zorunlu ve kutulu → `iki_katman`; aynı anda en çok 2 yazı katmanı.
4. **Son kart** (`son_kart`, VARSAYIM, tek dayanak AB01): ürün + logo + tek eylem + yalnız DOĞRU olan tek güvence. Rozet metni mağazanın gerçek teklifi, varsayılan yok; "KAPIDA ÖDEME" yalnız mağaza sunuyorsa. Sürekli yayındaki reklamda "Nur HEUTE / Sadece bugün" gibi aciliyet = sahte aciliyet riski, uyum kontrolü olmadan yazılmaz.
5. **Ritim** (varsayım, ölçülmedi): ilk 3 sn'de en az 3 görsel değişim.
6. **Kanıt anı** (en sağlam; AB04 0,9 sn · AB02 0,9–3 sn · TR01 3 sn · AB03 6,5 sn): tek, SONUCU gösterir (ürünü değil), en geç 7. sn ya da sürenin ilk yarısı. Kanıt anında gerçek ürün görüntüsü yoksa video kör jüriye girmez.
7. **Dev fiyat** (`dev_fiyat`, AB04): yalnız doğrulanmış teklifte; hikâye hattı `fiyat_izin: true` ister.
Sağlık/utanç iddiası (TR02 sınıfı) şablonla çözülmez: iddia kapısı geçerli.
**Sete giriş eşiği (iki kapı birden, öneri):** kanıt (aynı kreatif ≥60 gün ve o kreatifi kullanan ≥3 reklam · ya da AB erişim bilgisi · ya da organik izlenme hesap ortancasının ≥5 katı; ana teklif kapıda ödeme/sağlık vaadiyse kanıt tek başına sayılmaz) + zanaat (9:16, 8–30 sn, ürün ≤1 sn'de, kanıt anı ilk yarıda, ≤2 yazı katmanı, sesli dosya elde, kör jüri zanaat medyanı ≥7). Yalnız birini geçen referans "YALNIZ-DESEN" ya da "zanaat kulvarı" olarak ayrı tutulur, kural kaynağı olmaz.
TR dili: büyük harfte i→İ, ı→I (`dil="tr"`); `str.upper()` kullanma (ölçüldü: "iki"→"IKI"). TR kancası ≤ 8 kelime (ön-üretim kartı kapısı), şablon kapısı ≤ 7.
