# Viral Ürün Ekibi

Tek liderli Türkçe e-ticaret ekibi (Claude Code eklentisi: skill + ajan ekibi). Uçtan uca tek hat:
**ürün bul → doğrula → teklif → Shopify mağazasını kur → kreatif üret → yayınla ve ölç.** Instagram'da viral ürünleri bulur,
AliExpress'te henüz viral olmamış benzerlerini avlar, mağazayı (marka, görsel, metin, kurulum, site denetimi) kurar, ChatGPT +
Google Flow ile ürün videosu üretir ve kurgular. İçinde yüzlerce ürün ve viral video analizinden damıtılmış bir bilgi bankası var.

Bu depo **açık kaynaktır** (MIT). Hata bildirimi, yeni skill, bilgi bankasına katkı — hepsi Pull Request ile kabul edilir.
Katkı kuralları: [CONTRIBUTING.md](CONTRIBUTING.md) · Geliştirici şartnamesi: [docs/SARTNAME.md](docs/SARTNAME.md)

## İçindekiler

**Skill'ler** (`plugins/viral-urun-ekibi/skills/`)

| Skill | Ne yapar |
|---|---|
| `ekip-lideri` | Ekibin TEK lideri ve tek girişi: işi doğru kola verir, `.ekip/` hafızasını tutar, kollar arası köprü dosyalarını yazar, eksik araçları kontrol eder. |
| `magaza-kurucu` | Mağaza kolu: ürün fotoğrafı + ülkeden ya da ekibin `urun-paketi.json` dosyasından Shopify mağazası (5 aşama: ürün analizi, marka, görseller, metinler, kurulum + site denetimi). Tema paketi yoksa temasız modda çalışır. |
| `kesfet-urun-avi` | Instagram Reels/Keşfet'te viral ürün videolarını izler, ölçütlerle ayıklar, tabloya ve Excel'e kaydeder (Mac: iPhone Yansıtma; her yerde: Chrome). |
| `aliexpress-firsat` | Viral ürünlerin ortak DNA'sından arama terimi üretir, AliExpress'te henüz viral olmamış adayları bulur ve "zaten viral mi" kontrolü yapar. |
| `ai-video-kreatif` | Ürün kartı, 30 senaryo, ChatGPT ile başlangıç kareleri ve Google Flow ile klip üretimi. |
| `video-kurgu` | ffmpeg ile kurgu: klip kalite kontrolü, ekran üstü yazı, efekt, ses normalizasyonu, teslim. |
| `reklam-kutuphanesi-avi` | Meta Reklam Kütüphanesi'nde niş niş (US/TR/AB) kazanan reklam ve ürün taraması; mağaza → AliExpress eşleme, kazanan–kaybeden desen sayımı. |
| `teklif-ve-sayfa` | Kazanan ürün için teklif, iniş sayfası, itiraz bankası ve e-posta taslağı; baskı/sahte indirim ifadesi denetçisi. |
| `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` | Hareketli tasarım katmanı (HeyGen'in açık kaynak HyperFrames beceri paketi, Apache-2.0, değiştirilmeden): HTML'den video — kinetik yazı, geçiş, overlay, altyazı, ~450 hazır blok; render yerelde Node 22+ ve Chrome ister. `video-kurgu` aşama 8b'de çağrılır. |

**Ajanlar** (`plugins/viral-urun-ekibi/agents/`, 27 üye): çekirdek ekip 7 (`video-juri` kör video jürisi, `firsat-avcisi`, `kanit-savcisi`, `icerik-stratejisti`,
`kreatif-analisti`, `video-elestirmen`, `ses-tasarimcisi`) + mağaza kolu 20 (marka, görsel, site, denetim). Her üyenin İngilizce
unvanı, adı, Türkçe rolü ve modeli: `plugins/viral-urun-ekibi/ortak/ekip.md`.

**Sözleşme** (`plugins/viral-urun-ekibi/ortak/sozlesme/` + `ortak/paket.py`): kollar arasında veri taşıyan üç dosyanın şeması,
örnekleri, doğrulayıcısı ve yazıcı-okuyucu betiği: `urun-paketi.json` (ürün → mağaza), `magaza-paketi.json` (mağaza → video),
`video-paketi.json` (video → mağaza). Alan tablosu: `arayuz-sozlesmesi.md`. Üretim yapmadan uçtan uca deneme: `python3 scripts/sozlesme_test.py`.

**Ortak bilgi** (`plugins/viral-urun-ekibi/ortak/`): marka skoru, viral DNA, sözlük ve `bilgi/` altında ürün kataloğu,
kreatif notlar, fırsat geçmişi, üretim deneyimi, dersler.

## Mağaza kolu nasıl çalışır?
- **Tek giriş:** "mağaza kur" da dahil her iş `ekip-lideri` ile başlar. Ürün ekipten geldiyse kanıt, rakipler ve onaylı teklif
  `urun-paketi.json` ile mağazaya taşınır; hiçbir şey yeniden sorulmaz. Doğrudan fotoğraf + ülke vermek de yeterlidir.
- **Fiyatın tek kaynağı:** teklif tablosunda `bizim` satırı varsa o; yoksa sabit kural (2'li %10, 3'lü %18).
- **Tema:** mağaza aşaması özel bir tema paketiyle (tam mod) çalışacak biçimde yazıldı; paket bu depoda yok. Paketin yoksa
  **temasız mod** devreye girer: ürün, metin, görsel, sayfalar ve indirim Shopify'a, mağazanın mevcut temasına yazılır; tema
  şablonu yazılmaz ve senden tema istenmez.
- **Shopify bağlantısı:** eklenti Shopify'ın uzak bağlantısını (`.mcp.json`) getirir; ilk kullanımda `/mcp` → shopify ile giriş yaparsın.
- **Video mağazayla aynı sistemde:** altyazı ve kapak mağazanın yazı ailesini ve renklerini kullanır; videoda yalnız mağazanın
  onaylı iddiaları söylenir (kapı: `kurgu_kontrol.py --magaza-paketi`).
- **Model:** lider en güçlü modelle çalışmalı: oturumu `/model fable` ile aç (yoksa opus). En güçlü model yalnız kör jüri, kök neden ve strateji rollerinde
  (`model: fable`; hesabında yoksa o dosyalarda `opus` yaz); hacimli işler `sonnet`, ölçülebilir her şey betik (`ortak/ekip.md`).
- Claude görsel üretmez: mağazanın görsel adımında görseller ChatGPT'de üretilip sohbete eklenir.

### Dosya zinciri (ürün → mağaza → video → mağaza)
```
ürün bulundu (SAT) ──urun-paketi.json──▶ mağaza kolu ──magaza-paketi.json──▶ video ekibi
                                              ▲                                   │
                                              └───────── video-paketi.json ───────┘
```
1. `AliExpress'ten ürün bul` → SAT kararını onayla → ekip `is/NN-urun-adi/urun-paketi.json` yazar (`ortak/paket.py urun-yaz`).
2. `Bu ürün için mağaza kur` → mağaza kolu fotoğraf + ülke sormadan başlar, sonunda `is/NN-urun-adi/magaza-paketi.json` verir.
3. `Bu ürüne video yap` → ekip mağaza paketini okur (`paket.py magaza-oku` → `marka-kilidi.md`): aynı renkler, aynı yazı ailesi,
   yalnız onaylı iddialar, mağaza linki. Teslimde `teslim/video-paketi.json` çıkar (`paket.py video-yaz`).
4. `pdp-galeri` / `hero` işaretli videolar ürün sayfası galerisine girer; `reklam` işaretliler mağazaya yüklenmez.

## Hangi yolu seçmeliyim?

| Yol | Ne yapabilir | Kim için |
|---|---|---|
| **A. Claude Code eklentisi** (önerilen) | Hattın tamamı: Instagram'da gezinme, AliExpress tarama, Shopify mağaza kurulumu ve site denetimi (27 ajanla), Flow'da üretim, ffmpeg ile kurgu. Hafıza kendiliğinden tutulur. Görseller ChatGPT'de üretilir. | Bilgisayarında Claude Code kurabilen herkes (Mac en iyisi, Windows destekli) |
| **B. claude.ai veya ChatGPT Projesi** | Sohbette bilgi bankasıyla ürün yorumu, viral analiz, 30 senaryo, prompt yazımı. Tarayıcı/kurgu yok veya sınırlı. | Hiç kurulum istemeyen herkes → `plugins/viral-urun-ekibi/ekler/proje-paketi/KURULUM.md` |
| **C. ChatGPT plugin** | 16 beceri (8 iş akışı + 7 ekip rolü + bilgi bankası) ChatGPT'de; betikler kod yorumlayıcıda. Mağaza kolu tam çalışır (görsel üretimi sohbette, Shopify ChatGPT'nin kendi bağlantısıyla, Çalışma modu şart). Tarayıcı, telefon ve Flow adımlarını kullanıcı yapar; alt ajan, oturum kancası ve hareketli tasarım yok; hafıza DURUM bloğu + DEVAM KARTI. | ChatGPT'de Plugins yükleme seçeneği olan herkes → aşağıdaki **C** bölümü (ZIP: `dist/viral-urun-ekibi-chatgpt.zip`) |

## A. Claude Code kurulumu (5 adım)

Ön koşul: Claude Pro, Max veya Ultra planı · Mac için `brew install ffmpeg` ve `python3 -m pip install --user openpyxl pillow imageio-ffmpeg numpy` · Google Chrome · Mac (Windows'ta iPhone modu yok, tarayıcı modu çalışır).

1. **Claude Code'u kur** ve claude.ai hesabınla giriş yap (`claude` → `/login`).
2. **Depo:** herkese açık; ayrı erişim gerekmez. Kendi çatalını (fork) kurmak istersen aşağıdaki yolu kendininkiyle değiştir.
3. **Ekibi kur** (Claude Code içinde):
   ```
   /plugin marketplace add armanvibecoding/viral-urun-ekibi-market
   /plugin install viral-urun-ekibi@viral-urun-market
   ```
   Mağaza kolu aynı eklentinin içindedir; ayrı kurulum yok. Güncellemeleri kendiliğinden almak için: `/plugin` → Marketplaces → Enable auto-update.
4. **Araç izinleri:**
   - Chrome'a "Claude" eklentisini kur, Claude Code'da `/chrome` ile bağla.
   - Mac + iPhone modu için: `/mcp` → computer-use → Enable; Sistem Ayarları'nda Erişilebilirlik ve Ekran Kaydı izni; iPhone Yansıtma'yı bir kez elle aç.
   - Windows: PowerShell'de sırayla `winget install Git.Git`, `winget install Python.Python.3.12`,
     `winget install Gyan.FFmpeg`, sonra `py -m pip install --user openpyxl pillow imageio-ffmpeg numpy`.
     Komutlarda `python3` yerine `py -3` kullanılır (`python3` yazmak Microsoft Store'u açar).
5. **Başlat:** boş bir klasör aç, içinde `claude` çalıştır ve yaz:
   ```
   /viral-urun-ekibi:ekip-lideri
   ```
   Ekip lideri hafıza klasörünü (`.ekip/`) kurar, eksik araçları kontrol eder ve sana pazarını (Türkiye/ABD) sorar.

## C. ChatGPT plugin

1. `dist/viral-urun-ekibi-chatgpt.zip` dosyasını indir (GitHub'da dosyaya tıkla → **Download raw file**). ZIP'i açma.
2. ChatGPT → **Plugins** → yükleme seçeneği. İş alanında: yönetici konsolu → **Plugins** → **Add** → **Upload plugin**. Seçenek yoksa **Plugins → Skills → Create → Upload** ile `skills/` altındaki klasörleri tek tek yükle (önce `ekip-bilgi` ve `ekip-lideri`). Kişisel hesapta hangi planın gerektiği belgelerde net değil.
3. Yeni sohbette yaz: `Ekibi başlat. Pazarım Türkiye.` → her cevabın sonunda DURUM bloğu çıkar; yeni sohbete geçerken onu yapıştır.

ChatGPT'de tarayıcı, telefon ve Google Flow adımlarını sen yaparsın (ekran görüntüsü/metin yüklersin); liste `ekip-lideri` becerisinin başında.
ZIP'i yeniden üretmek: `sh scripts/chatgpt_paketi_yap.sh`. Plugin yüklenemezse B yolu (Proje + talimat) aynı bilgi bankasıyla çalışır.

## Kullanım örnekleri
- "Instagram'dan bugün 20 viral ürün bul."
- "Bulduğumuz ürünlerin ortak noktasına göre AliExpress'ten 5 yeni ürün getir."
- "Şu ürün için ABD pazarına 30 video planı yap: <link>"
- "V01–V05'in kliplerini kurgula ve teslim et."
- "Bu ürün için mağaza kur. Ülke: Türkiye." (ürün fotoğrafını ekle)
- "SAT olan ürünü Shopify'a aç, sonra videosunu mağazanın renkleriyle yap."
- "Kurulu mağazayı denetle: hız, arama, erişilebilirlik, satın alma kutusu."
- "Nerede kalmıştık?"

## Hafıza nasıl çalışır?
Her proje klasöründe `.ekip/` vardır: `DURUM.md` (nerede kaldık, sıradaki adım), `KARARLAR.md` (verdiğin kararlar),
`DERSLER.md` (öğrenilen dersler). Oturum açıldığında veya sohbet sıkıştırıldığında bu dosyalar Claude'a otomatik
yeniden okutulur; yeni oturumda kaldığı yerden devam eder. Ürün çıktıları `is/` klasöründedir.

## Kırmızı çizgiler (ekip bunlara uyar)
- Flow kredisi, sipariş, reklam gibi para harcayan her adımdan önce onay ister.
- Şifre girmez; giriş ekranında sana devreder.
- Instagram'da takip, yorum, DM, satın alma yapmaz.
- Başka markaların logosunu videolarda kullanmaz; doğrulayamadığı sayıyı uydurmaz.

## Bilinen sınırlar
- iPhone modu yalnız Mac (macOS 15+, iPhone Yansıtma). Ekran noktaları ilk kullanımda kalibrasyon ister.
- Google Flow arayüzü değişirse otomatik yükleme bozulabilir; o durumda ekip senden tek bir sürükle-bırak ister.
- ChatGPT, kendi tarayıcı eklentisi modunda dosyaları Flow'a yükleyemez; ChatGPT ile video üretiminde bulut tarayıcıda Google girişi gerekir.

## Katkı
Yeni skill eklemek, mevcut olanı düzeltmek ya da bilgi bankasına ürün/ders eklemek için [CONTRIBUTING.md](CONTRIBUTING.md)'yi oku.
PR öncesi kısaca: `claude plugin validate plugins/viral-urun-ekibi` geçmeli, kişisel bilgi (ad, e-posta, mağaza, hesap,
mutlak yol, API anahtarı) içermemeli. Mağaza kolunun kaynağı `moduller/magaza-kurucu/`'dadır (`skills/magaza-kurucu/` oradan
üretilir, elle düzenlenmez): `python3 moduller/magaza-kurucu/tools/build.py --check`, `python3 -m pytest -q moduller/magaza-kurucu/tests`
ve `python3 scripts/sozlesme_test.py` de geçmeli. Taşıma kaydı: [docs/gelistirici/TASIMA-ESLEME.md](docs/gelistirici/TASIMA-ESLEME.md).

## Lisans
[MIT](LICENSE) — © viral-urun-ekibi contributors.
HyperFrames becerileri (`skills/hyperframes*`, `skills/media-use`) Apache-2.0 lisanslıdır (© HeyGen, Inc.): [THIRD_PARTY_NOTICES.md](plugins/viral-urun-ekibi/THIRD_PARTY_NOTICES.md).

---

## English summary
**Viral Ürün Ekibi** ("Viral Product Team") is a Turkish-language Claude Code plugin: a team of skills and sub-agents that
(1) scouts viral product videos on Instagram Reels/Explore, (2) finds not-yet-viral look-alikes on AliExpress using the
shared "viral DNA" of winners, (3) plans and generates AI product videos with ChatGPT (start frames) and Google Flow
(clips), (4) edits them with ffmpeg (QC, captions, SFX, loudness), and (5) builds the Shopify store for a validated product
(brand, gallery images, copy, setup and site audit) under one lead skill, with JSON bridge files between the product, store and video arms. It ships with a knowledge base distilled from
hundreds of analysed products and videos, and keeps per-project memory in a `.ekip/` folder.

Install inside Claude Code:
```
/plugin marketplace add armanvibecoding/viral-urun-ekibi-market
/plugin install viral-urun-ekibi@viral-urun-market
```
The store-building arm (`magaza-kurucu` skill) ships inside the same plugin; the arms exchange `urun-paketi.json` /
`magaza-paketi.json` / `video-paketi.json` files (schemas in `plugins/viral-urun-ekibi/ortak/sozlesme/`).
Then run `/viral-urun-ekibi:ekip-lideri` in an empty folder. User-facing text is Turkish; contributions in English are
welcome too. See [CONTRIBUTING.md](CONTRIBUTING.md). License: MIT.
