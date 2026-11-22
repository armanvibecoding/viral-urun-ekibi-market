# Değişiklik günlüğü

Biçim [Keep a Changelog](https://keepachangelog.com/tr/1.1.0/) kuralına, sürümleme [Anlamsal Sürümleme](https://semver.org/lang/tr/) kuralına uyar.
Her sürümün tam geçmişi `git log` içindedir; burada kullanıcıya görünen değişiklikler özetlenir.

## [Yayımlanmamış]

## [0.3.0] - 2026-11-23

### Eklendi
- Tek zorlayıcı kapı (`kapi.py`): ön-üretimden krediye ve tesliminden yayına geçişi kapatır; aşım yalnızca `KARARLAR.md` içinde kullanıcı satırıyla mümkündür.
- Eleştirmen üçe bölündü: mekanik kontroller betiğe, zevk yargısı performansa göre kalibre edilen kör video jürisine (`video-juri`), kök neden ve düzeltme emri direktöre (`video-elestirmen`).
- Rol başına sonuç metriği ve haftalık karne betiği (`karne_uret.py`).
- Kural terfisi iki basamaklı: önce ürün kontratına, aynı kural ikinci üründe de çıkarsa eklentiye; tekrar eden kurallar `ortak/kurallar.md` içinde kimlikli tek kaynağa indi.
- Talimat bütçesi kapısı (`scripts/butce_kontrol.py`): beceri ve ajan dosyası boyutu, tekrar eden kural, tarihli anlatı denetimi (kırma testli).
- Topluluk dosyaları: `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `PRIVACY.md`, issue ve PR şablonları, GitHub Actions CI, eklenti ikonu, `README.en.md`.

### Değişti
- Sağlık ve sonuç dili artık yasak değil: uyarı ve bilgi notu üretir; uydurma veri kapıları korunur.
- Model tablosu: en güçlü model yalnızca kör jüri, kök neden ve strateji rollerinde; hacimli işler `sonnet`, ölçülebilir her şey betik.
- README ilk ekranı yeniden yazıldı (tek cümle, rozetler, akış diyagramı, 3 adımlık kurulum); terimler tek biçime getirildi (eklenti, beceri, ajan).
- Depo düzeni: iç plan ve analiz belgeleri `docs/gelistirici/`, betikler `scripts/` altına taşındı.
- Depo iki parçaya ayrıldı: `claude/` (Claude Code ve claude.ai rehberi) ve `chatgpt/` (ChatGPT rehberi + `proje-paketi/`); kök README yalnız iki kapı gösterir. `ekler/proje-paketi` → `chatgpt/proje-paketi`.
- Yükleme paketleri depoda tutulmaz; her sürümle Releases'a iki ZIP yüklenir: `viral-urun-ekibi-CLAUDE-v<sürüm>.zip` ve `viral-urun-ekibi-CHATGPT-v<sürüm>.zip` (`sh scripts/paketle.sh` ile üretilir).
- Beceri ve ajan dosyaları budandı: `ekip-lideri`, `ai-video-kreatif`, `video-kurgu` ve eleştirmen kısaldı, ayrıntı `referans/` dosyalarına taşındı (kapı hiçbir şeyi kaldırmadı).

### Düzeltildi
- Eklenti sürümü ile belgelerdeki sürüm tutarsızlığı giderildi (0.2.1 ↔ 0.3.0).
- Eklenti doğrulayıcısının `ICON_MISSING` ve `PRIVACY_URL_MISSING` uyarıları kapandı.

## [0.2.1] - 2026-11-19

### Eklendi
- Köprü sözleşmesi uzak kaynağa bağlandı: `ortak/sozlesme/` (kaynak ile bayt bayt aynı kopya, 19 test) ve yazıcı-okuyucu `ortak/paket.py`.

### Değişti
- Yerel köprü kaldırıldı; tek eklenti ve tek sözleşme kaynağı kaldı.

## [0.2.0] - 2026-11-19

### Eklendi
- **Mağaza kolu**: `magaza-kurucu` becerisi (5 aşama: ürün analizi, marka, görseller, metinler, Shopify kurulumu ve site denetimi) ve 20 mağaza ajanı aynı eklentiye katıldı; Shopify uzak bağlantısı (`.mcp.json`).
- Üç köprü dosyası: `urun-paketi.json` (ürün → mağaza), `magaza-paketi.json` (mağaza → video), `video-paketi.json` (video → mağaza).
- Temasız mod: özel tema paketi yoksa ürün, metin, görsel ve sayfalar mağazanın mevcut temasına yazılır.
- Ekip kadrosu 27 üyeye çıktı; her üyenin İngilizce unvanı, adı ve Türkçe rolü `ortak/ekip.md` içinde.
- ChatGPT paketi 16 beceriye çıktı (mağaza kolu dahil).

### Değişti
- "Tek lider": `ekip-lideri` mağaza hattını ve köprüyü de yönetir (ürün bul → doğrula → teklif → mağaza kur → kreatif → yayın).

## [0.1.0] - 2026-11-14

### Eklendi
- İlk yayın: `ekip-lideri`, `kesfet-urun-avi`, `aliexpress-firsat`, `ai-video-kreatif`, `video-kurgu` becerileri ve çekirdek ajanlar; `.ekip/` proje hafızası ve oturum kancası; yüzlerce ürün ve viral video analizinden damıtılmış bilgi bankası.
- Viral kurgu: hızlı kurgu, ses tasarımı (`ses-tasarimcisi`), eleştirmen ajanı, viral referans adımı, kalite kapıları.
- `reklam-kutuphanesi-avi` (Meta Reklam Kütüphanesi'nden kazanan reklam ve ürün taraması, kırma testli toplayıcı) ve `teklif-ve-sayfa`.
- ChatGPT plugin paketi ve claude.ai / ChatGPT Proje paketi.
- HyperFrames hareketli tasarım becerileri (Apache-2.0, değiştirilmeden) ve `video-kurgu` aşama 8b.
- Açık kaynak: MIT lisansı, katkı rehberi, anonimlik denetimi.

[Yayımlanmamış]: https://github.com/armanvibecoding/viral-urun-ekibi-market/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/armanvibecoding/viral-urun-ekibi-market/releases/tag/v0.3.0
