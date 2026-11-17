# Kurgu kuralları kontratı — şablon (`is/NN/kurgu/KURALLAR.md`)

Ürün başına bir dosya. **Üretimden ÖNCE**, ön-üretim eleştirisinde (Aşama 5, kredi onayından önce) doldurulur ve imzalanır.
Kurgucu brief'i yalnız bu dosyaya işaret eder; teslim eleştirmeni yalnız bu dosyadaki kurallara + puan cetvelinin ağır
kusurlarına göre düşürür. Kontratta olmayan bulgu "YENİ KURAL" olur (videoyu düşürmez, aşağıdaki öneri bölümüne girer).
Seri ortasında kontrat değişmez; değişiklik ancak sonraki seride ya da kullanıcı açık talimatıyla (tarih + gerekçe).

Kopyala → `is/NN/kurgu/KURALLAR.md`, `<…>` alanlarını doldur, uymayan satırı silme: "uygulanmaz" yaz.

```markdown
# KURALLAR — <ürün> · seri <ad/tarih>
İmza: ön-üretim eleştirisi <ELESTIRI-onuretim dosyası> · <YYYY-AA-GG> · eleştirmen çağrı no <n>
İzleyici: <kart.md sektör satırı, ör. soğuk ABD araç-modifiye izleyicisi> · pazar: <ABD/TR>
Puan cetveli: ${CLAUDE_PLUGIN_ROOT}/skills/video-kurgu/referans/puan-cetveli.md (sürüm tarihi <…>)

| # | Alan | Kural | Eşik (ölçülebilir) | Nasıl ölçülür |
|---|---|---|---|---|
| K1 | iskelet | süre ve vuruş | toplam <12–15> sn; plan ≥ <2> vuruş (<0,86> sn); drop <3,43> sn | ayar JSON + pano |
| K2 | kanca | ürün ilk ... sn'de | değişmiş ekran ≤ <0,9> sn; durağan stok plan ilk plan değil | pano 10 fps |
| K3 | stok sınırı | stok (eski hal) planı | ≤ <0,86> sn, ilk plan değil | ayar JSON |
| K4 | giriş türü | seride açılış dağılımı | aynı açılış karesi ≤ 1 video; giriş türleri: <sonuç-önce / punch / söküm / telefon> en fazla <n>'er | plan tablosu |
| K5 | yazı konumu | ürün/plaka kapatma | yakın planda konum ≤ <0,15>; plaka/ekran üstünde yazı yok; alt %20 + sağ %15 boş | kontrol karesi |
| K6 | yazı biçimi | satır/kelime | ≤ <5> kelime, ≤ 2 satır, yetim kelime yok | pano |
| K7 | telefon = ekran | seçilen = görünen | dokunulan karo sonraki her planda araçta; video seçilen içerikle biter | pano |
| K8 | kapanış | CTA planı | CTA değişmiş ekranlı planda, ≥ 3 sn; stok rozetle bitmez; organik videoda ad/fiyat kartı yok | pano |
| K9 | ses | müzik girişi, drop ve seviye | açılış diegetik ses; müzik 0. sn'de −30 dB'den 1,5–2 sn rampa, `muzik_giris.tuttu` (ağır kusur); −14 ±1 LUFS, tepe ≤ −1 dBTP, drop varsa drop_artis <6–10> dB, drop dışı sıçrama ≤ +10 dB, delik yok; müzik seçim gerekçesi (ses-tasarimi §2b) | `ses_olc.py --drop --muzik_stem --kapi` |
| K10 | malzeme | klip yeterliliği | özne başına video V ise klip ≥ 5 + 3·(V−2); ortak klip ≤ 4 video | plan × klip sayımı |
| K11 | iddia | yazıda/captionda | yasak: <fiyat (organikte ekranda hiç), yasallık, su geçirmezlik, kurulum süresi, "herkes soruyor"> | metin |
| K12 | ikna ve işlev | 2. izleme testi | izleyici 2. izlemede ürünün işlevini çıkarır (açık ya da imâ: <ses/yazı/görüntü>); yazıların ≥ yarısı merak/ikna/kimlik, özellik listesi yok; ABD hedefinde ≥ 1 ABD kültür unsuru: <…> | eleştirmen iki cümlesi + yazı sınıflaması |
| K.. | <ürüne özgü> | | | |

## Kabul edilen sınırlar (puan kırılabilir, düzeltme istenmez)
- <ör. plaka ay etiketi M3 kliplerinde değişiyor>

## Önceki seriden gelen YENİ KURAL önerileri (bu kontrata alınanlar)
- <tarih · kaynak video · kural · alındı/alınmadı>

## Bu seride çıkan YENİ KURAL önerileri (sonraki seriye)
- <teslim eleştirisinden; puanlar.jsonl `yeni_kural` alanıyla aynı metin>
```

Ölçüt: seri başına kurgu SONRASI eklenen kural sayısı ≤ 1 (önceki seri: 4). Fazlası çıkarsa ön-üretim imzası eksik demektir.
