import numpy as np, knob
from scipy.special import logsumexp
rng=np.random.default_rng(3)
T=24.0; e=np.arange(-T/2,T/2+1e-9,0.3); CW=6.0
def true_MI(D,sn,sig=1.35,nd=40,nc=50,nmc=1200):
    dg=np.linspace(0,D,nd); cg=np.linspace(-CW/2,CW/2,nc)
    M=np.stack([knob.mu(e,cg,d,sig) for d in dg]); Mf=M.reshape(nd*nc,-1)
    n2=(Mf**2).sum(1)
    ji=rng.integers(0,nd,nmc); ci=rng.integers(0,nc,nmc)
    X=M[ji,ci]+sn*rng.standard_normal((nmc,Mf.shape[1]))
    ll=-(((X**2).sum(1))[:,None]-2*X@Mf.T+n2[None,:])/(2*sn**2)
    ll=ll.reshape(nmc,nd,nc)
    lpd=logsumexp(ll,axis=2)-np.log(nc)           # log p(x|d_j)
    lpx=logsumexp(lpd,axis=1)-np.log(nd)          # log p(x)
    return np.mean(lpd[np.arange(nmc),ji]-lpx)
def ceiling(D,sn,sig=1.35,nd=14):
    dg=np.linspace(0.02,D,nd)
    F=np.array([knob.fisher_marg(e,d,sig,sn,1.0,CW,nmc=500) for d in dg])
    return np.log(1+0.5*np.trapezoid(np.sqrt(F),dg))
print("sn   D   trueMI(nats)  ceiling(nats)  ln(D/res)-ish  ratio")
for sn in [0.15,0.4]:
    for D in [1,2,4,6]:
        t=true_MI(D,sn); c=ceiling(D,sn)
        print("%.2f %d   %.3f        %.3f        ratio ceiling/true=%.2f"%(sn,D,t,c,c/max(t,1e-9)))
