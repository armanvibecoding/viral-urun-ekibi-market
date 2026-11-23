# İtiraz bankası (pazar başına)

Ne zaman okunur: akış adım 5 (itiraz SSS). Bu liste **soru yönü**dür, cevap metni değildir: her cevap ürünün gerçek özelliğinden,
kanıt dosyasından ya da kurucunun gerçek politikasından yazılır. Cevabı bilinmeyen soru sayfaya konmaz → `Bulunamayan veri`.
Sıra: önce rakip reklam yorumlarında **gerçekten geçen** sorular (sayıyla: "12 yorumda 'beden?'"), sonra bu banka.
Etiket: pazar kartı dayanağı [S#] `pazar-teklif-kurallari.md` kaynak listesinde.

## Ortak (her pazar)
| İtiraz | Cevap yönü (gerçek veriyle doldur) |
|---|---|
| Gerçekten çalışıyor mu? | mekanizmayı gösteren gerçek video/alıcı fotoğrafı; kanıt dosyası §7 bağlantısı. Yoksa soru sayfaya girmez |
| Ne zaman gelir? | `teslim_gun` (marj_hesap.py) + takip numarası verilir mi |
| Beğenmezsem? | iade süresi, kim öder, adımlar (garanti sütunuyla birebir) |
| Kalitesiz/ucuz malzeme mi? | malzeme, ölçü, ağırlık — ürün sayfası/numune ölçümü |
| Bana/evime/hayvanıma uyar mı? | ölçü tablosu, uyumlu modeller, kim için **değil** |
| Güvenli mi? | sertifika yalnız belgeliyse; çocuk/elektrikli ürün: belge yoksa satış kararı kanıt savcısına geri |

## TR — güven ve iade ağırlıklı [S4, S11]
| İtiraz | Cevap yönü |
|---|---|
| Dolandırıcı mı / gerçek firma mı? | unvan, adres, telefon/WhatsApp, mesafeli satış sözleşmesi bağlantısı |
| Kargo ücreti çıkar mı? | "kargo dahil" — fiyatın içinde olduğunu tek cümleyle |
| Kapıda ödeme var mı? | varsa koşulu (ek ücret varsa açıkça); yoksa güvenli ödeme altyapısının adı |
| Taksit var mı? | kaç taksit, hangi kartlar |
| İade gerçekten koşulsuz mu? | süre, iade kargosu kimde, para kaç günde döner |
| Yurt dışından mı geliyor, gümrük çıkar mı? | yerel stok ise söyle; değilse gümrük kimde — belirsizse satış yapılmaz |

## ABD
| İtiraz | Cevap yönü |
|---|---|
| Shipping time? | gerçek iş günü aralığı; Çin çıkışlıysa saklama |
| Is it worth the price vs Amazon? | farkı somut (paket, garanti, özellik) — rakibi kötüleme yok |
| Return policy? | gün sayısı, kim öder |
| Will I be charged extra fees/duties? | ABD'de de minimis yok → gümrük satıcıda mı (fiyata dahil mi) açıkça |
| Can I pay later? | BNPL varsa adı [S19] |

## UK
| İtiraz | Cevap yönü |
|---|---|
| Any extra charges at checkout/delivery? | toplam fiyat tek; VAT ve gümrük dahil (DMCC gizli ücret yasağı [S42]) |
| Delivery to UK — how long? | gerçek gün aralığı |
| Returns? | 14 gün + kendi garantin |

## DE
| İtiraz | Cevap yönü |
|---|---|
| Kauf auf Rechnung / PayPal? | mevcut ödeme yöntemleri [S33] |
| Rücksendung — wie, wer zahlt? | adım adım; iade oranı yüksek pazar [S35] |
| Wer ist der Verkäufer? (Impressum) | şirket bilgisi |
| CE / Sicherheitshinweise? | GPSR bilgisi: üretici, AB sorumlu kişi, uyarılar Almanca |

## FR
| İtiraz | Cevap yönü |
|---|---|
| Livraison et retours ? | süre, ücret, 14 gün |
| Paiement sécurisé / en plusieurs fois ? | mevcut yöntemler |
| L'image est-elle réelle ? | AI insan görüntüsü kullanıldıysa "Image virtuelle" ibaresi zaten görünür [S43] |

## ES
| İtiraz | Cevap yönü |
|---|---|
| ¿Cuánto tarda el envío? | gerçek gün |
| ¿Puedo devolverlo? | süre, ücret |
| ¿Opiniones reales? | yalnız gerçek alıcı yorumu/UGC (izinli) [S45]; yoksa soru sayfaya girmez |
