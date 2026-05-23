# Step 315 Tightness Audit

The formal worst-case-alpha factor `exp(-pi^2 k/8)` is extremely small. It passes the certified finite sample only because it is very loose. However, it is not a theorem-grade interference lower bound: bounded phase frequency alone does not prevent exact cancellation.

Empirically, Step 312 found alpha about `0.39-0.43`, while the worst-case uses `pi`. The sharp-vs-worst exponent gap is therefore on the order of `((pi^2-alpha^2)/2)*sigma^2`, which is exponentially large in k. Closing this gap requires the same pointwise high-order zeta-derivative phase-ratio control identified in Step 314.
