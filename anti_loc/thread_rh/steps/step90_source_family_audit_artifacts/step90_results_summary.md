# Step 90 — Candidate zeta source-family audit

This step audits candidate upstream-visible source ladders for the RH root-composite route. The gate is

\[
F_n=\sum_{s\in\mathcal S_n}\lambda_s Q_s^*\Theta_s^{-1}Q_s
\succeq \Lambda_n(\Theta_0^-)^{-1},
\qquad \Lambda_n\to\infty.
\]

If this lower frame holds on the completed anti-invariant response sector, then

\[
K_n^-\preceq \Lambda_n^{-1}\Theta_0^-\to0.
\]

The audit conclusion is:

- Prime-by-prime sources are upstream-visible and natural, but by themselves look like shift/log-frequency sources and inherit the low-frequency soft mode. They are support evidence unless paired with low-frequency and tail records.
- Dirichlet and Hecke character sources are the strongest root-composite candidates because finite character orthogonality gives actual lower frames.
- Selberg/automorphic sources may work if the carrier is chosen to be trace/automorphic, but they are carrier-dependent.
- de Branges kernels are a carrier candidate, not yet a source ladder.

The strongest path to pursue appears to be a conductor-indexed Dirichlet/Hecke character-source ladder, with a strict no-smuggling rule: sources must be declared upstream, not selected from off-critical-zero data.
