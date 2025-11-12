# A4: Eviction Policy Evaluation

This directory contains the implementation and experiments for Assignment 4 (A4): Evaluating eviction policies in a flash caching system.

## Overview

The assignment implements and evaluates three eviction schemes:

1. **E0 - Baseline LRU**: Classic Least Recently Used policy
2. **E1 - DT-SLRU**: Segmented LRU with Disk-Head Time (DT) aware promotion
3. **E2 - EDE**: Episode-Deadline Eviction with time-to-idle predictions

## Implementation

### Source Files

- `BCacheSim/cachesim/policies_a4.py` - Custom eviction policy implementations
- `BCacheSim/cachesim/sim_cache.py` - Integration with simulator (modified)
- `BCacheSim/cachesim/simulate_ap.py` - Command-line interface (modified)

### Configuration Files

- `runs/configs/e0_lru.json` - LRU baseline configuration
- `runs/configs/e1_dtslru.json` - DT-SLRU configuration with τ_DT parameter
- `runs/configs/e2_ede.json` - EDE configuration with α_tti and protected_cap parameters

## Running Experiments

### Prerequisites

1. Install dependencies (if not already done):
   ```bash
   conda env create -f BCacheSim/install/env_cachelib-py-3.11.yaml
   conda activate cachelib-py-3.11
   ```

2. Download trace data (if not already done):
   ```bash
   cd data
   bash get-tectonic.sh
   ```

### Run All Experiments

From the project root directory:

```bash
cd runs
bash run_a4_experiments.sh
```

This will run all three eviction policies (E0, E1, E2) sequentially.

### Run Individual Experiments

You can also run experiments individually:

```bash
# E0: LRU Baseline
./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap --config runs/configs/e0_lru.json

# E1: DT-SLRU
./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap --config runs/configs/e1_dtslru.json

# E2: EDE
./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap --config runs/configs/e2_ede.json
```

## Configuration Parameters

### Common Parameters

- `policy`: Policy class name (PolicyLRU, PolicyDTSLRU, or PolicyEDE)
- `policy_module`: Module containing the policy (BCacheSim.cachesim.policies_a4)
- `ap`: Admission policy (acceptall - to isolate eviction impact)
- `prefetch_when`: Prefetch setting (never - to isolate eviction impact)
- `trace`: Path to trace file
- `size_gb`: Cache size in GB
- `sample_ratio`: Trace sampling ratio
- `seek_time_ms`: Disk seek time in milliseconds (for DT calculation)
- `bandwidth_mbps`: Disk bandwidth in MB/s (for DT calculation)

### E1: DT-SLRU Specific

- `policy_kwargs.tau_dt`: DT-per-byte promotion threshold (default: 1.0)
  - Lower values → more items promoted to Protected
  - Higher values → fewer items promoted, more selective

### E2: EDE Specific

- `policy_kwargs.alpha_tti`: EWMA weight for time-to-idle prediction (default: 0.5)
  - Close to 1 → adapt quickly to recent inter-arrival times
  - Close to 0 → use historical average
- `policy_kwargs.protected_cap`: Maximum fraction of cache for protected items (default: 0.3)

## Output

Results are saved in:
- `runs/e0_lru/` - LRU results
- `runs/e1_dtslru/` - DT-SLRU results
- `runs/e2_ede/` - EDE results

Each directory contains:
- `*_cache_perf.txt` - Performance metrics (hit rate, miss rate, Peak DT, etc.)
- `*.out` - Simulation output log
- `*.err` - Error log (if any)

## Generate Figures

After running experiments, generate the 7 required figures:

### Quick Method (Python Script)
```bash
cd runs
python generate_figures.py
```

This generates all 7 figures in `runs/figures/`:
1. `figure1_peak_dt.png` - Peak DT comparison (E0-E2)
2. `figure2_median_dt.png` - Median DT comparison (E0-E2)
3. `figure3_hit_rate.png` - Hit rate comparison (E0-E2)
4. `figure4_cache_size.png` - Cache size sensitivity
5. `figure5_tau_dt.png` - E1 ablation study
6. `figure6_protected_cap.png` - E2 ablation study
7. `figure7_alpha_tti.png` - E2 ablation study

### Interactive Method (Jupyter Notebook)
```bash
cd runs
jupyter notebook generate_a4_figures.ipynb
```

The notebook allows you to:
- Load actual experiment results
- Customize figure styling
- Add additional analysis
- Export figures in different formats

**Note:** Initial figures use synthetic data. After running real experiments, the scripts will automatically use actual results.

## Key Metrics

The assignment evaluates policies based on:

1. **Peak Disk-head Time (Peak DT)** - Primary metric
2. **Median DT** - Secondary metric
3. **Hit Rate** - Secondary metric
4. **Flash Write Traffic** - Secondary metric

## Policy Descriptions

### E0: Baseline LRU

Classic LRU eviction - evicts the least recently used item. Simple and serves as the baseline for comparison.

### E1: DT-SLRU (Segmented LRU with DT-aware promotion)

Two segments:
- **Probation**: New items start here
- **Protected**: Items promoted on second hit OR high DT-per-byte

Victims are selected from Probation first. The τ_DT parameter controls promotion threshold.

### E2: EDE (Episode-Deadline Eviction)

Predicts item expiry using EWMA on inter-arrival times. Evicts items closest to predicted expiry. Items with high DT-per-byte are protected up to protected_cap fraction of cache.

## Ablation Studies

To run ablation studies as specified in the assignment:

### E1: τ_DT Threshold Study

Edit `runs/configs/e1_dtslru.json` and modify `policy_kwargs.tau_dt`:
- Low values (e.g., 0.5) → more promotion
- High values (e.g., 2.0) → less promotion

### E2: PROTECTED Cap Study

Edit `runs/configs/e2_ede.json` and modify `policy_kwargs.protected_cap`:
- Values like 0.2, 0.3, 0.4 control protected fraction

### E2: α_tti (EWMA) Study

Edit `runs/configs/e2_ede.json` and modify `policy_kwargs.alpha_tti`:
- Close to 1 (e.g., 0.8) → adapt quickly
- Close to 0 (e.g., 0.2) → use historical average

## Troubleshooting

### "Trace file not found"
Ensure you've downloaded the trace data:
```bash
cd data
bash get-tectonic.sh
```

### "Module not found" errors
Ensure you're in the correct conda environment:
```bash
conda activate cachelib-py-3.11
```

### "Config file format error"
Ensure JSON config files are valid. Use `python -m json.tool < config.json` to validate.

## References

- Assignment document: See attached PDF
- Baleen paper: [Baleen-FAST24.pdf](https://wonglkd.fi-de.net/papers/Baleen-FAST24.pdf)
- Repository: https://github.com/wonglkd/Baleen-FAST24
