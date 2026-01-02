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
# For initial sims, choosing dosing points along a circle in the (X, Z) plane with Y = 0 cm and center = (2, 1) cm
#coords = np.array([(0.5, 0), (0.5, pi/4), (0.5, pi/2), (0.5, 3*pi/4), (0.5, pi), (0.5, 5*pi/4), (0.5, 6*pi/4), (0.5, 7*pi/4)])
#origin = (2, 1)

# Choosing 1,000 dose points uniformly distributed over a unit sphere centered at (2, 0, 1) cm
num_dose_points = 1000
origin = (2, 0, 1)

## Set dwell positions ##
# These are defined in the bash file used to run the simulations
# 1 mm spacing from -25 cm to +25 mm
dwell_start = -25 # mm
dwell_end = 25 # mm

## Choose source dose rate ##
source_dose_rate = 5 # Gy/s - same across all output files

## Location of output files ##
#output_location = "1mmSpace-1e6_results/"
output_location = "1mmSpace-1e6_npy_files/"

## Name of dose points file ##
dose_file = "../mosh_src/dose_point_file_12-20-2025.npy"

## Number of bins and dosing grid half length - set in TOPAS parameter file ##
bins_mosh = 100
dose_grid_half_mosh = 5 # cm

## Name for output dose rate matrix file ##
save_name = "D_1mmSpace_1e6_1e3dosePoints.npy"

############################

#dose_points = polar_to_cart(coords, origin)

## Just realized an issue with this function for repeatability - need to use the same random seed 
## to avoid a different set of dosing points for each dwell position spacing. Alternatively, 
## I can generate the points and then save the resulting array (will probably be easier).
## ---> abstracting this outside the post-processing file for now
#dose_points = generate_points_uniform_sphere(num_dose_points, origin=origin)
dose_points = np.load(dose_file)
dwell_pos_transZ = np.array([x for x in range(dwell_start, dwell_end + 1)])/10 # dividing by 10 to convert mm --> cm

## Extract output files ##
# Note that output file array is sorted (lowest dwell pos) --> (highest dwell pos)
output_files = np.array(os.listdir(output_location))

indices = []
for s in output_files:
	s = os.path.splitext(s)[0] # remove file extension
	s = os.path.splitext(s)[0] ## repeated command to remove .csv for files with .csv.npy extension (will clean up later) ##
	c = int(s.split("_")[1]) # extract dwell position index from file name
	indices.append(c)
arg_sorted = np.argsort(np.array(indices))

sort_output = output_files[arg_sorted]

# Debugging
#print(sort_output)

## Define additional important parameters ##
num_dwell_pos = np.shape(sort_output)[0]
num_dose_points = np.shape(dose_points)[0]

lattice_mosh = dose_grid_half_mosh*2/bins_mosh

if np.shape(dwell_pos_transZ)[0] != np.shape(sort_output)[0]:
    raise ValueError("Number of dwell position Z coordinates must match number of output files")

## Construct and save dose rate matrix ##
D = dose_rate_matrix(sort_output, dose_points, dwell_pos_transZ, source_dose_rate, bins_mosh, dose_grid_half_mosh,
	file_ext=output_location, save=True, save_name=save_name)