#!/bin/sh
# kalibre.sh kırma testi (macOS/iPhone gerekmez): ortak.sh ve ekran.sh sahtelenir; konum.env yeni yazılırken uyarı çıkmalı,
# konum.env zaten varsa (kullanıcı doğrulamış) uyarı TEKRAR çıkmamalı. Çıkış 0 = hepsi geçti.
BURADA=$(cd "$(dirname "$0")" && pwd)
T=$(mktemp -d "${TMPDIR:-/tmp}/kalibre_test.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
cp "$BURADA/kalibre.sh" "$T/kalibre.sh"
cat > "$T/ortak.sh" <<'ORT'
D="$(dirname "$0")/ekip-arac"; mkdir -p "$D"; IP="$D/ip.png"; X=1; Y=2; W=3; H=4
pencere() { return 0; }
ORT
printf '#!/bin/sh\nexit 0\n' > "$T/ekran.sh" && mkdir -p "$T/ekip-arac" && cp "$T/ekran.sh" "$T/ekip-arac/ekran.sh" && chmod +x "$T/ekip-arac/ekran.sh"
ok=0; fail=0
kontrol() { if [ "$2" = "0" ]; then ok=$((ok+1)); echo "GEÇTİ $1"; else fail=$((fail+1)); echo "KALDI $1"; fi; }
C1=$(sh "$T/kalibre.sh" 2>&1)
echo "$C1" | grep -q "KALİBRASYON UYARISI"; kontrol "konum.env yok -> varsayılan yazılır ve KALİBRASYON UYARISI çıkar" $?
[ -f "$T/ekip-arac/konum.env" ]; kontrol "konum.env yazıldı" $?
C2=$(sh "$T/kalibre.sh" 2>&1)
echo "$C2" | grep -q "KALİBRASYON UYARISI"; r=$?; [ "$r" = "1" ]; kontrol "KIRMA konum.env zaten var -> uyarı tekrar çıkmaz" $?
echo "TOPLAM: $((ok+fail)) test, $fail kaldı"
[ "$fail" = "0" ]
