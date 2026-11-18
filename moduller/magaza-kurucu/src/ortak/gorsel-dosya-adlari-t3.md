# TEKNİK EK T3: görseller ve dosya adları

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 258–271. 0.3.0: galeri 8 kare, logo ve favicon kullanıcıdan (eski hâli repo `docs/ESKIDI.md`).

---

T3. Görseller ve dosya adları
Admin › İçerik › Dosyalar'a yüklenenleri `files(first:50, query:"filename:<marka>*") { nodes { ... on MediaImage { id fileStatus image { url width height } } } }` ile bul; hepsi `READY` olmalı.
| Görsel | Dosya adı | Nereye |
| Feed karesi G0 (1:1, ≥ 1500 px, YAZISIZ; 0.4.0) | `<marka>-urun-0.jpg` | ürün medyasında 1. sıra (ana görsel; Google Merchant Center `image_link`) |
| 8 galeri (1:1) | `<marka>-urun-1..8.jpg` | ürün medyası, G0'dan sonra bu sırayla (`productSet.files.originalSource` = dosya URL'si); hiçbir bölümde tekrar kullanılmaz |
| Banner masaüstü 1920×800 | `<marka>-banner-masaustu.jpg` | `index.json` → `e-hero-a.image_1` |
| Banner mobil 1080×1350 | `<marka>-banner-mobil.jpg` | `e-hero-a.image_1_mobile` |
| Logo (varsayılan: `gorseller` adımında üretilen yalnız ikon, şeffaf PNG; ya da kullanıcının dosyası) | `<marka>-logo.png` | ayar `logo` (koyu zemin sürümü varsa `logo_inverse`); dosya yoksa boş kalır, header mağaza adını canlı metin yazar |
| Favicon (isteğe bağlı; kullanıcı yükler; kare, ≥ 32 px) | `<marka>-favicon.png` | ayar `favicon`; dosya yoksa boş kalır |
| S1 fayda kartları (×3) | `<marka>-fayda-1..3.jpg` | ana sayfa `e-fayda3/kartlar/f1..f3/g.image` |
| S2 görsel + fayda listesi | `<marka>-fayda-liste.jpg` | ürün sayfası `e-faydayan/media.image` |
| S3 marka hikâyesi | `<marka>-hikaye.jpg` | ana sayfa `e-hikaye/media.image` |
| S4 Hakkımızda 21:9 | `<marka>-hakkimizda.jpg` | `page.about` → `gorsel/gorsel.image` (sonra bölümü aç) |
| S5 bilgi bandı | `<marka>-bilgi.jpg` | ana sayfa ve ürün sayfası `e-spec/media.image` |
`alt` metni pazar dilinde; banner'larda (masaüstü ve mobil) alt = görseldeki yazı.
S1–S5 görsellerinin zemini konacağı bölümün zemin rengidir (zemin hilesi, `tasarim-dili.md` §4).
