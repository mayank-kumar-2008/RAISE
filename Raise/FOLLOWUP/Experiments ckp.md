# RAISE follow-up experiments (in chat order)

Model throughout: two Gaussian returns, pulse ~ exp(-t^2/sigma^2), Gaussian noise sigma_n (default 0.15),
centroid nuisance c ~ U[-3,3] m, equal weights, integrate-and-dump bins. Python: numpy, scipy, sklearn (netroom only).
All results are single-seed simulations under these assumptions.

| # | File | What it does | Depends on |
|---|------|--------------|------------|
| 1 | knob.py | Core simulator: bin-averaged waveform mu(), marginal Fisher F_D(d), joint-ML MSE, MI ceiling (Eq. 6) | - |
| 2 | sweep.py | Knob sweeps: A pulse width, B bin width, C fixed-N window (1/F, ML-MSE, MI ceiling) | knob |
| 3 | zzb.py | Pointwise ZZB (paper form: valleyfill(h*Pe)) | knob |
| 4 | sweep2.py | Coarse-bin pulse-width sweep with ZZB; extended window sweep | knob, zzb |
| 5 | mi.py | Theorem-2 ceiling vs Monte Carlo true I(X;D) | knob |
| 6 | gzzb.py | Global ZZB (uniform d prior) vs exact Bayes MMSE | knob |
| 7 | zzb2.py | Paper valley-fill form vs standard form h*V{Pe}; A3 recheck | knob |
| 8 | rule.py | Design rule: signature-distance surrogate vs ZZB over bin widths | knob, zzb2 |
| 9 | netroom.py | Plain MLP vs exact MMSE (room for a new model) | knob |

Run order: python sweep.py; python sweep2.py; python mi.py; python gzzb.py; python zzb2.py; python rule.py; python netroom.py

Notes
- zzb2.py and gzzb.py execute their experiments at import time; rule.py imports zzb2, so its output starts with zzb2's printout.
- knob.py uses np.trapezoid (NumPy >= 2.0); use np.trapz on older NumPy.
- Runtime is minutes per script on one CPU core; seeds are fixed in each file.
