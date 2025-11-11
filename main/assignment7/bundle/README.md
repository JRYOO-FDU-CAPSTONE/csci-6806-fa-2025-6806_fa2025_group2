# Assignment 7 Bundle

This directory provides thin wrapper scripts that re-use the original
`assignment4` and `assignment5` source while giving Assignment 7 a
self-contained entry point. Each wrapper invokes the authoritative script in
the assignment directories, preserving a single source of truth.

This is the main execution hub for all simulations and figure generation.

## Structure

- `scripts/` – wrapper entry points for simulations and figure generation
- `configs/` – wrapper scripts for generating experiment configuration files (see `configs/README.md` for details)
- `run_all.py` – optional helper for listing and executing wrappers (to be added)
- `tests.md` – smoke-test log demonstrating wrapper execution (to be added)

## Implemented Wrappers

### Configuration Generation
- `configs/create_a4_configs.py` - Generate Assignment 4 experiment configs
- `configs/create_a5_configs.py` - Generate Assignment 5 experiment configs

### Assignment 4 Simulations
- `scripts/run_a4_all_simulations.py` - Run all Assignment 4 simulations
- `scripts/run_a4_cache_size_simulations.py` - Cache size sensitivity simulations
- `scripts/run_a4_tau_dt_simulations.py` - tau_DT ablation simulations
- `scripts/run_a4_protected_capacity_simulations.py` - Protected capacity simulations
- `scripts/run_a4_alpha_tti_simulations.py` - alpha_TTI adaptation simulations

### Assignment 4 Figure Generators
- `scripts/generate_a4_peak_median_hit_rate_figures.py` - Generate figures 1-3 (peak DT, median DT, hit rate)
- `scripts/generate_a4_cache_size_sensitivity_figure.py` - Generate figure 4 (cache size sensitivity)
- `scripts/generate_a4_tau_dt_ablation_figure.py` - Generate figure 5 (tau_DT ablation)
- `scripts/generate_a4_protected_capacity_figure.py` - Generate figure 6 (protected capacity)
- `scripts/generate_a4_alpha_tti_adaptation_figure.py` - Generate figure 7 (alpha_TTI adaptation)

### Assignment 5 Simulations
- `scripts/run_a5_tau_dt_simulations.py` - tau_DT ablation simulations
- `scripts/run_a5_protected_cap_simulations.py` - Protected capacity simulations
- `scripts/run_a5_alpha_tti_simulations.py` - alpha_TTI adaptation simulations

### Assignment 5 Figure Generators
- `scripts/generate_a5_peak_dt_tau_dt_figure.py` - Generate figure 1 (peak DT vs tau_DT)
- `scripts/generate_a5_hitrate_tau_dt_figure.py` - Generate figure 2 (hit rate vs tau_DT)
- `scripts/generate_a5_protected_cap_figure.py` - Generate figure 3 (protected capacity)
- `scripts/generate_a5_alpha_tti_figure.py` - Generate figure 4 (alpha_TTI)
- `scripts/generate_a5_combined_sensitivity_figure.py` - Generate figure 5 (combined sensitivity summary)

All wrappers rely on the shared helpers in `scripts/utils.py` and invoke the original scripts from `assignment4/` and `assignment5/` directories.



