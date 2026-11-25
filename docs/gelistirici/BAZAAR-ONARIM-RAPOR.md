# Bazaar onarım raporu (2026-11-24)

Sorun: gerçek kullanımda 36 aday, 0 SAT, 28 İZLE. SAT yapısal olarak imkânsızdı.

## Değişen dosyalar (commit yok)
- `plugins/viral-urun-ekibi/skills/bazaar/referans/tr-oranlari.tsv` doldu
- `.../referans/esikler.tsv` kota satırları
- `.../referans/olcutler.md`, `.../SKILL.md`
- `.../scripts/bazaar_kontrol.py` (kota, ig_tt notu), `.../scripts/kirma_testi.py` (49 yeni/uyarlanan vaka dahil 66 test)
- `plugins/viral-urun-ekibi/ortak/tarifler/06-trendyol-ve-aliexpress-avi.md`
- `tr_marj.py` değişmedi (kullanıcı hücresi > dosya zaten böyleydi).

## Oranlar (tarih 2026-11-24)
| anahtar | değer | durum | kaynak |
|---|---|---|---|
| kdv_yuzde | 20 | kaynakli | PwC bülteni (7346 sayılı karar, 10.07.2023). gib.gov.tr açılamadı (404); mali müşavirle doğrula |
| odeme_yuzde | 4.29 | kaynakli | iyzico yayınlı kurumsal oran (bireysel 4.49); karekod.org 2026 aynı. PayTR resmi sayfada oran yok (teklifle, %2,19'dan başlar, sabit ücret yok) |
| odeme_sabit | 0.25 | kaynakli | iyzico |
| musteri_kargo | 150 | kaynakli | ideasoft.com.tr tarife derlemesi: PTT 1 desi 150 TL il içi / 220 il dışı (KDV dahil, 04.02.2026); Yurtiçi 226,50 + KDV. 2-3 desi tarifede yok |
| kapida_odeme_orani_yuzde / kapida_ek_ucret | 0 / 0 | kurucu-karari | kurucu kapıda ödeme kullanmıyor |
| iade_orani_yuzde | 10 | varsayim | ölçülmüş TR kaynağı bulunamadı (dünya ort. %16,9; TR blog %20-30 giyim) |
| iade_birim_maliyet | 150 | varsayim | bir yön kargo kaybı |
| reklam_payi_yuzde | 25 | varsayim | yalnız net_kar için; karar_marj başabaş ROAS'tan gelir |

## Kök neden onarımları
1. Oranlar dolu; boş hücre artık HATA vermez, kaynak sırası kullanıcı > kaynakli > varsayim.
2. Instagram/TikTok (b) yapılamazsa engel değil: `viral_video=dogrulanamadi-giris`, `denetle` risk notu basar, karar düşmez. Meta (c) de yoksa en fazla İZLE (mevcut davranış, testli).
3. Kota: sabit 15/40 kalktı. Engel sinyali (`kota sonuc 429|403|captcha|bos`; art arda 3 boş = kilit), üst güvenlik sınırı 100 arama / 300 ürün (varsayim; 300'ü ben koydum, istenen yalnız 100'dü). Kök neden: kota.tsv'ye kayıt istekten önce yazılıyor, tekrar ve hatalı satır da sayılıyordu. Düzeltme: aynı hedef tekrarı sayılmaz, `kota iade` ile düşülür.
4. SKILL.md özet: en güçlü 3 her zaman, zorunlu son satır "Ben olsam: ... — risk: ...".
5. Tohum: ilk turda ≥5 niş, niş başına ≤5 aday (SKILL + tarif). Eşiklere dokunulmadı.

## DİKKAT: karar noktası
Kaynaklı oranlarla başabaş ROAS ≤ 2,0 kapısı pratikte tutmuyor. 699 TL satış / 250 TL alış fixture'ı: katkı 137-179 TL, ROAS 3,9-5,1 → marj kapısı ELE; kargo 80 TL olsa 2,81 → İZLE. `denetle` marjı içermediğinden SAT-ADAYI çıkar, ama marj adımı (tr_marj) SAT vermez. Seçenekler: kargo anlaşması oranı, daha yüksek satış fiyatı ya da kurucu ROAS eşiğine karar versin. Eşik gevşetilmedi.

## Test çıktıları
- `python3 skills/bazaar/scripts/kirma_testi.py`: TOPLAM 66 test, 0 kaldi
- `sh scripts/anonim_kontrol.sh`: temiz, çıkış 0
- `python3 scripts/sozlesme_test.py`: 49/49 geçti, çıkış 0
- Yeni vakalar: (i) iyi fixture SAT-ADAYI + kaynaklı oranla hesap; (ii) ig_tt tek başına düşürmez, Meta de yoksa İZLE; (iii) kapıda 0 iken ödeme = 19.00; (iv) tekrar/iade/429/3 boş kota.
