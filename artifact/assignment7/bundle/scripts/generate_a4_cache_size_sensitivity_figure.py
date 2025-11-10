"""Wrapper for Assignment 4 figure 4: cache size sensitivity analysis."""
from __future__ import annotations

from .utils import run_python_script


def main() -> None:
    """Invoke the original Assignment 4 cache size figure generator."""
    run_python_script("assignment4/scripts/figures/generate_figure_4.py")


if __name__ == "__main__":
    main()

