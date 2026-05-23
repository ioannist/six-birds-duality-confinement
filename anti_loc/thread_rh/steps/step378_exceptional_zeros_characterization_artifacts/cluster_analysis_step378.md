# Step 378 Cluster Analysis

Step 377 found seven nonnegative exceptions: `[34, 41, 64, 71, 79, 80, 92]`.

Adjacent exceptional index gaps: `[7, 23, 7, 8, 1, 12]`.
Adjacent exceptional T-gaps: `[13.227283, 45.655158, 14.962491, 13.140842, 3.249442, 20.165954]`.
Expected index gap for 7 uniformly scattered hits in 1..100: `12.625`.

The exceptions are not one compact T-cluster. They are late-skewed (`5/7` occur after `j>=64`) and include one adjacent pair (`j=79,80`), but also have large gaps (`23` indices between `41` and `64`, `12` between `80` and `92`).

Spacing comparison:

- mean exceptional `s_min`: `0.968621`
- mean non-exceptional `s_min`: `1.748771`
- mean exceptional `(mean_spacing - s_min)`: `0.953342`
- mean non-exceptional `(mean_spacing - s_min)`: `0.543540`

Derivative-ratio comparison:

- mean exceptional `|zeta''|/|zeta'|`: `3.976024`
- mean control `|zeta''|/|zeta'|`: `3.258517`
- mean non-exceptional `|zeta''|/|zeta'|`: `3.068314`

Interpretation: the exceptions are not a single compact T-cluster, but they do sit in locally compressed zero-neighborhoods. The strongest full-sample Pearson signal is `Re zeta''` versus `Delta_bar(T)-s_min` (`r=7.32214178608617594e-01`), and exceptional `s_min` is substantially smaller than the non-exceptional mean. This supports a close-pair/local-geometry explanation, though it is not a complete classifier.
