#!/usr/bin/env python3
"""Müzik zarfı: 0,5 sn RMS (dB) + bas (<150 Hz) zarfı; en büyük kalıcı yükseliş anları (drop adayı). Kullanım: muzik_analiz.py dosya..."""
import sys, subprocess, numpy as np
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _arac import FF
SR=22050
def oku(f, af=None):
    c=[FF,"-v","error","-i",f,"-ac","1","-ar",str(SR)]+(["-af",af] if af else [])+["-f","f32le","-"]
    return np.frombuffer(subprocess.run(c,capture_output=True).stdout,np.float32)
def zarf(x,w=0.5):
    h=int(w*SR); n=len(x)//h
    return 10*np.log10((x[:n*h].reshape(n,h)**2).mean(1)+1e-10)
for f in sys.argv[1:]:
    x=oku(f); b=oku(f,"lowpass=f=150")
    z=zarf(x); zb=zarf(b); n=min(len(z),len(zb)); z,zb=z[:n],zb[:n]
    print("\n==",f.split('/')[-1],"sure %.1f"%(len(x)/SR),"medyan %.1f dB"%np.median(z))
    print(" tam :"," ".join("%3d"%round(v) for v in z[:120]))
    print(" bas :"," ".join("%3d"%round(v) for v in zb[:120]))
    # drop adayı: bas zarfında 2 sn sonrası - 2 sn öncesi
    ad=[]
    for i in range(4,n-4):
        d=zb[i:i+4].mean()-zb[i-4:i].mean(); ad.append((d,i*0.5))
    ad.sort(reverse=True); sec=[]
    for d,t in ad:
        if all(abs(t-s)>3 for _,s in sec): sec.append((d,t))
        if len(sec)>=5: break
    print(" bas girişi adayları (dB artış @ sn):",", ".join("%.1f@%.1f"%(d,t) for d,t in sec))
    # ince zaman: en iyi adayın çevresinde 20 ms onset
    if sec:
        t0=sec[0][1]; a=int((t0-1.0)*SR); seg=b[max(a,0):a+int(2.5*SR)]; h=int(0.02*SR); m=len(seg)//h
        e=10*np.log10((seg[:m*h].reshape(m,h)**2).mean(1)+1e-10); k=int(np.argmax(np.diff(e))); print(" ince onset ≈ %.2f sn"%(max(a,0)/SR+(k+1)*0.02))
