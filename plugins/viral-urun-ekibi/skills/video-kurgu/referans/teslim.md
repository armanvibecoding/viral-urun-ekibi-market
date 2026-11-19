# Teslim paketi

## Klasör: is/NN-urun/teslim/
- `VNN.mp4` (kurgu çıktısı) · `VNN_kontrol.jpg` · `VNN_caption.txt`
- İstenirse `.zip`: kareler + klipler + `senaryolar.md/.csv` + promptlar.

## Caption (her videoda farklı)
- 1–2 kısa cümle; **ilk satır CTA'yı tekrarlar**. TR: `Yorumlara "KELİME" yaz, linki DM'den atayım 📩` ·
  yurt dışı: `Comment "WORD" 👇 I'll DM you the link`. Emoji burada serbest (videoda değil).
- 4–5 hashtag (genel + ürüne özgü karışık).
- Sonda: TR `🎥 Yapay zekâ ile üretildi` · yurt dışı `🎥 Made with AI`. Platformun AI etiketini aç (Meta, üçüncü taraf
  araçla yapılan videoya etiketi kendisi koymayabilir). AI insan görünüyorsa ibare videonun içinde de olsun (TR).
- Fiyat: ICE-01 (`ortak/kurallar.md`). Reklam
  kreatifinde ekranda fiyat pazar kartı kararıyla (TR fiyat kancası GÖZLEM). İndirim/stok/yorum uydurma.

## DM otomasyonu notu (kullanıcıya)
Instagram/Meta otomasyonunda anahtar kelime birebir ve büyük-küçük harfe duyarlı eşleşir: aynı kelimenin
`KELİME`, `Kelime`, `kelime` hâllerini ekle. Yanıt birkaç dakika gecikebilir.

## Ölçüm notu (kullanıcıya)
48. saatte (≥ 2.000 izlenme): paylaşım/izlenme ≥ %0,61 ve beğeni/izlenme ≥ %1,01 → kazanan; aynı klip setine yeni
kancalarla seri yap. Hiçbiri tutmazsa kancayı değil **görüntüyü** (şablon / ilk kare) değiştir.
Eşikler ve 10 varyasyonluk test planı: `<eklenti kökü>/skills/ai-video-kreatif/referans/olcum-ve-test-plani.md`.

## Mağaza koluna geri dönüş: `magaza/video-paketi.json` (mağaza kolu mağazayı kurduysa)
`python3 "<eklenti kökü>/ortak/paket.py" video-yaz is/NN/teslim --cikti is/NN/magaza/video-paketi.json [--pdp VNN] [--hero VNN] --dil <tr|en|yok>`
teslim klasöründeki her MP4'ü ölçer (ölçü, süre), `video-paketi.json` yazar ve `is/NN/magaza/` altındaki `urun-paketi.json` +
`magaza-paketi.json` ile zincir kontrolü yapar (para birimi, altyazı dili). Çıkış 0 olmadan dosya teslim edilmez.
- Varsayılan kullanım `reklam`: mağaza kolu bunları mağazaya YÜKLEMEZ.
- `--pdp VNN`: ürün sayfası galerisine girecek video (ürünü net gösteren, "yorumlara yaz" CTA'sı olmayan sürüm). Galerinin
  son sıralarına girer; ilk görselin (yazısız ürün karesi) yerini almaz.
- `--hero VNN`: ana sayfa üst bölümü için. Hangi videonun mağazaya gireceğine kullanıcı karar verir (KARARLAR.md).
- `--dil`: ekran yazısının dili; yazısız videoda `yok`.
Lider `video-paketi.json` ve işaretli MP4'leri mağaza koluna (`magaza-kurucu` › `shopify-kurulum`, `paket.py video-sec`) verir.

## Teslim raporu (≤ 6 satır)
Dosya yolları · süre/çözünürlük/LUFS (betik satırı) · kırpılan/yeniden üretilen klipler (saniyesiyle) · harcanan kredi ·
kalan kusurlar · varsayımlar. Son satır: "Kalan senaryoları üretmemi istersen 'devam' yaz." (yeni kredi onayıyla)
