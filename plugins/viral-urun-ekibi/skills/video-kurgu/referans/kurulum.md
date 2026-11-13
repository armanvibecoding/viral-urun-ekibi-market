# Kurulum ve öz-test

## Gerekenler
| Araç | macOS | Windows | Kontrol |
|---|---|---|---|
| Python 3.8+ | çoğu Mac'te `python3` var; yoksa `xcode-select --install` | `winget install Python.Python.3.12` → komut `py -3` | `python3 --version` / `py -3 --version` |
| Pillow | `python3 -m pip install pillow` | `py -3 -m pip install pillow` | `python3 -c "import PIL"` |
| ffmpeg | `brew install ffmpeg` ya da `python3 -m pip install imageio-ffmpeg` | `winget install Gyan.FFmpeg` ya da `py -3 -m pip install imageio-ffmpeg` | betikler kendisi bulur |

ffmpeg bulma sırası: PATH → `imageio-ffmpeg` paketi → kurulum talimatıyla durur. `imageio-ffmpeg` ffprobe içermez;
betikler ölçümü `ffmpeg -i` çıktısından yapar. winget sonrası yeni bir terminal aç (PATH yenilenir).

## Ortam raporu
`python3 "<bu becerinin klasörü>/scripts/ffaraclar.py" --font-test font_testi.png` → ffmpeg yolu, ffprobe, seçilen font,
pazar. `font_testi.png`'ye bak: "çğıİöşü ÇĞÖŞÜ / IĞDIR İSTANBUL ŞİŞLİ" doğru mu (kutucuk, noktasız İ yok).
Font bulunamazsa `--font <dosya.ttf>` ile ver (Türkçe harfleri içeren kalın bir font).

## Öz-test (kredi harcamaz)
`python3 "<bu becerinin klasörü>/scripts/kendini_test.py" --klasor kurgu_testi`
3 renkli test klibi + 1 sıçramalı klip üretir; klip_qc temizleri geçirmeli, sıçramalıyı YAKALAMALI (kapı kırılınca
tutuyor mu); Türkçe kanca + CTA + efektle kurgular; süre 12 sn, 1080×1920, −14 LUFS ölçer; `ara_kare_10sn.png` yazar.
Son satırlar `GEÇTİ` olmalı, çıkış kodu 0. Ara kareye gözle bak.

## Windows notları
- Komutlarda `python3` yerine `py -3`; yollarda ters bölü sorun değil, boşluklu yolu tırnakla.
- Konsol Türkçe karakterleri bozuk gösterirse `chcp 65001` (betikler çıktıyı UTF-8'e ayarlar).
- `prompt_uret.py --kopyala` panoya `clip` ile yazar.
