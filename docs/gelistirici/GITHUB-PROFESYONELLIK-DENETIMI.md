# GitHub profesyonellik denetimi

Tarih: 2026-11-23 · Kapsam: yalnız denetim, depoda başka dosya değişmedi, commit yok.
Ölçüm etiketi: **[koşuldu]** komut çalıştı · **[okundu]** dosya/sayfa açıldı · **[tahmin]** ölçülmedi.
İş miktarı: S = 1 saatten az · M = yarım gün · L = 1 gün+.

---

## Ana sonuç (3 cümle)

Eklentinin içeriği güçlü, ama vitrin (GitHub ilk sayfası) bir **iç çalışma klasörü** gibi duruyor: görsel yok, sürüm yok, topluluk dosyası yarım, `docs/` içinde kurucu iç planları açıkta, ikili ZIP git içinde.
GitHub'ın kendi "topluluk sağlığı" ölçümü **%57** [koşuldu: `gh api .../community/profile`].
En çok fark yaratan 5 düzeltme aşağıda; hepsi koda dokunmaz, toplam yaklaşık yarım gün.

---

## İLK 5 DÜZELTME (en yüksek etki / en az iş)

| # | Düzeltme | Neden önce | İş |
|---|---|---|---|
| 1 | **README'nin ilk ekranını yeniden yaz**: tek cümle + 1 görsel/GIF + rozetler + 3 satırlık kurulum. İngilizce özeti en üste (ya da `README.en.md`). | Ziyaretçi ilk 5 saniyede karar verir. Şimdi ilk ekran 6 satırlık uzun paragraf, görsel yok. | S–M |
| 2 | **Sürüm + Releases**: `v0.2.1` etiketi + GitHub Release; ChatGPT ZIP'i git'ten çıkarıp Release dosyası yap; `CHANGELOG.md` aç. | Şimdi etiket 0, release 0 [koşuldu: `git tag` boş, `latestRelease: null`]. ZIP 21 kez commit'lenmiş, `.git` 31 MB. | S |
| 3 | **Vitrin meta verisi**: ikon (`.claude-plugin/icon.png`), sosyal önizleme görseli, açıklama (Shopify ekle), 8–10 topic, `privacyPolicyUrl`, bozuk "documentation" bağlantısı. | Doğrulayıcı 2 uyarı veriyor; paylaşılan link gri varsayılan kartla çıkıyor; topic yalnız 3. | S |
| 4 | **`docs/` iç belgelerini ayır**: 6 iç plan/analiz dosyasını `docs/gelistirici/` ya da `docs/arsiv/` altına al, `docs/` köküne yalnız kullanıcıya yararlı belge kalsın; betikleri `scripts/`'e taşı. | `docs/` ilk bakışta "birleşme analizi, göç planı, Fable raporu" gösteriyor: kimin için olduğu belirsiz. | S |
| 5 | **Topluluk standardı paketi**: `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue + PR şablonları, `CHANGELOG.md`, 1 GitHub Actions iş akışı (validate + testler). | Hepsi yok [koşuldu: `ls .github` hata]. Rozet "CI passing" da buradan gelir. | M |

Sıralama mantığı: 1–3 görünür etkisi en yüksek; 4 sadece dosya taşıma; 5 güven verir ama biraz yazı ister.

---

## TAM LİSTE

Her bulgu: **sorun** · kanıt · düzeltme · etki · iş.

### 1. İlk izlenim

**1.1 README ilk ekranı ne olduğunu 1 cümlede söylemiyor**
- Kanıt: `README.md:3-6`. İlk blok 4 satırlık yoğun paragraf; "Claude Code eklentisi" 3. kelimeden sonra, "ne işe yarar" 4 cümle sonra. [okundu]
- Düzeltme: tek cümlelik vaat ("Instagram'da viral ürünü bul, Shopify mağazanı kur, AI videosunu üret: Claude Code ekibi") + altında 3 madde. Paragrafı 2. ekrana indir.
- Etki: yüksek · S

**1.2 Görsel, GIF, demo yok**
- Kanıt: README'de tek `![` / `<img` yok [koşuldu: grep]. Depoda zaten hazır görsel (`stil-capasi/*.jpg`) var ama bunlar iç şablon.
- Düzeltme: 1 adet 20–30 sn ekran kaydı GIF'i (`/viral-urun-ekibi:ekip-lideri` → ürün bul → rapor) ya da tek diyagram: dosya zincirini (README'de metin olarak var) görsel akışa çevir. Anonimlik: ekranda isim/hesap/mağaza adı olmasın.
- Etki: yüksek · M

**1.3 Rozet yok**
- Kanıt: README'de shields.io rozeti yok [koşuldu].
- Düzeltme: lisans (MIT), sürüm, CI durumu, "Claude Code plugin", dil (TR). 4 rozet yeter; fazlası gürültü.
- Etki: orta · S

**1.4 Kurulum "3 adım" değil, 5 adım + önkoşul duvarı**
- Kanıt: `README.md:72-94`. Önkoşul satırı tek satırda brew + pip + Chrome + Mac; 4. adım (araç izinleri) 3 alt madde, Windows için ayrı 4 komut. [okundu]
- Düzeltme: üstte "Hızlı başlangıç" 3 satır (`marketplace add`, `install`, `ekip-lideri`); önkoşullar ve Windows ayrıntısı altında katlanır bölüm (`<details>`) ya da `docs/KURULUM.md`.
- Etki: yüksek · S

**1.5 Bölüm başlıkları sıra atlıyor (A, C — B yok)**
- Kanıt: `README.md:72` "A.", `:96` "C.", B bölümü yok; tablo (`:64-70`) B'yi anıyor ama başlık yok. [koşuldu: `grep "^## "`]
- Düzeltme: B bölümünü yaz (Proje paketi, `ekler/proje-paketi/KURULUM.md`'ye 3 satırlık özet) ya da tabloyu 2 yola indir. Başlıkları "Yol A / Yol B / Yol C" yap.
- Etki: orta (özensizlik sinyali) · S

**1.6 GitHub sayfası ayarları**
- Kanıt [koşuldu: `gh repo view`]: açıklama var ama Shopify geçmiyor ("Viral ürün bulma, AliExpress fırsat avı, AI video üretimi ve kurgu için Türkçe Claude ekibi"); topics yalnız `claude-plugin, ecommerce, video`; homepage boş; `usesCustomOpenGraphImage: false`; Releases yok; Discussions kapalı.
- Önerilen topics: `claude-code`, `claude-code-plugin`, `claude-plugin`, `shopify`, `dropshipping`, `ecommerce`, `ai-video`, `viral-products`, `aliexpress`, `turkish`.
- Önerilen açıklama (İngilizce+Türkçe kısa): "Türkçe Claude Code eklentisi: viral ürün bul → Shopify mağazası kur → AI video üret | Turkish Claude Code plugin for product research, Shopify store setup and AI video".
- Sosyal önizleme: 1280×640 PNG, Ayarlar → Social preview. Şimdi GitHub otomatik gri kart üretiyor.
- Etki: orta-yüksek · S

**1.7 Community profile "documentation" bağlantısı ölü**
- Kanıt: API cevabında `documentation: .../tree/master/docs`; varsayılan dal `main` [koşuldu: `git branch -a` → yalnız `main`]. `master` dalı yok → bağlantı 404.
- Düzeltme: Ayarlar'da homepage/doc alanını `main` ya da boş yap (README'deki bağlantılar zaten göreli, sorun yok).
- Etki: düşük ama görünür · S

**1.8 Plugin ikonu ve gizlilik bağlantısı yok**
- Kanıt [koşuldu: `claude plugin validate plugins/viral-urun-ekibi`]: `ICON_MISSING` ve `PRIVACY_URL_MISSING` uyarıları; doğrulama geçiyor ama "dizin kontrolleri" uyarı veriyor. Eklenti uzak MCP'ye bağlanıyor (`.mcp.json` → Shopify), bu yüzden gizlilik uyarısı geçerli.
- Düzeltme: kare PNG (512–2048 px, <2 MB; SVG kabul edilmez) → `plugins/viral-urun-ekibi/.claude-plugin/icon.png`; `plugin.json`'a `privacyPolicyUrl` (kısa `PRIVACY.md`: eklenti kendisi veri toplamaz, `.ekip/` yerelde kalır, Shopify/ChatGPT/Flow kendi politikalarına tabidir).
- Not: doğrulayıcı "ikon yalnız ilk kayıtta listeleme ikonu olur" diyor, yani **ilk yayından önce** ekle.
- Etki: orta · S

**1.9 Lisans görünürlüğü iyi, tek eksik: telif satırı**
- Kanıt: `LICENSE` MIT, GitHub tanıyor (`licenseInfo: mit`). README'de "© viral-urun-ekibi contributors" yazıyor, `LICENSE`'ta da aynı olmalı. Üçüncü taraf: `THIRD_PARTY_NOTICES.md` + `licenses/APACHE-2.0.txt` var, çok iyi. [okundu]
- Düzeltme: gerekmiyor; yalnız `THIRD_PARTY_NOTICES.md` bağlantısını README ilk ekranına (Lisans satırına) taşı.
- Etki: düşük · S

### 2. Depo hijyeni

**2.1 İç çalışma belgeleri `docs/` köküne açık**
- Kanıt [okundu: `wc -l docs/*.md`]: `BIRLESME-ANALIZI.md` (261 satır), `GOC-PLANI.md` (247), `EKIP-GELISIM-PLANI-FABLE.md` (243), `GELISTIRME-ONERILERI-FABLE.md` (183), `BUDAMA-0.3.0.md` (46), `JURI-KALIBRASYON-PILOT.md` (43), `TASIMA-ESLEME.md` (166). Toplam 1.292 satır. Bunlar "iki depoyu birleştirme kararı", "kurucu kararları", model adı (Fable) içeriyor: **geliştirici iç hafızası**, kullanıcı için değil. `GOC-PLANI.md:6` başka bir yerel deponun adını ve "kurucu" ifadesini taşıyor.
- Düzeltme (iki seçenek):
  - A (önerilen): `docs/gelistirici/` altına taşı, `docs/README.md`'de "iç kayıt, kullanıcı okumak zorunda değil" notu.
  - B: git'ten çıkar, yerel kalsın (`.gitignore`). Geçmişte kalır; anonimlik açısından geçmiş zaten tarandı (aşağıda 2.7).
- Not: `SARTNAME.md` ve `anonim_kontrol.sh` **katkıcıya** yarar, kalsın.
- Etki: yüksek (profesyonellik algısı) · S

**2.2 Betikler `docs/` içinde**
- Kanıt: `scripts/anonim_kontrol.sh`, `butce_kontrol.py`, `chatgpt_paketi_yap.sh`, `proje_paketi_yap.sh`, `sozlesme_esitle.py`, `sozlesme_test.py`, `anonim-muaf.sha256` (dokümantasyon klasöründe 7 çalıştırılabilir/veri dosyası). README ve CONTRIBUTING bu yollara atıf yapıyor. [koşuldu: `ls docs`]
- Düzeltme: `scripts/` klasörü aç, taşı; README/CONTRIBUTING/SARTNAME/betik içi yolları güncelle; `grep -rn "docs/.*\.\(py\|sh\)"` ile eski yolu bırakma.
- Etki: orta · M (yol güncellemesi + testlerin hâlâ geçtiğini doğrula)

**2.3 İkili ZIP git geçmişinde**
- Kanıt [koşuldu]: `dist/viral-urun-ekibi-chatgpt.zip` 1,7 MB, en büyük takip edilen dosya; **21 farklı commit'te değişmiş** (`git log -- dist/...`); `.git` 31 MB, çalışma ağacı 49 MB. ZIP içeriği 267 dosya, tamamı zaten kaynaktan üretiliyor (`scripts/chatgpt_paketi_yap.sh`), yani **türev dosya**. README:98 kullanıcıyı "Download raw file" ile indirmeye yönlendiriyor (rahatsız edici adım).
- Düzeltme: ZIP'i `.gitignore`'a al (`dist/` zaten kısmen ignore: `dist/chatgpt/`), her sürümde `gh release create vX.Y.Z dist/*.zip` ile Release'e yükle, README'de "Releases → son sürüm → ZIP" bağlantısı ver. Geçmişi yeniden yazmak (filter-repo) **önerilmez**: 31 MB küçük, force-push bozar, kimse klonlamamış olsa da risk/kazanç kötü.
- Etki: yüksek · S

**2.4 Aynı içerik iki yerde (kaynak + üretilen kopya)**
- Kanıt [koşuldu]: `moduller/magaza-kurucu/` 120 takip edilen dosya; `plugins/viral-urun-ekibi/skills/magaza-kurucu/` 77 üretilen dosya (aynı yazı tipleri/görseller iki kez: `Anton-Regular.ttf`, `stil-capasi/*.jpg`). `ortak/sozlesme/` da `sozlesme_esitle.py` ile kopya. `ekler/proje-paketi/yuklenecek/urun-katalogu.md` ile `ortak/bilgi/urun-katalogu.md` **bayt bayt aynı** (307.545 bayt iki kez) [koşuldu: `cmp` → AYNI]. `.gitattributes:1` bunu bilerek kabul ediyor ("kaynak ve kopya aynı bayt").
- Düzeltme: kopya kasıtlı ve CI'da `build.py --check` ile korunuyor, bu **doğru tasarım**; ama ziyaretçi için "neden iki klasör?" sorusu doğuyor. Çözüm: `moduller/` adını **`src/`** ya da **`kaynak/magaza-kurucu/`** yap ve kökte tek paragraflık `ARCHITECTURE.md`/`docs/MIMARI.md` ("üretilen klasörleri elle düzenleme") yaz. `proje-paketi/yuklenecek/` kopyasını betikle üret, depoda tutma (ya da `.gitignore`).
- Etki: orta · M

**2.5 Kök klasör ve adlandırma karmaşası (Türkçe/İngilizce/ASCII karışık)**
- Kanıt [koşuldu: `ls`]: kökte `.claude/` (iki geliştirici ajanı: `platform-uyum-muhendisi.md`, `tasarim-dili.md`; kullanıcıya dönük değil), `moduller` (Türkçe), `plugins` (İngilizce), `dist`, `docs`; dosya adları: `ESKIDI` (büyük harf, Türkçe), `puan-cetveli-0.2.md` (kebab + sürüm sonekli), `puan_kaydet-0.2.py` (snake + kebab karışık), `anonim_kontrol.sh` (snake), `anonim-muaf.sha256` (kebab), `BIRLESME-ANALIZI.md` (büyük harf). `ortak/` `is/` `ekler/` Türkçe, `agents/` `skills/` `hooks/` İngilizce (Claude Code'un zorunlu adları). 
- Düzeltme: kural koy ve `SARTNAME.md`'ye yaz: "Claude Code'un zorunlu adları İngilizce; bizim klasör/dosya adları ASCII-Türkçe kebab-case; betikler `kebab-case`". En az: `ESKIDI` → `docs/arsiv/`, sürüm soneklerini (`-0.2`) at (sürüm git'te zaten var), `.claude/agents` geliştirici ajanlarını `CONTRIBUTING`'de anlat ya da `docs/gelistirici/`'ye taşı.
- Etki: orta · S–M

**2.6 `docs/ESKIDI/` ölü kod**
- Kanıt: `docs/ESKIDI/puan_kaydet-0.2.py`, `puan-cetveli-0.2.md`, `README.md` (eski sürüm betiği). [okundu]
- Düzeltme: git geçmişi zaten saklıyor; sil ya da `docs/arsiv/`'e al. Silme kırmızı çizgi sayılmaz (kullanıcı verisi değil, kaynak); yine de karar kurucunun.
- Etki: düşük · S

**2.7 `.gitignore` ve anonimlik**
- Kanıt: `.gitignore` 14 satır, çalışma dosyalarını (`.env`, `*.xlsx`, `*.mp4`, `.ekip/`, `is/`) ayıklıyor, iyi. Eksik: `.DS_Store` var ama `*.log`, `node_modules/`, `.idea/`, `.vscode/`, `Thumbs.db` yok. `moduller/magaza-kurucu/.pytest_cache` diskte var ama ignore'da, takip edilmiyor [koşuldu: `git check-ignore`]. Commit yazarı tek ve anonim: 47 commit, tek `noreply` kimliği [koşuldu: `git log --format`]. ev klasörü yolu taraması: **tek eşleşme** `hyperframes-cli/references/preview-render.md:181`, o da "yolları anonimleştir" talimatı içinde örnek (sızıntı değil) [okundu].
- Düzeltme: `.gitignore`'a 5 satır ekle. Anonimlik durumu **iyi**, değişiklik gerekmez; yalnız `anonim_kontrol.sh`'yi CI'a bağla (3.8).
- Etki: düşük · S

**2.8 Commit geçmişi okunabilirliği**
- Kanıt [koşuldu: `git log --format=%s`]: 47 commit, hepsi Türkçe, **biçim tutarlı değil**: `Paket 0.2.0: ...`, `Köprü (Faz 1): ...`, `B-v2 reçeteleri: ...`, `Kurucu geri bildirimi: ...`; birçoğu iç belgeye atıf yapıyor (`(öneri 5, 10, 11, 12)`, `(ekip gelişim planı §2, §6)`, `Faz 1/Faz 2`) → dışarıdan okuyan için anlamsız; "Kurucu geri bildirimi" kişi/rol açığı veriyor. Kullanıcıya dönük sürüm notu yok.
- Düzeltme: geçmişi **yeniden yazma**. İleriye dönük: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`), iç belge atfı yerine ne değiştiği. Kullanıcı görünür özet `CHANGELOG.md`'ye (3.1).
- Etki: orta · S (kural yazmak)

**2.9 Büyük dosyalar**
- Kanıt [koşuldu: `du`]: en büyük 3 takipli dosya: ZIP 1,7 MB; `riser.mp3` 316 KB; `urun-katalogu.md` 304 KB (×2). 100 MB sınırına uzak, sorun yok. `urun-katalogu.md` 300 KB metin: GitHub'da önizlenmiyor (render sınırı), kullanıcı için `.tsv`/`.json` düşünülebilir [tahmin].
- Etki: düşük · —

### 3. Topluluk standartları

[koşuldu: `gh api .../community/profile`, `ls`]

| Öğe | Durum | Düzeltme | İş |
|---|---|---|---|
| LICENSE | var (MIT, tanınıyor) | — | — |
| README | var | 1. bölüm | M |
| CONTRIBUTING | var (6,4 KB, kapsamlı) | kısa "ilk katkı 3 adım" ekle; Türkçe + İngilizce satır | S |
| CODE_OF_CONDUCT | **yok** | Contributor Covenant 2.1 (iletişim adresi: GitHub Security Advisory/Discussions, kişisel e-posta değil) | S |
| SECURITY | **yok** | `SECURITY.md`: "Private vulnerability reporting" aç; kapsam (betikler, kancalar `hooks/durum-yukle.sh`, MCP bağlantısı); yanıt süresi | S |
| Issue şablonları | **yok** | `.github/ISSUE_TEMPLATE/`: `hata.yml` (sürüm, platform, adım), `ozellik.yml`, `config.yml` (soru → Discussions) | S |
| PR şablonu | **yok** | `.github/PULL_REQUEST_TEMPLATE.md`: doğrulama kutucukları (`validate`, testler, anonimlik) | S |
| CHANGELOG | **yok** | Keep a Changelog biçimi; 0.2.0, 0.2.1, 0.3.0 (budama) girdileri `BUDAMA-0.3.0.md`'den damıtılır | S |
| Sürüm etiketi / Release | **yok** (0 etiket, `latestRelease: null`) | `plugin.json` 0.2.1, `docs/BUDAMA-0.3.0.md` "0.3.0" diyor ama `plugin.json` hâlâ 0.2.1 [okundu]: tutarlılığı çöz, sonra `v0.2.1`/`v0.3.0` etiketi + Release | S |
| THIRD_PARTY_NOTICES | **var, çok iyi** (hash'li kaynak, lisans metni) | — | — |
| Dependabot / CODEOWNERS | yok | opsiyonel; python bağımlılığı yok, gerekmez | — |
| Discussions | kapalı | aç, "Fikir / Soru" kategorileri; issue şablonu buraya yönlendirir | S |
| PRIVACY | yok | 1.8 | S |

**3.8 Otomatik doğrulama (GitHub Actions) yok**
- Kanıt: `.github/` klasörü yok [koşuldu]. Elle çalışan 5 kapı var ve hepsi yerelde geçiyor: `claude plugin validate` (geçti [koşuldu]), `python3 scripts/sozlesme_test.py`, `build.py --check`, `pytest moduller/magaza-kurucu/tests`, `scripts/anonim_kontrol.sh`, `scripts/butce_kontrol.py`.
- Düzeltme: `.github/workflows/dogrula.yml`: `push`/`pull_request`'te: Python 3.12 kur → `pip install pytest openpyxl pillow numpy` → `anonim_kontrol.sh` → `butce_kontrol.py` → `sozlesme_test.py` → `build.py --check` → `pytest -q`. `claude plugin validate` için CLI'nin CI'da kurulumu ayrı adım (`npm i -g @anthropic-ai/claude-code`) ve oturum açma gerektirmediği doğrulanmalı **[tahmin: CI'da koşmadım]**; gerekmezse JSON/frontmatter şema kontrolü betikle yapılır.
- Etki: yüksek (rozet + güven + PR'larda otomatik kapı) · M
- Dikkat: iş akışı `moduller/` altındaki bazı testlerin ffmpeg/OCR gerektirip gerektirmediğini bilmeden yazma; ilk koşuda kırmızı çıkarsa hangi testin ortam istediğini işaretle (`pytest.mark.skipif`).

### 4. Dil ve hedef kitle

**4.1 README yalnız Türkçe, İngilizce özet en altta ve sığ**
- Kanıt: `README.md:144-160` "English summary" son bölüm, 17 satır; GitHub arama/öneri motoru ve yabancı ziyaretçi bunu görmüyor. Plugin README'si de 2 satır İngilizce notla bitiyor. [okundu]
- Düzeltme: iki seçenek. **A (önerilen):** `README.md` Türkçe kalsın (asıl kitle TR), en üste "🇬🇧 English: README.en.md" bağlantısı; `README.en.md` 40–60 satır, Hızlı başlangıç + özellikler + sınırlar. **B:** tek README, en üstte iki dilli tek paragraf. i-have-adhd deposu bu kalıbı (dil bayrakları satırı + ayrı dosyalar) kullanıyor [okundu].
- Etki: orta-yüksek · M

**4.2 Terim tutarsızlığı**
- Kanıt [okundu]: aynı kavram için karışık kullanım: "eklenti" / "plugin" / "paket" (README başlık `C. ChatGPT plugin` ama `A. Claude Code kurulumu` "eklenti"); "skill" (`README.md:11`, `CONTRIBUTING`) / "beceri" (`README.md:32` ve plugin README'si: "Sekiz iş akışı", "becerisi"); "ajan" / "alt ajan" / "rol" / "üye"; "kol" / "hat" / "akış"; "pazar" (marketplace) ile "pazar" (market: Türkiye/ABD) aynı kelime, **çakışıyor** (`CONTRIBUTING.md:3` "eklenti pazarı", README "pazarını sorar").
- Düzeltme: `docs/SARTNAME.md` başına 8 satırlık **sözlük** (ortak/sozluk.md zaten var, dışarı açıkla): skill=beceri (ilk geçtiğinde parantez), plugin=eklenti, marketplace=eklenti kataloğu (≠ pazar), agent=ajan, market=hedef ülke. Sonra README'yi arama-değiştir ile tek biçime getir.
- Etki: orta · S–M

**4.3 Hedef kitle cümlesi eksik**
- Kanıt: "Kod bilmeyen bir e-ticaret girişimcisi" ifadesi yalnız `docs/SARTNAME.md:1` içinde (geliştirici belgesi). README kimin için olduğunu söylemiyor. [okundu]
- Düzeltme: README ilk ekrana "Kimin için: Türkiye/ABD pazarında dropshipping/e-ticaret kuran, kod bilmeyen girişimci" ve "Kimin için değil" 1 satır.
- Etki: orta · S

**4.4 Yasal/dürüstlük çerçevesi**
- Kanıt: README "Kırmızı çizgiler" iyi ve dürüst (`:120-124`). Eksik: "Instagram/AliExpress/Meta kullanım şartları, otomasyon riski, sonuç garantisi yok" tek satırlık **sorumluluk reddi**. ["Bilinen sınırlar" var, ama yasal bir uyarı yok.]
- Düzeltme: README altına 3 satır `## Uyarı` (bağımsız proje, markalarla bağlantısı yok, kullanım şartlarına uyum kullanıcıda, gelir vaadi yok).
- Etki: orta (güven, risk) · S

### 5. İyi desenler (yerel örnek eklentilerden) [okundu: `~/.claude/plugins/marketplaces`]

| Desen | Nerede | Bize uyarlama |
|---|---|---|
| Ortalı logo + tek satır slogan + lisans rozeti, hemen ardından **"Install" 1 komut** | `i-have-adhd/README.md:1-30` | 1.1–1.4 |
| Dil bayrakları satırı, çeviriler `.github/readme/` altında | `i-have-adhd/.github/readme/*` | 4.1: `README.en.md` ya da `.github/readme/` |
| `.github/` içinde PR şablonu, workflows, install kılavuzları | `i-have-adhd`, `impeccable`, `openai-codex` | 3 |
| `ISSUE_TEMPLATE/`, `CODEOWNERS`, `dependabot.yml` | `impeccable/.github` | 3 (şablonlar al, CODEOWNERS/dependabot isteğe bağlı) |
| `NOTICE` + `LICENSE` + `package.json` + `tests/` + `scripts/` kökte | `openai-codex` | `scripts/` + `tests/` açık adlı klasörler |
| README başında "Neyi gönderebilirsin/gönderemezsin" + güven uyarısı | `claude-plugins-official/README.md:1-20` | 4.4 uyarı satırı |
| Kök `README`'de yalnız indeks, yapıyı gösteren `Structure` bölümü | `claude-plugins-official/README.md` | 6. klasör ağacı |
| `logo.png` kökte; platform başına manifest (`.codex-plugin`, `.cursor`) | `i-have-adhd` | `icon.png` + isteğe bağlı çok platformlu manifest (şimdi gerekmez) |

Bizdeki iyi taraflar (korunmalı): anonimlik denetimi betiği, kırma testli kapılar, `THIRD_PARTY_NOTICES` ve Apache-2.0 metni, kapsamlı `CONTRIBUTING`, ASCII-Türkçe kuralı, tek kimlikli commit geçmişi, `validate` geçişi.

---

## ÖNERİLEN YENİ KLASÖR AĞACI

```
viral-urun-ekibi-market/
├─ README.md                      ← Türkçe, ilk ekran yeniden yazıldı
├─ README.en.md                   ← İngilizce (kısa)
├─ LICENSE
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ CODE_OF_CONDUCT.md
├─ SECURITY.md
├─ PRIVACY.md
├─ .gitignore
├─ .gitattributes
├─ .github/
│  ├─ workflows/dogrula.yml
│  ├─ ISSUE_TEMPLATE/{hata.yml, ozellik.yml, config.yml}
│  ├─ PULL_REQUEST_TEMPLATE.md
│  └─ social-preview.png          ← 1280×640
├─ .claude-plugin/marketplace.json
├─ plugins/viral-urun-ekibi/      ← kullanıcıya giden paket (değişmez)
│  ├─ .claude-plugin/{plugin.json, icon.png}
│  ├─ agents/  skills/  ortak/  hooks/  ekler/  licenses/
│  └─ README.md  THIRD_PARTY_NOTICES.md
├─ kaynak/magaza-kurucu/          ← eski `moduller/`; üretilen klasörün kaynağı
├─ scripts/                       ← eski `docs/*.sh|py` (anonim_kontrol, butce_kontrol, sozlesme_*, *_paketi_yap)
├─ docs/
│  ├─ README.md                   ← "kullanıcı belgeleri / geliştirici belgeleri" haritası
│  ├─ KURULUM.md                  ← Windows, önkoşullar (README'den taşınan)
│  ├─ MIMARI.md                   ← iki klasör neden var, dosya zinciri diyagramı
│  ├─ SARTNAME.md                 ← geliştirici şartnamesi + sözlük
│  ├─ TASIMA-ESLEME.md
│  └─ gelistirici/                ← iç kayıt: BIRLESME-ANALIZI, GOC-PLANI, EKIP-GELISIM-PLANI-FABLE,
│                                    GELISTIRME-ONERILERI-FABLE, BUDAMA-0.3.0, JURI-KALIBRASYON-PILOT, arsiv/
└─ (dist/ → git'te YOK; ZIP yalnız Releases'ta)
```
Not: `.claude/agents` (2 geliştirici ajanı) ya `docs/gelistirici/` altında anlatılır ya da yerinde kalır; Claude Code bu klasörü depoda çalışan geliştirici için okur, zararsız ama CONTRIBUTING'de bir cümleyle açıklanmalı.
Taşıma riski: `scripts/`, `kaynak/` adı değişince `build.py`, `sozlesme_esitle.py`, testler, README, CONTRIBUTING, SARTNAME ve CI yolları birlikte güncellenmeli; her taşıma sonrası `build.py --check` + `pytest` + `sozlesme_test.py` çıkış 0 olmadan commit yok.

---

## README İSKELETİ (üst 1,5 ekran + sıra)

```markdown
<p align="center"><img src=".github/social-preview.png" width="720" alt="Viral Ürün Ekibi"></p>

<h1 align="center">Viral Ürün Ekibi</h1>
<p align="center"><b>Viral ürünü bul, Shopify mağazanı kur, AI videosunu üret.<br>Tek komutla çalışan Türkçe Claude Code ekibi.</b></p>

<p align="center">
  <img alt="MIT" src="https://img.shields.io/badge/lisans-MIT-blue">
  <img alt="sürüm" src="https://img.shields.io/github/v/release/<kullanici>/viral-urun-ekibi-market">
  <img alt="CI" src="https://img.shields.io/github/actions/workflow/status/<kullanici>/viral-urun-ekibi-market/dogrula.yml">
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-eklenti-orange">
</p>
<p align="center">🇹🇷 Türkçe · <a href="README.en.md">🇬🇧 English</a></p>

![demo](docs/demo.gif)   ← 20–30 sn, isimsiz

## Hızlı başlangıç (3 adım)
1. `/plugin marketplace add <kullanici>/viral-urun-ekibi-market`
2. `/plugin install viral-urun-ekibi@viral-urun-market`
3. Boş klasörde: `/viral-urun-ekibi:ekip-lideri`
Önkoşullar ve Windows: [docs/KURULUM.md](docs/KURULUM.md)

## Ne yapar? (4 madde, ikonlu)
1. Instagram'da viral ürün bulur · 2. AliExpress'te henüz patlamamış benzerini avlar
3. Shopify mağazasını kurar · 4. 30 senaryo + AI video + kurgu

## Kimin için / Kimin için değil
## Hangi yolu seçmeliyim? (A Claude Code · B Proje · C ChatGPT)
## Nasıl çalışır? (dosya zinciri diyagramı)
## Kullanım örnekleri
## Hafıza · Kırmızı çizgiler · Bilinen sınırlar
## Uyarı (bağımsız proje, kullanım şartları, gelir vaadi yok)
## Katkı · Güvenlik · Lisans (+ THIRD_PARTY_NOTICES)
```
İlke: ilk ekranda **ne + kimin için + 3 satır kurulum + görsel**; tablolar, 27 ajan listesi, mağaza kolu ayrıntısı ikinci ekrandan sonra ya da `docs/`'ta.

---

## UYGULAMA SIRASI (kurucu onayından sonra)

1. Önce **güvenli, geri alınır** işler (yalnız ekleme): `CHANGELOG`, `SECURITY`, `CODE_OF_CONDUCT`, `.github/` şablonları, `icon.png`, `privacyPolicyUrl`, README ilk ekran, `README.en.md`, topics/açıklama/sosyal önizleme (GitHub ayarı).
2. Sonra **taşıma** (kırılabilir, her adımda test): `docs/gelistirici/`, `scripts/`, `kaynak/`.
3. En son **yayın**: etiket + Release + ZIP'i git'ten çıkarma, CI. Yayın/push kurucu onaylı.

## Doğrulanmayanlar (dürüst not)
- CI iş akışını çalıştırmadım; `claude plugin validate`'in CI'da oturumsuz koşup koşmadığı **bilinmiyor**.
- README'nin GitHub'da hangi görünümle render edildiğine (rozet/GIF) bakmadım; yalnız dosya ve `gh` verisi okundu.
- Sosyal önizleme ve "kaç kişi gördü" gibi trafik verisi ölçülmedi (depo 0 yıldız, trafik verisi için sahip izni gerekir).
