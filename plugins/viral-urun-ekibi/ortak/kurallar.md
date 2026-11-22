# Kural defteri (çalışma zamanı, tek kaynak)

Her kural **bir kez** burada yazılır. Beceri, ajan ve referans dosyaları kuralı yeniden yazmaz; kimliğiyle atıf yapar
(ör. `IDD-01`). Kural değişecekse yalnız bu dosya (ve varsa kapı betiği) değişir. Kapı sütunu doluysa hüküm betiğindir:
metin betikle çelişirse betik kazanır.

## İddia ve dil
| Kimlik | Kural | Kapı (betik → çıkış) |
|---|---|---|
| IDD-01 | **Sağlık ve sonuç dili yasak değildir.** "Ağrıyı geçirir", "tedavi eder", "zayıflatır", "horlamayı keser", hastalık adı, sonuç garantisi yazılabilir; metin elenmez, yumuşatılmaz, belge istenmez. Böyle bir cümle geçen çıktının (senaryo, sayfa, caption, rapor) sonuna tek satır eklenir: `Bilgi notu (kullanıcının sorumluluğu): <hangi cümle>; mevzuat ve platform reklam kuralı kullanıcının işidir.` Ürün seçiminde de eleme sebebi değildir. | `teklif_kontrol.py` (`islem=bilgi-notu` → UYARI, çıkış değişmez) · `ortak/paket.py iddia-kontrol` ve `kurgu_kontrol.py --magaza-paketi` (UYARI `[saglik-sonuc]`) |
| IDD-02 | **Uydurma veri yasaktır** (kalite kuralı, her yüzeyde): sahte yorum ve yıldız, uydurma müşteri/satış/izlenme sayısı ve istatistik, sahte indirim ve kanıtsız çizili fiyat, sahte stok/kıtlık ve geri sayım, belgesiz uzman/doktor/klinik/sertifika onayı, sahte önce-sonra, ürünün yapmadığını gösteren görüntü. Sayı gerekiyorsa yer tutucu (`{GERCEK_YORUM_SAYISI}`); bilinmeyen = `doğrulanamadı`. | `teklif_kontrol.py` (`islem=engel` → 1) · `paket.py iddia-kontrol` (listede olmayan sayı/otorite → 1) · `senaryo_kontrol.py` |
| PLT-01 | **Platform reklam politikası ayrı kapıdır** (IDD-01 bunu kaldırmaz): Meta/TikTok'un yasak ya da kısıtlı kategorisi, izleyicinin kişisel özelliğini söyleyen reklam kancası ("POV: you have back pain" = Meta kişisel özellik kuralı), hesap kapanma riski. Ürün ve kreatif kararında risk kullanıcıya **uyarı** olarak yazılır; reklamı yasak kategoride yol `studio/referans/kurgu-ve-yasaklar.md` §8 (imâ yolu) ve pazar kartı §6'dır. | pazar kartı §6 ihlali jüride ağır kusur · `spy` niş ELE kapısı |

## Ses
| Kimlik | Kural | Kapı (betik → çıkış) |
|---|---|---|
| SES-01 | **Müzik girişi:** video diegetik bir ses olayıyla açılır (kutu tık, telefon titreşimi); müzik 0. saniyede −30 dB'den başlar, 1,5–2 saniyede yatak seviyesine çıkar. Ortada "bir anda açılma" yok; kısık/boğuk yatak + drop'ta tam müzik tarifi bu kusurdur. İhlal ağır kusurdur. | `ses_olc.py --muzik_stem … --kapi` → 3 (başlangıç ≤ −20 dB · rampa 1,5–3,0 sn · 3 sn basamak ≤ +10 dB · açılış olayı ≥ −6 dB); `kapi.py yayin` `ses@V` |
| SES-02 | **Müziksiz teslim yok.** Kaynak Aşama 0'da izni alınmış olmalı (kullanıcının dosyası ya da açık lisanslı parça); telifli şarkı indirilmez. Müzik stem'i ayrı dosya olarak kaydedilir. | `kapi.py yayin`: stem yoksa `ses@V` KALDI |

## İçerik
| Kimlik | Kural | Kapı (betik → çıkış) |
|---|---|---|
| ICE-01 | **Organik videoda ekranda fiyat yok** (her pazar; "$", "TL", indirim yüzdesi, ad+fiyat kartı dahil). Fiyat caption, bio ve ürün sayfasındadır. Reklam kreatifinde ekranda gerçek fiyat olabilir (kökte `"kreatif": "reklam"`). İhlal ağır kusurdur. | `senaryo_kontrol.py` kural 10 → 1 |
| ICE-02 | **ABD hedefinde her videoda görünen en az bir ABD kültür unsuru** (`kultur` alanı; `pazar-katmani.md` §1). | `senaryo_kontrol.py` kural 11 → 1 |
| ICE-03 | **İşlev hissedilmeli:** izleyici ikinci izlemede ürünün ne işe yaradığını çıkarır. Açık söylenemeyen işlev en az iki kanaldan (ses, yazı, görüntü) imâ edilir (`kurgu-ve-yasaklar.md` §8). | kör jüri `anlasilir` alanı |

## Üretim
| Kimlik | Kural | Kapı (betik → çıkış) |
|---|---|---|
| URE-01 | **Bir Flow klibi ≈ 4,03 saniyedir; video süresi = Σ klip aralığı** (+ kredisiz katman). Senaryo klip başına daha uzun süre varsayamaz; süre anlamlı kredisiz katmanla uzatılır, aynı klibin ikinci kırpımı uzatma sayılmaz. | `video-elestirmen` ön-üretim süre bütçesi (kök neden `malzeme`); kontrat K1 |
| URE-02 | **Kural terfisi iki basamaklıdır:** yeni kural önce ürün kontratına (`is/NN/kurgu/KURALLAR.md`) ya da `.ekip/DERSLER.md`'ye girer; eklenti dosyasına ancak aynı kusur anahtarı ikinci kez (başka ürün ya da video) görülünce, üretici dosyada yerinde düzeltilerek girer. | `geri_bildirim_kontrol.py` → 1 (`kapi.py` `defter`) |

