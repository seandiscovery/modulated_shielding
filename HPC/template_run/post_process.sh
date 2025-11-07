#!/bin/bash

# Batch job input parameters
# See the tutorial page https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/#batch-jobs for more information

#SBATCH --job-name=TEMPLATE_post_process
#SBATCH --time=4:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=200G
#SBATCH --mail-type=ALL
#SBATCH --partition scavenge
#SBATCH --requeue

### Post-processing ###
module load miniconda
conda activate hpc_topas_test ## replace with name of your personal conda environment ##
python3 TEMPLATE_post_processing_5rod_85bins.py ## replace with name of post-processing file ##