---
name: bazaar
description: "Bazaar (Trendyol fırsat avı). Finds in-demand, not-yet-viral, cheap Trendyol products to sell in our own Shopify store. \"Trendyol'dan ürün bul\", \"Trendyol fırsatı\", \"Türkiye'de satılacak ürün\", \"ucuza alıp markalı satalım\", \"Trendyol'da ilgi gören ürün\" isteklerinde çağır."
---

# Trendyol fırsat avı

**Amaç:** Türkiye'de Trendyol'da ilgi gören, Instagram/TikTok'ta henüz viral olmamış, ucuza alınabilen ürünü bulmak; **kendi markalı Shopify mağazamızda** alışın 2–3 katına satmak.
**Bitiş durumu:** `is/firsat/trendyol/adaylar.tsv` denetimden geçti; kısa listedeki her ürünün `is/firsat/kanit/` altında kanıt dosyası var;
`urunler.xlsx` üretildi (çıktıda `TAMAM`); kullanıcıya ≤ 10 satır özet verildi; `.ekip/DURUM.md` güncel.

Önce oku: `${CLAUDE_PLUGIN_ROOT}/ortak/viral-dna.md` ve `${CLAUDE_PLUGIN_ROOT}/ortak/sozluk.md` (SAT / İZLE / ELE ve "zaten viral" yalnız sözlükteki anlamıyla).
Eşikler ve her ölçütün durumu (`deneme` / `varsayim` / `kurucu-karari`): `${CLAUDE_SKILL_DIR}/referans/esikler.tsv`. Ölçüt tablosu: `${CLAUDE_SKILL_DIR}/referans/olcutler.md`.
Başvuru modeli: `hunter` (hafıza protokolü, brief kuralları, özet biçimi aynı kalıp).
**Tarif:** `${CLAUDE_PLUGIN_ROOT}/ortak/tarifler/06-trendyol-ve-aliexpress-avi.md`. **İlk çalıştırma = oran turu:** `referans/tr-oranlari.tsv` boşsa önce her oranı kaynak URL'siyle doldur (kaynak yoksa boş kalır, oran uydurulmaz). Karar etiketleri: SAT · **SAT (koşullu)** (marj ya da viral doğrulanamadı, diğer ölçütler SAT; `denetle` `SAT-KOSULLU` yazar) · İZLE · ELE. Çıktı: **5 niş × 5 ürün**; görünüşü ucuz/estetiği zayıf ürün (telefon standı tipi) ELE.

## Akış (9 adım)
1. **Hafıza:** `.ekip/DURUM.md`, `.ekip/KARARLAR.md` oku. Pazar TR sabittir, sorulmaz. `is/firsat/trendyol/` yoksa `${CLAUDE_SKILL_DIR}/sablon/adaylar.tsv` ile kur.
2. **Kota:** `python3 "${CLAUDE_SKILL_DIR}/scripts/bazaar_kontrol.py" kota durum`. Çıkış 4 (günlük tavan) ya da 3 (kilit) ise dur, kullanıcıya söyle.
3. **Tohum:** arama terimleri (Türkçe, 2–4 kelime) iki kaynaktan: `ortak/viral-dna.md` mekanizmaları (ürün adı değil mekanizma) ve analiz veritabanında
   viral aileler (`v_viral_urun`) → aynı ailenin **farklı modeli**. Terimler `aramalar.tsv`'ye yazılır; aynı terim iki kez aranmaz.
4. **Tarama:** ağır iş `scout` ajanında. Chrome'da `https://www.trendyol.com/sr?q=<terim>` (sıralama: çok değerlendirilenler). Her arama ve her ürün sayfasından
   ÖNCE `bazaar_kontrol.py kota kaydet <arama|urun> <hedef>` (çıkış 0 olmadan istek yok). Ürün sayfasından okunur: ad, link, fiyat, değerlendirme sayısı,
   puan, diğer satıcı sayısı, satıcı adı, görsel. Satır `adaylar.tsv`'ye; yeni ürün öncesi `bazaar_kontrol.py tekrar <link>`.
   Okuma ayrıntısı: `${CLAUDE_SKILL_DIR}/referans/trendyol-okuma.md`.
5. **Ön eleme:** `bazaar_kontrol.py denetle adaylar.tsv [--elenenlere-yaz]` şemayı ve eşikleri uygular, her satıra `on_karar` yazar. Çıkış 0 olmadan kısa liste yok.
6. **Viral kontrolü:** (a) `bazaar_kontrol.py viral --db <proje>/veri/analiz.db adaylar.tsv` (yok / aile-var / ayni-urun-viral / dogrulanamadi; veritabanı yoksa hepsi
   dogrulanamadi); (b) Instagram ve TikTok'ta Türkçe ürün adıyla arama: aynı ürünün ≥ 500 bin izlenmeli videosu var mı (yalnız izle ve oku);
   (c) Meta Reklam Kütüphanesi TR: aktif reklam ≤ 3 mü (`hunter/referans/zaten-viral-kontrolu.md` §3; günlük sorgu kotası `spy` ile ortaktır).
7. **Marj:** kısa listedeki her ürün için `marj.csv` satırı → `python3 "${CLAUDE_SKILL_DIR}/scripts/tr_marj.py" marj.csv --cikti marj-sonuc.tsv` çıkış 0.
   Çıkış 0 olmadan marj yazılmaz. Oranları `referans/tr-oranlari.tsv` tutar; boşsa betik HATA verir, **oran uydurulmaz** (kurucu ya da araştırma turu doldurur).
8. **Kanıt:** sıra puanı en yüksek ≤ 5 aday `skeptic` ajanına; dosya `is/firsat/kanit/NN-urun-adi.md` (`hunter` şablonu + 3 ek bölüm: Tedarik ve fatura ·
   Fiyat şeffaflığı · Net marj). Tedarik: `referans/tedarik-ve-fatura.md`; şeffaflık puanı: `referans/fiyat-seffafligi.md`.
9. **Karar ve çıktı:** SAT / İZLE / ELE; ELE `elenenler.tsv`'ye. `sinama` 3/3 tutmadan "bulundu" denmez. Sonra
   `python3 "${CLAUDE_SKILL_DIR}/scripts/excel_hazirla.py" is/firsat/trendyol` → çıktıda `TAMAM`. SAT onaylanırsa `captain` `paket.py urun-yaz` ile `urun-paketi.json` yazar, iş `builder`'a geçer.

## Chrome kuralları (yalnız oku)
- Trendyol düz istekte (curl, WebFetch) engel döndürür; yalnız Claude in Chrome ile okunur. Tarayıcı yoksa sonuç `dogrulanamadi`.
- Günlük tavan ≤ 15 arama + ≤ 40 ürün sayfası, istekler arası ≥ 15 sn, oturum ≤ 1 saat. Tavanı `bazaar_kontrol.py kota` tutar; kayıtsız istek yapılmaz.
  Bu sayılar **başlangıç varsayımıdır** (Trendyol'da ölçülmedi).
- CAPTCHA ya da engel sayfası: çözme, atlatma, gizli pencere yok. Dur, okunanı kaydet, `kota kilit <sebep>` yaz; o gün Trendyol'a dokunulmaz.
- Yapılmaz: giriş, sepete ekleme, favori, satın alma, satıcıya mesaj, yorum. Satıcıyla iletişim kurucu kararıdır.

## Kapılar (hiçbiri atlanmaz)
1. `kota` çıkış 0 olmadan istek yok · 2. `denetle` çıkış 0 olmadan kısa liste yok · 3. `sinama` 3/3 olmadan "bulundu" yok ·
4. `tr_marj.py` çıkış 0 olmadan marj yok · 5. kanıt dosyası olmadan SAT yok · 6. `excel_hazirla.py` çıkış 0 olmadan "Excel hazır" yok.

## Kırmızı çizgiler
- Satın alma, numune, satıcıyla temas: kurucu onayı olmadan yok; onay `KARARLAR.md`'ye.
- Sahte çizili fiyat, sahte stok, sahte yorum yok (IDD-02). Trendyol siparişini doğrudan müşteri adresine göndermek varsayılan olarak yasak (`referans/tedarik-ve-fatura.md`).
- Vergi ve fatura cümleleri hüküm değildir; mali müşavirle doğrulanır.

## Referanslar
| Dosya | Ne zaman |
|---|---|
| `referans/olcutler.md` | ölçüt tablosu, net marj ve karar kuralı |
| `referans/trendyol-okuma.md` | sayfadan ne okunur, hangi sırayla |
| `referans/tedarik-ve-fatura.md` | A/B/C tedarik kademeleri, fatura |
| `referans/fiyat-seffafligi.md` | müşteri aynı ürünü Trendyol'da bulur riski, puan 0–3 |
| `referans/esikler.tsv`, `referans/tr-oranlari.tsv` | eşikler ve TR oranları (betikler buradan okur) |
| `scripts/kirma_testi.py` | betiklerin kendi testi (her kapı önce kırılır) |

## Kullanıcıya özet (≤ 10 satır)
Tarama (arama ve sayfa sayısı) · aday · SAT-ADAYI / İZLE / ELE sayısı · en güçlü 3 ürün (yorum, puan, alış, önerilen satış, çarpan) · kanıt dosyaları ·
Excel yolu · son satır tek cümle risk: Trendyol yorum sayısı satış adedi değildir (talep vekilidir); eşiklerin yarısı varsayımdır, ilk 20 üründe karar DENEME;
müşteri ürünü Trendyol'da ucuza bulabilir; TR reklam maliyeti ölçülmedi, `reklam_payi_yuzde` dolana kadar `net_kar` hesaplanmaz.
