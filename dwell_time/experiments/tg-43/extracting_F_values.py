# Allows Python to find mosh_src if this notebook is moved
import sys
sys.path.insert(0, "/Users/seanmullane/Desktop/Research_2025/modulated_shielding")

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
from mosh_src.plotting_functions import *

### Converting tg-43 anisotropy function table to useful format for extrapolation ###
# Extracts tg-43 anisotropy function values without associated (r, theta) values
F_values = np.genfromtxt("tg-43_data.csv", delimiter=",", skip_header=1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18))

# Extracts anisotropy function r values, removing an extra leading 0 
F_r = np.genfromtxt("tg-43_data.csv", delimiter=",", skip_footer=39)[1:]

# Extracts anisotropy function theta values, removing an extra leading 0
F_theta = np.genfromtxt("tg-43_data.csv", delimiter=",", usecols=(0))[1:]

# Construct numpy array where each row is in the format (r, theta, F_value)
anisotropy_func = np.zeros((np.shape(F_r)[0]*np.shape(F_theta)[0], 3))

it = np.nditer(F_values, flags=['multi_index'])
row = 0
for x in it:
    index = it.multi_index
    anisotropy_func[row][0] = F_r[index[1]]
    anisotropy_func[row][1] = F_theta[index[0]]
    anisotropy_func[row][2] = x
    row += 1
np.savetxt("anisotropy_func_values.txt", anisotropy_func)