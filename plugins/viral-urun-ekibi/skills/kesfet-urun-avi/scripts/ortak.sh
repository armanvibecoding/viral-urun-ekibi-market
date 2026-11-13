# ortak.sh — diğer iPhone betiklerinin ortak parçası (doğrudan çalıştırılmaz, `. ortak.sh` ile yüklenir).
# D = araç klasörü (kur.sh'nin kopyaladığı yer), PROJE = kullanıcının proje klasörü, GECICI = geçici dosyalar.
D=$(cd "$(dirname "$0")" && pwd)
PROJE=${CLAUDE_PROJECT_DIR:-$PWD}
GECICI=${KESFET_GECICI:-${TMPDIR:-/tmp}/kesfet}
mkdir -p "$GECICI"
IP="$GECICI/ip.png"
# Kalibrasyon değerleri (kalibre.sh yazar). Yoksa varsayılanlar — mutlaka ekran görüntüsüyle doğrulanır.
GERI_X=35; GERI_Y=120; HESAP_X=90; HESAP_Y=751; ARAMA_X=190; ARAMA_Y=118
[ -f "$D/konum.env" ] && . "$D/konum.env"

# pencere: iPhone Yansıtma penceresinin mantıksal konumu → X Y W H değişkenleri. Bulamazsa 1 döner.
pencere() {
  for ad in "iPhone Mirroring" "iPhone Yansıtma"; do
    B=$(osascript -e "tell application \"System Events\" to tell process \"$ad\" to get {position, size} of window 1" 2>/dev/null | tr -d ' ')
    [ -n "$B" ] && break
  done
  [ -n "$B" ] || { echo "HATA: iPhone Yansıtma penceresi bulunamadı (uygulama açık mı, iPhone kilitli/kullanımda mı?)" >&2; return 1; }
  X=$(echo "$B" | cut -d, -f1); Y=$(echo "$B" | cut -d, -f2); W=$(echo "$B" | cut -d, -f3); H=$(echo "$B" | cut -d, -f4)
}

# onde: iPhone penceresi öndeyse 0 döner
onde() {
  for ad in "iPhone Mirroring" "iPhone Yansıtma"; do
    [ "$(osascript -e "tell application \"System Events\" to tell process \"$ad\" to get frontmost" 2>/dev/null)" = true ] && return 0
  done
  return 1
}

one_getir() { open -a "iPhone Mirroring" 2>/dev/null || open -a "iPhone Yansıtma" 2>/dev/null; sleep 1; }
