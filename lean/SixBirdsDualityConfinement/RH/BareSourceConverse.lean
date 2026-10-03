import SixBirdsDualityConfinement.RH.ClassicalBareShell

/-!
Adversarial calibration of the abstract recognition-source type. On the
bare classical shell, RH itself can populate the type with a one-object
zero-energy DC model. Thus inhabitation of the type, without a specified
Selberg trace construction, is target-equivalent and must not be presented
as an independent source derivation.
-/

noncomputable section
open Filter
open scoped Topology

namespace SixBirdsDualityConfinement.RH.BareSourceConverse

open ClassicalZeroLedger ClassicalBareShell
open SixBirdsDualityConfinement.DualityConfinement

def pointLedger : Involution.InvolutiveObjectLedger where
  X := Unit
  J := id
  J_involutive := by intro x; rfl
  Weight := ℝ
  WeightPositive := fun w => 0 < w
  mu := fun _ => 1
  mu_positive := by intro; norm_num
  mu_support := [()]
  mu_support_complete := by intro x; cases x; simp
  Y := ℝ
  Scalar := ℝ
  add := (· + ·)
  smul := (· * ·)
  inner := (· * ·)
  norm := abs
  J_iso := Neg.neg
  J_iso_involutive := by intro y; simp
  J_iso_linear := by intro a y z; ring
  J_iso_isometry := by intro y; simp
  psi := fun _ => 0
  psi_equivariant := by intro x; simp

def pointSeparation : Separation.SeparatingReadout pointLedger where
  psi_minus := by change Unit → ℝ; exact fun _ => 0
  zero_Y := by change ℝ; exact 0
  separates_fixed_locus_on_visible := by intro x hx; simp [pointLedger]
  Scale := ℝ
  ScalePositive := fun ε => 0 < ε
  ScaleGE := (· ≥ ·)
  dist_to_fix := fun _ => 0
  norm_psi_minus := fun _ => 0
  modulus := id
  modulus_positive := by intro ε h; exact h
  quantitatively_separating := by
    intro ε hε x hx
    exfalso
    exact (not_le_of_gt hε) hx

def pointAntiInvariantLedger :
    AntiInvariantLedger.AntiInvariantLedger pointLedger where
  psi_minus := by change Unit → ℝ; exact fun _ => 0
  Cone := ℝ
  TraceValue := ℝ
  zero := 0
  A_X := 0
  Positive := fun a => 0 ≤ a
  positive_A_X := by norm_num
  preceq := (· ≤ ·)
  tr := id
  TraceLE := (· ≤ ·)
  trace_mono := by intro a b h; exact h
  integral_sq_norm := 0
  trace_identity := rfl
  psi_minus_ae_zero := True
  zero_iff_ae_zero := by simp

/-- This constructor uses RH to fill the hard readout equation. It is a
control on the generic source type, not a Selberg trace construction. -/
def gammaOfRH (hRH : CriticalStripRH) :
    RHConditional.GammaSdtcSelberg bareShell where
  ledger := pointLedger
  sep := pointSeparation
  A := pointAntiInvariantLedger
  same_readout := by intro x; rfl
  visible_zero_of_ae := by
    intro h x hx
    simp [pointAntiInvariantLedger, pointSeparation]
  zero_object := fun _ => ()
  zero_object_visible := by intro ρ; simp [pointLedger]
  encode := id
  encode_faithful := by intro r h; exact h
  readout_formula := by
    intro ρ
    have hz : riemannZeta ρ.val = 0 :=
      (completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp ρ.property.1
    have hr := hRH ρ.val hz ρ.property.2.1 ρ.property.2.2
    simp only [pointAntiInvariantLedger, bareShell, zeroLedger,
      fromComplex, realCoordinate, Function.id_def]
    change (0 : ℝ) = ρ.val.re - 1 / 2
    rw [hr]
    norm_num
  B_n := by change ℕ → ℝ; exact fun _ => 0
  domination_records := by intro n; change (0 : ℝ) ≤ 0; exact le_refl _
  B_n_positive := by intro n; change (0 : ℝ) ≤ 0; exact le_refl _
  traceReal := id
  traceReal_mono := by intro a b h; exact h
  traceReal_nonneg := by intro C hC; exact hC
  traceReal_zero_reflect := by intro t h; exact h
  trace_decay := by
    change Tendsto (fun _ : ℕ => (0 : ℝ)) atTop (𝓝 0)
    exact tendsto_const_nhds
  trace_zero_faithful := by intro h; rfl

/-- On the exact bare classical shell, mere inhabitation of the abstract
gamma record is logically equivalent to the critical-strip RH target. -/
theorem gamma_nonempty_iff_criticalStripRH :
    Nonempty (RHConditional.GammaSdtcSelberg.{0, 0, 0, 0, 0, 0, 0} bareShell) ↔
      CriticalStripRH := by
  constructor
  · rintro ⟨gamma⟩
    exact bareShell_gamma_implies_criticalStripRH gamma
  · intro hRH
    exact ⟨gammaOfRH hRH⟩


universe u v w h i eqv em ql ml vis audit

/-- A faithful zero detector on any real-coordinate carrier. -/
def zeroEncode {R : Involution.RealCoordinate.{u}} (r : R.Real) : ℝ := by
  classical
  exact if r = R.zero then 0 else 1

theorem zeroEncode_eq_zero_iff {R : Involution.RealCoordinate.{u}} (r : R.Real) :
    zeroEncode r = 0 ↔ r = R.zero := by
  classical
  by_cases hr : r = R.zero <;> simp [zeroEncode, hr]

/-- Every shell critical-line statement populates the generic recognition source
with the existing one-point zero-energy model. All shell universes are arbitrary;
the six DC apparatus universes are the level-zero universes of that model. -/
def gammaOfShellCriticalLine {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell.{u, v, w, h, i, eqv, em, ql, ml, vis, audit} R)
    (hline : ∀ rho : shell.Z_nt.Z_zeta_nt, (shell.Z_nt.rho rho).re = R.half) :
    RHConditional.GammaSdtcSelberg.{u, 0, 0, 0, 0, 0, 0, v, audit, w, h, i, eqv, em, ql, ml, vis}
      shell where
  ledger := pointLedger
  sep := pointSeparation
  A := pointAntiInvariantLedger
  same_readout := by intro x; rfl
  visible_zero_of_ae := by
    intro ha x hx
    simp [pointAntiInvariantLedger, pointSeparation]
  zero_object := fun _ => ()
  zero_object_visible := by intro rho; simp [pointLedger]
  encode := zeroEncode
  encode_faithful := by
    intro r hr
    exact (zeroEncode_eq_zero_iff r).mp hr
  readout_formula := by
    intro rho
    have hz : R.sub (shell.Z_nt.rho rho).re R.half = R.zero :=
      (R.sub_half_eq_zero_iff _).mpr (hline rho)
    change (0 : ℝ) = zeroEncode (R.sub (shell.Z_nt.rho rho).re R.half)
    rw [hz]
    exact ((zeroEncode_eq_zero_iff R.zero).mpr rfl).symm
  B_n := by change ℕ → ℝ; exact fun _ => 0
  domination_records := by intro n; change (0 : ℝ) ≤ 0; exact le_refl _
  B_n_positive := by intro n; change (0 : ℝ) ≤ 0; exact le_refl _
  traceReal := id
  traceReal_mono := by intro a b hab; exact hab
  traceReal_nonneg := by intro C hC; exact hC
  traceReal_zero_reflect := by intro t ht; exact ht
  trace_decay := by
    change Tendsto (fun _ : ℕ => (0 : ℝ)) atTop (𝓝 0)
    exact tendsto_const_nhds
  trace_zero_faithful := by intro ha; rfl

/-- The generic recognition-source type is target-equivalent on every shell. -/
theorem gamma_nonempty_iff_shell_criticalLine {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell.{u, v, w, h, i, eqv, em, ql, ml, vis, audit} R) :
    Nonempty (RHConditional.GammaSdtcSelberg.{u, 0, 0, 0, 0, 0, 0, v, audit, w, h, i, eqv, em, ql, ml, vis}
      shell) ↔ ∀ rho : shell.Z_nt.Z_zeta_nt, (shell.Z_nt.rho rho).re = R.half := by
  constructor
  · rintro ⟨gamma⟩
    exact RHConditional.rhConditional shell gamma
  · intro hline
    exact ⟨gammaOfShellCriticalLine shell hline⟩

/-- The general shell calibration agrees with the retained bare-shell RH calibration. -/
theorem bareShell_criticalLine_iff_criticalStripRH :
    (∀ rho : bareShell.Z_nt.Z_zeta_nt,
      (bareShell.Z_nt.rho rho).re = realCoordinate.half) ↔ CriticalStripRH :=
  (gamma_nonempty_iff_shell_criticalLine bareShell).symm.trans
    gamma_nonempty_iff_criticalStripRH

end SixBirdsDualityConfinement.RH.BareSourceConverse
