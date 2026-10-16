import numpy as np, knob
from scipy.special import erf, logsumexp
rng=np.random.default_rng(7)
SQPI=np.sqrt(np.pi)
T=24.0; E=np.arange(-T/2,T/2+1e-9,0.3); CW=6.0; SIG=1.35
def mub(c,d):  # batch: c,d arrays (n,) -> (n,nb)
    dt=np.diff(E); out=0
    for s in (-0.5,0.5):
        tau=(c+s*d)[:,None]; F=erf((E[None,:]-tau)/SIG)
        out=out+(SIG*SQPI/2)*(F[:,1:]-F[:,:-1])/dt[None,:]
    return out
def lp_marg(X,th,sn,nc=40):  # X (n,nb), th (n,) -> log p(x|th) marg over c grid
    cg=np.linspace(-CW/2,CW/2,nc); n=len(th)
    M=mub(np.tile(cg,n),np.repeat(th,nc)).reshape(n,nc,-1)
    ll=-((X[:,None,:]-M)**2).sum(-1)/(2*sn**2)
    return logsumexp(ll,axis=1)
def draw(th,sn):
    c=rng.uniform(-CW/2,CW/2,len(th)); M=mub(c,th)
    return M+sn*rng.standard_normal(M.shape)
def global_zzb(D,sn,nh=14,nsim=700):
    hs=np.linspace(0,D,nh+1); A=np.zeros(nh+1); A[0]=1.0
    for k,h in enumerate(hs[1:-1],1):
        th=rng.uniform(0,D-h,nsim)
        X0=draw(th,sn); X1=draw(th+h,sn)
        e0=np.mean(lp_marg(X0,th+h,sn)>lp_marg(X0,th,sn))
        e1=np.mean(lp_marg(X1,th,sn)>=lp_marg(X1,th+h,sn))
        pe=0.5*(e0+e1)
        A[k]=(2/D)*(D-h)*pe
    V=np.maximum.accumulate(A[::-1])[::-1]
    return np.trapezoid(hs/2*V,hs), np.trapezoid(hs/2*A,hs)
def mmse(D,sn,n=2500,nd=61,nc=40):
    dg=np.linspace(0,D,nd); cg=np.linspace(-CW/2,CW/2,nc)
    M=np.stack([knob.mu(E,cg,d,SIG) for d in dg]).reshape(nd*nc,-1); n2=(M**2).sum(1)
    d=rng.uniform(0,D,n); X=draw(d,sn)
    ll=-(((X**2).sum(1))[:,None]-2*X@M.T+n2[None,:])/(2*sn**2)
    lp=logsumexp(ll.reshape(n,nd,nc),axis=2); p=np.exp(lp-lp.max(1,keepdims=True)); p/=p.sum(1,keepdims=True)
    dh=p@dg; err=(dh-d)**2
    return err.mean(), err.std()/np.sqrt(n)
print("GLOBAL ZZB vs exact Bayes MMSE (uniform d prior [0,D]), sigma_pulse=1.35, dt=0.3")
print(" sn   D   prior var   ZZB(valley)  ZZB(no valley)   MMSE(+-SE)      MMSE/ZZB")
for sn in [0.15,0.4]:
    for D in [2,4,6]:
        z,zn=global_zzb(D,sn); m,se=mmse(D,sn)
        print("%.2f %d   %.3f      %.5f      %.5f        %.5f(%.5f)   %.2f"%(sn,D,D*D/12,z,zn,m,se,m/z))
