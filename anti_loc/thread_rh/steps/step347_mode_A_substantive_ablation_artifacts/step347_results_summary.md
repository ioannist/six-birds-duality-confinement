# Step 347 Results Summary

Substantive ablation check for the Step 345/346 `M^b` algebra.

Results over the 100 Stage-II reproduction rows:
- Ablation A (`F(H)=Z+Omega -> F(H)=Z`): changed `0/100`, failed `0/100`, max output change `0.0`.
- Ablation B (`F(Z)=H+Omega -> F(Z)=H`): changed `0/100`, failed `0/100`, max output change `0.0`.
- Ablation C (`F(Omega)=-Omega -> F(Omega)=0`): changed `0/100`, failed `0/100`, max output change `0.0`; F^2 identity fails on transfer-routed rows.
- Ablation D (`F(H)=Z+Omega -> F(H)=Zprime`): changed `30/100`, failed `29/100`, max output change `3.03645003489`.

Interpretation:
A/B/C do not alter numerical host outputs.  The obstruction symbol `Omega` is ledger-only in the current construction, and `F(Z)` is not used by the Stage-II reproduction paths.  Only replacing the zeta target basis in F(H) changes numerical output, which means the arithmetic work is done by the external realization evaluators, not by the virtual algebra's obstruction rewrite.

Stage II true-status verdict: `V_mode_A_stage_II_substantive_ablation_fails_algebra_decorative`.
