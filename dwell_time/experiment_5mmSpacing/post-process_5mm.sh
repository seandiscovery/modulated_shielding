#!/bin/bash

# Batch job input parameters
# See the tutorial page https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/#batch-jobs for more information

#SBATCH --job-name=post-process
#SBATCH --time=5:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --mail-type=ALL

#SBATCH --partition scavenge 
#SBATCH --requeue

module purge
module load SciPy-bundle/2024.05-gfbf-2024a
module load matplotlib

python3 dwell_pos_post-process_5mm.py

echo "completed post processing"