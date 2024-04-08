#!/bin/bash

# Batch job input parameters
# See the tutorial page https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/#batch-jobs for more information

#SBATCH --job-name=topas_test_job
#SBATCH --time=10:00:00
#SBATCH --partition scavenge
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --mail-type=ALL
#SBATCH --array=0-9

# Delete slurm.out files
#SBATCH --output=/dev/null
#SBATCH --error=/dev/null

module purge
module load TOPAS/3.9-foss-2022b
module list

# Replaces "ARRAY_TASK_ID" string from the hpc_test_position1Open_5rod_85bins.txt template file with the env_var $SLURM_ARRAY_TASK_ID
sed 's/ARRAY_TASK_ID/'"${SLURM_ARRAY_TASK_ID}"'/g' hpc_test_position1Open_5rod_85bins_FIVE.txt > input_${SLURM_ARRAY_TASK_ID}.in

topas input_${SLURM_ARRAY_TASK_ID}.in

rm input_${SLURM_ARRAY_TASK_ID}.in

# This line removes the slurm.out files for large batch jobs with O(1e3) output files
#rm slurm-${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out
#rm slurm-${SLURM_ARRAY_JOB_ID}.out