from pathlib import Path
import pandas as pd
base = Path(__file__).parent
df = pd.read_csv(base/'omega_filtration_density_sweep_step143.csv')
best = pd.read_csv(base/'omega_filtration_best_ladder_step143.csv')
assert {'N','K','R','epsilon_density','delta','short_ok','visibility_floor','effective_strength'}.issubset(df.columns)
assert best['N'].is_monotonic_increasing
assert (df['visibility_floor'] >= 0).all()
assert (df['epsilon_density'] <= 1).all()
print("Step 143 checks passed.")
print("Best rows:", len(best))
