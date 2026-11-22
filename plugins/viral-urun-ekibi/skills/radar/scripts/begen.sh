#!/bin/sh
# begen.sh — açık Reels videosunu ortasına çift dokunarak beğenir. YALNIZ kullanıcı izin verdiyse:
# .ekip/KARARLAR.md içinde "beğeni izni: evet" satırı yoksa çalışmaz.
. "$(dirname "$0")/ortak.sh"
grep -qi "beğeni izni: evet" "$PROJE/.ekip/KARARLAR.md" 2>/dev/null || { echo "DUR: kullanıcı beğeni izni vermedi (.ekip/KARARLAR.md)" >&2; exit 3; }
pencere || exit 1
onde || { echo "HATA: iPhone penceresi önde değil" >&2; exit 1; }
CX=$((X + W / 2)); CY=$((Y + H * 45 / 100))
"$D/tikla" $CX $CY; sleep 0.12; "$D/tikla" $CX $CY; sleep 1.5; "$D/ekran.sh" >/dev/null && echo "$IP"
