# Kural defteri (çalışma zamanı, tek kaynak)

Her kural **bir kez** burada yazılır. Beceri, ajan ve referans dosyaları kuralı yeniden yazmaz; kimliğiyle atıf yapar
(ör. `IDD-01`). Kural değişecekse yalnız bu dosya (ve varsa kapı betiği) değişir. Kapı sütunu doluysa hüküm betiğindir:
metin betikle çelişirse betik kazanır.

## İddia ve dil
| Kimlik | Kural | Kapı (betik → çıkış) |
|---|---|---|
| IDD-01 | **Sağlık ve sonuç dili yasak değildir.** "Ağrıyı geçirir", "tedavi eder", "zayıflatır", "horlamayı keser", hastalık adı, sonuç garantisi yazılabilir; metin elenmez, yumuşatılmaz, belge istenmez. Böyle bir cümle geçen çıktının (senaryo, sayfa, caption, rapor) sonuna tek satır eklenir: `Bilgi notu (kullanıcının sorumluluğu): <hangi cümle>; mevzuat ve platform reklam kuralı kullanıcının işidir.` Ürün seçiminde de eleme sebebi değildir. | `teklif_kontrol.py` (`islem=bilgi-notu` → UYARI, çıkış değişmez) · `ortak/paket.py iddia-kontrol` ve `kurgu_kontrol.py --magaza-paketi` (UYARI `[saglik-sonuc]`) |
| IDD-02 | **Uydurma veri yasaktır** (kalite kuralı, her yüzeyde): sahte yorum ve yıldız, uydurma müşteri/satış/izlenme sayısı ve istatistik, sahte indirim ve kanıtsız çizili fiyat, sahte stok/kıtlık ve geri sayım, belgesiz uzman/doktor/klinik/sertifika onayı, sahte önce-sonra, ürünün yapmadığını gösteren görüntü. Sayı gerekiyorsa yer tutucu (`{GERCEK_YORUM_SAYISI}`); bilinmeyen = `doğrulanamadı`. | `teklif_kontrol.py` (`islem=engel` → 1) · `paket.py iddia-kontrol` (listede olmayan sayı/otorite → 1) · `senaryo_kontrol.py` |
| PLT-01 | **Platform reklam politikası ayrı kapıdır** (IDD-01 bunu kaldırmaz): Meta/TikTok'un yasak ya da kısıtlı kategorisi, izleyicinin kişisel özelliğini söyleyen reklam kancası ("POV: you have back pain" = Meta kişisel özellik kuralı), hesap kapanma riski. Ürün ve kreatif kararında risk kullanıcıya **uyarı** olarak yazılır; reklamı yasak kategoride yol `ai-video-kreatif/referans/kurgu-ve-yasaklar.md` §8 (imâ yolu) ve pazar kartı §6'dır. | pazar kartı §6 ihlali jüride ağır kusur · `reklam-kutuphanesi-avi` niş ELE kapısı |
