from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
OUT=Path('/mnt/data/anti_localization_step43_taxonomy')

def plot_section():
    df=pd.read_csv(OUT/'section_cross_recombination_step43.csv')
    plt.figure()
    plt.plot(df['rho'], df['union_lambda_max'], marker='o')
    plt.axhline(1, linestyle='--')
    plt.xlabel('cross-section correlation rho')
    plt.ylabel('largest eigenvalue of stacked currency')
    plt.title('Section diagonal budgets do not control cross recombinations')
    plt.savefig(OUT/'section_cross_recombination_step43.png', bbox_inches='tight')
    plt.close()

def plot_bundle():
    df=pd.read_csv(OUT/'bundle_uniform_failure_step43.csv')
    plt.figure()
    plt.plot(df['fiber'], df['common_ratio'], marker='o')
    plt.axhline(1, linestyle='--')
    plt.xlabel('fiber index')
    plt.ylabel('ratio to common budget')
    plt.title('Fiberwise budgets can fail a uniform membrane')
    plt.savefig(OUT/'bundle_uniform_failure_step43.png', bbox_inches='tight')
    plt.close()

def plot_protocol():
    df=pd.read_csv(OUT/'protocol_stack_countermodel_step43.csv')
    plt.figure()
    plt.plot(df['protocols'], df['stack_lambda_max'], marker='o')
    plt.axhline(1, linestyle='--')
    plt.xlabel('number of duplicated protocols')
    plt.ylabel('largest eigenvalue of protocol stack')
    plt.title('Protocol-local budgets do not control protocol stack')
    plt.savefig(OUT/'protocol_stack_countermodel_step43.png', bbox_inches='tight')
    plt.close()

plot_section(); plot_bundle(); plot_protocol()
print('plots written')
