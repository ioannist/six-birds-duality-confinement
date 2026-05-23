# Step 126: Source-weighted matrix lower-frame import

## Main output

The unweighted finite prime-conductor block is settled, but the RH-relevant source route needs a source-weighted matrix lower frame:

\[
G_{q,w}(m,n)=\sum_{\chi\in\mathcal X_q} w_\chi\chi(n)\overline{\chi(m)}
\succeq \gamma_{q,w} H_N.
\]

For prime \(q\), support \(\mathcal N_N\subset\{1,\dots,L_N\}\), and \(L_N<q\), complete character orthogonality gives

\[
G_q^{\rm all}=(q-1)I.
\]

Removing the principal character gives

\[
G_q^{\rm prim}=(q-1)I-\mathbf 1\mathbf 1^*,
\]

so

\[
\lambda_{\min}(G_q^{\rm prim})=q-1-d_N,
\qquad d_N=|\mathcal N_N|.
\]

This finite frame is not the hard part anymore.

## Active import target

The hard analytic import is the weighted lower-frame theorem:

\[
\sum_{\chi\in\mathcal X_q}w_\chi\left|\sum_{n\in\mathcal N_N}a_n\chi(n)\right|^2
\ge \gamma_{q,w}\|a\|_{H_N}^2
\quad\text{for every }a.
\]

Existing moment and asymptotic-large-sieve results are relevant platforms, but scalar moments do not automatically give this operator-valued inequality.

## Three sufficient routes

1. **Weight floor:** if \(w_\chi\ge w_{\min}>0\), then \(G_{q,w}\ge w_{\min}G_q\). This is usually unavailable for L-weighted sources.

2. **Fluctuation control:** if \(G_{q,w}=\bar wG_q+E_w\) and \(\|E_w\|<\bar w\lambda_{\min}(G_q)\), the lower frame survives.

3. **Matrix moment asymptotic:** prove uniformly in coefficient vectors

\[
a^*G_{q,w}a=\operatorname{Main}(a)+\operatorname{Err}(a),
\qquad
\operatorname{Main}(a)\ge\gamma\|a\|_{H_N}^2,
\qquad
|\operatorname{Err}(a)|\le\varepsilon\operatorname{Main}(a).
\]

This is the project-native operator-valued lift.

## Framework consequence

Combining the weighted lower frame with residual coefficient visibility gives

\[
R_N^*G_{q,w}R_N
\succeq
\gamma_{q,w}c_{\rm hyb,N}G_{R,N}.
\]

The completed residual source route still needs

\[
\gamma_{q,w}c_{\rm hyb,N}\to\infty
\]

plus fixed/exhaustive tail promotion.

## Status

Step 126 imports standard analytic-number-theory infrastructure and identifies the exact nonstandard demand:

\[
\boxed{\text{a source-weighted matrix lower frame on the residual coefficient space.}}
\]

The next step should not re-prove character orthogonality. It should map a specific existing theorem—CIS/asymptotic large sieve, Tang--Wu mixed moments, Pratt--Robles perturbed moments, or recent mollified fourth moments—onto the matrix lower-frame gates and mark exactly which hypotheses fail.
