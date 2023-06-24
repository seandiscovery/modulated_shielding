# One-dimensional plotter for TOPAS outputs
# Plots radiation dose along various axes assuming cubic binning
# Author: Sean Mullane

import numpy as np 
import matplotlib.pyplot as plt
from math import pi

volume = np.genfromtxt("../Outputs/SMART_6channel_allBlocked_W_fine_201bins.csv", delimiter=",")

# Set parameters
# This script assume cubic bins i.e. XBins = YBins = ZBins
XBins = 201
YBins = 201
ZBins = 201
dose_grid_half = 1.005 # units = cm
plot_axis = 0 # set axis to plot against (0 = x, 1 = y)
const_axis = 1 # constant axis
theta = 0 # plot dose along an arbitrary vector
#dose_rx =  # units = Gy

z_slice = 50 # select z plane between 0 and (ZBins - 1)

# Extract (x, y, E) points along chosen z plane
xy_plane = np.empty([XBins*YBins, 3])
j = 0
# Note: may be able to make this simpler using Boolean indexing
for i in range(np.shape(volume)[0]):
	if volume[i,2] == z_slice:
		xy_plane[j] = np.array([volume[i,0], volume[i,1], volume[i,3]])
		j += 1

# Voxel --> distance conversion - shift origin via XBins/2 and scale via lattice length
lattice = dose_grid_half*2/XBins

xy_rescaled = (xy_plane[:,[0,1]] - int(XBins/2))*lattice
xy_plane[:,[0,1]] = xy_rescaled

# Scale dose delivered to % of dose prescription
#xy_plane[:,2] = (xy_plane[:,2]/dose_rx)*100

# Extract energy values along a line defined by a constant
#constant = 0
#mask = (xy_plane[:,const_axis]==constant)

# Development - extract energy values along angle theta = (0, pi/2)
# Deprecated - plotting along arbitrary angle in separate script
"""
b_x_urq = xy_plane[:,0] > 0
urq_x = xy_plane[b_x_urq]

b_y_urq = urq_x[:,1] > 0
urq = urq_x[b_y_urq]

# Set error for mask_angle
# Gives non-zero result, but highly discretized ---> another way to pick out line y/x = tan(theta)?
# Better idea - can I just convert the entire xy plane to polar coordinates at a given z slice? This may work!
err = 0.01

mask_angle = (urq[:,1]/urq[:,0] < np.arctan2(theta) + err) & (urq[:,1]/urq[:,0] < np.arctan2(theta) - err)
linear_energy = urq[mask_angle]
"""

linear_energy = xy_plane[mask]

# Optionally plot a range [r1, r2]
# Units = cm
r1 = 0.3
r2 = 1.0
b1 = (linear_energy[:,plot_axis] > r1) & (linear_energy[:,plot_axis] < r2)

r3 = -1.0
r4 = -0.3
b2 = (linear_energy[:,plot_axis] > r3) & (linear_energy[:,plot_axis] < r4)

# Optionally average -x and +x values to smooth out statistics (since system is symmetric about y-axis)
#linear_energy_avg = (linear_energy[:,2][b1] + np.flip(linear_energy[:,2][b2]))/2

# Plot values
fig, ax = plt.subplots()
ax.plot(linear_energy[:,plot_axis], linear_energy[:,2]) # plot entire range
#ax.plot(linear_energy[:,plot_axis][b1], linear_energy[:,2][b1]) # plot [r1, r2]
#ax.plot(linear_energy[:,plot_axis][b2], linear_energy[:,2][b2]) # plot [r3, r4]
#ax.plot(linear_energy[:,plot_axis][b1], linear_energy_avg) # plot averaged energy values over distance from applicator
#plt.savefig("../Outputs/zslice_50_range_0.3_1.0_yConst_avgE.png")
plt.show()
