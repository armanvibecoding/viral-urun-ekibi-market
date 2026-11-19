# senaryolar.json biçimi (alt ajan bunu yazar, betikler bunu okur)

```json
{
  "urun": "Mama piyanosu", "pazar": "TR", "cta_kelime": "PİYANO",
  "ortak": {"who": "one orange tabby cat with a white chest",
            "where": "a real living room with a wooden floor", "light": "soft daylight from one window"},
  "videolar": [
    {"no": 1, "mekanizma": "M8", "sablon": "S2", "an": "Gece 3'te kedi mama ister, sahibi uyuyor",
     "kanca": "Gece 3'te uyanmaktan kurtuldum", "aile": "K7", "kimlik": false,
     "giris": "gece kamerası, kedi yatakta", "ortam": "gece yatak odası", "ozne": "turuncu tekir",
     "sahneler": [
       {"eylem": "Kedi uyuyan sahibinin omzuna pati atar",
        "prompt": {"scene": "night bedroom, a cat stands on the bed next to a sleeping person's shoulder",
                   "position": "the cat's paw already touches the person's shoulder",
                   "camera": "static, high corner like a night camera",
                   "action": "the cat taps the sleeping person's shoulder once with its paw.",
                   "audio": ["soft paw tap on the shoulder"], "ambient": ["quiet room tone"]}},
       {"eylem": "Kedi piyanonun en dış tuşuna basar, mama tuşların altındaki açıklıktan düşer", "prompt": {"...": "..."}},
       {"eylem": "Kedi düşen mamayı yer, kameraya bakar", "prompt": {"...": "..."}}
     ],
     "etkilesim_sahne": 2, "sonuc_sahne": 2, "cta": "Yorumlara \"PİYANO\" yaz, linki DM'den atayım",
     "neden": "Gece problemi karesi (AI'ın kazandığı an) + net çözüm"}
  ]
}
```

| Alan | Zorunlu | Not |
|---|---|---|
| `no, mekanizma, sablon, an, kanca, aile, sahneler, etkilesim_sahne, sonuc_sahne, cta, neden` | evet | `kanca` K13'te boş; `mekanizma` birden çoksa "M1+M3" |
| `kimlik` | evet | kancada kimlik kelimesi (kedi annesi, dog dad…) varsa `true` |
| `giris` | evet | ilk klibin/ilk karenin kimliği (ortak klip kodu ya da "C1-k1 egzoz"); aynı giriş en fazla 2 videoda |
| `ortam` | evet | mekân + zaman ("gece yatak odası", "çatı otoparkı, mavi saat"); aynı ortam en fazla 6 videoda |
| `ozne` | seride özne değişiyorsa | araç/renk/hayvan ("mat siyah G63"); aynı özne ardışık iki videoda olmaz |
| `kultur` | ABD pazarında evet | görünen ABD kültür unsuru ("Sunday football, banliyö oturma odası"); `pazar-katmani.md` §1 |
| `yazilar` | isteğe bağlı | kanca dışı ekran yazıları listesi; fiyat kuralı ICE-01 (betik tarar) |
| kök `kreatif` | isteğe bağlı | `organik` (varsayılan) · `reklam`; ICE-01 yalnız `organik`te uygulanır |
| `sahneler[].eylem` | evet | Türkçe, tek eylem, tablo için |
| `sahneler[].prompt` | ilk 5 video | İngilizce. `scene`, `action` zorunlu; `position`, `camera`, `audio`, `ambient`, `who`, `where`, `light` isteğe bağlı (yoksa `ortak`tan) |
| `prompt.audio` | — | yalnız ACTION'daki eylemin sesi, sebebiyle: "single piano note as the white key goes down" |
| `prompt.ambient` | — | ortam sesi (room tone, hum, birds); kapıdan muaf |

Kontrol: `python3 scripts/senaryo_kontrol.py is/NN/senaryolar.json` → `senaryolar.md` + `.csv`.
Prompt: `python3 scripts/prompt_uret.py is/NN/senaryolar.json is/NN/kilit.txt --video 1 2 3 4 5`.

## kilit.txt örneği
```
PRODUCT: Low rectangular red pet toy on the floor with four big white keys at the front and a clear red lid on top; about 20 cm wide, smaller than a cat. Nothing else on it.
MECHANISM: Treats appear ONLY at the moment a white key goes down, from a narrow opening at floor level directly below the white keys; if no key is pressed, no treat appears.
WRONG: treats appearing without a key press, the lid opening by itself
```
Ekranlı ürün örneği: `SCREEN: the round screen keeps exactly the content shown in the start frame - the same glowing icon on a black background, same colors, same brightness; no new image, no text, no flicker.`
İçerik karede üretilir; değişim kesimde, aynı kadrajın yeni içerikli karesiyle (`flow-ve-chatgpt.md` "Sonra karesi"). Bindirme istisnadır (`video-kurgu/referans/ekran-bindirme.md`).

## is/NN-urun/DURUM.md örneği
```
# Mama piyanosu — aşama kaydı
Pazar: TR   Kredi: harcanan 36 / onaylı 72   Aşama: 6 (Flow)   CTA: PİYANO
| Video | Senaryo | Kareler | Klipler | QC | Kurgu | Teslim |
|---|---|---|---|---|---|---|
| V07 (örnek) | ✅ | 3/3 ✅ | 2/3 | — | — | — |
Sıradaki adım: V07_S3 klibini üret (deneme 1/3), sonra klip_qc.
```
