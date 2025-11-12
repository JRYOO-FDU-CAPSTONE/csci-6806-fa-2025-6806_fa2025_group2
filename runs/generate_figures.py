#!/usr/bin/env python3
"""
Generate all 7 required figures for A4 assignment.
Usage: python generate_figures.py
"""

import os
import json
import glob
import sys
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Create output directory
os.makedirs('figures', exist_ok=True)

def generate_figures_with_synthetic_data():
    """Generate all figures with synthetic/demo data"""
    
    print("Generating A4 Figures...")
    print("=" * 60)
    
    # Figure 1: Peak DT across schemes
    schemes = ['E0-LRU', 'E1-DTSLRU', 'E2-EDE']
    peak_dt = [45.2, 38.7, 35.4]
    colors = ['#e74c3c', '#3498db', '#2ecc71']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(schemes, peak_dt, color=colors, alpha=0.8, edgecolor='black')
    for bar, value in zip(bars, peak_dt):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
    plt.ylabel('Peak Disk-head Time (ms)', fontweight='bold')
    plt.xlabel('Eviction Scheme', fontweight='bold')
    plt.title('Figure 1: Peak DT across Eviction Schemes', fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/figure1_peak_dt.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 1: figures/figure1_peak_dt.png")
    
    # Figure 2: Median DT
    median_dt = [18.5, 16.2, 15.1]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(schemes, median_dt, color=colors, alpha=0.8, edgecolor='black')
    for bar, value in zip(bars, median_dt):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
    plt.ylabel('Median Disk-head Time (ms)', fontweight='bold')
    plt.xlabel('Eviction Scheme', fontweight='bold')
    plt.title('Figure 2: Median DT across Eviction Schemes', fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/figure2_median_dt.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 2: figures/figure2_median_dt.png")
    
    # Figure 3: Hit Rate
    hit_rate = [62.3, 68.5, 71.2]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(schemes, hit_rate, color=colors, alpha=0.8, edgecolor='black')
    for bar, value in zip(bars, hit_rate):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    plt.ylabel('Cache Hit Rate (%)', fontweight='bold')
    plt.xlabel('Eviction Scheme', fontweight='bold')
    plt.title('Figure 3: Hit Rate across Eviction Schemes', fontweight='bold')
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/figure3_hit_rate.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 3: figures/figure3_hit_rate.png")
    
    # Figure 4: Cache Size Sensitivity
    cache_sizes = [50, 75, 100, 125, 150]
    lru_peak = [58.3, 51.2, 45.2, 41.8, 38.5]
    best_peak = [48.7, 42.1, 35.4, 32.6, 29.8]
    
    plt.figure(figsize=(10, 6))
    plt.plot(cache_sizes, lru_peak, 'o-', linewidth=2.5, markersize=10,
            color='#e74c3c', label='E0-LRU', alpha=0.8)
    plt.plot(cache_sizes, best_peak, 's-', linewidth=2.5, markersize=10,
            color='#2ecc71', label='E2-EDE (Best)', alpha=0.8)
    plt.xlabel('Cache Size (GB)', fontweight='bold')
    plt.ylabel('Peak Disk-head Time (ms)', fontweight='bold')
    plt.title('Figure 4: Peak DT vs. Cache Size', fontweight='bold')
    plt.legend(fontsize=11, loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/figure4_cache_size.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 4: figures/figure4_cache_size.png")
    
    # Figure 5: τ_DT Ablation (E1)
    tau_dt = [0.5, 1.0, 1.5, 2.0, 2.5]
    peak_tau = [37.2, 38.7, 40.3, 42.1, 43.8]
    
    plt.figure(figsize=(10, 6))
    plt.plot(tau_dt, peak_tau, 'o-', linewidth=2.5, markersize=10,
            color='#3498db', alpha=0.8)
    plt.axvline(x=1.0, color='red', linestyle='--', alpha=0.5, label='Default')
    plt.xlabel('τ_DT (DT-per-byte threshold)', fontweight='bold')
    plt.ylabel('Peak Disk-head Time (ms)', fontweight='bold')
    plt.title('Figure 5: Peak DT vs. τ_DT (E1 DT-SLRU)', fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/figure5_tau_dt.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 5: figures/figure5_tau_dt.png")
    
    # Figure 6: PROTECTED Cap Ablation (E2)
    protected_cap = [0.1, 0.2, 0.3, 0.4, 0.5]
    peak_cap = [37.8, 36.2, 35.4, 36.1, 37.5]
    
    plt.figure(figsize=(10, 6))
    plt.plot(protected_cap, peak_cap, 'o-', linewidth=2.5, markersize=10,
            color='#2ecc71', alpha=0.8)
    plt.axvline(x=0.3, color='red', linestyle='--', alpha=0.5, label='Default')
    plt.xlabel('PROTECTED Cap (fraction)', fontweight='bold')
    plt.ylabel('Peak Disk-head Time (ms)', fontweight='bold')
    plt.title('Figure 6: Peak DT vs. PROTECTED Cap (E2 EDE)', fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/figure6_protected_cap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 6: figures/figure6_protected_cap.png")
    
    # Figure 7: α_tti Ablation (E2)
    alpha_tti = [0.1, 0.3, 0.5, 0.7, 0.9]
    peak_alpha = [38.2, 36.8, 35.4, 35.9, 37.1]
    
    plt.figure(figsize=(10, 6))
    plt.plot(alpha_tti, peak_alpha, 'o-', linewidth=2.5, markersize=10,
            color='#2ecc71', alpha=0.8)
    plt.axvline(x=0.5, color='red', linestyle='--', alpha=0.5, label='Default')
    plt.xlabel('α_tti (EWMA weight)', fontweight='bold')
    plt.ylabel('Peak Disk-head Time (ms)', fontweight='bold')
    plt.title('Figure 7: Peak DT vs. α_tti (E2 EDE)', fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/figure7_alpha_tti.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 7: figures/figure7_alpha_tti.png")
    
    print("=" * 60)
    print("All 7 figures generated successfully!")
    print("\nNote: These use synthetic data for demonstration.")
    print("To generate figures with real data:")
    print("  1. Run: bash run_a4_experiments.sh")
    print("  2. For ablations, edit configs and re-run experiments")
    print("  3. Use generate_a4_figures.ipynb notebook for custom analysis")
    print("=" * 60)

if __name__ == "__main__":
    try:
        generate_figures_with_synthetic_data()
    except Exception as e:
        print(f"Error generating figures: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
