import SixBirdsDualityConfinement.SourceWorkTrial

/-!
A source-provenance test for a real Hilbert XI return. If the state is
odd under a symmetry, the transport commutes with that symmetry, and
the step returns to the same state, its required source is odd. An
even source can then exist only at a transport fixed point. This is
algebra independent of either application.
-/

noncomputable section
namespace SixBirdsDualityConfinement.EvenSourceParity

open SixBirdsNeedles.XiCore

variable {E F : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [NormedAddCommGroup F] [InnerProductSpace ℝ F]

theorem fixed_odd_even_source_forces_zero
    (S : XiSourceStep E F) (J : E →L[ℝ] E)
    (hfixed : S.after = S.before)
    (hodd : J S.before = -S.before)
    (hcomm : ∀ v, J (S.transport v) = S.transport (J v))
    (heven : J S.source = S.source) :
    S.source = 0 ∧ S.transport S.before = S.before := by
  have hsource : S.source = S.before - S.transport S.before := by
    have hb := S.balance
    rw [hfixed] at hb
    calc
      S.source = (S.transport S.before + S.source) -
          S.transport S.before := by abel
      _ = S.before - S.transport S.before := by rw [← hb]
  have hoddT : J (S.transport S.before) =
      -S.transport S.before := by
    rw [hcomm, hodd, map_neg]
  have hoddsource : J S.source = -S.source := by
    rw [hsource, map_sub, hodd, hoddT]
    module
  have hneg : S.source = -S.source := heven.symm.trans hoddsource
  have htwo : (2 : ℝ) • S.source = 0 := by
    rw [two_smul]
    nth_rewrite 2 [hneg]
    exact add_neg_cancel _
  have hs : S.source = 0 :=
    (smul_eq_zero.mp htwo).resolve_left (by norm_num)
  constructor
  · exact hs
  · have hb := S.balance
    rw [hfixed, hs, add_zero] at hb
    exact hb.symm

theorem fixed_odd_even_source_zero_of_strict_transport
    (S : XiSourceStep E F) (J : E →L[ℝ] E)
    (hfixed : S.after = S.before)
    (hodd : J S.before = -S.before)
    (hcomm : ∀ v, J (S.transport v) = S.transport (J v))
    (heven : J S.source = S.source)
    (hstrict : ∀ v, v ≠ 0 → ‖S.transport v‖ < ‖v‖) :
    S.before = 0 := by
  have hT := (fixed_odd_even_source_forces_zero S J
    hfixed hodd hcomm heven).2
  by_contra hne
  have hlt := hstrict S.before hne
  rw [hT] at hlt
  exact (lt_irrefl _) hlt

#print axioms fixed_odd_even_source_forces_zero
#print axioms fixed_odd_even_source_zero_of_strict_transport

end SixBirdsDualityConfinement.EvenSourceParity
