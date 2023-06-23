# One-dimensional plotter for TOPAS outputs
# Plots radiation dose along various axes assuming cubic binning
# Author: Sean Mullane

import numpy as np 
import matplotlib.pyplot as plt 

volume = np.genfromtxt("../Outputs/SMART_6channel_allBlocked_W_fine_201bins.csv", delimiter=",")

# Set parameters
# This script assume cubic bins i.e. XBins = YBins = ZBins
XBins = 201
YBins = 201
ZBins = 201
dose_grid_half = 1.005 # units = cm
plot_axis = 1 # set axis to plot against
const_axis = 0 # constant axis
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
constant = 0
mask = (xy_plane[:,const_axis]==constant)

linear_energy = xy_plane[mask]

# Optionally plot a range [r1, r2]
# Units = cm
r1 = 0.3
r2 = 1.0
b1 = (linear_energy[:,plot_axis] > r1) & (linear_energy[:,plot_axis] < r2)

r3 = -1.0
r4 = -0.3
b2 = (linear_energy[:,plot_axis] > r3) & (linear_energy[:,plot_axis] < r4)

# Plot values
fig, ax = plt.subplots()
#ax.plot(linear_energy[:,plot_axis], linear_energy[:,2]) # plot entire range
#ax.plot(linear_energy[:,plot_axis][b1], linear_energy[:,2][b1]) # plot [r1, r2]
ax.plot(linear_energy[:,plot_axis][b2], linear_energy[:,2][b2]) # plot [r3, r4]
plt.savefig("../Outputs/zslice_50_range_neg0.3_neg1.0_xConst.png")
plt.show()
