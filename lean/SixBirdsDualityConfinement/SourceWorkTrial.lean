import SixBirdsDualityConfinement.RH.OrdinateHeatReturn

/-!
Trial of a problem-independent source-work closure for XI source steps.
This file proves only Hilbert algebra. No actual arithmetic or Navier
source-work estimate is asserted. A scalar fixed-point step below proves
that the proposed strict law cannot hold for every abstract source step.
-/

noncomputable section
open scoped InnerProduct InnerProductSpace
namespace SixBirdsDualityConfinement.SourceWorkTrial

open SixBirdsNeedles.XiCore

variable {E F : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℝ F]

def sourceWork (S : XiSourceStep E F) : ℝ :=
  2 * inner ℝ (hilbertKernelXi S.native (S.transport S.before))
    (hilbertKernelXi S.native S.source) +
      ‖hilbertKernelXi S.native S.source‖ ^ 2

def dissipationGap (S : XiSourceStep E F) : ℝ :=
  ‖hilbertKernelXi S.native S.before‖ ^ 2 -
    ‖hilbertKernelXi S.native (S.transport S.before)‖ ^ 2

/-- A proposed source-formation property: a step starting from zero
does not create a source. This property is separate from the
source-work inequality. -/
def ZeroInputSourceFree (S : XiSourceStep E F) : Prop :=
  S.before = 0 → S.source = 0

omit [CompleteSpace E] in
theorem source_zero_of_zero_endpoints (S : XiSourceStep E F)
    (hbefore : S.before = 0) (hafter : S.after = 0) :
    S.source = 0 := by
  have hbalance := S.balance
  rw [hbefore, hafter, map_zero, zero_add] at hbalance
  exact hbalance.symm

theorem xi_energy_balance (S : XiSourceStep E F) :
    ‖hilbertKernelXi S.native S.after‖ ^ 2 =
      ‖hilbertKernelXi S.native (S.transport S.before)‖ ^ 2 +
        sourceWork S := by
  rw [S.xi_return, norm_add_sq_real]
  unfold sourceWork
  ring

/-- Once the exact return identity is used, source work is the change
in XI energy from the transported state to the returned state. The
source is fixed by the balance field; this identity by itself imposes
no independent bound on the nonlinear or arithmetic source. -/
theorem sourceWork_eq_endpoint_difference (S : XiSourceStep E F) :
    sourceWork S =
      ‖hilbertKernelXi S.native S.after‖ ^ 2 -
        ‖hilbertKernelXi S.native (S.transport S.before)‖ ^ 2 := by
  have h := xi_energy_balance S
  linarith

/-- A fixed-point return makes the source work exactly equal to the
transport's lost XI energy. This uses only the exact return, so it cannot
serve as an independent source estimate. -/
theorem fixed_sourceWork_eq_dissipationGap
    (S : XiSourceStep E F) (hfixed : S.after = S.before) :
    sourceWork S = dissipationGap S := by
  rw [sourceWork_eq_endpoint_difference S, hfixed]
  rfl

/-- A single trial closure inequality. Its source work must be bounded
from the declared native currency and a strict fraction of heat loss. -/
def StrongSourceWork (θ C : ℝ) (S : XiSourceStep E F) : Prop :=
  sourceWork S ≤ θ * dissipationGap S +
    C * ‖hilbertNativeCurrency S.native S.after‖ ^ 2

/-- The same XI source-work law with an external source allowance.
The allowance can be supplied by a separate source calculus; declaring
it here does not establish that any arithmetic or nonlinear source
obeys the bound. -/
def StrongSourceWorkWithBudget (θ C B : ℝ)
    (S : XiSourceStep E F) : Prop :=
  sourceWork S ≤ θ * dissipationGap S +
    C * ‖hilbertNativeCurrency S.native S.after‖ ^ 2 + B

/-- The trial closure is exactly an endpoint energy inequality. Its
independent mathematical content must come from a law that restricts
which returned states are possible for the declared transport and
source provenance. -/
theorem strongSourceWork_iff_endpoint_bound
    (S : XiSourceStep E F) (θ C : ℝ) :
    StrongSourceWork θ C S ↔
      ‖hilbertKernelXi S.native S.after‖ ^ 2 ≤
        θ * ‖hilbertKernelXi S.native S.before‖ ^ 2 +
        (1 - θ) *
          ‖hilbertKernelXi S.native (S.transport S.before)‖ ^ 2 +
        C * ‖hilbertNativeCurrency S.native S.after‖ ^ 2 := by
  rw [StrongSourceWork, sourceWork_eq_endpoint_difference,
    dissipationGap]
  constructor <;> intro h <;> nlinarith

/-- On a fixed-point step, the trial closure is precisely a payment of
the full heat deficit by native currency. In particular, a blind native
channel cannot provide a strict discount unless that deficit vanishes. -/
theorem fixed_strongSourceWork_iff_gap_paid
    (S : XiSourceStep E F) (θ C : ℝ)
    (hfixed : S.after = S.before) :
    StrongSourceWork θ C S ↔
      (1 - θ) * dissipationGap S ≤
        C * ‖hilbertNativeCurrency S.native S.after‖ ^ 2 := by
  rw [StrongSourceWork, fixed_sourceWork_eq_dissipationGap S hfixed]
  constructor <;> intro h <;> nlinarith

/-- At the boundary value `θ = 1`, the heat gain disappears entirely
from the trial premise. -/
theorem strongSourceWork_one_iff_endpoint_bound
    (S : XiSourceStep E F) (C : ℝ) :
    StrongSourceWork 1 C S ↔
      ‖hilbertKernelXi S.native S.after‖ ^ 2 ≤
        ‖hilbertKernelXi S.native S.before‖ ^ 2 +
        C * ‖hilbertNativeCurrency S.native S.after‖ ^ 2 := by
  simpa using strongSourceWork_iff_endpoint_bound S 1 C

/-- A source step born from zero and invisible to the native channel has
no heat loss or native currency to pay for a nonzero return. The proposed
work law therefore forces its entire returned state to vanish, for any
coefficients. This is a general Hilbert fact, independent of arithmetic
or fluid provenance. -/
theorem zero_before_blind_strongSourceWork_iff_after_zero
    (S : XiSourceStep E F) (θ C : ℝ)
    (hbefore : S.before = 0)
    (hblind : hilbertNativeCurrency S.native S.after = 0) :
    StrongSourceWork θ C S ↔ S.after = 0 := by
  have htransport : S.transport S.before = 0 := by
    rw [hbefore, map_zero]
  have hgap : dissipationGap S = 0 := by
    simp [dissipationGap, hbefore]
  constructor
  · intro hwork
    have hxi : ‖hilbertKernelXi S.native S.after‖ ^ 2 ≤ 0 := by
      simpa [StrongSourceWork, sourceWork_eq_endpoint_difference,
        htransport, hgap, hblind] using hwork
    have hcurrency := hilbert_xi_currency S.native S.after
    rw [hblind, norm_zero] at hcurrency
    have hnorm : ‖S.after‖ = 0 := by
      nlinarith [sq_nonneg (‖S.after‖)]
    exact norm_eq_zero.mp hnorm
  · intro hafter
    have hsource : S.source = 0 :=
      source_zero_of_zero_endpoints S hbefore hafter
    simp [StrongSourceWork, sourceWork, hsource, hgap, hblind]

theorem xi_after_le_before_add_native
    (S : XiSourceStep E F) (θ C : ℝ)
    (hθ : θ ≤ 1)
    (hheat : ‖hilbertKernelXi S.native (S.transport S.before)‖ ^ 2 ≤
      ‖hilbertKernelXi S.native S.before‖ ^ 2)
    (hwork : StrongSourceWork θ C S) :
    ‖hilbertKernelXi S.native S.after‖ ^ 2 ≤
      ‖hilbertKernelXi S.native S.before‖ ^ 2 +
        C * ‖hilbertNativeCurrency S.native S.after‖ ^ 2 := by
  have hbalance := xi_energy_balance S
  unfold StrongSourceWork sourceWork dissipationGap at hwork
  unfold sourceWork at hbalance
  have hgap : 0 ≤
      ‖hilbertKernelXi S.native S.before‖ ^ 2 -
        ‖hilbertKernelXi S.native (S.transport S.before)‖ ^ 2 := sub_nonneg.mpr hheat
  nlinarith [mul_nonneg (sub_nonneg.mpr hθ) hgap]

/-- Heat contraction and a budgeted source law bound returned XI by
initial XI, native currency, and the declared external allowance. -/
theorem xi_after_le_before_add_native_and_budget
    (S : XiSourceStep E F) (θ C B : ℝ)
    (hθ : θ ≤ 1)
    (hheat : ‖hilbertKernelXi S.native (S.transport S.before)‖ ^ 2 ≤
      ‖hilbertKernelXi S.native S.before‖ ^ 2)
    (hwork : StrongSourceWorkWithBudget θ C B S) :
    ‖hilbertKernelXi S.native S.after‖ ^ 2 ≤
      ‖hilbertKernelXi S.native S.before‖ ^ 2 +
        C * ‖hilbertNativeCurrency S.native S.after‖ ^ 2 + B := by
  have hbalance := xi_energy_balance S
  unfold StrongSourceWorkWithBudget sourceWork dissipationGap at hwork
  unfold sourceWork at hbalance
  have hgap : 0 ≤
      ‖hilbertKernelXi S.native S.before‖ ^ 2 -
        ‖hilbertKernelXi S.native (S.transport S.before)‖ ^ 2 :=
    sub_nonneg.mpr hheat
  nlinarith [mul_nonneg (sub_nonneg.mpr hθ) hgap]

/-- On a fixed point with zero native currency, strict source-work
discount can hold only if the heat dissipation gap vanishes. -/
theorem fixed_native_zero_forces_zero_gap
    (S : XiSourceStep E F) (θ C : ℝ)
    (hθ : θ < 1) (hfixed : S.after = S.before)
    (hnative : hilbertNativeCurrency S.native S.after = 0)
    (hheat : 0 ≤ dissipationGap S)
    (hwork : StrongSourceWork θ C S) :
    dissipationGap S = 0 := by
  have hbalance := xi_energy_balance S
  rw [hfixed] at hbalance
  unfold StrongSourceWork at hwork
  rw [hnative, norm_zero] at hwork
  unfold dissipationGap at *
  nlinarith [mul_nonneg (sub_pos.mpr hθ).le hheat]

/-- A strict work discount is impossible at any nonzero heat-loss fixed
point whose returned state is invisible to the native probe. -/
theorem strict_work_fails_at_blind_fixed
    (S : XiSourceStep E F) (θ C : ℝ)
    (hθ : θ < 1) (hfixed : S.after = S.before)
    (hnative : hilbertNativeCurrency S.native S.after = 0)
    (hgap : 0 < dissipationGap S) :
    ¬ StrongSourceWork θ C S := by
  intro hwork
  have hz := fixed_native_zero_forces_zero_gap S θ C hθ hfixed
    hnative hgap.le hwork
  linarith

/-- A one-dimensional source exactly restores what a contractive transport
removed. It is a control showing that the generic Hilbert source-step type
alone cannot imply strict source-work closure. -/
def scalarBlindFixedStep : XiSourceStep ℝ ℝ where
  native := 0
  transport := (1 / 2 : ℝ) • ContinuousLinearMap.id ℝ ℝ
  before := 1
  after := 1
  source := 1 / 2
  balance := by norm_num

private theorem scalarBlindFixedStep_xi (x : ℝ) :
    hilbertKernelXi scalarBlindFixedStep.native x = x := by
  apply (scalarBlindFixedStep.native.ker.starProjection_eq_self_iff).mpr
  simp [scalarBlindFixedStep]

private theorem scalarBlindFixedStep_native (x : ℝ) :
    hilbertNativeCurrency scalarBlindFixedStep.native x = 0 := by
  apply scalarBlindFixedStep.native.ker.starProjection_orthogonal_apply_eq_zero
  simp [scalarBlindFixedStep]

theorem scalarBlindFixedStep_gap_pos :
    0 < dissipationGap scalarBlindFixedStep := by
  have htransport : scalarBlindFixedStep.transport scalarBlindFixedStep.before =
      (1 / 2 : ℝ) := by norm_num [scalarBlindFixedStep]
  rw [dissipationGap, htransport]
  change 0 < ‖hilbertKernelXi scalarBlindFixedStep.native (1 : ℝ)‖ ^ 2 -
    ‖hilbertKernelXi scalarBlindFixedStep.native (1 / 2 : ℝ)‖ ^ 2
  rw [scalarBlindFixedStep_xi, scalarBlindFixedStep_xi]
  norm_num

theorem scalarBlindFixedStep_forbids_strict_work (θ C : ℝ)
    (hθ : θ < 1) :
    ¬ StrongSourceWork θ C scalarBlindFixedStep := by
  apply strict_work_fails_at_blind_fixed scalarBlindFixedStep θ C hθ
  · rfl
  · exact scalarBlindFixedStep_native _
  · exact scalarBlindFixedStep_gap_pos

theorem no_universal_strict_source_work (θ C : ℝ) (hθ : θ < 1) :
    ¬ ∀ S : XiSourceStep ℝ ℝ, StrongSourceWork θ C S := by
  intro h
  exact scalarBlindFixedStep_forbids_strict_work θ C hθ (h scalarBlindFixedStep)

/-- An abstract zero-input blind birth with a nonzero source. It isolates
the shape of the arithmetic birth operation without asserting that it
has the arithmetic divisor's provenance. -/
def scalarBlindBirthStep : XiSourceStep ℝ ℝ where
  native := 0
  transport := ContinuousLinearMap.id ℝ ℝ
  before := 0
  after := 1
  source := 1
  balance := by norm_num

/-- The same blind birth with arbitrary returned amplitude. -/
def scalarBlindBirthStepScaled (r : ℝ) : XiSourceStep ℝ ℝ where
  native := 0
  transport := ContinuousLinearMap.id ℝ ℝ
  before := 0
  after := r
  source := r
  balance := by simp

/-- No finite scalar allowance makes the budgeted source-work law valid
for every abstract zero-input blind birth. Its formation domain must
exclude arbitrary source insertion. -/
theorem no_universal_budgeted_source_work (θ C B : ℝ) :
    ¬ ∀ S : XiSourceStep ℝ ℝ,
      StrongSourceWorkWithBudget θ C B S := by
  intro h
  let r : ℝ := |B| + 1
  let S := scalarBlindBirthStepScaled r
  have hwork := h S
  have hxi : hilbertKernelXi S.native S.after = r := by
    apply (S.native.ker.starProjection_eq_self_iff).mpr
    simp [S, scalarBlindBirthStepScaled]
  have hnative : hilbertNativeCurrency S.native S.after = 0 := by
    apply S.native.ker.starProjection_orthogonal_apply_eq_zero
    simp [S, scalarBlindBirthStepScaled]
  have hbound : ‖r‖ ^ 2 ≤ B := by
    unfold StrongSourceWorkWithBudget at hwork
    rw [sourceWork_eq_endpoint_difference,
      show S.transport S.before = 0 by simp [S, scalarBlindBirthStepScaled],
      hxi, hnative] at hwork
    have hgap : dissipationGap S = 0 := by
      simp [dissipationGap, S, scalarBlindBirthStepScaled]
    rw [hgap] at hwork
    simpa using hwork
  have hr : B < r ^ 2 := by
    dsimp [r]
    have habs : B ≤ |B| := le_abs_self B
    nlinarith [abs_nonneg B]
  rw [Real.norm_eq_abs, sq_abs] at hbound
  exact (not_lt_of_ge hbound) hr

/-- A work law over all zero-input, native-blind births is already false
on this scalar control, including at the boundary coefficient `θ = 1`.
Any viable common formation criterion must exclude this control by
substantive source provenance while admitting the actual RH births. -/
theorem scalarBlindBirthStep_forbids_work (θ C : ℝ) :
    ¬ StrongSourceWork θ C scalarBlindBirthStep := by
  intro hwork
  have hblind : hilbertNativeCurrency scalarBlindBirthStep.native
      scalarBlindBirthStep.after = 0 := by
    apply scalarBlindBirthStep.native.ker.starProjection_orthogonal_apply_eq_zero
    simp [scalarBlindBirthStep]
  have hzero := (zero_before_blind_strongSourceWork_iff_after_zero
    scalarBlindBirthStep θ C rfl hblind).mp hwork
  norm_num [scalarBlindBirthStep] at hzero

#print axioms scalarBlindFixedStep_forbids_strict_work
#print axioms source_zero_of_zero_endpoints
#print axioms no_universal_strict_source_work
#print axioms sourceWork_eq_endpoint_difference
#print axioms xi_after_le_before_add_native_and_budget
#print axioms no_universal_budgeted_source_work
#print axioms fixed_sourceWork_eq_dissipationGap
#print axioms fixed_strongSourceWork_iff_gap_paid
#print axioms strongSourceWork_iff_endpoint_bound
#print axioms strongSourceWork_one_iff_endpoint_bound
#print axioms zero_before_blind_strongSourceWork_iff_after_zero
#print axioms scalarBlindBirthStep_forbids_work

end SixBirdsDualityConfinement.SourceWorkTrial
