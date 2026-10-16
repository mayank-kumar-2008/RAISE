import numpy as np, knob, sys
from scipy.special import erf, logsumexp
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
rng=np.random.default_rng(21)
SQPI=np.sqrt(np.pi); T=24.0; E=np.arange(-T/2,T/2+1e-9,0.3); CW=6.0; SIG=1.35
def mub(c,d):
    dt=np.diff(E); out=0
    for s in (-0.5,0.5):
        tau=(c+s*d)[:,None]; F=erf((E[None,:]-tau)/SIG)
        out=out+(SIG*SQPI/2)*(F[:,1:]-F[:,:-1])/dt[None,:]
    return out
def draw(n,D,sn):
    d=rng.uniform(0,D,n); c=rng.uniform(-CW/2,CW/2,n); M=mub(c,d)
    return M+sn*rng.standard_normal(M.shape), d
def exact(X,d,D,sn,nd=61,nc=40):
    dg=np.linspace(0,D,nd); cg=np.linspace(-CW/2,CW/2,nc)
    M=np.stack([knob.mu(E,cg,x,SIG) for x in dg]).reshape(nd*nc,-1); n2=(M**2).sum(1)
    ll=-(((X**2).sum(1))[:,None]-2*X@M.T+n2[None,:])/(2*sn**2)
    lp=logsumexp(ll.reshape(len(X),nd,nc),axis=2); p=np.exp(lp-lp.max(1,keepdims=True)); p/=p.sum(1,keepdims=True)
    return p@dg
D=4.0
for sn in [0.15,0.4]:
    Xtr,dtr=draw(80000,D,sn); Xte,dte=draw(3000,D,sn)
    sc=StandardScaler().fit(Xtr)
    net=MLPRegressor(hidden_layer_sizes=(128,128),max_iter=60,early_stopping=True,n_iter_no_change=6,random_state=0,learning_rate_init=2e-3,batch_size=256)
    net.fit(sc.transform(Xtr),dtr)
    mn=np.mean((net.predict(sc.transform(Xte))-dte)**2)
    me=np.mean((exact(Xte,dte,D,sn)-dte)**2)
    print("sn=%.2f D=%d  MLP MSE=%.5f  exact MMSE=%.5f  MLP/MMSE=%.2f  (epochs=%d)"%(sn,D,mn,me,mn/me,net.n_iter_),flush=True)
