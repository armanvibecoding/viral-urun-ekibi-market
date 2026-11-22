---
name: studio
description: "Studio (AI video kreatifi). Prepares AI video creatives: scripts, start frames, clips. Bir ürün için AI video kreatifi hazırlar — ürünü araştırır, ürün kartı ve kilit metni yazar, 30 senaryo (kanca, şablon, sahneler) üretir, ChatGPT'de başlangıç karelerini, Google Flow'da (Omni, 9:16, 4 sn) klipleri ürettirir. \"Bu ürüne video yap\", \"30 senaryo yaz\", \"AI video kreatifi\", \"reels fikri\", \"başlangıç karesi\", \"Flow klibi üret\", \"kanca yaz\" isteklerinde çağır. Kurgu, yazı, ses ve teslim için cut becerisine geçer."
---

# AI video kreatif

Ürün fotoğrafından 30 senaryoya ve ilk örnek videonun kliplerine kadar götürür. Kullanıcıyla dil **Türkçe**;
görsel/video promptları **İngilizce**; ekran yazısı ve CTA **pazarın dilinde** (pazar `.ekip/KARARLAR.md`'den okunur:
Türkiye → Türkçe, yurt dışı → İngilizce). Kullanıcı kod bilmeyebilir; terminal işini sen yaparsın.
Python komutu: macOS/Linux `python3`, Windows `py -3` (Windows'ta `python3` yazmak Microsoft Store'u açar).

## Hafıza protokolü (her aşamada)
- Her ürün `is/NN-urun-adi/` altında. Aşama kaydı `is/NN-urun-adi/DURUM.md`: aşama no (0–9), her videonun
  hangi aşamada olduğu (tablo), onaylı kredi tavanı ve harcanan kredi. Şablon:
  `${CLAUDE_PLUGIN_ROOT}/skills/captain/referans/hafiza-sablonlari.md`.
- Her aşama bitince ürün `DURUM.md`'sini ve `.ekip/DURUM.md`'deki "Sıradaki adım"ı güncelle. Kullanıcı karar
  verdiği an (pazar, seçilen senaryo, kredi tavanı, CTA kelimesi) `.ekip/KARARLAR.md`'ye satır ekle.
- Oturum başında ya da "devam" denince önce ürün `DURUM.md`'sini oku, kaldığın aşamadan sürdür; biten aşamayı yeniden yapma.
- Uzun çıktı (kart, senaryo tablosu, prompt) dosyaya; sohbete 5–10 satır özet + dosya yolu.

## Aşamalar (ayrıntı: `${CLAUDE_SKILL_DIR}/referans/asamalar.md`)
| No | Aşama | Bitiş durumu (dosya) |
|---|---|---|
| 0 | Girdi + kapılar | ürün fotoğrafı `referans/` içinde; pazar, kredi tavanı, müzik izni, Flow hakları, Chrome indirme, logo/IP KARARLAR'da |
| 1 | Araştırma + ürün kartı + hikâye bankası | `kart.md` (sektör satırı + mekanizma kartı + işlev cümlesi) + `kilit.txt` + `viral-referans.md` + `hikaye-bankasi.md` |
| 2 | Temiz ürün görselleri | `referans/paket_*.png` + aynı-ürün panosu ve ölçüm tablosu |
| 3 | 30 senaryo | `senaryolar.json` + `senaryolar.md/.csv`, `senaryo_kontrol.py` çıkış 0 |
| 4 | Kare planı + promptlar | ilk 5 videonun `promptlar/VNN_SK_gorsel.txt` ve `_flow.txt` dosyaları |
| 5 | Başlangıç kareleri + ön-üretim hükmü | `kareler/VNN_SK.png` (1080×1920), kabul tablosu, `elestiri/juri.jsonl` ön-üretim satırı `gecti: true`, `kapi.py kredi` çıkış 0 |
| 6 | Flow klipleri | `klipler/VNN_SK.mp4` (720p), harcanan kredi DURUM'da |
| 7–9 | Klip kontrolü, kurgu, teslim | `cut` becerisi |

**Aşama 0 tek turdur:** kullanıcıya gidecek bütün kapılar (pazar, kredi tavanı, müzik kaynağı izni, Flow "kullanım
hakları" onayı, Chrome çoklu indirme izni, logo/IP) burada tek mesajda sorulur ve KARARLAR.md'ye yazılır; sonrası
sorusuz akar (liste ve istisnalar: `asamalar.md` Aşama 0).

Aşama 1'de kartı **gerçek fotoğraf ve satıcı açıklamasından** yaz (AI görselden değil). Mekanizmanın bilinmeyen kısmını
gösterme; o anı atlayan sahne kur ve `[DOĞRULA]` etiketle. Kilit metni bir kez yazılır, her promptu betik üretir.
**Mağaza kurulduysa** (`is/NN/magaza/magaza-paketi.json` var, Aşama 0): önce `python3 "${CLAUDE_PLUGIN_ROOT}/ortak/paket.py" magaza-oku
is/NN/magaza/magaza-paketi.json --cikti-dizin is/NN/kurgu` → `is/NN/magaza/marka-kilidi.md` + `video-ayar.json` + `onayli-iddialar.txt`
(çıkış 0 değilse dosya kullanılmaz; ayrıntı `asamalar.md` Aşama 0). Ürün referansı mağazanın yazısız G0 karesidir (`kilit.txt` ondan ve
mağazanın ürün kilidinden yazılır, ikinci bir kilit tanımı yapılmaz); senaryoda söylenen her sayı ve sonuç cümlesi
`onayli-iddialar.txt`'de olmalı (brief'e ekle); kapak ve son karede mağazanın renkleri ve başlık ailesi kullanılır.

**Viral referans (Aşama 1 sonu, atlanamaz; alt ajan izlenme okuyamaz, bu iş liderde):** TikTok'ta ≥ 5 sorgu, en az 10 video
izlenir, Meta Reklam Kütüphanesi satırı eklenir → `is/NN/viral-referans.md`. Referans izlenmeden senaryo ve kare üretilmez; bu
videoların kareleri kör jürinin referansıdır. Yöntem: `${CLAUDE_SKILL_DIR}/referans/uretim-kurallari.md` §1.

**Hikâye bankası (Aşama 1 sonu, sahne üretiminden önce):** `is/NN/hikaye-bankasi.md`, en az 10 aday; senaryo yalnız bankadan
seçilir. Bir sahne 2 kez yeniden üretilip tutmadıysa 3. üretim yerine bankaya dön. Satır biçimi: `uretim-kurallari.md` §2.

Aşama 3 ağır iştir: `icerik-stratejisti` alt ajanına ver (30 senaryonun yazımı ajanın varsayılan modelinde; hikâye bankası ve
ilk 5 senaryonun seçimi için ayrı çağrı, çağrıda en güçlü model). Brief'te: `is/NN/kart.md`, `kilit.txt`, pazar, CTA kelimesi,
dağılım kuralları (`asamalar.md` §3), çıktı biçimi `${CLAUDE_SKILL_DIR}/referans/senaryo-formati.md`, betik klasörü
`${CLAUDE_SKILL_DIR}/scripts/` (ajan değişkeni bilmez, yolu açık yaz), durma ölçütü "`senaryo_kontrol.py` çıkış 0". Ana oturuma yalnız özet + dosya yolu döner. Sonra betiği **sen de** koştur (ajan çıktısı sınanır).

**Ön-üretim hükmü (Aşama 5 sonu, kredi onayından önce):** ilk 5 videonun kareleri kör jüriye gider (`juri.py pano --mod onuretim`,
gerçek viral referansların ilk kareleriyle yan yana; `video-juri` 3 kopya; `juri.py birlestir`). Kalan video Flow'a gitmez;
kök nedeni `video-elestirmen` yazar, geçenler için kontratı (`kurgu/KURALLAR.md`) doldurur. Akış: `captain` "Hüküm hattı".
Kredi geçişinin tek kapısı: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/captain/scripts/kapi.py" kredi is/NN --proje .` (senaryo,
kontrat, hüküm, kredi onayı, defter). Çıkış 0 olmadan Flow'da üretim başlamaz; aşım yalnız kurucu kararıyla (`captain` §5c).

Örnek video için en güçlü ve AI riski en düşük senaryoyu (mekanizması `[DOĞRULA]` olmayan) seç, gerekçeyi tek satır yaz.

## Betikler (`${CLAUDE_SKILL_DIR}/scripts/`)
- `senaryo_kontrol.py is/NN/senaryolar.json` — sebep→sonuç, tekrar, benzerlik (difflib > 0,8), dağılım, TR kanca kuralları,
  giriş/ortam/özne çeşitliliği; tablo yazar.
- `prompt_uret.py is/NN/senaryolar.json is/NN/kilit.txt --video 1 2 3` — görsel + Flow promptları; kilit sayımı ve
  AUDIO ⊆ ACTION kapısı. Tek promptu panoya: `--kopyala 1 2 flow`.
- `kare_hazirla.py <indirilen.png> is/NN/kareler/V01_S1.png --referans <orijinal>` — 9:16 kırp, 1080×1920, md5 kontrolü.
  `--yan-yana orijinal uretilen pano.jpg --bolge x0,y0,x1,y1` — aynı ürün mü panosu.
- `ekran_tasi.py k2.png k3.png CX CY R k3_hizali.png` — "sonra" karesinin ekran bölgesini "önce" karesine taşır (kadraj sabit).
- `chatgpt_indir.js`, `flow_yukle.js` — Claude in Chrome `javascript_tool` için (kullanım: `referans/flow-ve-chatgpt.md`).
Betik DUR/❌ verirse düzelt ve tekrar koştur; geçmeden sonraki aşamaya geçme.

## Kare, klip, Flow ve kredi (üretimden önce oku: `${CLAUDE_SKILL_DIR}/referans/uretim-kurallari.md` §3–§5)
- Her kare ayrı görsel; her kareyi isteğe karşı **ölçerek** kontrol et (ölçüm/pano dosyası yoksa ✅ geçersiz); ❌ olanı
  orijinal referanstan tek düzeltmeyle yeniden üret, en fazla 2 deneme.
- Ürün ekranı/ışığı karenin içinde üretilir, içerik değişimi kesimdedir; kahraman karakter klipler arasında değişmez.
- Flow: Omni 1.2 Flash, 9:16, 4 sn, 720p = 12 kredi/klip; **tek kare = tek klip**; klip başına en fazla 3 deneme.
  Bir klip ≈ 4,03 sn'dir, süre = Σ klip (URE-01).
- **Kredi:** tavan onayı Aşama 0'da bir kez, tutarıyla KARARLAR.md'ye; tavan içinde tekrar sorma, aşacaksan DUR. Tavanı
  istemeden önce `python3 "${CLAUDE_SKILL_DIR}/scripts/malzeme_kontrol.py" <video-planı.md|json> --klip N --tavan X` → çıkış 0.
- Klipler inince hemen `cut` aşama 7: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/cut/scripts/klip_qc.py" is/NN/klipler/*.mp4 --pano`.
- Görüntü kaynağı önceliği: gerçek stok/kendi çekim > gerçek ürün fotoğrafı > AI klip; her videoda hareketli tasarım katmanı
  (`cut` Aşama 8b). Ayrıntı `uretim-kurallari.md` §6.
- Karar dosyaları: `referans/baslangic-karesi.md`, `sahne-sablonlari.md`, `kanca-kutuphanesi.md`, `kreatif-mantigi.md`,
  `pazar-katmani.md`, `meme-formatlari.md` (seride ≤ %30); yasaklar `kurgu-ve-yasaklar.md` §7; tamamı tek blokta `sistem-promptu.md`.

## Sınırlar
- Uydurma yok: ürünün yapmadığını gösterme; sayı, yorum, indirim, stok, fiyat uydurma. Emin değilsen `[DOĞRULA]`.
- Ekranda fiyat: ICE-01. Ekran yazısı ürünü listelemez, ikna eder (`kanca-kutuphanesi.md` §1b).
  İşlevi açık söylenemeyen ürün: `kurgu-ve-yasaklar.md` §8 İmâ yolu (ICE-03).
- Başka markanın logosu/ürün adı, lisanslı karakter/müzik, ünlü yüzü, sahte otorite yok. Sağlık ve sonuç dili yasak
  değil: yazılır, yumuşatılmaz, çıktıya bilgi notu eklenir (IDD-01); platform reklam riski ayrı uyarıdır (PLT-01). Kural kimlikleri (IDD, ICE, URE, SES, PLT): `${CLAUDE_PLUGIN_ROOT}/ortak/kurallar.md`.
  İstisna: ürün belirli bir markanın aracına/ürününe takılan aksesuarsa (ör. araç amblemi) marka görünürlüğünü kullanıcı
  karar verir; risk ona söylenir ve karar KARARLAR.md'ye yazılır.
- Google/ChatGPT girişinde dur, kullanıcıya devret; şifre isteme, yazma. Ödeme ekranında dur.
- Kullanıcı ChatGPT'de kendi başına yapmak isterse: `${CLAUDE_PLUGIN_ROOT}/ekler/chatgpt/studio.md`
  (Chrome eklentisi modunda ChatGPT Flow'a dosya yükleyemez; bulut tarayıcısında Google girişi kullanıcıdadır).

## Rapor (aşama sonunda, ≤6 satır)
Ne çıktı (dosya yolu) · kontrol sonucu (sayıyla) · harcanan/onaylı kredi · kalan kusurlar · sıradaki adım · varsa tek soru.
