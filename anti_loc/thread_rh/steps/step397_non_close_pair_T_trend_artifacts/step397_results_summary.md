# Step 397 Results Summary

## Inputs and Citations
- Step 196 foreclosure threshold used verbatim: `|L_k|>=0.034`.
- Step 292 raw proxy used verbatim: `delta_Dk=(zeta*M(G_star))^(k)(rho_j)`.
- Step 392 context used verbatim: one high-j raw-proxy failure at `j=470, k=5`.
- Step 395 context used verbatim: close-pair failure rate `15.6%`.
- Step 396 context used verbatim: `T is dominant predictor (r=0.329); s_min within CP not predictive (r=-0.021)`.

## Sample
- Candidate grid: `j = 25, 50, ..., 500`.
- Non-close-pair filter: `s_min > 1.5`.
- Included non-CP zeros: 3.
- Excluded grid points: j=25:s_min=1.3838365945092360172, j=75:s_min=1.0530702431319175001, j=100:s_min=1.2455908151089982008, j=125:s_min=0.97850739790323473566, j=150:s_min=1.118298313946417511, j=175:s_min=0.80138284959264894553, j=200:s_min=0.79898421159846596112, j=250:s_min=1.2376509189896154983, j=275:s_min=1.048920967279089192, j=300:s_min=1.216046873906164187, j=325:s_min=1.2317563311694305072, j=350:s_min=0.93504668314779770847, j=375:s_min=1.3576133657535895214, j=425:s_min=0.8490935557259782157, j=450:s_min=1.154316348820455184, j=475:s_min=1.1918480549926664742, j=500:s_min=1.1025539600991604464.

## Foreclosure Statistics
- Threshold: 0.034000000000000002442490654175344388931989669799805.
- Pass/fail: 3/0.
- Minimum `|delta_Dk(k=5)|`: 0.89385211317886256981827946579950640181270769302163 at `j=400`.
- Maximum `|delta_Dk(k=5)|`: 8.2321219788354583817076290532180295621863907453369 at `j=50`.
- Mean `|delta_Dk(k=5)|`: 3.7685313540010097e+00.

## Trend Fits
- Best model by RMSE: `quadratic_a_plus_bT_plus_cT2`.
- Best-model parameters: `a=1.3014364455726323e+01`, `b=-3.7572441917492129e-02`, `c_or_alpha=2.9042479639657541e-05`.
- Best-model RMSE: `1.4610104406664265e-12`.
- Best-model threshold crossing: `` (no_real_positive_crossing).

## Verdict
non_cp_stays_safely_above_threshold_in_sample.

This is a raw-proxy foreclosure diagnostic, not a theorem and not a claim about RH.
