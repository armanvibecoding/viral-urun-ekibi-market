# Ekip geliştirme planı 0.6 — her ekip üyesi, ölçülen kusuruyla (2026-11-25)

**Sonuç:** 24–25 Kasım gecesi 7 sınav koşuldu. Kusurların çoğu ekip üyesinin "bilgisizliğinden" değil **iki boşluktan** çıktı:
(1) **malzeme** (gerçek ürün görüntüsü yoktu) ve (2) **ölçüm** (kapı var ama kırma testi tutmuyor ya da hiç yok).
Bu yüzden plan önce ölçümü, sonra malzeme hattını, en son zevki geliştirir. Her madde **kırma testiyle** kapanır; eşik gevşetilmez.
Önceki plan `EKIP-GELISIM-PLANI-FABLE.md` (2026-11-19) "gerçeklik kaynağı" fikrini verir; bu belge onu bu gecenin ölçümüne bağlar.

## 1. Bu gecenin ölçümü (dayanak)

| Sınav | Sonuç | Kök neden |
|---|---|---|
| 01 ürün videosu | b-zor jüri GEÇTİ 7,0 · a-kolay 6,0 · c-tuzak 4,5 | gerçek görüntü gelince 3,5 → 7,0; a = ilk 2 sn durağan (kurgu); c = katalog çekimi (malzeme) |
| 02 kanca | mekanik GEÇTİ; jüri koşulmadı | ön-üretim kareleri yer tutucu |
| 03 hikâye | mekanik 3/3; jüri ölçülemez | hikâye referansı yok |
| 04 ses | 3/3 GEÇTİ (araç düzeltmesiyle) | drop artışı toniğe bağlıydı |
| 05 görsel | K3+yasaklı GEÇTİ; K1 kupa sapı tutarsızdı (düzeltildi) | sadakati üreten kendisi denetliyor; OCR yazım hatası kaçırıyor |
| 06 ürün avı | GEÇTİ | "iyi ürün" değil "doğru işlendi" ölçülüyor |
| 07 site | mekanik GEÇTİ | iç not müşteri metnine sızdı; mobil ekran yanlış alındı |

Kapıların yakalamadığı, **lider gözünün** yakaladığı 4 kusur: yanlış ürün (ütü), kupa sapı, sızan iç dil, mobil ekran. → Ana ders: her üretimden sonra lider kare/ekran panosuna bakar; bulunan her kusur bir kapıya dönüşür.

## 2. Ekip üyeleri: kusur → düzeltme → ölçüm

Öncelik: **Ö1** bu hafta (ölçüm), **Ö2** sonraki (malzeme/üretim), **Ö3** sonra (zevk/strateji).

### Video kolu
| Üye | Ölçülen kusur | Düzeltme | Kırma testi / ölçüm | Öncelik |
|---|---|---|---|---|
| **studio** (ön-üretim) | malzemesiz üretime izin veriyor | ön-üretim kartına zorunlu `malzeme` alanı: gerçek ürün klibi (tedarikçi videosu / kurucu çekimi) + `KAYNAK.tsv`; yoksa yalnız "ön-üretim" modu | malzemesiz kart → `on_uretim_karti.py kontrol` KALDI | Ö1 |
| **cut** (kurgu) | 01 a: ilk 2 sn dokuz kare aynı; 01 b tur2: yanlış ürün klibi mekanik kapıdan geçti | `kurgu_kontrol`: ilk 2 sn kare farkı (≥ 2 belirgin değişim); `klip_etiket` ↔ ön-üretim `malzeme` kaynağı eşleşmesi (etiket "ürün" ise klip KAYNAK.tsv'de olmalı) | tur3 a videosu KALDI vermeli; tur2 b (ütü) KALDI vermeli | Ö1 |
| **fixer** | kök neden sınıflaması bu gece doğru çalıştı (malzeme/kurgu) | değişiklik yok; teşhis sırasına "önce malzeme var mı" sorusu en başa | — | Ö3 |
| **mixer** (ses) | `drop_sn 3.429` varsayılanı 8,6 sn döngüde rampa kapısını aşıyor; hikâye true-peak testi kırma tutmuyor | varsayılanı döngü süresinden türet; gerçek AAC zinciriyle kırma vakası | düzeltme öncesi test KALDI vermeli | Ö2 |
| **story** (senaryo) | 02'de jüri yok; kanca kütüphanesi başlık eksiği (düzeltildi) | 02 ön-üretim karelerini tedarikçi görüntüsünden kur, jüriyi koş | 02 jüri 3 kopya | Ö2 |
| **decoder** | kural kaynağı süzgeçte zayıf çıktı (REFERANSLAR.md) | "insansız hareketli yazılı ürün videosu" kulvarına ≥ 3 TR + 3 AB referans | referanslar.tsv satır sayısı | Ö3 |
| **jury** | pano biçimi farklı (bizimki çerçevesiz) → körlük sızıntısı; performansa kalibre değil ("DENEME") | `juri.py pano`: tüm ögeleri aynı biçime getir (aynı kare sayısı, aynı ızgara, çerçeve/hesap adı kırpılmış); kalibrasyon turu: performansı bilinen 6 video | sızıntı: kopyaların "biçim farkı" notu 0 olmalı; kalibrasyon: sıra ↔ gerçek performans | Ö1 (biçim) · Ö3 (kalibrasyon) |

### Görsel ve site kolu
| Üye | Ölçülen kusur | Düzeltme | Kırma testi / ölçüm | Öncelik |
|---|---|---|---|---|
| **sentinel** (K1/K2) | sadakati üreten ajan kendisi işaretledi; OCR 1–2 harf hatayı geçiriyor; TR harfleri ölçülemiyor | K1 bağımsız sentinel koşusu (üreten ≠ denetleyen); OCR Latin eşleşmesi birebir; TR için Tesseract (kurucu onayı) | "ANZIEHEN"/"KLEBEBLAT" KALDI vermeli | Ö1 |
| **forge** (üretim) | indirme betiği eski kurucu dosyasını taşıdı; kupa sapı 2 görselde farklı | indirme alımı: zaman + boyut + beklenen ad, eski dosyaya dokunmaz (kural + betik); istemde kilit görseli her çağrıda yüklenir | sahte eski dosyayla test: taşınmamalı | Ö1 |
| **panel** | 05 referansı yok → jüri ölçülemez | gorsel referansı: pazar başına ≥ 3 başarılı ürün sayfası galerisi | referanslar.tsv ≥ 3/pazar | Ö2 |
| **copy** | `kanit_ani` (çekim talimatı) site metnine kopyalandı | kural: kanıt anı görsel brifidir; ek kapı: vaka `kanit_ani` cümleleri / "Kanıt", "Der Moment" kalıbı site metninde = KALDI | tur1 b/c metni KALDI vermeli | Ö1 |
| **probe** (hız/erişim/arama) | 4 kapı canlı mağaza istiyor → hep ölçülemez | yerel ölçüm: üretilen HTML'de Lighthouse + axe (hesap gerekmez); canlı mağaza ölçümü ayrı | bilerek kontrastı bozuk sayfa KALDI | Ö2 |
| **shopper / architect** | mobil ekran görüntüsü yatay taşıyor (yöntem hatası) | ekran alma: geniş pencerede 390 px iframe (hafızadaki ölçülmüş yöntem) | 390 px görüntüde yatay taşma 0 | Ö1 |
| **atlas / muse** (marka, referans) | bu gece sınanmadı | marka sınavı yok → önce sınav vakası yaz | — | Ö3 |

### Ürün kolu
| Üye | Ölçülen kusur | Düzeltme | Kırma testi / ölçüm | Öncelik |
|---|---|---|---|---|
| **scout** | AliExpress fiyat/link okuma düzeltildi; yasaklı desen yanlış eşleşti ("5.0, 3 yorum") | koşucu yasaklı desenini daralt | "5.0, 3 yorum" metni GEÇTİ vermeli, gerçek yasaklı KALDI | Ö2 |
| **skeptic** | öncelik satırı eklendi | sonuç bağlama: bırakılan ve seçilen ürünlerin 30 gün sonraki durumu (hüküm defteri) | 30 gün sonra isabet oranı | Ö3 |
| **hunter / bazaar** | 06 "iyi ürün" ölçmüyor | kurucu turnuvası: her taramada ilk 3 → kurucu sıralar; sıra deftere | kurucu–ekip uyumu | Ö3 |

### Lider
| Üye | Ölçülen kusur | Düzeltme | Ölçüm | Öncelik |
|---|---|---|---|---|
| **captain** | kapılar 4 kusuru kaçırdı, lider gözü yakaladı; tur sınırı 2 iken 3. tur gerekti | her üretimden sonra zorunlu "lider panosu" (video: fps2 ızgara; görsel: set şeridi; site: 4 ekran) + "gördüğün kusur → kapı adayı" satırı; malzeme değişirse tur sayacı sıfırlanır (kurucu onayıyla) | her tur raporunda pano yolu + kapı adayı listesi | Ö1 |

## 3. Sıralı yol (dalgalar)

1. **Dalga 1: ölçüm (1 gece, ~3 sa, ücretsiz).** Ö1 kapıları: ilk 2 sn kare farkı · klip↔malzeme eşleşmesi · OCR birebir · kanıt anı sızıntısı · mobil iframe · jüri pano biçimi · indirme güvenliği · studio malzeme alanı. Her biri kırma testiyle; sonra 01/05/07 yeniden koşulur (yeni kapılar eski kusurları yakalıyor mu).
2. **Dalga 2: malzeme ve üretim (1–2 gece).** Kupa kurgu turu (desen değişimi ilk 1,5 sn) · c-tuzak için önce/sonra içeren tedarikçi videosu · 02 jüri · mixer varsayılanı · Lighthouse/axe yerel.
3. **Dalga 3: referanslar (1 gece, salt-okuma tarayıcı).** 03 hikâye (DE/US/TR ≥ 3), 05 görsel, 07 site referansları → üç jüri kapısı ölçülebilir olur.
4. **Dalga 4: gerçek sonuç (sürekli).** Jüri kalibrasyonu (performansı bilinen videolar) · hüküm defteri (kurucu sıralaması, 30 gün ürün takibi) · haftalık karne.
5. **Sürüm 0.6.0:** kurucu isteyince `referans-0.6.0` dalında dosya adıyla commit + ZIP.

Durma kuralı her dalgada aynı: özellik başına en çok 2 tur, gece tavanı 02:00, kapı gevşetilmez, "YAPILAMAZ" geçerli çıkış.

## 4. Kurucu kararı gerekenler
- Tesseract kurulumu (Homebrew gerekir; TR harf denetimi için).
- Tedarikçi videolarının gerçek yayında kullanımı (satıcı izni).
- ROAS ≤ 2,0 kapısı · `kanca_sorusu`/`cevap_an` zorunlu kalsın mı (öneri: kalsın).
- Canlı mağaza ölçümü için Shopify geliştirici mağazası (hesap açma = kurucu).

## 5. Doğrulanmayanlar
- Jüri puanı gerçek izlenmeye karşı kalibre edilmedi; "GEÇTİ" deneme hükmüdür.
- Tek gecelik 3 vaka; pazar başına genelleme zayıf.
