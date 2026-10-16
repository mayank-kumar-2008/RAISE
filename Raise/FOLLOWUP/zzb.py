import numpy as np, knob
from scipy.special import logsumexp
rng=np.random.default_rng(1)
def zzb(edges,d,sig,sn,A,cw,nc=60,nsim=500,hs=np.linspace(0.05,4,18)):
    cg=np.linspace(-cw/2,cw/2,nc)
    M0=knob.mu(edges,cg,d,sig,A)
    def loglik(X,M): # marginal over c
        ll=-((X[:,None,:]-M[None,:,:])**2).sum(-1)/(2*sn**2)
        return logsumexp(ll,axis=1)-np.log(nc)
    f=[]
    for h in hs:
        M1=knob.mu(edges,cg,d+h,sig,A)
        ci=rng.integers(0,nc,nsim)
        X0=M0[ci]+sn*rng.standard_normal((nsim,M0.shape[1]))
        X1=M1[ci]+sn*rng.standard_normal((nsim,M0.shape[1]))
        p0=np.mean(loglik(X0,M1)>loglik(X0,M0))   # H0 true, decide H1
        p1=np.mean(loglik(X1,M0)>=loglik(X1,M1))  # H1 true, decide H0
        f.append(h*0.5*(p0+p1))
    f=np.array(f); v=np.maximum.accumulate(f[::-1])[::-1]
    return 0.5*np.trapezoid(v,hs)
