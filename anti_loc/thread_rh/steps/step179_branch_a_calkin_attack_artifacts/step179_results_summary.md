# Step 179: Branch A Calkin Attack

Verdict:

`calkin_class_verdict = V_branch_a_stuck_at_kappa`.

The Step 173 identity gives an operational formula for `P_infty`, hence for

```tex
C_l = (I-P_infty) M_{m_l} P_infty.
```

However the Branch A object is not `C_l` on the ambient Mellin space; it is

```tex
C_l P_eta
```

where `P_eta` is the projection onto

```tex
H_eta = closure span {J_a^*Y^a_{rho,k}}.
```

Under Step 153,

```tex
U_infty eta^a_{rho,k}
= T_a^* partial_{bar rho}^k K_a^Gamma(.,rho)
= kappa_{a,rho,k}.
```

Thus every direct Calkin-class route needs the same `kappa` data isolated in
Steps 177-178.

Attack outcomes:

- T2a matrix elements: blocked because `<eta_i,C_l eta_j>` requires
  `kappa_i,kappa_j`.
- T2b Hilbert-Schmidt / trace: blocked because the kernel/projection of
  `P_eta` requires an orthonormal frame or Gram kernel for `H_eta`, hence
  `kappa`.
- T2c Weyl sequence: blocked because PSWF/hard-support Weyl vectors are not
  actual `H_eta` vectors without a kappa/density theorem.
- T2d Step 175-176 `L_{rho,k}(G)` data: nonzero data do not identify
  `<eta_i,C_l eta_j>` without the pulled evaluator vector.

Branch A implication: neither compactness nor positive essential norm is
decided. Branch A is gated on the same Burnol projected-kernel theorem as
Branch B:

```tex
kappa_{a,rho,k}=T_a^* partial K_a^Gamma(.,rho).
```

CTMT pattern: Branch A Calkin class, Branch A actual Weyl promotion, and Branch
B SL164.1 all reduce to the same kappa / projected Sonine kernel record.
