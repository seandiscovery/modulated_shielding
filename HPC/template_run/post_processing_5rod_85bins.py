# Allows Python to find mosh_src if this file is moved
import sys
sys.path.insert(0, "../modulated_shielding/mosh_src") ## TEMPLATE - update this string to point to plotting_functions ##

# Add functionality to parse folders
import os

# Import matplotlib and numpy - helpful Python libraries for scientific computing
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as patches
from matplotlib import ticker
from math import pi
from decimal import Decimal

# Import all MOSH plotting functions
#from mosh_src.plotting_functions import *
from plotting_functions import *

############

## TEMPLATE - all of the parameters in this section should be updated ##

# Specify folder with output files and name of combined file here
top_folder = "../TEMPLATE_output_files"
combined_file_name = "TEMPLATE_1e9_position1Open_85_2.125_output.csv"

# Number of bins and dosing grid half-length - both set in TOPAS parameter files
bins_mosh = 85
dose_grid_half_mosh = 2.125 # cm

# Z coordinate of radioactive source - set in TOPAS parameter files
source_transZ_mosh = -0.5 # cm

# Applicator radius - set in TOPAS parameter files
applicator_rad = 0.3

# Computes the lattice length for the simulation space in cm
lattice_mosh = dose_grid_half_mosh*2/bins_mosh

# Assume dose point in center of ROI
dose_point = (0.0, 0.5)

source_rad = [0.03, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] # cm

# 0 = x, 1 = y, 2 = z
const_axis = 2

# Set the range of our contour plots
# Maximum range set by TOPAS parameter files
rngX = (-1.5, 1.5)
rngY = (-1.5, 1.5)

dose = 100 # % of dose
# Compute the plane of the source
source_plane = cm_to_voxel(np.array(source_transZ_mosh), bins_mosh, lattice_mosh)

############

# Generate list of output files
for dirpath, __, filenames in os.walk(top_folder):
    output_files = [dirpath + "/" + x for x in filenames]

############

# Combine the output files into a single file
total_energy = combine_files(output_files, save_file=True, file_name=combined_file_name)

#### DANGER ZONE - delete original output files ####

def DELETE_FILES(top_folder, safety=False):
    """
    Deletes all files and subdirectories starting from top_folder.
    Use with extreme caution; will delete all files on your computer if top_folder = "/".
    Will raise a ValueError if the parameter "safety" is not set to True as a safety guard against accidental use.
    """
    if safety:
        for dirpath, subdirs, filenames in os.walk(top_folder, topdown=False):
            for file in filenames:
                os.remove(os.path.join(dirpath, file))
            for sub in subdirs:
                os.rmdir(os.path.join(dirpath, sub))
        os.rmdir(top_folder)
        return True
    else:
        raise ValueError("You have not set safety=True. Verify that the parameter top_folder points to the correct location before using this function.")

# Use this function with EXTREME CAUTION. It will delete the directory top_folder once you have combined all the output files.
# Do not use this function until you are sure that you do not need the original 1e3 output files. 
# We recommend testing the file created by the function combine_files above to verify that data was stored correctly.
# In addition, you should double check that top_folder is the correct directory to delete before running.
# For example, if you run this function with top_folder = "/", it will delete ALL FILES ON YOUR COMPUTER.
###########################
safety=False # only set to True once you have double-checked that top_folder is correct
#DELETE_FILES(top_folder, safety=safety)
###########################