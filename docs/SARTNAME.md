# Geliştirici şartnamesi (paketi geliştirenler için — eklentiye yüklenmez)

Bu depo bir Claude Code eklenti pazarıdır. Pazardaki tek eklenti: `plugins/viral-urun-ekibi/`. Mağaza kolu (`magaza-kurucu`
becerisi, kaynağı `moduller/magaza-kurucu/`) aynı eklentinin içindedir; kollar dosyayla konuşur (§8).
Kullanıcıya görünen her metin **Türkçe**; kod, değişken, dosya adı İngilizce veya ASCII Türkçe olabilir.

## Sözlük (tek terim, tek anlam)
| Terim | Anlamı | Kullanma |
|---|---|---|
| eklenti | Claude Code plugin'i (`plugins/viral-urun-ekibi/`) | "plugin", "paket" (ChatGPT ZIP'i hariç: "ChatGPT paketi") |
| beceri | skill (`skills/<ad>/SKILL.md`); kod, yol ve dosya adlarında `skill`/`skills` aynen kalır | "skill" (düz yazıda) |
| ajan | alt ajan (`agents/<ad>.md`) | "rol" yalnız ChatGPT'de ajanın beceriye çevrilmiş hâli için |
| eklenti kataloğu | marketplace (`.claude-plugin/marketplace.json`) | "pazar" |
| hedef ülke / pazar | satış yapılan ülke (Türkiye, ABD) | marketplace anlamında "pazar" |
| kol | ürün, mağaza, video: köprü dosyasıyla bağlanan üç iş alanı | "hat" (yalnız `uctan-uca-hat` dosya adında) |

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
  skills/<beceri>/SKILL.md      ← ≤ 120 satır VE ≤ 12 000 bayt, ≤ 40 talimat. Ayrıntı referans dosyalara. (kapı: scripts/butce_kontrol.py)
  skills/<beceri>/referans/*.md ← gerektiğinde okunur (SKILL.md hangi durumda hangisini okuyacağını söyler)
  skills/<beceri>/scripts/      ← çalıştırılabilir yardımcılar
  agents/<ajan>.md              ← frontmatter: name, description, tools, model; ≤ 7 000 bayt; model ortak/ekip.md ile aynı
  ortak/                        ← birden çok becerinin kullandığı bilgi (marka skoru, viral DNA, sözlük)
  ortak/kurallar.md             ← kalıcı kuralların TEK kaynağı (kimlikli: SES-01, ICE-01 …); diğer dosyalar kimliğe atıf yapar
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
- Mutlak yol, kişisel e-posta, hesap/mağaza adı, oturum klasörü YASAK. Teslimden önce `sh scripts/anonim_kontrol.sh` 0 ile çıkmalı (kara liste depo dışında, hazırlayanın bilgisayarında).

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
- Tarih içeren kural yazma; kişiyi "kullanıcı" diye an. Kuralın hikâyesi `ortak/bilgi/dersler.md`'de durur.
- **Tek kaynak:** kalıcı kural bir kez `ortak/kurallar.md`'ye kimlikle yazılır; başka dosyada metni tekrarlanmaz (kapı HATA verir).
- **Kural terfisi iki basamak (URE-02):** tek örnekten eklenti kuralı çıkmaz. Yeni kural önce ürün kontratına; eklentiye aynı
  kusur ikinci kez (başka ürün/video) görülünce, kapsam etiketiyle girer. Sektöre özgü kural `referans/sektor/<sektör>.md`'ye.
- **Hüküm üç elde:** ölçü betikte (`kapi.py`), zevk kör jüride (`video-juri`, performans kalibrasyonlu), kök neden direktörde.
  Ölçülebilir bir kuralı ajan talimatına yazma; betiğe eşik + kırma testi olarak yaz.
- **Sağlık/sonuç dili yasak değil** (IDD-01: bilgi notu); uydurma veri yasak (IDD-02). Yeni hukuki yasak kullanıcıya sorulmadan eklenmez.
- **Model:** en güçlü model yalnız jüri, kök neden, strateji ve aylık budamada; mekanik iş betikte ya da ucuz modelde (`ortak/ekip.md`).
- Para/kredi harcayan her adım (Flow kredisi, sipariş, reklam) kullanıcı onayı ister; onay KARARLAR.md'ye yazılır.
- Instagram'da takip/yorum/DM/satın alma yok; yalnız izle, kaydır, profil/site oku (beğeni kullanıcı izin verirse).
- Marka/IP: başka markanın logosu veya ürün adı üretilen görsel/videoda kullanılmaz.

## 7. Bitti ölçütü (her beceri için)
1. `SKILL.md` frontmatter: `name`, `description` (ne zaman çağrılır — tetik cümleleri Türkçe).
2. Betikler gerçekten koşturuldu (çıkış kodu 0, örnek çıktı) — en az biri örnek veriyle.
3. Kişisel veri grep'i boş.
4. `ekler/chatgpt/<beceri>.md` var.
5. Hafıza protokolü SKILL.md'de bir bölüm olarak yer alıyor (hangi aşamada neyi yazar).

## 8. Kollar arası arayüz sözleşmesi
```
aliexpress-firsat (SAT) ──urun-paketi.json──▶ magaza-kurucu ──magaza-paketi.json──▶ ai-video-kreatif / video-kurgu
                                                   ▲                                         │
                                                   └────────────── video-paketi.json ────────┘
```
- Sözleşmenin tek kaynağı içerideki modüldür (`moduller/magaza-kurucu/src/ortak/sozlesme/` + `src/ortak/arayuz-sozlesmesi.md`).
  Eklentideki kopya `plugins/viral-urun-ekibi/ortak/sozlesme/` elle DÜZENLENMEZ: `python3 scripts/sozlesme_esitle.py` kaynaktaki
  `OZET.json`'u yeniden üretir ve kopyalar, `--kontrol` denetler. Sürüm 2 alanları: `teklif` (urun), `magaza.tema_modu`.
- Betik `ortak/paket.py`: `dogrula`, `urun-yaz` (SAT ürünü; `--teklif-tsv` verilirse sürüm 2, `--nis-kodu` `ortak/nis-esleme.tsv`
  ile çevrilir), `fiyat` (fiyatın tek kaynağı), `magaza-oku` (`marka-kilidi.md` + `--cikti-dizin` ile `video-ayar.json`,
  `onayli-iddialar.txt`), `iddia-kontrol` (kurgu_kontrol.py da kullanır), `video-yaz`, `video-sec`. Yazmadan önce şemadan geçirir;
  hata varsa dosya yazılmaz.
- Test (PR öncesi zorunlu): `python3 scripts/sozlesme_test.py` — kopya denetimi, örnekler, kırma testleri ve üretim yapmadan
  uçtan uca zincir. Çıkış 0 olmalı.

## 9. Commit öncesi kapılar (hepsi çıkış 0)
`sh scripts/anonim_kontrol.sh` · `sh scripts/proje_paketi_yap.sh` · `sh scripts/chatgpt_paketi_yap.sh` · `claude plugin validate plugins/viral-urun-ekibi` ·
`python3 scripts/sozlesme_test.py` · `python3 scripts/butce_kontrol.py` (+ `--kendini-sina`) · `cd moduller/magaza-kurucu && python3 -m pytest -q tests` ·
eklenti içi: `skills/ekip-lideri/scripts/kapi_test.py`, `karne_test.py` · `skills/video-kurgu/scripts/kendini_test.py`, `juri_test.py` ·
`skills/reklam-kutuphanesi-avi/scripts/kendini_test.py`, `toplayici_test.py` · `skills/teklif-ve-sayfa/scripts/kirma_testi.py` ·
`skills/aliexpress-firsat/scripts/kirma_testi.py`. Aylık budama ve çıkarılanlar: `docs/gelistirici/BUDAMA-0.3.0.md`, `docs/gelistirici/ESKIDI/`.
- Alan adı değişmez; yeni alan kaynakta (modül) eklenir, `surum` artar, sonra eşitlenir.
