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

# Location of CSV files output from TOPAS simulation
csv_loc = "results_4mmSpace_1e6/"

# Location to save .npy files generated in this script
save_location = "npy-results_4mm_1e6/"

output_csv = np.array(os.listdir(csv_loc))
for f in output_csv:
	volume = np.genfromtxt(csv_loc + f, delimiter=",")
	f = os.path.splitext(f)[0] # remove .csv file extension
	np.save(save_location + f + ".npy", volume)
	print("saved " + f)