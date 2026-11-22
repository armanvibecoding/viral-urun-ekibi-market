#!/bin/sh
# izle.sh AD [kare=8] [aralik_sn=3] — açık videoyu izlerken kare yakalar, kontakt sayfası yapar:
#   <proje>/is/kesfet/kareler/AD/sayfa.jpg  (AD: hesap adı, yalnız harf/rakam/-)
. "$(dirname "$0")/ortak.sh"
[ -n "$1" ] || { echo "kullanım: izle.sh AD [kare] [aralik_sn]" >&2; exit 2; }
N=${2:-8}; T=${3:-3}; O="$PROJE/is/kesfet/kareler/$1"; mkdir -p "$O"
pencere || exit 1
j=1; while [ $j -le "$N" ]; do
  /usr/sbin/screencapture -x -R"$X,$((Y + 40)),$W,$((H - 80))" "$O/k$(printf %02d $j).png"; sleep "$T"; j=$((j + 1))
done
python3 "$D/pano.py" "$O" "$O/sayfa.jpg"
