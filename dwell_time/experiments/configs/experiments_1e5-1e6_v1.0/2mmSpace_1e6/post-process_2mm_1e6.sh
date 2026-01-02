#!/bin/bash     
#SBATCH --partition=day
#SBATCH --job-name=post-process-1mm-1e6_fullPartition
#SBATCH --ntasks=1 --nodes=1
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=8G
#SBATCH --time=01-00:00:00
#SBATCH --mail-type=ALL
#################################################
# please DO NOT remove the following two commands
#################################################
module load StdEnv
export SLURM_EXPORT_ENV=ALL
#################################################

# module purge
module load SciPy-bundle/2024.05-gfbf-2024a
module load matplotlib

python3 npy_generation_2mm.py
python3 dwell_pos_post-process_2mm_1e6.py

echo "completed post processing"