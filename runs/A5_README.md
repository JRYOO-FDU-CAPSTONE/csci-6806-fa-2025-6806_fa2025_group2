# A5: Ablation Study

This assignment extends A4 by conducting fine-grained ablation experiments on the implemented eviction schemes. You will analyze how specific internal parameters affect overall performance.

## Overview

Unlike A4 which compared policies holistically, A5 isolates key design components to identify which factors contribute most to performance gains in Peak Disk-head Time (Peak DT) and related metrics.

## Ablation Dimensions

### 1. DT-SLRU (E1) - τ_DT Parameter

**Parameter:** τ_DT (promotion threshold)

**Goal:** Quantify how varying τ_DT affects Peak DT and Hit Rate

**Range:** Choose at least 5 values spaced logarithmically or evenly between low (0.1× default) and high (5× default)

**Default:** τ_DT = 1.0

**Test Values:** 0.1, 0.5, 1.0, 2.0, 5.0

### 2. Episode-Deadline Eviction (E2) - Two Ablations

#### a) PROTECTED Cap

**Parameter:** PROTECTED cap (fraction of cache for protected items)

**Goal:** Analyze trade-off between protection size and eviction agility

**Range:** Vary from 0.1 to 0.9 in increments of 0.2

**Default:** 0.3

**Test Values:** 0.1, 0.2, 0.3, 0.4, 0.5

#### b) αtti (time-to-idle EWMA)

**Parameter:** α_tti (EWMA weight for time-to-idle prediction)

**Goal:** Analyze how prediction responsiveness affects Peak DT stability

**Range:** Vary from 0.1 to 0.9

**Default:** 0.5

**Test Values:** 0.1, 0.3, 0.5, 0.7, 0.9

## Required Figures

All plots must use Python's matplotlib, include axis labels, units, legends, and descriptive captions.

### Figure 1: Peak DT vs τ_DT (DT-SLRU)
- X-axis: τ_DT values
- Y-axis: Peak DT (ms)
- Shows how promotion threshold affects peak performance

### Figure 2: Hit Rate vs τ_DT (DT-SLRU)
- X-axis: τ_DT values
- Y-axis: Hit Rate (%)
- Shows secondary metric trade-off

### Figure 3: Peak DT vs PROTECTED cap (EDE)
- X-axis: PROTECTED cap (fraction)
- Y-axis: Peak DT (ms)
- Analyzes protected capacity impact

### Figure 4: Peak DT vs αtti (EDE)
- X-axis: α_tti
- Y-axis: Peak DT (ms)
- Shows prediction responsiveness impact

### Figure 5: Combined Sensitivity Analysis
- Normalized Peak DT for all ablated parameters
- Allows visual comparison across different parameter types
- Baseline: Default values normalized to 1.0

## Running Ablation Experiments

### Quick Start

```bash
cd runs
bash run_a5_ablations.sh
```

This script will:
1. Generate all configuration files (15 total: 5 per ablation dimension)
2. Prompt you to run experiments
3. Execute all experiments if confirmed
4. Save results in `runs/ablations/`

### Manual Execution

#### 1. Generate Configs (already done by script)
```bash
bash run_a5_ablations.sh
# Press 'n' when asked to run experiments
```

#### 2. Run Individual Ablations

**E1 τ_DT Ablation:**
```bash
for tau in 0.1 0.5 1.0 2.0 5.0; do
  ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap \
    --config runs/configs/ablations/e1_tau_dt_${tau}.json
done
```

**E2 PROTECTED Cap Ablation:**
```bash
for cap in 0.1 0.2 0.3 0.4 0.5; do
  ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap \
    --config runs/configs/ablations/e2_protected_cap_${cap}.json
done
```

**E2 α_tti Ablation:**
```bash
for alpha in 0.1 0.3 0.5 0.7 0.9; do
  ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap \
    --config runs/configs/ablations/e2_alpha_tti_${alpha}.json
done
```

### Generate Figures

After running all experiments:

```bash
cd runs
python generate_a5_figures.py
```

Figures will be saved in `runs/figures_a5/`:
- `figure1_peak_dt_vs_tau_dt.png`
- `figure2_hit_rate_vs_tau_dt.png`
- `figure3_peak_dt_vs_protected_cap.png`
- `figure4_peak_dt_vs_alpha_tti.png`
- `figure5_combined_sensitivity.png`

## Analysis Requirements

For each figure, your report must include a **Figure X Analysis** paragraph with:

### Required Elements

1. **Explain the trend**: Describe the observed pattern in the data
2. **Causal mechanism**: Why does this parameter have this effect?
3. **Trade-offs**: What are the costs/benefits at different values?

### Example Analysis

**Figure 1 Analysis:**

"As τ_DT increases, fewer blocks enter the protected segment, reducing hit reuse but improving eviction agility. At low τ_DT (0.1), nearly all items with any DT are promoted, causing Protected to fill quickly and lose selectivity. At high τ_DT (5.0), only extremely high-DT items are protected, sacrificing potential hits for more aggressive eviction. The optimal value around 1.0 balances protection for truly valuable items while maintaining cache dynamism..."

## Important Notes

### Consistency Requirements

- **Each ablation must include at least 5 data points**
- **Average across 3 runs** to ensure consistency
- Use consistent logging, constants, and random seeds for reproducibility

### Metrics

- **Primary:** Peak DT (main evaluation metric)
- **Secondary:** Median DT, Hit Rate, Flash Write Traffic

### Scope & Setup

- Keep setup consistent with A4:
  - Admission policy: Admit-All (to isolate eviction)
  - Prefetch: Disabled (to isolate eviction)
  - Cache size: Fixed at 100 GB
  - Trace: Same trace slice (Region1, 0-0.1)

## Output Structure

```
runs/
├── ablations/
│   ├── e1_tau_dt_0.1/
│   ├── e1_tau_dt_0.5/
│   ├── e1_tau_dt_1.0/
│   ├── e1_tau_dt_2.0/
│   ├── e1_tau_dt_5.0/
│   ├── e2_protected_cap_0.1/
│   ├── e2_protected_cap_0.2/
│   ├── e2_protected_cap_0.3/
│   ├── e2_protected_cap_0.4/
│   ├── e2_protected_cap_0.5/
│   ├── e2_alpha_tti_0.1/
│   ├── e2_alpha_tti_0.3/
│   ├── e2_alpha_tti_0.5/
│   ├── e2_alpha_tti_0.7/
│   └── e2_alpha_tti_0.9/
├── figures_a5/
│   ├── figure1_peak_dt_vs_tau_dt.png
│   ├── figure2_hit_rate_vs_tau_dt.png
│   ├── figure3_peak_dt_vs_protected_cap.png
│   ├── figure4_peak_dt_vs_alpha_tti.png
│   └── figure5_combined_sensitivity.png
└── configs/
    └── ablations/
        ├── e1_tau_dt_*.json (5 files)
        ├── e2_protected_cap_*.json (5 files)
        └── e2_alpha_tti_*.json (5 files)
```

## Report Structure

Your A5 report should follow this structure:

### 1. Results (2 pages with figures and tables)

Present key findings with figures. Fill up the entire 2 pages.

### 2. Discussion (2 pages)

Interpret results, explain mechanisms, and compare with A4 findings. Each figure must have a Figure X Analysis paragraph.

**Required for each figure:**
- Describe the observed trend
- Explain the causal mechanism
- Discuss trade-offs

**Example structure:**
- "Figure 1 Analysis: As τ_DT increases..."
- "Figure 2 Analysis: Hit rate exhibits..."
- "Figure 3 Analysis: PROTECTED cap shows..."
- etc.

### 3. Limitations (½ page)

Discuss constraints such as:
- Parameter granularity (could test more values)
- Dataset representativeness (single trace)
- Model assumptions (seek time, bandwidth constants)

### 4. Member Contributions (≤ 1 page)

### 5. References (≤ 1 page)

Use BibTeX and cite all references in ACM format.

## Troubleshooting

### "Config file not found"
```bash
# Regenerate configs
bash run_a5_ablations.sh
# Press 'n' when prompted
```

### "Results already exist"
```bash
# Use --ignore-existing flag or remove old results
rm -rf runs/ablations/
```

### "Inconsistent results"
- Ensure same trace, random seed, and parameters
- Run multiple times and average
- Check that no other processes are interfering

## Comparison with A4

| Aspect | A4 | A5 |
|--------|----|----|
| Focus | Policy comparison | Parameter sensitivity |
| Experiments | 3 policies | 15 configurations (3 ablations × 5 values) |
| Figures | 7 (comparative) | 5 (analytical) |
| Analysis | Which policy is best? | Why does each parameter matter? |
| Depth | Holistic evaluation | Fine-grained component analysis |

## Summary

A5 dives deeper into understanding **why** policies work by isolating individual design choices:

- **E1 τ_DT**: How aggressive should promotion be?
- **E2 PROTECTED cap**: How much cache to reserve for high-value items?
- **E2 α_tti**: How responsive should predictions be to recent patterns?

By systematically varying each parameter while holding others constant, you identify which factors contribute most to Peak DT improvements.

## Quick Reference

```bash
# 1. Generate configs and run ablations
cd runs
bash run_a5_ablations.sh

# 2. Generate figures
python generate_a5_figures.py

# 3. View figures
open figures_a5/*.png

# 4. Write analysis for each figure explaining:
#    - The trend observed
#    - Why it occurs (mechanism)
#    - Trade-offs at different values
```

Good luck with your ablation study!
