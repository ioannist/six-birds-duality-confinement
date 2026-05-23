# Step 214 Results Summary

## Weyl Sequence

The tested sequence is
\[
  u_n={\kappa_{\rho_n,0}^{1/2}\over \|\kappa_{\rho_n,0}^{1/2}\|},
  \qquad n=1,\ldots,10,
\]
with \(\rho_n=1/2+i\gamma_n\).  The computation uses the Burnol-boundary
kernel model for \(\kappa\),
\[
  \kappa_{\rho_n}(\tau)\approx K_{1/2}^{\Gamma}(1/2+i\tau,\rho_n),
\]
sampled on a 120-node Gauss-Legendre grid in \([-80,80]\).

## Operator

The finite-grid Step 173 model was used:
\[
  Pf=f-\operatorname{sinc}*f-\sum_{j<N}\Psi_j\langle\Psi_j,f\rangle,
  \qquad C_\ell f=(I-P)e^{i\ell\tau}Pf,
\]
with \(\ell=\log 2\) and 24 PSWF terms.

## Results

The normalized values \(\|C_\ell u_n\|\) for \(n=1,\ldots,10\) are:

`1.7549, 1.8267, 0.7935, 1.8325, 1.8053, 1.2944, 1.8086, 1.5118, 1.8302, 1.8271`.

Finite-grid lim-inf estimate:
\[
  \min_{1\le n\le 10}\|C_\ell u_n\| = 0.7934538793.
\]
With a conservative finite-grid/transport-model error floor \(0.05\), the lower
bound remains
\[
  \delta_{10}\ge 0.7434538793.
\]

Robustness for \(\ell=\log 3\) and \(\ell=1.0\) also stayed bounded below:
minimum norms \(0.5442\) and \(0.6161\), respectively.

## Verdict

`V_branch_A_weyl_essential_obstruction` as a finite-grid diagnostic.

This does not prove the full infinite-carrier noncompactness theorem: the
transport theorem and asymptotic weak-null sequence proof still need to be
made exact. It does identify a strong candidate essential-norm obstruction and
exposes the next sub-residual: upgrade the finite diagnostic to an actual Weyl
sequence theorem.
