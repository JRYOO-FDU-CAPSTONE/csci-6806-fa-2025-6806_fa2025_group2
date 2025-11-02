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
    base_dir = Path("runs/a5")
    
    with open("runs/a4/e1_dtslru/config.json", 'r') as f:
        dtslru_base_config = json.load(f)
    
    with open("runs/a4/e2_ede/config.json", 'r') as f:
        ede_base_config = json.load(f)
    
    fig1_dir = base_dir / "fig_1_tau_dt"
    fig1_dir.mkdir(parents=True, exist_ok=True)
    
    tau_dt_values = [0.05, 0.1, 0.25, 0.5, 1.0, 1.5, 2.5]
    
    for tau in tau_dt_values:
        for run_num in [1, 2, 3]:
            exp_dir = fig1_dir / f"e1_dtslru_tau_{tau}" / f"run_{run_num}"
            exp_dir.mkdir(parents=True, exist_ok=True)
            
            config_mods = {
                "output_dir": f"runs/a5/fig_1_tau_dt/e1_dtslru_tau_{tau}/run_{run_num}",
                "tau_dt_threshold": tau
            }
            
            create_config_file(exp_dir / "config.json", dtslru_base_config, config_mods)
            print(f"Created: {exp_dir}/config.json")
    
    fig3_dir = base_dir / "fig_3_protected_cap"
    fig3_dir.mkdir(parents=True, exist_ok=True)
    
    protected_cap_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    for cap in protected_cap_values:
        for run_num in [1, 2, 3]:
            exp_dir = fig3_dir / f"e2_ede_cap_{cap}" / f"run_{run_num}"
            exp_dir.mkdir(parents=True, exist_ok=True)
            
            config_mods = {
                "output_dir": f"runs/a5/fig_3_protected_cap/e2_ede_cap_{cap}/run_{run_num}",
                "protected_cap": cap
            }
            
            create_config_file(exp_dir / "config.json", ede_base_config, config_mods)
            print(f"Created: {exp_dir}/config.json")
    
    fig4_dir = base_dir / "fig_4_alpha_tti"
    fig4_dir.mkdir(parents=True, exist_ok=True)
    
    alpha_tti_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    for alpha in alpha_tti_values:
        for run_num in [1, 2, 3]:
            exp_dir = fig4_dir / f"e2_ede_alpha_{alpha}" / f"run_{run_num}"
            exp_dir.mkdir(parents=True, exist_ok=True)
            
            config_mods = {
                "output_dir": f"runs/a5/fig_4_alpha_tti/e2_ede_alpha_{alpha}/run_{run_num}",
                "alpha_tti": alpha
            }
            
            create_config_file(exp_dir / "config.json", ede_base_config, config_mods)
            print(f"Created: {exp_dir}/config.json")
    
    print("\n" + "="*60)
    print("ALL ASSIGNMENT 5 EXPERIMENT CONFIGS CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"Figure 1 (tau_DT): {len(tau_dt_values)} values × 3 runs = {len(tau_dt_values) * 3} configs")
    print(f"Figure 3 (PROTECTED cap): {len(protected_cap_values)} values × 3 runs = {len(protected_cap_values) * 3} configs")
    print(f"Figure 4 (alpha_tti): {len(alpha_tti_values)} values × 3 runs = {len(alpha_tti_values) * 3} configs")
    print(f"Total: {(len(tau_dt_values) + len(protected_cap_values) + len(alpha_tti_values)) * 3} config files")
    print(f"Total simulations: {(len(tau_dt_values) + len(protected_cap_values) + len(alpha_tti_values)) * 3}")

if __name__ == "__main__":
    main()

