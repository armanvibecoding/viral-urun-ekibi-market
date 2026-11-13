# Geliştirici şartnamesi (paketi geliştirenler için — eklentiye yüklenmez)

Bu depo bir Claude Code eklenti pazarıdır. Tek eklenti: `plugins/viral-urun-ekibi/`.
Kullanıcıya görünen her metin **Türkçe**; kod, değişken, dosya adı İngilizce veya ASCII Türkçe olabilir.

## 1. Amaç
Kod bilmeyen bir e-ticaret girişimcisi eklentiyi kurar ve şu 4 işi Claude'a yaptırır:
1. `kesfet-urun-avi` — Instagram'da viral ürün bulma (Mac: iPhone Yansıtma; Windows/her yer: Chrome'da instagram.com).
2. `aliexpress-firsat` — viral ürünlerin ortak DNA'sından AliExpress'te henüz viral olmamış ürün bulma.
3. `ai-video-kreatif` — ChatGPT (görsel) + Google Flow (video) ile 30 senaryo ve örnek video.
4. `video-kurgu` — ffmpeg ile kurgu, yazı, ses, kalite kontrolü, teslim.
`ekip-lideri` hepsini yönetir ve hafızayı tutar.

## 2. Klasör sözleşmesi
```
plugins/viral-urun-ekibi/
  skills/<beceri>/SKILL.md      ← ≤ 120 satır, ≤ 40 talimat. Ayrıntı referans dosyalara.
  skills/<beceri>/referans/*.md ← gerektiğinde okunur (SKILL.md hangi durumda hangisini okuyacağını söyler)
  skills/<beceri>/scripts/      ← çalıştırılabilir yardımcılar
  agents/<ajan>.md              ← frontmatter: name, description, tools (, model)
  ortak/                        ← birden çok becerinin kullandığı bilgi (marka skoru, viral DNA, sözlük)
  ekler/chatgpt/                ← ChatGPT'ye yapıştırılacak sürümler (Claude yüklemez)
  hooks/                        ← SessionStart hafıza yükleyici (hazır, dokunma)
```
- Beceri içinden dosya yolu: `${CLAUDE_SKILL_DIR}/referans/x.md`, eklenti kökü: `${CLAUDE_PLUGIN_ROOT}/ortak/x.md`.
  Bu değişkenler Bash ortamında YOKTUR; yalnız markdown gövdesinde yazılır, Claude yüklerken yerine koyar.
- Kullanıcı verisi eklentiye ASLA yazılmaz. Çalışma klasörü = kullanıcının projesi (`.ekip/` + `is/`).
- Üst düzey `bin/` klasörü YASAK (claude.ai/Cowork kurmaz).

## 3. Hafıza protokolü (bağlam unutmasının çözümü — her beceri uyar)
Kullanıcının proje klasöründe:
```
.ekip/DURUM.md     ← ≤ 40 satır. Aktif iş, aşama, Sıradaki adım, açık sorular, bekleyen onaylar. ÜZERİNE yazılır.
.ekip/KARARLAR.md  ← yalnız ekleme. "- YYYY-AA-GG | konu | karar" (pazar, ürün, bütçe, yasak). Kullanıcı ne dediyse.
.ekip/DERSLER.md   ← yalnız ekleme. "- konu: ders (kanıt dosyası)". Tekrarlanan hata / ölçülmüş bulgu.
is/NN-urun-adi/    ← her ürünün tüm çıktıları; içinde DURUM.md (o ürünün aşama kaydı)
```
- SessionStart kancası (startup/resume/clear/compact) DURUM + son kararları bağlama basar. Yani bağlam sıkışsa da kayıt geri gelir.
- **Kural:** her aşama sonunda ve her kullanıcı kararından hemen sonra ilgili dosya güncellenir. Güncellenmeyen karar yok sayılır.
- Ağır işler (tarama, 30 senaryo, kurgu) alt ajana verilir; ana oturuma yalnız özet + dosya yolu döner (bağlamı korur).
- Uzun çıktı (tablo, senaryo) sohbete değil dosyaya yazılır; sohbete 5–10 satır özet.

## 4. Platform desteği
- **macOS:** tam (iPhone Yansıtma yalnız Mac; Swift araçları kaynak olarak gelir, ilk kurulumda `swiftc` ile derlenir).
- **Windows:** iPhone yerine Chrome'da instagram.com/reels (Claude in Chrome eklentisi). Betikler Python 3 veya POSIX sh (Windows'ta Git Bash). ffmpeg bulma sırası: `shutil.which("ffmpeg")` → `imageio_ffmpeg.get_ffmpeg_exe()` → kurulum talimatı (winget install Gyan.FFmpeg / brew install ffmpeg).
- Mutlak yol, kişisel e-posta, hesap/mağaza adı, oturum klasörü YASAK. Teslimden önce `sh docs/anonim_kontrol.sh` 0 ile çıkmalı (kara liste depo dışında, hazırlayanın bilgisayarında).

## 5. ChatGPT desteği
Her beceri için `ekler/chatgpt/<beceri>.md`: ChatGPT (Çalışma modu / Proje talimatı) için tek parça, kopyala-yapıştır sürüm.
Claude'a özgü araç adları (Agent, Bash, computer-use) yerine ChatGPT karşılığı (kod yorumlayıcı, tarayıcı, dosya yükleme) yazılır.
Bilinen ChatGPT sınırları (ölçüldü):
- Chrome eklentisi modunda dosyaları Google Flow'a YÜKLEYEMİYOR (Flow'un dosya girişi geçici; sürükle-bırak aracı yok).
- Bulut tarayıcısında Google girişi kullanıcıda; her oturumda bir kez.
- Kod ortamında ffmpeg var (7.x), moviepy yok. Görsel üretimi talimata birebir uymaz → ölçümle kontrol gerekir.

## 6. Yazım kuralları (talimat bütçesi)
- Talimat sayısı ≤ 40 / SKILL.md. Niyet + bitiş durumu yaz; adım yalnız kırılgan işlemde (komut, koordinat).
- "Bilmiyorum / doğrulanamadı" her çıktıda geçerli bir sonuçtur; uydurmak yasak.
- Tek terim tek kavram: "kanca" (hook), "sahne", "başlangıç karesi", "klip", "kurgu", "aday", "kanıt".
- Tarih içeren kural yazma; kişiyi "kullanıcı" diye an.
- Para/kredi harcayan her adım (Flow kredisi, sipariş, reklam) kullanıcı onayı ister; onay KARARLAR.md'ye yazılır.
- Instagram'da takip/yorum/DM/satın alma yok; yalnız izle, kaydır, profil/site oku (beğeni kullanıcı izin verirse).
- Marka/IP: başka markanın logosu veya ürün adı üretilen görsel/videoda kullanılmaz.

## 7. Bitti ölçütü (her beceri için)
1. `SKILL.md` frontmatter: `name`, `description` (ne zaman çağrılır — tetik cümleleri Türkçe).
2. Betikler gerçekten koşturuldu (çıkış kodu 0, örnek çıktı) — en az biri örnek veriyle.
3. Kişisel veri grep'i boş.
4. `ekler/chatgpt/<beceri>.md` var.
5. Hafıza protokolü SKILL.md'de bir bölüm olarak yer alıyor (hangi aşamada neyi yazar).
