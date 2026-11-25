# İşletme profili ve sürüm (ilk oturum)

Danışanın işletme kararları kendisine aittir; eklenti varsayılanları (kapıda ödeme yok, kat >= 2,2, satış >= 399 TL) kullanıcının kararı değildir. Bu yüzden profil sorulur.

## Profil sorusu (tek seferlik, sohbet sorusu; betik sormaz)
`.ekip/isletme-profili.tsv` yoksa ürün avına (`hunter`) başlamadan TEK mesajda en çok 5 kısa soru sor:
1. Kapıda ödeme kullanıyor musun? Kullanıyorsan oranı yüzde kaç, sipariş başına ek ücret kaç TL?
2. Hedef satış/alış katı (alt sınır)?
3. En düşük satış fiyatı (TL)?
4. Markanın kendi reklam ROAS'ı (biliyorsan)?
5. Satış kanalı: kendi Shopify mağazan mı, pazar yeri mi?

Cevabı yaz (yalnız verilenler; "bilmiyorum" = yazma):
`python3 "${CLAUDE_PLUGIN_ROOT}/ortak/profil.py" yaz kapida_odeme_orani_yuzde=30 kapida_ek_ucret=25 kat_min=2.5 satis_tl_min=399 marka_roas=2.8 kanal=shopify`

- Profil yoksa betikler eklenti varsayılanını kullanır ve çıktıda `PROFIL: yok` yazar; bunu kullanıcıya bir kez söyle.
- Soru bir daha sorulmaz; değişirse aynı komutla güncelle. Okuyanlar: `trendyol_kontrol.py` (kat_min, satis_tl_min), `tr_marj.py` (kapıda ödeme, marka_roas), `marj_hesap.py` (TR kapıda ödeme).
- Hedef pazar TR ise `ortak/bilgi/` (ABD/Instagram ağırlıklı) yerine TR kaynaklarını (Trendyol, Meta Reklam Kütüphanesi TR) öne çıkar; ilk 20 üründen sonra eşikleri kalibre et.

## Sürüm
Oturum kancası "Eklenti sürümü X" satırını basar; ilk mesajda bir kez söyle. Eski sürümle (örn. 0.4.0) çalışıyorsa güncelleme iste (README "Güncel sürüm nasıl kontrol edilir").

## İlk test kanalı
Reklam hesabı yoksa ya da kapandıysa kanalı sor ve `studio/referans/olcum-ve-test-plani.md` "Kanal seçimi" bölümüne yönlendir. Hesap kapanması/yasaklanması için platform kurallarını aşan yol önerme (yeni hesap açma önerme).
