Biçim: KARAKTER bloğu (1. satır eylem · 2. satır `ADIM 8/8 · Store Architect (Baran)` · ≤5 madde · kod bloğu yok · son satır `Sonraki:`).

# Adım 8/8 QA

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 215–226. 0.3.0: görsel diliyle gelen 4 kontrol eklendi.

---

ADIM 8/8 — QA
Önizlemede (`https://<mağaza>.myshopify.com/?preview_theme_id=<id>`) mobil (390 px) ve masaüstünde (1440 px) kontrol et, düzelt. Tarayıcın yoksa bu listeyi bana kontrol listesi olarak ver; sonuçları ben yazarım.
- Mağaza dili ve ödeme sayfası dili doğru; İngilizce ya da başka dilde kalmış metin yok
- Header: menü 5 öğe, "Satın Al" → ürün sayfası, bulunulan sayfa vurgulu
- Ürün sayfası C bloğundaki sırayla; adet indirimi satırlarının toplamı = sepetteki tutar (indirim sepette uygulanıyor)
- Fiyatlar okunuyor; taşma, başka marka/ürün adı, [DOĞRULA] veya yer tutucu yok
- Sepete ekle → çekmece → tutar doğru; TR'de onay kutusu işaretsizken ödemeye geçilemiyor
- Checkout'ta kargo seçenekleri ve tutarlar kargo sayfasıyla aynı
- Footer: Menü ve Yasal Bilgiler linkleri (4 sayfa) açılıyor
- Ürün galerisi: 9 görsel, G0 (yazısız feed karesi) ilk sırada, sonra G1–G8; hiçbir görselde ürün kenarda kesik değil; her görselin alt metni dolu
- Bölüm görselleri: görselin kenarı ile bölüm zemini arasında kutu kenarı görünmüyor (zemin hilesi; renk farkı varsa ⚠️ olarak yaz)
- Mobil (390 px) ana sayfa: banner görselindeki yazı ile vitrin şeridinin H1'i çelişmiyor; ikinci kez görünmesi bilinen tema sınırı, ⚠️ olarak yaz
- Logo yüklenmediyse header'da mağaza adı görünüyor
- MCP doğrulamaları: ürün ACTIVE + Online Store'da, menüler, kargo bölgesi, indirim `summary` değerleri
- Site denetimi (0.4.0): `site-denetimi.md` §1–5 (tipografi görsel = site, hız, G0 feed + alt metin, kontrast, satın alma kutusu)
Rapor: ✅ Tamamlanan | ⚠️ Benim yapmam gereken (yalnız gerçekten kalanlar)
Doğrulanması gereken verileri uydurma. MCP'nin yapamadığını yapılmış gibi gösterme.
