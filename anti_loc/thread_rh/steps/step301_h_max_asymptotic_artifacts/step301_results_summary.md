# Step 301 Results Summary

The far-left circle maxima are modeled with the zeta functional equation
`zeta(z)=chi(z) zeta(1-z)` and the right endpoint `b=3.7` of the final
`G_star` bump in the inherited convention `M(z)=int G(t)t^{-z}dt`.

Near `t=b-y`, the bump satisfies `beta ~ exp(-epsilon/(2y))`, so
`M(G)(z)` is approximated by

`|a_3| b^{-Re z} sqrt(pi) (epsilon/2)^{1/4} |(-z/b)|^{-3/4} exp(-Re(2 sqrt((epsilon/2)(-z/b))))`.

Thus `max_R |h|` is approximated by maximizing the product of this endpoint term with
`|chi(z) zeta(1-z)|` over `z=rho+R exp(i theta)`.  For Cauchy optimization,
the scanned maxima were summarized by the fitted closed form

`log H(R)=d+p R log R+q R+a log R`, with `d=-0.795709839093`, `p=0.921368384281`, `q=-1.04741592856`, `a=4.27182518978`.

Calibration at `z=2`: inherited `t^(-z)` M(G)(2) = `(0.00918536718619776932 + 0.0j)`, standard `t^(z-1)` Mellin = `(0.119078717980621549 + 0.0j)`.

The Cauchy prediction is an upper-bound scale, not an equality: direct rescans at the fitted `R*(k)` show `C_k=predicted/certified` remains large and variable.
