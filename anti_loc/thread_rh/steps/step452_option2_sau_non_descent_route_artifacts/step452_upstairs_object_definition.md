# Step 452 Upstairs Object Definition

## Chosen form

Use Form (c):

```text
U = omega_zeta_zero := (Z_zeta^nt, m_rho, J_L, psi_-, verifier events)
```

This is the typed completed zero-ledger object, not merely a numerical selector. It contains:

- the nontrivial zero multiset `Z_zeta^nt` with multiplicity data;
- the functional-equation involution `J_L(rho)=1-conj(rho)` inherited from `Sel^!_{zeta,tr}`;
- the anti-invariant readout `psi_-(rho)=Re(rho)-1/2`;
- zero-verifier events `Lambda_zeta(rho)=0` in `E^!_M^zero`.

## Why not choose only the selector form

The selector `N -> C` is too implementation-specific: any non-descent result for it can be dismissed as a coding or enumeration obstruction. The full typed ledger is the correct SAU upstairs object because `A_Z(zeta)` is formed from the ledger, not from a bare enumerator.

## Typing verdict

`omega_zeta_zero` is well typed as a promoted/upstairs object in the NDO bridge template: it is hidden from the current trace instrument but has predictive verifier access through `E^!_M^zero`.
