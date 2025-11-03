#!/usr/bin/env python3

import subprocess
import sys
import json
import lzma
from pathlib import Path
from statistics import mean, stdev

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

def extract_metrics_from_run(run_dir):
    run_path = Path(run_dir)
    
    if not run_path.exists():
        return None
    
    result_dirs = [d for d in run_path.iterdir() 
                  if d.is_dir() and d.name.startswith('acceptall-1_')]
    
    if not result_dirs:
        return None
    
    result_dir = result_dirs[0]
    stats_file = result_dir / 'full_0_0.1_cache_perf.txt.lzma'
    
    if not stats_file.exists():
        return None
    
    try:
        with lzma.open(stats_file, 'rt') as f:
            data = json.load(f)
            stats = data['stats']
            
            peak_dt = stats.get('service_time_used3', 0) / 1000.0
            median_dt = stats.get('service_time_used2', 0) / 1000.0
            
            chunk_hits = float(stats.get('chunk_hits', 0))
            chunk_queries = float(stats.get('chunk_queries', 0))
            hit_rate = (chunk_hits / chunk_queries * 100) if chunk_queries > 0 else 0
            
            flash_write_traffic = stats.get('flash_write_traffic_gb', 0)
            
            return {
                'peak_dt': peak_dt,
                'median_dt': median_dt,
                'hit_rate': hit_rate,
                'flash_write_traffic_gb': flash_write_traffic,
                'chunk_hits': chunk_hits,
                'chunk_queries': chunk_queries
            }
    except Exception as e:
        print(f"Error extracting metrics from {run_dir}: {e}")
        return None

def average_results_across_runs(run1_metrics, run2_metrics, run3_metrics):
    if not all([run1_metrics, run2_metrics, run3_metrics]):
        return None
    
    metrics_list = [run1_metrics, run2_metrics, run3_metrics]
    
    averaged = {}
    for key in run1_metrics.keys():
        if isinstance(run1_metrics[key], (int, float)):
            values = [m[key] for m in metrics_list]
            averaged[key] = mean(values)
            if len(values) >= 2:
                averaged[f'{key}_std'] = stdev(values)
            else:
                averaged[f'{key}_std'] = 0.0
        else:
            averaged[key] = run1_metrics[key]
    
    return averaged

def main():
    base_dir = Path("runs/a5/fig_1_tau_dt")
    tau_dt_values = [0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
    
    results = {}
    output_file = Path("assignment5/results/fig_1_tau_dt_results.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print("="*80)
    print("FIGURE 1: tau_DT ABLATION STUDY")
    print("="*80)
    print(f"Parameter values: {tau_dt_values}")
    print(f"Runs per value: 3")
    print(f"Total simulations: {len(tau_dt_values) * 3}")
    print("="*80)
    
    successful_sims = 0
    failed_sims = 0
    sim_count = 0
    
    for tau in tau_dt_values:
        print(f"\n{'='*80}")
        print(f"Processing tau_DT = {tau}")
        print(f"{'='*80}")
        
        exp_base_dir = base_dir / f"e1_dtslru_tau_{tau}"
        run_dirs = [exp_base_dir / f"run_{i}" for i in [1, 2, 3]]
        run_metrics = []
        
        for run_num, run_dir in enumerate(run_dirs, 1):
            config_path = run_dir / "config.json"
            
            if not config_path.exists():
                print(f"Config not found: {config_path}")
                continue
            
            sim_count += 1
            print(f"\n[Simulation {sim_count}/{len(tau_dt_values) * 3}] tau_DT={tau}, Run {run_num}")
            
            needs_simulation = True
            result_dir = run_dir
            result_dirs = [d for d in result_dir.iterdir() 
                          if d.is_dir() and d.name.startswith('acceptall-1_')]
            
            if result_dirs:
                stats_file = result_dirs[0] / 'full_0_0.1_cache_perf.txt.lzma'
                if stats_file.exists():
                    print(f"  Results already exist, skipping simulation")
                    needs_simulation = False
            
            if needs_simulation:
                if run_simulation(config_path):
                    successful_sims += 1
                else:
                    failed_sims += 1
                    continue
            
            metrics = extract_metrics_from_run(run_dir)
            if metrics:
                run_metrics.append(metrics)
                print(f"  Peak DT: {metrics['peak_dt']:.3f}s")
                print(f"  Hit Rate: {metrics['hit_rate']:.1f}%")
            else:
                print(f"  Warning: Could not extract metrics from run {run_num}")
        
        if len(run_metrics) == 3:
            averaged = average_results_across_runs(run_metrics[0], run_metrics[1], run_metrics[2])
            if averaged:
                results[tau] = averaged
                print(f"\n  AVERAGED RESULTS (tau_DT = {tau}):")
                print(f"    Peak DT: {averaged['peak_dt']:.3f}s ± {averaged.get('peak_dt_std', 0):.3f}s")
                print(f"    Median DT: {averaged['median_dt']:.3f}s ± {averaged.get('median_dt_std', 0):.3f}s")
                print(f"    Hit Rate: {averaged['hit_rate']:.1f}% ± {averaged.get('hit_rate_std', 0):.1f}%")
            else:
                print(f"  Error: Could not average results for tau_DT = {tau}")
        elif len(run_metrics) > 0:
            print(f"  Warning: Only {len(run_metrics)}/3 runs completed for tau_DT = {tau}")
        else:
            print(f"  Error: No successful runs for tau_DT = {tau}")
    
    print("\n" + "="*80)
    print("SAVING RESULTS")
    print("="*80)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_file}")
    print(f"\nTotal parameter values processed: {len(results)}/{len(tau_dt_values)}")
    
    print("\n" + "="*80)
    print("SIMULATION SUMMARY")
    print("="*80)
    print(f"Successful simulations: {successful_sims}")
    print(f"Failed simulations: {failed_sims}")
    print(f"Total simulations run: {sim_count}")
    
    print("\n" + "="*80)
    print("AVERAGED RESULTS SUMMARY")
    print("="*80)
    for tau in sorted(results.keys()):
        r = results[tau]
        print(f"tau_DT = {tau:.2f}: Peak DT = {r['peak_dt']:.3f}s, Hit Rate = {r['hit_rate']:.1f}%")

if __name__ == "__main__":
    main()

