# R_phase_hadamard Rule

## Formula

For a zero `rho_j` with nearest neighboring zero `rho_n`,

```text
g'_near(rho_j) = -1/(rho_n - rho_j).
```

If `rho_n = rho_j + i*s_min`, then:

```text
g'_near = +i/s_min.
```

If `rho_n = rho_j - i*s_min`, then:

```text
g'_near = -i/s_min.
```

The phase sign prediction is:

```text
phase_sign = sign(Re(2 * L'(rho_j) * g'_near)).
```

## Rewrite Form

```text
R_phase_hadamard:
  c[zero_id, L_prime, nearest_zero, mag_residual]
    -> c[mag_residual, phase_sign, phase_source=Hadamard_near_pair]
```

## Ablation

Dropping `R_phase_hadamard` removes the phase-sign ledger entirely. The joint `(mag, phase)` residual can no longer descend to `d[pass]`; only the magnitude residual remains.

## Scope

This rule covers the sign-flip phase proxy requested in this step. It is not the full complex phase of every matrix element and not the operator-compatibility component of H6.
