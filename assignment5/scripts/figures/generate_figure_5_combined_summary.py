#!/usr/bin/env python3

import json
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.style.use('default')
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 12,
    'lines.linewidth': 2.0,
    'lines.markersize': 8,
    'axes.linewidth': 0.8,
    'grid.alpha': 0.3,
    'figure.autolayout': True,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1
})

def load_all_results():
    """Load results from all ablation studies"""
    results = {}
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    
    # Load tau_DT results (Figure 1)
    fig1_file = project_root / 'assignment5' / 'results' / 'fig_1_tau_dt_results.json'
    if fig1_file.exists():
        with open(fig1_file, 'r') as f:
            data = json.load(f)
            results['tau_DT'] = {float(k): v['peak_dt'] for k, v in data.items()}
    
    # Load PROTECTED cap results (Figure 3)
    fig3_file = project_root / 'assignment5' / 'results' / 'fig_3_protected_cap_results.json'
    if fig3_file.exists():
        with open(fig3_file, 'r') as f:
            data = json.load(f)
            results['PROTECTED_cap'] = {float(k): v['peak_dt'] for k, v in data.items()}
    
    # Load alpha_TTI results (Figure 4)
    fig4_file = project_root / 'assignment5' / 'results' / 'fig_4_alpha_tti_results.json'
    if fig4_file.exists():
        with open(fig4_file, 'r') as f:
            data = json.load(f)
            results['alpha_TTI'] = {float(k): v['peak_dt'] for k, v in data.items()}
    
    return results

def normalize_to_baseline(results):
    """Normalize all Peak DT values to their respective baseline values and parameter values to 0-1 range"""
    normalized_dt = {}
    normalized_params = {}  # Normalize parameter values to 0-1 range
    
    # Define baseline values for each parameter
    baselines = {
        'tau_DT': 1.0,  # Baseline tau_DT
        'PROTECTED_cap': 0.5,  # Baseline PROTECTED cap
        'alpha_TTI': 0.1  # Baseline alpha_TTI
    }
    
    for param_name, param_results in results.items():
        baseline_value = baselines.get(param_name)
        if baseline_value in param_results:
            baseline_peak_dt = param_results[baseline_value]
            normalized_dt[param_name] = {
                val: peak_dt / baseline_peak_dt 
                for val, peak_dt in param_results.items()
            }
            
            # Normalize parameter values to 0-1 range
            param_values = list(param_results.keys())
            min_val = min(param_values)
            max_val = max(param_values)
            param_range = max_val - min_val
            
            if param_range > 0:
                normalized_params[param_name] = {
                    val: (val - min_val) / param_range
                    for val in param_values
                }
            else:
                normalized_params[param_name] = {
                    val: 0.5 for val in param_values  # All same value, set to middle
                }
            
            print(f"{param_name}: Baseline = {baseline_value}, Peak DT = {baseline_peak_dt:.3f}s")
    
    return normalized_dt, normalized_params

def generate_figure_5_combined(normalized_dt, normalized_params):
    """Generate combined sensitivity summary plot"""
    
    # Prepare data for plotting
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    colors = {
        'tau_DT': '#ff7f0e',      # Orange (matching Figure 1)
        'PROTECTED_cap': '#1f77b4',  # Blue (matching Figure 3)
        'alpha_TTI': '#d62728'    # Red (matching Figure 4)
    }
    
    markers = {
        'tau_DT': 'o',
        'PROTECTED_cap': '^',
        'alpha_TTI': 'v'
    }
    
    labels = {
        'tau_DT': 'τ_DT (E1 DT-SLRU)',
        'PROTECTED_cap': 'PROTECTED cap (E2 EDE)',
        'alpha_TTI': 'α_TTI (E2 EDE)'
    }
    
    # Plot each parameter using normalized parameter values
    for param_name in sorted(normalized_dt.keys()):
        param_results = normalized_dt[param_name]
        param_values = normalized_params[param_name]
        
        # Sort by normalized parameter value
        sorted_items = sorted(zip(param_values.keys(), param_values.values()))
        sorted_param_vals = [val for _, val in sorted_items]
        sorted_dt_vals = [param_results[key] for key, _ in sorted_items]
        
        ax.plot(sorted_param_vals, sorted_dt_vals,
                color=colors[param_name], 
                marker=markers[param_name],
                linewidth=2.5, 
                markersize=8,
                markerfacecolor='white', 
                markeredgewidth=2, 
                markeredgecolor=colors[param_name],
                label=labels[param_name],
                alpha=0.85)
    
    # Add reference line at normalized value = 1.0 (baseline)
    ax.axhline(y=1.0, color='black', linestyle='--', linewidth=2, alpha=0.5, label='Baseline')
    
    # Formatting
    ax.set_xlabel('Normalized Parameter Value (0 = min, 1 = max)', fontweight='bold', fontsize=18)
    ax.set_ylabel('Normalized Peak DT', fontweight='bold', fontsize=18, labelpad=10)
    
    # Set y-axis limits first
    all_normalized = []
    for param_results in normalized_dt.values():
        all_normalized.extend(param_results.values())
    
    y_min = min(0.85, min(all_normalized) - 0.05)
    y_max = max(1.2, max(all_normalized) + 0.05)
    ax.set_ylim(y_min, y_max)
    
    # Set title after limits to prevent overlap
    ax.set_title('Figure 5: Combined Sensitivity Summary: Normalized Peak DT for All Ablated Parameters',
                 fontweight='bold', pad=20, fontsize=18)
    
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.tick_params(axis='x', labelsize=18)  # Increased font size
    ax.tick_params(axis='y', labelsize=18)  # Increased font size
    
    # Legend - increased font size for better readability
    ax.legend(loc='best', frameon=True, fancybox=True, shadow=True, fontsize=16)
    
    # Adjust layout to prevent label overlaps
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.subplots_adjust(top=0.92)
    
    # Save figure
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    output_dir = project_root / 'assignment5' / 'report' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'figure_5_combined_sensitivity_summary.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure_5_combined_sensitivity_summary.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Figure 5 saved to {output_dir}/figure_5_combined_sensitivity_summary.png/.pdf")

def main():
    print("Assignment 5 Figure 5 Generation")
    print("="*50)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    os.chdir(project_root)
    
    print("Loading results from all ablation studies...")
    results = load_all_results()
    
    if not results:
        print("Error: No results found. Please ensure simulations have been run.")
        return
    
    print(f"Successfully loaded results for {len(results)} parameters")
    
    print("\nNormalizing to baseline values...")
    normalized_dt, normalized_params = normalize_to_baseline(results)
    
    print("\nGenerating Figure 5...")
    generate_figure_5_combined(normalized_dt, normalized_params)
    
    print("\n" + "="*50)
    print("FIGURE 5 GENERATION COMPLETE")
    print("="*50)
    print("Generated files:")
    print("  - assignment5/report/figures/figure_5_combined_sensitivity_summary.png/.pdf")

if __name__ == "__main__":
    main()

