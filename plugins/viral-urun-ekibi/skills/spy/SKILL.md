---
name: spy
description: Spy (Reklam kütüphanesi taraması). Scans the Meta Ad Library for ads and stores that are scaling. Meta Reklam Kütüphanesi'nde niş × pazar (ABD, TR, UK, DE/FR/ES) sistematik tarama — günde ≤30 sorgu, önce kontrol sorgusu; aktif gün, kopya sayısı, mağaza başına reklam ve Shopify mağaza yaşıyla ölçeklenen ürün/kreatifi betikle etiketler, AliExpress eşleme listesi ve haftalık niş raporu çıkarır. "Meta Reklam Kütüphanesi'nden niş tara", "bu nişte trend ürün ne", "rakip reklamları topla", "kazanan reklam bul", "ad library taraması", "hangi mağaza ölçekleniyor", "Shopify reklam toplayıcı", "pazar başına çok reklam topla", "derin analiz kuyruğu" isteklerinde çağır.
---

# Reklam kütüphanesi avı

**Amaç:** birinin para koyduğu kreatifleri (Meta reklamları) niş niş, tekrarlanabilir biçimde toplamak; ölçeklenen genç mağazayı ve
ürününü bulup `hunter` akışına, kazanan kreatifi kreatif kayda vermek.
**Bitiş durumu:** günün sorguları `is/meta/aramalar.tsv`'de (kontrol sonucu dahil); `reklamlar.tsv` / `sayfalar.tsv` / `magazalar.tsv`
güncel ve `kayit_denetle.py` temiz; haftalık turda `nis-raporu-<tarih>.md`; en çok 3 kreatif notu; `.ekip/DURUM.md` "Sıradaki adım".

Önce oku: `${CLAUDE_SKILL_DIR}/referans/erisim.md` (tarayıcı ve sınırlar), `${CLAUDE_SKILL_DIR}/referans/kayit-semasi.md` (dosyalar,
sinyaller, etiketler), `${CLAUDE_SKILL_DIR}/referans/nisler.md` (12 niş × 6 ülke kelime aileleri). Terimler `${CLAUDE_PLUGIN_ROOT}/ortak/sozluk.md`.

Python: macOS/Linux `python3`, Windows `py -3`. Betikler yalnız standart kütüphane. `S="${CLAUDE_SKILL_DIR}/scripts"` kısaltması aşağıda.

## Pazarlıksız kurallar
- **Yalnız bak / oku / kaydır.** Beğeni, takip, yorum, mesaj, kaydetme, reklama tıklayıp satın alma yok. Meta Reklam Kütüphanesi **girişsiz**.
- **Günde ≤30 sorgu, aralar ≥15 sn, oturum ≤1 saat**, kaydırma 4–7 sn. Kotayı `nis_kelime.py kaydet` tutar; kayıtsız sorgu kayda girmez.
- **Önce dolu kontrol sorgusu.** 0 kart = Meta sessizce kısıtlıyor → o gün Meta'ya dokunma, sonuç "doğrulanamadı". Her 0 kartlık sorgudan sonra kontrol tekrar.
- Instagram/TikTok yalnız kullanıcının **ayrı Chrome profilindeki kendi hesabıyla**, yalnız bak/kaydır (ayrıntı `erisim.md` §5).
- **Tarama yalnız lider oturumunda** (Chrome). Alt ajana tarayıcı işi verilmez; alt ajan yalnız TSV'lerden sentez/çürütme yapar.
- Sayı uydurma yok; okunamayan alan `görünmüyor`. Etiket (`OLCEKLENIYOR` / `TEST` / `ESKI-KAZANAN`) yalnız betikten; eşikler **DENEME**.
- Kozmetik/sağlık **ELE KAPISI**: taranır ama ürün önerilmez, eşlenmez. Gizli pencere, IP değiştirme, CAPTCHA atlatma yok.
- Uzun tablo sohbete yazılmaz; sohbete özet + dosya yolu.

## Hafıza protokolü
| Ne zaman | Ne yapılır |
|---|---|
| Başlarken | `.ekip/DURUM.md`, `.ekip/KARARLAR.md` okunur. `is/meta/` yoksa açılır (betikler dosyaları ilk yazışta kurar). |
| Pazar / niş | KARARLAR'da `\| pazar \|` / `\| meta-nis \|` satırı varsa o; yoksa varsayılan ABD + TR (+ UK), niş sırası nisler.md sırası. Kullanıcı seçerse hemen KARARLAR'a. |
| Her aşama sonunda | `.ekip/DURUM.md` üzerine yazılır (aktif iş, aşama, son çıktı, sıradaki adım, bekleyen onay). |
| Kısıt / hata tekrarı | `.ekip/DERSLER.md`'ye "- konu: ders (kanıt dosyası)". |

## Akış
| # | Ne | Komut / dosya |
|---|---|---|
| 1 | Hafıza oku, pazar + niş seç (günlük: 2 niş × 1 pazar; deneme turu: 1 niş × 3 pazar) | `nisler.md` |
| 2 | Tarayıcı seç (doğru bilgisayardaki Chrome), kontrol sorgusunu aç | `erisim.md` §2 |
| 3 | Günün planı → kontrolü kaydet ve sonucu yaz | `python3 "$S/nis_kelime.py" gun --kok is/meta --ulke US,TR,GB --nis evcil` · `kaydet --aile KONTROL ...` · `sonuc --kart N` (0 → çıkış 3, DUR) |
| 4 | Her sorgu: `kaydet` → URL'yi aç → `meta_topla.js` → bitince 2. sekmede `meta_aktar.js` → `get_page_text` → `is/meta/ham/` | `scripts/meta_topla.js`, `scripts/meta_aktar.js` |
| 5 | Kaydet, tekilleştir, aktif gün, birim toplamı, etiket | `python3 "$S/meta_kayit.py" kaydet --kok is/meta is/meta/ham/<dosya>-*.txt` |
| 6 | Ölçek: OLCEKLENIYOR adayların alan sorgusu ("~N sonuç") | `nis_kelime.py kaydet --aile ALAN --sorgu <alan>` → `meta_kayit.py alan --ulke .. --alan .. --sonuc N` |
| 7 | Mağaza: liste → Shopify sekmesinde `magaza_oku.js` → `meta_aktar.js` (KAYNAK='magaza') → aktar | `magaza_gecis.py liste` / `aktar` · teklif satırı elle `teklif.tsv` |
| 8 | AliExpress eşleme listesi (yalnız OLCEKLENIYOR + genç Shopify; ELE nişi hariç) → `hunter` akışı, kaynak `META-<kod>` | `magaza_gecis.py esleme` → `is/meta/aliexpress-esleme.md` |
| 9 | Niş başına en çok 3 OLCEKLENIYOR kreatifi Ad Library oynatıcısında izle (2 sn'de bir kare) → kreatif not + `kayit.csv` satırı (aynı sorgudan ≥1 TEST kreatif de) ; `reklamlar.tsv`'de `izlendi=E`, `not_no` | mevcut kreatif not şablonu (`radar`) |
| 10 | Haftalık (Pazar): Cuma ivme tekrarı (`gun --ivme`), sonra rapor + desen | `haftalik_rapor.py --kok is/meta` · `desen_say.py is/kesfet/kreatif/kayit.csv --cikti is/meta/desen-<tarih>.md` |
| 11 | Kapanış: `meta_kayit.py denetle --kok is/meta` temiz → DURUM.md | çıkış 0 olmadan "bitti" denmez |

Çıkış kodları: 0 tamam · 1 yanlış veri / kapı reddi (mesajı oku, düzelt) · 2 0 kart: kontrolü tekrarla · 3 **SINIRLAMA — bugün dur**.

## Ölçeklenen ürün ne olur
`OLCEKLENIYOR` = vekil sinyal, satış kanıtı değil. Eşleme listesindeki ürün `hunter` kapılarından (zaten-viral kontrolü,
kanıt savcısı) geçmeden SAT olmaz. Bant: hedef pazarda 1–10 reklamveren + artış = **erken dalga** (hedef); çok satıcı ve maliyete yakın
fiyat = **doymuş** (ELE). Kazanan reklam gövdesinde ≥3 reklamda geçen ifade raporda "yeni kelime adayı" çıkar → değerlendirip `nisler.md`'ye.

## Shopify reklam toplayıcı (çok pazar: US · TR · GB · DE · FR · ES · IT · NL)
Amaç: pazar başına zamanla binlerce reklamı tek depoda (`is/meta/reklam.db`) biriktirip **yalnız Shopify** mağazalarını
puanlamak; en iyi N (öneri 300) sayfa **derin analiz kuyruğu**na girer. Ayrıntı: `erisim.md` §6, şema `kayit-semasi.md` (son bölüm).
`DB=is/meta/reklam.db`.

| # | Ne | Komut |
|---|---|---|
| 1 | Kuyruk (bir kez; tekrar güvenli) | `python3 "$S/kuyruk.py" uret --db $DB --pazar US,DE,TR --yol ikisi` |
| 2a | MCP yolu (lider çağırır): `al` → çıktıdaki `parametre` ile `ads_library_search` → yanıtı OLDUĞU GİBİ `is/meta/<kaydet>` dosyasına yaz → işle | `kuyruk.py al --db $DB --yol mcp` · `toplanan_isle.py mcp --db $DB --id N <dosya>` |
| 2b | Chrome yolu: `al --yol chrome --kok is/meta` (kota bekçisi `nis_kelime.py`) → §3 toplama → ham döküm → işle | `toplanan_isle.py chrome --db $DB --id N is/meta/ham/<dosya>-*.txt` |
| 3 | Alan adı: MCP alan adı **vermez** → `bekleyen` listesindeki snapshot'ları Chrome'da aç, hedef linki oku | `shopify_kontrol.py bekleyen` · `alan-ekle --page-id .. --alan ..` |
| 4 | Shopify mı + mağaza yaşı (alan başına TEK istek, önbellek) | `shopify_kontrol.py kontrol --db $DB` |
| 5 | Puan + derin analiz kuyruğu | `basari_puani.py hesapla --db $DB --en-iyi 300 --cikti is/meta` → `derin-analiz-<pazar>.tsv` |
| 6 | (isteğe bağlı) Proje analiz veritabanına aktar | `analiz_db_aktar.py --db $DB --analiz-modul <proje>/veri/db.py --analiz-db <proje>/veri/analiz.db` |

**Hız ve etik (pazarlıksız):**
- MCP: **günde ≤150 çağrı, aralar ≥20 sn, niş başına 1 sorgu** (sayım + ≤50 örnek). Aracın kendi açıklaması toplu kazımayı
  yasaklar → bu yol hedefli niş araştırmasıdır, 25 bin hedefinin ana motoru değildir. Chrome: **≤30 sorgu/gün** (§3, değişmedi).
  Snapshot okuma ≤60/gün. Tavan/bekleme betikte yalnız DÜŞÜRÜLEBİLİR; yükseltmek kurucu kararıdır.
- **Engelde dur:** yanıtta hata/sınır izi, ekranda doğrulama/CAPTCHA/"şüpheli etkinlik" → `toplanan_isle.py` çıkış 3 verir ya da
  lider `kuyruk.py engel --id N --sebep ".."` yazar → o gün o yol **kilitli**; ertesi gün kaldığı yerden. Tekrar deneme, IP/profil
  değiştirme, kullanıcı ajanı taklidi, CAPTCHA çözme **yok**.
- Shopify kontrolü dürüst kimlikle (`viral-urun-ekibi-shopify-kontrol/1.0`), alanlar arası ≥10 sn, 429 → 24 sa erteleme,
  bir koşuda 3× 429 → koşu durur. 401/403 alan bir daha denenmez.
- Shopify olmayan kayıt silinmez (`shopify=0`), yalnız kuyruğa girmez. Puan vekildir, satış kanıtı değildir; derin analizden
  sonra ürün yine `hunter` kapılarından geçer.
- Anonimlik: depoya gerçek marka/sayfa adı yazılmaz; örnek veri `tests/` altında uydurma adlarla.

Çıkış kodları (toplayıcı): 0 tamam · 1 yanlış veri · 3 KİLİT/ENGEL — bugün bu yol durur · 4 günlük tavan doldu · 5 çok hızlı
(`bekle_sn` kadar bekle) · 6 kuyruk boş.

Tur sonunda: `python3 "${CLAUDE_SKILL_DIR}/scripts/excel_hazirla.py"` → `is/meta/reklam-urunler.xlsx`; çıktıda `TAMAM` görmelisin.

## Kendini sınama
`python3 "$S/kendini_test.py" [--gercek-ozet <eski-ozet.tsv>]` — 7 kırma testi; her kapı önce bozuk girdiyle ≠0 görülür, sonra geçer.
Betik değiştiyse bu test çıkış 0 vermeden kullanılmaz.
Toplayıcı: `python3 "$S/toplayici_test.py"` — 9 test (kuyruk, tavan, bozuk JSON, engel kilidi, tekilleştirme, Shopify tek istek/
429, puan kapısı, adaptör, pilot uçtan uca). Adaptörü de sınamak için `REKLAMAVI_ANALIZ_MODUL=<proje>/veri/db.py`. Tarayıcı tarafı (`*.js`) bu testle **sınanmaz**: her yeni Meta arayüzünde
ilk 5 kart ekranla elle karşılaştırılır (`erisim.md` §3).
