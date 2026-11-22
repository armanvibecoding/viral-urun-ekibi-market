Biçim: KARAKTER bloğu (1. satır eylem · 2. satır `ADIM 4/8 · Niche Art Director (Zeynep)` · ≤5 madde · kod bloğu yok · son satır `Sonraki:`).

# Adım 4/8 Fotoğraf planı

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 76–130. 0.3.0'da kullanıcının onayladığı görsel diliyle tek kural setine indirildi; değişen ve iptal edilen eski kurallar repo `docs/ESKIDI.md`'de. Prompt şablonları `uretim-promptlari.md`, kurallar `tasarim-dili.md`.

---

ADIM 4/8 — FOTOĞRAF PLANI
Bütün görselleri tek mesajda planla; bu planı Adım 5'te SEN üreteceksin. Görsel üretme.

4.0 Ön koşul (0.3.4): DEVAM KARTI'nda 5 HEX ve başlık yazı tipi tarifi yoksa plan yapılmaz, görsel üretilmez; `marka` adımına dön. Renk varyantı belirsizse ya da araştırma metni fotoğrafla çelişiyorsa (metin "mor ve yeşil", fotoğraf pembe-altın) plandan önce tek soru: "Hangi renk varyantını satıyoruz?" Görsel metni kuralı: `01-kurallar.md` "Görsel metni"; tek zemin HEX'i (G0–G8, B1, B2 aynı HEX; tablonun "Zemin hex" sütununda bu satırlarda tek değer), tipografi, kadraj ve ürün kayması: `tasarim-dili.md` §9.

4.1 Referans ve sadakat
- Referans YALNIZ benim yüklediğim fotoğraflardır; web'de bulduğun görselleri referans ya da örnek olarak listeleme. Fotoğraflarımı numarala ("Ref 1: ön", "Ref 2: yan" …). Ürün net değilse, filigran ya da başka marka logosu varsa, birden çok ürün varsa ya da etiket okunmuyorsa söyle; gerekirse daha iyi fotoğraf iste. Okuyamadığın yazıyı uydurma.
- Yabancı dilde (Çince vb.) etiket, tedarikçi logosu ve ambalaj yazısı korunmaz: o yüzey aynı renk ve dokuda yazısız üretilir. Bu referans yalnız ürünün formu için kullanılır. Yalnız ürünün kendi marka etiketi ya da pazar dilindeki etiketi korunur.
- Referanstan ürünün YAPISAL SADAKAT LİSTESİNİ çıkar: görselde birebir korunacak 5–10 somut detay, her biri referanstaki hâliyle. Örnekler:
  - giyilebilir ürün: kol ve paça uzunluğu, yaka/kapüşon formu, iç astar ve desen, kulak/kanat gibi ek parçalar ve bağlantı noktaları, kapanış (fermuar, çıtçıt, düğme) yeri ve görünümü
  - cihaz: düğme sayısı ve yeri, kablo/giriş, ekran, kapak
  - kozmetik: şişe/kavanoz formu, kapak tipi, etiket yerleşimi
  Listedeki tek bir sapma görseli reddettirir; "benzer" kabul edilmez.
- İnsan yok: görseller insansız, grafik ve ürün odaklıdır (model, el, yüz, yatak sahnesi yok). Tek istisna bedenli giyim: model gerekiyorsa kullanıcıya tek satırla sor; onaylanırsa modeli bir kez tarif et ve aynı tarifi her promptta kelimesi kelimesine kullan.

4.2 Planlanacaklar
- G0 feed karesi (0.4.0, `istemler/g0-feed.md`): galerinin 1. sırası, YAZISIZ, tek ürün, ürünün uzun kenarı tuvalin %75–86'sı, ≥ 1500 px. Google Merchant Center ana görselde yazı/rozet/logo/kenarlık yasaklıyor; galeri yazılı kalır, feed'e yalnız bu kare gider. Planda G1'den sonra üretilir.
- G1–G8: 8 kare galeri (1:1), grafik ve yazılı. Şablonlar ve nişe göre sıra: `uretim-promptlari.md` §2 ve §6. Her biri ayrı bir satış görevi taşır. Aynı poz, aynı açı ya da yalnız estetik amaçlı görsel kabul edilmez.
  - G1 ana tanıtım (ÖNCE bu üretilir ve onaylatılır; `ortak-istem-bloklari.md`): asimetrik afiş, solda dev başlık satır satır, sağda ürün; somut fayda başlığı (2–5 kelime) + ürün + en fazla 1 kısa alt satır (ürün satırı); önden ya da 3/4 açı; ürün kadrajın %60–70'i; ürünün tamamı görünür. Bu görsel koleksiyon ve sepet küçük resmidir, küçükken de okunmalı.
  - G2–G8: nişin sırasıyla makro fotoğraf kartları (çizgi ikon yok), nasıl çalışır (işaret çizgileri), dev sayı, kullanım adımları (insansız), kutu içeriği + ölçü, sınıfa karşı karşılaştırma, zaman çizelgesi. Sıranın itiraz karşılayan karelerini Bulgular'daki itirazlara göre seç.
  - Doğrulanmış içerik bir kareyi doldurmuyorsa içerik uydurulmaz: o kare yerine yakın plan doku ya da kutu/ölçü karesi gelir.
- B1 masaüstü banner, 1920×800 (2.4:1): metinli (0.3.5): etiket + dev başlık + alt metin + buton solda, ürün sağda; sol yarısı boş banner yok. B2 mobil banner, 1080×1350 (4:5): tipografi görselin içinde (M2 düzeni).
- Logo ve favicon bu adımda üretilmez: planda tek satırla anılır (varsayılan: yalnız ikon, yazısız, şeffaf PNG; Adım 5'in başında `istemler/logo-ikon.md` ile). Canlı metin logo yalnız kullanıcı isterse.
- S1–S5 site bölüm görselleri. Her biri bölümünün satış görevini taşır, yazısızdır ve galeriden ayrı üretilir. Galeri fotoğrafları hiçbir bölümde tekrar kullanılmaz.
  Zemin hilesi: her S görselinin zemini, konacağı bölümün zemin rengiyle aynı hex'tir; ürün hiçbir kenara değmez.
  - S1 3 fayda kartı: 3 ayrı dikey görsel, 4:5; her biri bir faydayı gösterir
  - S2 görsel + fayda listesi (ürün sayfası): 4:5
  - S3 marka hikâyesi: 4:5
  - S4 Hakkımızda geniş görseli: 21:9, en az 1920 px genişlik
  - S5 ürün özellikleri bandı: 4:5, ZORUNLU (ürün sayfasındaki "Özellikler" bölümü bu görselle basılır; ürünün kumaşını, dokusunu ya da etiketini gösteren yakın ama galeriden farklı bir kare). Atlarsan tema galerinin son fotoğrafını tekrar kullanır
  Yalnız ürüne uygun olanları planla. Önce/sonra görseli ÜRETİLMEZ: yalnız benim verdiğim gerçek fotoğraf kullanılır (T4.3 `n-os`).

4.3 Kurallar (tutarlı, premium, CRO odaklı set)
- Konsepti hazır listeden değil, Bulgular'daki rakip görsel dilinden ayrışarak belirle; tek cümleyle yaz ("set fikri").
- Stil tek yerde sabitlenir: `uretim-promptlari.md` 12 blok sistemi (ROL → ÜRÜN KİLİDİ → STİL ÇAPASI → … → DÜZELTME). Yer tutucular (§1) planda bir kez doldurulur; her promptta aynı değer kullanılır. Ayrı STİL BLOĞU yazılmaz.
- Ürünü kendi kelimelerinle yeniden tarif etme; referansı göster: "Ref 1'deki ürünün AYNISI". Her prompta koruma listesi (şekil, oran, renk, malzeme, logo, parça sayısı) ve yapısal sadakat listesi girer.
- Sahne dili: düz tek renk zemin, tek ışık kaynağı, kısa yumuşak gölge; kamera yüksekliği ve ürün dönüşü AÇI satırında derece olarak. Yüzey malzemesi (taş, traverten, mermer, ahşap masa) ve süs yazılmaz.
- Şu kelimeleri kullanma, plastik ve yapay görüntü verir: 8k, hyperrealistic, masterpiece, flawless, perfect, ultra detailed, studio polish. İstediğini olumlu yaz: "dağınıklık olmasın" deme, "sade, düz açık gri zemin" de.
- Arka plan düz tek renk ve konacağı yüzeyin zeminiyle aynı hex (zemin hilesi). Ürün hiçbir kenara değmez: her kenarda en az %6 boş zemin. Geçiş, kirli sarı, çamurlu ya da gri-kahve ton ve rastgele bulanık doku yok.
- Yazı: G1 somut fayda başlığı + en fazla 1 kısa alt satır (doğrulanmış ürün gerçeği; kargo/iade/garanti değil); G2–G8 yazılı grafik serbest (METİNLER bloğunda olmayan yazı yok); S1–S5 ve B1 yazısız; B2'de tipografi görselin içinde. Ürünün kendi etiketi korunur.
- Banner:
  - B2 metinleri: etiket (ürün adı · miktar, büyük harf), başlık en fazla 6, alt metin en fazla 8 kelime, kısa buton, ürün satırı; pazar dilinde. Marka adı yalnız ambalajda. Türkçede büyük harf: i → İ, ı → I ("MİNİK", "MINIK" değil). Yalnız gerçek ürün iddiası; "Ücretsiz kargo" gibi lojistik/kampanya yazısı görsele yazılmaz (mağaza kuralı olsa bile).
  - B1'de görsele yazı eklenmez; sol yarı sakin alandır.
  - Masaüstü ve mobil AYRI tasarlanır: aynı ürün ve renk sistemi, ama dikey için yeniden kurulmuş kompozisyon. Biri diğerinin kırpılmışı olmaz.

Çıktı:
- Set fikri, SADAKAT LİSTESİ, niş anahtarı (A/B), yer tutucu değerleri (bir kez).
- Tek tablo: No | CRO görevi | Şablon (G0–G8, B1, B2, S1–S5) | Açı (diğerlerinden farkı) | Metinler | Zemin hex | Oran ve piksel.
- Üretim promptu her görsel için `uretim-promptlari.md` §3 sırasıyla kurulur (planda yazma; istersem gösterirsin).
Sor: "Fotoğraf planı onaylı mı? (revize için numara yaz)"
