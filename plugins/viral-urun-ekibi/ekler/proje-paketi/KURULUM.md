# Kurulum — claude.ai veya ChatGPT'de "Viral Ürün Ekibi" Projesi

Kod bilmen gerekmez. 10 dakikada bir Proje açıp talimatı ve bilgi dosyalarını yüklersin; sonra sohbette
"şu ürün viral olur mu", "buna benzer ne var", "şu ürüne 30 video yaz" diye sorarsın.

## 0) Dosyaları bilgisayarına indir
Sana paylaşılan GitHub sayfasında yeşil **Code** düğmesine bas → **Download ZIP**. İnen ZIP'e çift tıkla.
Açılan klasörde şu yola gir: `plugins` → `viral-urun-ekibi` → `ekler` → `proje-paketi`. Aşağıdaki dosyalar orada.
(Sana ZIP yerine doğrudan `proje-paketi` klasörü gönderildiyse bu adımı atla.)

## Bu klasörde ne var
| Dosya | Ne yapacaksın |
|---|---|
| `TALIMAT.md` | İçindeki metnin **tamamını** kopyalayıp Proje'nin talimat alanına yapıştıracaksın (~6.800 karakter). |
| `yuklenecek/` klasörü (9 dosya) | Hepsini Proje'ye **dosya** olarak yükleyeceksin. |

## A) claude.ai (Claude)
1. claude.ai'ye gir → sol menüde **Projects** (Projeler) → **Create project** (Proje oluştur).
2. Ad: `Viral Ürün Ekibi` → oluştur.
3. Sağdaki **Project knowledge** bölümünde **Set project instructions** (Proje talimatı) → `TALIMAT.md` içeriğini yapıştır → kaydet.
4. Aynı bölümde **+ Add content → Upload from device** → `yuklenecek/` klasöründeki 9 dosyanın hepsini seç → yükle.
5. Proje içinde yeni sohbet başlat ve aşağıdaki örnek mesajlardan birini yaz.

## B) ChatGPT
1. chatgpt.com'a gir → sol menüde **Projects** → **New project** (Yeni proje).
2. Ad: `Viral Ürün Ekibi` → oluştur.
3. Proje sayfasında **Instructions** (Talimatlar) → `TALIMAT.md` içeriğini yapıştır → kaydet.
4. **Add files** (Dosya ekle) → `yuklenecek/` klasöründeki 9 dosyayı yükle. (Planına göre proje başına dosya sınırı olabilir; 9 dosya çoğu planda sığar.)
5. Proje içinde yeni sohbet başlat.
- Video kurgusu için ChatGPT'nin kod/dosya özelliği (ffmpeg) kullanılır; klipleri sohbete yüklersin.
- ChatGPT tarayıcı modunda Google Flow'a dosya yükleyemez; Flow adımını sen yaparsın, model promptu verir.

## C) ADHD dostu cevap biçimi
Proje talimatı cevapları zaten ADHD dostu biçimde verdirir (ilk satır yapılacak iş, numaralı adımlar, her mesajda durum,
en fazla 5 öğe). Proje DIŞINDAKİ sohbetlerde de istiyorsan `ADHD-KISISELLESTIRME.md` içindeki metni ChatGPT'de
Kişiselleştirme → Özel talimatlar'a, claude.ai'de Settings → Profile'a yapıştır. Kapatmak için sohbette "normal mod" yaz.

## İlk mesaj örnekleri (kopyala-yapıştır)
1. `Bu ürün viral olur mu? Kedi için köpekbalığı ağzı şeklinde yuva. AliExpress linki: <link>. Benzer ürünleri ve hangi kancanın tuttuğunu da göster.`
2. `Ekte bir Reels ekran görüntüsü var. Ürünü, hesabın marka mı deneyici mi olduğunu ve neden tuttuğunu tablo satırı olarak yaz.`
3. `Evcil hayvan kategorisinde 1 milyonun üstünde izlenen videolarda hangi kancalar tuttu? En iyi 10'u not numarasıyla listele.`
4. `ABD için Noel'e yetişecek, henüz viral olmamış 5 AliExpress ürünü bulmak istiyorum. Hangi arama terimleriyle başlayayım ve daha önce elenenleri tekrar önerme.`
5. `Şu ürüne 30 video planı yaz: <ürün adı + fotoğraf>. Önce mekanizma kartını ve ürün kilidini çıkar, sonra ilk 5 videoyu ver.`

## Sohbetler arası hafıza
Proje sohbetleri birbirini otomatik hatırlamaz. Her cevabın sonunda bir **DURUM** bloğu çıkar (aktif iş, aşama,
kararlar, sıradaki adım). Yeni sohbete geçerken son DURUM bloğunu kopyalayıp ilk mesaja yapıştır: kaldığı yerden devam eder.

## Güncelleme
Bilgi dosyaları yenilendiğinde Proje'deki eski dosyaları sil, `yuklenecek/` klasöründeki yenilerini yükle. Talimat değiştiyse talimat alanını da yeniden yapıştır.

## Bilmen gerekenler
- Para/kredi harcayan her adımda (Flow kredisi, numune, reklam) model senden açık onay ister.
- Model Instagram'da takip/yorum/DM yapmaz; sayı bilmiyorsa "doğrulanamadı" der, uydurmaz.
- Dosyalardaki sayılar gözlem anındaki değerlerdir; karar vermeden önce ürün sayfasını yeniden aç.
