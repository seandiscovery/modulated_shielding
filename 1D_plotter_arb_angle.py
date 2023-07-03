# One-dimensional plotter for TOPAS outputs - arbitrary angle
# Note that input angles must be in the half-open interval (0, pi]
# Author: Sean Mullane

import numpy as np 
import matplotlib.pyplot as plt
from math import pi

volume = np.genfromtxt("../Outputs/SMART_6channel_allBlocked_W_fine_201bins.csv", delimiter=",")

# Define vector to plot - inputs must be in half-open interval (0, pi]
theta = pi/2

# Set parameters
# This script assume cubic bins i.e. XBins = YBins = ZBins
XBins = 201
YBins = 201
ZBins = 201
dose_grid_half = 1.005 # units = cm
plot_axis = 0 # set axis to plot against (0 = r, 1 = theta)
const_axis = 1 # constant axis
err = 0.001 # set error for plotting along theta

z_slice = 50 # select z plane between 0 and (ZBins - 1)

xy_plane = volume[volume[:,2] == z_slice]
xy_plane = np.delete(xy_plane, 2, 1)

# Voxel --> distance conversion - shift origin via XBins/2 and scale via lattice length
lattice = dose_grid_half*2/XBins

xy_rescaled = (xy_plane[:,[0,1]] - int(XBins/2))*lattice
xy_plane[:,[0,1]] = xy_rescaled

# Transform Cartesian to polar coordinates
xy_polar = np.empty(np.shape(xy_plane))
xy_polar[:,0] = np.sqrt(xy_plane[:,0]**2 + xy_plane[:,1]**2) # (x, y) --> r
xy_polar[:,1] = np.arctan2(xy_plane[:,1], xy_plane[:,0]) # (x, y) --> theta
xy_polar[:,2] = xy_plane[:,2] # energy

# Extract (r, theta, E) values along line defined by theta
mask_theta = (xy_polar[:,const_axis] < theta + err) & (xy_polar[:,const_axis] > theta - err) # assumes theta = constant 
mask_pi = (xy_polar[:,const_axis] < (theta - pi) + err) & (xy_polar[:,const_axis] > (theta - pi) - err)

linear_energy = xy_polar[(mask_theta + mask_pi)]

# Multiply values along (theta + pi) by -1 for easier plotting
mask_invert = (linear_energy[:,const_axis] < (theta - pi) + err) & (linear_energy[:,const_axis] > (theta - pi) - err)
linear_energy[:,0][mask_invert] *= -1

# Optionally plot a range (r1, r2)
# Units = cm
r1 = 0.3
r2 = 1.0
b1 = (linear_energy[:,plot_axis] > r1) & (linear_energy[:,plot_axis] < r2)

fix, ax = plt.subplots()
ax.scatter(linear_energy[:,plot_axis], linear_energy[:,2]) # plot entire range
#ax.plot(linear_energy[:,plot_axis][b1], linear_energy[:,2][b1]) # plot [r1, r2]
plt.show()

