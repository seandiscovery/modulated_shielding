import numpy as np 
import matplotlib.pyplot as plt

# Import volume scorer file - comma delimited
volume = np.genfromtxt("../Outputs/SMART_6channel_allBlocked_W_fine_201bins.csv", delimiter=",")

z_slice = 50 # select z plane between 0 and (ZBins - 1)

# Set parameters
XBins = 201
YBins = 201
ZBins = 201
dose_grid_half = 1.005 # units = cm
radius = 0.3 # radius of applicator (cm)

xy_plane = volume[volume[:,2] == z_slice]
xy_plane = np.delete(xy_plane, 2, 1)

# Voxel --> distance conversion - shift origin via XBins/2 and scale via lattice length
lattice = dose_grid_half*2/XBins

X = (np.arange(0,XBins) - int(XBins/2))*lattice
Y = (np.arange(0,YBins) - int(YBins/2))*lattice

Z = np.reshape(xy_plane[:,2], (XBins, YBins))

fig, ax = plt.subplots()
ax.contourf(X,Y,Z)

#circle = plt.Circle((0,0), radius=radius, edgecolor="red", fill=False)
#ax.add_patch(circle)

plt.show()