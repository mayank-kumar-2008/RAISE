import numpy as np, knob
from scipy.special import erfc, logsumexp
from scipy.stats import spearmanr
rng=np.random.default_rng(5)
Q=lambda x:0.5*erfc(x/np.sqrt(2))
T=24.0; CW=6.0; DL=1.0
E=np.arange(-T/2,T/2+1e-9,DL)

# 1) aliasing amplitude vs sigma/Delta (single pulse, phase modulation of sum_k mu_k^2)
print("1) alias modulation m(sigma/Delta) = (Emax-Emin)/(Emax+Emin)")
r=[];lm=[]
for s in np.arange(0.25,0.81,0.05):
    ph=np.linspace(0,DL,61)
    En=np.array([ (knob.mu(E,np.array([p]),0.0,s,1.0)**2).sum()/2 for p in ph])  # d=0 -> two overlapped; shape still single Gaussian*2
    m=(En.max()-En.min())/(En.max()+En.min()); r.append(s/DL); lm.append(np.log(m))
    print("  s/D=%.2f  m=%.4f"%(s/DL,m))
r=np.array(r); lm=np.array(lm)
p=np.polyfit(r**2,lm,1); print("  fit ln m = %.3f*(s/D)^2 + %.3f ; theory slope -pi^2/2=%.3f (with sinc corrections)"%(p[0],p[1],-np.pi**2/2))

# 2) rho-optimal sigma/Delta vs offset h
def rho(edges,d,h,sig,A,nc=81):
    cg=np.linspace(-CW/2,CW/2,nc); M0=knob.mu(edges,cg,d,sig,A); M1=knob.mu(edges,cg,d+h,sig,A)
    D2=(M0**2).sum(1)[:,None]-2*M0@M1.T+(M1**2).sum(1)[None,:]; return np.sqrt(max(D2.min(),0))
sg=np.arange(0.30,1.51,0.05)
print("\n2) argmax_sigma rho(d,h) (fixed energy, Delta=1) : h -> optimum sigma/Delta")
for d in [1.0,2.0]:
    out=[]
    for h in [0.1,0.2,0.4,0.8,1.6,3.2]:
        rv=[rho(E,d,h,s,(1.35/s)**0.5) for s in sg]; out.append("h=%.1f:%.2f"%(h,sg[int(np.argmax(rv))]))
    print("  d=%.0f  "%d+"  ".join(out))

# 3) SNR scaling: surrogate optimum vs sigma_n, and ZZB (standard form) MC optimum
hs=np.linspace(0.05,4,40)
def surrogate(d,s,sn):
    A=(1.35/s)**0.5; pe=np.array([Q(rho(E,d,h,s,A)/(2*sn)) for h in hs]); V=np.maximum.accumulate(pe[::-1])[::-1]
    return 0.5*np.trapezoid(hs*V,hs)
def zzb_std(d,s,sn,nc=60,nsim=400,hh=np.linspace(0.05,4,24)):
    A=(1.35/s)**0.5; cg=np.linspace(-CW/2,CW/2,nc); M0=knob.mu(E,cg,d,s,A)
    ll=lambda X,M: logsumexp(-((X[:,None,:]-M[None,:,:])**2).sum(-1)/(2*sn**2),axis=1)
    pe=[]
    for h in hh:
        M1=knob.mu(E,cg,d+h,s,A); ci=rng.integers(0,nc,nsim)
        X0=M0[ci]+sn*rng.standard_normal((nsim,M0.shape[1])); X1=M1[ci]+sn*rng.standard_normal((nsim,M0.shape[1]))
        pe.append(0.5*(np.mean(ll(X0,M1)>ll(X0,M0))+np.mean(ll(X1,M0)>=ll(X1,M1))))
    pe=np.array(pe); V=np.maximum.accumulate(pe[::-1])[::-1]; return 0.5*np.trapezoid(hh*V,hh)
print("\n3) optimum sigma/Delta vs noise (d=1, Delta=1)")
zs=[0.35,0.5,0.6,0.7,0.8,0.9,1.1]
for sn in [0.08,0.15,0.3,0.6]:
    su=np.array([surrogate(1.0,s,sn) for s in sg]); sf=sg[su.argmin()]
    zz=np.array([zzb_std(1.0,s,sn) for s in zs])
    ss=np.array([surrogate(1.0,s,sn) for s in zs])
    print("  sn=%.2f  surrogate(fine grid) opt s/D=%.2f | ZZB-MC opt s/D=%.2f (grid %s) | spearman(sur,zzb)=%.2f"%(sn,sf,zs[int(zz.argmin())],zs,spearmanr(ss,zz)[0]),flush=True)
    print("     ZZB values:",np.round(zz,4))
