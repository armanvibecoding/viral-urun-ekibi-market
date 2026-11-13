#!/bin/sh
# Paketi hazırlayanın kimliğini ele veren izleri arar. Eşleşme varsa dosya:satır basar, 1 ile çıkar; temizse 0.
# Kara liste DEPODA DEĞİL, hazırlayanın bilgisayarında durur (liste kimliği ele vereceği için):
#   ${YASAK_DOSYASI:-$HOME/.config/viral-urun-ekibi/yasak.txt}   — satır başına bir ERE deseni (büyük/küçük harf duyarsız)
#   ${IZIN_DOSYASI:-$HOME/.config/viral-urun-ekibi/myshopify-izin.txt} — izinli başka mağaza alt alan adları (a|b|c)
# Kullanım: sh docs/anonim_kontrol.sh [klasör]   (varsayılan: deponun tamamı, .git hariç)
KOK="$(cd "$(dirname "$0")/.." && pwd)"
HEDEF="${1:-$KOK}"
YASAK_DOSYASI="${YASAK_DOSYASI:-$HOME/.config/viral-urun-ekibi/yasak.txt}"
IZIN_DOSYASI="${IZIN_DOSYASI:-$HOME/.config/viral-urun-ekibi/myshopify-izin.txt}"
if [ ! -s "$YASAK_DOSYASI" ]; then
  echo "HATA: kara liste yok: $YASAK_DOSYASI (kendi adın, e-postan, mağaza/proje adların — satır başına bir desen)"; exit 2
fi
IZIN="$(cat "$IZIN_DOSYASI" 2>/dev/null)"; [ -z "$IZIN" ] && IZIN='^$'
TMP="$(mktemp)"
while IFS= read -r desen; do
  [ -z "$desen" ] && continue
  grep -rnIiE --exclude-dir=.git -- "$desen" "$HEDEF" 2>/dev/null | awk '{print "[eşleşme] " $0}'
done < "$YASAK_DOSYASI" > "$TMP"
grep -rnIoiE --exclude-dir=.git -- '[a-z0-9-]+\.myshopify\.com' "$HEDEF" 2>/dev/null \
  | grep -viE "(^|:)($IZIN)\.myshopify\.com" | awk '{print "[myshopify] " $0}' >> "$TMP"
if [ -s "$TMP" ]; then
  cat "$TMP"; echo "---"; echo "ANONİMLİK İHLALİ: $(wc -l < "$TMP" | tr -d ' ') satır"; rm -f "$TMP"; exit 1
fi
rm -f "$TMP"; echo "temiz: $HEDEF"; exit 0
