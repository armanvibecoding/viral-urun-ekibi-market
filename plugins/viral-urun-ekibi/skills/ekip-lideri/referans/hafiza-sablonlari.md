# Hafıza şablonları (`.ekip/` ilk kurulumda bunlarla oluşturulur)

## .ekip/DURUM.md  (≤40 satır, her aşama sonunda ÜZERİNE yazılır)
```
# DURUM — son güncelleme: YYYY-AA-GG SS:DD
Aktif iş: <ör. 04-dijital-amblem — 30 video>
Aşama: <ör. ai-video-kreatif / Aşama 5 (kareler) — 12/90 kare tamam>
Sıradaki adım: <tek cümle, doğrudan uygulanabilir>
Bekleyen onaylar: <ör. V01–V05 için 180 kredi — kullanıcı onayı bekleniyor | yok>
Açık sorular: <yok | soru>
Son çıktılar: <dosya yolları, en fazla 5>
Diğer işler: <ör. 02-x: kurgu bitti, teslim edildi>
```

## .ekip/KARARLAR.md  (yalnız ekleme)
```
# KARARLAR — kullanıcının verdiği kararlar. Silinmez; değişirse yeni satır eklenir (son satır geçerlidir).
- YYYY-AA-GG | pazar | Türkiye
- YYYY-AA-GG | bütçe | Flow için tek seferde en fazla 200 kredi, üstü sorulur
```

## .ekip/DERSLER.md  (yalnız ekleme)
```
# DERSLER — ölçülmüş bulgular ve tekrar eden hatalar. Her satır: konu: ders (kanıt dosyası)
```

## is/NN-urun-adi/DURUM.md  (ürün başına aşama kaydı)
```
# <ürün> — aşama kaydı
Pazar: <TR/ABD>   Kredi: harcanan X / onaylı Y
| Video | Senaryo | Kareler | Klipler | Kurgu | Teslim |
|---|---|---|---|---|---|
| V01 | ✅ | ✅ | 2/3 | — | — |
```
