# Katkı rehberi

Katkın için teşekkürler. Bu depo bir Claude Code eklenti kataloğudur; katalogdaki tek eklenti `plugins/viral-urun-ekibi/` altındadır (mağaza kolu dahil).
Ayrıntılı klasör sözleşmesi ve yazım kuralları: [docs/SARTNAME.md](docs/SARTNAME.md). Bu dosya kısa yoldur.

**İlk katkı, 3 adım:** (1) depoyu çatalla (fork) ve bir dal aç, (2) değişikliği yap, [§4](#4-pr-göndermeden-önce-zorunlu)'teki kapıları çalıştır,
(3) Pull Request aç (şablon seni yönlendirir). Davranış kuralları: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · güvenlik açığı: [SECURITY.md](SECURITY.md).
GitHub Actions (`.github/workflows/ci.yml`) testleri her PR'da çalıştırır; anonimlik denetimi kara liste depo dışında durduğu için CI'da
"atlandı" der, onu kendi bilgisayarında çalıştırman gerekir. In English: PRs and issues in English are welcome; user-facing text stays Turkish.

## 1. Yerelde kurulum (geliştirme için)

```sh
git clone https://github.com/armanvibecoding/viral-urun-ekibi-market.git
cd viral-urun-ekibi-market
```

Claude Code içinde yerel çalışma kopyanı katalog olarak ekle — böylece değişikliklerini yayına girmeden denersin:

```
/plugin marketplace add ./
/plugin install viral-urun-ekibi@viral-urun-market
```

Değişiklikten sonra `/plugin` → Marketplaces → viral-urun-market → Update (ya da Claude Code'u yeniden başlat).
Araç ön koşulları (ffmpeg, Python paketleri, Chrome eklentisi) için [claude/README.md](claude/README.md) içindeki "Gereksinimler" bölümüne bak.

## 2. Beceri eklemek veya değiştirmek

- Yeni beceri: `plugins/viral-urun-ekibi/skills/<beceri-adi>/SKILL.md` (frontmatter'da `name` ve `description` zorunlu).
  - `description` becerinin **ne zaman** çağrılacağını söyler; tetikleyici cümleleri buraya yaz.
  - `SKILL.md` kısa kalır (≤ 120 satır). Ayrıntı `referans/*.md` dosyalarına, çalıştırılabilir yardımcılar `scripts/`'e.
- Yol yazımı: beceri içinden `${CLAUDE_SKILL_DIR}/referans/x.md`, eklenti kökünden `${CLAUDE_PLUGIN_ROOT}/ortak/x.md`.
  **Mutlak yol (ev klasörünü ya da sürücü harfini içeren yol) yazma.** Bu değişkenler yalnız markdown gövdesinde açılır; Bash ortamında yoktur.
- Yeni ajan: `plugins/viral-urun-ekibi/agents/<ajan>.md` (frontmatter: `name`, `description`, `tools`).
  Açıklama ekip kalıbıyla başlar: `İngilizce unvan (Ad · Türkçe rol).` ve üye `ortak/ekip.md` tablosuna eklenir. Mağaza kolu
  ajanında frontmatter'dan sonraki ilk satır `<!-- kol: magaza -->` olur (ChatGPT paketine rol becerisi olarak girmez).
- Mağaza kolu (`skills/magaza-kurucu/`) **üretilen** klasördür, elle düzenlenmez. Kaynak: `moduller/magaza-kurucu/` (aşamalar
  `skills/`, ortak dosyalar `src/ortak/`). Değişiklikten sonra `python3 moduller/magaza-kurucu/tools/build.py`, sonra
  `python3 -m pytest -q moduller/magaza-kurucu/tests`. Her aşama SKILL.md ≤ 5.120 bayt.
- Köprü dosyalarının (`urun-paketi.json`, `magaza-paketi.json`, `video-paketi.json`) alanı değişirse üçü birlikte güncellenir:
  kaynak `moduller/magaza-kurucu/src/ortak/sozlesme/` (şemalar, `ornek/`, `paket_dogrula.py`) + `src/ortak/arayuz-sozlesmesi.md`;
  `surum` artar, alan silinmez. Sonra `python3 scripts/sozlesme_esitle.py` (kopya `plugins/viral-urun-ekibi/ortak/sozlesme/`),
  `python3 moduller/magaza-kurucu/tools/build.py` ve `python3 scripts/sozlesme_test.py` çıkış 0 olmalı. Betik: `ortak/paket.py`.
- Ortak bilgi (`ortak/`) birden çok becerinin kullandığı bilgidir. Bilgi bankasını (`ortak/bilgi/`) değiştirdiysen
  claude.ai/ChatGPT proje paketini yeniden üret: `sh scripts/proje_paketi_yap.sh` (çıktı `chatgpt/proje-paketi/yuklenecek/`). Yükleme ZIP'lerini `sh scripts/paketle.sh` üretir.
- Kullanıcıya görünen metin **Türkçe**; kod, değişken ve dosya adları İngilizce ya da ASCII Türkçe olabilir.
- Kullanıcı verisi eklentiye yazılmaz; çalışma çıktısı kullanıcının proje klasöründe (`.ekip/`, `is/`) durur.
- Davranışı değiştiren her PR'da `plugins/viral-urun-ekibi/.claude-plugin/plugin.json` içindeki `version`'ı artır ve `CHANGELOG.md`'ye bir satır ekle.

## 3. Bilgi bankasına katkı

Ürün, kreatif not veya ders eklerken **kaynağı ve ölçümü** yaz (izlenme/beğeni nereden okundu, hangi gün).
Doğrulanmamış sayı yazma; tahminse "tahmin" diye işaretle. Kendi mağazanın satış, ciro, kâr ya da tedarikçi
anlaşması bilgilerini ekleme — bu depo herkese açıktır.

## 4. PR göndermeden önce (zorunlu)

1. **Doğrulama:**
   ```sh
   claude plugin validate plugins/viral-urun-ekibi
   claude plugin validate .
   ```
   İkisi de `Validation passed` demeli.
2. **Python betikleri** değiştiyse en az bir kez çalıştır; `video-kurgu` için `python3 plugins/viral-urun-ekibi/skills/video-kurgu/scripts/kendini_test.py`.
3. **Arayüz sözleşmesi** (Mağaza Kurucu ile dosya alışverişi): `python3 scripts/sozlesme_test.py` çıkış 0 vermeli.
   `plugins/viral-urun-ekibi/ortak/sozlesme/` elle düzenlenmez (kaynağı Mağaza Kurucu deposu; `docs/SARTNAME.md` §8).
4. **Anonimlik ve güvenlik kontrolü** (aşağıda).
5. PR açıklamasına neyi neden değiştirdiğini ve nasıl denediğini yaz.

## 5. Anonimlik ve güvenlik

Bu paket kimseyi ele vermeyecek şekilde tasarlandı. Gönderdiğin hiçbir dosyada şunlar olmamalı:
adın, e-postan, telefonun, kendi mağaza/alan adın, kendi Instagram/TikTok hesabın, GitHub kullanıcı adın,
bilgisayarındaki mutlak yollar (ev klasörü adını içeren her yol), API anahtarı/token, müşteri verisi.

### Kişisel kara liste (önerilir)

`scripts/anonim_kontrol.sh`, **senin bilgisayarında, depo dışında** duran bir kara listeyle tüm dosyaları tarar.
Liste depoya girmez (girerse kendisi kimliğini ele verir).

```sh
mkdir -p ~/.config/viral-urun-ekibi
# Satır başına bir desen (ERE, büyük/küçük harf duyarsız). Örnek desenler — kendi bilgilerinle değiştir:
cat > ~/.config/viral-urun-ekibi/yasak.txt <<'LISTE'
ad-soyad
kullanici-adim
ornek@eposta\.com
magazam
LISTE
chmod 600 ~/.config/viral-urun-ekibi/yasak.txt

sh scripts/anonim_kontrol.sh          # depo kökünü tarar; temizse 0, eşleşme varsa dosya:satır basar ve 1 döner
```

- Betik ayrıca her `*.myshopify.com` alan adını işaretler. Bilgi bankasında bilerek tutulan **başka** mağazaların alt
  alan adlarını `~/.config/viral-urun-ekibi/myshopify-izin.txt` içine `a|b|c` biçiminde yazarak izinli yapabilirsin.
- Liste yolunu değiştirmek için `YASAK_DOSYASI=... IZIN_DOSYASI=... sh scripts/anonim_kontrol.sh`.
- Commit'lerin yazar bilgisi de kimlik taşır. İstersen GitHub'ın `<id>+<kullanici>@users.noreply.github.com`
  adresini kullan.
- Gizli bilgi (anahtar, şifre, `.env`) asla commit'lenmez; `.gitignore` bunları dışarıda bırakır. Yanlışlıkla
  gönderdiysen anahtarı hemen iptal et — geçmişten silmek yetmez.

## 6. Davranış

Saygılı ol, eleştiriyi koda yap, kişiye değil. Para harcayan, hesaba giriş yapan ya da başkası adına işlem yapan
adımlar her zaman kullanıcı onayından geçmeli — bu kuralı gevşeten PR kabul edilmez.
