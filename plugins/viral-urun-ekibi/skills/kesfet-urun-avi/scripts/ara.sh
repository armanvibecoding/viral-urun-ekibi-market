#!/bin/sh
# ara.sh METIN — (Instagram Ara sekmesindeyken) arama kutusuna yazar, Enter'a basar, sonucu yakalar.
# Her adımda iPhone penceresinin önde olduğunu kontrol eder: değilse YAZMAZ (yazı başka uygulamaya gitmesin).
. "$(dirname "$0")/ortak.sh"
[ -n "$1" ] || { echo "kullanım: ara.sh METIN" >&2; exit 2; }
onde || one_getir; sleep 1
onde || { echo "HATA: iPhone penceresi önde değil, yazmıyorum" >&2; exit 1; }
"$D/dokun.sh" "$ARAMA_X" "$ARAMA_Y" 1 >/dev/null
onde || { echo "HATA: pencere kayboldu" >&2; exit 1; }
osascript -e 'tell application "System Events" to keystroke "a" using command down' -e 'tell application "System Events" to key code 51'
onde || { echo "HATA: pencere kayboldu" >&2; exit 1; }
python3 "$D/yaz.py" "${1#@}"; sleep 1
onde && [ "${ENTER:-1}" = 1 ] && osascript -e 'tell application "System Events" to key code 36'
sleep 3; "$D/ekran.sh" >/dev/null && echo "$IP — arama kutusundaki yazıyı kontrol et; bozuksa .ekip/arac/klavye (us|tr) değiştir"
