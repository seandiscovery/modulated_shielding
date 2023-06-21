# One-dimensional plotter for TOPAS outputs
# Plots radiation dose along the line y = x assuming cubic binning
# Author: Sean Mullane

import numpy as np 
import matplotlib.pyplot as plt 

volume = np.genfromtxt("../Outputs/SMART_6channel_allBlocked_W_fine_201bins.csv", delimiter=",")

# Bins from TOPAS config file
# This script assume cubic bins i.e. XBins = YBins = ZBins
XBins = 201
YBins = 201
ZBins = 201
dose_grid_half = 2.505 # units = cm

z_slice = 100 # select z plane between 0 and (ZBins - 1)

# Extract (x, y, E) points along chosen z plane
xy_plane = np.empty([XBins*YBins, 3])
j = 0
# Note: may be able to make this simpler using Boolean indexing
for i in range(np.shape(volume)[0]):
	if volume[i,2] == z_slice:
		xy_plane[j] = np.array([volume[i,0], volume[i,1], volume[i,3]])
		j += 1

# Extract energy values along line y = x
mask = (xy_plane[:,0]==xy_plane[:,1])
linear_energy = xy_plane[mask]

# Convert (x, y) voxels to distance
lattice = dose_grid_half*2/XBins
unit = np.sqrt(2*lattice*lattice)

# linspace better than arange - see https://numpy.org/doc/stable/reference/generated/numpy.arange.html
distance = np.linspace(-((XBins - 1)/2)*unit, ((XBins - 1)/2)*unit, XBins)

# Current problem: how to extract distance and energy values corresponding to region 3 mm --> 8 mm from center of applicator?
# Should be able to use Boolean indexing on distance array, but haven't figured out how to do this yet
# Once we have values for distance array, how do we extract appropriate energies from linear_energy array?

# Plot values
fig, ax = plt.subplots()
ax.plot(distance, linear_energy[:,2])
plt.show()