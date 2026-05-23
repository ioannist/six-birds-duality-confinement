# Step 423 Results Summary

## Bound Formulas

```text
|arch'(rho)| <= 0.5|log(pi/q)| + 0.5 log(max(2,(T+a+2)/2)) + zeta pole terms.
|g'_rest(rho)| <= Lambda^2 + |Lambda| + 0.0462, Lambda=log(qT/(2*pi)).
|A(rho)| <= 2|L'(rho)|(|arch'|+|g'_rest|).
```

The corresponding structural spacing condition is

```text
s_min < 2/(K log^2(qT/(2*pi))), with K=4 in the conservative audit.
```

## Classification

- Explicit A-bound classifier: `20/46` total, `0/26` exceptional, `20/20` baseline.
- Spacing-only K=4 classifier: `20/46` total, `0/26` exceptional, `20/20` baseline.

## Verdict

The bound is too loose for theorem-grade closure. It correctly rejects the 20 non-exceptional baseline cells but fails to certify all 26 positive exceptional cells because the global `Lambda^2` far-zero envelope overwhelms the close-pair term. A sharper local Hadamard remainder estimate, not just RvM density, is needed.
