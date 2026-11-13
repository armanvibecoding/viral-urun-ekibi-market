// ChatGPT sohbetindeki SON üretilen görseli indirir (Claude in Chrome -> javascript_tool içine yapıştır).
// __AD__ yerine dosya adını yaz (ör. V01_S1.png). Görsel üretimi BİTMEDEN çalıştırma: önceki kare iner.
// Dönen değer: [görsel sayısı, bayt]. İnen dosya tarayıcının İndirilenler klasörüne düşer;
// sonra: python3 kare_hazirla.py <indirilen> is/NN-urun/kareler/V01_S1.png --referans <orijinal ürün fotoğrafı>
const AD = '__AD__';
const imgs = [...document.querySelectorAll('main img')].filter(i =>
  /^(Oluşturulan görsel|Generated image)/i.test(i.alt || '') && i.naturalWidth >= 900);
if (!imgs.length) throw new Error('Üretilmiş görsel bulunamadı (alt metni farklı olabilir)');
const b = await (await fetch(imgs[imgs.length - 1].src)).blob();
const a = document.createElement('a');
a.href = URL.createObjectURL(b); a.download = AD; document.body.appendChild(a); a.click();
[imgs.length, b.size];
