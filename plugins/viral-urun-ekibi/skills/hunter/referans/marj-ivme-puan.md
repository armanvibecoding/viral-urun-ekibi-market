# İniş maliyeti, 7 günlük ivme ve 10 ölçütlü ürün puanı

Ne zaman okunur: kısa listeye giren aday için kanıt dosyası yazılırken (akış adım 7) ve gün 7 ölçümünde.
Eski A–D sıra puanı (`kanit-ve-karar.md` §1) ön eleme için kalır; bu dosya kısa listeyi **iniş maliyeti + ivme** ile puanlar.

## 1. İniş maliyeti — `is/firsat/marj.csv`
Şablon: `${CLAUDE_SKILL_DIR}/sablon/marj.csv`. Bir satır = bir ürün × bir pazar. Tutarlar **o pazarın para biriminde**
(US USD · TR TRY · UK GBP · DE/FR/ES EUR); betik kur çevirmez, çevirdiğin kuru `kaynak_notu`'na yaz.

| Sütun | Ne | Boşsa |
|---|---|---|
| `satis_fiyati` | müşterinin ödediği fiyat (AB/UK/TR'de KDV dahil) | HATA |
| `urun_maliyeti` · `kargo` | AliExpress/CJ **normal** fiyat + hedef pazara kargo | HATA |
| `gumruk_orani_yuzde` | ürünün tarife oranı (ABD: HS + menşe; Çin için ek tarifeler dahil) | eşik altıysa pazar kuralı; yoksa HATA |
| `tarife_kalemi` | pakette kaç farklı tarife alt başlığı (AB 3 €/kalem) | 1 |
| `araci_sabit` | gümrük aracısı / beyan ücreti, sipariş başına | oranlar dosyası; yoksa HATA |
| `odeme_yuzde` · `odeme_sabit` | ödeme sağlayıcı / COD tahsilat ücreti | oranlar dosyası; yoksa HATA |
| `iade_orani_yuzde` · `iade_birim_maliyet` | iade + **kapıda ödeme reddi** oranı ve iade edilen sipariş başına kayıp (gidiş+dönüş kargo, COD ücreti, satılamayan ürün) | oranlar dosyası; yoksa HATA |
| `teslim_gun` | hedef pazarda müşteriye kadar gün | HATA |

Ödeme, aracı ve iade için **eklentide varsayılan yok** (hesaba ve tedarikçiye göre değişir). Kendi değerini
`is/firsat/pazar-oranlari.tsv` dosyasına (aynı başlıkla: `pazar anahtar deger durum tarih kaynak not`) bir kez yaz;
betik onu eklentideki tablonun üstüne okur. Bilinmeyen değer tahminle doldurulmaz — satır hesaplanmaz, kanıt dosyasına
"doğrulanamadı" yazılır.

Komut: `python3 "${CLAUDE_SKILL_DIR}/scripts/marj_hesap.py" is/firsat/marj.csv --cikti is/firsat/marj-sonuc.tsv`
Çıkış 1 = eksik/yanlış veri. `UYARI` satırları doğrulanmamış ya da 180 günden eski oranı gösterir → kanıt dosyasının
"Bulunamayan veri" bölümüne aynen geçer.

### Pazar oranları (tarihli, düzenlenebilir) — `${CLAUDE_SKILL_DIR}/referans/pazar-oranlari.tsv`
`durum`: `dogrulandi` (birincil kaynak açıldı) · `ikincil` (hukuk bürosu/haber, birbirini tutuyor) · `dogrulanmadi` · `model` (hesap varsayımı).
Özet (2026-11-17):
- **ABD:** 800 $ de minimis 29.08.2025'te tüm ülkeler için askıya alındı → eşik yok, her satıra ürün tarife oranı (ikincil).
- **TR:** 30 € bireysel muafiyetin 6 Şubat 2026'da kalktığı iddiası → **doğrulanmadı** (resmî metin açılmadı). Varsayım: TR = yerel stok.
- **AB (DE/FR/ES):** 150 € gümrük muafiyeti 1 Temmuz 2026'da kalktı; 150 € altına geçici **3 €/tarife alt başlığı** (ikincil;
  "ürün başı mı kalem başı mı" kaynaklar çelişkili). KDV 22 € muafiyeti 2021'de kalktı, ≤150 €'da IOSS ile satışta tahsil (doğrulanmadı).
- **UK:** ≤135 £ gümrük muafiyeti sürüyor, en geç Ekim 2028'de kalkacak (ikincil); VAT satışta tahsil.
Oran değişince satırı silme: yeni `tarih` ve `kaynak` ile güncelle.

### Elle sağlama örneği (kırma testinde birebir tutuyor)
ABD, satış 39,99 $ · ürün 8 · kargo 4 · tarife %30 (FOB → matrah 8) · aracı 1,50 · ödeme %2,9 + 0,30 · iade %5 × 12:
gümrük 2,40 · ödeme 1,4597 · iade 0,60 → iniş **17,96** · kâr **22,03** · çarpan 39,99 / 17,96 = **2,23×** → P5 = 1.
(Eski hesap satış ÷ (ürün+kargo) = 3,33× gösterirdi: iniş maliyeti ürünü "≥3×"ten "2–3×"e indiriyor.)

## 2. 7 günlük ivme — `is/firsat/ivme.csv`
Şablon: `${CLAUDE_SKILL_DIR}/sablon/ivme.csv`. Her ürün için iki satır: `olcum=t0` (kısa listeye girdiği gün) ve `olcum=t7` (7–14 gün sonra),
**aynı yerden, aynı sorguyla** okunur; sorgu `kaynak_notu`'na yazılır.

| Sinyal | Nereden |
|---|---|
| `reklam_sayisi` (zorunlu) | Meta Reklam Kütüphanesi, hedef ülke, aktif, tam ifade (`zaten-viral-kontrolu.md` §3; kontrol sorgusu dolu olmalı) |
| `yorum_sayisi` | rakip ürün sayfası (Judge.me/Loox) — yalnız **değişim** anlamlı |
| `bsr` | Amazon Best Sellers Rank (küçülmesi = iyileşme) |
| `trendyol_degerlendirme` · `tiktok_satilan` | TR Trendyol · ABD TikTok Shop ürün kartı |
| `yeni_magaza` | aynı ürünü satan mağaza sayısı (`/products.json` ürün eklenme tarihi) |
| `perakende_satici` | Amazon/Walmart/Trendyol'da aynı ürünü satan satıcı sayısı |
| `akraba_kanit` | E/H — K2 akraba ürün kanıtı (`ortak/viral-dna.md`) |

Komutlar: `python3 "${CLAUDE_SKILL_DIR}/scripts/ivme_olc.py" bekleyen is/firsat/ivme.csv` (bugün t7'si gelenler; her oturum başında)
· `... ivme_olc.py bant is/firsat/ivme.csv` → **ERKEN DALGA / BOŞ / DOYMUŞ / BELİRSİZ** + P3, P4.
Ölçülmeyen sinyal boş bırakılır (0 yazılmaz — 0 "ölçtüm, yok" demektir). Eşikler `referans/ivme-esikleri.tsv`'de, **öneri, ölçülmedi**;
ilk 3 üründen sonra kalibre edilir.

## 3. Ürün puanı (10 ölçüt × 0–2 = 0–20) — kanıt dosyasına tablo olarak
Kapılar (K1 gösterilebilirlik, K2 akraba, K3 veto — `ortak/viral-dna.md`) geçilmeden puanlanmaz.

| # | Ölçüt | 0 | 1 | 2 | Kaynak |
|---|---|---|---|---|---|
| P1 | Mekanizma gücü | akraba yok | akraba var, M4/M13 tek başına | akraba ≥3 bağımsız markada milyon ya da M2/M3 | `kanit-ve-karar.md` §1 A ekseni |
| P2 | Kreatif kanıt (kendi kayıt tablomuz) | kazanan satır 0 | 1–2 | ≥3 farklı hesap | kreatif kayıt |
| P3 | Talep ivmesi (7 gün) | ölçülemedi / düşüş | sabit | artış | `ivme_olc.py bant` |
| P4 | Girilebilirlik | DOYMUŞ | BOŞ / BELİRSİZ | ERKEN DALGA | `ivme_olc.py bant` |
| P5 | Brüt marj (iniş maliyetiyle) | <2× | 2–3× | ≥3× | `marj_hesap.py` |
| P6 | Teslim süresi hedef pazarda | >15 gün | 8–15 | ≤7 | `marj_hesap.py` |
| P7 | Mekanizma doğrulaması | doğrulanamadı | satıcı videosu gerçek | alıcı foto/videosu | `kanit-ve-karar.md` §2 |
| P8 | Üretilebilirlik (AI ya da gerçek çekim) | AI kanıtı yok | AI kanıtı 1–2 | ≥3 ya da gerçek çekim mümkün | studio |
| P9 | Paylaşım tetikleyicisi | yok | sezon/hediye | şaka/kimlik/ortak acı (V4) | `ortak/viral-dna.md` |
| P10 | Uyum ve iade riski | veto yakını / beden / kırılgan | orta | düşük + pazar kapısı temiz | `kanit-ve-karar.md` §3 Riskler |

Kanıt dosyasına yazım: `| P1 | P2 | … | P10 | Toplam |` + her 0 için tek cümle neden.
**Eşik (deneme — ilk 5 karardan sonra kalibre):** ≥14 SAT adayı · 10–13 İZLE · ≤9 ELE.
Puan SAT için **tek başına yetmez**: `kanit-ve-karar.md` §2 koşulları (mekanizma alıcı kanıtıyla doğrulandı, sınama geçti) aynen geçerli.
P7 = 0 olan ürün toplam kaç olursa olsun SAT olmaz.
