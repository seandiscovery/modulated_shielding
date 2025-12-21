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

csv_loc = "2mmSpace-1e6_results/"
save_location = "2mmSpace-1e6_npy_files/"

output_csv = np.array(os.listdir(csv_loc))
output_npy = np.array(os.listdir(save_location))

for f in output_csv:
	volume = np.genfromtxt(csv_loc + f, delimiter=",")
	np.save(save_location + f + ".npy", volume)
	print("saved " + f)

#for f in output_npy:
	#volume = np.load(save_location + f)
	#print("loaded " + f)