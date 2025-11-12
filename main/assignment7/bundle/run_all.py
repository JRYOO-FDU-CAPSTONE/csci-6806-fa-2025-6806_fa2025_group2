#!/usr/bin/env python3
"""Bundle helper script for listing and running Assignment 7 wrappers.

This script provides a convenient way to discover and execute wrapper scripts
for simulations and figure generation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add scripts directory to path for imports
scripts_dir = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from utils import run_python_script, get_project_root

# Define all available wrappers organized by category
WRAPPERS = {
    "config": {
        "create_a4_configs": {
            "script": "main/assignment7/bundle/configs/create_a4_configs.py",
            "description": "Generate Assignment 4 experiment configuration files",
            "category": "Configuration",
        },
        "create_a5_configs": {
            "script": "main/assignment7/bundle/configs/create_a5_configs.py",
            "description": "Generate Assignment 5 experiment configuration files",
            "category": "Configuration",
        },
    },
    "a4_sim": {
        "run_a4_all": {
            "script": "main/assignment7/bundle/scripts/run_a4_all_simulations.py",
            "description": "Run all Assignment 4 simulations",
            "category": "Assignment 4 Simulations",
        },
        "run_a4_cache_size": {
            "script": "main/assignment7/bundle/scripts/run_a4_cache_size_simulations.py",
            "description": "Run Assignment 4 cache size sensitivity simulations",
            "category": "Assignment 4 Simulations",
        },
        "run_a4_tau_dt": {
            "script": "main/assignment7/bundle/scripts/run_a4_tau_dt_simulations.py",
            "description": "Run Assignment 4 tau_DT ablation simulations",
            "category": "Assignment 4 Simulations",
        },
        "run_a4_protected_cap": {
            "script": "main/assignment7/bundle/scripts/run_a4_protected_capacity_simulations.py",
            "description": "Run Assignment 4 protected capacity simulations",
            "category": "Assignment 4 Simulations",
        },
        "run_a4_alpha_tti": {
            "script": "main/assignment7/bundle/scripts/run_a4_alpha_tti_simulations.py",
            "description": "Run Assignment 4 alpha_TTI adaptation simulations",
            "category": "Assignment 4 Simulations",
        },
    },
    "a4_fig": {
        "generate_a4_figures_1_2_3": {
            "script": "main/assignment7/bundle/scripts/generate_a4_peak_median_hit_rate_figures.py",
            "description": "Generate Assignment 4 figures 1-3 (peak DT, median DT, hit rate)",
            "category": "Assignment 4 Figures",
        },
        "generate_a4_figure_4": {
            "script": "main/assignment7/bundle/scripts/generate_a4_cache_size_sensitivity_figure.py",
            "description": "Generate Assignment 4 figure 4 (cache size sensitivity)",
            "category": "Assignment 4 Figures",
        },
        "generate_a4_figure_5": {
            "script": "main/assignment7/bundle/scripts/generate_a4_tau_dt_ablation_figure.py",
            "description": "Generate Assignment 4 figure 5 (tau_DT ablation)",
            "category": "Assignment 4 Figures",
        },
        "generate_a4_figure_6": {
            "script": "main/assignment7/bundle/scripts/generate_a4_protected_capacity_figure.py",
            "description": "Generate Assignment 4 figure 6 (protected capacity)",
            "category": "Assignment 4 Figures",
        },
        "generate_a4_figure_7": {
            "script": "main/assignment7/bundle/scripts/generate_a4_alpha_tti_adaptation_figure.py",
            "description": "Generate Assignment 4 figure 7 (alpha_TTI adaptation)",
            "category": "Assignment 4 Figures",
        },
    },
    "a5_sim": {
        "run_a5_tau_dt": {
            "script": "main/assignment7/bundle/scripts/run_a5_tau_dt_simulations.py",
            "description": "Run Assignment 5 tau_DT ablation simulations",
            "category": "Assignment 5 Simulations",
        },
        "run_a5_protected_cap": {
            "script": "main/assignment7/bundle/scripts/run_a5_protected_cap_simulations.py",
            "description": "Run Assignment 5 protected capacity simulations",
            "category": "Assignment 5 Simulations",
        },
        "run_a5_alpha_tti": {
            "script": "main/assignment7/bundle/scripts/run_a5_alpha_tti_simulations.py",
            "description": "Run Assignment 5 alpha_TTI adaptation simulations",
            "category": "Assignment 5 Simulations",
        },
    },
    "a5_fig": {
        "generate_a5_figure_1": {
            "script": "main/assignment7/bundle/scripts/generate_a5_peak_dt_tau_dt_figure.py",
            "description": "Generate Assignment 5 figure 1 (peak DT vs tau_DT)",
            "category": "Assignment 5 Figures",
        },
        "generate_a5_figure_2": {
            "script": "main/assignment7/bundle/scripts/generate_a5_hitrate_tau_dt_figure.py",
            "description": "Generate Assignment 5 figure 2 (hit rate vs tau_DT)",
            "category": "Assignment 5 Figures",
        },
        "generate_a5_figure_3": {
            "script": "main/assignment7/bundle/scripts/generate_a5_protected_cap_figure.py",
            "description": "Generate Assignment 5 figure 3 (protected capacity)",
            "category": "Assignment 5 Figures",
        },
        "generate_a5_figure_4": {
            "script": "main/assignment7/bundle/scripts/generate_a5_alpha_tti_figure.py",
            "description": "Generate Assignment 5 figure 4 (alpha_TTI)",
            "category": "Assignment 5 Figures",
        },
        "generate_a5_figure_5": {
            "script": "main/assignment7/bundle/scripts/generate_a5_combined_sensitivity_figure.py",
            "description": "Generate Assignment 5 figure 5 (combined sensitivity summary)",
            "category": "Assignment 5 Figures",
        },
    },
}


def list_wrappers(category: str | None = None) -> None:
    """List all available wrappers, optionally filtered by category."""
    print("Available Wrappers:")
    print("=" * 80)
    
    # Flatten wrappers for easier processing
    all_wrappers = {}
    for category_dict in WRAPPERS.values():
        all_wrappers.update(category_dict)
    
    # Group by category
    by_category: dict[str, list[tuple[str, dict[str, str]]]] = {}
    for name, info in all_wrappers.items():
        cat = info["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append((name, info))
    
    # Filter by category if specified
    if category:
        category_lower = category.lower()
        by_category = {
            k: v for k, v in by_category.items()
            if category_lower in k.lower()
        }
    
    # Print wrappers grouped by category
    for cat, wrappers_list in sorted(by_category.items()):
        print(f"\n{cat}:")
        print("-" * 80)
        for name, info in sorted(wrappers_list):
            print(f"  {name:40s} - {info['description']}")
    
    print("\n" + "=" * 80)
    print(f"Total: {len(all_wrappers)} wrappers available")
    print("\nUsage: python run_all.py <wrapper_name>")
    print("       python run_all.py --list [category]")


def run_wrapper(name: str) -> None:
    """Run a wrapper by name."""
    # Find the wrapper
    wrapper_info = None
    for category_dict in WRAPPERS.values():
        if name in category_dict:
            wrapper_info = category_dict[name]
            break
    
    if not wrapper_info:
        print(f"Error: Wrapper '{name}' not found.")
        print("\nAvailable wrappers:")
        list_wrappers()
        sys.exit(1)
    
    script_path = wrapper_info["script"]
    project_root = get_project_root()
    full_script_path = project_root / script_path
    
    if not full_script_path.exists():
        print(f"Error: Script not found: {full_script_path}")
        sys.exit(1)
    
    print(f"Running: {name}")
    print(f"Description: {wrapper_info['description']}")
    print(f"Script: {script_path}")
    print("=" * 80)
    
    # Run the script as a Python module to handle relative imports correctly
    # Convert path to module path: main/assignment7/bundle/scripts/script.py
    # becomes: main.assignment7.bundle.scripts.script
    import subprocess
    
    # Get relative path from project root
    rel_path = full_script_path.relative_to(project_root)
    # Convert to module path
    module_path = str(rel_path.with_suffix("")).replace("/", ".").replace("\\", ".")
    
    try:
        # Run as module from project root
        subprocess.run(
            [sys.executable, "-m", module_path],
            cwd=str(project_root),
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"\nError: Wrapper '{name}' failed with exit code {e.returncode}")
        sys.exit(e.returncode)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Assignment 7 Bundle Helper - List and run wrapper scripts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_all.py --list                    # List all wrappers
  python run_all.py --list config             # List config wrappers
  python run_all.py --list a4                 # List Assignment 4 wrappers
  python run_all.py create_a4_configs         # Run create_a4_configs wrapper
  python run_all.py generate_a4_figure_5      # Generate Assignment 4 figure 5
        """,
    )
    
    parser.add_argument(
        "wrapper",
        nargs="?",
        help="Name of wrapper to run",
    )
    
    parser.add_argument(
        "--list",
        "-l",
        metavar="CATEGORY",
        nargs="?",
        const="",
        help="List available wrappers (optionally filtered by category)",
    )
    
    args = parser.parse_args()
    
    # Change to project root
    project_root = get_project_root()
    import os
    os.chdir(project_root)
    
    if args.list is not None:
        # List mode
        category = args.list if args.list else None
        list_wrappers(category)
    elif args.wrapper:
        # Run mode
        run_wrapper(args.wrapper)
    else:
        # No arguments - show help and list all
        parser.print_help()
        print("\n")
        list_wrappers()


if __name__ == "__main__":
    main()

