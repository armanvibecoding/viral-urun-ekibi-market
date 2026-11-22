# scripts/sablon.py: yardımcı bilgi kartı ve başlık düzeltici

Ana yöntem DEĞİL (bkz. `uretim-promptlari.md`). Yalnız şu iki durumda kullanılır:
1. Görsel modelin yazdığı Türkçe başlık bozuk (ı/i, İ noktası, ş, ğ, ç, ö, ü) ve 2 denemede düzelmedi.
2. Kutu içeriği ya da karşılaştırma tablosu gibi bilgi kartı gerekiyor ve kullanıcı istedi.

Kaynak: `research/prototip` (2026-11-15). Prototip çıktıları kullanıcı tarafından ana yöntem olarak reddedildi.

## Ne yapar
Ürün fotoğrafı + metin JSON → 1080×1080 PNG. Yazı, ikon ve düzeni PIL basar; Türkçe büyük harf `tr_upper()` ile (i → İ, ı → I). Yalnız Pillow gerekir; internet, numpy, raqm gerekmez.

| Şablon | JSON alanları |
|---|---|
| `hero-temiz` | yok (yazısız, ürün kareyi %82 kaplar) |
| `ana-fayda` | `ust_baslik?`, `baslik` (≤6 kelime), `faydalar[{ikon,metin}]×3` |
| `nasil-kullanilir` | `baslik`, `adimlar[3]` |
| `karsilastirma` | `baslik`, `biz`, `onlar`, `satirlar[{ozellik,biz,onlar}]≤4` |
| `kutu-icerigi` | `baslik`, `parcalar[{ikon,ad,adet}]≤4`, `etiketler[{metin,x,y}]?` |

İkonlar (kodla çizilir): `sicaklik sarj saat kalkan damla yaprak kupa kutu altlik kablo telefon kitapcik tik carpi`. Paletler: `acik`, `koyu` ya da marka renkleriyle dict.

Kurallar: kartlardaki her yazı yalnız Adım 3'te doğrulanmış bilgidir; [DOĞRULA] işaretli bilgi karta yazılmaz. Karşılaştırmada rakip marka adı yok.

## Kullanım (kod aracında)
Fontlar skill içinde: `assets/fonts/` (Anton, Barlow; SIL OFL 1.1, lisans dosyaları yanında). Script yolu `scripts/sablon.py`; font klasörünü kendisi bulur. Skill klasörü başka yere kopyalandıysa `MK_FONT_DIR` ortam değişkeniyle font klasörü verilir.

```
python scripts/sablon.py --tpl kutu-icerigi --urun urun.png --json metin.json --out kart.png --palet acik
python scripts/sablon.py --tpl ana-fayda --urun urun.png --json metin.json --out kart.png --arka-plan sahne.png
python scripts/sablon.py --demo --urun urun.jpg --outdir cikti
```
Python'dan: `im, rapor = render_slot("karsilastirma", "urun.jpg", metin_dict, "acik")`.

Çıkış kodu 0 = bütün ölçümler geçti (yazı ≥ 40 px, kontrast ≥ 4.5). 2 = kontrast, yazı boyu ya da taşma hatası; ayrıntı `*.olcum.json`. `SIGMADI → metni kısalt` gelirse metni kısalt, yazıyı küçültme.

## Sınırlar
- Beyaz ya da açık renk ürün beyaz zeminde eşikle kesilemez; ürünü renkli düz zeminde ya da şeffaf PNG olarak ver.
- Sahne modu (`--arka-plan`) yalnız sentetik gradyanla test edildi.
- `etiketler` koordinatları tahmindir, yanlış noktayı gösterebilir; etiketsiz liste her zaman güvenli.
- ChatGPT sandbox'ındaki Pillow sürümünde test edilmedi (Pillow ≥ 10 gerekir).
