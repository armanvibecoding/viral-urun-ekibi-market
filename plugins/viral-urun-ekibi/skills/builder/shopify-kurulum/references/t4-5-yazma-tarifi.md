# TEKNİK EK T4.5: şablon yazma tarifi (GEÇERLİ YOL)

Kaynak: `kaynak/KAYNAK-PROMPT.md`, satır 365–408. Adımlar ve kurallar aynı; kaynaktaki satır içi Python kodu 0.3.0'da `scripts/t4_yama.py` betiğine taşındı ve testlendi (`tests/test_t4_yama.py`, gerçek Ana Tema şablonlarıyla).
Şablon yazımının tek geçerli yolu budur. `theme-bash-yolu.md` ölçülmemiş alternatiftir, kullanıcı onayı olmadan kullanılmaz.

Betik neyi durdurur (çıkış kodu 1, `YAZMA: …`, çıktı dosyası yazılmaz): olmayan bölüm ya da blok; ne şablonda ne tema şemasında bulunan ayar adı (yazım hatası dahil); şemadaki tipe uymayan değer (checkbox, sayı aralığı, seçenek listesi, richtext etiketi, görsel adresi); aynı yolun iki kez verilmesi; yama sonrası bölüm ya da blok sayısının, sırasının, tipinin değişmesi; okunan şablonun sunucunun bildirdiği boyuttan ya da T4.0 bölüm sayısından farklı olması.

---

## 0. Betiği bul (oturumda bir kez)
Kod aracında çalıştır:
```bash
find / -name t4_yama.py -path "*shopify-kurulum*" 2>/dev/null | head -1
```
Çıkan mutlak yolu sonraki komutlarda `YAMA` olarak kullan. `ayar-sozlugu.json` aynı klasördedir; betik onu kendisi bulur (ayar adı ve değer kontrolü buradan gelir).
- Bulunamazsa: skill'deki `scripts/t4_yama.py` dosyasını oku ve çalışma klasörüne birebir yaz. Sözlüğü taşıyamazsan betik sözlüksüz çalışır: yalnız şablonda zaten bulunan ayarları yazar, yeni ayar adı eklemez. Eklenemeyen ayarı tema editörü listesine koy.
- Kod aracın (Python) yoksa şablon yazma; bana tema editöründe tıklanacak yerleri bölüm bölüm ver.

## 1–6. Her JSON dosyası için ayrı ayrı
1. **Yedek:** `themeFilesCopy` ile dosyayı aynı klasörde `-yedek` ekli adla kopyala (`templates/index.json` → `templates/index.yedek.json`, `templates/product.nis-gadget.json` → `templates/product.nis-gadget-yedek.json`). `config/settings_data.json` kopyalanamazsa yedeksiz devam et; 6. adımdaki kontrol yeter.
2. **Oku:** `theme(id) { files(filenames: ["<dosya>"]) { nodes { filename size body { ... on OnlineStoreThemeFileBodyText { content } ... on OnlineStoreThemeFileBodyUrl { url } } } } }`. `content` metnini HİÇ DEĞİŞTİRMEDEN `taban.json` dosyasına yaz, `size` değerini not et. Gövde `url` olarak gelirse aşağıdaki "Gövde adres olarak gelirse" bölümüne geç.
3. **Yama dosyası:** tablodaki HER ayar ayrı satır, metinler birebir. `yama.json`:
   ```json
   [{"yol": "e-serit/c1/i.icon", "deger": "truck"},
    {"yol": "e-serit/c1/m/b.text", "deger": "<p>Ücretsiz kargo</p>"},
    {"yol": "e-kars.disabled", "deger": false}]
   ```
   Yol: `<bölüm>[/<blok>/<alt blok>…].<ayar>`. Ayar `disabled` ise bölüm ya da blok açılır (`false`) ya da kapanır (`true`). Değerin tipi şemaya uymalı: checkbox `true/false`, sayı tırnaksız, richtext `<p>`/`<ul>`/`<ol>`/`<h1-6>` ile başlar, görsel `shopify://shop_images/<dosya-adı>`.
4. **Çalıştır:**
   ```bash
   python "$YAMA" --sablon taban.json --yama yama.json --cikti cikti.json --boyut <size> --bolum-sayisi <T4.0 bölüm sayısı>
   ```
   - Çıkış 0 ve son satır `GEÇTİ | … | <N> karakter | …` → 5. adıma geç. Üstteki `yol: eski -> yeni` satırlarını rapora koy.
   - Çıkış 1 ve `YAZMA: …` → YAZMA. Hatayı DEVAM KARTI'na yaz, sonraki dosyaya geç. `ayar yok` hatasında ayar adını tahminle değiştirip yeniden deneme; `tema-haritasi-t4.md`'ye bak, orada da yoksa o ayarı tema editörü listesine koy.
   - Çıkış 2 → komut yanlış yazıldı; kullanım mesajına göre düzelt.
5. **Yaz:** `cikti.json` metnini HİÇ DEĞİŞTİRMEDEN, tek karakter eksiltmeden `themeFilesUpsert` `value` alanına koy. Gönderdiğin metnin uzunluğu `GEÇTİ` satırındaki karakter sayısıyla aynı olmalı. Tek çağrıda eksiksiz gönderemiyorsan YAZMA (T0).
6. **Kontrol:** dosyayı sunucudan tekrar oku, `tekrar.json`'a yaz ve çalıştır:
   ```bash
   python "$YAMA" --kontrol tekrar.json --taban taban.json --yama yama.json
   ```
   `KONTROL GEÇTİ` çıkmazsa `themeFilesCopy` ile yedeği asıl dosyanın üstüne geri kopyala, raporda ✗ yaz ve dur.

İstisnalar:
- S.S.S. `faq` bölümüne yeni `question` / `category` bloğu eklenebilir. O dosyada komuta `--haric faq` ekle, yeni blokları yama dosyasının `bloklar` listesine yaz; mevcut bloklar silinemez, sırası değişemez:
  ```json
  {"haric": ["faq"],
   "bloklar": [{"bolum": "faq", "id": "q_kutu", "type": "question", "sonra": "q_teslim",
                "settings": {"question": "Kutuda ne var?", "answer": "<p>Cihaz ve taşıma kılıfı.</p>"}}],
   "degisiklikler": [{"yol": "faq.heading", "deger": "Sık sorulanlar"}]}
  ```
- `config/settings_data.json`: betik dosyayı kendisi tanır. Yol yalnız ayar adıdır (`{"yol": "badge_position", "deger": "top-left"}`), etkin preset'e yazılır. Harita yerine üst düzey anahtarların, preset adlarının ve bölüm anahtarlarının aynı kaldığını betik kontrol eder.
- `sections/*-group.json`: şablonla aynı yapıdadır, aynı komutla yazılır.

## Gövde adres olarak gelirse (`url`)
Büyük dosyada `body`, `content` yerine kısa ömürlü bir `url` olarak gelebilir. Sırayla dene:
1. **Python ile indir:**
   ```python
   import urllib.request
   open("taban.json", "wb").write(urllib.request.urlopen(URL, timeout=30).read())
   ```
   Adresin süresi dolduysa (403/404) 2. adımdaki sorguyu tekrarla, yeni `url` al. Çalışma (Work) modunda kod aracının ağ erişimi kapalıysa bu adım bağlantı hatası verir [DOĞRULA: Work ağ erişimi ve Shopify CDN adresine izin ölçülmedi]. Aynı adresi ikinci kez deneme, 2'ye geç.
2. **Sunucuda, parça parça oku (`theme_bash`):** yalnız OKUMA için kullan; yazma bu tarifle yapılır. İlk çağrıdan önce sunucudaki `/skills/editing-themes/SKILL.md`'yi oku. [DOĞRULA: `theme_bash` çıktı sınırı, `sha256sum` varlığı ve yayınlanmamış temada okuma ölçülmedi.]
   ```bash
   F=templates/product.nis-gadget.json
   wc -l < "$F"
   wc -c < "$F"
   sha256sum "$F"
   ```
   Sonra satır aralıklarıyla yazdır (bayt değil satırla böl; Türkçe harf iki parçaya bölünmesin): `sed -n '1,600p' "$F"`, ardından `sed -n '601,1200p' "$F"` … son satıra kadar. Her parçayı sırayla, HİÇ DEĞİŞTİRMEDEN dosyaya ekle. Sonra Python'da boyutu (`os.path.getsize`) ve `hashlib.sha256` değerini sunucudakiyle karşılaştır; ikisi de aynı değilse parçayı yeniden oku, yine tutmazsa YAZMA. `sha256sum` yoksa yalnız boyut ve satır sayısıyla karşılaştır.
3. **İkisi de olmazsa:** şablonu YAZMA, tema editörü listesine geç. Okuyamadığın dosyayı tahminle ya da sıfırdan ASLA yazma (T0).
