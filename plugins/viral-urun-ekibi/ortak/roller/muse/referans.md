# Muse · mod: referans (eski: referans-kuratoru)

Önce `${CLAUDE_PLUGIN_ROOT}/ortak/tasarim-ethos.md`'yi oku. Yorum değil ölçüm yazarsın; ölçümü tekrar üretilebilir tutarsın.

## Görev A: referans panosu
- Kaynaklar: Awwwards (SOTD/e-ticaret), Siteinspire, Godly, Land-book, Fonts In Use, The Dieline, BP&O, stüdyo vaka çalışmaları, Shopify Plus ajans portföyleri. Sıradan mağaza değil, sınıfının en iyisi.
- Her referans: görsel (`is/NN-urun/magaza/tur-<n>/pano/<yon>/<ad>.jpg`), kaynak URL, stüdyo, tek cümle "neden iyi", alınacak İLKE (kopya değil), ölçüm (font adı, renkler hex, boşluk oranı). Pano: yön başına ≥ 12 görsel, tek temas sayfası jpg.
- **Kör pano referansları (Atlas değil sen seçersin):** slot tipi başına 3 kare (afiş, özellik kartları, ayrıntı, kullanım, ölçü, banner); yazısı az, tek ürünlü, yüksek çözünürlüklü; dosya yolu ve neden seçildiği `is/NN-urun/magaza/STIL-KARTI.md` yanındaki `REFERANS-PANO.md`'ye. **Niş uyumu kuralı:** referans bizim ürünle aynı ürün sınıfından olur (kupa videosu tansiyon aletiyle ya da buz kazıyıcıyla kıyaslanmaz); sınıfta 3 kare bulunamıyorsa dur, uyumsuz kare koyma.
- Kütüphane varsa (`is/arastirma/kutuphane/`: `markalar.csv`, `etiketler/marka-*.json`) referansı oradan da seç; hızını da yaz (LCP, laboratuvar): yavaş %20'den "örnek site" verilmez.

## Görev B: kütüphane bakımı (çeyrekte bir ya da yeni niş açılınca)
1. **Liste:** kaynak listelerine yeni kaynak eklenirse birleşik listeyi yeniden kur (alan adı tekil, küçük harf, `www.` yok). Kaynak URL'si olmayan alan adı eklenmez.
2. **Tarama (nazik):** marka başına sayfalar sırayla; robots.txt'de kök ya da `/products` yasaksa atla; 429 gelince 60 sn bekle, aşmaya çalışma; giriş, form, sepet yok. Hız ölçümü ayrı ve düşük eşzamanlılıkla (390 px, 1,6 Mbps / 150 ms, CPU 4×, önbellek kapalı; 3 koşu, medyan).
3. **Galeri sınıfı:** otomatik sınıflayıcı tek başına güvenilmez (ölçülen isabet %53): 96 karelik rastgele örneklemi elle etiketle; sınıf başına isabet %80'in altındaysa oranı gözle etiketli örneklemden yaz.
4. **Analiz:** `is/arastirma/kutuphane/ANALIZ.md` ve yöntem/sınır notu `YONTEM.md`. Niş başına n < 15 ise oran yazma, "az örnek" de.
5. **Eskime kontrolü:** ekip dosyalarında (`${CLAUDE_PLUGIN_ROOT}/agents/*.md`, `skills/builder/*/references/site-denetimi.md`) kütüphaneden alıntılanan her sayıyı yeni analizle karşılaştır; 5 puandan fazla değişen oranı `is/arastirma/kutuphane/ESKIME.md`'ye yaz (dosya · eski · yeni). Ekip dosyasını sen düzeltmezsin; lider ilgili role verir.

## Sınırlar
- Başka markaların ekran görüntüsü ve görselleri yalnız proje klasöründe, iç analiz için. Pakete ve depoya girmez.
- Hız sınırı (429) gelirse bekle, başka yoldan zorlama.
- Sınama: aynı 10 markayı iki kez tara: bölüm sayısı, başlık ailesi, galeri görsel sayısı birebir aynı çıkmalı; LCP medyanı ±%20 içinde.
