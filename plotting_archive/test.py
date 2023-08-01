import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import ticker
from math import pi
from decimal import Decimal
from plotting_functions import *

file = "../Outputs_0724/bin_0.5mm_hist_10e7.csv"
z_slice = 51
norm_point = (0.3, 0.0)
bins = 101
dose_grid_half = 2.55
lattice = dose_grid_half*2/bins
source_transZ = -0.5
source_plane = cm_to_voxel(np.array(source_transZ), bins, dose_grid_half*2/bins)

volume = np.genfromtxt(file, delimiter=",")
plane = volume[volume[:,2] == z_slice]
plane = np.delete(plane, 2, 1)

## Test #1: scaling energy to dose before processing ##
#eng_test_theta, eng_test_r = energy_along_theta(file, pi, (101, 101), 2.55, source_plane, scale=True, norm_point=norm_point)

#X, Y1, Y2, Y3, Yerr = plotter_1D(eng_test_theta)

X, Y, energy, std_dev = contour_energy(file, (101, 101), 2.55, source_plane, 2, (-1.0, 1.0), (-1.0, 1.0), 
	source_rad=0.03, scale=True, norm_point=norm_point, zero_source=False, std_dev=False)

fig, ax = plt.subplots()

contour = ax.contourf(X, Y, energy, locator=ticker.LinearLocator(), norm="linear", cmap="rainbow")
cbar = fig.colorbar(contour)

## Test #2: defining normalization manually ##
# Source: https://matplotlib.org/stable/tutorials/colors/colormapnorms.html
"""
norm_energy = norm_energy_test(plane, norm_point, 101, lattice)

def _forward(x, norm_energy=norm_energy):
	return (x/norm_energy)*100

def _inverse(y, norm_energy=norm_energy):
	return (y/100)*norm_energy

norm = colors.FuncNorm((_forward, _inverse), vmin=0, vmax=500, clip=True)
test = ax.pcolormesh(X, Y, energy, norm=norm, cmap="rainbow")
#test = ax.contourf(X, Y, energy, norm=norm, cmap="rainbow")

cbar = fig.colorbar(test)
"""
plt.show()


