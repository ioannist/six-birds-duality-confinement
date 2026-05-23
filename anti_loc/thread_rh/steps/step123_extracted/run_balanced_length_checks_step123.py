
from pathlib import Path
import re, csv, json
root = Path(__file__).resolve().parent
tex = (root/'muntz_shadow_balanced_length_step123.tex').read_text()
checks = []
checks.append(('has_balanced_length_theorem', 'Balanced-length theorem' in tex))
checks.append(('has_failure_theorem', 'Length incompatibility obstruction' in tex))
checks.append(('has_theta_min', '\\theta_{\\min,N}' in tex))
checks.append(('has_gamma_c_condition', '\\gamma_Nc_{{\\rm hyb},N}\\to\\infty' in tex))
# simple brace balance ignoring escaped braces is overkill; count raw braces
checks.append(('brace_balance', tex.count('{') == tex.count('}')))
checks.append(('begin_end_document', tex.count('\\begin{document}') == tex.count('\\end{document}') == 1))
with open(root/'latex_structure_check_step123.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['check','passed']); w.writerows(checks)
print(checks)
