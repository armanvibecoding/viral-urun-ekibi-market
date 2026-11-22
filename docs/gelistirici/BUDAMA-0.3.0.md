# Kural budaması 0.3.0 (ne nereden çıktı, tek kaynağı neresi)

Hiçbir kapı ya da test kaldırılmadı; kural **metinleri** tek kaynağa indi, ayrıntı referans dosyalarına taşındı.
Kapı: `python3 scripts/butce_kontrol.py` (commit öncesi; `--kendini-sina` ile kırma testi).

## Ölçüm (önce → sonra)
| Ölçüm | Önce (0.2.1) | Sonra (0.3.0) |
|---|---|---|
| `ekip-lideri/SKILL.md` | 141 satır · 15 092 bayt | 120 satır · 11 921 bayt |
| `ai-video-kreatif/SKILL.md` | 149 satır · 15 526 bayt | 103 satır · 9 954 bayt |
| `video-kurgu/SKILL.md` | 152 satır · 15 863 bayt | 91 satır · 8 811 bayt |
| `agents/video-elestirmen.md` | 101 satır · 10 550 bayt | 58 satır · 5 022 bayt |
| Eleştirmenin okuduğu cetvel (`puan-cetveli.md`) | 119 satır · 14 297 bayt | çalışma zamanında yok; `agir-kusurlar.md` 26 satır |
| Müzik girişi kuralının tam metni (md dosyası) | 10 dosya | `kurallar.md` (tek kaynak) + izinli 3 (yöntem `ses-tasarimi.md`, tarihçe `dersler.md` ve onun proje paketi kopyası, tek başına yapıştırılan `ekler/chatgpt/video-kurgu.md`) |
| Organikte fiyat kuralının tam metni (md dosyası) | 17 dosya | `kurallar.md` (tek kaynak) + izinli tarihçe ve ChatGPT ekleri; diğerleri `ICE-01` atfı |
| Beceri ve ajan dosyalarında tarihli anlatı | 4 | 0 (kapı) |

## Taşınanlar (içerik aynı, yer değişti)
| Nereden | Nereye |
|---|---|
| `ai-video-kreatif/SKILL.md`: viral referans yöntemi, hikâye bankası biçimi, kare ve klip kuralları, Flow ve kredi, görüntü kaynağı önceliği | `ai-video-kreatif/referans/uretim-kurallari.md` |
| `video-kurgu/SKILL.md`: hızlı kurgu ve ses kuralları | `video-kurgu/referans/kurgu-kurallari.md` |
| `video-kurgu/SKILL.md`: Aşama 8b adımları | `video-kurgu/referans/hareketli-tasarim.md` |
| `video-kurgu/SKILL.md`: plaka, rozet, telefon karosu, "ürün ilk 0,9 sn" (tek ürün serisinden gelen kurallar) | `video-kurgu/referans/sektor/arac-aksesuar.md` |
| `ekip-lideri/SKILL.md` §2b adımları | `ekip-lideri/referans/uctan-uca-hat.md` |
| `ekip-lideri/SKILL.md` hüküm hattı komutları + kalibrasyon adımları | `ekip-lideri/referans/hukum-hatti.md` |
| `ekip-lideri/SKILL.md` §5b ayrıntısı | `ekip-lideri/referans/duzeltme-dongusu.md` (iki basamaklı terfiyle yeniden yazıldı) |
| HyperFrames beceri adları paragrafı | `ekip-lideri/referans/kurulum-kontrol.md` |

## Tek kaynağa inenler (`ortak/kurallar.md`)
IDD-01 sağlık/sonuç dili (bilgi notu) · IDD-02 uydurma veri · PLT-01 platform reklam politikası · SES-01 müzik girişi ·
SES-02 müziksiz teslim yok · ICE-01 organikte fiyat · ICE-02 ABD kültür unsuru · ICE-03 işlev hissedilmeli ·
URE-01 klip süresi · URE-02 kural terfisi.

## Çalışma zamanından çıkanlar
`docs/gelistirici/ESKIDI/README.md` (eski puan cetveli ve `puan_kaydet.py`).

## Davranışı değişen kurallar (budama değil, karar)
- Kural terfisi: "aynı turda eklentiye işle" → önce ürün kontratı, eklentiye ikinci örnekte (URE-02; kapı `geri_bildirim_kontrol.py`).
- Lider öz denetim listesi artık büyümez; kaçan kusur deftere girer.
- "Kurucunun reddettiği GEÇTİ = cetvele çapa satırı" kaldırıldı; jüri yalnız performans kalibrasyonuyla değişir.

## Bilerek dokunulmayanlar
- Referans dosyalarındaki tarihli anlatı cümleleri ve ≥ 10 KB referanslar (kapı UYARI basar; sonraki budama).
- `kurgu_kontrol.py` içindeki sektöre özgü kurallar (araç, telefon, rozet): betikte duruyor, sektör ekine bağlandı; kuralların
  betikte sektör bayrağına ayrılması sonraki iş.
