# Ekip (tek lider, 27 çalışma zamanı üyesi)

Lider: **Team Lead (Kerem)** = `captain` becerisi (ana oturum; `model: fable`, çağrıldığı turda geçerli). Kullanıcıya üye **unvanı ve adıyla** anılır ("Brand Strategist (Elif) konumlamayı çıkardı"); çağrıda ajan adı kullanılır (`viral-urun-ekibi:<ajan>`).
Model sütunu ajan dosyasındaki `model:` alanıdır. `fable` = en güçlü model; yalnız dört işte kullanılır: **kör jüri** (`video-juri`, `kor-elestirmen`), **kök neden** (`video-elestirmen`, `tasarim-direktoru`), **strateji ve yön** (`marka-stratejisti`, `kimlik-direktoru`, `nis-stil-mimari`; hikâye seçimi ve kısa liste çağrıda model verilerek) ve **aylık kural budaması** (geliştirici işi). Hacimli ve kalıp işler `sonnet`, yazım kontrolü `haiku`, ölçülebilir her şey betik. Hesabında `fable` yoksa o dosyalarda `opus` yaz. "Çağrıda model: fable" = lider o tek çağrıda ajanı güçlü modelle çalıştırır; dosyadaki varsayılan değişmez.

## Çekirdek ekip: ürün ve kreatif
| Unvan (ad) | Türkçe rol | Ajan | Model | Ne zaman |
|---|---|---|---|---|
| Product Research Lead (Kaan) | Fırsat avcısı | `firsat-avcisi` | sonnet | AliExpress taraması; mağaza kolunda pazar ve rakip araştırması |
| Risk & Validation Analyst (Selin) | Kanıt savcısı | `kanit-savcisi` | opus | SAT kararından önce; sayfa iddialarını çürütür; yalnız son 3 adayda çağrıda model: fable |
| Creative Strategy Analyst (Arda) | Kreatif analisti | `kreatif-analisti` | sonnet | viral video desenleri (sayım betik ve SQL işi; desen yorumu ayda bir, çağrıda model: fable) |
| Content Strategist (Ece) | İçerik stratejisti | `icerik-stratejisti` | sonnet | 30 senaryonun yazımı; hikâye bankası ve ilk 5 seçimi için çağrıda model: fable |
| Blind Video Panelist (Aras) | Kör video jürisi | `video-juri` | fable | kredi onayından ve teslimden önce, 3 bağımsız kopya; kalibrasyon turu |
| Creative Director (QA) (Deniz) | Kök neden ve düzeltme direktörü | `video-elestirmen` | fable | jüri hükmü açıklandıktan sonra, tur başına bir kez |
| Sound Designer (Ozan) | Ses tasarımcısı | `ses-tasarimcisi` | sonnet | kurgu aşama 8 (ölçüm okuyup komut üretir; yargı betik eşiklerinde) |

## Mağaza kolu: marka ve görsel
| Unvan (ad) | Türkçe rol | Ajan | Model | Ne zaman |
|---|---|---|---|---|
| Brand Strategist (Elif) | Marka stratejisti | `marka-stratejisti` | fable | görsel kararlardan önce |
| Reference Curator (Mert) | Referans küratörü ve kütüphane bakımcısı | `referans-kuratoru` | sonnet | strateji sonrası; yeni niş |
| Brand Identity Director (Defne) | Marka kimliği direktörü | `kimlik-direktoru` | fable | 3 kimlik yönü |
| Logo Designer (Lale) | Logo araştırmacısı ve tasarımcısı | `logo-tasarimci` | opus | marka adımı, logo brifi |
| Niche Art Director (Zeynep) | Niş stil mimarı | `nis-stil-mimari` | fable | yeni niş; nişe uygunluk düşükse |
| Typography Systems Designer (Emre) | Tipografi sistemcisi | `tipografi-sistemcisi` | opus | marka adımı; her görsel/site turu |
| Product Fidelity Analyst (Burak) | Ürün kilidi analisti | `urun-kilidi-analisti` | opus | üretimden önce ve her turdan sonra |
| Copywriter (Naz) | Görsel metin yazarı | `metin-yazari` | opus | istemlerden önce |
| Prompt Engineer (Can) | İstem mühendisi | `prompt-muhendisi` | opus | üretim istemleri |
| Image Production Operator (Tolga) | Görsel üretim operatörü ve koşu kaydedicisi | `gorsel-uretici` | sonnet | onaylı üretim listesi; gerçek ortam koşusu |
| Visual QA Inspector (İpek) | Görsel yazım bekçisi (OCR) | `gorsel-qa` | haiku | her görsel |
| Set Consistency Auditor (Onur) | Seri tutarlılık denetçisi | `seri-tutarlilik-denetcisi` | opus | tur sonu, kör panodan önce |
| Blind Review Panelist (Derin) | Kör eleştirmen | `kor-elestirmen` | fable | tur sonu, 3 bağımsız kopya |
| Design Director (Ufuk) | Tasarım direktörü (kök neden, düzeltme emri) | `tasarim-direktoru` | fable | tur sonu, eşleşme açıldıktan sonra |

## Mağaza kolu: site ve denetim
| Unvan (ad) | Türkçe rol | Ajan | Model | Ne zaman |
|---|---|---|---|---|
| Store Architect (Baran) | Site bölüm mimarı | `site-bolum-mimari` | opus | metinlerden önce |
| Brand Voice Auditor (Seda) | Marka sesi denetçisi | `marka-sesi-denetcisi` | sonnet | metinlerden sonra |
| CRO & UX Auditor (Cem) | Dönüşüm ve kullanılabilirlik denetçisi | `cro-ux-denetcisi` | sonnet | kurulum sonrası |
| Performance Engineer (Umut) | Hız mühendisi | `hiz-muhendisi` | sonnet | kurulum sonrası |
| SEO & AI Search Specialist (Aslı) | Arama ve feed uzmanı | `seo-aio-uzmani` | sonnet | metinler ve kurulum |
| Accessibility Auditor (Yasemin) | Erişilebilirlik denetçisi | `erisilebilirlik-denetcisi` | sonnet | marka adımı ve kurulum sonrası |

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
| Eski iki rol | Yeni üye | Neden |
|---|---|---|
| logo araştırmacısı + logo tasarımcısı | Logo Designer (Lale) | araştırma istemin girdisidir; ayrı ajan aynı raporu iki kez okuyordu |
| görsel üretici + gerçek ortam koşucusu | Image Production Operator (Tolga) | ikisi de aynı tarayıcıda aynı hesabı sürer, aynı izin kapısı |
| referans küratörü + kütüphane bakımcısı | Reference Curator (Mert) | ikisi de aynı referans havuzunu toplar ve günceller |

Mağaza aşamalarındaki durum satırı (`ADIM n/8 · <Unvan>`) aynı unvanları kullanır: 1–2 Product Research Lead (Kaan) · 3 Brand Strategist (Elif) / Brand Identity Director (Defne) · 4–5 Niche Art Director (Zeynep) / Design Director (Ufuk) · 6 Copywriter (Naz) · 7–8 Store Architect (Baran).

Geliştirme ekibi (pakete girmez, yalnız eklenti deposunda): Platform Compatibility Engineer (Tuna), Design Language Lead (Kuzey) → depo kökünde `.claude/agents/`.
