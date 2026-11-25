#!/usr/bin/env python3
"""Kanca + tipografi + geçiş + SFX paketi testi (kredisiz, ağsız, render yok). python3 sablon_test.py → çıkış 0 = hepsi geçti.
pytest de toplar (test_ ile başlayan işlevler). Kırma testleri: kanca 3 satır / 8 kelime, CTA alt güvenli alanda, ilk pencere ≠ 0, bilinmeyen şablon."""
import json
import os
import re
import subprocess
import sys
import tempfile

BURADA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURADA)
sys.path.insert(0, os.path.join(BURADA, "..", "scripts", "hikaye"))
import bloklar as B  # noqa: E402
import sfx_esle  # noqa: E402

TP = B.TP


def _yeni():
    B.sifirla()


def _kirilir(fn, *a, **k):
    try:
        fn(*a, **k)
    except SystemExit as e:
        return "HATA" in str(e)
    return False


def test_ayristirma():
    s = TP.satirlar("Don't show this / to a *dog mom* now Sound *familiar*?")
    assert s[0] == [("Don't", False), ("show", False), ("this", False)]
    assert [k for k, v in s[1] if v] == ["dog", "mom", "familiar?"]


def test_kanca_ilk_karede_gorunur():
    _yeni()
    TP.ig_kutu(0, 2.0, "POV: a mug that / *reacts* to heat")
    html = " ".join(B.P)
    assert 'data-start="0.0"' in html and "igk" in html
    ilk = [t for t in B.T if "opacity:0" in t.replace(" ", "") and "w0" in t]
    assert not ilk, "kanca kelimeleri 0. karede opacity 0 başlamamalı: %s" % ilk
    assert any(o["tur"] == "yazi" and o["t"] == 0 for o in TP.OL)


def test_kanca_siniri():
    _yeni()
    assert _kirilir(TP.ig_kutu, 0, 2.0, "bir iki / üç dört / beş")                     # 3 satır
    assert _kirilir(TP.kalin_kontur, 0, 2.0, "one two three four five six seven eight")  # 8 kelime
    assert _kirilir(TP.tepki, 0, 2.0, "a b c d e f g", "WHAT?!")                        # 7 + dev kelime = 8
    TP.kalin_kontur(0, 2.0, "one two three four five six seven")                        # 7 kelime serbest
    TP.kalin_kontur(1.0, 2.0, "bir iki / üç dört / beş")                                # kanca değil (bas ≥ 0,05): sınır yok


def test_alti_sablon_uretir():
    _yeni()
    TP.ig_kutu(0, 2, "a b")
    TP.kalin_kontur(0.1, 2, "a b")
    TP.karaoke(0.1, 2, "a b c", zamanlar=[0, 0.3, 0.6])
    TP.tepki(0.1, 2, "Im sorry but", "WHAT?!")
    TP.cta_rozet(0.1, 2, "DOG")
    TP.sayac(0.1, 2, 100, "%", etiket="fur gone")
    html = " ".join(B.P)
    for ad in ("igk", "kk", "kar", "tk", "cta", "say"):
        assert 'class="tx %s' % ad in html, ad
    assert "“DOG”" in html and "elastic" in " ".join(B.T)
    turler = {o["tur"] for o in TP.OL}
    assert {"yazi", "sok", "cta", "kanit"} <= turler


def test_tr_ab_paketi():
    _yeni()
    assert TP.buyuk("istanbul ışık iki", "tr") == "İSTANBUL IŞIK İKİ" and TP.buyuk("iki", "en") == "IKI"
    TP.ig_kutu(0, 2, "Arabasını *evi gibi* / görenlerin yeni favorisi", vurgu_stil="renk", emoji="😳", dil="tr", renk="#E11D2E")
    TP.uzman_kutu(2, 2, "Nefes borusu / *tıkandığında*", dil="tr")
    TP.tek_kelime(4, 2.4, "En konuşulan toparlayıcıyı sonunda", adim=0.5, ok=True, dil="tr")
    TP.iki_katman(6.5, 2, {"sablon": "kalin_kontur", "metin": "a b"}, {"metin": "küçük altyazı"})
    try:
        TP.son_kart(8.5, 2, "TR")
        raise AssertionError("TR son_kart rozetsiz geçmemeli (varsayılan kapıda ödeme yok)")
    except SystemExit:
        pass
    TP.son_kart(8.5, 2, "TR", rozet="ÜCRETSİZ KARGO")
    TP.son_kart(10.5, 2, "DE", rozet="X", ikinci="Y", dugme="Z", top=800)
    TP.son_kart(12.5, 2, "US", anahtar="DOG")
    TP.son_kart(14.5, 2, "US")
    TP.dev_fiyat(16.5, 2, "−23€", cikartma="−15%")
    html = " ".join(B.P)
    assert "igk renk" in html and "😳" in html and "TIKANDIĞINDA" in html
    assert "ÜCRETSİZ KARGO" in html and "KAPIDA ÖDEME" not in html and 'class="skr link"' in html and "tkw" in html and "cikartma" in html and "alty" in html
    assert 'rgba(0,0,0,0.80)' in html                                                   # uzman kutu siyah
    # kırma: tek kelime tabanı, süre, pazar, güvenli alan
    assert _kirilir(TP.tek_kelime, 0, 3, "a b c", adim=0.2)
    assert _kirilir(TP.tek_kelime, 0, 1, "a b c d", adim=0.5)
    assert _kirilir(TP.tek_kelime, 0, 3, "a b", top=1500)
    assert _kirilir(TP.son_kart, 0, 2, "FR")
    assert _kirilir(TP.son_kart, 0, 2, "DE")                                           # AB'de rozet metni zorunlu (uydurma teklif yok)
    assert _kirilir(TP.son_kart, 0, 2, "DE", rozet="X", ikinci="Y", dugme="Z", top=1200)
    assert _kirilir(TP.altyazi, 0, 2, "metin", top=1500)
    assert _kirilir(TP.iki_katman, 0, 2, {"sablon": "yok"}, {"metin": "x"})


def test_ikili_kiyas():
    _yeni()
    TP.ikili_kiyas(0, 4, "Hangisi 10 saniyede kurudu?", "ESKİ YÖNTEM", "ÜRÜN", kazanan="sag", cevap_an=3.0)
    html, js = " ".join(B.P), " ".join(B.T)
    assert 'class="bolen"' in html and "ikes sol" in html and "ikes sag" in html and "ESKİ YÖNTEM" in html
    assert 'class="ikdim sol"' in html and "iktik" in html and "igk" in html            # kaybeden sol karardı, tik sağda, üstte soru kutusu
    assert re.search(r'id="ikk\d+T"', html)                                            # tik öğesi
    assert any(o["tur"] == "kanit" and o["t"] == 3.0 for o in TP.OL)
    assert not re.search(r",\s*-\d+(\.\d+)?\);", js)                                  # negatif GSAP konumu yok
    _yeni()
    TP.ikili_kiyas(0, 4, "Hangisi daha hızlı?", "A", "B")                              # kazananı olmayan kıyas: tik/karartma yok
    assert "iktik" not in " ".join(B.P) and "ikdim" not in " ".join(B.P)
    # soru kutusu telefonda okunur: tek satırda ~42 px kalıyordu → 2 satıra bölünüp büyür (≥ 72 px), genişlik sağ/sol 130 px güvenli alanda
    _yeni()
    TP.ikili_kiyas(0, 4, "Hangisi 10 saniyede kurudu?", "A", "B")
    h = " ".join(B.P)
    boy = int(re.search(r'class="tx igk renk" style="[^"]*?font-size:(\d+)px', h).group(1))
    assert boy >= 72, "soru yazısı küçük: %d px" % boy
    assert h.count('class="sat"') == 2                                                  # 2 satıra bölündü
    sol, gen = [int(x) for x in re.search(r'class="tx igk renk" style="[^"]*?left:(\d+)px;width:(\d+)px', h).groups()]
    assert sol >= 110 and sol + gen <= 1080 - 110
    _yeni()
    TP.ikili_kiyas(0, 4, "Hangisi daha hızlı?", "A", "B")                              # kısa soru da büyük
    assert int(re.search(r'class="tx igk renk" style="[^"]*?font-size:(\d+)px', " ".join(B.P)).group(1)) >= 80
    _yeni()
    assert TP.IK_ETIKET_TOP + 90 <= TP.OKUMA_ALT                                        # etiketler y ≤ 1330
    # kırma: tek soru, 7 kelime, iki etiket, kazanan değeri, cevap anı aralığı, üst güvenli alan
    assert _kirilir(TP.ikili_kiyas, 0, 4, "Hangisi? Bu mu?", "A", "B")
    assert _kirilir(TP.ikili_kiyas, 0, 4, "Soru yok bu cümlede", "A", "B")
    assert _kirilir(TP.ikili_kiyas, 0, 4, "bir iki üç dört beş altı yedi sekiz mi?", "A", "B")
    assert _kirilir(TP.ikili_kiyas, 0, 4, "Hangisi?", "", "B")
    assert _kirilir(TP.ikili_kiyas, 0, 4, "Hangisi?", "A", "B", kazanan="orta")
    assert _kirilir(TP.ikili_kiyas, 0, 4, "Hangisi?", "A", "B", kazanan="sol", cevap_an=5.0)
    assert _kirilir(TP.ikili_kiyas, 0, 4, "Hangisi?", "A", "B", top=100)


def test_deneme_sayaci():
    _yeni()
    TP.deneme_sayaci(0, 6, 3, [1.5, 3.0, 4.5], kural="3 leke. Tek silme.")
    html, js = " ".join(B.P), " ".join(B.T)
    for k in range(4):
        assert ">%d/3<" % k in html, k                                                  # 0/3 → 1/3 → 2/3 → 3/3
    assert re.search(r'id="dsy\d+s0"', html)
    assert js.count("opacity:0},") >= 3 and "#22C55E" in js                             # son adım yeşil
    adimlar = [o["t"] for o in TP.OL if o.get("sablon") == "deneme_sayaci"]
    assert adimlar == [1.5, 3.0, 4.5]
    assert "silme" in html
    assert not re.search(r",\s*-\d+(\.\d+)?\);", js)                                  # negatif GSAP konumu yok
    # kırma: adım sayısı, sıra, aralık, toplam, kural uzunluğu, güvenli alan
    assert _kirilir(TP.deneme_sayaci, 0, 6, 3, [1, 2])
    assert _kirilir(TP.deneme_sayaci, 0, 6, 3, [3, 2, 4])
    assert _kirilir(TP.deneme_sayaci, 0, 6, 3, [0, 2, 4])                                # ilk adım bas'ta
    assert _kirilir(TP.deneme_sayaci, 0, 6, 3, [1, 2, 6])                                # son adım bitişte
    assert _kirilir(TP.deneme_sayaci, 0, 6, 1, [1])
    assert _kirilir(TP.deneme_sayaci, 0, 6, 3, [1, 2, 3], kural="bir iki üç dört beş altı yedi sekiz")
    assert _kirilir(TP.deneme_sayaci, 0, 6, 3, [1, 2, 3], kural="a / b")
    assert _kirilir(TP.deneme_sayaci, 0, 6, 3, [1, 2, 3], top_sayac=1200)


def test_cta_guvenli_alan_ve_donusum():
    _yeni()
    assert _kirilir(TP.cta_rozet, 1, 2, "X", top=1500)                                  # alt 420 px güvenli alana giriyor
    assert _kirilir(TP.donusum, [[0.5, 2.0]], {"sablon": "ig_kutu", "metin": "a"}, {"sablon": "cta_rozet", "anahtar": "X"})   # ilk pencere 0'da değil
    assert _kirilir(TP.donusum, [[0, 2.0]], {"sablon": "yok", "metin": "a"}, {"sablon": "cta_rozet", "anahtar": "X"})
    _yeni()
    TP.donusum([[0, 2.0], [2.0, 4.0], [4.0, 6.0]], {"sablon": "ig_kutu", "metin": "a b"}, {"sablon": "cta_rozet", "anahtar": "X"})
    html = " ".join(B.P)
    assert 'id="dn0"' in html and 'id="dn1"' in html and 'id="dn2"' in html
    assert "igk" in html and "cta" in html


def test_gecis_klipleri():
    _yeni()
    t_ = [0, 1.5, 3.0, 4.5]
    TP.klipler([{"i": 0}, {"i": 1}, {"i": 2, "tur": "bolunmus", "etiket1": "A", "etiket2": "B"}], t_, ["whip", "punch"], 4.5)
    html, js = " ".join(B.P), " ".join(B.T)
    assert "x:-950" in js and "scale:1.22" in js                                       # whip ve punch hareketi
    assert 'id="a2bolen"' in html and "yarim sag" in html
    tipler = [o["tip"] for o in TP.OL if o["tur"] == "kesme"]
    assert tipler == ["whip", "punch"]


def test_sfx_esleme():
    ol = [{"t": 0, "tur": "yazi"}, {"t": 1.4, "tur": "kesme", "tip": "whip"}, {"t": 2.2, "tur": "cta"}, {"t": 3.1, "tur": "kesme", "tip": "punch"},
          {"t": 4.6, "tur": "kanit", "ses": "ding"}, {"t": 6.0, "tur": "cta"}, {"t": 5.0, "tur": "yazi"}, {"t": 6.4, "tur": "kesme", "tip": "punch"}]
    r = sfx_esle.esle(ol, 8.0, drop=4.6, max10=6)
    ks = [e["k"] for e in r["plan"]]
    assert ks[0] == "acilis" and r["plan"][0]["t"] < 0.5                                 # 0. sn diegetik olay hiç elenmez
    assert "kanit" in ks and "riser" in ks and "whip" in ks and "cta" in ks
    assert len(r["plan"]) <= 6 and r["elenen"], "yoğunluk kapısı fazlayı elemeli"
    assert r["riser"] and float(r["riser"].split(":")[0]) < 4.6                          # riser drop'tan önce biter
    assert r["sfx"].startswith("lib_pop.mp3@0.02:-4")
    r2 = sfx_esle.esle(ol, 8.0, drop=4.6, max10=3)                                       # sıkı pencere: önemli olaylar kalır
    assert len(r2["plan"]) <= 3 and "acilis" in [e["k"] for e in r2["plan"]] and "kanit" in [e["k"] for e in r2["plan"]]
    for ad, (dosya, db, _) in sfx_esle.KART.items():
        assert db <= -3, ad
    assert sfx_esle.KART["bubble"][0] == "bubble.wav" and sfx_esle.KART["whoosh"][1] == -9


def test_sfx_kaynaklari_ve_lisans():
    with tempfile.TemporaryDirectory() as d:
        sfx_esle.klasor_hazirla(d)
        for ad, (dosya, _, _) in sfx_esle.KART.items():
            if dosya.startswith("lib_"):
                assert os.path.getsize(os.path.join(d, dosya)) > 1000, dosya
    lic = open(os.path.join(BURADA, "LISANS-SFX.md"), encoding="utf-8").read()
    for dosya in ("lib_whoosh-short.mp3", "lib_pop.mp3", "lib_sparkle.mp3", "lib_ping.mp3", "lib_impact-bass-2.mp3", "bubble.wav"):
        assert dosya in lic, dosya


def test_muzik_sentez():
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "m.wav")
        r = subprocess.run([sys.executable, os.path.join(BURADA, "muzik_sentez.py"), out, "--sure", "12", "--drop_bar", "2"], capture_output=True, text=True)
        assert r.returncode == 0 and "drop_sn=" in r.stdout and os.path.getsize(out) > 100000


def _svg(klasor, ad):
    """Jenerik yer tutucu (daire + harf); gerçek logo/ürün dosyası depoya girmez."""
    yol = os.path.join(klasor, ad)
    with open(yol, "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400"><circle cx="200" cy="200" r="190" fill="#d9a066"/>'
                '<text x="200" y="270" font-size="220" text-anchor="middle" fill="#fff">A</text></svg>')
    return yol


def _negatif_yok(js, html):
    assert not re.search(r",\s*-\d+(\.\d+)?\);", js), "negatif GSAP konumu"
    assert all(float(x) >= 0 for x in re.findall(r'data-start="(-?[\d.]+)"', html)), "negatif data-start"


def test_urun_gecisi():
    with tempfile.TemporaryDirectory() as d:
        svg = _svg(d, "urun.svg")
        _yeni()
        TP.urun_gecisi(2.0, 4.0, svg, kick="YENİ", ust1="Evde", ust2="*sessiz* güç", alt="bugün dene")
        html, js = " ".join(B.P), " ".join(B.T)
        assert 'data-start="1.3"' in html and 'data-duration="4.7"' in html            # bas−0,7 başlar, sure+0,7 sürer
        assert 'tl.to("#ug1w",{opacity:1,duration:0.7,ease:"sine.inOut"},1.3)' in js   # 0,7 sn çapraz geçiş
        assert 'scale:1.06' in js and 'brightness(0.6)' in js and "duration:1.0" in js
        assert ',1.6)' in js                                                            # yazılar geçişten 0,3 sn sonra
        assert 'class="ugw"' in html and "assets/img/urun.svg" in html and d not in html   # ev/geçici dizin HTML'e sızmaz
        assert html.count('class="clip ugy"') == 1                                      # tek yazı katmanı
        _negatif_yok(js, html)
        # ilk karede: sahne opacity 0 ile (CSS) başlar, önceki klip görünür kalır
        assert re.search(r"\.ugw \{[^}]*opacity:0", open(os.path.join(BURADA, "sablon.css"), encoding="utf-8").read())
        assert any(o["tur"] == "yazi" and o["t"] == 1.6 for o in TP.OL)
        with tempfile.TemporaryDirectory() as k:
            TP.varliklari_kopyala(k)
            assert os.path.getsize(os.path.join(k, "assets", "img", "urun.svg")) > 100
        # kırma: bas < gecis (negatif başlangıç), kısa süre, olmayan görsel, geçersiz uzantı, güvenli alan
        assert _kirilir(TP.urun_gecisi, 0.5, 4.0, svg)
        assert _kirilir(TP.urun_gecisi, 2.0, 1.0, svg)
        assert _kirilir(TP.urun_gecisi, 2.0, 4.0, os.path.join(d, "yok.png"))
        assert _kirilir(TP.urun_gecisi, 2.0, 4.0, os.path.join(d, "urun.svg"), top_yazi=100)
        assert _kirilir(TP.urun_gecisi, 2.0, 4.0, svg, alt_top=1300)
        try:
            TP.urun_gecisi(2.0, 4.0, os.path.join(d, "yok.png"))
        except SystemExit as e:
            assert "bulunamadı" in str(e)
    _yeni()
    TP.urun_gecisi(1.0, 3.0, None, ust2="yalnız yazı")                                # görselsiz de çalışır
    assert 'class="ugu"' not in " ".join(B.P) and "<img" not in " ".join(B.P)


def test_dip_gecis():
    _yeni()
    TP.dip_gecis(2.5)
    html, js = " ".join(B.P), " ".join(B.T)
    assert 'data-start="2.15"' in html and 'data-track-index="8"' in html              # kesimden 0,35 sn önce
    assert 'tl.fromTo("#dip1i",{opacity:0},{opacity:0.7,duration:0.35,ease:"sine.in"},2.15)' in js   # ilk karede örtü yok (opacity 0 başlar)
    assert 'tl.to("#dip1i",{opacity:0,duration:0.6,ease:"sine.out"},2.5)' in js        # 0,6 sn açılış
    assert 'class="tx' not in html and "kpy" not in html                              # yazı katmanı yok
    _negatif_yok(js, html)
    TP.dip_gecis(4.0, once=0.5, ac=0.8, yogunluk=1.0)
    # kırma: z < once (negatif konum), yoğunluk, süreler
    assert _kirilir(TP.dip_gecis, 0.2)
    assert _kirilir(TP.dip_gecis, 3.0, yogunluk=1.5)
    assert _kirilir(TP.dip_gecis, 3.0, once=0)


def test_kapanis():
    with tempfile.TemporaryDirectory() as d:
        logo = _svg(d, "logo.svg")
        _yeni()
        TP.kapanis(0.5, 4.5, logo, "MARKA", alt_satir="alt satır", yazi="Şimdi dene")
        html, js = " ".join(B.P), " ".join(B.T)
        assert html.count('class="kpy') <= 2 and html.count('class="kpy') == 2          # CTA + marka/alt satır; logo görsel katman
        assert "assets/img/logo.svg" in html and ">MARKA<" in html and ">alt satır<" in html and d not in html
        assert 'data-start="4.2" data-duration="0.8"' in html                            # son 0,8 sn siyaha fade (bit = 5.0)
        assert 'tl.fromTo("#kp1ki",{opacity:0},{opacity:1,duration:0.8,ease:"sine.in"},4.2)' in js
        assert "scale:0.82" in js and "tl.set(" not in js                                # yumuşak kapalıyken odak yumuşatma yok (blur yalnız tl.set ile)
        assert 'tl.fromTo("#kp1zi",{opacity:0}' in js                                    # örtü opacity 0 başlar: ilk karede video görünür
        _negatif_yok(js, html)
        # yumuşak: odak yumuşatma + uzun (1,4 sn) kararma
        _yeni()
        TP.kapanis(0.5, 4.5, logo, "MARKA", alt_satir="alt", yumusak=2)
        html, js = " ".join(B.P), " ".join(B.T)
        assert 'tl.set("#kp1ld, #kp1b",{filter:"blur(2.0px)"},0)' in js
        assert 'data-start="3.6" data-duration="1.4"' in html
        assert html.count('class="kpy') == 1                                             # CTA yok → tek yazı katmanı
        _negatif_yok(js, html)
        _yeni()
        TP.kapanis(0, 3, logo, "M")                                                      # bas=0 serbest; hiçbir tween negatif değil
        _negatif_yok(" ".join(B.T), " ".join(B.P))
        # kırma: olmayan logo (anlaşılır hata), boş marka, kısa süre, 8 kelimelik CTA, 3 satırlı CTA, güvenli alan
        try:
            TP.kapanis(0.5, 4.5, os.path.join(d, "yok.png"), "M")
            raise AssertionError("olmayan logo geçmemeli")
        except SystemExit as e:
            assert "HATA" in str(e) and "logo" in str(e) and "bulunamadı" in str(e)
        assert _kirilir(TP.kapanis, 0.5, 4.5, logo, " ")
        assert _kirilir(TP.kapanis, 0.5, 2.0, logo, "M")
        assert _kirilir(TP.kapanis, 0.5, 4.5, logo, "M", yumusak=2, kapan_sn=1.4, yazi="a b c d e f g h")
        assert _kirilir(TP.kapanis, 0.5, 4.5, logo, "M", yazi="a / b / c")
        assert _kirilir(TP.kapanis, 0.5, 4.5, logo, "M", top_logo=1100)
        assert _kirilir(TP.kapanis, 0.5, 4.5, logo, "M", top_yazi=100, yazi="a b")
        # sahne ayarı yolundan (TURLER) çağrılabilir
        assert {"urun_gecisi", "dip_gecis", "kapanis"} <= set(TP.TURLER)


def _ffmpeg_bul():
    import shutil
    yol = shutil.which("ffmpeg")
    try:
        import imageio_ffmpeg
        yol = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # noqa: BLE001
        pass
    return yol


def test_ses_son_fade_egri():
    """--son_fade_egri qsin son N sn yumuşak fade-out verir; bayrak yokken davranış eskisiyle aynı (doğrusal, bayrak yok)."""
    ff = _ffmpeg_bul()
    if not ff:
        print("ATLANDI test_ses_son_fade_egri: ffmpeg yok")
        return
    try:
        import numpy as np
    except ImportError:
        print("ATLANDI test_ses_son_fade_egri: numpy yok")
        return
    ses = os.path.join(BURADA, "..", "scripts", "ses_tasarla.py")
    src = open(ses, encoding="utf-8").read()
    assert 'afade=t=out:st={max(0,sure-a.son_fade):.3f}:d={a.son_fade}"' in src          # varsayılan grafik bozulmadı (curve yalnız bayrakla eklenir)
    with tempfile.TemporaryDirectory() as d:
        v, m = os.path.join(d, "v.mp4"), os.path.join(d, "m.wav")
        subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=64x64:d=10", "-f", "lavfi", "-i", "anoisesrc=d=10:c=pink:a=0.05",
                        "-shortest", "-c:v", "libx264", "-c:a", "aac", v], check=True)
        subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "sine=f=220:d=10", m], check=True)

        def kos(*ek):
            n = len(os.listdir(d))
            o, st = os.path.join(d, "o%d.wav" % n), os.path.join(d, "st%d" % n)
            r = subprocess.run([sys.executable, ses, "--video", v, "--muzik", m, "--cikti", o, "--stem_klasoru", st] + list(ek), capture_output=True, text=True)
            assert r.returncode == 0 and os.path.exists(os.path.join(st, "muz.wav")), r.stderr[-300:]
            raw = subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-i", os.path.join(st, "muz.wav"), "-f", "f32le", "-ac", "1", "-ar", "8000", "-"], capture_output=True).stdout   # yalnız müzik stem'i
            x = np.frombuffer(raw, dtype=np.float32)
            return np.sqrt(np.mean(x[-int(0.5 * 8000):] ** 2)), np.sqrt(np.mean(x[-int(2.5 * 8000):-int(2.0 * 8000)] ** 2))
        son_v, orta_v = kos()                                                               # varsayılan (0,8 sn)
        son_y, orta_y = kos("--son_fade", "2.5", "--son_fade_egri", "qsin")
        assert son_y < son_v * 0.7, "yumuşak fade son 0,5 sn'yi belirgin kısmalı (%.4f vs %.4f)" % (son_y, son_v)
        assert orta_y < orta_v, "2,5 sn fade başlangıcı (son 2,5–2,0 sn) varsayılandan daha kısık olmalı"


def _calistir():
    sonuc = []
    for ad, fn in sorted(globals().items()):
        if ad.startswith("test_") and callable(fn):
            try:
                fn()
                print("GEÇTİ", ad)
                sonuc.append(True)
            except Exception as e:  # noqa: BLE001
                print("KALDI ", ad, "|", repr(e)[:300])
                sonuc.append(False)
    print("%d/%d geçti" % (sum(sonuc), len(sonuc)))
    return 0 if all(sonuc) else 1


if __name__ == "__main__":
    sys.exit(_calistir())
