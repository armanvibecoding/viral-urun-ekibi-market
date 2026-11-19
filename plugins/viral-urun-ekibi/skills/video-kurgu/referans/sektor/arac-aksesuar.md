# Sektör eki: araç aksesuarı (ekranlı amblem, rozet, plaka çevresi ürünleri)

Yalnız bu sektördeki ürünlerde geçerlidir; genel kurgu kuralları `../kurgu-kurallari.md`, ürün kontratı `is/NN/kurgu/KURALLAR.md`.
Kaynağı tek ürün serisidir (ikinci üründe yeniden görülmeden genel kurala terfi etmez). Kapı: `kurgu_kontrol.py` (`urun`, `stok`,
`telefon`, `yazi_yeri`, `kanca` kuralları; eşikler betikte).

- **Yazı ürünü/plakayı kapatmaz:** yakın planda (kirp ≥ 1,3 ya da rozet/plaka kadrajın alt yarısında) yazı konumu ≤ 0,15.
  Panoda her yazının altında plaka rakamı ya da ürün ekranı varsa düzelt.
- **Telefon karosu = araç ekranı:** telefonda dokunulan içerik, sonraki her planda araç ekranında aynı içerik olarak kalır;
  aracın içerikleri arasında yoksa telefon planı kullanılmaz. Ekranda dokunuş yoksa `tik` sesi yok.
- **Ürün ilk 0,9 sn'de görünür** (2. tur eleştiri: geçen videoların hepsi değişmiş ekranı ilk karede ya da < 0,9 sn'de gösterdi;
  durağan stok plan en fazla 0,86 sn ve ilk plan değil). Söküm klibi sökülen rozetin logosunu göstermiyorsa söküm kancası kullanılmaz.
- **İlk 1,7 sn kancayı görüntüyle kanıtlar:** durağan stok geniş plan ile açma. Ya sonuç önce (değişmiş ekran yakın), ya
  rozete punch (kirp ≥ 1,4), ya söküm/kutu eylemi. Ortak klipteki ikon/araç rengi bu araçla uyuşmuyorsa ≤ 0,9 sn ve ilk
  plan olmaz. Kancadaki nesne ("star", "pump", "walk over") görüntüde yoksa kanca değişir.
