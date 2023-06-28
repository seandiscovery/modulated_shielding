import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# Import volume scorer file - comma delimited
volume = np.genfromtxt("../Outputs/SMART_6channel_allBlocked_W_fine_201bins.csv", delimiter=",")

z_slice = 50 # select z plane between 0 and (ZBins - 1)

# Set parameters
# This script assume cubic bins i.e. XBins = YBins = ZBins
XBins = 201
YBins = 201
ZBins = 201
dose_grid_half = 1.005 # units = cm
radius = 0.3 # radius of applicator

xy_plane = volume[volume[:,2] == z_slice]
xy_plane = np.delete(xy_plane, 2, 1)

# Voxel --> distance conversion - shift origin via XBins/2 and scale via lattice length
lattice = dose_grid_half*2/XBins

xy_rescaled = (xy_plane[:,[0,1]] - int(XBins/2))*lattice
xy_plane[:,[0,1]] = xy_rescaled

# Min-max normalization on energy values
xy_plane[:,2] = (xy_plane[:,2] - np.min(xy_plane[:,2]))/(np.max(xy_plane[:,2]) - np.min(xy_plane[:,2]))

X, Y = np.meshgrid(xy_plane[:,0], xy_plane[:,1])

triang = tri.Triangulation(xy_plane[:,0], xy_plane[:,1])
interpolator = tri.LinearTriInterpolator(triang, xy_plane[:,2])

Z = interpolator(X, Y)

fig, ax = plt.subplots()
ax.countourf(X, Y, Z)

circle = plt.Circle((0,0), radius=radius, edgecolor="red", fill=False)
ax.add_patch(circle)

plt.show()