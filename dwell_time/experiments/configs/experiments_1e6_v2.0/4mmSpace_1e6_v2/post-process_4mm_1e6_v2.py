# Allows Python to find mosh_src if this file is moved
import sys
sys.path.insert(0, "../")

# Add functionality to parse folders
import os

# Import matplotlib and numpy - helpful Python libraries for scientific computing
import numpy as np
from math import pi
from decimal import Decimal

# Import all MOSH plotting functions
from mosh_src.plotting_functions import *

#### Tunable parameters ####
############################

## Choose dose points and origin ##
# Option 1: choose dosing points (via polar coordinates) along a circle in the (X, Z) plane with Y = 0 cm
#coords = np.array([(0.5, 0), (0.5, pi/4), (0.5, pi/2), (0.5, 3*pi/4), (0.5, pi), (0.5, 5*pi/4), (0.5, 6*pi/4), (0.5, 7*pi/4)])
#origin = (2, 1)

# Option 2: choose dose points uniformly distributed over a unit sphere centered at a point of your choosing
num_dose_points = 1000
origin = (2, 0, 1)

## Set dwell positions ##
# These are defined in the bash file used to run the simulations
dwell_start = -25 # mm
dwell_end = 25 # mm
spacing = 4 # mm

## Choose source dose rate ##
source_dose_rate = 5 # Gy/s - same across all output files

## Location of output files ##
# These should be .npy files, NOT csv files
output_location = "npy-results_4mm_1e6/"

## Name of dose points file ##
# This file specifies the location of the dose points and should be generated before running 
# post-processing if the dose points are not explicitly selected. Run the function generate_points_uniform_sphere
# with save=True from the file plotting_functions.py. 
dose_file = "../mosh_src/dose_point_file_12-20-2025.npy"

## Number of bins and dosing grid half length - set in TOPAS parameter file ##
bins_mosh = 100
dose_grid_half_mosh = 5 # cm

## Name for output dose rate matrix file ##
save_name = "D_4mmSpace_1e6_v2.npy"

############################

# If you specified the dosing points via polar coordinates, run this function to convert them to Cartesian coordinates
#dose_points = polar_to_cart(coords, origin)

# If you used generate_points_uniform_sphere to generate dosing points, use this function to load the file into a numpy array
dose_points = np.load(dose_file)

## Generate array of dwell positions for the source ##
dwell_pos_transZ = np.array([x for x in range(dwell_start, dwell_end + 1, spacing)])/10 # dividing by 10 to convert mm --> cm

## Extract output files ##
# Note that we sort the output file array from (lowest dwell pos) --> (highest dwell pos)
output_files = np.array(os.listdir(output_location))
indices = []
for s in output_files:
	s = os.path.splitext(s)[0] # remove .npy file extension
	c = int(s.split("_")[1]) # extract dwell position index from file name
	indices.append(c)
arg_sorted = np.argsort(np.array(indices))

sort_output = output_files[arg_sorted]

## Define additional important parameters ##
num_dwell_pos = np.shape(sort_output)[0]
num_dose_points = np.shape(dose_points)[0]

lattice_mosh = dose_grid_half_mosh*2/bins_mosh

if np.shape(dwell_pos_transZ)[0] != np.shape(sort_output)[0]:
    raise ValueError("Number of dwell position Z coordinates must match number of output files")

## Construct and save dose rate matrix ##
D = dose_rate_matrix(sort_output, dose_points, dwell_pos_transZ, source_dose_rate, bins_mosh, dose_grid_half_mosh,
	file_ext=output_location, save=True, save_name=save_name)