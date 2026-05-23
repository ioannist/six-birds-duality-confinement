# Step 180: CTMT Formalization

Verdict:

`final_verdict = V_CTMT_formalized`.

Foundational typed condition:

**Carrier-Typed Matrix-Element Terminality (CTMT).**

A residual closure attempt on a typed carrier exhibits CTMT when the available
operator identities reduce the route to a carrier-native matrix-element family

```tex
M(alpha,beta,gamma)=<a_alpha, P_beta b_gamma>
```

where the vectors, projection, and transport are carrier-typed, and inherited
records do not supply enough kernel/transport data to decide `M`, nor make the
`M`-decision target-equivalent.

Resolution modes:

1. `CTMT-stuck`: the M-family is the exact external-content interface.
2. `CTMT-foreclosed-numerical`: a different lawful operational chain computes
   at least one M-value nonzero with a sharp lower bound.
3. `CTMT-bridge-failure`: the matrix family is not defined across carriers
   because the carrier comparison is missing.

Four instances:

- A: Branch A Calkin class. `M=<eta_i,C_l eta_j>`, projection data `P_eta`,
  `P_infty` by `K_infty^op`. Resolution: waiting on `kappa`; verdict
  `V_branch_a_stuck_at_kappa`.
- B: Branch B SL164.1. `M=c_ij(l)=<e_i,C_l e_j>`. Resolution: waiting on the
  same `kappa`; verdict `V_kappa_classical_theorem_needed`.
- C: Branch C full-carrier ZI-COV(i). `M=L_{rho,k}(G)=<M_zeta G,P_infty y>`.
  Resolution: numerical disproof by four nonzero values; verdict
  `V_branch_c_foreclosed_generic`.
- H6: Hecke zeta-fiber descent. `M` is an attempted cross-carrier comparison
  pairing. Resolution: bridge non-comparability; verdict `V-NC`.

Corpus inclusion candidate: true, target file flagged as
`anti_loc/CTMT.md` for a future corpus update.  This step does not perform a
framework-level corpus edit.
