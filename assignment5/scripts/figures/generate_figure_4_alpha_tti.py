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

def get_global_peak_dt_range():
    """Calculate global y-axis range for Peak DT across all ablation studies"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    
    all_peak_dt = []
    
    # Load Figure 1 results
    fig1_file = project_root / 'assignment5' / 'results' / 'fig_1_tau_dt_results.json'
    if fig1_file.exists():
        with open(fig1_file, 'r') as f:
            data = json.load(f)
            all_peak_dt.extend([v['peak_dt'] for v in data.values()])
    
    # Load Figure 3 results
    fig3_file = project_root / 'assignment5' / 'results' / 'fig_3_protected_cap_results.json'
    if fig3_file.exists():
        with open(fig3_file, 'r') as f:
            data = json.load(f)
            all_peak_dt.extend([v['peak_dt'] for v in data.values()])
    
    # Load Figure 4 results
    fig4_file = project_root / 'assignment5' / 'results' / 'fig_4_alpha_tti_results.json'
    if fig4_file.exists():
        with open(fig4_file, 'r') as f:
            data = json.load(f)
            all_peak_dt.extend([v['peak_dt'] for v in data.values()])
    
    if not all_peak_dt:
        return None, None
    
    global_min = min(all_peak_dt)
    global_max = max(all_peak_dt)
    
    # Add 3% margin for better readability
    y_min = global_min * 0.97
    y_max = global_max * 1.03
    
    return y_min, y_max

def extract_alpha_tti_metrics():
    results = {}
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    results_file = project_root / 'assignment5' / 'results' / 'fig_4_alpha_tti_results.json'
    
    if not results_file.exists():
        print(f"Error: Results file not found: {results_file}")
        print("Please ensure simulation results are available.")
        return results
    
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        for alpha_str, metrics in data.items():
            alpha = float(alpha_str)
            results[alpha] = {
                'peak_dt': metrics['peak_dt'],
                'peak_dt_std': metrics.get('peak_dt_std', 0.0),
                'median_dt': metrics['median_dt'],
                'hit_rate': metrics['hit_rate']
            }
            
            print(f"alpha_tti = {alpha:.2f}: Peak DT = {results[alpha]['peak_dt']:.3f}s, "
                  f"Hit Rate = {results[alpha]['hit_rate']:.1f}%")
    
    except Exception as e:
        print(f"Error reading results file: {e}")
        return results
    
    return results

def generate_figure_4_peak_dt(results):
    alpha_values = sorted(results.keys())
    peak_dt_values = [results[alpha]['peak_dt'] for alpha in alpha_values]
    peak_dt_stds = [results[alpha]['peak_dt_std'] for alpha in alpha_values]
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Use a different color from figures 1, 2, and 3
    color = '#d62728'  # Red color
    ax.plot(alpha_values, peak_dt_values, 
             color=color, marker='v', linewidth=2.5, markersize=8,
             markerfacecolor='white', markeredgewidth=2, markeredgecolor=color,
             label='Peak DT (E2 EDE)')
    
    seen_values = set()
    annotation_offset = 10  # Match Assignment 4 offset
    
    for i, (alpha, dt) in enumerate(zip(alpha_values, peak_dt_values)):
        dt_rounded = round(dt, 2)
        if dt_rounded not in seen_values:
            seen_values.add(dt_rounded)
            offset_y = annotation_offset
            
            # Check for nearby points to avoid overlaps
            if i > 0 and abs(peak_dt_values[i-1] - dt) < 0.05:
                offset_y = -annotation_offset - 5
            elif i < len(alpha_values) - 1 and abs(peak_dt_values[i+1] - dt) < 0.05:
                offset_y = -annotation_offset - 5
            
            ax.annotate(f'{dt:.2f}s', (alpha, dt), 
                        xytext=(0, offset_y), textcoords='offset points',
                        fontsize=16, ha='center', fontweight='bold')
    
    ax.set_xlabel('α_TTI Adaptation Rate', fontweight='bold', fontsize=16)
    ax.set_ylabel('Peak Disk-head Time (seconds)', fontweight='bold', fontsize=16, labelpad=10)
    
    ax.set_xlim(min(alpha_values) - 0.05, max(alpha_values) + 0.05)
    # Use global y-axis range for consistency across figures 1, 3, and 4
    y_min_global, y_max_global = get_global_peak_dt_range()
    if y_min_global is None or y_max_global is None:
        # Fallback to local range if global calculation fails
        y_min, y_max = min(peak_dt_values), max(peak_dt_values)
        y_min_global = y_min * 0.98
        y_max_global = y_max * 1.02
    ax.set_ylim(y_min_global, y_max_global)
    
    # Set title after y-axis limits to prevent overlap
    ax.set_title('Figure 4: Peak DT vs. α_TTI (E2 EDE)', fontweight='bold', pad=20, fontsize=16)
    
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    
    # Highlight the optimal point (minimum Peak DT)
    min_dt_idx = peak_dt_values.index(min(peak_dt_values))
    optimal_alpha = alpha_values[min_dt_idx]
    ax.axvline(x=optimal_alpha, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
    # Position annotation within plot bounds, near top but below title
    ax.text(optimal_alpha, y_max_global, f'Optimal (α_TTI = {optimal_alpha:.1f})', 
            ha='center', va='bottom', fontsize=16, color='red', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Adjust layout to prevent label overlaps - leave more room at top
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.subplots_adjust(top=0.92)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    output_dir = project_root / 'assignment5' / 'report' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'figure_4_peak_dt_alpha_tti.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure_4_peak_dt_alpha_tti.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Figure 4 saved to {output_dir}/figure_4_peak_dt_alpha_tti.png/.pdf")

def main():
    print("Assignment 5 Figure 4 Generation")
    print("="*50)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    os.chdir(project_root)
    
    print("Extracting alpha_tti ablation study metrics...")
    results = extract_alpha_tti_metrics()
    
    if not results:
        print("Error: No results found. Please ensure simulations have been run.")
        return
    
    print(f"Successfully extracted metrics for {len(results)} alpha_tti values")
    
    print("\nGenerating Figure 4...")
    generate_figure_4_peak_dt(results)
    
    print("\n" + "="*50)
    print("FIGURE 4 GENERATION COMPLETE")
    print("="*50)
    print("Generated files:")
    print("  - assignment5/report/figures/figure_4_peak_dt_alpha_tti.png/.pdf")

if __name__ == "__main__":
    main()

