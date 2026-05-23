import SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger
import SixBirdsDualityConfinement.DualityConfinement.Separation

/-!
# Duality Confinement paper -- `DirectConfinement`

Direct confinement consequences, qualitative and quantitative, derived
from the trace identity plus separation.
-/

namespace SixBirdsDualityConfinement.DualityConfinement.DirectConfinement

universe u v w z q r

/--
Separation confinement in the finite visible-support regime.

The abstract proposition `mu_nonfixed_zero` represents
`mu (X \ Fix(J)) = 0`.  The two bridge hypotheses spell out the
measure-theoretic reading of `psi_minus_ae_zero`: it gives the
measure-zero confinement statement, and in the finite positive-weight
case it gives pointwise vanishing on visible support.  Separation then
identifies those visible objects with `Fix(J)`.
-/
theorem separationConfinement
    {ledger :
      Involution.InvolutiveObjectLedger.{u, v, w}}
    (sep : Separation.SeparatingReadout.{u, v, w, r} ledger)
    (A :
      AntiInvariantLedger.AntiInvariantLedger.{u, v, w, z, q}
        ledger)
    (same_readout :
      ∀ x : ledger.X, A.psi_minus x = sep.psi_minus x)
    (mu_nonfixed_zero : Prop)
    (mu_zero_of_ae : A.psi_minus_ae_zero → mu_nonfixed_zero)
    (visible_zero_of_ae :
      A.psi_minus_ae_zero →
        ∀ x : ledger.X, x ∈ ledger.mu_support →
          A.psi_minus x = sep.zero_Y)
    (hzero : A.A_X = A.zero) :
    mu_nonfixed_zero ∧
      ∀ x : ledger.X, x ∈ ledger.mu_support → ledger.J x = x := by
  have hTrace :=
    AntiInvariantLedger.traceIdentity A
  have hAe : A.psi_minus_ae_zero := hTrace.right.mp hzero
  refine And.intro (mu_zero_of_ae hAe) ?_
  intro x hx
  have hAZero : A.psi_minus x = sep.zero_Y :=
    visible_zero_of_ae hAe x hx
  have hSepZero : sep.psi_minus x = sep.zero_Y := by
    rw [← same_readout x]
    exact hAZero
  exact (sep.separates_fixed_locus_on_visible x hx).mp hSepZero

/--
Quantitative confinement from quantitative separation and Markov's
inequality.

For each positive `epsilon`, `measure_far_bound epsilon` denotes the
paper inequality
`mu {x | dist(x, Fix(J)) >= epsilon} <= tr(A_X) / m(epsilon)^2`.
The `markov_bound` hypothesis is the abstract Markov step applied to
the trace identity and the pointwise lower bound supplied by
quantitative separation.
-/
theorem quantitativeConfinement
    {ledger :
      Involution.InvolutiveObjectLedger.{u, v, w}}
    (sep : Separation.SeparatingReadout.{u, v, w, r} ledger)
    (A :
      AntiInvariantLedger.AntiInvariantLedger.{u, v, w, z, q}
        ledger)
    (measure_far_bound : sep.Scale → Prop)
    (markov_bound :
      ∀ ε : sep.Scale,
        sep.ScalePositive ε →
          (∀ x : ledger.X,
            sep.ScaleGE (sep.dist_to_fix x) ε →
              sep.ScaleGE (sep.norm_psi_minus x) (sep.modulus ε)) →
            A.tr A.A_X = A.integral_sq_norm →
              measure_far_bound ε) :
    ∀ ε : sep.Scale,
      sep.ScalePositive ε → measure_far_bound ε := by
  intro ε hε
  have hTrace :=
    AntiInvariantLedger.traceIdentity A
  exact
    markov_bound ε hε
      (sep.quantitatively_separating ε hε)
      hTrace.left

end SixBirdsDualityConfinement.DualityConfinement.DirectConfinement
