# Step 448 Zero Ledger and Anti-Invariant Ledger (Stage I.8)

Let `Z_L^nt` be the multiset of nontrivial zeros of the completed function `Lambda_L`, with multiplicities `m_rho`.

Use the positive multiplicity-counting measure

```math
mu_L({rho})=m_rho.
```

Define

```math
A_Z(L)=int_{rho in Z_L^nt} psi_-(rho) psi_-(rho)^* dmu_L(rho)
      = sum_{rho in Z_L^nt} m_rho |Re(rho)-1/2|^2.
```

This is positive semidefinite. In scalar response space it is a nonnegative extended trace-class ledger; for zeta the completed zero ledger is read with the standard exhaustivity/tail convention. If needed, finite ledgers use the moving-ledger tail condition from Step 69.

This is exactly the `A_X` form of `def:main:involutive-ledger`, specialized to the completed zero ledger.
