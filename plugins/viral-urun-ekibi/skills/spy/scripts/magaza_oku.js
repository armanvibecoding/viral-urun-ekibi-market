// spy · magaza_oku.js
// Kısa listedeki Shopify mağazalarının /products.json?limit=250 verisini insan hızında (8–15 sn arayla, sırayla) okur.
// Herhangi bir Shopify mağaza sekmesinde javascript_tool ile çalıştır (o sekmeden diğer mağazalara CORS açık — ölçüldü).
// Girdi — `magaza_gecis.py liste` çıktısındaki satırı aynı çağrıda üste koy:
//   window.__REKLAMAVI_MAGAZALAR = [{alan: 'ornek.com', yollar: ['urun-handle']}, ...];
// Birikim: localStorage['__reklamavi_magaza'] → meta_aktar.js (window.__REKLAMAVI_KAYNAK='magaza') ile oku.
// Satır: alan · durum(OK/KAPALI/HATA-<kod>) · urun_sayisi · ilk_urun · son_urun · medyan_fiyat · ana_urun · ana_urun_eklenme · ana_fiyat · ana_cizili · ana_handle
(() => {
  const liste = window.__REKLAMAVI_MAGAZALAR;
  if (!Array.isArray(liste) || !liste.length) return 'HATA: window.__REKLAMAVI_MAGAZALAR boş';
  if (window.__reklamavi_magaza_calisiyor) return 'zaten çalışıyor: ' + localStorage.getItem('__reklamavi_magaza_durum');
  window.__reklamavi_magaza_calisiyor = true;
  const iki = n => String(n).padStart(2, '0');
  const d = new Date();
  const okuma = `${d.getFullYear()}-${iki(d.getMonth() + 1)}-${iki(d.getDate())}`;
  const ANAHTAR = '__reklamavi_magaza';
  let k;
  try { k = JSON.parse(localStorage.getItem(ANAHTAR) || 'null'); } catch (e) { k = null; }
  if (!k || k.okuma !== okuma) k = { okuma, sira: [], sonuc: {} };
  const bekle = ms => new Promise(r => setTimeout(r, ms));
  const medyan = a => { if (!a.length) return ''; const s = a.slice().sort((x, y) => x - y); const m = Math.floor(s.length / 2); return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
  (async () => {
    let i = 0;
    for (const m of liste) {
      i++;
      const alan = String(m.alan || '').toLowerCase().replace(/^www\./, '');
      if (!alan || k.sonuc[alan]) continue;
      let satir;
      try {
        const r = await fetch(`https://${alan}/products.json?limit=250`, { credentials: 'omit' });
        if (r.status === 401 || r.status === 402 || r.status === 404 || r.status === 423) satir = [alan, 'KAPALI', '', '', '', '', '', '', '', '', ''];
        else if (!r.ok) satir = [alan, 'HATA-' + r.status, '', '', '', '', '', '', '', '', ''];
        else {
          const j = await r.json();
          const p = Array.isArray(j.products) ? j.products : [];
          if (!p.length) satir = [alan, 'KAPALI', '0', '', '', '', '', '', '', '', ''];
          else {
            const tarih = x => String(x.created_at || x.published_at || '').slice(0, 10);
            const tarihler = p.map(tarih).filter(Boolean).sort();
            const fiyat = x => parseFloat(((x.variants || [])[0] || {}).price);
            const fiyatlar = p.map(fiyat).filter(v => !isNaN(v));
            const yollar = (m.yollar || []).map(String);
            const ana = p.find(x => yollar.includes(x.handle)) || p.slice().sort((a, b) => tarih(a) < tarih(b) ? -1 : 1)[0];
            const v0 = (ana.variants || [])[0] || {};
            satir = [alan, 'OK', String(p.length), tarihler[0] || '', tarihler[tarihler.length - 1] || '', String(medyan(fiyatlar)),
              String(ana.title || ''), tarih(ana), String(v0.price || ''), String(v0.compare_at_price || ''), String(ana.handle || '')];
          }
        }
      } catch (e) { satir = [alan, 'HATA-ag', '', '', '', '', '', '', '', '', '']; }
      k.sira.push(alan); k.sonuc[alan] = satir;
      localStorage.setItem(ANAHTAR, JSON.stringify(k));
      localStorage.setItem(ANAHTAR + '_durum', JSON.stringify({ okunan: i, toplam: liste.length, bitti: false }));
      if (i < liste.length) await bekle(8000 + Math.random() * 7000);
    }
    localStorage.setItem(ANAHTAR + '_durum', JSON.stringify({ okunan: i, toplam: liste.length, bitti: true }));
    window.__reklamavi_magaza_calisiyor = false;
  })();
  return `başladı: ${liste.length} mağaza, 8–15 sn arayla (~${Math.round(liste.length * 11.5 / 60)} dk). Durum: localStorage '__reklamavi_magaza_durum'`;
})();
