Biçim: KARAKTER bloğu (1. satır eylem · 2. satır `ADIM 1/8 · Product Research Lead (Kaan)` (Pazar), `ADIM 2/8 · Product Research Lead (Kaan)` (Araştırma) · ≤5 madde · kod bloğu yok · son satır `Sonraki:`).

# Adım 1/8 Pazar ve Adım 3/8 Araştırma

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 57–58 ve 66–74. 0.3.0: araştırma marka adından önce yapılır (eski sıra repo `docs/ESKIDI.md`).
Plugin notu: Adım 3'ün "Marka kimliği" maddesi `marka` skill'inde, "Ürün içeriği" maddesi `metinler` skill'inde son hâline getirilir; burada taslak ve doğrulanmış gerçekler çıkar.

---

ADIM 1/8 — PAZAR
Ürün fotoğraflarını ve bu promptu aldığında yalnız şunu sor: "Bu ürünü hangi ülke veya pazarda satacağız?"

ADIM 3/8 — ARAŞTIRMA, MARKA VE ÜRÜN İÇERİĞİ
Pazar belli olunca (marka adını beklemeden) hedef pazarda tek seferlik araştırmayı yap ve tek mesajda ver:
- Ürün: ne olduğu, kategori, özellikler, [DOĞRULA] listesi; fotoğraflarda okunamayan ya da emin olmadığın bilgi
- Bulgular (en fazla 5): hedef kitle, satın alma motivasyonu, itirazlar, 3 rakip + fiyatları, rakiplerin görsel dili ve ürün sayfası düzeni
- Konumlandırma ve fiyat segmenti (1–2 satır); niş (`nis-…`) ve varyantlar
- Marka kimliği: renk paleti (5 HEX, kontrast kontrolü yapılmış), body fontu (listeden), ses tonu, slogan; rakiplerden ayrışma 1 satır
- Ürün içeriği: başlık; kısa ve detaylı açıklama; 3 fayda maddesi (tek satır, doğrulanabilir); "Nasıl kullanılır"; satış avantajları
- Fiyat: tekli fiyat ve adet indirimi oranları (rakip fiyatlarına göre). Karşılaştırma (üstü çizili) fiyatı yalnız gerçek fiyat geçmişi varsa.
Sor: "Araştırma onaylı mı? (revize için numara yaz)" (marka onayı `marka` skill'inde sorulur)
