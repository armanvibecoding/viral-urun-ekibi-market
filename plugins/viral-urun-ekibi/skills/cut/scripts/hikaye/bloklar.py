"""Hikâye hattı blokları: kinetik tipografi sahneleri (HyperFrames HTML + GSAP zaman çizgisi).
Her fonksiyon P (HTML) ve T (GSAP) listelerine ekler; sahne() ayar JSON'undaki bir sahneyi çağırır."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import hazirla, vid, yaz, tema_css  # noqa: E402,F401

P, T = [], []
t = T.append
STIL = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stil.css"), encoding="utf-8").read()


def sifirla():
    del P[:]
    del T[:]


def W(s, cls=""):
    """'a b *c*' → kelime span'ları; *x* = metal italik."""
    o = []
    for k in s.split(" "):
        if k == "/": o.append("<br>"); continue
        m = k.startswith("*") and k.endswith("*")
        k = k.strip("*").replace("_", " ")
        o.append(f'<span class="w {"metal it " if m else ""}{cls}">{k}</span>')
    return " ".join(o)
def klipler(PLAN):
    for pid, f, bas, sure, z0, z1, org in PLAN:
        p, tt = vid(pid, f, bas, sure, z0, z1, org); P.append(p); t(tt)
def perde(bas, sure, pid):
    P.append(f'<div id="{pid}" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="1"><div class="perdei"></div><div class="altperde"></div></div>')
def kanca(bas, sure, ust, buyuk, kick="", boy=218, top=480, pid="kanca", boyust=84):
    kk = f'<div class="kick kanca-kick" id="{pid}k" style="top:{top-88}px">{kick}</div>' if kick else ""
    P.append(f'''<div id="{pid}" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="4">{kk}<div class="kanca" style="top:{top}px">
  <div class="k-a sh" style="font-size:{boyust}px">{W(ust)}</div><div class="k-b"><span class="w metal buyuk" id="{pid}b" style="font-size:{boy}px">{buyuk}</span></div></div></div>''')
    t(f'tl.fromTo("#{pid}b",{{scale:1.1}},{{scale:1,duration:0.6,ease:"expo.out"}},{bas});')
    t(f'tl.to("#{pid} .w, #{pid} .kick",{{opacity:0,filter:"blur(8px)",duration:0.16,stagger:0.02,ease:"power2.in"}},{bas+sure-0.26});')
def balonlar(bas, sure, L, pid="bl", top=330):
    h = "".join(f'<div class="bl b{i+1}" id="{pid}{i+1}">{x}</div>' for i, (x, _) in enumerate(L))
    P.append(f'<div id="{pid}" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="4"><div class="balonlar" style="top:{top}px">{h}</div></div>')
    for i, (_, b) in enumerate(L):
        t(f'tl.fromTo("#{pid}{i+1}",{{opacity:0,scale:0.6,y:40}},{{opacity:1,scale:1,y:0,duration:0.32,ease:"back.out(1.8)"}},{b});')
    t(f'tl.to("#{pid} .bl",{{opacity:0,y:-30,duration:0.16,stagger:0.03,ease:"power2.in"}},{bas+sure-0.24});')
def damga(bas, sure, kick, damga_yazi, alt, pid, boy=190, top=420):
    P.append(f'''<div id="{pid}" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="4"><div class="blok" style="top:{top}px">
  <div class="kick">{kick}</div><div class="damga" id="{pid}d"><span style="font-size:{boy}px">{damga_yazi}</span></div>
  <div class="alt sh" id="{pid}a">{alt}</div></div></div>''')
    t(f'tl.fromTo("#{pid} .kick",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{bas+0.08});')
    t(f'tl.fromTo("#{pid}d",{{opacity:0,scale:2.4,rotation:-18}},{{opacity:1,scale:1,rotation:-6,duration:0.22,ease:"power4.in"}},{bas+0.85});')
    t(f'tl.fromTo("#{pid}d",{{x:0}},{{keyframes:[{{x:-6,duration:0.03}},{{x:6,duration:0.03}},{{x:-3,duration:0.03}},{{x:0,duration:0.03}}]}},{bas+1.07});')
    t(f'tl.fromTo("#{pid}a",{{opacity:0,y:20,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.35,ease:"power2.out"}},{bas+1.75});')
    t(f'tl.to("#{pid} .blok",{{opacity:0,filter:"blur(8px)",duration:0.16,ease:"power2.in"}},{bas+sure-0.18});')
def blok(bas, sure, kick, ana, pid, cls="orta", top=420, alt="", gecikme=0.55, boy=None):
    """kick + kelime kelime gelen ana satır (W sözdizimi) + isteğe bağlı alt satır."""
    a = f'<div class="alt sh" id="{pid}a">{alt}</div>' if alt else ""
    kk = f'<div class="kick">{kick}</div>' if kick else ""
    P.append(f'''<div id="{pid}" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="4"><div class="blok" style="top:{top}px">
  {kk}<div class="{cls} sh" style="margin-top:26px{";font-size:%dpx" % boy if boy else ""}">{W(ana)}</div>{a}</div></div>''')
    if kick: t(f'tl.fromTo("#{pid} .kick",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{bas+0.08});')
    t(f'tl.fromTo("#{pid} .w",{{opacity:0,filter:"blur(8px)",y:16}},{{opacity:1,filter:"blur(0px)",y:0,duration:0.2,stagger:0.11,ease:"expo.out"}},{bas+(gecikme if kick else 0.1)});')
    if alt: t(f'tl.fromTo("#{pid}a",{{opacity:0,y:20,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.35,ease:"power2.out"}},{bas+gecikme+1.0});')
    t(f'tl.to("#{pid} .blok",{{opacity:0,filter:"blur(8px)",duration:0.16,ease:"power2.in"}},{bas+sure-0.2});')
def iki(bas, sure, kickA, anaA, buyukB, pid, gecis=None, top=420, boyB=150, noktalar=False):
    """önce küçük cümle (A), sonra dev metal kelime (B)."""
    g = gecis if gecis else bas + sure * 0.48
    nk = "".join(f'<span class="nokta metal" id="{pid}n{i}">.</span>' for i in (1, 2, 3)) if noktalar else ""
    P.append(f'''<div id="{pid}" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="4"><div class="blok" style="top:{top}px">
  <div id="{pid}A"><div class="kick">{kickA}</div><div class="orta sh" style="margin-top:20px">{anaA}</div></div>
  <div id="{pid}B" style="position:absolute;left:0;top:0;width:1080px;opacity:0"><div class="dev2"><span class="metal it" id="{pid}u" style="display:inline-block;font-weight:900;font-size:{boyB}px;letter-spacing:-0.035em;line-height:1.12;padding:0 20px;filter:drop-shadow(0 8px 30px rgba(0,0,0,0.7));white-space:normal">{buyukB}</span>{nk}</div></div></div></div>''')
    t(f'tl.fromTo("#{pid}A",{{opacity:0,y:18,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.3,ease:"power2.out"}},{bas+0.06});')
    t(f'tl.to("#{pid}A",{{opacity:0,y:-30,filter:"blur(8px)",duration:0.16,ease:"power2.in"}},{g-0.16});')
    t(f'tl.set("#{pid}B",{{opacity:1}},{g});')
    t(f'tl.fromTo("#{pid}u",{{opacity:0,scale:1.2,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.35,ease:"expo.out"}},{g});')
    if noktalar:
        for i in (1, 2, 3): t(f'tl.fromTo("#{pid}n{i}",{{opacity:0}},{{opacity:1,duration:0.08}},{g+0.2+0.2*i});')
    t(f'tl.to("#{pid} .blok",{{opacity:0,filter:"blur(8px)",duration:0.14,ease:"power2.in"}},{bas+sure-0.16});')
def urun(bas, sure, img, kick, ust1, ust2, cips, w=570, sol=None, ust=640, don0=5, don1=-2.5, flas=True, boy1=112, boy2=128, bg="radial-gradient(ellipse 90% 60% at 50% 62%, #16204F 0%, var(--navy) 55%, var(--zemin) 100%)", cipstop=1452, mask=True, doku=False):
    sol = (1080 - w) // 2 if sol is None else sol
    par = f'<div class="parilti" style="width:{w}px;height:1000px;-webkit-mask-image:url(assets/img/{img});mask-image:url(assets/img/{img});-webkit-mask-size:{w}px auto;mask-size:{w}px auto"><div class="bant" id="par"></div></div>' if mask else ""
    P.append(f'''<div id="s5" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="0">
  <div class="s5bg" style="background:{bg}"></div><div class="huzme" id="huzme"></div>{'<div class="saten" id="saten"></div>' if doku else ''}
  <div class="urunw" id="urunw" style="left:{sol}px;top:{ust}px;width:{w}px;height:auto"><img src="assets/img/{img}" alt="" style="width:{w}px">{par}</div>
  {'<div class="satenon" id="satenon"></div>' if doku else ''}<div class="altkarart"></div></div>''')
    if doku: t(f'tl.fromTo("#saten, #satenon",{{scale:1.12,xPercent:2}},{{scale:1.0,xPercent:-2,duration:{sure},ease:"none"}},{bas});')
    t(f'tl.fromTo("#urunw",{{y:420,scale:0.94,rotation:{don0}}},{{y:0,scale:1,rotation:0,duration:1.0,ease:"expo.out"}},{bas});')
    t(f'tl.to("#urunw",{{y:-26,rotation:{don1},scale:1.04,duration:{sure-1.0},ease:"sine.inOut"}},{bas+1.0});')
    if mask: t(f'tl.fromTo("#par",{{xPercent:-130}},{{xPercent:130,duration:0.8,ease:"power2.inOut"}},{bas+0.7});')
    t(f'tl.fromTo("#huzme",{{opacity:0.2,rotation:-8}},{{opacity:0.65,rotation:6,duration:{sure},ease:"sine.inOut"}},{bas});')
    if flas:
        P.append(f'<div id="flas" class="clip" data-start="{bas}" data-duration="0.4" data-track-index="9"><div class="flasi" id="flasi"></div></div>')
        t(f'tl.fromTo("#flasi",{{opacity:0.85}},{{opacity:0,duration:0.36,ease:"power2.out"}},{bas});')
    P.append(f'''<div id="s5y" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="4">
  <div class="kick k5">{kick}</div>
  <div class="s5ust"><span style="font-size:{boy1}px">{W(ust1, "sh")}</span><br><span style="font-size:{boy2}px">{W(ust2)}</span></div>
  <div class="s5alt inter" id="cips" style="top:{cipstop}px">{cips}</div></div>''')
    t(f'tl.fromTo("#s5y .k5",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{bas+0.1});')
    t(f'tl.fromTo("#s5y .s5ust .w",{{opacity:0,filter:"blur(8px)",scale:1.2}},{{opacity:1,filter:"blur(0px)",scale:1,duration:0.26,stagger:0.13,ease:"expo.out"}},{bas+0.35});')
    t(f'tl.fromTo("#cips",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"power2.out"}},{bas+1.4});')
    t(f'tl.to("#s5y",{{opacity:0,duration:0.15}},{bas+sure-0.15});')
def bilgi(bas, sure, html, pid="not", top=1490):
    P.append(f'<div id="{pid}" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="6"><div class="not" id="{pid}i" style="top:{top}px">{html}</div></div>')
    t(f'tl.fromTo("#{pid}i",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,ease:"power2.out"}},{bas+0.1});')
    t(f'tl.to("#{pid}i",{{opacity:0,duration:0.2}},{bas+sure-0.22});')
def son(bas, sure, a, b, marka, boy=150, top=420, pid="son"):
    P.append(f'''<div id="{pid}" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="5"><div class="sonyazi" style="top:{top}px">
  <div class="s-a sh">{W(a)}</div><div class="s-b"><span class="w metal it" id="hc" style="font-size:{boy}px">{b}</span></div>
  <div class="marka inter" id="marka" style="position:relative;left:auto;top:auto;margin:34px auto 0;width:auto;display:inline-block;padding:0 44px;white-space:nowrap">{marka}</div></div></div>''')
    t(f'tl.fromTo("#{pid} .s-a .w",{{opacity:0,filter:"blur(6px)",y:14}},{{opacity:1,filter:"blur(0px)",y:0,duration:0.12,stagger:0.06,ease:"power2.out"}},{bas+0.02});')
    t(f'tl.fromTo("#hc",{{opacity:0,scale:1.2,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.4,ease:"expo.out"}},{bas+0.22});')
    t(f'tl.fromTo("#marka",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{bas+0.4});')


def flas(bas, pid=None):
    pid = pid or "fl%d" % int(round(bas * 10))
    P.append(f'<div id="{pid}" class="clip" data-start="{bas}" data-duration="0.4" data-track-index="9"><div class="flasi" id="{pid}i"></div></div>')
    t(f'tl.fromTo("#{pid}i",{{opacity:0.85}},{{opacity:0,duration:0.36,ease:"power2.out"}},{bas});')


def bolum(bas, sure, metin, ek="", pid="bc"):
    """Sarı bölüm etiketi (belgesel/şerit hissi)."""
    P.append(f'<div id="{pid}" class="clip" data-start="{bas}" data-duration="{sure}" data-track-index="6"><div class="bolum inter" id="{pid}i"><i></i>{metin} <b>{ek}</b></div></div>')
    t(f'tl.fromTo("#{pid}i",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.3,ease:"power2.out"}},{bas+0.1});')
    t(f'tl.to("#{pid}i",{{opacity:0,duration:0.2}},{bas+sure-0.24});')


# ayar JSON sahne türleri → fonksiyon + anahtar eşlemesi (i = kesim aralığı numarası → bas/sure kesimlerden gelir)
TURLER = {"kanca": kanca, "blok": blok, "iki": iki, "damga": damga, "balonlar": balonlar, "urun": urun, "bilgi": bilgi, "son": son, "flas": flas, "bolum": bolum}


def sahne(s, t_, urun_png="urun.png", urun_w=570, doku=False):
    """s: {"tur": "blok", "i": 1, ...} — i verilirse bas=t_[i], sure=t_[i+1]-t_[i]; açık "bas"/"sure" bunları ezer."""
    s = dict(s)
    tur = s.pop("tur")
    if tur not in TURLER:
        raise SystemExit("bilinmeyen sahne türü: %s (izinli: %s)" % (tur, ", ".join(TURLER)))
    i = s.pop("i", None)
    if i is not None:
        s.setdefault("bas", t_[i])
        s.setdefault("sure", round(t_[i + 1] - t_[i], 2))
    pid = s.pop("pid", None)
    if pid:
        s["pid"] = pid
    elif i is not None and tur in ("blok", "bilgi", "iki", "damga", "balonlar"):
        s["pid"] = "%s%d" % ({"blok": "b", "bilgi": "n", "iki": "k", "damga": "d", "balonlar": "x"}[tur], i)
    if tur == "blok":
        s.setdefault("kick", "")
    if tur == "bilgi":
        g = s.pop("gec", 0.9)
        s["bas"] = round(s["bas"] + g, 2)
        s["sure"] = round(s["sure"] - g - 0.1, 2)
    if tur == "urun":
        s.setdefault("img", urun_png)
        s.setdefault("w", urun_w)
        s.setdefault("doku", doku)
    TURLER[tur](**s)


def metinler():
    """Sahnelere yazılan tüm görünür metin (kapılar için): P içindeki etiketsiz düz metin."""
    import re
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", " ".join(P)))


def bitir(K, SURE, DROP, kesimler, tema=None, ek_css="", doku=False):
    tema = dict(tema or {})
    if doku:
        tema["doku"] = "url(assets/img/doku.jpg)"
    yaz(K, P, T, tema_css(tema) + STIL + ek_css, SURE)
    with open(os.path.join(K, "zaman.json"), "w") as f:
        json.dump({"sure": SURE, "drop": DROP, "kesimler": kesimler}, f)
