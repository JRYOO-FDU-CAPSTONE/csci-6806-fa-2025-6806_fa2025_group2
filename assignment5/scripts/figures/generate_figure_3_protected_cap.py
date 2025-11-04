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

def extract_protected_cap_metrics():
    results = {}
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    results_file = project_root / 'assignment5' / 'results' / 'fig_3_protected_cap_results.json'
    
    if not results_file.exists():
        print(f"Error: Results file not found: {results_file}")
        print("Please ensure simulation results are available.")
        return results
    
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        for cap_str, metrics in data.items():
            cap = float(cap_str)
            results[cap] = {
                'peak_dt': metrics['peak_dt'],
                'peak_dt_std': metrics.get('peak_dt_std', 0.0),
                'median_dt': metrics['median_dt'],
                'hit_rate': metrics['hit_rate']
            }
            
            print(f"PROTECTED cap = {cap:.2f}: Peak DT = {results[cap]['peak_dt']:.3f}s, "
                  f"Hit Rate = {results[cap]['hit_rate']:.1f}%")
    
    except Exception as e:
        print(f"Error reading results file: {e}")
        return results
    
    return results

def generate_figure_3_peak_dt(results):
    cap_values = sorted(results.keys())
    peak_dt_values = [results[cap]['peak_dt'] for cap in cap_values]
    peak_dt_stds = [results[cap]['peak_dt_std'] for cap in cap_values]
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Use a different color from figures 1 and 2
    color = '#1f77b4'  # Blue color
    ax.plot(cap_values, peak_dt_values, 
             color=color, marker='^', linewidth=2.5, markersize=8,
             markerfacecolor='white', markeredgewidth=2, markeredgecolor=color,
             label='Peak DT (E2 EDE)')
    
    seen_values = set()
    annotation_offset = 10  # Match Assignment 4 offset
    
    for i, (cap, dt) in enumerate(zip(cap_values, peak_dt_values)):
        dt_rounded = round(dt, 2)
        if dt_rounded not in seen_values:
            seen_values.add(dt_rounded)
            offset_y = annotation_offset
            
            # Check for nearby points to avoid overlaps
            if i > 0 and abs(peak_dt_values[i-1] - dt) < 0.05:
                offset_y = -annotation_offset - 5
            elif i < len(cap_values) - 1 and abs(peak_dt_values[i+1] - dt) < 0.05:
                offset_y = -annotation_offset - 5
            
            ax.annotate(f'{dt:.2f}s', (cap, dt), 
                        xytext=(0, offset_y), textcoords='offset points',
                        fontsize=16, ha='center', fontweight='bold')
    
    ax.set_xlabel('PROTECTED Cap', fontweight='bold', fontsize=16)
    ax.set_ylabel('Peak Disk-head Time (seconds)', fontweight='bold', fontsize=16, labelpad=10)
    
    ax.set_xlim(min(cap_values) - 0.05, max(cap_values) + 0.05)
    # Use global y-axis range for consistency across figures 1, 3, and 4
    y_min_global, y_max_global = get_global_peak_dt_range()
    if y_min_global is None or y_max_global is None:
        # Fallback to local range if global calculation fails
        y_min, y_max = min(peak_dt_values), max(peak_dt_values)
        y_min_global = y_min * 0.98
        y_max_global = y_max * 1.02
    ax.set_ylim(y_min_global, y_max_global)
    
    # Set title after y-axis limits to prevent overlap
    ax.set_title('Figure 3: Peak DT vs. PROTECTED cap (E2 EDE)', fontweight='bold', pad=20, fontsize=16)
    
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    
    # Highlight the optimal point (minimum Peak DT)
    min_dt_idx = peak_dt_values.index(min(peak_dt_values))
    optimal_cap = cap_values[min_dt_idx]
    ax.axvline(x=optimal_cap, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
    # Position annotation within plot bounds, near top but below title
    ax.text(optimal_cap, y_max_global, f'Optimal (cap = {optimal_cap:.1f})', 
            ha='center', va='bottom', fontsize=16, color='red', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Adjust layout to prevent label overlaps - leave more room at top
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.subplots_adjust(top=0.92)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    output_dir = project_root / 'assignment5' / 'report' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'figure_3_peak_dt_protected_cap.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure_3_peak_dt_protected_cap.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Figure 3 saved to {output_dir}/figure_3_peak_dt_protected_cap.png/.pdf")

def main():
    print("Assignment 5 Figure 3 Generation")
    print("="*50)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    os.chdir(project_root)
    
    print("Extracting PROTECTED cap ablation study metrics...")
    results = extract_protected_cap_metrics()
    
    if not results:
        print("Error: No results found. Please ensure simulations have been run.")
        return
    
    print(f"Successfully extracted metrics for {len(results)} PROTECTED cap values")
    
    print("\nGenerating Figure 3...")
    generate_figure_3_peak_dt(results)
    
    print("\n" + "="*50)
    print("FIGURE 3 GENERATION COMPLETE")
    print("="*50)
    print("Generated files:")
    print("  - assignment5/report/figures/figure_3_peak_dt_protected_cap.png/.pdf")

if __name__ == "__main__":
    main()

