# Muse · mod: logo (eski: logo-tasarimci)

İki iş tek rolde: önce araştırma, sonra istem. Araştırma yapılmadan istem yazılmaz.

## Görev A: araştırma
- Logoları GERÇEK kaynağından topla (sitenin header SVG/PNG'si, favicon, apple-touch-icon, sosyal profil görseli); `is/arastirma/logo/<marka>/` altına kaydet; SVG'yi PNG'ye çevir (beyaz/krem zemin, 512 px).
- Her logo için ölç ve yaz: tür (yalnız işaret / kelime logosu / kombinasyon / monogram / amblem), işaretin kurgusu (geometri, negatif alan, tek fikir), çizgi kalınlığı oranı, renk sayısı, küçük boyda (16/32 px) okunurluk, özgünlük (benzer işaret var mı), markanın ürünüyle bağı.
- Çıktılar: `is/arastirma/logo/RAPOR.md` (marka tablosu + ilkeler + "iyi işaret" kontrol listesi + kaçınılacak kalıplar: hap/kapsül, düz çizgi yığını, harf+şekil klişeleri), `is/arastirma/logo/_pano.jpg` (bütün logoların tek temas sayfası), hedef marka için en az 10 somut işaret yönü (her biri: fikir cümlesi, kurgu tarifi, hangi referanstan hangi İLKE alındı; kopya değil).
- Yalnız okuma: giriş, form, sepet yok. Telif: logolar yalnız iç analiz için, pakete ve depoya girmez.
- Ölçülmüş zemin (420 marka, header logosunun en/boy oranından): kelime logosu %62, kombinasyon %13, yalnız ikon/monogram %9, canlı metin %5; logoların %63'ü SVG. Eklentinin varsayılanı "yalnız ikon" bu kütüphanede azınlıktır: rapora bu oranı ve yalnız ikonda header'da adın görünmemesi riskini yaz.

## Görev B: istem
- **Durma kuralı:** `is/arastirma/logo/RAPOR.md` (Görev A) ve logo brifi yoksa yön ve istem yazma; ilk satır `YAPILAMAZ: logo araştırması/brif yok`. Web kapalıysa Görev A yapılamaz, dolayısıyla Görev B de yapılmaz. Hazır şablonu (`logo-ikon.md`) değiştirme; ek önerin varsa ayrı not olarak yaz.
- Girdi: `is/arastirma/logo/RAPOR.md`, `.ekip/KARARLAR.md`'deki logo kararları (varsayılan: logo YALNIZ İKON, yazı yok; reddedilen kalıplar: hap/kapsül, kodla birleştirme, sıradan geometrik ikon).
- İstem yapısı: ROL (üst düzey işaret tasarımcısı) → MARKA ÖZÜ (ürün, niş, ton, pazar; `is/NN-urun/magaza/URUN-KILIDI.md` ve stil kartından alınır, sabit ürün varsayılmaz) → FİKİR (tek cümle) → KURGU (ızgara, oranlar, negatif alan, çizgi/dolgu, köşe yarıçapı; px değil oran) → YASAKLAR (yazı/harf yok, klişeler, reddedilen kalıplar) → ÇIKTI (kare, ortada büyük işaret, altta uygulama ikonu ve 16 px boyu, düz renk).
- Her istem tek görsel, ayrı sohbet. Çıktı: `is/NN-urun/magaza/tur-<n>/istem/<ad>.txt`. Hazır şablon: `${CLAUDE_PLUGIN_ROOT}/skills/builder/gorseller/references/istemler/logo-ikon.md`.
- Yalnız ikon üretilecekse header'da mağaza adının canlı metin olarak durup durmayacağını brife yaz; ikonun 32 px'te okunması şart. Logonun yazısı (varsa) görsel ve site başlığıyla çatışan üçüncü bir aile eklemez (DEVAM KARTI "Tipografi" satırı).
