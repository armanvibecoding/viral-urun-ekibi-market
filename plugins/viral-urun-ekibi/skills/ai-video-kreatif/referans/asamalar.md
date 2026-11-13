# Aşamalar 0–6 — ayrıntı

Kaynak: ~100 milyon izlenen ürün videosunun saha incelemesi + 30 videoluk gerçek bir AI seri üretiminde ölçülen hatalar.
Kodlar: M = mekanizma, S = şablon, K = kanca ailesi (aşağıda). Kural etiketi: KURAL ≥3 kayıt · ADAY 2 · GÖZLEM 1.

## Klasör (kullanıcının projesi)
```
is/NN-urun-adi/
  DURUM.md            aşama kaydı (video × aşama tablosu, kredi)
  kart.md             ürün + mekanizma kartı, kaynaklar, [DOĞRULA] listesi
  kilit.txt           PRODUCT / MECHANISM / SCREEN / AVOID / WRONG (İngilizce)
  referans/           orijinal ürün fotoğrafları, paket_*.png (temiz ürün görselleri), aynı-ürün panoları
  senaryolar.json     30 senaryo (biçim: senaryo-formati.md) -> senaryolar.md / .csv betikle
  promptlar/          VNN_SK_gorsel.txt, VNN_SK_flow.txt (betikle)
  kareler/            VNN_SK.png (1080×1920) + _onizleme.jpg
  klipler/            VNN_SK.mp4 (720p) + _qc.jpg panolar
  kurgu/  teslim/     video-kurgu becerisi
```

## Aşama 0 — Girdi (tek soru turu)
Tek mesajda sor: 1) ürün fotoğrafı (yoksa bekle) 2) pazar (KARARLAR'da yoksa: Türkiye mi, yurt dışı/hangi ülke mi)
3) varsa ürün linki ve satış fiyatı. Link/fiyat yoksa onlarsız devam et; varsayımı tek satır yaz.
Kararları KARARLAR.md'ye yaz. Fotoğrafları `is/NN/referans/` altına kopyala.

## Aşama 1 — Araştırma + ürün kartı + kilit
- Web: ne işe yarar, kim alır / kime hediye alınır, benzer viral videolar ne gösteriyor. Viral videodaki ürün bizimkiyle
  AYNI mı karşılaştır (benzer ≠ aynı). Sahneden sahneye değişen (AI) satıcı videosu kaynak değildir. Captcha veren siteyi atla.
- **Mekanizma kartı** (atlanamaz): görünüm (renk, malzeme, parça sayısı, üzerindeki yazı birebir, boyut — ele/hayvana göre) ·
  etkileşim noktası (tuş, delik, kapak, sap) · sonuç TAM OLARAK nereden çıkar/nerede görünür · gerçek ses · ürünün
  YAPMADIKLARI (kendi kendine hareket etmez, büyümez…). Görseller çelişirse en sık görüleni seç, "varsayım" yaz.
- `kilit.txt` (İngilizce):
  - `PRODUCT:` tek paragraf, her promptta birebir (betik sayar).
  - `MECHANISM:` sonuç YALNIZ nereden, hangi eylemle çıkar; eylem yoksa sonuç yok. Belirsiz yön (under/near) yazma, yeri adıyla.
  - `SCREEN:` ekranlı/yazılı üründe: "the screen shows one flat uniform [renk] color - no image, no icon, no text, no flicker".
  - `WRONG:` ürünün yanlış davranışları (Flow AVOID'a eklenir). `AVOID:` görsel için ek yasaklar.

## Aşama 2 — Temiz ürün görselleri (ChatGPT)
- Orijinalden 2–3 temiz paket çekimi (ön, yan, kullanım açısı): "clean pack shot of the exact product from the reference
  photo, plain light-grey background, no text, no props" + PRODUCT kilidi. Orijinalde başka marka logosu varsa yükleme,
  metinden üret (model logoyu sızdırır).
- **Aynı ürün mü** (göz kararı ✅ yasak): `kare_hazirla.py --yan-yana` ile pano; yazı/parça bölgesini `--bolge` ile 2×;
  iki görselde aynı 2 oranı pikselle ölç (ör. tuş genişliği / gövde genişliği), sapma > %10 = ❌; karttaki parçaları
  numarala, parça başına ✅/❌ + renk + yazı harf harf + fazladan/eksik parça. Pano dosyası yoksa ✅ geçersiz.
- ❌ olanı orijinalden tek düzeltmeyle yeniden üret; 2 denemede tutmazsa o açıyı bırak.

## Aşama 3 — 30 senaryo (alt ajan: icerik-stratejisti)
**Bilgi tabanı**
- Görüntü izlenmeyi, kanca paylaşımı taşır; zayıf görüntüyü kanca kurtarmaz. İlk saniyede ürün çalışıyor ya da problem
  görünüyor. 8–15 sn, konuşma yok, gerçek ürün sesi + telifsiz efekt. Kopya ölür: aynı fikir, YENİ an.
- AI'ın KAZANDIĞI: çekilemeyen hayvan/bebek anı · hayvanın ürünle "şakanın kendisi" olduğu an · gece kamerası problem
  karesi · yabancı tepkisi · reveal. KAYBETTİĞİ: mağaza rafı, kalabalık, önlüklü uzman, AI kurucu yüzü.
- Mekanizmalar: M1 anlık dönüşüm · M2 canlı karaktere dönüşür · M3 başka şeye benzeyen ürün · M4 görünmeyen kir görünür ·
  M5 kimlik/kültür · M6 nostalji · M7 canlıyı bedende taşıma · M8 hayvan problemi → huzur · M9 bebek huzuru ·
  M10 beden rahatlaması · M11 küçük dert → hızlı çözüm · M12 aile oyunu · M13 mekanizma/ASMR · M14 zararsız prank · M15 kişiye özel.
- Şablonlar: S1 tek sahne gag · S2 problem → "Vs…" → çözüm · S3 karton prototip → "VS" → sonuç · S4 çekilemeyen
  hayvan/bebek anı · S5 yabancı tepkisi · S6 mekân montajı · S7 ürün dönüşür · S8 dayanıklılık testi · S9 POV sorun →
  idealize sonuç · S10 AI kanca + gerçek çekim. Ayrıntı ve dolu örnek: `sahne-sablonlari.md`.
- Kanca aileleri: K1 yasak ("DO NOT show this to a DOG MOM…") · K2 zorunluluk ("Every CAT MOM NEEDS this!") ·
  K3 kesik hediye ("The perfect gift for your husband doesn't exi-") · K4 bağlamlı hediye · K5 alıntı-ironi
  ("\"Babe, we DON'T need that\" / Me:") · K6 yetişkin parası · K7/K8 POV · K9 durum cümlesi · K10 kimlik hitabı ·
  K11 kartlar ("The problem" → "Vs…" → "The solution") · K12 soru ("Rate this 1–10") · K13 yazısız.
  Hediye kancası kimliksiz olmaz. Ayrıntı: `kanca-kutuphanesi.md`.

**Dil (pazara göre)** — yurt dışı: doğal İngilizce. Türkiye: gündelik Instagram dili, "sen" hitabı; İngilizce kalıbı
çevirme. Örnek: "Kedisi olan herkese lazım", "Eşim \"buna ne gerek var\" dedi / Ben: …", "Kedim bunu görünce aklı gitti",
"Bunu kedi annelerinden saklayın". Kimlik kelimesi kancaların EN FAZLA yarısında. Kötü (zorlama): "KÖPEK BABASISIN,
orkestra şefi değil". TR ölçülebilir kural (betik tarar): kanca ≤ 8 kelime; yok: "keşfedin", "hayatınızı değiştirecek",
"sizler için", "hemen sipariş verin", "mükemmel", "kaliteli", "tanışın", "işte", "artık", "—". Türkçe büyük harfi elle
yaz (kodda `upper()` "i"yi "I" yapar → "KEDI"); ç ğ ı İ ö ş ü doğru olsun. Emoji yalnız caption'da (videoda kutucuk olur).
**CTA kelimesi:** ürünü anlatan tek kelime, BÜYÜK harf, seride AYNI, marka adı değil. TR: `Yorumlara "KELİME" yaz, linki
DM'den atayım` · yurt dışı: `Comment "WORD" and I'll DM you the link`. Fiyat yurt dışında caption/bio'da; TR'de ekranda
yalnız GERÇEK fiyatla.

**Kurallar**
- Dağılım: ≥ 8 mekanizma, ≥ 6 şablon, ≥ 6 kanca ailesi; ürüne uymayan kota için kullanılmaz (uyan azsa söyle);
  hiçbir şablon > 6; aynı aile art arda yok; ≥ 3 yazısız (K13); kimlik kelimeli kanca ≤ 15.
- Her video 3–4 sahne × 4 sn, her sahne TEK eylem (tek klipte eylem zinciri AI'da bozulur). Son sahnede CTA ≥ 3 sn.
  S1 tek sahne gag: 2–3 klip aynı kadrajda kesmesiz.
- SEBEP → SONUÇ: etkileşim (basma, takma, açma) sonuçtan ÖNCE ya da AYNI klipte. "Vs…" sonrası da bu sıra korunur.
- FARKLI AN: farklılık sol/sağ pati ya da 1./2. tuştan DEĞİL; an, bağlam, kim kullanıyor, ortam, zaman, kamera tipinden
  (gece kamerası, misafir tepkisi, iki hayvan yarışı, ilk tanışma, paket açılışı, sahibi öğretiyor).
- Her videoda bir kez çıkış noktasının yakın planı (sonucun açıklıktan çıktığı an, el/patiden ayrı görünür).

## Aşama 4 — Kare planı + promptlar
Her sahne için `senaryolar.json` içinde `prompt` alanı (İngilizce): scene, position (el/patinin TAM yeri), camera,
action, audio, ambient. İlk 5 senaryo için doldurulur; kalanlar üretim sırasında. Promptları `prompt_uret.py` yazar.
Kare kuralları (şablon ekler; sahne metninde de uy): fotogerçekçi "iPhone Reels karesi", gerçek ev, tek ışık; bokeh,
stüdyo, CGI yok; 8k/hyperrealistic/cinematic yazma · ana öğeler ortadaki %70'te (2:3 → 9:16 kırpmada kesilmesin) ·
ürün kadrajın ≥ 1/3'ü · üst %25 düz zemin (yazı gelecek) · alt %20 ve sağ %15 boş · en fazla 3 özne · her sahne farklı
kadraj (S1 hariç) · **etkileşim karede hazır**: pati/el basacağı yerde ZATEN durur, çıkış açıklığından uzakta (havadaki
pati video modelinde yanlış parçaya iner) · olmamış olayın izi yok · hazne doluysa dolu çiz · pati dışarıdan giriyorsa
hayvan gövdesi karede olmasın.

## Aşama 5 — Başlangıç kareleri
- Seçilen senaryonun 3–4 karesi AYRI görsel, aynı sohbette. Görsel bitmeden indirme (önceki kare iner).
  2:3 (1024×1536) gelmesi hata değil: `kare_hazirla.py` ortadan 9:16 kırpar.
- Kabul — SERT (❌, yeniden üret): ürün yanlış · yazı bozuk · oran sapması > %10 · fazladan uzuv/hayvan (4 bacak, 1 kuyruk,
  5 parmak) · hayvan/ortam kareler arası değişiyor · pati/el yanlış yerde · olmamış olayın izi · poster/logo ·
  iki kare aynı kadraj. YUMUŞAK (devam, raporla): ürünün kadraj payı, kamera yüksekliği, üst boşluk → kırp/pad ile düzelt.
- Kırpılmış karede ürün/pati kesildiyse kareyi yeniden üret. Seri boyunca aynı hayvan: kabul edilen ilk hayvanlı kareyi
  sonraki videolarda "model referansı" olarak ekle.

## Aşama 6 — Flow klipleri
Ayrıntı: `flow-ve-chatgpt.md`. Video promptu kalıbı (betik üretir): tek kamera, tek eylem ("Only this one action
happens"), ürün sabit, MECHANISM, SCREEN LOCK, ışık sabit, AUDIO yalnız ACTION'daki 1–3 gerçek ses, konuşma/müzik yok,
AVOID + WRONG, ürün kilidi, "ONE continuous shot". Her denemede TEK değişiklik; klip başına ≤ 3 deneme (tavan içinde).

## Hata kataloğu (gerçek seride görüldü)
| Hata | Kök sebep | Önlem |
|---|---|---|
| Pati yanlış parçaya indi | Başlangıç karesinde pati havada | etkileşim karede hazır |
| Kimse dokunmadan ürün çalıştı | AUDIO'da ACTION'da olmayan ses | `prompt_uret.py` AUDIO ⊆ ACTION kapısı |
| Basmadan önce yerde sonuç vardı | Karede olmamış olayın izi | kare kontrolü |
| Hayvan klip içinde cins değiştirdi | Video modeli (yavaş dönüşüm) | 4 fps pano, her kare |
| Işınlanma / nesne kayboldu | Klip içi gizli kesme | `klip_qc.py` sıçrama ölçümü, kırp |
| Ürün yazısı bozuldu | Düzenleme üstüne düzenleme | hep orijinal referanstan |
| Sonuç patiden çıkıyor gibi | Çıkış açıklığı kapalı/belirsiz | MECHANISM satırı + yakın plan |
| Tüm seri yanlış mekanizmayla | Ürün AI görselden okundu | kart gerçek fotoğraftan |
