# RAISE -> CVPR: Follow-up Experiments, Interpretations, and Leads

Status: 2026-10-16. All experiments are **simulations**, single seed, run on the assumed model described in Section 2. Nothing has yet been demonstrated on real data. Replicate these results in your own code before quoting them as paper numbers.

---------------------------------------------------------------------------------------------------

## 0. Summary

1. The original paper was rejected because its **claims exceeded its evidence**; the mathematics was not found to be wrong (the reviewers' own assessment: "maths are not incorrect, main text oversells").
2. What the simulations now show reasonably well:
   - The **global Ziv-Zakai bound (ZZB)** (with a prior on d) is valid for every estimator, requires no local-homogeneity assumption, and lies within **1.06-1.58x** of the exact Bayes-MMSE. This is the most direct route to a "provably tight floor".
   - **Fisher/CRB and the Theorem-2 MI ceiling miss the design optimum; the ZZB captures it.** With fixed bins, the pulse width has an interior optimum at sigma/Delta ~ 0.5-0.9 (centre ~0.65-0.7), and the optimum shifts toward wider pulses as noise increases.
   - A plain MLP comes within ~1.3x of the exact MMSE, so a new architecture has no more than ~30% room in the in-prior simulated setting.
3. Comparison with Chan et al. (CVPR 2024): their package (closed form plus real-data curve) is currently more complete. The edge here is: **CRB-based design analysis misses this problem's optimum, whereas a tight global bound does not.**
4. Missing: a closed-form sigma*/Delta and any real-data test. These are the gating items.

---------------------------------------------------------------------------------------------------

## 1. Review Analysis: Problems in the Original Paper and How They Will Be Resolved

### 1.1 Summary of the Reviews

| Reviewer | Recommendation | Main points |
|---|---|---|
| Reviewer (first, unnamed) | Reject; soundness "mostly no" | (a) "Estimator-agnostic floor" is an overclaim because the ZZHE is a two-point average and rests on a local-homogeneity assumption; (b) headroom is an upper bound on *possible improvement*, not "unrecoverable error"; (c) the floor is ~1000x smaller than the observed error, which is the opposite of what the paper intended to show; (d) compare 3DEP against actual GEDI products (overlapping footprints), keeping simulation as a control; (e) define symbols (tau, x, I(theta)) before use |
| Reviewer #3 | Weak Reject; soundness "mostly yes" | Claims exceed validation; local-homogeneity assumption; threshold (kappa) not calibrated; real-world validation is semi-synthetic; present as a framework/diagnostic; state assumptions and limitations in the main text; soften validation claims |
| Meta-reviewer | Reject | Topic is highly relevant and of interest to the REO-2 community; both reviewers have major concerns about support for the claims |

Note: this is a **workshop** review (the reviews state "unsuitable for the workshop"), not a NeurIPS main-track review. No reviewer called the topic irrelevant or the idea wrong.

### 1.2 Issue Register (Reviewers plus Own Audit)

"Source": R = raised by a reviewer; A = found in the own audit (not raised by reviewers).
Status: SIM-DONE = resolved/tested in simulation; WRITE = writing task only; OPEN = data/experiment outstanding.

| # | Issue | Source | Resolution plan | Status |
|---|---|---|---|---|
| P1 | "Estimator-agnostic floor" is an overclaim; the pointwise ZZB rests on local homogeneity | R | Base the estimator-agnostic claim on the **global ZZB** (prior on d), which is valid for every estimator. Name the pointwise version "two-point lower bound under local homogeneity" and state the assumption in the main text. Evidence: E4 | SIM-DONE + WRITE |
| P2 | Headroom is misinterpreted | R | Headroom = Lcurrent - L = "maximum improvement not yet ruled out", not fundamental error. Remove "separates fixable from fundamental" | WRITE |
| P3 | Floor is ~1000x loose on real data, making headroom vacuous | R | Claim tightness only where it was observed. From the paper's Table 5: at d>=1.7 the MLE is within 1.57-1.96x of the floor; at d<=1.0 it ranges from 1.5x to ~60x (the MLE also fails through the swap basin there, so the gap cannot be separated into floor versus estimator). Global ZZB vs. exact MMSE: 1.06-1.58x (E4) | SIM-DONE; real data OPEN |
| P4 | Real validation is in the wrong regime: the threshold is ~sigma_pulse ~1.35 m, yet ALS d_true spans 2.12-21.38 m and only the "<4 m" bin touches the threshold | A | Obtain near-threshold real bins (d <~ 3 m), or drop the headline claim | OPEN |
| P5 | sigma_n = 0.15 is a placeholder, and the absolute floor value depends on it | R3 + A | Use the real `noise_stddev_corrected` | OPEN (data) |
| P6 | Semi-synthetic waveforms; no direct comparison with GEDI | R | GEDI L1B plus overlapping ALS, or the GEDI rebinning test (Section 7). Keep simulation as a control | OPEN |
| P7 | kappa / H_NWCS is an uncalibrated convention | R3 | State the operational scale. The design-rule range (sigma/Delta) provides a separate, measurable threshold | WRITE / OPEN |
| P8 | Eq. 7: the bound integrates over the prior range [0,D] and does not vanish near collapse (the "2.00 nats" is a fixed number); the Fano argument does not follow from this bound | A | Present Theorem 2 as a "certificate" together with measured tightness (E3); remove the "approaches zero" statement or restrict it to D <~ the collapse scale | WRITE |
| P9 | Algorithm line 5: `valleyfill(h * Perr)`, whereas the standard ZZ form is `h * valleyfill(Perr)` | A | Check in your own code. In simulation the paper form came out 7-16% larger (E5). Re-run Tables 4-6 with the standard form | OPEN (check own repo) |
| P10 | Fig. 4 caption "all converge / none crosses below": the networks sit ~3-10x above the floor (reading the figure's floor against Table 3); the oracle falls below the floor at d=0.30 (0.0290 vs. ~0.042); the Table 3 caption mentions the floor but there is no floor column | A | Correct the caption, add a floor column, and describe the oracle as a "known-centroid, separate setting". Compare estimators by prior-averaged MSE against the global ZZB (method E7) | WRITE |
| P11 | Fig. 3 / App. D encoder probe does not test the bound | A | Drop or recast | WRITE |
| P12 | GEDI Table 1 (3-6x error reduction, correlations) is not causal evidence for the mechanism | A | Remove as validation or replace with the rebinning test | OPEN |
| P13 | Undefined symbols; limitations placed in the appendix/end | R | Define in Section 2 first; move limitations to the abstract/introduction | WRITE |
| P14 | Related work: ToF multipath, resolution-limit literature, and Chan 2024 are absent | A | Chan 2024 has been read (Section 4). The rest (Gupta 2019, Fisher guidance 2022, Compressive SPC 2022, Fermat paths, Naik 2015, TöRF, Transient NeRF) are not yet read | PARTIAL |
| P15 | Theorem 2 is a composition of existing results (Fisher -> MI + DPI) | A | Novelty = application plus **measured tightness**, not a "new theorem" | WRITE |

### 1.3 Claim Ledger (Parts of the Paper)

Tier: A = solid and novel; B = sound but limited in novelty/scope; C = suggestive; D = drop. Currently **no tier A**.

| Component | Tier |
|---|---|
| Marginal (centroid-integrated) vs. Schur Fisher, 74% divergence near collapse (App. C) | B |
| Valley-filling max-selection bias in MC-ZZB (App. E) | B |
| Pointwise ZZHE (two-point, tight for d >~ 1.7 sigma) | B |
| Global ZZB tight vs. exact MMSE (E4) | B+ (real data pending) |
| ZZB (not Fisher/MI) predicts the design optimum (E2, E6, E8) | B/C (replication and real data pending) |
| Theorem 2 MI ceiling as a certificate | C |
| Swap-basin analogy (App. A) | C/D |
| GEDI 3-6x transition | C -> drop as validation |
| Encoder probe | D |

---------------------------------------------------------------------------------------------------

## 2. Common Model and Conventions (All Scripts)

- Waveform: two Gaussian returns, pulse ~ exp(-t^2/sigma^2) (RAISE convention; FWHM = 1.665 sigma). Equal weights.
- tau1 = c - d/2, tau2 = c + d/2. Centroid nuisance c ~ U[-3, 3] m (cw = 6). Default sigma_pulse = 1.35 m.
- Detector: integrate-and-dump bins (bin-average, closed form via erf). Window 24 m. Default bins 0.3 m (E3-E4) and 1.0 m (A3, design-rule runs).
- Noise: white Gaussian sigma_n (default 0.15, the RAISE placeholder). "Fixed energy" normalisation: amplitude A = (1.35/sigma)^0.5.
- Estimators: joint-ML grid search (d>=0), posterior mean (exact Bayes), sklearn MLP.
- **The photon-counting (Poisson) model from the memory file was not used here.** Everything is based on RAISE's Gaussian-waveform model.

Known limitations of the code: the d-grid step of 0.1 and the d>=0 constraint in `mse_ml` introduce boundary bias at small d (the CRB is not valid there); MC noise of a few percent; `fisher_marg` uses a posterior-weighted score with a numerical derivative; single seed.

---------------------------------------------------------------------------------------------------

## 3. Experiments (in Chat Order)

Core: `knob.py` = simulator (mu(), marginal Fisher F_D, joint-ML MSE, MI ceiling Eq. 6).

### E1. Knob Sweeps: `sweep.py`

**Motivation:** the question was whether F_D and the MI ceiling predict the optimum for the design knobs (pulse width, bin width, sampling). This is a first stress test.

**What is run:** metrics = 1/F_D (CRB-type), joint-ML MSE, MI ceiling, for d in {0.5, 1, 2}.
A1: pulse width (fixed peak, 0.15 m bins). A2: (fixed energy, 0.15 m bins). A3: (fixed energy, 1.0 m bins). B1: bin width (window fixed, noise^2 ~ 1/dt). C: fixed N=48 bins with the window T varied.

**Result (full table is obtained by running the script):**
- A1/A2: the narrower the pulse, the better. Monotone, no optimum.
- B1: no optimum in bin width. Flat up to Dt <= ~0.6 m (~0.44 sigma), degrades at 1.2 m.
- C: the window has an interior optimum at T ~ 6 m, equal to the prior width (cw=6).
- A3 (coarse bins): 1/F says the narrowest pulse is best, but the actual ML-MSE minimum is at sigma ~ 0.7. **This is where the design-rule lead originated.**

**Interpretation:**
- B1 is expected from the data-processing inequality: finer bins are never worse, so the optimum is at 0 and only a knee is found.
- The optimum in C ("cover the prior") is trivial.
- In A3, 1/F is wrong because the Fisher information is *local*. With coarse bins, a narrow pulse falls between bins and the likelihood becomes multimodal (global ambiguity), which Fisher cannot see.

**Caveat:** in C, at T=3 the ML-MSE is 0.72 and 1/F is 0.011; this may also be a failure of the ML estimator, and the ZZB was not run here. The fixed-peak-amplitude version of A3 was not run.

### E2. Verifying A3 with the ZZB: `zzb.py` + `sweep2.py`

**Motivation:** in E1, 1/F and the ML-MSE gave different optima. The aim was to determine which one the ZZB supports.

**What is run:** `zzb.py` = pointwise ZZB, **paper-form** valley-fill (`valleyfill(h*Pe)`), MC Bayes-optimal LR test, centroid marginalised. `sweep2.py` = A3 refinement plus extended window sweep.

**Result (d=1, 1.0 m bins, fixed energy, paper-form ZZB):**

| sigma | 1/F | L_ZZB | ML-MSE |
|---|---|---|---|
| 0.25 | 0.0106 | 0.0327 | 0.108 |
| 0.40 | 0.0108 | 0.0134 | 0.052 |
| 0.55 | 0.0120 | 0.0091 | 0.037 |
| **0.70** | 0.0181 | **0.0088** | **0.026** |
| 0.85 | 0.0245 | 0.0118 | 0.030 |
| 1.00 | 0.0380 | 0.0169 | 0.052 |
| 1.35 | 0.0904 | 0.0344 | 0.141 |

At d=2, the ZZB and ML also both have their minimum at sigma ~ 0.7. The MI ceiling also prefers a narrow pulse (sigma=0.4: 3.077 > sigma=0.7: 3.009).

**Interpretation:** the ZZB compares two distinct (c, d) hypotheses, so it captures the aliasing ambiguity. Fisher information and the MI ceiling derived from it cannot. This is the foundation of the entire design-rule claim.

**Caveat:** ZZB noise (nsim=500) and max-selection bias; sigma 0.55 vs. 0.7 is a statistical tie.

### E3. Tightness of the Theorem-2 Ceiling: `mi.py`

**Motivation:** the unknown tightness of the bound was identified as troubling. The true I(X;D) was computed by MC (uniform d prior on [0,D], 40 d-points x 50 c-points, nmc=1200) and compared with the Eq. 6 ceiling.

**Result:**

| sigma_n | D (m) | true MI (nats) | ceiling | ratio |
|---|---|---|---|---|
| 0.15 | 1 | 0.366 | 1.017 | 2.78 |
| 0.15 | 2 | 1.230 | 1.947 | 1.58 |
| 0.15 | 4 | 2.057 | 2.791 | 1.36 |
| 0.15 | 6 | 2.520 | 3.202 | 1.27 |
| 0.40 | 1 | 0.075 | 0.495 | 6.60 |
| 0.40 | 2 | 0.525 | 1.168 | 2.22 |
| 0.40 | 4 | 1.210 | 1.903 | 1.57 |
| 0.40 | 6 | 1.598 | 2.259 | 1.41 |

**Interpretation:**
- The bound is valid (above the true MI in every case).
- The absolute gap is ~0.4-0.8 nats, so in the bulk (D>=4) the ratio is 1.3-1.6x. In the collapse regime (D~1, noisy) the true MI is ~0.1 nats while the ceiling is ~0.5, a ratio of 6.6x. Conjecture: slack from the "+1" in `ln(1+x)` (not verified).
- That is, the bound is weakest exactly where the paper's headline claim lies, and it is useless for design (E1/E2).
- Regarding the D-dependence of Eq. 7: it does not vanish at collapse (0.5-1.0 nats even at D=1).

**Caveat:** the MC error of the true MI is ~ +-0.03-0.05 nats; the value of 0.075 for D=1, sigma_n=0.4 is near the noise level.

**Lead:** the ratio ceiling/true as a function of (D, sigma_n) could become an honest figure, converting a limitation into a result.

### E4. Global ZZB vs. Exact Bayes-MMSE: `gzzb.py` (Most Important)

**Motivation:** a direct fix for P1/P3. The global ZZB (uniform prior on d) is valid for every estimator and needs no local homogeneity. The question: how tight is it?

**What is run:** global ZZB (Bellini-Tartara form), A(h) = (2/D)(D-h) Pe(h); bound = integral of (h/2) V{A}(h). MMSE = posterior-mean estimator, 61 d-grid x 40 c-grid, n=2500.

**Result:**

| sigma_n | D | ZZB | MMSE (SE) | MMSE/ZZB |
|---|---|---|---|---|
| 0.15 | 2 | 0.0254 | 0.0291 (0.0010) | 1.14 |
| 0.15 | 4 | 0.0146 | 0.0214 (0.0009) | 1.47 |
| 0.15 | 6 | 0.0113 | 0.0179 (0.0007) | 1.58 |
| 0.40 | 2 | 0.1045 | 0.1218 (0.0038) | 1.16 |
| 0.40 | 4 | 0.0943 | 0.1001 (0.0031) | 1.06 |
| 0.40 | 6 | 0.0928 | 0.1058 (0.0035) | 1.14 |

With and without valley-filling the results are almost identical (A(h) is already monotone).

**Interpretation:** the ZZB is always below the MMSE (sanity check), with a gap of 1.06-1.58x versus the paper's 1000x. The reviewers' biggest objection (tightness plus homogeneity) disappears in the simulated setting. **The estimator-agnostic claim survives in its correct form** (global Bayesian); it need not be dropped.

**Caveat:** this is a Bayesian statement (prior on d), not a pointwise conditional MSE. The MMSE uses the exact likelihood (the model-correct best case). Tightness on real data is not demonstrated.

### E5. Algorithm Line-5 Check: `zzb2.py`

**Motivation:** Algorithm line 5 states `valleyfill(h*Perr)`. The standard form is `h*V{Perr}`, and since max_{h'>=h} h'P(h') >= h * max P(h'), the paper form can exceed the bound.

**Result (pointwise, sigma=1.35, 0.3 m bins, sigma_n=0.15):**

| d | paper-form | standard | ratio |
|---|---|---|---|
| 0.3 | 0.03048 | 0.02617 | 1.16 |
| 1.0 | 0.00906 | 0.00843 | 1.07 |
| 2.0 | 0.00518 | 0.00482 | 1.07 |
| 3.0 | 0.00615 | 0.00570 | 1.08 |

A3 recheck (standard form, d=1, 1.0 m bins): sigma 0.25/0.4/0.55/0.7/0.85/1.0/1.35 -> 0.0244 / 0.0117 / 0.0074 / 0.0077 / 0.0107 / 0.0136 / 0.0290. The minimum is at sigma 0.55-0.7, so the E2 optimum is retained.

**Interpretation:** the gap is small, but it raises a question about the validity of the bound. **Check which form is implemented in your own code.** If it is the paper form, re-run Tables 4-6 with the standard form.

### E6. Basis of the Design Rule Within the Bound: `rule.py`

**Motivation:** the question was whether the rule can be derived from the bound itself.

**Idea:** the error of the ZZB test (d vs. d+h, centroid marginalised) is determined mostly by one deterministic quantity: the centroid-invariant signature distance rho(d,h) = min over c,c' of || mu(c,d) - mu(c',d+h) ||, with Pe ~ Q(rho / 2 sigma_n). Surrogate bound = 0.5 * integral of h * V{Q(rho/2sigma_n)}. No MC is needed.

**Result (d=1, sigma_n=0.15):**

| Bin Delta (m) | ZZB optimum sigma (sigma/Delta) | Surrogate optimum (sigma/Delta) | Spearman |
|---|---|---|---|
| 0.5 | 0.30 (0.6) | 0.40 (0.8) | 0.79 |
| 1.0 | 0.70 (0.7) | 0.70 (0.7) | 0.89 |
| 2.0 | 1.20 (0.6) | 1.60 (0.8) | 0.89 |

**Interpretation:** the ZZB optimum is sigma/Delta ~0.6-0.7 for all three Delta, so the rule scales (FWHM ~ 1.1 x Delta). Mechanism: when bins are coarse, the sampled shape changes with the centroid (aliasing) and the min-over-c distance falls; if the pulse is too wide, resolution is lost.

**Caveat:** the surrogate is not a bound (2-4x above the ZZB at narrow sigma) and is for ranking only. 7-point sigma grid, d=1, single seed.

### E7. Room for a New Model: `netroom.py`

**Motivation:** the idea of an info-budget-inspired model/attention/tokens. First it is necessary to ask how far a plain network is from the exact best estimator.

**What is run:** sklearn MLP (128,128), 80k prior-sampled waveforms, MSE loss, D=4, 3000 test samples, exact MMSE on the same test set.

**Result:**

| sigma_n | MLP MSE | exact MMSE | MLP/MMSE | MLP/ZZB (from E4) |
|---|---|---|---|---|
| 0.15 | 0.0276 | 0.0208 | 1.32 | ~1.9 |
| 0.40 | 0.1369 | 0.1043 | 1.31 | ~1.4 |

**Interpretation:** in the in-prior, well-specified simulated setting, a simple MLP is within ~1.3x of the best possible (early-stopped and undertrained, so the gap may shrink further). Architecture accounts for at most ~30%. Attention/info-budget tokens cannot be the headline here.

**Caveat:** only an MLP was run (torch was unavailable, so no CNN/transformer), single seed. Room may exist where a plain net breaks down: prior/pulse/noise shift, model misspecification, few labels. This has not yet been tested.

### E8. Toward a Closed Form, and SNR Scaling: `closed.py`

**Motivation:** a closed form and some real validation will be required. Three building blocks.

**(1) Aliasing amplitude law.** Phase modulation of sum_k mu_k^2 for a single pulse: m(sigma/Delta) = (Emax-Emin)/(Emax+Emin).
Result: m = 0.33 (0.25), 0.19 (0.50), 0.09 (0.65), 0.03 (0.80). Fit: ln m = -4.17 (sigma/D)^2 - 0.71 (m ~ 0.49 exp(-4.17 (sigma/D)^2)). Theoretical slope: -pi^2/2 = -4.93 (the remaining difference is attributable to box-blur sinc).
**Correction:** an alias term exp(-pi^2 sigma^2 / Delta^2) had been conjectured earlier. That exponent was off by ~2x. (The script uses two coincident pulses at `d=0`, which does not affect the relative modulation.)

**(2) Noise-free optimum (from rho).** Fixed energy, Delta=1: at d=1, for h = 0.1/0.2/0.4/0.8/1.6/3.2 the optimum sigma/Delta = 0.75/0.75/0.70/0.70/0.80/1.40; at d=2, 0.80/0.80/0.80/0.75/0.80/0.85. In other words, geometry mostly fixes the optimum at ~0.7-0.8.

**(3) SNR scaling (d=1, Delta=1):**

| sigma_n | ZZB-MC optimum sigma/Delta | surrogate optimum |
|---|---|---|
| 0.08 | 0.5 (flat 0.5-0.7) | 0.70 |
| 0.15 | 0.6 | 0.70 |
| 0.30 | 0.6 (flat 0.6-0.8) | 0.80 |
| 0.60 | 0.9 | 0.95 |

ZZB values (sigma/Delta = 0.35, 0.5, 0.6, 0.7, 0.8, 0.9, 1.1): sigma_n=0.15 -> 0.0138, 0.0080, 0.0075, 0.0082, 0.0099, 0.0113, 0.0189.

**Interpretation:**
- As noise increases, the optimum moves toward a wider pulse (the relevant offset h grows and the optimum follows it; plausible, not proven).
- **The basin is shallow:** within +-0.15 of the optimum the ZZB changes by ~10-20%; at sigma/Delta = 0.35 or 1.1 it is 1.8-2.5x worse. The practical rule is therefore a range: **sigma/Delta in [0.5, 0.9], FWHM ~ 0.8-1.5 x Delta.** A razor-sharp closed form is probably unnecessary.
- A realistic closed form = the aliasing law (analytic via Poisson summation) plus Q(rho/2sigma_n), giving an implicit equation and a one-line fit. Whether a fully explicit formula exists is unknown.

**Caveat:** because of ZZB MC noise, the argmin is not reliable in low-noise cases (flat basin). d=1 only. Single seed.

---------------------------------------------------------------------------------------------------

## 4. Literature Positioning

**Chan et al., CVPR 2024, "Resolution Limit of Single-Photon LiDAR"** (read from the NSF PAR copy):
- Knob = spatial pixel count N (resolution vs. per-pixel SNR at fixed flux). MSE = bias (spatial discretisation) + variance (photon noise); closed-form optimum N* ~ (sqrt(alpha0)*||c|| / sigma_t)^(1/2).
- A single return per pixel; multipath is not assumed. Variance comes from the CRB/ML (unbiased); the paper itself notes that advanced post-processing could beat the bound.
- Simulation plus real SPAD data; however, no valley appeared in the real data (the optimum lies beyond the sensor resolution), so the real-data prediction of the optimum was not tested, only the curve trend.

| | Chan 2024 | This work's rule |
|---|---|---|
| Knob | pixel count N | pulse width vs. bin width |
| Problem | single return | two overlapping returns |
| Mechanism | bias-variance (classical) | aliasing (classical matched sampling) |
| Closed form | yes | not yet |
| Basis | CRB/ML, unbiased | global ZZB, valid for every estimator, 1.06-1.58x of MMSE |
| Real data | partial | none |

**Verdict:** as a rule package, Chan et al. is more novel and complete. The real edge of this work: their variance term is CRB-based, and in E1/E2 the CRB-type 1/F says "the narrower the better" while the ZZB and ML show a U-shape. "CRB-based design rules miss this problem's optimum, whereas a tight global bound gives the correct optimum" is a defensible contribution. The two problems are complementary (Chan: spatial; this work: temporal two-return, which they exclude).

**Not read (unverified):** Gupta et al. CVPR 2019 (photon-flooded), Fisher-Information Guidance (CVPR 2022), Compressive Single-Photon 3D (CVPR 2022), Theory of Fermat Paths (CVPR 2019), Naik 2015, Fuentes-Jimenez 2012, Su 2018, TöRF, Transient NeRF, PlatoNeRF, Malik 2025. Verify before citing; the related-work section must explicitly state how this work differs from the multipath-correction literature.

---------------------------------------------------------------------------------------------------

## 5. Promising Leads (Ranked)

| # | Lead | Evidence | What could kill it |
|---|---|---|---|
| L1 | Global ZZB as a tight, assumption-free floor | E4: 1.06-1.58x | The ratio becomes large on real or misspecified data |
| L2 | ZZB-based design rule (sigma/Delta in [0.5,0.9]); CRB/MI miss it | E1, E2, E5, E6, E8 | The optimum disappears with d, sigma_n, weights, or fixed-peak normalisation |
| L3 | Semi-closed-form sigma*/Delta from the aliasing law | E8 | The derivation does not fit, or the optimum is so shallow that it makes no difference |
| L4 | GEDI rebinning test (real waveforms, real pulse, real noise) | Not yet run | The knee does not appear at the predicted location |
| L5 | MI-ceiling tightness map as an honest figure | E3 | -- (low risk, low impact) |
| L6 | Sensor-config-conditioned estimator / information-weighted sampling | Conceptual only | A plain net matches the Bayes estimator under the shift test |

**Weak / dead (on current evidence):**
- MI ceiling (Theorem 2) as a design tool: gives the wrong optimum in E1/E2.
- Pulse width or bin width as a standalone knob: monotone or only a knee.
- Fisher-weighted attention: it is a matched filter, and the net learns it by itself (indirectly from E7).
- Making a "new model" the headline in the in-prior simulated setting: ~30% room (E7).
- The LSTM/Transformer vanishing-gradient analogy: that is an optimisation problem, whereas here the issue is information loss at the sensor (DPI). The only loose analogy: near collapse the score variance F_D -> 0, so the training signal weakens; the fix is sampling/loss weighting, not architecture.

---------------------------------------------------------------------------------------------------

## 6. What Has Been Tried for CVPR

| Direction | What was done | Verdict |
|---|---|---|
| Tight floor | Global ZZB vs. MMSE (E4), MI-ceiling tightness (E3) | Needed, but not a standalone headline; real-data consistency outstanding |
| Sensor design rule | Knob sweeps, ZZB check, surrogate, SNR scaling (E1, E2, E5, E6, E8) | Most promising; a classical rule, with novelty = "a tight bound predicts it, the CRB does not" |
| New model / tokens | Plain-net room test (E7) | ~30% room in in-prior simulation; shift/misspecification test pending |
| Training method | Conceptual (info-weighted sampling) | Untested |
| Literature gap | Comparison with Chan 2024 | Closed form plus real-data curve are the conditions for reaching their bar |

**Recommended storyline (on current evidence):** "A tight, assumption-free information bound that predicts the sampling design rule where CRB-based criteria fail", with the gap between learned estimators and the bound as an ablation.

---------------------------------------------------------------------------------------------------

## 7. Next Steps and Go/No-Go Gates

1. **Analytic derivation of the aliasing law** (Poisson summation) -> semi-closed-form sigma*/Delta. Kill criterion: a large mismatch between the derived and measured m(sigma/Delta).
2. **Robustness of the rule:** d in {0.5, 2}, sigma_n, weights (w != 0.5), fixed-peak normalisation, point-sampling detector, finer sigma grid, multiple seeds.
3. **GEDI rebinning test (real data):** re-bin GEDI waveforms to coarser Delta and examine error vs. Delta. Prediction: GEDI has sigma=1.35 m and Delta=0.15 m (sigma/Delta ~ 9, oversampled), so error should be ~flat until sigma/Delta ~1.5-2 (Delta ~ 0.7-0.9 m) and then degrade rapidly. This is falsifiable. (GEDI data cannot be downloaded in the sandbox; the script is still to be written.)
4. **Own ALS semi-synthetic pipeline** with the real `noise_stddev_corrected` and varying Delta; increase the number of near-threshold bins (d <~ 3 m).
5. **Shift/misspecification test (for the model idea):** train the net on one configuration, test on a shifted prior/pulse/noise, and compare with the Bayes estimator (correct parameters). If the plain net matches Bayes, close the model direction.
6. **Public SPAD datasets** (availability not yet checked).

**Honest limit:** no option provides "fully real two-return ground truth". Moreover, GEDI's pulse is hardware-fixed, so on real data the pulse width can only be broadened (by convolution), not narrowed; Delta is varied by rebinning.

---------------------------------------------------------------------------------------------------

## 8. Files and How to Run Them

| # | File | Contents |
|---|---|---|
| 1 | knob.py | Core simulator |
| 2 | sweep.py | E1 |
| 3 | zzb.py | Pointwise ZZB, paper form (E2) |
| 4 | sweep2.py | E2 |
| 5 | mi.py | E3 |
| 6 | gzzb.py | E4 (now import-safe) |
| 7 | zzb2.py | E5 (now import-safe, `both()` function) |
| 8 | rule.py | E6 |
| 9 | netroom.py | E7 |
| 10 | closed.py | E8 |

`python sweep.py; python sweep2.py; python mi.py; python gzzb.py; python zzb2.py; python rule.py; python netroom.py; python closed.py`

Notes: `np.trapezoid` requires NumPy>=2.0 (use `np.trapz` on older versions); netroom requires sklearn; each script takes a few minutes on a single CPU core; seeds are fixed in every file. `gzzb.py` and `zzb2.py` now run inside `if __name__ == "__main__"`, so `rule.py` no longer re-runs the experiment on import.

---------------------------------------------------------------------------------------------------

## 9. What Has NOT Been Done (Honestly)

- Any real-data test (GEDI/ALS/SPAD) in this follow-up.
- Fixed-peak-amplitude pulse-width sweep; point-sampling detector; scaling in d or weights; multiple seeds.
- ZZB-vs-ML check on the window knob (C).
- CNN/transformer baselines (torch was unavailable).
- Closed-form derivation.
- This follow-up on the photon-counting (Poisson) model.
- Literature: nothing read beyond Chan 2024.
