# Step 415 U^flat Stage II Proper Descent Paths

## U^flat Signature Used Verbatim From Step 356

Step 356 declared:

```text
Sigma = {a, b, c, d, e}
```

with:

```text
b: zeta residual atom
c: comparison atom carrying (lambda_mag, lambda_phase)
d: operator-compatibility audit atom
e: non-descending defect witness
```

and rewrite rules:

```text
R_Z_load: b -> b[data_Z]
R_compare: (a[data_H], b[data_Z]) -> c[lambda_mag, lambda_phase]
R_operator_audit: c -> d[lambda_mag, lambda_phase, operator_status]
R_block: d -> e when any residual is nonzero or operator status is missing
R_admit: d -> d_admissible only when all residuals are zero and operator status is certified
```

For Stage II proper, the comparison atom is used as a local reproduction certificate against known framework-internal values, not as an H6 transfer comparison.

## Case A: Branch C Raw Foreclosure Value

Known value:

```text
|delta_D5(rho_1, G_star)| = 4.27655747020364416822589300031
```

Descent:

```text
b[delta_D5_rho1_G_star]
  --R_Z_load-->
b[data_Z = 4.27655747020364416822589300031]
  --q-->
4.27655747020364416822589300031
  --R_compare against Step 380 certified scalar-->
c[relative_error = 0]
  --R_operator_audit-->
d[pass]
```

## Case B: Branch C Gamma Vector

Known Step 324 vector:

```text
gamma(rho_1..rho_5) = [0.2046, 0.1379, 0.1002, 0.0819, 0.0521]
```

Descent:

```text
b[gamma_vector_rho1_5]
  --R_Z_load-->
b[data_Z = gamma_vector]
  --q-->
[0.2046, 0.1379, 0.1002, 0.0819, 0.0521]
  --R_compare against Step 324 vector-->
c[max_relative_error = 0]
  --R_operator_audit-->
d[pass]
```

## Case C: Zeta Double-Prime Sign Vector

Known Step 377/381 sign vector:

```text
sign Re zeta''(rho_j):
j=1: -1
j=2: -1
j=3: -1
j=4: -1
j=34: +1
```

Descent:

```text
b[zeta_double_prime_sign_vector]
  --R_Z_load-->
b[data_Z = sign_vector]
  --q-->
[-1, -1, -1, -1, +1]
  --R_compare against certified sign vector-->
c[mismatch_rate = 0]
  --R_operator_audit-->
d[pass]
```

## Stage II Status

All three reproductions are non-H6 zeta-side framework facts. They use the same finite operational grammar `G_U_flat` declared at Step 356 and do not introduce a transfer primitive.
