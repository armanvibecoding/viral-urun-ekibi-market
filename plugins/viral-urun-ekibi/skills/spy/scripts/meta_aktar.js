// spy · meta_aktar.js
// localStorage'daki birikimi get_page_text ile okunacak düz metne çevirir (aynı origin'de 2. sekmede çalıştır).
// Sayfanın gövdesini <pre> ile DEĞİŞTİRİR — toplama sekmesinde değil, ayrı sekmede çalıştır.
// Ayar — aynı çağrıda üste bir satır:
//   window.__REKLAMAVI_PARCA = 1;          // hangi parça (1..N); her parça ≤40.000 karakter
//   window.__REKLAMAVI_KAYNAK = 'magaza';  // magaza_oku.js birikimi için (varsayılan: reklam)
//   window.__REKLAMAVI_INDIR = true;       // tek dosya olarak İndirilenler'e kaydet (izin verilirse en temiz yol)
// Çıktı biçimi meta_kayit.py / magaza_gecis.py tarafından denetlenir: kart sayısı ya da parça eksikse betik reddeder.
(() => {
  const PARCA_BOYU = 40000;
  const kaynak = window.__REKLAMAVI_KAYNAK === 'magaza' ? 'magaza' : 'reklam';
  const anahtar = kaynak === 'magaza' ? '__reklamavi_magaza' : '__reklamavi';
  let k;
  try { k = JSON.parse(localStorage.getItem(anahtar) || 'null'); } catch (e) { return 'HATA: birikim bozuk JSON'; }
  if (!k) return `HATA: bu origin'de ${anahtar} yok (toplama başka alan adında mı yapıldı?)`;
  const temiz = s => String(s == null ? '' : s).replace(/[\t\r\n]+/g, ' ').trim();
  let baslikTaban, satirlar;
  if (kaynak === 'reklam') {
    const m = k.meta;
    satirlar = k.sira.map(kod => k.kartlar[kod].map(temiz).join('\t'));
    baslikTaban = ['#REKLAMAVI v1', 'ulke=' + m.ulke, 'sorgu=' + temiz(m.sorgu), 'nis=' + temiz(m.nis), 'aile=' + m.aile,
      'siralama=' + m.siralama, 'baslangic=' + m.baslangic, 'kart=' + satirlar.length];
  } else {
    satirlar = k.sira.map(alan => k.sonuc[alan].map(temiz).join('\t'));
    baslikTaban = ['#REKLAMAVI-MAGAZA v1', 'okuma=' + k.okuma, 'adet=' + satirlar.length];
  }
  const parcalar = [[]];
  let boy = 0;
  for (const s of satirlar) {
    if (boy + s.length + 1 > PARCA_BOYU && parcalar[parcalar.length - 1].length) { parcalar.push([]); boy = 0; }
    parcalar[parcalar.length - 1].push(s);
    boy += s.length + 1;
  }
  const n = parcalar.length;
  const metin = i => [baslikTaban.concat('parca=' + i + '/' + n).join('\t')].concat(parcalar[i - 1]).join('\n');
  if (window.__REKLAMAVI_INDIR) {
    const tum = parcalar.map((_, i) => metin(i + 1)).join('\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([tum], { type: 'text/plain;charset=utf-8' }));
    a.download = `reklamavi-${kaynak}-${Date.now()}.txt`;
    document.body.appendChild(a); a.click(); a.remove();
    return `indirildi: ${a.download} · ${satirlar.length} satır, ${n} parça (tek dosyada)`;
  }
  const i = Math.min(Math.max(parseInt(window.__REKLAMAVI_PARCA || 1, 10), 1), n);
  const pre = document.createElement('pre');
  pre.id = 'reklamavi';
  pre.textContent = metin(i);
  document.body.replaceChildren(pre);
  return `parça ${i}/${n} gösteriliyor (${satirlar.length} satır toplam) — şimdi get_page_text`;
})();
