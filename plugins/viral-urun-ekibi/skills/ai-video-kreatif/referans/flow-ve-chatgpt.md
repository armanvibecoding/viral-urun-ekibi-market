# ChatGPT (kareler) ve Google Flow (klipler) — tarayıcı işlemleri

Claude in Chrome bağlıysa bu işleri sen yaparsın; değilse promptları dosyadan kullanıcıya ver, o üretir ve dosyaları
`is/NN/kareler/` ya da `is/NN/klipler/` altına koyar; kontrolü sen yaparsın.
Birden çok tarayıcı bağlıysa önce hangisinin kullanıcının bu bilgisayarı olduğunu doğrula.

## Giriş ve izinler
- ChatGPT ve Google girişleri kullanıcıdadır. Giriş ekranı çıkarsa DUR: "Giriş yap, bitince 'devam' yaz." Şifre isteme.
- Flow ilk dosya yüklemede "kullanım hakları" onayı ister: kullanıcı bir kez kabul eder.
- Tarayıcı eklentisi dosya yükleme izni sorarsa kullanıcı "izin ver" der.

## ChatGPT — başlangıç kareleri (kredi harcamaz, onay gerekmez)
1. Yeni sohbet; ürün fotoğrafı + temiz paket çekimi (Aşama 2) ekle; `promptlar/VNN_S1_gorsel.txt` metnini yapıştır.
2. Sahne 2+ aynı sohbette (CONTINUITY LOCK betikte). Her kare ayrı görsel.
3. Görsel tamamen bitince `scripts/chatgpt_indir.js` (`__AD__` → `VNN_SK.png`) ile indir. Bitmeden indirirsen önceki kare iner.
4. `kare_hazirla.py <İndirilenler>/VNN_SK.png is/NN/kareler/VNN_SK.png --referans <orijinal>` → önizlemeye bak, kabul tablosu.
Hız sınırı gelirse 1 dk bekle, kaldığın kareden devam et.

## Flow — klipler (KREDİ: tavan onayı olmadan başlama)
Adres: `labs.google/fx/tools/flow` (flow.google adresine yönlenebilir). Arayüz değişir: menü adına güvenme, ekrandaki
yükleme/üretim kontrollerini kullan.
- Ayarlar: video 9:16, x1, model **Omni 1.2 Flash** (en düşük kredili image-to-video; pahalısı ayrı onay), **720p**.
  720p = 12 kredi/klip (ekranda da oku). 360p kullanma.
- Akış: yeni proje → kareyi yükle (aşağıda) → karenin menüsünden "Animasyon ekle" / kareden video → `VNN_SK_flow.txt`
  metnini yapıştır → gönder → kredi onay penceresinde "Onayla" (her zaman onayla seçeneğini işaretleme) → bitene kadar bekle.
- **Yükleme (ölçülmüş yöntem):** Flow'un "Yükle" düğmesi dosya girişini tıklama anında oluşturup siliyor; doğrudan
  setFiles hata vermeden boşa düşer. `scripts/flow_yukle.js`: (1) gizli kalıcı `<input type=file id=ek-dosya>` ekle →
  (2) `file_upload` aracıyla dosyayı bu girişe ver → (3) `.cdk-overlay-backdrop` öğelerini kaldır, DataTransfer ile medya
  alanına `dragenter` / `dragover` / `drop` gönder. Kareyi medya alanında ekran görüntüsünde GÖRMEDEN ilerleme.
  Başarısızsa (arayüz değişmiş olabilir) kullanıcıdan tek bir sürükle-bırak iste.
- İndirme: klip → menü → İndir → **720p**. Izgarada "Video yüklenemedi" görünürse klip bozuk değildir: panelden aç, üstten indir.
- İndirilen dosyayı `is/NN/klipler/VNN_SK.mp4` adıyla kaydet; dosya adı sırayı taşımaz, ilk karesine bakarak eşle.
- Her klipten sonra ürün `DURUM.md`'sine harcanan krediyi ekle. Tavanı aşacaksan DUR ve yeni onay iste.

## Klip kabul (video-kurgu aşama 7'ye geçmeden)
`klip_qc.py` çıkış 0 + 4 fps panoda her kare: ürün kendi kendine çalışıyor/büyüyor/renk değiştiriyor mu · sonuç yanlış
yerden/patiden çıkıyor mu · hayvan cins değiştiriyor mu · ışınlanma/kaybolma · fazladan pati. Hata uçtaysa KIRP
(kredi yok). Ortadaysa kök sebebi (kare / prompt / AUDIO satırı) düzelt, tavan içinde yeniden üret. "Yeterince iyi" yok.
