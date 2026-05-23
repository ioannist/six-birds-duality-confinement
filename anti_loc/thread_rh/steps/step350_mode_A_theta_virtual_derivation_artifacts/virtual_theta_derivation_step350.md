# Step 350 Virtual Theta Derivation Attempt

Goal: derive the free-energy field `theta(T,d)` without using the step 324
empirical coefficients in

`theta_empirical(T,d) = 4.118 T^(-0.997) - 0.039 d^(0.409)`.

## GUE / Pair-Correlation Carrier

Let `T = Im(rho)` and let `d` be the nearest-neighbor zero gap.  Under the
Montgomery-GUE spacing heuristic, the average local zero spacing at height
`T` is

`s_GUE(T) = 2 pi / log(T/(2 pi))`.

The local compression ratio is

`kappa(T,d) = s_GUE(T) / d`.

This uses only the height, the local zero gap, and universal constants.

## Candidate Virtual Fields

Three coefficient-free candidates were tested:

1. `theta_1 = kappa / T`.
2. `theta_pi = pi kappa / T`.
3. Prompt-shaped field:
   `theta_prompt = (2 pi / d)/log(T/(2 pi)) - sqrt(d)/(2 pi)`.

The primary candidate is `theta_pi`, since it is the only one with the right
order of magnitude at `rho_1` without empirical tuning.

## Free-Energy Readout

Each candidate field is inserted into the inherited step 349 stationary
equation

`gamma + 0.75 gamma^3 = theta_virtual(T,d)`.

No step 324 fit coefficients are used in the virtual theta candidates.

## Outcome

The best coefficient-free candidate `theta_pi` matches `rho_1` reasonably but
misses `rho_2` and `rho_3` by more than the 30% acceptance threshold.  The
virtual derivation therefore does not replace the empirical field.
