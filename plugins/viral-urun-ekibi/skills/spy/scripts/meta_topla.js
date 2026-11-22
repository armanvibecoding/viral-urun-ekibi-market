// spy · meta_topla.js
// Meta Reklam Kütüphanesi SONUÇ sayfasında (facebook.com/ads/library/?...) javascript_tool ile çalıştırılır.
// Yalnız okur ve insan hızında kaydırır (4–7 sn); tıklamaz, beğenmez, mesaj atmaz.
// Kartları localStorage['__reklamavi'] içinde biriktirir; javascript_tool çıktısı ~1.000 karakterde kesildiği için
// veri sonra meta_aktar.js ile okunur.
// Ayar (isteğe bağlı) — aynı çağrıda bu dosyanın ÜSTÜNE bir satır ekle:
//   window.__REKLAMAVI_AYAR = {nis: 'evcil', aile: 'U', limit: 300, dakika: 20};
// Durum okumak: JSON.parse(localStorage.getItem('__reklamavi_durum'))
// Erken durdurmak: localStorage.setItem('__reklamavi_dur', '1')
(() => {
  const AYAR = Object.assign({ nis: '-', aile: 'U', siralama: '', limit: 300, dakika: 20, bosTur: 5, sifirla: false },
    window.__REKLAMAVI_AYAR || {});
  const ANAHTAR = '__reklamavi';
  const url = new URL(location.href);
  if (!/\/ads\/library/.test(url.pathname)) return 'HATA: bu sayfa Meta Reklam Kütüphanesi değil';
  const ulke = (url.searchParams.get('country') || '').toUpperCase();
  const sorgu = (url.searchParams.get('q') || '').replace(/^["“]|["”]$/g, '').trim();
  const mod = url.searchParams.get('sort_data[mode]') || '';
  const siralama = AYAR.siralama || (mod === 'relevancy_monthly_grouped' ? 'yeni' : 'gosterim');
  const iki = n => String(n).padStart(2, '0');
  const d = new Date();
  const baslangic = `${d.getFullYear()}-${iki(d.getMonth() + 1)}-${iki(d.getDate())}T${iki(d.getHours())}:${iki(d.getMinutes())}`;

  const KOD_ETIKET = /^(Kütüphane Kodu|Library ID|Bibliotheks-ID|ID de la bibliothèque|Identificador de la biblioteca|ID de la biblioteca)\s*:?/i;
  const KOD_SAYI = /(Kütüphane Kodu|Library ID|Bibliotheks-ID|ID de la bibliothèque|Identificador de la biblioteca|ID de la biblioteca)\s*:?\s*(\d{6,})/i;
  const KOD_HEPSI = /(Kütüphane Kodu|Library ID|Bibliotheks-ID|ID de la bibliothèque|Identificador de la biblioteca|ID de la biblioteca)\s*:?\s*\d{6,}/gi;
  const TARIH = /(yayınlanmaya başladı|Started running|Läuft seit|Schaltung seit|Diffusion commencée|Début de la diffusion|Empezó a circular|Se empezó a publicar)/i;
  const KOPYA = /(\d+)\s*(reklam|ads?|Anzeigen|publicités|anuncios)\b[\s\S]{0,60}?(kreatif|creative|Werbemittel|contenu|contenido|creatividad)/i;
  const CTA = /(Şimdi Alışveriş Yap|Alışverişe Başla|Daha Fazla Bilgi Al|Hemen Sipariş Ver|Sipariş Ver|Satın Al|Shop Now|Shop now|Learn More|Learn more|Order Now|Order now|Buy Now|Get Offer|Jetzt einkaufen|Mehr dazu|Jetzt bestellen|Acheter|En savoir plus|Commander|Comprar|Más información|Comprar ahora|Pedir ahora)/;
  const temiz = s => (s || '').replace(/[\t\r\n]+/g, ' ').replace(/\s+/g, ' ').trim();

  let kayit = null;
  try { kayit = JSON.parse(localStorage.getItem(ANAHTAR) || 'null'); } catch (e) { kayit = null; }
  const ayniSorgu = kayit && kayit.meta && kayit.meta.ulke === ulke && kayit.meta.sorgu === sorgu && kayit.meta.baslangic.slice(0, 10) === baslangic.slice(0, 10);
  if (!kayit || AYAR.sifirla || !ayniSorgu) {
    kayit = { meta: { ulke, sorgu, nis: AYAR.nis, aile: AYAR.aile, siralama, baslangic }, sira: [], kartlar: {} };
  }

  const kodSay = el => ((el.textContent || '').match(KOD_HEPSI) || []).length;

  function linkCoz(href) {
    try {
      const u = new URL(href, location.href);
      if (/(^|\.)facebook\.com$/.test(u.hostname) && u.pathname.startsWith('/l.php')) {
        const hedef = u.searchParams.get('u');
        if (!hedef) return '';
        const h = new URL(hedef);
        return h.hostname + h.pathname;                 // sorgu dizgesi (utm vb.) atılır
      }
      if (/facebook\.com|fbcdn|instagram\.com\/accounts/.test(u.hostname)) return '';
      return u.hostname + u.pathname;
    } catch (e) { return ''; }
  }

  function kartOku(kok, kod) {
    const yapraklar = [...kok.querySelectorAll('span,div,a')].filter(e => e.childElementCount === 0);
    const tarihEl = yapraklar.find(e => TARIH.test(e.textContent || ''));
    const metin = kok.innerText || kok.textContent || '';
    const km = metin.match(KOPYA);
    const linkler = [...kok.querySelectorAll('a[href]')];
    let hedef = '';
    for (const a of linkler) { const h = linkCoz(a.getAttribute('href')); if (h) { hedef = h; break; } }
    let sayfa = '';
    for (const a of linkler) {
      const h = a.getAttribute('href') || '';
      const t = temiz(a.textContent);
      if (t && /facebook\.com\/(?!ads\/library|l\.php)/.test(h) && !KOD_ETIKET.test(t) && t.length < 80) { sayfa = t; break; }
    }
    let govde = '';
    const pre = kok.querySelector('[style*="pre-wrap"]');
    if (pre) govde = temiz(pre.textContent);
    if (!govde) {
      const adaylar = yapraklar.map(e => temiz(e.textContent)).filter(t => t.length > 30 && !TARIH.test(t) && !KOD_ETIKET.test(t));
      adaylar.sort((a, b) => b.length - a.length);
      govde = adaylar[0] || '';
    }
    const cm = metin.match(CTA);
    const medya = kok.querySelector('video') ? 'video' : (kok.querySelectorAll('img').length > 1 ? 'gorsel' : '');
    return [kod, temiz(sayfa), temiz(tarihEl ? tarihEl.textContent : ''), temiz(km ? km[0] : ''),
      tarihEl ? '1' : '0', hedef, cm ? cm[0] : '', medya, govde.slice(0, 500)];
  }

  function tara() {
    let yeni = 0;
    const yapraklar = [...document.querySelectorAll('span,div')].filter(e => e.childElementCount === 0 && KOD_ETIKET.test(temiz(e.textContent)));
    for (const y of yapraklar) {
      const m = temiz(y.textContent).match(KOD_SAYI) || temiz(y.parentElement ? y.parentElement.textContent : '').match(KOD_SAYI);
      if (!m) continue;
      const kod = m[2];
      if (kayit.kartlar[kod] && kayit.kartlar[kod][4] === '1') continue;
      let kok = y;
      while (kok.parentElement && kok.parentElement !== document.body && kodSay(kok.parentElement) === 1) kok = kok.parentElement;
      if (!kayit.kartlar[kod]) { kayit.sira.push(kod); yeni++; }
      kayit.kartlar[kod] = kartOku(kok, kod);
    }
    return yeni;
  }

  function kaydet(durum) {
    localStorage.setItem(ANAHTAR, JSON.stringify(kayit));
    localStorage.setItem(ANAHTAR + '_durum', JSON.stringify(Object.assign({ kart: kayit.sira.length, sorgu, ulke }, durum)));
  }

  if (window.__reklamavi_calisiyor) return 'zaten çalışıyor — durum: ' + localStorage.getItem(ANAHTAR + '_durum');
  window.__reklamavi_calisiyor = true;
  localStorage.removeItem(ANAHTAR + '_dur');
  const t0 = Date.now();
  const bekle = ms => new Promise(r => setTimeout(r, ms));
  (async () => {
    let bos = 0, tur = 0, sebep = '';
    try {
      while (true) {
        tur++;
        const yeni = tara();
        bos = yeni ? 0 : bos + 1;
        kaydet({ tur, bitti: false });
        if (kayit.sira.length >= AYAR.limit) { sebep = 'limit'; break; }
        if (bos >= AYAR.bosTur) { sebep = 'yeni kart gelmiyor (liste sonu ya da yükleme durdu)'; break; }
        if (Date.now() - t0 > AYAR.dakika * 60000) { sebep = 'süre'; break; }
        if (localStorage.getItem(ANAHTAR + '_dur') === '1') { sebep = 'elle durduruldu'; break; }
        window.scrollTo(0, document.documentElement.scrollHeight);
        window.dispatchEvent(new Event('scroll'));
        await bekle(4000 + Math.random() * 3000);
      }
    } catch (e) { sebep = 'hata: ' + e.message; }
    tara();
    kaydet({ tur, bitti: true, sebep });
    window.__reklamavi_calisiyor = false;
  })();
  return `başladı: ${ulke} "${sorgu}" (${siralama}) · mevcut kart ${kayit.sira.length} · limit ${AYAR.limit} · durum için localStorage '__reklamavi_durum'`;
})();
