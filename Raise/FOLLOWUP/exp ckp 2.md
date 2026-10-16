# RAISE — combined experiment notebook

`RAISE_all_experiments.ipynb` collects every experiment behind the paper
**"RAISE: Representation Agnostic Information and Separation Estimation"** in one notebook, ordered the way the paper uses them.
It was assembled from the 18 notebooks in `mess.zip`. Where no notebook contained an experiment the paper reports, it was generated from the paper's description.

## 1. How to run

1. Open in Colab (GPU runtime for Sections 5 and 8).
2. Section 0 has `QUICK = True`. This is a toy-scale smoke test (minutes). Numbers will **not** match the paper.
3. For paper-grade numbers set `QUICK = False` and expect hours for Sections 3, 4, 5, 8, 9.
4. Run top to bottom. Later sections reuse variables from earlier ones, and some function names (e.g. `zzb_floor`) are redefined with different signatures in Sections 3 and 9, so order matters.
5. Outputs (figures, CSV tables, JSON) go to `raise_outputs/`.

Sections 8 and 9 download data: NASA Earthdata login (GEDI L2B, about 21–25 granules, several GB), USGS 3DEP LAZ tiles (about 300 MB), Copernicus DEM tiles.

## 2. Map: paper element → notebook section → provenance

| Paper element | Section | Provenance | Status |
|---|---|---|---|
| Fig. 1b/1c (collapse, Fisher collapse) | 1 | regenerated | Fig. 1c noise level unknown (placeholder) |
| Theorem, Eq. 4–7, **2.00 nats** | 1 | `Untitled4 (1)` cell 1, patched | Reproduced (logged 2.0024) |
| App. C, Table 2 (Schur vs exact) | 2 | generated | Reproduced (see §3) |
| App. E (grid convergence, valley-fill bias) | 3 | `Untitled28` cells 1–10 | Verbatim; heavy sweeps gated by `QUICK` |
| App. F Table 4 (3 estimators × 10 d) | 3 | `Untitled28` cells 11–15 + tally | Verbatim + tally cell |
| App. F Table 5, Fig. 5 (noise robustness) | 4 | `Untitled7 (2)` cells 0, 1, 3 | Patched; logged 24/24 |
| App. D Table 3, Fig. 4 (5 architectures) | 5 | rewritten from `Untitled7 (2)` cell 2 | Original never finished |
| App. D Fig. 3 (encoder probe) | 6 | generated | No source notebook |
| App. A (M=2 swap basin) | 7 | generated | No source notebook |
| Sec. 3 Table 1 (real GEDI), App. B | 8 | `Untitled22` cells 0,2,7,8,17–24 + generated | Two Table-1 rows were never computed in any notebook |
| App. G Table 6, Fig. 2 (ALS validation) | 9 | `algorithm_ppr (2)` cells 1–17, 21–24 | Verbatim |
| Continuous-d ablation, MMSE baseline | 9b | `ablation_pipeline (2)` | Patched; original ran on synthetic stand-in |

Section labels in the notebook: **VERBATIM** (unchanged), **PATCHED** (mechanical change, listed), **FIXED** (was broken), **GENERATED** (written from the paper; assumptions in the cell).

## 3. What was verified

Run in a sandbox (CPU only, `QUICK` mode unless noted): Sections 0–4, 6 and 7 execute end to end. Sections 5 (needs PyTorch), 8 and 9 (need network/GPU) were only syntax-checked, **not executed**.

- Section 1: 2.0009 nats (QUICK rerun) vs 2.0024 logged vs 2.00 in the paper.
- Section 2 at paper settings (n_c=800, n_mc=8000, 4 seeds): divergence 72.8% / 41.7% / 6.6% at d = 0.05 / 0.10 / 0.30 (paper: 73.7 / 42.0 / 8.9); I_Schur(0.05)=0.0474, matching the paper's 0.047. d=0.30 is slightly lower than the paper's value.
- Section 7 (Appendix A), 200 starts: with a perturbed-truth initialisation the swap basin captures 0.5–6.5% of starts at d/H = 0.6–1.0, consistent with the paper's "1–8%". The swap configuration becomes distinguishable (ΔNLL ≥ 3) from d/H ≈ 0.6, consistent with "0.6–0.8". The criterion and initialisation are my interpretation; the paper does not state them.
- Section 6 (probe), full size: separation-probe MAE falls 36–38% with ratio (latent ≥ 8) and R² rises from about 0.26 to 0.75 — the right direction but weaker than the paper's −43% and 0.72 → 0.91, and the centroid control is not flat (MAE 0.19–0.35). Report what you get; do not tune to the paper.

## 4. Things to fix before submission

1. **Untraceable numbers.** No logged run exists for: Table 1 "roughness r=0.612, N=7,894" and "geolocation r=1.000"; Table 3's values; Fig. 3; Appendix A's figures; the original Fig. 1. Sections 5–8 regenerate them; update the paper from the new output. (The GEDI neural-field holdout in the logs has N=7,886, not 7,894.)
2. **Table 4 says 29/30; the primary locked run gives 24/30.** The extra passes come from re-running only failing rows at higher precision, and d=1.689 global-MLE (negative lower bound) was handled as a "heavy-tail characterisation". The printed table shows original values. Either report 24/30 plus targeted re-checks, or re-run all 30 rows at the higher precision.
3. **GEDI "3–6× error reduction".** The metric is |error| / roughness, binned by roughness / H_NWCS, so the denominator is the binning variable. Use the raw-RMSE-per-bin cell at the end of Section 8.
4. **ALS Table 6.** The floor is computed once per bin at one representative footprint with n_sim=150 and a 15-point h-grid, not the "locked" 800 / 40 the paper states. The original <4 m bin (n=16) failed the margin (12.11 ± 7.69 vs 0.0038); it passed after enrichment to n=36. The representative footprint in Cell 13 is selected using the median of squared errors rather than of d_true. Section 9b (continuous curve) addresses this.
5. **Ablation notebook.** The uploaded copy ran on a 60-footprint synthetic stand-in, and MMSE had the lowest headroom in only 75% of the sweep. Do not cite either result until Section 9b is run on the real footprints.
6. **Pulse convention.** The footnote defines the pulse as exp(−t²/σ²) (κ = 2√ln2, σ = 1.3503 m for 15 ns), but all code simulates exp(−t²/(2σ²)). With σ = 1.3503 that pulse has FWHM 3.18 m rather than GEDI's 2.25 m. Pick one convention and state it.
7. **Fig. 2 vs text.** The figure labels headroom as mean − floor (67.2, 22.2, 35.9, 86.2); the text's "9.4 to 71.3" is the 2-SE lower bound − floor. Say which.

## 5. Notebooks not used

| File | What it is |
|---|---|
| `Untitled29` (and `(1)`, identical) | Photon-count scaling d* ∝ N^(−1/4) — next paper (temporal-lidar thread) |
| `Untitled10` | Measurement-compression / sensor-design study — same thread |
| `Untitled23`, `Untitled25` | CRLB-blow-up calibration of κ (κ is "future work" in the paper); swap-floor sketch |
| `Untitled5 (2)` | Early ZZB prototyping, superseded by `Untitled28` |
| `Untitled2 (1)` | LROC lunar DTM download (fails with `IndexError`) |
| `Untitled3`, `Untitled27`, `Untitled8`, `Untitled10 (1)` | Unrelated (chess codec, CTF generator, OceanGuard, magic squares) |
| IGMC cells of `Untitled22` | Not in the paper; cells 9–16 ran on a placeholder dataframe |

## 6. Still needed from you

Send any notebook that produced: the Table 1 roughness/geolocation numbers, Table 3, the encoder probe (Fig. 3), Appendix A, Fig. 1. If they exist, they replace the generated cells and the paper's numbers become traceable.
