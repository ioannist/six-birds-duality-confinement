from pathlib import Path
import json, csv, re
base = Path(__file__).resolve().parent
tex = base / 'rh_hecke_idele_carrier_sketch_step92.tex'
text = tex.read_text()
# crude environment balance check
begins = re.findall(r'\\begin\{([^}]+)\}', text)
ends = re.findall(r'\\end\{([^}]+)\}', text)
counts = {}
for b in begins: counts[b] = counts.get(b,0)+1
for e in ends: counts[e] = counts.get(e,0)-1
ok = all(v==0 for v in counts.values())
with open(base/'latex_structure_check_step92.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['check','result','details'])
    w.writerow(['environment_balance',ok,json.dumps(counts,sort_keys=True)])
print('environment balance', ok)
