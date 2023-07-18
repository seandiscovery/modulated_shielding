import numpy as np 
import matplotlib.pyplot as plt

# Import volume scorer file - comma delimited
volume = np.genfromtxt("../Outputs/test.csv", delimiter=",")

num_Hx = 1e5 # number of histories in run

# Set dose grid parameters
XBins = 51
YBins = 51
ZBins = 51
dose_grid_half = 2.505 #1.005 # units = cm

# Compute lattice length
latticeX = dose_grid_half*2/XBins
latticeY = dose_grid_half*2/YBins
latticeZ = dose_grid_half*2/ZBins

# Define slice to be plotted
const_plane = 45 # select constant plane between 0 and (X/Y/ZBins - 1)
const_axis = 2 # 0 = x, 1 = y, 2 = z

# Define plane to be plotted - e.g. (YBins, ZBins) for x-axis = constant
plane_tuple = (XBins, YBins)

# Define region of interest (ROI) to compute variance
# Units = cm
roi_x0 = 0.3
roi_x1 = 0.9

roi_y0 = -0.3
roi_y1 = 0.3

#roi_z0 = 0.0
#roi_z1 = 0.0

plane = volume[volume[:,const_axis] == const_plane]
plane = np.delete(plane, const_axis, 1)

# Voxel --> distance conversion - shift origin via XBins/2 and scale via lattice length
X = (np.arange(0,XBins) - int(XBins/2))*latticeX
Y = (np.arange(0,YBins) - int(YBins/2))*latticeY
#Z = (np.arange(0,ZBins) - int(ZBins/2))*latticeZ

energy_sum = np.transpose(np.reshape(plane[:,2], plane_tuple))

# Select values in desired range
mask_X = (X > roi_x0) & (X < roi_x1)
mask_Y = (Y > roi_y0) & (Y < roi_y1)
#mask_Z = (Z > roi_z0) & (Z < roi_z1)

std_dev_values = np.transpose(np.reshape(plane[:,3], plane_tuple))
std_dev_of_sum = np.sqrt(num_Hx)*std_dev_values[mask_Y][:,mask_X]

energy_in_roi = energy_sum[mask_Y][:,mask_X]

# Add errors in quadrature
# Note: neglects covariance between adjacent voxels
roi_total_error = np.sqrt(np.sum(np.square(std_dev_of_sum)))

roi_total_dose = np.sum(energy_in_roi)

# For comparison, extract std dev from voxel at center of roi
roi_center_index_x = int(np.shape(std_dev_of_sum)[0]/2)
roi_center_index_y = int(np.shape(std_dev_of_sum)[1]/2)

std_dev_center_voxel = std_dev_of_sum[roi_center_index_x][roi_center_index_y]

print("Total dose = " + str(roi_total_dose))
print("Std dev of dose = " + str(roi_total_error))
print("Dose at center voxel of roi = " + str(energy_in_roi[roi_center_index_x][roi_center_index_y]))
print("Std dev at center voxel of roi = " + str(std_dev_center_voxel))
