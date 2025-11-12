from __future__ import annotations

import sys
from pathlib import Path

scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from utils import run_python_script


def main() -> None:
    run_python_script("assignment5/scripts/config/create_a5_experiment_configs.py")


if __name__ == "__main__":
    main()

