---
name: kesfet-urun-avi
description: Instagram Reels/Keşfet'te viral ürün videolarını izler; izlenme, beğeni, paylaşım, satıcı profili ve marka skoruyla ayıklar; her biri farklı ürünleri tabloya ve Excel'e kaydeder. Mac'te iPhone Yansıtma ile, Windows'ta ve her yerde Chrome'da instagram.com ile çalışır. "Instagram'dan ürün bul", "Keşfet'ten viral ürün çıkar", "Reels'te ürün avı", "insta taraması yap", "viral ürün listesi" isteklerinde çağır.
---

# Instagram keşif ürün avı

Amaç: tek ürün mağazası / dropshipping için güçlü ürün adaylarını Instagram'da bulmak ve her biri
**farklı** ürün olan, kanıtı yazılı bir liste + Excel teslim etmek. Kullanıcı kod bilmeyebilir: komutları
sen çalıştırırsın, ona yalnız sonuç ve gerekirse tek bir yapması gereken şey söylersin.

## Instagram kuralları (pazarlıksız)
- Yalnız kaydır, izle, profile bak, bio linkindeki siteye salt-okuma bak.
- Takip, yorum, DM, kaydetme, paylaşma, satın alma, "ilgilenmiyorum / ilgimi çekmiyor" YOK. Bildirime dokunma.
- Beğeni yalnız kullanıcı açıkça isterse: önce `.ekip/KARARLAR.md`'ye `- YYYY-AA-GG | instagram | beğeni izni: evet` yaz
  (iPhone `begen.sh` bu satır olmadan çalışmaz).
- Giriş/şifre kullanıcıdadır; giriş ekranı çıkarsa kullanıcıdan girmesini iste, bekle.

## 1. Başla (her oturumda)
1. Hafızayı oku: `.ekip/DURUM.md`, `.ekip/KARARLAR.md` (pazar, ürün yasakları, hedef adet), `is/kesfet/DURUM.md` son 10 satır.
2. Dosyaları hazırla: `sh "${CLAUDE_SKILL_DIR}/scripts/baslat.sh"` (var olana dokunmaz).
3. Modu seç — **kullanıcıya sorma**: `sh "${CLAUDE_SKILL_DIR}/scripts/platform.sh"` → `iphone` | `tarayici`.
   Kullanıcı açıkça "Chrome'la yap" dediyse `tarayici`.
4. `iphone` ise `${CLAUDE_SKILL_DIR}/referans/iphone.md`'yi oku. `.ekip/arac/tikla` yoksa
   `sh "${CLAUDE_SKILL_DIR}/scripts/kur.sh"`; sonra her oturumda `sh .ekip/arac/kalibre.sh` ve ip.png'yi aç.
   Kurulum/izin/pencere hatası çözülemiyorsa sebebi kullanıcıya söyle ve `tarayici` moduna geç.
5. `tarayici` ise `${CLAUDE_SKILL_DIR}/referans/tarayici.md`'yi oku.
6. Hedefi belirle: kullanıcı adet/pazar/kategori dediyse onu, demediyse 20 yeni ürün; KARARLAR.md'ye yaz.

## 2. Tarama döngüsü (bir video = bir aday)
Her aday için şu bitiş durumuna ulaş:
- **Gördün:** videodan en az bir kare/kontakt sayfası (iPhone: `izle.sh AD`; tarayıcı: ekran görüntüleri).
  Görmediğin ürünü yazma.
- **Okudun:** izlenme, beğeni, paylaşım, hesap; profil: takipçi, gönderi, bio linki. Görünmeyen sayı = "görünmüyor".
- **Ayıkladın:** `${CLAUDE_SKILL_DIR}/referans/urun-tanima.md` ölçütleriyle Al / Atla / Ele-ama-not.
- **Tekrar değil:** `sh "${CLAUDE_SKILL_DIR}/scripts/kontrol.sh" @hesap "ayırt edici kelime"` → `YENİ` değilse
  listeye ekleme; aynı ürün başka satıcıdaysa `is/kesfet/rakipler.md`'ye satıcıyı yaz.
- **Kaydettin:** `sh "${CLAUDE_SKILL_DIR}/scripts/ekle.sh" "ürün|@hesap|izlenme|beğeni|profil notu|site / fiyat|KARAR|neden"`.
  KARAR: AL / AL (sezonluk) / YEDEK / ELE. Neden ürüne özgü olmalı (kim alır, acı/wow, gösterilebilirlik, risk).

Marka skoru: AL adayının profilinde Reels ızgarasına bak, `${CLAUDE_PLUGIN_ROOT}/ortak/marka-skoru.md`
rubriğiyle puanla, `is/kesfet/marka-skorlari.md`'ye satır ekle (DROP-MARKA / GERÇEK-MARKA / DENEYİCİ).
Skoru ≥7 hesabın çok izlenen videosu için `${CLAUDE_SKILL_DIR}/referans/kreatif-not-sablonu.md` ile
`is/kesfet/kreatif/notlar/`'a not yaz — kullanıcı kreatif analiz istiyorsa ya da hedefte varsa.

Akış reklama veya tek kategoriye kayarsa Keşfet'e dön/yenile. Aynı aileden 3. ürünü eklemeden önce düşün:
liste çeşitli olmalı.

## 3. Hafıza protokolü (bağlam unutmasın diye — atlanmaz)
| Ne zaman | Ne yazılır |
|---|---|
| Her eklenen ürün | `is/kesfet/urunler.md` (`ekle.sh` yazar) — tek kaynak; sohbete tablo dökme |
| Her 10 ürün ve her tur sonu | `python3 "${CLAUDE_SKILL_DIR}/scripts/excel_yap.py"` → `is/kesfet/kesfet-urunler.xlsx` (çıktıda `TAMAM` görmelisin) |
| Her tur sonu | `is/kesfet/DURUM.md`'ye ekle: `- tarih saat | mod | +N ürün (AL/YEDEK/ELE) | nerede kaldın (Keşfet/Reels, son hesap)` |
| Her tur sonu | `.ekip/DURUM.md`'yi üzerine yaz (≤40 satır): aktif iş, toplam, **Sıradaki adım**, açık sorular |
| Kullanıcı karar verince | Hemen `.ekip/KARARLAR.md`'ye ekle (pazar, kategori yasağı, beğeni izni, hedef adet) |
| Yeni ölçülmüş tuzak/ders | `.ekip/DERSLER.md`'ye `- konu: ders (kanıt dosyası)` |

Tur = yaklaşık 10 aday ya da kesinti (telefon kullanımda, giriş istendi, kısıt). Kesintide önce yaz, sonra dur.
Yeni oturumda "devam et" = DURUM.md'deki "Sıradaki adım"dan sürdür; listeyi baştan tarama.

## 4. Ekip ve bağlam
- Ekran kontrolü (iPhone/Chrome) alt ajana verilmez; tarama bu oturumda yapılır. Bağlamı korumak için
  kareleri ve uzun notları dosyaya yaz, sohbete her turda 3–5 satır özet ver.
- `is/kesfet/kreatif/notlar/`'da en az 10 MARKA notu birikince desen çıkarımı için `kreatif-analisti`
  ajanını çağır (brief: okunacak klasör, yazılacak dosyalar, bilinen/elenen desenler). Sonucundan 2 desenin
  not numaralarını açıp gerçekten orada mı bak; tutmuyorsa çıktıyı "şüpheli" say.

## 5. Bitiş
Hedef adede ulaşınca ya da kullanıcı durdurunca: `excel_yap.py` → çıktıda `TAMAM` ve sayılar →
hafıza dosyalarını güncelle → kullanıcıya en fazla 10 satır: toplam ve AL/YEDEK/ELE dağılımı, en güçlü
5 ürün (izlenme + paylaşım + marka skoru ile), sezon aciliyeti, Excel yolu. Doğrulayamadığın sayıyı
"doğrulanamadı" diye yaz; tahmini ölçüm gibi sunma.

## Dosyalar
| Yol | İş |
|---|---|
| `${CLAUDE_SKILL_DIR}/scripts/baslat.sh` · `platform.sh` | Dosyaları kurar · modu seçer |
| `${CLAUDE_SKILL_DIR}/scripts/kontrol.sh` · `ekle.sh` | Tekrar kontrolü · numaralı satır ekleme (8 alan, hesap tekrarını reddeder) |
| `${CLAUDE_SKILL_DIR}/scripts/excel_yap.py` | md → Excel (Ürünler / Marka Skorları / Rakip & Notlar / Özet); openpyxl gerekir |
| `${CLAUDE_SKILL_DIR}/scripts/kur.sh` | Yalnız macOS: Swift araçlarını derler → `.ekip/arac/` |
| `${CLAUDE_SKILL_DIR}/referans/` | iphone.md · tarayici.md · urun-tanima.md · kreatif-not-sablonu.md |

Python komutu: macOS/Linux `python3`, Windows `py -3` (Windows'ta `python3` yazmak Microsoft Store'u açar). `sh` komutları Windows'ta Git Bash ile çalışır.
openpyxl yoksa betiğin yazdığı kurulum komutunu çalıştır (ücretsiz paket), sonra tekrar dene.
