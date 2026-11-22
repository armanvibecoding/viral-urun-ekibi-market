# Başlangıç karesi — ChatGPT'de üretilen ilk görsel

> Kaynak notu: bu dosya ~100 milyon izlenen ürün videosunun saha incelemesinden (kayıt numaraları köşeli parantezde, ör. [058]) ve bir dış araştırmadan derlendi. Ham veri seti eklentiye dahil değildir; sayılar o ölçümün sonucudur.

Hat: her sahne için ChatGPT'de **1 başlangıç karesi** → aynı kare + video promptu Gemini Omni'ye → 4–6 sn klip.
Bu dosya "ilk kare ne göstermeli"yi milyon kayıtlardan çıkarır. Etiket: KURAL ≥3 · ADAY 2 · GÖZLEM 1.

## 0. Önce: temiz ürün referansı (2026-11-07, dış araştırma notu madde 12)
Tedarikçi (AliExpress) fotoğrafı çoğu zaman yazılı, kolajlı, çok ürünlüdür ve bu kirlilik her kareye taşınır.
İlk iş: düz, nötr zeminde, tek ürün, yazısız, tam görünür bir **paket çekimi** (gerçek numune varsa telefonla çek; yoksa ChatGPT'de tedarikçi fotoğrafından "clean pack shot on plain light-grey background, no text, no props" üret ve ürünü fotoğrafla karşılaştır).
Sonraki tüm kareler ve Omni referansı bu görsele bakar (https://runware.ai/docs/models/google-gemini-omni-flash-1-1/guides/reference-driven-video.md · https://www.opus.pro/blog/product-photo-to-commercial-seedance).
Kare modeli seçimi belirsiz: ürün fotoğrafında Nano Banana Pro, logo/yazıda GPT Image 2 önde görünüyor (tek benchmark, https://www.pixazo.ai/blog/gpt-image-2-benchmark-real-pixazo-prompts) — kit ChatGPT ile devam eder.

## 1. İlk kare tipleri (birini seç)

| Tip | Ne gösterir | Etiket | Kanıt |
|---|---|---|---|
| İ1 Kullanım anı | ürün elde/vücutta **çalışırken**; 1 sn'de ne yaptığı anlaşılıyor | KURAL | 001, 003, 053, 057, 066, 072, 085, 093, 102, 114, 121, 123, 125 |
| İ2 Problem anı (ürünsüz) | tanıdık, komik ya da sinir bozucu an: kedi sürücünün yüzüne atlıyor, kıllı lavabo, üşüyen köpek, sıkıştıran araç | KURAL | 044, 047, 074, 077, 084, 100, 112, 116, 119, 120, 126 |
| İ3 Tuhaf görüntü | ürün bir karakter/garip nesne gibi: direksiyonda kaplumbağa kabuğu, kapıdan giren kırkayak-köpek, dev çıplak ayak terlik | KURAL | 006, 038, 057, 063, 075, 081, 087, 123 |
| İ4 Cansız → canlı | peluş sanılan şey bebek/hayvan çıkıyor (ilk kare arkadan peluş) | KURAL | 065, 096, 103 |
| İ5 Karanlık + ürün ışığı | karanlık odada ürünün kendi ışığı en parlak nokta | KURAL | 020, 036, 057, 062, 072, 078 |
| İ6 Gece / güvenlik kamerası | gri IR görüntü, köşede REC; problem karesi "gerçek" görünür | KURAL | 074, 084, 120 |
| İ7 Örtü / kapı / paket açılışı | battaniye altı, kapı kolu POV, poşetten/paketten çıkarma, bez altından reveal | KURAL | 062, 064, 077, 078, 088, 106, 135, 136 |

Kaçınılan ilk kare: **mağaza rafı / kalabalık kuyruğu / ekip** (N1: 047, 070, 071, 080, 083, 086, 107, 120, 123, 132; 132'de milyon olan video 2 sn jenerik rafla açılıyor ama gövde kullanım — GÖZLEM) ve **beyaz önlüklü "uzman"** (059: 2,3–17,3B).

## 2. Kamera dili

- **Yüzsüz POV / yalnız vücut parçası** (eller, ayak, bacak, sırt) — KURAL: 059, 062, 066, 085, 097, 109, 117, 121, 123.
- **Yer seviyesi / alçak açı** ürünü büyük gösterir — ADAY: 038 (terlik), 073 (mini araba).
- **Üstten sabit** (yatak, yuva, masa) — KURAL: 080, 089, 123 (+ 093 masa, 101 flat-lay).
- **Sabit kadraj, aynı set** — R1: aynı kadraj 296 kez [060], 61 kez [093], 34 kez [067].

## 3. Görsel kurallar

1. **9:16 dikey.** ChatGPT dikey seçeneği 1024×1536 (2:3) olarak listeleniyor (web: https://tanstack.com/ai/latest/docs/guides/image-generation); 2:3 gelirse ana öğe ortada kalsın, kurguda 9:16'ya kırp.
   Omni'de görsel girdi verilince oran girdiyi izler (web, üçüncü taraf: https://runware.ai/docs/models/google-gemini-omni-flash-1-1/guides/resolution-and-duration).
2. **Gerçek-telefon görünümü** (gerçek çekim 66/97 milyon): doğal gürültü, kusurlu ev, tek kaynak ışık. AI-1/AI-2 sahnelerinde bile ev/sokak sıradan olsun.
   İstisna: AI-5 idealize huzur karesi sıcak, yumuşak ışık [094, 089].
3. **Ürün sadakati:** ekli ürün fotoğrafıyla aynı şekil, renk, parça sayısı, logo. Ürün kadrajın en az üçte biri.
   "Match the attached photo" yetmez: görünen detayları kelimeyle yaz (malzeme, kapak, etiket rengi: "matte black dropper cap, cream label") ve değişmeyecek parçaları tek tek say (ARAŞTIRMA madde 11, Runware URL'si §0).
4. **Kompozisyon:** ana öğe ortadaki %70'te; **üst üçte bir sakin** (ekran yazısı); alt %20 ve sağ %15'e önemli şey koyma (Instagram arayüzü).
5. **Görselde yazı yok** (kutu logosu hariç). Ekran yazısı kurguda eklenir.
6. **Problem karesi soluk/gri, çözüm karesi renkli** — ADAY: 044 (siyah-beyaz problem), 084/120 (gri IR → sıcak çözüm).
7. **Süreklilik:** 1. kareden sonraki her kare promptu `CONTINUITY LOCK` ile başlar (aynı kişi, kıyafet, hayvan, oda, ürün). Sabit karakter/set milyonlarda tekrar ediyor: 082 (aynı kadın, aynı beyaz kanepe), 099 (aynı adam), 124 (aynı sınıf).
8. **Marka/mağaza/karakter yok:** raf, tabela, forma, kostüm üstünde gerçek marka ya da lisanslı karakter çizdirme.
9. **El kuralları** (ARAŞTIRMA madde 9; https://magichour.ai/blog/how-to-fix-ai-video-faces-and-hands · https://morphic.com/resources/how-to/ai-video-troubleshooting):
   tek, basit tutuş · el kadrajda büyük (küçük el bozuluyor) · ürünle temas noktası **ilk karede** açıkça görünür · elden ele verme iki ayrı sahne ·
   "ürünü göster" ve "ürünü kullan" ayrı sahne (boyut kayması) · ilk karede bozuk el varsa animasyona geçme, önce kareyi düzelt.
10. **En fazla 3 özne** (kişi + hayvan): Omni'de 4+ özne birbirine karışıyor (https://morphic.com/resources/how-to/gemini-omni-flash-1-1-guide).
12. **Hikâyeye hizmet etmeyen obje yok:** promptta kadrajdaki HER obje sayılır ("only these objects: …") ve
   "no cup rings, no stains, no hair ties, no clutter" AVOID satırına yazılır. "Gerçek-telefon görünümü" (madde 2) dağınıklık
   demek değildir. Kare kabulünde lider/eleştirmen sayılmamış objeyi arar; varsa kare yeniden üretilir (2026-11-17).
   Ek referans görseli (karakter, kutu, el) eski bir kareden geliyorsa yalnız o nesneye KIRPILIR; 'ignore the glasses…'
   talimatıyla kirli kare eklenmez (ek görselin objeleri ve adı geçen obje yeni kareye sızar).
11. **"Sinematik" görünüm yok:** sığ alan derinliği, bokeh, anamorfik parlama, stüdyo ışığı AI'ı ele veren işaretler (ARAŞTIRMA madde 10) → AVOID satırında.

## 4. Görsel prompt kalıbı (İngilizce)

```
Vertical 9:16 phone-video still frame, photorealistic, looks like a real Instagram Reel shot on an iPhone.
SCENE: [ilk kare tipi İ1–İ7: tek cümle, ne oluyor].
PRODUCT: [ürün: şekil, renk, malzeme, parça] — match the attached product photo exactly (shape, color, parts, logo). Keep identical: [parça 1], [parça 2], [etiket rengi].
WHO: [kişi/hayvan: yaş, saç, kıyafet / tür, renk], seen from [POV hands | low ground angle | top-down | security camera corner].
WHERE: a real, ordinary [oda/mekân] in [ülke/pazar]; only the objects listed in SCENE (no stains, no cup rings, no clutter — §3 madde 12).
LIGHT: [tek kaynak: ceiling lamp | window daylight | the product's own glow | grey night-vision IR].
FRAMING: main subject in the middle 70%, product at least one third of the frame; top third calm for a caption; nothing important in the bottom 20% or right 15%.
TEXTURE: natural phone noise, slight motion blur.
AVOID: any text or letters, watermark, store signage, brand logos other than ours, licensed characters, extra fingers, distorted hands or paws, plastic skin, studio backdrop, studio lighting, shallow depth of field, bokeh, anamorphic flare, warped logo, distorted label, garbled text, more than three people or animals, CGI render look.
```

Sonraki kareler:
```
CONTINUITY LOCK: same [kişi], same [hayvan/bebek], same [oda], same product exactly as the attached product photo.
Vertical 9:16 phone-video still, photorealistic, natural phone noise.
SCENE: [...]
```

## 5. Kontrol listesi (üretimden sonra)
- El/pati/parmak sayısı doğru mu? Tutuş fiziksel olarak mümkün mü (akıcı görünen ama imkânsız tutuş reddedilir)? Ürün parça sayısı fotoğrafla aynı mı?
- Kutu/etiket yazısı bozuk mu (en küçük yazıyı tam çözünürlükte oku)?
- Görselde harf/yazı/tabela var mı → yeniden üret.
- İlk kare 1 sn'de "ne oluyor"u anlatıyor mu? (Anlatmıyorsa İ1 ya da İ3'e geç.)
- Mağaza/kalabalık/uzman görünümü sızdı mı → çıkar.

## 6. Ürün tipi modülleri (kartın sektör satırında seçilir; kareye §5'e ek olarak uygulanır)
Kaynak: ekranlı ürün serisinin ret eleştirileri (ekran/telefon) ve sektör sayımı (`kreatif-mantigi.md` §6). Diğer tiplerde AI kanıtı yok → GÖZLEM.

| Modül | Bilinen hata | Kare RED ölçütü |
|---|---|---|
| **Ekranlı / ışıklı** | düz renge bindirilen içerik perspektiften taştı, camda yansıma yoktu, hale rengi içerikle uyuşmadı; aşırı parlak ekran gerçeğinden farklı | içerik karede değil · hale rengi ≠ içerik rengi · camda yansıma çizgisi yok · ekranda yazı/rakam · çevre ışığında patlama (kırpılmış beyaz) |
| **Uygulamalı (telefondan kontrol)** | dokunuştan önce sonuç zaten değişmişti; telefon ekranı hiç görünmedi; kırpım sonucu kadraj dışında bıraktı | telefon ekranı ve seçilen karo görünmüyor · "önce" karesinde sonucun izi var · dokunuş ve sonuç aynı karede değil ya da kesimle bağlı değil |
| **Giyilebilir (insan)** | AI kanıtı çoğu hayvan/bebek taşıyan giysi; yetişkin modada beden oturuşu ölçülmedi | kumaş vücuda oturmuyor (havada duran kol/yaka) · kırışık yok, plastik doku · beden oranı ürün fotoğrafından >%10 sapıyor · fazladan cep/fermuar · yüz kadraj dışıysa göğüs/kolye üst kenara kayar → yazı alanı üst üçte bir değil, kolyenin altındaki orta bant; istemde 'caption room below the pendant' yazılır |
| **Mobilya / oda ölçeği** | oda ölçeği ve katlanma mekaniği için AI kanıtı yok | insan-boy ölçeği yok ya da tutarsız (kapı ~2 m referansıyla ölç) · eğri duvar/kapı çizgisi · katlı/açık hal parça sayısı farklı |
| **Sıvı / kozmetik / doku** | AI sıvı fiziği test edilmedi; "sıvı + cam" zaten veto | AI karesi kullanılmaz: gövde gerçek çekim (S10 hibrit: AI yalnız kanca); krem/köpük dokusu AI'da üretilmez |
