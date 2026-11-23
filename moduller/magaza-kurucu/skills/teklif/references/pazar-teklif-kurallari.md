# Pazar kartına göre teklif tasarımı (TR · ABD · UK · AB: DE/FR/ES)

Ne zaman okunur: akış adım 3–4 (teklif + sayfa). 2026-11-17 itibarıyla.
Etiket: **[K]** kaynak açıldı/ikincil kaynakla tutarlı · **[D]** doğrulanmadı (bu turda kaynak metni açılmadı — yayından önce kurucu ya da
hukukçu kontrol eder). `S#` = aşağıdaki kaynak listesi (pazar kültür araştırması, 2026-11-17). dil, fiyat yeri, AI ibaresi için `pazar-katmani.md`.
Bu dosya hukuki görüş değildir; **en sıkı yorum** seçilmiştir.

## Ortak taban (her pazar)
- Yorum, puan, müşteri/satış/stok sayısı, uzman onayı, önce-sonra: yalnız gerçek ve belgeli. Yoksa yer tutucu `{...}` ya da hiç.
- Aciliyet yalnız gerçek ve tarihli kampanyada; geri sayım sayacı, sahte stok, "X kişi bakıyor" hiçbir pazarda yok.
- Çizili fiyat: yalnız gerçekten uygulanmış önceki fiyat + kanıt (`karsilastirma_kaniti`). Kanıt yoksa çizili fiyat yok.
- Paket indirimi sonrası iniş maliyeti çarpanı ≥2× kalmalı (`hunter/scripts/marj_hesap.py`); kalmıyorsa paket indirimi küçülür.
- Garanti ne yazıyorsa o uygulanır; uygulanamayacak garanti (ör. "ömür boyu") yazılmaz.

## TR — güven > fiyat
| Öğe | Karar | Dayanak |
|---|---|---|
| Fiyat | **Kargo dahil** tek fiyat, KDV dahil, ekranda net | güven %48 · teslimat %45 · kolay iade %40 · fiyat %37 [K: Amazon TR/Veri Enstitüsü, S4]; saha 125 "Kargo dahil sadece ___ TL" |
| Garanti | "Koşulsuz iade" — süresiyle (yasal 14 gün cayma hakkının üstü güven sinyali) ve **gerçekten uygulanır** | saha 125 [K]; 14 gün cayma: Mesafeli Sözleşmeler Yönetmeliği [D] |
| Ödeme | yerli altyapı (iyzico/PayTR/Shopier), **taksit görünür**; kapıda ödeme A/B testi (genel payı %3,5, sosyal trafikte etkisi ölçülmedi) | S3, S5 [K]; COD etkisi [D — test] |
| Aciliyet | **YOK.** "Son 1 ürün", "sadece bugün" dolandırıcılık işareti olarak algılanıyor | S11 [K] |
| Sosyal kanıt | yalnız satın alanın yorumu; AI kullanımı açıkça belirtilir; gerçek kişinin AI kopyasıyla tavsiye yok | Ticari Reklam Yönetmeliği değişikliği 1 Ağu 2026 (haber özeti) [D], S10 |
| İndirim | önceki fiyat kuralı: haberde "son 10 gün en düşük", eski kural 30 gün → **30 gün** uygula | `pazar-katmani.md` §3 [D] |
| Zorunlu sayfalar | ön bilgilendirme formu, mesafeli satış sözleşmesi, iade koşulları, satıcı unvan/adres/iletişim | [D] |
| İnfluencer | `#reklam`/`#işbirliği` baştan görünür | S9 [K] |

## ABD — FTC
| Öğe | Karar | Dayanak |
|---|---|---|
| Fiyat | 30–60 $ bandı (saha medyanı 46,97 $); fiyat videoda değil caption/sayfada | `pazar-katmani.md` §1 [K saha] |
| Paket | 2'li/3'lü paket yaygın (65 sitenin 20'sinde paket uygulaması) | `pazar-katmani.md` §1 [K saha] |
| Ödeme | BNPL görünür (Shop Pay/Klarna/Afterpay) | S19 [K] |
| Sosyal kanıt | FTC sahte yorum/tanıklık kuralı (21 Eki 2024): sahte, AI üretimi, satın alınmış ya da olumluya şartlı yorum, sahte takipçi göstergesi yasak; **AI kişi "aldım" demez** | ftc.gov final rule (pazar-katmani URL) [K] |
| Açıklama | ücretli/ilişkili tanıtım "hemen görünür" açıklanır | S22 [K ikincil] |
| Çizili fiyat | önceki fiyat iyi niyetle, makul süre gerçekten uygulanmış olmalı (FTC aldatıcı fiyat rehberi) | [D] |
| Kargo | belirtilen sürede, süre yoksa 30 günde gönderim (Mail Order Rule) → teslim süresini gerçekçi yaz (`marj_hesap.py` teslim_gun) | [D] |
| Aciliyet | sahte kıtlık/geri sayım "dark pattern" | [D] |

## UK — CMA / DMCC
| Öğe | Karar | Dayanak |
|---|---|---|
| Sosyal kanıt | sahte ya da teşviki gizlenen yorum yasak (DMCC, 6 Nis 2025'ten) | Which? (S42) [K] |
| Fiyat | zorunlu ücretler dahil **tek toplam fiyat** (gizli/sonradan eklenen ücret yasak); VAT dahil | S42 [K]; VAT dahil gösterim [D] |
| Aciliyet | "çok kısa süre mevcut" yalanı kara listede (UCPD Ek I m.7'nin UK karşılığı) | [D] |
| Yaptırım | CMA doğrudan para cezası yetkisi (DMCC) | [D] |
| İade | 14 gün cayma (Consumer Contracts Regulations) | [D] |

## AB — DE · FR · ES (ortak)
| Öğe | Karar | Dayanak |
|---|---|---|
| İndirim | indirim duyurusunda önceki fiyat = **son 30 günün en düşüğü** (Omnibus) | `pazar-katmani.md` §2 (hukuk bürosu özeti) [K ikincil] |
| Aciliyet | sahte "sınırlı süre/stok" UCPD Ek I kara listesi | [D] |
| Yorum | yorumların gerçek alıcıdan geldiği nasıl doğrulanıyor, sayfada yazılır; sahte yorum yasak (Omnibus) | `pazar-katmani.md` §2 [K ikincil] |
| GPSR | listede üretici adı/adresi/iletişim, AB'de sorumlu kişi (üretici AB dışındaysa), ürün tanımlayıcı, görsel, yerel dilde uyarı/güvenlik bilgisi; 13 Ara 2024'ten beri | D25/D26 [K ikincil, tarih resmî metinle teyit edilmedi] |
| AI | gerçekçi AI görüntü/video açıkça belirtilir (AI Yasası m.50, 2 Ağu 2026) | `pazar-katmani.md` §2 [K] |
| İade | 14 gün cayma hakkı | [D] |
| **DE** | PayPal + **faturayla ödeme** (Rechnung/Klarna) görünür; iade kültürü yüksek → iade adımları açık; bedensiz ürün tercih; Impressum | S33–S35 [K]; Impressum [D] |
| **FR** | AI insan görüntüsü → **"Image virtuelle"**, rötuş → "Image retouchée" (influencer yasası; marka hesabında da ihtiyatlı uygula); "soldes" kelimesi yalnız resmî indirim dönemlerinde; sayfa Fransızca | S43, S44 [K]; dil zorunluluğu [D] |
| **ES** | aile/arkadaş tavsiyesi en etkili kaynak (%87) → gerçek alıcı UGC (izinli); Bizum yaygınlığı | S45 [K, 2013 verisi]; Bizum [D] |

## Kaynaklar (S#)
- S3 Ticaret Bakanlığı, E-Ticaretin Görünümü 2025 — https://ticaret.gov.tr/duyurular/turkiyede-e-ticaretin-gorunumu-raporu-yayinlandi-12-05-2026
- S4 Capital, "E-ticarette güven fiyatın önüne geçti" — https://www.capital.com.tr/sirket-panosu/sirket-panosu-haberleri/e-ticarette-guven-fiyatin-onune-gecti
- S5 BKM ara dönem raporu 2025 — https://bkm.com.tr/wp-content/uploads/2025/05/1.-Ara-Donem-Faaliyet-Raporu.pdf
- S9 Ticaret Bakanlığı, sosyal medya etkileyicileri kılavuzu — https://ticaret.gov.tr/haberler/ticaret-bakanligi-sosyal-medya-etkileyicileri-icin-kilavuz-yayimladi
- S10 Ticaret Bakanlığı, yönetmelik değişikliği (1 Ağu 2026) — https://ticaret.gov.tr/haberler/aldaticici-reklam-ve-haksiz-ticari-uygulamalarla-mucadelede-yeni-donem-basliyor
- S11 Sözcü, dijital mecralar araştırması — https://www.sozcu.com.tr/internetten-alisveris-yapan-iki-kisiden-biri-magduriyet-yasiyor-p16236
- S19 Adobe, Cyber Monday 2025 — https://news.adobe.com/news/2025/12/adobe-cyber-monday-hits-record
- S22 MoFo, FTC Disclosures 101 — https://mofo.com/resources/insights/191119-guidance-online-endorsers
- S33 Cross-Border Magazine, Almanya ödeme 2025 — https://cross-border-magazine.com/e-commerce-payment-germany-2025/
- S35 TextilWirtschaft, European Return-O-Meter — https://www.textilwirtschaft.de/business/news/retourenforscher-legen-european-return-o-meter-vor-so-hoch-sind-die-retourenquoten-im-deutschen-online-modehandel-237248
- S42 Which?, DMCC sahte yorum/gizli ücret yasağı — https://www.which.co.uk/news/article/fake-reviews-and-sneaky-fees-banned-under-new-law-campaigned-for-by-which-aLzVp4g0S76D
- S43 Bird & Bird, Fransa influencer yasası 2023 — https://cm.twobirds.com/en/insights/2023/france/promulgation-de-la-loi-visant-a-encadrer-l-influence-commerciale
- S44 info.gouv.fr, Soldes d'hiver 2026 — https://www.info.gouv.fr/actualite/soldes-d-hiver-2026-calendrier-et-dates
- S45 Nielsen (2013), İspanya — https://www.nielsen.com/insights/2013/la-publicidad-con-humor-la-que-mas-cala/
- D25 CMS, GPSR özeti — https://cms.law/en/gbr/legal-updates/the-new-eu-general-product-safety-regulation-what-you-need-to-know
- D26 Avrupa Komisyonu, GPSR soru-cevap — https://webgate.ec.europa.eu/safety/consumers/consumers_safety_gate/obligationsForBusinesses/documents/Q&A.pdf
