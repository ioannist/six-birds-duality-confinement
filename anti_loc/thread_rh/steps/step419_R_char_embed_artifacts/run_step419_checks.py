#!/usr/bin/env python3
from pathlib import Path
import csv, json, math, sys

ART = Path(__file__).resolve().parent
REQUIRED = [
    'R_char_embed_rule_step419.md',
    'training_calibration_step419.csv',
    'in_sample_verification_step419.csv',
    'OOS_verification_step419.csv',
    'C5_C6_C11_satisfaction_step419.md',
    'step419_results_summary.md',
    'mode_b_constraint_ledger_step419_snapshot.csv',
    'mode_b_target_lineage_step419_snapshot.csv',
    'mode_b_grammar_manifest_G_U_flat_reg_embed_step419.csv',
    'step419_schema.json',
    'nonclaim_boundary_step419.md',
    'run_step419_checks.py',
]

def fail(msg):
    print(f'step419 validation FAILED: {msg}')
    sys.exit(1)

for name in REQUIRED:
    p = ART / name
    if not p.exists():
        fail(f'missing {name}')
    if p.stat().st_size == 0:
        fail(f'empty {name}')

with (ART/'step419_schema.json').open() as f:
    schema = json.load(f)
if schema.get('step') != 419:
    fail('schema step is not 419')

with (ART/'training_calibration_step419.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
if len(rows) != 1:
    fail('training calibration should contain exactly one aggregate row')
row = rows[0]
train = float(row['train_log_RMSE'])
hold = float(row['holdout_log_RMSE'])
ratio = float(row['holdout_to_training_ratio'])
if not (train > 0 and hold > 0 and ratio > 0):
    fail('invalid RMSE metrics')

with (ART/'OOS_verification_step419.csv').open(newline='') as f:
    oos = list(csv.DictReader(f))
chars = {r['character'] for r in oos}
if not {'chi_13','chi_15','ALL_OOS'} <= chars:
    fail('OOS verification missing chi_13, chi_15, or ALL_OOS')

with (ART/'mode_b_grammar_manifest_G_U_flat_reg_embed_step419.csv').open(newline='') as f:
    manifest = list(csv.DictReader(f))
if len(manifest) != 1 or manifest[0].get('grammar_id') != 'G_U_flat_reg_embed':
    fail('grammar manifest malformed')
if 'R_char_embed' not in manifest[0].get('allowed_rewrite_or_update_rules',''):
    fail('manifest does not declare R_char_embed')

print('step419 validation passed')
