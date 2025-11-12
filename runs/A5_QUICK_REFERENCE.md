# A5 Quick Reference

## What is A5?

A5 is an **Ablation Study** that extends A4 by analyzing how specific parameters affect eviction policy performance. Instead of comparing policies holistically, A5 isolates individual design components.

## Key Differences from A4

| Aspect | A4 | A5 |
|--------|----|----|
| **Goal** | Compare 3 policies | Analyze parameter sensitivity |
| **Experiments** | 3 configs | 15 configs (3 ablations × 5 values each) |
| **Figures** | 7 comparative | 5 analytical |
| **Focus** | Which is best? | Why does each parameter matter? |

## Ablation Parameters

### E1: DT-SLRU
- **τ_DT** (promotion threshold): 0.1, 0.5, 1.0, 2.0, 5.0
  - Controls when items promote from Probation to Protected

### E2: EDE
- **PROTECTED cap** (protected fraction): 0.1, 0.2, 0.3, 0.4, 0.5
  - Fraction of cache reserved for high-DT items
- **α_tti** (EWMA weight): 0.1, 0.3, 0.5, 0.7, 0.9
  - How quickly predictions adapt to recent patterns

## Quick Commands

### Generate All Configs
```bash
cd runs
bash run_a5_ablations.sh
# Press 'n' to just create configs without running
```

### Run All Ablations
```bash
cd runs  
bash run_a5_ablations.sh
# Press 'y' to run all experiments
```

### Generate Figures
```bash
cd runs
python generate_a5_figures.py
```

### View Figures
```bash
open runs/figures_a5/*.png
```

## Required Figures

1. **Figure 1**: Peak DT vs τ_DT (E1)
2. **Figure 2**: Hit Rate vs τ_DT (E1)
3. **Figure 3**: Peak DT vs PROTECTED cap (E2)
4. **Figure 4**: Peak DT vs α_tti (E2)
5. **Figure 5**: Combined sensitivity (normalized)

## File Locations

### Configs
```
runs/configs/ablations/
├── e1_tau_dt_0.1.json
├── e1_tau_dt_0.5.json
├── e1_tau_dt_1.0.json (default)
├── e1_tau_dt_2.0.json
├── e1_tau_dt_5.0.json
├── e2_protected_cap_0.1.json
├── e2_protected_cap_0.2.json
├── e2_protected_cap_0.3.json (default)
├── e2_protected_cap_0.4.json
├── e2_protected_cap_0.5.json
├── e2_alpha_tti_0.1.json
├── e2_alpha_tti_0.3.json
├── e2_alpha_tti_0.5.json (default)
├── e2_alpha_tti_0.7.json
└── e2_alpha_tti_0.9.json
```

### Results
```
runs/ablations/
├── e1_tau_dt_0.1/
├── e1_tau_dt_0.5/
...
└── e2_alpha_tti_0.9/
```

### Figures
```
runs/figures_a5/
├── figure1_peak_dt_vs_tau_dt.png
├── figure2_hit_rate_vs_tau_dt.png
├── figure3_peak_dt_vs_protected_cap.png
├── figure4_peak_dt_vs_alpha_tti.png
└── figure5_combined_sensitivity.png
```

## Analysis Requirements

For **each figure**, write a paragraph with:

1. **Trend**: What pattern do you observe?
2. **Mechanism**: Why does this happen?
3. **Trade-offs**: What are the costs/benefits?

### Example

**Figure 1 Analysis:**

"As τ_DT increases, fewer items enter the Protected segment, reducing hit reuse but improving eviction agility. At low τ_DT (0.1), nearly all items are promoted, causing Protected to fill and lose selectivity. At high τ_DT (5.0), only extremely high-DT items are protected, sacrificing hits for aggressive eviction. The optimal value around 1.0 balances protection for valuable items while maintaining cache dynamism..."

## Running Individual Ablations

### E1: τ_DT Ablation
```bash
for tau in 0.1 0.5 1.0 2.0 5.0; do
  ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap \
    --config runs/configs/ablations/e1_tau_dt_${tau}.json
done
```

### E2: PROTECTED Cap
```bash
for cap in 0.1 0.2 0.3 0.4 0.5; do
  ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap \
    --config runs/configs/ablations/e2_protected_cap_${cap}.json
done
```

### E2: α_tti
```bash
for alpha in 0.1 0.3 0.5 0.7 0.9; do
  ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap \
    --config runs/configs/ablations/e2_alpha_tti_${alpha}.json
done
```

## Status Checklist

- [x] Eviction policies implemented (from A4)
- [x] Configuration files generator created
- [x] Ablation runner script created
- [x] Figure generation script created
- [x] A5-specific documentation created
- [ ] Run all 15 ablation experiments
- [ ] Generate figures with real data
- [ ] Write analysis for each figure

## Important Notes

### Consistency
- Run each config **3 times** and average results
- Use same trace, cache size, and parameters
- Use consistent random seeds

### Data Points
- Minimum **5 values per parameter**
- Values should be spaced appropriately (logarithmic or linear)
- Cover reasonable range (not just around default)

### Metrics
- **Primary**: Peak DT
- **Secondary**: Median DT, Hit Rate, Flash Write Traffic

## Workflow

```bash
# 1. Setup (if not done)
cd /Users/mishuthescarecrow/Baleen-FAST24

# 2. Generate configs and run ablations
cd runs
bash run_a5_ablations.sh
# Answer 'y' to run experiments

# 3. Generate figures
python generate_a5_figures.py

# 4. View figures
open figures_a5/*.png

# 5. Write analysis
# - One paragraph per figure
# - Explain trend, mechanism, trade-offs
# - Compare with A4 findings if relevant
```

## Troubleshooting

**"Configs not found"**
```bash
bash run_a5_ablations.sh  # Regenerate
```

**"Results already exist"**
```bash
rm -rf runs/ablations/  # Clear old results
```

**"Figures use synthetic data"**
- This is expected before running experiments
- Run ablations first, then regenerate figures

## Summary

A5 answers: **Why do these policies work?**

- E1 τ_DT: How aggressive should promotion be?
- E2 PROTECTED cap: How much to reserve for valuable items?
- E2 α_tti: How responsive should predictions be?

By varying one parameter at a time, you identify which design choices matter most for Peak DT performance.
