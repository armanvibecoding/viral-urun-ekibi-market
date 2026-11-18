# Mağaza ekibi: yollar, çıktılar, eksik dosya kuralı

Ne zaman okunur: mağaza kolundaki bir ekip üyesi (ajan) işe başlarken, bir kez.

## 1. Kim yönetir
Tek lider `ekip-lideri` becerisidir. Brief ondan gelir, rapor ona döner. Kullanıcıya doğrudan soru sormazsın; sorunu raporun en üstüne tek satır yazarsın. Kullanıcıya unvanınla anılırsın ("Brand Strategist (Elif) konumlamayı çıkardı").

## 2. Yollar
| Ne | Yer |
|---|---|
| Ürünün mağaza işi (girdi ve çıktılar) | `is/NN-urun/magaza/` (proje klasörü) |
| Üretim turu | `is/NN-urun/magaza/tur-<n>/` (`istem/`, `aday/`, `secili/`, `pano/`) |
| Köprü dosyaları | `is/NN-urun/magaza/urun-paketi.json`, `magaza-paketi.json`, `video-paketi.json` |
| Aşama kuralları, şablonlar, betikler | `${CLAUDE_PLUGIN_ROOT}/skills/magaza-kurucu/<aşama>/` (`references/`, `scripts/`, `assets/`) |
| Site denetimi maddeleri (eşikler ve kaynakları) | `${CLAUDE_PLUGIN_ROOT}/skills/magaza-kurucu/shopify-kurulum/references/site-denetimi.md` |
| Görsel kabul kontrolü | `${CLAUDE_PLUGIN_ROOT}/skills/magaza-kurucu/gorseller/references/kabul-kontrolu.md` |
| Tasarım ilkeleri (yasak varsayılanlar) | `${CLAUDE_PLUGIN_ROOT}/ortak/tasarim-ethos.md` |
| Proje araştırma kütüphanesi (isteğe bağlı) | `is/arastirma/` |

## 3. `is/arastirma/` nedir, yoksa ne olur
Bazı ekip dosyaları `is/arastirma/kutuphane/ANALIZ.md`, `KANIT.md`, `plan/` gibi dosyalara atıf yapar. Bunlar başarılı mağazaların ölçüm kütüphanesi ve çalışma planlarıdır; **eklentiyle gelmez** (başka markaların ekran görüntüleri telif nedeniyle dağıtılmaz), kullanıcının projesinde varsa okunur.
- Dosya varsa: oku, sayıyı oradan al.
- Dosya yoksa: ekip dosyanın içinde yazan ölçülmüş sayıları ve §2'deki eklenti dosyalarını kullan; raporun başına "kütüphane yok: gömülü sayılar kullanıldı" yaz. Sayı ya da kaynak uydurma. "Önce oku" listesindeki eksik dosya işi durdurmaz.
- "KANIT x.y" numaraları o kütüphanedeki kanıt tablosunun satırlarıdır; dosya yoksa numarayı aynen aktar, kaynağı `site-denetimi.md`'den göster.

## 4. Kurallar (hepsi için)
- Para ya da kullanıcı hesabı harcayan iş (ChatGPT görsel üretimi, Shopify yazımı) yalnız liderin brief'inde "kullanıcı onayladı" satırı varsa yapılır.
- Üreten kendini puanlamaz: zevk puanı `kor-elestirmen`, ölçüm kapıları denetçilerindir.
- Tek örnekten kalıcı kural çıkmaz: eklentiye işlenecek ders 2+ görselde ya da 2+ üründe görülmüş olmalı.
- Başka markaların görselleri yalnız iç analiz içindir; pakete ve depoya girmez.
- Tema paketi yoksa mağaza temasız modda kurulur (`skills/magaza-kurucu/shopify-kurulum/references/ekip-koprusu.md` §3); tema gerektiren maddeyi "ölçülmedi (temasız mod)" diye yaz.
