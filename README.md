# Project Documentation

## System Requirements
OS:
- Ubuntu 22.04 (tested)
- macOS 14 (expected compatible)
- Windows 10/11 (used during development)

CPU:
- x86_64 with AVX2 support

RAM:
- Minimum: 8 GB
- Recommended: 16 GB if running multiple simulations or notebooks in parallel

Disk:
- ~20 GB free for traces, intermediate results, and generated figures

GPU:
- Not required
- Optional if you want to accelerate ML components; CPU-only works for all required tasks

Python:
- 3.10 or 3.11

Key Python dependencies (installed via provided requirements/environment files):
- numpy==1.24.2
- pandas==1.5.3
- scipy==1.10.1
- scikit-learn==1.2.2
- lightgbm==3.3.5
- matplotlib==3.7.1
- seaborn==0.12.1
- tqdm
- psutil
- jupyterlab
- redis (optional; only for advanced runs)

Notes:
- We verified the wrapper commands on Windows 10 and Ubuntu 22.04. macOS 14 should work similarly.
- If you use Conda/Mamba, the environment YAML in `BCacheSim/install/` sets compatible versions for you. For pip, use `BCacheSim/install/requirements.txt`.
- Trace downloads can be large; confirm free disk space before running simulations.

## Setup & Installation

Provide step-by-step commands (with approximate time estimates).

### Step 1 - Clone repository

**Time estimate: ~1-2 minutes**

```bash
git clone --recurse-submodules https://github.com/JRYOO-FDU-CAPSTONE/csci-6806-fa-2025-6806_fa2025_group2.git
cd csci-6806-fa-2025-6806_fa2025_group2
```

### Step 2 - Create virtual environment

**Time estimate: ~30 seconds**

```bash
python3 -m venv baleen-env
```

### Step 3 - Activate virtual environment

**Time estimate: ~5 seconds**

```bash
source baleen-env/bin/activate
```

**Note:** On Windows, use `baleen-env\Scripts\activate` instead.

### Step 4 - Install dependencies

**Time estimate: ~2-5 minutes**

```bash
pip install -r BCacheSim/install/requirements.txt
```

**Note:** The requirements file includes all necessary packages. Alternatively, use Conda: `conda env create -f BCacheSim/install/env_cachelib-py-3.11.yaml` then `conda activate cachelib-py-3.11`.

## Reproduction Instructions

Include explicit commands for regenerating all figures and tables from your report, with filenames and runtimes.

### Assignment 4 Figures

#### Figure 1-3 - Baseline Comparison (Peak DT, Median DT, Hit Rate)

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a4_peak_median_hit_rate_figures.py
```

**Output files:**
- `assignment4/outputs/figure_1_peak_dt.png` and `.pdf`
- `assignment4/outputs/figure_2_median_dt.png` and `.pdf`
- `assignment4/outputs/figure_3_hit_rate.png` and `.pdf`
- `assignment4/outputs/assignment_4_figures_1_2_3_combined.png` and `.pdf`

**Runtime:** ~30 seconds

**Note:** Requires baseline simulation results (e0_lru, e1_dtslru, e2_ede) in `runs/a4/`.

---

#### Figure 4 - Cache Size Sensitivity

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a4_cache_size_sensitivity_figure.py
```

**Output files:**
- `assignment4/outputs/figure_4_cache_size.png` and `.pdf`

**Runtime:** ~30 seconds

**Note:** Requires cache size sensitivity simulation results in `runs/a4/fig_4_cache_size_sensitivity/`.

---

#### Figure 5 - tau_DT Ablation Study

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a4_tau_dt_ablation_figure.py
```

**Output files:**
- `assignment4/outputs/figure_5_tau_dt.png` and `.pdf`
- `assignment4/outputs/figure_5a_peak_dt_vs_tau_dt.png` and `.pdf`
- `assignment4/outputs/figure_5b_hit_rate_vs_tau_dt.png` and `.pdf`

**Runtime:** ~30 seconds

**Note:** Requires tau_DT ablation simulation results in `runs/a4/fig_5_tau_dt_ablation/`.

---

#### Figure 6 - Protected Capacity Ablation

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a4_protected_capacity_figure.py
```

**Output files:**
- `assignment4/outputs/figure_6_protected_cap.png` and `.pdf`
- `assignment4/outputs/figure_6a_peak_dt_vs_protected_cap.png` and `.pdf`
- `assignment4/outputs/figure_6b_hit_rate_utilization_vs_protected_cap.png` and `.pdf`

**Runtime:** ~30 seconds

**Note:** Requires protected capacity ablation simulation results in `runs/a4/fig_6_protected_cap_ablation/`.

---

#### Figure 7 - alpha_TTI Adaptation Study

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a4_alpha_tti_adaptation_figure.py
```

**Output files:**
- `assignment4/outputs/figure_7_alpha_tti.png` and `.pdf`
- `assignment4/outputs/figure_7a_peak_dt_vs_alpha_tti.png` and `.pdf`
- `assignment4/outputs/figure_7b_hit_rate_adaptation_vs_alpha_tti.png` and `.pdf`

**Runtime:** ~30 seconds

**Note:** Requires alpha_TTI adaptation simulation results in `runs/a4/fig_7_alpha_tti_ablation/`.

---

### Assignment 5 Figures

#### Figure 1 - Peak DT vs. tau_DT Sensitivity

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a5_peak_dt_tau_dt_figure.py
```

**Output files:**
- `assignment5/report/figures/figure_1_peak_dt_tau_dt.png` and `.pdf`

**Runtime:** ~30 seconds

**Note:** Requires aggregated results in `assignment5/results/fig_1_tau_dt_results.json`.

---

#### Figure 2 - Hit Rate vs. tau_DT Sensitivity

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a5_hitrate_tau_dt_figure.py
```

**Output files:**
- `assignment5/report/figures/figure_2_hitrate_tau_dt.png` and `.pdf`

**Runtime:** ~30 seconds

**Note:** Requires aggregated results in `assignment5/results/fig_1_tau_dt_results.json`.

---

#### Figure 3 - Peak DT vs. Protected Capacity

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a5_protected_cap_figure.py
```

**Output files:**
- `assignment5/report/figures/figure_3_peak_dt_protected_cap.png` and `.pdf`

**Runtime:** ~30 seconds

**Note:** Requires aggregated results in `assignment5/results/fig_3_protected_cap_results.json`.

---

#### Figure 4 - Peak DT vs. alpha_TTI

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a5_alpha_tti_figure.py
```

**Output files:**
- `assignment5/report/figures/figure_4_peak_dt_alpha_tti.png` and `.pdf`

**Runtime:** ~30 seconds

**Note:** Requires aggregated results in `assignment5/results/fig_4_alpha_tti_results.json`.

---

#### Figure 5 - Combined Sensitivity Summary

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a5_combined_sensitivity_figure.py
```

**Output files:**
- `assignment5/report/figures/figure_5_combined_sensitivity_summary.png` and `.pdf`

**Runtime:** ~30 seconds

**Note:** Requires all three result files: `fig_1_tau_dt_results.json`, `fig_3_protected_cap_results.json`, and `fig_4_alpha_tti_results.json`.

---

### Running All Figure Generation Commands

To regenerate all figures at once:

```bash
# Assignment 4 figures
python main/assignment7/bundle/scripts/generate_a4_peak_median_hit_rate_figures.py
python main/assignment7/bundle/scripts/generate_a4_cache_size_sensitivity_figure.py
python main/assignment7/bundle/scripts/generate_a4_tau_dt_ablation_figure.py
python main/assignment7/bundle/scripts/generate_a4_protected_capacity_figure.py
python main/assignment7/bundle/scripts/generate_a4_alpha_tti_adaptation_figure.py

# Assignment 5 figures
python main/assignment7/bundle/scripts/generate_a5_peak_dt_tau_dt_figure.py
python main/assignment7/bundle/scripts/generate_a5_hitrate_tau_dt_figure.py
python main/assignment7/bundle/scripts/generate_a5_protected_cap_figure.py
python main/assignment7/bundle/scripts/generate_a5_alpha_tti_figure.py
python main/assignment7/bundle/scripts/generate_a5_combined_sensitivity_figure.py
```

**Total runtime for all figures:** ~5 minutes (assuming simulation results already exist)

**Note:** All figure generation commands require simulation results to exist. If simulations have not been run, execute the simulation wrappers first (see `main/assignment7/bundle/README.md` for simulation commands).

## Validation Checklist


### Test 1 - Config Generation

**Command:**
```bash
python main/assignment7/bundle/configs/create_a4_configs.py
```

**Expected Output:**
- Success message: "ALL EXPERIMENT CONFIGS CREATED SUCCESSFULLY!"
- Config files created in `runs/a4/fig_4_cache_size_sensitivity/` (12 configs)
- Config files created in `runs/a4/fig_5_tau_dt_ablation/` (12 configs)
- Config files created in `runs/a4/fig_6_protected_cap_ablation/` (12 configs)
- Config files created in `runs/a4/fig_7_alpha_tti_ablation/` (12 configs)
- Total: 48 config files created

**Verification:**
```bash
# Verify config files exist
ls runs/a4/fig_4_cache_size_sensitivity/*/config.json | wc -l  
ls runs/a4/fig_5_tau_dt_ablation/*/config.json | wc -l        
```

---

### Test 2 - Figure Generation

**Command:**
```bash
python main/assignment7/bundle/scripts/generate_a4_peak_median_hit_rate_figures.py
```

**Expected Output:**
- Success message: "FIGURE GENERATION COMPLETE"
- Files created:
  - `assignment4/outputs/figure_1_peak_dt.png` and `.pdf`
  - `assignment4/outputs/figure_2_median_dt.png` and `.pdf`
  - `assignment4/outputs/figure_3_hit_rate.png` and `.pdf`
  - `assignment4/outputs/assignment_4_figures_1_2_3_combined.png` and `.pdf`

**Verification:**
```bash

test -f assignment4/outputs/figure_1_peak_dt.png && echo "Figure 1 exists" || echo "Figure 1 missing"
test -f assignment4/outputs/figure_2_median_dt.png && echo "Figure 2 exists" || echo "Figure 2 missing"
test -f assignment4/outputs/figure_3_hit_rate.png && echo "Figure 3 exists" || echo "Figure 3 missing"
```

**Note:** This test requires baseline simulation results (e0_lru, e1_dtslru, e2_ede) to exist in `runs/a4/`.

---

### Test 3 - Simulation Metrics Validation

**Command:**
```bash
python -c "
import json
import lzma
from pathlib import Path

# Check E1 DT-SLRU baseline results
result_file = Path('runs/a4/e1_dtslru/acceptall-1_lru_366.475GB/full_0_0.1_cache_perf.txt.lzma')
if result_file.exists():
    with lzma.open(result_file, 'rt') as f:
        data = json.load(f)
        stats = data['stats']
        peak_dt = stats.get('service_time_used3', 0) / 1000.0
        hit_rate = (stats.get('chunk_hits', 0) / stats.get('chunk_queries', 1)) * 100
        print(f'Peak DT: {peak_dt:.3f}s')
        print(f'Hit Rate: {hit_rate:.1f}%')
        print(f'Expected: Peak DT ≈ 3.8-4.0s, Hit Rate ≈ 4-6%')
else:
    print('Results file not found')
"
```

**Expected Output:**
- Peak DT: ≈ 3.8-4.0 seconds (for E1 DT-SLRU baseline)
- Hit Rate: ≈ 4-6% (for E1 DT-SLRU baseline)
- Metrics extracted successfully from simulation results

**Verification:**
- Peak DT should be between 3.0 and 4.5 seconds for baseline configurations
- Hit Rate should be between 3% and 10% for baseline configurations
- Results file (`full_0_0.1_cache_perf.txt.lzma`) should exist and be valid JSON

**Note:** This test validates that simulation results contain expected metrics. Exact values may vary slightly depending on trace data and system configuration, but should fall within the specified ranges.

---

### Test 4 - Bundle Helper Script

**Command:**
```bash
python main/assignment7/bundle/run_all.py --list
```

**Expected Output:**
- List of all available wrappers organized by category
- Categories: Configuration, Assignment 4 Simulations, Assignment 4 Figures, Assignment 5 Simulations, Assignment 5 Figures
- Total count of wrappers (should show 23+ wrappers)
- Usage instructions displayed

**Verification:**
- Output should include wrapper names like `create_a4_configs`, `generate_a4_figure_5`, etc.
- All wrapper categories should be listed
- No errors in wrapper discovery

---

### Test 5 - Result File Structure Validation

**Command:**
```bash
python -c "
import json
import lzma
from pathlib import Path

# Validate result file structure
result_file = Path('runs/a4/e1_dtslru/acceptall-1_lru_366.475GB/full_0_0.1_cache_perf.txt.lzma')
if result_file.exists():
    with lzma.open(result_file, 'rt') as f:
        data = json.load(f)
        if 'stats' in data:
            stats = data['stats']
            required_keys = ['service_time_used3', 'service_time_used2', 'chunk_hits', 'chunk_queries']
            missing = [k for k in required_keys if k not in stats]
            if missing:
                print(f'Missing keys: {missing}')
            else:
                print('All required keys present')
                print('Result file structure is valid')
        else:
            print('Invalid result file structure: missing stats key')
else:
    print('Results file not found')
"
```

**Expected Output:**
- All required keys present
- Result file structure is valid
- No missing keys error

**Verification:**
- Result files should contain `stats` key
- Stats should contain: `service_time_used3`, `service_time_used2`, `chunk_hits`, `chunk_queries`
- File should be valid compressed JSON (lzma format)

---

## Running All Validation Tests

To run all validation tests in sequence:

```bash
# Test 1: Config generation
python main/assignment7/bundle/configs/create_a4_configs.py

# Test 2: Figure generation (requires baseline results)
python main/assignment7/bundle/scripts/generate_a4_peak_median_hit_rate_figures.py

# Test 3: Simulation metrics (quick check)
python -c "import json, lzma; from pathlib import Path; f=Path('runs/a4/e1_dtslru/acceptall-1_lru_366.475GB/full_0_0.1_cache_perf.txt.lzma'); d=json.load(lzma.open(f,'rt')); s=d['stats']; print(f\"Peak DT: {s['service_time_used3']/1000:.3f}s, Hit Rate: {(s['chunk_hits']/s['chunk_queries']*100):.1f}%\")"

# Test 4: Bundle helper
python main/assignment7/bundle/run_all.py --list

# Test 5: Result file structure
python -c "import json, lzma; from pathlib import Path; f=Path('runs/a4/e1_dtslru/acceptall-1_lru_366.475GB/full_0_0.1_cache_perf.txt.lzma'); d=json.load(lzma.open(f,'rt')); print('Valid' if 'stats' in d and all(k in d['stats'] for k in ['service_time_used3','chunk_hits','chunk_queries']) else 'Invalid')"
```

**Expected:** All tests should complete without errors and produce the expected outputs listed above.

## Limitations

1. **Testbed code not included:** This repository contains only the Python simulator code. The testbed code that modified CacheLib is not included, as it was based on a proprietary internal version of CacheLib and is pending a rebase on the open-source version.

2. **Simulation runtime:** Each simulation takes approximately 10-30 minutes to complete. Running all experiments for a single figure (e.g., cache size sensitivity with 12 configurations) can take 2-6 hours. Assignment 5 experiments require 3 runs per parameter value, further increasing total runtime.

3. **Disk head time constants:** Meta's exact constants for the disk head time function are not released. This repository uses constants (seek time and bandwidth) measured on university testbed hard disks, meaning results will not exactly match the paper's values, though trends and relative performance should be consistent.

4. **Memory and disk requirements:** Memory usage scales with trace file size, and simulations require significant disk space for intermediate results. Running multiple simulations in parallel requires 16+ GB RAM. Trace files themselves can be several GB in size.

5. **Base configuration dependency:** All experiments require baseline configuration files (`runs/a4/e0_lru/config.json`, `runs/a4/e1_dtslru/config.json`, `runs/a4/e2_ede/config.json`) to exist before generating experiment-specific configs. These base configs must be created manually or provided separately.


