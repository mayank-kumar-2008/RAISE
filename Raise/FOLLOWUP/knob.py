import numpy as np
from scipy.special import erf
rng=np.random.default_rng(0)
SQPI=np.sqrt(np.pi)

def mu(edges, c, d, sig, A=1.0):
    # integrate-and-dump bin means of two Gaussian pulses exp(-(t-tau)^2/sig^2); c shape (nc,)
    dt=np.diff(edges)
    out=0
    for s in (-0.5,0.5):
        tau=(c+s*d)[:,None]
        F=erf((edges[None,:]-tau)/sig)
        out=out+A*(sig*SQPI/2)*(F[:,1:]-F[:,:-1])/dt[None,:]
    return out  # (nc, nbins)

def fisher_marg(edges,d,sig,sn,A,cw,nc=80,nmc=1500,h=1e-3):
    cg=np.linspace(-cw/2,cw/2,nc)
    M=mu(edges,cg,d,sig,A)
    dM=(mu(edges,cg,d+h,sig,A)-mu(edges,cg,max(d-h,0),sig,A))/(d+h-max(d-h,0))
    ci=rng.integers(0,nc,nmc)
    X=M[ci]+sn*rng.standard_normal((nmc,M.shape[1]))
    # loglik for each c: -|x-M|^2/(2sn^2)
    ll=-((X[:,None,:]-M[None,:,:])**2).sum(-1)/(2*sn**2)
    ll-=ll.max(1,keepdims=True); p=np.exp(ll); p/=p.sum(1,keepdims=True)
    sc=np.einsum('mc,mck->m',p,(X[:,None,:]-M[None,:,:])*dM[None,:,:])/sn**2
    return np.mean(sc**2)

def mse_ml(edges,d,sig,sn,A,cw,ntr=600,nc=60,nd=60,dmax=6.0):
    cg=np.linspace(-cw/2,cw/2,nc); dg=np.linspace(0,dmax,nd)
    G=np.stack([mu(edges,cg,dd,sig,A) for dd in dg])  # (nd,nc,nb)
    Gf=G.reshape(nd*nc,-1)
    c0=rng.uniform(-cw/2,cw/2,ntr)
    M0=mu(edges,c0,d,sig,A)  # (ntr,nb) uses same d for each; c vary
    X=M0+sn*rng.standard_normal(M0.shape)
    # joint ML: min |x-G|^2
    D2=(X**2).sum(1)[:,None]-2*X@Gf.T+(Gf**2).sum(1)[None,:]
    k=D2.argmin(1); dhat=dg[k//nc]
    return np.mean((dhat-d)**2)

def mi_ceiling(edges,sig,sn,A,cw,dmax=6.0,nd=14):
    dg=np.linspace(0.05,dmax,nd)
    F=np.array([fisher_marg(edges,d,sig,sn,A,cw,nmc=600) for d in dg])
    return np.log(1+0.5*np.trapezoid(np.sqrt(F),dg))
