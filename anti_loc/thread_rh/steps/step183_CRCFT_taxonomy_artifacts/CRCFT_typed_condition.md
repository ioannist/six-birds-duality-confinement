# Classical-RH Carrier Foreclosure Taxonomy (CRCFT)

## Definition

A typed primary carrier `C` carrying a candidate residual `Xi_C` aimed at RH is
classically-RH-equivalent (CRE) when at least one of the following holds:

1. `C` belongs to a named classical RH approach, such as Hilbert-Polya,
   de Branges, Connes adelic or semilocal, Selberg trace, Burnol/Sonine, or
   Hecke carriers.
2. Closure of `Xi_C` is logically equivalent to RH.

CRCFT says that, under framework discipline, a tested CRE carrier terminates
in at least one typed foreclosure mode.

## Modes

`CRCFT-CTMT`: matrix-element terminus. The closure attempt reaches a
carrier-native matrix-element family. The obstruction is post-reduction.

`CRCFT-TE`: target-equivalence. The central positivity, spectral, or
structural condition is RH-equivalent. The obstruction is pre-reduction.

`CRCFT-BF`: bridge-failure. The carrier is non-comparable to the target ledger
or has wrong spectral/comparison type. The obstruction is at the
carrier-comparison level.

## Instances

| Carrier | Route | Mode | Obstruction | Step |
|---|---|---|---|---|
| Burnol/Sonine | Branch A Calkin G2-G5 | CRCFT-CTMT-stuck | `kappa` / Burnol projected-kernel theorem | 179 |
| Burnol/Sonine | Branch B SL164.1 | CRCFT-CTMT-stuck | same `kappa` vector | 177-178 |
| Burnol/Sonine | Branch C shifted co-Poisson | CRCFT-CTMT-foreclosed-numerical | nonzero `L_{rho,k}` across four data points | 175-176 |
| Hecke | H6 zeta-fiber descent | CRCFT-BF | V-NC ledger-relative non-comparability | 168 |
| de Branges `H(E_RH)` | `Xi_dB` closure | CRCFT-TE | de Branges RH program plus Conrey-Li survival | 181 |
| HP/BK standard `H_xp` | standard spectral ledger | CRCFT-BF | continuous `R` spectrum; interval spectra arithmetic | 182 |
| HP/BK modified | cutoff/boundary exact matching | CRCFT-TE | exact matching is non-inherited HP/RH assertion | 182 |

## Consequence Theorem

When a CRE carrier exhibits CRCFT in mode `m`:

- If `m = CTMT`, the framework output is the precise carrier-native
  matrix-element family and its resolution mode.
- If `m = TE`, the framework output is a target-equivalence no-go; direct
  pursuit is structurally circular.
- If `m = BF`, the framework output is a bridge-failure statement naming the
  comparison axis that fails.

In all three modes, the framework contribution is a typed external-content
interface, not a proof of RH.

## Coverage Conjecture

Every CRE carrier exhibits CRCFT in at least one of the three modes.

Status: conjecture. It is supported by 4 carriers and 7 instances in the
current iteration. It is refutable by exhibiting a CRE carrier with a
completed, non-target-equivalent, non-CRCFT closure.

## Relationship to CTMT

CTMT is the matrix-element-terminus typed condition. CRCFT is broader: it
contains CTMT as its post-reduction mode and adds target-equivalence and
bridge-failure for pre-reduction and carrier-comparison failures.

## Corpus Status

Flagged for future foundational-corpus inclusion. Integration was not
performed in Step 183.
