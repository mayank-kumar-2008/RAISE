import numpy as np, knob
from scipy.special import logsumexp
rng=np.random.default_rng(11)
def both(edges,d,sig,sn,A,cw,nc=60,nsim=800,hs=np.linspace(0.05,4,40)):
    cg=np.linspace(-cw/2,cw/2,nc); M0=knob.mu(edges,cg,d,sig,A)
    def ll(X,M): return logsumexp(-((X[:,None,:]-M[None,:,:])**2).sum(-1)/(2*sn**2),axis=1)
    pe=[]
    for h in hs:
        M1=knob.mu(edges,cg,d+h,sig,A); ci=rng.integers(0,nc,nsim)
        X0=M0[ci]+sn*rng.standard_normal((nsim,M0.shape[1])); X1=M1[ci]+sn*rng.standard_normal((nsim,M0.shape[1]))
        pe.append(0.5*(np.mean(ll(X0,M1)>ll(X0,M0))+np.mean(ll(X1,M0)>=ll(X1,M1))))
    pe=np.array(pe); V=lambda f: np.maximum.accumulate(f[::-1])[::-1]
    paper=0.5*np.trapezoid(V(hs*pe),hs)      # valleyfill(h*Pe)  as written in Algorithm l.5
    std=0.5*np.trapezoid(hs*V(pe),hs)        # h * valleyfill(Pe) standard ZZ form
    return paper,std
e=np.arange(-12,12.001,0.3)
print("pointwise, sigma=1.35, dt=0.3, sn=0.15 : d, paper-form, standard-form, ratio")
for d in [0.3,1.0,2.0,3.0]:
    p,s=both(e,d,1.35,0.15,1.0,6.0); print(d,"%.5f %.5f %.2f"%(p,s,p/s))
e1=np.arange(-12,12.001,1.0)
print("\nA3 re-check (bins 1.0m, fixed energy), d=1: sigma, paper-form, standard-form")
for s in [0.25,0.4,0.55,0.7,0.85,1.0,1.35]:
    p,st=both(e1,1.0,s,0.15,(1.35/s)**0.5,6.0,nsim=500,hs=np.linspace(0.05,4,24)); print(s,"%.4f %.4f"%(p,st))
