# Step 273 Results Summary

Verdict: `V_chowla_in_Ia_pure_arithmetic_k_correlation`.

Chowla carrier declaration:

```text
Xi_chowla(a,e;N) =
  N^{-1} |sum_{n<=N} prod_i mu(n+a_i)^{e_i}|
```

with distinct shifts `a_i` and the standard Mobius-power convention
`e_i in {1,2}`.  The `epsilon_i = +/-1` notation is not used literally for
Mobius powers, since `mu(n)^{-1}` is undefined when `mu(n)=0`.

Closure is `Xi_chowla -> 0` for all distinct shifts and nontrivial exponent
patterns.

Classification:

- Chowla fits the Cross-Correlation Extension.
- It is **Type Ia-pure-arithmetic**.
- It requires a sub-sub-type refinement:
  - `2-correlation`: SOC, full Selberg orthonormality.
  - `k-correlation / multi-shift`: Chowla, Elliott.

Known-status audit:

- `k=1` recovers the PNT-scale Mobius average.
- Tao 2016 proved logarithmically averaged two-point Chowla/Elliott cases.
- Tao-Teravainen proved logarithmically averaged odd-order cases.
- Full ordinary Chowla for all `k` remains open.

Corpus status:

`anti_loc/findings_framework.md` was updated.  Cross-Correlation Extension is
now:

```text
candidate (verified-on-6-correlation-instances,
all-three-main-subtypes-covered,
Type-Ia refined and sub-subtyped) corpus-pending
```

No proof of Chowla, Elliott, RH, or any Cross-Correlation target is claimed.
