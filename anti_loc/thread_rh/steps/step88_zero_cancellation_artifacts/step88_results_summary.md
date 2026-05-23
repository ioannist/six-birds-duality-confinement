
# Step 88: Zero-Side Low-Frequency Cancellation Audit

This step audits the zero-side cancellation route for the completed zeta paired-Weil carrier.

## Main conclusion

The paired Weil carrier has a legal low-frequency zero:

\[
\Psi(0)=0.
\]

To control capacity near that zero, it is not enough that the zero-side readout is anti-invariant or vanishes at \(\xi=0\). The proof needs a **uniform primitive / derivative factorization**:

\[
\widehat g_y(\xi)=\xi\widehat h_y(\xi),
\qquad
\|h_y\|^2\le y^*\Theta_{\rm prim}y.
\]

Then, when \(\Psi(\xi)\ge c\xi^2\),

\[
\int_{|\xi|<\varepsilon}
\frac{|\widehat g_y(\xi)|^2}{\Psi(\xi)}d\xi
\le
c^{-1}y^*\Theta_{\rm prim}y.
\]

## Warning

Oddness / anti-invariance gives formal cancellation at \(\xi=0\), but not a uniform membrane. A sequence

\[
\widehat g_\varepsilon(\xi)=N_\varepsilon \xi e^{-\xi^2/(2\varepsilon^2)}
\]

has \(\|g_\varepsilon\|=1\) and vanishes at zero, but its capacity relative to \(\Psi(\xi)\sim\xi^2\) grows like \(\varepsilon^{-2}\).

## RH status

The readout

\[
\operatorname{Re}(s)-\frac12
\]

separates off-critical zeros from the critical line. But separation is not the same as low-frequency cancellation in the log-side paired carrier.

The zero-side cancellation route is viable only if the actual zero-side readout has a bounded primitive / derivative-factorization certificate.

## Next pressure point

Either prove that primitive factorization for \(V_Z\), or move to the source-coercivity route.
