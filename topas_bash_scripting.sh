#!/bin/bash

# Automates inputs to TOPAS via the Terminal on Mac
# If using for the first time, run the command 'chmod u+rx topas_bash_scripting.sh' to make the file executable

export TOPAS_G4_DATA_DIR=/Applications/G4Data
export QT_QPA_PLATFORM_PLUGIN_PATH=/Applications/topas/Frameworks

# Don't forget to update the input file path (or move this .sh file) before running
# Guide to save stdout to file: https://askubuntu.com/questions/420981/how-do-i-save-terminal-output-to-a-file

#/Applications/topas/bin/topas SimpleDoseScorer.txt # do not save terminal output
/Applications/topas/bin/topas SimpleDoseScorer.txt | tee -a test.txt # save terminal output to test.txt

echo "############ Finished first simulation ###############" | tee -a test.txt # flag output to test.txt

# Insert as many additional TOPAS input files as necessary here, in the format:
# /Applications/topas/bin/topas my_topas_config_file.txt