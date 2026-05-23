import SixBirdsDualityConfinement.DualityConfinement.DirectConfinement

/-!
Duality Confinement paper — module ExhaustiveSqueeze.

Stub. Populated by codex during Phase G per the queue at
`formalization/traceability/queue_duality_confinement.csv`.
-/

namespace SixBirdsDualityConfinement.DualityConfinement.ExhaustiveSqueeze

universe u v w z q r

/--
An exhaustive moving ledger for a completed anti-invariant ledger.

The fields `A_X_n`, `iota_n`, and `T_n` encode the finite-window
ledger, transport, and positive tail.  The fields ending in `_bound`
encode the bounded regime `A_X_n ⪯ B_n`; `vanishing_exhaustive`
represents `tr(iota_n B_n iota_n*) + tr T_n -> 0`.
-/
structure ExhaustiveMovingLedger
    {ledger :
      Involution.InvolutiveObjectLedger.{u, v, w}}
    (A :
      AntiInvariantLedger.AntiInvariantLedger.{u, v, w, z, q}
        ledger) where
  add : A.Cone → A.Cone → A.Cone
  A_X_n : Nat → A.Cone
  B_n : Nat → A.Cone
  iota_n : Nat → A.Cone → A.Cone
  T_n : Nat → A.Cone
  T_n_positive : ∀ n : Nat, A.Positive (T_n n)
  B_n_positive : ∀ n : Nat, A.Positive (B_n n)
  moving_bound : ∀ n : Nat, A.preceq (A_X_n n) (B_n n)
  transported_A_X_n : Nat → A.Cone
  transported_B_n : Nat → A.Cone
  transported_A_X_n_def :
    ∀ n : Nat, transported_A_X_n n = iota_n n (A_X_n n)
  transported_B_n_def :
    ∀ n : Nat, transported_B_n n = iota_n n (B_n n)
  upper_moving : Nat → A.Cone
  upper_bound : Nat → A.Cone
  upper_moving_def :
    ∀ n : Nat, upper_moving n = add (transported_A_X_n n) (T_n n)
  upper_bound_def :
    ∀ n : Nat, upper_bound n = add (transported_B_n n) (T_n n)
  exhaustive : ∀ n : Nat, A.preceq A.A_X (upper_moving n)
  exhaustive_bound : ∀ n : Nat, A.preceq A.A_X (upper_bound n)
  vanishing_exhaustive : Prop

/--
Exhaustive ledger squeeze.

Vanishing exhaustivity squeezes the trace of `A_X` to zero; positivity
then gives `A_X = 0`.  With readout separation, the direct confinement
theorem gives confinement of visible mass to the fixed locus.
-/
theorem exhaustiveSqueeze
    {ledger :
      Involution.InvolutiveObjectLedger.{u, v, w}}
    (sep : Separation.SeparatingReadout.{u, v, w, r} ledger)
    (A :
      AntiInvariantLedger.AntiInvariantLedger.{u, v, w, z, q}
        ledger)
    (M : ExhaustiveMovingLedger A)
    (same_readout :
      ∀ x : ledger.X, A.psi_minus x = sep.psi_minus x)
    (mu_nonfixed_zero : Prop)
    (mu_zero_of_ae : A.psi_minus_ae_zero → mu_nonfixed_zero)
    (visible_zero_of_ae :
      A.psi_minus_ae_zero →
        ∀ x : ledger.X, x ∈ ledger.mu_support →
          A.psi_minus x = sep.zero_Y)
    (hvanishing : M.vanishing_exhaustive)
    (TraceNonnegative : A.TraceValue → Prop)
    (positive_trace_nonnegative :
      ∀ C : A.Cone, A.Positive C → TraceNonnegative (A.tr C))
    (TraceZero : A.TraceValue)
    (squeeze_trace_zero :
      TraceNonnegative (A.tr A.A_X) →
        (∀ n : Nat, A.TraceLE (A.tr A.A_X) (A.tr (M.upper_bound n))) →
          M.vanishing_exhaustive →
            A.tr A.A_X = TraceZero)
    (trace_zero_positive_zero :
      A.tr A.A_X = TraceZero → A.A_X = A.zero) :
    A.A_X = A.zero ∧ mu_nonfixed_zero := by
  have hTraceNonnegative : TraceNonnegative (A.tr A.A_X) :=
    positive_trace_nonnegative A.A_X A.positive_A_X
  have hTraceUpper :
      ∀ n : Nat, A.TraceLE (A.tr A.A_X) (A.tr (M.upper_bound n)) := by
    intro n
    exact A.trace_mono A.A_X (M.upper_bound n) (M.exhaustive_bound n)
  have hTraceZero : A.tr A.A_X = TraceZero :=
    squeeze_trace_zero hTraceNonnegative hTraceUpper hvanishing
  have hAZero : A.A_X = A.zero :=
    trace_zero_positive_zero hTraceZero
  exact
    And.intro hAZero
      (DirectConfinement.separationConfinement
        sep A same_readout mu_nonfixed_zero mu_zero_of_ae
        visible_zero_of_ae hAZero).left

end SixBirdsDualityConfinement.DualityConfinement.ExhaustiveSqueeze
