# A4 Assignment Implementation Summary

## Implementation Complete ✓

All three eviction policies have been successfully implemented and tested.

## What Was Implemented

### 1. Eviction Policies (`BCacheSim/cachesim/policies_a4.py`)

#### E0: PolicyLRU - Baseline LRU
- Classic Least Recently Used eviction
- Items evicted in order of last access time (oldest first)
- Serves as baseline for comparison

**Key Methods:**
- `admit(key, item)` - Add item to cache
- `touch(key)` - Move item to MRU position on hit
- `evict(key=None)` - Evict LRU item
- `victim()` - Return next victim without evicting

#### E1: PolicyDTSLRU - Segmented LRU with DT-aware Promotion
- Two segments: **Probation** (for new items) and **Protected** (for promoted items)
- New items start in Probation
- Promotion to Protected on: **second hit OR high DT-per-byte** (≥ τ_DT)
- Victims selected from Probation first, then Protected

**Key Parameters:**
- `tau_dt` - DT-per-byte threshold for promotion (default: 1.0 ms/byte)
- `seek_time_ms` - Disk seek time for DT calculation (default: 5.0 ms)
- `bandwidth_mbps` - Disk bandwidth for DT calculation (default: 100 MB/s)

**Key Methods:**
- `admit(key, item)` - Add to Probation, calculate DT-per-byte
- `touch(key)` - Handle hit, may promote to Protected
- `evict(key=None)` - Evict from Probation first
- `victim()` - Return next victim (from Probation preferentially)

#### E2: PolicyEDE - Episode-Deadline Eviction
- Predicts item expiry using EWMA (Exponentially Weighted Moving Average)
- Based on inter-arrival times (time between accesses)
- Evicts items closest to predicted expiry time
- High DT-per-byte items tracked separately (up to protected_cap)

**Key Parameters:**
- `alpha_tti` - EWMA weight for time-to-idle (default: 0.5)
  - Close to 1.0 → adapt quickly to recent patterns
  - Close to 0.0 → rely more on historical average
- `protected_cap` - Max fraction for protected items (default: 0.3)

**Key Methods:**
- `admit(key, item)` - Calculate initial expiry estimate
- `touch(key)` - Update expiry estimate using EWMA
- `evict(key=None)` - Evict item with earliest predicted expiry
- `victim()` - Return item with earliest expiry

### 2. DT-per-byte Calculation

**Function:** `compute_dt_per_byte(size_bytes, seek_time_ms, bandwidth_mbps)`

Calculates disk-head time per byte:
```
DT_total = seek_time + transfer_time
transfer_time = size / bandwidth
DT_per_byte = DT_total / size
```

This metric captures the "cost" of fetching an object from disk:
- **Smaller objects**: Higher DT-per-byte (seek time dominates)
- **Larger objects**: Lower DT-per-byte (seek time amortized)

### 3. Simulator Integration

**Modified Files:**
- `BCacheSim/cachesim/sim_cache.py` - Added custom policy loading logic
- `BCacheSim/cachesim/simulate_ap.py` - Added CLI arguments for policies

**New Arguments:**
- `--policy` - Policy class name (e.g., PolicyLRU, PolicyDTSLRU, PolicyEDE)
- `--policy-module` - Module path (default: BCacheSim.cachesim.policies_a4)
- `--policy-kwargs` - Policy constructor arguments as dict
- `--seek-time-ms` - Disk seek time (default: 5.0 ms)
- `--bandwidth-mbps` - Disk bandwidth (default: 100 MB/s)

### 4. Configuration Files

Three JSON config files in `runs/configs/`:

**e0_lru.json:**
```json
{
  "policy": "PolicyLRU",
  "ap": "acceptall",
  "prefetch_when": "never",
  "size_gb": 100,
  "sample_ratio": 0.1
}
```

**e1_dtslru.json:**
```json
{
  "policy": "PolicyDTSLRU",
  "policy_kwargs": {"tau_dt": 1.0},
  "ap": "acceptall",
  "prefetch_when": "never",
  "size_gb": 100,
  "sample_ratio": 0.1
}
```

**e2_ede.json:**
```json
{
  "policy": "PolicyEDE",
  "policy_kwargs": {"alpha_tti": 0.5, "protected_cap": 0.3},
  "ap": "acceptall",
  "prefetch_when": "never",
  "size_gb": 100,
  "sample_ratio": 0.1
}
```

### 5. Testing & Documentation

**Test Script:** `runs/test_policies.py`
- Unit tests for all three policies
- Tests DT calculation
- Tests admission, eviction, and victim selection
- All tests passing ✓

**Run Script:** `runs/run_a4_experiments.sh`
- Automated script to run all three experiments
- Checks for required data files
- Runs simulations sequentially
- Reports results locations

**Documentation:** `runs/A4_README.md`
- Complete usage guide
- Parameter descriptions
- Ablation study instructions
- Troubleshooting tips

## How to Use

### Quick Start

1. **Run Unit Tests:**
   ```bash
   cd /Users/mishuthescarecrow/Baleen-FAST24
   python runs/test_policies.py
   ```

2. **Run All Experiments:**
   ```bash
   cd runs
   bash run_a4_experiments.sh
   ```

3. **Run Individual Experiment:**
   ```bash
   ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap \
     --config runs/configs/e0_lru.json
   ```

### Verify Implementation

The unit tests verify:
- ✓ DT-per-byte calculation is correct
- ✓ LRU evicts oldest item
- ✓ DT-SLRU has two segments and promotes correctly
- ✓ EDE calculates expiry times and evicts by deadline

### Ablation Studies

**E1: Vary τ_DT threshold**
```bash
# Edit runs/configs/e1_dtslru.json
# Change "tau_dt" to 0.5, 1.0, 2.0, etc.
# Then re-run experiment
```

**E2: Vary α_tti (EWMA weight)**
```bash
# Edit runs/configs/e2_ede.json
# Change "alpha_tti" to 0.2, 0.5, 0.8, etc.
# Then re-run experiment
```

**E2: Vary protected_cap**
```bash
# Edit runs/configs/e2_ede.json
# Change "protected_cap" to 0.2, 0.3, 0.4, etc.
# Then re-run experiment
```

## Key Design Decisions

### 1. Integration Approach
- Policies implement same interface as existing LRUPolicy and TTLPolicy
- Allows drop-in replacement in QueueCache
- Methods: `admit()`, `touch()`, `evict()`, `victim()`, `__contains__()`, `__len__()`, etc.

### 2. DT Calculation
- Computed on-demand during admission
- Uses configurable seek time and bandwidth parameters
- Realistic model: DT = seek_time + size/bandwidth

### 3. E1 DT-SLRU Implementation
- Uses OrderedDict for both Probation and Protected lists
- Maintains hit counters for promotion logic
- Evicts from Probation preferentially (FIFO within segment)

### 4. E2 EDE Implementation
- Uses min-heap for efficient expiry-based eviction
- Lazy heap cleanup (stale entries skipped during eviction)
- EWMA formula: `new_expiry = now + α×IAT + (1-α)×prev_remaining_time`

### 5. Configuration via JSON
- Leverages existing jsonargparse infrastructure
- Easy to specify policy and parameters
- Supports nested kwargs via policy_kwargs

## Expected Results

When running experiments, you should see:
- **Peak DT** metrics for each policy in `*_cache_perf.txt` files
- **Hit rates** showing cache effectiveness
- **Median DT** for typical workload performance

**Hypothesis:**
- E0 (LRU): Baseline performance
- E1 (DT-SLRU): Better Peak DT by protecting high-DT items
- E2 (EDE): Even better by predicting reuse and protecting accordingly

## Files Changed/Created

### Modified Files:
1. `BCacheSim/cachesim/policies_a4.py` - All three policies (450+ lines)
2. `BCacheSim/cachesim/sim_cache.py` - Custom policy loading (~30 lines added)
3. `BCacheSim/cachesim/simulate_ap.py` - CLI arguments (~10 lines added)

### Created Files:
1. `runs/configs/e0_lru.json` - LRU config
2. `runs/configs/e1_dtslru.json` - DT-SLRU config
3. `runs/configs/e2_ede.json` - EDE config
4. `runs/run_a4_experiments.sh` - Experiment runner
5. `runs/test_policies.py` - Unit tests
6. `runs/A4_README.md` - User documentation
7. `runs/IMPLEMENTATION_SUMMARY.md` - This file

### Output Directories:
- `runs/e0_lru/` - LRU results (created on first run)
- `runs/e1_dtslru/` - DT-SLRU results (created on first run)
- `runs/e2_ede/` - EDE results (created on first run)

## Next Steps

1. **Run experiments** with trace data to collect metrics
2. **Compare results** across three policies (E0, E1, E2)
3. **Run ablation studies** by varying parameters
4. **Generate figures** using provided notebook templates
5. **Write analysis** discussing which policy performs best and why

## Troubleshooting

**Issue:** ModuleNotFoundError
**Solution:** Make sure you're running from project root and BCacheSim is in path

**Issue:** Trace file not found
**Solution:** Run `cd data && bash get-tectonic.sh` to download traces

**Issue:** Config parse error
**Solution:** Validate JSON with `python -m json.tool < config.json`

## Summary

✅ All three eviction policies implemented and tested
✅ Integrated with existing Baleen simulator
✅ Configuration files ready for experiments
✅ Unit tests passing
✅ Documentation complete
✅ Ready for evaluation!

The implementation follows the assignment requirements and leverages the existing Baleen infrastructure while adding new eviction schemes that can be easily evaluated and compared.
