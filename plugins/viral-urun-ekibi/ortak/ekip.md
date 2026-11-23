# Ekip (tek lider, 17 çalışma zamanı üyesi)

Lider: **Captain** = `captain` becerisi (ana oturum; `model: fable`, çağrıldığı turda geçerli). Kullanıcıya üye **kod adı ve Türkçe rolüyle** anılır ("Jury (kör video jürisi) videoyu puanladı"); çağrıda ajan kimliği kullanılır (`viral-urun-ekibi:<ajan>`). Eski ad ile yeni ad eşlemesi: `ortak/ad-haritasi.tsv`.
Model sütunu ajan dosyasındaki `model:` alanıdır. `fable` = en güçlü model; yalnız dört işte kullanılır: **kör jüri** (`jury`, `panel`), **kök neden** (`fixer`, `director`), **strateji ve yön** (`atlas`; hikâye seçimi ve kısa liste çağrıda model verilerek) ve **aylık kural budaması** (geliştirici işi). Hacimli ve kalıp işler `sonnet`, ölçülebilir her şey betik. Hesabında `fable` yoksa o dosyalarda `opus` yaz. "Çağrıda model: fable" = lider o tek çağrıda ajanı güçlü modelle çalıştırır; dosyadaki varsayılan değişmez. Yeni not: `forge` mod `istem` aynı görselde iki tur üst üste Panel eşiğinin altında kalırsa o çağrıda model: opus.

## Ürün ve video (7)
| Kod adı | Türkçe rol | Ajan | Model | Ne zaman |
|---|---|---|---|---|
| Scout | Fırsat avcısı | `scout` | sonnet | AliExpress ve Trendyol taraması; mağaza kolunda pazar ve rakip araştırması |
| Skeptic | Kanıt savcısı | `skeptic` | opus | SAT kararından önce; sayfa iddialarını çürütür; yalnız son 3 adayda çağrıda model: fable |
| Decoder | Kreatif analisti | `decoder` | sonnet | viral video desenleri (sayım betik ve SQL işi; desen yorumu ayda bir, çağrıda model: fable) |
| Story | İçerik stratejisti | `story` | sonnet | 30 senaryonun yazımı; hikâye bankası ve ilk 5 seçimi için çağrıda model: fable |
| Jury | Kör video jürisi | `jury` | fable | kredi onayından ve teslimden önce, 3 bağımsız kopya; kalibrasyon turu |
| Fixer | Video kök neden direktörü | `fixer` | fable | jüri hükmü açıklandıktan sonra, tur başına bir kez |
| Mixer | Ses tasarımcısı | `mixer` | sonnet | kurgu aşama 8 (ölçüm okuyup komut üretir; yargı betik eşiklerinde) |

## Mağaza (10)
Birleşen rollerde brief'te `mod:` satırı zorunludur; mod dosyaları `ortak/roller/<ajan>/<mod>.md`.
| Kod adı | Türkçe rol | Ajan | Model | Ne zaman |
|---|---|---|---|---|
| Atlas | Marka ve stil stratejisti | `atlas` | fable | modlar: strateji, kimlik, stil; Aşama 1 ve Aşama 2 başı |
| Muse | Referans ve logo araştırmacısı | `muse` | sonnet | modlar: referans, logo; Aşama 1 |
| Copy | Metin yazarı | `copy` | sonnet | Aşama 1, istemlerden önce |
| Forge | İstem yazarı ve görsel üretim operatörü | `forge` | sonnet | modlar: istem, uretim; Aşama 2 |
| Sentinel | Görsel kapı bekçisi | `sentinel` | sonnet | modlar: kilit, yazim, seri; üretimden önce ve her turdan sonra |
| Panel | Kör görsel jürisi | `panel` | fable | tur sonu, 3 bağımsız kopya |
| Director | Görsel kök neden direktörü | `director` | fable | tur sonu, eşleşme açıldıktan sonra |
| Architect | Site ve tipografi mimarı | `architect` | sonnet | modlar: bolum, tipografi; Aşama 1 ve Aşama 3 |
| Probe | Teknik denetçi | `probe` | sonnet | modlar: hiz, erisim, arama; Aşama 1 (renk kontrastı) ve Aşama 3 |
| Shopper | Müşteri gözü denetçisi | `shopper` | sonnet | modlar: donusum, ses; Aşama 1 sonu ve Aşama 3 |

## Rol başına sonuç metriği (haftalık karne: `skills/captain/scripts/karne_uret.py`)
Her rol ara doğrulukla değil **sonuçla** ölçülür; kaynak kullanıcının beğenisi değil gerçek performans kaydıdır. Betik rol
başına bir satır basar; veri yoksa "veri yok" yazar. Bir rol 3 hafta üst üste "veri yok" kalırsa gelişim işi durur, kullanıcıya tek soru gider.
| Rol | Sonuç metriği | Veri nereden gelir |
|---|---|---|
| Fırsat avcısı | önerdiği adaylardan izleme ölçümünde büyüyenlerin oranı | `is/firsat/ivme.csv` (t0 → t7/t30) |
| Kanıt savcısı | SAT kararının 30. günde ayakta kalma oranı | kanıt dosyasında `sonuc_30gun:` satırı |
| Kreatif analisti | ayrı tutulan videolarda yönü tutan desen oranı | `is/kesfet/desen-test.tsv` (aynı hesapta kazanan–kaybeden) |
| İçerik stratejisti | 48. saat paylaşım/izlenme medyanı (eşik %0,61) | `is/NN/yayin/olcum.csv` |
| Kör jüri (video ve görsel) | jüri sırası ↔ gerçek performans, Spearman ρ (≥ 0,5 uyumlu) | `juri.py kalibrasyon` → `.ekip/juri-kalibrasyon.jsonl` |
| Direktör (kök neden) | kalan videolardan ≤ 3 turda geçenlerin oranı | `is/NN/elestiri/juri.jsonl` |
| Ses tasarımcısı | ses kapısından ilk koşuda geçen video oranı | `.ekip/kapi.jsonl` (`ses@V`) |
| Kurgu | teknik + kurgu + görüntü kapılarından ilk koşuda geçen video oranı | `.ekip/kapi.jsonl` |
| Ekip lideri | ilk koşuda geçen geçiş oranı; aşım sayısı | `.ekip/kapi.jsonl` |
| Mağaza kolu (marka, görsel, site, denetim) | sepete ekleme oranı (sepete ekleme / oturum), düzeltme öncesi ve sonrası | `is/NN/magaza/analitik.csv` (Shopify analitiğinden yalnız okunur) |

## Birleşen roller (aynı işi yapanlar tek üyede)
| Eski roller | Yeni üye | Modlar |
|---|---|---|
| marka stratejisti + kimlik direktörü + niş stil mimarı | Atlas | strateji · kimlik · stil |
| referans küratörü + logo tasarımcısı | Muse | referans · logo |
| istem mühendisi + görsel üretici | Forge | istem · uretim |
| ürün kilidi analisti + görsel QA + seri tutarlılık denetçisi | Sentinel | kilit · yazim · seri |
| site bölüm mimarı + tipografi sistemcisi | Architect | bolum · tipografi |
| hız mühendisi + erişilebilirlik denetçisi + SEO/AIO uzmanı | Probe | hiz · erisim · arama |
| CRO/UX denetçisi + marka sesi denetçisi | Shopper | donusum · ses |

Bağımsızlık korunur: Panel hiçbir üreticiyle birleşmedi; Director, Panel'den ayrıdır; üreten ölçmez (Forge ↔ Sentinel ↔ Panel ayrı roller); yazan denetlemez (Copy ↔ Shopper mod `ses`).

Mağaza aşamalarındaki durum satırı (`AŞAMA a/3 · ADIM n/9 · <Kod adı>`) aynı kod adlarını kullanır: 1–2 Scout · 3–4 Atlas · 5 Copy · 6 Atlas · 7 Forge (kabulde Director) · 8 Architect · 9 Probe.

Geliştirme ekibi (pakete girmez, yalnız eklenti deposunda): Platform Compatibility Engineer (Tuna), Design Language Lead (Kuzey) → depo kökünde `.claude/agents/`.
