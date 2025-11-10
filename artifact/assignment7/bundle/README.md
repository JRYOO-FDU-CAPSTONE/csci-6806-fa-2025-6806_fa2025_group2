# Assignment 7 Bundle

This directory provides thin wrapper scripts that re-use the original
`assignments/a4` and `assignments/a5` source while giving Assignment 7 a
self-contained entry point. Each wrapper invokes the authoritative script in
the assignments directory, preserving a single source of truth.

## Structure

- `scripts/` – wrapper entry points for simulations and figure generation
- `configs/` – references or copies of any configuration files required by the wrappers
- `run_all.py` – optional helper for listing and executing wrappers
- `tests.md` – smoke-test log demonstrating wrapper execution (added later)

## Planned Wrappers

- Assignment 4 simulations
- Assignment 4 figure generators
- Assignment 5 simulations
- Assignment 5 figure generators

Each wrapper will rely on the shared helpers in `scripts/utils.py`.

