# Ekran içeriğini kurguda bindirme (istisna)

**Kural:** ekran içeriği başlangıç karesinde üretilir (görsel model hale, cam yansıması ve perspektifi kendisi yapar),
klipte `SCREEN LOCK` ile sabit kalır, değişim kesimde olur (`ai-video-kreatif` "Kare ve klip kuralları").
Düz renge sonradan daire bindirme reddedildi: açılı kadrajda elips taşması, yansımasız cam, yanlış hale rengi.
**Bindirme yalnız istisna:** karede üretilemeyen hareketli içerik (döngü animasyonu) gerektiğinde ve şu üç şartla:
maske ekranın perspektifine uyar (açılı kadrajda elips/dikdörtgen `--en-boy`), cam yansıması katmanı eklenir,
kumlanma ve parlaklık kareye eşlenir. Biri sağlanmazsa bindirme yapılmaz, içerik karede üretilir.
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
- Geçiş karelerinde aynı anda en fazla 2 katman (ör. çıkan + giren plan); ayırıcı çizgi/bölme ürün kırpımının üstünden
  geçmez. Kontrol: geçiş anlarının ±0,5 sn'sinde 10 fps pano.
- Kırmızı-mavi dönüşümlü yanıp sönme yok (polis ışığı çağrışımı); hızlı flaş yok; animasyon hızı ≤ 2 Hz.
- Ekran parlaklığı karedeki ışıkla uyumlu: abartılı parlaklık ürünü olduğundan farklı gösterir = yanıltıcı görüntü.
- Islak zemin yansıması, cam yansıması gibi ek gerçekçilik katmanları bu betikte yok; gerekiyorsa ayrı ffmpeg katmanıyla
  ve yine 4 fps panoyla kontrol edilerek eklenir.
