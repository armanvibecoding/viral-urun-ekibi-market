# Viral Ürün Ekibi

Instagram'da viral ürünleri bulan, AliExpress'te henüz viral olmamış benzerlerini avlayan, ChatGPT + Google Flow ile
ürün videosu üreten ve videoları kurgulayan Türkçe bir Claude ekibi. İçinde yüzlerce ürün ve viral video analizinden
damıtılmış bir bilgi bankası var.

## Hangi yolu seçmeliyim?

| Yol | Ne yapabilir | Kim için |
|---|---|---|
| **A. Claude Code eklentisi** (önerilen) | Dört işin tamamı: Instagram'da gezinme, AliExpress tarama, Flow'da üretim, ffmpeg ile kurgu. Hafıza kendiliğinden tutulur. | Bilgisayarında Claude Code kurabilen herkes (Mac en iyisi, Windows destekli) |
| **B. claude.ai veya ChatGPT Projesi** | Sohbette bilgi bankasıyla ürün yorumu, viral analiz, 30 senaryo, prompt yazımı. Tarayıcı/kurgu yok veya sınırlı. | Hiç kurulum istemeyen herkes → `plugins/viral-urun-ekibi/ekler/proje-paketi/KURULUM.md` |

## A. Claude Code kurulumu (5 adım)

Ön koşul: Claude Pro, Max veya Ultra planı · Mac için `brew install ffmpeg` ve `python3 -m pip install --user openpyxl pillow imageio-ffmpeg` · Google Chrome · Mac (Windows'ta iPhone modu yok, tarayıcı modu çalışır).

1. **Claude Code'u kur** ve claude.ai hesabınla giriş yap (`claude` → `/login`).
2. **Depoya erişim:** sana paylaşılan GitHub deposuna davet linkinden katıl. Gerekirse `gh auth login`.
3. **Ekibi kur** (Claude Code içinde):
   ```
   /plugin marketplace add armanvibecoding/viral-urun-ekibi-market
   /plugin install viral-urun-ekibi@viral-urun-market
   ```
   Güncellemeleri kendiliğinden almak için: `/plugin` → Marketplaces → Enable auto-update.
4. **Araç izinleri:**
   - Chrome'a "Claude" eklentisini kur, Claude Code'da `/chrome` ile bağla.
   - Mac + iPhone modu için: `/mcp` → computer-use → Enable; Sistem Ayarları'nda Erişilebilirlik ve Ekran Kaydı izni; iPhone Yansıtma'yı bir kez elle aç.
   - Windows: PowerShell'de sırayla `winget install Git.Git`, `winget install Python.Python.3.12`,
     `winget install Gyan.FFmpeg`, sonra `py -m pip install --user openpyxl pillow imageio-ffmpeg`.
     Komutlarda `python3` yerine `py -3` kullanılır (`python3` yazmak Microsoft Store'u açar).
5. **Başlat:** boş bir klasör aç, içinde `claude` çalıştır ve yaz:
   ```
   /viral-urun-ekibi:ekip-lideri
   ```
   Ekip lideri hafıza klasörünü (`.ekip/`) kurar, eksik araçları kontrol eder ve sana pazarını (Türkiye/ABD) sorar.

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
