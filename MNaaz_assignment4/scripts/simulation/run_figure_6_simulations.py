#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def run_simulation(config_path):
    cmd = [
        sys.executable, "-B", "-m", "BCacheSim.cachesim.simulate_ap",
        "--config", str(config_path),
        "--ignore-existing"
    ]
    
    print(f"\n{'='*80}")
    print(f"Running simulation: {config_path}")
    print(f"{'='*80}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*80}")
    
    try:
        result = subprocess.run(cmd, timeout=3600)
        if result.returncode == 0:
            print(f"\nSuccess: {config_path}")
            return True
        else:
            print(f"\nFailed: {config_path} (exit code: {result.returncode})")
            return False
    except subprocess.TimeoutExpired:
        print(f"\nTimeout: {config_path}")
        return False
    except Exception as e:
        print(f"\nError: {config_path} - {e}")
        return False

def main():
    base_dir = Path("runs/a4/fig_6_protected_cap_ablation")
    cap_values = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8]
    
    simulations = []
    for cap in cap_values:
        simulations.append(base_dir / f"e2_ede_cap_{cap}" / "config.json")
    
    print(f"Figure 6: PROTECTED cap Ablation Study - {len(simulations)} simulations")
    print("="*60)
    
    successful = 0
    failed = 0
    
    for i, config_path in enumerate(simulations, 1):
        print(f"\n[{i}/{len(simulations)}] Processing {config_path}")
        
        if not config_path.exists():
            print(f"Config file not found: {config_path}")
            failed += 1
            continue
        
        if run_simulation(config_path):
            successful += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print("FIGURE 6 SIMULATION SUMMARY")
    print("="*60)
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(simulations)}")

if __name__ == "__main__":
    main()

