#!/usr/bin/env python3

"""
Assignment 5 Figure 6 Generation Script
Generates Figure 6: Hit Rate Sensitivity for PROTECTED cap and α_TTI

This script creates a combined figure showing hit rate sensitivity to:
- PROTECTED cap (E2 EDE)
- α_TTI adaptation rate (E2 EDE)

This complements Figure 2 (hit rate vs τ_DT) to provide complete hit rate
sensitivity analysis across all three key parameters.
"""

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

def extract_protected_cap_metrics():
    """Extract hit rate metrics for PROTECTED cap ablation study"""
    results = {}
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    results_file = project_root / 'assignment5' / 'results' / 'fig_3_protected_cap_results.json'
    
    if not results_file.exists():
        print(f"Error: Results file not found: {results_file}")
        return results
    
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        for cap_str, metrics in data.items():
            cap = float(cap_str)
            results[cap] = {
                'hit_rate': metrics['hit_rate'],
                'hit_rate_std': metrics.get('hit_rate_std', 0.0)
            }
            
            print(f"PROTECTED cap = {cap:.2f}: Hit Rate = {results[cap]['hit_rate']:.1f}% "
                  f"(std: {results[cap]['hit_rate_std']:.2f}%)")
    
    except Exception as e:
        print(f"Error reading protected cap results file: {e}")
        return results
    
    return results

def extract_alpha_tti_metrics():
    """Extract hit rate metrics for α_TTI ablation study"""
    results = {}
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    results_file = project_root / 'assignment5' / 'results' / 'fig_4_alpha_tti_results.json'
    
    if not results_file.exists():
        print(f"Error: Results file not found: {results_file}")
        return results
    
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        for alpha_str, metrics in data.items():
            alpha = float(alpha_str)
            results[alpha] = {
                'hit_rate': metrics['hit_rate'],
                'hit_rate_std': metrics.get('hit_rate_std', 0.0)
            }
            
            print(f"α_TTI = {alpha:.2f}: Hit Rate = {results[alpha]['hit_rate']:.1f}% "
                  f"(std: {results[alpha]['hit_rate_std']:.2f}%)")
    
    except Exception as e:
        print(f"Error reading alpha_tti results file: {e}")
        return results
    
    return results

def generate_figure_6a_hitrate_protected_cap(protected_cap_results):
    """Generate Figure 6a: Hit Rate vs PROTECTED cap"""
    
    # Create single figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    cap_values = sorted(protected_cap_results.keys())
    hit_rate_values = [protected_cap_results[cap]['hit_rate'] for cap in cap_values]
    hit_rate_stds = [protected_cap_results[cap]['hit_rate_std'] for cap in cap_values]
    
    color = '#1f77b4'  # Blue
    ax.plot(cap_values, hit_rate_values, 
             color=color, marker='^', linewidth=2.5, markersize=8,
             markerfacecolor='white', markeredgewidth=2, markeredgecolor=color,
             label='Hit Rate (E2 EDE)')
    
    # Add error bars if standard deviations are available
    if any(std > 0 for std in hit_rate_stds):
        ax.errorbar(cap_values, hit_rate_values, yerr=hit_rate_stds,
                    fmt='none', ecolor=color, alpha=0.5, capsize=4, capthick=1.5)
    
    # Annotate key points
    seen_values = set()
    annotation_offset = 10
    
    for i, (cap, hr) in enumerate(zip(cap_values, hit_rate_values)):
        hr_rounded = round(hr, 1)
        if hr_rounded not in seen_values:
            seen_values.add(hr_rounded)
            offset_y = annotation_offset
            
            # Check for nearby points to avoid overlaps
            if i > 0 and abs(hit_rate_values[i-1] - hr) < 0.5:
                offset_y = -annotation_offset - 5
            elif i < len(cap_values) - 1 and abs(hit_rate_values[i+1] - hr) < 0.5:
                offset_y = -annotation_offset - 5
            
            ax.annotate(f'{hr:.1f}%', (cap, hr), 
                        xytext=(0, offset_y), textcoords='offset points',
                        fontsize=16, ha='center', fontweight='bold')
    
    ax.set_xlabel('PROTECTED Cap', fontweight='bold', fontsize=16)
    ax.set_ylabel('Cache Hit Rate (%)', fontweight='bold', fontsize=16, labelpad=10)
    ax.set_title('Hit Rate vs. PROTECTED Cap (E2 EDE)', fontweight='bold', pad=20, fontsize=16)
    
    ax.set_xlim(min(cap_values) - 0.05, max(cap_values) + 0.05)
    y_min, y_max = min(hit_rate_values), max(hit_rate_values)
    ax.set_ylim(y_min * 0.95, y_max * 1.05)
    
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    
    # Highlight optimal point (maximum hit rate)
    max_hr_idx = hit_rate_values.index(max(hit_rate_values))
    optimal_cap = cap_values[max_hr_idx]
    ax.axvline(x=optimal_cap, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
    ax.text(optimal_cap, y_max * 1.02, f'Optimal (cap = {optimal_cap:.1f})', 
            ha='center', va='bottom', fontsize=16, color='red', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save figure
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    output_dir = project_root / 'assignment5' / 'report' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'figure_6a_hitrate_protected_cap.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure_6a_hitrate_protected_cap.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Figure 6a saved to {output_dir}/figure_6a_hitrate_protected_cap.png/.pdf")

def generate_figure_6b_hitrate_alpha_tti(alpha_tti_results):
    """Generate Figure 6b: Hit Rate vs α_TTI"""
    
    # Create single figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    alpha_values = sorted(alpha_tti_results.keys())
    hit_rate_values = [alpha_tti_results[alpha]['hit_rate'] for alpha in alpha_values]
    hit_rate_stds = [alpha_tti_results[alpha]['hit_rate_std'] for alpha in alpha_values]
    
    color = '#d62728'  # Red
    ax.plot(alpha_values, hit_rate_values, 
             color=color, marker='v', linewidth=2.5, markersize=8,
             markerfacecolor='white', markeredgewidth=2, markeredgecolor=color,
             label='Hit Rate (E2 EDE)')
    
    # Add error bars if standard deviations are available
    if any(std > 0 for std in hit_rate_stds):
        ax.errorbar(alpha_values, hit_rate_values, yerr=hit_rate_stds,
                    fmt='none', ecolor=color, alpha=0.5, capsize=4, capthick=1.5)
    
    # Annotate key points
    seen_values = set()
    annotation_offset = 10
    
    for i, (alpha, hr) in enumerate(zip(alpha_values, hit_rate_values)):
        hr_rounded = round(hr, 1)
        if hr_rounded not in seen_values:
            seen_values.add(hr_rounded)
            offset_y = annotation_offset
            
            # Check for nearby points to avoid overlaps
            if i > 0 and abs(hit_rate_values[i-1] - hr) < 0.5:
                offset_y = -annotation_offset - 5
            elif i < len(alpha_values) - 1 and abs(hit_rate_values[i+1] - hr) < 0.5:
                offset_y = -annotation_offset - 5
            
            ax.annotate(f'{hr:.1f}%', (alpha, hr), 
                        xytext=(0, offset_y), textcoords='offset points',
                        fontsize=16, ha='center', fontweight='bold')
    
    ax.set_xlabel('α_TTI Adaptation Rate', fontweight='bold', fontsize=16)
    ax.set_ylabel('Cache Hit Rate (%)', fontweight='bold', fontsize=16, labelpad=10)
    ax.set_title('Hit Rate vs. α_TTI (E2 EDE)', fontweight='bold', pad=20, fontsize=16)
    
    ax.set_xlim(min(alpha_values) - 0.05, max(alpha_values) + 0.05)
    y_min, y_max = min(hit_rate_values), max(hit_rate_values)
    ax.set_ylim(y_min * 0.95, y_max * 1.05)
    
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    
    # Highlight optimal point (maximum hit rate)
    max_hr_idx = hit_rate_values.index(max(hit_rate_values))
    optimal_alpha = alpha_values[max_hr_idx]
    ax.axvline(x=optimal_alpha, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
    ax.text(optimal_alpha, y_max * 1.02, f'Optimal (α_TTI = {optimal_alpha:.1f})', 
            ha='center', va='bottom', fontsize=16, color='red', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save figure
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    output_dir = project_root / 'assignment5' / 'report' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'figure_6b_hitrate_alpha_tti.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure_6b_hitrate_alpha_tti.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Figure 6b saved to {output_dir}/figure_6b_hitrate_alpha_tti.png/.pdf")

def generate_analysis_report(protected_cap_results, alpha_tti_results):
    """Generate analysis report for hit rate sensitivity"""
    
    print("\n" + "="*80)
    print("FIGURE 6 ANALYSIS - Hit Rate Sensitivity (E2 EDE)")
    print("="*80)
    
    # PROTECTED Cap Analysis
    cap_values = sorted(protected_cap_results.keys())
    hit_rates_cap = [protected_cap_results[cap]['hit_rate'] for cap in cap_values]
    
    print("\nPROTECTED Cap Hit Rate Sensitivity:")
    print("-" * 60)
    print(f"{'PROTECTED Cap':<15} {'Hit Rate (%)':<15} {'Std Dev (%)':<15}")
    print("-" * 60)
    for cap in cap_values:
        hr = protected_cap_results[cap]['hit_rate']
        std = protected_cap_results[cap]['hit_rate_std']
        print(f"{cap:<15.2f} {hr:<15.1f} {std:<15.2f}")
    
    max_hr_cap = max(cap_values, key=lambda c: protected_cap_results[c]['hit_rate'])
    print(f"\nOptimal PROTECTED Cap for Hit Rate: {max_hr_cap:.2f} "
          f"({protected_cap_results[max_hr_cap]['hit_rate']:.1f}%)")
    
    # α_TTI Analysis
    alpha_values = sorted(alpha_tti_results.keys())
    hit_rates_alpha = [alpha_tti_results[alpha]['hit_rate'] for alpha in alpha_values]
    
    print("\nα_TTI Hit Rate Sensitivity:")
    print("-" * 60)
    print(f"{'α_TTI':<15} {'Hit Rate (%)':<15} {'Std Dev (%)':<15}")
    print("-" * 60)
    for alpha in alpha_values:
        hr = alpha_tti_results[alpha]['hit_rate']
        std = alpha_tti_results[alpha]['hit_rate_std']
        print(f"{alpha:<15.2f} {hr:<15.1f} {std:<15.2f}")
    
    max_hr_alpha = max(alpha_values, key=lambda a: alpha_tti_results[a]['hit_rate'])
    print(f"\nOptimal α_TTI for Hit Rate: {max_hr_alpha:.2f} "
          f"({alpha_tti_results[max_hr_alpha]['hit_rate']:.1f}%)")
    
    # Comparative Analysis
    print("\n" + "="*80)
    print("KEY INSIGHTS:")
    print("="*80)
    print(f"1. PROTECTED Cap Impact: Hit rate varies from {min(hit_rates_cap):.1f}% to "
          f"{max(hit_rates_cap):.1f}% ({max(hit_rates_cap) - min(hit_rates_cap):.1f}% range)")
    print(f"2. α_TTI Impact: Hit rate varies from {min(hit_rates_alpha):.1f}% to "
          f"{max(hit_rates_alpha):.1f}% ({max(hit_rates_alpha) - min(hit_rates_alpha):.1f}% range)")
    print(f"3. Optimal Configuration: PROTECTED cap = {max_hr_cap:.2f}, "
          f"α_TTI = {max_hr_alpha:.2f}")
    
    print("\n" + "="*80)

def main():
    print("Assignment 5 Figure 6 Generation")
    print("="*50)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    os.chdir(project_root)
    
    print("\nExtracting PROTECTED cap hit rate metrics...")
    protected_cap_results = extract_protected_cap_metrics()
    
    print("\nExtracting α_TTI hit rate metrics...")
    alpha_tti_results = extract_alpha_tti_metrics()
    
    if not protected_cap_results or not alpha_tti_results:
        print("Error: Missing results data. Please ensure simulations have been run.")
        return
    
    print(f"\nSuccessfully extracted metrics:")
    print(f"  - {len(protected_cap_results)} PROTECTED cap values")
    print(f"  - {len(alpha_tti_results)} α_TTI values")
    
    print("\nGenerating Figure 6a (Hit Rate vs PROTECTED Cap)...")
    generate_figure_6a_hitrate_protected_cap(protected_cap_results)
    
    print("\nGenerating Figure 6b (Hit Rate vs α_TTI)...")
    generate_figure_6b_hitrate_alpha_tti(alpha_tti_results)
    
    generate_analysis_report(protected_cap_results, alpha_tti_results)
    
    print("\n" + "="*50)
    print("FIGURE 6 GENERATION COMPLETE")
    print("="*50)
    print("Generated files:")
    print("  - assignment5/report/figures/figure_6a_hitrate_protected_cap.png/.pdf")
    print("  - assignment5/report/figures/figure_6b_hitrate_alpha_tti.png/.pdf")
    print("\nFigures provide:")
    print("  * Figure 6a: Hit rate sensitivity to PROTECTED cap (E2 EDE)")
    print("  * Figure 6b: Hit rate sensitivity to α_TTI (E2 EDE)")
    print("  * Completes hit rate analysis across all three key parameters")
    print("  * ACM sigconf formatting with proper error bars")

if __name__ == "__main__":
    main()

