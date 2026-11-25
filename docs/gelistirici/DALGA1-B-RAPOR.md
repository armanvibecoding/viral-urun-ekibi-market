# Dalga 1 B: rol ve tanım maddeleri (2026-11-25)
Sonuç: 4, 7, 8, 9, 16, 18, 19, 20 (metin), 21 (metin), 23, 31, 32 uygulandı; YAPILAMAZ yok. Talimat satırı 1142 → 1141 (agents + ortak/roller + ekip.md + magaza-ekibi.md + 3 yeni ortak dosya dahil, net artış yok).
kurucuyu ilgilendiren: karar yok. Betik tarafına devredilenler en altta.

| Madde | Dosyalar (satır önce → sonra) | Durum |
|---|---|---|
| 4 rapor şablonu + KİM DENETLEDİ + öz-denetim = olculemedi | yeni `ortak/rapor-sablonu.md` (7 satır); tanım cümlesi `ortak/sozlesme-rol.md` madde 2-3 | tamam |
| 7 ortak sözleşme 8 satır + her ajanda tek atıf | yeni `ortak/sozlesme-rol.md` (8 madde); 17 ajanda atıf (10 mağaza ajanında mevcut "Yollar" satırına eklendi, 7'sinde +1 satır); 7 dispatch ajanından "mod yoksa" satırı silindi, `magaza-ekibi.md` §1'e taşındı (32 → 33) | tamam |
| 8 araçlar | `panel.md` Bash silindi; `jury.md` Glob silindi (+brief dosya listesi verir cümlesi); `decoder.md` Bash eklendi + "n'yi betik sayar" cümlesi, prompt biçimi blok (5 satır) yeni `skills/radar/referans/prompt-dosyasi-sablonu.md`'ye taşındı (58 → 54) | tamam |
| 9 Copy site, Shopper ses, ekip.md durum satırı | `copy.md` (33 → 36: mod gorsel/site, dil "pazarın dilinde"); `shopper/ses.md` madde 6 çok dilli + DE/EN test; `shopper.md` description; `ekip.md:61` "5 Copy (mod `site`; görsel içi yazı mod `gorsel`)". Çıktı dosyası adı `SITE-METNI.md` (benim seçimim) | tamam |
| 16 referans seçimi + niş uyumu | `atlas/stil.md` adım 5 Muse'a devredildi; `muse/referans.md` (20 → 21) kör pano referansı + niş uyumu kuralı; `studio/SKILL.md` viral referans seçim kuralı (kurgulayan seçmez, Decoder/Muse aday, niş+pazar+dilim) | tamam |
| 18 Sentinel | `sentinel/seri.md` (36 → 33): §1 düzeltme Forge'a, K2 çift paragraf silindi; `yazim.md` TR gözle = olculemedi, Latin birebir; `forge/istem.md` (37 → 38) düzeltme adımı | tamam |
| 19 Story | `story.md` (62 → 55): kota cümlesi, banka "yoksa dur", R74 bloğu atıfa | tamam |
| 20 Mixer (metin) | `mixer.md` (66 → 65): çıkış kodu kuralı + ARAÇ ŞÜPHESİ, uzun komut satırı silindi (`--help`) | tamam |
| 21 Skeptic (metin) | `skeptic.md` 12 sayfa bütçesi, `SAT-KOŞULLU`, bulunamadı≠çürütme; MCP paragrafı Scout ile tek kopya `ortak/mcp-kanit-araclari.md`; `hunter/referans/kanit-ve-karar.md` §2'ye SAT-KOŞULLU. ROAS eşiği ve bazaar dosyalarına dokunulmadı | tamam |
| 23 pazar kartı + dil kuralı | `magaza-ekibi.md` §4 "Pazar ve dil" tek madde (10 rolün hepsi bunu okur) | tamam |
| 31 Director | `director.md` (46 → 38): site sınıfları silindi, `captain/SKILL.md` yönlendirme tablosuna taşındı (119 → 120); tek eşik 9 (benim seçimim; Atlas/Copy zaten 9, gösterim 8,5 → 9) | tamam |
| 32 devam + 20 dk | `sozlesme-rol.md` madde 4 | tamam |

## Test çıkışları
- `scripts/sozlesme_test.py` 49/49 · `scripts/ad_testi.py` 0 hata · `captain/scripts/kapi_test.py` 42 test 0 kaldı · `hunter/scripts/kirma_testi.py` 16 test 0 kaldı · `studio/scripts/senaryo_kontrol_test.py` GEÇTİ satırları.
- Ajan frontmatter (name/description/tools/model): 17/17 geçerli; `claude plugin validate` "Validation passed".
- `bash scripts/anonim_kontrol.sh`: temiz, çıkış 0.
- `scripts/sinav_kos_test.py` başlangıçta 120 sn'yi aştı, arka planda bitti (çıkış 0), değişiklikten sonra yeniden koşulmadı.

## Betik tarafına devredilenler
- `SAT-KOŞULLU` hüküm değeri: `firsat_kontrol.py`/denetleyiciler tanımıyorsa eklenmeli.
- Story kota cümlesi ile `senaryo_kontrol.py` ≥ 8 mekanizma / ≥ 6 şablon kapısı çelişebilir.
- Rapor şablonu başlıkları (`KİM DENETLEDİ`, `ÖZ-DENETİM`) koşucu/kapı ayrıştırıcısına bağlanacak; şablon yolu `ortak/rapor-sablonu.md`.
