import SixBirdsDualityConfinement.RH.XiSourceStepInstance

/-!
On actual reflected completed-zeta zero windows, a transport commuting with
the J involution preserves the odd displacement sector. If such a transport
is used in a fixed-point source step, its required source is odd too. The
invariant native probe sees none of those three states. This does not claim
that the arithmetic theta/prime constructions induce a J-commuting operator
on zero windows; no such operator has yet been constructed.
-/

noncomputable section
open scoped InnerProduct InnerProductSpace
namespace SixBirdsDualityConfinement.RH.JEquivariantSourceAudit

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution JTransportNoGo
open SixBirdsNeedles.XiCore

theorem invariantVector_J_fixed
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    windowJTransport W hW (invariantVector W) = invariantVector W := by
  ext ρ
  rfl

theorem invariantProbe_J_invariant
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    invariantProbe W (windowJTransport W hW v) =
      invariantProbe W v := by
  change inner ℝ (invariantVector W) (windowJTransport W hW v) =
    inner ℝ (invariantVector W) v
  have h := (windowJTransport W hW).inner_map_map (invariantVector W) v
  rw [invariantVector_J_fixed W hW] at h
  exact h

theorem invariantProbe_zero_of_J_odd
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hodd : windowJTransport W hW v = -v) :
    invariantProbe W v = 0 := by
  have h := invariantProbe_J_invariant W hW v
  rw [hodd, map_neg] at h
  have hv : -(invariantProbe W v) = invariantProbe W v := h
  linarith

theorem commuting_transport_preserves_J_odd
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (T : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hcomm : ∀ v, T (windowJTransport W hW v) =
      windowJTransport W hW (T v))
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hodd : windowJTransport W hW v = -v) :
    windowJTransport W hW (T v) = -T v := by
  rw [← hcomm v, hodd, map_neg]

/-- The exact source in any fixed-point source step is the difference of
the state and its transported image. -/
theorem XiSourceStep.source_eq_of_fixed_point
    {E F : Type*}
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    (S : XiSourceStep E F) (hfixed : S.after = S.before) :
    S.source = S.before - S.transport S.before := by
  calc
    S.source = S.after - S.transport S.before := by rw [S.balance]; abel
    _ = S.before - S.transport S.before := by rw [hfixed]

/-- For an actual J-odd zero-window displacement, any commuting transport
and its fixed-point source are both native-blind. The source can still have
nonzero XI size; no source payment or strict gain is asserted here. -/
theorem commuting_window_step_native_channels_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (T : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hcomm : ∀ v, T (windowJTransport W hW v) =
      windowJTransport W hW (T v))
    (source : EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hbalance : displacementVector m W =
      T (displacementVector m W) + source) :
    invariantProbe W (displacementVector m W) = 0 ∧
      invariantProbe W (T (displacementVector m W)) = 0 ∧
      invariantProbe W source = 0 := by
  let d := displacementVector m W
  have hdodd : windowJTransport W hW d = -d :=
    windowJTransport_displacement_neg m hm W hW
  have hTodd : windowJTransport W hW (T d) = -T d :=
    commuting_transport_preserves_J_odd W hW T hcomm d hdodd
  have hd : invariantProbe W d = 0 :=
    invariantProbe_zero_of_J_odd W hW d hdodd
  have hTd : invariantProbe W (T d) = 0 :=
    invariantProbe_zero_of_J_odd W hW (T d) hTodd
  change d = T d + source at hbalance
  have hs : source = d - T d := by
    calc
      source = (T d + source) - T d := by abel
      _ = d - T d := by rw [← hbalance]
  refine ⟨hd, hTd, ?_⟩
  rw [hs, map_sub, hd, hTd, sub_self]

/-- The preceding probe blindness is exactly blindness of the native XI
currency on the actual state, transported state, and declared source. -/
theorem commuting_window_step_native_currency_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (T : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hcomm : ∀ v, T (windowJTransport W hW v) =
      windowJTransport W hW (T v))
    (source : EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hbalance : displacementVector m W =
      T (displacementVector m W) + source) :
    hilbertNativeCurrency (invariantProbe W) (displacementVector m W) = 0 ∧
      hilbertNativeCurrency (invariantProbe W)
        (T (displacementVector m W)) = 0 ∧
      hilbertNativeCurrency (invariantProbe W) source = 0 := by
  obtain ⟨hd, hTd, hs⟩ :=
    commuting_window_step_native_channels_zero m hm W hW T hcomm source hbalance
  refine ⟨?_, ?_, ?_⟩
  · exact (invariantProbe W).ker.starProjection_orthogonal_apply_eq_zero hd
  · exact (invariantProbe W).ker.starProjection_orthogonal_apply_eq_zero hTd
  · exact (invariantProbe W).ker.starProjection_orthogonal_apply_eq_zero hs

end SixBirdsDualityConfinement.RH.JEquivariantSourceAudit
