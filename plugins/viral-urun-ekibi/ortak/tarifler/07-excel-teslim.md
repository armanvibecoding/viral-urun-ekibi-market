# Tarif 07 — Excel teslim

## Amaç
Ürün bulma becerilerinin (radar, spy, hunter, bazaar) çıktısını tek biçimli, doğrulanmış `.xlsx` olarak teslim etmek.

## Girdi
`urunler.tsv` (12 alan: urun, link, ilgi, ilgi_sayi, alis, satis, para, marj_kat, karar, neden, kaynak, tarih) · isteğe bağlı ham tablo (`--ayrinti`) · teslim yeri (kopya klasörü ya da dosya yolu).

## Adımlar
1. `urunler.tsv` yaz; `karar` yalnız `SAT`, `SAT (koşullu)`, `İZLE`, `ELE`.
2. Yaz: `python3 "${CLAUDE_PLUGIN_ROOT}/ortak/excel_yaz.py" --urunler urunler.tsv --kaynak bazaar --cikti is/NN/liste.xlsx --ayrinti ham.tsv --kopya teslim/Urun-Listesi.xlsx`
   - `--kopya` bir **dosya yolu** (`.xlsx`) ya da klasör olabilir: dosya yolu verilirse o ada kopyalanır, klasör verilirse aynı adla içine konur (kırma testi: `excel_test.py`).
3. Çıktı satırı: `TAMAM … · N ürün (SAT a / SAT-koşullu b / İZLE c / ELE d)`; çıkış 0.
4. openpyxl yoksa çıkış 3: `python3 -m pip install --user openpyxl`.

## Kalite çıtası
Tam 3 sayfa (Ürünler, Ayrıntı, Nasıl okunur) · yazıdan sonra dosya yeniden açılıp ölçülür · sıralama SAT, SAT (koşullu), İZLE, ELE (her grupta ilgi büyükten küçüğe) · kopya dosyası gerçekten dosya.

## Kapılar
`excel_yaz.py` çıkış 0 · `excel_test.py` çıkış 0.

## Sık hata ve düzeltmesi
- `--kopya` klasör sanıp dosya adıyla klasör açıyordu → düzeltildi; dosya yolu dosyaya kopyalanır.
- Çıkış 1 "karar … izinli" → karar yazımı (büyük/küçük, Türkçe İ) kontrol et.

## Bitti tanımı
`.xlsx` hem `is/NN/` altında hem kullanıcının istediği yerde (dosya olarak), ölçüm satırı raporda.
