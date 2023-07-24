from plotting_functions import *
from math import pi
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import ticker
from decimal import Decimal
"""
Plots standard deviation from TOPAS output files in various helpful ways.
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

### Step 1: plot std dev as function of radius or angle ###

energy_storage = []
plot_labels = []
for i in range(np.shape(files)[0]):
	source_plane = cm_to_voxel(source_transZ[i], num_bins[i], dose_grid_half[i]*2/num_bins[i])

	# If plotting an arbitrary z plane, use "z_slices[i]" as fifth argument
	# If plotting plane of source, use "source_plane" as fifth argument
	eng_at_const_theta, eng_at_const_r = energy_along_theta(files[i], angle, (num_bins[i], num_bins[i]), dose_grid_half[i], 
		source_plane, err=0.1, radius=radius)

	plot1_name = f"plot_{'%.2E' % Decimal(num_Hx[i])}_{num_bins[i]}_{dose_grid_half[i]}.png"
	plot2_name = f"std_dev_plot_{'%.2E' % Decimal(num_Hx[i])}_{num_bins[i]}_{dose_grid_half[i]}.png"

	"""
	To plot std dev as function of radius:
		- eng_to_plot = eng_at_const_theta
		- ind_var = 0
		- Adjust plot_rng as desired (entire range --> plt_rng = (0,0))

	To plot std dev as function of theta:
		- eng_to_plot = eng_at_const_r
		- ind_var = 1
		- Adjust plot_rng as desired

	To save figures of energy vs radius/theta, set save=True
	Don't forget to adjust the plot title when changing the independent variable!
	"""
	eng_to_plot = eng_at_const_r
	plot_tuple = plotter_1D(eng_to_plot, ind_var=1, plot_rng=(pi/2, pi), std_dev=True, num_Hx=num_Hx[i], 
		plot1=plot1_name, plot2=plot2_name, verbose=True, scatter=True, save=False)

	energy_storage.append(plot_tuple)
	plot_labels.append(plot2_name)

fig1, ax1 = plt.subplots()

line_handles = []
line_format = "o" # set to "o" for scatter plot
for i in range(len(energy_storage)):	
	line, = ax1.plot(energy_storage[i][0], energy_storage[i][2], line_format, color=plot_colors[i], label=plot_labels[i])
	line_handles.append(line)

ax1.legend(handles=line_handles)
ax1.set_title("Std dev vs theta, radius = 0.3 cm")

#fig1.savefig("std_dev_trend.png")

### Step 2: contour plot of standard deviation across applicator ###
x_range = (0.3, 0.8)
y_range = (-0.25, 0.25)
source_rad = 0.03

for i in range(np.shape(files)[0]):
	source_plane = cm_to_voxel(source_transZ[i], num_bins[i], dose_grid_half[i]*2/num_bins[i])

	X, Y, energy, std_dev = contour_energy(files[i], (num_bins[i], num_bins[i]), dose_grid_half[i], source_plane, 2, 
		x_range, y_range, source_rad=source_rad, zero_source=False, std_dev=True)

	fig2, ax2 = plt.subplots()

	contour = ax2.contourf(X, Y, std_dev, locator=ticker.LogLocator(), norm=colors.LogNorm(), cmap="rainbow") # log normalization
	#contour = ax2.contourf(X, Y, std_dev, locator=ticker.LinearLocator(), norm="linear", cmap="rainbow") # linear normalization
	cbar = fig2.colorbar(contour)

	ax2.set_title(plot_labels[i])
	fig2.savefig(plot_labels[i])
