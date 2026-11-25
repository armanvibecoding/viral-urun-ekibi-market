# Danışan açığı raporu — eklenti neden danışanın bilgisayarında zorlanıyor (2026-11-25)

Kapsam: `plugins/viral-urun-ekibi/` + depo kökü `scripts/`. Yöntem: yalnız okuma. Yollar eklenti köküne göredir, ev dizini `~`.
Danışan kanıtı: iki saha dosyası (danışan geri bildirim özeti + kullanım bulguları, 23-24 Kas) ve bir danışanın eklenti çıktısındaki 4 sebep.

## Sonuç (5 satır)
1. Kurucu hipotezi KISMEN doğru: kod yolları büyük oranda temizlenmiş (mutlak ev dizini yolu yok, kurulum denetimi `ortak/on_ucus.py` var), asıl açık yolda değil VERİDE ve KARARDA: viral veritabanı, kurucunun iş kararları (kapıda ödeme yok, 399 TL tabanı, 2,2 kat) ve kurucunun hesapları/oturumları danışana varsayılan olarak gömülü geliyor.
2. Danışanı durduran 3 şey: (a) viral veri yok, her üründe `dogrulanamadi` (şu an DÜZELTİLİYOR), (b) danışanın kendi iş profili sorulmadan kurucunun profili varsayılan (YENİ, düzeltilmiyor), (c) danışan eski sürümle (0.4.0) çalıştı ve sürümünü/güncelini görmüyor (YENİ).
3. 8 şikâyetin hepsi 6 kök nedene bağlandı (aşağıda); 4'ü şu an ayrı ajanlarla düzeltiliyor, 4 yeni Ö1/Ö2 satırı kaldı.
4. Doğrudan "danışanın makinesinde kırılır" kod bağımlılığı az: OCR venv (`skills/cut/scripts/juri.py:158`), `--analiz-db` zorunlu (`juri.py:606`), macOS-özel radar betikleri (Windows'ta yok, belgelenmiş).
5. `bash scripts/anonim_kontrol.sh` çıkış 0 (rapor yazıldıktan sonra yeniden koşuldu).

## Kök nedenler (danışan şikâyetleri bunlara bağlanır)
| Kod | Kök neden |
|---|---|
| K1 | Veri: eklentiyle gelmeyen yerel veri (viral veritabanı `veri/analiz.db`, referans video panoları, tedarikçi/kare dosyaları) |
| K2 | Karar: kurucunun kişisel iş kararları danışanın varsayılanı olarak gömülü, danışanın profili sorulmuyor |
| K3 | Hesap/oturum: kurucunun açık oturumları varsayılıyor (Instagram, TikTok, Meta, ElevenLabs, ChatGPT, Flow) ve yedek yol zayıf |
| K4 | Ortam: kurulum gerektiren araçlar ve macOS'a özgü adımlar (kurulum anlatısı eksik/dağınık) |
| K5 | Sürüm/dağıtım: yanlış dosya, eski sürüm, güncelleme görünmezliği |
| K6 | Çıktı biçimi: ajan karar yükünü danışana bırakıyor, etiketler (SAT/İZLE) açıklanmıyor |

## A) Yerel bağımlılık taraması

### A1. Mutlak/ev dizini yolları
- Mutlak ev dizini yolları, kurucunun proje klasörü adı ve yerel ses aracı adı eklenti ve `scripts/` içinde bulunmadı (grep sıfır).
- `~/.local/share/viral-urun-ekibi/{ocr-venv,excel-venv,web-olcum}`: `ortak/on_ucus.py:168,195`, `ortak/excel_test.py:21`, `ortak/web_olcum.py:21`, `skills/cut/scripts/juri.py:158`, `skills/cut/scripts/juri_test.py:176`, `skills/builder/gorseller/scripts/ocr_kontrol_test.py:11`. Bunlar danışanda da aynı yolu kurar (makineye özgü değil, kurulum yolu); sorun yalnız venv yoksa sessiz düşmesi (D-04).
- `~/.cache/viral-urun-ekibi/sfx` (`skills/cut/scripts/hikaye/_arac.py:22`): ilk kullanımda üretilir, sorun yok.
- `~/.config/viral-urun-ekibi/yasak.txt` (`scripts/anonim_kontrol.sh:20-21`): yalnız yayıncı betiği, danışan çalıştırmaz; dosya yoksa çıkış 2 ile net hata veriyor.

### A2. Eklentiyle gelmeyen veri
| Veri | Nerede bekleniyor | Yoksa ne oluyor |
|---|---|---|
| `<proje>/veri/analiz.db` (viral veritabanı) | `skills/bazaar/SKILL.md:27`, `ortak/tarifler/06-trendyol-ve-aliexpress-avi.md:16`, `skills/bazaar/scripts/bazaar_kontrol.py:511-513` | UYARI basıp her satıra `dogrulanamadi`: sessiz değil ama sonuç: hiçbir ürün SAT olamaz (şikâyet 4) |
| `<proje>/veri/analiz.db` (jüri seti) | `skills/cut/scripts/juri.py:606` (`--analiz-db` zorunlu), `skills/captain/referans/hukum-hatti.md:18` | `VERİ YOK` çıkış 3: durur; danışan referans setini kuramaz |
| `analiz_db_aktar.py` (spy → proje veritabanı) | `skills/spy/SKILL.md:71,95` | İsteğe bağlı; yoksa atlanır, sorun değil |
| Referans kare panoları (`kareler/`, `referans-0.6/kareler/`) | `ortak/sinav/*/referanslar.tsv` | Yalnız sürüm öncesi sınav (`scripts/sinav_kos.py --referans-kok`); danışanı etkilemez |
| `.ekip/` hafızası | `hooks/durum-yukle.sh:6,13`, `skills/captain/SKILL.md:24` | Yoksa captain kurar; sorun yok |
| `is/arastirma/`, `is/kesfet/` | `ortak/roller/*/…`, `skills/radar/SKILL.md:20` | "yoksa arama, gömülü sayıyı kullan" kuralı var; sorun yok |
| `ortak/bilgi/*.md` (2140 satır) | `hooks/durum-yukle.sh:7` | Paketle GELİYOR, ama içeriği kurucunun Instagram/ABD ağırlıklı taraması; TR danışanı için zayıf (D-09) |
| `ortak/bilgi` kataloğu, `viral-dna.md` | Paketle geliyor | Sorun yok |

### A3. Kurulum gerektiren araçlar
| Araç | Anlatım | Yoksa |
|---|---|---|
| ffmpeg/ffprobe | `claude/README.md:35,43`, `skills/captain/referans/kurulum-kontrol.md:8`, `skills/cut/referans/kurulum.md:8` | `ortak/on_ucus.py:162` net hata + kurulum komutu; `ffaraclar.py:27` net hata. İYİ |
| Pillow, numpy, openpyxl, imageio-ffmpeg | README:35 | `on_ucus.py:166,190` ölçer. Ama 15 betik numpy ve Pillow içe aktarımıyla başlıyor, korumasız (ham Python içe aktarma hatası): `skills/cut/scripts/` ve `skills/builder/gorseller/scripts/` altındaki betikler (liste: `grep -rlE "^import numpy|^from PIL" skills`) |
| RapidOCR, Tesseract | README'de YOK; `on_ucus.py:166-171` ve `captain/referans/kurulum-kontrol.md` tablosunda satır YOK | `on_ucus.py` "olculemedi" yazar (geçti sayılmaz), betik venv'i sessizce arar |
| Node 22.19+, HyperFrames, Chrome | README:37, kurulum-kontrol.md:18 | `on_ucus.py:172-185` net hata |
| Lighthouse/axe | `web_olcum.py kur` | `on_ucus.py:196-199` net hata |
| Swift derleyici (iPhone modu) | kurulum-kontrol.md:14 | yalnız Mac iPhone modu |

### A4. MCP/hesap gerektiren adımlar
| Adım | Hesap | Yedek yol |
|---|---|---|
| Shopify | `.mcp.json` giriş | Yok: temasız mod var ama mağaza hesabı şart (belgeli, `claude/README.md`) |
| Meta Reklam Kütüphanesi | girişsiz | Chrome yoksa yok; Meta TR kapsamı sınırlı uyarısı çıktıda var |
| Instagram/TikTok izlenme | giriş ister | `dogrulanamadi-giris` + risk notu (`skills/bazaar/SKILL.md:28`); gerçek yedek yok (şikâyet 4) |
| Google Ads ve benzeri kanıt MCP | yalnız `ortak/mcp-kanit-araclari.md:2` "varsa kullan, yoksa web" | Yedek yazılı, sorun yok |
| ElevenLabs, ChatGPT, Flow | kullanıcı oturumu | Girişte durur (`skills/studio/SKILL.md:101`); README "Gereksinimler" bölümünde bu üç hesap ve kredi maliyeti listelenmiyor (D-10) |
| Reklam/test kanalı hesabı | yok | Hiçbir yerde "reklam hesabın yoksa/kapandıysa" yolu yok (şikâyet 8: Facebook hesabı gitti) |

### A5. Makineye özgü ayarlar
- `skills/radar/scripts/ortak.sh:14-30`, `ara.sh:10`, `yaz.py:37`: `osascript`, iPhone Yansıtma. Yalnız macOS; Windows'ta iPhone modu yok (README:42-44 belgeli, tarayıcı modu yedek).
- `skills/radar/scripts/kalibre.sh:11`: "Başlangıç değerleri tek bir iPhone'da ölçüldü" varsayılan koordinatlar; her çağrıda pencereden hesaplansa da başka iPhone modelinde ip.png ile doğrulama gerekir (D-12).
- `skills/studio/scripts/prompt_uret.py:121`, `skills/studio/referans/flow-ve-chatgpt.md:21`: `pbcopy` (macOS); Windows'ta dosyadan yapıştırma yedeği yazılı değil.
- `ortak/mobil_ekran.py`: Chrome yolu ortam değişkeni + macOS + PATH; Windows Chrome yolu (`C:\Program Files\…`) denenmiyor (D-13).

### A6. Kurucunun kişisel kararlarına/hafızasına atıf
- 91 dosyada "kurucu" geçiyor. Danışanın göreceği, içeriği eklentide olmayan atıflar:
  - `skills/cut/SKILL.md:71`, `skills/studio/SKILL.md:62,64`, `skills/captain/SKILL.md:47,107,111`: "aşım yalnız KURUCUNUN cümlesiyle", "veriyi kurucu girer". Danışan için "kurucu" kim? Kapı aşım yetkisi danışanın değil kurucunun gibi okunuyor.
  - `skills/bazaar/referans/tr-oranlari.tsv:6,7` (kapıda ödeme 0, `kurucu-karari`), `esikler.tsv:6,7,9` (kat ≥2,2; satış ≥399 TL; ROAS), `skills/bazaar/referans/olcutler.md:11`, `skills/bazaar/SKILL.md:8` ("kendi markalı Shopify mağazamızda", "satıcıyla iletişim kurucu kararıdır").
  - `ortak/kurallar.md:31`, `ortak/bilgi/dersler.md:105` ("ABD kültürü ≥1 unsur; kurucu kararı").
  - `KARARLAR.md` beklentisi: `hooks/durum-yukle.sh:13`, `skills/hunter/SKILL.md:20,22`, `agents/skeptic.md:21` (pazar yoksa dur). Burada atıf güvenli: dosya yoksa danışana sorar.
- `MASTER-PLAN`, `karne.md` atfı eklentide yok (temiz).

## B) Danışan şikâyetleri → kök neden
| Şikâyet | Kaynak | Kök neden |
|---|---|---|
| S1 SAT için net marj gerek, oranlar kaynaksız | danışan çıktısı sebep 1; saha 22:05, 22:25 | K2 + K1 (oran tablosu boştu; 0.5.0'da dolduruldu ama bir kısmı `varsayim`; danışan 0.4.0'daydı K5) |
| S2 alış = Trendyol perakende fiyatı | danışan çıktısı sebep 2 | K1/K2: tedarikçi (AliExpress/1688) adımı akışta zorunlu değildi; 0.5.0 `bazaar_kontrol.py:35,150-154,452-460` bunu yasaklıyor, danışan eski sürüm |
| S3 örneklem küçük (15 arama, 31 sayfa) | danışan çıktısı sebep 3; saha 22:29 "29/40 arama, 37/100 sayfa"; "25/25 hak doldu" | K2/K4: kota başka bir platformdan (AliExpress 15/40) kopyalanmıştı; `esikler.tsv:11-12` 100/300'e çıkarıldı, `skills/bazaar/SKILL.md:39-40` engel sinyaline bağlandı. Danışan eski sürümde |
| S4 viral veritabanı yok → her üründe dogrulanamadi | danışan çıktısı sebep 4; saha 22:05 | K1 (doğrudan) + K3 (girişsiz IG/TikTok) |
| S5 kurulum zip'i doğrulamadan geçmedi (18,8 kB) | saha 20:40 | K5 (yanlış dosya); README'ye uyarı eklendi (`claude/README.md:25`) |
| S6 SAT/İZLE etiketi kafa karıştırdı, "sen olsan nasıl seçerdin" | saha 23:06, 23:24 | K6 |
| S7 kör jüri 3 referans istedi, referans yoktu; "ekranlı plan yok" | saha 21:57 | K1 (referans kaynağı yok) + ürün tipi (düzeltildi: `kurgu_kontrol.py:221-227`) |
| S8 "plugin'le aradım böyle şeyler dedi" (beklenti dışı/düşük kalite sonuç) | danışan | K1 + K2 (ürün zevki/niş çeşitliliği kurucunun taramasından; TR verisi 1 milyon kayıtta zayıf, `tarifler/06:…`) + K6 |
| S9 "Facebook hesabım gitti, TikTok'ta mı test edeyim?" | danışan | K3: eklentide reklam hesabı olmadan/kapandıysa test kanalı yolu yok; `studio/referans/olcum-ve-test-plani.md` yalnız Instagram Insights varsayıyor |

## C) Şu an ayrı ajanlarla düzeltiliyor (tekrar önerilmiyor)
- DÜZELTİLİYOR: yalnız-SAT karar sistemi (`bazaar`/`hunter`) → S1, S2, S3, S6 bu işte kısmen kapanıyor.
- DÜZELTİLİYOR: sansürlü viral veri paketi (`ortak/bilgi/viral-urunler.tsv` + `ortak/viral_db.py`) → S4, `bazaar_kontrol.py viral` bağlantısı.
- DÜZELTİLİYOR: ROAS markaya özel (`esikler.tsv:9`, `olcutler.md:26`, `tr_marj.py`).
- Aşağıdaki tabloda bu üçüne bağlı satırlar "(DÜZELTİLİYOR)" ile işaretli ve yeni öneri içermez.

## Bulgu tablosu
Öncelik: Ö1 danışanı durduruyor · Ö2 kaliteyi düşürüyor · Ö3 kozmetik. Süre = bir geliştirici + sınama.

| # | Sorun | Kanıt | Danışana etkisi | Düzeltme önerisi (somut) | Öncelik | Süre |
|---|---|---|---|---|---|---|
| D-01 | Viral veritabanı yok, tüm ürünler `dogrulanamadi` | `skills/bazaar/SKILL.md:27`; `bazaar_kontrol.py:511-513`; S4 | Hiçbir ürün SAT olamaz | (DÜZELTİLİYOR: sansürlü veri paketi + `viral_db.py`) | Ö1 | — |
| D-02 | Yalnız-SAT karar sistemi, alış tedarikçiden | `bazaar_kontrol.py:35,150-154,452-460`; S1, S2, S6 | Danışan etiketi anlamıyor | (DÜZELTİLİYOR: bazaar/hunter) | Ö1 | — |
| D-03 | ROAS markaya özel | `esikler.tsv:9`; `olcutler.md:26` | Sabit eşik yanlış markaya | (DÜZELTİLİYOR) | Ö2 | — |
| D-04 | İş profili sorulmuyor: kurucunun kararları danışanın varsayılanı | `tr-oranlari.tsv:6-7` kapıda ödeme 0; `esikler.tsv:6-7` kat 2,2 / satış ≥399 TL; `olcutler.md:11`; `bazaar/SKILL.md:8` | Kapıda ödeme kullanan ya da 399 TL altı nişte çalışan danışanın tüm adayları yanlış etiketlenir; S1/S8 hissi | `captain` ilk oturumda 4 soru: kapıda ödeme var mı, hedef satış tabanı, hedef kat, mağaza adı/markası → `.ekip/KARARLAR.md` `profil` satırları; `bazaar_kontrol.py` ve `tr_marj.py` önce profili, yoksa tablo varsayılanını okur. `kurucu-karari` etiketlerini `varsayilan-profil` yap ve çıktıda "varsayılan profil kullanıldı" yaz | Ö1 | 0,5 gün |
| D-05 | Sürüm uyuşmazlığı: danışan 0.4.0 ile çalıştı, düzeltmeler 0.5.0'da | S5; S1-S3 | Çözülmüş hatayı yeniden görür, güveni düşer | `hooks/durum-yukle.sh` başına eklenti sürümünü yaz (`plugin.json`'dan); `captain` ilk mesajında "Sürüm 0.5.0" göstersin; README'ye "sürümünü `/plugin` listesinden kontrol et, eskiyse güncelle" satırı. claude.ai zip kullanıcıları için release notuna "otomatik güncelleme yok" uyarısı | Ö1 | 2 saat |
| D-06 | Kapı aşımı "kurucunun cümlesi" olarak yazılı; danışan kurucu değil | `skills/cut/SKILL.md:71`; `studio/SKILL.md:62,64`; `captain/SKILL.md:47,107,111` | Danışan "ben aşabilir miyim?" diye durur ya da bilmeden aşar | Danışana dönük metinde "kurucu" yerine "proje sahibi (sen)"; kurucu kararı gerekçeleri `ortak/kurallar.md`'de kalsın. Kapı mesajlarını (`juri.py:12`, `kapi.py`) "aşım için şu cümleyi yaz: …" biçimine çevir | Ö2 | 3 saat |
| D-07 | Jüri referans seti kaynağı yok; `set` komutu `analiz.db` ister | `juri.py:606`; `hukum-hatti.md:18`; S7 | Jüri çalıştırılamaz; teslim "jüri yapılamadı"da kalır | `juri.py set` için `--referans-klasoru` alternatifi (kullanıcının indirdiği 3 videoyu kare panosuna çevir) + yönerge; `yapilamadi` yolu zaten var (`cut/SKILL.md:71`), onu varsayılan akış yap | Ö2 | 0,5 gün |
| D-08 | Korumasız numpy/Pillow içe aktarımı (15 betik) | `skills/cut/scripts/` ve `skills/builder/gorseller/scripts/` betikleri | Betik ham Python içe aktarma hatası ile düşer; danışan ne kuracağını bilmez | Ortak `ortak/bagimlilik.py` içinde `gerek("numpy","pillow")` → Türkçe mesaj + kurulum komutu + çıkış 2; her betiğin ilk satırında çağır. Test: modülü gizleyen kırma testi | Ö2 | 0,5 gün |
| D-09 | `ortak/bilgi` (2140 satır) Instagram/ABD ağırlıklı, TR danışanı için zayıf | `ortak/bilgi/urun-katalogu.md` (930 satır, Keşfet taraması); `esikler.tsv:11` TR 1 milyon kayıt | Öneriler TR'de alakasız (S8) | README'de pazar kapsamını yaz ("katalog ABD/IG ağırlıklı, TR için ilk 20 üründen sonra kalibre"); `captain` pazar TR ise `bilgi/` yerine TR kaynaklarını öne çıkarsın | Ö2 | 2 saat |
| D-10 | README gereksinimleri eksik: ChatGPT, Flow, ElevenLabs hesabı/kredisi, Tesseract, RapidOCR, ffprobe, Swift | `claude/README.md:32-37`; `on_ucus.py:166-171` | Danışan işin ortasında "hesabım yok" diye durur | `claude/README.md` Gereksinimler'e "Hesaplar ve maliyet" tablosu (hangi kol hangi hesabı ister, kredi tavanı) + `on_ucus.py hepsi` komutunu "ilk iş" olarak göster; kurulum-kontrol.md tablosuna OCR/Tesseract satırı | Ö2 | 2 saat |
| D-11 | Reklam/test kanalı yedeği yok (Facebook hesabı kapandıysa) | `studio/referans/olcum-ve-test-plani.md:37,73`; S9 | Danışan test planını bilmez, "TikTok'ta mı?" diye sorar | `olcum-ve-test-plani.md`'ye "Kanal seçimi" bölümü: Instagram organik Reels, TikTok organik, TikTok Shop; her kanal için ölçülecek 3 sayı (3 sn tutma, paylaşım, link tıklaması) ve "reklam hesabı gerekmez" notu; `captain` ilk testte kanalı sorsun. Hesap kapanması/yasaklanması hakkında platform kurallarını ihlal edecek yönlendirme YOK (yeni hesap açma önerme) | Ö2 | 3 saat |
| D-12 | Radar iPhone koordinatları tek cihazda ölçülmüş | `skills/radar/scripts/kalibre.sh:11` | Başka iPhone/ekran oranında yanlış tıklar | `kalibre.sh` ilk çalıştırmada ip.png üzerinde 4 noktayı kullanıcıya doğrulatsın (onay yoksa konum.env yazılmasın) | Ö3 | 2 saat |
| D-13 | Windows Chrome yolu ve `pbcopy` yedeği yok | `ortak/mobil_ekran.py` (Chrome yolu); `studio/scripts/prompt_uret.py:121` | Windows danışanda mobil ekran ve pano adımı çalışmaz | `CHROME_YOLU` yoksa `%ProgramFiles%\Google\Chrome\Application\chrome.exe`'yi dene; `prompt_uret.py` `clip`/dosya yedeği | Ö3 | 1 saat |
| D-14 | Ajan karar yükünü danışana bırakıyor; tek gerekçeli öneri kuralı yalnız tarifte | S6 (saha 23:24); `tarifler/06:…` "Ben olsam" satırı | Danışan "neye göre seçeyim" der | `bazaar/SKILL.md` rapor şablonuna zorunlu son satır olarak taşı; çıktı kontrolüne ("Ben olsam:" satırı yoksa kapı kalır) ekle | Ö2 | 2 saat |
| D-15 | SAT/İZLE/SAT-ADAYI etiketi tek cümleyle anlatılıyor, danışan "satı niye karıştırdın" | S6 (saha 23:10); `bazaar/SKILL.md:64` | Etiket karışıklığı | Rapor başına 3 satırlık etiket sözlüğü ("SAT-ADAYI = tüm kapılar geçti, hâlâ ilk test gerekir"); etiket adını tek yerde sabitle (D-02 ile birlikte) | Ö2 | 1 saat |
| D-16 | Kota/ledger hatası bir arama hakkını yaktı | saha 22:29 | Günlük tarama erken biter | `kota iade` (`bazaar/SKILL.md:40`) 0.5.0'da var; danışan eski sürümde. Yeni iş yok: D-05 ile kapanır | Ö3 | — |
| D-17 | "kendi markalı mağazamızda" (bizim/biz dili) | `bazaar/SKILL.md:8` | Danışana kurucunun mağazasıymış gibi okunur | "senin Shopify mağazanda" | Ö3 | 15 dk |
| D-18 | Hook çıktısındaki sabit dil/ADHD biçimi ve "AD DEĞİŞİKLİĞİ (0.4.0)" satırı artık gereksiz | `hooks/durum-yukle.sh:8,9` | Her oturumda gereksiz bağlam | 0.5.0'da kaldır; sürüm satırıyla (D-05) değiştir | Ö3 | 15 dk |

## Önerilen sıra (tek günde Ö1)
1. D-05 sürüm görünürlüğü (2 saat). 2. D-04 iş profili sorusu (0,5 gün). 3. D-01/02/03 zaten ayrı ajanlarda; bitince D-04 ile birlikte uçtan uca koş. Sonra Ö2: D-08, D-07, D-10, D-14, D-15, D-09, D-11, D-06.

## Doğrulama
- `bash scripts/anonim_kontrol.sh` → çıkış 0.
- Bulgular dosya:satır ile açılabilir; grep sonuçları bu oturumda koşuldu. Sürüm 0.5.0 çalışma ağacında bazı dosyalar işlenmemiş (`git status` kirli, başka ajanlar çalışıyor); satır numaraları o anki içeriğe göredir.
