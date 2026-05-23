# Step 330 Results Summary

Corrected construction used:
`E_eta(z)=exp(-i eta z) Lambda(1/2+i z,chi)` with `eta=1`, and `E_eta#(z)=conj(E_eta(conj z))`.
For self-dual `epsilon=1`, the bare completed L-function split collapses, but this phase-separated Hermite-Biehler proxy gives `|E|>|E#|` in the upper half-plane.

Source anchors:
- de Branges kernel formula, as cited in Step 330 audit source: `k_w(z) = (overline{E(w)}E(z) - overline{E^*(w)}E^*(z))/(2 pi i(overline{w}-z))`.
- Burnol 2002, Step 291 extract: `La fonction E_lambda(w) est une fonction entière satisfaisant la condition de de Branges.`

Computed corrected max-kappa values:
- `chi_3`: corrected max|kappa| `0.000184195959157185212`; old near-zero `2.71172862549152262e-84`; HB ratio `3.00416602394643338`.
- `chi_4`: corrected max|kappa| `0.00406751508841795164`; old near-zero `3.80951365616557532e-83`; HB ratio `3.00416602394643338`.
- `chi_5a`: corrected max|kappa| `0.00129167072621003235`; old near-zero `1.82979095400600317e-83`; HB ratio `3.00416602394643338`.
- `chi_13a`: corrected max|kappa| `0.319647078591062396`; old near-zero `2.13112518643226391e-81`; HB ratio `3.00416602394643338`.

Score update: `stays_2.0_partial_weak_nonzero_no_2.5`.
Verdict: `V_corrected_E_Esharp_self_dual_weak_nonzero_subthreshold`.

Boundary: this is a constructive phase-separated de Branges proxy. It rescues the self-dual finite model numerically, but it is not a proof of Hecke H4 closure or GRH.
