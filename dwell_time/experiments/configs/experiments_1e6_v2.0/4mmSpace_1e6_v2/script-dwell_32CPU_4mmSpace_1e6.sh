#!/bin/bash     
#SBATCH --partition=day
#SBATCH --job-name=4mmSpace-32cpu-1e6
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
module load TOPAS/3.9-foss-2022b
module list

# Iterate over negative dwell positions
# Of note, this syntax only allows integer dwell positions, but we can easily change to allow iteration over non-integer positions
file="dwell_32CPU_4mmSpace_1e6.txt"
start=-25
end=25
step_size=4

for ((i=start; i<=end; i+=step_size)); do
	rand_i=$(date +%s) # generate a unique positive random seed for each TOPAS run

	# Make sure to use i (not rand_i) for the variable Ge/Source/TransZ
	sed "s|^d:Ge/Source/TransZ[[:space:]]*=.*|d:Ge/Source/TransZ=${i} mm|" "$file" > "input_${i}.txt"
	echo "saved placeholder file ${i}"

	sed 's|ARRAY_TASK_ID|'"${i}"'|g' "input_${i}.txt" > "input_temp_${i}.txt"
	sed 's|RANDOM_SEED|'"${rand_i}"'|g' "input_temp_${i}.txt" > input_${i}.in
	echo "saved input file ${i}"

	topas input_${i}.in

	rm input_${i}.txt
	rm input_temp_${i}.txt
	rm input_${i}.in

done