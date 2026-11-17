---
name: reklam-kutuphanesi-avi
description: Meta Reklam Kütüphanesi'nde niş × pazar (ABD, TR, UK, DE/FR/ES) sistematik tarama — günde ≤30 sorgu, önce kontrol sorgusu; aktif gün, kopya sayısı, mağaza başına reklam ve Shopify mağaza yaşıyla ölçeklenen ürün/kreatifi betikle etiketler, AliExpress eşleme listesi ve haftalık niş raporu çıkarır. "Meta Reklam Kütüphanesi'nden niş tara", "bu nişte trend ürün ne", "rakip reklamları topla", "kazanan reklam bul", "ad library taraması", "hangi mağaza ölçekleniyor" isteklerinde çağır.
---

# Reklam kütüphanesi avı

**Amaç:** birinin para koyduğu kreatifleri (Meta reklamları) niş niş, tekrarlanabilir biçimde toplamak; ölçeklenen genç mağazayı ve
ürününü bulup `aliexpress-firsat` akışına, kazanan kreatifi kreatif kayda vermek.
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
| 8 | AliExpress eşleme listesi (yalnız OLCEKLENIYOR + genç Shopify; ELE nişi hariç) → `aliexpress-firsat` akışı, kaynak `META-<kod>` | `magaza_gecis.py esleme` → `is/meta/aliexpress-esleme.md` |
| 9 | Niş başına en çok 3 OLCEKLENIYOR kreatifi Ad Library oynatıcısında izle (2 sn'de bir kare) → kreatif not + `kayit.csv` satırı (aynı sorgudan ≥1 TEST kreatif de) ; `reklamlar.tsv`'de `izlendi=E`, `not_no` | mevcut kreatif not şablonu (`kesfet-urun-avi`) |
| 10 | Haftalık (Pazar): Cuma ivme tekrarı (`gun --ivme`), sonra rapor + desen | `haftalik_rapor.py --kok is/meta` · `desen_say.py is/kesfet/kreatif/kayit.csv --cikti is/meta/desen-<tarih>.md` |
| 11 | Kapanış: `meta_kayit.py denetle --kok is/meta` temiz → DURUM.md | çıkış 0 olmadan "bitti" denmez |

Çıkış kodları: 0 tamam · 1 yanlış veri / kapı reddi (mesajı oku, düzelt) · 2 0 kart: kontrolü tekrarla · 3 **SINIRLAMA — bugün dur**.

## Ölçeklenen ürün ne olur
`OLCEKLENIYOR` = vekil sinyal, satış kanıtı değil. Eşleme listesindeki ürün `aliexpress-firsat` kapılarından (zaten-viral kontrolü,
kanıt savcısı) geçmeden SAT olmaz. Bant: hedef pazarda 1–10 reklamveren + artış = **erken dalga** (hedef); çok satıcı ve maliyete yakın
fiyat = **doymuş** (ELE). Kazanan reklam gövdesinde ≥3 reklamda geçen ifade raporda "yeni kelime adayı" çıkar → değerlendirip `nisler.md`'ye.

## Kendini sınama
`python3 "$S/kendini_test.py" [--gercek-ozet <eski-ozet.tsv>]` — 7 kırma testi; her kapı önce bozuk girdiyle ≠0 görülür, sonra geçer.
Betik değiştiyse bu test çıkış 0 vermeden kullanılmaz. Tarayıcı tarafı (`*.js`) bu testle **sınanmaz**: her yeni Meta arayüzünde
ilk 5 kart ekranla elle karşılaştırılır (`erisim.md` §3).
