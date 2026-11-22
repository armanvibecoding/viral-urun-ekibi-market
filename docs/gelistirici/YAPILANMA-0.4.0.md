# Yapılanma 0.4.0 — tasarım (uygulanmadı)

Durum: **yalnız tasarım.** Bu belge yazılırken depoda başka hiçbir dosya değişmedi. Uygulayan: Sonnet. Karar veren: kurucu.
Kaynak kararlar: proje `KARARLAR.md`, 2026-11-23 satırları. Ölçümler bu depodan, 2026-11-23 (commit `25aafea`).

---

## 0. TEK SAYFALIK ÖZET (kurucu için)

**Ne değişiyor, 5 madde**
1. Beceri ve rol adları tek kelimelik İngilizce kod adı oluyor. Eski adlar bir sürüm boyunca çalışmaya devam eder.
2. Yeni beceri: **Bazaar** (Trendyol'da ilgi gören, henüz viral olmamış, ucuz ürün; satış kendi Shopify mağazamızda).
3. Bütün ürün bulma becerileri aynı 3 sayfalı, 10 sütunlu Excel'i üretir.
4. Mağaza kurulumu 3 aşama. Teklif ayrı beceri olmaktan çıkar, 1. aşamaya girer.
5. Mağaza rolleri 20 → 10 (kurucu notunda 17 yazıyordu; depoda sayılan 20). Toplam ajan 27 → 17.

**Beceriler (9)**

| Kod adı | Ne yapar | Eski ad |
|---|---|---|
| **Captain** | Ekibi yönetir, işi dağıtır, hafızayı tutar | ekip-lideri |
| **Radar** | Instagram Keşfet'te viral ürünü bulur | kesfet-urun-avi |
| **Spy** | Meta Reklam Kütüphanesi'nde ölçeklenen reklamı bulur | reklam-kutuphanesi-avi |
| **Hunter** | AliExpress'te henüz viral olmamış ürünü bulur | aliexpress-firsat |
| **Bazaar** | Trendyol'da ilgi gören, viral olmamış ucuz ürünü bulur | yeni |
| **Builder** | Shopify mağazasını 3 aşamada kurar (teklif dahil) | magaza-kurucu + teklif-ve-sayfa |
| **Studio** | Ürüne AI video kreatifi hazırlar | ai-video-kreatif |
| **Cut** | Klipleri kurgular, ses ve yazı ekler, teslim eder | video-kurgu |
| HyperFrames (4 beceri) | Üçüncü taraf, dokunulmaz | aynı |

**Mağaza: 3 aşama**

| Aşama | İçinde ne var | Senden ne istenir |
|---|---|---|
| ① **Plan** | Pazar, ürün araştırması, teklif (fiyat, paket, garanti), marka, bütün site metni, Shopify planı, yasal metinler | 3 onay |
| ② **Görseller** | Fotoğraf planı, logo ikonu, galeri, banner, kabul kontrolü | 2 onay |
| ③ **Site** | Shopify kurulumu, kalite kontrolü, site denetimi | 1 elle iş listesi |

**Mağaza rolleri (10)**

| Kod adı | Türkçe | Model | Eski kaç rol |
|---|---|---|---|
| **Atlas** | Marka ve stil stratejisti | fable | 3 |
| **Muse** | Referans ve logo araştırmacısı | sonnet | 2 |
| **Copy** | Metin yazarı | sonnet | 1 |
| **Forge** | İstem yazarı ve görsel üretim operatörü | sonnet | 2 |
| **Sentinel** | Görsel kapı bekçisi (ürün kilidi, yazım, seri) | sonnet | 3 |
| **Panel** | Kör görsel jürisi | fable | 1 |
| **Director** | Görsel kök neden direktörü | fable | 1 |
| **Architect** | Site ve tipografi mimarı | sonnet | 2 |
| **Probe** | Teknik denetçi (hız, erişilebilirlik, arama) | sonnet | 3 |
| **Shopper** | Müşteri gözü denetçisi (dönüşüm, marka sesi) | sonnet | 2 |

**Ürün ve video rolleri (7, birleştirme yok):** Scout (fırsat avcısı) · Skeptic (kanıt savcısı) · Decoder (kreatif analisti) · Story (içerik stratejisti) · Jury (kör video jürisi) · Fixer (video kök neden direktörü) · Mixer (ses tasarımcısı).

**Senden beklenen tek karar:** bu ad listesini onayla ya da değiştirmek istediğin adı söyle. Onaydan sonra uygulama §7'deki 40 adımla yürür.

---

## 1. Ad sistemi

### 1.1 Kurallar (pazarlıksız)
1. Kimlik = tek İngilizce kelime, küçük harf, `[a-z]+`. Kod adı = aynı kelimenin ilk harfi büyük hâli (`radar` → Radar).
2. Beceri ve ajan kimlikleri **tek havuzda benzersizdir** (ChatGPT paketinde ajanlar da beceri olur; çakışma olamaz).
3. Kullanıcıya üye şöyle anılır: `Kod adı (Türkçe rol)`. Örnek: "Jury (kör video jürisi) videoyu puanladı". İnsan adları (Kerem, Kaan, Elif …) ve İngilizce unvanlar (Product Research Lead …) **kaldırılır**.
4. Her beceri ve ajanın `description` alanı şu kalıpla başlar: `<Kod adı> (<Türkçe rol>). <tek satır İngilizce görev>.` Ardından eski açıklamadaki Türkçe tetik cümleleri **aynen** kalır.
5. Tek kaynak: `plugins/viral-urun-ekibi/ortak/ad-haritasi.tsv` (§1.4). Belgeler ve testler adı buradan okur.
6. **Değişmeyenler:** eklenti adı `viral-urun-ekibi` · pazar yeri adı `viral-urun-market` · `moduller/magaza-kurucu/` klasör yolu · beceri içi klasör adları (`referans/`, `scripts/`, `sablon/`, `references/`) · betik dosya adları · kullanıcı proje yolları (`.ekip/`, `is/kesfet/`, `is/firsat/`, `is/meta/`, `is/NN-urun/`) · veri değerleri (ör. `analiz_db_aktar.py` içindeki `"kaynak": "reklam-kutuphanesi-avi"`) · HyperFrames becerileri (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`) · ChatGPT paketindeki `ekip-bilgi` · mağaza bölüm klasörleri (`urun-analiz`, `marka`, `gorseller`, `metinler`, `shopify-kurulum`).
7. Karne betiğindeki Türkçe rol etiketleri ("Fırsat avcısı" …) değişmez; kod adı yalnız kimlik ve gösterimdir.

### 1.2 Beceriler

| Eski kimlik | Yeni kimlik | Kod adı | İngilizce görev (tek satır) | Türkçe açıklama |
|---|---|---|---|---|
| `ekip-lideri` | `captain` | Captain | Runs the team: routes work, guards the gates, keeps the memory. | Ekip lideri |
| `kesfet-urun-avi` | `radar` | Radar | Scans Instagram Explore for products that are already going viral. | Instagram viral ürün taraması |
| `reklam-kutuphanesi-avi` | `spy` | Spy | Scans the Meta Ad Library for ads and stores that are scaling. | Reklam kütüphanesi taraması |
| `aliexpress-firsat` | `hunter` | Hunter | Finds AliExpress products that are not viral yet and proves the case. | AliExpress fırsat avı |
| (yok) | `bazaar` | Bazaar | Finds in-demand, not-yet-viral, cheap Trendyol products to sell in our own Shopify store. | Trendyol fırsat avı |
| `magaza-kurucu` | `builder` | Builder | Builds the Shopify store in three stages: plan, visuals, site. | Mağaza kurucu |
| `teklif-ve-sayfa` | (beceri kalkar) → `builder` Aşama 1, `teklif` bölümü | — | — | Teklif Builder'ın içinde |
| `ai-video-kreatif` | `studio` | Studio | Prepares AI video creatives: scripts, start frames, clips. | AI video kreatifi |
| `video-kurgu` | `cut` | Cut | Edits clips into the final video: text, sound, delivery. | Video kurgu |

KARARLAR.md'de geçen "Trendyol Hunter" = **Bazaar**. Gerekçe: iki fırsat becerisi tek kelimeyle ayırt edilsin (Hunter = AliExpress, Bazaar = Trendyol).

### 1.3 Ajanlar (17)

| Eski kimlik | Yeni kimlik | Kod adı | İngilizce görev | Türkçe rol | Model |
|---|---|---|---|---|---|
| `firsat-avcisi` | `scout` | Scout | Finds not-yet-viral product candidates on marketplaces. | Fırsat avcısı | sonnet |
| `kanit-savcisi` | `skeptic` | Skeptic | Tries to disprove each shortlisted product before we sell it. | Kanıt savcısı | opus |
| `kreatif-analisti` | `decoder` | Decoder | Extracts repeating hook and format patterns from viral videos. | Kreatif analisti | sonnet |
| `icerik-stratejisti` | `story` | Story | Writes the 30 video scripts for a product. | İçerik stratejisti | sonnet |
| `video-juri` | `jury` | Jury | Scores unnamed video boards blind against real viral references. | Kör video jürisi | fable |
| `video-elestirmen` | `fixer` | Fixer | Names the root cause of a failed video and writes the fix order. | Video kök neden direktörü | fable |
| `ses-tasarimcisi` | `mixer` | Mixer | Plans and measures sound, effects and music for short video. | Ses tasarımcısı | sonnet |
| `marka-stratejisti` + `kimlik-direktoru` + `nis-stil-mimari` | `atlas` | Atlas | Sets brand positioning, identity directions and the niche style card. | Marka ve stil stratejisti | fable |
| `referans-kuratoru` + `logo-tasarimci` | `muse` | Muse | Collects measured design references and logo directions. | Referans ve logo araştırmacısı | sonnet |
| `metin-yazari` | `copy` | Copy | Writes the in-image copy from verified facts only. | Metin yazarı | sonnet |
| `prompt-muhendisi` + `gorsel-uretici` | `forge` | Forge | Writes image prompts and runs the approved production list. | İstem yazarı ve üretim operatörü | sonnet |
| `urun-kilidi-analisti` + `gorsel-qa` + `seri-tutarlilik-denetcisi` | `sentinel` | Sentinel | Guards image gates K1–K4: product fidelity, spelling, set consistency. | Görsel kapı bekçisi | sonnet |
| `kor-elestirmen` | `panel` | Panel | Scores unnamed image boards blind against niche references. | Kör görsel jürisi | fable |
| `tasarim-direktoru` | `director` | Director | Names the root cause of a failed image and writes one-variable fix orders. | Görsel kök neden direktörü | fable |
| `site-bolum-mimari` + `tipografi-sistemcisi` | `architect` | Architect | Plans store sections and maps image typography to theme settings. | Site ve tipografi mimarı | sonnet |
| `hiz-muhendisi` + `erisilebilirlik-denetcisi` + `seo-aio-uzmani` | `probe` | Probe | Measures speed, accessibility and search/feed readiness. | Teknik denetçi | sonnet |
| `cro-ux-denetcisi` + `marka-sesi-denetcisi` | `shopper` | Shopper | Audits the store as a buyer: conversion, usability, brand voice. | Müşteri gözü denetçisi | sonnet |

**Ürün ve video tarafında birleştirme önerisi: yok.** Gerekçe:
- Jury ile Panel birleştirilmez: `referans/hukum-hatti.md` "jüri talimatı kalibrasyonsuz değiştirilmez" diyor; Jury'de bilerek `Bash` yok, Panel'de var.
- Fixer ile Director birleştirilmez: girdileri (video kareleri ↔ görsel seti) ve kök neden sınıfları farklı.
- 0.5.0 adayı: Jury + Panel tek jüri. Ön koşul: video jüri kalibrasyonu UYUMLU çıkmış olmalı (ρ ≥ 0,5, n ≥ 8).

### 1.4 Tek kaynak dosyası: `ortak/ad-haritasi.tsv`
Sütunlar (sekme ayraçlı, başlık satırı var): `tur` (`beceri` | `ajan`) · `eski` · `yeni` · `kod_adi` · `gorev_en` · `rol_tr` · `model` · `mod` (yalnız birleşen ajanlarda: eski ajanın yeni roldeki mod adı).
- Her eski kimlik bir satırdır (birleşen 3 eski ajan = 3 satır, hepsinin `yeni` değeri aynı).
- `bazaar` satırında `eski` = `-`.
- `teklif-ve-sayfa` satırında `yeni` = `builder`, `mod` = `teklif`.
- Mod adları: atlas → `strateji`, `kimlik`, `stil` · muse → `referans`, `logo` · forge → `istem`, `uretim` · sentinel → `kilit`, `yazim`, `seri` · architect → `bolum`, `tipografi` · probe → `hiz`, `erisim`, `arama` · shopper → `donusum`, `ses`.

### 1.5 Eski adların çalışması (alias) — kesin yöntem

**Beceriler:** Claude Code'da beceri için yerleşik alias yok. Yöntem: eski klasörde yalnız yönlendiren ince `SKILL.md` kalır.

Dosya: `plugins/viral-urun-ekibi/skills/<eski-ad>/SKILL.md` (klasörde başka dosya olmaz). Örnek (`kesfet-urun-avi`):

```
---
name: kesfet-urun-avi
description: "Eski ad (0.5.0'da kaldırılır). Yeni ad: radar. Yalnız kullanıcı bu eski adı yazdığında çalışır."
disable-model-invocation: true
---
<!-- alias: radar -->
# Ad değişti: kesfet-urun-avi → radar

Bu beceri 0.4.0'da `radar` adına taşındı.
1. Skill aracıyla `viral-urun-ekibi:radar` becerisini çağır ve kullanıcının isteğini aynen ona ilet.
2. Kullanıcıya tek satır yaz: "Bu becerinin yeni adı Radar. Bundan sonra `/viral-urun-ekibi:radar` yazabilirsin."
Başka bir şey yapma.
```

- 8 alias klasörü: `ekip-lideri`→captain · `kesfet-urun-avi`→radar · `reklam-kutuphanesi-avi`→spy · `aliexpress-firsat`→hunter · `magaza-kurucu`→builder · `teklif-ve-sayfa`→builder · `ai-video-kreatif`→studio · `video-kurgu`→cut.
- `teklif-ve-sayfa` alias'ının 1. maddesi farklıdır: "`viral-urun-ekibi:builder` becerisini çağır; kullanıcıya teklifin artık Builder Aşama 1'in 3. adımı olduğunu söyle; yalnız teklif isteniyorsa Builder'a 'yalnız teklif bölümü' de."
- `disable-model-invocation: true` alias'ı modelin beceri listesinden çıkarır (tetik çakışması ve bağlam yükü olmaz); kullanıcı `/viral-urun-ekibi:<eski-ad>` yazınca yine çalışır.
- **Ölçülmeyen nokta:** bu alanın beceri dosyasında çalıştığı bu depoda sınanmadı (alan bu makinede yalnız başka bir eklentinin komut dosyalarında görüldü). Kabul ölçütü: `claude plugin validate plugins/viral-urun-ekibi` çıkış 0. Çıkış ≠ 0 ise o satırı sil; açıklama "Eski ad" ile başladığı için yanlış tetiklenme riski düşüktür.
- İşaret `<!-- alias: <yeni> -->` zorunludur: paketleme ve test betikleri alias'ı bu satırdan tanır.
- Alias'lar ChatGPT paketine **girmez**. 0.5.0'da silinir (CHANGELOG'a "Kaldırılacak" başlığıyla yazılır).

**Ajanlar:** alias yapılmaz (ajanı kullanıcı değil Captain çağırır; yönlendiren ajan boş bir alt ajan turu harcar ve alt ajan başka ajan çağıramaz). Eski ajan dosyaları silinir.

**Eski proje hafızası** (`.ekip/DURUM.md` içinde "Sıradaki adım: aliexpress-firsat …" gibi eski adlar): iki önlem.
1. `hooks/durum-yukle.sh` ikinci `echo` satırından sonra şu satırı basar: `echo "AD DEĞİŞİKLİĞİ (0.4.0): hafızada eski beceri/ajan adı görürsen yenisini kullan. Harita: $K/ortak/ad-haritasi.tsv"`
2. Captain `SKILL.md` §1 madde 2'ye bir cümle: "DURUM.md'de eski ad varsa `ortak/ad-haritasi.tsv`'den yenisini bul; dosyayı bir sonraki yazışta yeni adla yaz."

---

## 2. Yeni beceri listesi ve klasör ağacı

```
plugins/viral-urun-ekibi/
  .claude-plugin/plugin.json            sürüm 0.4.0
  agents/                               17 dosya (§1.3 yeni kimlikler)
  hooks/                                durum-yukle.sh (+1 satır), hooks.json (aynı)
  ortak/
    ad-haritasi.tsv                     YENİ (tek kaynak)
    excel_yaz.py                        YENİ (§6)
    excel_test.py                       YENİ (kırma testi)
    roller/<kod>/<mod>.md               YENİ (birleşen 7 rolün mod dosyaları, §4.3)
    ekip.md                             yeniden yazılır (§4.4)
    magaza-ekibi.md, kurallar.md, sozluk.md, paket.py, sozlesme/, bilgi/ …   yalnız ad atıfları
  ekler/chatgpt/
    radar.md  hunter.md  studio.md  cut.md   (eski: kesfet-urun-avi.md, aliexpress-firsat.md, ai-video-kreatif.md, video-kurgu.md)
  skills/
    captain/        ← ekip-lideri (git mv)
    radar/          ← kesfet-urun-avi (git mv)
    spy/            ← reklam-kutuphanesi-avi (git mv)
    hunter/         ← aliexpress-firsat (git mv)
    bazaar/         YENİ (§5)
      SKILL.md
      referans/  trendyol-okuma.md · olcutler.md · tedarik-ve-fatura.md · fiyat-seffafligi.md · esikler.tsv · tr-oranlari.tsv
      sablon/    adaylar.tsv
      scripts/   bazaar_kontrol.py · tr_marj.py · excel_hazirla.py · kirma_testi.py
    builder/        ← magaza-kurucu (ÜRETİLEN klasör; elle düzenlenmez, build.py yazar)
      SKILL.md  urun-analiz/  teklif/  marka/  metinler/  gorseller/  shopify-kurulum/
    studio/         ← ai-video-kreatif (git mv)
    cut/            ← video-kurgu (git mv)
    hyperframes/ hyperframes-cli/ hyperframes-registry/ media-use/   dokunulmaz
    ekip-lideri/ kesfet-urun-avi/ reklam-kutuphanesi-avi/ aliexpress-firsat/
    magaza-kurucu/ teklif-ve-sayfa/ ai-video-kreatif/ video-kurgu/     yalnız alias SKILL.md (§1.5)

moduller/magaza-kurucu/                 klasör yolu AYNI; içindeki beceri adı builder
  skills/urun-analiz/ teklif/(YENİ) marka/ metinler/ gorseller/ shopify-kurulum/
  src/tek/SKILL.md                      3 aşamalı sıralayıcı, name: builder
  surum.json                            name: builder, version: 0.6.0
scripts/
  ad_testi.py                           YENİ (ad sistemi kapısı, kırma testli)
```

Sayım: gerçek beceri 9 kendi + 4 üçüncü taraf; alias 8; ajan 17.

---

## 3. Mağaza kurulumu: 3 aşama

### 3.1 Karar: 3 aşama = sıra ve gösterim; bölüm klasörleri kalır
- Kullanıcının gördüğü ve sıralayıcının yönettiği birim **3 aşamadır**.
- Her aşama, modüldeki **bölüm** klasörlerini sırayla çalıştırır. Bölüm klasör adları değişmez (eski DEVAM KARTI'ndaki `Sıradaki: gorseller` satırı çalışmaya devam eder; testler ve `build.py` yolları korunur).
- Yeni bölüm: `teklif` (eski `teklif-ve-sayfa` becerisinin içeriği).
- **Sıra değişir:** `metinler` artık `gorseller`'den önce çalışır.

| Aşama | Ad | Bölümler (sırayla) | Onaylar |
|---|---|---|---|
| ① | Plan | `urun-analiz` → `teklif` → `marka` → `metinler` | araştırma + teklif (tek onay) · marka · plan + yasal metinler |
| ② | Görseller | `gorseller` | fotoğraf planı · G1 |
| ③ | Site | `shopify-kurulum` | 7.2 elle iş listesi (durak) · sonda DEVAM KARTI |

### 3.2 Adım numaraları (8 → 9)

| Yeni | Aşama | İş | Bölüm | Eski gerçek sıra | Durum satırındaki kod adı |
|---|---|---|---|---|---|
| 1/9 | ① | Pazar | urun-analiz | 1/8 | Scout |
| 2/9 | ① | Araştırma | urun-analiz | 2/8 | Scout |
| 3/9 | ① | Teklif (fiyat, paket, garanti, itiraz SSS) | teklif | yeni | Atlas |
| 4/9 | ① | Marka (ad, palet, font, logo brifi) | marka | 3/8 | Atlas |
| 5/9 | ① | Site planı + bütün metinler + yasal metinler | metinler | 6/8 | Copy |
| 6/9 | ② | Fotoğraf planı | gorseller | 4/8 | Atlas |
| 7/9 | ② | Görsel üretimi ve kabul | gorseller | 5/8 | Forge (kabulde Director) |
| 8/9 | ③ | Kurulum | shopify-kurulum | 7/8 | Architect |
| 9/9 | ③ | Kalite kontrolü + site denetimi | shopify-kurulum | 8/8 | Probe |

Yeni durum satırı (her mesajın 2. satırı):
`AŞAMA a/3 · ADIM n/9 · <Kod adı> · senden ~N dk · <şerit>`
Örnek: `AŞAMA 1/3 · ADIM 4/9 · Atlas · senden ~30 sn · ✓1–3 ▶4 ○5–9`

`references/adim-*.md` dosya adları ve içlerindeki kaynak metin başlıkları (`ADIM 3/8 — …`) **değişmez** (kaynak kapsam testi bunları ölçer; "dosya düzeni içindir" kuralı zaten var).

### 3.3 Sıra değişiminin gerektirdiği 4 içerik kuralı
1. **Görsel metinleri Aşama 1'de yazılır ve kilitlenir.** `metinler` bölümü site metniyle birlikte G1–G8 başlıklarını ve B1/B2 banner metnini (etiket, başlık, alt metin, buton, ürün satırı) yazar; DEVAM KARTI'nın "Onaylı metinler" satırına girer. Kural kaynağı aynı: `01-kurallar.md` "Görsel metni".
2. **Fotoğraf planı metin yazmaz.** `gorseller` bölümünün plan tablosundaki "Metinler" sütunu DEVAM KARTI'ndan birebir alınır. Kartta görsel metni yoksa (eski kart) plan eskisi gibi kendisi yazar.
3. **Plan görsel numarasını önceden kullanır.** `metinler` tablolarındaki "Görsel (no)" sütunu sabit adlarla doldurulur (G0–G8, B1, B2, S1–S5; `gorsel-dosya-adlari-t3.md`). Aşama 2'de üretilemeyen görsel DEVAM KARTI "Bekleyen" satırına yazılır; Aşama 3 o alanı boş bırakır (tema gizler).
4. **Ön koşullar karta bakar, sıraya değil.** Her bölüm başlarken kartta ihtiyaç duyduğu alanı arar: `teklif` → araştırma bulguları · `marka` → fiyat · `metinler` → marka adı, ses tonu, 5 HEX · `gorseller` → 5 HEX + başlık yazı tipi tarifi · `shopify-kurulum` → onaylı plan + görsel listesi. Eksikse o alanı üreten bölüme döner.

### 3.4 `teklif` bölümü (eski `teklif-ve-sayfa`)
- **Atlanır:** `urun-paketi.json` içinde `teklif.kaynak` = `teklif.tsv` ise (teklif zaten onaylı). Kartın Teklif satırı pakettekiyle doldurulur.
- **Tam mod** (tarayıcı var, Claude Code): rakip teklifleri topla (≥ 10 satır, aynı pazardan ≥ 5) → desen say → `bizim` satırı → `teklif_kontrol.py sema` çıkış 0 → itiraz SSS → e-posta/upsell taslağı → `teklif_kontrol.py tara` çıkış 0.
- **Hafif mod** (tarayıcı yok ya da ChatGPT): araştırmadaki 3 rakip + sabit kural (2'li %10, 3'lü %18); `bizim` satırı yine yazılır; karta "teklif: hafif mod" notu.
- Çıktı yolları (değişmez): `is/NN-urun/teklif/teklif.tsv` · `teklif-deseni.md` · `itiraz-sss.md` · `eposta-upsell.md`. `sayfa.md` yalnız temasız modda yazılır.
- Fiyatın tek kaynağı kuralı aynı: `teklif.tsv` `bizim` satırı. `ortak/paket.py` arayüzü değişmez.
- Araştırma ve teklif **tek onayda** sunulur: "Araştırma ve teklif onaylı mı? (revize için numara yaz)".

### 3.5 DEVAM KARTI ve köprü sözleşmesi (bozulmaz)
- Kart alanları **silinmez, yeniden adlandırılmaz.** İki ek satır (eklemeli):
  - En üste, `Biçim:` satırından sonra: `Düzen: 3A` (3 aşamalı düzen işareti).
  - `Fiyat + adet indirimi:` satırından sonra: `Teklif: garanti · kargo · ödeme · kaynak (teklif.tsv | hafif mod | sabit kural)`.
- `Sıradaki: <bölüm> · <adım>` biçimi aynı; bölüm adları aynı.
- **Eski kart kuralı** (`00-calisma-tarzi.md` DEVAM KARTI bölümüne eklenir): "Kartta `Düzen: 3A` yoksa eski düzen kartıdır: baştan başlama, karttaki 'Sıradaki' bölümden devam et, eski adım numarasını §3.2 tablosuyla çevir, kurulumdan önce eksik bölümü (çoğunlukla `metinler`) tamamla."
- Şemalar (`urun-paketi`, `magaza-paketi`, `video-paketi`; `surum` "2"), `paket_dogrula.py`, `paket.py` komutları ve çıkış kodları **değişmez.** Yalnız yorum ve metin içindeki beceri adları güncellenir.

---

## 4. Mağaza rolleri: 20 → 10

### 4.1 Rol tablosu

| Kod adı | Kimlik | Model | Aldığı eski roller → mod | Araçlar | Aşama |
|---|---|---|---|---|---|
| Atlas | `atlas` | fable | marka-stratejisti → `strateji` · kimlik-direktoru → `kimlik` · nis-stil-mimari → `stil` | Read, Glob, Grep, Bash, Write, WebFetch, WebSearch | ① ve ② başı |
| Muse | `muse` | sonnet | referans-kuratoru → `referans` · logo-tasarimci → `logo` (araştırma + yönler + logo istemleri, dosya bölünmez) | Read, Glob, Grep, Bash, Write, WebFetch, WebSearch | ① |
| Copy | `copy` | sonnet | metin-yazari (tek mod) | Read, Glob, Grep, Write | ① |
| Forge | `forge` | sonnet | prompt-muhendisi → `istem` · gorsel-uretici → `uretim` | Read, Glob, Grep, Bash, Write, Edit, `mcp__claude-in-chrome__tabs_context_mcp`, `…tabs_create_mcp`, `…navigate`, `…get_page_text`, `…find`, `…read_page`, `…computer`, `…tabs_close_mcp` | ② |
| Sentinel | `sentinel` | sonnet | urun-kilidi-analisti → `kilit` · gorsel-qa → `yazim` · seri-tutarlilik-denetcisi → `seri` | Read, Glob, Grep, Bash, Write | ② |
| Panel | `panel` | fable | kor-elestirmen (tek mod, 3 bağımsız kopya) | Read, Glob, Bash, Write | ② |
| Director | `director` | fable | tasarim-direktoru (tek mod) | Read, Glob, Grep, Bash, Write | ② |
| Architect | `architect` | sonnet | site-bolum-mimari → `bolum` · tipografi-sistemcisi → `tipografi` | Read, Write, Glob, Grep, Bash | ① ve ③ |
| Probe | `probe` | sonnet | hiz-muhendisi → `hiz` · erisilebilirlik-denetcisi → `erisim` · seo-aio-uzmani → `arama` | Bash, Read, Write, Glob, Grep, WebFetch | ① (renk kontrastı) ve ③ |
| Shopper | `shopper` | sonnet | cro-ux-denetcisi → `donusum` · marka-sesi-denetcisi → `ses` | Read, Write, Glob, Grep, Bash | ① sonu ve ③ |

### 4.2 Bağımsızlık kuralları (birleştirmede korunanlar)
1. Panel hiçbir üreticiyle birleşmedi; brief'i yalnız pano klasörü + kopya numarasıdır.
2. Director, Panel'den ayrıdır (eşleşme açıldıktan sonra okur; birleşirse körlük bozulur).
3. Üreten ölçmez: Forge (üretir) ↔ Sentinel (K1–K4 ölçer) ↔ Panel (zevk) üç ayrı roldür.
4. Yazan denetlemez: Copy (yazar) ↔ Shopper mod `ses` (marka sesini denetler) ayrıdır.
5. Forge mod `uretim` istemi **değiştirmez** (eski gorsel-uretici kuralı mod dosyasında aynen kalır).
6. Aynı rol aynı anda farklı modlarla paralel çağrılabilir (site denetimi: Probe ×3 mod + Shopper ×2 mod = 5 paralel çağrı; rapor dosyaları aynı: `HIZ.md`, `ERISIM.md`, `SEO.md`, `CRO.md`, `SES.md`).

### 4.3 Birleşik ajan dosyası kalıbı (7 rol: atlas, muse, forge, sentinel, architect, probe, shopper)
Amaç: içerik yeniden yazılmaz, **taşınır**. Ajan dosyası sınırı 7.000 bayt (bütçe kapısı).

1. Her eski ajan dosyasının gövdesi (frontmatter, `<!-- kol: magaza -->`, `# Başlık`, "Ekipteki adın …" ve "Yollar, çıktı yerleri …" satırları **hariç**) aynen şuraya taşınır: `ortak/roller/<kod>/<mod>.md`. İlk satır: `# <Kod adı> · mod: <mod> (eski: <eski-kimlik>)`.
2. Yeni ajan dosyası `agents/<kod>.md` yalnız şunu içerir:

```
---
name: <kod>
description: <Kod adı> (<Türkçe rol>). <İngilizce görev>. <eski açıklamaların "ne zaman çalışır" cümleleri, mod başına bir cümle>
tools: <§4.1 araç listesi>
model: <§4.1 model>
---
<!-- kol: magaza -->
# <Kod adı>

Kullanıcıya "<Kod adı> (<Türkçe rol>)" diye anılırsın. Brief Captain'den gelir, rapor ona döner.
Yollar, çıktı yerleri ve eksik dosya kuralı: `${CLAUDE_PLUGIN_ROOT}/ortak/magaza-ekibi.md` (işe başlarken bir kez oku).

Brief'te `mod:` satırı vardır. O modun dosyasını BAŞTAN SONA oku, yalnız o modun işini yap.
| Mod | Dosya | Ne zaman |
|---|---|---|
| <mod> | `${CLAUDE_PLUGIN_ROOT}/ortak/roller/<kod>/<mod>.md` | <tek satır> |
Brief'te `mod:` yoksa işi yapma; raporun ilk satırına "mod belirtilmedi" yaz.
```

3. Tek modlu 3 rol (copy, panel, director): `git mv` + yalnız frontmatter `name`, `description` başı, `# Başlık` ve "Ekipteki adın …" satırı değişir. Gövdeye dokunulmaz. Model: copy `opus` → `sonnet`; panel ve director `fable` kalır.
4. Mod dosyalarının içindeki eski ajan adları ad haritasına göre `<kod>` (gerekiyorsa `<kod> (mod: <mod>)`) olur.
5. `ortak/roller/` ChatGPT paketine girmez (mağaza ajanları da girmiyor).

### 4.4 `ortak/ekip.md` yeni içeriği
- Başlık: `# Ekip (tek lider, 17 çalışma zamanı üyesi)`.
- Lider paragrafı: "Lider: **Captain** = `captain` becerisi …"; "üye **kod adı ve Türkçe rolüyle** anılır".
- Model paragrafı: fable yalnız `jury`, `panel` (kör jüri), `fixer`, `director` (kök neden), `atlas` (strateji ve yön).
- Tablo 1 "Ürün ve video" (7 satır) ve Tablo 2 "Mağaza" (10 satır). Sütunlar: `Kod adı | Türkçe rol | Ajan | Model | Ne zaman`. **Ajan sütununda kimlik ters tırnak içinde, model sütunu `| sonnet |` biçiminde yazılır** (bütçe kapısı 6 bu satırı okur).
- "Çağrıda model" notları aynen taşınır (skeptic son 3 adayda fable; story hikâye seçiminde fable; decoder aylık desen yorumunda fable). Yeni not: "Forge mod `istem` aynı görselde iki tur üst üste Panel eşiğinin altında kalırsa o çağrıda model: opus."
- "Rol başına sonuç metriği" tablosu aynen kalır (Türkçe etiketler değişmez).
- "Birleşen roller" tablosu §4.1'deki 7 birleşmeyle değiştirilir.
- Son paragraftaki durum satırı eşlemesi §3.2'deki kod adlarıyla yazılır. Geliştirme ekibi satırı aynı kalır.

---

## 5. Yeni beceri: Bazaar (Trendyol fırsat avı)

### 5.1 Tanım
- **Amaç:** Türkiye'de Trendyol'da ilgi gören, Instagram/TikTok'ta henüz viral olmamış, ucuza alınabilen ürünü bulmak; **kendi markalı Shopify mağazamızda** alışın 2–3 katına satmak.
- **Bitiş durumu:** `is/firsat/trendyol/adaylar.tsv` denetimden geçti · kısa listedeki her ürünün `is/firsat/kanit/` altında kanıt dosyası var · `urunler.xlsx` üretildi (§6) · kullanıcıya ≤ 10 satır özet · `.ekip/DURUM.md` güncel.
- **Frontmatter:** `name: bazaar` · açıklama: `Bazaar (Trendyol fırsat avı). Finds in-demand, not-yet-viral, cheap Trendyol products to sell in our own Shopify store. "Trendyol'dan ürün bul", "Trendyol fırsatı", "Türkiye'de satılacak ürün", "ucuza alıp markalı satalım", "Trendyol'da ilgi gören ürün" isteklerinde çağır.`
- **Örnek alınan:** `skills/hunter/` (hafıza protokolü, brief kuralları, "Erişim gerçekleri", özet biçimi aynı kalıpla yazılır). Elle yapılmış ilk deneme: proje klasöründe `firsat/trendyol/deneme-2026-11-23.tsv` (5 ürün; eşiklerin çıkış noktası).

### 5.2 Akış (9 adım)
1. **Hafıza:** `.ekip/DURUM.md`, `.ekip/KARARLAR.md` oku. Pazar TR sabittir, sorulmaz. `is/firsat/trendyol/` yoksa şablondan kur.
2. **Kota:** `bazaar_kontrol.py kota durum`. Günlük tavan dolduysa (çıkış 4) dur, kullanıcıya söyle.
3. **Tohum:** arama terimleri iki kaynaktan: (a) `ortak/viral-dna.md` mekanizmaları (ürün adı değil mekanizma), (b) analiz veritabanında viral aileler (`v_viral_urun`, hüküm `VIRAL-URUN`) → aynı ailenin **farklı modeli**. Terimler Türkçe, 2–4 kelime. Her terim `aramalar.tsv`'ye yazılır; aynı terim iki kez aranmaz.
4. **Tarama (Scout):** Chrome'da `https://www.trendyol.com/sr?q=<terim>` (sıralama: çok değerlendirilenler). Her arama ve her ürün sayfası açılmadan önce `kota kaydet`. Ürün sayfasından okunur: ad, link, fiyat, değerlendirme sayısı, puan, "diğer satıcılar" sayısı, satıcı adı, görsel (bakıldı mı). Satır `adaylar.tsv`'ye.
5. **Ön eleme (betik):** `bazaar_kontrol.py denetle` şemayı ve eşikleri uygular (§5.4); her satıra `on_karar` yazar.
6. **Viral kontrolü:** (a) `bazaar_kontrol.py viral --db <proje>/veri/analiz.db` → her aday için `yok` / `aile-var` / `ayni-urun-viral` / `dogrulanamadi` (veritabanı yoksa hepsi `dogrulanamadi`, çıkış 0); (b) Instagram ve TikTok'ta Türkçe ürün adıyla arama: aynı ürünün ≥ 500 bin izlenmeli videosu var mı (yalnız izle ve oku); (c) Meta Reklam Kütüphanesi TR: aktif reklam ≤ 3 mü (`hunter/referans/zaten-viral-kontrolu.md` §3 kuralları, günlük sorgu kotası Spy ile ortaktır).
7. **Marj:** kısa listedeki her ürün için `marj.csv` satırı → `tr_marj.py` çıkış 0. Çıkış 0 olmadan marj yazılmaz.
8. **Kanıt (Skeptic):** sıra puanı en yüksek ≤ 5 aday. Kanıt dosyası `is/firsat/kanit/NN-urun-adi.md` (Hunter ile aynı şablon + 3 ek bölüm: Tedarik ve fatura · Fiyat şeffaflığı · Net marj).
9. **Karar ve çıktı:** SAT / İZLE / ELE (`ortak/sozluk.md` anlamıyla). ELE → `elenenler.tsv`. `excel_hazirla.py` → `ortak/excel_yaz.py`. SAT onaylanırsa Captain `paket.py urun-yaz` ile `urun-paketi.json` yazar, iş Builder'a geçer.

### 5.3 Chrome kuralları (yalnız oku)
- Trendyol düz istekte (curl, WebFetch) engel döndürür; yalnız Claude in Chrome ile okunur. Tarayıcı yoksa sonuç `dogrulanamadi`.
- Günlük tavan: **≤ 15 arama + ≤ 40 ürün sayfası.** İstekler arası **≥ 15 sn.** Oturum ≤ 1 saat. Tavanı `bazaar_kontrol.py kota` tutar (`is/firsat/trendyol/kota.tsv`); kayıtsız istek yapılmaz.
- Bu sayılar **başlangıç varsayımıdır** (AliExpress'te ölçülen tempo örnek alındı; Trendyol'da ölçülmedi). `referans/esikler.tsv`'de `durum=varsayim` olarak durur.
- CAPTCHA ya da engel sayfası: çözme, atlatma, gizli pencere yok. Dur, okunanı kaydet, `kota kilit` yaz (o gün Trendyol'a dokunulmaz).
- Yapılmaz: giriş, sepete ekleme, favori, satın alma, satıcıya mesaj, yorum. Satıcıyla iletişim kurucu kararıdır.

### 5.4 Ölçütler (`referans/esikler.tsv`; hepsi tarihli, `durum` sütunlu, betik koddan değil dosyadan okur)

| Ölçüt | SAT adayı | İZLE | ELE | Dayanak |
|---|---|---|---|---|
| Değerlendirme sayısı (talep) | 150–3.000 | 50–149 | < 50 ya da > 3.000 (doygun) | deneme: 243 ve 969 aday, 10.314 doygun |
| Puan | ≥ 4,2 | 4,0–4,1 | < 4,0 | deneme: 4,1–4,5 |
| Aynı ürünü satan satıcı | ≤ 5 | 6–15 | > 15 | varsayım |
| Alış fiyatı | 100–600 TL | 601–900 TL | < 100 TL ya da > 900 TL | deneme: 170–321 TL |
| Hedef satış / alış | ≥ 2,2 kat ve satış ≥ 399 TL | 1,8–2,19 kat | < 1,8 kat | kurucu kararı (2–3 kat) |
| Viral durumu | `yok` ya da `aile-var` (model farklı) | `dogrulanamadi` | `ayni-urun-viral` (≥ 500 bin izlenme) | `ortak/sozluk.md` "Zaten viral" |
| Meta TR aktif reklam | ≤ 3 | 4–10 | > 10 | Hunter kuralı |
| Başabaş ROAS (§5.5) | ≤ 2,0 | 2,01–3,0 | > 3,0 | varsayım |
| Fiyat şeffaflığı puanı (§5.7) | 0–1 | 2 | 3 ve aşma yolu yok | varsayım |
| Veto | — | — | lisanslı/marka görünümlü ürün, bebek güvenliği iddiası, riskli kargo (pil, sıvı, cam) | Hunter kuralı |

- Satırın kararı = en kötü ölçütün kararı. Bir ölçüt okunamadıysa o ölçüt `dogrulanamadi` yazılır ve satır en fazla İZLE olur.
- "varsayım" işaretli eşikler 20 ürün kanıt dosyasına ulaşınca gerçek sonuçla yeniden ayarlanır; betik bunu çıktısının son satırında hatırlatır ("N/20 kanıt: eşikler DENEME").

### 5.5 Net marj (`scripts/tr_marj.py`, yalnız standart kütüphane)
Girdi `marj.csv` sütunları: `urun, satis_fiyati, alis_fiyati, alis_kdv_dahil(E/H), fatura_kurumsal(E/H), kdv_yuzde, tedarik_kargo, musteri_kargo, odeme_yuzde, odeme_sabit, kapida_odeme_orani_yuzde, kapida_ek_ucret, iade_orani_yuzde, iade_birim_maliyet, reklam_payi_yuzde, kaynak_notu`.
Boş hücre → `referans/tr-oranlari.tsv` varsayılanı; o da yoksa HATA (tahmin yok).

```
net_gelir   = satis_fiyati / (1 + kdv)
alis_net    = alis_fiyati / (1 + kdv)   (alis_kdv_dahil=E ve fatura_kurumsal=E ise; değilse alis_fiyati aynen)
odeme       = satis_fiyati * odeme_yuzde + odeme_sabit + kapida_odeme_orani * kapida_ek_ucret
iade        = iade_orani * iade_birim_maliyet
maliyet     = alis_net + tedarik_kargo + musteri_kargo + odeme + iade
katki       = net_gelir - maliyet                    (reklam öncesi)
carpan      = net_gelir / maliyet
basabas_roas= satis_fiyati / katki                   (katki ≤ 0 ise "zarar")
reklam      = satis_fiyati * reklam_payi_yuzde
net_kar     = katki - reklam
```
- Çıktı (TSV): her satır için `katki, carpan, basabas_roas, net_kar, karar_marj` + kullanılan her oranın kaynağı ve tarihi.
- Çıkış: 0 hesap tamam · 1 veri hatası · 2 kullanım hatası (Hunter `marj_hesap.py` ile aynı sözleşme).
- `tr-oranlari.tsv` sütunları: `anahtar, deger, durum(resmi|ikincil|varsayim|dogrulanmadi), tarih, kaynak, not`. İlk satırlar: `kdv_yuzde`, `odeme_yuzde`, `odeme_sabit`, `musteri_kargo`, `kapida_odeme_orani_yuzde`, `kapida_ek_ucret`, `iade_orani_yuzde`, `iade_birim_maliyet`, `reklam_payi_yuzde`. **Değerleri Sonnet uydurmaz:** her satır `durum=dogrulanmadi` ve boş `deger` ile açılır; kurucu ya da araştırma turu doldurur. Değer boşken betik HATA verir (bilerek).
- `kirma_testi.py`: en az 10 test (boş oran → çıkış 1 · katkı ≤ 0 → "zarar" · fatura yok → KDV düşülmez · eşik sınır değerleri · kota tavanı → çıkış 4 · bozuk TSV → çıkış 1 · tekrar eden link → "DAHA ONCE GORULDU"). Her kapı önce bozuk girdiyle ≠ 0 görülür.

### 5.6 Tedarik ve fatura akışı (`referans/tedarik-ve-fatura.md`)

| Kademe | Ne zaman | Nasıl | Risk |
|---|---|---|---|
| A. Test stoğu | ilk 5–20 satış | Trendyol'dan kendi adresine perakende alım, **kurumsal fatura** ile; kendi paketinle gönderim | stok parası bağlanır; fatura kurumsal değilse KDV indirilemez |
| B. Satıcıyla doğrudan | haftada ≥ 10 satış | Trendyol satıcı profilindeki firma unvanından doğrudan toptan; fatura firmadan firmaya | satıcı toptan vermeyebilir |
| C. Üretici / ithalat | ayda ≥ 100 satış | 1688 ya da yerli üretici; marj en yüksek | süre, gümrük, minimum adet |

- **Yasak varsayılan:** Trendyol siparişini doğrudan müşteri adresine göndermek. Sebep: paket ve fatura Trendyol satıcısından gider, fiyat müşteriye görünür, marka kırılır. Trendyol kullanım koşulları açısından durumu **doğrulanmadı**; bu yol yalnız kurucu açıkça isterse ve KARARLAR'a yazılırsa açılır.
- Vergi ve fatura cümleleri hüküm değildir: dosyanın başına `Bilgi notu (kullanıcının sorumluluğu): mali müşavirle doğrula.` satırı girer.
- Satın alma, numune, satıcıyla temas: kurucu onayı olmadan yok; onay KARARLAR.md'ye.

### 5.7 Fiyat şeffaflığı riski (`referans/fiyat-seffafligi.md`)
Puan 0–3; her "evet" 1 puan:
1. Ürünün Türkçe genel adı Google'da arandığında ilk sayfada Trendyol kartı aynı görselle çıkıyor mu?
2. Tedarikçi fotoğrafıyla görsel arama aynı ürünü ilk sonuçlarda veriyor mu?
3. Ürün tek başına, set ya da ek parça olmadan mı satılacak (birebir fiyat karşılaştırması mümkün mü)?

Aşma yolları (kanıt dosyasına hangisinin uygulanacağı yazılır):
- **Marka:** kendi marka adı ve ürün adı; Trendyol'daki genel ad başlıkta kullanılmaz (Builder Aşama 1).
- **Görsel:** tedarikçi fotoğrafı sitede kullanılmaz; galeri Builder Aşama 2'de yeniden üretilir.
- **Paket:** 2'li/3'lü set ya da tamamlayıcı ek parça (birebir karşılaştırmayı bozar).
- **Teklif:** garanti, iade süresi, kapıda ödeme, hızlı kargo (Builder `teklif` bölümü).
- **Kreatif:** talep videoyla yaratılır (Studio); arayan değil gören müşteri.
- Yapılmaz: sahte çizili fiyat, sahte stok, sahte yorum (IDD-02).

### 5.8 Dosyalar

| Dosya | Yazan | İçerik |
|---|---|---|
| `is/firsat/trendyol/aramalar.tsv` | betik | tarih · terim · kaynak (dna/aile) · bakılan sayfa · sonuç |
| `is/firsat/trendyol/kota.tsv` | betik | tarih · saat · tür (arama/urun) · hedef · kilit |
| `is/firsat/trendyol/adaylar.tsv` | Scout + betik | `no, urun, trendyol_link, alis_tl, yorum, puan, satici_sayisi, satici, gorsel_bakildi, mekanizma, aile, viral_db, viral_video, meta_reklam, onerilen_satis_tl, on_karar, karar, neden, okuma_tarihi` |
| `is/firsat/trendyol/marj.csv` + `marj-sonuc.tsv` | lider + betik | §5.5 |
| `is/firsat/trendyol/elenenler.tsv` | betik | link · sebep · tarih (bir daha önerilmez) |
| `is/firsat/kanit/NN-urun-adi.md` | Skeptic | Hunter şablonu + 3 ek bölüm |
| `is/firsat/trendyol/urunler.xlsx` | `excel_hazirla.py` → `ortak/excel_yaz.py` | §6 |

`bazaar_kontrol.py` alt komutları: `kota durum|kaydet|kilit` · `tekrar <link ya da ad>` · `denetle <adaylar.tsv>` · `viral --db <yol> <adaylar.tsv>` · `sinama <adaylar.tsv>` (rastgele 3 satır yeniden açılıp karşılaştırılır). Çıkış: 0 tamam · 1 veri hatası · 2 kullanım · 3 kilit · 4 günlük tavan.

### 5.9 Kapılar
1. `kota` çıkış 0 olmadan istek yok.
2. `denetle` çıkış 0 olmadan kısa liste yok.
3. `sinama` 3/3 tutmadan kullanıcıya "bulundu" denmez.
4. `tr_marj.py` çıkış 0 olmadan marj yazılmaz.
5. Kanıt dosyası olmadan SAT yok (`ortak/sozluk.md`).
6. `excel_yaz.py` çıkış 0 olmadan "Excel hazır" denmez.

### 5.10 Riskler (kullanıcıya özetin son satırında tek cümleyle yazılır)
- Trendyol değerlendirme sayısı satış adedi değildir; talep vekilidir.
- Eşiklerin yarısı varsayım; ilk 20 üründe karar **DENEME** etiketlidir.
- Müşteri ürünü Trendyol'da ucuza bulabilir (§5.7); marj bu riske göre okunur.
- TR'de reklam maliyeti ölçülmedi; `reklam_payi_yuzde` dolana kadar `net_kar` hesaplanmaz.

---

## 6. Tek Excel şablonu

### 6.1 Kural
Radar, Spy, Hunter, Bazaar **aynı** dosya düzenini üretir. Tam 3 sayfa. Birleştirilmiş hücre yok. Üstte başlık/banner satırı yok: 1. satır sütun adlarıdır.

**Sayfa 1 — "Ürünler"** (tam 10 sütun)

| # | Sütun adı | Tür | Genişlik | Not |
|---|---|---|---|---|
| A | Ürün | metin | 38 | kısa ad |
| B | Link | köprü | 9 | hücre metni `aç`, köprü tam URL |
| C | İlgi | metin | 22 | kaynağa göre: `2,4 Mn izlenme` · `969 yorum · 4,1` · `57 satış` · `12 reklam · 45 gün` |
| D | Alış | sayı | 11 | para biçimi satırın `para` alanından (`₺` / `$` / `€` / `£`); bilinmiyorsa boş |
| E | Satış | sayı | 11 | aynı |
| F | Marj (kat) | sayı `0.0"×"` | 10 | marj betiğinden gelen çarpan; yoksa boş. Betik kendi hesaplamaz |
| G | Karar | metin | 9 | yalnız `SAT` / `İZLE` / `ELE`; hücre rengi: SAT `C6EFCE`, İZLE `FFEB9C`, ELE `FFC7CE`; kalın |
| H | Neden | metin | 60 | tek cümle, ≤ 140 karakter, satır kaydırma açık |
| I | Kaynak | metin | 12 | `Instagram` / `Meta reklam` / `AliExpress` / `Trendyol` |
| J | Tarih | tarih `yyyy-mm-dd` | 11 | okuma tarihi |

Biçim: 1. satır kalın, beyaz yazı, zemin `1F2937` · `freeze_panes = "A2"` · `auto_filter` = `A1:J<son>` · sıralama: SAT, İZLE, ELE; her grupta `ilgi_sayi` büyükten küçüğe · satır yüksekliği otomatik.

**Sayfa 2 — "Ayrıntı":** kaynağın ham tablosu, sütunları olduğu gibi (sınır yok). 1. satır sütun adı, dondurulmuş, filtreli. Birden çok ham dosya verilirse yalnız ilki yazılır, diğerleri için uyarı basılır (tek ham tablo kuralı).

**Sayfa 3 — "Nasıl okunur":** iki sütun (`Ne`, `Anlamı`), en çok 12 satır: 10 sütunun birer satırlık anlamı + karar renkleri + kaynağa özgü "İlgi" tanımı. Metin betiğin içinde sabittir.

### 6.2 Betik: `ortak/excel_yaz.py`
```
python3 "${CLAUDE_PLUGIN_ROOT}/ortak/excel_yaz.py" \
  --urunler <urunler.tsv> --kaynak <radar|spy|hunter|bazaar> --cikti <dosya.xlsx> \
  [--ayrinti <ham.tsv|.csv|.md>] [--kopya <klasör>]
```
- Girdi `urunler.tsv` (sekme, başlıklı, UTF-8), 12 alan: `urun, link, ilgi, ilgi_sayi, alis, satis, para, marj_kat, karar, neden, kaynak, tarih`.
- Doğrulama (yazmadan önce; biri tutmazsa çıkış 1, dosya yazılmaz): başlık tam bu 12 alan · `karar` ∈ {SAT, İZLE, ELE} · `urun` dolu · `link` boş ya da `http` ile başlar · `alis`, `satis`, `marj_kat`, `ilgi_sayi` boş ya da sayı (ondalık virgül kabul edilir) · `tarih` `YYYY-AA-GG` · `neden` ≤ 140 karakter · `para` ∈ {TRY, USD, EUR, GBP, boş}.
- Yazdıktan sonra **dosyayı yeniden açar ve ölçer** (tutmazsa çıkış 1): sayfa adları tam `["Ürünler", "Ayrıntı", "Nasıl okunur"]` · Ürünler `max_column == 10` · veri satırı sayısı = girdi satırı · birleştirilmiş hücre 0 · `freeze_panes == "A2"` · `auto_filter.ref` dolu.
- `--ayrinti` `.md` ise ilk Markdown tablosunu okur. `--kopya` verilirse dosyayı o klasöre de kopyalar (kurucunun masaüstü rapor klasörü; yolu Captain KARARLAR'daki `| excel-klasoru |` satırından verir, satır yoksa kopyalanmaz).
- Çıkış: 0 `TAMAM <yol> · N ürün (SAT a / İZLE b / ELE c)` · 1 veri ya da doğrulama hatası · 2 kullanım hatası · 3 `openpyxl` yok (kurulum komutunu basar).
- `ortak/excel_test.py` (kırma testi, en az 8 test): geçersiz karar · 11 alanlı başlık · 141 karakter neden · bozuk tarih · boş girdi (0 ürün → çıkış 1) · doğru girdi → çıkış 0 ve 6 ölçümün hepsi · ondalık virgül · `.md` ayrıntı. Her red önce görülür.

### 6.3 Kim çağırır (her beceride ince bir hazırlayıcı; şablonu hiçbiri kendisi çizmez)

| Beceri | Hazırlayıcı | Okuduğu kaynak | Karar eşlemesi | "İlgi" | Çıktı |
|---|---|---|---|---|---|
| Radar | `skills/radar/scripts/excel_yap.py` (adı kalır, gövdesi hazırlayıcı olur) | `is/kesfet/urunler.md` | `AL` ve `AL (sezonluk)` → SAT (sezonluk notu Neden'in başına) · `YEDEK` → İZLE · `ELE` → ELE | izlenme | `is/kesfet/kesfet-urunler.xlsx` (yol aynı) |
| Spy | `skills/spy/scripts/excel_hazirla.py` (yeni) | `is/meta/sayfalar.tsv` | `OLCEKLENIYOR` → İZLE ("Hunter eşlemesine girer") · `ESKI-KAZANAN` → ELE · `TEST` ve `BILINMIYOR` yalnız Ayrıntı'da | `reklam_sayisi` reklam · `max_aktif_gun` gün | `is/meta/reklam-urunler.xlsx` |
| Hunter | `skills/hunter/scripts/excel_hazirla.py` (yeni) | `is/firsat/adaylar.md` + `marj_hesap.py --cikti` dosyası | `SAT` → SAT · `İZLE`, `AÇIK`, `KISA LİSTE` → İZLE · `ELE` → ELE | ürün sayfası satışı | `is/firsat/firsat-urunler.xlsx` |
| Bazaar | `skills/bazaar/scripts/excel_hazirla.py` (yeni) | `is/firsat/trendyol/adaylar.tsv` + `marj-sonuc.tsv` | `karar` sütunu aynen; boşsa `on_karar` (`SAT-ADAYI` → İZLE) | yorum · puan | `is/firsat/trendyol/urunler.xlsx` |

- Hazırlayıcı yalnız iki iş yapar: `urunler.tsv` yazar, sonra `excel_yaz.py`'yi alt süreç olarak çağırır ve çıkış kodunu aynen döndürür.
- SAT yalnız kanıt dosyası olan üründe yazılır (Hunter ve Bazaar). Spy hiçbir zaman SAT yazmaz.
- Radar'ın eski ek sayfaları (Marka Skorları, Rakip & Notlar, Özet) Excel'e girmez; `.md` dosyalarında kalır. Radar `SKILL.md` satır 80'deki sayfa listesi güncellenir.
- ChatGPT paketinde `ortak/excel_yaz.py` `skills/ekip-bilgi/references/` altına bayt bayt gider (mevcut kural); hazırlayıcılar kod yorumlayıcıda koşulur.

---

## 7. Uygulama planı (Sonnet için)

**Genel kurallar**
- Dal: `yapilanma-0.4.0`. Her FAZ sonunda tek commit; `git add` dosya adıyla (asla `-A` / `.`); commit öncesi `git status --short`.
- Taşıma her zaman `git mv`. Üretilen klasör (`skills/builder/`) elle düzenlenmez.
- Bir adımın "Doğrula" komutu geçmeden sonraki adıma geçilmez. Geçmiyorsa dur, çıktıyı rapora yaz.
- Test güncellemesi yalnız **ad ve numara** değiştirir; hiçbir `assert` silinmez, hiçbir eşik gevşetilmez. Silmek zorunda kalırsan dur ve bildir.
- Yayın, `git push`, Releases yüklemesi bu planın dışında (kurucu onayı).

### FAZ 0 — Başlangıç ölçümü
1. `git checkout -b yapilanma-0.4.0`. Doğrula: `git status --short` boş.
2. Bütün kapıları koş ve çıkış kodlarını rapora yaz (hepsi 0 olmalı; değilse dur):
   `python3 scripts/sozlesme_test.py` · `python3 scripts/butce_kontrol.py` · `python3 scripts/butce_kontrol.py --kendini-sina` · `python3 moduller/magaza-kurucu/tools/build.py --check` · `python3 -m pytest -q moduller/magaza-kurucu/tests` · `python3 plugins/viral-urun-ekibi/skills/ekip-lideri/scripts/kapi_test.py` · `…/karne_test.py` · `…/video-kurgu/scripts/kendini_test.py` · `…/juri_test.py` · `…/reklam-kutuphanesi-avi/scripts/kendini_test.py` · `…/toplayici_test.py` · `…/teklif-ve-sayfa/scripts/kirma_testi.py` · `…/aliexpress-firsat/scripts/kirma_testi.py` · `sh scripts/anonim_kontrol.sh` · `sh scripts/paketle.sh`.

### FAZ 1 — Ad haritası ve ad kapısı
3. `plugins/viral-urun-ekibi/ortak/ad-haritasi.tsv` yaz (§1.2, §1.3, §1.4; 9 beceri satırı + 27 ajan satırı). Doğrula: `awk -F'\t' 'NR>1' <dosya> | wc -l` = 36.
4. `scripts/ad_testi.py` yaz. Kapılar (çıkış 1):
   a. `skills/*/SKILL.md` içinde alias işareti olmayan her becerinin klasör adı = frontmatter `name` = haritadaki bir `yeni` değeri (üçüncü taraf 4 beceri hariç, sabit liste).
   b. `agents/*.md` dosya adları kümesi = haritadaki ajan `yeni` değerleri kümesi (17).
   c. Beceri ve ajan `yeni` değerleri birlikte benzersiz.
   d. Haritadaki her beceri `eski` değeri için alias klasörü var, içinde yalnız `SKILL.md` var, işaretteki hedef mevcut bir beceri.
   e. Eski kimliklerden hiçbiri izinli yerler dışında geçmiyor. İzinli: alias klasörleri · `ortak/ad-haritasi.tsv` · `CHANGELOG.md` · `docs/gelistirici/` · `dist/` · `.git/` · `moduller/magaza-kurucu` yol parçası · `analiz_db_aktar.py` içindeki `"kaynak"` satırı · `ortak/roller/*/*.md` ilk satırındaki `(eski: …)`.
   f. Her beceri ve ajan `description` alanı `<Kod adı> (` ile başlıyor.
   g. Birleşen her ajanın her modu için `ortak/roller/<kod>/<mod>.md` var.
   `--kendini-sina`: geçici kopyada her kapıyı bir kez kırar ve çıkış 1 görür (butce_kontrol.py ile aynı desen).
   Doğrula (bu aşamada): `python3 scripts/ad_testi.py` çıkış **1** (henüz taşınmadı; kapının kırmızı olduğunu gör). Rapora yaz.

### FAZ 2 — Becerileri taşı
5. `git mv` (7 klasör): `ekip-lideri`→`captain` · `kesfet-urun-avi`→`radar` · `reklam-kutuphanesi-avi`→`spy` · `aliexpress-firsat`→`hunter` · `ai-video-kreatif`→`studio` · `video-kurgu`→`cut`. `magaza-kurucu` klasörünü `git mv` ile `builder` yap (içeriği FAZ 6'da yeniden üretilecek). `teklif-ve-sayfa` şimdilik yerinde kalır.
6. `git mv ekler/chatgpt/`: `kesfet-urun-avi.md`→`radar.md` · `aliexpress-firsat.md`→`hunter.md` · `ai-video-kreatif.md`→`studio.md` · `video-kurgu.md`→`cut.md`.
7. Atıf değişimi için **tek seferlik** Python betiği yaz (depoya girmez, geçici klasörde durur). Kurallar:
   - Eşlemeyi `ad-haritasi.tsv`'den okur; yalnız `tur=beceri` satırları, `teklif-ve-sayfa` **hariç**.
   - Desen: `(?<![\w-])<eski>(?![\w-])`. Önce `moduller/magaza-kurucu` dizgisini yer tutucuya çevirir, değişimden sonra geri koyar.
   - Kapsam: depodaki metin dosyaları (`.md .py .sh .js .json .yml .yaml .tsv .csv .txt .swift .gitattributes`).
   - Hariç: `.git/` · `dist/` · `docs/gelistirici/` · `CHANGELOG.md` · `plugins/viral-urun-ekibi/licenses/` · `skills/hyperframes*/` · `skills/media-use/` · `.pytest_cache/`.
   - Bitince değişen dosya sayısını ve dosya başına değişim sayısını basar.
8. Betiği koş. Sonra **elle geri al**: `skills/spy/scripts/analiz_db_aktar.py` içindeki `"kaynak": "spy"` → `"kaynak": "reklam-kutuphanesi-avi"` (veri değeri).
9. Frontmatter: 7 becerinin `description` alanının başına `<Kod adı> (<Türkçe rol>). <İngilizce görev>. ` ekle (§1.2). Captain'de `model: fable` satırı kalır.
10. Captain `SKILL.md`: "(ekipteki adın Kerem)" ve "unvanı ve adıyla an" cümlelerini §1.1 madde 3'e göre değiştir; "27 üye" → "17 üye"; §1 madde 2'ye §1.5'teki eski ad cümlesini ekle. **Bayt sınırı:** dosya bugün 11.949 / 12.000 bayt. Sınır aşılırsa "Yayın döngüsü" paragrafını `referans/yayin-dongusu.md`'ye taşı, yerine tek satır atıf bırak.
    Doğrula (FAZ 2): `python3 scripts/butce_kontrol.py` 0 · `captain/scripts/kapi_test.py` 0 · `karne_test.py` 0 · `cut/scripts/kendini_test.py` 0 · `juri_test.py` 0 · `spy/scripts/kendini_test.py` 0 · `toplayici_test.py` 0 · `hunter/scripts/kirma_testi.py` 0.

### FAZ 3 — Alias'lar
11. 8 alias klasörü ve `SKILL.md` dosyası yaz (§1.5 kalıbı; `teklif-ve-sayfa` alias'ı FAZ 6 adım 22'den sonra yazılır).
12. `hooks/durum-yukle.sh`'e §1.5'teki satırı ekle.
    Doğrula: `claude plugin validate plugins/viral-urun-ekibi` çıkış 0 (CLI yoksa "ölçülmedi" yaz). Çıkış ≠ 0 ve hata `disable-model-invocation` ise o satırı 8 dosyadan sil, yeniden doğrula, rapora yaz.

### FAZ 4 — Ürün ve video ajanları (7)
13. `git mv agents/`: `firsat-avcisi`→`scout` · `kanit-savcisi`→`skeptic` · `kreatif-analisti`→`decoder` · `icerik-stratejisti`→`story` · `video-juri`→`jury` · `video-elestirmen`→`fixer` · `ses-tasarimcisi`→`mixer`.
14. Adım 7'deki betiği bu 7 ajan satırıyla yeniden koş.
15. Her dosyada yalnız şunlar değişir: frontmatter `name` · `description` başı (`<Kod adı> (<Türkçe rol>). <İngilizce görev>. ` + eski açıklamanın insan adı ve unvanı çıkarılmış hâli) · `# Başlık` · "Ekipteki adın **X**; kullanıcıya … diye anılırsın" cümlesi → `Kullanıcıya "<Kod adı> (<Türkçe rol>)" diye anılırsın.` **`jury.md` gövdesine başka hiçbir değişiklik yapılmaz** (kalibrasyon kuralı). `model:` ve `tools:` aynı kalır.
    Doğrula: `git diff --stat` içinde `jury.md` için değişen satır ≤ 6 · `juri_test.py` 0 · `kapi_test.py` 0.

### FAZ 5 — Mağaza ajanları (20 → 10)
16. Tek modlu 3 rol: `git mv` `metin-yazari`→`copy` · `kor-elestirmen`→`panel` · `tasarim-direktoru`→`director`; §4.3 madde 3'ü uygula (`copy` modeli `sonnet`).
17. Birleşen 7 rol için §4.3 madde 1–2: 17 eski gövdeyi `ortak/roller/<kod>/<mod>.md`'ye taşı (`git mv` + başlık satırı düzenlemesi), 7 yeni `agents/<kod>.md` yaz (§4.1 model ve araçlar), 17 eski ajan dosyası böylece `agents/` altından çıkmış olur.
18. Adım 7'deki betiği mağaza ajan satırlarıyla koş (çoktan-bire eşleme: eski ad → `<kod>`). Sonra `grep -rn "\`atlas\`, \`atlas\`\|\`probe\`, \`probe\`"` benzeri yinelenmeleri ara ve tekilleştir.
19. `ortak/ekip.md`'yi §4.4'e göre yeniden yaz. `ortak/magaza-ekibi.md`: §1'deki unvan örneğini kod adına çevir; §4 "zevk puanı `panel`"; §2 tablosuna satır ekle: `Rol mod dosyaları | ${CLAUDE_PLUGIN_ROOT}/ortak/roller/<kod>/<mod>.md`.
    Doğrula: `ls plugins/viral-urun-ekibi/agents | wc -l` = 17 · `python3 scripts/butce_kontrol.py` 0 (ajan ≤ 7.000 bayt, kadro modeli = dosya modeli) · her eski gövdenin taşındığını say: `ls plugins/viral-urun-ekibi/ortak/roller/*/*.md | wc -l` = 17.

### FAZ 6 — Mağaza 3 aşama + teklif bölümü (kaynak: `moduller/magaza-kurucu/`)
20. `tools/build.py`: `SKILLER = ["urun-analiz", "teklif", "marka", "metinler", "gorseller", "shopify-kurulum"]`. `KOPYALAR`'da `00-calisma-tarzi.md` ve `01-kurallar.md` `TUM` olduğu için `teklif`'e kendiliğinden gider; `ekip-koprusu.md` listesine `"teklif"` ekle. (Adım 7 betiği `TEK_KOK`, zip adları, `BIRLESIK` yolu ve `surum.json` `name` denetimini zaten `builder` yaptı; `openai.yaml` görünen ad denetimi `"Mağaza Kurucu"` kalır.)
21. `skills/teklif/` kur (`git mv` ile `plugins/viral-urun-ekibi/skills/teklif-ve-sayfa/` içinden): `referans/*` → `references/` · `sablon/*` → `assets/` · `scripts/*` → `scripts/`. `agents/openai.yaml` başka bir bölümünkinden kopyalanıp ad ve açıklaması uyarlanır.
22. `skills/teklif/SKILL.md` yaz (≤ 5.120 bayt; `name: teklif`; frontmatter yalnız `name` + `description`): §3.4 içeriği + eski becerinin "Akış" 1–7 adımları. Eski "Kurallar (pazarlıksız)" bloğu **aynen** `references/teklif-kurallari.md`'ye taşınır. Dosyada `${CLAUDE_…}` kalmaz: yollar `references/…`, `scripts/…`, `assets/…`. Eklentiye özgü dosyalar (`ortak/sozluk.md`, `ortak/kurallar.md`, pazar katmanı) "varsa oku" diye anılır. Karakter hatırlatma satırı: `AŞAMA 1/3 · ADIM 3/9 · Atlas · …`.
23. `src/tek/SKILL.md` (sıralayıcı; ≤ 5.120 bayt, `name: builder`): "5 aşama" → "3 aşama"; aşama tablosu §3.1 (her bölüm için `` `<bölüm>/ASAMA.md` `` yolu tabloda geçmeli, `build.py` bunu denetler); durum satırı §3.2; "Çalışma modu" bölümünde "aşama 3" → "Aşama 2 (görseller)", "aşama 5" → "Aşama 3 (site)".
24. Bölüm `SKILL.md` dosyaları (6 adet): "Akış" satırı yeni sırayla (`1 urun-analiz → 2 teklif → 3 marka → 4 metinler → 5 gorseller → 6 shopify-kurulum`; başına "AŞAMA a/3") · karakter hatırlatma satırları §3.2 numara ve kod adlarıyla · "sıradaki" atıfları: `urun-analiz` → `teklif` · `teklif` → `marka` · `marka` → `metinler` · `metinler` → `gorseller` · `gorseller` → `shopify-kurulum` · ön koşul cümleleri §3.3 madde 4 · `metinler`'e §3.3 madde 1 ve 3 · `gorseller`'e §3.3 madde 2 · `urun-analiz` adım 4'ün onay sorusu kalkar (onay `teklif` sonunda, §3.4).
25. `src/ortak/00-calisma-tarzi.md`: KARAKTER bloğunda durum satırı biçimi ve örneği (§3.2) · UNVANLAR satırı §3.2 kod adlarıyla · "MESAJ BAŞLIĞI NUMARASI" satırı 9 adımla · DEVAM KARTI şablonuna §3.5'teki 2 satır ve "Eski kart kuralı". Kaynak metin (`MASTER PROMPT …` altı) **değişmez**; yalnız "AKIŞ" altındaki "Skill sırası" satırı yeni sırayla yazılır.
26. `src/ortak/ekip-koprusu.md`: §3 temasız mod ve §4'teki `teklif-ve-sayfa/referans/yasak-ifadeler.tsv` → `teklif/references/yasak-ifadeler.tsv`; "teklif becerisi" → "`teklif` bölümü"; §7'deki 5 denetçi adı → `probe` (mod `hiz`, `erisim`, `arama`) ve `shopper` (mod `donusum`, `ses`). `marka/references/namelix-ajan.md`: `ADIM 3/8 · Brand Strategist (Elif)` → `AŞAMA 1/3 · ADIM 4/9 · Atlas`.
27. Testler (yalnız ad ve numara): `test_karakter.py` (`SKILLER` 6 bölüm; biçim dizgileri ve regex `ADIM \d/9`; örnek satır) · `test_tek_paket.py`, `test_birlesik.py` (bölüm listeleri; lider dosyasında aranan parçalar) · `test_manifest.py` (yol). `test_kaynak_kapsam.py` regex'i (`ADIM \d/8`) **değişmez** (kaynak metni ölçer).
28. `surum.json`: `version` `0.6.0`. Modül `README.md`: "5 aşama" → "3 aşama, 6 bölüm".
29. `python3 moduller/magaza-kurucu/tools/build.py` (üretir). Sonra `plugins/viral-urun-ekibi/skills/teklif-ve-sayfa/` altında kalan dosya olmadığını gör ve alias `SKILL.md`'sini yaz (adım 11).
30. Eklenti tarafındaki yollar: `captain/scripts/kapi.py` ve `kapi_test.py` içinde teklif betiğine giden yol varsa `skills/builder/teklif/scripts/teklif_kontrol.py` · `scripts/sozlesme_test.py` satır 92: `skills/builder/teklif/assets/teklif.tsv` · `captain/referans/uctan-uca-hat.md` adım 2: "Teklif: `builder` Aşama 1 (`teklif` bölümü)" · Captain yönlendirme tablosu: teklif satırı silinir, Builder satırı "(3 aşama)" olur, Bazaar satırı eklenir (`Trendyol'dan ilgi gören ürün | bazaar | scout, sonra skeptic`), site denetimi satırı "Builder Aşama 3".
    Doğrula (FAZ 6): `build.py --check` 0 · `pytest -q moduller/magaza-kurucu/tests` 0 · `python3 plugins/viral-urun-ekibi/skills/builder/teklif/scripts/kirma_testi.py` 0 · `python3 scripts/sozlesme_test.py` 0 · `wc -c moduller/magaza-kurucu/skills/*/SKILL.md moduller/magaza-kurucu/src/tek/SKILL.md` her biri ≤ 5.120.

### FAZ 7 — Ortak Excel
31. `ortak/excel_yaz.py` ve `ortak/excel_test.py` yaz (§6.1, §6.2). Doğrula: `python3 plugins/viral-urun-ekibi/ortak/excel_test.py` 0 (her red görüldü).
32. Radar: `scripts/excel_yap.py` gövdesini hazırlayıcıya çevir (§6.3); `SKILL.md`'deki sayfa listesini güncelle. Spy ve Hunter: `scripts/excel_hazirla.py` yaz; `SKILL.md`'lerine tek satır ekle ("Tur sonunda: `excel_hazirla.py` → çıktıda `TAMAM`"). Doğrula: her hazırlayıcı için elle kurulmuş 3 satırlık örnek girdiyle çıkış 0 ve üretilen dosyada sayfa adları + `max_column == 10` (ölçümü `excel_yaz.py` kendisi basar).
33. Gerçek veriyle bir kez (salt okunur, proje klasöründeki Radar verisinden): çıktıdaki `TAMAM … N ürün` satırını rapora yaz.

### FAZ 8 — Bazaar
34. `skills/bazaar/` dosyalarını yaz (§5; ağaç §2). `SKILL.md` ≤ 120 satır ve ≤ 12.000 bayt; ayrıntı `referans/` dosyalarında. `referans/esikler.tsv` §5.4 tablosundan; `referans/tr-oranlari.tsv` boş değerli (§5.5).
35. `scripts/kirma_testi.py` yaz ve koş. Doğrula: çıkış 0, ≥ 10 test, her kapı önce kırmızı görüldü.
36. Deneme verisiyle kuru koşu: proje klasöründeki `firsat/trendyol/deneme-2026-11-23.tsv`'yi `adaylar.tsv` biçimine çevirip `denetle` + `excel_hazirla.py` koş. Beklenen: 5 satır; mantar lamba (10.314 yorum) ELE; tırnak makası İZLE (`aile-var`). Tutmazsa eşik değil **betik** incelenir; sonucu rapora yaz. (Tarayıcı açılmaz, Trendyol'a istek atılmaz.)

### FAZ 9 — Paketleme, CI, belgeler
37. `scripts/chatgpt_paketi_yap.sh`: alias işaretli becerileri (`<!-- alias:`) pakete alma · `ortak/roller/` klasörünü alma · `OZEL` sözlüğünden `teklif-ve-sayfa` anahtarını sil, `bazaar` anahtarı ekle (Trendyol sayfalarını kullanıcı açar; `bazaar_kontrol.py`, `tr_marj.py`, `excel_hazirla.py` kod yorumlayıcıda koşulabilir) · `BECERI_ON` desenine `bazaar` ekle, `teklif-ve-sayfa` çıkar · ChatGPT notlarındaki "5 aşama" ve rol adı cümlelerini güncelle · `HAM = {"builder"}`.
38. `.github/workflows/ci.yml`: yolları yeni klasör adlarıyla yaz; ekle: `python scripts/ad_testi.py` + `--kendini-sina` · `python plugins/viral-urun-ekibi/ortak/excel_test.py` · `python plugins/viral-urun-ekibi/skills/bazaar/scripts/kirma_testi.py` · teklif kırma testi yolu `skills/builder/teklif/scripts/kirma_testi.py`. `scripts/butce_kontrol.py` `DISARIDA` listesinde `magaza-kurucu` → `builder`; alias işaretli `SKILL.md` çekirdek beceri sayımına girmez.
39. Belgeler: `README.md`, `README.en.md`, `claude/README.md`, `chatgpt/README.md`, `chatgpt/proje-paketi/*.md`, `plugins/viral-urun-ekibi/README.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/hata.yml`: beceri ve rol tablolarını §0'daki tablolarla değiştir; "27 üye" → "17"; "5 aşama" → "3 aşama"; `ortak/sozluk.md`'ye "Kod adı" ve "Alias" satırları. `plugin.json` ve `marketplace.json` açıklamalarına "Trendyol fırsat avı" ekle.

### FAZ 10 — Sürüm
40. `plugin.json` `version` `0.4.0`. `CHANGELOG.md`'de `## [Yayımlanmamış]` altına `## [0.4.0] - <uygulama günü>` (satırlar §7.1). Sonra **bütün kapılar** (FAZ 0 listesi yeni yollarla + yeni 4 test): hepsi çıkış 0. `sh scripts/paketle.sh` → iki ZIP adı `…-v0.4.0.zip`. `unzip -l` ile gör: Claude ZIP'inde 8 alias klasörü var, ChatGPT ZIP'inde yok; ChatGPT ZIP'inde `skills/bazaar/` ve `skills/builder/teklif/` var. `python3 scripts/ad_testi.py` 0 ve `--kendini-sina` 0.

### 7.1 CHANGELOG satırları (0.4.0)
```
### Eklendi
- Bazaar becerisi: Trendyol'da ilgi gören, henüz viral olmamış ürünleri bulur; net marj, tedarik ve fiyat şeffaflığı riskini hesaplar. Satış kendi Shopify mağazasında.
- Tek Excel şablonu (`ortak/excel_yaz.py`): bütün ürün bulma becerileri aynı 3 sayfalı, 10 sütunlu dosyayı üretir.
- Ad haritası (`ortak/ad-haritasi.tsv`) ve ad kapısı (`scripts/ad_testi.py`).

### Değişti
- Beceri adları kod adı oldu: Captain, Radar, Spy, Hunter, Builder, Studio, Cut. Eski adlar bu sürümde yönlendirme olarak çalışır.
- Ekip rolleri kod adıyla anılır; insan adları ve İngilizce unvanlar kalktı.
- Mağaza kurulumu 3 aşama: Plan, Görseller, Site. Site metinleri artık görsellerden önce yazılır; adım sayısı 8 → 9.
- Teklif ayrı beceri olmaktan çıktı; Builder'ın 1. aşamasında `teklif` bölümü oldu.
- Mağaza rolleri 20 → 10 (toplam ajan 27 → 17). Kör jüri ve kök neden rolleri ayrı kaldı.
- Radar Excel'i: Marka Skorları, Rakip & Notlar ve Özet sayfaları dosyadan çıktı (`.md` dosyalarında duruyor).

### Kaldırılacak (0.5.0)
- Eski beceri adlarının yönlendirmeleri: ekip-lideri, kesfet-urun-avi, reklam-kutuphanesi-avi, aliexpress-firsat, magaza-kurucu, teklif-ve-sayfa, ai-video-kreatif, video-kurgu.
```

### 7.2 Geriye uyumluluk özeti

| Ne | 0.4.0'da durum |
|---|---|
| `/viral-urun-ekibi:<eski beceri adı>` | çalışır (alias) |
| Eski ajan adıyla çağrı | çalışmaz; harita + oturum kancası uyarısı |
| `.ekip/` ve `is/` dosyaları | aynen okunur; yol değişmedi |
| Eski DEVAM KARTI (`ADIM n/8`, `Düzen` satırı yok) | çalışır (§3.5 eski kart kuralı) |
| `urun-paketi.json`, `magaza-paketi.json`, `video-paketi.json` | değişmedi (`surum` "2") |
| `is/kesfet/kesfet-urunler.xlsx` | aynı yol, yeni düzen |
| `is/NN-urun/teklif/teklif.tsv` | aynı yol, aynı şema |
| ChatGPT paketi | yeni ZIP eskisinin yerine yüklenir; alias yok |

### 7.3 Kapı ve test listesi (0.4.0 sonunda hepsi çıkış 0)

| # | Komut | Yeni mi |
|---|---|---|
| 1 | `python3 scripts/ad_testi.py` ve `--kendini-sina` | yeni |
| 2 | `python3 scripts/butce_kontrol.py` ve `--kendini-sina` | güncellendi |
| 3 | `python3 scripts/sozlesme_test.py` | yol |
| 4 | `python3 moduller/magaza-kurucu/tools/build.py --check` | güncellendi |
| 5 | `python3 -m pytest -q moduller/magaza-kurucu/tests` | ad ve numara |
| 6 | `captain/scripts/kapi_test.py`, `karne_test.py` | yol |
| 7 | `cut/scripts/kendini_test.py`, `juri_test.py` | yol |
| 8 | `spy/scripts/kendini_test.py`, `toplayici_test.py` | yol |
| 9 | `hunter/scripts/kirma_testi.py` | yol |
| 10 | `builder/teklif/scripts/kirma_testi.py` | yol |
| 11 | `ortak/excel_test.py` | yeni |
| 12 | `bazaar/scripts/kirma_testi.py` | yeni |
| 13 | `sh scripts/anonim_kontrol.sh` | aynı |
| 14 | `claude plugin validate plugins/viral-urun-ekibi` ve `.` | aynı |
| 15 | `sh scripts/proje_paketi_yap.sh` · `sh scripts/paketle.sh` | güncellendi |

---

## 8. Riskler

| # | Risk | Olasılık | Önlem |
|---|---|---|---|
| 1 | `disable-model-invocation` beceri dosyasında beklendiği gibi çalışmaz | orta (ölçülmedi) | adım 12: doğrulayıcı reddederse satır silinir; açıklama "Eski ad" ile başlar |
| 2 | Toplu ad değişimi veri değerini ya da modül yolunu bozar | orta | değişim betiği sınır desenli, `moduller/magaza-kurucu` korumalı; veri satırı elle geri alınır; `ad_testi.py` kapı e |
| 3 | Captain `SKILL.md` 12.000 bayt sınırını aşar (bugün 51 bayt boş) | yüksek | adım 10: paragraf referans dosyasına taşınır; bütçe kapısı ölçer |
| 4 | Sıra değişimi: metin görselden önce yazılınca görselle uyuşmayan başlık | orta | görsel metinleri Aşama 1'de kilitlenir; Aşama 2 yalnız karttan alır; üretilemeyen görsel "Bekleyen"e yazılır |
| 5 | Yarım kalmış eski mağaza işleri (eski kart) yeni sırayla karışır | orta | `Düzen: 3A` işareti + eski kart kuralı; ön koşullar sıraya değil karta bakar |
| 6 | Model düşüşü (opus → sonnet: copy, forge, sentinel, architect, muse) görsel kalitesini düşürür | orta | Panel (fable) kapısı aynı; iki tur eşik altı → o çağrıda opus (§4.4); mağaza karnesindeki sepete ekleme oranı izlenir |
| 7 | Birleşik ajan yanlış modla çalışır ya da mod dosyasını okumaz | düşük | brief'te `mod:` zorunlu; yoksa ajan işi yapmaz; `ad_testi.py` kapı g dosyaları sayar |
| 8 | Jüri talimatı yanlışlıkla değişir, kalibrasyon geçersizleşir | düşük | adım 15: `jury.md` diff ≤ 6 satır ölçülür |
| 9 | Bazaar eşikleri 5 ürünlük denemeden ve varsayımdan geliyor | yüksek | eşikler TSV'de `durum` sütunlu; ilk 20 üründe karar DENEME; marj oranları boş başlar, betik boşken HATA verir |
| 10 | Trendyol engeli ya da kullanım koşulu ihlali | orta | yalnız oku, günlük tavan, ≥ 15 sn, CAPTCHA'da kilit; doğrudan müşteri adresine sipariş varsayılan yasak |
| 11 | Müşteri ürünü Trendyol'da ucuza bulur | yüksek | fiyat şeffaflığı puanı karar ölçütü; marka, görsel, paket, teklif, kreatif aşma yolları kanıt dosyasında |
| 12 | Radar Excel'inden çıkan sayfaları kurucu arar | düşük | CHANGELOG satırı; veriler `.md` dosyalarında |
| 13 | Kurucunun bilgisayarındaki yerel ajan kopyaları (`firsat-avcisi-mcp`, `kanit-savcisi-mcp`) eski adla kalır | kesin | depo dışı; Sonnet dokunmaz. Captain'e ayrı iş: `scout-mcp`, `skeptic-mcp` olarak yeniden adlandır |
| 14 | Kurulu kullanıcıda eski sürüm önbelleği iki ad kümesini birlikte gösterir | düşük | sürüm 0.4.0 artışı önbelleği yeniler; README'ye "güncelledikten sonra oturumu yeniden başlat" satırı |

### Kapsam dışı (bilerek, 0.4.0'da yapılmaz)
- Mağaza bölüm klasörlerinin ve betik dosya adlarının İngilizceleştirilmesi.
- ChatGPT paketindeki `ekip-bilgi` becerisinin yeniden adlandırılması.
- Jury + Panel birleşmesi (0.5.0 adayı, kalibrasyon şartlı).
- Yorum bölümü (KARARLAR: "şimdilik yok").
- `tr-oranlari.tsv` değerlerinin doldurulması (araştırma turu ya da kurucu).
