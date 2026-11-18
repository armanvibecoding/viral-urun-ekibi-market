#!/bin/sh
# Paketi hazırlayanın kimliğini ele veren izleri arar. Eşleşme varsa dosya:satır basar, 1 ile çıkar; temizse 0.
# Kara liste DEPODA DEĞİL, hazırlayanın bilgisayarında durur (liste kimliği ele vereceği için):
#   ${YASAK_DOSYASI:-$HOME/.config/viral-urun-ekibi/yasak.txt}   — satır başına bir ERE deseni (büyük/küçük harf duyarsız)
#   ${IZIN_DOSYASI:-$HOME/.config/viral-urun-ekibi/myshopify-izin.txt} — izinli başka mağaza alt alan adları (a|b|c)
# Kullanım: sh docs/anonim_kontrol.sh [klasör]   (varsayılan: deponun tamamı, .git hariç)
# Üçüncü taraf (HyperFrames, Apache-2.0) dosyaları kara listeden YALNIZ imzaları tutuyorsa muaftır:
#   plugins/viral-urun-ekibi/licenses/hyperframes.sha256 (eklenti köküne göreli yollar). Dosya değişmiş ya da eksikse
#   ihlal sayılır; listede olmayan yeni dosya muaf değildir. Bilinçli değişiklikten sonra imzayı yeniden üret:
#   cd plugins/viral-urun-ekibi && find skills/hyperframes skills/hyperframes-cli skills/hyperframes-registry skills/media-use \
#     -type f | LC_ALL=C sort | xargs shasum -a 256 > licenses/hyperframes.sha256
KOK="$(cd "$(dirname "$0")/.." && pwd)"
HEDEF="${1:-$KOK}"
YASAK_DOSYASI="${YASAK_DOSYASI:-$HOME/.config/viral-urun-ekibi/yasak.txt}"
IZIN_DOSYASI="${IZIN_DOSYASI:-$HOME/.config/viral-urun-ekibi/myshopify-izin.txt}"
if [ ! -s "$YASAK_DOSYASI" ]; then
  echo "HATA: kara liste yok: $YASAK_DOSYASI (kendi adın, e-postan, mağaza/proje adların — satır başına bir desen)"; exit 2
fi
IZIN="$(cat "$IZIN_DOSYASI" 2>/dev/null)"; [ -z "$IZIN" ] && IZIN='^$'
TMP="$(mktemp)"; MUAF="$(mktemp)"
EKLENTI="$KOK/plugins/viral-urun-ekibi"; IMZA="$EKLENTI/licenses/hyperframes.sha256"
if [ -f "$IMZA" ]; then
  if command -v shasum >/dev/null; then SHA="shasum -a 256"; else SHA="sha256sum"; fi
  # Tutmayan satır = ihlal; tutan dosyanın mutlak yolu muaf listesine.
  ( cd "$EKLENTI" && $SHA -c "$IMZA" 2>/dev/null ) | while IFS= read -r satir; do
    yol="${satir%: *}"; durum="${satir##*: }"
    if [ "$durum" = "OK" ]; then echo "$EKLENTI/$yol:" >> "$MUAF"; else echo "[üçüncü-taraf] imza tutmuyor ($durum): $yol"; fi
  done > "$TMP.ut"
fi
muaf_sil() { if [ -s "$MUAF" ]; then awk 'NR==FNR{m[++n]=$0;next}{for(i=1;i<=n;i++) if(index($0,m[i])==1) next; print}' "$MUAF" -; else cat; fi; }
while IFS= read -r desen; do
  [ -z "$desen" ] && continue
  grep -rnIiE --exclude-dir=.git -- "$desen" "$HEDEF" 2>/dev/null | muaf_sil | awk '{print "[eşleşme] " $0}'
done < "$YASAK_DOSYASI" > "$TMP"
[ -f "$TMP.ut" ] && cat "$TMP.ut" >> "$TMP"; rm -f "$TMP.ut" "$MUAF"
grep -rnIoiE --exclude-dir=.git -- '[a-z0-9-]+\.myshopify\.com' "$HEDEF" 2>/dev/null \
  | grep -viE "(^|:)($IZIN)\.myshopify\.com" | awk '{print "[myshopify] " $0}' >> "$TMP"
if [ -s "$TMP" ]; then
  cat "$TMP"; echo "---"; echo "ANONİMLİK İHLALİ: $(wc -l < "$TMP" | tr -d ' ') satır"; rm -f "$TMP"; exit 1
fi
rm -f "$TMP"; echo "temiz: $HEDEF"; exit 0
