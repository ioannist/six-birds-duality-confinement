# Step 276 Results Summary — Branch A Essential-Norm Universality

## Baseline Sweep

The requested \(10\times 8\) sweep was computed with the inherited local-window PSWF/Sonine approximation at \(T=5000\), mpmath dps \(80\), and GL1400 quadrature.

Baseline maximum:

- \(\sigma=0.35\)
- \(\ell=2.0\)
- \(\Phi=0.490476620029825228\)

This matches the step 220 inherited reference
\[
\Phi_{\max}(\sigma=0.35,\ell=2.0)=0.4904766190
\]
to the displayed precision.  The top requested-grid cells remain concentrated near \(\ell=2.0\), \(\sigma=0.30\ldots0.50\).

Local finite-difference diagnostics near \((0.35,2.0)\):

- \(\partial_\sigma\Phi\) proxy: \(0.0701919986311816\), using \(\sigma=0.30,0.40\).
- \(\partial_\ell\Phi\) proxy: \(-0.0190705307781465\), using \(\ell=1.75,2.25\).

The requested grid still selects the inherited point, but the finite-difference data is not an exact stationary-point theorem.

## Filter Family Comparison

At \((\sigma,\ell)=(0.35,2.0)\), \(T=5000\):

| Filter family | \(\Phi\) |
|---|---:|
| Burnol/Sonine PSWF24 baseline | 0.490476620029825 |
| Burnol/Sonine PSWF12 truncated | 0.490476620029825 |
| sinc-only hard truncation | 0.490476618976904 |
| smoothed step-function diagnostic | 0.465502995589057 |

The baseline, PSWF-truncated, and sinc-only variants are stable at the inherited value.  The smoothed step-function diagnostic shifts the value by about \(2.50\times10^{-2}\).

## Assessment

The number \(0.4904766190\) is stable inside the hard-truncation / inherited Sonine local-window family, but it is not universal across the tested filter families.  No simple closed-form constant match was identified.

Verdict: `V_branch_A_essential_norm_family_specific`.
