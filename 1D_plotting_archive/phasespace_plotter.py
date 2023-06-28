import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.patches as ptc
import seaborn as sns
from scipy.interpolate import griddata

# This script assumes we are running the phase space scorer along a surface (e.g. ZMinusSurface)

# Import phase space file
phase = np.genfromtxt("/Users/seanmullane/Desktop/Research_2023/Outputs/cylinder_test_output_1.phsp")

# Extract energy deposition along the relevant axis (e.g. along z axis if we use ZMinusSurface parameter)
x_pos = phase[:,0]
y_pos = phase[:,1]
mev = phase[:,5]

energy_z = np.column_stack((x_pos, y_pos, mev))

# Min-max normalization on mev values
# Is this necessary?
mev_normal = (mev - np.min(mev))/(np.max(mev) - np.min(mev))

# Since data is semi-random, extrapolate to a grid
# Method 1: https://matplotlib.org/stable/gallery/images_contours_and_fields/irregulardatagrid.html
# Method 2: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html#scipy.interpolate.griddata

fig, ax = plt.subplots()

x_grid = np.linspace(-100, 100, num=1000)
y_grid = np.linspace(-100, 100, num=1000)
X, Y = np.meshgrid(x_pos, y_pos) # get a better plot if we meshgrid on sampled points, not a generated linspace

# Method 1: using LinearTriInterpolator

triang = tri.Triangulation(x_pos, y_pos)
interpolator = tri.LinearTriInterpolator(triang, mev_normal)

Z = interpolator(X, Y)

#ax.scatter(X, Y) # what does meshgrid on sampled points looks like?
ax.contourf(X, Y, Z)

# Method #2: scipy griddata function
"""
test_grid = griddata((x_pos, y_pos), mev, (X, Y), method = "linear")
ax.imshow(test_grid)
"""
# Method #3: matplotlib tricontour function
# This one doesn't seem to work particularly well
# ax.tricontour(x_pos, y_pos, mev_normal)

#ax.scatter(x_pos, y_pos) # optionally display scatter of voxels receiving particles

# Optional: draw end of cylinder on plot (for geometry = TsCylinder)
circle = plt.Circle((0,0), radius=50.0, edgecolor="red", fill=False)
ax.add_patch(circle)

plt.show()