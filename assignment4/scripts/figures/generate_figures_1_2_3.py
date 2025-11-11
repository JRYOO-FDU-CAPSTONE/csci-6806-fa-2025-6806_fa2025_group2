#!/usr/bin/env python3

import json
import lzma
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
    'lines.linewidth': 1.5,
    'axes.linewidth': 0.8,
    'grid.alpha': 0.3,
    'figure.autolayout': True,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1
})

def extract_metrics_from_results():
    results = {}
    
    experiments = {
        'e0_lru': 'E0-LRU',
        'e1_dtslru': 'E1-DT-SLRU', 
        'e2_ede': 'E2-EDE'
    }
    
    base_path = Path('runs/a4')
    
    for exp_dir, label in experiments.items():
        exp_path = base_path / exp_dir
        
        result_dirs = [d for d in exp_path.iterdir() if d.is_dir() and d.name.startswith('acceptall-1_')]
        if not result_dirs:
            print(f"Warning: No results found for {exp_dir}")
            continue
            
        result_dir = result_dirs[0]
        stats_file = result_dir / 'full_0_0.1_cache_perf.txt.lzma'
        
        if not stats_file.exists():
            print(f"Warning: Stats file not found for {exp_dir}")
            continue
            
        try:
            with lzma.open(stats_file, 'rt') as f:
                data = json.load(f)
                stats = data['stats']
                
                peak_dt = stats.get('service_time_used3', 0) / 1000.0
                median_dt = stats.get('service_time_used2', 0) / 1000.0
                chunk_hits = float(stats.get('chunk_hits', 0))
                chunk_queries = float(stats.get('chunk_queries', 0))
                hit_rate = (chunk_hits / chunk_queries * 100) if chunk_queries > 0 else 0
                
                results[label] = {
                    'peak_dt': peak_dt,
                    'median_dt': median_dt,
                    'hit_rate': hit_rate,
                    'chunk_hits': chunk_hits,
                    'chunk_queries': chunk_queries
                }
                
                print(f"{label} Results:")
                print(f"  Peak DT: {peak_dt:.3f}s")
                print(f"  Median DT: {median_dt:.3f}s")
                print(f"  Hit Rate: {hit_rate:.1f}%")
                print()
                
        except Exception as e:
            print(f"Error processing {exp_dir}: {e}")
            continue
    
    return results

def generate_figure_1_peak_dt(results):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    schemes = list(results.keys())
    peak_dt_values = [results[scheme]['peak_dt'] for scheme in schemes]
    
    bars = ax.bar(schemes, peak_dt_values, 
                  color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                  alpha=0.8, edgecolor='black', linewidth=0.8)
    
    for bar, value in zip(bars, peak_dt_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{value:.3f}s', ha='center', va='bottom', fontweight='bold', fontsize=16)
    
    ax.set_ylabel('Peak Disk-head Time (seconds)', fontweight='bold', fontsize=16)
    ax.set_xlabel('Eviction Scheme', fontweight='bold', fontsize=16)
    ax.set_title('Figure 1: Peak DT across eviction schemes (E0-E2)', 
                 fontweight='bold', pad=20, fontsize=16)
    
    y_max = max(peak_dt_values) * 1.15
    ax.set_ylim(0, y_max)
    
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_axisbelow(True)
    
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('figure_1_peak_dt.png', dpi=300, bbox_inches='tight')
    plt.savefig('figure_1_peak_dt.pdf', bbox_inches='tight')
    print("Figure 1 saved as figure_1_peak_dt.png and figure_1_peak_dt.pdf")

def generate_figure_2_median_dt(results):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    schemes = list(results.keys())
    median_dt_values = [results[scheme]['median_dt'] for scheme in schemes]

    bars = ax.bar(schemes, median_dt_values,
                  color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                  alpha=0.8, edgecolor='black', linewidth=0.8)

    for bar, value in zip(bars, median_dt_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{value:.3f}s', ha='center', va='bottom', fontweight='bold', fontsize=16)

    ax.set_ylabel('Median Disk-head Time (seconds)', fontweight='bold', fontsize=16)
    ax.set_xlabel('Eviction Scheme', fontweight='bold', fontsize=16)
    ax.set_title('Figure 2: Median DT across eviction schemes (E0-E2)',
                 fontweight='bold', pad=20, fontsize=16)

    y_max = max(median_dt_values) * 1.15
    ax.set_ylim(0, y_max)

    ax.grid(True, alpha=0.3, axis='y')
    ax.set_axisbelow(True)

    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('figure_2_median_dt.png', dpi=300, bbox_inches='tight')
    plt.savefig('figure_2_median_dt.pdf', bbox_inches='tight')
    print("Figure 2 saved as figure_2_median_dt.png and figure_2_median_dt.pdf")

def generate_figure_3_hit_rate(results):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    schemes = list(results.keys())
    hit_rate_values = [results[scheme]['hit_rate'] for scheme in schemes]

    bars = ax.bar(schemes, hit_rate_values,
                  color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                  alpha=0.8, edgecolor='black', linewidth=0.8)

    for bar, value in zip(bars, hit_rate_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=16)

    ax.set_ylabel('Cache Hit Rate (%)', fontweight='bold', fontsize=16)
    ax.set_xlabel('Eviction Scheme', fontweight='bold', fontsize=16)
    ax.set_title('Figure 3: Cache Hit Rate (%) across eviction schemes (E0-E2)',
                 fontweight='bold', pad=20, fontsize=16)

    y_max = max(hit_rate_values) * 1.15
    ax.set_ylim(0, y_max)

    ax.grid(True, alpha=0.3, axis='y')
    ax.set_axisbelow(True)

    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('figure_3_hit_rate.png', dpi=300, bbox_inches='tight')
    plt.savefig('figure_3_hit_rate.pdf', bbox_inches='tight')
    print("Figure 3 saved as figure_3_hit_rate.png and figure_3_hit_rate.pdf")

def generate_combined_figure(results):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    schemes = list(results.keys())
    
    peak_dt_values = [results[scheme]['peak_dt'] for scheme in schemes]
    bars1 = axes[0].bar(schemes, peak_dt_values,
                       color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                       alpha=0.8, edgecolor='black', linewidth=0.8)
    
    for bar, value in zip(bars1, peak_dt_values):
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{value:.3f}s', ha='center', va='bottom', fontweight='bold')
    
    axes[0].set_ylabel('Peak Disk-head Time (seconds)', fontweight='bold')
    axes[0].set_title('(a) Peak DT', fontweight='bold', fontsize=16)
    axes[0].set_ylim(0, max(peak_dt_values) * 1.15)
    axes[0].grid(True, alpha=0.3, axis='y')
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['right'].set_visible(False)
    
    median_dt_values = [results[scheme]['median_dt'] for scheme in schemes]
    bars2 = axes[1].bar(schemes, median_dt_values,
                       color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                       alpha=0.8, edgecolor='black', linewidth=0.8)
    
    for bar, value in zip(bars2, median_dt_values):
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.005,
                    f'{value:.3f}s', ha='center', va='bottom', fontweight='bold')
    
    axes[1].set_ylabel('Median Disk-head Time (seconds)', fontweight='bold')
    axes[1].set_title('(b) Median DT', fontweight='bold', fontsize=16)
    axes[1].set_ylim(0, max(median_dt_values) * 1.15)
    axes[1].grid(True, alpha=0.3, axis='y')
    axes[1].spines['top'].set_visible(False)
    axes[1].spines['right'].set_visible(False)
    
    hit_rate_values = [results[scheme]['hit_rate'] for scheme in schemes]
    bars3 = axes[2].bar(schemes, hit_rate_values,
                       color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                       alpha=0.8, edgecolor='black', linewidth=0.8)
    
    for bar, value in zip(bars3, hit_rate_values):
        height = bar.get_height()
        axes[2].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    axes[2].set_ylabel('Cache Hit Rate (%)', fontweight='bold')
    axes[2].set_title('(c) Hit Rate', fontweight='bold', fontsize=16)
    axes[2].set_ylim(0, max(hit_rate_values) * 1.15)
    axes[2].grid(True, alpha=0.3, axis='y')
    axes[2].spines['top'].set_visible(False)
    axes[2].spines['right'].set_visible(False)
    
    plt.suptitle('Assignment 4: Eviction Policy Comparison (E0-E2)', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('assignment_4_figures_1_2_3_combined.png', dpi=300, bbox_inches='tight')
    plt.savefig('assignment_4_figures_1_2_3_combined.pdf', bbox_inches='tight')
    print("Combined figure saved as assignment_4_figures_1_2_3_combined.png and .pdf")

def generate_analysis_report(results):
    print("\n" + "="*80)
    print("ASSIGNMENT 4 FIGURE ANALYSIS")
    print("="*80)
    
    schemes = list(results.keys())
    
    print("\nFIGURE 1 ANALYSIS - Peak Disk-head Time:")
    print("-" * 50)
    peak_values = [results[scheme]['peak_dt'] for scheme in schemes]
    for scheme, value in zip(schemes, peak_values):
        print(f"  {scheme}: {value:.3f}s")
    
    print(f"\n**Analysis:** Peak DT shows {schemes[0]} achieving the lowest peak disk-head time "
          f"({peak_values[0]:.3f}s), followed by {schemes[1]} ({peak_values[1]:.3f}s) and "
          f"{schemes[2]} ({peak_values[2]:.3f}s). This indicates that the baseline LRU policy "
          f"provides the best worst-case performance, while the advanced DT-SLRU and EDE policies "
          f"show higher peak latencies, suggesting they may prioritize different optimization objectives.")
    
    print("\nFIGURE 2 ANALYSIS - Median Disk-head Time:")
    print("-" * 50)
    median_values = [results[scheme]['median_dt'] for scheme in schemes]
    for scheme, value in zip(schemes, median_values):
        print(f"  {scheme}: {value:.3f}s")
    
    print(f"\n**Analysis:** Median DT follows a similar pattern to peak DT, with {schemes[0]} "
          f"achieving the lowest median latency ({median_values[0]:.3f}s). The close values between "
          f"peak and median DT for {schemes[1]} and {schemes[2]} suggest these policies may have "
          f"more consistent performance characteristics, though at higher absolute latency levels.")
    
    print("\nFIGURE 3 ANALYSIS - Cache Hit Rate:")
    print("-" * 50)
    hit_rate_values = [results[scheme]['hit_rate'] for scheme in schemes]
    for scheme, value in zip(schemes, hit_rate_values):
        print(f"  {scheme}: {value:.1f}%")
    
    print(f"\n**Analysis:** Cache hit rates show {schemes[0]} achieving the highest hit rate "
          f"({hit_rate_values[0]:.1f}%), significantly outperforming {schemes[1]} ({hit_rate_values[1]:.1f}%) "
          f"and {schemes[2]} ({hit_rate_values[2]:.1f}%). This suggests that the baseline LRU policy "
          f"is most effective at retaining frequently accessed items, while the advanced policies may "
          f"be more selective in their retention decisions, potentially trading hit rate for other "
          f"optimization goals such as reducing specific types of latency.")
    
    print("\n" + "="*80)

def main():
    print("Assignment 4 Figure Generation")
    print("="*50)
    
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("Extracting metrics from simulation results...")
    results = extract_metrics_from_results()
    
    if not results:
        print("Error: No results found. Please ensure simulations have been run.")
        return
    
    print(f"Successfully extracted metrics for {len(results)} experiments")
    
    print("\nGenerating individual figures...")
    generate_figure_1_peak_dt(results)
    generate_figure_2_median_dt(results)
    generate_figure_3_hit_rate(results)
    
    print("\nGenerating combined figure...")
    generate_combined_figure(results)
    
    generate_analysis_report(results)
    
    print("\n" + "="*50)
    print("FIGURE GENERATION COMPLETE")
    print("="*50)
    print("Generated files:")
    print("  - figure_1_peak_dt.png/.pdf")
    print("  - figure_2_median_dt.png/.pdf") 
    print("  - figure_3_hit_rate.png/.pdf")
    print("  - assignment_4_figures_1_2_3_combined.png/.pdf")

if __name__ == "__main__":
    main()