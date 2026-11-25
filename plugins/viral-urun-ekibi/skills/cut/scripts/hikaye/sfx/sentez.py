#!/usr/bin/env python3
"""v7 sentetik efektler (numpy; kendi üretimimiz, lisans gerekmez). python3 sentez.py → aynı klasöre wav."""
import wave, os, sys
try:
    import numpy as np
except ImportError as _hata:  # ham ImportError yerine anlaşılır mesaj, çıkış 3 (kurulum eksik)
    print("kurulum eksik: '%s' paketi bulunamadı. Kur: python3 -m pip install --user numpy (Windows: py -3 -m pip install --user numpy)" % (_hata.name or "numpy"), file=sys.stderr)
    sys.exit(3)
SR=48000; K=os.environ.get('SFX_CIKTI') or os.path.dirname(os.path.abspath(__file__)); os.makedirs(K,exist_ok=True); rng=np.random.default_rng(7)
def yaz(ad,x,tepe=0.9):
    x=np.asarray(x,np.float64); x=x/ (np.abs(x).max()+1e-9)*tepe
    with wave.open(os.path.join(K,ad),'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype('<i2').tobytes())
def t(s): return np.arange(int(s*SR))/SR
def lp(x,a):
    y=np.zeros_like(x); p=0.0
    for i,v in enumerate(x): p+=a*(v-p); y[i]=p
    return y
def hp(x,a): return x-lp(x,a)
# mantar "pop": kısa bas darbe + gürültü patlaması + köpük fısıltısı kuyruğu
tt=t(1.2); pop=np.sin(2*np.pi*(180*np.exp(-tt*30)+70)*tt)*np.exp(-tt*28)
pop+=0.7*hp(rng.standard_normal(len(tt)),0.3)*np.exp(-tt*60)
pop+=0.10*hp(rng.standard_normal(len(tt)),0.5)*np.exp(-tt*3.2)*(tt>0.03)
yaz('pop.wav',pop)
# köpük fısıltısı (1,6 sn)
tt=t(1.6); yaz('kopuk.wav',hp(rng.standard_normal(len(tt)),0.6)*np.minimum(tt/0.15,1)*np.exp(-tt*1.6),0.5)
# saat tiki / tok
tt=t(0.09); yaz('tik.wav',np.sin(2*np.pi*2400*tt)*np.exp(-tt*120)+0.5*np.sin(2*np.pi*900*tt)*np.exp(-tt*80))
tt=t(0.12); yaz('tok.wav',np.sin(2*np.pi*1500*tt)*np.exp(-tt*90)+0.6*np.sin(2*np.pi*600*tt)*np.exp(-tt*60))
# fare/sekme tıkı
tt=t(0.05); yaz('tikla.wav',hp(rng.standard_normal(len(tt)),0.4)*np.exp(-tt*220)+0.6*np.sin(2*np.pi*3200*tt)*np.exp(-tt*200))
# balon "pop" (UI)
tt=t(0.14); yaz('balon.wav',np.sin(2*np.pi*(520+900*tt)*tt)*np.exp(-tt*40))
# havai fişek: bas patlama + çıtırtı kuyruğu (2,2 sn)
tt=t(2.2); f=np.sin(2*np.pi*(90*np.exp(-tt*9)+38)*tt)*np.exp(-tt*5)
f+=0.8*lp(rng.standard_normal(len(tt)),0.08)*np.exp(-tt*14)
cit=hp(rng.standard_normal(len(tt)),0.5)*(rng.random(len(tt))>0.9985)
cit=np.convolve(cit,np.exp(-np.arange(400)/60.0),'same')*np.exp(-np.maximum(tt-0.25,0)*2.2)*(tt>0.2)
yaz('fisek.wav',f+0.9*cit/ (np.abs(cit).max()+1e-9))
# çan / çıngırak (Noel): harmonik olmayan kısmi sesler
tt=t(1.6); c=sum(a*np.sin(2*np.pi*fq*tt)*np.exp(-tt*d) for fq,a,d in [(1318,1,3.5),(2637,0.6,5),(3951,0.35,7),(5274,0.2,9),(1975,0.3,4)])
yaz('can.wav',c,0.7)
tt=t(0.5); j=np.zeros(len(tt))
for k in range(5):
    s=int(k*0.085*SR); n=len(tt)-s; u=tt[:n]; j[s:]+=(np.sin(2*np.pi*4200*u)+0.7*np.sin(2*np.pi*6100*u)+0.5*hp(rng.standard_normal(n),0.6))*np.exp(-u*40)
yaz('cingirak.wav',j,0.6)
# telefon titreşimi (kısa-kısa)
def bz(s):
    u=t(s); return np.sign(np.sin(2*np.pi*165*u))*0.5+np.sin(2*np.pi*165*u)+0.3*np.sin(2*np.pi*330*u)
z=np.concatenate([bz(0.22)*np.hanning(int(0.22*SR))**0.3,np.zeros(int(0.12*SR)),bz(0.34)*np.hanning(int(0.34*SR))**0.3])
yaz('buzz.wav',lp(z,0.12),0.8)
# su damlası
tt=t(0.35); yaz('damla.wav',np.sin(2*np.pi*(700+2600*tt)*tt)*np.exp(-tt*22)*np.minimum(tt/0.004,1),0.7)
# kibrit/mum "fış"
tt=t(0.6); yaz('fis.wav',hp(rng.standard_normal(len(tt)),0.5)*np.minimum(tt/0.02,1)*np.exp(-tt*7),0.5)
# yorum balonu / CTA "bubble": iki kısa yükselen kabarcık sesi (kendi üretimimiz)
def kabarcik(f0, f1, sure, g=1.0):
    u = t(sure); ph = 2*np.pi*(f0*u + (f1-f0)*u*u/(2*sure))
    return g*np.sin(ph)*np.exp(-u*(5.0/sure))*np.minimum(u/0.004, 1)
b1 = kabarcik(420, 980, 0.11); b2 = kabarcik(560, 1300, 0.13, 0.8)
z = np.zeros(int(0.17*SR)+len(b2)); z[:len(b1)] += b1; z[int(0.17*SR):int(0.17*SR)+len(b2)] += b2
yaz('bubble.wav', z, 0.75)
print(sorted(f for f in os.listdir(K) if f.endswith('.wav')))
