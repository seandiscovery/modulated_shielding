import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import pi
from decimal import Decimal

"""
Suite of functions to process data from TOPAS simulations. 
Author: Sean Mullane, June 2023 - Novemebr 2025

Notes: 
	- This file makes heavy use of Boolean indexing to efficiently extract information from numpy arrays. 
	If unfamiliar with Boolean indexing, see: https://numpy.org/doc/stable/user/basics.indexing.html#boolean-array-indexing
	
	- All functions in this file assume Xbins = Ybins.
"""

#### Plotting helper functions ####

def generate_plane(file: str, const_plane: int, const_axis: int) -> np.ndarray:
	"""
	Extracts a two-dimensional plane from a three-dimensional TOPAS csv file.
	
	Parameters:
		- file: str - input csv file
		- const_plane: int - specifies the voxel that is held constant when extracting plane
		- const_axis: int - axis to hold constant when extracting plane (0 = x, 1 = y, 2 = z)

	Returns:
		- numpy array with columns (x, y, energy, std_dev) 
	"""
	volume = np.genfromtxt(file, delimiter=",")

	# volume has columns (x, y, z, energy, std_dev)
	plane = volume[volume[:,const_axis] == const_plane]
	plane = np.delete(plane, const_axis, 1)

	return plane

def combine_files(files: list, save_file: bool=True, file_name: str="combined_energy.csv") -> np.ndarray:
	"""
	Combines multiple output files by adding energy values assigned to each voxel.

	Parameters:
		- files: list - a list of strings specifying location of TOPAS output csv files
		- save_file: bool - flag to determine whether the combined energy tensor is saved to a 
		csv file
	
	Returns:
		- numpy array with columns (x, y, z, total_energy, total_std_dev), where total_energy is 
		the summed energy across a given voxel for n = length(files) output files and total_std_dev
		is the appropriately combined standard deviations for that voxel
	"""
	energy_storage = []
	# Extract tensors with columns (x, y, z, energy, std_dev)
	for f in files:
		energy_storage.append(np.genfromtxt(f, delimiter=","))

	combined_eng = np.zeros(np.shape(energy_storage[0]))
	combined_eng[:,0:3] = energy_storage[0][:,0:3]
	for volume in energy_storage:
		combined_eng[:,3] += volume[:,3]

	if save_file:
		np.savetxt(file_name, combined_eng, delimiter=",")

	return combined_eng

def cm_to_voxel(cm: np.ndarray, bins: int, lattice: float) -> np.ndarray:
	"""
	Converts Cartesian space to voxel space. Inverse of voxel_to_cm.

	Parameters:
		- cm: np.ndarray - numpy array specifying distances (in cm) for conversion
		- bins: int - number of bins from the simulation
		- lattice: float - lattice length of dosing grid

	Returns:
		- numpy array of voxel values
	"""
	return (int(bins/2) + (cm/lattice).round()).astype(int)

def voxel_to_cm(voxels: np.ndarray, bins: int, lattice: float) -> np.ndarray:
	"""
	Converts voxel space to Cartesian space. Inverse of cm_to_voxel.

	Parameters:
		- voxels: np.ndarray - numpy array specifying voxels for conversion
		- bins: int - number of bins from the simulation
		- lattice: float - lattice length of dosing grid

	Returns: 
		- numpy array of cm values
	"""
	return (voxels - int(bins/2))*lattice

def cart_to_polar(cart_plane: np.ndarray, origin: tuple) -> np.ndarray:
	""" 
	Transform 2D Cartesian coordinates to polar coordinates. 

	Parameters:
		- cart_plane: np.ndarray - matrix of values to convert. Assumes first two columns are Cartesian coordinates; 
		remaining columns returned unchanged.
		- origin: tuple - contains coordinates of new origin during polar transformation

	Returns:
		- numpy array; first two columns in polar coordinates, remaining columns unchanged
	"""
	num_cols = np.shape(cart_plane)[1]
	polar_plane = np.empty(np.shape(cart_plane))
	
	polar_plane[:,0] = np.sqrt((cart_plane[:,0] - origin[0])**2 + (cart_plane[:,1] - origin[1])**2) # (x, y) --> r
	polar_plane[:,1] = np.arctan2(cart_plane[:,1] - origin[1], cart_plane[:,0] - origin[0]) # (x, y) --> theta
	
	for i in range(2, num_cols):
		polar_plane[:,i] = cart_plane[:,i]

	return polar_plane

def extract_norm_energy(file: str, const_plane: int, const_axis: int, norm_point: tuple, bins: int, lattice: float) -> tuple:
	"""
	Given an input voxel, extracts the energy deposited in that voxel during the TOPAS simulation.

	Parameters:
		- file: str - input csv file
		- const_plane: int - voxel that is held constant when extracting plane
		- const_axis: int - axis to hold constant when extracting plane (0 = x, 1 = y, 2 = z)
		- norm_point: tuple - point (in cm) at which we are extracting the energy value
		- bins: int - number of bins from the simulation
		- lattice: float - lattice length of the dosing grid

	Returns:
		- Tuple specifying energy at norm_point and voxels of the point
	"""
	plane = generate_plane(file, const_plane, const_axis)

	norm_point_voxel = cm_to_voxel(np.array(norm_point), bins, lattice)
	mask = (plane[:,0] == norm_point_voxel[0]) & (plane[:,1] == norm_point_voxel[1])

	# plane has columns (x, y, energy, std_dev)
	norm_energy = plane[mask][0][2]

	return (norm_energy, norm_point_voxel)

def normalize_energy(plane: np.ndarray, norm_energy: float, dose: float) -> np.ndarray:
	"""
	Normalizes energy in each voxel to a prescription dose defined at the voxel norm_point.

	Parameters:
		- plane: np.ndarray - numpy array specifying plane for analysis, with columns (x, y, energy, std_dev)
		- norm_energy: float - energy returned from extract_norm_energy above
		- dose: float - desired prescription dose delivered to norm_point

	Returns:
		- numpy matrix with energy values scaled to prescription dose, all other values unchanged
	"""
	# Scale energy and standard deviation values
	plane[:,2:] = (plane[:,2:]/norm_energy)*dose

	return plane

#### Plotting functions ####

def energy_along_theta(file: str, theta: float, bins: tuple, dose_grid_half: float, z_slice: int, err: float=0.001, 
	radius: float=0.0, scale: bool=False, norm_energy: float=0.0, dose: float=0.0) -> tuple:
	"""
	Returns energy along an angle theta in range (0, pi]. Optionally returns energy from voxels at a distance radius from the 
	origin.

	Parameters:
		- file: str - input csv file
		- theta: float - angle along which energy values are extracted. Range = (0, pi] - use theta = pi to plot along x-axis
		- bins: tuple - number of bins from the simulation in format (bins, bins)
		- dose_grid_half: float - dosing grid half length
		- z_slice: int - value of the voxel held constant when running generate_plane; not required to be along z-axis
		- err: float - tolerance when extracting voxels that lie along an angle theta.
		- radius: float - if radius > 0, function will also extract energy from voxels at radius +/- err from the origin 
		- scale: bool - if True, normalizes extracted energy values to the dose delivered at norm_point 
		- norm_energy: float - energy extracted from norm_point. Must be nonzero if scale == True.
		- dose: float - prescription dose delivered to norm_point. Must be nonzero if scale == True.

	Returns:
		- Tuple (linear_energy, eng_at_const_r), where
			- linear_energy is a numpy array specifying energy in voxels along theta, with columns (r, theta, energy, std_dev)
			- eng_at_const_r is a numpy array specifying energy in voxels at radius +/- err, with columns (r, theta, energy, std_dev)
		- If radius == 0, eng_at_const_r is returned as None
	"""
	if theta <= 0 or theta > pi: raise ValueError("Parameter theta must be in range (0, pi] - use theta = pi to plot along x-axis")

	# plane has columns (x, y, energy, std_dev)
	plane = generate_plane(file, z_slice, 2)

	# Scale all voxels to prescription dose
	if scale:
		if (norm_energy == 0) or (dose == 0): raise ValueError("norm_energy and/or dose cannot be 0 if scaling energy values")
		plane = normalize_energy(plane, norm_energy, dose)

	# Transform voxel space ---> Cartesian space
	plane[:,0] = voxel_to_cm(plane[:,0], bins[0], dose_grid_half*2/bins[0]) # transform x
	plane[:,1] = voxel_to_cm(plane[:,1], bins[1], dose_grid_half*2/bins[1]) # transform y

	# Transform Cartesian space ---> polar space
	polar = cart_to_polar(plane)

	# Extract energy values along theta - create Boolean masks
	mask_theta = (polar[:,1] < theta + err) & (polar[:,1] > theta - err)
	mask_pi = (polar[:,1] < (theta - pi) + err) & (polar[:,1] > (theta - pi) - err)

	linear_energy = polar[(mask_theta + mask_pi)]

	# Multiply r-values along (theta - pi) by -1 for easier plotting
	mask_invert = (linear_energy[:,1] < (theta - pi) + err) & (linear_energy[:,1] > (theta - pi) - err)
	linear_energy[:,0][mask_invert] *= -1

	eng_at_const_r = None
	if radius > 0:
		# Extract energy values at constant radius - create Boolean masks
		mask_radius = (polar[:,0] < radius + err) & (polar[:,0] > radius - err)
		eng_at_const_r = polar[mask_radius]

	return (linear_energy, eng_at_const_r)

def average_energy(linear_energy: np.ndarray, std_dev: bool=False) -> np.ndarray:
	"""
	Averages energy along theta and (theta - pi) to smooth out statistical fluctuations.

	Parameters:
		- linear_energy: np.ndarray - numpy array specifying energy along theta, with columns (r, theta, energy, std_dev)
		- std_dev: bool - if True, appropriately combines standard deviation values for corresponding voxels when averaging

	Returns:
		- numpy array eng_pos_r specifying average energy along theta and (theta - pi), with columns 
		(r, theta, average_energy, average_std_dev)
	"""

	# Drops the point (0,0)
	mask_neg_r = (linear_energy[:,0] < 0)
	mask_pos_r = (linear_energy[:,0] > 0)
	
	# Extract energy at positive and negative radius
	eng_neg_r = linear_energy[mask_neg_r]
	eng_pos_r = linear_energy[mask_pos_r]

	if np.shape(eng_neg_r) != np.shape(eng_pos_r):
		raise ValueError("eng_neg_r and eng_pos_r are not the same shape. The parameter err in energy_along_theta may be too high.")

	# Average energy values
	# Note that eng_pos_r and eng_neg_r must be same shape per the error message above
	eng_pos_r[:,2] = (eng_pos_r[:,2] + eng_neg_r[:,2])/2

	if std_dev:
		# Add errors in quadrature
		eng_pos_r[:,3] = np.sqrt(eng_pos_r[:,3]**2 + eng_neg_r[:,3]**2)

	return eng_pos_r

def plotter_1D(linear_energy: np.ndarray, ind_var: int=0, plot_rng: tuple=(0,0), std_dev: bool=False, num_Hx: float=0.0) -> tuple:
	"""
	Constructs numpy arrays to plot energy or std dev as a function of radius/angle.

	Parameters:
		- linear_energy: np.ndarray - numpy array specifying energy along theta or at radius r, with columns (r, theta, energy, std_dev)
		- ind_var: int - sets independent variable of plot (0 = radius, 1 = angle)
		- plot_rng: tubple - tuple setting range for x-axis; if plot_rng[0] == plot_rng[1], plots entire range
		- std_dev: bool - if True, plots standard dev for each point
		- num_Hx: float - number of histories from simulation; must be nonzero if std_dev == True

	Returns:
		- Tuple (x, energy, std_dev_sum, std_dev_mean, yerr), where
			- x = independent variable (radius or theta)
			- energy = dependent variable 
			- std_dev_sum = standard dev of total energy deposited in voxel
			- std_dev_mean = standard dev of mean energy deposited in voxel
			- yerr = deprecated - do not use
	"""

	if ind_var > 1 or ind_var < 0: raise ValueError("Independent variable must be 0 = radius or 1 = angle")

	if plot_rng[0] == plot_rng[1]:
		# Plot entire range
		r1 = np.min(linear_energy[:,ind_var])
		r2 = np.max(linear_energy[:,ind_var])
	else:
		# Plot range specified by plot_rng
		r1 = plot_rng[0]
		r2 = plot_rng[1]
	
	# Boolean mask to extract x- and y-axis values within plot_rng
	b1 = (linear_energy[:,ind_var] >= r1) & (linear_energy[:,ind_var] <= r2)

	yerr = None
	std_dev_of_sum = np.empty(np.shape(linear_energy[:,0]))
	std_dev_of_mean = np.empty(np.shape(linear_energy[:,0]))

	if std_dev:
		if num_Hx == 0: raise ValueError("If plotting std dev, number of histories must be specified (cannot be zero)")
		if np.shape(linear_energy)[1] < 3: raise ValueError("Input csv file does not contain std dev information")

		# See https://topas.readthedocs.io/en/latest/parameters/scoring/misc.html#statistical-information
		std_dev_of_sum = np.sqrt(num_Hx)*linear_energy[:,3]
		std_dev_of_mean = linear_energy[:,3]/np.sqrt(num_Hx)

		yerr = std_dev_of_sum[b1]/2 # do not use - deprecated

	# Use Boolean mask b1 to extract x-axis, y-axis, and standard deviation values
	return (linear_energy[:,ind_var][b1], linear_energy[:,2][b1], std_dev_of_sum[b1], std_dev_of_mean[b1], yerr)

"""
def contour_energy(file: str, bins: tuple, dose_grid_half: float, const_plane: int, const_axis: int, rng_X: tuple, rng_Y: tuple, source_rad: float=0.0, 
	scale: bool=False, norm_energy: float=0.0, dose: float=0.0, zero_source: bool=False, 
	std_dev: bool=False, origin: tuple=(0,0), zero_region: str="circle") -> tuple:
	pass
"""

def contour_energy(file: str, bins: tuple, dose_grid_half: float, const_plane: int, const_axis: int, rng_X: tuple, rng_Y: tuple, 
	scale: bool=False, norm_energy: float=0.0, dose: float=0.0,
	zero_source: bool=False, zero_region: str="circle", origin: tuple=(0,0), source_rad: float=0.0, source_rect: tuple=(0,0),
	std_dev: bool=False) -> tuple:
	"""
	Constructs numpy arrays for use in matplotlib contour plotting functions.

	Parameters - required:
		- file: str - input csv file
		- bins: tuple - number of bins from the simulation in format (bins, bins)
		- dose_grid_half: float - dosing grid half length
		- const_plane: int - specifies the voxel that is held constant when extracting plane
		- const_axis: int - axis to hold constant when extracting plane (0 = x, 1 = y, 2 = z)
		- rng_X: tuple - range of x-axis
		- rng_Y: tuple - range of y-axis

	Parameters - optional - scaling:
		- scale: bool - if True, normalizes extracted energy values to the dose delivered at norm_point
		- norm_energy: float - energy extracted from norm_point. Must be nonzero if scale == True.
		- dose: float - prescription dose delivered to norm_point. Must be nonzero if scale == True.

	Parameters - optional - source zeroing:
		- zero_source: float - if True, all voxels with r < source_rad have their energies set to 0
		- zero_region: str - sets shape of region zeroed when zero_source = True; must be "circle" or "rectangle"
		- origin: tuple - sets the coordinate origin; used to shift the center of the region that is zeroed when zero_source = True
		- source_rad: float - specifies radius within which voxel energies are set to 0. Must be nonzero if zero_source == True.
		- source_rect: tuple - defines width and height of rectangular area to zero in format (w, h)

	Parameters - optional - standard deviation
		- std_dev: bool - if True, calculates standard dev for each voxel

	Returns:
		- Tuple (X, Y, heights, std_dev), where
			- X is a numpy array of X-coordinates
			- Y is a numpy array of Y-coordinates
			- heights are the energy values for each voxel (i.e. height of contour plot at a particular location)
			- std_dev is standard dev value at each voxel
	"""
	plane = generate_plane(file, const_plane, const_axis)

	# Scale all voxels to prescription dose
	if scale:
		if (norm_energy == 0) or (dose == 0): raise ValueError("norm_energy and/or dose cannot be 0 if normalizing energy values")
		plane = normalize_energy(plane, norm_energy, dose)

	# Using (X, Y) notation here, but could be (X, Z) or (Y, Z) as well
	# Construct X and Y axes for contour plot
	X = voxel_to_cm(np.arange(0,bins[0]), bins[0], dose_grid_half*2/bins[0])
	Y = voxel_to_cm(np.arange(0,bins[1]), bins[1], dose_grid_half*2/bins[1])

	# Define Boolean masks to extract range of each axis
	mask_X = (X > rng_X[0]) & (X < rng_X[1])
	mask_Y = (Y > rng_Y[0]) & (Y < rng_Y[1])

	# Zero source for r < source_rad
	if zero_source:
		if ((source_rad <= 0)) and (zero_region == "circle"): raise ValueError("Source radius must be > 0 if zeroing source on contour plot")
		if ((source_rect[0] <= 0) or (source_rect[1] <= 0)) and (zero_region == "rectangle"): 
			raise ValueError("Rectangle height, width must be > 0 if zeroing source")
		if (zero_region != "circle") and (zero_region != "rectangle"): raise ValueError("zero_region must be circle or rectangle")

		# Convert voxel --> Cartesian
		plane[:,0] = voxel_to_cm(plane[:,0], bins[0], dose_grid_half*2/bins[0])
		plane[:,1] = voxel_to_cm(plane[:,1], bins[1], dose_grid_half*2/bins[1])

		if zero_region == "circle": 
			# Convert Cartesian --> polar
			polar_plane = cart_to_polar(plane, origin)

			# Extract values with r < source_rad and set energies to zero
			polar_mask = polar_plane[:,0] <= source_rad
			plane[:,2][polar_mask] *= 0 # recall that plane has columns (x, y, energy, std_dev)

		if zero_region == "rectangle":
			cart_mask_x = (plane[:,0] <= (origin[0] + source_rect[0]/2)) & (plane[:,0] > (origin[0] - source_rect[0]/2))
			cart_mask_y = (plane[:,1] <= (origin[1] + source_rect[1]/2)) & (plane[:,1] > (origin[1] - source_rect[1]/2))
			total_cart_mask = cart_mask_x & cart_mask_y

			plane[:,2][total_cart_mask] *= 0
	
	# Reshape the energy column of plane to a format compatible with the matplotlib countour function
	height_values = np.reshape(plane[:,2], bins)[mask_X][:,mask_Y]

	# Extract standard dev values if necessary
	std_dev_values = None
	if std_dev:
		std_dev_values = np.transpose(np.reshape(plane[:,3], bins))[mask_Y][:,mask_X]

	# Note that we use Boolean masks mask_X and mask_Y defined above to extract X- and Y-axes
	return (X[mask_X], Y[mask_Y], height_values, std_dev_values)

#### Optimization functions ####

def dose_rate_matrix(output_files: np.ndarray, dose_points: np.ndarray, dwell_pos_Z: np.ndarray, 
	source_dose_rate: float, bins: int, dose_grid_half: int, 
	file_ext: str="", save: bool=True, save_name: str="matrix.npy") -> np.ndarray:
	"""
	Construct dose rate matrix for linear penalty model and saves matrix in .npy format for later use.

	Parameters - required:
		- output_files: np.ndarray - array of output files, where each file is a simulation for one source dwell position
		- dose_points: np.ndarray - array of tuples containing dose points in (X, Y, Z) format (constant across all simulations)
		- dwell_pos_Z: np.ndarray - Z coordinate of dwell positions; we assume all sources have (x, y) = (0, 0) corresponding to applicator center

		- source_dose_rate: float - dose rate at the source (constant across all simulations)
		- bins: int - number of bins from the simulation (we assume bins_X = bins_Y = bins_Z) as defined in TOPAS parameter file 
		- dose_grid_half: int - dosing grid half length as defined in TOPAS parameter file

	Parameters - optional:
		- file_ext: str - optional file extension to allow function to find output files
		- save: bool - if True, saves constructed matrix
		- save_name: str - name for matrix when saved, including file extension if applicable

	Returns:
		- Numpy array of size (num_dose_points, num_dwell_positions) were d_ij is the energy deposited at dosing point i
		due to the source at dwell position j
	"""
	if np.shape(dwell_pos_Z)[0] != np.shape(output_files)[0]:
		raise ValueError("Number of dwell position Z coordinates must match number of output files")

	# Set the number of dose points and the number of dwell positions
	num_dose_points = np.shape(dose_points)[0]
	num_dwell_pos = np.shape(output_files)[0]

	# Compute the lattice length for the simulation space in cm
	lattice = dose_grid_half*2/bins

	# Initialize and construct the dose rate matrix
	D = np.zeros((num_dose_points, num_dwell_pos))

	for j in range(num_dwell_pos):
    	# Step 1 - extract normalized dose rate @ source
		source_plane = cm_to_voxel(np.array(dwell_pos_Z[j]), bins, lattice)

    	## Note - in this function, we're first holding the Z-axis constant by setting const_plane to the Z-coordinate
    	## of the source and setting const_axis = 2 (recall 0 = X, Y = 1, Z = 2; see def of extract_norm_energy for more detail).
    	## We then set the parameter norm_point (corresponding to the location of the source in the X, Y plane) to (X, Y) = (0, 0), 
    	## since the source is centered in the applicator.
		source_energy, __ = extract_norm_energy(file_ext + output_files[j], source_plane, 2, (0, 0), bins, lattice)

	    # Step 2 - iterate over dose points, extract energy, and scale to source_energy
		for i in range(num_dose_points):
			dose_point_Z = dose_points[i][2] # for second index - 0 = X, 1 = Y, 2 = Z
	        
			dose_plane = cm_to_voxel(np.array(dose_point_Z), bins, lattice)

	        ## Again, holding the Z-axis as constant first
			dose_energy, __ = extract_norm_energy(file_ext + output_files[j], dose_plane, 2, (dose_points[i][0], dose_points[i][1]), 
				bins, lattice)

			normed_dose_energy = (dose_energy/source_energy)*source_dose_rate
			D[i][j] = normed_dose_energy

	# Save matrix
	if save:
		np.save(save_name, D)

	return D

#### Rotation functions ####

def rotate_applicator(energy: np.ndarray, theta: float) -> np.ndarray:
	"""
	Uses Pillow (Python Imaging Library) to rotate the applicator's radiation distribution.
	Note that information loss during rotation is inversely proportional to voxel density.

	Parameters:
		- energy: np.ndarray - matrix with energy values from contour plot (equivalent to "height" returned from contour_energy")
		- theta: float - angle for rotation; must be in degrees (not radians)

	Returns:
		- Matrix with energy values rotated by theta
	"""
	Im = Image.fromarray(energy)
	Im = Im.rotate(theta)
	return np.array(Im)
