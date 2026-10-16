# RAISE -> CVPR: follow-up experiments, interpretations, leads

Status: 2026-10-16. Sab experiments **simulation** hain, ek seed, mere assumed model pe (section 2). Real data pe abhi kuch bhi saabit nahi hua. Isko paper ke numbers ki tarah quote karne se pehle apne code mein replicate karo.

---------------------------------------------------------------------------------------------------

## 0. TL;DR

1. Original paper reject isliye hua ki **claims evidence se bade the**, math galat nahi nikla (reviewers ka khud ka kehna: "maths are not incorrect, main text oversells").
2. Sim mein jo ab kaafi ache se dikha:
   - **Global Ziv-Zakai bound** (d pe prior ke saath) har estimator ke liye valid hai, local-homogeneity assumption ke bina, aur exact Bayes-MMSE ke **1.06-1.58x** ke andar hai. Yeh "provably tight floor" ka sabse seedha route hai.
   - **Fisher/CRB aur Theorem-2 ka MI ceiling design optimum miss karte hain; ZZB pakadta hai.** Fixed bins pe pulse width ka interior optimum sigma/Delta ~ 0.5-0.9 (centre ~0.65-0.7), noise badhne pe optimum chauda hota hai.
   - Plain MLP exact MMSE ke ~1.3x ke andar aa jaata hai -> naye architecture ke liye in-prior simulated setting mein ~30% se zyada jagah nahi.
3. Chan et al. CVPR 2024 se tulna: unka package (closed form + real-data curve) abhi zyada complete hai. Tumhari edge: **CRB-based design analysis is problem ka optimum miss karta hai, tight global bound nahi.**
4. Missing: closed-form sigma*/Delta, aur koi bhi real-data test. Yahi gate hai.

---------------------------------------------------------------------------------------------------

## 1. Reviews ka analysis: original paper mein kya dikkatein thin, ab kaise resolve hongi

### 1.1 Reviews ka saar

| Reviewer | Recommendation | Main points |
|---|---|---|
| Reviewer (pehla, unnamed) | Reject; soundness "mostly no" | (a) "estimator-agnostic floor" overclaim, kyunki ZZHE two-point average hai aur local-homogeneity assumption pe tika hai; (b) headroom = upper bound on *possible improvement*, floor "unrecoverable error" nahi; (c) floor observed error se ~1000x chhota -> paper jo dikhana chahta tha uske ulta; (d) 3DEP ko actual GEDI products (overlapping footprints) se compare karo, simulation ko control rakho; (e) symbols (tau, x, I(theta)) pehle define karo |
| Reviewer #3 | Weak Reject; soundness "mostly yes" | Claims validation se bade; local-homogeneity assumption; threshold (kappa) calibrated nahi; real-world validation semi-synthetic; framework/diagnostic ki tarah present karo; assumptions aur limitations main text mein; validation claims soften karo |
| Meta-reviewer | Reject | Topic highly relevant, REO-2 community ke liye interesting; dono reviewers ko claims ke support pe major concern |

Dhyan do: yeh **workshop** review hai (reviews mein "unsuitable for the workshop"), NeurIPS main track nahi. Aur kisi ne topic ko irrelevant ya idea ko galat nahi kaha.

### 1.2 Issue register (reviewers + mera audit)

"Source" mein R = reviewer ne pakda, A = mere audit mein mila (reviewers ne nahi bola).
Status: SIM-DONE = simulation mein resolve/test ho gaya; WRITE = sirf likhne ka kaam; OPEN = data/experiment baaki.

| # | Issue | Source | Resolution plan | Status |
|---|---|---|---|---|
| P1 | "Estimator-agnostic floor" overclaim; pointwise ZZB local homogeneity pe tika hai | R | Estimator-agnostic claim **global ZZB** (prior on d) pe rakho, jo har estimator ke liye valid hai. Pointwise version ka naam "two-point lower bound under local homogeneity", assumption main text mein. Evidence: E4 | SIM-DONE + WRITE |
| P2 | Headroom ka galat interpretation | R | Headroom = Lcurrent - L = "maximum improvement jo rule out nahi hua", fundamental error nahi. "Separates fixable from fundamental" hatao | WRITE |
| P3 | Floor ~1000x loose real data pe -> headroom vacuous | R | Tightness claim sirf wahan jahan dikhi. Paper ke Table 5 se: d>=1.7 pe MLE floor ke 1.57-1.96x ke andar; d<=1.0 pe 1.5x se ~60x (yahan MLE swap-basin se bhi fail hota hai, to gap floor ka hai ya estimator ka, alag nahi kiya ja sakta). Global ZZB vs exact MMSE: 1.06-1.58x (E4) | SIM-DONE; real data OPEN |
| P4 | Real validation galat regime mein: threshold ~sigma_pulse ~1.35 m, par ALS d_true 2.12-21.38 m, sirf "<4 m" bin threshold ko chhoota hai | A | Near-threshold real bins (d <~ 3 m) chahiye, ya headline claim hatao | OPEN |
| P5 | sigma_n = 0.15 placeholder, floor ka absolute value isi pe depend | R3 + A | Real `noise_stddev_corrected` use karo | OPEN (data) |
| P6 | Semi-synthetic waveforms, GEDI se direct comparison nahi | R | GEDI L1B + overlapping ALS, ya GEDI rebinning test (section 7). Simulation control ke taur pe rakho | OPEN |
| P7 | kappa / H_NWCS uncalibrated convention | R3 | Operational scale likho. Design-rule range (sigma/Delta) ek alag, measurable threshold deta hai | WRITE / OPEN |
| P8 | Eq. 7: bound prior range [0,D] pe integrate hota hai, collapse ke paas zero nahi hota ("2.00 nats" fixed number); Fano wali line is bound se follow nahi karti | A | Theorem 2 ko "certificate" bana ke measured tightness ke saath do (E3), "approaches zero" line hatao ya D <~ collapse scale tak limit karo | WRITE |
| P9 | Algorithm line 5: `valleyfill(h * Perr)`, jabki standard ZZ form `h * valleyfill(Perr)` hai | A | Apne code mein check karo. Meri sim mein paper-form 7-16% bada nikla (E5). Standard form use karke Tables 4-6 dubara chalao | OPEN (apne repo mein check) |
| P10 | Fig 4 caption "all converge / none crosses below": nets floor se ~3-10x upar hain (Table 3 ke saath figure ka floor padh ke); Oracle d=0.30 pe floor ke neeche (0.0290 vs ~0.042); Table 3 caption floor ka zikr karta hai par floor column hai nahi | A | Caption sach likho, floor column add karo, oracle ko "known-centroid, alag setting" likho. Estimators ko prior-averaged MSE vs global ZZB pe compare karo (method E7) | WRITE |
| P11 | Fig 3 / App. D encoder-probe bound test nahi karta | A | Drop ya recast | WRITE |
| P12 | GEDI Table 1 (3-6x error reduction, correlations) mechanism ka causal saboot nahi | A | Validation ke taur pe hatao ya rebinning test se replace karo | OPEN |
| P13 | Undefined symbols, limitations appendix/end mein | R | Section 2 mein pehle define; limitations abstract/intro mein | WRITE |
| P14 | Related work: ToF multipath, resolution-limit literature, Chan 2024 absent | A | Chan 2024 padha (section 4). Baaki (Gupta 2019, Fisher-guidance 2022, Compressive SPC 2022, Fermat paths, Naik 2015, TöRF, Transient NeRF) abhi padhe nahi | PARTIAL |
| P15 | Theorem 2 existing results ki composition (Fisher->MI + DPI) hai | A | Novelty = application + **measured tightness**, na ki "naya theorem" | WRITE |

### 1.3 Claim ledger (paper ke hisse)

Tier: A solid+novel, B sound par novelty/scope limited, C suggestive, D drop. Abhi **koi A nahi**.

| Hissa | Tier |
|---|---|
| Marginal (centroid-integrated) vs Schur Fisher, 74% divergence near collapse (App. C) | B |
| Valley-filling max-selection bias in MC-ZZB (App. E) | B |
| Pointwise ZZHE (two-point, d >~ 1.7 sigma pe tight) | B |
| Global ZZB tight vs exact MMSE (E4) | B+ (real data pending) |
| ZZB (not Fisher/MI) predicts design optimum (E2, E6, E8) | B/C (replicate + real data pending) |
| Theorem 2 MI ceiling as certificate | C |
| Swap-basin analogy (App. A) | C/D |
| GEDI 3-6x transition | C -> drop as validation |
| Encoder probe | D |

---------------------------------------------------------------------------------------------------

## 2. Common model aur conventions (sab scripts)

- Waveform: do Gaussian returns, pulse ~ exp(-t^2/sigma^2) (RAISE convention; FWHM = 1.665 sigma). Equal weights.
- tau1 = c - d/2, tau2 = c + d/2. Centroid nuisance c ~ U[-3, 3] m (cw = 6). sigma_pulse = 1.35 m default.
- Detector: integrate-and-dump bins (bin-average, closed form via erf). Window 24 m. Default bins 0.3 m (E3-E4), 1.0 m (A3, design-rule runs).
- Noise: white Gaussian sigma_n (default 0.15, RAISE ka placeholder). "Fixed energy" normalisation: amplitude A = (1.35/sigma)^0.5.
- Estimators: joint-ML grid search (d>=0), posterior mean (exact Bayes), sklearn MLP.
- **Memory-file wala photon-counting (Poisson) model yahan use nahi hua.** Yeh sab RAISE ke Gaussian-waveform model pe hai.

Code ki known limitations: `mse_ml` ka d-grid step 0.1 aur d>=0 constraint small d pe boundary bias deta hai (CRB wahan valid nahi); MC noise kuch percent; `fisher_marg` posterior-weighted score + numerical derivative; ek seed.

---------------------------------------------------------------------------------------------------

## 3. Experiments (chat order mein)

Core: `knob.py` = simulator (mu(), marginal Fisher F_D, joint-ML MSE, MI ceiling Eq. 6).

### E1. Knob sweeps: `sweep.py`

**Kyun:** tumne poocha ki design knob (pulse width, bin width, sampling) ke liye F_D / MI ceiling optimum predict karte hain ya nahi. Pehle brutal check.

**Kya chalta hai:** metrics = 1/F_D (CRB-type), joint-ML MSE, MI ceiling, d in {0.5, 1, 2}.
A1 pulse width (fixed peak, 0.15 m bins), A2 (fixed energy, 0.15 m bins), A3 (fixed energy, 1.0 m bins), B1 bin width (window fixed, noise^2 ~ 1/dt), C fixed N=48 bins aur window T vary.

**Result (poora table script chalake lo):**
- A1/A2: pulse jitna narrow, utna achha. Monotone, koi optimum nahi.
- B1: bin width pe optimum nahi. Dt <= ~0.6 m (~0.44 sigma) tak flat, 1.2 m pe bigadta hai.
- C: window ka interior optimum T ~ 6 m, yaani prior width (cw=6) ke barabar.
- A3 (coarse bins): 1/F kehta hai narrowest pulse best, par actual ML-MSE ka minimum sigma ~ 0.7 pe hai. **Yahin se design-rule ka lead nikla.**

**Interpretation:**
- B1 data-processing inequality se expected hai: finer bins kabhi worse nahi, to optimum 0 hai, sirf knee milti hai.
- C ka optimum "prior ko cover karo" hai, trivial.
- A3 mein 1/F galat isliye hai ki Fisher *local* hai. Coarse bins pe narrow pulse bins ke beech girta hai aur likelihood multimodal ho jaata hai (global ambiguity), jo Fisher nahi dekh sakta.

**Caveat:** C mein T=3 pe ML-MSE 0.72 aur 1/F 0.011; yeh ML estimator ka failure bhi ho sakta hai, ZZB yahan chalaya nahi gaya. Fixed-peak-amplitude A3 chalaya nahi.

### E2. A3 ko ZZB se verify: `zzb.py` + `sweep2.py`

**Kyun:** E1 mein 1/F aur ML-MSE alag optimum de rahe the. Pata karna tha ki ZZB kiski taraf hai.

**Kya:** `zzb.py` = pointwise ZZB, **paper-form** valley-fill (`valleyfill(h*Pe)`), MC Bayes-optimal LR test, centroid marginalised. `sweep2.py` = A3 refine + window sweep extend.

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

d=2 pe bhi ZZB aur ML dono sigma ~ 0.7 pe minimum dete hain. MI ceiling bhi narrow pulse prefer karta hai (sigma=0.4: 3.077 > sigma=0.7: 3.009).

**Interpretation:** ZZB do alag (c, d) hypotheses compare karta hai, isliye aliasing wali ambiguity pakadta hai. Fisher aur uska derived MI ceiling nahi pakad paate. Yeh poore design-rule claim ki neev hai.

**Caveat:** ZZB noise (nsim=500) aur max-selection bias; sigma 0.55 vs 0.7 statistical tie.

### E3. Theorem-2 ceiling kitna tight hai: `mi.py`

**Kyun:** "bound kitna tight hai woh unknown hai" tumhe troubling lag raha tha. True I(X;D) ko MC se nikala (uniform d prior [0,D], 40 d-points x 50 c-points, nmc=1200) aur Eq. 6 ke ceiling se compare kiya.

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
- Bound valid hai (har case mein true MI ke upar).
- Absolute gap ~0.4-0.8 nats, to bulk (D>=4) mein ratio 1.3-1.6x. Collapse regime (D~1, noisy) mein true MI ~0.1 nats par ceiling ~0.5 -> ratio 6.6x. Mera guess: `ln(1+x)` ka "+1" slack (verify nahi kiya).
- Yaani bound wahan sabse kamzor hai jahan paper ka headline claim hai, aur design ke liye bekaar (E1/E2).
- Eq. 7 ki D-dependence: collapse pe yeh zero nahi hota (D=1 pe bhi 0.5-1.0 nats).

**Caveat:** true MI ka MC error ~ +-0.03-0.05 nats; D=1, sigma_n=0.4 wala 0.075 noise ke paas hai.

**Lead:** ceiling/true vs (D, sigma_n) ek honest figure ban sakta hai, jo limitation ko result mein badal deta hai.

### E4. Global ZZB vs exact Bayes-MMSE: `gzzb.py` (sabse important)

**Kyun:** P1/P3 ka seedha fix. Global ZZB (d pe uniform prior) har estimator pe valid hai, local-homogeneity ki zaroorat nahi. Poochha: kitna tight hai?

**Kya:** global ZZB (Bellini-Tartara form), A(h) = (2/D)(D-h) Pe(h); bound = integral of (h/2) V{A}(h). MMSE = posterior-mean estimator, 61 d-grid x 40 c-grid, n=2500.

**Result:**

| sigma_n | D | ZZB | MMSE (SE) | MMSE/ZZB |
|---|---|---|---|---|
| 0.15 | 2 | 0.0254 | 0.0291 (0.0010) | 1.14 |
| 0.15 | 4 | 0.0146 | 0.0214 (0.0009) | 1.47 |
| 0.15 | 6 | 0.0113 | 0.0179 (0.0007) | 1.58 |
| 0.40 | 2 | 0.1045 | 0.1218 (0.0038) | 1.16 |
| 0.40 | 4 | 0.0943 | 0.1001 (0.0031) | 1.06 |
| 0.40 | 6 | 0.0928 | 0.1058 (0.0035) | 1.14 |

Valley-fill ke saath/bina almost same (A(h) already monotone).

**Interpretation:** ZZB hamesha MMSE ke neeche (sanity), gap 1.06-1.58x vs paper ka 1000x. Reviewer ka sabse bada objection (tightness + homogeneity) simulated setting mein khatam. **Estimator-agnostic claim sahi form mein bachi hai** (global Bayesian), dropna zaroori nahi.

**Caveat:** Bayesian statement hai (prior on d), pointwise conditional MSE nahi. MMSE exact likelihood use karta hai (model-correct best case). Real data pe tightness saabit nahi.

### E5. Algorithm line-5 check: `zzb2.py`

**Kyun:** Algorithm line 5 `valleyfill(h*Perr)` likhta hai. Standard form `h*V{Perr}` hai, aur max_{h'>=h} h'P(h') >= h * max P(h') hota hai, to paper-form bound se bada ho sakta hai.

**Result (pointwise, sigma=1.35, 0.3 m bins, sigma_n=0.15):**

| d | paper-form | standard | ratio |
|---|---|---|---|
| 0.3 | 0.03048 | 0.02617 | 1.16 |
| 1.0 | 0.00906 | 0.00843 | 1.07 |
| 2.0 | 0.00518 | 0.00482 | 1.07 |
| 3.0 | 0.00615 | 0.00570 | 1.08 |

A3 recheck (standard form, d=1, 1.0 m bins): sigma 0.25/0.4/0.55/0.7/0.85/1.0/1.35 -> 0.0244 / 0.0117 / 0.0074 / 0.0077 / 0.0107 / 0.0136 / 0.0290. Minimum sigma 0.55-0.7, E2 wala optimum bacha rehta hai.

**Interpretation:** gap chhota hai par bound ki validity ka sawaal hai. **Apne code mein dekho ki kaunsa form implement hai.** Agar paper-form hai to Tables 4-6 standard form pe dubara chalao.

### E6. Design rule ka basis bound ke andar: `rule.py`

**Kyun:** tumne poocha ki rule bound se hi derive ho sakta hai ya nahi.

**Idea:** ZZB ke test (d vs d+h, centroid marginalised) ki error mostly ek deterministic quantity decide karti hai: centroid-invariant signature distance rho(d,h) = min over c,c' of || mu(c,d) - mu(c',d+h) ||, aur Pe ~ Q(rho / 2 sigma_n). Surrogate bound = 0.5 * integral of h * V{Q(rho/2sigma_n)}. MC nahi lagta.

**Result (d=1, sigma_n=0.15):**

| Bin Delta (m) | ZZB optimum sigma (sigma/Delta) | Surrogate optimum (sigma/Delta) | Spearman |
|---|---|---|---|
| 0.5 | 0.30 (0.6) | 0.40 (0.8) | 0.79 |
| 1.0 | 0.70 (0.7) | 0.70 (0.7) | 0.89 |
| 2.0 | 1.20 (0.6) | 1.60 (0.8) | 0.89 |

**Interpretation:** ZZB ka optimum sigma/Delta ~0.6-0.7 teeno Delta pe -> rule scale karta hai (FWHM ~ 1.1 x Delta). Mechanism: bins coarse hon to centroid ke saath sampled shape badalta hai (aliasing) aur min-over-c distance gir jaati hai; pulse zyada chauda ho to resolution jaati hai.

**Caveat:** surrogate bound nahi hai (narrow sigma pe ZZB se 2-4x upar), sirf ranking ke liye. 7-point sigma grid, d=1, ek seed.

### E7. Naye model ke liye jagah: `netroom.py`

**Kyun:** tumhara idea: info-budget se inspired model/attention/tokens. Pehle poochna zaroori: plain network exact best estimator se kitna door hai?

**Kya:** sklearn MLP (128,128), 80k prior-sampled waveforms, MSE loss, D=4, test 3000 samples, exact MMSE usi test set pe.

**Result:**

| sigma_n | MLP MSE | exact MMSE | MLP/MMSE | MLP/ZZB (E4 se) |
|---|---|---|---|---|
| 0.15 | 0.0276 | 0.0208 | 1.32 | ~1.9 |
| 0.40 | 0.1369 | 0.1043 | 1.31 | ~1.4 |

**Interpretation:** in-prior, well-specified simulated setting mein simple MLP best-possible ke ~1.3x ke andar hai (early-stopped, undertrained, to gap aur ghat sakta hai). Architecture se zyada se zyada ~30% ka sawaal. Attention/info-budget tokens yahan headline nahi bana sakte.

**Caveat:** sirf MLP (torch nahi tha, CNN/transformer nahi chale), ek seed. Jagah wahan ho sakti hai jahan plain net toot-ta hai: prior/pulse/noise shift, model misspecification, kam labels. Abhi test nahi hua.

### E8. Closed-form ki taraf + SNR scaling: `closed.py`

**Kyun:** tumne kaha closed form aur real validation ka kuch karna hoga. Teen building blocks.

**(1) Aliasing amplitude law.** Single pulse ke sum_k mu_k^2 ka phase modulation m(sigma/Delta) = (Emax-Emin)/(Emax+Emin).
Result: m = 0.33 (0.25), 0.19 (0.50), 0.09 (0.65), 0.03 (0.80). Fit: ln m = -4.17 (sigma/D)^2 - 0.71 (m ~ 0.49 exp(-4.17 (sigma/D)^2)). Theory slope -pi^2/2 = -4.93 (box-blur sinc baaki fark deta hai).
**Correction:** pehle maine alias term exp(-pi^2 sigma^2 / Delta^2) conjecture kiya tha. Woh exponent ~2x galat tha. (Script `d=0` pe do coincident pulses use karti hai, relative modulation pe farak nahi padta.)

**(2) Noise-free optimum (rho se).** Fixed energy, Delta=1: d=1 pe h = 0.1/0.2/0.4/0.8/1.6/3.2 ke liye optimum sigma/Delta = 0.75/0.75/0.70/0.70/0.80/1.40; d=2 pe 0.80/0.80/0.80/0.75/0.80/0.85. Matlab zyadatar geometry ~0.7-0.8 decide karti hai.

**(3) SNR scaling (d=1, Delta=1):**

| sigma_n | ZZB-MC optimum sigma/Delta | surrogate optimum |
|---|---|---|
| 0.08 | 0.5 (flat 0.5-0.7) | 0.70 |
| 0.15 | 0.6 | 0.70 |
| 0.30 | 0.6 (flat 0.6-0.8) | 0.80 |
| 0.60 | 0.9 | 0.95 |

ZZB values (sigma/Delta = 0.35, 0.5, 0.6, 0.7, 0.8, 0.9, 1.1): sigma_n=0.15 -> 0.0138, 0.0080, 0.0075, 0.0082, 0.0099, 0.0113, 0.0189.

**Interpretation:**
- Noise badhne pe optimum chauda pulse ki taraf jaata hai (relevant offset h bada ho jaata hai aur optimum use follow karta hai; plausible, saabit nahi).
- **Basin shallow hai:** optimum ke +-0.15 ke andar ZZB ~10-20% badalta hai; sigma/Delta = 0.35 ya 1.1 pe 1.8-2.5x kharab. Practical rule ek range hai: **sigma/Delta in [0.5, 0.9], FWHM ~ 0.8-1.5 x Delta.** Razor-sharp closed form shayad zaroori nahi.
- Realistic closed form = aliasing law (Poisson summation se analytic) + Q(rho/2sigma_n) -> implicit equation + ek-line fit. Fully explicit formula milega ya nahi, pata nahi.

**Caveat:** ZZB MC noise ke karan low-noise cases mein argmin pakka nahi (flat basin). Sirf d=1. Ek seed.

---------------------------------------------------------------------------------------------------

## 4. Literature positioning

**Chan et al., CVPR 2024, "Resolution Limit of Single-Photon LiDAR"** (NSF PAR copy se padha):
- Knob = spatial pixel count N (fixed flux pe resolution vs per-pixel SNR). MSE = bias (spatial discretisation) + variance (photon noise); closed-form optimum N* ~ (sqrt(alpha0)*||c|| / sigma_t)^(1/2).
- Single return per pixel, multipath assume nahi. Variance CRB/ML (unbiased) se; paper khud kehta hai ki advanced post-processing bound se behtar ho sakta hai.
- Simulation + real SPAD data; par real data pe valley nahi dikha (optimum sensor resolution se bahar), to optimum ki real prediction test nahi hui, sirf curve trend.

| | Chan 2024 | Tumhara rule |
|---|---|---|
| Knob | pixel count N | pulse width vs bin width |
| Problem | single return | do overlapping returns |
| Mechanism | bias-variance (classic) | aliasing (classic matched sampling) |
| Closed form | haan | nahi (abhi) |
| Basis | CRB/ML, unbiased | global ZZB, har estimator pe valid, MMSE ke 1.06-1.58x |
| Real data | partial | koi nahi |

**Verdict:** rule ke package ke taur pe Chan ka zyada novel/complete. Tumhari asli edge: unka variance term CRB-based hai; E1/E2 mein CRB-type 1/F "jitna narrow utna achha" kehta hai jabki ZZB aur ML U-shape dikhate hain. "CRB-based design rules is problem ka optimum miss karte hain, tight global bound sahi optimum deta hai" ek defensible contribution hai. Dono problems complementary hain (Chan spatial, tum temporal two-return, jise woh exclude karte hain).

**Padhe nahi (unverified):** Gupta et al. CVPR 2019 (photon-flooded), Fisher-Information Guidance (CVPR 2022), Compressive Single-Photon 3D (CVPR 2022), Theory of Fermat Paths (CVPR 2019), Naik 2015, Fuentes-Jimenez 2012, Su 2018, TöRF, Transient NeRF, PlatoNeRF, Malik 2025. Cite karne se pehle verify karo; related work mein explicitly likhna padega ki yeh multipath-correction literature se kaise alag hai.

---------------------------------------------------------------------------------------------------

## 5. Promising leads (ranked)

| # | Lead | Evidence | Kya ise maar sakta hai |
|---|---|---|---|
| L1 | Global ZZB as tight, assumption-free floor | E4: 1.06-1.58x | real/misspecified data pe ratio bade ho jaaye |
| L2 | ZZB-based design rule (sigma/Delta in [0.5,0.9]); CRB/MI miss karte hain | E1, E2, E5, E6, E8 | d, sigma_n, weights, fixed-peak normalisation pe optimum ud jaaye |
| L3 | Aliasing-law se semi-closed-form sigma*/Delta | E8 | derivation fit nahi hui, ya optimum shallow hone se koi farak na pade |
| L4 | GEDI rebinning test (real waveforms, real pulse, real noise) | abhi nahi chala | knee predicted jagah pe na aaye |
| L5 | MI-ceiling tightness map as honest figure | E3 | -- (low risk, low impact) |
| L6 | Sensor-config-conditioned estimator / information-weighted sampling | sirf conceptual | shift test mein plain net Bayes ke baraabar nikle |

**Weak / dead (abhi ke saboot se):**
- MI ceiling (Theorem 2) as design tool: E1/E2 mein galat optimum.
- Pulse width ya bin width akele knob: monotone ya sirf knee.
- Fisher-weighted attention: matched filter hai, net khud seekh leta hai (E7 se indirect).
- "Naye model" ko in-prior simulated setting mein headline banana: ~30% jagah (E7).
- LSTM/Transformer vanishing-gradient analogy: wo optimization hai; yahan problem sensor pe information loss (DPI) hai. Loose analog bas itna: collapse ke paas score variance F_D -> 0, to training signal kamzor; uska fix sampling/loss weighting hai, architecture nahi.

---------------------------------------------------------------------------------------------------

## 6. CVPR ke liye humne kya kya try kiya

| Direction | Kya kiya | Verdict |
|---|---|---|
| Tight floor | Global ZZB vs MMSE (E4), MI-ceiling tightness (E3) | Chahiye par akela headline nahi; real-data consistency baaki |
| Sensor design rule | Knob sweeps, ZZB check, surrogate, SNR scaling (E1, E2, E5, E6, E8) | Sabse promising; classic rule, novelty = "tight bound predicts it, CRB nahi" |
| Naya model / tokens | Plain-net room test (E7) | In-prior sim mein ~30% room; shift/misspecification test pending |
| Training method | Conceptual (info-weighted sampling) | Untested |
| Literature gap | Chan 2024 compare | Closed form + real-data curve = unke bar tak pahunchne ki shartein |

**Recommended storyline (abhi ke saboot se):** "Tight, assumption-free information bound jo sampling design rule predict karta hai, jahan CRB-based criteria fail hote hain", learned estimators ka bound se gap ablation ke taur pe.

---------------------------------------------------------------------------------------------------

## 7. Next steps aur go/no-go gates

1. **Aliasing law ka analytic derivation** (Poisson summation) -> semi-closed-form sigma*/Delta. Kill: agar derived aur measured m(sigma/Delta) mein bada mismatch aaye.
2. **Rule ki robustness:** d in {0.5, 2}, sigma_n, weights (w != 0.5), fixed-peak normalisation, point-sampling detector, finer sigma grid, multiple seeds.
3. **GEDI rebinning test (real data):** GEDI waveforms ko coarser Delta pe re-bin karo, error vs Delta dekho. Prediction: GEDI sigma=1.35 m, Delta=0.15 m (sigma/Delta ~ 9, oversampled) -> error ~flat jab tak sigma/Delta ~1.5-2 (Delta ~ 0.7-0.9 m), uske baad tezi se bigadna. Falsifiable. (GEDI data sandbox se download nahi hota; script likhni baaki hai.)
4. **Apna ALS semi-synthetic pipeline** real `noise_stddev_corrected` ke saath aur Delta vary karke; near-threshold bins (d <~ 3 m) badhao.
5. **Shift/misspecification test (model idea ke liye):** net ko ek config pe train, shifted prior/pulse/noise pe test, Bayes estimator (correct params) se compare. Agar plain net Bayes ke barabar rahe, model direction band.
6. **Public SPAD datasets** (availability check nahi hua).

**Honest limit:** koi bhi option "fully real two-return ground truth" nahi deta. Aur GEDI ka pulse hardware-fixed hai, to pulse width real data pe sirf broaden ho sakti hai (convolution se), narrow nahi; Delta rebinning se vary hota hai.

---------------------------------------------------------------------------------------------------

## 8. Files aur kaise chalayein

| # | File | Kya |
|---|---|---|
| 1 | knob.py | Core simulator |
| 2 | sweep.py | E1 |
| 3 | zzb.py | pointwise ZZB, paper-form (E2) |
| 4 | sweep2.py | E2 |
| 5 | mi.py | E3 |
| 6 | gzzb.py | E4 (ab import-safe) |
| 7 | zzb2.py | E5 (ab import-safe, `both()` function) |
| 8 | rule.py | E6 |
| 9 | netroom.py | E7 |
| 10 | closed.py | E8 |

`python sweep.py; python sweep2.py; python mi.py; python gzzb.py; python zzb2.py; python rule.py; python netroom.py; python closed.py`

Notes: `np.trapezoid` NumPy>=2.0 chahiye (purane pe `np.trapz`); netroom ko sklearn chahiye; runtime ek CPU core pe har script ke liye kuch minute; seeds har file mein fixed. `gzzb.py` aur `zzb2.py` ab `if __name__ == "__main__"` ke andar chalte hain, to `rule.py` import pe dobara experiment nahi chalata.

---------------------------------------------------------------------------------------------------

## 9. Jo abhi tak NAHI hua (honestly)

- Koi bhi real-data test (GEDI/ALS/SPAD) is follow-up mein.
- Fixed-peak-amplitude pulse-width sweep; point-sampling detector; d ya weights ka scaling; multiple seeds.
- ZZB-vs-ML check window knob (C) pe.
- CNN/transformer baselines (torch nahi tha).
- Closed-form derivation.
- Photon-counting (Poisson) model pe yeh follow-up.
- Literature: Chan 2024 ke alawa kuch padha nahi.
