# Step 452 Descent Bridge Justification

## Chosen bridge

Use `B = I_tr`, the lawful trace instrument from Step 448 Stage I.4.

Step 448 states: `I_tr` reads completed L-data through admissible trace observables and has the visibility partition:

- visible: completed trace observables in `E^!_Q^tr`;
- suppressed: zero-ledger predictive data not readable at current trace level;
- outside: arithmetic claims not present in the closure record;
- unknown: proposed recognition records not yet accepted, including `Gamma_SDTC`.

This is precisely the lower/current interface through which the zero ledger would have to descend if SAU is to explain the SDTC target by non-descent.

## Alternatives discarded

- `I_zero_ledger_direct`: wrong level. It is predictive/verification access, not lower current trace access.
- `I_finite_window`: too narrow. It would only prove windowed non-descent or windowed visibility.
- Direct canonical zero selector bridge: target-level and not the trace instrument produced by `Sel^!_{zeta,tr}`.

## Bridge verdict

`I_tr` is the correct bridge for this SAU attempt. The failure, if any, must occur in the witness and validation fields, not in bridge selection.
