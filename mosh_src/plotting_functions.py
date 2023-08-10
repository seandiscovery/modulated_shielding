import numpy as np
import matplotlib.pyplot as plt
from math import pi
from decimal import Decimal

"""
Suite of functions to process data from TOPAS simulations. 
Author: Sean Mullane, June - August 2023

Note: this file makes heavy use of Boolean indexing to efficiently extract information from numpy arrays. 
If unfamiliar with Boolean indexing, see: https://numpy.org/doc/stable/user/basics.indexing.html#boolean-array-indexing
"""

def generate_plane(file: str, const_plane: int, const_axis: int) -> np.ndarray:
	volume = np.genfromtxt(file, delimiter=",")

	plane = volume[volume[:,const_axis] == const_plane]
	plane = np.delete(plane, const_axis, 1)

	return plane

def cm_to_voxel(cm: np.ndarray, bins: int, lattice: float) -> np.ndarray:
	"""
	Converts Cartesian space to voxel space. Inverse of voxel_to_cm.
	"""
	return int(bins/2) + (cm/lattice).astype(int)

def voxel_to_cm(voxels: np.ndarray, bins: int, lattice: float) -> np.ndarray:
	"""
	Converts voxel space to Cartesian space. Inverse of cm_to_voxel.
	"""
	return (voxels - int(bins/2))*lattice

def cart_to_polar(cart_plane: np.ndarray) -> np.ndarray:
	""" 
	Transform 2D Cartesian coordinates to Polar coordinates. 
	Assumes input matrix where first two columns are Cartesian coordinates; remaining columns returned unchanged.
	"""
	num_cols = np.shape(cart_plane)[1]
	polar_plane = np.empty(np.shape(cart_plane))
	
	polar_plane[:,0] = np.sqrt(cart_plane[:,0]**2 + cart_plane[:,1]**2) # (x, y) --> r
	polar_plane[:,1] = np.arctan2(cart_plane[:,1], cart_plane[:,0]) # (x, y) --> theta
	
	for i in range(2, num_cols):
		polar_plane[:,i] = cart_plane[:,i]

	return polar_plane

def extract_norm_energy(file: str, const_plane: int, const_axis: int, norm_point: tuple, bins: int, lattice: float) -> tuple:
	plane = generate_plane(file, const_plane, const_axis)

	norm_point_voxel = cm_to_voxel(np.array(norm_point), bins, lattice)
	mask = (plane[:,0] == norm_point_voxel[0]) & (plane[:,1] == norm_point_voxel[1])

	norm_energy = plane[mask][0][2]

	return (norm_energy, norm_point_voxel)

def normalize_energy(plane: np.ndarray, norm_energy: float) -> np.ndarray:
	"""
	Normalizes energy in each voxel to a prescription dose defined at the voxel norm_point.
	Assumes XBins = YBins.
	"""
	plane[:,2] = (plane[:,2]/norm_energy)*100

	return plane

def energy_along_theta(file: str, theta: float, bins: tuple, dose_grid_half: float, z_slice: int, err: float=0.001, 
	radius: float=0.0, scale: bool=False, norm_energy: float=0.0) -> tuple:
	"""
	Returns energy along an angle theta in range (0, pi].
	To also return the energy at a constant radius, set parameter radius to be > 0.
	"""
	if theta <= 0 or theta > pi: raise ValueError("Parameter theta must be in range (0, pi] - use theta = pi to plot along x-axis")

	# Extract plane of plot
	volume = np.genfromtxt(file, delimiter=",")

	plane = volume[volume[:,2] == z_slice]
	plane = np.delete(plane, 2, 1)

	if scale:
		if norm_energy == 0: raise ValueError("norm_energy cannot be 0 if scaling energy values")
		plane = normalize_energy(plane, norm_energy)

	# Transform voxel space ---> Cartesian space
	plane[:,0] = voxel_to_cm(plane[:,0], bins[0], dose_grid_half*2/bins[0])
	plane[:,1] = voxel_to_cm(plane[:,1], bins[1], dose_grid_half*2/bins[1])

	# Transform Cartesian space ---> polar space
	polar = cart_to_polar(plane)

	# Extract energy values along theta
	mask_theta = (polar[:,1] < theta + err) & (polar[:,1] > theta - err)
	mask_pi = (polar[:,1] < (theta - pi) + err) & (polar[:,1] > (theta - pi) - err)

	linear_energy = polar[(mask_theta + mask_pi)]

	# Multiply r-values along (theta - pi) by -1 for plotting
	mask_invert = (linear_energy[:,1] < (theta - pi) + err) & (linear_energy[:,1] > (theta - pi) - err)
	linear_energy[:,0][mask_invert] *= -1

	eng_at_const_r = None
	if radius > 0:
		mask_radius = (polar[:,0] < radius + err) & (polar[:,0] > radius - err)
		eng_at_const_r = polar[mask_radius]

	return (linear_energy, eng_at_const_r)

def average_energy(linear_energy: np.ndarray, std_dev: bool=False) -> np.ndarray:
	"""
	Averages energy along theta and (theta - pi) to smooth out statistical fluctuations.
	Assumes linear_energy has column format: r, theta, energy_sum, std_dev (optional), where r < 0 indicates values along (theta - pi)
	"""
	# Drops the point (0,0)
	mask_neg_r = (linear_energy[:,0] < 0)
	mask_pos_r = (linear_energy[:,0] > 0)
	
	eng_neg_r = linear_energy[mask_neg_r]
	eng_pos_r = linear_energy[mask_pos_r]

	eng_pos_r[:,2] = (eng_pos_r[:,2] + eng_neg_r[:,2])/2

	if std_dev:
		# Add errors in quadrature
		eng_pos_r[:,3] = np.sqrt(eng_pos_r[:,3]**2 + eng_neg_r[:,3]**2)

	return eng_pos_r

def plotter_1D(linear_energy: np.ndarray, ind_var: int=0, plot_rng: tuple=(0,0), std_dev: bool=False, num_Hx: float=0.0) -> tuple:
	"""
	Constructs numpy arrays to plot energy or std dev as a function of radius/angle.

	Parameters:
		- ind_var --> sets independent variable of plot: 0 = radius, 1 = angle
	"""

	if ind_var > 1 or ind_var < 0: raise ValueError("Independent variable must be 0 = radius or 1 = angle")

	if plot_rng[0] == plot_rng[1]:
		# Plot entire range
		r1 = np.min(linear_energy[:,ind_var])
		r2 = np.max(linear_energy[:,ind_var])
	else:
		r1 = plot_rng[0]
		r2 = plot_rng[1]
	
	b1 = (linear_energy[:,ind_var] >= r1) & (linear_energy[:,ind_var] <= r2)

	yerr = None
	std_dev_of_sum = np.empty(np.shape(linear_energy[:,0]))
	std_dev_of_mean = np.empty(np.shape(linear_energy[:,0]))

	if std_dev:
		if num_Hx == 0: raise ValueError("If plotting std dev, number of histories must be specified (cannot be zero)")
		if np.shape(linear_energy)[1] < 3: raise ValueError("Input csv file does not contain std dev information")

		std_dev_of_sum = np.sqrt(num_Hx)*linear_energy[:,3]
		std_dev_of_mean = linear_energy[:,3]/np.sqrt(num_Hx)
		yerr = std_dev_of_sum[b1]/2

	return (linear_energy[:,ind_var][b1], linear_energy[:,2][b1], std_dev_of_sum[b1], std_dev_of_mean[b1], yerr)

def contour_energy(file: str, bins: tuple, dose_grid_half: float, const_plane: int, const_axis: int, rng_X: tuple, rng_Y: tuple, 
	source_rad: float=0.0, scale: bool=False, norm_energy: float=0.0, zero_source: bool=False, std_dev: bool=False) -> tuple:
	"""
	Constructs numpy arrays for use in matplotlib contour plotting functions.
	"""
	plane = generate_plane(file, const_plane, const_axis)

	if scale:
		if norm_energy == 0: raise ValueError("norm_energy cannot be 0 if scaling energy values")
		plane = normalize_energy(plane, norm_energy)

	# Using (X, Y) notation here, but could be (X, Z) or (Y, Z) as well
	X = voxel_to_cm(np.arange(0,bins[0]), bins[0], dose_grid_half*2/bins[0])
	Y = voxel_to_cm(np.arange(0,bins[1]), bins[1], dose_grid_half*2/bins[1])

	mask_X = (X > rng_X[0]) & (X < rng_X[1])
	mask_Y = (Y > rng_Y[0]) & (Y < rng_Y[1])

	if zero_source:
		if source_rad == 0: raise ValueError("Source radius must be > 0 if zeroing source on contour plot")

		plane[:,0] = voxel_to_cm(plane[:,0], bins[0], dose_grid_half*2/bins[0])
		plane[:,1] = voxel_to_cm(plane[:,1], bins[1], dose_grid_half*2/bins[1])

		polar_plane = cart_to_polar(plane)
		polar_mask = polar_plane[:,0] <= source_rad

		plane[:,2][polar_mask] *= 0

	height_values = np.transpose(np.reshape(plane[:,2], bins))[mask_Y][:,mask_X]

	std_dev_values = None
	if std_dev:
		std_dev_values = np.transpose(np.reshape(plane[:,3], bins))[mask_Y][:,mask_X]

	return (X[mask_X], Y[mask_Y], height_values, std_dev_values)
