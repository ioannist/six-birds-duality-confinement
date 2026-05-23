# Step 448 Translation Theorem (Stage II)

**Theorem T.** For the completed zero ledger of `L`,

```math
A_Z(L)=0 \iff RH(L).
```

Equivalently, every nontrivial zero `rho in Z_L^nt` satisfies `Re(rho)=1/2` iff the anti-invariant ledger vanishes.

## Forward direction

By construction,

```math
A_Z(L)=sum_{rho in Z_L^nt} m_rho |Re(rho)-1/2|^2.
```

Each term is nonnegative and `m_rho>0`. If `A_Z(L)=0`, every term vanishes, so `Re(rho)=1/2` for every nontrivial zero. That is `RH(L)`.

## Reverse direction

If `RH(L)` holds, then every nontrivial zero has `Re(rho)=1/2`, hence `psi_-(rho)=0` for every zero and `A_Z(L)=0`.

## Bookkeeping and grade

The proof uses only the definition of `A_Z(L)`, positivity of squared distance, and the fixed-locus readout. It does not use `Gamma_SDTC`, Weil positivity, RH as an assumption, or a recognition source. The theorem is theorem-grade by construction. Its content is near-immediate; the load-bearing work is closure admissibility and future recognition.
