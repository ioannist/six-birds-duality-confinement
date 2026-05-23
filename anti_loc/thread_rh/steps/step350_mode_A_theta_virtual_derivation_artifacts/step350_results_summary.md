# Step 350 Results Summary

Attempted to derive the step 349 free-energy field `theta(T,d)` from
GUE/local-spacing structure rather than inheriting the empirical step 324 fit.

The tested coefficient-free candidates were:

- `theta_1 = kappa/T`
- `theta_pi = pi kappa/T`
- `theta_prompt = (2 pi/d)/log(T/(2 pi)) - sqrt(d)/(2 pi)`

where `kappa = s_GUE(T)/d` and `s_GUE(T) = 2 pi/log(T/(2 pi))`.

The primary no-tune candidate `theta_pi` gave:

| rho | theta_virtual | theta_empirical | theta rel err | gamma_virtual | gamma rel err |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.250094 | 0.207797 | 0.204 | 0.239758 | 0.172 |
| 2 | 0.194920 | 0.129011 | 0.511 | 0.189793 | 0.376 |
| 3 | 0.143228 | 0.097569 | 0.468 | 0.141120 | 0.408 |

Only `rho_1` passes the 30% gamma threshold.  `rho_2` and `rho_3` fail.

Replacing virtual `theta_pi` with the empirical step 349 theta changes the
stationary gamma output by 15.9%, 32.8%, and 31.3% respectively.  The
derivations are distinct, but the virtual derivation is not accurate enough.

Verdict:

`V_mode_A_theta_derivation_failed_empirical_field_still_required`.

This makes the third Mode A calibration an effective cyclic retract for the
purpose of replacing empirical input.  Mode B is licensed under the inherited
memory criterion of at least three non-clone Mode A retracts.
