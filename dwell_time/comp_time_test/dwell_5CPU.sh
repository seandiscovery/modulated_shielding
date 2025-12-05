#!/bin/bash

# Batch job input parameters
# See the tutorial page https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/#batch-jobs for more information

#SBATCH --job-name=dwell_iter_5CPU
#SBATCH --time=10:00:00
#SBATCH --cpus-per-task=5 # should match parameter i:Ts/NumberOfThreads in TOPAS parameter file
#SBATCH --nodes=1 # added specification for single node
#SBATCH --ntasks=1 # added specification for single task - note that Geant4 uses MPI standard
#SBATCH --mem-per-cpu=10G
#SBATCH --mail-type=ALL
# Removing array iteration due to for loop below // SBATCH --array=0-999

#SBATCH --partition scavenge ## avoids charges for HPC time ##
#SBATCH --requeue ## if this option is not used, scavenge runs may be dropped (see https://slurm.schedmd.com/preempt.html) ##

# Keeping output files for debugging // SBATCH --output=/dev/null ## this option dumps the slurm output files ##

module purge
module load TOPAS/3.9-foss-2022b
module list

# Iterate over dwell positions
# Of note, this syntax only allows integer dwell positions, but we can easily change to allow iteration over non-integer positions
file="hollow_dwell_it_5CPU.txt"
for i in {-1..0}; do
	neg_i=$(( -1*i )) # avoid using negative number as random seed in our TOPAS input file

	# Make sure to use i (not neg_i) for the variable Ge/Source/TransZ
	sed "s|^d:Ge/Source/TransZ[[:space:]]*=.*|d:Ge/Source/TransZ=${i} mm|" "$file" > "input_${neg_i}.txt"
	echo "saved placeholder file ${neg_i}"

	sed 's|ARRAY_TASK_ID|'"${neg_i}"'|g' "input_${neg_i}.txt" > input_${neg_i}.in
	echo "saved input file ${neg_i}"

	topas input_${neg_i}.in

	#rm input_${neg_i}.txt
	#rm input_${neg_i}.in

done