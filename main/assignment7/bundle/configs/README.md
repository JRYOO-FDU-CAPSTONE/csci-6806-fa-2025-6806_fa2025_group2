# Configuration Files

This directory contains references and documentation for configuration files used by the Assignment 7 bundle wrappers.

## Overview

Configuration files are generated dynamically by running config creation scripts. The generated configs are stored in the `runs/` directory and are used by simulation scripts.

## Configuration Setup

### Assignment 4 Configs

**Origin:** `assignment4/scripts/config/create_all_experiment_configs.py`

**Base Configs Required:**
- `runs/a4/e0_lru/config.json` - Base config for LRU eviction policy
- `runs/a4/e1_dtslru/config.json` - Base config for DT-SLRU eviction policy
- `runs/a4/e2_ede/config.json` - Base config for EDE eviction policy

**Generated Configs Location:** `runs/a4/`

**Generated Configs:**
- `runs/a4/fig_4_cache_size_sensitivity/` - Cache size sensitivity experiments
- `runs/a4/fig_5_tau_dt_ablation/` - tau_DT ablation experiments
- `runs/a4/fig_6_protected_cap_ablation/` - Protected capacity ablation experiments
- `runs/a4/fig_7_alpha_tti_ablation/` - alpha_TTI ablation experiments

**Usage:**
```bash
python main/assignment7/bundle/configs/create_a4_configs.py
```

### Assignment 5 Configs

**Origin:** `assignment5/scripts/config/create_a5_experiment_configs.py`

**Base Configs Required:**
- `runs/a4/e1_dtslru/config.json` - Base config for DT-SLRU (inherited from A4)
- `runs/a4/e2_ede/config.json` - Base config for EDE (inherited from A4)

**Generated Configs Location:** `runs/a5/`

**Generated Configs:**
- `runs/a5/fig_1_tau_dt/` - tau_DT ablation experiments (3 runs per value)
- `runs/a5/fig_3_protected_cap/` - Protected capacity experiments (3 runs per value)
- `runs/a5/fig_4_alpha_tti/` - alpha_TTI adaptation experiments (3 runs per value)

**Usage:**
```bash
python main/assignment7/bundle/configs/create_a5_configs.py
```

## Setup Order

1. Ensure base configs exist in `runs/a4/e0_lru/`, `runs/a4/e1_dtslru/`, and `runs/a4/e2_ede/`
2. Run Assignment 4 config creation: `create_a4_configs.py`
3. Run Assignment 5 config creation: `create_a5_configs.py` (requires A4 base configs)

## Notes

- Config files are generated in JSON format
- Each experiment gets its own directory with a `config.json` file
- Assignment 5 experiments include multiple runs (3 runs per parameter value) for statistical significance
- Base configs must exist before running config creation scripts
- Generated configs are stored in `runs/` directory, not in this bundle folder

