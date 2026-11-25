# Ekip köprüsü: mağaza aşamalarının ekibin geri kalanıyla bağı

Ne zaman okunur: `urun-paketi.json` geldiğinde, tema paketi yokken, site metni yazılırken, kurulum bitince, video geldiğinde.
Mağaza Kurucu, Viral Ürün Ekibi'nin mağaza koludur. Ekibin tek lideri `captain` becerisidir: işi o başlatır, onayları o toplar, hafızayı o tutar. Bu dosya aşamaların ekipten ne alıp ekibe ne verdiğini söyler.

## 1. Dosyalar ve hafıza
- Proje klasörü varsa (Claude Code) her şey `is/NN-urun/magaza/` altındadır: `devam-karti.md`, `urun-paketi.json`, `magaza-paketi.json`, `video-paketi.json`. Aşama sonunda DEVAM KARTI bu dosyaya da yazılır; lider `.ekip/DURUM.md`'ye tek satır ekler.
- Proje klasörü yoksa (ChatGPT, sohbet): aynı dosyalar sohbete eklenir ya da indirilebilir dosya olarak verilir; hafıza DEVAM KARTI'dır.
- Köprü betiği: `ortak/paket.py` (eklenti kökünde; şema ve doğrulayıcı yanındaki `ortak/sozlesme/`). Yeri: `find / -name paket.py -path "*ortak*" 2>/dev/null | head -1`. Bulunamazsa (kod aracı yok) dosyayı `arayuz-sozlesmesi.md` tablosuna göre elle yaz ve oku; alan uydurma.

## 2. Girdi: `urun-paketi.json` (ekibin ürün kolu üretir)
1. Önce doğrula: `python3 <paket.py> dogrula urun <dosya>`. Çıkış 1 ise eksik alanı kullanıcıya tek satırla söyle; uydurma.
2. `kaynak` alanı olan özellik doğrulanmış gerçektir; kaynaksız özellik [DOĞRULA] listesine girer.
3. `rakipler` ve `kanit` araştırmanın başlangıcıdır: yeniden arama, yalnız eksik olanı tamamla.
4. **Fiyatın tek kaynağı `teklif` alanıdır:**
   - `teklif.kaynak` = `teklif.tsv` → fiyat, para ve `paketler` (adet indirimi) ONAYLI değerdir. Birebir alınır, yeniden önerilmez, sorulmaz.
   - `teklif.kaynak` = `sabit-kural` ya da dosya yok → tekli fiyatı sen önerirsin; adet indirimi sabit kural: 2'li %10, 3'lü %18 (gerekçeyle değişebilir).
   - İki kaynak çelişirse `teklif.tsv` kazanır. Sonraki aşamalarda DEVAM KARTI'ndaki değer değişmez.

## 3. Tema modu (kurulumdan önce bir kez belirlenir, DEVAM KARTI'na yazılır)
- **Tam mod:** kullanıcıda `tema.json`'daki zip var (ad ve boyut tutuyor). Akış kaynak metindeki gibi: tema yüklenir, şablonlar T4.5 ile yazılır, tema ayarları (T10) yapılır.
- **Temasız mod:** zip yok. Tema istenmez, kullanıcı tema aramaya gönderilmez. Mağazanın mevcut temasına dokunulmaz:
  - Yapılır: metafield ve metaobject tanımları, görsel yükleme, ürün (başlık, açıklama, galeri, varyant, fiyat), adet indirimi, sayfalar ve yasal sayfalar, kargo, koleksiyon, menüler.
  - Atlanır ve "temasız mod" notuyla listelenir: tema zip'i yüklemesi, T4.5 şablon yazımı, tema ayarları (font, renk, logo bağlama), niş şablonu (`templateSuffix`).
  - Ürün sayfası metni: tema bölüm haritası yerine `teklif` bölümünün sayfa iskeleti (`assets/sayfa-iskeleti.md`) sırası kullanılır (ilk ekran → fayda → kanıt → itiraz → SSS). Metin ürün açıklamasına ve sayfalara yazılır; temadaki bölümlere yerleştirmeyi kullanıcı tema düzenleyicisinde yapar. Kullanıcıya verilecek tek liste: hangi metin hangi bölüme, hangi font ve HEX tema ayarına.
  - QA'da tema kaynaklı maddeler "ölçülmedi (temasız mod)" yazılır; site denetimi yine yapılır.
- `magaza-paketi.json` `magaza.tema_modu`: `tam` ya da `temasiz`.

## 4. Site metni kapısı (metinler aşaması)
- Yasak ifade listesi tek yerdedir: `teklif/references/yasak-ifadeler.tsv`. Kod aracı varsa onaydan önce: `python3 <teklif_kontrol.py> tara --pazar <ülke kodu> <metin dosyası>` → çıkış 0 şart (yeri: `find / -name teklif_kontrol.py 2>/dev/null | head -1`).
- Kapı sağlık ya da sonuç cümlesinde takılırsa metni kendin yumuşatma ve silme: kullanıcıya tek satırla sor (cümle kalsın mı), kararı DEVAM KARTI'na yaz. Kalan cümlenin altına "Bilgi notu (kullanıcının sorumluluğu)" satırı girer.
- `teklif` bölümü çalıştıysa iddia–kanıt listesi, SSS ve itiraz yanıtları oradan alınır; yeniden yazılmaz, yalnız temanın alan sınırlarına sığdırılır.

## 5. Çıktı: `magaza-paketi.json` (kurulum sonunda)
1. DEVAM KARTI'ndan `arayuz-sozlesmesi.md` tablosuna göre yaz: `surum` "2". Renk, font adı, onaylı metin ve fiyat birebir. Bilinmeyen değer (marka adı, ürün başlığı, fiyat, görseller) `null` + `eksik[]` yazılır; fiyat 0 ya da yer tutucu yazılmaz, marka adı için `marka.ad_kaynak` zorunludur.
2. `onayli_metinler.iddialar`: sitede geçen her sayı ve sonuç cümlesi, kaynağıyla. Video yalnız bu listeyi söyleyebilir; listeye girmeyen iddia videoya giremez.
3. Doğrula: `python3 <paket.py> dogrula magaza <dosya>` → çıkış 0 olmadan "bitti" denmez.

## 6. Geri dönüş: `video-paketi.json`
- `python3 <paket.py> video-sec <dosya>` yalnız `pdp-galeri` ve `hero` videolarını listeler; yalnız onlar yüklenir. Video galerinin sonuna girer, G0'ın yerini almaz. `reklam` videosu mağazaya yüklenmez.

## 7. Site denetimi ekibi (kurulum sonrası; alt ajan olan ortamda)
`site-denetimi.md` maddelerini lider şu ekip üyelerine paralel verir, her biri `is/NN-urun/magaza/` altına rapor yazar: `shopper` mod `donusum` (`CRO.md`), `probe` mod `hiz` (`HIZ.md`), `probe` mod `arama` (`SEO.md`), `probe` mod `erisim` (`ERISIM.md`), `shopper` mod `ses` (`SES.md`); brief'te `mod:` satırı zorunludur. Alt ajan yoksa aynı kontrol listesini bu aşama kendisi uygular.
