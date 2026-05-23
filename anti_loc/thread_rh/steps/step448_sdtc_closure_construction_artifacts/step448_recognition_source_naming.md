# Step 448 Recognition Source Naming (Stage III)

`Gamma_SDTC-Selberg` is named, not accepted.

## Source statement

`Gamma_SDTC-Selberg` asserts that on the completed self-dual trace closure `Sel^!_{L,tr}`, under `I_tr` and `J_L`, the anti-invariant object ledger collapses:

```math
A_Z(L)=0.
```

Equivalently, in needles.tex Section 5 form, it supplies completed domination records

```math
A_Z(L) <= B_n,   tr B_n -> 0,
```

so `thm:main:duality-confinement-master` yields ledger confinement.

For zeta: `Gamma_SDTC-zeta |- A_Z(zeta)=0`.

## Readout

`Readout_SDTC := A_Z(L)=0`. By Theorem T this is target-equivalent to `RH(L)`.

## Source-record vs readout distinction

The source record is not the readout. It contains:

- `Gamma_DualityConf` from needles.tex Section 5;
- `Gamma_VDiff-TSO(RH)` placement in trace-state-only column;
- `Sel^!_{L,tr}` from this dispatch;
- `I_tr`, `J_L`, `A_Z(L)`;
- `Readout_SDTC`;
- audit/provenance chain steps 65, 67, 69, 71-84, 441-447, and this step.

Status: named source only. Not accepted as recognition source in this dispatch.
