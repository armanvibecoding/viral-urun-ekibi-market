# Üçüncü taraf bildirimleri (Third-party notices)

Bu eklentinin kendi kodu ve metinleri MIT lisanslıdır (depo kökündeki `LICENSE`). Aşağıdaki klasörler başka bir
projeden alınmıştır ve **kendi lisanslarıyla** dağıtılır; MIT bu klasörleri kapsamaz.

## HyperFrames skills

| Alan | Değer |
|---|---|
| Proje | HyperFrames — HTML'den video üreten hareketli tasarım çatısı |
| Telif sahibi | Copyright 2026 HeyGen, Inc. |
| Lisans | Apache License 2.0 — tam metin: [`licenses/APACHE-2.0.txt`](licenses/APACHE-2.0.txt) (kaynak: https://www.apache.org/licenses/LICENSE-2.0.txt) |
| Kaynak | https://github.com/heygen-com/hyperframes (`skills/` klasörü, etiket `v0.9.19`) |
| npm paketi (CLI) | `hyperframes` — pakete dahil DEĞİL; kullanıcı `npx hyperframes` ile kendi makinesine indirir |
| NOTICE dosyası | Kaynak depoda yok (kontrol: 2026-11-18) |

Alınan klasörler (eklenti içinde `skills/` altında, aynı adlarla):

| Klasör | Kaynak klasör hash'i (skills kilit dosyası) | Değişiklik |
|---|---|---|
| `skills/hyperframes/` | `dde1f2ae6ee90ae398010f82c0e0823d8a049941` | **Yok** — dosyalar olduğu gibi kopyalandı |
| `skills/hyperframes-cli/` | `999df2a15fefd5b190e96238b62cecae5648228b` | **Yok** |
| `skills/hyperframes-registry/` | `ca686aa889dbc82a3f8723df546a31f65ed2956c` | **Yok** |
| `skills/media-use/` | `7c1f1f94d097cd36175113e511f3a0742f35bc5c` | **Yok** |

Her dosyanın SHA-256 imzası: [`licenses/hyperframes.sha256`](licenses/hyperframes.sha256) (222 dosya). "Değişiklik yok"
iddiası buradan sınanır: `cd plugins/viral-urun-ekibi && shasum -a 256 -c licenses/hyperframes.sha256`.
`scripts/anonim_kontrol.sh` de bu imzayı doğrular; tutmayan dosya ihlal sayılır.

İleride bu klasörlerde bir dosya değiştirilirse, Apache-2.0 madde 4(b) gereği o dosyanın başına
"Modified by Viral Ürün Ekibi" notu ve tarih eklenir; bu tablo ve imza dosyası güncellenir.

Bu klasörlerin içinde kendi lisanslarıyla gelen varlıklar (HyperFrames'in dağıttığı biçimde, değişmeden):

- `skills/hyperframes/assets/frame-presets/code-editorial/fonts/` — EB Garamond, Inter, JetBrains Mono (SIL Open Font
  License 1.1; metinler aynı klasörde `OFL-*.txt`).
- `skills/media-use/audio/assets/sfx/*.mp3` — Pixabay Content License (ayrıntı: aynı klasörde `CREDITS.md`).

"HyperFrames" ve "HeyGen" adları sahiplerine aittir; bu eklenti HeyGen tarafından yapılmamış ya da onaylanmamıştır.
