# Step 56 — Proof polish pass on v0.4

This step tightens the load-bearing statements in the formed-layer membrane manuscript.

## Polished points

1. **Singular audits now use the legal energy quotient.**
   For `C >= 0`, all capacity/currency/cost statements are made on
   `E_C = (ker C)^perp`, with `C_0 = C|_{E_C} > 0`.  Any probe seeing `ker C`
   causes `failed_null_mode` unless the null direction is lawfully quotiented or excluded.

2. **Minimum-spend duality has the correct range condition.**
   For null-legal `L`,
   `Cost_C(z;L) = z^* K_L^dagger z` only for `z in Ran L_0 = Ran K_L`; otherwise the cost is infinite.

3. **Ξ is a first-class Schur/projection residual.**
   For null-legal native and dissolving probes `L,D`,
   `Xi_C(D|L) = K_DD - K_DL K_LL^dagger K_LD = T_D(I-P_L)T_D^* >= 0`.
   It is the Loewner-minimal residual over all factorizations `D ≈ A L`.

4. **Exact adequacy is quotient-level.**
   `Xi_C(D|L)=0` iff `D_0 = A L_0` iff `ker L_0 subset ker D_0`.

5. **Strict extension monotonicity is Schur-complement monotonicity.**
   Adding probes `M` gives
   `Xi(D|[L;M]) = Xi(D|L) - K_DM|L K_MM|L^dagger K_MD|L <= Xi(D|L)`.

6. **Acceptance semantics are separated.**
   Matrix budget `K <= Theta` is equivalent to no recombination witness at the mathematical ledger level.  Six Birds acceptance is stronger: it requires formed closure, exact package, null legality, native family, adequacy, predictive transport, protocol honesty, all-six statuses, witness-ledger completion, and nonclaim boundary.

## Check results

Finite algebra checks were run only to catch formula mistakes.  They are not Six Birds simulations.

- Max singular cost duality error: about `1.87e-11`.
- Max Ξ projection identity error: about `7.97e-14`.
- Max Ξ optimal residual identity error: about `1.49e-13`.

## Output

The step includes a proof-polish note and a v0.5 manuscript with the patched theorem statements.
