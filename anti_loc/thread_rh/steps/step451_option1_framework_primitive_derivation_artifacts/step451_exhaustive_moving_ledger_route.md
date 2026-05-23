# Step 451 Exhaustive Moving Ledger Route

## Candidate construction

Use needles.tex `def:main:exhaustive-moving-ledger` with a zero-window parameter `T_n -> infinity`.

Define the finite-window ledger

```text
A_Z,n(zeta) = sum_{rho in Z_zeta^nt, |Im rho| <= T_n} m_rho |Re(rho)-1/2|^2.
```

Let `iota_n` be the inclusion of the finite zero-window ledger into the completed ledger and let `T_n^tail >= 0` record omitted anti-invariant mass. The formal squeeze has the shape cited by step 69:

```text
A_Z(zeta) <= iota_n A_Z,n(zeta) iota_n^* + T_n^tail.
```

If a finite-window domination record `A_Z,n(zeta) <= B_n^win` were available, needles.tex `thm:main:exhaustive-ledger-squeeze` would require

```text
tr(iota_n B_n^win iota_n^*) + tr(T_n^tail) -> 0.
```

## Attempted convergence sources

- Framework exhaustivity supplies the **form** of the moving ledger and tail bookkeeping.
- Functional equation supplies the involution `J(s)=1-conj(s)` and paired zero packets.
- Foundations II visibility records say which windowed records are visible, suppressed, outside, or unknown.

None of these primitives proves vanishing of the off-critical anti-invariant tail. Finite windows can compute or record mass, but they cannot make the global trace tend to zero without additional analytic content.

## Failure point

A trivial choice `B_n^win=A_Z,n(zeta)` is positive and dominates the window, but then `tr(B_n^win)` tends to the very anti-invariant mass whose vanishing is equivalent to the target. Setting it to zero would assume RH. A nontrivial choice needs a source theorem controlling the off-critical mass across all windows.

## Named missing input

`Xi_SDTC_trace_decay_input`: tail/exhaustivity trace decay for the completed zero ledger, not just finite-window bookkeeping.

## Route verdict

Partial only. The moving-ledger route cleanly identifies the tail term but does not prove `tr T_n^tail -> 0` from framework primitives.
