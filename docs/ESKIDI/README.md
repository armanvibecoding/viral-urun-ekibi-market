# Eskidi (çalışma zamanından çıkarılanlar; silinmedi, iz burada)

| Dosya | Ne zaman | Neden çıktı | Yerine |
|---|---|---|---|
| `puan-cetveli-0.2.md` (eski `skills/video-kurgu/referans/puan-cetveli.md`) | 0.3.0 | Tek eleştirmen hem ölçüyü hem zevki puanlıyordu; kanca alanı 45 satırda hep 6–8 (std 0,74), 12 teslimin 0'ı geçti | Zevk: kör jüri (`agents/video-juri.md`, `juri.py`). Ölçü: `kapi.py` altındaki betikler. Ağır kusur listesi: `referans/agir-kusurlar.md` |
| `puan_kaydet-0.2.py` (eski `skills/video-kurgu/scripts/puan_kaydet.py`) | 0.3.0 | Eleştirmenin kendi puanını kaydettiği betik; hüküm artık `juri.py birlestir`den geliyor | `juri.py birlestir --kayit is/NN/elestiri/juri.jsonl`. Eski `puanlar.jsonl` dosyaları `kapi.py` ve `juri.py ayirt` tarafından hâlâ okunur |

Kural budama kaydı (hangi kural nereden çıktı, tek kaynağı neresi): `docs/BUDAMA-0.3.0.md`.
