import numpy as np 
import matplotlib.pyplot as plt

# Import volume scorer file - comma delimited
volume = np.genfromtxt("../Outputs/SMART_6channel_allBlocked_W_fine_201bins.csv", delimiter=",")

# Define slice to be plotted
const_plane = 100 # select constant plane between 0 and (X/Y/ZBins - 1)
const_axis = 1 # 0 = x, 1 = y, 2 = z

# Set dose grid parameters
XBins = 201
YBins = 201
ZBins = 201
dose_grid_half = 1.005 # units = cm
radius = 0.3 # radius of applicator (cm)

# Define plane to be plotted - e.g. (YBins, ZBins) for x-axis = constant
plane_tuple = (XBins,ZBins)

# Set range to plot (units = cm)
# Assumes origin at center of applicator
x0 = -1.0
x1 = 0.0

#y0 = -1.0
#y1 = 0.0

z0 = -1.0
z1 = 1.0

plane = volume[volume[:,const_axis] == const_plane]
plane = np.delete(plane, const_axis, 1)

# Voxel --> distance conversion - shift origin via XBins/2 and scale via lattice length
latticeX = dose_grid_half*2/XBins
#latticeY = dose_grid_half*2/YBins
latticeZ = dose_grid_half*2/ZBins

X = (np.arange(0,XBins) - int(XBins/2))*latticeX
#Y = (np.arange(0,YBins) - int(YBins/2))*latticeY
Z = (np.arange(0,ZBins) - int(ZBins/2))*latticeZ

# Select values in desired range
mask_X = (X > x0) & (X < x1)
#mask_Y = (Y > y0) & (Y < y1)
mask_Z = (Z > z0) & (Z < z1)

height_values = np.reshape(plane[:,2], plane_tuple)

fig, ax = plt.subplots()

#ax.contourf(X[mask_X], Y[mask_Y], height_values[mask_Y][:,mask_X], cmap="rainbow") # plotting (x,y) plane
#ax.contourf(Y[mask_Y], Z[mask_Z], height_values[mask_Z][:,mask_Y], cmap="rainbow") # plotting (y,z) plane
ax.contourf(X[mask_X], Z[mask_Z], height_values[mask_Z][:,mask_X], cmap="rainbow") # plotting (x,z) plane

# Optionally draw edge of applicator on plot
#circle = plt.Circle((0,0), radius=radius, edgecolor="red", fill=False)
#ax.add_patch(circle)

plt.show()