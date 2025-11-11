"""Shared helper utilities for Assignment 7 bundle wrapper scripts.

These helpers keep the wrappers lightweight by providing:

* A reliable way to resolve the project root (independent of CWD)
* A thin subprocess wrapper with consistent logging and error handling
* A convenience helper for invoking Python scripts relative to the project root
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Iterable, Mapping, MutableSequence, Sequence, Union

__all__ = [
    "get_project_root",
    "run_command",
    "run_python_script",
]

# Cache the resolved root so repeated calls are inexpensive.
_PROJECT_ROOT = Path(__file__).resolve().parents[3]


def get_project_root() -> Path:
    """Return the absolute path to the repository root.

    Raises:
        FileNotFoundError: If the expected root layout is not present.
    """
    expected = (_PROJECT_ROOT / "BCacheSim")
    if not expected.exists():
        raise FileNotFoundError(
            f"Expected project root at {_PROJECT_ROOT} is missing 'BCacheSim/'. "
            "Ensure the bundle is running inside the Baleen assignment repository."
        )
    return _PROJECT_ROOT


def _normalize_args(args: Sequence[Union[str, Path]]) -> MutableSequence[str]:
    normalized: MutableSequence[str] = []
    for arg in args:
        if isinstance(arg, Path):
            normalized.append(str(arg))
        else:
            normalized.append(str(arg))
    return normalized


def run_command(
    args: Sequence[Union[str, Path]],
    *,
    cwd: Union[str, Path, None] = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run a subprocess with consistent logging and error reporting."""
    command = _normalize_args(args)
    resolved_cwd = Path(cwd) if isinstance(cwd, (str, Path)) else None

    print(f"[bundle] running: {' '.join(command)}")
    if resolved_cwd:
        print(f"[bundle] cwd: {resolved_cwd}")

    try:
        return subprocess.run(
            command,
            cwd=str(resolved_cwd) if resolved_cwd else None,
            env=env,
            check=True,
            text=True,
            capture_output=capture_output,
        )
    except subprocess.CalledProcessError as exc:
        if capture_output:
            if exc.stdout:
                print("[bundle] stdout:\n" + exc.stdout)
            if exc.stderr:
                print("[bundle] stderr:\n" + exc.stderr, file=sys.stderr)
        raise


def run_python_script(
    relative_path: Union[str, Path],
    *script_args: Union[str, Path],
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Execute a Python script identified by its path relative to the repo root."""
    script_path = get_project_root() / Path(relative_path)
    if not script_path.exists():
        raise FileNotFoundError(f"Python script not found: {script_path}")

    cmd: list[Union[str, Path]] = [sys.executable, script_path]
    if script_args:
        cmd.extend(script_args)
    return run_command(
        cmd,
        cwd=script_path.parent,
        capture_output=capture_output,
    )



