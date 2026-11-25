# ChatGPT (kareler) ve Google Flow (klipler) — tarayıcı işlemleri

Claude in Chrome bağlıysa bu işleri sen yaparsın; değilse promptları dosyadan kullanıcıya ver, o üretir ve dosyaları
`is/NN/kareler/` ya da `is/NN/klipler/` altına koyar; kontrolü sen yaparsın.
Birden çok tarayıcı bağlıysa önce hangisinin kullanıcının bu bilgisayarı olduğunu doğrula.

## Giriş ve izinler (Aşama 0'da bir kez sorulur)
- ChatGPT ve Google girişleri kullanıcıdadır. Giriş ekranı çıkarsa DUR: "Giriş yap, bitince 'devam' yaz." Şifre isteme.
- Flow ilk dosya yüklemede "kullanım hakları" onayı ister: kullanıcı bir kez kabul eder.
- Tarayıcı eklentisi dosya yükleme izni, Chrome çoklu indirme izni sorarsa kullanıcı bir kez "izin ver" der.

## ChatGPT — başlangıç kareleri (kredi harcamaz, onay gerekmez)
1. Yeni sohbet; ürün fotoğrafı + temiz paket çekimi (Aşama 2) ekle; `promptlar/VNN_S1_gorsel.txt` metnini yapıştır.
2. Sahne 2+ aynı sohbette (CONTINUITY LOCK betikte). Her kare ayrı görsel.
3. Görsel tamamen bitince `scripts/chatgpt_indir.js` (`__AD__` → `VNN_SK.png`) ile indir. Bitmeden indirirsen önceki kare iner.
4. `kare_hazirla.py <İndirilenler>/VNN_SK.png is/NN/kareler/VNN_SK.png --referans <orijinal>` → önizlemeye bak, kabul tablosu.
Hız sınırı gelirse 1 dk bekle, kaldığın kareden devam et.

### Toplu prompt (seri üretim, ölçülmüş yöntem)
Uzun metin yapıştırılınca ChatGPT onu ek dosyaya çevirir; promptlar tek tek ve sayfanın içinden gönderilir:
1. Tüm promptlar tek JSON'a (`[{"ad": "C1_k2", "prompt": "..."}]`) → panoya al (Mac: `pbcopy < promptlar.json`; Windows: PowerShell `Get-Content -Raw -Encoding utf8 promptlar.json | Set-Clipboard`; araç yoksa dosyayı aç, içeriği elle kopyala).
2. Sayfada capture-phase `paste` dinleyicisi kur: panodaki metni `localStorage`'a yazar ve `preventDefault()` ile
   kutuya yapışmasını engeller; kullanıcı ya da `computer` aracı bir kez Cmd+V yapar.
3. Her gönderim: kutuya odaklan → `document.execCommand('insertText', false, prompt)` → `button[aria-label="Gönder"]`
   tıkla (arayüz dili Türkçe değilse etiketi ekrandan oku: "Send prompt"). Üretim sürerken `button[aria-label="Durdur"]`
   vardır; yok olunca görsel bitmiştir.
4. İndirme: sayfadaki son büyük görsel (`naturalWidth >= 900`, `src` `blob:` ile başlar) → `fetch` + `<a download>` ile `ad`.png.
- Sayfa CSP'si iç içe `eval`'e izin vermez: yardımcı fonksiyonları `window.<ad> = ...` ile doğrudan tanımla.
- Üç sekmede paralel üretim çalışıyor (her sekme ayrı sohbet, ayrı localStorage anahtarı).

### "Sonra" karesi (k3 — k2 ile aynı kadraj, yalnız ekran içeriği farklı)
"Aynı fotoğraf, yalnız ekranı değiştir" denince ChatGPT kadrajı ya da plakayı da değiştirebiliyor (ölçüldü: 3 araçtan 2'sinde).
Yöntem: k3'ü üret (kadraj kaysa da olur) → ekran merkezini ve yarıçapını k2'de ölç →
`python3 scripts/ekran_tasi.py k2.png k3.png CX CY R k3_hizali.png` (ekran + parıltıyı yumuşak dairesel maskeyle k2'ye
taşır; küçük kaymayı ekran çevresinde blok eşlemeyle bulur). Çıkış 1 = çevre eşleşmedi: `kare_hazirla.py --yan-yana`
panosuyla bak, gerekirse k3'ü yeniden üret. Flow'a `k3_hizali.png` verilir.

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

## Klip kabul (cut aşama 7'ye geçmeden)
`klip_qc.py` çıkış 0 + 4 fps panoda her kare: ürün kendi kendine çalışıyor/büyüyor/renk değiştiriyor mu · sonuç yanlış
yerden/patiden çıkıyor mu · hayvan cins değiştiriyor mu · ışınlanma/kaybolma · fazladan pati. Hata uçtaysa KIRP
(kredi yok). Ortadaysa kök sebebi (kare / prompt / AUDIO satırı) düzelt, tavan içinde yeniden üret. "Yeterince iyi" yok.

## Flow ajanı ile üretim (ölçülmüş dersler)
- Ajan klibi dosya ADIYLA değil, mesaja EKLENMİŞ görsellerle eşler; ek yoksa son yüklenenleri alır. Kareleri sohbet kutusuna sürükle-bırakla ekle ve promptta her klibin görselini İÇERİĞİYLE tarif et ("genç ayakta, amblem siyah" gibi). Ek sırasına güvenme; ters görünebilir.
- **Politika reddi:** Flow istemi politika gerekçesiyle reddederse istem yeniden ifade edilmez (kelime oyunuyla filtreyi
  aşmaya çalışmak hesap riski). Kontrata (KURALLAR.md) üretimden ÖNCE her riskli klip için bir "politika yedeği" satırı yazılır
  (daha masum sahne, aynı hikâye işlevi); ret gelirse yalnız o yedek denenir, o da reddedilirse klip kurgudan çıkar ve lidere yazılır.
- Onay kartı 1–2 dk içinde onaylanmazsa üretim iptal olur (kredi düşmez): "Tekrar dene" de ve hemen onayla.
- Flow içindeki görsel düzenleme (Nano Banana) 0 kredi; kare düzeltmesi orada bedava yapılabilir.
- Model "SCREEN LOCK"a rağmen ekran içeriğini değiştirebilir ya da ikinci (hayalet) bir ürün çizebilir: 4 fps panoyla bul, değişen ucu kırp ya da tavan içinde yeniden üret. Sabit kamerada hayalet nesne, ilk karenin temiz bölgesiyle (çevreye göre parlaklık eşlemeli, geniş yumuşak kenar) silinir.
- İndirme: "Videolar" görünümünde karo → sağ tık → İndir → 720p (Orijinal boyut, ücretsiz). 1080p/4K yükseltmedir.

## Seri üretim — örnek klip tablosu (30 video, 9 özne)
| Klip | Ne | Yeniden kullanım |
|---|---|---|
| k1 | kahraman giriş (özneye özgü hareket: egzoz, kapı, varış) | yalnız o özne |
| k2 | önce: yakın plan, ekranda stok içerik | yalnız o özne |
| k3 | sonra: k2 ile AYNI kadraj, içerik 1 (`ekran_tasi.py`) | yalnız o özne |
| k4 | içerik 2, başka açı | yalnız o özne |
| k5 | geniş kimlik planı (ortam + özne) | yalnız o özne |
| O1–O8 | ortak: telefon dokunuşu (2 el/kılıf varyantı), kutu açılışı, eldivenli/çıplak elde ürün, söküm makro (2 renk), konnektör | her biri ≤ 4 video, ardışık değil |
Kredi: 9 özne × 5 + 8 ortak = 53 klip × 12 = 636 kredi (+ yeniden deneme payı) → 30 video. Her özne 3 videoda, ardışık değil;
`senaryolar.json`'da `giris`, `ortam`, `ozne` alanları doldurulur, `senaryo_kontrol.py` tekrarları yakalar.
