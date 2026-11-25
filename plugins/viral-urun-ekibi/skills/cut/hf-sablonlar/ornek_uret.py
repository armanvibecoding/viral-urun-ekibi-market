#!/usr/bin/env python3
"""Altı şablonun bağımsız HyperFrames örnek kompozisyonlarını üretir: ornekler/<sablon>/index.html (+ sahne.json = parametreler).

  python3 ornek_uret.py [ornekler_klasoru]       sonra:  cd ornekler/<sablon> && npx hyperframes check --json
Her örnek koyu degrade zemin + (varsa) hareket veren yüzen şekil üzerinde şablonu gösterir; kendi klibinizin üstüne koymak için
index.html içindeki `zemin` bloğunu <video> ile değiştirin. Parametre sözlüğü sahne.json'dadır (hikâye ayarındaki "sahneler" öğesiyle aynı biçim).
"""
import json
import os
import sys

BURADA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BURADA, "..", "scripts", "hikaye"))
import bloklar as B  # noqa: E402

TP = B.TP
SURE = 5.0
ORNEK = {
    "ig_kutu": {"tur": "ig_kutu", "bas": 0, "sure": SURE, "metin": "POV: a mug that / *reacts* to heat", "renk": "#FFE600", "top": 300},
    "kalin_kontur": {"tur": "kalin_kontur", "bas": 0, "sure": SURE, "metin": "Don't show this / to a *dog mom*", "renk": "#FFE600", "top": 300},
    "karaoke": {"tur": "karaoke", "bas": 0, "sure": SURE, "metin": "Why does my dog / *shed* everywhere?", "zamanlar": [0, 0.3, 0.6, 0.9, 1.2, 1.5], "top": 300},
    "tepki": {"tur": "tepki", "bas": 0, "sure": SURE, "ust": "Im sorry but", "buyuk": "WHAT?!", "top": 300},
    "cta_rozet": {"tur": "cta_rozet", "bas": 0, "sure": SURE, "anahtar": "DOG", "top": 1120},
    "sayac": {"tur": "sayac", "bas": 0, "sure": SURE, "deger": 100, "sonek": "%", "etiket": "*fur* gone", "top": 420},
    # TR/AB referans paketi (REFERANSLAR 0.6)
    "ig_kutu_renk_emoji": {"tur": "ig_kutu", "bas": 0, "sure": SURE, "metin": "Arabasını *evi gibi* / görenlerin yeni favorisi", "vurgu_stil": "renk", "renk": "#E11D2E", "emoji": "😳", "dil": "tr", "top": 300},
    "tek_kelime": {"tur": "tek_kelime", "bas": 0, "sure": SURE, "metin": "En konuşulan toparlayıcıyı sonunda aldım", "ok": True, "dil": "tr", "top": 820, "adim": 0.5},
    "uzman_kutu": {"tur": "uzman_kutu", "bas": 0, "sure": SURE, "metin": "Nefes borusu / *tıkandığında*", "dil": "tr", "top": 300},
    "iki_katman": {"tur": "iki_katman", "bas": 0, "sure": SURE, "kanca": {"sablon": "kalin_kontur", "metin": "3 yudum içebilirse / *oyson* alacak", "top": 300},
                   "altyazi_ayar": {"metin": "bugün bunu sokakta deneyeceğiz", "top": 1000}},
    "son_kart_tr": {"tur": "son_kart", "bas": 0, "sure": SURE, "pazar": "TR", "rozet": "ÜCRETSİZ KARGO", "top": 1000},
    "son_kart_de": {"tur": "son_kart", "bas": 0, "sure": SURE, "pazar": "DE", "rozet": "−50% Nur HEUTE", "ikinci": "+ GRATIS VERSAND", "dugme": "Jetzt bestellen", "top": 780},
    "son_kart_us": {"tur": "son_kart", "bas": 0, "sure": SURE, "pazar": "US", "top": 1100},
    "dev_fiyat": {"tur": "dev_fiyat", "bas": 0, "sure": SURE, "metin": "−23€", "cikartma": "−15%", "top": 380},
    # uzman yöntemi (R74): R1 yan yana ikili kıyas çerçevesi · R2 konuşmasız tek kurallı test + sayaç
    "ikili_kiyas": {"tur": "ikili_kiyas", "bas": 0, "sure": SURE, "soru": "Hangisi 10 saniyede kurudu?", "sol_etiket": "ESKİ YÖNTEM", "sag_etiket": "ÜRÜN", "kazanan": "sag", "cevap_an": 3.6},
    "deneme_sayaci": {"tur": "deneme_sayaci", "bas": 0, "sure": SURE, "toplam": 3, "adimlar": [1.2, 2.6, 4.0], "kural": "3 leke. Tek silme."},
    # geçiş + kapanış paketi (müşteri kitinden genelleştirildi); görsel/logo = jenerik yer tutucu SVG (YER_TUTUCU), dosya adı sahne.json'da kalır
    "urun_gecisi": {"tur": "urun_gecisi", "bas": 1.0, "sure": 4.0, "gorsel": "yer-tutucu-urun.svg", "kick": "YENİ", "ust1": "Evde sessiz", "ust2": "*güçlü* sonuç", "alt": "bugün dene"},
    "dip_gecis": {"tur": "dip_gecis", "z": 2.5},
    "kapanis": {"tur": "kapanis", "bas": 0.5, "sure": 4.5, "logo": "yer-tutucu-logo.svg", "marka": "MARKA", "alt_satir": "ALT SATIR", "yazi": "Şimdi dene"},
    "kapanis_yumusak": {"tur": "kapanis", "bas": 0.5, "sure": 4.5, "logo": "yer-tutucu-logo.svg", "marka": "MARKA", "alt_satir": "ALT SATIR", "yumusak": 2},
}
YER_TUTUCU = {
    "yer-tutucu-logo.svg": '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400"><circle cx="200" cy="200" r="190" fill="#c9a36b"/><text x="200" y="272" font-size="230" text-anchor="middle" fill="#ffffff" font-family="sans-serif" font-weight="700">A</text></svg>',
    "yer-tutucu-urun.svg": '<svg xmlns="http://www.w3.org/2000/svg" width="570" height="760"><rect x="130" y="20" width="310" height="720" rx="60" fill="#e8e2d8"/><rect x="170" y="80" width="230" height="40" rx="20" fill="#c9a36b"/></svg>',
}
ZEMIN = ('<div id="zemin" class="clip" data-start="0" data-duration="SURE" data-track-index="0">'
         '<div style="position:absolute;inset:0;background:linear-gradient(160deg,#243B55 0%,#141E30 60%,#0b0f1a 100%)"></div>'
         '<div id="sekil" style="position:absolute;left:260px;top:900px;width:560px;height:560px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#f5d9a8,#c47d4a 60%,#6b3a22 100%)"></div></div>').replace("SURE", str(SURE))


def kur(ad, sahne, klasor):
    B.sifirla()
    B.P.append(ZEMIN)
    B.T.append('tl.fromTo("#sekil",{y:0,scale:1},{y:-60,scale:1.08,duration:%s,ease:"sine.inOut"},0);' % SURE)
    TP.ust_perde(SURE)
    s = dict(sahne)
    tur = s.pop("tur")
    for anahtar in ("gorsel", "logo"):   # yer tutucu SVG'yi örnek klasörüne yaz, mutlak yolunu çağrıya ver (sahne.json yalnız dosya adını tutar)
        if s.get(anahtar) in YER_TUTUCU:
            yol = os.path.join(klasor, ad, "assets", "img")
            os.makedirs(yol, exist_ok=True)
            with open(os.path.join(yol, s[anahtar]), "w", encoding="utf-8") as f:
                f.write(YER_TUTUCU[s[anahtar]])
            s[anahtar] = os.path.join(yol, s[anahtar])
    TP.TURLER[tur](**s)
    k = os.path.join(klasor, ad)
    os.makedirs(k, exist_ok=True)
    with open(os.path.join(k, "hyperframes.json"), "w") as f:
        json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json", "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
                   "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}, "authoringSkill": "hyperframes"}, f, indent=2)
    with open(os.path.join(k, "meta.json"), "w") as f:
        json.dump({"id": ad, "name": ad}, f)
    B.bitir(k, SURE, 0, [], None, "", False)
    for gecici in ("zaman.json", "olaylar.json"):   # örnek için gerekmez
        os.remove(os.path.join(k, gecici))
    with open(os.path.join(k, "sahne.json"), "w", encoding="utf-8") as f:
        json.dump(sahne, f, ensure_ascii=False, indent=2)
    return k


def main():
    klasor = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(BURADA, "ornekler")
    for ad, s in ORNEK.items():
        print(kur(ad, s, klasor))


if __name__ == "__main__":
    main()
