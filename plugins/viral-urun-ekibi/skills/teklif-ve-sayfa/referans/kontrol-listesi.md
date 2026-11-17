# Kontrol listesi (taslak "hazır" denmeden önce)

Her madde `[x]` ya da `[ ] neden` ile `is/NN-urun/kontrol.md`'ye kopyalanır. Betik maddeleri çıkış koduyla kanıtlanır.

## Betik
- [ ] `teklif_kontrol.py sema is/NN-urun/teklif.tsv` → çıkış 0 (çıktının son satırı kontrol.md'ye)
- [ ] `teklif_kontrol.py tara --pazar <P> sayfa.md itiraz-sss.md eposta-upsell.md` → çıkış 0
- [ ] `marj_hesap.py` paket fiyatlarıyla (1x/2x/3x ayrı satır) → her pakette çarpan ≥2×

## Kanıt (uydurma yok)
- [ ] Sayfadaki her iddianın yanında `[K: kanit/NN#…]` var; bağlanamayan iddia silindi
- [ ] Yorum/puan/sayı alanları ya gerçek kaynaklı ya `{YER_TUTUCU}`; yer tutucu yayından önce kurucu tarafından doldurulacak diye DURUM.md'de
- [ ] Mekanizma görüntüsü gerçek (alıcı/numune); AI görüntü ise etiketli ve "aldım" diyen AI kişi yok
- [ ] Önce-sonra, uzman/doktor, sertifika ifadesi yok (ya da belge dosyası bağlı)

## Teklif
- [ ] Çizili fiyat yalnız kanıtlı (`karsilastirma_kaniti`); AB/UK/TR'de son 30 gün en düşük fiyat kuralına uygun
- [ ] Aciliyet yok ya da gerçek tarihli kampanya (TR'de hiç yok)
- [ ] Garanti metni = gerçekten uygulanacak politika (kurucu onayı KARARLAR.md'de)
- [ ] Kargo vaadi = `teslim_gun`; gümrük/ek ücret müşteriye sürpriz değil (UK: tek toplam fiyat)

## Pazar
- [ ] **TR:** kargo dahil fiyat · koşulsuz iade süresi · taksit görünür · mesafeli satış + ön bilgilendirme bağlantısı · baskı cümlesi yok
- [ ] **ABD:** FTC — sahte/AI yorum yok, ilişkili tanıtım açıklaması görünür
- [ ] **UK:** DMCC — sahte yorum yok, gizli ücret yok
- [ ] **AB:** Omnibus 30 gün · GPSR (üretici, AB sorumlu kişi, ürün tanımlayıcı, yerel dilde uyarı) · gerçekçi AI video etiketi
- [ ] **FR:** AI insan → "Image virtuelle" · "soldes" yalnız resmî dönemde · Fransızca
- [ ] **DE:** fatura/PayPal görünür · Impressum · iade adımları

## Sınır
- [ ] Rakip metni kopyalanmadı (yalnız yapı)
- [ ] Yayın, fiyat girişi, uygulama kurulumu, e-posta gönderimi yapılmadı — kurucu kararı bekleniyor (DURUM.md "Bekleyen onaylar")
