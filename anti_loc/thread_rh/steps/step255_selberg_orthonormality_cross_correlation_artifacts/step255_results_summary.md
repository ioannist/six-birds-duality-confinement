# Step 255 Results Summary

## Full Selberg Orthonormality Carrier

For primitive Selberg-class functions `L1,L2`, define

`S_12(x) = sum_{p<=x} a_p(L1) conjugate(a_p(L2))/p`.

Full orthonormality has two components:

- diagonal: `S_LL(x) = n_L log log x + O(1)`;
- off-diagonal: `S_12(x) = O(1)` for `L1 != L2`.

Normalization note: the standard Selberg diagonal constant is `n_L`, expected
to be `1` for primitive functions.  It is not the order of the pole at `s=1`;
using pole order would incorrectly make nontrivial primitive Dirichlet
characters have zero diagonal mass.

## Cross-Correlation Extension

**Selberg-Class Cross-Correlation Extension (candidate).** Beyond the per-L
RH-analogue framework of step 232, the Selberg class admits multi-L residuals:
pairwise coefficient correlations, orthonormality, and joint-zero
decorrelation.  These are second-order typed carriers because they involve
pairs or families of primitive L-functions, not a single L-function's RH
analogue.

## Evidence

1. SOC off-diagonal carrier, step 254: `S_12(x)` for `L1 != L2`.
2. Full orthonormality carrier, step 255: diagonal norm plus off-diagonal
   bounded correlation.

Status: `candidate (verified-on-2-Selberg-instances) corpus-pending`.

The finding was deposited in:

`/home/repos/six-birds-foundations-iii/anti_loc/findings_framework.md`

## Verdict

`V_selberg_orthonormality_cross_correlation_typed`.

No proof of SOC, full orthonormality, GRH, or RH is claimed.
