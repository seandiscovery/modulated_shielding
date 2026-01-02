# Dwell position iteration instructions

This folder contains functionality to (1) run multiple TOPAS simulations with the source moved to a new dwell position (along the Z-axis) with each simulation; (2) convert the TOPAS output CSV files to .npy files; and (3) generate a dose rate matrix from these output files that can be used to run a linear penalty optimization model to determine the best distribution of dwell times over dwell positions.

hollow_applicator_template.txt ---> dwell_simulation_script_template.sh ---> output csv files

npy_generation_template ---> output npy files

template_dwell_pos_post-process.py ---> dose rate matrix ---> linear penalty model

(post-process_template.sh used to run npy_generation and post processing scripts)