#!/bin/bash

# Automates inputs to TOPAS via the Terminal on Mac
# If using for the first time, run the command 'chmod u+rx topas_bash_scripting.sh' to make the file executable

export TOPAS_G4_DATA_DIR=/Applications/G4Data
export QT_QPA_PLATFORM_PLUGIN_PATH=/Applications/topas/Frameworks

# Don't forget to update the input file path (or move this .sh file) before running

/Applications/topas/bin/topas SimpleDoseScorer.txt

# Insert as many additional TOPAS input files as necessary here, in the format:
# /Applications/topas/bin/topas my_topas_config_file.txt