#!/usr/bin/env python3

import json
import os
import matplotlib.pyplot as plt
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

def extract_tau_dt_metrics():
    results = {}
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    results_file = project_root / 'assignment5' / 'results' / 'fig_1_tau_dt_results.json'
    
    if not results_file.exists():
        print(f"Error: Results file not found: {results_file}")
        print("Please ensure simulation results are available.")
        return results
    
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        for tau_str, metrics in data.items():
            tau = float(tau_str)
            results[tau] = {
                'peak_dt': metrics['peak_dt'],
                'median_dt': metrics['median_dt'],
                'hit_rate': metrics['hit_rate']
            }
            
            print(f"tau_DT = {tau:.2f}: Peak DT = {results[tau]['peak_dt']:.3f}s, "
                  f"Hit Rate = {results[tau]['hit_rate']:.1f}%")
    
    except Exception as e:
        print(f"Error reading results file: {e}")
        return results
    
    return results

def generate_figure_2_hit_rate(results):
    tau_values = sorted(results.keys())
    hit_rate_values = [results[tau]['hit_rate'] for tau in tau_values]
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    ax.plot(tau_values, hit_rate_values, 
             color='#2ca02c', marker='s', linewidth=2.5, markersize=8,
             markerfacecolor='white', markeredgewidth=2, markeredgecolor='#2ca02c',
             label='Hit Rate (E1 DT-SLRU)')
    
    seen_values = set()
    annotation_offset = 10  # Match Assignment 4 offset
    
    for i, (tau, hr) in enumerate(zip(tau_values, hit_rate_values)):
        hr_rounded = round(hr, 1)
        if hr_rounded not in seen_values:
            seen_values.add(hr_rounded)
            offset_y = annotation_offset
            
            # Check for nearby points to avoid overlaps
            if i > 0 and abs(hit_rate_values[i-1] - hr) < 0.5:
                offset_y = -annotation_offset - 5
            elif i < len(tau_values) - 1 and abs(hit_rate_values[i+1] - hr) < 0.5:
                offset_y = -annotation_offset - 5
            
            ax.annotate(f'{hr:.1f}%', (tau, hr), 
                        xytext=(0, offset_y), textcoords='offset points',
                        fontsize=16, ha='center', fontweight='bold')
    
    ax.set_xlabel('τ_DT Promotion Threshold', fontweight='bold', fontsize=16)
    ax.set_ylabel('Cache Hit Rate (%)', fontweight='bold', fontsize=16, labelpad=10)
    
    ax.set_xlim(min(tau_values) - 0.05, max(tau_values) + 0.05)
    y_min, y_max = min(hit_rate_values), max(hit_rate_values)
    ax.set_ylim(y_min * 0.95, y_max * 1.05)
    
    # Set title after y-axis limits to prevent overlap
    ax.set_title('Figure 2: Hit Rate vs. τ_DT (E1 DT-SLRU)', fontweight='bold', pad=20, fontsize=16)
    
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    
    # Set x-axis ticks to exactly match tau_DT values
    ax.set_xticks(tau_values)
    ax.set_xticklabels([f'{tau:.2f}' for tau in tau_values], rotation=45, ha='right')
    
    baseline_tau = 1.0
    if baseline_tau in tau_values:
        ax.axvline(x=baseline_tau, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
        # Position annotation within plot bounds, near top but below title
        ax.text(baseline_tau, y_max * 1.05, 'Baseline (τ_DT = 1.0)', 
                ha='center', va='bottom', fontsize=16, color='red', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Adjust layout to prevent label overlaps - leave more room at top
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.subplots_adjust(top=0.92)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    output_dir = project_root / 'assignment5' / 'report' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'figure_2_hitrate_tau_dt.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure_2_hitrate_tau_dt.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Figure 2 saved to {output_dir}/figure_2_hitrate_tau_dt.png/.pdf")

def main():
    print("Assignment 5 Figure 2 Generation")
    print("="*50)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    os.chdir(project_root)
    
    print("Extracting tau_DT ablation study metrics...")
    results = extract_tau_dt_metrics()
    
    if not results:
        print("Error: No results found. Please ensure simulations have been run.")
        return
    
    print(f"Successfully extracted metrics for {len(results)} tau_DT values")
    
    print("\nGenerating Figure 2...")
    generate_figure_2_hit_rate(results)
    
    print("\n" + "="*50)
    print("FIGURE 2 GENERATION COMPLETE")
    print("="*50)
    print("Generated files:")
    print("  - assignment5/report/figures/figure_2_hitrate_tau_dt.png/.pdf")

if __name__ == "__main__":
    main()

