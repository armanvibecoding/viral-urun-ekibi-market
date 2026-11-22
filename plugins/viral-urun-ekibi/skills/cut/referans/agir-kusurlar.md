# Ağır kusurlar ve kök neden sınıfları (direktör ve lider için; jüri bu dosyayı okumaz)

Puan cetveli kaldırıldı: zevki kör jüri (bir sayfalık kendi rubriği), ölçüyü betikler verir. Bu dosya yalnız iki şeyi tutar.

## 1. Ağır kusurlar (jüri puanından bağımsız; biri varsa video teslim edilmez)
| Kusur | Nasıl saptanır |
|---|---|
| Müzik girişi kuralı ihlali (SES-01) | `ses_olc.py --kapi` çıkış 3 (`kapi.py` `ses@V`) |
| Organik videoda ekranda fiyat (ICE-01) | `senaryo_kontrol.py` kural 10; teslimde panoda yazı taraması |
| Uydurma veri: fiyat, yasallık, su geçirmezlik, "herkes soruyor", kurulum süresi, sahte yorum/sayı (IDD-02) | `paket.py iddia-kontrol` (`kapi.py` `iddia@V`); mağaza paketi yoksa direktör yazıları tek tek okur |
| Seçilen ≠ görünen: dokunulan içerik sonraki planda görünmüyor ya da başka içerik çıkıyor | `kurgu_kontrol.py` `telefon` kuralı (sektör eki) |
| Ürün, el ya da yüz ≥ 0,5 sn boyunca biçim değiştiriyor ya da eriyor | `klip_qc.py` + 4 kare/sn pano; kör jüri `gercek` alanı |
| Render hatası: kesim dışı renk sıçraması, son saniyelerde gürültü | `kurgu_kontrol.py --goruntu` çıkış 3 (`kapi.py` `goruntu@V`) |
| Yasa dışı kullanım imâsı; hassas kategoride pazar kartı §6 ihlali, imâ seviyesi 0 ya da 3 (PLT-01) | direktör; `kurgu-ve-yasaklar.md` §8 |
Sağlık ve sonuç dili ağır kusur değildir (IDD-01: bilgi notu). Soru biçimindeki kanca ("Is this legal?") iddia değildir; cevabı uydurmadır.

## 2. Kök neden sınıfları (direktör tek sınıf seçer)
| Sınıf | Belirti | Sonraki adım |
|---|---|---|
| `kurgu` | malzeme iyi; sıra, kesim, yazı ya da ses yerleşimi kötü | kurgu turu (≤ 3 emir) |
| `kare` | başlangıç karesi ya da klip yapay/yanlış | o kare/klip yeniden; kredi tavanı içinde |
| `hikâye` | ilk karede olay yok, işlev anlaşılmıyor, gönderme isteği yok | kurgu turu açılmaz; hikâye bankası |
| `malzeme` | gereken plan/klip yok; süre bütçesi dolmuyor (URE-01) | eksik malzeme + kredi hesabı kullanıcıya |
| `tavan` | 3 tur doldu ya da son iki turda jüri toplamı artışı < 0,3 | dur; kullanıcıya tek soru |
