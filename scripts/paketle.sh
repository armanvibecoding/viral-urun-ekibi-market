#!/bin/sh
# Tek komutla iki yükleme paketi üretir (dist/ altına; git'te tutulmaz, GitHub Releases'a yüklenir):
#   dist/viral-urun-ekibi-CLAUDE-v<sürüm>.zip   Claude: claude.ai / Claude uygulaması → Customize > Plugins > Add > Upload plugin
#                                               (tam eklenti: .claude-plugin + beceriler + ajanlar + kancalar + ortak + HyperFrames)
#   dist/viral-urun-ekibi-CHATGPT-v<sürüm>.zip  ChatGPT: Plugins → yükle (scripts/chatgpt_paketi_yap.sh çıktısı)
# Kullanım: SINAV_CIKTI_KOK=<7 sınavın çıktı kökü> sh scripts/paketle.sh   (önce scripts/surum_oncesi.sh çıkış 0 şart; PAKETLE_TASLAK=1 taslak)
# Claude ZIP biçimi (resmî doküman, claude.com/docs/plugins/build): manifest `.claude-plugin/plugin.json` ZIP kökünde ya da
# TEK üst klasörün içinde olmalı; üst düzey `bin/` klasörü claude.ai'de kurulumu engeller. Biz tek üst klasör (viral-urun-ekibi/) kullanırız.
set -e
KOK="$(cd "$(dirname "$0")/.." && pwd)"
E="$KOK/plugins/viral-urun-ekibi"
DIST="$KOK/dist"
command -v python3 >/dev/null || { echo "HATA: python3 gerekli"; exit 1; }
command -v zip >/dev/null || { echo "HATA: zip gerekli"; exit 1; }
# 0) Sürüm öncesi kapı (denetim 2026-11-25 #11): birim testleri + 7 sınav (--hepsi) + anonimlik hepsi GEÇMEDEN paket çıkmaz.
#    Sınav çıktı kökü: SINAV_CIKTI_KOK (+ isteğe SINAV_REFERANS_KOK, FFMPEG_DIZIN). Geliştirme taslağı için PAKETLE_TASLAK=1 (kapı atlanır, açık uyarı basılır).
if [ "${PAKETLE_TASLAK:-}" = "1" ]; then
  echo "UYARI: TASLAK PAKET — sürüm öncesi kapı (scripts/surum_oncesi.sh) ATLANDI; bu zip sürüm DEĞİLDİR."
else
  sh "$KOK/scripts/surum_oncesi.sh" || { echo "HATA: sürüm öncesi kapı geçmedi (çıkış $?): paket üretilmedi. Taslak için PAKETLE_TASLAK=1"; exit 1; }
fi
SURUM="$(python3 -I -c 'import json,sys;print(json.load(open(sys.argv[1],encoding="utf-8"))["version"])' "$E/.claude-plugin/plugin.json")"
[ -d "$E/bin" ] && { echo "HATA: eklentide üst düzey bin/ var; claude.ai kurulumu engellenir"; exit 1; }
CLAUDE_ZIP="$DIST/viral-urun-ekibi-CLAUDE-v$SURUM.zip"
CHATGPT_ZIP="$DIST/viral-urun-ekibi-CHATGPT-v$SURUM.zip"
mkdir -p "$DIST"
rm -f "$CLAUDE_ZIP" "$DIST"/viral-urun-ekibi-chatgpt.zip "$DIST"/viral-urun-ekibi-CHATGPT-*.zip

# 1) Claude paketi: eklenti klasörü olduğu gibi, tek üst klasör altında; çöp dosyalar hariç
( cd "$KOK/plugins" && zip -qr -X "$CLAUDE_ZIP" viral-urun-ekibi -x '*/.DS_Store' '*/__pycache__/*' '*.pyc' '*/.pytest_cache/*' )
# Doğrulama: manifest yerinde mi, yasak bin/ yok mu
unzip -l "$CLAUDE_ZIP" | grep -q ' viral-urun-ekibi/.claude-plugin/plugin.json$' || { echo "HATA: ZIP içinde manifest yok"; exit 1; }
unzip -l "$CLAUDE_ZIP" | grep -q ' viral-urun-ekibi/bin/' && { echo "HATA: ZIP içinde bin/ var"; exit 1; }

# 2) ChatGPT paketi
sh "$KOK/scripts/chatgpt_paketi_yap.sh" >/dev/null
[ -f "$CHATGPT_ZIP" ] || { echo "HATA: ChatGPT ZIP üretilmedi: $CHATGPT_ZIP"; exit 1; }

for z in "$CLAUDE_ZIP" "$CHATGPT_ZIP"; do
  echo "$(basename "$z") · $(unzip -Z1 "$z" | grep -vc '/$') dosya · $(wc -c < "$z" | tr -d ' ') bayt"
done
