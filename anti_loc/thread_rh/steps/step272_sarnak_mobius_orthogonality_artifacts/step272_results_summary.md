# Step 272 Results Summary

Verdict: `V_sarnak_in_cross_correlation_Ia`.

Sarnak's Mobius-orthogonality carrier was declared as:

```text
Xi_MO(N;T,f,x) = (1/N) |sum_{n<=N} mu(n) f(T^n x)|
```

for every zero-topological-entropy system `(X,T)`, every `f in C(X)`, and
every `x in X`.  Closure is `Xi_MO -> 0` for all admissible data.

Classification:

- **Cross-Correlation Extension**: fits after Type Ia subtype refinement.
  MO is a correlation residual between an arithmetic multiplicative sequence
  and a deterministic zero-entropy sequence.
- **Subconvexity Extension**: excluded.  MO is not a critical-line growth-rate
  residual.  Qualitative MO implies PNT through the trivial dynamical system,
  but it does not imply the RH-strength `sum_{n<=N} mu(n)=O(N^(1/2+epsilon))`
  without an added quantitative rate.
- **Zero-Density Extension**: excluded.  MO is not a zero-count residual.
- **11th finding**: not needed.  Existing Cross-Correlation Extension absorbs
  MO with a new arithmetic-dynamical Type Ia subtype.

Subtype update:

| subtype | description | examples |
|---|---|---|
| Type Ia-pure-arithmetic | coefficient/coefficient correlations | SOC, full Selberg orthonormality |
| Type Ia-arithmetic-dynamical | multiplicative function vs deterministic zero-entropy sequence | Sarnak MO |
| Type Ib | single-L zero correlations | Montgomery, Hejhal |
| Type II | multi-L/family zero correlations | Rudnick-Sarnak, Katz-Sarnak |

Corpus status:

`anti_loc/findings_framework.md` was updated.  Cross-Correlation Extension is
now `candidate (verified-on-5-correlation-instances, all-three-main-subtypes-covered, Type-Ia refined) corpus-pending`.

No proof of MO, RH, subconvexity, or zero-density is claimed.
