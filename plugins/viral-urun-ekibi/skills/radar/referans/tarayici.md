# Tarayıcı modu (Claude in Chrome + instagram.com) — Windows, Linux, iPhone'suz Mac

Aynı iş, telefonda değil Chrome'da `instagram.com` üzerinde yapılır. Gerekenler: Chrome + **Claude in
Chrome** eklentisi bağlı, kullanıcı Instagram'a **kendisi** giriş yapmış. Claude şifre yazmaz, giriş
yapmaz; giriş ekranı görürse kullanıcıdan girmesini ister ve bekler.

> Durum: bu mod iPhone moduyla aynı kurallarla yazıldı ama bu pakette gerçek bir turla ölçülmedi.
> Aşağıdaki "doğrula" işaretli adımları ilk turda ekran görüntüsüyle kontrol et; tutmayanı
> `.ekip/DERSLER.md`'ye yaz.

## Başlangıç
1. Chrome araçlarını tek seferde yükle (tabs_context_mcp, navigate, computer, read_page, find,
   get_page_text, tabs_create_mcp). Birden çok tarayıcı bağlıysa **bu bilgisayardakini** seç
   (`list_connected_browsers` → `select_browser`); varsayılan yanlış olabilir.
2. Yeni sekme → `https://www.instagram.com/reels/` (Reels akışı) ya da `https://www.instagram.com/explore/`.
3. Ekran görüntüsü al: giriş sayfası, çerez onayı ya da "Daha sonra tekrar dene" var mı bak.

## Döngü (bir video = bir aday)
1. **Gör:** ekran görüntüsü al; videoda ürün ne, ekran yazısı ne (kanca)? Gerekirse 3–4 sn arayla 2–3
   görüntü daha (video ilerlesin).
2. **Oku:** `find`/`read_page` ile hesap adı, beğeni, yorum sayısı, açıklama metni. Sayı ekranda
   görünmüyorsa "görünmüyor" yaz — tahmin etme.
3. **Profil:** hesap adına tıkla ya da `https://www.instagram.com/<hesap>/` aç → takipçi, gönderi sayısı,
   bio, bio linki. Reels izlenme sayıları profilin **Reels** sekmesindeki ızgarada görünür
   (`https://www.instagram.com/<hesap>/reels/`) — doğrula. Bio linkindeki siteye yalnız bakılır.
4. **Karar + kayıt:** `referans/urun-tanima.md` → `kontrol.sh` → `ekle.sh`.
5. **Sonraki video:** Reels sayfasında `computer` aracıyla klavye `ArrowDown` (ya da video üstünde fare
   tekerleği `scroll`) — doğrula: URL'deki reel kimliği değişti mi. Profilden döndüysen tarayıcı geri.

## Tuzaklar
- `javascript_tool` sayfadan izole çalışır; `window.scrollTo` Instagram'ın kendi kaydırma olayını
  tetiklemez. Kaydırma ve geçişi `computer` aracının gerçek tuş/tekerlek olaylarıyla yap.
- Yavaş git: video başına en az 5–10 sn. "Daha sonra tekrar dene", boş akış veya giriş isteği = kısıt
  işareti → turu bitir, kayıtları yaz, en az 1 saat dur.
- Sponsorlu gönderi ("Sponsorlu"/"Reklam") da veri: aynı pazarda reklam verildiğinin kanıtıdır, not et.
- Instagram web arayüzü sık değişir: düğme yerini ezberleme, her adımda ekran görüntüsüne bak.
- Bildirim/DM penceresi açılırsa kapat (Escape), hiçbir şey yazma.

## ChatGPT
Aynı iş ChatGPT ajan modunun tarayıcısıyla da yapılabilir: eklentideki `ekler/chatgpt/radar.md`.
