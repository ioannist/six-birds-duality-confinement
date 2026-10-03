import SixBirdsDualityConfinement.RH.ArithmeticXiJensen
import SixBirdsDualityConfinement.RH.RHConditional

/-!
Bridge between the paper's critical-strip zeta-zero statement and
Mathlib's full `RiemannHypothesis` predicate. A nontrivial zeta zero
outside the strip would force a zero of the entire completion there;
the Gamma factor's exceptional points are precisely the excluded
trivial negative-even zeros, while `ζ(0) ≠ 0` handles the origin.
-/

noncomputable section
namespace SixBirdsDualityConfinement.RH.FullClassicalRHBridge

open ClassicalZeroLedger ArithmeticXiJensen

theorem riemannHypothesis_of_criticalStripRH
    (hRH : CriticalStripRH) : RiemannHypothesis := by
  intro s hz hnontrivial hs1
  have hs0 : s ≠ 0 := by
    intro h
    subst s
    norm_num [riemannZeta_zero] at hz
  have hgamma : Complex.Gammaℝ s ≠ 0 := by
    intro h
    obtain ⟨n, hn⟩ := Complex.Gammaℝ_eq_zero_iff.mp h
    cases n with
    | zero =>
        apply hs0
        simpa using hn
    | succ n =>
        apply hnontrivial
        refine ⟨n, ?_⟩
        simpa [Nat.succ_eq_add_one, mul_assoc] using hn
  have hcompleted : completedRiemannZeta s = 0 := by
    rw [riemannZeta_def_of_ne_zero hs0] at hz
    simpa [hgamma] using hz
  have hxi : arithmeticXiEntire s = 0 := by
    rw [arithmeticXiEntire_eq_completed s hs0 hs1, hcompleted]
    ring
  obtain ⟨hlo, hhi⟩ := arithmeticXiEntire_zero_in_critical_strip s hxi
  exact hRH s hz hlo hhi

theorem criticalStripRH_iff_riemannHypothesis :
    CriticalStripRH ↔ RiemannHypothesis := by
  constructor
  · exact riemannHypothesis_of_criticalStripRH
  · exact criticalStripRH_of_riemannHypothesis

/-- The existing recognition-record conditional now reaches Mathlib's
full classical RH predicate. No recognition-source fields are discharged
by this bridge; it only pays the formerly separate zero-localization
step. -/
theorem rhConditionalFullClassical
    {R : Involution.RealCoordinate}
    (shell : SatSelShell.SatSelShell R)
    (gamma : RHConditional.GammaSdtcSelberg shell)
    (ident : RHConditional.ClassicalZeroIdentification shell) :
    RiemannHypothesis :=
  riemannHypothesis_of_criticalStripRH
    (RHConditional.rhConditionalClassical shell gamma ident)

#print axioms riemannHypothesis_of_criticalStripRH
#print axioms criticalStripRH_iff_riemannHypothesis
#print axioms rhConditionalFullClassical

end SixBirdsDualityConfinement.RH.FullClassicalRHBridge
