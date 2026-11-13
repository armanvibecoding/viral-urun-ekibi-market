---
name: ai-video-kreatif
description: Bir ürün için AI video kreatifi hazırlar — ürünü araştırır, ürün kartı ve kilit metni yazar, 30 senaryo (kanca, şablon, sahneler) üretir, ChatGPT'de başlangıç karelerini, Google Flow'da (Omni, 9:16, 4 sn) klipleri ürettirir. "Bu ürüne video yap", "30 senaryo yaz", "AI video kreatifi", "reels fikri", "başlangıç karesi", "Flow klibi üret", "kanca yaz" isteklerinde çağır. Kurgu, yazı, ses ve teslim için video-kurgu becerisine geçer.
---

# AI video kreatif

Ürün fotoğrafından 30 senaryoya ve ilk örnek videonun kliplerine kadar götürür. Kullanıcıyla dil **Türkçe**;
görsel/video promptları **İngilizce**; ekran yazısı ve CTA **pazarın dilinde** (pazar `.ekip/KARARLAR.md`'den okunur:
Türkiye → Türkçe, yurt dışı → İngilizce). Kullanıcı kod bilmeyebilir; terminal işini sen yaparsın.
Python komutu: macOS/Linux `python3`, Windows `py -3` (Windows'ta `python3` yazmak Microsoft Store'u açar).

## Hafıza protokolü (her aşamada)
- Her ürün `is/NN-urun-adi/` altında. Aşama kaydı `is/NN-urun-adi/DURUM.md`: aşama no (0–9), her videonun
  hangi aşamada olduğu (tablo), onaylı kredi tavanı ve harcanan kredi. Şablon:
  `${CLAUDE_PLUGIN_ROOT}/skills/ekip-lideri/referans/hafiza-sablonlari.md`.
- Her aşama bitince ürün `DURUM.md`'sini ve `.ekip/DURUM.md`'deki "Sıradaki adım"ı güncelle. Kullanıcı karar
  verdiği an (pazar, seçilen senaryo, kredi tavanı, CTA kelimesi) `.ekip/KARARLAR.md`'ye satır ekle.
- Oturum başında ya da "devam" denince önce ürün `DURUM.md`'sini oku, kaldığın aşamadan sürdür; biten aşamayı yeniden yapma.
- Uzun çıktı (kart, senaryo tablosu, prompt) dosyaya; sohbete 5–10 satır özet + dosya yolu.

## Aşamalar (ayrıntı: `${CLAUDE_SKILL_DIR}/referans/asamalar.md`)
| No | Aşama | Bitiş durumu (dosya) |
|---|---|---|
| 0 | Girdi | ürün fotoğrafı `referans/` içinde; pazar KARARLAR'da; link/fiyat varsa `kart.md`'de |
| 1 | Araştırma + ürün kartı | `kart.md` (mekanizma kartı) + `kilit.txt` (PRODUCT / MECHANISM / SCREEN / WRONG) |
| 2 | Temiz ürün görselleri | `referans/paket_*.png` + aynı-ürün panosu ve ölçüm tablosu |
| 3 | 30 senaryo | `senaryolar.json` + `senaryolar.md/.csv`, `senaryo_kontrol.py` çıkış 0 |
| 4 | Kare planı + promptlar | ilk 5 videonun `promptlar/VNN_SK_gorsel.txt` ve `_flow.txt` dosyaları |
| 5 | Başlangıç kareleri | `kareler/VNN_SK.png` (1080×1920), kabul tablosu |
| 6 | Flow klipleri | `klipler/VNN_SK.mp4` (720p), harcanan kredi DURUM'da |
| 7–9 | Klip kontrolü, kurgu, teslim | `video-kurgu` becerisi |

Aşama 1'de kartı **gerçek fotoğraf ve satıcı açıklamasından** yaz (AI görselden değil). Mekanizmanın bilinmeyen kısmını
gösterme; o anı atlayan sahne kur ve `[DOĞRULA]` etiketle. Kilit metni bir kez yazılır, her promptu betik üretir.

Aşama 3 ağır iştir: `icerik-stratejisti` alt ajanına ver. Brief'te: `is/NN/kart.md`, `kilit.txt`, pazar, CTA kelimesi,
dağılım kuralları (`asamalar.md` §3), çıktı biçimi `${CLAUDE_SKILL_DIR}/referans/senaryo-formati.md`, betik klasörü
`${CLAUDE_SKILL_DIR}/scripts/` (ajan değişkeni bilmez, yolu açık yaz), durma ölçütü "`senaryo_kontrol.py` çıkış 0". Ana oturuma yalnız özet + dosya yolu döner. Sonra betiği **sen de** koştur (ajan çıktısı sınanır).

Örnek video için en güçlü ve AI riski en düşük senaryoyu (mekanizması `[DOĞRULA]` olmayan) seç, gerekçeyi tek satır yaz.

## Betikler (`${CLAUDE_SKILL_DIR}/scripts/`)
- `senaryo_kontrol.py is/NN/senaryolar.json` — sebep→sonuç, tekrar, benzerlik (difflib > 0,8), dağılım, TR kanca kuralları; tablo yazar.
- `prompt_uret.py is/NN/senaryolar.json is/NN/kilit.txt --video 1 2 3` — görsel + Flow promptları; kilit sayımı ve
  AUDIO ⊆ ACTION kapısı. Tek promptu panoya: `--kopyala 1 2 flow`.
- `kare_hazirla.py <indirilen.png> is/NN/kareler/V01_S1.png --referans <orijinal>` — 9:16 kırp, 1080×1920, md5 kontrolü.
  `--yan-yana orijinal uretilen pano.jpg --bolge x0,y0,x1,y1` — aynı ürün mü panosu.
- `chatgpt_indir.js`, `flow_yukle.js` — Claude in Chrome `javascript_tool` için (kullanım: `referans/flow-ve-chatgpt.md`).
Betik DUR/❌ verirse düzelt ve tekrar koştur; geçmeden sonraki aşamaya geçme.

## Kare ve klip kuralları (en sık hata buradan çıkar)
- Her kare ayrı görsel (kolaj değil), aynı video aynı ChatGPT sohbetinde; sahne 2+ `CONTINUITY LOCK` ile (betik ekler).
- Her kareyi isteğe karşı **ölçerek** kontrol et: ürün parça/renk/yazı, 4 bacak/5 parmak, aynı hayvan, etkileşim noktası
  karede hazır, olmamış olayın izi yok, logo/poster yok. Göz kararı ✅ yazma; ölçüm/pano dosyası yoksa ✅ geçersiz.
  ❌ olanı ORİJİNAL referanstan tek düzeltmeyle yeniden üret, en fazla 2 deneme; tutmazsa sonraki uygun senaryoya geç.
- AI ekran, yazı, logo, parmak ve ince geometriyi bozar: ürün üstü ekran içeriği ve yazı **kurguda bindirilir**
  (karede ekran kapalı ya da düz tek renk; `kilit.txt` içinde `SCREEN:` satırı).
- Kare tipi, kamera, kanca, şablon kararları için: `referans/baslangic-karesi.md`, `sahne-sablonlari.md`,
  `kanca-kutuphanesi.md`, `kreatif-mantigi.md`, `pazar-katmani.md`; yasaklar `kurgu-ve-yasaklar.md` §7; tamamı tek blokta
  `sistem-promptu.md`; gerçek plan çıktısı biçimi `ornek-plan.md`; test/devam-öldür eşikleri `olcum-ve-test-plani.md`.

## Flow ve kredi (ölçülmüş)
- Model **Omni 1.2 Flash**, 9:16, x1, 4 sn, **720p = 12 kredi/klip**. 360p kullanılmaz. Pahalı model ayrı onay ister.
- Kredi harcayan her üretimden önce **tek seferlik tavan onayı** al: "N klip + en fazla R yeniden deneme = toplam en fazla
  X kredi (720p klip başı 12, ekranda okudum). Onaylıyor musun?" Onayı tutarıyla KARARLAR.md'ye yaz. Tavan içinde tekrar
  sorma; aşacaksan DUR. Kredi bilgisini her üretimde ekrandan da oku.
- Klip başına en fazla 3 deneme, her denemede tek değişiklik. İndirilen dosya adı sırayı taşımaz: klibi ilk karesine bakarak eşle.
- Yükleme yöntemi, giriş, kullanım hakları onayı, indirme: `${CLAUDE_SKILL_DIR}/referans/flow-ve-chatgpt.md`.
  Tarayıcı aracı yoksa promptları dosyadan kullanıcıya ver; o üretir, sen klipleri kontrol edersin.
- Klipler inince hemen `video-kurgu` aşama 7: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/video-kurgu/scripts/klip_qc.py" is/NN/klipler/*.mp4 --pano`.

## Sınırlar
- Uydurma yok: ürünün yapmadığını gösterme; sayı, yorum, indirim, stok, fiyat uydurma. Emin değilsen `[DOĞRULA]`.
- Başka markanın logosu/ürün adı, lisanslı karakter/müzik, ünlü yüzü, sağlık/güvenlik iddiası, sahte otorite yok.
- Google/ChatGPT girişinde dur, kullanıcıya devret; şifre isteme, yazma. Ödeme ekranında dur.
- Kullanıcı ChatGPT'de kendi başına yapmak isterse: `${CLAUDE_PLUGIN_ROOT}/ekler/chatgpt/ai-video-kreatif.md`
  (Chrome eklentisi modunda ChatGPT Flow'a dosya yükleyemez; bulut tarayıcısında Google girişi kullanıcıdadır).

## Rapor (aşama sonunda, ≤6 satır)
Ne çıktı (dosya yolu) · kontrol sonucu (sayıyla) · harcanan/onaylı kredi · kalan kusurlar · sıradaki adım · varsa tek soru.
