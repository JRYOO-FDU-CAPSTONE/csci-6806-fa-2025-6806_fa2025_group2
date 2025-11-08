#!/usr/bin/env python3

import os
import json
from pathlib import Path

def create_config_file(output_path, base_config, modifications):
    config = base_config.copy()
    config.update(modifications)
    
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)

def main():
    base_dir = Path("runs/a4")
    
    with open("runs/a4/e0_lru/config.json", 'r') as f:
        lru_base_config = json.load(f)
    
    with open("runs/a4/e1_dtslru/config.json", 'r') as f:
        dtslru_base_config = json.load(f)
    
    with open("runs/a4/e2_ede/config.json", 'r') as f:
        ede_base_config = json.load(f)
    
    fig4_dir = base_dir / "fig_4_cache_size_sensitivity"
    fig4_dir.mkdir(exist_ok=True)
    
    cache_sizes = [100, 200, 300, 500, 750, 1000]
    
    for size in cache_sizes:
        exp_dir = fig4_dir / f"e0_lru_{size}GB"
        exp_dir.mkdir(exist_ok=True)
        
        config_mods = {
            "output_dir": f"runs/a4/fig_4_cache_size_sensitivity/e0_lru_{size}GB",
            "size_gb": size
        }
        
        create_config_file(exp_dir / "config.json", lru_base_config, config_mods)
        print(f"Created: {exp_dir}/config.json")
    
    for size in cache_sizes:
        exp_dir = fig4_dir / f"e1_dtslru_{size}GB"
        exp_dir.mkdir(exist_ok=True)
        
        config_mods = {
            "output_dir": f"runs/a4/fig_4_cache_size_sensitivity/e1_dtslru_{size}GB",
            "size_gb": size
        }
        
        create_config_file(exp_dir / "config.json", dtslru_base_config, config_mods)
        print(f"Created: {exp_dir}/config.json")
    
    fig5_dir = base_dir / "fig_5_tau_dt_ablation"
    fig5_dir.mkdir(exist_ok=True)
    
    tau_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0]
    
    for tau in tau_values:
        exp_dir = fig5_dir / f"e1_dtslru_tau_{tau}"
        exp_dir.mkdir(exist_ok=True)
        
        config_mods = {
            "output_dir": f"runs/a4/fig_5_tau_dt_ablation/e1_dtslru_tau_{tau}",
            "tau_dt_threshold": tau
        }
        
        create_config_file(exp_dir / "config.json", dtslru_base_config, config_mods)
        print(f"Created: {exp_dir}/config.json")
    
    fig6_dir = base_dir / "fig_6_protected_cap_ablation"
    fig6_dir.mkdir(exist_ok=True)
    
    cap_values = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8]
    
    for cap in cap_values:
        exp_dir = fig6_dir / f"e2_ede_cap_{cap}"
        exp_dir.mkdir(exist_ok=True)
        
        config_mods = {
            "output_dir": f"runs/a4/fig_6_protected_cap_ablation/e2_ede_cap_{cap}",
            "protected_cap": cap
        }
        
        create_config_file(exp_dir / "config.json", ede_base_config, config_mods)
        print(f"Created: {exp_dir}/config.json")
    
    fig7_dir = base_dir / "fig_7_alpha_tti_ablation"
    fig7_dir.mkdir(exist_ok=True)
    
    alpha_values = [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    
    for alpha in alpha_values:
        exp_dir = fig7_dir / f"e2_ede_alpha_{alpha}"
        exp_dir.mkdir(exist_ok=True)
        
        config_mods = {
            "output_dir": f"runs/a4/fig_7_alpha_tti_ablation/e2_ede_alpha_{alpha}",
            "alpha_tti": alpha
        }
        
        create_config_file(exp_dir / "config.json", ede_base_config, config_mods)
        print(f"Created: {exp_dir}/config.json")
    
    print("\n" + "="*60)
    print("ALL EXPERIMENT CONFIGS CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"Figure 4 (Cache Size): {len(cache_sizes) * 2} experiments")
    print(f"Figure 5 (τ_DT): {len(tau_values)} experiments")
    print(f"Figure 6 (PROTECTED cap): {len(cap_values)} experiments")
    print(f"Figure 7 (α_tti): {len(alpha_values)} experiments")
    print(f"Total: {len(cache_sizes) * 2 + len(tau_values) + len(cap_values) + len(alpha_values)} experiments")

if __name__ == "__main__":
    main()

