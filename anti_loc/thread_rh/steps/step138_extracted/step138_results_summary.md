# Step 138 summary: Ω-threshold optimization for blind-projected incidence

This step chooses the threshold variables in the GCD-log blind-sector repair:

- blind threshold `R`, defining the blind Walsh family `B_R`;
- Ω cutoff `K`, defining the low/high divisibility split;
- prime window `y`, defining the finite squarefree Boolean model.

The main bound is

```tex
δ_{R,K,N} \le L_{R,K}(y)+T_{R,K}(y)σ_{K,N}.
```

Here `L` is low-Ω weighted leakage, `T` is the blind-projected high-tail incidence norm, and `σ` is the actual Burnol/Müntz residual seed tail.

If the GCD-log kernel has lower frame `γ_q β_R` on the nonblind sector and `δ<1`, then the restricted source route retains a positive lower-frame floor:

```tex
R_N^*K_qR_N \succeq γ_q β_R(1-δ^2)G_{B,N}.
```

Exact suppression is not necessary. A uniform positive floor is enough if the source strength diverges and the residual tail promotes to the completed carrier.

The finite numerical checks are only Boolean algebra sanity checks. The open analytic record remains the actual incidence-conditioned Burnol/Müntz seed-tail estimate.
