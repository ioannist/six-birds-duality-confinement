# Step 404 Results Summary

## Corrected Eq. 3.7 Computation

Using

```text
B_p^+(T)
 = (4*pi*T)^p/(2*pi*(p-2)!)
   * sum_{ell>=1} ell^(p-1) exp(-4*pi*T*ell),
```

for `T in {1,10,100,1000}` and `p in {3,7,12}`.

## B_p Values

At `T=1`:

- `p=3`: `B_p = 0.00110141342687`
- `p=7`: `B_p = 0.228928278022`
- `p=12`: `B_p = 2.38870061501`

At `T=10`:

- `p=3`: `B_p = 8.40224943257e-50`
- `p=7`: `B_p = 1.74603835705e-43`
- `p=12`: `B_p = 1.80934470314e-37`

At `T=100` and `T=1000`, all values are exponentially smaller; see CSV.

## Phi_max Diagnostic

Using compact-sup normalization `B_p/(p^(3/2)/(2*pi))`, the largest tested
value is

```text
T=1, p=12: 0.3610519714.
```

At `T=10`, the largest tested value is

```text
p=12: 2.7348235602e-38.
```

No tested cell matches Step220 `Phi_max = 0.4904766190`.

## Verdict

The corrected diagonal Bergman formula does not reproduce Branch A `Phi_max`.
The previous `1/2` candidate was a formula-extraction artifact.  Branch A still
requires a wavepacket/off-diagonal transport calculation into the Step173
PSWF/sinc `P_infty` model.

No RH claim is made.
