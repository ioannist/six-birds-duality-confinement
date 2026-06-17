import SixBirdsDualityConfinement.DualityConfinement.DirectConfinement
import SixBirdsDualityConfinement.DualityConfinement.Domination

/-!
# Duality Confinement paper -- `MasterTheorem`

The duality-confinement membrane theorem: a typed positive-cone
squeeze converting a vanishing-trace domination sequence into
fixed-locus confinement.
-/

namespace SixBirdsDualityConfinement.DualityConfinement.MasterTheorem

universe u v w z q r

/--
Duality-confinement membrane theorem.

The sequence `B_n` represents completed domination records
`A_X ⪯ B_n` with `B_n ⪰ 0`.  The abstract proposition
`tr_B_n_tends_zero` represents `tr B_n -> 0`.  The three non-definitional
analytic steps from the paper are explicit hypotheses: positive trace
nonnegativity, the squeeze-to-zero principle, and trace-zero positivity
forcing `A_X = 0`.  The final step is the direct separation confinement
theorem.
-/
theorem masterTheorem
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
    (B_n : Nat → A.Cone)
    (domination_records :
      ∀ n : Nat, A.preceq A.A_X (B_n n))
    (B_n_positive : ∀ n : Nat, A.Positive (B_n n))
    (tr_B_n_tends_zero : Prop)
    (h_tr_B_n_tends_zero : tr_B_n_tends_zero)
    (TraceNonnegative : A.TraceValue → Prop)
    (positive_trace_nonnegative :
      ∀ C : A.Cone, A.Positive C → TraceNonnegative (A.tr C))
    (TraceZero : A.TraceValue)
    (squeeze_trace_zero :
      TraceNonnegative (A.tr A.A_X) →
        (∀ n : Nat, A.TraceLE (A.tr A.A_X) (A.tr (B_n n))) →
          (∀ n : Nat, A.Positive (B_n n)) →
            tr_B_n_tends_zero →
              A.tr A.A_X = TraceZero)
    (trace_zero_positive_zero :
      A.tr A.A_X = TraceZero → A.A_X = A.zero) :
    mu_nonfixed_zero := by
  have hTraceNonnegative : TraceNonnegative (A.tr A.A_X) :=
    positive_trace_nonnegative A.A_X A.positive_A_X
  have hTraceUpper :
      ∀ n : Nat, A.TraceLE (A.tr A.A_X) (A.tr (B_n n)) := by
    intro n
    exact A.trace_mono A.A_X (B_n n) (domination_records n)
  have hTraceZero : A.tr A.A_X = TraceZero :=
    squeeze_trace_zero hTraceNonnegative hTraceUpper
      B_n_positive h_tr_B_n_tends_zero
  have hAZero : A.A_X = A.zero :=
    trace_zero_positive_zero hTraceZero
  exact
    (DirectConfinement.separationConfinement
      sep A same_readout mu_nonfixed_zero mu_zero_of_ae
      visible_zero_of_ae hAZero).left

end SixBirdsDualityConfinement.DualityConfinement.MasterTheorem
