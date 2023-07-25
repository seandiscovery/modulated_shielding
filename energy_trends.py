from plotting_functions import *
from math import pi
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import ticker
from decimal import Decimal
"""
Plots dose from TOPAS output files in various helpful ways.
Author: Sean Mullane, July - August 2023

This file assumes a cubic dose space (i.e. same number of bins along each dimension of dosing space). 
"""

files = np.array(["../Outputs_0724/bin_0.5mm_hist_10e7.csv", "../Outputs_0724/bin_1mm_hist_10e7.csv", 
	"../Outputs_0724/bin_0.5mm_hist_10e6.csv", "../Outputs_0724/bin_1mm_hist_10e6.csv"])

angle = pi/4
radius = 0.3

num_Hx = np.array([1e7, 1e7, 1e6, 1e6])
num_bins = np.array([101, 51, 101, 51])
dose_grid_half = np.array([2.55, 2.55, 2.55, 2.55])
plot_colors = ["blue", "red", "green", "yellow", "orange"]

# Use source_transZ to plot in the z plane of the source
# Use z_slices to plot an arbitrary z plane for each file
source_transZ = np.array([-0.5, -0.5, -0.5, -0.5])
z_slices = np.array([25, 25, 25, 25])