# iPhone modu (macOS + iPhone Yansıtma)

Instagram, iPhone Yansıtma penceresinde açık telefonda gezilir. Ekranı görmek için Claude
`ekran.sh` ile pencereyi yakalar ve görüntüyü **Read** ile açar; tıklama/kaydırma Swift araçlarıyla
gerçek fare olayı olarak gönderilir.

## Neden computer-use değil
Ölçüldü: iPhone Yansıtma penceresinde computer-use `scroll` ve `left_click_drag` içeriği kaydırmıyor;
computer-use `screenshot` bazı sürümlerde boş dönüyor ve tıklama hit-testi yanlış uygulamayı (Bildirim
Merkezi, Terminal) gösterip reddediyor. Bu yüzden ana yol aşağıdaki araçlardır. computer-use varsa yalnız
uygulamayı öne getirmek (`open_application`) için yardımcıdır.

## Kurulum (bir kez, kullanıcının proje klasöründe)
1. `sh "<beceri>/scripts/kur.sh"` → `.ekip/arac/` içine `tikla`, `kay` derlenir, betikler kopyalanır.
   `swiftc` yoksa betik `xcode-select --install` talimatını yazar; kullanıcıya bunu söyle ve bekle.
2. İzinler: Sistem Ayarları > Gizlilik ve Güvenlik > **Erişilebilirlik** ve **Ekran Kaydı** →
   Claude'u çalıştıran uygulama (Terminal ya da Claude) açık olmalı. Kullanıcı yapar; Claude açamaz.
3. iPhone Yansıtma açık, iPhone kilitli ve yakında, Instagram açık.
4. **Kalibrasyon gerekli:** `sh .ekip/arac/kalibre.sh` → pencere konumunu bulur, `konum.env` yazar,
   `ip.png` yakalar. `ip.png`'yi Read ile aç; geri oku, Reels'teki kullanıcı adı ve arama kutusu
   `konum.env`'deki noktalarda mı bak. Değilse dosyayı düzelt. Varsayılanlar tek bir iPhone'da ölçüldü.

## Araçlar (`.ekip/arac/`)
| Araç | İş |
|---|---|
| `ekran.sh [dosya]` | Pencereyi yakalar → `$TMPDIR/kesfet/ip.png` (900 px yükseklik). Koordinatlar bu görüntüye göredir |
| `dokun.sh PX PY [sn]` | ip.png koordinatına gerçek tık + bekle + yeniden yakala. Pencere önde değilse tıklamaz |
| `kaydir.sh asagi\|yukari\|sonraki [adet]` | Pencere ortasında tekerlek. `sonraki` = Reels'te sonraki video |
| `izle.sh AD [kare] [sn]` | Açık videodan kare yakalar → `is/kesfet/kareler/AD/sayfa.jpg` kontakt sayfası |
| `ara.sh METIN` | Ara sekmesinde hesap/kelime arar (yazmadan önce pencerenin önde olduğunu kontrol eder) |
| `begen.sh` | Çift dokunarak beğenir — yalnız `.ekip/KARARLAR.md`'de "beğeni izni: evet" varsa çalışır |
| `konum.env` | Geri oku / kullanıcı adı / arama kutusu noktaları (`GERI_X GERI_Y …`) |
| `klavye` | `us` veya `tr` — `ara.sh`'nin tuş düzeni |

## İki tarama yolu
1. **Reels zinciri (verimli):** bir ürün videosu aç → `izle.sh` → kullanıcı adına `dokun.sh $HESAP_X $HESAP_Y`
   → profili `ekran.sh` ile oku → geri (`dokun.sh $GERI_X $GERI_Y`) → `kaydir.sh sonraki`. Instagram benzer
   ürünleri art arda getirir. Akış reklama/tek kategoriye kayarsa Keşfet'e dön, yenile (`kaydir.sh yukari`).
2. **Keşfet ızgarası:** `ekran.sh` → kutunun merkezini ip.png'den oku → `dokun.sh` → aynı inceleme → geri.
   Satır bitince `kaydir.sh asagi`. Izgara kaydıysa kapaklar yer değiştirir: şüphede yeni `ekran.sh`.

## Tuzaklar (ölçülmüş dersler)
- Her kaydırma/tıklamadan sonra ip.png'ye bak: pencere kapanırsa video görülmeden geçilir. Pencere yoksa
  önce `open -a "iPhone Mirroring"`, sonra devam.
- Terminal/başka pencere iPhone penceresinin önüne geçerse olaylar yanlış uygulamaya gider. Betikler
  "önde değil" deyip durur; `open -a "iPhone Mirroring"` ile öne getir. Terminal tam ekrandaysa her
  komut masaüstü geçişi yapar → betik sonrası 1–2 sn bekle.
- Pencere öndeyken bile yazı başka uygulamaya gidebilir: `ara.sh` her adımda öne-gelme kontrolü yapar;
  kendi `osascript keystroke` komutunu yazma. Panodan yapıştırma iPhone'da onay diyaloğunda takılır.
- iPhone tuş düzeni kendiliğinden ABD↔TR değişebilir: her aramadan sonra kutudaki metni ip.png'de oku;
  bozuksa (`i` → `'`, `.` → `ç`) `.ekip/arac/klavye` dosyasını `us`↔`tr` değiştir.
- "iPhone Kullanımda" / "Kamera Kullanımda" ekranı = kullanıcı telefonu elde kullanıyor → dur, Excel ve
  not işine geç, kullanıcıya söyle; telefona dokunmaya çalışma.
- DM bildirim bandı ekranın üstüne iner: üst sıradaki kutuya basmadan hemen önce yakala; bant varsa
  5 sn bekle. Bildirime asla dokunma. Bildirim Merkezi açık kalırsa Escape:
  `osascript -e 'tell application "System Events" to key code 53'`.
- Açıklama paneli (siyah alt panel) açılırsa Escape; ses/müzik sayfası açılırsa geri.
- Kaydırma adımı tek makinede ölçüldü (`kay` 40×10 ≈ 400 px). Kaymıyorsa `KAY_TIK=80 sh kaydir.sh asagi`.
- Başka bir Claude oturumu fareyi/ekranı kullanıyorsa iki oturum çakışır → kullanıcıya söyle, bekle.

## Windows'ta çalışmaz
Bu modun tamamı (iPhone Yansıtma, Swift, osascript, screencapture) yalnız macOS'tadır. Windows'ta
`referans/tarayici.md`.
