# Carrier-Typed Matrix-Element Terminality (CTMT)

## Definition

A residual closure attempt on a typed carrier `C` exhibits
**Carrier-Typed Matrix-Element Terminality (CTMT)** when, after applying the
available operational identities and structural reductions, the closure
question reduces to deciding a carrier-native matrix-element family

```tex
M(alpha,beta,gamma) = <a_alpha, P_beta b_gamma>
```

where:

- `a_alpha` and `b_gamma` are carrier-native vectors, such as legal generators,
  zero evaluators, pulled evaluators, packet atoms, or source atoms;
- `P_beta` is a carrier-native projection, transport, quotient map, or
  operational kernel;
- inherited records do not supply enough kernel/transport data to compute
  `M`;
- the `M`-decision is not already target-equivalent to the desired conclusion;
- public-shadow and finite-window evidence are not promoted into the typed
  carrier without a bridge theorem.

## Resolution Modes

`CTMT-stuck`: the M-family is well typed, but a kernel/transport theorem is
missing.  The M-family is the exact external-content interface.

`CTMT-foreclosed-numerical`: a different lawful operational chain bypasses the
missing theorem and computes at least one M-value nonzero with a sharp lower
bound.  The route is foreclosed under the inherited normalization.

`CTMT-bridge-failure`: the attempted matrix family crosses carriers, but the
carrier comparison data are missing.  The carrier-pivot or descent bridge fails
under inherited records.

## Instances

| Instance | Carrier | M form | Projection / bridge | Resolution mode | Verdict |
|---|---|---|---|---|---|
| A | Burnol/Sonine | `<eta_i,C_l eta_j>` | `P_eta`, `P_infty` via `K_infty^op` | CTMT-stuck waiting on `kappa` | `V_branch_a_stuck_at_kappa` |
| B | Burnol/Sonine | `c_ij(l)=<e_i,C_l e_j>` | `P_infty` via `K_infty^op`; pulled evaluators via `kappa` | CTMT-stuck waiting on `kappa` | `V_kappa_classical_theorem_needed` |
| C | Burnol/Sonine | `L_{rho,k}(G)=<M_zeta G,P_infty y_{rho,k}>` | `P_infty` via `K_infty^op` | CTMT-foreclosed-numerical by four nonzero values, all `|L| >= 0.11` | `V_branch_c_foreclosed_generic` |
| H6 | Hecke to Burnol/Sonine | attempted cross-carrier pairing `<carrier1 vector,P carrier2 vector>` | carrier comparison / descent bridge | CTMT-bridge-failure | `V-NC` |

## Consequence Theorem

When a typed carrier exhibits CTMT, the framework output is not a vague
external-operator-theory request.  It is the exact carrier-native M-family,
its vectors, its projection/transport, and one of the three typed outcomes:

- `CTMT-stuck`: external work supplying the missing data resolves the route;
- `CTMT-foreclosed-numerical`: a nonzero M-value forecloses the route under the
  inherited normalization;
- `CTMT-bridge-failure`: the carrier-pivot fails because the M-family is not
  defined across carriers.

## Corpus Status

This file is a standalone candidate for foundational corpus inclusion.  The
suggested future target is:

```text
anti_loc/CTMT.md
```

This Step 180 artifact does not perform that corpus-level update.
