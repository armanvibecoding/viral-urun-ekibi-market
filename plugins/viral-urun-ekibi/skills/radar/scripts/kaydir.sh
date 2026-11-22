#!/bin/sh
# kaydir.sh asagi|yukari|sonraki [adet=1] — pencere ortasında gerçek tekerlek olayı (kay). Koordinat pencereden hesaplanır.
#   asagi/yukari: ızgarada ~yarım ekran · sonraki: Reels'te bir sonraki video (hızlı fiske)
# Adım büyüklükleri tek bir makinede ölçüldü; kaymıyorsa KAY_TIK / KAY_PX ile artır.
. "$(dirname "$0")/ortak.sh"
pencere || exit 1
onde || one_getir
onde || { echo "HATA: iPhone penceresi önde değil, kaydırmıyorum" >&2; exit 1; }
CX=$((X + W / 2)); CY=$((Y + H * 60 / 100))
case "$1" in
  asagi)   T=${KAY_TIK:-50};  P=${KAY_PX:-10}; M=8 ;;
  yukari)  T=-${KAY_TIK:-50}; P=${KAY_PX:-10}; M=8 ;;
  sonraki) T=${KAY_TIK:-25};  P=${KAY_PX:-40}; M=4 ;;
  *) echo "kullanım: kaydir.sh asagi|yukari|sonraki [adet]" >&2; exit 2 ;;
esac
i=0; while [ $i -lt "${2:-1}" ]; do "$D/kay" "$CX" "$CY" "$T" "$P" "$M"; sleep 2; i=$((i + 1)); done
sleep 1; "$D/ekran.sh" >/dev/null && echo "$IP"
