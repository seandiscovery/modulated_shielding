import numpy as np 
import matplotlib.pyplot as plt

run_Hx = np.array([1e5, 1e6, 1e7, 1e8])
input_files = np.array(["../Outputs/test.csv", "../Outputs/test_1.csv", "../Outputs/test_2.csv", "../Outputs/test_3.csv"])

## Set parameters - assumed constant between simulations ##
XBins = 51
YBins = 51
ZBins = 51
dose_grid_half = 2.505 #1.005 # units = cm

latticeX = dose_grid_half*2/XBins
latticeY = dose_grid_half*2/YBins
latticeZ = dose_grid_half*2/ZBins

const_plane = 45 # select constant plane between 0 and (X/Y/ZBins - 1)
const_axis = 2 # 0 = x, 1 = y, 2 = z

plane_tuple = (XBins, YBins)

# Define region of interest (ROI) to compute variance
# Units = cm
roi_x0 = 0.3
roi_x1 = 0.9

roi_y0 = -0.3
roi_y1 = 0.3

#roi_z0 = 0.0
#roi_z1 = 0.0

X = (np.arange(0,XBins) - int(XBins/2))*latticeX
Y = (np.arange(0,YBins) - int(YBins/2))*latticeY
#Z = (np.arange(0,ZBins) - int(ZBins/2))*latticeZ

mask_X = (X > roi_x0) & (X < roi_x1)
mask_Y = (Y > roi_y0) & (Y < roi_y1)
#mask_Z = (Z > roi_z0) & (Z < roi_z1)

doses = np.empty(np.shape(run_Hx))
std_devs = np.empty(np.shape(run_Hx))
for i in range(np.shape(run_Hx)[0]):
	volume = np.genfromtxt(input_files[i], delimiter=",")
	num_hx = run_Hx[i]

	plane = volume[volume[:,const_axis] == const_plane]
	plane = np.delete(plane, const_axis, 1)

	energy_sum = np.transpose(np.reshape(plane[:,2], plane_tuple))

	std_dev_values = np.transpose(np.reshape(plane[:,3], plane_tuple))
	std_dev_of_sum = np.sqrt(num_Hx)*std_dev_values[mask_Y][:,mask_X]

	energy_in_roi = energy_sum[mask_Y][:,mask_X]# Add errors in quadrature

	# Note: neglects covariance between adjacent voxels
	roi_total_error = np.sqrt(np.sum(np.square(std_dev_of_sum)))

	roi_total_dose = np.sum(energy_in_roi)

	doses[i] = roi_total_dose
	std_devs[i] = roi_total_error

fig, ax = plt.subplots()
ax.scatter(run_Hx, doses, color="red")
ax.scatter(run_Hx, std_devs, color="blue")

plt.show()
