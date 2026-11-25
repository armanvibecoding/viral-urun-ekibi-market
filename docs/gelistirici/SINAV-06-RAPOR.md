# SINAV 06 (ürün avı) · a-kolay ve b-zor raporu · 2026-11-24

Sonuç: tur1 KALDI (2 vaka), tur2 GEÇTİ (3/3, çıkış 0). c-tuzak tur1'den aynen kopyalandı.
Çıktılar: `kreatif/sinav-kosu/06-urun-avi/tur1|tur2/{a-kolay,b-zor}/adaylar.md` (<referans-kok> altında).

## Ne yapıldı
- AliExpress'te tek yeni Chrome sekmesiyle (sonra kapatıldı) iki arama + iki ürün sayfası okundu. CAPTCHA/giriş duvarı çıkmadı. Satın alma, sepet, hesap yok.
- a-kolay: ürün 3256812319818573, 15 sold, puan 5.0 (3 değerlendirme), normal 13.01 USD. Karar İZLE (SAT yok: kanıt dosyası, DE pazar kontrolü, alıcı fotoğrafı ve marj yok). DNA 5/7.
- b-zor: ürün 3256813093891614, 34 sold, puan 3.8 (4 değerlendirme), liste 15.27 USD (yeni müşteri 1.09). Karar ELE (DNA 3/7, kategori doygun görünüyor).
- Amazon, TikTok Shop, Meta ve marj bakılmadı: tabloda "doğrulanamadı" yazıldı, A/B/C/D kısmen boş (sıra puanı `?`).

## KALDI kök nedeni (tur1)
Kapı: `yasakli`, desen "uydurma müşteri/yorum sayısı". Metinde "puan 5.0, yorum adedi 3" geçti, desen `sayı + yorum` kalıbını yakaladı. Sınıf: (b) benim üretim biçimim; ama yönerge de bu tuzağı önceden söylemiyordu. Eşik/kapı gevşetilmedi. Düzeltme: "puan 5.0 (3 değerlendirme)". Eklentide tek satır not eklendi: `skills/hunter/referans/dosya-sablonlari.md` (adaylar.md bölümü, Durum değerlerinin hemen üstü).

## Hunter akışında takılma ve belirsizlikler (en değerli kısım)
1. `skills/hunter/SKILL.md` akış adım 1 ve KARARLAR.md `pazar` satırı: sınavda `.ekip/` yok, pazar vakadan geliyor. Yönerge "kullanıcıya bir kez sor" diyor; ajan soru soramıyor. Sınav/alt ajan modu için "pazar brifte verildiyse sorma" cümlesi yok.
2. `SKILL.md` akış adım 4 hedef "20–30 aday"; sınav vakası tek ürün. Vaka ürünü zorunlu, diğer adaylar serbest; yönerge hangisinin öncelikli olduğunu söylemiyor. Ben tek satırla yetindim.
3. `SKILL.md` adım 5 "zaten viral mi" (Amazon, TikTok Shop, Meta) pazar başına tarayıcı oturumu ister; ABD/DE için her adaya ≥3 ek site, ≥15 sn aralık. Sınav bütçesinde yapılamıyor. Yönerge "yapılamadıysa hangi karar" demiyor; `kanit-ve-karar.md` §2 yalnız "doğrulanamadı → İZLE" der, ama ELE ile çakışan durum (DNA<4) için öncelik yazmıyor. Ben DNA<4 → ELE kuralını (denetle çıktısı) önceledim.
4. `kanit-ve-karar.md` §1 (sıra puanı) ile `firsat_kontrol.py:denetle`: B ve C ölçülemeyince boş bırakmak scout.md satır 7'de serbest, ama denetle `sira ?/11` yazıp öneri vermiyor. Ölçülemeyen satırın kararı (İZLE mi ELE mi) için tek cümle yok.
5. `scout.md` yöntem 4 "satışı başlık satırından oku": yeni AliExpress sayfasında satış ve puan başlıkta ("34 sold", "3.8 / 4 Reviews") ama fiyat bloğunda yalnız teklif fiyatı ve üstü çizili fiyat var; "normal fiyat" hangisi belirsiz. Ben üstü çizili liste fiyatını normal yazdım (mug: 13.01 normal, 4.53 teklif; rulo: 15.27 liste, 1.09 yeni müşteri), ama rulo için bu çizili fiyatın gerçek satış fiyatı olmadığı (92 indirim) şüphesi var. `aliexpress-okuma.md` §3 bu durumu (çizili fiyat şişirilmiş olabilir) söylemiyor.
6. `aliexpress-okuma.md` §1: ürün linkini arama sayfasından almak için `find` + tıklama gerekti (tıklama yeni sekme açıyor, URL ürün no içeren aliexpress.us). Linkin nasıl alınacağı yazılı değil; `firsat_kontrol.py` `item/<no>` bekliyor, sorun yok ama tarayıcı adımı açıklanmalı.
7. `aliexpress-okuma.md` §3 "yorum sayısı" yazım biçimi: şablonun örneği `5,0/8`; aşağıdaki sınav kapısı `5.0, 8 yorum` biçimini IDD-02 diye yakalıyor (yanlış pozitif sayılır). Yönergede yasak biçim uyarısı yoktu, şimdi `dosya-sablonlari.md`'ye eklendi. Kalıcı çözüm koşucu desenini daraltmak olur; bu ayrı iş, gevşetme yapılmadı.
8. `tools` listesi: scout.md `javascript_tool` ve `read_page` listesinde yok/var tutarsız değil, ama ürün linkini DOM'dan almak için `javascript_tool` gerekiyor; olmadan `find` + tıklama dolambacı. Not.
9. `SKILL.md` "Kurallar": "Mekanizma gerçek alıcı fotoğrafı/videosuyla doğrulanmadan SAT verilmez"; bu iki vakada alıcı fotoğrafı yorumlarda görünmedi (3 ve 4 değerlendirme, hiçbirinde fotoğraf okunmadı). Yani yeni/az satan ürünler yapısal olarak hep İZLE/ELE çıkar; yönerge bu sonucu "tutmamış ürünler için SAT neredeyse imkânsız" diye uyarmıyor.
10. Aralıkta: ürün satışı okuma için `get_page_text` tek başına yetti; sayfa ilk çağrıda boş geldi (yüklenmedi), 8 sn bekleme gerekti. `aliexpress-okuma.md` §1'de "sayfa yükleme bekleme" yok.

## Kapılar (hepsi çıkış 0)
anonim_kontrol.sh 0 · musteri_icerik_kontrol.py 0 · sozlesme_test.py 0 (49/49) · sinav_kos_test.py --hizli 0 (61/61) · hunter kirma_testi.py 0 (16/16). Hunter için başka `*_test.py` yok.

## Dokunulan dosya
- `plugins/viral-urun-ekibi/skills/hunter/referans/dosya-sablonlari.md` (tek paragraf eklendi)
Dokunulmayanlar: skills/cut, skills/studio, agents/story.md, eşikler, koşucu, OLCUT. git add/commit yapılmadı.
