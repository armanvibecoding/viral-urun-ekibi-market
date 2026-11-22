#!/bin/sh
# dokun.sh PX PY [bekle_sn=3] — ip.png (900 px yükseklik) koordinatındaki noktaya gerçek tık, bekle, yeniden yakala.
. "$(dirname "$0")/ortak.sh"
[ $# -ge 2 ] || { echo "kullanım: dokun.sh PX PY [bekle_sn]" >&2; exit 2; }
pencere || exit 1
onde || one_getir
onde || { echo "HATA: iPhone penceresi önde değil, tıklamıyorum" >&2; exit 1; }
LX=$(echo "$X + $1 * $H / 900" | bc -l); LY=$(echo "$Y + $2 * $H / 900" | bc -l)
"$D/tikla" "$LX" "$LY"; sleep "${3:-3}"; "$D/ekran.sh" >/dev/null && echo "$IP"
