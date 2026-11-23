# Düzeltme döngüsü ve kural terfisi (captain §5b ayrıntısı)

Amaç: kullanıcı aynı şeyi iki kez yazmasın; ama tek ürünün özel kuralı herkese açık eklentiye de sızmasın (URE-02).

## Defter satırı (`.ekip/GERI-BILDIRIM.md`, şablon `hafiza-sablonlari.md`)
tarih · kaynak (kullanıcı / direktör) · anahtar (ör. `ani-muzik`, `organik-fiyat`) · geri bildirim · işlenen dosya:bölüm · durum ·
bildirildi. Kullanıcı bir mesajda 5 şey söylediyse 5 satır.

## Basamak 1 — ilk örnek: ürün kontratı
- Kural bu ürünün kontratına (`is/NN/kurgu/KURALLAR.md`) ya da `.ekip/DERSLER.md`'ye yazılır; defterde "İşlenen dosya" o yoldur
  (`is/…` ya da `.ekip/…`), durum `İŞLENDİ`.
- İlk örnekte "İşlenen dosya" bir eklenti dosyasıysa (`agents/`, `skills/`, `ortak/`) kapı KALIR: "tek örnekten eklenti kuralı".
- İstisna yok; kullanıcı kuralın hemen herkese geçmesini istiyorsa bu bir aşımdır (`kapi-asimi` satırı, kendi cümlesiyle).

## Basamak 2 — ikinci örnek: eklentiye terfi
- Aynı anahtar ikinci kez (başka ürün ya da başka video) görüldüğünde kural yetmemiştir. O kusuru ÜRETEN ajan/beceri dosyası
  yerinde düzeltilir: yanlış yönlendiren cümleyi bul ve değiştir (yalnız kural eklemek yetmez; eski cümle silinmeden yenisi
  eklenirse ajan çelişkiyi eskisinden okur).
- Kural metni tek yerde yaşar: `ortak/kurallar.md`'ye kimlikle (alan öneki + sıra no) yazılır; diğer dosyalar yalnız kimliğe atıf yapar.
  Kapsam etiketi yazılır (sektör, pazar, format). Sektöre özgüyse `skills/cut/referans/sektor/<sektör>.md`'ye girer.
- Ölçülebiliyorsa kapıya çevir (betik eşiği) ve kırma testiyle kanıtla; kapıya çevrilen kuralın metni tek satıra iner.
- Yeni satırın durumu `TEKRAR-DÜZELTİLDİ`, dosya sütunu üretici dosya (`agents/…` ya da `skills/…`).
- Ders: `ortak/bilgi/dersler.md`'ye tarihli madde (ne yapılır/yapılmaz, çünkü, kanıt) ve `.ekip/DERSLER.md`'ye bir satır.

## Kapı (`geri_bildirim_kontrol.py`; `kapi.py` her iki geçişte koşturur)
AÇIK satır · dosyası olmayan satır · bildirilmemiş satır · ilk örnekte eklenti dosyası · tekrar eden kusurda üretici
düzeltilmemiş · defter hiç yok → geçiş kalır.

## Aylık budama (en güçlü modelle, ayda bir ya da sürüm başına)
Depo kökünde (kurulan eklentide değil, GitHub deposunda) `python3 scripts/butce_kontrol.py` çıktısına bakılır (beceri boyutu, tekrar eden kural, tarihli anlatı). 30 gündür hiçbir defter
satırında ya da kapıda tetiklenmeyen ve kapıya çevrilmiş kural metinden çıkar; çıkarılan `docs/gelistirici/ESKIDI/` altına kaydedilir.
