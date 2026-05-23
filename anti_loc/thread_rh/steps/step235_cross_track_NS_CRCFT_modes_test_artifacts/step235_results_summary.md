# Step 235 Results Summary

## Target

Test whether the CRCFT modes TE, CTMT, and BF classify the Navier--Stokes track components. CRCFT was RH-derived at step 183 and cross-track verified on BSD and Hodge at steps 233--234.

## NS Track Readout

Records read:

- `/home/repos/six-birds-foundations-iii/anti_loc/thread_ns/cascade_map_ns.md`
- `/home/repos/six-birds-foundations-iii/anti_loc/thread_ns/steps/ns54_extracted/ns54_results_summary.md`
- `/home/repos/six-birds-foundations-iii/anti_loc/thread_ns/steps/ns55_extracted/ns55_results_summary.md`
- `/home/repos/six-birds-foundations-iii/anti_loc/thread_ns/steps/ns45_extracted/ns45_results_summary.md`
- `/home/repos/six-birds-foundations-iii/anti_loc/thread_ns/steps/ns50_extracted/ns50_results_summary.md`
- `/home/repos/six-birds-foundations-iii/anti_loc/thread_ns/steps/ns51_extracted/ns51_results_summary.md`
- `/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step223_cross_track_NS_CTMT_test_artifacts/step223_results_summary.md`

The NS track is diagnostic-complete at `ns55`. The remaining frontier consists of four external PDE obligations:

1. `EXT1`: sector-matched radius-window product theorem.
2. `EXT2`: BKM/BG time gate for the Gevrey envelope.
3. `EXT3`: sector match for the BG mismatch ledger.
4. `EXT4`: tail/lift budget in the same context.

The residual chain is:

`Xi(D_BG | L_phys) -> Omega_src + physical-native gap -> Omega_gap -> Omega_rem -> Omega_bb -> Omega_mm -> Omega_amp`.

## CRCFT Mode Classification

| NS component | CRCFT mode | Reason |
|---|---|---|
| `EXT1` sector-matched radius-window product | TE with CTMT proof gate | The exact theorem is the terminal missing PDE statement; if proved with auxiliary gates it closes `Omega_amp` and reduces the root residual. |
| `EXT2` BKM/BG time gate | TE | BKM/BG continuation is target-strength for smooth continuation in the chosen readout. |
| `EXT3` sector match | BF | Sparse/Gevrey evidence does not transport unless it controls the same BG mismatch sector. |
| `EXT4` tail/lift budget | CTMT | Requires explicit quantitative tail and tangent-lift estimates in the same carrier. |
| `Omega_src` | BF with CTMT decomposition | Raw nonlinear source shadows do not promote; they must enter lawful source-admission slots. |
| `Omega_gap / Omega_rem` | CTMT | Localization and remainder decomposition are terminal PDE-budget gates. |
| `Omega_bb` | BF with CTMT threshold | Packing-only size estimates fail to suppress amplitude unless the sharp exponent threshold is paid. |
| `Omega_mm` | BF | It is the sector-mismatch residual itself. |
| `Omega_amp` | TE with CTMT terminal estimate | It is the final sharp obstruction; the radius-window product theorem is the needed terminal estimate. |

## Literature Audit

The PDE literature supplies major continuation criteria, regularity criteria, and guardrails, but not the exact `EXT1` theorem:

- Beale--Kato--Majda gives the vorticity blowup/continuation criterion used as target readout.
- Caffarelli--Kohn--Nirenberg gives partial regularity, not amplitude closure.
- Constantin--Fefferman gives geometric depletion criteria, not the fixed-ledger sector-matched radius-window theorem.
- Koch--Tataru gives critical-space well-posedness infrastructure.
- Tao's averaged NS blowup and Buckmaster--Vicol weak-solution nonuniqueness act as guardrails against energy-only or weak-solution-only bridges.
- Bradshaw--Grujic and Grujic--Xu supply frequency/sparseness route templates but still expose fixed-ledger, amplitude, sector, and time gates.

## Framework Upgrade

Verdict: `V_ns_CRCFT_modes_verified`.

CRCFT now has cross-track support on RH, BSD, Hodge, and NS: `verified-on-4-track-instances`. The NS adaptation is PDE-estimate-terminal: CTMT becomes quantitative estimate terminality, BF becomes failed sector/source/metric transport, and TE sits at the radius-window/time-gate closure layer.

No Navier--Stokes regularity or RH proof is claimed.
