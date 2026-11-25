# SINAV 07-site · TUR 1 raporu (2026-11-25)

Çıktı: `<referans-kok>/sinav-kosu/07-site/tur1/` · koşucu çıkışı 3 (KALDI yok; olculemedi var).

## Başlık ve kanca
- a-kolay (US): "Pour something hot. Watch the black disappear." · kanca: "Hot liquid goes in. The surface turns clear. The pattern appears."
- b-zor (TR): "Koltuktaki tüy sayfaya taşınsın." · kanca: "Ruloyu koltukta gezdirirsin. Tüy ve toz sayfaya yapışır." (problem önce, çözüm sonra)
- c-tuzak (DE): "Schultern zurück. Ganz leicht erinnert." · kanca: "Dieselbe Person, ein Bild: erst ohne Band, dann mit Band." (imâ yolu, sağlık/sonuç iddiası yok)

## Kapı tabloları (SONUC.md'den aynen)

## a-kolay (Isıyla renk değiştiren kupa · US)

| Kapı | Durum | Ayrıntı |
|---|---|---|
| dosyalar | GEÇTİ | tamam |
| iddia_kontrol | GEÇTİ | çıkış 0 iddia kontrolü: 30 satır okundu, 0 ihlal, 0 bilgi notu → GEÇTİ |
| yasakli | GEÇTİ | yasaklı çıktı yok |
| hiz_cwv | olculemedi | ölçen betik depoda yok — probe `hiz`: mobil hız/Core Web Vitals (canlı mağaza + PageSpeed gerekir) |
| erisim_wcag | olculemedi | ölçen betik depoda yok — probe `erisim`: WCAG 2.2 AA (canlı sayfa + araç gerekir) |
| arama_merchant | olculemedi | ölçen betik depoda yok — probe `arama`: arama/Merchant/yapay zekâ araması (canlı sayfa gerekir) |
| donusum_kullanilabilirlik | olculemedi | ölçen betik depoda yok — shopper `donusum`: müşteri gözü denetimi (ajan yargısı; betik yok) |
| juri | olculemedi | referans yuvası dolu değil: pazar US için 0/3 çözülen kare panosu (referanslar.tsv'yi doldur; --referans-kok verilmedi) |

## b-zor (Tüy toplayıcı rulo · TR)

| Kapı | Durum | Ayrıntı |
|---|---|---|
| dosyalar | GEÇTİ | tamam |
| iddia_kontrol | GEÇTİ | çıkış 0 iddia kontrolü: 29 satır okundu, 0 ihlal, 0 bilgi notu → GEÇTİ |
| yasakli | GEÇTİ | yasaklı çıktı yok |
| hiz_cwv | olculemedi | ölçen betik depoda yok — probe `hiz`: mobil hız/Core Web Vitals (canlı mağaza + PageSpeed gerekir) |
| erisim_wcag | olculemedi | ölçen betik depoda yok — probe `erisim`: WCAG 2.2 AA (canlı sayfa + araç gerekir) |
| arama_merchant | olculemedi | ölçen betik depoda yok — probe `arama`: arama/Merchant/yapay zekâ araması (canlı sayfa gerekir) |
| donusum_kullanilabilirlik | olculemedi | ölçen betik depoda yok — shopper `donusum`: müşteri gözü denetimi (ajan yargısı; betik yok) |
| juri | olculemedi | referans yuvası dolu değil: pazar TR için 0/3 çözülen kare panosu (referanslar.tsv'yi doldur; --referans-kok verilmedi) |

## c-tuzak (Duruş düzeltici · DE)

| Kapı | Durum | Ayrıntı |
|---|---|---|
| dosyalar | GEÇTİ | tamam |
| iddia_kontrol | GEÇTİ | çıkış 0 iddia kontrolü: 31 satır okundu, 0 ihlal, 0 bilgi notu → GEÇTİ |
| yasakli | GEÇTİ | yasaklı çıktı yok |
| hiz_cwv | olculemedi | ölçen betik depoda yok — probe `hiz`: mobil hız/Core Web Vitals (canlı mağaza + PageSpeed gerekir) |
| erisim_wcag | olculemedi | ölçen betik depoda yok — probe `erisim`: WCAG 2.2 AA (canlı sayfa + araç gerekir) |
| arama_merchant | olculemedi | ölçen betik depoda yok — probe `arama`: arama/Merchant/yapay zekâ araması (canlı sayfa gerekir) |
| donusum_kullanilabilirlik | olculemedi | ölçen betik depoda yok — shopper `donusum`: müşteri gözü denetimi (ajan yargısı; betik yok) |
| juri | olculemedi | referans yuvası dolu değil: pazar DE için 0/3 çözülen kare panosu (referanslar.tsv'yi doldur; --referans-kok verilmedi) |

## Referans yuvaları

`referanslar.tsv`: 0 satır, 0 tanesinde `kare_panosu_yolu` dolu.
Jüri en az 3 pazar-uyumlu, tür-uyumlu, yolu çözülen referans ister; eksikse kapı `olculemedi` kalır.


## Açık sorunlar
- a-kolay iddia_kontrol ilk koşuda KALDI (SSS'teki "350 ml, as stated on the packaging." onaylı listede yoktu); `onayli_metinler.iddialar`'a "350 ml" eklenince 2. denemede GEÇTİ (2 deneme hakkı kullanıldı).
- Paket şeması `urun.fiyat` ve `gorseller` (en az 1) zorunlu: fiyat 0, görsel "yok-yer-tutucu.jpg" yer tutucu yazıldı; sitede fiyat satırı yok. Şema/ürün gerçeğiyle uyumsuz, ayrı iş.
- Marka adları (Reveal Mug, Çekim Rulo, Aufrecht Band) vakada yok, tarafımdan uydurma jenerik ad.
- Jüri: referans yuvası boş (US/TR/DE 0/3), koşulmadı. hiz/erisim/arama/donusum betiksiz: olculemedi.
- Ekran görüntüleri düz renk bloklu; gerçek ürün görseli yok. Chrome headless çalıştı (her vaka 4 png + kaynak html).
- DE metni yerli-kontrolden geçmedi (kendi yazımım); "Ist das ein medizinisches Produkt?" SSS'si savunmacı, sınanmalı.
