"""HyperFrames tipografi + geçiş şablonları (kanca · tipografi · geçiş paketi). Kredisiz, ağsız üretim; yalnız HTML + GSAP metni yazar.

Altı yazı şablonu (hepsi parametreli: metin, vurgu kelime(ler), renk, konum, süre):
  ig_kutu       (a) IG-yerli beyaz kutu, siyah yazı; vurgu kelime renkli kutu
  kalin_kontur  (b) kalın sans, beyaz + siyah kontur/gölge; vurgu kelime renkli
  karaoke       (c) kelime kelime karaoke vurgu (kelime sırayla renk + büyüme)
  tepki         (d) "I'm sorry but WHAT?!" tepki/şok: küçük cümle + dev kelime çarpması
  cta_rozet     (e) "Comment 'X'" yorum-anahtar rozeti + zıplayan ok
  sayac         (f) kanıt / rakam sayacı (0 → N, bitişte çarpma)
  donusum       kanca ↔ CTA dönüşümlü (pencereler listesi; ayrı bitiş kartı yok)
TR/AB referans paketi (REFERANSLAR 0.6): uzman_kutu (siyah kutu BÜYÜK HARF), tek_kelime (kelime kelime, göğüs hizası), altyazi + iki_katman (büyük kanca + küçük
  konuşma altyazısı), son_kart (mağazanın gerçek teklif rozeti · AB teklif/kargo rozeti + düğme · ABD Comment/LINK IN BIO), dev_fiyat (dev kırmızı vuruş); ig_kutu'ya vurgu_stil="renk" + emoji.
Geçiş + kapanış paketi (genel; müşteri kitinden taşındı): urun_gecisi (ürün sahnesi 0,7 sn çapraz geçiş), dip_gecis (kesimden önce kararma → açılış), kapanis (logo + marka + alt satır, son 0,8 sn siyaha fade; yumusak=px).
Klip katmanı: klipler() — plan başına geçiş (whip | punch | kesim), bölünmüş ekran, donmuş "sorun anı", yakın çekim (z0).
Yazı metni sözdizimi (bloklar.W ile aynı): '/' satır kırar · '*kelime*' ya da '*iki kelime*' vurgu · '_' kelime içi boşluk.

Güvenli alan (IG arayüzü, 1080×1920): üst 220 px ve alt 420 px boş, sağ 130 px boş. Kanca: 0. karede görünür, ≤ 2 satır, ≤ 7 kelime.
Kullanım: bloklar.py bu modülü içe aktarır (baglan(P, T)); sahne türleri ayar JSON'unda "tur": "ig_kutu" vb. yazılır.
"""
import json
import os
import re

P = T = None
OL = []          # ses olayları (sfx_esle.py okur): {"t": sn, "tur": yazi|kesme|kanit|cta|sok, ...}
_SAYAC = [0]
IKI_YARI = 540
GUVENLI_UST, GUVENLI_ALT = 220, 420   # px (1080×1920)
OKUMA_ALT = 1330                       # yeni öğeler (altyazı, son kart) için önerilen alt sınır: HyperFrames dikey kılavuzu (168–1330 bandı)
KANCA_KELIME_MAX, KANCA_SATIR_MAX = 7, 2
KANCA_TURLERI = ("kanca", "ig_kutu", "kalin_kontur", "karaoke", "tepki", "donusum", "uzman_kutu", "tek_kelime", "iki_katman")


def baglan(p, t):
    global P, T
    P, T = p, t


def sifirla():
    del OL[:]
    del VARLIK[:]
    _SAYAC[0] = 0


def _t(s):
    T.append(s)


def _id(pid, on="t"):
    if pid:
        return pid
    _SAYAC[0] += 1
    return "%s%d" % (on, _SAYAC[0])


def _r(x):
    return round(float(x), 3)


def satirlar(metin, vurgu=None):
    """'a *b* / c' → [[('a', False), ('b', True)], [('c', False)]]; vurgu listesindeki kelimeler de vurgulu."""
    vs = {v.lower().strip(".,!?\"'“”") for v in (vurgu or ())}
    sat = []
    for parca in str(metin).split("/"):
        ks, icinde = [], False
        for k in parca.split():
            if k.startswith("*"):
                icinde = True
            k2 = k.lstrip("*")
            kapanis = "*" in k2
            kk = k2.replace("*", "").replace("_", " ")
            ks.append((kk, icinde or kk.lower().strip(".,!?\"'“”") in vs))
            if kapanis:
                icinde = False
        if ks:
            sat.append(ks)
    return sat


def buyuk(s, dil="en"):
    """Büyük harf: TR'de i→İ, ı→I (str.upper() Türkçe'yi bozar)."""
    if dil == "tr":
        s = s.replace("i", "İ").replace("ı", "I")
    return s.upper()


def kelime_sayisi(sat):
    return sum(len(s) for s in sat)


def kanca_kapisi(sat, bas, ad):
    """İlk karedeki yazı (bas < 0,05) kanca sayılır: ≤ 2 satır, ≤ 7 kelime (saha: kısa kanca)."""
    if float(bas) < 0.05 and (len(sat) > KANCA_SATIR_MAX or kelime_sayisi(sat) > KANCA_KELIME_MAX):
        raise SystemExit("HATA: kanca (%s) %d satır / %d kelime; en çok %d satır, %d kelime" %
                         (ad, len(sat), kelime_sayisi(sat), KANCA_SATIR_MAX, KANCA_KELIME_MAX))


def _kap(pid, bas, sure, ic, track=4):
    P.append('<div id="%s" class="clip" data-start="%s" data-duration="%s" data-track-index="%d">%s</div>' % (pid, _r(bas), _r(sure), track, ic))
    if float(bas) >= 0.05:   # kanca dışı yazılar kısa yumuşak girer: büyük beyaz kutunun tek karede belirmesi görüntü kapısında sıçrama sayılır
        _t('tl.fromTo("#%s .tx",{opacity:0},{opacity:1,duration:0.12,ease:"none"},%s);' % (pid, _r(bas)))


def _cik(pid, bas, sure):
    _t('tl.to("#%s .tx",{opacity:0,duration:0.12,ease:"power2.in"},%s);' % (pid, _r(bas + sure - 0.14)))


def _kelimeler_html(pid, sat, sarma=None):
    n, satir_html = 0, []
    for s in sat:
        ws = []
        for k, v in s:
            ws.append('<span class="w%s" id="%sw%d">%s</span>' % (" v" if v else "", pid, n, k))
            n += 1
        ic = " ".join(ws)
        satir_html.append('<div class="sat">%s</div>' % (('<span class="%s">%s</span>' % (sarma, ic)) if sarma else ic))
    return "".join(satir_html), n


def _pop(pid, n, bas, adim, ilk):
    """Kelime kelime pop-in: ilk `ilk` kelime 0. karede görünür (hafif çarpma), kalanlar `adim` (0,08–0,12 sn) arayla opacity 0'dan girer."""
    for i in range(n):
        if ilk >= n and n > 0:      # tüm satır 0. karede okunur (küçük resim = tam kanca); pop = kelime sırasıyla zıplama
            _t('tl.fromTo("#%sw%d",{scale:1},{keyframes:[{scale:1.22,duration:0.05,ease:"power2.out"},{scale:1,duration:0.08,ease:"power2.in"}]},%s);' % (pid, i, _r(bas + i * adim)))
        elif i < ilk:
            _t('tl.fromTo("#%sw%d",{scale:1.2},{scale:1,duration:0.14,ease:"power3.out"},%s);' % (pid, i, _r(bas)))
        else:
            k = (i - ilk + 1) if ilk > 0 else i
            _t('tl.fromTo("#%sw%d",{opacity:0,scale:0.55,y:24},{opacity:1,scale:1,y:0,duration:0.1,ease:"back.out(2.4)"},%s);' % (pid, i, _r(bas + k * adim)))


def _ilk(ilk_kare, bas, n):
    if ilk_kare in ("hepsi", "all"):
        return n
    if ilk_kare is None:
        return n if float(bas) < 0.05 else 0
    return min(int(ilk_kare), n)


def sigdir(sat, boy, ek_em=0.0, genislik=760, faktor=0.62):
    """Satır sarmasın: en uzun satır (karakter × ~0,62 em (Montserrat 800–900 + kelime boşluğu; 0,57 ile ig_kutu kancası 3 satıra sarıldı, ölçüldü) + ek) genislik px'e sığacak yazı boyu (üst sınır = istenen boy)."""
    maxc = max(sum(len(k) for k, _ in s) + len(s) - 1 for s in sat) if sat else 1
    return int(min(boy, genislik / (maxc * faktor + ek_em)))


def _stil(top, boy, renk, ek=""):
    return 'top:%dpx;font-size:%dpx;--vurgu:%s;%s' % (top, boy, renk, ek)


# ---------------------------------------------------------------- (a) IG-yerli kutu
def ig_kutu(bas, sure, metin, vurgu=None, renk="#FFE600", top=300, boy=96, adim=0.1, ilk_kare=None, vurgu_stil="kutu", emoji="",
            kutu_renk=None, yazi_renk=None, buyuk_harf=False, dil="en", pid=None, genislik=760):
    """genislik: yazı satırının sığacağı px (varsayılan 760 = eski davranış; kapsayıcı genislik+20 px, ortalı).
    vurgu_stil: 'kutu' (vurgu kelime renkli kutu) | 'renk' (yalnız yazı rengi; TR01/AB01: beyaz kutu + TEK kırmızı kelime). emoji: son kelimeye eklenir.
    kutu_renk/yazi_renk: siyah kutu beyaz yazı (uzman_kutu) için. buyuk_harf: dil='tr' için i→İ."""
    pid = _id(pid, "igk")
    if buyuk_harf:
        metin = buyuk(metin, dil)
    sat = satirlar(metin, vurgu)
    if emoji and sat:
        sat[-1][-1] = (sat[-1][-1][0] + " " + emoji, sat[-1][-1][1])
    kanca_kapisi(sat, bas, pid)
    ic, n = _kelimeler_html(pid, sat, sarma="kutu")
    boy = sigdir(sat, boy, ek_em=1.9 if buyuk_harf else 1.2, faktor=0.74 if buyuk_harf else 0.62, genislik=genislik)
    ek = ""
    if genislik != 760:
        ek += "left:%dpx;width:%dpx;" % ((1080 - (genislik + 20)) // 2, genislik + 20)
    if kutu_renk:
        ek += "--kutu:%s;" % kutu_renk
    if yazi_renk:
        ek += "--yazi:%s;" % yazi_renk
    _kap(pid, bas, sure, '<div class="tx igk%s" style="%s">%s</div>' % (" renk" if vurgu_stil == "renk" else "", _stil(top, boy, renk, ek), ic))
    _pop(pid, n, bas, adim, _ilk(ilk_kare, bas, n))
    _cik(pid, bas, sure)
    OL.append({"t": _r(bas), "tur": "yazi", "sablon": "ig_kutu"})


def uzman_kutu(bas, sure, metin, vurgu=None, renk="#FFE600", top=300, boy=92, dil="en", **k):
    """Siyah kutu, beyaz KALIN BÜYÜK HARF (uzman/acil; TR03, TR05); vurgu kelime sarı yazı."""
    ig_kutu(bas, sure, metin, vurgu=vurgu, renk=renk, top=top, boy=boy, vurgu_stil="renk", kutu_renk="rgba(0,0,0,0.80)", yazi_renk="#ffffff",
            buyuk_harf=True, dil=dil, **k)


# ---------------------------------------------------------------- (b) kalın kontur
def kalin_kontur(bas, sure, metin, vurgu=None, renk="#FFE600", top=300, boy=118, adim=0.1, ilk_kare=None, buyuk_harf=False, dil="en", pid=None):
    pid = _id(pid, "kk")
    if buyuk_harf:
        metin = buyuk(metin, dil)
    sat = satirlar(metin, vurgu)
    kanca_kapisi(sat, bas, pid)
    ic, n = _kelimeler_html(pid, sat)
    boy = sigdir(sat, boy, ek_em=0.3, faktor=0.74 if buyuk_harf else 0.62)
    _kap(pid, bas, sure, '<div class="tx kk" style="%s">%s</div>' % (_stil(top, boy, renk), ic))
    _pop(pid, n, bas, adim, _ilk(ilk_kare, bas, n))
    _cik(pid, bas, sure)
    OL.append({"t": _r(bas), "tur": "yazi", "sablon": "kalin_kontur"})


# ---------------------------------------------------------------- (c) karaoke
def karaoke(bas, sure, metin, vurgu=None, renk="#FFE600", top=300, boy=104, adim=0.3, zamanlar=None, pid=None):
    """Tüm satır 0. karede görünür (soluk); kelimeler sırayla renk + büyüme alır. zamanlar: kelime başına saniye (yoksa adim aralığı)."""
    pid = _id(pid, "kar")
    sat = satirlar(metin, vurgu)
    kanca_kapisi(sat, bas, pid)
    ic, n = _kelimeler_html(pid, sat)
    boy = sigdir(sat, boy, ek_em=0.5, genislik=680, faktor=0.68)
    _kap(pid, bas, sure, '<div class="tx kar" style="%s"><span class="pil">%s</span></div>' % (_stil(top, boy, renk), ic))
    zs = [float(z) for z in zamanlar] if zamanlar else [i * adim for i in range(n)]
    if len(zs) < n:
        raise SystemExit("HATA: karaoke zamanlar %d < kelime %d" % (len(zs), n))
    for i in range(n):
        a = _r(bas + zs[i])
        _t('tl.fromTo("#%sw%d",{opacity:0.55,color:"#ffffff",scale:1},{opacity:1,color:"%s",scale:1.14,duration:0.08,ease:"power2.out"},%s);' % (pid, i, renk, a))
        if i + 1 < n:
            _t('tl.to("#%sw%d",{color:"#ffffff",scale:1,duration:0.1,ease:"power2.out"},%s);' % (pid, i, _r(bas + zs[i + 1])))
    _cik(pid, bas, sure)
    OL.append({"t": _r(bas), "tur": "yazi", "sablon": "karaoke"})


# ---------------------------------------------------------------- (d) tepki / şok
def tepki(bas, sure, ust, buyuk, vurgu=None, renk="#FFE600", top=300, boy=100, adim=0.1, slam=0.35, pid=None):
    """ust: küçük cümle ("Im sorry but"), buyuk: dev kelime ("WHAT?!"). Küçük cümle 0. karede; dev kelime `slam` sn sonra çarpar."""
    pid = _id(pid, "tk")
    sat = satirlar(ust, vurgu)
    toplam = kelime_sayisi(sat) + 1
    if float(bas) < 0.05 and (toplam > KANCA_KELIME_MAX or len(sat) + 1 > KANCA_SATIR_MAX):
        raise SystemExit("HATA: kanca (%s) %d kelime / %d satır; en çok %d kelime, %d satır" % (pid, toplam, len(sat) + 1, KANCA_KELIME_MAX, KANCA_SATIR_MAX))
    ic, n = _kelimeler_html(pid, sat)
    boy = sigdir(sat, boy, ek_em=0.3)
    bboy = int(min(250, 740 / (len(buyuk) * 0.68)))      # dev kelime güvenli genişliğe sığar (kontur + italik payı)
    ic = ('<div class="ust kk" style="font-size:%dpx">%s</div><div class="buyuk" id="%sb" style="font-size:%dpx" data-layout-allow-overlap data-layout-allow-overflow>%s</div>'
          % (boy, ic, pid, bboy, buyuk))
    _kap(pid, bas, sure, '<div class="tx tk" style="top:%dpx;--vurgu:%s">%s</div>' % (top, renk, ic))
    _pop(pid, n, bas, adim, n if float(bas) < 0.05 else 0)
    b = _r(bas + slam)
    _t('tl.fromTo("#%sb",{opacity:0,scale:3.0,rotation:-14},{opacity:1,scale:1,rotation:-5,duration:0.2,ease:"power4.in"},%s);' % (pid, b))
    _t('tl.fromTo("#%sb",{x:0},{keyframes:[{x:-14,duration:0.035},{x:14,duration:0.035},{x:-8,duration:0.035},{x:0,duration:0.035}]},%s);' % (pid, _r(bas + slam + 0.2)))
    _cik(pid, bas, sure)
    OL.append({"t": _r(bas), "tur": "yazi", "sablon": "tepki"})
    OL.append({"t": _r(bas + slam + 0.2), "tur": "sok"})


# ---------------------------------------------------------------- (e) yorum-anahtar CTA rozeti
_BAL = '<svg width="76" height="76" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L3 20.5l1.5-4.6A8 8 0 1 1 21 12z"/></svg>'
_OK = '<svg class="ok" id="%sok" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 6px 0 rgba(0,0,0,0.85))"><path d="M12 3v16"/><path d="M5 12l7 8 7-8"/></svg>'


def cta_rozet(bas, sure, anahtar, on="Comment", alt="", renk="#16A34A", top=1130, boy=68, pid=None):
    """Yeşil rozet: Comment “ANAHTAR” + alt satır + zıplayan ok. Konum alt güvenli alanın (y ≥ 1500) üstünde kalır."""
    pid = _id(pid, "cta")
    if top + 330 > 1920 - GUVENLI_ALT:
        raise SystemExit("HATA: cta_rozet top=%d alt güvenli alana (y≥%d) giriyor" % (top, 1920 - GUVENLI_ALT))
    alt_html = ""
    if alt:   # isteğe bağlı alt satır (saha: ekranda yalnız Comment "X"; "DM link" caption'da); okunma tabanı: 0,5 + 0,3 sn/kelime
        sat = satirlar(alt)
        a_ic, _n = _kelimeler_html(pid, sat)
        alt_html = '<div class="alt kk" id="%sa">%s</div>' % (pid, a_ic)
    ic = ('<div class="rozet" id="%sr" style="background:%s;font-size:%dpx"><span class="bal">%s</span><span class="on">%s</span>'
          '<span class="anahtar">“%s”</span></div>%s%s') % (pid, renk, boy, _BAL, on, anahtar, alt_html, _OK % pid)
    _kap(pid, bas, sure, '<div class="tx cta" style="top:%dpx">%s</div>' % (top, ic), track=5)
    _t('tl.fromTo("#%sr",{opacity:0,scale:0.4,y:40},{opacity:1,scale:1,y:0,duration:0.3,ease:"back.out(2)"},%s);' % (pid, _r(bas)))
    if alt:
        _t('tl.fromTo("#%sa",{opacity:0,y:18},{opacity:1,y:0,duration:0.25,ease:"power2.out"},%s);' % (pid, _r(bas + 0.25)))
    tekrar = max(1, int((sure - 0.6) / 0.34))
    _t('tl.fromTo("#%sok",{y:0},{y:28,duration:0.34,ease:"sine.inOut",yoyo:true,repeat:%d},%s);' % (pid, tekrar, _r(bas + 0.5)))
    _cik(pid, bas, sure)
    OL.append({"t": _r(bas), "tur": "cta"})


# ---------------------------------------------------------------- (f) kanıt / rakam sayacı
def sayac(bas, sure, deger, sonek="%", onek="", etiket="", vurgu=None, renk="#FFE600", top=420, boy=84, sayim=0.9, pid=None):
    """0 → deger sayımı (deterministik: zaman çizgisi tween'i), bitişte çarpma. Fiyat/para birimi yok (onek '$' kapıdan geçmez)."""
    pid = _id(pid, "say")
    sat = satirlar(etiket, vurgu)
    et_html, n = _kelimeler_html(pid, sat)
    ic = '<div class="sayi" id="%sn">%s0%s</div><div class="etk kk" style="font-size:%dpx">%s</div>' % (pid, onek, sonek, boy, et_html)
    _kap(pid, bas, sure, '<div class="tx say" style="top:%dpx;--vurgu:%s">%s</div>' % (top, renk, ic))
    b0 = _r(bas + 0.1)
    _t('var o%s={v:0};' % pid)
    _t('tl.to(o%s,{v:%s,duration:%s,ease:"power2.out",onUpdate:function(){document.getElementById("%sn").textContent="%s"+Math.round(o%s.v)+"%s";}},%s);' %
       (pid, deger, _r(sayim), pid, onek, pid, sonek, b0))
    son = _r(b0 + sayim)
    _t('tl.fromTo("#%sn",{scale:1.28},{scale:1,duration:0.4,ease:"elastic.out(1,0.5)"},%s);' % (pid, son))
    _pop(pid, n, bas, 0.1, 0 if n == 0 else 0)
    _cik(pid, bas, sure)
    OL.append({"t": son, "tur": "kanit", "ses": "ding", "sablon": "sayac"})


# ---------------------------------------------------------------- (g) tek kelime (TR06/TR04): kelime kelime, BÜYÜK HARF, sarı-beyaz, göğüs hizası
_OKK = '<svg class="kok" id="%sok" width="150" height="150" viewBox="0 0 24 24" fill="none" stroke="#E11D2E" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 4px 0 rgba(0,0,0,0.6));position:absolute;left:-10px;top:-170px"><path d="M4 4l15 15"/><path d="M19 8v11H8"/></svg>'


def tek_kelime(bas, sure, metin, adim=0.4, renkler=("#FFE600", "#FFFFFF"), top=820, boy=150, ok=False, dil="en", pid=None):
    """Ekranda tek kelime; sırayla değişir (sarı-beyaz dönüşümlü), BÜYÜK HARF, göğüs hizası (top 700–1000). Kelime ≥ 0,3 sn. ok=True: kırmızı ok."""
    pid = _id(pid, "tw")
    kel = [k for s_ in satirlar(metin) for k, _ in s_]
    n = len(kel)
    if adim < 0.3:
        raise SystemExit("HATA: tek_kelime adim %.2f < 0,30 sn (tek kelime okunma tabanı)" % adim)
    if n * adim > sure + 0.01:
        raise SystemExit("HATA: tek_kelime %d kelime × %.2f sn = %.2f sn > süre %.2f" % (n, adim, n * adim, sure))
    if float(bas) < 0.05 and n > KANCA_KELIME_MAX:
        raise SystemExit("HATA: kanca (%s) %d kelime; en çok %d" % (pid, n, KANCA_KELIME_MAX))
    if not 560 <= top <= 1100:
        raise SystemExit("HATA: tek_kelime top=%d göğüs hizası (560–1100) dışında" % top)
    maxc = max(len(k) for k in kel)
    boy = int(min(boy, 680 / (maxc * 0.70)))
    ws = "".join('<div class="tkw" id="%sw%d" style="font-size:%dpx;color:%s">%s</div>' % (pid, i, boy, renkler[i % len(renkler)], buyuk(k, dil)) for i, k in enumerate(kel))
    _kap(pid, bas, sure, '<div class="tx tw" style="top:%dpx;height:%dpx">%s%s</div>' % (top, int(boy * 1.3), ws, (_OKK % pid) if ok else ""))
    for i in range(n):
        t0 = _r(bas + i * adim)
        if i > 0:
            _t('tl.fromTo("#%sw%d",{opacity:0,scale:1.25},{opacity:1,scale:1,duration:0.09,ease:"power3.out"},%s);' % (pid, i, t0))
        else:
            _t('tl.fromTo("#%sw0",{scale:1.2},{scale:1,duration:0.1,ease:"power3.out"},%s);' % (pid, _r(bas)))
        if i + 1 < n:
            _t('tl.set("#%sw%d",{opacity:0},%s);' % (pid, i, _r(bas + (i + 1) * adim)))
        else:
            _t('tl.to("#%sw%d",{opacity:0,duration:0.12,ease:"power2.in"},%s);' % (pid, i, _r(bas + sure - 0.14)))
    for i in range(1, n):
        _t('tl.set("#%sw%d",{opacity:0},0);' % (pid, i))      # başlangıç durumu (fromTo ilk sırada olduğundan ayrıca)
    if ok:
        _t('tl.fromTo("#%sok",{x:0,y:0},{x:14,y:14,duration:0.3,ease:"sine.inOut",yoyo:true,repeat:%d},%s);' % (pid, max(1, int((sure - 0.2) / 0.3)), _r(bas + 0.2)))
    OL.append({"t": _r(bas), "tur": "yazi", "sablon": "tek_kelime"})


# ---------------------------------------------------------------- (h) küçük konuşma altyazısı + iki katman (TR04, AB01, AB04)
def altyazi(bas, sure, metin, top=1080, boy=48, renk="#FFFFFF", pid=None):
    """İkinci katman: küçük beyaz konuşma altyazısı (kanca yazısının altında). Alt güvenli alana (y ≥ 1500) girmez."""
    pid = _id(pid, "alt")
    sat = satirlar(metin)
    n_sat = max(1, int(sum(len(k) for s_ in sat for k, _ in s_) * boy * 0.6 / 740) + 1)
    if top + n_sat * boy * 1.25 > OKUMA_ALT:
        raise SystemExit("HATA: altyazi top=%d + %d satır alt sınıra (y≥%d) giriyor" % (top, n_sat, OKUMA_ALT))
    ic, n = _kelimeler_html(pid, [[(k, v) for k, v in s_] for s_ in sat])
    _kap(pid, bas, sure, '<div class="tx alty" style="top:%dpx;font-size:%dpx;--vurgu:%s;color:%s">%s</div>' % (top, boy, "#FFE600", renk, ic), track=6)
    _cik(pid, bas, sure)


def iki_katman(bas, sure, kanca, altyazi_ayar, pid="ik"):
    """Büyük kanca + küçük konuşma altyazısı birlikte. kanca: {"sablon": ..., ...}; altyazi_ayar: {"metin": ..., "top": ...}."""
    cfg = dict(kanca)
    ad = cfg.pop("sablon")
    if ad not in SABLON:
        raise SystemExit("HATA: iki_katman bilinmeyen şablon %r" % ad)
    SABLON[ad](bas=bas, sure=sure, pid=pid + "k", **cfg)
    altyazi(bas=bas, sure=sure, pid=pid + "a", **dict(altyazi_ayar))


# ---------------------------------------------------------------- (i) pazar son kartı: mağaza teklif rozeti · AB indirim/kargo rozeti + düğme · ABD Comment/LINK IN BIO
def son_kart(bas, sure, pazar, rozet="", ikinci="", dugme="", anahtar="", top=900, pid=None):
    """TR/DE/AB: kırmızı rozet = mağazanın GERÇEK teklifi (rozet=…; ör. "ÜCRETSİZ KARGO", "KAPIDA ÖDEME" yalnız mağaza sunuyorsa). Varsayılan YOK. DE/AB: kırmızı teklif rozeti (rozet=… doğrulanmış teklif), `ikinci` (ör. kargo) ve düğme.
    ABD: anahtar varsa Comment “X” rozeti, yoksa LINK IN BIO. Metinleri çağıran verir (indirim/fiyat metni = doğrulanmış iddia; hikâye hattında fiyat_izin ister)."""
    pid = _id(pid, "sk")
    pz = str(pazar).upper()
    if pz not in ("TR", "DE", "AB", "US"):
        raise SystemExit("HATA: son_kart pazar %r (TR | DE | AB | US)" % pazar)
    if pz == "US" and anahtar:
        return cta_rozet(bas, sure, anahtar, top=min(top, 1170), pid=pid)
    parcalar, yukseklik = [], 0
    if pz == "US":
        parcalar.append('<div class="skr link" id="%sr">LINK IN BIO</div>' % pid)
        yukseklik += 140
    else:
        r = rozet
        if not r:
            raise SystemExit("HATA: son_kart %s için rozet metni gerekli: mağazanın gerçek teklifi (ayar.json); referans rozetini kopyalama" % pz)
        parcalar.append('<div class="skr" id="%sr">%s</div>' % (pid, r))
        yukseklik += 150
    if ikinci:
        parcalar.append('<div class="ski" id="%si">%s</div>' % (pid, ikinci))
        yukseklik += 100
    if dugme:
        parcalar.append('<div class="skd" id="%sd">%s</div>' % (pid, dugme))
        yukseklik += 130
    if top + yukseklik > OKUMA_ALT:
        raise SystemExit("HATA: son_kart top=%d + yükseklik %d alt sınıra (y≥%d) giriyor" % (top, yukseklik, OKUMA_ALT))
    _kap(pid, bas, sure, '<div class="tx sk" style="top:%dpx">%s</div>' % (top, "".join(parcalar)), track=5)
    _t('tl.fromTo("#%sr",{opacity:0,scale:0.5,y:30},{opacity:1,scale:1,y:0,duration:0.28,ease:"back.out(2)"},%s);' % (pid, _r(bas)))
    if ikinci:
        _t('tl.fromTo("#%si",{opacity:0,x:-60},{opacity:1,x:0,duration:0.25,ease:"power3.out"},%s);' % (pid, _r(bas + 0.22)))
    if dugme:
        _t('tl.fromTo("#%sd",{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.28,ease:"back.out(2)"},%s);' % (pid, _r(bas + 0.45)))
        _t('tl.to("#%sd",{scale:1.07,duration:0.4,ease:"sine.inOut",yoyo:true,repeat:%d},%s);' % (pid, max(1, int((sure - 0.9) / 0.4)), _r(bas + 0.8)))
    _cik(pid, bas, sure)
    OL.append({"t": _r(bas), "tur": "cta"})


# ---------------------------------------------------------------- (j) dev fiyat/indirim vuruşu (AB04 "−23€")
def dev_fiyat(bas, sure, metin, renk="#E11D2E", top=380, boy=260, cikartma="", pid=None):
    """Dev kırmızı vuruş (beyaz kontur): çarpar (2,2×→1×) + sarsıntı; isteğe bağlı pembe yuvarlak çıkartma (cikartma='−15%'). Metin doğrulanmış tekliftir."""
    pid = _id(pid, "df")
    boy = int(min(boy, 740 / (len(metin) * 0.66)))
    ck = '<div class="cikartma" id="%sc" data-layout-allow-overlap>%s</div>' % (pid, cikartma) if cikartma else ""
    _kap(pid, bas, sure, '<div class="tx df" style="top:%dpx;--vurgu:%s"><div class="dev" id="%sd" style="font-size:%dpx" data-layout-allow-overlap>%s</div>%s</div>' % (top, renk, pid, boy, metin, ck))
    _t('tl.fromTo("#%sd",{opacity:0,scale:2.2},{opacity:1,scale:1,duration:0.2,ease:"power4.in"},%s);' % (pid, _r(bas)))
    _t('tl.fromTo("#%sd",{x:0},{keyframes:[{x:-12,duration:0.035},{x:12,duration:0.035},{x:-6,duration:0.035},{x:0,duration:0.035}]},%s);' % (pid, _r(bas + 0.2)))
    if cikartma:
        _t('tl.fromTo("#%sc",{opacity:0,scale:0.3,rotation:-30},{opacity:1,scale:1,rotation:-12,duration:0.3,ease:"back.out(2.4)"},%s);' % (pid, _r(bas + 0.3)))
    _cik(pid, bas, sure)
    OL.append({"t": _r(bas + 0.2), "tur": "sok"})


# ---------------------------------------------------------------- (k) ikili kıyas çerçevesi (R1) + deneme sayacı (R2) — uzman yöntemi (R74)
_TIK = ('<svg class="iktik" id="%sT" width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="3.4" stroke-linecap="round" '
        'stroke-linejoin="round" style="position:absolute;left:%dpx;top:640px;filter:drop-shadow(0 6px 0 rgba(0,0,0,0.6));opacity:0"><circle cx="12" cy="12" r="10" fill="rgba(0,0,0,0.55)"/>'
        '<path d="M7 12.5l3.2 3.2L17 8.8"/></svg>')
IK_ETIKET_TOP = 1120       # etiket rozetleri (yükseklik ~90 px) y ≤ 1330 bandında biter
IK_MERKEZ = {"sol": 270, "sag": 810}


IK_SORU_BOY, IK_SORU_GENISLIK = 116, 820   # soru kutusu: telefonda okunur (eski: tek satır ≈ 42 px); 2 satıra bölününce yazı büyür


def _soru_bol(soru):
    """Tek cümleyi (≥ 3 kelime) karakter sayısı dengeli 2 satıra böler ("a b / c d"); kısa soru tek satır kalır. Sigdir satır başına sığdırır → yazı ~2× büyür."""
    k = str(soru).split()
    if len(k) < 3:
        return str(soru)
    en = min(range(1, len(k)), key=lambda i: max(len(" ".join(k[:i])), len(" ".join(k[i:]))))
    return " ".join(k[:en]) + " / " + " ".join(k[en:])


def ikili_kiyas(bas, sure, soru, sol_etiket, sag_etiket, kazanan=None, cevap_an=None, renk="#FFE600", top=300, pid=None, boy=IK_SORU_BOY):
    """R1 (uzman yöntemi, R74): dikey bölünmüş ekran ÇERÇEVESİ. İki video alanı (sol/sağ 540 px) çağıranın klibidir; burada yalnız orta çizgi, iki etiket rozeti
    ve üstte TEK soru kutusu var. kazanan='sol'|'sag' verilirse `cevap_an`da (mutlak sn; varsayılan bas + sure×0,7) kazanan tarafa tik + diğer tarafa hafif karartma.
    Soru tek soru olmalı: tek '?' ve ≤ 7 kelime. Kıyas sonucu GERÇEK çekimle gösterilir (kazananı uydurma)."""
    pid = _id(pid, "ikk")
    sat = satirlar(soru)
    if str(soru).count("?") != 1:
        raise SystemExit("HATA: ikili_kiyas tek soru ister (tam bir '?'): %r" % soru)
    if "/" in str(soru) or kelime_sayisi(sat) > KANCA_KELIME_MAX:
        raise SystemExit("HATA: ikili_kiyas soru tek cümle ('/' ile satır kırma; 2 satıra kendisi bölünür) ve ≤ %d kelime olmalı" % KANCA_KELIME_MAX)
    if not (str(sol_etiket).strip() and str(sag_etiket).strip()):
        raise SystemExit("HATA: ikili_kiyas iki etiket de gerekli (sol_etiket, sag_etiket)")
    if kazanan not in (None, "sol", "sag"):
        raise SystemExit("HATA: ikili_kiyas kazanan 'sol' | 'sag' | None (verilen %r)" % kazanan)
    if top < GUVENLI_UST:
        raise SystemExit("HATA: ikili_kiyas top=%d üst güvenli alana (y<%d) giriyor" % (top, GUVENLI_UST))
    ca = float(bas) + float(sure) * 0.7 if cevap_an is None else float(cevap_an)
    if kazanan and not (float(bas) < ca < float(bas) + float(sure)):
        raise SystemExit("HATA: ikili_kiyas cevap_an %.2f yayın aralığının (%.2f–%.2f) dışında" % (ca, float(bas), float(bas) + float(sure)))
    ig_kutu(bas, sure, _soru_bol(soru), vurgu_stil="renk", renk=renk, top=top, boy=boy, genislik=IK_SORU_GENISLIK, pid=pid + "q")
    parcalar = ['<div class="bolen" id="%sb"></div>' % pid]
    for yon, e in (("sol", sol_etiket), ("sag", sag_etiket)):
        boy = int(min(44, 250 / (len(str(e)) * 0.7)))
        parcalar.append('<div class="ikes %s" id="%s%s" style="top:%dpx;font-size:%dpx">%s</div>' % (yon, pid, yon, IK_ETIKET_TOP, boy, e))
    if kazanan:
        kaybeden = "sag" if kazanan == "sol" else "sol"
        parcalar.append('<div class="ikdim %s" id="%sdim"></div>' % (kaybeden, pid))
        parcalar.append(_TIK % (pid, IK_MERKEZ[kazanan] - 110))
    _kap(pid, bas, sure, '<div class="tx ikf">%s</div>' % "".join(parcalar), track=5)
    for yon in ("sol", "sag"):
        _t('tl.fromTo("#%s%s",{opacity:0,y:20},{opacity:1,y:0,duration:0.22,ease:"back.out(1.8)"},%s);' % (pid, yon, _r(bas + 0.1)))
    if kazanan:
        _t('tl.fromTo("#%sdim",{opacity:0},{opacity:1,duration:0.3,ease:"power2.out"},%s);' % (pid, _r(ca)))
        _t('tl.fromTo("#%sT",{opacity:0,scale:0.3},{opacity:1,scale:1,duration:0.3,ease:"back.out(2.4)"},%s);' % (pid, _r(ca)))
        OL.append({"t": _r(ca), "tur": "kanit", "ses": "ding", "sablon": "ikili_kiyas"})
    _cik(pid, bas, sure)
    OL.append({"t": _r(bas), "tur": "yazi", "sablon": "ikili_kiyas"})


def deneme_sayaci(bas, sure, toplam, adimlar, kural="3 leke. Tek silme.", renk="#FFE600", top_kural=300, top_sayac=520, pid=None):
    """R2 (uzman yöntemi, R74): konuşmasız tek kurallı test. Üstte tek satır kural, altında '0/N' sayaç; `adimlar` = N adet MUTLAK saniye (artan,
    bas'tan sonra, bitişten önce): her adımda sayaç k/N'e atlar, sonuncuda yeşile döner. Adım zamanları gerçek çekimdeki sonuç anlarına bağlanır (uydurma ilerleme yok).
    Sayaç durumları üst üste duran ayrı öğelerdir (deterministik: tween seek'te yeniden kurulur)."""
    pid = _id(pid, "dsy")
    toplam = int(toplam)
    adimlar = [float(a) for a in (adimlar or [])]
    if not 2 <= toplam <= 10:
        raise SystemExit("HATA: deneme_sayaci toplam 2–10 olmalı (verilen %r)" % toplam)
    if len(adimlar) != toplam:
        raise SystemExit("HATA: deneme_sayaci %d adım zamanı ister, %d verildi" % (toplam, len(adimlar)))
    if any(b <= a for a, b in zip(adimlar, adimlar[1:])):
        raise SystemExit("HATA: deneme_sayaci adım zamanları artan olmalı: %s" % adimlar)
    if adimlar[0] <= float(bas) or adimlar[-1] >= float(bas) + float(sure):
        raise SystemExit("HATA: deneme_sayaci adımlar (%.2f–%.2f) yayın aralığının (%.2f–%.2f) içinde olmalı" % (adimlar[0], adimlar[-1], float(bas), float(bas) + float(sure)))
    sat = satirlar(kural)
    if "/" in str(kural) or kelime_sayisi(sat) > KANCA_KELIME_MAX:
        raise SystemExit("HATA: deneme_sayaci kural tek satır ve ≤ %d kelime olmalı" % KANCA_KELIME_MAX)
    if top_kural < GUVENLI_UST or top_sayac + 300 > OKUMA_ALT:
        raise SystemExit("HATA: deneme_sayaci konum güvenli alanın dışında (top_kural≥%d, top_sayac+300≤%d)" % (GUVENLI_UST, OKUMA_ALT))
    ig_kutu(bas, sure, kural, vurgu_stil="renk", renk=renk, top=top_kural, pid=pid + "k")
    ds = []
    for k in range(toplam + 1):
        ds.append('<span class="dsd" id="%ss%d"%s>%d/%d</span>' % (pid, k, "" if k == 0 else ' style="opacity:0"', k, toplam))
    _kap(pid, bas, sure, '<div class="tx say dsy" style="top:%dpx;--vurgu:%s"><div class="sayi">%s</div></div>' % (top_sayac, renk, "".join(ds)), track=5)
    for k, t in enumerate(adimlar, start=1):
        _t('tl.set("#%ss%d",{opacity:0},%s);' % (pid, k - 1, _r(t)))
        _t('tl.fromTo("#%ss%d",{opacity:0,scale:1.35},{opacity:1,scale:1,duration:0.28,ease:"back.out(2.2)"},%s);' % (pid, k, _r(t)))
        OL.append({"t": _r(t), "tur": "kanit", "ses": "ding", "sablon": "deneme_sayaci"})
    _t('tl.set("#%ss%d",{color:"#22C55E"},%s);' % (pid, toplam, _r(adimlar[-1])))
    _cik(pid, bas, sure)


# ---------------------------------------------------------------- geçiş + kapanış (ürün çapraz geçişi · dip · logo/marka kapanışı)
VARLIK = []                    # (kaynak yol, hedef ad): varliklari_kopyala(klasor) assets/img/ altına kopyalar
VARLIK_UZANTI = (".png", ".jpg", ".jpeg", ".webp", ".svg")
UG_BG = "radial-gradient(ellipse 90% 60% at 50% 62%, #1d2b4f 0%, #0e1530 55%, #070b1a 100%)"


def _varlik(yol, ad):
    """Görsel/logo dosyasını doğrular, kopyalanacaklar listesine yazar, HTML'de kullanılacak göreli yolu döndürür."""
    if not yol or not os.path.isfile(str(yol)):
        raise SystemExit("HATA: %s dosyası bulunamadı: %r (yolu kontrol et; dosya depoya konmaz, çağıran verir)" % (ad, yol))
    if not str(yol).lower().endswith(VARLIK_UZANTI):
        raise SystemExit("HATA: %s uzantısı desteklenmiyor: %r (izinli: %s)" % (ad, yol, ", ".join(VARLIK_UZANTI)))
    kaynak, hedef = os.path.abspath(str(yol)), os.path.basename(str(yol))
    for k, h in VARLIK:
        if h == hedef and k != kaynak:
            raise SystemExit("HATA: %s için aynı ada sahip farklı dosya zaten kullanılıyor: %r" % (ad, hedef))
    if (kaynak, hedef) not in VARLIK:
        VARLIK.append((kaynak, hedef))
    return "assets/img/" + hedef


def varliklari_kopyala(klasor):
    """urun_gecisi/kapanis görsellerini <klasor>/assets/img/ altına kopyalar (zaten oradaysa dokunmaz)."""
    import shutil
    hedef_k = os.path.join(klasor, "assets", "img")
    os.makedirs(hedef_k, exist_ok=True)
    for kaynak, ad in VARLIK:
        h = os.path.join(hedef_k, ad)
        if not (os.path.exists(h) and os.path.samefile(kaynak, h)):
            shutil.copy2(kaynak, h)


def _esc(x):
    return (str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def urun_gecisi(bas, sure, gorsel=None, kick="", ust1="", ust2="", alt="", gecis=0.7, w=570, ust=640, top_yazi=300, alt_top=1180,
                bg=UG_BG, boy1=104, boy2=120, renk="#FFE600", pid=None):
    """Ürün sahnesi `gecis` (0,7) sn çapraz geçişle girer: önceki klibin son `gecis` sn'si üstüne opacity 0→1, ilk 1 sn scale 1.06→1,0 + parlaklık 0,6→1;
    yazılar geçişten 0,3 sn sonra opacity+y ile yumuşak girer. `bas` = ürünün oturduğu an (ritim/drop); sahne bas−gecis'te başlar → bas ≥ gecis olmalı
    (GSAP'e negatif konum verilmez). gorsel: ürün PNG/JPG/SVG yolu (None → yalnız zemin + yazı). Tek yazı katmanı: kick · ust1 · ust2 (vurgu rengi) · alt."""
    pid = _id(pid, "ug")
    bas, sure, gecis = float(bas), float(sure), float(gecis)
    if not 0.2 <= gecis <= 1.5:
        raise SystemExit("HATA: urun_gecisi gecis 0,2–1,5 sn olmalı (verilen %r)" % gecis)
    if bas < gecis:
        raise SystemExit("HATA: urun_gecisi bas=%.2f < gecis=%.2f: çapraz geçiş önceki klibin son %.2f sn'si üstüne biner, başlangıç negatif olamaz" % (bas, gecis, gecis))
    if sure < 1.6:
        raise SystemExit("HATA: urun_gecisi sure ≥ 1,6 sn olmalı (ürün girişi 1,2 sn + alt satır; verilen %.2f)" % sure)
    if top_yazi < GUVENLI_UST or alt_top + 90 > OKUMA_ALT:
        raise SystemExit("HATA: urun_gecisi yazı konumu güvenli alanın dışında (top_yazi≥%d, alt_top+90≤%d)" % (GUVENLI_UST, OKUMA_ALT))
    src = _varlik(gorsel, "urun_gecisi görseli") if gorsel else None
    e, sd = _r(bas - gecis), _r(sure + gecis)
    img = ('<div class="ugu" id="%su" style="left:%dpx;top:%dpx;width:%dpx"><img src="%s" alt="" style="width:%dpx"></div>' % (pid, (1080 - int(w)) // 2, int(ust), int(w), src, int(w))) if src else ""
    P.append('<div id="%s" class="clip" data-start="%s" data-duration="%s" data-track-index="3"><div class="ugw" id="%sw"><div class="ugbg" style="background:%s"></div>%s</div></div>' % (pid, e, sd, pid, bg, img))
    _t('tl.to("#%sw",{opacity:1,duration:%s,ease:"sine.inOut"},%s);' % (pid, _r(gecis), e))
    _t('tl.fromTo("#%sw",{scale:1.06},{scale:1,duration:1.0,ease:"power2.out"},%s);' % (pid, e))
    _t('tl.fromTo("#%sw",{filter:"brightness(0.6)"},{filter:"brightness(1)",duration:1.0,ease:"sine.out"},%s);' % (pid, e))
    if src:
        _t('tl.fromTo("#%su",{y:420,scale:0.94,rotation:5},{y:0,scale:1,rotation:0,duration:1.2,ease:"expo.out"},%s);' % (pid, _r(bas)))
        _t('tl.to("#%su",{y:-26,rotation:-2.5,scale:1.04,duration:%s,ease:"sine.inOut"},%s);' % (pid, _r(sure - 1.2), _r(bas + 1.2)))
    y = []
    if kick:
        y.append('<div class="ugk" id="%sk" style="top:%dpx;--vurgu:%s">%s</div>' % (pid, int(top_yazi), renk, _esc(kick)))
    if ust1 or ust2:
        sat = []
        for ad, yazi, b in (("a", ust1, boy1), ("b", ust2, boy2)):
            if yazi:
                kel = "".join('<span class="w%s">%s</span> ' % (" v" if ad == "b" else "", _esc(k)) for k in str(yazi).split())
                sat.append('<div class="ugs" style="font-size:%dpx">%s</div>' % (int(b), kel))
        y.append('<div class="ugust" id="%sy" style="top:%dpx;--vurgu:%s">%s</div>' % (pid, int(top_yazi) + 70, renk, "".join(sat)))
    if alt:
        y.append('<div class="uga" id="%sa" style="top:%dpx">%s</div>' % (pid, int(alt_top), _esc(alt)))
    if y:
        P.append('<div id="%sx" class="clip ugy" data-start="%s" data-duration="%s" data-track-index="4">%s</div>' % (pid, e, sd, "".join(y)))
        if kick:
            _t('tl.fromTo("#%sk",{opacity:0,y:-14},{opacity:1,y:0,duration:0.5,ease:"power2.out"},%s);' % (pid, _r(e + 0.3)))
        if ust1 or ust2:
            _t('tl.fromTo("#%sy .w",{opacity:0,y:18},{opacity:1,y:0,duration:0.5,stagger:0.13,ease:"power2.out"},%s);' % (pid, _r(e + 0.45)))
        if alt:
            _t('tl.fromTo("#%sa",{opacity:0,y:20},{opacity:1,y:0,duration:0.45,ease:"power2.out"},%s);' % (pid, _r(bas + 1.4)))
        _t('tl.to("#%sx",{opacity:0,duration:0.15},%s);' % (pid, _r(bas + sure - 0.15)))
        OL.append({"t": _r(e + 0.3), "tur": "yazi", "sablon": "urun_gecisi"})


def dip_gecis(z, once=0.35, ac=0.6, yogunluk=0.7, renk="#000000", pid=None):
    """Sert kesmeyi yumuşatır (ürünsüz videoda sahne→sahne): kesim z'den `once` (0,35) sn ÖNCE kararma 0→yogunluk, z'den sonra `ac` (0,6) sn'de açılış.
    z ≥ once olmalı (GSAP'e negatif konum verilmez). Yazı katmanı yok."""
    z, once, ac = float(z), float(once), float(ac)
    pid = _id(pid, "dip")
    if not 0.0 < yogunluk <= 1.0:
        raise SystemExit("HATA: dip_gecis yogunluk 0–1 arası olmalı (verilen %r)" % yogunluk)
    if once <= 0 or ac <= 0:
        raise SystemExit("HATA: dip_gecis once ve ac > 0 olmalı")
    if z < once:
        raise SystemExit("HATA: dip_gecis kesim z=%.2f < once=%.2f: kararma başlangıcı negatif olamaz" % (z, once))
    bas = _r(z - once)
    P.append('<div id="%s" class="clip" data-start="%s" data-duration="%s" data-track-index="8"><div class="dipi" id="%si" style="background:%s"></div></div>' % (pid, bas, _r(once + ac + 0.05), pid, renk))
    _t('tl.fromTo("#%si",{opacity:0},{opacity:%s,duration:%s,ease:"sine.in"},%s);' % (pid, _r(yogunluk), _r(once), bas))
    _t('tl.to("#%si",{opacity:0,duration:%s,ease:"sine.out"},%s);' % (pid, _r(ac), _r(z)))


KAPANIS_FADE, KAPANIS_FADE_YUMUSAK = 0.8, 1.4


def kapanis(bas, sure, logo, marka, alt_satir="", yazi="", yumusak=0, kapan_sn=None, top_yazi=300, top_logo=640, logo_boy=300, zemin="#07080d", pid=None):
    """Kapanış: [yazi (isteğe bağlı tek satır CTA)] + logo (daire maske, fade+scale 0,82→1) + marka adı + alt satır; son `kapan_sn` (0,8; yumusak ise 1,4) sn siyaha fade.
    En çok 2 yazı katmanı (CTA + marka/alt satır); logo görsel katmandır. Süre sonu = bas+sure. logo: PNG/JPG/SVG yolu (çağıran verir, depoya girmez).
    yumusak: px; >0 → logo ve alt satıra hafif odak yumuşatma (düz/karanlık sahneden sonra görüntü-gürültü kapısı için) + uzun (1,4 sn) kararma."""
    pid = _id(pid, "kp")
    bas, sure, yumusak = float(bas), float(sure), float(yumusak)
    kapan = (KAPANIS_FADE_YUMUSAK if yumusak > 0 else KAPANIS_FADE) if kapan_sn is None else float(kapan_sn)
    if not str(marka).strip():
        raise SystemExit("HATA: kapanis marka adı boş olamaz")
    src = _varlik(logo, "kapanis logosu")
    if bas < 0 or sure - kapan < 1.7:
        raise SystemExit("HATA: kapanis sure=%.2f çok kısa: logo girişi + %.1f sn kararma için en az %.1f sn gerekir" % (sure, kapan, 1.7 + kapan))
    sat = satirlar(yazi) if yazi else []
    if sat:
        kanca_kapisi(sat, 0.0, pid)   # CTA da ≤ 2 satır / ≤ 7 kelime
    if top_yazi < GUVENLI_UST or top_logo + logo_boy + 250 > OKUMA_ALT:
        raise SystemExit("HATA: kapanis konum güvenli alanın dışında (top_yazi≥%d, top_logo+logo_boy+250≤%d)" % (GUVENLI_UST, OKUMA_ALT))
    bit = _r(bas + sure)
    # zemin (logoyu taşıyan koyu perde) + logo disk
    P.append('<div id="%sz" class="clip" data-start="%s" data-duration="%s" data-track-index="3"><div class="kpz" id="%szi" style="background:%s"></div></div>' % (pid, _r(bas), _r(sure), pid, zemin))
    _t('tl.fromTo("#%szi",{opacity:0},{opacity:1,duration:0.7,ease:"sine.inOut"},%s);' % (pid, _r(bas)))
    if sat:
        ic, _n = _kelimeler_html(pid + "c", sat)
        P.append('<div id="%sc" class="clip" data-start="%s" data-duration="%s" data-track-index="5"><div class="kpy kpc" style="top:%dpx;font-size:%dpx">%s</div></div>'
                 % (pid, _r(bas), _r(sure), int(top_yazi), sigdir(sat, 96, ek_em=0.6, genislik=780), ic))
        _t('tl.fromTo("#%sc .w",{opacity:0,filter:"blur(6px)",y:14},{opacity:1,filter:"blur(0px)",y:0,duration:0.2,stagger:0.06,ease:"power2.out"},%s);' % (pid, _r(bas + 0.02)))
    P.append('<div id="%sl" class="clip" data-start="%s" data-duration="%s" data-track-index="6"><div class="kpl" id="%sld" style="top:%dpx;width:%dpx;height:%dpx;margin-left:%dpx;background-image:url(%s)"></div></div>'
             % (pid, _r(bas + 0.5), _r(sure - 0.5), pid, int(top_logo), int(logo_boy), int(logo_boy), -int(logo_boy) // 2, src))
    ty = int(top_logo + logo_boy + 40)
    P.append('<div id="%sm" class="clip" data-start="%s" data-duration="%s" data-track-index="7"><div class="kpy kpm" style="top:%dpx"><div class="kpa" id="%sa">%s</div>%s</div></div>'
             % (pid, _r(bas + 0.5), _r(sure - 0.5), ty, pid, _esc(marka), ('<div class="kpb" id="%sb">%s</div>' % (pid, _esc(alt_satir))) if alt_satir else ""))
    if yumusak > 0:
        _t('tl.set("#%sld%s",{filter:"blur(%spx)"},0);' % (pid, (", #%sb" % pid) if alt_satir else "", _r(yumusak)))
    _t('tl.fromTo("#%sld",{opacity:0,scale:0.82},{opacity:1,scale:1,duration:0.7,ease:"power2.out"},%s);' % (pid, _r(bas + 0.5)))
    _t('tl.fromTo("#%sa",{opacity:0,y:16},{opacity:1,y:0,duration:0.6,ease:"power2.out"},%s);' % (pid, _r(bas + 0.75)))
    if alt_satir:
        _t('tl.fromTo("#%sb",{opacity:0,y:12},{opacity:1,y:0,duration:0.6,ease:"power2.out"},%s);' % (pid, _r(bas + 0.95)))
    # son siyaha fade (en üst katman)
    P.append('<div id="%sk" class="clip" data-start="%s" data-duration="%s" data-track-index="10"><div class="kpk" id="%ski"></div></div>' % (pid, _r(bit - kapan), _r(kapan), pid))
    _t('tl.fromTo("#%ski",{opacity:0},{opacity:1,duration:%s,ease:"sine.in"},%s);' % (pid, _r(kapan), _r(bit - kapan)))


# ---------------------------------------------------------------- kanca ↔ CTA dönüşümlü
SABLON = {"ig_kutu": ig_kutu, "kalin_kontur": kalin_kontur, "karaoke": karaoke, "tepki": tepki, "cta_rozet": cta_rozet, "sayac": sayac,
          "uzman_kutu": uzman_kutu, "tek_kelime": tek_kelime, "altyazi": altyazi, "son_kart": son_kart, "dev_fiyat": dev_fiyat,
          "ikili_kiyas": ikili_kiyas, "deneme_sayaci": deneme_sayaci}


def donusum(pencereler, kanca, cta, pid="dn", bas=None, sure=None):
    """Ekranda kanca yazısı ile CTA sırayla değişir (saha K15). pencereler: [[bas, bit], ...]; çift sıra kanca, tek sıra CTA.
    kanca/cta: {"sablon": "ig_kutu", ...şablon parametreleri (bas/sure hariç)}. İlk pencere bas=0 olmalı (kanca ilk karede)."""
    if not pencereler or float(pencereler[0][0]) > 0.05:
        raise SystemExit("HATA: donusum ilk pencere 0. saniyede başlamalı (kanca ilk karede)")
    for k, (a, b) in enumerate(pencereler):
        cfg = dict(kanca if k % 2 == 0 else cta)
        ad = cfg.pop("sablon")
        if ad not in SABLON:
            raise SystemExit("HATA: donusum bilinmeyen şablon %r (izinli: %s)" % (ad, ", ".join(SABLON)))
        cfg["pid"] = "%s%d" % (pid, k)
        SABLON[ad](bas=a, sure=_r(b - a), **cfg)


def ust_perde(sure):
    P.append('<div id="ustperde" class="clip" data-start="0" data-duration="%s" data-track-index="2"><div class="ustperde"></div></div>' % _r(sure))


# ---------------------------------------------------------------- klip katmanı: geçişler, bölünmüş ekran, donmuş kare, yakın çekim
GECIS_OV = {"whip": 0.16, "punch": 0.0, "kesim": 0.0}


def _vid(id_, dosya, bas, sure, stil=""):
    return ('<video id="%s" class="clip vid" src="assets/video/%s" data-start="%s" data-duration="%s" data-media-start="0" data-track-index="0" muted playsinline%s></video>'
            % (id_, dosya, _r(bas), _r(sure), (' style="%s"' % stil) if stil else ""))


def klipler(plan, t_, gecisler, sure):
    """plan: [{i, tur: klip|bolunmus|donuk, dosya, dosya2?, etiket1?, etiket2?, z0?, z1?, hiz?}] kesim aralığı i → t_[i]..t_[i+1].
    gecisler[k]: k. kesimde (klip k-1 → k) geçiş: whip | punch | kesim. Yan etki: P/T/OL doldurur."""
    plan = sorted(plan, key=lambda p: p["i"])
    for sira, p in enumerate(plan):
        i = p["i"]
        bas, bit = t_[i], t_[i + 1]
        g = gecisler[i - 1] if i >= 1 and i - 1 < len(gecisler) else "kesim"
        ov = GECIS_OV.get(g, 0.0) if i >= 1 else 0.0
        s0, d0 = bas - ov, (bit - bas) + ov
        vid_id = "a%d" % i
        z0 = p.get("z0", 1.0 if i % 2 == 0 else 1.06)
        z1 = p.get("z1", 1.07 if i % 2 == 0 else 1.0)
        if p.get("tur") == "bolunmus":
            ic = ('<div class="yarim sol">%s</div><div class="yarim sag">%s</div>' %
                  (_vid(vid_id + "L", "a%d.mp4" % i, s0, d0), _vid(vid_id + "R", "a%db.mp4" % i, s0, d0)))
            P.append('<div class="tr" id="%str" data-layout-allow-overflow style="z-index:%d"><div class="cam" id="%scam" data-layout-allow-overflow>%s</div></div>' % (vid_id, 10 + sira, vid_id, ic))
            P.append('<div id="%sbolen" class="clip" data-start="%s" data-duration="%s" data-track-index="3" style="z-index:30"><div class="bolen"></div></div>' % (vid_id, _r(bas), _r(bit - bas)))
            for yon, e in (("sol", p.get("etiket1", "")), ("sag", p.get("etiket2", ""))):
                if e:
                    eid = "%s%s" % (vid_id, yon)
                    P.append('<div id="%s" class="clip" data-start="%s" data-duration="%s" data-track-index="6"><div class="etik %s" id="%si">%s</div></div>' % (eid, _r(bas + 0.1), _r(bit - bas - 0.1), yon, eid, e))
                    _t('tl.fromTo("#%si",{opacity:0,y:20},{opacity:1,y:0,duration:0.22,ease:"back.out(1.8)"},%s);' % (eid, _r(bas + 0.1)))
        else:
            P.append('<div class="tr" id="%str" data-layout-allow-overflow style="z-index:%d"><div class="cam" id="%scam" data-layout-allow-overflow>%s</div></div>' % (vid_id, 10 + sira, vid_id, _vid(vid_id, "a%d.mp4" % i, s0, d0)))
        _t('tl.fromTo("#%scam",{scale:%s},{scale:%s,duration:%s,ease:"none"},%s);' % (vid_id, z0, z1, _r(d0), _r(s0)))
        if p.get("tur") == "donuk":
            P.append('<div id="%shalka" class="clip" data-start="%s" data-duration="%s" data-track-index="3"><div class="sorunhalka" id="%shi"></div></div>' % (vid_id, _r(bas), _r(bit - bas), vid_id))
            _t('tl.fromTo("#%shi",{opacity:0},{opacity:1,duration:0.25,ease:"power2.out"},%s);' % (vid_id, _r(bas)))
        # geçiş hareketi: giren klip (bu klip) ve çıkan klip (bir önceki)
        if i >= 1:
            onceki = "a%d" % (plan[sira - 1]["i"]) if sira > 0 else None
            if g == "whip" and onceki:
                _t('tl.to("#%str",{x:-950,scale:1.08,duration:%s,ease:"power3.in"},%s);' % (onceki, _r(ov), _r(bas - ov)))
                _t('tl.fromTo("#%str",{x:950,scale:1.08},{x:0,scale:1,duration:%s,ease:"power3.out"},%s);' % (vid_id, _r(ov + 0.06), _r(bas - ov)))
                P.append('<div id="sk%d" class="clip streak" data-start="%s" data-duration="%s" data-track-index="7"><div class="sk" id="sk%di"></div></div>' % (i, _r(bas - ov), _r(ov + 0.1), i))
                _t('tl.fromTo("#sk%di",{x:1200,opacity:0.9},{x:-1200,opacity:0,duration:%s,ease:"power2.inOut"},%s);' % (i, _r(ov + 0.08), _r(bas - ov)))
                OL.append({"t": _r(bas - ov), "tur": "kesme", "tip": "whip"})
            elif g == "punch" and onceki:
                _t('tl.to("#%str",{scale:1.22,duration:0.12,ease:"power2.in"},%s);' % (onceki, _r(bas - 0.12)))
                _t('tl.fromTo("#%str",{scale:1.22},{scale:1,duration:0.28,ease:"expo.out"},%s);' % (vid_id, _r(bas)))
                OL.append({"t": _r(bas - 0.12), "tur": "kesme", "tip": "punch"})
    return sorted(OL, key=lambda o: o["t"])


def olaylari_yaz(klasor, drop=None):
    with open(os.path.join(klasor, "olaylar.json"), "w", encoding="utf-8") as f:
        json.dump({"olaylar": sorted(OL, key=lambda o: o["t"]), "drop": drop}, f, ensure_ascii=False, indent=1)


TURLER = dict(SABLON, donusum=donusum, iki_katman=iki_katman, urun_gecisi=urun_gecisi, dip_gecis=dip_gecis, kapanis=kapanis)
