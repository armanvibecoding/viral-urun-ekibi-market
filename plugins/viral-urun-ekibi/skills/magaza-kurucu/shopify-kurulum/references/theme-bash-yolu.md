# theme_bash + jq ile şablon yazımı (ÖLÇÜLMEDİ, KULLANMA)

**Durum: ÖLÇÜLMEDİ.** Gerçek mağazada hiç denenmedi. Geçerli tek yol `t4-5-yazma-tarifi.md` (T4.5). Bu dosya yalnız kullanıcı "theme_bash yolunu dene" derse ve Ana Tema üzerinde bir kez ölçüldükten sonra kullanılır.

Kaynak: `research/format/RAPOR.md` §4 (2026-11-15). Tarif taslaktır, test edilmedi.

## Neden
Shopify bağlantısında (ChatGPT eklentisi ve Claude bağlayıcısı) `theme_bash`, `theme_commit`, `theme_screenshot`, `theme_publish` araçları var. `theme_bash` Shopify sunucusunda tema dosyaları üzerinde sandbox bash çalıştırır (`jq`, `sed`, `awk`, `diff`; ağ yok). Değişiklik `theme_commit`'e kadar bekleyen kalır. 50–110 KB'lık şablon modelden geçmez; model yalnız küçük bir yama listesi gönderir.

Bilinen sınırlar (aracın şemasından): script en fazla 65 536 karakter; `;` ve `||` ile ayrılmış komutlar reddedilebilir, `&&` ve yeni satır kullan. İlk değişiklikten önce sunucudaki `/skills/editing-themes/SKILL.md` okunmalı; bu skill'in "yalnız ayar değeri yaz" kuralı her zaman önceliklidir.

## Taslak tarif (her şablon için tek `theme_bash` çağrısı)
```bash
F=templates/product.nis-gadget.json
cp "$F" "${F%.json}-yedek.json"
# baştaki /* ... */ yorumunu at, saf JSON'a çevir
awk 'NR==1&&/^\/\*/{c=1} c{if(/\*\//)c=0; next} {print}' "$F" > /tmp/taban.json
cat > /tmp/yama.json <<'EOF'
[{"yol":"e-serit/c1/i.icon","deger":"truck"},{"yol":"e-kars.disabled","deger":true}]
EOF
jq -e --slurpfile y /tmp/yama.json -f /dev/stdin /tmp/taban.json > /tmp/yeni.json <<'JQ'
def p($yol): ($yol|split(".")) as [$n,$a] | ($n|split("/")) as $s
  | (["sections",$s[0]] + ([$s[1:][]|["blocks",.]]|add // [])) as $d
  | {d:$d, a:$a};
reduce $y[0][] as $c (.;
  p($c.yol) as $q
  | if getpath($q.d) == null then error("YOK: "+$c.yol) else . end
  | if $q.a=="disabled" then (if $c.deger then setpath($q.d+["disabled"];true) else delpaths([$q.d+["disabled"]]) end)
    else setpath($q.d+["settings",$q.a]; $c.deger) end)
JQ
H='def h: {order, s:(.sections|map_values({type, block_order, b:[.. | objects | select(has("blocks")) | .blocks | to_entries[] | [.key,.value.type,(.value.block_order//[])]]}))}; h'
[ "$(jq -cS "$H" /tmp/taban.json)" = "$(jq -cS "$H" /tmp/yeni.json)" ] && jq -c . /tmp/yeni.json > "$F" && echo "OK $(jq '.order|length' "$F") bölüm, $(wc -c < "$F") bayt"
```
Sonra: `theme_screenshot` (ilgili sayfa, `both`) → `theme_commit` (açıklama: "Ürün sayfası metinleri"). Hata olursa aynı `theme_bash` ile yedek geri kopyalanır.

## Koruma kuralları
- `theme_bash` içinde `rm`, `mv` ve `.liquid`, `snippets/`, `assets/`, `locales/` yollarına yazma YASAK (tek istisna kendi yedek ve geçici dosyaları).
- `theme_publish` çağrılmaz; tema yayını kullanıcının işidir.
- `/tmp`'nin yazılabilir olduğu doğrulanmadı; değilse ara dosyalar tema kökünde `_tmp/` altına yazılıp aynı çağrıda silinir.

## Ölçülecekler (kullanmadan önce)
1. Ana Tema'da `editing-themes` SKILL.md okunur.
2. `/tmp`, `awk` davranışı ve 65 KB sınırı denenir.
3. Bir şablonda yama + harita kontrolü çalıştırılır; `theme_commit` kullanıcı onayıyla.
