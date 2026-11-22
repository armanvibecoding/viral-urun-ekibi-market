#!/bin/sh
# ekran.sh [dosya] — iPhone Yansıtma penceresini yakalar, 900 px yüksekliğe küçültür (varsayılan: $GECICI/ip.png).
# Bu görüntüdeki koordinatlar dokun.sh'nin kullandığı koordinatlardır.
. "$(dirname "$0")/ortak.sh"
O=${1:-$IP}
pencere || exit 1
/usr/sbin/screencapture -x -R"$X,$Y,$W,$H" "$O" || { echo "HATA: ekran yakalanamadı — Sistem Ayarları > Gizlilik > Ekran Kaydı izni gerekli" >&2; exit 1; }
sips -Z 900 "$O" >/dev/null && echo "$O (pencere=$X,$Y,$W,$H)"
