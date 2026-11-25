# Geçiş/kapanış taşıma raporu (2026-11-24)

Kaynak: müşteri video kitindeki 3 teknik (yalnız okundu, değiştirilmedi). Hedef: `plugins/viral-urun-ekibi/skills/cut/`. Marka/kişi adı, ev dizini, logo dosyası depoda yok; örneklerde jenerik SVG yer tutucu.

## Değişen dosyalar (hepsi `skills/cut/` altında)
- `hf-sablonlar/tipografi.py`: yeni `urun_gecisi`, `dip_gecis`, `kapanis`, `varliklari_kopyala`; `ig_kutu`'ya `genislik` parametresi (varsayılan 760 = eski davranış); `ikili_kiyas` soru kutusu büyütüldü; `TURLER`'e 3 yeni tür.
- `hf-sablonlar/sablon.css`: (l) geçiş + kapanış stilleri.
- `scripts/hikaye/bloklar.py`: `bitir` içinde `TP.varliklari_kopyala(K)` (görseller assets/img/'ye).
- `scripts/ses_tasarla.py`: `--son_fade_egri` (tri|qsin|hsin|esin|log|par|cub|exp); varsayılan None = eski grafik birebir.
- `hf-sablonlar/sablon_test.py`: `test_urun_gecisi`, `test_dip_gecis`, `test_kapanis`, `test_ses_son_fade_egri`; `test_ikili_kiyas`'a büyüklük/genişlik kontrolü. Mevcut hiçbir test/eşik gevşetilmedi.
- `hf-sablonlar/ornek_uret.py`: 4 örnek + yer tutucu SVG üretimi; `ornekler/{urun_gecisi,dip_gecis,kapanis,kapanis_yumusak}/` üretildi, `ornekler/ikili_kiyas/` yenilendi.
- `hf-sablonlar/README.md`: 3 satır + ikili_kiyas satırı + referans tablosu satırı.

## İmzalar
- `urun_gecisi(bas, sure, gorsel=None, kick="", ust1="", ust2="", alt="", gecis=0.7, w=570, ust=640, top_yazi=300, alt_top=1180, bg=UG_BG, boy1=104, boy2=120, renk="#FFE600", pid=None)` — sahne `bas-gecis`'te başlar, `bas >= gecis` şart (negatif GSAP konumu yok).
- `dip_gecis(z, once=0.35, ac=0.6, yogunluk=0.7, renk="#000000", pid=None)` — `z >= once` şart.
- `kapanis(bas, sure, logo, marka, alt_satir="", yazi="", yumusak=0, kapan_sn=None, top_yazi=300, top_logo=640, logo_boy=300, zemin="#07080d", pid=None)` — kapan_sn varsayılan 0,8 (yumusak>0 ise 1,4); en çok 2 yazı katmanı (`kpy`); logo yoksa "HATA: kapanis logosu dosyası bulunamadı".
- Ses: `ses_tasarla.py ... --son_fade 2.5 --son_fade_egri qsin` (yerel ffmpeg ve imageio ffmpeg'de `afade` + `qsin` çalıştı).
- `ikili_kiyas(..., boy=116)`: ≥3 kelimelik soru dengeli 2 satıra bölünür, `sigdir` 820 px'e sığdırır; "Hangisi 10 saniyede kurudu?" eski ~42 px → şimdi ≥ 72 px (testte ölçülür).

## Kapı çıkış kodları (depo kökünde)
| Kapı | Çıkış |
|---|---|
| `sablon_test.py` (16/16) | 0 |
| `sh scripts/anonim_kontrol.sh` | 0 |
| `python3 scripts/musteri_icerik_kontrol.py` | 0 |
| `python3 scripts/sozlesme_test.py` (49/49) | 0 |
| `python3 scripts/sinav_kos_test.py --hizli` (61 test, 0 kaldı) | 0 |

Ek: 5 örnek için `npx hyperframes check --json` → `ok: true`; `.hyperframes/` önbelleği silindi.

## Notlar / sınırlar
- Kaynaktaki ürün parıltı (mask shimmer) ve ürüne özel flaş genelleştirilmedi (müşteri görseline bağlı); çapraz geçiş, scale/parlaklık, yazı gecikmesi, dip, kapanış kilidi ve yumuşak mod taşındı.
- Kaynaktaki `son()` CTA + logo kilidi tek `kapanis` fonksiyonuna birleşti (`yazi` isteğe bağlı).
- `ornekler/*` dışındaki mevcut örnekler yeniden üretildi ama içerikleri değişmedi.
