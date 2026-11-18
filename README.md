# Viral Ürün Ekibi

Instagram'da viral ürünleri bulan, AliExpress'te henüz viral olmamış benzerlerini avlayan, ChatGPT + Google Flow ile
ürün videosu üreten ve videoları kurgulayan Türkçe bir Claude Code eklentisi (skill + ajan ekibi). İçinde yüzlerce ürün
ve viral video analizinden damıtılmış bir bilgi bankası var.

Bu depo **açık kaynaktır** (MIT). Hata bildirimi, yeni skill, bilgi bankasına katkı — hepsi Pull Request ile kabul edilir.
Katkı kuralları: [CONTRIBUTING.md](CONTRIBUTING.md) · Geliştirici şartnamesi: [docs/SARTNAME.md](docs/SARTNAME.md)

## İçindekiler

**Skill'ler** (`plugins/viral-urun-ekibi/skills/`)

| Skill | Ne yapar |
|---|---|
| `ekip-lideri` | Ekibi yönetir, `.ekip/` hafızasını kurar ve tutar, eksik araçları kontrol eder. Her oturumun girişi. |
| `kesfet-urun-avi` | Instagram Reels/Keşfet'te viral ürün videolarını izler, ölçütlerle ayıklar, tabloya ve Excel'e kaydeder (Mac: iPhone Yansıtma; her yerde: Chrome). |
| `aliexpress-firsat` | Viral ürünlerin ortak DNA'sından arama terimi üretir, AliExpress'te henüz viral olmamış adayları bulur ve "zaten viral mi" kontrolü yapar. |
| `ai-video-kreatif` | Ürün kartı, 30 senaryo, ChatGPT ile başlangıç kareleri ve Google Flow ile klip üretimi. |
| `video-kurgu` | ffmpeg ile kurgu: klip kalite kontrolü, ekran üstü yazı, efekt, ses normalizasyonu, teslim. |
| `reklam-kutuphanesi-avi` | Meta Reklam Kütüphanesi'nde niş niş (US/TR/AB) kazanan reklam ve ürün taraması; mağaza → AliExpress eşleme, kazanan–kaybeden desen sayımı. |
| `teklif-ve-sayfa` | Kazanan ürün için teklif, iniş sayfası, itiraz bankası ve e-posta taslağı; baskı/sahte indirim ifadesi denetçisi. |
| `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` | Hareketli tasarım katmanı (HeyGen'in açık kaynak HyperFrames beceri paketi, Apache-2.0, değiştirilmeden): HTML'den video — kinetik yazı, geçiş, overlay, altyazı, ~450 hazır blok; render yerelde Node 22+ ve Chrome ister. `video-kurgu` aşama 8b'de çağrılır. |

**Ajanlar** (`plugins/viral-urun-ekibi/agents/`): `firsat-avcisi`, `kanit-savcisi`, `icerik-stratejisti`,
`kreatif-analisti`, `video-elestirmen`, `ses-tasarimcisi`.

**Ortak bilgi** (`plugins/viral-urun-ekibi/ortak/`): marka skoru, viral DNA, sözlük ve `bilgi/` altında ürün kataloğu,
kreatif notlar, fırsat geçmişi, üretim deneyimi, dersler.

## Birleşik kurulum: Viral Ürün Ekibi + Mağaza Kurucu (tek sayfa)

Bu pazarda iki eklenti var. Her biri tek başına çalışır; birlikte kurulursa ürün bulmadan mağazaya, mağazadan videoya dosyayla bağlanır.

| Eklenti | Ne yapar | Kaynak |
|---|---|---|
| `viral-urun-ekibi` | Viral ürün bulur, AliExpress'te fırsat avlar, AI video üretir ve kurgular | bu depo (`plugins/viral-urun-ekibi/`) |
| `magaza-kurucu` | Ürün fotoğrafı + ülkeden (ya da `urun-paketi.json`'dan) Master Tema ile Shopify mağazası kurar | [armanvibecoding/magaza-kurucu](https://github.com/armanvibecoding/magaza-kurucu) |

```
ürün bulundu (SAT) ──urun-paketi.json──▶ Mağaza Kurucu ──magaza-paketi.json──▶ video ekibi
                                              ▲                                    │
                                              └───────── video-paketi.json ────────┘
```

### Claude Code (3 komut)
```
/plugin marketplace add armanvibecoding/viral-urun-ekibi-market
/plugin install viral-urun-ekibi@viral-urun-market
/plugin install magaza-kurucu@viral-urun-market
```
- Ön koşullar ve araç izinleri: aşağıdaki **A** bölümü. Mağaza Kurucu Shopify bağlayıcısını kendisi getirir; ilk kullanımda `/mcp` → shopify → giriş.
- Mağaza Kurucu'yu daha önce kendi pazarından (`magaza-kurucu@magaza-kurucu`) kurduysan yeniden kurma; o kurulum aynı eklentidir ve çalışmaya devam eder.
- Claude görsel üretmez: Mağaza Kurucu'nun görsel adımında görseller ChatGPT'de üretilip sohbete eklenir.

### ChatGPT (2 dosya)
1. **Viral Ürün Ekibi:** `dist/viral-urun-ekibi-chatgpt.zip` → **Plugins** → yükle (ayrıntı: aşağıdaki **C** bölümü).
2. **Mağaza Kurucu:** `magaza-kurucu.zip` (sürüm 0.4.2 ve üstü; [Releases](https://github.com/armanvibecoding/magaza-kurucu/releases), orada yoksa o depoda `python tools/build.py` → `dist/chatgpt/magaza-kurucu.zip`) → **Plugins › Skills › Create › Upload from your computer**. Yalnız Çalışma (Work) modunda çalışır.
3. **Shopify:** `chatgpt.com/plugins/shopify` → **+** → mağazayı seç, izin ver.

Mağaza Kurucu'nun ayrıntılı kurulumu (Claude.ai yolu dahil): o depodaki [KURULUM.md](https://github.com/armanvibecoding/magaza-kurucu/blob/main/KURULUM.md).

### Birlikte kullanım (dosya zinciri)
1. `AliExpress'ten ürün bul` → SAT kararını onayla → ekip `is/NN-urun-adi/urun-paketi.json` yazar.
2. `Bu ürün için mağaza kur` de ve o dosyayı ver (Claude Code: yol; ChatGPT: sohbete ekle) → Mağaza Kurucu fotoğraf + ülke sormadan başlar, sonunda `magaza-paketi.json` verir. Dosyayı ürün klasörüne koy (`is/NN-urun-adi/`).
3. `Bu ürüne video yap` → ekip mağaza paketini okur (`marka-kilidi.md`): aynı renkler, aynı yazı ailesi, yalnız onaylı iddialar, mağaza linki. Teslimde `teslim/video-paketi.json` çıkar.
4. `video-paketi.json` + `pdp-galeri` / `hero` işaretli videoları Mağaza Kurucu'ya ver → ürün sayfası galerisine girer. `reklam` işaretliler mağazaya yüklenmez.

Dosyaların biçimi iki eklentide aynı kaynaktan gelir: `plugins/viral-urun-ekibi/ortak/sozlesme/` (alan tablosu `arayuz-sozlesmesi.md`, şemalar, örnekler, doğrulayıcı). Üretim yapmadan uçtan uca deneme: `python3 docs/sozlesme_test.py`.

Doğrulanmadı: ChatGPT'de plugin ZIP'i yüklemenin kişisel hesaplarda açık olup olmadığı (C bölümündeki not) ve iki eklentinin aynı ChatGPT sohbetinde birlikte tetiklenmesi; önerilen kullanım ekip için bir sohbet, Mağaza Kurucu için ayrı bir Work sohbetidir.

## Hangi yolu seçmeliyim?

| Yol | Ne yapabilir | Kim için |
|---|---|---|
| **A. Claude Code eklentisi** (önerilen) | Dört işin tamamı: Instagram'da gezinme, AliExpress tarama, Flow'da üretim, ffmpeg ile kurgu. Hafıza kendiliğinden tutulur. | Bilgisayarında Claude Code kurabilen herkes (Mac en iyisi, Windows destekli) |
| **B. claude.ai veya ChatGPT Projesi** | Sohbette bilgi bankasıyla ürün yorumu, viral analiz, 30 senaryo, prompt yazımı. Tarayıcı/kurgu yok veya sınırlı. | Hiç kurulum istemeyen herkes → `plugins/viral-urun-ekibi/ekler/proje-paketi/KURULUM.md` |
| **C. ChatGPT plugin** | 14 beceri (7 iş akışı + 6 ekip rolü + bilgi bankası) ChatGPT'de; betikler kod yorumlayıcıda. Tarayıcı, telefon ve Flow adımlarını kullanıcı yapar; hafıza DURUM bloğuyla. | ChatGPT'de Plugins yükleme seçeneği olan herkes → aşağıdaki **C** bölümü (ZIP: `dist/viral-urun-ekibi-chatgpt.zip`) |

## A. Claude Code kurulumu (5 adım)

Ön koşul: Claude Pro, Max veya Ultra planı · Mac için `brew install ffmpeg` ve `python3 -m pip install --user openpyxl pillow imageio-ffmpeg numpy` · Google Chrome · Mac (Windows'ta iPhone modu yok, tarayıcı modu çalışır).

1. **Claude Code'u kur** ve claude.ai hesabınla giriş yap (`claude` → `/login`).
2. **Depo:** herkese açık; ayrı erişim gerekmez. Kendi çatalını (fork) kurmak istersen aşağıdaki yolu kendininkiyle değiştir.
3. **Ekibi kur** (Claude Code içinde):
   ```
   /plugin marketplace add armanvibecoding/viral-urun-ekibi-market
   /plugin install viral-urun-ekibi@viral-urun-market
   /plugin install magaza-kurucu@viral-urun-market
   ```
   Üçüncü satır isteğe bağlıdır (Shopify mağazası da kurulacaksa). Güncellemeleri kendiliğinden almak için: `/plugin` → Marketplaces → Enable auto-update.
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
ZIP'i yeniden üretmek: `sh docs/chatgpt_paketi_yap.sh`. Plugin yüklenemezse B yolu (Proje + talimat) aynı bilgi bankasıyla çalışır.

## Kullanım örnekleri
- "Instagram'dan bugün 20 viral ürün bul."
- "Bulduğumuz ürünlerin ortak noktasına göre AliExpress'ten 5 yeni ürün getir."
- "Şu ürün için ABD pazarına 30 video planı yap: <link>"
- "V01–V05'in kliplerini kurgula ve teslim et."
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
mutlak yol, API anahtarı) içermemeli.

## Lisans
[MIT](LICENSE) — © viral-urun-ekibi contributors.
HyperFrames becerileri (`skills/hyperframes*`, `skills/media-use`) Apache-2.0 lisanslıdır (© HeyGen, Inc.): [THIRD_PARTY_NOTICES.md](plugins/viral-urun-ekibi/THIRD_PARTY_NOTICES.md).

---

## English summary
**Viral Ürün Ekibi** ("Viral Product Team") is a Turkish-language Claude Code plugin: a team of skills and sub-agents that
(1) scouts viral product videos on Instagram Reels/Explore, (2) finds not-yet-viral look-alikes on AliExpress using the
shared "viral DNA" of winners, (3) plans and generates AI product videos with ChatGPT (start frames) and Google Flow
(clips), and (4) edits them with ffmpeg (QC, captions, SFX, loudness). It ships with a knowledge base distilled from
hundreds of analysed products and videos, and keeps per-project memory in a `.ekip/` folder.

Install inside Claude Code:
```
/plugin marketplace add armanvibecoding/viral-urun-ekibi-market
/plugin install viral-urun-ekibi@viral-urun-market
/plugin install magaza-kurucu@viral-urun-market
```
The third line is optional: `magaza-kurucu` (separate repo, listed in this marketplace) builds a Shopify store from the
product the team found; the two plugins exchange `urun-paketi.json` / `magaza-paketi.json` / `video-paketi.json` files.
Then run `/viral-urun-ekibi:ekip-lideri` in an empty folder. User-facing text is Turkish; contributions in English are
welcome too. See [CONTRIBUTING.md](CONTRIBUTING.md). License: MIT.
