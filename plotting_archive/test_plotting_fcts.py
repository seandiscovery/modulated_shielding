from plotting_functions import *
from math import pi
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import ticker

#file = "../Outputs/SMART_Applicator_6channel_output.csv"

file = "../Outputs_0724/bin_0.5mm_hist_10e7.csv"

source_transZ = -0.5
source_plane = cm_to_voxel(source_transZ, 101, 2.55*2/101)

#energy, eng_const_r = energy_along_theta(file, pi, (51, 51, 51), 1.25, source_plane, radius=0.3)

#test = average_energy(energy)

#plotting_output = plotter_1D(eng_const_r, ind_var=1, std_dev=True, num_Hx=1e7, verbose=True, plot1="../Outputs/theta_plot_test.png", plot2="../Outputs/theta_stdDev_test.png", scatter=True)

#test, __ = energy_along_theta(file, pi, (51, 51), 1.25, source_plane, radius=0.3)

X, Y, energy, std_dev = contour_energy(file, (101, 101), 2.55, source_plane, 2, (-1.0,1.0), (-1.0,1.0), source_rad=0.03, zero_source=False, std_dev=True)

fig, ax = plt.subplots()

test = ax.contourf(X, Y, std_dev, locator=ticker.LogLocator(), norm=colors.LogNorm(), cmap="rainbow")
cbar = fig.colorbar(test)

plt.show()