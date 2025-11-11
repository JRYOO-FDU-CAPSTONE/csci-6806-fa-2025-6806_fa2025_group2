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
    base_dir = Path("runs/a4/fig_4_cache_size_sensitivity")
    cache_sizes = [100, 200, 300, 500, 750, 1000]
    
    simulations = []
    
    for size in cache_sizes:
        simulations.append(base_dir / f"e0_lru_{size}GB" / "config.json")
    
    for size in cache_sizes:
        simulations.append(base_dir / f"e1_dtslru_{size}GB" / "config.json")
    
    print(f"Figure 4: Cache Size Sensitivity - {len(simulations)} simulations")
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
    print("FIGURE 4 SIMULATION SUMMARY")
    print("="*60)
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(simulations)}")

if __name__ == "__main__":
    main()

