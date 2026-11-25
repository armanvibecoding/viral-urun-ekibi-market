#!/bin/sh
# kalibre.sh — iPhone Yansıtma penceresini bulur, ilk ekran görüntüsünü alır ve konum.env'yi (yoksa) varsayılanlarla yazar.
# Sabit ekran koordinatı yoktur: tüm tık/kaydırma noktaları her çağrıda pencere konumundan hesaplanır.
# Pencere İÇİNDEKİ düğmelerin yeri (geri oku, kullanıcı adı, arama kutusu) iPhone modeline göre değişebilir:
# bu yüzden ip.png'yi AÇIP bakmak ve konum.env'yi düzeltmek gerekir (KALİBRASYON GEREKLİ).
. "$(dirname "$0")/ortak.sh"
pencere || exit 1
echo "pencere (mantıksal nokta): x=$X y=$Y genişlik=$W yükseklik=$H"
if [ ! -f "$D/konum.env" ]; then
  cat > "$D/konum.env" <<KON
# ip.png (900 px yükseklik) koordinatları. Başlangıç değerleri tek bir iPhone'da ölçüldü — ip.png'de DOĞRULA.
GERI_X=35; GERI_Y=120      # sol üst geri oku
HESAP_X=90; HESAP_Y=751    # Reels videosunda kullanıcı adı
ARAMA_X=190; ARAMA_Y=118   # Ara sekmesinde arama kutusu
KON
  echo "konum.env yazıldı (varsayılan): $D/konum.env"
  echo "KALİBRASYON UYARISI: bu başlangıç koordinatları TEK bir iPhone modelinde ölçüldü. Senin iPhone'un ekran oranı farklıysa tıklamalar yanlış yere gider; ip.png'yi aç, geri oku / kullanıcı adı / arama kutusunu kontrol et, gerekirse konum.env'yi düzelt."
fi
[ -f "$D/klavye" ] || echo us > "$D/klavye"
"$D/ekran.sh" || exit 1
echo "SIRADAKİ: $IP dosyasını aç; geri oku / kullanıcı adı / arama kutusu konum.env'deki noktalarda mı bak, değilse düzelt."
