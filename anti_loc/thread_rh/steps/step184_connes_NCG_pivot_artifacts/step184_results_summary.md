# Step 184: Connes Adelic / NCG Carrier Pivot

Verdict:

`connes_verdict = V_connes_CRCFT_TE`.

Carrier declaration:

The Connes typed carrier is the adelic/noncommutative-geometric carrier built
from the adele class space

```tex
X_Q = A_Q / Q^*
```

with idele class group

```tex
C_Q = A_Q^* / Q^*
```

acting by scaling. The typed Hilbert space `H_C` is the completed quotient or
cohomological carrier used by Connes to remove the trivial representation and
realize the spectral side of the explicit formula. The operator `D_C` is the
infinitesimal generator of the modulus/scaling action on this completed
carrier.

Trace formula:

For suitable test functions `h` on `C_Q`, the Connes trace formula compares
a spectral trace `Tr(pi_C(h)|H_C)` with the arithmetic explicit-formula side:
prime/von-Mangoldt orbital terms plus archimedean terms and pole/trivial
corrections.

Parent residual:

`Xi_Connes` is the typed trace-defect residual between the spectral side and
the completed arithmetic explicit-formula side, after quotienting the trivial
modes and enforcing tail/exhaustivity.

CRCFT classification:

`CRCFT-TE`. A native Connes closure at full strength is the classical Connes
RH-equivalent trace-formula/spectral-realization condition. The inherited
records do not supply an independent completed spectral ledger, determinant
convergence theorem, or tail record. Finite spectral triples remain support
evidence only.

New no-go:

`Connes adelic trace-formula full closure target-equivalence / completed spectral ledger not inherited`.

Coverage status:

`CRCFT_coverage_conjecture_status = strengthens`. Connes adds another CRE
carrier instance in the target-equivalence mode; no non-CRCFT route was found.
