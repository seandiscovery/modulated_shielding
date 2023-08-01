import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from plotting_functions import *

# Import volume scorer file - comma delimited
#volume = np.genfromtxt("../Outputs/1e7_test.csv", delimiter=",")
volume = np.genfromtxt("../Outputs/1e7_test.csv", delimiter=",")

# Set dose grid parameters
XBins = 51
YBins = 51
ZBins = 51
dose_grid_half = 1.25 #2.55 #2.505 # units = cm

# Compute lattice length
latticeX = dose_grid_half*2/XBins
latticeY = dose_grid_half*2/YBins
latticeZ = dose_grid_half*2/ZBins

# Compute plane of source
source_transZ = -0.5 # cm
source_plane = cm_to_voxel(source_transZ, ZBins, latticeZ)
#source_plane = int(ZBins/2) + int(source_transZ/latticeZ)

# Define slice to be plotted
#const_plane = 25 # select constant plane between 0 and (X/Y/ZBins - 1)
const_plane = source_plane # alternatively, select plane of source
const_axis = 2 # 0 = x, 1 = y, 2 = z --> must be set to "2" if plotting plane of source

radius = 0.3 # radius of applicator (cm)
channel_rad = 0.08 # radius of source channel (cm)

# What are the correct coordinates for the source in plotting coordinate system?
source_loc = (0, 0) # (x, y) coordinates of source (cm)

# Define plane to be plotted - e.g. (YBins, ZBins) for x-axis = constant
plane_tuple = (XBins, YBins)

# Set range to plot (units = cm)
# Assumes origin at center of applicator
x0 = -0.6
x1 = 0.6

y0 = -0.6
y1 = 0.6

z0 = -2.5
z1 = 2.5

plane = volume[volume[:,const_axis] == const_plane]
plane = np.delete(plane, const_axis, 1)

# Set and extract normalization point (cm)
norm_point = (0, 0.4)
x_norm = cm_to_voxel(norm_point[0], XBins, latticeX)
y_norm = cm_to_voxel(norm_point[1], YBins, latticeY)
norm_mask = (plane[:,0] == x_norm) & (plane[:,1] == y_norm)

energy_norm = (plane[norm_mask])[0,2]

# Scale energy values inside applicator by 1/energy_norm
zeroing_radius = 0.03 # cm
cm_plane_test = voxel_to_cm(plane, XBins, latticeX)

plane_polar = cart_to_polar(cm_plane_test)

polar_mask = plane_polar[:,0] <= radius #zeroing_radius
#plane[:,2][polar_mask] *= 0 # another potential option - use logarithmic normalization so all energy levels are visible?
# logarithmic normalization works well - reveals details outside of source

# Voxel --> distance conversion - shift origin via XBins/2 and scale via lattice length
X = voxel_to_cm(np.arange(0,XBins), XBins, latticeX)
Y = voxel_to_cm(np.arange(0,YBins), YBins, latticeY)
Z = voxel_to_cm(np.arange(0,ZBins), ZBins, latticeZ)

# Select values in desired range
mask_X = (X > x0) & (X < x1)
mask_Y = (Y > y0) & (Y < y1)
mask_Z = (Z > z0) & (Z < z1)

height_values = np.transpose(np.reshape(plane[:,2], plane_tuple))[mask_Y][:,mask_X] # should the matrix be transposed here?
#std_dev_values = np.transpose(np.reshape(plane[:,3], plane_tuple)) # extract standard deviation values, if included in output

fig, ax = plt.subplots()

ax.contour(X[mask_X], Y[mask_Y], height_values, norm=colors.LogNorm(), cmap="rainbow") # plotting (x,y) plane with log normalization
#ax.contourf(X[mask_X], Y[mask_Y], height_values, cmap="rainbow") # plotting (x,y) plane without log normalization
#ax.contourf(Y[mask_Y], Z[mask_Z], height_values[mask_Z][:,mask_Y], cmap="rainbow") # plotting (y,z) plane
#ax.contourf(X[mask_X], Z[mask_Z], height_values[mask_Z][:,mask_X], cmap="rainbow") # plotting (x,z) plane

# Optionally draw edge of applicator on plot
# Only supported for (x,y) plane
#circle = plt.Circle((0,0), radius=radius, edgecolor="red", fill=False)
#ax.add_patch(circle)

# Optionally draw source channel on plot
# Only supported for (x,y) plane
#source_channel = plt.Circle(source_loc, radius=channel_rad, edgecolor="Orange", fill=False)
#ax.add_patch(source_channel)

plt.show()
