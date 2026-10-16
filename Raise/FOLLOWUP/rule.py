import numpy as np, knob
from scipy.special import erfc
import zzb2
SN=0.15; CW=6.0; T=24.0; D0=1.0
Q=lambda x:0.5*erfc(x/np.sqrt(2))
def rho(edges,d,h,sig,A,nc=81):
    # centroid-invariant signature distance: min over c,c' in prior of ||mu(c,d)-mu(c',d+h)||
    cg=np.linspace(-CW/2,CW/2,nc)
    M0=knob.mu(edges,cg,d,sig,A); M1=knob.mu(edges,cg,d+h,sig,A)
    D2=(M0**2).sum(1)[:,None]-2*M0@M1.T+(M1**2).sum(1)[None,:]
    return np.sqrt(max(D2.min(),0))
def surrogate(edges,d,sig,A,sn,hs):
    pe=np.array([Q(rho(edges,d,h,sig,A)/(2*sn)) for h in hs])
    V=np.maximum.accumulate(pe[::-1])[::-1]
    return 0.5*np.trapezoid(hs*V,hs)
hs=np.linspace(0.05,4,40)
print("Delta  sigma | surrogate(d=1)  ZZB(d=1)")
for Dl in [0.5,1.0,2.0]:
    e=np.arange(-T/2,T/2+1e-9,Dl)
    sigs=[0.25,0.35,0.5,0.7,0.9,1.2,1.6] if Dl>=1 else [0.15,0.2,0.3,0.4,0.55,0.8,1.2]
    sig_s=[];sur=[];zz=[]
    for s in sigs:
        A=(1.35/s)**0.5
        sur.append(surrogate(e,D0,s,A,SN,hs))
        p,st=zzb2.both(e,D0,s,SN,A,CW,nsim=400,hs=np.linspace(0.05,4,24)); zz.append(st)
    sur=np.array(sur); zz=np.array(zz)
    for s,a,b in zip(sigs,sur,zz): print("%.1f   %.2f | %.5f   %.5f"%(Dl,s,a,b))
    i,j=sur.argmin(),zz.argmin()
    from scipy.stats import spearmanr
    print("  -> argmin surrogate sigma=%.2f (sigma/Delta=%.2f) | argmin ZZB sigma=%.2f (sigma/Delta=%.2f) | spearman=%.2f\n"%(sigs[i],sigs[i]/Dl,sigs[j],sigs[j]/Dl,spearmanr(sur,zz)[0]))
