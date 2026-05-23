#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
out=Path(__file__).resolve().parent
df=pd.read_csv(out/'slow_omega_ladder_scenarios_step142.csv')
assert (df['epsilon_density']>=0).all()
assert (df['delta_blind']>=0).all()
assert (df['visibility_floor']>=0).all()
print('Step 142 checks passed', len(df))
