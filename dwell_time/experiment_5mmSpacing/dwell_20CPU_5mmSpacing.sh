#!/bin/bash

# Batch job input parameters
# See the tutorial page https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/#batch-jobs for more information

#SBATCH --job-name=dwell_iter_20CPU_5mmSpace
#SBATCH --time=10:00:00
#SBATCH --cpus-per-task=20 # should match parameter i:Ts/NumberOfThreads in TOPAS parameter file
#SBATCH --nodes=1 # added specification for single node
#SBATCH --ntasks=1 # added specification for single task - note that Geant4 uses MPI standard
#SBATCH --mem-per-cpu=3G # of note, TOTAL memory ~ 800 MB for 2 dwell positions ---> predict ~ 40 GB for 100 dwell positions
#SBATCH --mail-type=ALL

#SBATCH --partition scavenge 
#SBATCH --requeue

# Keeping output files for debugging // SBATCH --output=/dev/null ## this option dumps the slurm output files ##

module purge
module load TOPAS/3.9-foss-2022b
module list

# Iterate over negative dwell positions
# Of note, this syntax only allows integer dwell positions, but we can easily change to allow iteration over non-integer positions
file="hollow_dwell_20CPU_5mmSpacing.txt"
for ((i=-25; i<0; i+=5)); do
	neg_i=$(( -1*i )) # avoid using negative number as random seed in our TOPAS input file

	# Make sure to use i (not neg_i) for the variable Ge/Source/TransZ
	sed "s|^d:Ge/Source/TransZ[[:space:]]*=.*|d:Ge/Source/TransZ=${i} mm|" "$file" > "input_${i}.txt"
	echo "saved placeholder file ${i}"

	sed 's|ARRAY_TASK_ID|'"${i}"'|g' "input_${i}.txt" > "input_temp_${i}.txt"
	sed 's|RANDOM_SEED|'"${neg_i}"'|g' "input_temp_${i}.txt" > input_${i}.in
	echo "saved input file ${i}"

	topas input_${i}.in

	rm input_${i}.txt
	rm input_temp_${i}.txt
	rm input_${i}.in


done

# Iterate over positive dwell positions
for ((i=0; i<=25; i+=5)); do
	i_rand=$(( 10*i )) # avoid repeating random seed in TOPAS input file and overwriting input files created above

	# Make sure to use i (not i_rand) for the variable Ge/Source/TransZ
	sed "s|^d:Ge/Source/TransZ[[:space:]]*=.*|d:Ge/Source/TransZ=${i} mm|" "$file" > "input_${i}.txt"
	echo "saved placeholder file ${i}"

	sed 's|ARRAY_TASK_ID|'"${i}"'|g' "input_${i}.txt" > "input_temp_${i}.txt"
	sed 's|RANDOM_SEED|'"${i_rand}"'|g' "input_temp_${i}.txt" > input_${i}.in
	echo "saved input file ${i}"

	topas input_${i}.in

	rm input_${i}.txt
	rm input_temp_${i}.txt
	rm input_${i}.in

done