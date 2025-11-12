# A4 Quick Reference

## Files to Submit/Review

### Core Implementation
- `BCacheSim/cachesim/policies_a4.py` - **Main implementation** (450+ lines)

### Configuration
- `runs/configs/e0_lru.json` - E0 configuration
- `runs/configs/e1_dtslru.json` - E1 configuration  
- `runs/configs/e2_ede.json` - E2 configuration

### Testing & Scripts
- `runs/test_policies.py` - Unit tests (all passing)
- `runs/run_a4_experiments.sh` - Experiment runner

### Documentation
- `runs/A4_README.md` - User guide
- `runs/IMPLEMENTATION_SUMMARY.md` - Implementation details
- `runs/QUICK_REFERENCE.md` - This file

## Commands

### Test Policies
```bash
cd /Users/mishuthescarecrow/Baleen-FAST24
python runs/test_policies.py
```

### Run All Experiments
```bash
cd runs
bash run_a4_experiments.sh
```

### Generate Figures
```bash
cd runs
python generate_figures.py
# Or use Jupyter notebook:
jupyter notebook generate_a4_figures.ipynb
```

### Run Single Experiment
```bash
# E0 (LRU)
./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap --config runs/configs/e0_lru.json

# E1 (DT-SLRU)
./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap --config runs/configs/e1_dtslru.json

# E2 (EDE)
./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap --config runs/configs/e2_ede.json
```

## Policy Overview

| Policy | Type | Key Feature | Parameters |
|--------|------|-------------|------------|
| E0: PolicyLRU | Baseline | Classic LRU | None |
| E1: PolicyDTSLRU | Segmented | DT-aware promotion | `tau_dt` (default: 1.0) |
| E2: PolicyEDE | Predictive | EWMA expiry prediction | `alpha_tti` (0.5), `protected_cap` (0.3) |

## Key Parameters

### E1: DT-SLRU
- **tau_dt**: DT-per-byte threshold for promotion to Protected
  - Lower (0.5) = more items protected
  - Higher (2.0) = fewer items protected

### E2: EDE
- **alpha_tti**: EWMA weight (0.0 to 1.0)
  - 0.8-1.0 = adapt quickly to recent patterns
  - 0.0-0.2 = rely on historical average
- **protected_cap**: Max fraction for protected items (0.0 to 1.0)
  - 0.2 = 20% protected
  - 0.4 = 40% protected

## Metrics to Analyze

Primary:
- **Peak Disk-head Time (Peak DT)** - Main metric

Secondary:
- **Median DT** - Typical performance
- **Hit Rate** - Cache effectiveness
- **Flash Write Traffic** - Write amplification

## Ablation Studies

### E1: τ_DT Threshold
```bash
# Edit runs/configs/e1_dtslru.json
# Try: 0.5, 1.0, 1.5, 2.0
"policy_kwargs": {"tau_dt": 1.0}
```

### E2: α_tti (EWMA)
```bash
# Edit runs/configs/e2_ede.json
# Try: 0.2, 0.5, 0.8
"policy_kwargs": {"alpha_tti": 0.5, "protected_cap": 0.3}
```

### E2: Protected Cap
```bash
# Edit runs/configs/e2_ede.json
# Try: 0.2, 0.3, 0.4
"policy_kwargs": {"alpha_tti": 0.5, "protected_cap": 0.3}
```

## Results Location

After running experiments:
- `runs/e0_lru/*_cache_perf.txt`
- `runs/e1_dtslru/*_cache_perf.txt`
- `runs/e2_ede/*_cache_perf.txt`

## Common Issues

**"Trace file not found"**
```bash
cd data
bash get-tectonic.sh
```

**"Module not found"**
```bash
conda activate cachelib-py-3.11
```

**"Results already exist"**
```bash
# Add --ignore-existing flag or delete old results
rm -rf runs/e0_lru runs/e1_dtslru runs/e2_ede
```

## Implementation Checklist

- [x] E0: PolicyLRU implemented
- [x] E1: PolicyDTSLRU implemented with 2 segments
- [x] E2: PolicyEDE implemented with EWMA
- [x] DT-per-byte calculation
- [x] Integration with simulator
- [x] Config files created
- [x] Unit tests passing
- [x] Documentation complete

## Status: Ready for Experiments ✓

All implementation is complete. You can now:
1. Run experiments with trace data
2. Collect metrics (Peak DT, hit rate, etc.)
3. Generate figures comparing E0, E1, E2
4. Run ablation studies
5. Write analysis

## Contact/Help

- See `runs/A4_README.md` for detailed instructions
- See `runs/IMPLEMENTATION_SUMMARY.md` for design details
- Check assignment PDF for requirements
