# Yalnız SAT: ürün avı karar sistemi (bazaar + hunter)

Tarih: 2026-11-25 · Karar: kurucu (danışan geri bildirimlerinden: "SAT/İZLE/ELE muhabbeti can sıkıcı, sadece SAT, Satları göster"; ölçülen durum: 36 aday 0 SAT).
Kapsam dışı bırakılanlar: `ortak/sinav/**`, `scripts/sinav_kos.py`, cut/studio/builder, `tr_marj.py` ROAS hesabı (yalnız oran varsayılanı eklendi, aşağıda).

## 1. Ne değişti (eski → yeni kural)

| Konu | Eski | Yeni |
|---|---|---|
| Sınıflar | SAT, SAT (koşullu), İZLE, ELE | Yalnız SAT ve ELE. Kullanıcıya (sohbet, Excel ana sayfası, rapor) yalnız SAT gider |
| Bilinmeyen ölçüt | `dogrulanamadi`/boş → satır en fazla İZLE (`olcutler.md`, `kanit-ve-karar.md` Öncelik satırı, `satir_karari`) | Engel değil: `neden` sütununda "Kontrol et: ..." notu, SAT kartında "ilk testte kontrol et" |
| ELE | en kötü ölçütün kararı; ölçülmüş "sınır" bandı İZLE | Yalnız kanıtlı engel: veto, kanıtlı negatif katkı (marj), kanıtlı doygunluk (satıcı, Meta, aynı ürün viral), eşiğin altında talep (yorum/puan), kat < 2,2 ya da satış < 399. Eski İZLE bantları (yorum 50–149, puan 4,0–4,19, satıcı 6–15, kat 1,8–2,19, Meta 4–10) ölçülmüş olduğu için ELE. Eşik değerleri DEĞİŞMEDİ |
| `alis_tl` | Trendyol perakende fiyatı okunuyordu, 100–600 TL bandı, kat = satış/alış | `alis_tl` yalnız tedarikçi (AliExpress/1688 aynı ürün; kaynak `alis_kaynak`). Trendyol fiyatı `rakip_tl` + hedef `onerilen_satis_tl`. Tedarikçi yoksa `alis_tl` boş, not "tedarikçi bulunamadı", kat = not. `alis_tl` bandı engel olmaktan çıktı (Trendyol perakendesine göre konmuştu); engel kat'tır |
| Kanıt ajanı | "aynı ürün başka yerde daha ucuz" ELE gerekçesi olabiliyordu | Skeptic bununla ELE vermez (tedarikçi daha ucuzsa marjdır); yalnız Trendyol'da aynı ürün hedefin altındaysa fiyat notu |
| Marka ROAS | yoksa `dogrulanamadi` → en fazla İZLE (`olcutler.md`) | yoksa SAT + not "marka ROAS yok"; `tr_marj.py` ROAS hesabı değişmedi, yalnız `denetle --marj-sonuc` birleştirmesi |
| tr-oranlari | değeri olmayan oran → HATA ("tahmin yapılmaz") | tsv'de değer yoksa yerleşik temkinli varsayılan (`tr_marj.py` `TEMKINLI`, tsv'deki kaynaklı değerlerle aynı), `oran_kaynaklari`'na "varsayim"; hesap durmaz |
| Viral veritabanı | yoksa `dogrulanamadi` → İZLE | engel değil, not; ücretsiz vekil Meta aktif reklam sayısı + satıcı sayısı (mevcut ölçütler) |
| Kota | üst sınır + "k adaya kadar" | üst güvenlik sınırı kalır; hedef "N SAT bulana kadar" (N=5 varsayılan, `ozet --hedef N`). N'e ulaşılamazsa tek satır "k SAT buldum, sebep: ...", İZLE listesi yok |
| Excel | 4 karar sınıfı, hepsi ana sayfada | "Ürünler" yalnız SAT (kanıt dosyalı); ham tablo gizli "Ayrıntı" sayfasında (denetim); SAT yoksa boş Ürünler (`--bos-izinli`) |
| Hunter | sıra 6–7 İZLE, SAT-KOŞULLU tek eksik kanıt kuralı | sıra <8 ölçülmüşse ELE; eksik sıra/numune/zaten viral/marj = not; SAT-KOŞULLU eski yazımı SAT sayılır, hata vermez |
| Mekanizma | alıcı videosuyla doğrulanmadan SAT yok | doğrulanamadıysa SAT + kartın ilk notu "ilk testte mekanizmayı doğrula"; çalışmadığı KANITLANIRSA ELE (kurucu kararının doğrudan sonucu; eski ders kalkmadı, nota taşındı) |

Şema: `adaylar.tsv` eski 19 alan kabul edilir (sinav fixture'ı değişmeden geçer); 22 alanlı yeni şema = + `rakip_tl`, `alis_kaynak`, `veto` (`sablon/adaylar.tsv`). 22 alanlı dosyada `alis_tl` dolu ama `alis_kaynak` boşsa, `alis_tl` = `rakip_tl` ise ya da `alis_kaynak` Trendyol ise `denetle` HATA verir.

## 2. Değişen dosyalar (dosya:satır)

Betikler
- `plugins/viral-urun-ekibi/skills/bazaar/scripts/bazaar_kontrol.py`: şema 19/22 (36); `sat_ailesi` (53); `satir_karari` yeni karar mantığı (132); `neden_yaz` (219); `nihai` (247); `adaylari_oku` (270); `denetle` (425, `--marj-sonuc`, alış denetimi, SAT-ve-engel çelişkisi HATA); yeni `ozet` (514).
- `.../bazaar/scripts/excel_hazirla.py`: `neden_kart` (57), `hazirla` (68): yalnız SAT + kanıt dosyalı satır; gizli Ayrıntı.
- `.../bazaar/scripts/tr_marj.py`: `TEMKINLI` (36) ve `al()` yedeği (123). ROAS koduna dokunulmadı.
- `.../hunter/scripts/firsat_kontrol.py`: `oneri_hesapla` (178), `nihai` (213), `ozet` (225), `denetle` (121, SAT-KOŞULLU hatası kalktı, SAT+engel ve Trendyol fiyatı HATA).
- `.../hunter/scripts/excel_hazirla.py`: `hazirla` (106) yalnız SAT.
- `ortak/excel_yaz.py`: `KARARLAR` (28) `SAT (koşullu)` çıktı, `--ayrinti-gizli`, `--bos-izinli` (267), hunter/bazaar özet satırı "N SAT".
- Testler: `bazaar/scripts/kirma_testi.py`, `hunter/scripts/kirma_testi.py`, `ortak/excel_test.py`.

Belgeler / kurallar
- `bazaar/referans/olcutler.md` (tablo ve kurallar baştan), `trendyol-okuma.md` (3. adım fiyat ayrımı), `tedarik-ve-fatura.md`, `fiyat-seffafligi.md`, `esikler.tsv` (dayanak sütunları), `sablon/adaylar.tsv` (22 alan), `bazaar/SKILL.md`.
- `hunter/SKILL.md`, `hunter/referans/kanit-ve-karar.md` (§2 karar kuralı, öncelik satırı kalktı), `dosya-sablonlari.md`, `zaten-viral-kontrolu.md`, `marj-ivme-puan.md`.
- `agents/skeptic.md`, `agents/scout.md`; `ortak/sozluk.md` (SAT/İZLE/ELE tanımları); `ortak/tarifler/06-...md`, `07-excel-teslim.md`.
- Dokunulmadı (üretilmiş kopyalar): `ekler/chatgpt/tarifler/06,07` (`scripts/chatgpt_paketi_yap.sh` ile yeniden üretilir).

## 3. Kırma testi: önce eski kod, sonra yeni kod

Önce = eski betikler (bazaar: çalışma kopyası değişmeden; hunter: `git show HEAD` kopyaları geçici klasörde; hunter ölçütü yalnız (a)–(f) satırlarıdır, geçici klasörde `marj_hesap` yolları bozuk olduğundan o testler yoruma katılmaz).

Bazaar (eski kod, 100 test, 31 KALDI; ilgili satırlar):
```
KALDI | (a) tüm ölçütler iyi ama viral=dogrulanamadi -> SAT-ADAYI | SAT-KOSULLU
KALDI | (b) marka ROAS yok (karar_marj dogrulanamadi) -> SAT-ADAYI | HATA: başlık tam bu 19 alan olmalı ...
KALDI | (b) ... ve not düşer: 'marka ROAS'
KALDI | (c) kanıtlı negatif katkı (katkı -12,50) -> ELE
KALDI | (d) veto (lisans/marka görünümü) -> ELE
KALDI | (e) alis_tl == rakip_tl ... -> denetim HATA
KALDI | (f) özet çıkış 0 | bazaar_kontrol.py: ... (ozet alt komutu yok, kullanım metni, çıkış 2)
```
Hunter (eski kod): (a) not düşmedi, `ozet` yok (çıkış 2); (b) "marj hesaplanmadı" notu yok; (c) negatif marj + durum SAT çıkış 0 (beklenen 1); (d) veto + SAT çıkış 0; (e) Trendyol fiyatı kabul (çıkış 0); (f) `ozet` yok.

Sonra = yeni kod:
```
bazaar  python3 skills/bazaar/scripts/kirma_testi.py  -> TOPLAM: 100 test, 0 kaldi   (çıkış 0)
hunter  python3 skills/hunter/scripts/kirma_testi.py  -> TOPLAM: 40 test, 0 kaldi    (çıkış 0)
excel   python3 ortak/excel_test.py                   -> TOPLAM: 76 test, 0 kaldı    (çıkış 0)
anonim  bash scripts/anonim_kontrol.sh                -> temiz (çıkış 0)
```
Vakalar: (a) viral=dogrulanamadi → SAT-ADAYI + "viral" notu; (b) marka ROAS yok → SAT + "marka ROAS" notu, ROAS iyiyse not yok; (c) katkı −12,50 / başabaş "zarar" → ELE; (d) veto dolu → ELE, "yok" → SAT; (e) `alis_tl`=`rakip_tl`, `alis_kaynak` Trendyol, alış var kaynak yok → üçü de HATA (çıkış 1), tedarikçi alışı + ayrı Trendyol fiyatı → 0; (f) 4 satırlık karışık tabloda `ozet` yalnız SAT'ı basar, `İZLE`/`ELE` sözcüğü ve elenen ürün adı yok, ≤10 satır, hedef 5 ve 1 SAT → "1 SAT buldum, sebep: ..." tek satır, hedef 1 → sebep satırı yok. Ek: Excel hazırlayıcı yalnız SAT satırı yazar, kanıt dosyası yoksa SAT kullanıcıya gitmez; uçtan uca (openpyxl venv): Ürünler 1 satır, Ayrıntı gizli, `TAMAM ... · 1 SAT`.

Mevcut testlerden bilerek değişenler (kurucu kararı gereği beklenen çıktı eski sınıfa göre yazılmıştı): yorum 149/50, puan 4,1, satış<399, satıcı/viral/Meta/marj doğrulanamadı vakaları İZLE/SAT-KOSULLU → ELE ya da SAT-ADAYI; "SAT-KOŞULLU eksik kanıtsız → HATA" artık 0; "boş oran → HATA" artık varsayılanla 0; hunter SAT-KOŞULLU hata vakaları 0; excel_test SAT (koşullu) → SAT.

Uyumluluk: `scripts/sinav_kos_test.py` bazaar 19 alanlı fixture'ı ve hunter `İZLE` durumlu fixture'ı kullanıyor; ikisi de yeni `denetle` ile çıkış 0 verdi (elle denendi). Tam `sinav_kos_test.py` koşusu sonucu raporun sonunda.

## 4. Açık noktalar (kurucuya)
1. Ölçülmüş "sınır" bandı artık ELE (ör. yorum 100, puan 4,1). Bu sistemi katı tutar; çok az SAT çıkarsa tek ayar `esikler.tsv`'deki bant sınırlarıdır (kurucu kararı gerekir, ben gevşetmedim).
2. Mekanizma doğrulanamadıysa SAT verilir (eski ders nota taşındı). Bu, "30 video boşa gitti" riskini artırır; ilk testte alıcı videosu şart notu kartın başında durur.
3. `alis_tl` bandı (100–600 TL) engel olmaktan çıktı: Trendyol perakendesine göre konmuştu, tedarikçi alışıyla anlamsız.
4. Hunter'da "marka ROAS" yok (yalnız marj çarpanı); hunter için eşdeğer: marj boş = not, `zarar`/≤1,0 = ELE.
