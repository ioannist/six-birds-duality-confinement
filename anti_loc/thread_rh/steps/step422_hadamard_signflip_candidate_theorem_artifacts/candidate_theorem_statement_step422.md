# Step 422 Candidate Theorem Statement

## Candidate Theorem

Let `L(s, chi)` be a primitive Dirichlet L-function and let `rho` be a simple critical-line zero. Write

```text
g'(rho) = arch(rho) + g'_near(rho) + g'_rest(rho),
g'_near(rho) = -1/(rho_nearest-rho).
```

Define

```text
A(rho) = 2 Re[L'(rho)(arch(rho)+g'_rest(rho))],
B(rho) = 2 Re[L'(rho)g'_near(rho)].
```

Then the candidate sign-flip criterion is:

```text
Re L''(rho) >= 0  iff  B(rho) > 0 and |B(rho)| > |A(rho)|.
```

## Audit Result

- Exceptional set: `26/26` matched.
- Non-exceptional baseline: `20/20` matched.
- Total: `46/46` matched.

## Edge Cases

- chi_3 j=39: |A|=4.94616, |B|=5.11588, rel_gap=0.0332, group=exceptional
- chi_13 j=10: |A|=4.8684, |B|=5.27057, rel_gap=0.0763, group=exceptional
- chi_5 j=22: |A|=5.38539, |B|=5.98431, rel_gap=0.1001, group=exceptional
- chi_11 j=21: |A|=6.44712, |B|=7.37372, rel_gap=0.1257, group=exceptional
- chi_7 j=10: |A|=3.29269, |B|=3.87125, rel_gap=0.1495, group=exceptional
- chi_7 j=3: |A|=2.8574, |B|=2.43015, rel_gap=0.1495, group=non_exceptional_baseline
- zeta j=92: |A|=3.28642, |B|=3.87433, rel_gap=0.1517, group=exceptional
- chi_13 j=2: |A|=3.06627, |B|=2.58391, rel_gap=0.1573, group=non_exceptional_baseline

## Verdict

candidate theorem statement is empirically exact on the 46-cell audit set. This is still a candidate theorem, not a proof: the remaining theorem-grade task is an analytic bound on `A(rho)` in terms of conductor, height, and neighboring zero geometry.
