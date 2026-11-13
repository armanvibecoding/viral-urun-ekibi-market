// Google Flow'a başlangıç karesi yükleme (Claude in Chrome). Flow'un "Yükle" düğmesi dosya girişini tıklama
// anında oluşturup siliyor; setFiles boşa düşüyor. Çalışan yöntem (ölçüldü): gizli kalıcı bir <input type=file>
// ekle -> file_upload aracıyla dosyayı ona ver -> açık menü/perde (.cdk-overlay-backdrop) öğelerini kaldır ->
// DataTransfer ile medya alanına dragenter/dragover/drop gönder. Arayüz değişebilir: kare medya alanında
// GÖRÜNMEZSE kullanıcıdan tek bir sürükle-bırak iste. İlk yüklemede Flow "kullanım hakları" onayı sorar:
// kullanıcı bir kez kabul eder.

// ADIM 1 (javascript_tool): gizli girişi ekle.
(() => {
  let i = document.getElementById('ek-dosya');
  if (!i) { i = document.createElement('input'); i.type = 'file'; i.id = 'ek-dosya';
    i.accept = 'image/*'; i.style.display = 'none'; document.body.appendChild(i); }
  return 'hazır: #ek-dosya';
})();

// ADIM 2: file_upload aracıyla dosyayı '#ek-dosya' öğesine ver (find/read_page ile ref'ini al).

// ADIM 3 (javascript_tool): perdeyi kaldır ve medya alanına bırak. HEDEF seçicisini read_page ile doğrula;
// bulunamazsa sayfanın ortasındaki öğeye bırakılır.
(() => {
  const i = document.getElementById('ek-dosya');
  if (!i || !i.files.length) return 'dosya yok: önce ADIM 2';
  document.querySelectorAll('.cdk-overlay-backdrop').forEach(e => e.remove());
  const HEDEF = document.querySelector('[aria-label*="medya" i], [aria-label*="media" i], main')
    || document.elementFromPoint(innerWidth / 2, innerHeight / 2);
  const dt = new DataTransfer(); dt.items.add(i.files[0]);
  for (const t of ['dragenter', 'dragover', 'drop'])
    HEDEF.dispatchEvent(new DragEvent(t, { bubbles: true, cancelable: true, dataTransfer: dt }));
  return 'bırakıldı: ' + i.files[0].name + ' -> ' + (HEDEF.getAttribute('aria-label') || HEDEF.tagName);
})();
// Sonra ekran görüntüsüyle kareyi medya alanında GÖR (yükleme %100). Görmeden üretime geçme.
