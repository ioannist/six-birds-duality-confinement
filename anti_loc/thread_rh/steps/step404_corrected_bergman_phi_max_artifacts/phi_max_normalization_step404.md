# Step 404: Corrected Bergman Eq. 3.7 Normalization

## Formula Used

The corrected Auvray-Ma-Marinescu full-paper formula supplied for this step is

```text
B_p^{D*}(z)
 = (log|z|^2)^p/(2*pi*(p-2)!)
   * sum_{ell=1}^infty ell^(p-1) * |z|^(2*ell).
```

With `z=exp(2*pi*i*w)`, `Im(w)=T`,

```text
|z|^2 = exp(-4*pi*T),      x=-log|z|^2=4*pi*T,
|z|^(2*ell)=exp(-x*ell).
```

For positivity of the Bergman kernel, the computation reports the standard
positive convention

```text
B_p^+(T)
 = x^p/(2*pi*(p-2)!)
   * sum_{ell>=1} ell^(p-1) exp(-x*ell).
```

The literal signed value with `(log|z|^2)^p=(-x)^p` is also recorded; it is
negative for odd `p`.

## Normalization Test

A diagnostic compact-part normalization was computed:

```text
Phi_diag(p,T) = B_p^+(T) / (p^(3/2)/(2*pi)).
```

This is not claimed to be the true Step220 wavepacket norm; it is the natural
test requested against Auvray-Ma-Marinescu Corollary 2.3.

## Outcome

At `T=1`, the largest diagnostic value among `p=3,7,12` is

```text
p=12: Phi_diag = 0.3610519714.
```

This is still far from the Step220 value `0.4904766190`.

At `T=10`, all values are exponentially small:

```text
p=3:  ~1.016e-49
p=7:  ~5.924e-44
p=12: ~2.735e-38
```

At `T=100` and `T=1000`, the values are even smaller.

## Interpretation

The corrected diagonal Bergman kernel does not reproduce Step220's flat
large-`T` value near `0.4905`.  A polynomial Poincare volume factor cannot
turn the exponential `exp(-4*pi*T)` cusp decay into the Step220 flat
PSWF/sinc wavepacket norm.

Thus the earlier `Phi_max ~= 1/2` candidate was a formula-extraction artifact.
Branch A is not closed by the corrected diagonal Bergman kernel alone.

The remaining object needed is still an off-diagonal/log-cusp transport from
the corrected Bergman kernel to the Step173 PSWF/sinc `P_infty` action.
