import numpy as np, knob, sys
np.set_printoptions(precision=4,suppress=True)
SN=0.15; CW=6.0; DT=[0.5,1.0,2.0]
def run(label,cfgs):
    print("\n==",label)
    print("%-26s"%"setting"+"".join(["  1/F(d=%.1f) MSE_ML"%d for d in DT])+"   MIceil")
    res=[]
    for name,edges,sig,sn,A in cfgs:
        row=[]
        for d in DT:
            F=knob.fisher_marg(edges,d,sig,sn,A,CW); m=knob.mse_ml(edges,d,sig,sn,A,CW)
            row+= [1/F,m]
        mi=knob.mi_ceiling(edges,sig,sn,A,CW,nd=10)
        res.append((name,row,mi))
        print("%-26s"%name+"".join(["  %9.4f %7.4f"%(row[2*i],row[2*i+1]) for i in range(len(DT))])+"   %.3f"%mi)
    return res
T=24.0
# A: pulse width, fixed peak amplitude vs fixed energy, fine bins 0.15 m
sigs=[0.4,0.7,1.0,1.35,2.0,3.0]
e_fine=np.arange(-T/2,T/2+1e-9,0.15)
run("A1 pulse width sigma, FIXED PEAK amp, bins 0.15m, fixed per-bin noise",
    [("sigma=%.2f"%s,e_fine,s,SN,1.0) for s in sigs])
run("A2 pulse width sigma, FIXED ENERGY, bins 0.15m",
    [("sigma=%.2f"%s,e_fine,s,SN,(1.35/s)**0.5) for s in sigs])
# A3: coarse bins 1.0m, fixed energy
e_c=np.arange(-T/2,T/2+1e-9,1.0)
run("A3 pulse width sigma, FIXED ENERGY, bins 1.0m",
    [("sigma=%.2f"%s,e_c,s,SN,(1.35/s)**0.5) for s in sigs])
# B: bin width, fixed window, noise var ~ 1/dt (physical) 
dts=[0.15,0.3,0.6,1.2,2.4]
run("B1 bin width, fixed window, noise^2 ∝ 1/dt (sn=0.15 at 0.15m)",
    [("dt=%.2f"%b,np.arange(-T/2,T/2+1e-9,b),1.35,SN*np.sqrt(0.15/b),1.0) for b in dts])
# C: fixed N bins=48, window T varies
N=48
Ts=[8,12,16,24,36,60]
run("C fixed N=48 bins, window T varies (cw=6, sigma=1.35)",
    [("T=%d dt=%.2f"%(t,t/N),np.linspace(-t/2,t/2,N+1),1.35,SN,1.0) for t in Ts])
