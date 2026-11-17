# Nişler ve kelime aileleri (makine okur: `nis_kelime.py`)

Biçim kuralı (bozma — betik okur): `## <kod> — <ad>` başlığı, altında `| PAZAR | AİLE | ifade; ifade; ... |` satırları.
Pazar = Meta ülke kodu: US (ABD) · TR · GB (UK) · DE · FR · ES. Aile:
- **U — ürün tipi**: jenerik ürün adı, tam ifade aranır. İlk 2 terim günlük plana girer (sıra = öncelik).
- **K — kimlik/kanca**: ürünü isteyecek ya da hediye alacak grup (`ai-video-kreatif/referans/kanca-kutuphanesi.md` §2 kovaları). İlk terim plana girer.
- **F — süzgeç kökü**: aranmaz; S (dropship sinyali) sorgusundan gelen reklamın nişini gövde metninden bulmak için. Kök yazılır (önek eşleşir: `kedi` → `kediniz`).
- **S — dropship sinyali** (`_sinyal` bölümü): nişten bağımsız teklif dili, tek başına tam ifade aranır, sonuç F/U ile nişe dağıtılır.
- **KONTROL** (`_kontrol` bölümü): her zaman dolu dönmesi beklenen büyük marka; 0 kart = Meta kısıtı.

Durum: TR'de S ailesinin ilk 3 terimi **ölçüldü** (ilk TR turu: 3 sorgu, ~1.650 reklam). Geri kalan her terim **öneri, ölçülmedi** —
ilk turda 0 ya da alakasız dönen terim silinir, kazanan reklam gövdelerinde ≥3 kez geçen 2–3 kelimelik ifade (`haftalik_rapor.py`
"yeni kelime adayı") eklenir. AB'de (DE/FR/ES) U satırının sonundaki İngilizce terim bilerek konuldu: AB'ye İngilizce reklam da gidiyor.
Kozmetik/sağlık **ELE KAPISI**: yalnız süzgeç (sinyal olarak sayılır), sorgu planına ve ürün önerisine girmez.

## _kontrol — Kontrol sorgusu (her oturum başında + her 0 kartlık sonuçtan sonra)
| US | KONTROL | nike |
| TR | KONTROL | trendyol |
| GB | KONTROL | tesco |
| DE | KONTROL | zalando |
| FR | KONTROL | decathlon |
| ES | KONTROL | zara |

## _sinyal — Dropship sinyali (nişten bağımsız)
| US | S | free shipping; limited stock; 50% off; selling fast; buy 2 get 1 |
| TR | S | kapıda ödeme; şeffaf kargo; sınırlı stok; ücretsiz kargo; 2 al 1 öde |
| GB | S | free UK delivery; limited stock; 50% off; free delivery; selling fast |
| DE | S | kostenloser Versand; nur noch wenige; 50% Rabatt; Kauf auf Rechnung; free shipping |
| FR | S | livraison gratuite; stock limité; -50%; paiement à la livraison; free shipping |
| ES | S | envío gratis; stock limitado; 50% de descuento; pago contra reembolso; free shipping |

## evcil — Evcil hayvan
| US | U | dog bed; cat tree; dog harness; cat toy; pet hair remover; dog car seat |
| US | K | dog mom; cat mom; dog dad; small dog owners |
| US | F | dog; puppy; cat; kitten; pet; paw |
| TR | U | kedi yatağı; köpek tasması; kedi oyuncağı; tüy toplayıcı; köpek yatağı; mama kabı |
| TR | K | kedi annesi; köpek annesi; patili dost; kedi sahipleri |
| TR | F | kedi; köpek; patili; evcil; mama; pati |
| GB | U | dog bed; cat tree; dog harness; cat toy; pet hair remover; dog coat |
| GB | K | dog mum; cat mum; dog owners; cat lovers |
| GB | F | dog; puppy; cat; kitten; pet; paw |
| DE | U | Hundebett; Katzenbaum; Hundegeschirr; Katzenspielzeug; Tierhaarentferner; dog bed |
| DE | K | Hundemama; Katzenmama; Hundebesitzer; Katzenliebhaber |
| DE | F | hund; welpe; katze; kätzchen; haustier; pfote |
| FR | U | lit pour chien; arbre à chat; harnais chien; jouet chat; brosse poils animaux; dog bed |
| FR | K | maman de chien; maman chat; propriétaires de chiens; amoureux des chats |
| FR | F | chien; chiot; chat; chaton; animal; patte |
| ES | U | cama para perro; rascador para gatos; arnés perro; juguete gato; quitapelos mascotas; dog bed |
| ES | K | mamá perruna; mamá gatuna; dueños de perros; amantes de los gatos |
| ES | F | perro; cachorro; gato; gatito; mascota; patita |

## bebek — Bebek ve ebeveyn
| US | U | baby carrier; baby monitor; teether; swaddle; baby bath; toddler toy |
| US | K | new mom; first time mom; boy mom; toddler parents |
| US | F | baby; newborn; toddler; infant; mom; nursery |
| TR | U | kanguru; bebek telsizi; diş kaşıyıcı; kundak; bebek küveti; montessori oyuncak |
| TR | K | yeni anne; ilk kez anne; anne adayı; bebek annesi |
| TR | F | bebek; yenidoğan; anne; çocuk; emzik; kundak |
| GB | U | baby carrier; baby monitor; teether; swaddle; baby bath; toddler toy |
| GB | K | new mum; first time mum; mum of two; toddler parents |
| GB | F | baby; newborn; toddler; infant; mum; nursery |
| DE | U | Babytrage; Babyphone; Beißring; Pucksack; Babybadewanne; baby carrier |
| DE | K | frischgebackene Mama; Mamas; Eltern von Kleinkindern; werdende Mama |
| DE | F | baby; neugeboren; kleinkind; mama; kinderzimmer; schnuller |
| FR | U | porte-bébé; babyphone; anneau de dentition; gigoteuse; baignoire bébé; baby carrier |
| FR | K | jeune maman; futures mamans; parents de bambins; maman |
| FR | F | bébé; nouveau-né; enfant; maman; tétine; naissance |
| ES | U | mochila portabebés; vigilabebés; mordedor; saco de dormir bebé; bañera bebé; baby carrier |
| ES | K | mamá primeriza; nuevas mamás; padres de niños pequeños; futura mamá |
| ES | F | bebé; recién nacido; niño; mamá; chupete; peque |

## ev-isik — Ev dekor ve ışık
| US | U | sunset lamp; galaxy projector; moon lamp; led strip lights; wall art; night light |
| US | K | home decor lovers; cozy home; plant lovers; bedroom aesthetic |
| US | F | lamp; light; decor; projector; led; room |
| TR | U | gün batımı lambası; galaksi projektör; ay lambası; led şerit; gece lambası; duvar dekoru |
| TR | K | ev dekorasyonu sevenler; evini sevenler; yeni ev; çeyiz |
| TR | F | lamba; ışık; dekor; projektör; led; salon |
| GB | U | sunset lamp; galaxy projector; moon lamp; led strip lights; wall art; night light |
| GB | K | home decor lovers; cosy home; plant lovers; bedroom makeover |
| GB | F | lamp; light; decor; projector; led; room |
| DE | U | Sonnenuntergangslampe; Sternenhimmel Projektor; Mondlampe; LED Streifen; Nachtlicht; sunset lamp |
| DE | K | Deko Liebhaber; gemütliches Zuhause; Pflanzenliebhaber; Wohnungsdeko |
| DE | F | lampe; licht; deko; projektor; led; wohnzimmer |
| FR | U | lampe coucher de soleil; projecteur galaxie; lampe lune; ruban led; veilleuse; sunset lamp |
| FR | K | amoureux de la déco; cocooning; amoureux des plantes; déco chambre |
| FR | F | lampe; lumière; déco; projecteur; led; salon |
| ES | U | lámpara atardecer; proyector galaxia; lámpara luna; tira led; luz nocturna; sunset lamp |
| ES | K | amantes de la decoración; hogar acogedor; amantes de las plantas; decoración dormitorio |
| ES | F | lámpara; luz; decoración; proyector; led; salón |

## mutfak — Mutfak
| US | U | vegetable chopper; garlic press; oil sprayer; mini blender; food storage; spice rack |
| US | K | home cooks; busy moms; meal preppers; kitchen lovers |
| US | F | kitchen; cooking; chef; blender; recipe; food |
| TR | U | sebze doğrayıcı; sarımsak ezici; yağ spreyi; mini blender; saklama kabı; baharatlık |
| TR | K | ev hanımları; mutfağı sevenler; pratik anneler; yemek yapmayı sevenler |
| TR | F | mutfak; yemek; doğra; tencere; tava; tarif |
| GB | U | vegetable chopper; garlic press; oil sprayer; mini blender; food storage; spice rack |
| GB | K | home cooks; busy mums; meal preppers; kitchen lovers |
| GB | F | kitchen; cooking; chef; blender; recipe; food |
| DE | U | Gemüseschneider; Knoblauchpresse; Ölsprüher; Mini Mixer; Vorratsdosen; vegetable chopper |
| DE | K | Hobbyköche; Meal Prep; Küchenliebhaber; vielbeschäftigte Mamas |
| DE | F | küche; kochen; koch; mixer; rezept; essen |
| FR | U | coupe légumes; presse ail; spray huile; mini blender; boîtes de conservation; vegetable chopper |
| FR | K | cuisiniers amateurs; batch cooking; amoureux de la cuisine; mamans pressées |
| FR | F | cuisine; cuisiner; chef; mixeur; recette; repas |
| ES | U | picador de verduras; prensa ajos; spray aceite; mini batidora; tarros herméticos; vegetable chopper |
| ES | K | cocineros caseros; amantes de la cocina; mamás ocupadas; batch cooking |
| ES | F | cocina; cocinar; chef; batidora; receta; comida |

## banyo-bakim — Banyo ve kişisel bakım (sağlık iddiasız)
| US | U | shower head filter; toilet stool; bathroom organizer; hair dryer brush; electric toothbrush holder; towel warmer |
| US | K | self care lovers; clean girl; bathroom glow up; organized moms |
| US | F | shower; bathroom; toilet; bath; towel; hair |
| TR | U | filtreli duş başlığı; klozet taburesi; banyo düzenleyici; fön fırçası; diş fırçalığı; havlu askısı |
| TR | K | kendine bakanlar; temizlik sevenler; banyo düzeni; düzenli anneler |
| TR | F | duş; banyo; klozet; havlu; saç; lavabo |
| GB | U | shower head filter; toilet stool; bathroom organiser; hair dryer brush; toothbrush holder; heated towel rail |
| GB | K | self care lovers; clean girl; bathroom glow up; organised mums |
| GB | F | shower; bathroom; toilet; bath; towel; hair |
| DE | U | Duschkopf Filter; Toilettenhocker; Badezimmer Organizer; Warmluftbürste; Zahnbürstenhalter; shower head filter |
| DE | K | Self Care; Ordnungsliebhaber; Badezimmer Makeover; Putzfans |
| DE | F | dusche; bad; toilette; handtuch; haare; waschbecken |
| FR | U | pommeau de douche filtrant; tabouret toilette; rangement salle de bain; brosse soufflante; porte brosse à dents; shower head filter |
| FR | K | self care; adeptes du rangement; salle de bain relookée; fans de ménage |
| FR | F | douche; salle de bain; toilette; serviette; cheveux; lavabo |
| ES | U | alcachofa ducha filtro; taburete inodoro; organizador baño; cepillo secador; portacepillos; shower head filter |
| ES | K | autocuidado; amantes del orden; baño renovado; fans de la limpieza |
| ES | F | ducha; baño; inodoro; toalla; pelo; lavabo |

## arac — Araç aksesuarı
| US | U | car organizer; car phone holder; car vacuum; seat gap filler; car trash can; obd2 scanner |
| US | K | car guys; car lovers; car girls; new drivers |
| US | F | car; truck; vehicle; driver; seat; dashboard |
| TR | U | araç düzenleyici; araç telefon tutucu; araç süpürgesi; koltuk arası boşluk; oto çöp kutusu; arıza tespit cihazı |
| TR | K | araba tutkunları; araba sevenler; yeni ehliyet; motor tutkunları |
| TR | F | araç; araba; oto; sürücü; koltuk; motor |
| GB | U | car organiser; car phone holder; car vacuum; seat gap filler; car bin; obd2 scanner |
| GB | K | car guys; petrolheads; car lovers; new drivers |
| GB | F | car; vehicle; driver; seat; dashboard; motor |
| DE | U | Auto Organizer; Handyhalterung Auto; Autostaubsauger; Sitzlückenfüller; Auto Mülleimer; car organizer |
| DE | K | Autoliebhaber; Autofans; Fahranfänger; Tuning Fans |
| DE | F | auto; fahrzeug; fahrer; sitz; armaturenbrett; kfz |
| FR | U | organisateur voiture; support téléphone voiture; aspirateur voiture; comble espace siège; poubelle voiture; car organizer |
| FR | K | passionnés d'auto; fans de voitures; jeunes conducteurs; amoureux de l'automobile |
| FR | F | voiture; auto; conducteur; siège; tableau de bord; véhicule |
| ES | U | organizador coche; soporte móvil coche; aspiradora coche; relleno hueco asiento; papelera coche; car organizer |
| ES | K | amantes del motor; fans de los coches; conductores noveles; apasionados del coche |
| ES | F | coche; auto; conductor; asiento; salpicadero; vehículo |

## gadget — Teknoloji ve gadget
| US | U | magnetic power bank; mini projector; wireless charger; phone stand; bluetooth tracker; smart ring |
| US | K | tech lovers; gadget lovers; gamers; work from home |
| US | F | wireless; charger; bluetooth; usb; phone; smart |
| TR | U | manyetik powerbank; mini projeksiyon; kablosuz şarj; telefon standı; akıllı takip cihazı; akıllı yüzük |
| TR | K | teknoloji meraklıları; teknoloji sevenler; oyuncular; evden çalışanlar |
| TR | F | kablosuz; şarj; bluetooth; usb; telefon; akıllı |
| GB | U | magnetic power bank; mini projector; wireless charger; phone stand; bluetooth tracker; smart ring |
| GB | K | tech lovers; gadget lovers; gamers; work from home |
| GB | F | wireless; charger; bluetooth; usb; phone; smart |
| DE | U | magnetische Powerbank; Mini Beamer; kabelloses Ladegerät; Handyständer; Bluetooth Tracker; power bank |
| DE | K | Technikfans; Gadget Liebhaber; Gamer; Homeoffice |
| DE | F | kabellos; ladegerät; bluetooth; usb; handy; smart |
| FR | U | batterie externe magnétique; mini vidéoprojecteur; chargeur sans fil; support téléphone; traceur bluetooth; power bank |
| FR | K | fans de tech; amateurs de gadgets; gamers; télétravail |
| FR | F | sans fil; chargeur; bluetooth; usb; téléphone; connecté |
| ES | U | batería externa magnética; mini proyector; cargador inalámbrico; soporte móvil; localizador bluetooth; power bank |
| ES | K | amantes de la tecnología; fans de gadgets; gamers; teletrabajo |
| ES | F | inalámbrico; cargador; bluetooth; usb; móvil; inteligente |

## fitness — Fitness ve spor
| US | U | resistance bands; walking pad; ab roller; massage gun; pilates ring; jump rope |
| US | K | gym girls; gym rats; home workout; runners |
| US | F | workout; gym; fitness; exercise; muscle; training |
| TR | U | direnç bandı; yürüme bandı; karın tekerleği; masaj tabancası; pilates çemberi; atlama ipi |
| TR | K | spor tutkunları; evde spor yapanlar; koşucular; fit anneler |
| TR | F | spor; antrenman; egzersiz; fitness; kas; pilates |
| GB | U | resistance bands; walking pad; ab roller; massage gun; pilates ring; skipping rope |
| GB | K | gym girls; gym lads; home workout; runners |
| GB | F | workout; gym; fitness; exercise; muscle; training |
| DE | U | Widerstandsbänder; Walking Pad; Bauchroller; Massagepistole; Pilates Ring; resistance bands |
| DE | K | Fitnessfans; Home Workout; Läufer; Gym Girls |
| DE | F | training; fitness; sport; übung; muskel; workout |
| FR | U | bandes élastiques; tapis de marche; roue abdominale; pistolet de massage; anneau pilates; resistance bands |
| FR | K | fans de sport; sport à la maison; coureurs; gym girls |
| FR | F | entraînement; sport; fitness; exercice; muscle; workout |
| ES | U | bandas elásticas; cinta de andar; rueda abdominal; pistola de masaje; aro pilates; resistance bands |
| ES | K | amantes del deporte; entrenar en casa; corredores; gym girls |
| ES | F | entrenamiento; deporte; fitness; ejercicio; músculo; workout |

## seyahat — Seyahat
| US | U | packing cubes; travel pillow; carry on backpack; luggage scale; travel organizer; compression bag |
| US | K | travel buddy; frequent flyers; travel lovers; backpackers |
| US | F | travel; luggage; suitcase; flight; trip; packing |
| TR | U | valiz düzenleyici; boyun yastığı; kabin sırt çantası; bavul tartısı; seyahat organizeri; vakumlu saklama torbası |
| TR | K | gezginler; seyahat tutkunları; tatilciler; sık uçanlar |
| TR | F | seyahat; valiz; bavul; tatil; uçak; yolculuk |
| GB | U | packing cubes; travel pillow; cabin bag; luggage scale; travel organiser; compression bag |
| GB | K | travel buddy; frequent flyers; holiday lovers; backpackers |
| GB | F | travel; luggage; suitcase; holiday; flight; packing |
| DE | U | Packwürfel; Nackenkissen; Handgepäck Rucksack; Kofferwaage; Reiseorganizer; packing cubes |
| DE | K | Reiselustige; Vielflieger; Backpacker; Urlaubsfans |
| DE | F | reise; koffer; gepäck; urlaub; flug; packen |
| FR | U | cubes de rangement valise; coussin de voyage; sac cabine; pèse bagage; organiseur de voyage; packing cubes |
| FR | K | voyageurs; grands voyageurs; backpackers; amoureux du voyage |
| FR | F | voyage; valise; bagage; vacances; vol; avion |
| ES | U | organizadores de maleta; almohada de viaje; mochila cabina; báscula maleta; organizador de viaje; packing cubes |
| ES | K | viajeros; amantes de viajar; mochileros; viajeros frecuentes |
| ES | F | viaje; maleta; equipaje; vacaciones; vuelo; avión |

## hediye — Hediye ve kişiye özel
| US | U | custom necklace; personalized gift; name necklace; photo lamp; star map; memory box |
| US | K | gift for her; gift for husband; boyfriend gift; mom gift |
| US | F | gift; personalized; custom; engraved; birthday; anniversary |
| TR | U | isimli kolye; kişiye özel hediye; fotoğraflı lamba; yıldız haritası; anı kutusu; isimli bileklik |
| TR | K | sevgiliye hediye; anneye hediye; eşime hediye; kız arkadaşa hediye |
| TR | F | hediye; kişiye özel; isimli; sevgili; doğum günü; yıldönümü |
| GB | U | custom necklace; personalised gift; name necklace; photo lamp; star map; memory box |
| GB | K | gift for her; secret santa; gift for husband; mum gift |
| GB | F | gift; personalised; custom; engraved; birthday; anniversary |
| DE | U | personalisierte Kette; personalisiertes Geschenk; Namenskette; Fotolampe; Sternenkarte; custom necklace |
| DE | K | Geschenk für sie; Geschenk für Freund; Wichtelgeschenk; Geschenk für Mama |
| DE | F | geschenk; personalisiert; gravur; geburtstag; jahrestag; name |
| FR | U | collier personnalisé; cadeau personnalisé; collier prénom; lampe photo; carte des étoiles; custom necklace |
| FR | K | cadeau pour elle; cadeau homme; cadeau maman; idée cadeau couple |
| FR | F | cadeau; personnalisé; gravé; anniversaire; prénom; couple |
| ES | U | collar personalizado; regalo personalizado; collar con nombre; lámpara foto; mapa estelar; custom necklace |
| ES | K | regalo para ella; regalo para novio; regalo para mamá; amigo invisible |
| ES | F | regalo; personalizado; grabado; cumpleaños; aniversario; nombre |

## eglence-saka — Yetişkin eğlencesi / şaka ve masa oyuncağı ("adult money" oyuncak, gag hediye)
| US | U | fidget toy; desk toy; prank gift; gag gift; building blocks; mini arcade |
| US | K | adult with money; 90s kid; office workers; gamers |
| US | F | toy; prank; gag; funny; fidget; collectible |
| TR | U | stres oyuncağı; masa oyuncağı; şaka hediye; eşek şakası; yapı blokları; mini atari |
| TR | K | 90'lar çocukları; ofis çalışanları; oyuncular; büyümeyenler |
| TR | F | oyuncak; şaka; komik; eğlence; stres; koleksiyon |
| GB | U | fidget toy; desk toy; prank gift; gag gift; building blocks; secret santa gift |
| GB | K | 90s kid; office workers; gamers; big kids |
| GB | F | toy; prank; gag; funny; fidget; collectible |
| DE | U | Anti Stress Spielzeug; Schreibtisch Spielzeug; Scherzartikel; Wichtelgeschenk lustig; Bausteine; fidget toy |
| DE | K | 90er Kinder; Büroalltag; Gamer; große Kinder |
| DE | F | spielzeug; scherz; lustig; spaß; sammler; fidget |
| FR | U | jouet anti stress; jouet de bureau; farce et attrape; cadeau humour; briques de construction; fidget toy |
| FR | K | enfants des années 90; collègues de bureau; gamers; grands enfants |
| FR | F | jouet; farce; drôle; humour; collection; fidget |
| ES | U | juguete antiestrés; juguete de escritorio; broma; regalo divertido; bloques de construcción; fidget toy |
| ES | K | niños de los 90; oficinistas; gamers; amigo invisible |
| ES | F | juguete; broma; divertido; humor; coleccionable; fidget |

## uyku-mobilya — Uyku ve mobilya (sağlık iddiasız)
| US | U | cooling pillow; weighted blanket; bed fan; sleep mask; mattress topper; bedside organizer |
| US | K | hot sleepers; light sleepers; side sleepers; night owls |
| US | F | sleep; pillow; blanket; bed; mattress; bedroom |
| TR | U | serinletici yastık; ağırlıklı battaniye; yatak fanı; uyku maskesi; yatak pedi; baza düzenleyici |
| TR | K | sıcakta uyuyamayanlar; hafif uykulular; yan yatanlar; gece kuşları |
| TR | F | uyku; yastık; battaniye; yatak; nevresim; yorgan |
| GB | U | cooling pillow; weighted blanket; bed fan; sleep mask; mattress topper; bedside organiser |
| GB | K | hot sleepers; light sleepers; side sleepers; night owls |
| GB | F | sleep; pillow; blanket; bed; mattress; duvet |
| DE | U | Kühlkissen; Gewichtsdecke; Bettventilator; Schlafmaske; Matratzenauflage; weighted blanket |
| DE | K | Seitenschläfer; leichter Schlaf; Nachteulen; schwitzen nachts |
| DE | F | schlaf; kissen; decke; bett; matratze; schlafzimmer |
| FR | U | oreiller rafraîchissant; couverture lestée; ventilateur de lit; masque de sommeil; surmatelas; weighted blanket |
| FR | K | dormeurs sur le côté; sommeil léger; oiseaux de nuit; ceux qui ont chaud la nuit |
| FR | F | sommeil; oreiller; couverture; lit; matelas; chambre |
| ES | U | almohada refrescante; manta con peso; ventilador de cama; antifaz para dormir; topper colchón; weighted blanket |
| ES | K | duermen de lado; sueño ligero; noctámbulos; calor por la noche |
| ES | F | dormir; almohada; manta; cama; colchón; dormitorio |

## kozmetik-saglik — Kozmetik ve sağlık (ELE KAPISI: yalnız süzgeç, sorgu ve ürün önerisi yok)
| US | F | serum; cream; supplement; pain relief; posture; skin; lotion |
| TR | F | krem; serum; ağrı; macun; cilt; sağlık; losyon; magnezyum |
| GB | F | serum; cream; supplement; pain relief; posture; skin; lotion |
| DE | F | serum; creme; nahrungsergänzung; schmerz; haltung; haut |
| FR | F | sérum; crème; complément; douleur; posture; peau |
| ES | F | sérum; crema; suplemento; dolor; postura; piel |
