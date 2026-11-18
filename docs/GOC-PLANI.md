# Göç planı: Mağaza Kurucu → Viral Ürün Ekibi (tek plugin, tek lider)

**Sonuç:** 5 faz, 27 adım. Her adımın bir kanıtı var (çıkış kodu, sayı ya da dosya). Uygulayıcı ajan adımları sırayla yapar. B deposu ancak Faz 5'te gizlenir; o adım taşınan dosya sayısı (142/142) ve testler geçtikten sonra, kurucu onayıyla yapılır.
Tarih: 2026-11-18 · Dayanak: `docs/BIRLESME-ANALIZI.md` (seçenek a) + kurucu kararları (aşağıda) · Tahmini iş: 34–42 saat [tahmin].
Kısaltmalar: **A** = `plugins/viral-urun-ekibi/` (bu depo) · **B** = `armanvibecoding/magaza-kurucu` (yerel kopya `~/Documents/magaza-kurucu`, HEAD `d3191ae`).

---

## 0. Kurucu kararları (onaylı, plana işlendi)
| # | Karar | Plandaki karşılığı |
|---|---|---|
| 1 | "Sorunsuz birleştir"; analizdeki seçenek (a) | Faz 1–4 |
| 2 | **Tek lider.** B'nin yönlendiricisi ekip-lideri ile birleşir; ikinci lider kalmaz | §2 ve adım 2.4 |
| 3 | Lider ve kritik roller en güçlü modelde (Fable) | §3: `model: fable` desteklenir, dokümanla doğrulandı |
| 4 | B'nin rolleri A'nın ad kalıbına girer: İngilizce unvan + insan adı + Türkçe rol; çakışan ad olmaz, aynı işi yapan roller birleşir | §1 rol tablosu |
| 5 | B'nin Shopify site analiz sistemi korunur ve A'nın akışıyla beslenir | §4 |
| 6 | Birleşik yapı `armanvibecoding/viral-urun-ekibi-market` deposunda yaşar. B, içerik taşınıp doğrulandıktan **sonra** gizlenir | Faz 5 (son adım) |

### Analizden sapan iki karar (ölçümle)
1. **`git subtree` KULLANILMAZ, B'nin geçmişi taşınmaz.** B'nin 22 commit'inin tamamının yazarı kurucunun GitHub kullanıcı adı; A'nın 33 commit'i "viral-urun-ekibi" adıyla atılmış. B'nin commit mesajlarında 1 kara liste eşleşmesi de var. [koşuldu] Geçmiş taşınırsa A'nın anonimliği geçmişten bozulur. Çözüm: dosyalar tek yeni commit'le kopyalanır, geçmiş gizlenen B deposunda kalır.
2. **B'nin yönlendiricisi ayrı beceri olarak kalmaz.** Yönlendirmeyle ilgili görevleri ekip-lideri'ne geçer. Aşamalar `magaza-kurulumu` adlı lider olmayan bir becerinin içinde durur.

---

## 1. Rol tablosu (A'nın kalıbı: İngilizce unvan + insan adı + Türkçe rol)

Not: A'nın 6 ajan dosyasında insan adları **henüz yazılı değil** (grep boş). Adlar team-lead mesajından alındı; adım 2.5'te dosyalara yazılır.

### 1a. Lider + A'nın 6 rolü (dosya adları DEĞİŞMEZ, geriye dönük uyum için)
| Unvan (ad) | Türkçe rol | Dosya | Model (şimdi → önerilen) | Yer |
|---|---|---|---|---|
| **Team Lead (Kerem)** | Ekip lideri (tek giriş, mağaza hattı dahil) | `skills/ekip-lideri/SKILL.md` | yok → `fable` | beceri |
| Product Research Lead (Kaan) | Fırsat avcısı | `agents/firsat-avcisi.md` | sonnet → sonnet | çalışma |
| Content Strategist (Ece) | İçerik stratejisti | `agents/icerik-stratejisti.md` | yok → opus | çalışma |
| Risk & Validation Analyst (Selin) | Kanıt savcısı | `agents/kanit-savcisi.md` | opus → **fable** | çalışma |
| Creative Strategy Analyst (Arda) | Kreatif analisti | `agents/kreatif-analisti.md` | opus → opus | çalışma |
| Creative Director (QA) (Deniz) | Video eleştirmeni | `agents/video-elestirmen.md` | opus → **fable** | çalışma |
| Sound Designer (Ozan) | Ses tasarımcısı | `agents/ses-tasarimcisi.md` | opus → sonnet (ölçüm ve komut üretimi) | çalışma |

### 1b. B'nin 25 rolü → 19 rol (6 birleşme)
Sütunlar: **Yer = çalışma** (plugin `agents/`, Claude Code'da kullanıcı işinde çağrılır) ya da **geliştirme** (depo kökü `.claude/agents/`, pakete girmez, `research/` okur).

| # | Unvan (ad) | Türkçe rol | Yeni dosya | Kaynak B rolü | Model | Yer |
|---|---|---|---|---|---|---|
| 1 | Brand Strategist (Aylin) | Marka stratejisti | `marka-stratejisti.md` | marka-stratejisti | opus | geliştirme |
| 2 | Design Reference Curator (Defne) | Referans küratörü | `referans-kuratoru.md` | referans-kuratoru | sonnet | geliştirme |
| 3 | Brand Creative Director (Lale) | Marka kreatif direktörü | `marka-kreatif-direktoru.md` | kreatif-direktor (A'daki "Creative Director (QA)" ile çakışmasın diye yeni ad) | **fable** | geliştirme |
| 4 | Niche Style Architect (Bora) | Niş stil mimarı | `nis-stil-mimari.md` | nis-stil-mimari | opus | geliştirme |
| 5 | Design Systems Lead (Nil) | Tasarım sistemi sorumlusu | `tasarim-sistemi.md` | **tasarim-dili + tipografi-sistemcisi** (ikisi de tipografi ölçeği ve renk rolü yazıyordu) | opus | geliştirme |
| 6 | Product Fidelity Analyst (Emre) | Ürün kilidi analisti (görsel + video) | `urun-kilidi-analisti.md` | urun-kilidi-analisti (+ A'nın `kilit.txt` işi) | opus | **çalışma** |
| 7 | Visual Copywriter (Zeynep) | Görsel metin yazarı | `gorsel-metin-yazari.md` | metin-yazari (A'nın içerik stratejistinden ayrışsın diye yeni ad) | opus (fable → opus: yaratıcı ama kapılı iş) | geliştirme |
| 8 | Prompt Engineer (Tolga) | İstem mühendisi | `prompt-muhendisi.md` | prompt-muhendisi | opus | geliştirme |
| 9 | ChatGPT Run Engineer (Burak) | ChatGPT koşu mühendisi | `chatgpt-kosu-muhendisi.md` | **gorsel-uretici + benchmark-kosucusu** (ikisi de gerçek ChatGPT hesabında Playwright ile koşuyordu) | sonnet | geliştirme |
| 10 | Visual QA Engineer (Cem) | Görsel kalite denetçisi | `gorsel-qa.md` | **gorsel-qa + seri-tutarlilik-denetcisi** (ikisi de K2 yazım kapısını ölçüyordu) | sonnet | geliştirme |
| 11 | Blind Taste Juror (İpek) | Kör zevk jürisi (görsel, site **ve video**) | `kor-elestirmen.md` | kor-elestirmen (Fable önerisi: video için de kör jüri; `docs/GELISTIRME-ONERILERI-FABLE.md` §3/1) | **fable** | **çalışma** |
| 12 | Design Director (Ufuk) | Tasarım direktörü (kök neden + tek değişkenli emir) | `tasarim-direktoru.md` | tasarim-direktoru | **fable** | geliştirme |
| 13 | Logo Designer (Mert) | Logo tasarımcısı | `logo-tasarimci.md` | **logo-arastirmaci + logo-tasarimci** (araştırma → istem tek zincir; kullanıcı düzeyinde aynı adlı bir `logo-arastirmaci` ajanı da var) | opus | geliştirme |
| 14 | Page Architect (Pelin) | Sayfa mimarı | `site-bolum-mimari.md` | site-bolum-mimari (+ A `teklif-ve-sayfa` sayfa iskeleti sahibi) | opus | **çalışma** |
| 15 | Brand Voice Editor (Seda) | Marka sesi editörü | `marka-sesi-denetcisi.md` | marka-sesi-denetcisi | sonnet | geliştirme |
| 16 | CRO & UX Auditor (Onur) | Dönüşüm ve kullanılabilirlik denetçisi | `cro-ux-denetcisi.md` | cro-ux-denetcisi | sonnet | **çalışma** |
| 17 | Technical Site Auditor (Efe) | Teknik site denetçisi (hız, erişilebilirlik, arama/feed) | `teknik-site-denetcisi.md` | **hiz-muhendisi + erisilebilirlik-denetcisi + seo-aio-uzmani** (üçü de kurulum sonrası mekanik ölçüm: laboratuvar hız, WCAG, JSON-LD/feed) | sonnet | **çalışma** |
| 18 | Platform Release Engineer (Barış) | Platform ve sürüm mühendisi (iki paket, sözleşme) | `platform-uyum-muhendisi.md` | platform-uyum-muhendisi (+ A'nın `chatgpt_paketi_yap.sh` sorumluluğu) | sonnet | geliştirme |
| 19 | Market Library Keeper (Gizem) | Kütüphane bakımcısı (site analiz sistemi) | `kutuphane-bakimci.md` | kutuphane-bakimci | sonnet | geliştirme |

Sayım: B'den 19 rol + A'dan 6 rol + lider = **26 ad, hepsi tekil**. Kontrol listesi: Kerem, Kaan, Ece, Selin, Arda, Deniz, Ozan, Aylin, Defne, Lale, Bora, Nil, Emre, Zeynep, Tolga, Burak, Cem, İpek, Ufuk, Mert, Pelin, Seda, Onur, Efe, Barış, Gizem. Dosya adlarında da çakışma yok (adım 2.5'te test edilir).

Fable alan rol sayısı: **6** (lider, Selin, Deniz, Lale, İpek, Ufuk). Gerekçe: kurucu "en iyisi" istedi; Fable incelemesi de güçlü modelin yalnız az sayıdaki yüksek kaldıraçlı yargıda değer kattığını söylüyor (`GELISTIRME-ONERILERI-FABLE.md` §1/5). Tarama, ölçüm ve komut üreten roller Fable almaz (maliyet).

### 1c. Neden 5 rol "çalışma" yerine geçiyor
- Bu 5 rolün işi kullanıcının kendi ürününde gerekiyor ve `research/` olmadan da çalışıyor:
  - Emre: ürün kilidi.
  - İpek: kör jüri.
  - Pelin: sayfa planı.
  - Onur ve Efe: kurulum sonrası denetim.
- Kütüphane sayıları zaten `src/ortak/site-denetimi.md` ve `tasarim-dili.md` içine gömülü. Bu ajanların `research/...` atıfları çalışma kopyasında `skills/magaza-kurulumu/<aşama>/references/` yollarına çevrilir.
- Kalan 14 rol `research/` (kütüphane, ham pano, test klasörleri) olmadan çalışamaz. Bu yüzden geliştirme ekibinde kalırlar.
- **ChatGPT paketinde** bu 5 ajan rol becerisine **çevrilmez**. İşleri zaten aşama dosyalarında var (B'nin tasarımı); çevrilirlerse tetik çakışması olur.

---

## 2. Tek lider: ne nereye gider

| B yönlendiricisindeki görev (`src/tek/SKILL.md`) | Birleşik yapıda nereye gider |
|---|---|
| Giriş tetikleri ("mağaza kur", "bu ürünü X'te satacağız", DEVAM KARTI + "devam") | `ekip-lideri` açıklamasına eklenir. Başka hiçbir beceri açıklamasında giriş tetiği kalmaz |
| Aşama sırası tablosu, "önceki onaylanmadan sonrakine geçme" | `ekip-lideri/referans/magaza-hatti.md` (yeni dosya). SKILL.md'de 1 satırlık yönlendirme + dosya yolu |
| KARAKTER (durum satırı `ADIM n/8`, ≤5 madde, `Sonraki:`) | aşama dosyalarında kalır. Lider mağaza hattındayken bu biçimi uygular (A'nın ADHD kurallarıyla uyumlu) |
| DEVAM KARTI ↔ yeni sohbet | Claude Code'da `is/NN-urun/magaza/devam-karti.md` + `.ekip/DURUM.md` satırı. ChatGPT'de DURUM bloğu + kart |
| Dosya ve betik bulma (`find / -name …`) | `magaza-kurulumu/SKILL.md` içinde kalır (aşama yürütücüsünün teknik işi, liderlik değil) |
| Çalışma modu notu (ChatGPT Work, Claude görsel üretmez) | lider kurulum kapılarına (`kurulum-kontrol.md`) |

**Yeni beceri: `skills/magaza-kurulumu/`** (eski yönlendirici + 5 aşama klasörü, `ASAMA.md` frontmatter'sız).
- Frontmatter: `name: magaza-kurulumu` + `user-invocable: false` (Claude Code'da `/` menüsünde görünmez, kullanıcı doğrudan çalıştıramaz, lider çağırır).
- Bu alanın anlamı doğrulandı: "Set to `false` when only Claude should invoke the skill: Claude Code hides it from the `/` menu" (code.claude.com/docs/en/skills).
- Açıklama "Ekip lideri yönlendirir" diye başlar. Kullanıcı tetiği içermez.
- ChatGPT tarafı: `agents/openai.yaml` içinde `allow_implicit_invocation: false` [DOĞRULA]. B'nin kendi dosyası "alan adları resmi dokümanda doğrulanmadı" diyor.
  - Yedek yol: alan çalışmazsa değer `true` kalır, açıklama yalnız lider yönlendirmesini anlatır.
  - Gerçek ChatGPT koşusunda hangisinin işlediği kayda geçer (adım 3.4).

---

## 3. Model alanı: neler destekleniyor (doğrulandı)

| Yer | Desteklenen değerler | Kaynak | Sonuç |
|---|---|---|---|
| Ajan frontmatter (`agents/*.md`) | `sonnet`, `opus`, `haiku`, `fable`, tam model kimliği (ör. `claude-opus-5-5`), `inherit`. Boş bırakılırsa Claude Code sıradaki modeli seçer | code.claude.com/docs/en/sub-agents, "frontmatter reference" ve "Choose a model" [okundu] | `model: fable` **destekleniyor**. B'de 5 ajan bugün zaten `fable` kullanıyor |
| Plugin ajanı kısıtı | "plugin subagents don't support the `hooks`, `mcpServers`, or `permissionMode` frontmatter fields" | aynı sayfa | `model` ve `tools` kısıtlı değil. A'nın ajanlarında `mcpServers`/`hooks` yok, sorun yok |
| Beceri frontmatter (`SKILL.md`) | `model:`, `/model` ile aynı değerler ya da `inherit`. "The override applies for the rest of the current turn … The session model resumes when you send your next prompt." Kurumun `availableModels` izin listesinde yoksa ya da auto mod o modeli desteklemiyorsa kullanılmaz | code.claude.com/docs/en/skills [okundu] | Liderde `model: fable` yalnız lider becerisinin çağrıldığı **turu** Fable yapar. Sonraki mesajda oturum modeline döner |
| ChatGPT | model alanı yok; modeli kullanıcı seçer | — | paketleyici `model:` alanını atar. A'nın `fm_yaz` işlevi zaten yalnız name + description yazıyor [okundu]. B'nin `build.py`'si fazla alanı **hata** sayıyor (`ekstra = set(fm) - {"name","description"}`): plugin kopyasında `model`/`user-invocable`'a izin verilmeli, ChatGPT kopyasında silinmeli |

**Liderin her turda Fable olması için:** `ekip-lideri` frontmatter'ına `model: fable` yazılır. README'ye de "en iyi sonuç için oturumu `/model fable` ile açın" satırı eklenir. Beceri alanı yalnız o turu kapsar, kalıcı değildir.
**Doğrulanmadı:** kullanıcının planında Fable yoksa ne olduğu (sessizce oturum modeli mi, hata mı). Adım 3.3'te Fable olmayan bir hesapla denenir; sonuç README'ye yazılır.

---

## 4. Site analiz sistemi (B'nin "kütüphane v2"si): ne yapıyor, nerede, nasıl korunur

### 4a. Ne yapıyor [okundu: `docs/EKIP-v2.md` §2, `.claude/agents/kutuphane-bakimci.md`, `site-bolum-mimari.md`]
| Halka | Ne | Çıktı |
|---|---|---|
| 1. Liste | Shopify vaka çalışmaları, ecomm.design, Awwwards, Land-book, büyüme listeleri, niş tohumu → 1.293 alan adı; kaynak URL'si olmayan alan adı eklenmez | `kaynak-listeler/`, `HEPSI.tsv` |
| 2. Tarama | `node _arac/tara.mjs` (`MOD=hafif`: ana sayfa 1440 px, ürün sayfası 1440 + 390 px, `products.json`; `MOD=hiz`: mobil laboratuvar hızı). robots.txt'ye uyar, 429 gelince bekler, giriş/form/sepet yok | 465 tarandı, 420 marka ölçüldü (376'sı Shopify, 16 niş) |
| 3. Galeri sınıfı | `galeri_siniflandir.py` + 96 karelik elle etiketleme (sınıflayıcı %53 isabetli; oranlar elle etiketli örneklemden) | `DOGRULAMA.md` |
| 4. Analiz | `birlestir.py` + `analiz.py` | `ANALIZ.md`, `_analiz.json`, `markalar.jsonl/.csv` |
| 5. Kanıt | 55 maddelik kural tablosu (Google, web.dev, Baymard, WCAG, Shopify) ve güç derecesi | `KANIT.md` |
| 6. Eskime | ekip dosyalarındaki sayılar yeni analizle karşılaştırılır; 5 puandan fazla değişen işaretlenir | `ESKIME.md` |
| Tüketiciler | Pelin (bölüm iskeleti: medyan 9 bölüm, hero %79 …), Onur (satın alma kutusu: mobil CTA ilk ekranda %18 …), Efe (hız: hızlı %20 → 1,0 MB), Bora, Lale, Aylin, Nil, Defne. Çalışma zamanında sayılar `src/ortak/site-denetimi.md`, `tasarim-dili.md` ve `01-kurallar.md` içine gömülü | — |

### 4b. Bulunan risk: veri depoda YOK
- `research/` B'de **gitignore'lu** ("research/ public depoya girmez"). Git geçmişinde de hiç yok (`git log --all -- research` boş). Bu Mac'te de yok. [koşuldu]
- İzler başka bir makineyi gösteriyor (Windows ev yolu, IPv4 ağ notu). **B'yi gizlemek kütüphaneyi kaybettirmez, ama kütüphane şu an tek bir makinede duruyor.** Adım 0.3 onu bulup yedeklemeden göç ilerlemez.
- Kütüphane bulunamazsa çalışma zamanı etkilenmez (sayılar gömülü). Etkilenen yalnız bakım ve yenileme: Gizem, Pelin'in testi ve 8 geliştirme rolü.

### 4c. Birleşik yapıda korunma
| Parça | Yeni yer | Herkese açık mı |
|---|---|---|
| Araçlar (`_arac/*.mjs`, `*.py`), `YONTEM.md`, `KANIT.md` (kaynakları kamuya açık kılavuzlar), `ANALIZ.md` (toplu oranlar) | `arastirma/kutuphane/` | evet, anonim kapısından geçerse |
| `markalar.jsonl/.csv` (marka başına ölçüm), `_ham/`, `_pano/`, `_kor/` | `arastirma/kutuphane/_veri/` | **hayır**: `.gitignore` + depo dışı yedek (B'nin bugünkü kuralı: başka markaların ekran ve görselleri depoya girmez) |
| Gömülü sayılar | `skills/magaza-kurulumu/*/references/` | evet (bugünkü gibi) |
| Eskime kapısı | Gizem'in akışı; yolları `arastirma/kutuphane/` olarak güncellenir | — |

### 4d. A'nın akışıyla beslenme (iki yönlü; ortak anahtar = alan adı, küçük harf, `www.` yok)

```
reklam-kutuphanesi-avi ──(ölçeklenen Shopify mağazaları + basari_puani)──▶ kütüphane kaynak listesi "meta-kazanan"
        ▲                                                                    │ tara.mjs → ANALIZ (niş başına n büyür)
        │ (kütüphanedeki marka = GERÇEK-MARKA etiketi; DROP-MARKA ayrımı)      ▼
teklif-ve-sayfa ◀──(ANALIZ §5 ürün sayfası oranları + KANIT kuralları = taban çizgisi)── kütüphane
        │
        └──(teklif.tsv rakip satırları: paket, garanti, kargo, ödeme)──▶ markalar.jsonl'a alan adıyla eklenir (teklif alanları)
```
| Yön | Ne akar | Neyi düzeltir | Uygulama (adım 2.11) |
|---|---|---|---|
| A → kütüphane | `reklam-kutuphanesi-avi`'nin Shopify olduğu doğrulanmış (`shopify_kontrol.py`) ve `basari_puani.py` eşiğini geçen mağazaları; kaynak = Reklam Kütüphanesi URL'si | B'nin iki açığı: (1) başarı "kaynakla tanımlı, satışla değil" (YONTEM); reklam süresi ve ölçeği davranışsal sinyal ekler. (2) n < 15 olan nişlerde oran yazılmıyordu; niş niş tarama bu nişleri doldurur | `magaza_gecis.py` çıktısını `kaynak-listeler/meta-kazanan.tsv` biçiminde yazan dar bir dışa aktarım (yeni betik `kutuphaneye_aktar.py`) + kırma testi |
| A → kütüphane | `teklif-ve-sayfa` `teklif.tsv` rakip satırları | kütüphanede teklif alanı yok (yalnız "paket/adet indirimi %30", "kargo/iade satırı %27") | `analiz.py` alan adıyla birleştirir; `gorulmedi` boş sayılır |
| Kütüphane → A | ANALIZ §5 oranları + KANIT 1.x, 7.x | A'nın teklif deseni n≈10 rakiple çalışıyor; 343 ürün sayfalık taban "bizim desen kütüphaneden ne kadar sapıyor" sorusunu yanıtlar | `teklif-ve-sayfa` Akış adım 2'ye tek satır: desen tablosuna "kütüphane oranı" sütunu (kaynak: gömülü `site-denetimi.md`) |
| Kütüphane → A | Pelin'in ölçülmüş bölüm iskeleti | A'nın `sayfa-iskeleti.md` sırası ölçülmemişti | temasız modda Pelin iskeleti verir; `sayfa-iskeleti.md` başına "sıra: Pelin'in `SAYFA-PLANI.md`'si varsa o" |
| Kütüphane → A | kütüphanedeki alan adları | `marka-skoru.md` GERÇEK-MARKA / DROP-MARKA ayrımı | `reklam-kutuphanesi-avi` alan adı kütüphanede varsa `GERÇEK-MARKA` adayı diye işaretler (karar değil, ipucu) |

---

## 5. Adımlar

**Uygulayıcı için sınırlar:**
- Dosya adıyla stage et; `git add -A` / `git add .` yasak.
- `.env` okunmaz.
- **Push, release, depo görünürlüğü ve B deposuna yazma ancak kurucunun o adımdaki açık onayıyla yapılır** (dışa dönük, geri alınması zor).
- HyperFrames dosyalarına dokunulmaz (Apache-2.0, değiştirilmeden).
- Para harcanmaz.

### Faz 0: Hazırlık ve taban ölçümü
| # | Adım | Kanıt |
|---|---|---|
| 0.1 | A'da dal aç: `birlesme/magaza-kurucu`. Bugün çalışma ağacında yalnız 2 izlenmeyen doküman var (`BIRLESME-ANALIZI.md`, `GELISTIRME-ONERILERI-FABLE.md`); HyperFrames işi commit'lenmiş (`e90acb9`) | `git status --short` yalnız bu 2 dosyayı gösterir · `git branch --show-current` |
| 0.2 | B yereli = origin: `git -C ~/Documents/magaza-kurucu fetch && git status -sb`. HEAD `d3191ae` değilse yeni commit'ler dahil edilir ve sayılar yeniden alınır | "up to date" · `git ls-files \| wc -l` = **142** (bugün) |
| 0.3 | **Kütüphaneyi bul ve yedekle** (`research/`, özellikle `kutuphane-v2/`). Kurucuya tek soru: "Mağaza Kurucu'nun `research/` klasörü hangi bilgisayarda?" Bulununca depo dışına kopyala (ör. `~/Documents/_arsiv/magaza-kurucu-research/`) | `ANALIZ.md`, `KANIT.md`, `YONTEM.md`, `_arac/tara.mjs` var · `markalar.jsonl` satır sayısı = 420 · kopyanın sha256 listesi |
| 0.4 | Taban sayılarını kaydet → `docs/goc/taban.txt`: B `build.py --check` (GEÇTİ, 11 uyarı), B pytest (60 geçti / 20 atlandı), A `claude plugin validate` (geçti), A ChatGPT ZIP'i (163 dosya, 652.769 B), A ve B anonim kapısı (8 / 49 satır) | dosya var, 6 satır |

### Faz 1: Köprü (yalnız A; B'ye dokunmaz)
| # | Adım | Kanıt |
|---|---|---|
| 1.1 | Sözleşmenin tek kaynağı: `A/sozlesme/arayuz-sozlesmesi.md` (B'deki metin birebir) + `ornek/urun-paketi.json`, `magaza-paketi.json`, `video-paketi.json` (B'nin tablolarındaki örnek değerlerle) + `sozlesme_test.py` (zorunlu alanlar, `surum`) | test çıkışı 0 · bir zorunlu alanı silinmiş kopya → çıkış 1 |
| 1.2 | `aliexpress-firsat/scripts/urun_paketi_yaz.py`: SAT kanıt dosyası + `adaylar.md` + `marj.csv` + (varsa) `teklif.tsv` `bizim` satırı → `is/NN/magaza/urun-paketi.json`. Pazar kodu ISO-3166 (`GB`, `US`); niş eşlemesi tablosu (`reklam-kutuphanesi-avi` niş kodu → `nis-…`) | örnek veriyle üretilen dosya `sozlesme_test.py`'den geçer · kırma testi |
| 1.3 | `video-kurgu/scripts/magaza_paketi_oku.py` + `kurgu_kontrol.py`'ye kapı: metin katmanındaki iddia `onayli_metinler.iddialar` içinde değilse hata. Altyazı rengi ve başlık ailesi paketten (yoksa bugünkü davranış) | kırma testi: listede olmayan iddia → 1, olan → 0 · `kendini_test.py` geçer |
| 1.4 | `video-kurgu` teslimde `video-paketi.json` yazar (`kullanim` = `reklam` varsayılan; `pdp-galeri`/`hero` kurucu seçer) | şema testi 0 |
| 1.5 | Commit 1 (yalnız köprü dosyaları, adlarıyla) | `git show --stat` yalnız Faz 1 dosyaları |

### Faz 2: Taşıma (geçmişsiz kopya)
| # | Adım | Kanıt |
|---|---|---|
| 2.1 | `git -C B archive d3191ae \| tar -x -C <geçici>` → aşağıdaki eşleme. **Her B dosyası** `docs/goc/TASINAN.tsv`'ye yazılır (B yolu · sha256 · yeni yol · durum: `kopya` / `donusturuldu` / `birlesti`). Beklenen: 110 `kopya` (skills 77, src 10, tests 11, tools 2, docs 4, config 1, kaynak 1, README, KURULUM, .gitignore, .gitattributes → `moduller/magaza-kurucu/`), 25 `donusturuldu` (`.claude/agents/` → §1b'deki 19 dosya), 7 `birlesti` (`.claude-plugin/`×2, `.codex-plugin/`, `.agents/`, `plugin.json`, `.mcp.json`, `LICENSE` → A manifestleri) | TSV 142 satır · `kopya` satırlarında sha256 kaynakla aynı (anonim temizlikten önce) · B'de olup TSV'de olmayan yol = 0 |
| 2.2 | Anonim temizlik (`moduller/`, yeni ajanlar): tema adı → "tema paketi" (dosya adı `config/tema.json`'dan okunur, metne yazılmaz), kaynak prompt dosya adı → nötr ad (`kaynak/KAYNAK-PROMPT.md`; test yolu da), hedef kullanıcı kelimesi → "kullanıcı", Windows yolu silinir (`OCR_TESSDATA` yoksa açık hata), masaüstü yolu → `TEMA_ZIP` ortam değişkeni, telif satırı → "viral-urun-ekibi contributors". HyperFrames'teki İngilizce "masaüstü" kelimesi yanlış alarmı için kurucu kendi kara listesini daraltır (liste depo dışında, ajan değiştirmez) | `sh docs/anonim_kontrol.sh` → çıkış **0** |
| 2.3 | `moduller/magaza-kurucu/tools/build.py`: yeni hedef `A/skills/magaza-kurulumu/` (yönlendirici gövdesi + 5 aşama, `agents/openai.yaml` ChatGPT kopyasında). Frontmatter izni: plugin kopyasında `name`, `description`, `user-invocable`; ChatGPT kopyasında yalnız `name`, `description`. `arayuz-sozlesmesi.md` artık `A/sozlesme/`'den kopyalanır. Testlerde yol/ad güncellemesi | `build.py --check` → GEÇTİ · pytest ≥ 60 geçti, 0 kaldı · üretilen `SKILL.md` ≤ 5.120 B |
| 2.4 | **Tek lider:** §2 tablosu uygulanır. `ekip-lideri/SKILL.md`: açıklamaya mağaza tetikleri, `model: fable`, ekip tablosu (§1 unvan + ad), yönlendirme satırı "mağaza kur → `magaza-kurulumu` (aşama 1'den ya da `urun-paketi.json` ile)". Ayrıntı yeni `referans/magaza-hatti.md`'ye. Kapılar (`kurulum-kontrol.md`): tema zip'i (yoksa temasız mod), Shopify bağlantısı, hedef tema `UNPUBLISHED` | `wc -c ekip-lideri/SKILL.md` artışı ≤ 1.024 B (Fable incelemesi: talimat bütçesi zaten aşılmış) · **tek giriş testi:** `ekip-lideri` dışındaki hiçbir SKILL.md açıklamasında "oturum başında", "mağaza kur", "devam et" geçmez (yeni `tests/tek_lider_test.py`, çıkış 0) |
| 2.5 | Roller: A'nın 6 ajanına unvan + ad (açıklamanın ilk cümlesi: `Risk & Validation Analyst (Selin) (Kanıt savcısı).`); 5 çalışma rolü `A/agents/`'a (`research/` atıfları aşama references yollarına çevrilmiş); 14 geliştirme rolü depo kökü `.claude/agents/`'a; birleşen rollerin kontrol listeleri tek dosyada (kural kaybı yok: eski dosyaların her "##" başlığı yeni dosyada) | `claude plugin validate` geçer · ad tekilliği testi (26 ad, 25 dosya adı tekil) · birleşme testi: 6 birleşmede kaynak dosyaların başlık listesi ⊂ yeni dosya |
| 2.6 | Model alanları §1 tablosuna göre | `grep -h '^model:' A/agents/*.md .claude/agents/*.md A/skills/*/SKILL.md` değerleri ⊂ {sonnet, opus, haiku, fable} · fable sayısı = 6 |
| 2.7 | `A/.mcp.json`: Shopify `{"type":"http","url":"https://setup.shopify.com/mcp"}` | validate geçer · Claude Code `/mcp` listesinde `shopify` |
| 2.8 | Manifestler: `A/.claude-plugin/plugin.json` 0.2.0 + açıklamaya mağaza kurulumu; marketplace açıklaması; ChatGPT manifestine B'nin `interface` bloğu (displayName, shortDescription ≤ 30 karakter, defaultPrompt: "Ekibi başlat. Pazarım Türkiye.", "Bu ürün için mağaza kur. Ülke: Türkiye") | `test_manifest.py` benzeri sürüm eşitliği testi 0 |
| 2.9 | Lisans: tek `LICENSE` (MIT, contributors); `THIRD_PARTY_NOTICES.md`'ye OFL fontlar (Anton, Barlow; `OFL-*.txt` dosyaları yerinde) | grep: `OFL` notice'ta var · font dosyası sayısı 4 ttf + 2 txt |
| 2.10 | Hafıza: `hafiza-sablonlari.md`'ye `is/NN-urun/magaza/` (devam-karti.md + 3 JSON); `DURUM.md` şablonuna "Mağaza:" satırı; hook'a tek satır (varsa `is/*/magaza/devam-karti.md` yolunu basar) | boş klasörde lider kurulumu → `.ekip/` 4 dosya; örnek `is/01/magaza/devam-karti.md` ile hook çıktısında yol görünür |
| 2.11 | §4d bağlantıları: `kutuphaneye_aktar.py` (kırma testli), `teklif-ve-sayfa` desen tablosuna "kütüphane oranı" sütunu, `sayfa-iskeleti.md` sıra kuralı, `teklif-ve-sayfa` tema modu kuralı (tema varsa sayfa metnini `metinler` aşaması yazar), B'nin yasak kelimeleri `yasak-ifadeler.tsv`'ye, fiyat önceliği (`bizim` satırı varsa o; yoksa B'nin 2'li %10 / 3'lü %18 kuralı) `urun-analiz` adım 3'e | `teklif_kontrol.py tara` B örnek metninde 0 · yasak kelime içeren metinde 1 · `aliexpress-firsat`/`teklif-ve-sayfa` `kirma_testi.py` geçer |
| 2.12 | ChatGPT paketleyici: `magaza-kurulumu` TERİM dönüşümünden geçmeden kopyalanır (B zaten ChatGPT için yazılmış); 5 çalışma ajanı rol becerisine çevrilmez; `model:`/`user-invocable:` atılır. Yan ürün: `dist/magaza-kurucu.zip` (kullanıcıların bugünkü tek dosya yolu, aynı kaynaktan; kendi yönlendiricisiyle **ayrı ürün**dür, birleşik plugin değildir) | beceri sayısı = **15** (14 + `magaza-kurulumu`) · `${CLAUDE_` = 0 · `^model:` = 0 · ZIP ≤ 2 MB · `magaza-kurucu.zip` `build.py --check`'ten geçer |
| 2.13 | Commit 2–n (her alt adım ayrı, dosya adlarıyla) | `git log --oneline birlesme/magaza-kurucu` |

### Faz 3: Doğrulama
| # | Adım | Kanıt |
|---|---|---|
| 3.1 | Bütün kapılar (§6) | hepsi 0 / geçti |
| 3.2 | Claude Code temiz kurulum: yeni klasörde `/plugin marketplace add <yerel A yolu>` → `/plugin install` → `/viral-urun-ekibi:ekip-lideri` | `.ekip/` kuruldu · `/` menüsünde `magaza-kurulumu` YOK · "mağaza kur" isteği liderden `magaza-kurulumu`'na gidiyor (oturum dökümü) |
| 3.3 | Model: lider turunda Fable mı (oturum dökümünde model adı); Fable'sız bir hesapta davranış (sessiz düşüş mü, hata mı) | sonuç README'ye bir satır |
| 3.4 | **Uçtan uca gerçek koşu** (para harcamadan: Flow kredisi istenirse dur): 1 SAT ürünü → `urun-paketi.json` → mağaza (geliştirme mağazası ya da UNPUBLISHED tema) → `magaza-paketi.json` → altyazılı kısa video (mevcut klip) → `video-paketi.json` → galeride video. ChatGPT Work'te ZIP'i **kurucu yükler** (ajan dosya seçiciye tıklayamaz) ve aynı akışı başlatır; `allow_implicit_invocation` sonucu kaydedilir | `is/NN/magaza/` altında 3 JSON + kart · Shopify ürün gid'i · kurucunun gözle onayı · `docs/goc/KOSU.md` |
| 3.5 | Geriye dönük uyum: eski bir `.ekip/` klasörüyle yeni sürüm açılır | hook çıktısı hatasız · DURUM'daki "Sıradaki adım"dan devam |

### Faz 4: Yayın (kurucu onayıyla)
| # | Adım | Kanıt |
|---|---|---|
| 4.1 | Dalı `main`'e birleştir, push (onay: "push et") | `git log origin/main -1` = birleşme commit'i |
| 4.2 | A'da release `v0.2.0`: `viral-urun-ekibi-chatgpt.zip` + `magaza-kurucu.zip` | `gh release view v0.2.0` iki dosya |
| 4.3 | Bağlantılar: A README'ye mağaza bölümü ve ChatGPT tek dosya yolu; `KURULUM.md` içindeki eski indirme adresi (B Releases) → A Releases | `grep -r "magaza-kurucu/releases"` = 0 |

### Faz 5: B deposunu gizle (SON ADIM)
| # | Adım | Kanıt |
|---|---|---|
| 5.1 | Ön koşul denetimi (hepsi şart): (a) `TASINAN.tsv` **142/142** satır, `kopya` satırlarının sha256'sı tutuyor (temizlenenler `donusturuldu` olarak işaretli) · (b) `moduller/magaza-kurucu` pytest ≥ 60 geçti, 0 kaldı · `build.py --check` GEÇTİ · (c) §6 kapıları 0 · (d) 3.4 uçtan uca koşu kaydı var · (e) 0.3 kütüphane yedeği var · (f) 4.2 release'te `magaza-kurucu.zip` var · (g) B'de yerelde olup origin'e gitmemiş commit yok (`git -C B status -sb`) | `docs/goc/ONKOSUL.md` 7 işaretli satır |
| 5.2 | Kurucu onayı: "magaza-kurucu deposunu gizle". Seçim: **private** (önerim: anonimlik B'nin geçmişiyle de korunur) ya da **arşiv** (salt okunur ama herkese açık kalır, kimlik izleri görünür) | onay KARARLAR'da |
| 5.3 | `gh repo edit armanvibecoding/magaza-kurucu --visibility private --accept-visibility-change-consequences` (ya da `gh repo archive`). Sonuçları: B'deki Releases bağlantıları ve `claude plugin marketplace add armanvibecoding/magaza-kurucu` dışarıdan çalışmaz; yıldız ve izleyiciler düşer | `gh repo view armanvibecoding/magaza-kurucu --json visibility` → `PRIVATE` · oturumsuz `curl -s -o /dev/null -w '%{http_code}' https://github.com/armanvibecoding/magaza-kurucu` → `404` |
| 5.4 | Yerel B kopyası silinmez (geçmiş ve `research/` izleri için kalır) | `ls ~/Documents/magaza-kurucu` |

---

## 6. Kapılar (Faz 3'te ve her sonraki PR'da)
1. `sh docs/anonim_kontrol.sh` → 0
2. `claude plugin validate plugins/viral-urun-ekibi` ve `claude plugin validate .` → geçti
3. `python3 moduller/magaza-kurucu/tools/build.py --check` → GEÇTİ · `python3 -m pytest moduller/magaza-kurucu/tests` → ≥ 60 geçti, 0 kaldı
4. A'nın mevcut testleri: `video-kurgu` ve `reklam-kutuphanesi-avi` `kendini_test.py`, `aliexpress-firsat` ve `teklif-ve-sayfa` `kirma_testi.py`, `geri_bildirim_kontrol.py`
5. Yeni: `sozlesme_test.py` · `tek_lider_test.py` · ad tekilliği ve birleşme testi · model değeri testi · ChatGPT paket kapısı (15 beceri, `${CLAUDE_`=0, `model:`=0, ≤ 2 MB)
6. Kırma kuralı: her yeni kapı en az bir kez bilerek kırılıp kırmızıya döndüğü görülür (`.ekip` dersi: kırılmayan kapı yeşil sayılmaz)

## 7. Açık riskler (uygulayıcı karşılaşırsa durur ve bildirir)
| Risk | Belirti | Ne yapılır |
|---|---|---|
| Kütüphane bulunamaz | 0.3'te `research/` hiçbir makinede yok | Göç sürer (çalışma zamanı etkilenmez); 14 geliştirme rolüne "veri yok" notu; Faz 5'e geçmeden kurucuya bildirilir |
| `research/` içinde kimlik izi | 0.3 kopyasında anonim kapısı ≠ 0 | yalnız `_veri/`'ye (gitignore) konur, açık kısma alınmaz |
| ChatGPT 15 beceriyi ya da `allow_implicit_invocation: false`'ı kabul etmez | yükleme hatası ya da mağaza becerisinin kendi kendine tetiklenmesi | yedek: değeri `true` yap, açıklamayı daralt; olmazsa `magaza-kurucu.zip` ayrı yüklenir (kayda geçer) |
| Fable kullanıcının planında yok | 3.3 | README notu; çalışma bozulmuyorsa değer kalır |
| Fable maliyeti | 6 rol × her çağrı | kurucunun kararı uygulandı; Fable incelemesindeki "az sayıda yargı" sınırı aşılmadı (6 rol) |
| B'ye göç sırasında yeni commit gelir | 0.2'den sonra origin ilerler | 2.1 yeniden koşulur, TSV yeniden üretilir |
