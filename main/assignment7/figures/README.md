# Figure Archive

This directory contains copies of all final figure outputs from Assignment 4 and Assignment 5. All figures are provided in both PNG and PDF formats for maximum compatibility.

## Figure Provenance

### Assignment 4 Figures

All Assignment 4 figures are generated from simulation results in `runs/a4/` and are created by scripts in `assignment4/scripts/figures/`.

#### Baseline Comparison Figures (Figures 1-3)

**Source:** `assignment4/scripts/figures/generate_figures_1_2_3.py`

- **figure_1_peak_dt.png/pdf** - Peak Disk-head Time comparison across eviction schemes (E0-LRU, E1-DT-SLRU, E2-EDE)
  - Data source: `runs/a4/e0_lru/`, `runs/a4/e1_dtslru/`, `runs/a4/e2_ede/`
  - Shows peak DT values for baseline cache configurations

- **figure_2_median_dt.png/pdf** - Median Disk-head Time comparison across eviction schemes
  - Data source: `runs/a4/e0_lru/`, `runs/a4/e1_dtslru/`, `runs/a4/e2_ede/`
  - Shows median DT values for baseline cache configurations

- **figure_3_hit_rate.png/pdf** - Cache Hit Rate comparison across eviction schemes
  - Data source: `runs/a4/e0_lru/`, `runs/a4/e1_dtslru/`, `runs/a4/e2_ede/`
  - Shows hit rate percentages for baseline cache configurations

- **assignment_4_figures_1_2_3_combined.png/pdf** - Combined figure showing all three baseline metrics
  - Combines figures 1-3 into a single multi-panel figure
  - Provides comprehensive overview of baseline performance

#### Cache Size Sensitivity (Figure 4)

**Source:** `assignment4/scripts/figures/generate_figure_4.py`

- **figure_4_cache_size.png/pdf** - Peak DT vs. Cache Size sensitivity analysis
  - Data source: `runs/a4/fig_4_cache_size_sensitivity/`
  - Compares E0-LRU and E1-DT-SLRU across cache sizes: 100, 200, 300, 500, 750, 1000 GB
  - Shows how cache size affects peak disk-head time

#### tau_DT Ablation Study (Figure 5)

**Source:** `assignment4/scripts/figures/generate_figure_5.py`

- **figure_5_tau_dt.png/pdf** - Combined tau_DT ablation study results
  - Data source: `runs/a4/fig_5_tau_dt_ablation/`
  - Analyzes E1 DT-SLRU with tau_DT values: 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0

- **figure_5a_peak_dt_vs_tau_dt.png/pdf** - Peak DT vs. tau_DT parameter
  - Shows how peak disk-head time varies with tau_DT threshold

- **figure_5b_hit_rate_vs_tau_dt.png/pdf** - Hit Rate vs. tau_DT parameter
  - Shows how cache hit rate varies with tau_DT threshold

#### Protected Capacity Ablation Study (Figure 6)

**Source:** `assignment4/scripts/figures/generate_figure_6.py`

- **figure_6_protected_cap.png/pdf** - Combined protected capacity ablation study results
  - Data source: `runs/a4/fig_6_protected_cap_ablation/`
  - Analyzes E2 EDE with protected capacity values: 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8

- **figure_6a_peak_dt_vs_protected_cap.png/pdf** - Peak DT vs. Protected Capacity
  - Shows how peak disk-head time varies with protected capacity parameter

- **figure_6b_hit_rate_utilization_vs_protected_cap.png/pdf** - Hit Rate and Utilization vs. Protected Capacity
  - Shows how cache hit rate and utilization vary with protected capacity parameter

#### alpha_TTI Adaptation Study (Figure 7)

**Source:** `assignment4/scripts/figures/generate_figure_7.py`

- **figure_7_alpha_tti.png/pdf** - Combined alpha_TTI adaptation study results
  - Data source: `runs/a4/fig_7_alpha_tti_ablation/`
  - Analyzes E2 EDE with alpha_TTI values: 0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9

- **figure_7a_peak_dt_vs_alpha_tti.png/pdf** - Peak DT vs. alpha_TTI Adaptation Rate
  - Shows how peak disk-head time varies with alpha_TTI adaptation rate

- **figure_7b_hit_rate_adaptation_vs_alpha_tti.png/pdf** - Hit Rate and Adaptation vs. alpha_TTI
  - Shows how cache hit rate and adaptation behavior vary with alpha_TTI parameter

---

### Assignment 5 Figures

All Assignment 5 figures are generated from simulation results in `runs/a5/` and aggregated results in `assignment5/results/`. Figures are created by scripts in `assignment5/scripts/figures/`.

#### tau_DT Sensitivity Analysis (Figures 1-2)

**Source:** 
- `assignment5/scripts/figures/generate_figure_1_tau_dt.py`
- `assignment5/scripts/figures/generate_figure_2_hitrate_tau_dt.py`

- **figure_1_peak_dt_tau_dt.png/pdf** - Peak DT vs. tau_DT sensitivity analysis
  - Data source: `assignment5/results/fig_1_tau_dt_results.json`
  - Analyzes E1 DT-SLRU with tau_DT values: 0.1, 0.25, 0.5, 1.0, 2.5, 5.0
  - Results averaged across 3 runs per parameter value
  - Shows normalized peak disk-head time sensitivity to tau_DT parameter

- **figure_2_hitrate_tau_dt.png/pdf** - Hit Rate vs. tau_DT sensitivity analysis
  - Data source: `assignment5/results/fig_1_tau_dt_results.json`
  - Same parameter values as Figure 1
  - Shows cache hit rate sensitivity to tau_DT parameter

#### Protected Capacity Sensitivity Analysis (Figure 3)

**Source:** `assignment5/scripts/figures/generate_figure_3_protected_cap.py`

- **figure_3_peak_dt_protected_cap.png/pdf** - Peak DT vs. Protected Capacity sensitivity analysis
  - Data source: `assignment5/results/fig_3_protected_cap_results.json`
  - Analyzes E2 EDE with protected capacity values: 0.1, 0.3, 0.5, 0.7, 0.9
  - Results averaged across 3 runs per parameter value
  - Shows peak disk-head time sensitivity to protected capacity parameter

#### alpha_TTI Sensitivity Analysis (Figure 4)

**Source:** `assignment5/scripts/figures/generate_figure_4_alpha_tti.py`

- **figure_4_peak_dt_alpha_tti.png/pdf** - Peak DT vs. alpha_TTI sensitivity analysis
  - Data source: `assignment5/results/fig_4_alpha_tti_results.json`
  - Analyzes E2 EDE with alpha_TTI values: 0.1, 0.3, 0.5, 0.7, 0.9
  - Results averaged across 3 runs per parameter value
  - Shows peak disk-head time sensitivity to alpha_TTI adaptation rate

#### Combined Sensitivity Summary (Figure 5)

**Source:** `assignment5/scripts/figures/generate_figure_5_combined_summary.py`

- **figure_5_combined_sensitivity_summary.png/pdf** - Combined sensitivity summary for all ablated parameters
  - Data sources: 
    - `assignment5/results/fig_1_tau_dt_results.json`
    - `assignment5/results/fig_3_protected_cap_results.json`
    - `assignment5/results/fig_4_alpha_tti_results.json`
  - Normalizes all Peak DT values to their respective baseline values
  - Normalizes parameter values to 0-1 range for comparison
  - Shows comparative sensitivity of tau_DT, PROTECTED cap, and alpha_TTI parameters
  - Provides unified view of parameter sensitivity across all ablation studies

---

## Regenerating Figures

All figures can be regenerated using the bundle wrapper scripts in `main/assignment7/bundle/scripts/`:

### Assignment 4 Figures

```bash
# Generate baseline figures (1-3)
python main/assignment7/bundle/scripts/generate_a4_peak_median_hit_rate_figures.py

# Generate cache size sensitivity figure (4)
python main/assignment7/bundle/scripts/generate_a4_cache_size_sensitivity_figure.py

# Generate tau_DT ablation figure (5)
python main/assignment7/bundle/scripts/generate_a4_tau_dt_ablation_figure.py

# Generate protected capacity figure (6)
python main/assignment7/bundle/scripts/generate_a4_protected_capacity_figure.py

# Generate alpha_TTI adaptation figure (7)
python main/assignment7/bundle/scripts/generate_a4_alpha_tti_adaptation_figure.py
```

### Assignment 5 Figures

```bash
# Generate tau_DT sensitivity figures (1-2)
python main/assignment7/bundle/scripts/generate_a5_peak_dt_tau_dt_figure.py
python main/assignment7/bundle/scripts/generate_a5_hitrate_tau_dt_figure.py

# Generate protected capacity figure (3)
python main/assignment7/bundle/scripts/generate_a5_protected_cap_figure.py

# Generate alpha_TTI figure (4)
python main/assignment7/bundle/scripts/generate_a5_alpha_tti_figure.py

# Generate combined sensitivity summary (5)
python main/assignment7/bundle/scripts/generate_a5_combined_sensitivity_figure.py
```

### Using run_all.py Helper

You can also use the bundle helper script:

```bash
# List all figure generation wrappers
python main/assignment7/bundle/run_all.py --list a4_fig
python main/assignment7/bundle/run_all.py --list a5_fig

# Run a specific figure generator
python main/assignment7/bundle/run_all.py generate_a4_figure_5
python main/assignment7/bundle/run_all.py generate_a5_figure_1
```

---

## File Statistics

- **Total Figures:** 19 unique figures (38 files including PNG and PDF)
- **Assignment 4:** 14 figures (28 files)
- **Assignment 5:** 5 figures (10 files)
- **Formats:** PNG (for preview) and PDF (for publication)

---

## Notes

- All figures are generated using matplotlib with ACM sigconf formatting
- Figures use consistent color schemes and styling across assignments
- PNG files are suitable for web viewing and quick preview
- PDF files are suitable for publication and high-quality printing
- Original figure generation scripts preserve single source of truth in `assignment4/` and `assignment5/` directories
- This archive provides a consolidated view of all figures for Assignment 7 documentation

---

## Updating This Archive

When regenerating figures:

1. Run the appropriate figure generation wrapper script
2. Copy the new figure files from `assignment4/outputs/` or `assignment5/report/figures/` to this directory
3. Update this README if figure descriptions or data sources change
4. Verify both PNG and PDF versions are updated

---

## Reference

For detailed information about figure generation and data processing, see:
- `assignment4/scripts/figures/` - Assignment 4 figure generation scripts
- `assignment5/scripts/figures/` - Assignment 5 figure generation scripts
- `main/assignment7/bundle/README.md` - Bundle wrapper documentation
- `assignment4/documentation/ASSIGNMENT_4_SIMULATION_GUIDE.md` - Assignment 4 simulation guide

