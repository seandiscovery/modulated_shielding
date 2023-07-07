import numpy as np 
import matplotlib.pyplot as plt

# Import volume scorer file - comma delimited
volume = np.genfromtxt("sean_input_files/test_2.csv", delimiter=",")

# Set dose grid parameters
XBins = 201
YBins = 201
ZBins = 201
dose_grid_half = 2.505 #1.005 # units = cm

# Compute lattice length
latticeX = dose_grid_half*2/XBins
latticeY = dose_grid_half*2/YBins
latticeZ = dose_grid_half*2/ZBins

# Compute plane of source
source_transZ = -0.5 # cm
source_plane = int(ZBins/2) + int(source_transZ/latticeZ)

# Define slice to be plotted
const_plane = 100 # select constant plane between 0 and (X/Y/ZBins - 1)
#const_plane = source_plane # alternatively, select plane of source
const_axis = 2 # 0 = x, 1 = y, 2 = z --> must be set to "2" if plotting plane of source

radius = 0.3 # radius of applicator (cm)
channel_rad = 0.08 # radius of source channel (cm)

# What are the correct coordinates for the source in plotting coordinate system?
source_loc = (0, 0.18) # (x, y) coordinates of source (cm)

# Define plane to be plotted - e.g. (YBins, ZBins) for x-axis = constant
plane_tuple = (XBins, YBins)

# Set range to plot (units = cm)
# Assumes origin at center of applicator
x0 = -2.5
x1 = 2.5

y0 = -2.5
y1 = 2.5

#z0 = -2.5
#z1 = 2.5

plane = volume[volume[:,const_axis] == const_plane]
plane = np.delete(plane, const_axis, 1)

# Voxel --> distance conversion - shift origin via XBins/2 and scale via lattice length
X = (np.arange(0,XBins) - int(XBins/2))*latticeX
Y = (np.arange(0,YBins) - int(YBins/2))*latticeY
#Z = (np.arange(0,ZBins) - int(ZBins/2))*latticeZ

# Select values in desired range
mask_X = (X > x0) & (X < x1)
mask_Y = (Y > y0) & (Y < y1)
#mask_Z = (Z > z0) & (Z < z1)

height_values = np.transpose(np.reshape(plane[:,2], plane_tuple)) # should the matrix be transposed here?

fig, ax = plt.subplots()

ax.contourf(X[mask_X], Y[mask_Y], height_values[mask_Y][:,mask_X], cmap="rainbow") # plotting (x,y) plane
#ax.contourf(Y[mask_Y], Z[mask_Z], height_values[mask_Z][:,mask_Y], cmap="rainbow") # plotting (y,z) plane
#ax.contourf(X[mask_X], Z[mask_Z], height_values[mask_Z][:,mask_X], cmap="rainbow") # plotting (x,z) plane

# Optionally draw edge of applicator on plot
# Only supported for (x,y) plane
circle = plt.Circle((0,0), radius=radius, edgecolor="red", fill=False)
ax.add_patch(circle)

# Optionally draw source channel on plot
# Only supported for (x,y) plane
source_channel = plt.Circle(source_loc, radius=channel_rad, edgecolor="Orange", fill=False)
ax.add_patch(source_channel)

plt.show()
