# Tedarik ve fatura

Bilgi notu (kullanıcının sorumluluğu): vergi ve fatura cümleleri hüküm değildir; mali müşavirle doğrula.

**Alış fiyatı kaynağı:** `alis_tl` tedarikçi fiyatıdır (AliExpress/1688 aynı ürün, ya da A kademesinde Trendyol perakende alımının GERÇEK maliyeti satın alma sonrası). Trendyol vitrin fiyatı `alis_tl` olarak yazılmaz (`denetle` HATA verir): o fiyat hedef satış/rakip fiyatıdır (`rakip_tl`). Tedarikçi bulunamadıysa ürün ELE değildir; SAT kartında "tedarikçi bulunamadı" notu olur.

| Kademe | Ne zaman | Nasıl | Risk |
|---|---|---|---|
| A. Test stoğu | ilk 5–20 satış | Trendyol'dan kendi adresine perakende alım, **kurumsal fatura** ile; kendi paketinle gönderim | stok parası bağlanır; fatura kurumsal değilse KDV indirilemez |
| B. Satıcıyla doğrudan | haftada ≥ 10 satış | Trendyol satıcı profilindeki firma unvanından doğrudan toptan; fatura firmadan firmaya | satıcı toptan vermeyebilir |
| C. Üretici / ithalat | ayda ≥ 100 satış | 1688 ya da yerli üretici; marj en yüksek | süre, gümrük, minimum adet |

- **Yasak varsayılan:** Trendyol siparişini doğrudan müşteri adresine göndermek. Paket ve fatura Trendyol satıcısından gider, fiyat müşteriye görünür, marka kırılır.
  Trendyol kullanım koşulları açısından durumu **doğrulanmadı**; bu yol yalnız kurucu açıkça isterse ve `KARARLAR.md`'ye yazılırsa açılır.
- Satın alma, numune, satıcıyla temas: kurucu onayı olmadan yok; onay `KARARLAR.md`'ye.
- Kanıt dosyasının "Tedarik ve fatura" bölümü hangi kademeyle başlanacağını ve fatura tipini yazar.
