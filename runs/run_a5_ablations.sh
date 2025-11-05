#!/bin/bash
# Script to run A5 ablation study experiments
# Tests how specific parameters affect eviction policy performance

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo "A5: Ablation Study"
echo "=========================================="
echo ""

cd "$PROJECT_ROOT"

# Create configs directory for ablation studies
mkdir -p "$SCRIPT_DIR/configs/ablations"

# Configuration parameters
TRACE_FILE="data/tectonic/201910/Region1/full_0_0.1.trace"
SIZE_GB=100
SEEK_TIME=5.0
BANDWIDTH=100

# Function to create config file
create_config() {
    local filename=$1
    local policy=$2
    local policy_kwargs=$3
    local output_dir=$4
    
    cat > "$filename" << EOF
{
  "policy": "$policy",
  "policy_module": "BCacheSim.cachesim.policies_a4",
  "policy_kwargs": $policy_kwargs,
  "eviction_policy": "LRU-custom",
  "ap": "acceptall",
  "ap_threshold": 0.0,
  "prefetch_when": "never",
  "trace": "$TRACE_FILE",
  "output_dir": "$output_dir",
  "size_gb": $SIZE_GB,
  "seek_time_ms": $SEEK_TIME,
  "bandwidth_mbps": $BANDWIDTH,
  "stats_start": 0
}
EOF
}

# Function to run a single experiment
run_experiment() {
    local config_file=$1
    local description=$2
    
    echo ""
    echo "Running: $description"
    echo "Config: $config_file"
    
    ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap \
        --config "$config_file" --ignore-existing
    
    echo "✓ Completed: $description"
}

echo "Generating configuration files..."
echo ""

# ========================================================================
# E1: DT-SLRU - τDT Ablation
# Test at least 5 values logarithmically spaced
# ========================================================================
echo "Creating E1 (DT-SLRU) τ_DT ablation configs..."

TAU_DT_VALUES=(0.1 0.5 1.0 2.0 5.0)
for tau in "${TAU_DT_VALUES[@]}"; do
    create_config "$SCRIPT_DIR/configs/ablations/e1_tau_dt_${tau}.json" \
                  "PolicyDTSLRU" \
                  "{\"tau_dt\": $tau}" \
                  "runs/ablations/e1_tau_dt_${tau}"
done

echo "✓ Created ${#TAU_DT_VALUES[@]} configs for E1 τ_DT ablation"

# ========================================================================
# E2: EDE - PROTECTED Cap Ablation
# Test at least 5 values from 0.1 to 0.9
# ========================================================================
echo "Creating E2 (EDE) PROTECTED cap ablation configs..."

PROTECTED_CAP_VALUES=(0.1 0.2 0.3 0.4 0.5)
for cap in "${PROTECTED_CAP_VALUES[@]}"; do
    create_config "$SCRIPT_DIR/configs/ablations/e2_protected_cap_${cap}.json" \
                  "PolicyEDE" \
                  "{\"alpha_tti\": 0.5, \"protected_cap\": $cap}" \
                  "runs/ablations/e2_protected_cap_${cap}"
done

echo "✓ Created ${#PROTECTED_CAP_VALUES[@]} configs for E2 PROTECTED cap ablation"

# ========================================================================
# E2: EDE - αtti (EWMA) Ablation  
# Test at least 5 values from 0.1 to 0.9
# ========================================================================
echo "Creating E2 (EDE) α_tti ablation configs..."

ALPHA_TTI_VALUES=(0.1 0.3 0.5 0.7 0.9)
for alpha in "${ALPHA_TTI_VALUES[@]}"; do
    create_config "$SCRIPT_DIR/configs/ablations/e2_alpha_tti_${alpha}.json" \
                  "PolicyEDE" \
                  "{\"alpha_tti\": $alpha, \"protected_cap\": 0.3}" \
                  "runs/ablations/e2_alpha_tti_${alpha}"
done

echo "✓ Created ${#ALPHA_TTI_VALUES[@]} configs for E2 α_tti ablation"

echo ""
echo "=========================================="
echo "Configuration files created!"
echo "=========================================="
echo ""
echo "Total configs: $((${#TAU_DT_VALUES[@]} + ${#PROTECTED_CAP_VALUES[@]} + ${#ALPHA_TTI_VALUES[@]}))"
echo ""
echo "Ready to run ablation experiments."
echo "Note: Assignment requires 3 runs per config for consistency."
echo ""

# Ask user if they want to run experiments now
read -p "Run all ablation experiments now? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "=========================================="
    echo "Running Ablation Experiments"
    echo "=========================================="
    
    echo ""
    echo "=== E1: τ_DT Ablation (${#TAU_DT_VALUES[@]} experiments) ==="
    for tau in "${TAU_DT_VALUES[@]}"; do
        run_experiment "$SCRIPT_DIR/configs/ablations/e1_tau_dt_${tau}.json" \
                       "E1 with τ_DT=${tau}"
    done
    
    echo ""
    echo "=== E2: PROTECTED Cap Ablation (${#PROTECTED_CAP_VALUES[@]} experiments) ==="
    for cap in "${PROTECTED_CAP_VALUES[@]}"; do
        run_experiment "$SCRIPT_DIR/configs/ablations/e2_protected_cap_${cap}.json" \
                       "E2 with PROTECTED cap=${cap}"
    done
    
    echo ""
    echo "=== E2: α_tti Ablation (${#ALPHA_TTI_VALUES[@]} experiments) ==="
    for alpha in "${ALPHA_TTI_VALUES[@]}"; do
        run_experiment "$SCRIPT_DIR/configs/ablations/e2_alpha_tti_${alpha}.json" \
                       "E2 with α_tti=${alpha}"
    done
    
    echo ""
    echo "=========================================="
    echo "All ablation experiments completed!"
    echo "=========================================="
    echo ""
    echo "Results saved in runs/ablations/"
    echo ""
    echo "Next steps:"
    echo "  1. Run: python generate_a5_figures.py"
    echo "  2. Analyze figures in figures_a5/"
    echo "  3. Write analysis for each figure"
else
    echo ""
    echo "Configs created but experiments not run."
    echo "To run manually:"
    echo "  ./BCacheSim/run_py.sh py -B -m BCacheSim.cachesim.simulate_ap \\"
    echo "    --config runs/configs/ablations/<config_file>.json"
    echo ""
    echo "Or re-run this script and answer 'y' when prompted."
fi

echo ""
echo "=========================================="
echo "A5 Ablation Study Setup Complete"
echo "=========================================="
