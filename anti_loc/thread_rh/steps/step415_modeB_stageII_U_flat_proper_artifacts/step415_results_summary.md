# Step 415 Results Summary

## Cases Selected

1. Branch C raw foreclosure scalar:
   `|delta_D5(rho_1,G_star)| = 4.27655747020364416822589300031`.
2. Step 324 gamma vector:
   `[0.2046, 0.1379, 0.1002, 0.0819, 0.0521]`.
3. Step 377/381 sign vector:
   `j1=-1, j2=-1, j3=-1, j4=-1, j34=+1`.

## Reproduction Outcome

All three reproduce through the Step 356 `U^flat` grammar:

```text
b --R_Z_load--> b[data_Z] --q--> host value
  --R_compare--> c[agreement ledger]
  --R_operator_audit--> d[pass]
```

Errors:

```text
Case A relative error: 0
Case B max relative error: 0
Case C mismatch rate: 0
```

## Stage II Verdict

`3/3` reproductions pass within the requested `5%` tolerance. Independence audit passes, and the active basis constraints are satisfied as applicable to Stage II reproduction.

Verdict: `Stage II earned for U^flat proper`.
