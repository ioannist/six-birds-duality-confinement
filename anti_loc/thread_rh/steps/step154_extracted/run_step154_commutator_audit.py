import numpy as np
import pandas as pd
from pathlib import Path
out=Path(__file__).parent
sv=pd.read_csv(out/'commutator_singular_values_step154.csv')
summary=pd.read_csv(out/'commutator_scenario_summary_step154.csv')
assert len(sv)>0
assert len(summary)>0
assert summary['top_singular_value'].max()>0.1
print({'status':'ok','max_top_singular':float(summary['top_singular_value'].max()),'rows':len(summary)})
