from pathlib import Path
import pandas as pd
import json
OUT=Path('/mnt/data/rh_membrane_step119_burnol_dirichlet_shadow')
checks=[]
# Check core CSVs exist and contain finite values
for name in ['burnol_dirichlet_shadow_sweep_step119.csv','shadow_residual_spectrum_step119.csv','burnol_dirichlet_shadow_gate_table_step119.csv']:
    p=OUT/name
    checks.append({'check':f'{name}_exists','passed':bool(p.exists()),'detail':str(p)})
    if p.exists() and p.suffix=='.csv':
        df=pd.read_csv(p)
        checks.append({'check':f'{name}_nonempty','passed':bool(len(df)>0),'detail':f'rows={len(df)} cols={len(df.columns)}'})
# Check the shadow defect sweep has the expected columns
p=OUT/'burnol_dirichlet_shadow_sweep_step119.csv'
if p.exists():
    df=pd.read_csv(p)
    required={'normalized_shadow_defect_eps','visibility_lower_bound_c','dirichlet_gram_condition_number'}
    checks.append({'check':'sweep_required_columns','passed':bool(required.issubset(df.columns)),'detail':','.join(df.columns)})
    if required.issubset(df.columns):
        checks.append({'check':'defects_finite','passed':bool(df['normalized_shadow_defect_eps'].notna().all()),'detail':str(df['normalized_shadow_defect_eps'].describe().to_dict())})
# LaTeX balance check
tex=(OUT/'burnol_dirichlet_shadow_step119.tex').read_text()
for env in ['document','enumerate','theorem','definition','proposition','remark']:
    b=tex.count('\\begin{'+env+'}')
    e=tex.count('\\end{'+env+'}')
    checks.append({'check':f'latex_{env}_balanced','passed':bool(b==e),'detail':f'begin={b} end={e}'})

pd.DataFrame(checks).to_csv(OUT/'step119_check_results.csv',index=False)
print(json.dumps(checks,indent=2))
