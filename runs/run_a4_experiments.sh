#!/bin/bash
# Script to run A4 assignment experiments
# Evaluates three eviction policies: E0 (LRU), E1 (DT-SLRU), E2 (EDE)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo "A4: Eviction Policy Evaluation"
echo "=========================================="
echo ""

# Check if data exists
if [ ! -d "$PROJECT_ROOT/data/tectonic/201910" ]; then
    echo "Error: Trace data not found at $PROJECT_ROOT/data/tectonic/201910"
    echo "Please run: cd $PROJECT_ROOT/data && bash get-tectonic.sh"
    exit 1
fi

# Check if trace file exists
TRACE_FILE="$PROJECT_ROOT/data/tectonic/201910/201910_Region1_0_0.1.trace"
if [ ! -f "$TRACE_FILE" ]; then
    echo "Error: Trace file not found: $TRACE_FILE"
    echo "Available files in data/tectonic/201910:"
    ls -lh "$PROJECT_ROOT/data/tectonic/201910/" 2>/dev/null || echo "Directory not found"
    exit 1
fi

cd "$PROJECT_ROOT"

# Function to run a single experiment
run_experiment() {
    local config_name=$1
    local config_file="$SCRIPT_DIR/configs/${config_name}.json"
    
    echo ""
    echo "=========================================="
    echo "Running: $config_name"
    echo "Config: $config_file"
    echo "=========================================="
    
    if [ ! -f "$config_file" ]; then
        echo "Error: Config file not found: $config_file"
        return 1
    fi
    
    # Run the simulation
    ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap --config "$config_file"
    
    echo "Completed: $config_name"
    echo ""
}

# Run all three experiments
echo "Starting experiments..."
echo ""

run_experiment "e0_lru"
run_experiment "e1_dtslru"
run_experiment "e2_ede"

echo ""
echo "=========================================="
echo "All experiments completed!"
echo "=========================================="
echo ""
echo "Results are saved in:"
echo "  - runs/e0_lru/"
echo "  - runs/e1_dtslru/"
echo "  - runs/e2_ede/"
echo ""
echo "To compare results, you can check the *_cache_perf.txt files"
echo "or use the provided Jupyter notebooks for visualization."
