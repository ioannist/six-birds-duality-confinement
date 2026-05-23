# Step 425 Theorem-Grade Verdict

## Refined Bound Tested

Under the manager-provided Step 424 Selberg-Hejhal scale, this step tests

```text
|g'_rest(rho)| <= C log(qT/(2*pi))
```

and combines it with the Step 423 Archimedean envelope:

```text
|A(rho)|_bound = 2 |L'(rho)| ( |arch'(rho)|_bound + C log(qT/(2*pi)) ).
```

The classifier is:

```text
predicted_signflip = B(rho)>0 and |B(rho)| > |A(rho)|_bound.
```

## Sweep Result

Best tested C: `0.5` with `20/46` matches.
Smallest C achieving 46/46: `none`.

No tested `C in {0.5,1.0,1.5,2.0,3.0}` achieves theorem-grade 46/46 classification. The bound remains too large for all positive exceptional cells because even the log-scale tail plus Archimedean envelope exceeds `|B|`.

## Verbatim Step Anchors

- Step 422: `Re L''(rho) >= 0 iff B(rho) > 0 and |B(rho)| > |A(rho)|`.
- Step 423: `log^2` bound was too loose and certified `0/26` exceptional.
- Step 424: Selberg-Hejhal gives typical `O(log T)`, not `O(log^2 T)`.
