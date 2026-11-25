
# Hunter · kaynak: Trendyol (akış)

Ne zaman okunur: `hunter` SKILL.md "Kaynak seçimi" Trendyol dediğinde. Yalnız-SAT kuralı, hafıza protokolü, brief kuralları ve özet biçimi hunter SKILL.md ile ortaktır; burada yalnız Trendyol'a özgü adımlar var.

**Yalnız SAT (eklenti kuralı):** kullanıcıya (sohbet özeti, Excel ana sayfası, rapor) YALNIZ SAT ürünleri gider; İZLE ve "SAT (koşullu)" yoktur. ELE yalnız kanıtlı engeldir (veto · kanıtlı negatif katkı · kanıtlı doygunluk · eşiğin altında talep); okunamayan/ölçülemeyen ölçüt (viral, marka ROAS, tedarikçi, satıcı sayısı …) engel değil, SAT kartında "ilk testte kontrol et" notudur. Elenenler ve denetim kaydı `adaylar.tsv` / `elenenler.tsv` ve Excel'in gizli "Ayrıntı" sayfasında kalır, kullanıcıya listelenmez.

**Amaç:** Türkiye'de Trendyol'da ilgi gören, Instagram/TikTok'ta henüz viral olmamış, ucuza alınabilen ürünü bulmak; **senin Shopify mağazanda** (kendi markanla) alışın 2–3 katına satmak.
**Bitiş durumu:** `is/firsat/trendyol/adaylar.tsv` denetimden geçti; kısa listedeki her ürünün `is/firsat/kanit/` altında kanıt dosyası var;
`urunler.xlsx` üretildi (çıktıda `TAMAM`; ana sayfada yalnız SAT); kullanıcıya ≤ 10 satır SAT özeti verildi; `.ekip/DURUM.md` güncel.

Önce oku: `${CLAUDE_PLUGIN_ROOT}/ortak/viral-dna.md` ve `${CLAUDE_PLUGIN_ROOT}/ortak/sozluk.md` (SAT / ELE ve "zaten viral" yalnız sözlükteki anlamıyla).
Eşikler ve her ölçütün durumu (`deneme` / `varsayim` / `varsayilan` / `profil`): `${CLAUDE_SKILL_DIR}/trendyol/referans/esikler.tsv`. Ölçüt tablosu: `${CLAUDE_SKILL_DIR}/trendyol/referans/olcutler.md`.
**Tarif:** `${CLAUDE_PLUGIN_ROOT}/ortak/tarifler/06-trendyol-ve-aliexpress-avi.md`. **Oranlar:** `${CLAUDE_SKILL_DIR}/trendyol/referans/tr-oranlari.tsv` kaynaklı varsayılanlarla dolu (durum `kaynakli` / `varsayim` / `varsayilan`, tarih, URL). Kaynak sırası: kullanıcının kendi oranı (marj.csv hücresi) > işletme profili (`.ekip/isletme-profili.tsv`) > eklenti varsayılanı (`kaynakli` / `varsayim` / `varsayilan`); kapıda ödeme profil yoksa 0 sayılır (eklenti varsayılanı, senin kararın değil). Tarih eskiyse ya da kullanıcı kargo/sanal POS anlaşması yaptıysa oran turu yinelenir; bulunamayan oran uydurulmaz. Karar: `denetle` her satıra `SAT-ADAYI` ya da `ELE` yazar; kanıt dosyası gelince SAT olur. Çıktı hedefi: **N SAT bulana kadar** (varsayılan N=5, kullanıcı değiştirebilir; ürün/niş yığılması yok); görünüşü ucuz/estetiği zayıf ürün (telefon standı tipi) ELE.

## Akış (9 adım)
0. **İşletme profili:** `.ekip/isletme-profili.tsv` varsa betikler (`trendyol_kontrol.py`, `tr_marj.py`) onu okur; yoksa eklenti varsayılanı kullanılır ve çıktıda `PROFIL: yok` yazar. Profil `captain` ilk oturumda sorulur (tek seferlik); sen sorma, yalnız `PROFIL: yok` satırını raporda göster.
1. **Hafıza:** `.ekip/DURUM.md`, `.ekip/KARARLAR.md` oku. Pazar TR sabittir, sorulmaz. `is/firsat/trendyol/` yoksa `${CLAUDE_SKILL_DIR}/trendyol/sablon/adaylar.tsv` ile kur.
2. **Kota:** `python3 "${CLAUDE_SKILL_DIR}/trendyol/scripts/trendyol_kontrol.py" kota durum`. Çıkış 4 (günlük tavan) ya da 3 (kilit) ise dur, kullanıcıya söyle.
3. **Tohum:** ilk turda **en az 5 farklı niş**, niş başına **≤ 5 aday** (tek nişe yığılma yok); estetiği zayıf/jenerik ürün (telefon standı tipi) ELE. Arama terimleri (Türkçe, 2–4 kelime) iki kaynaktan: `ortak/viral-dna.md` mekanizmaları (ürün adı değil mekanizma) ve analiz veritabanında
   viral aileler (`v_viral_urun`) → aynı ailenin **farklı modeli**. Terimler `aramalar.tsv`'ye yazılır; aynı terim iki kez aranmaz.
4. **Tarama:** ağır iş `scout` ajanında. Chrome'da `https://www.trendyol.com/sr?q=<terim>` (sıralama: çok değerlendirilenler). Her arama ve her ürün sayfasından
   ÖNCE `trendyol_kontrol.py kota kaydet <arama|urun> <hedef>` (çıkış 0 olmadan istek yok). Ürün sayfasından okunur: ad, link, Trendyol fiyatı (= `rakip_tl`/hedef satış, ASLA `alis_tl`), değerlendirme sayısı,
   puan, diğer satıcı sayısı, satıcı adı, görsel. Alış fiyatı (`alis_tl`) tedarikçiden (AliExpress/1688 aynı ürün) okunur, kaynağı `alis_kaynak`ta; bulunamazsa boş ve not. Satır `adaylar.tsv`'ye; yeni ürün öncesi `trendyol_kontrol.py tekrar <link>`.
   Okuma ayrıntısı: `${CLAUDE_SKILL_DIR}/trendyol/referans/trendyol-okuma.md`.
5. **Ön eleme:** `trendyol_kontrol.py denetle adaylar.tsv [--elenenlere-yaz] [--marj-sonuc marj-sonuc.tsv]` şemayı ve eşikleri uygular, her satıra `on_karar` (SAT-ADAYI / ELE) yazar; `neden` sütununa "Kontrol et: …" (SAT) ya da "ELE sebebi: …" notunu yazar. Trendyol fiyatı `alis_tl`'ye yazılmışsa HATA verir. Çıkış 0 olmadan kısa liste yok.
6. **Viral kontrolü:** (a) `trendyol_kontrol.py viral adaylar.tsv` (eklentiyle gelen sansürlü tablo `ortak/bilgi/viral-urunler.tsv`; kendi `analiz.db`'n varsa `--db <yol>` ile o kullanılır) (yok / aile-var / ayni-urun-viral / dogrulanamadi; tablo da yoksa hepsi
   dogrulanamadi); (b) Instagram ve TikTok'ta Türkçe ürün adıyla arama: aynı ürünün ≥ 500 bin izlenmeli videosu var mı (yalnız izle ve oku). Giriş isteyip yapılamazsa **engel değildir**: `viral_video` sütununa `dogrulanamadi-giris` yaz (`denetle` bunu `ig_tt=dogrulanamadi-giris` risk notu olarak basar, kararı düşürmez); karar (a) + (c) ile verilir;
   (c) Meta Reklam Kütüphanesi TR: aktif reklam ≤ 3 mü (`${CLAUDE_SKILL_DIR}/referans/zaten-viral-kontrolu.md` §3; günlük sorgu kotası `spy` ile ortaktır). (c) de yapılamazsa engel değildir: karar (a) ve satıcı sayısıyla verilir, SAT kartında "Meta reklam sayısı okunamadı" notu olur. Viral veritabanı yokken "zaten viral mi" engel değil nottur; ücretsiz vekil Meta aktif reklam sayısı ve satıcı sayısıdır.
7. **Marj:** kısa listedeki her ürün için `marj.csv` satırı → `python3 "${CLAUDE_SKILL_DIR}/trendyol/scripts/tr_marj.py" marj.csv --cikti marj-sonuc.tsv` çıkış 0.
   Çıkış 0 olmadan marj yazılmaz. Oranları `${CLAUDE_SKILL_DIR}/trendyol/referans/tr-oranlari.tsv` tutar; değeri olmayan oran için betik yerleşik temkinli varsayılanı kullanır ve `oran_kaynaklari`na "varsayim" yazar (hesap durmaz). Marka ROAS yoksa `karar_marj` `dogrulanamadi`: SAT'ı engellemez, kart notu olur. `alis_tl` tedarikçi alışıdır; tedarikçi yoksa marj hesaplanmaz, not düşer.
8. **Kanıt:** sıra puanı en yüksek ≤ 5 aday `skeptic` ajanına; dosya `is/firsat/kanit/NN-urun-adi.md` (hunter kanıt şablonu + 3 ek bölüm: Tedarik ve fatura ·
   Fiyat şeffaflığı · Net marj). Tedarik: `${CLAUDE_SKILL_DIR}/trendyol/referans/tedarik-ve-fatura.md`; şeffaflık puanı: `${CLAUDE_SKILL_DIR}/trendyol/referans/fiyat-seffafligi.md`.
9. **Karar ve çıktı:** SAT ya da ELE; ELE `elenenler.tsv`'ye (kullanıcıya gösterilmez). Kanıt ajanı "aynı ürün başka yerde daha ucuz" gerekçesiyle ELE vermez (tedarikçi daha ucuzsa bu marjdır); yalnız Trendyol'da aynı ürünün satış fiyatı hedefimizin altındaysa fiyat notu yazar. `sinama` 3/3 tutmadan "bulundu" denmez. Sonra
   `python3 "${CLAUDE_SKILL_DIR}/trendyol/scripts/excel_hazirla.py" is/firsat/trendyol` → çıktıda `TAMAM`. SAT onaylanırsa `captain` `paket.py urun-yaz` ile `urun-paketi.json` yazar, iş `builder`'a geçer.

## Chrome kuralları (yalnız oku)
- Trendyol düz istekte (curl, WebFetch) engel döndürür; yalnız Claude in Chrome ile okunur. Tarayıcı yoksa sonuç `dogrulanamadi`.
- Sabit günlük kota yok; hedef **N SAT bulana kadar** taramaktır (varsayılan N=5). **Engel sinyaline göre dur** (HTTP 429/403, captcha/robot sayfası, art arda 3 boş sonuç sayfası). Her istekten sonra `trendyol_kontrol.py kota sonuc <ok|bos|429|403|captcha>`; engel sinyali kilit yazar (çıkış 3), o gün Trendyol'a dokunulmaz. İstekler arası ≥ 15 sn, oturum ≤ 1 saat. Üst güvenlik sınırı 100 arama + 300 ürün sayfası/gün (`varsayim`, ölçülmedi).
- Kayıt hatası kota yakmaz: aynı hedefin tekrarı sayılmaz; başarısız/yanlış kayıt `kota iade <arama|urun> <hedef>` ile düşülür.
- CAPTCHA ya da engel sayfası: çözme, atlatma, gizli pencere yok. Dur, okunanı kaydet, `kota sonuc captcha` yaz.
- Yapılmaz: giriş, sepete ekleme, favori, satın alma, satıcıya mesaj, yorum. Satıcıyla iletişim kullanıcının kararıdır.

## Kapılar (hiçbiri atlanmaz)
1. `kota` çıkış 0 olmadan istek yok · 2. `denetle` çıkış 0 olmadan kısa liste yok · 3. `sinama` 3/3 olmadan "bulundu" yok ·
4. `tr_marj.py` çıkış 0 olmadan marj yok · 5. kanıt dosyası olmadan SAT yok · 6. `excel_hazirla.py` çıkış 0 olmadan "Excel hazır" yok.

## Kırmızı çizgiler
- Satın alma, numune, satıcıyla temas: kullanıcı onayı olmadan yok; onay `KARARLAR.md`'ye.
- Sahte çizili fiyat, sahte stok, sahte yorum yok (IDD-02). Trendyol siparişini doğrudan müşteri adresine göndermek varsayılan olarak yasak (`${CLAUDE_SKILL_DIR}/trendyol/referans/tedarik-ve-fatura.md`).
- Vergi ve fatura cümleleri hüküm değildir; mali müşavirle doğrulanır.

## Referanslar
| Dosya | Ne zaman |
|---|---|
| `${CLAUDE_SKILL_DIR}/trendyol/referans/olcutler.md` | ölçüt tablosu, net marj ve karar kuralı |
| `${CLAUDE_SKILL_DIR}/trendyol/referans/trendyol-okuma.md` | sayfadan ne okunur, hangi sırayla |
| `${CLAUDE_SKILL_DIR}/trendyol/referans/tedarik-ve-fatura.md` | A/B/C tedarik kademeleri, fatura |
| `${CLAUDE_SKILL_DIR}/trendyol/referans/fiyat-seffafligi.md` | müşteri aynı ürünü Trendyol'da bulur riski, puan 0–3 |
| `${CLAUDE_SKILL_DIR}/trendyol/referans/esikler.tsv`, `${CLAUDE_SKILL_DIR}/trendyol/referans/tr-oranlari.tsv` | eşikler ve TR oranları (betikler buradan okur) |
| `${CLAUDE_SKILL_DIR}/trendyol/scripts/kirma_testi.py` | betiklerin kendi testi (her kapı önce kırılır); şema: eski 19 alan ya da + `rakip_tl`, `alis_kaynak`, `veto` (22 alan, `${CLAUDE_SKILL_DIR}/trendyol/sablon/adaylar.tsv`) |

## Kullanıcıya özet (≤ 10 satır, YALNIZ SAT)
`python3 "${CLAUDE_SKILL_DIR}/trendyol/scripts/trendyol_kontrol.py" ozet is/firsat/trendyol/adaylar.tsv --hedef N` çıktısı aynen verilir: `SAT k/N` · her SAT için ürün, yorum · puan, alış (tedarikçi) → satış (kat), "ilk testte kontrol et" notları · kanıt dosyası yolu · Excel yolu.
İZLE/ELE satırı, sayısı ve ürün adı kullanıcıya yazılmaz. N'e ulaşılamazsa tek satır: `k SAT buldum, sebep: …` (İZLE listesi yok). Son satır tek cümle risk: Trendyol yorum sayısı satış adedi değildir (talep vekilidir); eşiklerin yarısı varsayımdır, ilk 20 üründe karar DENEME; TR reklam maliyeti ölçülmedi.

**Zorunlu son satır (SAT varsa):** `Ben olsam: <SAT ürün> — <üründen 1 gerekçe> — risk: <1 risk>`. SAT yoksa yalnız `0 SAT buldum, sebep: …`.
