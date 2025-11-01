# Assignment 4 Simulation Guide

## Setup

First, create all the experiment configs:

```bash
python assignment4/scripts/config/create_all_experiment_configs.py
```

This creates all the config files needed for the experiments.

## Running Simulations

You can run all simulations at once:

```bash
python assignment4/scripts/simulation/run_all_simulations.py
```

Or run them by figure:

```bash
python assignment4/scripts/simulation/run_figure_4_simulations.py
python assignment4/scripts/simulation/run_figure_5_simulations.py
python assignment4/scripts/simulation/run_figure_6_simulations.py
python assignment4/scripts/simulation/run_figure_7_simulations.py
```

Each simulation takes like 10-30 minutes, so running all of them takes a while.

## Generating Figures

After the simulations finish, run these to generate the figures:

```bash
python assignment4/scripts/figures/generate_figures_1_2_3.py
python assignment4/scripts/figures/generate_figure_4.py
python assignment4/scripts/figures/generate_figure_5.py
python assignment4/scripts/figures/generate_figure_6.py
python assignment4/scripts/figures/generate_figure_7.py
```

The figures get saved as PNG and PDF files.

## Notes

- Make sure you have the baseline experiments (e0_lru, e1_dtslru, e2_ede) already run
- Figures 1-3 use the baseline data
- The other figures need the new experiments to be run first
- If something fails, check that the config files exist and the data directory is set up correctly
