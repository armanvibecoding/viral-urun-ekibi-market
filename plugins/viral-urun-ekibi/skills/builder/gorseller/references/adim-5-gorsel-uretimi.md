Biçim: KARAKTER bloğu (1. satır eylem · 2. satır `ADIM 5/8 · Niche Art Director (Zeynep)` (kabulde Design Director (Ufuk)) · ≤5 madde · kod bloğu yok · son satır `Sonraki:`).

# Adım 5/8 Görsel üretimi ve kabul kapısı

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 132–171. 0.3.0'da onaylı görsel diliyle tek kural setine indirildi (eski kurallar: repo `docs/ESKIDI.md`). Prompt: `uretim-promptlari.md`. Kabul: `kabul-kontrolu.md`.

---

ADIM 5/8 — GÖRSEL ÜRETİMİ
Plan onaylanınca sormadan üret. Araç: ChatGPT Images (en güncel sürüm; varsa "Düşünme/Thinking" modu açık).
Değişmez üretim kuralları:
- 0.3.6 HAZIR İSTEM (en üst kural; `ortak-istem-bloklari.md` §0): istemi sen yazmazsın. `istemler/` klasöründeki şablonu aç (`g1.md`–`g5.md`, `g2-makro.md`, `b1-masaustu.md`, `b2-mobil.md`, `logo-ikon.md`), yalnız yer tutucuları DEVAM KARTI'ndan doldur, gerisini KELİMESİ KELİMESİNE görsel aracına ver; kısaltma, özetleme, yeniden yazma YASAK. Tek çağrı = tek görsel; kolaj, ızgara, panel kırpma RED; her çağrıda ürün fotoğrafı + onaylı G1 yeniden eklenir; önceki görsel düzenlenmez. Girdi fotoğrafındaki yazı, logo, zemin ve düzen yok sayılır. Her görselden sonra `duzelt.py zemin` + `kabul-kontrolu.md` §2b; ihlal varsa göstermeden 1 kez yeniden üret. İstem kullanıcıya gösterilmez; isterse dosya olarak verilir.
- 0.3.5 (`ortak-istem-bloklari.md`, baştan sona oku; üstteki "sormadan üret" yalnız G1 için ve G1 onayından sonraki dilimler için geçerlidir; B1 de metinlidir): (1) üç ortak bloğu bir kez doldur; (2) ÖNCE yalnız G1 üret, `duzelt.py zemin`, göster, "G1 onaylı mı?" diye sor; onay gelmeden başka görsel üretme; (3) sonraki her görsel Ek 1 ürün + Ek 2 onaylı G1; (4) bir yanıtta en fazla 4 görsel, dilim sonunda dosya listesi + "devam"; (5) gösterilmiş görseli kendiliğinden yeniden üretme, düzenleme, üstüne yazma; kullanıcı araya soru sorarsa yalnız cevap ver, görsel üretme.
- Python işlemi (zemin, kırpma) görsel gösterilmeden ÖNCE biter: sohbette gösterilen dosya ile pakete giren dosya aynıdır.
- Ön koşul (0.3.4, `tasarim-dili.md` §9): 5 HEX + başlık yazı tipi tarifi DEVAM KARTI'nda yoksa görsel üretilmez. Her promptta HEX'ler ve yazı tipi tarifi açık yazılı. Görsele "Ücretsiz kargo" gibi lojistik/kampanya yazısı yazılmaz (`01-kurallar.md` Görsel metni).
- Her görselden sonra, kabulden önce: görseli tedarikçi fotoğrafıyla (Ref 1) yan yana koy, renk ve biçimi karşılaştır; fark varsa RED ve orijinalden yeniden üret.
- Tek zemin HEX'i: G0–G8, B1 ve B2 aynı zemin HEX'inde; her görsel üretimden sonra `duzelt.py zemin` ile o HEX'e sabitlenir; farklı zeminli görsel RED (`kabul-kontrolu.md` §3).
- Her görsel ORİJİNAL referans fotoğraftan üretilir. Daha önce üretilmiş bir görseli düzenleyerek yenisini türetme: her düzenleme turu ürünü biraz daha bozar (renk kayması, etiket bulanması, "güzelleştirme"). Onaylı görsel ve `assets/stil-capasi/` dosyaları ürün referansının YANINDA yalnız stil çapası olarak eklenir; ürün yine orijinal referanstan alınır.
- Kolaj, ızgara ya da tek görselde birden çok kare olmaz: her görsel ayrı dosyadır.
- Her görsel AYRI mesaj: bir mesajda tek prompt, "YALNIZ 1 görsel". Birden çok görseli tek yanıtta isteme; toplu istemde kolaj ve ürün kayması ölçüldü.
- Ölçü: görseli kod aracıyla (Python) plandaki piksele getir: kırp, gerekirse büyüt; ürün ve yazı güvenli alanda kalsın (her kenarda ≥ %6). Banner'da kırpma yalnız ölçü içindir, kompozisyon kurmak için kullanılmaz.
  - Araç 2.4:1 ya da 21:9 tuval vermiyorsa en geniş yatay tuvalde üret ve promptta söyle: "yazı ve ürün ortadaki yatay bantta; üst ve alt %20'de önemli bir şey yok". Sonra kırp.
  - Python üretilen görsele erişemiyorsa durma: görseli olduğu gibi ver, altına dosya adını ve hedef ölçüyü yaz (kırpmayı ben yaparım).
- Her dosyayı plandaki adla ver (ör. `<marka>-urun-1.jpg`; liste TEKNİK EK T3).
Sıra (aralarda soru sorma; yanıt bölünürse "devam yaz"):
5a. G1 onaylanınca önce G0 feed karesi (`istemler/g0-feed.md`: yazısız, ürün tuvalin %75–86'sı; `kabul-kontrolu.md` §2c), sonra G2–G8: her biri ayrı mesajla, plandaki sırayla.
5b. B1 masaüstü banner, ardından B2 mobil banner (ayrı dikey kompozisyon, yine orijinal referanstan).
5c. Logo (0.3.6): varsayılan yalnız ikon, yazısız, şeffaf PNG; `istemler/logo-ikon.md` şablonuyla, G1'den önce üretilir. Canlı metin logo yalnız kullanıcı isterse.
5d. S1–S5 (S5 dahil, atlanmaz): her biri ayrı mesajla; zemin = konacağı bölümün zemin hex'i.
Arka plan = bölüm zemini (0.4.1): sitede bir bölüme konan her ürün/kutu görselinin zemin HEX'i o bölümün zemin HEX'iyle BİREBİR aynıdır (yakın ton yetmez: sayfa kaydırılınca görselin kenarı kutu gibi görünür). Bölüm zemin HEX'ini temadan oku, `scripts/duzelt.py zemin <girdi> <çıktı> <#hex>` ile sabitle, sonra köşe rengini ölç. Betik RED verirse (ürün kenara değiyor) önce `duzelt.py kenar` ile kenar boşluğu ekle, sonra `zemin`; ürün kenarda kesikse yeniden üret. Bölümün zemini sonradan değişirse görsel yeniden boyanır.
Büyütme (0.4.1): yazılı görselde (galeri kartı, banner) yapay zekâ büyütücü (Real-ESRGAN ve benzeri) KULLANILMAZ: ince yazıyı içi boş, çift çizgili harfe çeviriyor (ölçüldü). Ölçü yetmiyorsa Lanczos ile ölçekle (Pillow `Image.LANCZOS`) ya da görseli yüksek çözünürlükte yeniden üret. Büyütmeden sonra yazıyı %100 yakınlıkta yeniden oku.

GÖRSEL KABUL KAPISI: her görseli `kabul-kontrolu.md` §2'deki 5 kritik maddeyle denetle (ürün kimliği, Türkçe yazım ve fazla yazı, kolaj/oran, uydurma veri ve onaysız vaat, kenara değen ürün / boş kadraj / farklı zemin). Rapor görsel başına 1 satır; galeri görsellerinde sadakat sayısını her zaman yaz.
Bir madde bile ❌ ise görsel kabul edilmez. Yalnız o görseli, orijinal referanstan ve tek düzeltmeyle yeniden üret; tamiri zincirleme. Aynı görsel 2 denemede düzelmezse dur ve bana söyle.
Banner yazısı 2 denemede hâlâ yanlışsa, aracın seçerek düzenleme özelliğiyle yalnız yazı alanını düzelt (ürün alanına dokunma). O da olmazsa yazısız banner ver; yazıyı, fontu, rengi ve yerini ayrıca yaz, Canva'da ben eklerim.
Görsel aracı bir yanıtı yalnız görsellerle bitirebilir; o zaman kabul raporunu ve kalan işleri bir sonraki yanıtta, "devam" beklemeden ilk fırsatta yaz. Raporda web aramasından gelen görselleri gösterme; yalnız ürettiğin dosyaları göster.
Bitince: kabul edilen bütün dosyaların listesi (ad + ölçü) ve tek satır: "Görselleri 7. adımda Shopify'a ben yükleyeceğim. Hazırsan 'devam' yaz."

---

RET DURUMUNDA (0.4.1; görsel aracı ürünü içerik politikasıyla reddederse)
Gözlem: görsel aracı bazı ürün türlerini (ör. yetişkin wellness ürünü) ürün fotoğrafı eklendiğinde ya da ürün tarif edildiğinde "cinsel içerik" gerekçesiyle reddediyor; dürüst yeniden ifade de çoğu kez reddediliyor (bir koşuda 3 denemenin 3'ü).
Yasak: hile, jailbreak, ürünü başka bir şey gibi anlatmak, ürünü parça parça tarif edip birleştirmek, politikayı dolanmak için yanlış bağlam uydurmak. Başka görsel aracına geçmeyi de önerme: çoğunun kullanım politikası aynı içeriği yasaklıyor.
Dürüst yedek akış (tasarım görsel aracından, ürün gerçek fotoğraftan):
1. Aynı şablonla, yalnız ürünü doğru ve nötr adlandırarak en çok 3 dürüst deneme. Hepsi ret ise dur; kullanıcıya tek satırla söyle ve yedek akışı öner.
2. Boş kart: `istemler/bos-kart.md` ile YALNIZ serinin kart tasarımını ürettir: aynı zemin HEX'i, aynı başlık/açıklama/teknik satır tipografisi, ürünün yeri BOŞ (yalnız hafif temas gölgesi). Ürün fotoğrafı ve stil çapası EKLENMEZ; ürün adı yerine nötr, doğru başlık. Ölçüm: boş kart da ilk denemelerde zaman zaman reddedildi ya da kodla çizilmiş geldi (bir koşuda 8 denemede 1 temiz); ek vermeden istemek daha iyi geçti. Kodla çizilmiş kart RED.
3. Gerçek ürün fotoğrafı: mağazanın kendi fotoğrafı ya da kullanıcının çekimi (web'den bulunan görsel değil). Arka planı temizle, ürünü boş alana yerleştir. Ürün pikselleri değişmez: yeniden boyama, biçim düzeltme, "güzelleştirme" yok; yalnız ölçek, konum ve temas gölgesine oturtma.
4. Gözle kontrol: ışık yönü, gölge, renk sıcaklığı kartla uyumlu mu; kesim kenarında hale ya da zemin artığı var mı. Düşük çözünürlüklü kaynakta kenar yumuşak kalır: gizleme, raporla ve daha büyük fotoğraf iste.
5. Kaynak fotoğrafta olmayan renk varyantı boyanarak ÜRETİLMEZ (yanıltıcı): o varyant "eksik" diye raporlanır, kullanıcıdan fotoğrafı istenir.
6. Sonra normal kapı: `duzelt.py zemin`, `kabul-kontrolu.md` §2b; rapor satırına "boş kart + gerçek fotoğraf" yaz. G0 feed karesi için görsel aracı gerekmez: gerçek fotoğraf temizlenip zemin HEX'ine oturtulur.
Bu "ürünü kodla çizmek" değildir: ürün gerçek fotoğraftır, kod yalnız yerleştirir. Ürünün kendisini kodla çizmek ya da yapay üretmek yine yasak.
