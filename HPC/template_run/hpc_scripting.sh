#!/bin/bash

# Batch job input parameters
# See the tutorial page https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/#batch-jobs for more information

#SBATCH --job-name=TEMPLATE_position1Open_5rod_85bins ## replace w/desired job name ##
#SBATCH --time=10:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=6G
#SBATCH --mail-type=ALL
#SBATCH --array=0-999 ## update to desired number of runs - this will run 1,000 simulations ##

#SBATCH --partition scavenge ## avoids charges for HPC time ##
#SBATCH --requeue ## if this option is not used, scavenge runs may be dropped (see https://slurm.schedmd.com/preempt.html) ##

#SBATCH --output=/dev/null ## this option dumps the slurm output files ##

module purge
module load TOPAS/3.9-foss-2022b
module list

# Replaces "ARRAY_TASK_ID" string from the TOPAS input file with the env_var $SLURM_ARRAY_TASK_ID
## You should replace "TEMPLATE_hpc_position1Open_5rod_85bins.txt" with the actual name of your input file ##
sed 's/ARRAY_TASK_ID/'"${SLURM_ARRAY_TASK_ID}"'/g' TEMPLATE_hpc_position1Open_5rod_85bins.txt > input_${SLURM_ARRAY_TASK_ID}.in

topas input_${SLURM_ARRAY_TASK_ID}.in

rm input_${SLURM_ARRAY_TASK_ID}.in