# Ekip (tek lider, 27 çalışma zamanı üyesi)

Lider: **Team Lead (Kerem)** = `ekip-lideri` becerisi (ana oturum; `model: fable`, çağrıldığı turda geçerli). Kullanıcıya üye **unvanı ve adıyla** anılır ("Brand Strategist (Elif) konumlamayı çıkardı"); çağrıda ajan adı kullanılır (`viral-urun-ekibi:<ajan>`).
Model sütunu ajan dosyasındaki `model:` alanıdır. `fable` = en güçlü model: yanlışı pahalı, seyrek çağrılan yargı rolleri (eleştirmenler, strateji, direktörler). Hesabında yoksa o dosyalarda `opus` yaz.

## Çekirdek ekip: ürün ve kreatif
| Unvan (ad) | Türkçe rol | Ajan | Model | Ne zaman |
|---|---|---|---|---|
| Product Research Lead (Kaan) | Fırsat avcısı | `firsat-avcisi` | sonnet | AliExpress taraması; mağaza kolunda pazar ve rakip araştırması |
| Risk & Validation Analyst (Selin) | Kanıt savcısı | `kanit-savcisi` | opus | SAT kararından önce; sayfa iddialarını çürütür |
| Creative Strategy Analyst (Arda) | Kreatif analisti | `kreatif-analisti` | opus | viral video desenleri |
| Content Strategist (Ece) | İçerik stratejisti | `icerik-stratejisti` | fable | 30 senaryo, hikâye seçimi |
| Blind Video Panelist (Aras) | Kör video jürisi | `video-juri` | fable | kredi onayından ve teslimden önce, 3 bağımsız kopya; kalibrasyon turu |
| Creative Director (QA) (Deniz) | Kök neden ve düzeltme direktörü | `video-elestirmen` | fable | jüri hükmü açıklandıktan sonra, tur başına bir kez |
| Sound Designer (Ozan) | Ses tasarımcısı | `ses-tasarimcisi` | opus | kurgu aşama 8 |

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
| Copywriter (Naz) | Görsel metin yazarı | `metin-yazari` | fable | istemlerden önce |
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

## Birleşen roller (aynı işi yapanlar tek üyede)
| Eski iki rol | Yeni üye | Neden |
|---|---|---|
| logo araştırmacısı + logo tasarımcısı | Logo Designer (Lale) | araştırma istemin girdisidir; ayrı ajan aynı raporu iki kez okuyordu |
| görsel üretici + gerçek ortam koşucusu | Image Production Operator (Tolga) | ikisi de aynı tarayıcıda aynı hesabı sürer, aynı izin kapısı |
| referans küratörü + kütüphane bakımcısı | Reference Curator (Mert) | ikisi de aynı referans havuzunu toplar ve günceller |

Mağaza aşamalarındaki durum satırı (`ADIM n/8 · <Unvan>`) aynı unvanları kullanır: 1–2 Product Research Lead (Kaan) · 3 Brand Strategist (Elif) / Brand Identity Director (Defne) · 4–5 Niche Art Director (Zeynep) / Design Director (Ufuk) · 6 Copywriter (Naz) · 7–8 Store Architect (Baran).

Geliştirme ekibi (pakete girmez, yalnız eklenti deposunda): Platform Compatibility Engineer (Tuna), Design Language Lead (Kuzey) → depo kökünde `.claude/agents/`.
