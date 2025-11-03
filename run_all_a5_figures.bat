@echo off
echo ============================================
echo Assignment 5: Running tau_DT Simulations
echo ============================================
python assignment5\scripts\simulation\run_fig1_tau_dt.py

echo.
echo ============================================
echo Generating Figure 1: Peak DT vs tau_DT
echo ============================================
python assignment5\scripts\figures\generate_figure_1_tau_dt.py

echo.
echo ============================================
echo Generating Figure 2: Hit Rate vs tau_DT
echo ============================================
python assignment5\scripts\figures\generate_figure_2_hitrate_tau_dt.py

echo.
echo ============================================
echo Generating Figure 5: Combined Summary
echo ============================================
python assignment5\scripts\figures\generate_figure_5_combined_summary.py

echo.
echo ============================================
echo ALL ASSIGNMENT 5 FIGURES COMPLETE!
echo ============================================
pause

