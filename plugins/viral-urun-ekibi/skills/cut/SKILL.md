---
name: cut
description: "Cut (Video kurgu). Edits clips into the final video: text, sound, delivery. AI klipleri (Flow/Omni ya da çekim) ffmpeg ile kurgular — klip kalite kontrolü (sıçrama ölçümü + 4 fps pano), kırpma, ekran içeriği bindirme, ekran üstü kanca/CTA yazısı, efekt ve −14 LUFS ses, kontrol karesi, caption ve teslim paketi. \"Klipleri kurgula\", \"videoyu birleştir\", \"yazı ekle\", \"ses ekle\", \"klipleri kontrol et\", \"kurgu yap\", \"teslim et\", \"final videoyu çıkar\" isteklerinde çağır."
---

# Video kurgu

Klipten teslim edilebilir MP4'e: 1080×1920, 30 fps, H.264 + AAC, +faststart, 8–15 sn. Kullanıcıyla dil **Türkçe**;
ekran yazısı ve CTA **pazarın dilinde** (`.ekip/KARARLAR.md`'deki son `| pazar |` satırı; betik kendisi okur).
Betikler `${CLAUDE_SKILL_DIR}/scripts/` altında; Python komutu: macOS/Linux `python3`, Windows `py -3` (Windows'ta `python3` yazmak Microsoft Store'u açar).
Gereken: Python 3.8+, Pillow, ffmpeg (PATH ya da `imageio-ffmpeg` paketi). Kurulum: `${CLAUDE_SKILL_DIR}/referans/kurulum.md`.
**Varsayılan kurgu tarifi:** `${CLAUDE_PLUGIN_ROOT}/ortak/tarifler/01-urun-videosu-tr-reels.md` (ayarda `"yazi_stil": "kutulu"`; ekransız üründe `"urun_tipi": "ekransiz"`). 25 sn organik hikâye: tarif 02, betikler `scripts/hikaye/` (`uret.py ayar.json`).
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
  AUDIO satırı) yaz, `studio` aşama 6'ya dön (kredi tavanı içinde). "Yeterince iyi" yok.
- Ölçüm işaretledi ama panoda doğal hareket görüyorsan (hızlı kafa çevirme) plan numarasını `qc_izin`'e ekle ve gerekçeyi yaz.

## Ekran / yazı içeren ürünler (istisna, kurgudan önce)
Ekran içeriği karede üretilir, değişim kesimdedir (`studio` "Kare ve klip kuralları"). Bindirme yalnız karede
üretilemeyen hareketli içerik içindir ve elips/perspektif, cam yansıması, kumlanma eşlemesi ister:
`ekran_bindir.py klip --kareler` ile ilk/son kareyi çıkar, ekran merkezini ve iç genişliğini ölç, sonra
`ekran_bindir.py klip anim.mp4 cikti.mp4 --x0 --y0 --d0 [--x1 --y1 --d1]`. Ardından çıktıya tekrar `klip_qc.py --pano`:
her karede bindirme ekranın içinde mi. Yöntem ve ayarlar: `${CLAUDE_SKILL_DIR}/referans/ekran-bindirme.md`.

## Aşama 8 — Kurgu
0. Mağaza kurulduysa (`is/NN/magaza/magaza-paketi.json`): `is/NN/kurgu/video-ayar.json` (`ortak/paket.py magaza-oku --cikti-dizin` çıktısı) yazı
   ailesini, renkleri ve linki verir; ekran yazısı ve altyazı mağazayla aynı aile ve renkle kurulur. Kurgu ön-kontrolüne
   `--magaza-paketi is/NN/magaza/magaza-paketi.json` eklenir: onaylı listede olmayan iddia = HATA `[iddia]`, gevşetilmez.
1. `is/NN/kurgu/VNN.json` ayar dosyasını yaz (alanlar `kurgu.py` başındaki açıklamada ve `referans/kurgu-kurallari.md`).
2. Koştur: `python3 "${CLAUDE_SKILL_DIR}/scripts/kurgu.py" is/NN/kurgu/VNN.json --proje .`
   Betik kapıları kendisi uygular (720p altı, sıçrama); geçmezse kurgu yapılmaz.
3. Çıktı satırını oku: süre KURALLAR.md K1 aralığında (kontrat yoksa ürün gösterimi 8–15 sn, hikâye 20–30 sn), 1080×1920,
   −14 ±1 LUFS. K1 dışındaysa video eleştiriye GÖNDERİLMEZ; önce düzelt.
   Teslim öncesi görüntü kapısı: `python3 "${CLAUDE_SKILL_DIR}/scripts/kurgu_kontrol.py" --goruntu VNN.mp4 --kesimler <plan başları>`
   → çıkış 0 (kesim dışı RGB sıçraması ya da son 2 sn gürültü → 3, render hatası).
4. `VNN_kontrol.jpg`'ye bak (her planın ortası + son kare): yazı okunuyor mu, ürünü/çıkış noktasını örtüyor mu,
   CTA son ≥ 3 sn'de ve kancanın hemen altında mı. Örtüyorsa `yazi_konum` ya da `kanca_gizle` ile yeniden koştur.
   KURALLAR.md'deki kredisiz her K maddesini tek tek işaretle (✓ / ✗ + kanıt: dosya, saniye); işaretsiz madde varsa
   video eleştiriye GÖNDERİLMEZ.
**Viral (hızlı) kurgu — varsayılan reklam kurgusu:** `hizli_kurgu.py ayar.json` (alanlar betiğin başında). Kurgu kuralları
(kanca ilk karede, vuruşa oturan plan, yazı biçimi ve konumu, ses, müzik, drop, döngü): `${CLAUDE_SKILL_DIR}/referans/kurgu-kurallari.md`
— kurgudan önce oku. Sektöre özgü kurallar ayrı ektedir (ör. `referans/sektor/arac-aksesuar.md`); ürünün sektör eki yoksa
yalnız genel kurallar ve ürün kontratı (`is/NN/kurgu/KURALLAR.md`) geçerlidir.
- En güçlü an ilk karede; ilk karede ses de olsun. Plan = 2 ya da 4 vuruş, 2 vuruştan kısa plan yok; toplam 12–15 sn.
- Yazı ürünü örtmez; alt %20 ve sağ %15 boş; emoji videoya girmez (caption'a). Ekranda fiyat: ICE-01.
- **Ses:** `mixer` ajanı `ses_tasarla.py`dan önce efekt planını çıkarır. Müzik videoda olmalı (SES-02) ve müzik girişi
  kuralına uyar (SES-01); müzik stem'i `is/NN/ses/stem_VNN/muz.wav` olarak kaydedilir (kapı onu ölçer). Yöntem: `referans/ses-tasarimi.md`.
- **Ön-kontrol (kurgudan sonra, jüriden önce):** `hizli_kurgu.py ayar.json --katı` (okunma UYARI'sı = çıkış 1), sonra
  `kurgu_kontrol.py ayar.json --video VIDEO.mp4` → çıkış 0. Klip içerikleri `klipler/klip_etiket.json`dan okunur (biçim betiğin başında).
- **Hüküm:** kör jüri (`juri.py pano --mod teslim` → `jury` 3 kopya → `juri.py birlestir`; akış `captain` "Hüküm hattı")
  videoyu gerçek viral referanslarla yan yana puanlar. Kalırsa kök nedeni `fixer` yazar.
  **Referans < 3 ise iş durmaz, kullanıcıya soru sorulmaz:** `juri.py yapilamadi is/NN --video VNN --referans-sayisi N --neden "…"` → kapı "JÜRİ YAPILAMADI" notuyla geçer, teslim notuna yazılır; referans bulma ayrı iş (DURUM.md).
- **Teslim geçişinin tek kapısı:** `python3 "${CLAUDE_PLUGIN_ROOT}/skills/captain/scripts/kapi.py" yayin is/NN --proje . --kopyala`
  (teknik, kurgu, görüntü, ses, iddia, hüküm, defter, sözleşme); çıkış 0 olmadan `teslim/` klasörüne video konmaz.

## Aşama 8b — Hareketli tasarım katmanı (HyperFrames; her reklam videosunda)
Kinetik tipografi, geçiş, ilerleme/sayaç, UI kartı, önce/sonra silmesi. ffmpeg temel kurguyu yapar; hareketli katmanı
HyperFrames üretir. Ön koşul: Node 22+ ve `npx hyperframes doctor --json` → `ok`. Adımlar (registry'de ara, proje kur, temel video
yazısız, kontrol ve render, saydam bindirme, sonra aynı ön-kontrol kapısı): `${CLAUDE_SKILL_DIR}/referans/hareketli-tasarim.md`.
Yazı metni ve zamanı tek kaynaktan gelir (`is/NN/kurgu/VNN.json`); yeni metin uydurulmaz. Katman kurulamıyorsa yazı
`hizli_kurgu.py` ile kalır ve raporda yazılır. ChatGPT'de bu aşama yok.

## Aşama 9 — Teslim
`is/NN/teslim/` altına: MP4 + kontrol karesi + caption metni (+ istenirse kareler, klipler, senaryo tablosu .zip).
Caption, hashtag, AI etiketi, DM otomasyonu, 48. saat ölçüm eşikleri: `${CLAUDE_SKILL_DIR}/referans/teslim.md`.
Mağaza kurulduysa teslimde `video-paketi.json` yazılır: `python3 "${CLAUDE_PLUGIN_ROOT}/ortak/paket.py" video-yaz is/NN/teslim
--cikti is/NN/magaza/video-paketi.json [--pdp VNN] [--hero VNN] --dil <tr|en|yok>` (işaretlenmeyen = `reklam`; yalnız `pdp-galeri`
ve `hero` mağazaya yüklenir; hangi video nereye: `teslim.md`). Çıkış 0 olmadan mağaza koluna devredilmez.
Teslim raporu: yeniden üretilen/kırpılan klipler (saniyesiyle), harcanan kredi, kalan kusurlar, varsayımlar.
Sesi dinleyemediysen bunu açıkça yaz.

## Sınırlar
- Kontrol etmediğin klibi "temiz" ilan etme; "bitti" = dosya + ölçüm satırı + kontrol karesine bakıldı.
- Başka markanın logosu, lisanslı karakter, sahte fiyat/yorum/indirim videoya girmez (aksesuar istisnası: kullanıcı kararı, KARARLAR.md).
- Yeniden üretim kredi harcar: `studio` kredi kuralı geçerli (tek seferlik tavan onayı, KARARLAR.md).
- ChatGPT'de tek başına kurgu isteyen kullanıcıya: `${CLAUDE_PLUGIN_ROOT}/ekler/chatgpt/cut.md`.
