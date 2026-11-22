# Kurgu kuralları kontratı — şablon (`is/NN/kurgu/KURALLAR.md`)

Ürün başına bir dosya. **Üretimden ÖNCE**, ön-üretim hükmünden sonra (Aşama 5, kredi onayından önce) `fixer` doldurur.
Kurgucu brief'i yalnız bu dosyaya işaret eder; kör jüri bu dosyayı GÖRMEZ. Bu ürüne özgü her yeni kural önce buraya girer
(kural terfisi URE-02: eklentiye ancak ikinci örnekte). Kontratta olmayan bulgu aşağıdaki öneri bölümüne girer.
Seri ortasında kontrat değişmez; değişiklik ancak sonraki seride ya da kullanıcı açık talimatıyla (tarih + gerekçe).

Kopyala → `is/NN/kurgu/KURALLAR.md`, `<…>` alanlarını doldur, uymayan satırı silme: "uygulanmaz" yaz.

```markdown
# KURALLAR — <ürün> · seri <ad/tarih>
İmza: ön-üretim <ELESTIRI-onuretim dosyası> · <YYYY-AA-GG>
İzleyici: <kart.md sektör satırı, ör. soğuk ABD araç-modifiye izleyicisi> · pazar: <ABD/TR>
Ağır kusurlar: ${CLAUDE_PLUGIN_ROOT}/skills/cut/referans/agir-kusurlar.md · kalıcı kurallar: ${CLAUDE_PLUGIN_ROOT}/ortak/kurallar.md

| # | Alan | Kural | Eşik (ölçülebilir) | Nasıl ölçülür |
|---|---|---|---|---|
| K1 | iskelet | süre ve vuruş | toplam <12–15> sn = Σ(klip aralığı / hız) + donuk kareler; her klip aralığı ≤ 4,03 sn (Flow klibi ölçülen süresi); plan ≥ <2> vuruş (<0,86> sn); drop <3,43> sn | ayar JSON + pano |
| K2 | kanca | ürün ilk ... sn'de | değişmiş ekran ≤ <0,9> sn; durağan stok plan ilk plan değil | pano 10 fps |
| K3 | stok sınırı | stok (eski hal) planı | ≤ <0,86> sn, ilk plan değil | ayar JSON |
| K4 | giriş türü | seride açılış dağılımı | aynı açılış karesi ≤ 1 video; giriş türleri: <sonuç-önce / punch / söküm / telefon> en fazla <n>'er | plan tablosu |
| K5 | yazı konumu | ürün/plaka kapatma | yakın planda konum ≤ <0,15>; plaka/ekran üstünde ve ürünün üstünde yazı yok; alt %20 + sağ %15 boş | kontrol karesi — her kırpım/zoom planı için ayrı kare |
| K6 | yazı biçimi | satır/kelime | ≤ <5> kelime, ≤ 2 satır, yetim kelime yok | pano |
| K7 | telefon = ekran | seçilen = görünen | dokunulan karo sonraki her planda araçta; video seçilen içerikle biter | pano |
| K8 | kapanış | CTA planı | CTA değişmiş ekranlı planda, ≥ 3 sn; stok rozetle bitmez; ad/fiyat kartı yok (ICE-01) | pano |
| K9 | ses | müzik girişi, drop ve seviye | müzik girişi SES-01 (`muzik_giris.tuttu`); −14 ±1 LUFS, tepe ≤ −1 dBTP, drop varsa drop_artis <6–10> dB, drop dışı sıçrama ≤ +10 dB, delik yok; müzik seçim gerekçesi (ses-tasarimi §2b) | `ses_olc.py --drop --muzik_stem --kapi` |
| K10 | malzeme | klip yeterliliği | özne başına video V ise klip ≥ 5 + 3·(V−2); ortak klip ≤ 4 video | plan × klip sayımı |
| K11 | iddia | yazıda/captionda | yasak: <fiyat (ICE-01), yasallık, su geçirmezlik, kurulum süresi, "herkes soruyor"> | metin |
| K12 | ikna ve işlev | 2. izleme testi | izleyici 2. izlemede ürünün işlevini çıkarır (açık ya da imâ: <ses/yazı/görüntü>); yazıların ≥ yarısı merak/ikna/kimlik, özellik listesi yok; ABD hedefinde ≥ 1 ABD kültür unsuru: <…> | eleştirmen iki cümlesi + yazı sınıflaması |
| K.. | <ürüne özgü> | | | |

## Kabul edilen sınırlar (puan kırılabilir, düzeltme istenmez)
- <ör. plaka ay etiketi M3 kliplerinde değişiyor>

## Önceki seriden gelen YENİ KURAL önerileri (bu kontrata alınanlar)
- <tarih · kaynak video · kural · alındı/alınmadı>

## Bu seride çıkan YENİ KURAL önerileri (sonraki seriye)
- <direktör raporundaki ÜRÜN kapsamlı reçeteler>
```

Ölçüt: seri başına kurgu SONRASI eklenen kural sayısı ≤ 1 (önceki seri: 4). Fazlası çıkarsa ön-üretim imzası eksik demektir.
