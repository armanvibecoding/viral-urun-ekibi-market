# Tarif 11 — Biçim kopyala, kendi dokunuşunu ekle (+ biçim kütüphanesi)

## Amaç
Aynı nişte tutmuş bir videonun **kare sırasını** iskelet alıp ürünü içine yerleştirmek, **tek değişkeni** değiştirmek ve kendi çektiğin görüntüyle yayınlamak.
Biçim + kendi dokunuşun = senin sürümün. Yöntem etiketi: **uzman yöntemi (R74)** — uygulayıcı yöntemi, istatistik kanıtı değil (aynı metin 2,5 Mn ve 343 B aldı; "garanti viral" iddiası yok).

## Yasak (telif + kişilik hakkı)
Başkasının **görüntüsü, sesi, yüzü, klibi, müziği ALINMAZ**; ekran kaydı, yeniden yükleme, "ilham" adıyla kare kare kopya yok. Alınan tek şey: sahne **sırası** ve ritim (hangi saniyede ne tür bir kare). Referans videonun hesabı/adı depoya, senaryoya ya da yazıya yazılmaz; yalnız kayıt numarası.

## Girdi
Aynı nişte tutmuş 1 referans video (izlenme kaydı: sayı + tarih) · kendi ürününün gerçek çekimi ya da gerçek ürün fotoğrafı (`uretim-kurallari.md` §6) · ön-üretim kartı (tarif 01 adım 0).

## Adımlar
1. **Kare panosunu çıkar:** referans videoyu yerel dosya olarak panoya çevir: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/cut/scripts/klip_qc.py" referans.mp4 --pano` → `referans_qc.jpg` (4 kare/sn, zaman damgalı). Pano yalnız çözümleme içindir; teslim videosuna girmez, depoya konmaz.
2. **Kare sırasını yaz (zamanlı iskelet):** tabloya her kesim için `sn aralığı · plan türü · kameradaki özne · ekran yazısı rolü` (kopyalama değil, rol: "kanca sorusu", "sayaç", "sonuç"). Örnek: `0–1,5 sn: tek soru yazısı + iki yan yana alan` · `1,5–6 sn: test, sayaç atlar` · `6–8 sn: kazanan alan + tik`.
3. **Ürünü yerleştir:** her satıra kendi ürününün gerçek çekimini koy. Sahne sırası aynı, görüntü senin.
4. **Tek değişken:** referanstan yalnız BİR şeyi değiştir (ürün, ya da test kuralı, ya da kanca sorusu). İkisini birden değiştirme; tutarsa neden tuttuğu okunabilsin.
5. **Kanca = senin sorun:** ilk yazı izleyicinin durumundan/sorusundan başlar (R4), tek soru + cevap anı (A); marka ile açılmaz.
6. Üret: tarif 01 (reklam) ya da tarif 02 (hikâye); HyperFrames şablonları: R1 `ikili_kiyas`, R2 `deneme_sayaci` (`skills/cut/hf-sablonlar/README.md`).
7. **Kayıt:** `is/NN/bicim-kaydi.tsv` → kütüphaneye satır ekle (aşağıda).

## Biçim kütüphanesi (fikir avı disiplini)
Uygulayıcı yöntemi (R74): günde ≥ 2 saat kaydırıp tutmuş biçim toplamak. Bu eklentide hedef: **haftada ≥ 10 tutmuş biçim kaydı**.
| Alan | İçerik |
|---|---|
| `no` / `tarih` | kayıt numarası, toplandığı gün |
| `nis` | ürün niş etiketi |
| `izlenme` | referansın görünen izlenmesi (+ tarih; sayı kaynak ekranı) |
| `kare_sirasi` | adım 2'deki zamanlı iskelet (tek satır: `0–1,5 soru | 1,5–6 test+sayaç | 6–8 sonuç`) |
| `pano` | yerel pano dosya adı (depoya konmaz) |
| `biçim_adi` | kendi koyduğun ad (hesap adı değil) |
| `denendi` | boş / ürün adı + yayın tarihi + 48. saat sonucu |
Kural: kayıt başına kare sırası zorunlu (yalnız "güzel video" kaydı sayılmaz); aynı biçim ≥ 3 kayıtta görülürse "tekrar eden biçim" işaretle; haftalık kayıt < 10 ise bunu DURUM.md'ye "fikir avı eksik" yaz.

## Kalite çıtası
Kare sırası zamanlı tabloda · hiçbir karede başkasının görüntüsü/sesi/yüzü yok · tek değişken adı yazılı · kanca marka/"biz" ile başlamıyor · gerçek çekim (AI görüntü reklamı "sahte" görünür).

## Kapılar
Ön-üretim kartı geçerli (tarif 01 adım 0) · `senaryo_kontrol.py` çıkış 0 (R4, açık döngü alanları) · tarif 01/02 kapıları · `anonim_kontrol` (depoya referans hesabı/adı yazma).

## Sık hata
- "Biçimi kopyaladım" diye klibi/sesi olduğu gibi kullanmak → telif + kişilik hakkı; yeniden çek.
- Aynı anda ürün + kural + kanca değiştirmek → neden tuttuğu okunmaz.
- Tek hit biçimi "garanti" saymak → aynı biçim iki yayında 2,5 Mn ve 343 B aldı; tekrar yayın deneyi (tarif 10 adım 7).

## Bitti tanımı
Zamanlı kare sırası + gerçek çekimli video + `bicim-kaydi.tsv` satırı; 48. saat sonucu tabloda (`olcum-ve-test-plani.md` §3, §3b).
