"""Wrapper for Assignment 4 figures 1–3: peak DT, median DT, cache hit rate."""
from __future__ import annotations

from .utils import run_python_script


def main() -> None:
    """Invoke the original Assignment 4 figure generator for figures 1–3."""
    run_python_script("assignment4/scripts/figures/generate_figures_1_2_3.py")


if __name__ == "__main__":
    main()

