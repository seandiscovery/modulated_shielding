# One-dimensional plotter for TOPAS outputs - arbitrary angle
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
plot_axis = 0 # set axis to plot against (0 = r, 1 = theta)
const_axis = 1 # constant axis
theta = 0 # plot dose along a vector in interval theta = [0, pi]
err = 0.01 # set error for plotting along theta

z_slice = 50 # select z plane between 0 and (ZBins - 1)

xy_plane = volume[volume[:,2] == z_slice]
xy_plane = np.delete(xy_plane, 2, 1)

# Extract (x, y, E) points along chosen z plane
"""
xy_plane = np.empty([XBins*YBins, 3])
j = 0
# Note: may be able to make this simpler using Boolean indexing
for i in range(np.shape(volume)[0]):
	if volume[i,2] == z_slice:
		xy_plane[j] = np.array([volume[i,0], volume[i,1], volume[i,3]])
		j += 1
"""

# Voxel --> distance conversion - shift origin via XBins/2 and scale via lattice length
lattice = dose_grid_half*2/XBins

xy_rescaled = (xy_plane[:,[0,1]] - int(XBins/2))*lattice
xy_plane[:,[0,1]] = xy_rescaled

# Transform Cartesian to polar coordinates
xy_polar = np.empty(np.shape(xy_plane))
xy_polar[:,0] = np.sqrt(xy_plane[:,0]**2 + xy_plane[:,1]**2) # (x, y) --> r
xy_polar[:,1] = np.arctan2(xy_plane[:,1], xy_plane[:,0]) # (x, y) --> theta
xy_polar[:,2] = xy_plane[:,2] # energy

mask1 = (xy_polar[:,const_axis] < theta + err) & (xy_polar[:,const_axis] > theta - err) # assumes theta = constant 
mask0 = (xy_polar[:,const_axis] < (theta + pi) + err) & (xy_polar[:,const_axis] > (theta + pi) - err)
mask10 = mask0 + mask1

#mask2 = (xy_polar[:,const_axis] == theta)
#mask3 = (xy_polar[:,const_axis] == theta + pi)
#mask4 = mask2 + mask3

linear_energy_1 = xy_polar[mask10]

maskA = (linear_energy_1[:,const_axis] < (theta + pi) + err) & (linear_energy_1[:,const_axis] > (theta + pi) - err)
linear_energy_1[:,0][maskA] *= -1

#print(linear_energy_1)

#linear_energy_2 = xy_polar[mask4]
#linear_energy_2[:,0][linear_energy_2[:,const_axis] == theta + pi] *= -1

#print(np.shape(linear_energy_2))
#print(linear_energy_1)

# Optionally plot a range (r1, r2)
# Units = cm
r1 = 0.3
r2 = 1.0
b1 = (linear_energy_1[:,plot_axis] > r1) & (linear_energy_1[:,plot_axis] < r2)

fix, ax = plt.subplots()
#ax.plot(linear_energy_1[:,plot_axis], linear_energy_1[:,2], color="red") # plot entire range
ax.plot(linear_energy_1[:,plot_axis][b1], linear_energy_1[:,2][b1]) # plot [r1, r2]
#ax.plot(linear_energy_2[:,plot_axis], linear_energy_2[:,2], color="blue")
plt.show()


