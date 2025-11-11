# Assignment 7 Artifact Documentation

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
- Optional if you want to accelerate ML components; CPU-only works for all required A7 tasks

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

## Reproduction Instructions

## Validation Checklist

## Limitations

## Supporting Evidence
