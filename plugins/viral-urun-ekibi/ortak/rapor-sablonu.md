# Rapor şablonu (her rol; sabit sıra)
1. İlk satır: tek cümle sonuç.
2. İkinci satır: `kurucuyu ilgilendiren: <para | dosyasına dokunma | karar>` ya da `yok`.
3. `DENEME SAYISI n/sınır` (n > sınır ise ilk satıra da yaz).
4. `SONUÇ` · `KAPI ÇIKTISI` (komut + çıkış kodu, aynen) · `DOKUNULAN DOSYALAR` · `ÖLÇÜLEMEYEN`.
5. `KİM DENETLEDİ`: rol adı; denetleyen üreten rolün kendisiyse `ÖZ-DENETİM` (kapıda `olculemedi` sayılır). Raporda `ÜRETEN: <rol>` satırı da yer alır; koşucu `KİM DENETLEDİ` ile karşılaştırır.
6. Son satır: tek sonraki adım.
Kural kimliği, çıkış kodu ve jargon (`olculemedi`, `K1–K4`) yalnız `KAPI ÇIKTISI` bölümünde kalır; ilk iki satır kurucunun okuyacağı düzdür.
