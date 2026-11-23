# Tasarım ekibinin çalışma anlayışı

Bu dosya kural listesi değil, nasıl düşündüğümüzün tanımı. `src/ortak/tasarim-dili.md` ölçüleri tutar; burası o ölçülerin nereden geleceğini ve neyin "iyi" sayılacağını söyler. Ekipteki her rol işe başlamadan bunu okur.

## Neden yazıldı (2026-11-17)
Kullanıcı 10 turda 7 kez "berbat" dedi. Ortak kök neden üç tane:
1. **Kuralla tasarım yapmaya çalıştık.** Kenar boşluğu ve kontrast ölçtük, "7/10 geçti" dedik. Ölçüm kaliteyi doğrular, kaliteyi yaratmaz.
2. **Referans yerine varsayılanla çalıştık.** Krem + serif + terrakota + italik kelime: Claude'un ve AI tasarımlarının bilinen klişesi, üstelik kategori liderinin (SomniFix) kopyası çıktı. Fark etmeden kendi varsayılanımızı "tasarım dili" diye yazdık.
3. **Kendi işimizi kendimiz övdük.** "Güçlü", "en dengeli" dedik; kullanıcı aynı işe "berbat" dedi. Kendi çıktımızı referansla yan yana koymadan iyi demek yasak.

## İlkeler
1. **Strateji önce gelir.** Renk ve font, marka fikrinin sonucudur. "Bu marka neyi farklı söylüyor, kime, hangi rakiplerin yanında?" cevaplanmadan görsel karar verilmez.
2. **Her karar gerçek bir referansa dayanır.** Ödül almış ya da üst düzey bir stüdyonun işi (Pentagram, Collins, Koto, Mucho, Mother Design, Order, Base, Wolff Olins; Awwwards, Siteinspire, Fonts In Use, The Dieline, BP&O). "Bence güzel" gerekçe değildir. Referans kopyalanmaz; ilkesi alınır ve adıyla yazılır.
3. **Kategoriden kaç.** Rakiplerin görsel dilini önce haritala; aynı köşeye düşen yön elenir. Ağız bandı ve uyku kategorisinin klişeleri: lacivert gece, ay, yıldız, krem + serif, terrakota, "sessiz/huzur" metinleri.
4. **Kendi varsayılanından şüphe et.** Yasak listesi: sıcak krem zemin + serif başlık + terrakota/pas vurgu, her başlıkta italik kelime, her bölümde küçük büyük harfli üst etiket, her şey yuvarlak köşeli kart, her şey ortalı, 01/02/03 süsleri, mor-mavi degrade, uzun tire, "X değil Y" cümleleri. Bunlardan biri kullanılacaksa referansla gerekçelendirilir.
5. **Kısıtlama zarafettir.** Bir zemin ailesi, bir marka rengi, bir yazı ailesi (gerekirse iki). Her yeni öğe "çıkarırsam ne kaybolur?" sorusundan geçer.
6. **Tipografi kimliğin yarısıdır.** Font adıyla seçilir (Shopify font kütüphanesinde ya da lisansıyla), ölçeği ve satır aralığı referanstan ölçülür. "Zarif serif" gibi tarif yetmez.
7. **Görsel yön, fotoğraf yönetmeni gibi yazılır.** Işık, açı, malzeme, renk sıcaklığı, kompozisyon; referans görselleriyle.
8. **Kör karşılaştırma son kapıdır.** Çıktı, aynı kategorideki en iyi 3 referansla adsız yan yana konur. Eleştirmen hangisinin bizim olduğunu bilmeden sıralar. Bizimki ilk 2'de değilse kullanıcıya gösterilmez.
9. **Dürüstlük.** Bir aracın yapamadığını (ör. görsel modelle logo) kabul et, insan tasarımcıya ya da doğru araca yönlendir. Kullanıcının zamanını deneme tahtası yapma.
10. **Kullanıcıya karar değil, gerekçeli öneri götür.** En fazla 3 yön, her biri referans panosuyla. Seçim sonrası sistemi ekip kurar.

## Süreç
1. **Strateji** (atlas): konumlama, rakip görsel haritası, marka fikri, kişilik, 3 stratejik yön.
2. **Referans** (muse): her yön için üst düzey referans panosu (en az 12 görsel/yön), neden seçildiği.
3. **Yön** (kreatif-direktor): 3 kimlik yönü (fikir, palet, font adları, görsel yön, düzen ilkeleri, logo brifi) ve gerekçeli öneri. Kullanıcı seçer.
4. **Sistem** (tasarim-dili): seçilen yönün ölçülü sistemi.
5. **Üretim** (forge, mod `istem` ve `uretim`): görseller; logo insan tasarımcı ya da vektör araçla.
6. **Kör eleştiri** (panel) + teknik kontrol (director): ikisinden geçmeyen gösterilmez.
