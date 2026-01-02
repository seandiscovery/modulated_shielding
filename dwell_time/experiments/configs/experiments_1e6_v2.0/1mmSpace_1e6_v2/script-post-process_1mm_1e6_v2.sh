#!/bin/bash     
#SBATCH --partition=day
#SBATCH --job-name=post-process-1mm-1e6
#SBATCH --ntasks=1 --nodes=1
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=3G
#SBATCH --time=01-00:00:00
#SBATCH --mail-type=ALL
#################################################
# please DO NOT remove the following two commands
#################################################
module load StdEnv
export SLURM_EXPORT_ENV=ALL
#################################################

### This option dumps the slurm output files - comment out to keep the output for debugging ###
# Keeping output files for debugging // SBATCH --output=/dev/null

# module purge
module load SciPy-bundle/2024.05-gfbf-2024a
module load matplotlib

# Generate .npy files from .csv output files
python3 npy_generation_1mm_v2.py
echo "completed generation of .npy files"

# Run post-processing
python3 post-process_1mm_1e6_v2.py
echo "completed post processing"