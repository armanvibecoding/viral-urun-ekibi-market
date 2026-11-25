# SFX lisans kaydı (kanca + tipografi paketi)

Kaynak ve lisans ses dosyası başına; hepsi kredisiz, yerel, tekrar üretilebilir. Eşleme tablosu: `sfx_esle.py` başlığı.

| Efekt (olay) | Dosya | Kaynak | Lisans |
|---|---|---|---|
| kesme → whoosh | `lib_whoosh-short.mp3` (= `skills/media-use/audio/assets/sfx/whoosh-short.mp3`) | Pixabay Sound Effects | Pixabay Content License (ticari serbest, atıf gerekmez; `media-use/audio/assets/sfx/CREDITS.md`) |
| yazı girişi → pop | `lib_pop.mp3` | Pixabay | Pixabay Content License |
| kanıt anı → sparkle | `lib_sparkle.mp3` | Pixabay | Pixabay Content License |
| sayaç bitişi → ding | `lib_ping.mp3` | Pixabay | Pixabay Content License |
| şok → darbe | `lib_impact-bass-2.mp3` | Pixabay | Pixabay Content License |
| CTA → bubble | `bubble.wav` | `scripts/hikaye/sfx/sentez.py` (numpy, kendi üretimimiz) | lisans gerekmez |
| riser | ses_tasarla `--riser` (sentetik) | kendi üretimimiz | lisans gerekmez |
| demo müziği | `muzik_sentez.py` çıktısı | kendi üretimimiz (numpy) | lisans gerekmez |

Pixabay Content License tek başına "yeniden dağıtım" yapmaz: dosyalar eklentide zaten paketli (`media-use`); ses efektini bağımsız dosya olarak satmak/yeniden yayımlamak yasak. Videoya gömülü kullanım serbest.
Not: efektler kulakla dinlenmedi; zaman ve seviye `ses_olc.py --kapi` ile ölçülür.
