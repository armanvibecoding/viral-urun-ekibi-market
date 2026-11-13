# Ekran / yazı içeriğini kurguda bindirme

**İlke:** AI'a ekranda, tabelada, ambalaj yazısında görüntü çizdirilmez; 4 sn içinde değişir, harf/şekil bozulur.
Başlangıç karesinde ekran **kapalı siyah cam** ya da **düz tek renk** (bindirilecek animasyonun baskın rengi) üretilir;
Flow promptunda `SCREEN LOCK` (renk 4 sn sabit, desen/ikon/titreme yok — `kilit.txt` `SCREEN:` satırından betik ekler).
Animasyon kurguda maskeyle ekranın içine konur. Aynı klip seti farklı animasyonla yeniden kullanılabilir (aynı set, çok varyasyon).
Kamera yalnız **sabit / yavaş itme / yavaş yana kayma** (doğrusal hareket iki ölçümle izlenir); elde tutulan sahnede el "perfectly still".

## Adımlar (her klip)
1. **Animasyonu bir kez hazırla:** kare (ör. 1080×1080), 30 fps, birkaç saniyelik döngü; MP4 ya da PNG. Rakam/harf
   gereken içerik burada çizilir — okunaklı yazı yalnız bu katmanda. Özgün ve markasız olmalı (başka markanın logosu yok).
2. **Ölç:** `python3 ekran_bindir.py klip.mp4 --kareler` → `klip_ilk.png`, `klip_son.png`. Ekran merkezini (x, y) ve
   iç genişliğini (çerçeve hariç, px) KLİBİN kendi pikselinde iki karede not et.
3. **Bindir:** `python3 ekran_bindir.py klip.mp4 anim.mp4 klip_bindirmeli.mp4 --x0 X0 --y0 Y0 --d0 D0 --x1 X1 --y1 Y1 --d1 D1`
   (sabit kamerada yalnız x0/y0/d0). Dikdörtgen ekran: `--sekil dikdortgen --en-boy <yükseklik/genişlik>`.
   Işığa eşleme: `--parlaklik -0.15` (gündüz daha soluk) … `0.1` (gece); gece/IR kamerası sahnesinde `--gri`.
4. **Kontrol (zorunlu):** `python3 klip_qc.py klip_bindirmeli.mp4 --pano` → her karede bindirme ekranın içinde mi,
   kenardan > 3 px taşıyor mu? Taşıyorsa kamera hareketi doğrusal değil → klibi sabit kamerayla yeniden üret ya da
   taşan saniyeyi kırp. AI ekranın kendisinde desen/titreme üretmişse (kenardan sızar) → RED.
5. Kurgu ayarında bu klibi kullan; yazı (kanca, CTA) bindirmeden SONRA eklenir ve ekranı örtmez.

## Kurallar
- Kırmızı-mavi dönüşümlü yanıp sönme yok (polis ışığı çağrışımı); hızlı flaş yok; animasyon hızı ≤ 2 Hz.
- Ekran parlaklığı karedeki ışıkla uyumlu: abartılı parlaklık ürünü olduğundan farklı gösterir = yanıltıcı görüntü.
- Islak zemin yansıması, cam yansıması gibi ek gerçekçilik katmanları bu betikte yok; gerekiyorsa ayrı ffmpeg katmanıyla
  ve yine 4 fps panoyla kontrol edilerek eklenir.
