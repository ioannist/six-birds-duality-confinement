# Step 448 Lawful Trace Instrument (Stage I.4)

`I_tr` is the lawful trace instrument on `H^!_L`. It reads completed L-data through admissible trace observables and records instrument-relative visibility.

Visibility partition:

- visible: completed trace observables in `E^!_Q^tr` with provenance and threshold records;
- suppressed: zero-ledger predictive data not readable at current trace level;
- outside: arithmetic claims not present in the closure record;
- unknown: proposed recognition records not yet accepted, including `Gamma_SDTC`.

`I_tr` distinguishes current-layer trace observables `E^!_Q^tr` from predictive-layer zero-ledger observables `E^!_M^zero`. This prevents the closure from reading RH directly out of the zero ledger while still allowing the translation theorem once `A_Z` is constructed.
