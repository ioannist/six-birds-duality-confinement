# Step 434 Periodic-Orbit Action Audit

The Sierra Hamiltonian has closed classical trajectories. This repairs the open-orbit problem of `H=xp` and permits Bohr-Sommerfeld quantization.

However, the relevant semiclassical object is an EBK/Bohr-Sommerfeld action for a one-dimensional closed orbit family, giving the smooth counting law. It is not a Gutzwiller sum over a primitive orbit spectrum canonically equal to `log p`.

For zeta, the fluctuating explicit formula requires prime-side terms involving `log p` and prime powers. Sierra's model accounts for the smooth Riemann-von Mangoldt term, not the prime fluctuation side.

## Structural comparison

| n | log p_n | Sierra primitive action object | structural match? |
|---:|---:|---|---|
| 1 | 0.693147 | EBK orbit action / smooth level index | no canonical equality |
| 2 | 1.098612 | EBK orbit action / smooth level index | no canonical equality |
| 3 | 1.609438 | EBK orbit action / smooth level index | no canonical equality |
| 4 | 1.945910 | EBK orbit action / smooth level index | no canonical equality |
| 5 | 2.397895 | EBK orbit action / smooth level index | no canonical equality |
| 6 | 2.564949 | EBK orbit action / smooth level index | no canonical equality |
| 7 | 2.833213 | EBK orbit action / smooth level index | no canonical equality |
| 8 | 2.944439 | EBK orbit action / smooth level index | no canonical equality |
| 9 | 3.135494 | EBK orbit action / smooth level index | no canonical equality |
| 10 | 3.367296 | EBK orbit action / smooth level index | no canonical equality |

## Result

`C_length_spectrum_arithmetic_mismatch` is not discharged. Replacing geodesic lengths by phase-space actions avoids the Step 433 geodesic substrate, but the same structural issue reappears: the primitive action spectrum is not derived as `log p`.
