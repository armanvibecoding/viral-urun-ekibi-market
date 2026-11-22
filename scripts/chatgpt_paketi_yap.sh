#!/bin/sh
# Viral Ürün Ekibi eklentisinden ChatGPT'ye yüklenebilir plugin ZIP'i üretir. Kaynağa DOKUNMAZ.
# Çıktı: dist/chatgpt/viral-urun-ekibi/ (dönüştürülmüş kopya) + dist/viral-urun-ekibi-CHATGPT-v<sürüm>.zip
# ZIP git içinde TUTULMAZ (dist/ .gitignore'da): her sürümde GitHub Releases sayfasına yüklenir (scripts/paketle.sh iki ZIP'i de üretir).
# Kullanım: sh scripts/chatgpt_paketi_yap.sh   (depo kökünden ya da herhangi bir yerden)
# Dönüşüm özeti:
#   - hooks/ ve agents/ pakete girmez; hook'un işi ekip-lideri SKILL.md başına talimat olur.
#   - HyperFrames becerileri (hyperframes, hyperframes-cli, hyperframes-registry, media-use) pakete GİRMEZ:
#     render yerel Node 22+ + Chrome + CLI ister (ChatGPT'de yok), iş döngüsü check/snapshot/render olmadan doğrulanamaz,
#     ZIP'i ~0,65 MB'tan ~2,6 MB'a ve 163 dosyadan ~385'e çıkarır; terim dönüşümü Apache-2.0 dosyalarını değiştirirdi.
#   - Çekirdek ekibin 7 ajanı -> ayrı skill (skills/<ajan-adı>/SKILL.md), aynı sohbette uygulanan rol.
#   - Mağaza kolu ajanları (dosyada "<!-- kol: magaza -->" işareti) pakete GİRMEZ: işleri magaza-kurucu aşama dosyalarının
#     içindedir (ChatGPT'de alt ajan yok; 20 rol becerisi tetik çakışması ve bağlam yükü olurdu).
#   - magaza-kurucu becerisi DÖNÜŞTÜRÜLMEDEN kopyalanır (kaynağı iki yüzey için yazılmış ve ChatGPT'de koşulmuş; ek not girmez).
#   - Köprü (ortak/paket.py + ortak/nis-esleme.tsv + ortak/sozlesme/) skills/ekip-bilgi/references/ altına bayt bayt girer;
#     .mcp.json girmez (ChatGPT kendi Shopify bağlantısını kullanır).
#   - Kök plugin.json'a com.openai arayüz bloğu (görünen ad, kısa açıklama, örnek istekler) yazılır.
#   - ortak/ -> skills/ekip-bilgi/references/ (ayrı bilgi skill'i); ekler/chatgpt/ -> skills/ekip-bilgi/references/chatgpt/
#   - ${CLAUDE_SKILL_DIR} / ${CLAUDE_PLUGIN_ROOT} -> paket köküne göreli yol; Claude'a özgü terimler nötr dile.
#   - Kökte plugin.json (agent-plugins şeması) + .claude-plugin/plugin.json (aynı ad/sürüm/açıklama).
#   - ortak/sozlesme/ (kollar arası arayüz sözleşmesi) ve ortak/ altındaki betik/veri dosyaları (.py, .tsv, .json) dönüştürülmeden,
#     bayt bayt kopyalanır (terim dönüşümü kodu ve OZET.json özetlerini bozardı).
set -e
KOK="$(cd "$(dirname "$0")/.." && pwd)"
KAYNAK="$KOK/plugins/viral-urun-ekibi"
DIST="$KOK/dist"
HEDEF="$DIST/chatgpt/viral-urun-ekibi"
SURUM="$(python3 -I -c 'import json,sys;print(json.load(open(sys.argv[1],encoding="utf-8"))["version"])' "$KAYNAK/.claude-plugin/plugin.json")"
ZIP="$DIST/viral-urun-ekibi-CHATGPT-v$SURUM.zip"

[ -f "$KAYNAK/.claude-plugin/plugin.json" ] || { echo "HATA: kaynak eklenti yok: $KAYNAK"; exit 1; }
command -v python3 >/dev/null || { echo "HATA: python3 gerekli"; exit 1; }
command -v zip >/dev/null || { echo "HATA: zip gerekli"; exit 1; }

rm -rf "$DIST/chatgpt" "$ZIP"
mkdir -p "$HEDEF"

python3 -I - "$KAYNAK" "$HEDEF" "$KOK/LICENSE" <<'PY'
import json, os, re, shutil, sys

kaynak, hedef, lisans = sys.argv[1], sys.argv[2], sys.argv[3]
METIN = {".md", ".txt", ".csv", ".tsv", ".py", ".sh", ".js", ".swift", ".json"}
ATLA_AD = {".DS_Store", "__pycache__"}

def oku(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def yaz(p, s):
    if p.endswith(".md"):
        s = onek_ekle(s)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)

# ---------- 1) Metin dönüşümü ----------
def yol_cevir(s, skill):
    """skill: dosyanın ait olduğu skill adı (CLAUDE_SKILL_DIR için) ya da None."""
    s = s.replace("${CLAUDE_PLUGIN_ROOT}/ortak/", "skills/ekip-bilgi/references/")
    s = s.replace("${CLAUDE_PLUGIN_ROOT}/ekler/chatgpt/", "skills/ekip-bilgi/references/chatgpt/")
    s = s.replace("${CLAUDE_PLUGIN_ROOT}/", "")
    s = s.replace("${CLAUDE_PLUGIN_ROOT}", ".")
    if skill:
        s = s.replace("${CLAUDE_SKILL_DIR}", "skills/" + skill)
    s = s.replace("${CLAUDE_PROJECT_DIR", "${PROJE_DIZINI")
    s = s.replace('"CLAUDE_PROJECT_DIR"', '"PROJE_DIZINI"')
    s = s.replace("CLAUDE_PROJECT_DIR", "PROJE_DIZINI")
    return s

# Sıra önemli: uzun ifade önce.
TERIM = [
    ("Claude in Chrome ile yap", "tarayıcı otomasyonuyla yap"),
    ("Claude in Chrome", "tarayıcı otomasyon eklentisi"),
    ('Chrome\'a "Claude" eklentisini kur, `/chrome` ile bağla', "Chrome'a tarayıcı otomasyon eklentisini kur ve bağla"),
    ("Chrome + Claude eklentisi", "Chrome + tarayıcı otomasyon eklentisi"),
    ("`/mcp` → computer-use → Enable", "bilgisayar kontrolü aracını aç"),
    ("Claude eklentisi", "tarayıcı otomasyon eklentisi"),
    ("Claude'u çalıştıran uygulamayı (Terminal / Claude)", "asistanı çalıştıran uygulamayı (Terminal / asistan uygulaması)"),
    ("Claude'u çalıştıran uygulama (Terminal ya da Claude)", "asistanı çalıştıran uygulama (Terminal ya da asistan uygulaması)"),
    ("Claude oturumu", "asistan oturumu"),
    ("Claude'un", "asistanın"),
    ("Claude'u", "asistanı"),
    ("Claude", "asistan"),
    ("computer-use", "bilgisayar kontrolü aracı"),
    ("javascript_tool", "sayfada-JS-çalıştırma aracı"),
    ("get_page_text", "sayfa-metni-okuma"),
    ("WebFetch", "düz web isteği"),
    ("WebSearch", "web araması"),
    ("oturum kancası zaten bağlama basmış olabilir", "kullanıcı son DURUM bloğunu yapıştırmış olabilir"),
    ("Alt ajanın", "Yardımcı rolün"),
    ("Alt ajana", "Yardımcı role"),
    ("alt ajanlarda", "yardımcı rollerde"),
    ("alt ajanına", "rolüne"),
    ("alt ajana", "yardımcı role"),
    ("Alt ajan", "Yardımcı rol"),
    ("alt ajan", "yardımcı rol"),
]

BECERI_ON = re.compile(r"(?<![\w/.-])((?:ai-video-kreatif|aliexpress-firsat|video-kurgu|kesfet-urun-avi|ekip-lideri|reklam-kutuphanesi-avi|teklif-ve-sayfa)/(?:referans|scripts|sablon)\b)")

def onek_ekle(s):
    """`ai-video-kreatif/referans/x.md` gibi öneksiz beceri yolunu paket köküne bağlar (yalnız markdown)."""
    return BECERI_ON.sub(r"skills/\1", s)

def terim_cevir(s):
    for a, b in TERIM:
        s = s.replace(a, b)
    return s

# ---------- 2) ChatGPT notları ----------
GENEL_NOT = """> **ChatGPT'de çalışma notu** (paket dönüştürücüsü ekledi; aşağıdaki adımlar silinmedi, burada nasıl okunacağı yazıyor)
> 1. **Cevap biçimi:** her mesaj ADHD dostu — ilk satır yapılacak iş, numaralı adımlar, her mesajda durum, liste ≤5, giriş/kapanış nezaketi yok. Tam kurallar: `skills/ekip-bilgi/references/adhd-kurallari.md`.
> 2. **Hafıza:** `.ekip/` klasörü yok. `DURUM.md` / `KARARLAR.md` / `DERSLER.md` okunur/yazılır denen her yerde cevabın sonundaki **DURUM bloğunu** kullan (biçim: `skills/ekip-lideri/SKILL.md`). Kullanıcı eski bir DURUM bloğu yapıştırırsa oradan devam et; bloktaki kararları yeniden sorma.
> 3. **`is/` dosyaları:** kod yorumlayıcı açıksa orada üret ve indirilebilir dosya olarak ver; kapalıysa içeriği sohbete parça parça yaz.
> 4. **Yollar** paket köküne göredir (`skills/...`); ortak bilgi `skills/ekip-bilgi/references/` altında. Kod yorumlayıcının paket dosyalarını görüp görmediği **doğrulanmadı**; göremiyorsa kullanıcıdan gereken betiği ya da dosyayı sohbete yüklemesini iste.
> 5. **Araçlar:** tarayıcı otomasyonu, bilgisayar/telefon kontrolü (iPhone Yansıtma), yerel terminal ve Google Flow otomasyonu burada yok. Bu adımları **kullanıcı yapar** ve sonucu (ekran görüntüsü, sayfa metni, dosya) sohbete yükler. ChatGPT ajan modu web sayfası açabilir ama bu paketle sınanmadı (**doğrulanmadı**). Python betikleri kod yorumlayıcıda koşulabilir; ffmpeg'i kullanmadan önce `ffmpeg -version` ile ölç.
> 6. **Ekip rolleri:** çekirdek ekipte "ajan" ya da "yardımcı rol" denen üye aynı adlı beceridir (`skills/<ad>/SKILL.md`). Ayrı süreç yok: role aynı sohbette sen geçersin, brief'i kendine yazarsın, çıktıyı yine sınarsın. Mağaza kolu üyeleri (marka, görsel, site, denetim) ayrı beceri DEĞİLDİR: işleri `skills/magaza-kurucu/<aşama>/` dosyalarının içindedir; site denetimini o aşama kendisi uygular.
> 7. **Mağaza ve köprü:** Shopify işlemleri ChatGPT'nin Shopify bağlantısıyla, Çalışma (Work) modunda yapılır. Köprü betiği `skills/ekip-bilgi/references/paket.py` kod yorumlayıcıda koşulur; `is/NN-urun/magaza/` dosyaları sohbete eklenir ya da indirilebilir dosya olarak verilir.
"""

OZEL = {
    "ekip-lideri": [
        "Bu paketteki bütün ekip becerileri ve roller aşağıdaki tabloda; ortam kontrolü (`referans/kurulum-kontrol.md`) yerine ChatGPT'de yalnız şunu sor: kod yorumlayıcı ve dosya yükleme açık mı.",
        "**Kullanıcının elle yaptığı adımlar** (ilk oturumda bir kez söyle): (1) Instagram/Reels taraması → ekran görüntüsü, link ya da hesap adı yükler · (2) AliExpress, Trendyol, Amazon, Meta Reklam Kütüphanesi, rakip mağaza → sayfayı açar, metnini ya da ekran görüntüsünü yükler · (3) Google Flow klip üretimi → kendisi üretir (kredi = önce onay), sen promptu dosya olarak verirsin · (4) müzik → kendisi indirir ve yükler · (5) yeni sohbete geçerken son DURUM bloğunu yapıştırır.",
        "**Kod yorumlayıcıda senin yaptıkların:** Python betikleri, ffmpeg kurgusu, Excel/CSV/TSV dosyaları. Tarayıcı JS betikleri (`*.js`) ve macOS/iPhone araçları (`*.swift`, iPhone `.sh` betikleri) burada çalışmaz.",
        "`scripts/yayin_olc.py` (48. saat ölçümü) kod yorumlayıcıda koşulur; içgörü sayılarını kullanıcı girer.",
        "Mağaza işi (`magaza-kurucu`) bu pakette tam çalışır: görsel üretimi bu sohbette, Shopify yazımı ChatGPT'nin Shopify bağlantısıyla (Çalışma modu şart). Mağaza kolu ajanları yoktur; aşama dosyaları aynı işi tek seste yürütür. Oturum modeli notu (Fable) burada geçersizdir.",
        "HyperFrames becerileri (`viral-urun-ekibi:hyperframes` vb.) bu pakette **yok**: hareketli tasarım render'ı yerel Node + Chrome ister. Yönlendirme tablosundaki hareketli tasarım satırı burada `video-kurgu` notundaki yolla yürür.",
    ],
    "kesfet-urun-avi": [
        "Instagram/telefon taramasını **kullanıcı yapar**: Reels ekran görüntüsü, video linki ya da hesap adı yükler; sen okur, ayıklar, tabloya yazarsın.",
        "`kur.sh`, `*.swift`, `izle.sh`, `kaydir.sh`, `dokun.sh`, `begen.sh` yalnız macOS + iPhone Yansıtma içindir — ChatGPT'de çalışmaz.",
        "`baslat.sh` / `ekle.sh` / `kontrol.sh` yerine tabloyu kod yorumlayıcıda tut; `excel_yap.py` kod yorumlayıcıda koşulabilir (openpyxl gerekir; doğrulanmadı).",
    ],
    "aliexpress-firsat": [
        "AliExpress / Trendyol / Amazon / Meta Reklam Kütüphanesi sayfalarını **kullanıcı açar** ve ürün sayfası metnini ya da ekran görüntüsünü yükler (ajan modu sınanmadı). Görmediğin satış sayısını yazma: `doğrulanamadı`.",
        "`firsat_kontrol.py`, `marj_hesap.py`, `ivme_olc.py`, `kirma_testi.py` kod yorumlayıcıda koşulabilir.",
        "`urun-paketi.json` (mağaza kolunun girdisi) `skills/ekip-bilgi/references/paket.py urun-yaz` ile kod yorumlayıcıda yazılır ve indirilebilir dosya olarak verilir; mağaza işi aynı paketteki `magaza-kurucu` becerisiyle bu dosyadan başlar.",
    ],
    "ai-video-kreatif": [
        "Başlangıç karelerini ChatGPT'nin görsel üretimiyle bu sohbette üretebilirsin (kullanılabiliyorsa; her kare yine ölçülerek kontrol edilir).",
        "Google Flow klip üretimini **kullanıcı yapar** (kredi harcar → önce onay, tutar DURUM bloğundaki Kararlar satırına). Promptları dosya olarak ver; `chatgpt_indir.js`, `flow_yukle.js` tarayıcı otomasyonu içindir, burada kullanılmaz.",
        "`magaza-paketi.json` kullanıcı tarafından sohbete eklenir; `skills/ekip-bilgi/references/paket.py magaza-oku <dosya>` kod yorumlayıcıda koşulur, çıkan marka kilidi DURUM bloğunun Kararlar satırına tek satır özetle girer.",
        "TikTok / Meta viral referansı: kullanıcı link ve ekran görüntüsü verir; izlenme sayısı görünmüyorsa `doğrulanamadı`. `senaryo_kontrol.py`, `prompt_uret.py`, `kare_hazirla.py`, `malzeme_kontrol.py` kod yorumlayıcıda koşulabilir.",
    ],
    "video-kurgu": [
        "Kurgu kod yorumlayıcıda ffmpeg ile yapılır; kullanıcı klipleri sohbete yükler. Daha önceki bir ölçümde kod ortamında ffmpeg 7.x vardı, moviepy yoktu (`skills/ekip-bilgi/references/chatgpt/video-kurgu.md`) — yine de `ffmpeg -version` ile ölç.",
        "`video-paketi.json`: `skills/ekip-bilgi/references/paket.py video-yaz <teslim klasörü>` kod yorumlayıcıda; indirilebilir dosya olarak verilir (mağaza koluna geri dönüş: `magaza-kurucu` › `shopify-kurulum`).",
        "Müzik indirme (Pixabay `curl`) burada yok: kullanıcı müziği indirir ve yükler. Sesi dinleyemezsin: kullanıcı videoyu bir kez sesli izler.",
        "**Aşama 8b (HyperFrames hareketli katman) ChatGPT'de çalışmaz** (yerel Node + Chrome + CLI). Burada: yazıyı `hizli_kurgu.py` ile göm ve hareketli katman planını yaz (hangi saniyede hangi öğe: kinetik yazı, geçiş, sayaç, UI kartı). Render, eklentinin yerel kurulumunda (Node + Chrome olan bilgisayar) yapılır; bunu teslim raporunda \"hareketli katman yok\" diye belirt.",
    ],
    "reklam-kutuphanesi-avi": [
        "Meta Reklam Kütüphanesi taramasını **kullanıcı yapar**: sorguyu açar, sonuç sayfasının metnini ya da ekran görüntüsünü yükler. `meta_topla.js`, `meta_aktar.js`, `magaza_oku.js` tarayıcı otomasyonu içindir, burada çalışmaz.",
        "`meta_kayit.py`, `nis_kelime.py`, `magaza_gecis.py`, `haftalik_rapor.py`, `desen_say.py` kod yorumlayıcıda koşulabilir. Günde ≤30 sorgu kuralı kullanıcı için de geçerli.",
    ],
    "teklif-ve-sayfa": [
        "Rakip mağaza sayfalarını **kullanıcı açar** ve metnini/ekran görüntüsünü yükler (ya da web araması). `teklif_kontrol.py` kod yorumlayıcıda koşulabilir.",
    ],
    "firsat-avcisi": [
        "AliExpress sayfalarını kullanıcı açar ve yükler; tarayıcı yoksa yalnız arama terimlerini ve web araması bulgularını yaz, \"AliExpress taranamadı (tarayıcı yok)\" de.",
    ],
    "kanit-savcisi": [
        "Pazar ve mağaza aramalarını kullanıcı açar ya da web araması yapılır; açılmayan kaynak `bulunamadı` / `doğrulanamadı`.",
    ],
    "icerik-stratejisti": [
        "`senaryo_kontrol.py` kod yorumlayıcıda koşulur; çıkış 0 olmadan senaryo teslim edilmez.",
    ],
    "kreatif-analisti": [
        "Kreatif notları kullanıcı yükler; yoksa `skills/ekip-bilgi/references/bilgi/kreatif-notlar.md` kaynak alınır.",
    ],
    "video-elestirmen": [
        "Jüri hükmü ve `kapi.py` çıktısı sohbette yoksa kök neden yazma; önce onları iste.",
    ],
    "video-juri": [
        "**Aynı sohbet kör değildir.** Bu rol YENİ ve boş bir sohbette uygulanır: kullanıcı yalnız bu dosyayı ve `juri.py pano`nun ürettiği pano görsellerini yükler (senaryo, kontrat, hangi ögenin bizim olduğu yüklenmez). 3 kopya = 3 ayrı yeni sohbet; her birinin JSON çıktısı `KOR-<n>.json` olarak kaydedilir ve asıl sohbette `juri.py birlestir` ile birleştirilir.",
    ],
    "ses-tasarimcisi": [
        "`ses_tasarla.py` / `ses_olc.py` kod yorumlayıcıda (ffmpeg gerekir) koşulur; dinleyemediğini `doğrulanamadı` diye yaz.",
    ],
}

ROL_NOTU = """> **Rol becerisi.** Bu üye ayrı bir ajan değildir: ekip lideri ya da ilgili beceri bu role geçtiğinde veya kullanıcı doğrudan istediğinde aynı sohbette uygulanır. "Ana oturuma / lidere bildir" = sohbette kullanıcıya açıkça yaz.
"""

LIDER_BASI = """> **Her mesajda geçerli (eski oturum kancasının işi).**
> - **Cevap biçimi (ADHD dostu, kullanıcı "normal mod" diyene kadar):** ilk satır yapılacak iş · çok adımlı iş numaralı liste · her mesajda durum ("5 adımdan 3'ü bitti, sıradaki: …") · süre somut · biten iş dosya adıyla görünür · liste ≤5 öğe · giriş/özet tekrarı/"umarım yardımcı olur" yok · hata düz tonla: sebep + düzeltme · tek somut sonraki adımla bitir. Tam kurallar: `skills/ekip-bilgi/references/adhd-kurallari.md`.
> - **Bilgi:** ürün/viral/video sorularında önce `skills/ekip-bilgi/references/bilgi/README.md` (hangi soruda hangi dosya), `viral-dna.md`, `marka-skoru.md`.
> - **Hafıza = DURUM bloğu.** Sohbetler birbirini görmez; HER cevabın sonuna şu bloğu koy (≤10 satır):
>
> ```
> DURUM
> - Pazar: <Türkiye / ABD / diğer — ilk sohbette bir kez sorulur>
> - Aktif iş: <iş akışı + ürün>
> - Aşama: <ör. aday puanlandı / 10/30 video yazıldı>
> - Kararlar: <kullanıcının verdiği kararlar ve onaylar (pazar, kredi tavanı, izinler)>
> - Açık sorular: <kullanıcıdan beklenen>
> - Sıradaki adım: <tek somut adım>
> ```
>
> Kullanıcı yeni sohbete bir DURUM bloğu yapıştırırsa oradan devam et; bloktaki kararları yeniden sorma. "Nerede kalmıştık" sorusunu yalnız yapıştırılan bloktan cevapla; hatırladığını sanma.
"""

def not_blogu(skill, rol=False):
    s = GENEL_NOT
    ek = OZEL.get(skill, [])
    if ek:
        s += ">\n> **Bu becerede:**\n" + "".join("> - " + e + "\n" for e in ek)
    if rol:
        s = ROL_NOTU + ">\n" + s
    return s + "\n"

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)

def frontmatter_ayir(s):
    m = FM.match(s)
    if not m:
        raise SystemExit("frontmatter yok")
    alanlar = {}
    for satir in m.group(1).splitlines():
        if ":" in satir and not satir.startswith(" "):
            k, v = satir.split(":", 1)
            alanlar[k.strip()] = v.strip()
    return alanlar, s[m.end():]

# ChatGPT'nin beceri seçimini yanıltacak ortam ifadeleri (açıklamada).
ACIKLAMA_DUZELT = [
    ("Hafızayı (.ekip/) kurar ve okur", "Hafızayı her cevabın sonundaki DURUM bloğuyla tutar"),
    ("Mac'te iPhone Yansıtma ile, Windows'ta ve her yerde Chrome'da instagram.com ile çalışır.",
     "Kullanıcının yüklediği Reels ekran görüntüsü, video linki ya da hesap adıyla çalışır."),
]

def fm_yaz(ad, aciklama):
    for a, b in ACIKLAMA_DUZELT:
        aciklama = aciklama.replace(a, b)
    aciklama = terim_cevir(aciklama)
    return "---\nname: %s\ndescription: %s\n---\n" % (ad, json.dumps(aciklama, ensure_ascii=False))

# ---------- 3) Skill'ler ----------
skills_k = os.path.join(kaynak, "skills")
skills_h = os.path.join(hedef, "skills")
# HyperFrames (Apache-2.0, yerel render) ChatGPT paketine girmez — gerekçe dosya başında.
HARIC = {"hyperframes", "hyperframes-cli", "hyperframes-registry", "media-use"}
# Dönüştürülmeden kopyalanan beceriler (iki yüzey için yazılmış kaynak; içinde ${CLAUDE_...} olmamalı — sondaki kapı ölçer).
HAM = {"magaza-kurucu"}
skill_adlari = sorted(d for d in os.listdir(skills_k) if os.path.isdir(os.path.join(skills_k, d)) and d not in HARIC)

for ad in sorted(HAM & set(skill_adlari)):
    shutil.copytree(os.path.join(skills_k, ad), os.path.join(skills_h, ad),
                    ignore=shutil.ignore_patterns(*ATLA_AD, "*.pyc"))

for ad in skill_adlari:
    if ad in HAM:
        continue
    for kok, dirs, files in os.walk(os.path.join(skills_k, ad)):
        dirs[:] = sorted(d for d in dirs if d not in ATLA_AD)
        for f in sorted(files):
            if f in ATLA_AD:
                continue
            kp = os.path.join(kok, f)
            hp = os.path.join(skills_h, os.path.relpath(kp, skills_k))
            uzanti = os.path.splitext(f)[1]
            if uzanti not in METIN:
                os.makedirs(os.path.dirname(hp), exist_ok=True)
                shutil.copy2(kp, hp)
                continue
            s = terim_cevir(yol_cevir(oku(kp), ad))
            if f == "SKILL.md" and kok == os.path.join(skills_k, ad):
                alan, govde = frontmatter_ayir(s)
                if ad == "ekip-lideri":
                    govde = govde.replace("| Unvan | Rol | Ajan |", "| Unvan | Rol | Beceri (rol) |")
                    govde = govde.replace("çağrıda ajan adını kullan.", "role geçerken beceri adını kullan (`skills/<ad>/SKILL.md`).")
                    govde = "\n".join(l for l in govde.split("\n") if "ChatGPT'de yapmak istiyor" not in l and "THIRD_PARTY_NOTICES" not in l)
                    ust = LIDER_BASI + "\n" + not_blogu(ad)
                else:
                    ust = not_blogu(ad)
                # Not, ilk başlıktan hemen sonra girer.
                parca = govde.split("\n", 2)
                if parca[0] == "" and parca[1].startswith("# "):
                    govde = "\n" + parca[1] + "\n\n" + ust + parca[2].lstrip("\n")
                else:
                    govde = "\n" + ust + govde
                s = fm_yaz(alan["name"], alan["description"]) + govde
            yaz(hp, s)
            shutil.copymode(kp, hp)

# ---------- 4) Ajanlar -> rol skill'leri ----------
ajan_k = os.path.join(kaynak, "agents")
AJAN_BECERI = {"ses-tasarimcisi": "video-kurgu"}
MAGAZA_ISARET = "<!-- kol: magaza -->"
tum_ajan = sorted(f[:-3] for f in os.listdir(ajan_k) if f.endswith(".md"))
magaza_ajan = [a for a in tum_ajan if MAGAZA_ISARET in oku(os.path.join(ajan_k, a + ".md"))]
ajanlar = [a for a in tum_ajan if a not in magaza_ajan]
for ad in ajanlar:
    if ad in skill_adlari:
        raise SystemExit("ad çakışması: " + ad)
    # Ajan dosyasında ${CLAUDE_SKILL_DIR} onu çağıran becerinin klasörüdür.
    s = terim_cevir(yol_cevir(oku(os.path.join(ajan_k, ad + ".md")), AJAN_BECERI.get(ad)))
    alan, govde = frontmatter_ayir(s)
    parca = govde.split("\n", 2)
    ust = not_blogu(ad, rol=True)
    if parca[0] == "" and parca[1].startswith("# "):
        govde = "\n" + parca[1] + "\n\n" + ust + parca[2].lstrip("\n")
    else:
        govde = "\n" + ust + govde
    yaz(os.path.join(skills_h, ad, "SKILL.md"), fm_yaz(alan["name"], alan["description"]) + govde)

# ---------- 5) Ortak bilgi -> ekip-bilgi skill'i ----------
bilgi_h = os.path.join(skills_h, "ekip-bilgi")
for kok, dirs, files in os.walk(os.path.join(kaynak, "ortak")):
    dirs[:] = sorted(d for d in dirs if d not in ATLA_AD)
    for f in sorted(files):
        if f in ATLA_AD:
            continue
        kp = os.path.join(kok, f)
        hp = os.path.join(bilgi_h, "references", os.path.relpath(kp, os.path.join(kaynak, "ortak")))
        if "sozlesme" in os.path.relpath(kok, os.path.join(kaynak, "ortak")).replace(os.sep, "/").split("/") \
                or f.endswith((".py", ".tsv", ".json")):
            # Sözleşme kaynağıyla bayt bayt aynı kalır (OZET.json); betik/veri dosyasına terim dönüşümü yapılmaz.
            os.makedirs(os.path.dirname(hp), exist_ok=True)
            with open(kp, "rb") as g, open(hp, "wb") as h:
                h.write(g.read().replace(b"\r\n", b"\n"))
            continue
        yaz(hp, terim_cevir(yol_cevir(oku(kp), None)))
cg = os.path.join(kaynak, "ekler", "chatgpt")
if os.path.isdir(cg):
    for f in sorted(os.listdir(cg)):
        if f.endswith(".md"):
            yaz(os.path.join(bilgi_h, "references", "chatgpt", f), terim_cevir(yol_cevir(oku(os.path.join(cg, f)), None)))


tum_beceri = skill_adlari + ajanlar
yaz(os.path.join(bilgi_h, "SKILL.md"), fm_yaz(
    "ekip-bilgi",
    "Viral Ürün Ekibi'nin ortak bilgi bankası: viral ürün DNA'sı (kapılar, 7 ölçüt, M1–M14 mekanizmaları), marka skoru, "
    "sözlük, ADHD dostu cevap kuralları, 600+ ürünlük Instagram kataloğu, 116 viral video kreatif notu, 80 değerlendirilmiş "
    "AliExpress adayı ve ölçülmüş dersler. \"Şu ürün viral olur mu\", \"buna benzer ne var\", \"bu kategoride hangi kanca tuttu\", "
    "\"bu ürünü daha önce inceledik mi\", \"bu hesap marka mı\" sorularında ve diğer ekip becerileri skills/ekip-bilgi/references/ "
    "altındaki bir dosyaya atıf yaptığında kullan.") + """
# Ekip bilgi bankası

Diğer ekip becerilerinin ortak kaynağı. Cevap vermeden önce ilgili dosyada ara (ürün adı, kategori, kanca kelimesi);
sayıyı ve linki dosyada nasılsa öyle aktar, dosyada yoksa "kayıtta yok" de. Genel bilgiyle doldurduğun yeri "tahmin" diye işaretle.

## Hangi soruda hangi dosya
Tam tablo: `references/bilgi/README.md`. Kısa yol:

| Soru | Dosya |
|---|---|
| Viral olur mu? Kapılar, 7 ölçüt, mekanizmalar | `references/viral-dna.md` |
| Hesap örnek alınacak marka mı? | `references/marka-skoru.md` |
| Benzer ürün, kategori, izlenme | `references/bilgi/urun-katalogu.md` |
| Hangi kanca/sahne tuttu | `references/bilgi/kreatif-notlar.md` |
| Daha önce incelendi mi, neden elendi | `references/bilgi/firsat-gecmisi.md`, `references/bilgi/dersler.md` |
| 30 video planı örnekleri | `references/bilgi/uretim-deneyimi.md` |
| Terimler | `references/sozluk.md` |
| Cevap biçimi | `references/adhd-kurallari.md` |
| ChatGPT'de tek parça iş akışı metinleri | `references/chatgpt/` |
| Kollar arası dosya alışverişi (`urun-paketi.json`, `magaza-paketi.json`, `video-paketi.json`) | `references/sozlesme/arayuz-sozlesmesi.md`, betik `references/paket.py` |

## Okuma kuralları
- Kod numaraları kanıt izidir: `S063` ürün = `kreatif-notlar.md` içinde **063** notu.
- Sayılar gözlem anındaki değerlerdir; karar öncesi yeniden açılır.
- Bu dosyalarda kullanıcı verisi yoktur; kullanıcının kendi işi DURUM bloğunda ve ürettiğin dosyalarda tutulur.
""")

# ---------- 6) Manifestler + README + LICENSE ----------
kaynak_mf = json.load(open(os.path.join(kaynak, ".claude-plugin", "plugin.json"), encoding="utf-8"))
aciklama = ("Türkçe e-ticaret ekibi, tek lider: viral ürün analizi, AliExpress'te henüz viral olmamış ürün avı ve kanıt "
            "dosyası, Meta Reklam Kütüphanesi taraması, teklif, Shopify mağaza kurulumu (marka, görsel, metin, site denetimi), "
            "AI video senaryosu ve başlangıç karesi promptları, ffmpeg ile kurgu. %d beceri; tarayıcı ve telefon adımlarını "
            "kullanıcı yapar." % (len(tum_beceri) + 1))
kok_mf = {
    "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "name": kaynak_mf["name"],
    "version": kaynak_mf["version"],
    "description": aciklama,
    "author": kaynak_mf.get("author", {"name": "Viral Ürün Ekibi"}),
    "license": kaynak_mf.get("license", "MIT"),
    "keywords": kaynak_mf.get("keywords", []),
    "extensions": {"com.openai": {"interface": {
        "displayName": kaynak_mf.get("displayName", "Viral Ürün Ekibi"),
        "shortDescription": "Ürün bul, mağaza kur, video üret",
        "longDescription": ("Tek liderli Türkçe e-ticaret ekibi. Ürünü bulur ve kanıtla doğrular, teklifi kurar, Shopify mağazasını "
                            "açar (marka adı, logo, galeri görselleri, site metni, kurulum ve site denetimi), AI video senaryosunu ve "
                            "karelerini hazırlar, kurguyu yapar. Her adımda kararı ekip verir, gerekçesini tek satırda söyler; sen "
                            "onaylarsın. Mağaza ve görsel adımları için Çalışma modu ve Shopify bağlantısı gerekir."),
        "developerName": kaynak_mf.get("author", {}).get("name", "Viral Ürün Ekibi"),
        "category": "Productivity",
        "capabilities": ["Interactive", "Write"],
        "defaultPrompt": ["Ekibi başlat", "Bu ürün için mağaza kur. Ülke: Türkiye", "Bu ürüne video yap"],
    }}},
}
claude_mf = {k: v for k, v in kok_mf.items() if k not in ("$schema", "extensions")}
if "displayName" in kaynak_mf:
    claude_mf["displayName"] = kaynak_mf["displayName"]
yaz(os.path.join(hedef, "plugin.json"), json.dumps(kok_mf, ensure_ascii=False, indent=2) + "\n")
yaz(os.path.join(hedef, ".claude-plugin", "plugin.json"), json.dumps(claude_mf, ensure_ascii=False, indent=2) + "\n")
shutil.copy2(lisans, os.path.join(hedef, "LICENSE"))

satirlar = []
for ad in tum_beceri + ["ekip-bilgi"]:
    satirlar.append("| `%s` | %s |" % (ad, "rol" if ad in ajanlar else ("bilgi" if ad == "ekip-bilgi" else "iş akışı")))
yaz(os.path.join(hedef, "README.md"), """# Viral Ürün Ekibi — ChatGPT paketi

Bu klasör `scripts/chatgpt_paketi_yap.sh` ile üretildi; elle düzenleme (bir sonraki üretimde silinir).
Başlangıç: sohbette "ekibi başlat" yaz → `ekip-lideri` becerisi devreye girer. Hafıza her cevabın sonundaki DURUM bloğudur.

| Beceri | Tür |
|---|---|
""" + "\n".join(satirlar) + "\n")
# Kapı: markdown'da çözülmemiş Claude değişkeni kalmamalı.
kalan = []
for kok, _, files in os.walk(hedef):
    for f in files:
        if f.endswith(".md") and "${CLAUDE_" in oku(os.path.join(kok, f)):
            kalan.append(os.path.relpath(os.path.join(kok, f), hedef))
if kalan:
    raise SystemExit("HATA: çözülmemiş ${CLAUDE_...}: " + ", ".join(kalan))
# Kapı: ham kopyalanan becerinin dosyaları kaynakla bayt bayt aynı; mağaza kolu ajanı beceriye dönüşmemiş.
for ad in HAM & set(skill_adlari):
    for kok, _, files in os.walk(os.path.join(skills_k, ad)):
        for f in files:
            if f in ATLA_AD or f.endswith(".pyc") or "__pycache__" in kok:
                continue
            kp = os.path.join(kok, f)
            hp = os.path.join(skills_h, os.path.relpath(kp, skills_k))
            if not os.path.exists(hp) or open(kp, "rb").read() != open(hp, "rb").read():
                raise SystemExit("HATA: ham kopya farklı: " + os.path.relpath(kp, skills_k))
sizan = [a for a in magaza_ajan if os.path.isdir(os.path.join(skills_h, a))]
if sizan:
    raise SystemExit("HATA: mağaza kolu ajanı beceriye dönüşmüş: " + ", ".join(sizan))
for zorunlu in ("paket.py", "nis-esleme.tsv", "sozlesme/paket_dogrula.py", "sozlesme/OZET.json"):
    if not os.path.exists(os.path.join(bilgi_h, "references", *zorunlu.split("/"))):
        raise SystemExit("HATA: köprü dosyası pakette yok: skills/ekip-bilgi/references/" + zorunlu)
print("beceri: %d (%d iş akışı + %d rol + ekip-bilgi) · mağaza kolu ajanı pakete girmedi: %d · köprü: skills/ekip-bilgi/references/paket.py + sozlesme/"
      % (len(tum_beceri) + 1, len(skill_adlari), len(ajanlar), len(magaza_ajan)))
PY

# Tekrar üretilebilir ZIP: sabit zaman damgası, sıralı dosya listesi, ek alan yok.
find "$HEDEF" -exec touch -h -t 202601010000 {} +
( cd "$DIST/chatgpt" && find viral-urun-ekibi -type f | LC_ALL=C sort | zip -q -X -@ "$ZIP" )
ADET=$(find "$HEDEF" -type f | wc -l | tr -d ' ')
BOYUT=$(wc -c < "$ZIP" | tr -d ' ')
echo "klasör: $HEDEF ($ADET dosya)"
echo "zip: $ZIP ($BOYUT bayt)"
# Kapı: boyut tavanı (resmî sınır bulunamadı; güvenli tavan 2,5 MB — fontlar ve stil çapası ~1 MB).
[ "$BOYUT" -le 2621440 ] || { echo "HATA: zip $BOYUT bayt > 2621440"; exit 1; }
