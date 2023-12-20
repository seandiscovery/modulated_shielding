#!/bin/bash

# Load TOPAS
module avail TOPAS
module load TOPAS/3.9-foss-2022b

# all TOPAS folders currently loaded on clusters
# compare to /Applications/topas/ on my local computer
cd /vast/palmer/apps/avx2/software/TOPAS/3.9-foss-2022b

export TOPAS_G4_DATA_DIR=/vast/palmer/apps/avx2/software/TOPAS/3.9-foss-2022b/G4Data
export QT_QPA_PLATFORM_PLUGIN_PATH= # can't find Frameworks folder on clusters TOPAS module - in a different place? Not necessary to run?

# Next steps -
# - figure out where Frameworks folder lives
# - get a basic TOPAS sim running on cluster w/salloc (similar to tutorial process)
# - get a few TOPAS sims running on cluster w/sbatch
# - start thinking about organizing TOPAS input files to maximize efficiency on cluster w/batch jobs
