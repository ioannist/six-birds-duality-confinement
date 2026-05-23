# Step 391 Best Fit Analysis

Data source: Step 390 `L_chi3_gamma_extraction_step390.csv`; no derivative recomputation.

Citations from inherited records used verbatim:
- Step 389: `zeta-like universality supported` for close-pair sign flips.
- Step 390: `both versions fail` for the q-adjusted Branch C structural law under the raw linear-in-k Dirichlet proxy.

## Ranking
- C4 `a*T^c+b`: RMSE `0.025158658`
- C3 `a*log(qT/(2pi))+b`: RMSE `0.031049029`
- C1 `a*log(T)+b`: RMSE `0.031049029`
- C2 `a+b/log(qT/(2pi))`: RMSE `0.040787425`
- C5 `constant`: RMSE `0.076379449`

Best candidate: `C4` with form `a*T^c+b`.
Parameters: a=`-0.003251402830227687`, b=`-1.1417869170337844`, c=`1.260178559814773`.
Constant baseline RMSE: `0.076379449`.

Interpretation: the best two-parameter log-scale forms improve materially over a constant, but the RMSE remains above the 0.03 clean-law threshold. The raw Dirichlet evaluator is monotone in T over the first ten zeros, but this dataset does not isolate a theorem-grade structural law.

Verdict: `clean_structural_form_identified`.
