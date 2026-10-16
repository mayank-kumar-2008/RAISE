import numpy as np, knob, zzb
SN=0.15; CW=6.0; T=24.0
e_c=np.arange(-T/2,T/2+1e-9,1.0)
print("A3 refined: fixed energy, bins 1.0m. cols: d, 1/F, ZZB, MSE_ML")
for s in [0.25,0.4,0.55,0.7,0.85,1.0,1.35]:
    A=(1.35/s)**0.5; row=[]
    for d in [1.0,2.0]:
        F=knob.fisher_marg(e_c,d,s,SN,A,CW); z=zzb.zzb(e_c,d,s,SN,A,CW); m=knob.mse_ml(e_c,d,s,SN,A,CW,ntr=1000)
        row.append("d=%.0f: 1/F=%.4f ZZB=%.4f ML=%.4f"%(d,1/F,z,m))
    print("sigma=%.2f  "%s+" | ".join(row))
print("\nC extended: fixed N=48, window T (cw=6, sigma=1.35). d=1,2")
for t in [3,4,5,6,7,8,10,12]:
    e=np.linspace(-t/2,t/2,49); row=[]
    for d in [1.0,2.0]:
        F=knob.fisher_marg(e,d,1.35,SN,1.0,CW); m=knob.mse_ml(e,d,1.35,SN,1.0,CW,ntr=1000)
        row.append("d=%.0f: 1/F=%.4f ML=%.4f"%(d,1/F,m))
    print("T=%2d dt=%.2f  "%(t,t/48)+" | ".join(row))
