# Step 177: Branch B SL164.1 Attack

Verdict:

`SL164_verdict = V_SL164_stuck_at_normalization`.

The transport-chain derivation succeeds formally.  Define

```tex
kappa_{a,w} := T_a^* K_a^Gamma(.,w)
```

as the Mellin-side pulled evaluator at zero label `w`, and let
`P = mathsf P_infty`.  Step 173 gives an operational action for `P` on any
known Mellin-side vector:

```tex
(P kappa_w)(tau)
= kappa_w(tau)
  - int sinc(tau-u) kappa_w(u) du
  - sum_n Psi_n(tau) <kappa_w, Psi_n>.
```

Therefore the projected kernel and SL164.1 entries reduce to

```tex
K_proj(z,w) = <kappa_{a,z}, P kappa_{a,w}>

c_{ij}(ell)
= <kappa_i - P kappa_i, M_{m_ell} P kappa_j>
  / (||kappa_i|| ||kappa_j||).
```

This is the requested operational composition of Step 173 with Step 153.

The numerical evaluation does not lawfully start, because Step 153 explicitly
leaves

```tex
K_a^Gamma = P_{L_a^Gamma} K_a^{Gamma,amb}
```

as a projected Sonine kernel and warns that omitting the projection gives only
the ambient Hardy shadow.  The missing numerical input is the explicit
Mellin-line vector

```tex
kappa_{a,w}(tau)=T_a^*K_a^Gamma(.,w)(1/2+i tau),
```

equivalently the action of `P_{L_a^Gamma}` on `K_a^{Gamma,amb}`.

Attempted numerical pair:

```tex
c_{11}(log 2), a_0=1/2, rho_1=1/2+14.134725141734693 i.
```

Status: `not_evaluable_missing_kappa`.

Branch B implication: SL164.1 is sharpened from a generic "projected kernel
missing" record to the specific missing Mellin vector `kappa_{a,w}` / projected
Sonine-kernel action.  The finite-carrier diagnostic remains indeterminate.
