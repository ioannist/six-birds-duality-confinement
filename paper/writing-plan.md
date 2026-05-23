# Writing Plan — Duality Confinement + RH papers

Status: stub. Populate after mechanization (Phase G of
`PLAN_mechanization.md`) completes for each axis, before the first
drafting dispatch.

This file is the manager-side runbook for the drafting arc. It lists
per-section dispatches in document order with prerequisites,
prompt-construction hints, and review cadence.

## Protocol (inherited)

- One codex task per dispatch. No batching of subsections.
- Resume by UUID; per-paper drafting threads:
  - Paper 1 (duality confinement): `paper/duality_confinement/.codex_thread_id`
  - Paper 2 (RH): `paper/rh/.codex_thread_id`
- Codex writes files directly via `--full-auto`; manager reviews files.
- Build after every dispatch: `make paper-preflight-duality_confinement`
  / `make paper-preflight-rh`.

## Dispatch table — duality_confinement

TODO: row per section/subsection.

## Dispatch table — rh

TODO: row per section/subsection.
