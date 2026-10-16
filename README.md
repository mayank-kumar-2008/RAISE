# RAISE: Representation Agnostic Information and Separation Estimation

> **In short:** RAISE studies why waveform sensors (e.g. spaceborne lidar like GEDI) fail to separate two overlapping echoes. It argues the failure is an *information limit* of the sensor, not an architecture or training problem, and builds a bound (Ziv-Zakai) that says how much of an estimator's error is fixable versus unavoidable. This repo holds the original NeurIPS-workshop submission, the notebook behind its experiments, and a follow-up simulation study aimed at a CVPR resubmission after the paper was rejected.

**Status (2026-10-16):** The original paper was rejected from the workshop because its claims exceeded its evidence. The reviewers did not find the mathematics wrong. The follow-up work is **simulation only, single seed, and nothing is validated on real data yet.** Replicate before quoting any number as a paper result.

---

## 1. The problem and the idea

A waveform sensor sees two reflecting surfaces (say canopy top and ground) as a sum of two overlapping pulses:

```
W_obs(t) = w1 * P(t - tau1) + w2 * P(t - tau2) + noise
c = (tau1 + tau2) / 2     (centroid, a nuisance parameter)
d = tau2 - tau1           (separation, the quantity we want)
```

When `d` is small relative to the pulse width, the waveform barely changes with `d`. The paper's claims:

1. **Information collapse.** The marginal Fisher information `F_D(d)` (with the centroid integrated out) vanishes below a threshold separation. That gives a representation-independent ceiling via a mutual-information bound plus the data-processing inequality (the paper's "Theorem 2", worth about 2.00 nats).
2. **ZZHE (Ziv-Zakai Headroom Estimator).** A diagnostic that compares a deployed estimator's error with a Ziv-Zakai floor to show how much improvement is still possible.
3. **Validation** on GEDI L2B spaceborne lidar and on airborne LiDAR (ALS) ground truth.

The follow-up work asks what survives the review. The current answer: the **global Ziv-Zakai bound** (with a prior on `d`) is valid for every estimator and sits within 1.06-1.58x of the exact Bayes-MMSE in simulation. Fisher/CRB-based and MI-based criteria miss the sensor-design optimum, while the ZZB captures it.

---

## 2. Repository layout

```
Raise/
├── RAISE.pdf                        # The original submitted paper (13 pages)
├── OldRaise/
│   ├── RAISE_all_experiments.ipynb  # One notebook with every experiment behind the paper
│   └── README_previous.md           # Hinglish version of the follow-up README (see note below)
└── FOLLOWUP/
    ├── README_followup.md           # Full follow-up report (English): reviews, issues, experiments E1-E8, leads
    ├── README_followup_hinglish.md  # Same report in Hinglish
    ├── Experiments ckp.md           # Checkpoint: table of the follow-up scripts and the run order
    ├── exp ckp 2.md                 # Checkpoint: guide to the combined notebook (section map, caveats, fixes)
    ├── knob.py                      # Core simulator (used by almost every script)
    ├── sweep.py   sweep2.py         # Design-knob sweeps (E1, E2)
    ├── zzb.py     zzb2.py           # Pointwise ZZB (paper form, then standard form) (E2, E5)
    ├── gzzb.py                      # Global ZZB vs exact Bayes-MMSE (E4)
    ├── mi.py                        # Theorem-2 MI ceiling vs true MI (E3)
    ├── rule.py                      # Design-rule surrogate vs ZZB (E6)
    ├── netroom.py                   # Plain MLP vs exact MMSE (E7)
    └── closed.py                    # Aliasing law, noise-free optimum, SNR scaling (E8)
```

> **Note on the READMEs:** `OldRaise/README_previous.md` and `FOLLOWUP/README_followup_hinglish.md` are byte-identical. Both are the Hinglish write-up of the follow-up study, and the second is a duplicate. Consider deleting one. `exp ckp 2.md` actually documents the *notebook*, while `Experiments ckp.md` documents the *scripts*. Renaming them (for example `NOTEBOOK_GUIDE.md` and `SCRIPTS_GUIDE.md`) would make that clearer.

---

## 3. How to approach this repo (suggested reading order)

1. **`RAISE.pdf`**: read the abstract and Sections 1-2 to understand the claim, the model (Eq. 1-7), and what was originally promised.
2. **`FOLLOWUP/README_followup.md`**: the most important file. Read Section 0 (summary), then Section 1 (reviewer critique and the issue register P1-P15) and Section 3 (experiments E1-E8).
3. **`FOLLOWUP/knob.py`**: read it before any other script, because every experiment builds on it.
4. **Run the scripts** in the order given in Section 5 below.
5. **`OldRaise/RAISE_all_experiments.ipynb`** plus `FOLLOWUP/exp ckp 2.md`: use these only when you need to reproduce or fix the paper's original tables and figures (needs GPU and data downloads for some sections).

---

## 4. What each part contains

### 4.1 `RAISE.pdf`: the original paper
Anonymous NeurIPS 2026 workshop submission. It covers the identifiability-collapse theory, the ZZHE diagnostic, GEDI validation (Table 1), the architecture-convergence study (Table 3, Fig. 4), synthetic cross-estimator validation (Table 4), noise robustness (Table 5), and ALS validation (Table 6, Fig. 2).

### 4.2 `OldRaise/RAISE_all_experiments.ipynb`: paper experiments in one notebook
88 cells, assembled from 18 earlier notebooks, ordered the way the paper uses them.

| Section | Content | Paper element |
|---|---|---|
| 0 | Setup, `QUICK` flag (toy scale by default) | |
| 1 | Marginal Fisher information to MI ceiling (2.00 nats) | Eq. 4-7, Fig. 1 |
| 2 | Schur-complement vs exact marginal Fisher | App. C, Table 2 |
| 3 | ZZHE convergence diagnostics, cross-estimator validation | App. E, Table 4 |
| 4 | Noise-level robustness of the floor | App. F, Table 5, Fig. 5 |
| 5 | Cross-architecture convergence to the floor | App. D, Table 3, Fig. 4 |
| 6 | Encoder probe | App. D, Fig. 3 |
| 7 | Swap-basin loss-landscape observation (M = 2) | App. A |
| 8 | Real GEDI L2B validation | Sec. 3, Table 1, App. B |
| 9 / 9b | Independent ALS validation, plus ablations | App. G, Table 6, Fig. 2 |
| 10 | Notebooks in the zip that are not part of this paper | |
| 11 | Issues found while assembling (read before submission) | |

**How to run:** open in Colab (GPU for Sections 5 and 8). Keep `QUICK = True` for a smoke test, which gives toy numbers that will *not* match the paper. Set `QUICK = False` for paper-grade runs, which take hours for Sections 3, 4, 5, 8, 9. Run top to bottom, because later sections reuse variables and some function names (e.g. `zzb_floor`) are redefined. Sections 8-9 need a NASA Earthdata login (GEDI L2B), USGS 3DEP LAZ tiles, and Copernicus DEM tiles. Outputs go to `raise_outputs/`.

**Verification status:** Sections 0-4, 6, 7 were executed end to end on CPU in QUICK mode. Sections 5, 8, 9 were only syntax-checked, not executed.

**Known problems to fix before any resubmission** (details in `exp ckp 2.md`):
- Several paper numbers have no logged run (Table 1 roughness and geolocation values, Table 3, Fig. 3, Appendix A, original Fig. 1).
- Table 4 says 29/30 passes, but the primary locked run gives 24/30.
- The GEDI "3-6x error reduction" uses a metric whose denominator is also the binning variable.
- ALS Table 6 used a smaller floor computation than stated (n_sim=150 and 15 h-points, versus 800 and 40 in the text). The <4 m bin only passed after enrichment.
- The ablation notebook ran on a synthetic stand-in, so do not cite it.
- Pulse convention mismatch: the footnote says `exp(-t²/σ²)`, but the code simulates `exp(-t²/(2σ²))`.
- Figure 2 labels headroom as mean minus floor, while the text uses the 2-SE lower bound minus floor.

### 4.3 `FOLLOWUP/`: simulation study after the rejection

**Shared model (all scripts):** two equal-weight Gaussian returns `exp(-t²/σ²)` with `σ_pulse = 1.35 m` (FWHM = 1.665σ). The centroid is `c ~ U[-3, 3] m`. The detector is integrate-and-dump bins over a 24 m window, with default bin widths of 0.3 m (E3, E4) and 1.0 m (design-rule runs). Noise is white Gaussian with `σ_n = 0.15` (a placeholder). "Fixed energy" means amplitude `A = (1.35/σ)^0.5`. Estimators are joint-ML grid search, posterior mean (exact Bayes), and an sklearn MLP. The Poisson photon-counting model is **not** used.

| File | Experiment | What it does |
|---|---|---|
| `knob.py` | Core | Bin-averaged waveform `mu()`, marginal Fisher `fisher_marg`, joint-ML MSE `mse_ml`, MI ceiling `mi_ceiling` (Eq. 6) |
| `sweep.py` | E1 | Sweeps pulse width, bin width and window against 1/F_D, ML-MSE and MI ceiling. Fisher says "narrower is better" while ML-MSE shows an optimum at coarse bins, which is where the design-rule lead came from |
| `zzb.py` | E2 | Pointwise Ziv-Zakai bound (paper-form valley-fill) via Monte Carlo likelihood-ratio tests, centroid marginalised |
| `sweep2.py` | E2 | Coarse-bin pulse-width sweep with the ZZB, plus an extended window sweep. Confirms the optimum at σ ≈ 0.7 for d = 1, 1.0 m bins |
| `mi.py` | E3 | True mutual information (Monte Carlo) vs the Theorem-2 ceiling. The ceiling is valid but 1.3-6.6x loose, worst in the collapse regime |
| `gzzb.py` | E4 | **Most important.** Global ZZB (uniform prior on d) vs exact Bayes-MMSE. The ratio is 1.06-1.58x |
| `zzb2.py` | E5 | Checks the paper's Algorithm line 5 `valleyfill(h·Pe)` against the standard `h·valleyfill(Pe)`. The paper form is 7-16% larger |
| `rule.py` | E6 | Signature-distance surrogate `Q(ρ/2σ_n)` vs the ZZB for the best σ per bin width. The ZZB optimum is σ/Δ ≈ 0.6-0.7 |
| `netroom.py` | E7 | Plain MLP vs exact MMSE. The MLP is within ~1.3x, so there is little room for a new architecture in this setting (needs sklearn) |
| `closed.py` | E8 | Aliasing amplitude law, noise-free optimum, and SNR scaling of the optimum. The practical rule is σ/Δ in [0.5, 0.9] |

---

## 5. Running the follow-up scripts

```bash
cd FOLLOWUP
pip install numpy scipy scikit-learn        # NumPy >= 2.0 (else replace np.trapezoid with np.trapz)
python sweep.py; python sweep2.py; python mi.py; python gzzb.py
python zzb2.py; python rule.py; python netroom.py; python closed.py
```

- Each script takes a few minutes on one CPU core, and seeds are fixed in every file.
- `knob.py` is a library, so there is no need to run it directly.
- `gzzb.py` and `zzb2.py` now run inside `if __name__ == "__main__"`, so `rule.py` no longer re-runs them on import. (The older `Experiments ckp.md` still says otherwise, and that note is outdated.)
- `closed.py` is missing from the table in `Experiments ckp.md`, but it exists and is listed in `README_followup.md`.

---

## 6. Key findings so far (simulation only)

1. **Global ZZB is a tight, assumption-free floor** in simulation: 1.06-1.58x of the exact MMSE (E4). This repairs the reviewers' "estimator-agnostic" and "1000x loose" objections, but only in simulation.
2. **Fisher/CRB and the Theorem-2 MI ceiling miss the design optimum, and the ZZB gets it.** With fixed bins the best pulse width is σ/Δ ≈ 0.5-0.9 (centre ~0.65-0.7), and it moves toward wider pulses as noise rises. The basin is shallow, so the rule is a range, not a single value.
3. **A plain MLP is within ~1.3x of the best possible estimator** in the in-prior simulated setting, so "a new architecture" cannot be the headline there.
4. **Versus Chan et al., CVPR 2024** (single-photon lidar resolution limit): their package, with a closed form and a real-data curve, is currently more complete. The edge here is that CRB-based design analysis misses this problem's optimum while a tight global bound does not. That edge is only defensible with real-data support.

**Recommended storyline:** a tight, assumption-free information bound that predicts the sensor-sampling design rule where CRB-based criteria fail, with the learned-estimator gap as an ablation.

---

## 7. What is still missing (go/no-go gates)

- **Any real-data test.** The planned one is GEDI rebinning: coarsen the bins and check that error stays flat until σ/Δ ≈ 1.5-2, then degrades. This is falsifiable.
- A closed-form or semi-closed-form `σ*/Δ` from the aliasing law (Poisson summation).
- Robustness of the rule across d, σ_n, unequal weights, fixed-peak normalisation, a point-sampling detector, and multiple seeds.
- ALS pipeline with the real `noise_stddev_corrected` and more near-threshold bins (d ≲ 3 m). The current ALS bins are mostly far from the threshold.
- A shift/misspecification test for the model idea (train on one configuration, test on another).
- CNN/transformer baselines (torch was unavailable in the sandbox).
- Related-work reading: only Chan 2024 has been read so far.
- Check which ZZB valley-fill form your own code uses, and re-run Tables 4-6 with the standard form if needed.

---

