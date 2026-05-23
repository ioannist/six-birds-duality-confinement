# Step 85: Low-Frequency Coercivity Gate for the Paired Weil Carrier

## Main point

The paired prime/gamma feature package is positive, but it is not automatically coercive. Paired shift/CND carriers satisfy

\[
\Psi(0)=0.
\]

Thus they have a legal zero at low frequency. Positivity of the paired completed Weil feature does not by itself yield anti-invariant budget collapse.

## Main theorem

For a CND/paired shift symbol

\[
\Psi(\xi)=c\xi^2+2\int(1-\cos(a\xi))\,\mu(da),
\]

we always have

\[
\Psi(0)=0.
\]

If the response space permits arbitrarily low frequencies, then there is no positive spectral gap:

\[
\inf \frac{\int \Psi(\xi)|\widehat f(\xi)|^2d\xi}{\int |\widehat f(\xi)|^2d\xi}=0.
\]

The anti-invariant condition does not remove this zero: odd/anti-invariant low-frequency wave packets can still concentrate near \(\xi=0\).

## Low-frequency cancellation criterion

If near zero

\[
\Psi(\xi)\asymp |\xi|^{2r},
\]

and

\[
|\widehat g(\xi)|\lesssim |\xi|^s,
\]

then the local capacity integral

\[
\int_{|\xi|<\varepsilon}\frac{|\widehat g(\xi)|^2}{\Psi(\xi)}d\xi
\]

is finite in one dimension iff

\[
s>r-\frac12.
\]

For the usual shift-difference zero \(r=1\), this becomes

\[
s>\frac12.
\]

## RH implication

The paired prime/gamma carrier is a positive candidate, but the RH route still needs a legal-zero record:

1. quotient/gap record;
2. low-frequency cancellation of the zero-side readout;
3. strict-extension source growth giving full-sector coercivity;
4. explicit low-frequency defect/nonclaim record.

## Bottom line

Positive paired Weil features are necessary but not sufficient. The next analytic gate is low-frequency coercivity / legal-zero handling.
