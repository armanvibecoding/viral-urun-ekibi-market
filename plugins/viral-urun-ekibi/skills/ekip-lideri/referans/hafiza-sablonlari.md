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

## .ekip/GERI-BILDIRIM.md  (geri bildirim defteri; satır silinmez, durum güncellenir — SKILL §5b)
```
# GERİ BİLDİRİM DEFTERİ — kurucu geri bildirimi + eleştirmenin KALICI reçeteleri. Kapı: scripts/geri_bildirim_kontrol.py
# Durum: AÇIK · İŞLENDİ · TEKRAR-DÜZELTİLDİ (aynı anahtar 2. kez → üretici ajan/beceri dosyası düzeltildi) · REDDEDİLDİ (gerekçe)
| # | Tarih | Kaynak | Anahtar | Geri bildirim / kusur | İşlenen dosya:bölüm | Durum | Bildirildi |
|---|---|---|---|---|---|---|---|
| 1 | YYYY-AA-GG | kurucu | ani-muzik | "müzik bir anda açılıyor" (H1, 12,6 sn) | skills/video-kurgu/referans/ses-tasarimi.md:§2 | İŞLENDİ | evet |
```

## is/NN-urun-adi/DURUM.md  (ürün başına aşama kaydı)
```
# <ürün> — aşama kaydı
Pazar: <TR/ABD>   Kredi: harcanan X / onaylı Y
| Video | Senaryo | Kareler | Klipler | Kurgu | Teslim |
|---|---|---|---|---|---|
| V01 | ✅ | ✅ | 2/3 | — | — |
```
