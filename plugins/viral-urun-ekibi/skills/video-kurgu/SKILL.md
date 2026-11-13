---
name: video-kurgu
description: AI klipleri (Flow/Omni ya da çekim) ffmpeg ile kurgular — klip kalite kontrolü (sıçrama ölçümü + 4 fps pano), kırpma, ekran içeriği bindirme, ekran üstü kanca/CTA yazısı, efekt ve −14 LUFS ses, kontrol karesi, caption ve teslim paketi. "Klipleri kurgula", "videoyu birleştir", "yazı ekle", "ses ekle", "klipleri kontrol et", "kurgu yap", "teslim et", "final videoyu çıkar" isteklerinde çağır.
---

# Video kurgu

Klipten teslim edilebilir MP4'e: 1080×1920, 30 fps, H.264 + AAC, +faststart, 8–15 sn. Kullanıcıyla dil **Türkçe**;
ekran yazısı ve CTA **pazarın dilinde** (`.ekip/KARARLAR.md`'deki son `| pazar |` satırı; betik kendisi okur).
Betikler `${CLAUDE_SKILL_DIR}/scripts/` altında; Python komutu: macOS/Linux `python3`, Windows `py -3` (Windows'ta `python3` yazmak Microsoft Store'u açar).
Gereken: Python 3.8+, Pillow, ffmpeg (PATH ya da `imageio-ffmpeg` paketi). Kurulum: `${CLAUDE_SKILL_DIR}/referans/kurulum.md`.
İlk kullanımda öz-testi koştur (kredi harcamaz): `python3 "${CLAUDE_SKILL_DIR}/scripts/kendini_test.py" --klasor kurgu_testi`
→ son satırlar GEÇTİ ve `ara_kare_10sn.png`'de Türkçe harfler doğru olmalı.

## Hafıza protokolü
- Aşama kaydı `is/NN-urun-adi/DURUM.md`: aşama 7 (klip kontrolü), 8 (kurgu), 9 (teslim); video başına QC/Kurgu/Teslim
  sütunları. Her video bitince güncelle; `.ekip/DURUM.md` "Sıradaki adım"ı yaz.
- Kırpma kararları, `qc_izin` istisnaları ve gerekçeleri `is/NN/kurgu/VNN.json` içinde kalır (ayar dosyası = kayıt).
- Tekrarlanan klip hatası (aynı kök sebep ikinci kez) `.ekip/DERSLER.md`'ye bir satır.
- Oturum kesilirse: DURUM'daki ilk "—" hücresinden devam; var olan `kurgu/VNN.mp4` yeniden üretilmez.

## Aşama 7 — Klip kontrolü (kurgudan ÖNCE, atlanamaz)
```
python3 "${CLAUDE_SKILL_DIR}/scripts/klip_qc.py" is/NN/klipler/V01_S*.mp4 --pano
```
- Çıkış 1 = sıçrama (ışınlanma, nesne kaybı, gizli kesme) ya da yükseklik < 1280 (720p altı) → kurguya geçme.
- Ölçüm yavaş dönüşümü yakalamaz: her klibin `_qc.jpg` panosunu (saniyede 4 kare) **her karesiyle** aç ve bak:
  ürün kendi kendine çalışıyor/büyüyor/renk değiştiriyor mu · sonuç yanlış yerden ya da el/patiden çıkıyor mu ·
  hayvan/kişi cins, renk, yüz değiştiriyor mu · fazladan uzuv · ürün yazısı bozuluyor mu. 4 fps altına inme.
- Hata klibin başında/sonundaysa → kırp (ayar dosyasında saniye aralığı). Ortadaysa → kök sebebi (kare / prompt /
  AUDIO satırı) yaz, `ai-video-kreatif` aşama 6'ya dön (kredi tavanı içinde). "Yeterince iyi" yok.
- Ölçüm işaretledi ama panoda doğal hareket görüyorsan (hızlı kafa çevirme) plan numarasını `qc_izin`'e ekle ve gerekçeyi yaz.

## Ekran / yazı içeren ürünler (gerekirse, kurgudan önce)
AI ekran, yazı, logo ve ince geometriyi bozar; bu içerik kurguda bindirilir:
`ekran_bindir.py klip --kareler` ile ilk/son kareyi çıkar, ekran merkezini ve iç genişliğini ölç, sonra
`ekran_bindir.py klip anim.mp4 cikti.mp4 --x0 --y0 --d0 [--x1 --y1 --d1]`. Ardından çıktıya tekrar `klip_qc.py --pano`:
her karede bindirme ekranın içinde mi. Yöntem ve ayarlar: `${CLAUDE_SKILL_DIR}/referans/ekran-bindirme.md`.

## Aşama 8 — Kurgu
1. `is/NN/kurgu/VNN.json` ayar dosyasını yaz (alanlar `kurgu.py` başındaki açıklamada ve `referans/kurgu-kurallari.md`).
2. Koştur: `python3 "${CLAUDE_SKILL_DIR}/scripts/kurgu.py" is/NN/kurgu/VNN.json --proje .`
   Betik kapıları kendisi uygular (720p altı, sıçrama); geçmezse kurgu yapılmaz.
3. Çıktı satırını oku: süre 8–15 sn, 1080×1920, −14 ±1 LUFS. Değilse düzelt.
4. `VNN_kontrol.jpg`'ye bak (her planın ortası + son kare): yazı okunuyor mu, ürünü/çıkış noktasını örtüyor mu,
   CTA son ≥ 3 sn'de ve kancanın hemen altında mı. Örtüyorsa `yazi_konum` ya da `kanca_gizle` ile yeniden koştur.
Kurallar (ayrıntı `referans/kurgu-kurallari.md`):
- Kanca beyaz kalın, siyah konturlu, 1–3 satır; konum "oto" en boş bandı seçer (alt %20 ve sağ %15 hariç).
- Emoji videoya girmez (betik çıkarır, uyarır) → caption'a taşı. Türkçe büyük harfi elle yaz; kodda `upper()` kullanma.
- Font: betik Türkçe harfleri (çğıİöşü) ölçerek seçer; ilk kurulumda font test karesine bak.
- Ses: klibin gerçek sesi + gerekirse kullanıcının **kendi telifsiz** efekt dosyası (`sfx`, `hizala: true` efekti
  klipteki gerçek ses anına oturtur). Lisanslı müzik yok. Hedef −14 LUFS, ölç-düzelt döngüsüyle.
- Toplam 10–15 sn; tek sahne şablonunda kesme yok; son kare ilk kareye bağlanabiliyorsa döngü kur.

## Aşama 9 — Teslim
`is/NN/teslim/` altına: MP4 + kontrol karesi + caption metni (+ istenirse kareler, klipler, senaryo tablosu .zip).
Caption, hashtag, AI etiketi, DM otomasyonu, 48. saat ölçüm eşikleri: `${CLAUDE_SKILL_DIR}/referans/teslim.md`.
Teslim raporu: yeniden üretilen/kırpılan klipler (saniyesiyle), harcanan kredi, kalan kusurlar, varsayımlar.
Sesi dinleyemediysen bunu açıkça yaz.

## Sınırlar
- Kontrol etmediğin klibi "temiz" ilan etme; "bitti" = dosya + ölçüm satırı + kontrol karesine bakıldı.
- Başka markanın logosu, lisanslı müzik/karakter, sahte fiyat/yorum/indirim videoya girmez.
- Yeniden üretim kredi harcar: `ai-video-kreatif` kredi kuralı geçerli (tek seferlik tavan onayı, KARARLAR.md).
- ChatGPT'de tek başına kurgu isteyen kullanıcıya: `${CLAUDE_PLUGIN_ROOT}/ekler/chatgpt/video-kurgu.md`.
