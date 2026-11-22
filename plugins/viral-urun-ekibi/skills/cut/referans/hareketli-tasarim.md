# Hareketli tasarım katmanı (cut Aşama 8b; SKILL.md'den taşındı, içerik aynı)

`studio` "Görüntü kaynağı önceliği" madde 4'ün uygulandığı yer: kinetik tipografi (vuruşa oturan, vurgu
kelimesi renkli), geçiş, ilerleme/sayaç, UI kartı, önce/sonra silmesi. ffmpeg temel kurguyu (klip, kesim, ses) yapar;
hareketli katmanı HyperFrames üretir. Ön koşul: Node 22+ ve `npx hyperframes doctor --json` → `ok` (yoksa `captain`
kurulum kontrolü; kurulumu kullanıcı onaylar). Bu katman kurulamıyorsa yazı `hizli_kurgu.py` ile kalır ve raporda yazılır.
1. **Önce oku:** `viral-urun-ekibi:hyperframes` becerisi (render sözleşmesi, iş döngüsü) — kompozisyon kuralları ondan.
   CLI komutları `viral-urun-ekibi:hyperframes-cli`, hazır bloklar `viral-urun-ekibi:hyperframes-registry`, ses/görsel
   varlık `viral-urun-ekibi:media-use`. Kişisel `~/.claude/skills` kopyası varsa da bu paketteki becerileri kullan.
2. **Registry'de önce ara, elle yapma:** her öğe için
   `npx hyperframes catalog --query "<öğenin işi, İngilizce>" --json` → uyanı `npx hyperframes add <ad> --json`
   (ör. kinetik yazı `bottom-up-letters`/`blur-in`, altyazı `caption-*`, geçiş `beat-freeze-cut`, önce/sonra `before-after-wipe`).
3. **Proje:** `npx hyperframes init is/NN/hareketli/VNN --skip-skills --skill=hyperframes` (beceri kurmasın:
   `--skip-skills` şart). 1080×1920, 30 fps, süre = temel kurgu süresi. Yazı zamanları ve metni **tek kaynaktan**:
   `is/NN/kurgu/VNN.json` içindeki `yazilar`/`cta` (bas/bit sn) — kompozisyona aynen taşınır, yeni metin uydurulmaz.
   Font, renk, konum ve "alt %20 + sağ %15 boş, ürünü örtme" kuralları yukarıdaki yazı kuralları ile aynıdır.
4. **Temel video yazısız:** ayar dosyasının kopyasında `yazilar`, plan `yazi` alanları ve `cta` boşaltılıp
   `hizli_kurgu.py` ile `is/NN/kurgu/VNN_temel.mp4` üretilir (ses dahil); asıl `VNN.json` değişmez (kapılar onu okur).
5. **Kontrol ve render:** `npx hyperframes check --json` (her hata düzeltilir) → `npx hyperframes snapshot` ile
   karelere bak (`.hyperframes/artifacts/snapshots/`) → saydam katman:
   `npx hyperframes render is/NN/hareketli/VNN --format webm --quality delivery --output is/NN/hareketli/VNN_katman.webm`.
6. **Bindir (ses temelden):**
   `ffmpeg -i is/NN/kurgu/VNN_temel.mp4 -c:v libvpx-vp9 -i is/NN/hareketli/VNN_katman.webm -filter_complex "[0:v][1:v]overlay=0:0:shortest=1[v]" -map "[v]" -map 0:a -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart is/NN/kurgu/VNN.mp4`
   (`-c:v libvpx-vp9` katman girişinden ÖNCE şart: yoksa ffmpeg saydamlığı okumaz, katman opak olur ve temel videoyu örter —
   sentetik testte ölçüldü. Bindirmeden sonra bir karede ürünün göründüğüne bak.)
7. Sonra aşama 8'in ön-kontrol kapısı aynen: `kurgu_kontrol.py is/NN/kurgu/VNN.json --video is/NN/kurgu/VNN.mp4` ve `--goruntu`.
   Kesim dışı sıçrama hareketli öğeden geliyorsa kareye bak, gerekçeyi yaz; eşik gevşetilmez.
Telemetri: HyperFrames CLI kullanım sayacı gönderir; kullanıcı isterse `npx hyperframes telemetry disable`.
ChatGPT'de bu aşama yok (render yerel Node + Chrome ister).
