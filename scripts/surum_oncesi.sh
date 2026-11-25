#!/bin/sh
# Sürüm öncesi tek kapı (denetim 2026-11-25 #11): birim testleri + 7 sınav (--hepsi) + anonimlik. Hepsi GEÇMEDEN paket çıkmaz.
# Kullanım: sh scripts/surum_oncesi.sh [SINAV_CIKTI_KOK] [--referans-kok KLASOR]
#   SINAV_CIKTI_KOK   <kök>/<özellik>/<tur>/<vaka>/ düzeninde 7 sınavın çıktı kökü (ortam değişkeni de olur). Yoksa çıkış 2: ölçülmeyen sınav yeşil sayılmaz.
#   --referans-kok    referanslar.tsv yollarının çözüleceği klasör (ortam: SINAV_REFERANS_KOK)
#   FFMPEG_DIZIN      ffmpeg/ffprobe'un durduğu klasör (PATH'te yoksa); OCR ortamı ~/.local/share/viral-urun-ekibi/ocr-venv varsa kullanılır.
# Çıkış: 0 hepsi GEÇTİ · 1 en az bir KALDI · 2 kullanım hatası (sınav çıktı kökü yok) · 3 KALDI yok ama ölçülemeyen/bekleyen var (sürüm için yeterli DEĞİL).
# (geri_test.py bağımsız değişken ister, kendi başına test değildir: dışarıda.)  Birim testi çıkış 3 = ölçülemedi (ör. araç yok); tek satırlık özette ayrı sayılır ve sürümü engeller.
KOK="$(cd "$(dirname "$0")/.." && pwd)"
SINAV_KOK="${1:-$SINAV_CIKTI_KOK}"
[ "$#" -gt 0 ] && shift
REF="${SINAV_REFERANS_KOK:-}"
while [ "$#" -gt 0 ]; do case "$1" in --referans-kok) REF="$2"; shift 2;; *) echo "HATA: bilinmeyen bağımsız değişken: $1"; exit 2;; esac; done
[ -n "$FFMPEG_DIZIN" ] && PATH="$FFMPEG_DIZIN:$PATH"
export PATH
if [ -z "$SINAV_KOK" ] || [ ! -d "$SINAV_KOK" ]; then
  echo "SÜRÜM ÖNCESİ: KALDI — sınav çıktı kökü yok (SINAV_CIKTI_KOK ya da ilk bağımsız değişken). 7 sınav koşulmadan sürüm çıkmaz."; exit 2
fi
GECTI=0; KALDI=0; OLCULEMEDI=0; LISTE=""
TMP="$(mktemp)"
find "$KOK" \( -name '*_test.py' -o -name 'kirma_testi.py' -o -name 'test_hikaye.py' \) \
  -not -path '*/dist/*' -not -path '*/node_modules/*' -not -path '*/moduller/*' -not -path '*/media-use/*' -not -path '*/hf-sablonlar/*' -not -name 'geri_test.py' | sort > "$TMP"
while read -r T; do
  ( cd "$(dirname "$T")" && python3 "$(basename "$T")" >/dev/null 2>&1 </dev/null ); RC=$?
  case $RC in
    0) GECTI=$((GECTI+1));;
    3) OLCULEMEDI=$((OLCULEMEDI+1)); LISTE="$LISTE\n  olculemedi: ${T#$KOK/}";;
    *) KALDI=$((KALDI+1)); LISTE="$LISTE\n  KALDI(çıkış $RC): ${T#$KOK/}";;
  esac
done < "$TMP"
rm -f "$TMP"
echo "BİRİM TESTLERİ: GEÇTİ $GECTI · KALDI $KALDI · ölçülemedi $OLCULEMEDI"
[ -n "$LISTE" ] && printf "$LISTE\n"
HEPSI_ARG=""; [ -n "$REF" ] && HEPSI_ARG="--referans-kok $REF"
python3 "$KOK/scripts/sinav_kos.py" --hepsi "$SINAV_KOK" $HEPSI_ARG; SRC=$?
sh "$KOK/scripts/anonim_kontrol.sh" >/dev/null 2>&1; ARC=$?
echo "ANONİMLİK: $([ $ARC -eq 0 ] && echo GEÇTİ || echo "KALDI (çıkış $ARC)")"
CIKIS=0
[ "$KALDI" -gt 0 ] || [ "$SRC" -eq 1 ] || [ "$SRC" -eq 2 ] || [ "$ARC" -ne 0 ] && CIKIS=1
if [ "$CIKIS" -eq 0 ] && { [ "$OLCULEMEDI" -gt 0 ] || [ "$SRC" -eq 3 ]; }; then CIKIS=3; fi
case $CIKIS in 0) SONUC="GEÇTİ";; 3) SONUC="TAMAMLANMADI (ölçülemeyen/bekleyen var; sürüm için yeterli değil)";; *) SONUC="KALDI";; esac
echo "SÜRÜM ÖNCESİ: $SONUC · birim ($GECTI/$KALDI/$OLCULEMEDI) · sınav çıkış $SRC · anonimlik çıkış $ARC · çıkış $CIKIS"
exit $CIKIS
