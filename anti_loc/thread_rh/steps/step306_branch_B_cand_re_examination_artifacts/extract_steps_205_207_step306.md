# Step 306 Extracts From Steps 205-207

## Step 205

From `derive_kappa_tau_step205.py`:

> `K_a^Gamma(s,w)=[E_lambda(s)E_lambda(w)-E_lambda(1-s)E_lambda(1-w)]/(s+w-1) in Burnol bilinear convention`

> `K_a^Gamma(1/2+i tau,rho_i)`

> `candidate_shadow_not_certified_as_kappa`

> `T_a^*K_a^Gamma(.,rho_i)(1/2+i tau)=K_a^Gamma(1/2+i tau,rho_i) or corrected explicit U_infty J_a^*M_Gamma^* action`

> `missing_transport_theorem`

> `kappa_i(tau) remains T_a^*K_a^Gamma(.,rho_i), not the raw boundary kernel unless the missing transport theorem is supplied`

From `nonclaim_boundary_step205.md`:

> `This step does **not** certify the candidate boundary-kernel values as `kappa_i(tau)`.`

## Step 206

From `derive_transport_sampling_step206.py`:

> `M_Gamma is the completed Mellin map/multiplier producing M(f)(s)=pi^{-s/2}Gamma(s/2)fhat(s). Its Hilbert-space adjoint M_Gamma^* on L_a^Gamma kernels is not specified as pointwise multiplication in inherited records.`

> `M_Gamma^* K_a^Gamma(.,rho)`

> `inherited records do not define M_Gamma^* on B(E_a) kernels as pointwise gamma multiplication/cancellation`

> `no inherited theorem identifies this with K_a^Gamma(1/2+i tau,rho) or with a gamma-corrected boundary formula`

> `need explicit U_infty J_a^* M_Gamma^* action on B(E_a) reproducing kernels`

## Step 207

From `step207_kappa_candidates_comparison.tex`:

> `This step tests two candidate formulas for
> \[
>   \kappa_i(\tau)=\bigl[T_{1/2}^*K_{1/2}^{\Gamma}(\cdot,\rho_i)\bigr](1/2+i\tau)
> \]`

> `the first candidate is
> \[
>   \mathrm{CAND1}_i(\tau)=K_{1/2}^{\Gamma}(1/2+i\tau,\rho_i).
> \]`

> `The tested candidate is therefore the single-term normalization probe
> \[
>   \mathrm{CAND2}_i(\tau)=
>   \frac{\zeta(1/2+i\tau)}
>   {(1/2+i\tau-\rho_i)\zeta'(\rho_i)\pi^{-\rho_i/2}\Gamma(\rho_i/2)}.
> \]`

> `For \(a=1/2\), Burnol states that suitable linear combinations are required.`

> `Thus the candidates do not agree up to a constant at the available numerical
> level.`

> `Since the transport-sampling formula is unresolved, Step 207 does not select
> either candidate and does not evaluate \(c_{ij}\) or \(\Xi_{\rm matrix\_source}\).`

> `The next typed dependency is the explicit action of
> \[
>   T_a^*=U_\infty J_a^*M_\Gamma^*
> \]
> on \(B(E_a)\) reproducing kernels, or a sharpened proof that the \(a<1\)
> Burnol dual system reduces to a specified linear combination matching the
> boundary kernel.`
