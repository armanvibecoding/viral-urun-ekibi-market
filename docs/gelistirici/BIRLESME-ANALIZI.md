# Birleşme analizi: Viral Ürün Ekibi (A) + Mağaza Kurucu (B)

**Sonuç:** Önerim (a): B'yi A deposuna tek beceri olarak (`magaza-kurucu`, yönlendirici + 5 aşama) taşımak. Ama önce köprü (2 JSON dosyası) kurulmalı, önce de kurucu anonimlik ve Master Tema kararını vermeli.
Tarih: 2026-11-18 · Yalnız analiz: iki depoda da dosya değişmedi (bu belge dışında), commit yok.
Ölçüm yöntemi her satırda yazıyor: **[okundu]** dosya açıldı · **[koşuldu]** komut çalıştı, çıkış kodu var · **[tahmin]** ölçülmedi.

> **Güncelleme (kurucu kararları sonrası):** uygulanacak plan → `docs/gelistirici/GOC-PLANI.md`. Bu belgedeki iki öneri değişti:
> (1) `git subtree` YOK. B'nin commit yazarı ve geçmişindeki kara liste eşleşmesi A'nın anonimliğini bozar; dosyalar geçmişsiz kopyalanır.
> (2) `magaza-kurucu` yönlendiricisi ikinci lider olarak kalmaz. Yönlendirme görevleri `ekip-lideri`'ne geçer, aşamalar `magaza-kurulumu` becerisinde (`user-invocable: false`) durur.
> §7'deki kararların bir kısmı verildi (birleştir, tek lider, A'nın ad kalıbı, B gizlenecek); kalanların uygulamadaki karşılığı planın §0'ında.

---

## 0. On satırlık özet
1. A: 11 beceri (4'ü HyperFrames, başka ajan ekliyor, commit'lenmedi) + 6 çalışma ajanı + 1 SessionStart hook'u + `.ekip/` hafızası. Claude Code öncelikli, ChatGPT ZIP'i 14 beceri. [okundu]
2. B: 5 aşama becerisi + yönlendirici (`src/tek/SKILL.md`), hook yok, ajanları yalnız geliştirme ekibi (25 rol, pakete girmez). ChatGPT öncelikli, hafıza sohbetteki DEVAM KARTI. [okundu]
3. B'deki birleşme arayüz sözleşmesi (`src/ortak/arayuz-sozlesmesi.md`) 3 dosya öngörüyor: `urun-paketi.json` → B → `magaza-paketi.json` → video → `video-paketi.json` → B. [okundu]
4. **A bu sözleşmeye bugün hiç uymuyor:** A'da bu üç dosya adını geçen tek satır yok (grep boş). Verinin çoğu A'da zaten var, yalnız yazan/okuyan betik eksik. [koşuldu]
5. Aynı adlı beceri ya da ajan yok. Aynı işi yapan iki şey var: fiyat/teklif (A `teklif-ve-sayfa` ↔ B `urun-analiz`), ürün sayfası metni (A `sayfa-iskeleti` ↔ B `metinler` + Master Tema haritası), yasak ifade listesi (iki ayrı liste). [okundu]
6. **En büyük engel anonimlik:** B, A'nın kara liste kapısından **49 satırla** geçemiyor (Master Tema / kaynak prompt dosya adı, hedef kullanıcı kelimesi, bir Windows ev yolu, bir masaüstü yolu). A'nın kendisi de şu an 8 satırla düşüyor; hepsi yeni HyperFrames dosyalarındaki İngilizce "masaüstü" kelimesi, yani yanlış alarm. [koşuldu]
7. İkinci engel: B'nin 5. aşaması özel bir tema zip'ine (Master Tema, yönetici verir, depoda yok) bağlı. A'nın herkese açık kullanıcısında bu zip olmayacak. [okundu]
8. ChatGPT'de birleşik ZIP yaklaşık 1,7 MB ve yaklaşık 15 beceri olur. Yerel betik, metin ve görsel üretimi çalışır. Hook, ajan, Chrome eklentisi, iPhone, HyperFrames ve yerel MCP çalışmaz. Shopify, ChatGPT'nin kendi Shopify eklentisiyle çalışır. [tahmin: boyut ölçüldü, yükleme denenmedi]
9. Seçenekler: (a) tek depo tek plugin 28–36 saat · (b) tek marketplace iki plugin + köprü 10–14 saat · (c) A'yı B'ye gömmek 40+ saat. [tahmin]
10. Kurucunun vereceği 5 karar §7'de. 1 ve 3 numaralı kararlar (anonimlik, tema) verilmeden taşıma başlamamalı.

---

## 1. Envanter

### 1a. Beceriler ve ajanlar
| | A: Viral Ürün Ekibi | B: Mağaza Kurucu |
|---|---|---|
| Beceri | `ekip-lideri`, `kesfet-urun-avi`, `aliexpress-firsat`, `reklam-kutuphanesi-avi`, `teklif-ve-sayfa`, `ai-video-kreatif`, `video-kurgu` + `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` (izlenmiyor, ekleniyor) | `urun-analiz`, `marka`, `gorseller`, `metinler`, `shopify-kurulum` + tek paket yönlendiricisi `magaza-kurucu` (`src/tek/`) |
| Çalışma ajanı | 6: `firsat-avcisi`, `kanit-savcisi`, `icerik-stratejisti`, `kreatif-analisti`, `video-elestirmen`, `ses-tasarimcisi` | yok. Roller aşama dosyalarının içinde (unvan yalnız durum satırında) |
| Geliştirme ajanı | yok | 25 rol, `.claude/agents/` (pakete girmez) |
| SKILL.md boyutu | 4,5–15,1 KB; `video-kurgu` 15.084 B, `ai-video-kreatif` 14.845 B [koşuldu] | hepsi ≤ 5.120 B; bu sınırı B kendisi koymuş (`tools/build.py` `SKILL_MAX_BAYT`), resmî bir sınır değil [okundu] |
| Hook | `SessionStart` → `hooks/durum-yukle.sh` (`.ekip/DURUM.md`, KARARLAR, DERSLER, açık geri bildirim satırlarını bağlama basar) | yok |

### 1b. Betikler, bağımlılıklar, MCP
| | A | B |
|---|---|---|
| Diller | Python 3 (~45 betik), sh (~12), Swift (2: iPhone tıklama), JS (4 tarayıcı enjeksiyonu), HyperFrames: Node `.mjs` | Python 3 (`duzelt.py`, `sablon.py`, `t4_yama.py`, `tools/build.py`, `tools/ocr_kontrol.py`) |
| Dış bağımlılık | ffmpeg, openpyxl, pillow, imageio-ffmpeg, numpy, Chrome + Claude eklentisi, computer-use (Mac + iPhone Yansıtma), HyperFrames için Node 22+ | Pillow (≥ 10, `sablon.py` için), OCR için isteğe bağlı RapidOCR + Tesseract `tur`, fontlar pakette (Anton, Barlow, OFL) |
| MCP | plugin `.mcp.json` yok. Claude in Chrome ve computer-use kullanıcı tarafında kurulu. Yerelde Meta ve ürün analizi MCP'leri var ama plugin'e bağlı değil | `.mcp.json`: Shopify `http` → `https://setup.shopify.com/mcp` (uzak HTTPS). ChatGPT'de Shopify'ın kendi eklentisi kullanılıyor |

### 1c. Hafıza, kurulum, ChatGPT, test, lisans, anonimlik
| | A | B |
|---|---|---|
| Hafıza | proje klasöründe `.ekip/` (DURUM, KARARLAR, DERSLER, GERI-BILDIRIM) + `is/` (çıktılar); ChatGPT'de DURUM bloğu | sohbette DEVAM KARTI + `devam-karti.md`, yani durumsuz. Yeni sohbette kartın yapıştırılması gerekiyor |
| Kurulum | Claude Code: `/plugin marketplace add …/viral-urun-ekibi-market` → `/plugin install viral-urun-ekibi@viral-urun-market` | ChatGPT Work: Skills › Upload `magaza-kurucu.zip`. Claude: claude.ai plugin zip'i ya da `claude plugin marketplace add …/magaza-kurucu` |
| ChatGPT paketi | `scripts/chatgpt_paketi_yap.sh`: hook → lider talimatı, 6 ajan → rol becerisi, `ortak/` → `ekip-bilgi`, `${CLAUDE_*}` → göreli yol, HyperFrames hariç. 14 beceri, 0,65 MB, 163 dosya [koşuldu] | `tools/build.py`: 5 skill zip'i + tek paket (yönlendirici + `<aşama>/ASAMA.md`) + `agents/openai.yaml` + `com.openai` arayüz manifesti (`.codex-plugin/`, kök `plugin.json`) |
| Test | `kendini_test.py` (video-kurgu, reklam-kutuphanesi-avi), `kirma_testi.py` (aliexpress-firsat, teklif-ve-sayfa), `geri_bildirim_kontrol.py`, `claude plugin validate` → **geçti** [koşuldu] | `pytest tests` → **60 geçti, 20 atlandı** (tema deposu yerelde yok); `build.py --check` → **GEÇTİ**, 11 uyarı (~10 KB üstü reference) [koşuldu] |
| Lisans | MIT, "viral-urun-ekibi contributors"; HyperFrames Apache-2.0 (HeyGen) | MIT, telif sahibi GitHub kullanıcı adıyla yazılı; fontlar OFL 1.1 |
| Anonimlik | kapı var: `scripts/anonim_kontrol.sh`, kara liste depo dışında (28 desen). Bugün **çıkış 1**, 8 satır, hepsi HyperFrames'teki İngilizce "masaüstü" kelimesi (yanlış alarm) | kapı yok, kimlik bilerek açık (yazar, depo, tema adı). A'nın kapısında **çıkış 1, 49 satır** [koşuldu] |
| GitHub | PUBLIC | PUBLIC. Son release **v0.3.6**, kaynak 0.4.1: danışmanın indirdiği zip eski [koşuldu] |

---

## 2. Örtüşme ve çakışma

### 2a. Aynı işi yapan iki şey
| Konu | A | B | Çakışma | Önerilen çözüm |
|---|---|---|---|---|
| Fiyat ve paket | `teklif-ve-sayfa`: rakip teklif deseni (n≥3) + pazar kuralı + marj ≥2× (`marj_hesap.py`) | `urun-analiz`: sabit kural 2'li %10, 3'lü %18 (gerekçeyle değişebilir), "fiyatı sorma, öner" | İki farklı fiyat çıkabilir | `teklif.tsv` içinde `bizim` satırı varsa o geçerli olur ve `urun-paketi.json`'a girer. B onu "onaylı değer" sayar (karar 4) |
| Ürün sayfası | `sablon/sayfa-iskeleti.md`: temadan bağımsız. Hero videosu, "kim için değil" satırı, `{TESLIM_GUN}` var | `metinler`: yalnız Master Tema bölümleri (`tema-haritasi-t4.md`), teslim süresi bilinmiyorsa yazılmaz | Master Tema varsa A'nın iskeleti boşa gider | Master Tema varsa sayfayı B'nin `metinler` aşaması yazar. A yalnız teklifi, iddia–kanıt listesini, SSS'yi ve e-postayı verir. Tema yoksa A'nın iskeleti kullanılır |
| Yasak ifade | `referans/yasak-ifadeler.tsv` (betik tarar: `teklif_kontrol.py tara`) | `01-kurallar.md` içinde düz metin liste ("doğal", "organik", "çok satan", "N bin müşteri"…) | İki liste, yalnız biri makineyle denetleniyor | B'nin kelimeleri A'nın TSV'sine girer. B'nin site metni de `tara` kapısından geçer |
| Eleştiri / QA | `video-elestirmen` (video, 2 mod), lider öz denetimi | çalışma zamanında `site-denetimi.md` (Adım 8) ve görsel `kabul-kontrolu.md`; geliştirmede `kor-elestirmen`, `gorsel-qa` | Konuları ayrı (video ↔ site/görsel), çakışma yok | İkisi de kalır. Ortak kural: "üretici kendini puanlamaz" |
| Görsel üretimi | `ai-video-kreatif`: ChatGPT'de başlangıç karesi, `kilit.txt` (ürün kilidi), kaynak önceliği: gerçek çekim > ürün fotoğrafı > AI | `gorseller`: ChatGPT'de galeri, ürün kilidi, tek zemin HEX'i, yazısız G0, "tek çağrı = tek görsel" | Aynı ürün için iki ayrı kilit tanımı | B çalıştıysa `magaza-paketi.json` `gorseller[G0]` video için ürün referansı olur. A'nın `kilit.txt`'si B'nin ürün kilidinden türetilir |

### 2b. Ad, unvan, sözlük ve biçim farkları
| Konu | A | B | Karar önerisi |
|---|---|---|---|
| Kullanıcıya hitap | "kullanıcı / kurucu", girişimci | "danışman", danışman bir müşterinin mağazasını kurar | Birleşik metinde "kullanıcı" (karar 2) |
| Ses | ekip var, unvanla anılır ("Creative Director (QA) eleştirdi") | tek ses, **"ekibimiz" yasak**, unvan yalnız durum satırında | Lider ve A becerileri ekip sesiyle konuşur. Mağaza aşamaları B'nin karakter bloğuyla (`ADIM n/8 · …`) kalır |
| Unvan çakışması | "Creative Director (QA)" = video eleştirmeni | "Kreatif Direktör" = marka kimliği | A'da unvan "Video Eleştirmeni (QA)" olur |
| Pazar kodu | sözlükte "TR / ABD"; teklifte `UK`; reklam avında Meta kodu `GB` | sözleşmede `{ "ulke": "US" }` (ISO) | Sözleşmede ISO-3166 (`GB`), arayüzde Türkçe ad |
| Niş | `reklam-kutuphanesi-avi/referans/nisler.md` kodları (kelime aileleri) | `nis-guzellik`, `nis-gadget` … (tema `templateSuffix`) | `urun-paketi.json` üretilirken eşleme tablosu kullanılır, yeni ortak sözlük gerekmez |
| Kanıt dili | Kanıt = URL + okunan değer + tarih; SAT / İZLE / ELE | doğrulanmış gerçek / `[DOĞRULA]`; sözleşmede `kaynak` alanı olan özellik doğrulanmış sayılır | A'nın kanıtı `ozellikler[].kaynak` ve `kanit[]` alanlarına taşınır |
| Mesaj biçimi | hook ADHD kurallarını basar (`ortak/adhd-kurallari.md`): "5 adımdan 3'ü bitti" | `00-calisma-tarzi.md` KARAKTER: 1. satır eylem, 2. satır durum, ≤5 madde, kod bloğu yok, son satır `Sonraki:` | Uyumlu, ikisi de ADHD dostu. Hook'a "mağaza aşamasında B biçimi" satırı eklenir |
| Hook | tek SessionStart | yok | Çakışma yok. Hook mağaza durumunu da (`is/*/magaza/devam-karti.md`) basabilir |

### 2c. Klasör ve hafıza çakışması
- İki tarafta aynı adlı dosya yok. B proje klasörüne bir şey yazmıyor (her şey sohbette), A ise `.ekip/` ve `is/` kullanıyor. Doğal yer `is/NN-urun/magaza/` olur: `devam-karti.md`, `urun-paketi.json`, `magaza-paketi.json`, `video-paketi.json`.
- Aynı adı taşıyan dosya: `00-calisma-tarzi.md` B'de 5 kopya (build kopyalıyor). A'da bu ad yok, çakışma yok.

---

## 3. Uçtan uca akış ve köprü

### 3a. Bugün (iki plugin ayrı)
| # | Adım | Kim | Elle aktarılan |
|---|---|---|---|
| 1 | Ürün bul, doğrula (SAT) | A: `kesfet` / `reklam-kutuphanesi-avi` → `aliexpress-firsat` + `kanit-savcisi` | — |
| 2 | Teklif | A: `teklif-ve-sayfa` | — |
| 3 | Mağaza kur | B: yalnız "fotoğraf + ülke" ister | **Ürün fotoğrafı ve ülke elle verilir. A'nın kanıtı, fiyatı, rakipleri kaybolur; B araştırmayı baştan yapar ve fiyatı yeniden önerir** |
| 4 | Kreatif üret | A: `ai-video-kreatif` → `video-kurgu` | **B'nin renkleri, başlık fontu, onaylı iddiaları ve ürün URL'si (UTM dahil) aktarılmıyor. Video kendi fontunu seçiyor ve onaylanmamış iddia söyleyebilir** |
| 5 | Yayın / öğrenme | A: `yayin_olc.py` (48. saat) | **Video Shopify galerisine elle yükleniyor. Ölçüm mağaza tarafına dönmüyor** |

### 3b. Birleşince köprü dosyaları
| Dosya | Üreten | Okuyan | A'da kaynak veri | Eksik |
|---|---|---|---|---|
| `urun-paketi.json` | A (yeni: `urun_paketi_yaz.py`, aliexpress-firsat ya da teklif-ve-sayfa sonunda) | B `urun-analiz` | ad: `adaylar.md` · fotoğraflar: Ali sayfası · tedarik fiyatı: `marj.csv` · pazar: KARARLAR · rakipler: `teklif.tsv` rakip satırları · kanıt: `kanit/NN-*.md` + reklam kaydı | `urun.nis` eşlemesi, kaynaklı `ozellikler[]`, `varyantlar[]` (kanıt dosyasında düzenli alan yok) |
| `magaza-paketi.json` | B `shopify-kurulum` sonu (zaten tanımlı) | A `ai-video-kreatif` (ürün referansı G0, kilit) + `video-kurgu` (altyazı rengi/fontu, onaylı iddialar, UTM) | — | A'da okuyucu betik yok. `kurgu_kontrol.py` "onaylı listede olmayan iddia = hata" kapısını bilmiyor |
| `video-paketi.json` | A `video-kurgu` teslim (yeni) | B `shopify-kurulum` (yalnız `pdp-galeri` / `hero`) | `is/NN/teslim/` dosyaları | yazıcı yok |

### 3c. Sözleşmenin öngördüğü ve A'nın uyumu
| Sözleşme kuralı | A bugün |
|---|---|
| Tek bağ dosya, MCP ya da ortak veritabanı yok | uyumlu (A da dosya tabanlı) |
| Para, fiyat ve onaylı metin dosyadan birebir taşınır | A'nın "uydurma yok" kuralıyla uyumlu ama uygulayan betik yok |
| Video yalnız `onayli_metinler.iddialar` listesini söyler | **uyumsuz:** A iddiaları kendi kanıt dosyasından alıyor, onaylı liste kavramı yok |
| Alan eklenirse `surum` artar, alan silinmez | A'nın teklif alanı eklenirse `surum: "2"` olur |
| Başka plugin'in görselini B yeniden üretmez | uyumlu |
| Uygulama oranı | **0 / 3 dosya** (A tarafında ne yazıcı ne okuyucu var) |

---

## 4. ChatGPT uyumu (birleşik ZIP)

### 4a. Ne çalışır, ne çalışmaz
| Parça | ChatGPT'de | Not |
|---|---|---|
| Beceri metinleri, references, ekip bilgi bankası | çalışır | A'nın paketleyicisi `${CLAUDE_*}` değişkenlerini zaten nötr yola çeviriyor |
| Python betikleri (kod aracı) | çoğu çalışır | `duzelt.py`, `t4_yama.py`, `teklif_kontrol.py`, `marj_hesap.py`, `senaryo_kontrol.py`. ffmpeg 7.x var (A SARTNAME, ölçülmüş). `sablon.py` Pillow ≥ 10 ister |
| Görsel üretimi (B galeri, A başlangıç karesi) | çalışır, ChatGPT'de Claude'dan **daha iyi** | Claude görsel üretmez. B de A da ChatGPT'yi buna kullanıyor |
| Shopify yazma | çalışır (ChatGPT'nin Shopify eklentisiyle) | Her mutation onay penceresi açar (B: tahmin 20–40). `.mcp.json` ChatGPT'de kullanılmaz |
| Hook (SessionStart) | çalışmaz | paketleyici lider başına talimat koyar. Hafıza DURUM bloğu + DEVAM KARTI |
| Ajanlar | çalışmaz | rol becerisine dönüşür (A: 6 rol becerisi) |
| Claude in Chrome / computer-use / iPhone | çalışmaz | kullanıcı yapar ya da ChatGPT ajan tarayıcısı. Flow'a dosya yükleyemiyor (A, ölçülmüş) |
| HyperFrames (4 beceri) | pakete girmez | Node 22+, Chrome ve CLI ister. A paketleyicisi zaten hariç tutuyor |
| Yerel MCP (Meta, ürün analizi) | çalışmaz | ChatGPT yalnız uzak HTTPS MCP kabul eder. Shopify uzak HTTPS olduğu için sorun değil |

### 4b. Sayı ve boyut
| Ölçü | Değer | Kaynak |
|---|---|---|
| A ChatGPT ZIP'i | 652.769 B, 163 dosya, 14 beceri | [koşuldu] |
| B beceri ağacı (zip) | ~1,03 MB, 79 dosya (fontlar ve stil çapası görselleri ~1 MB) | [koşuldu: geçici deneme zip'i] |
| Birleşik tahmin | ~1,7 MB, ~240 dosya, 15 beceri (A 14 + `magaza-kurucu` tek beceri) | [tahmin] |
| Resmî sınırlar | beceri sayısı, ZIP boyutu ve SKILL.md boyutu için resmî sınır **bulunamadı**. B 25 MB'lık güvenli bir tavan ve SKILL.md ≤ 5 KB kuralını kendisi koymuş | [DOĞRULA] |
| Yükleme yolu | B: Skills › Upload tek skill zip'i (gerçek koşuyla denendi, 0.3.x). A: Plugins › Upload. B'nin notu: "plugin zip'i Skills'e büyük olasılıkla reddedilir" | [DOĞRULA: birleşik plugin ZIP'i yüklenmedi] |

### 4c. ChatGPT'ye özgü riskler
1. **Tetik çakışması:** B "iki kopya aynı isteğe birlikte tetiklenir" sorununu yaşamış. "Ürün sayfası" ve "landing" A'nın `teklif-ve-sayfa` becerisini, "ürün açıklaması" ve "SSS" B'nin `metinler` aşamasını tetikliyor. B tek beceri olarak girerse (aşamalar `ASAMA.md`, frontmatter'sız) risk küçülür.
2. **Manifest:** A'nın ChatGPT manifestinde `interface` (displayName, defaultPrompt) yok, B'de var. Birleşikte B'nin `com.openai` arayüz deseni alınmalı.
3. **Dizin yayını için eksikler** (B KURULUM): ikon, gizlilik URL'si, ≤ 30 karakter kısa açıklama.
4. **Çalışma modu:** B yalnız Work modunda çalışıyor (test14: Sohbet modunda şablonlar okunmadı). A'nın ChatGPT yolu bunu zorunlu tutmuyor. Birleşikte Work zorunlu olur.

---

## 5. Birleştirme seçenekleri

| | (a) Tek plugin, tek depo (A deposu ev sahibi) | (b) Tek marketplace, iki plugin + köprü | (c) A'yı B'ye gömme (B deposu ev sahibi) |
|---|---|---|---|
| Ne | B kaynağı `moduller/magaza-kurucu/` altına taşınır (`git subtree`, geçmiş korunur). B'nin build'i `plugins/viral-urun-ekibi/skills/magaza-kurucu/` tek becerisini üretir. Tek ZIP, tek giriş (`ekip-lideri`) | A marketplace'ine B plugin girdisi eklenir (GitHub kaynağı). İki ayrı plugin, iki ayrı ChatGPT yüklemesi, ortada 3 JSON | B'nin 5 KB kuralı ve tek-ses karakteri altına A'nın 11 becerisi girer |
| Artı | Kurucunun istediği tek kurulum · tek lider, tek hafıza · köprü dosyaları aynı `is/NN/` klasöründe, elle taşıma yok · danışman yolu (`magaza-kurucu.zip`) aynı kaynaktan yan ürün olarak sürer | Az iş, düşük risk · anonimlik kapısı bozulmaz (B ayrı depoda kalır) · B'nin danışman kitlesi hiç etkilenmez | B'nin ChatGPT disiplini (boyut, tek ses) tüm pakete yayılır |
| Eksi | Anonimlik temizliği şart (49 satır) · iki farklı build sistemi bir depoda · B'nin tema zip'i herkese açık kullanıcıda yok | "Tek plugin" isteğini karşılamaz · ChatGPT'de iki ayrı yükleme, iki ayrı hafıza biçimi · tetik çakışması iki plugin arasında yine var | A'nın 15 KB'lık becerileri ve hook'u B kurallarına sığmaz · A'nın Claude Code ağırlıklı işleri (iPhone, Chrome, ffmpeg) B'nin ChatGPT öncelikli yapısına ters · mevcut A kullanıcılarının kurulumu kırılır |
| İş | **28–36 saat** [tahmin] | **10–14 saat** [tahmin] | **40+ saat** [tahmin] |
| Risk | orta (anonimlik ve ChatGPT yüklemesi doğrulanmadı) | düşük | yüksek |

**Önerim: (a), iki fazda.**
- **Faz 1 = (b)'nin köprü işi** (§6 adım 2–4): değeri hemen gelir, (a)'ya da (b)'ye de yarar, geri alınması kolay.
- **Faz 2 = taşıma.** Kararlar 1 ve 3 verildikten sonra başlar.

Gerekçe:
1. Giriş, hafıza, hook ve kullanıcısı olan marketplace A'da.
2. B zaten tek beceri paketi (yönlendirici + aşamalar) üretiyor ve bu paket ChatGPT'de gerçek koşuyla denenmiş. Bu yüzden B'yi parçalamadan tek beceri olarak almak en az kırılma demek.
3. Eklentinin adı (`viral-urun-ekibi`) değişmezse mevcut A kullanıcılarının `.ekip/` klasörü ve beceri önekleri olduğu gibi çalışır.

---

## 6. Önerilen birleşik yapı

### 6a. Klasör ağacı
```
viral-urun-ekibi-market/
├── .claude-plugin/marketplace.json          (tek plugin: viral-urun-ekibi 0.2.0)
├── .claude/agents/                          (B'nin 25 geliştirme rolü; pakete girmez; anonim temizlikten geçer)
├── moduller/magaza-kurucu/                  (B kaynağı: skills/ src/ tools/ tests/ config/; git subtree)
│   └── tools/build.py                       (yeni hedef: ../../plugins/viral-urun-ekibi/skills/magaza-kurucu/ + dist/magaza-kurucu.zip)
├── plugins/viral-urun-ekibi/
│   ├── .claude-plugin/plugin.json           (0.2.0)
│   ├── .mcp.json                            (YENİ: Shopify http https://setup.shopify.com/mcp)
│   ├── hooks/                               (aynı; + mağaza DEVAM KARTI satırı)
│   ├── agents/                              (6 ajan aynı; video-elestirmen unvanı "Video Eleştirmeni (QA)")
│   ├── ortak/                               (sozluk.md + 4 terim: onaylı iddia, magaza-paketi, niş eşlemesi, ISO pazar kodu)
│   ├── sozlesme/                            (YENİ: arayuz-sozlesmesi.md TEK kaynak + 3 örnek JSON + şema testi)
│   └── skills/
│       ├── ekip-lideri/                     (yönlendirme tablosuna "mağaza kur" satırı + 2 yeni kapı)
│       ├── kesfet-urun-avi/ aliexpress-firsat/ reklam-kutuphanesi-avi/   (aynı; aliexpress-firsat SAT sonunda urun-paketi.json)
│       ├── teklif-ve-sayfa/                 (teklif + iddia–kanıt + SSS + e-posta; Master Tema varsa sayfa metni magaza-kurucu'ya)
│       ├── magaza-kurucu/                   (ÜRETİLEN: yönlendirici SKILL.md + urun-analiz/ marka/ gorseller/ metinler/ shopify-kurulum/ ASAMA.md)
│       ├── ai-video-kreatif/                (magaza-paketi.json varsa G0 + kilit + onaylı iddialar)
│       ├── video-kurgu/                     (magaza-paketi okuyucu + video-paketi yazıcı + iddia kapısı)
│       └── hyperframes*/ media-use/         (öbür ajanın işi, dokunulmaz)
└── docs/ (anonim_kontrol.sh, chatgpt_paketi_yap.sh → magaza-kurucu'yu dönüştürmeden kopyalar)
```

### 6b. Silinen, birleşen, yeniden adlanan
| Öğe | İşlem |
|---|---|
| B'nin 5 ayrı Claude becerisi | birleşik plugin'de tek `magaza-kurucu` becerisi olur (B'nin tek paketiyle aynı). Ayrı 5 skill zip'i yalnız eski danışman yolu için `dist/`'te kalabilir |
| B `01-kurallar.md` yasak kelimeleri | A `teklif-ve-sayfa/referans/yasak-ifadeler.tsv`'ye taşınır. Metin listesi TSV'ye atıf olur |
| `arayuz-sozlesmesi.md` (B'de 3 kopya) | `plugins/viral-urun-ekibi/sozlesme/` tek kaynak olur. B build'i oradan kopyalar |
| A `sayfa-iskeleti.md` | kalır; yalnız "tema yok" modunda kullanılır |
| Kaldırılan | hiçbiri. Kural ve dosya silinmez; yalnız yönlendirme değişir |

### 6c. Hafıza ve giriş noktası
- **Tek giriş:** `viral-urun-ekibi:ekip-lideri`. "Mağaza kur" isteği, `is/NN/` ürünü SAT ise `urun-paketi.json` yazıldıktan sonra `magaza-kurucu`'ya yönlenir. Kullanıcı doğrudan fotoğraf + ülke verirse `magaza-kurucu` tek başına çalışır (B'nin bugünkü davranışı).
- **Hafıza:** `.ekip/` aynı kalır. Mağaza durumu `is/NN-urun/magaza/devam-karti.md` dosyasında tutulur (B'nin kart biçimi birebir). `DURUM.md`'ye tek satır eklenir: `Mağaza: <aşama> · is/NN/magaza/devam-karti.md`. ChatGPT'de DURUM bloğu ve DEVAM KARTI birlikte verilir.
- **Yeni kapılar** (KARARLAR'da yoksa, yalnız mağaza işinin başında sorulur): tema zip'i var mı (ad ve sha256 `config/tema.json` ile karşılaştırılır) · Shopify bağlı mı · hedef tema `UNPUBLISHED` mi (B'nin kuralı).
- **Ad ve sürüm:** plugin adı `viral-urun-ekibi` kalır (önek ve kurulum komutu değişmez), sürüm `0.2.0`, sözleşme `surum: "1"` (teklif alanı eklenirse `"2"`). `magaza-kurucu` modülünün kendi sürümü (0.4.x) `ASAMA` başlığında korunur.

### 6d. Migration adımları (her biri doğrulanabilir)
| # | Adım | Doğrulama (çıktı) |
|---|---|---|
| 0 | HyperFrames ajanının işi commit'lenir (A'da şu an 8 değişmiş + 6 izlenmeyen yol var). Birleşme ayrı dalda yapılır | `git status --short` boş · `claude plugin validate plugins/viral-urun-ekibi` geçer |
| 1 | Kurucu kararları (§7) `.ekip/KARARLAR.md`'ye yazılır | 5 satır |
| 2 | A'ya `urun_paketi_yaz.py` eklenir (SAT kanıtı + adaylar + marj + teklif → JSON) ve örnek veriyle kırma testi yazılır | test çıkışı 0 · zorunlu alanı silinen örnek → çıkış 1 |
| 3 | A'ya `magaza_paketi_oku.py` eklenir; `kurgu_kontrol.py`'ye "onaylı listede olmayan iddia = hata" kapısı girer | kırma testi: listede olmayan iddia → çıkış 1, listede olan → 0 |
| 4 | `video-kurgu` teslimde `video-paketi.json` yazar | şema testi 0 · B tarafında `shopify-kurulum` yalnız `pdp-galeri`/`hero` seçer (örnek dosyayla) |
| 5 | B kaynağı `moduller/magaza-kurucu/` altına `git subtree add` ile alınır | `python3 moduller/magaza-kurucu/tools/build.py --check` → GEÇTİ · pytest 60 geçti / 20 atlandı (bugünkü taban) |
| 6 | build.py'ye birleşik hedef eklenir (`skills/magaza-kurucu/`, `agents/openai.yaml` hariç); sözleşme tek kaynaktan kopyalanır | `claude plugin validate` geçer · Claude Code'da `viral-urun-ekibi:magaza-kurucu` listelenir |
| 7 | Anonimlik temizliği: tema adı, kaynak prompt dosya adı, hedef kullanıcı kelimesi nötrleşir; Windows yolu kaldırılır (`OCR_TESSDATA` zorunlu olur); masaüstü test yolu ortam değişkenine geçer; HyperFrames yanlış alarmı için kurucu kendi kara listesini daraltır (liste depoda değil) | `sh scripts/anonim_kontrol.sh` → çıkış 0 |
| 8 | `ekip-lideri` yönlendirme ve kapıları, `hafiza-sablonlari.md`'ye `is/NN/magaza/`, `teklif-ve-sayfa`'ya tema modu kuralı, yasak ifadeler TSV'ye eklenir | `teklif_kontrol.py tara` B'nin örnek site metninde çıkış 0 · yeni tetik çakışma testi (beceri açıklamalarındaki tetik cümleleri kesişmiyor) çıkış 0 |
| 9 | Plugin köküne `.mcp.json` (Shopify) eklenir | validate geçer · Claude Code `/mcp`'de shopify listelenir |
| 10 | `chatgpt_paketi_yap.sh` `magaza-kurucu`'yu dönüştürmeden alır; manifest `com.openai` arayüzünü alır | ZIP üretilir · `${CLAUDE_` kapısı 0 · beceri sayısı 15 · boyut ≤ 2 MB |
| 11 | Danışman yolu: `dist/magaza-kurucu.zip` aynı kaynaktan üretilir. B deposu README'si yeni yere yönlendirir (kurucu kararı 5) | eski release'e göre yeni zip'in sha256'sı farklı · Releases'te 0.4.1+ var |
| 12 | Uçtan uca gerçek koşu (Claude Code + ChatGPT Work): 1 SAT ürünü → `urun-paketi` → mağaza (UNPUBLISHED tema) → `magaza-paketi` → altyazılı video → `video-paketi` → galeriye yükleme | 3 JSON dosyası `is/NN/magaza/` içinde · Shopify ürün gid'i · galeride video var · kurucunun gözle onayı |

### 6e. Test ve kapılar (birleşik depoda her PR'da)
1. `sh scripts/anonim_kontrol.sh` → 0
2. `claude plugin validate plugins/viral-urun-ekibi` ve `claude plugin validate .` → geçer
3. `python3 moduller/magaza-kurucu/tools/build.py --check` + `pytest moduller/magaza-kurucu/tests` → geçer
4. A'nın mevcut kapıları: `kendini_test.py` (video-kurgu, reklam-kutuphanesi-avi), `kirma_testi.py` (aliexpress-firsat, teklif-ve-sayfa)
5. Yeni: sözleşme şema testi (3 örnek JSON, iki tarafın okuyucu ve yazıcısıyla) + tetik çakışma testi + ChatGPT paketi kapısı (beceri sayısı, boyut, `${CLAUDE_`)

### 6f. Geriye dönük uyumluluk
| Kim | Ne olur |
|---|---|
| Mevcut A kullanıcısı (`.ekip/` var) | plugin adı aynı olduğu için `/plugin` güncellemesi yeter. `.ekip/` biçimi değişmez; yeni satırlar isteğe bağlı. `magaza-paketi.json` yoksa video akışı bugünkü gibi çalışır |
| Mevcut B danışmanı (ChatGPT) | `magaza-kurucu.zip` aynı adla üretilmeye devam eder; davranış değişmez. Yeni sohbette DEVAM KARTI yapıştırma aynı |
| B'yi Claude'da marketplace'ten kuran | `magaza-kurucu@magaza-kurucu` B deposunda kalırsa çalışır. Arşivlenirse README yönlendirir. Önek değişir (`magaza-kurucu:` → `viral-urun-ekibi:magaza-kurucu`) |
| Sözleşme | `surum: "1"` alanları silinmez; B'nin "sözleşme dışı alan okunmaz" kuralı korunur |

---

## 7. Kurucuya sorulacak kararlar (5)
1. **Anonimlik:** B'nin içeriği (tema adı, kaynak prompt adı, "danışman" kelimesi, kişisel yollar) A'nın herkese açık, anonim deposuna girecek. Önerim: birleşik pakette nötr adlar ("tema paketi", "kullanıcı") ve kapının zorunlu olması. Alternatif: B'nin kimliği açık kalsın, A'nın anonimliğinden vazgeçilsin.
2. **Hedef kullanıcı ve ses:** birleşik plugin kime konuşacak, girişimciye mi danışmana mı? Önerim: "kullanıcı". A becerileri ekip sesiyle, mağaza aşamaları B'nin tek ses ve durum satırı biçimiyle konuşur.
3. **Master Tema bağımlılığı:** tema zip'i olmayan herkese açık kullanıcı için ne olacak? Seçenekler: (önerim) "temasız mod": ürün, sayfa, metin ve görsel Shopify'a yazılır, tema şablonu yazılmaz, A'nın sayfa iskeleti kullanılır · ya da mağaza aşaması yalnız tema sahiplerine açık olur · ya da tema da açık dağıtılır.
4. **Fiyat önceliği:** A'nın rakip desenine ve marja dayanan teklifi mi, B'nin sabit paket indirimi (2'li %10, 3'lü %18) mi? Önerim: `teklif.tsv` içinde `bizim` satırı varsa o geçer, yoksa B'nin kuralı.
5. **Ad ve B deposunun akıbeti:** plugin adı `viral-urun-ekibi` kalsın mı (önerim: evet, mevcut kurulumlar kırılmaz)? B deposu arşiv + yönlendirme mi olsun, ayrı yayın mı sürsün? Not: B'nin son release'i v0.3.6, kaynak 0.4.1; danışman eski zip'i indiriyor.

---

## Ek: ölçüm kaynakları
- Anonimlik: `sh scripts/anonim_kontrol.sh <B yerel kopyası>` → çıkış 1, 49 satır · `sh scripts/anonim_kontrol.sh` (A) → çıkış 1, 8 satır (HyperFrames). Eşleşen desenler bu belgeye yazılmadı (kara liste kimliği ele verir).
- B: `python3 tools/build.py --check` → GEÇTİ (11 uyarı) · `pytest -q -p no:cacheprovider tests` → 60 geçti, 20 atlandı.
- A: `claude plugin validate plugins/viral-urun-ekibi` → geçti · `unzip -l dist/viral-urun-ekibi-chatgpt.zip` → 163 dosya.
- GitHub: `gh repo view` → iki depo da PUBLIC; B'nin son release'i v0.3.6.
- Saat tahminleri ölçülmedi; iki deponun dosya ve betik sayısından çıkarıldı.
