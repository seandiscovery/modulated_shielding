def contour_normalization(energy: np.ndarray, dose: float, roi_cm: tuple, bins: int, lattice: float) -> np.ndarray:
	"""
	DEPRECATED - but keeping until confirm that simpler normalization code is correct

	Normalize the energy values of the simulation to a prescription energy value at a particular ROI

	roi_cm units = real space (cm)

	Use with caution - if roi_cm is chosen inside an area w/zeroed energy, will encounter divide-by-zero error
	"""
	roi_point_voxel = cm_to_voxel(np.array(roi_cm), bins, lattice)
	dose_point = energy[roi_point_voxel[0], roi_point_voxel[1]]
	print(dose_point) # debug
	print(roi_point_voxel) # debug

	normalized_energy = (energy/dose_point)*dose

	"""
	# Deprecated method - above is simpler + reduces probability of divide-by-zero error

	mask = energy > 0
	scaling_factors = np.zeros(np.shape(energy))

	it = np.nditer(mask, flags=['multi_index'])
	for x in it:
		if x:
			scaling_factors[it.multi_index] = dose_point/energy[it.multi_index]
		else:
			scaling_factors[it.multi_index] = np.inf

	normalized_energy = dose/scaling_factors

	"""
	
	return normalized_energy

#### Rotation functions ####

def twoD_rot(theta: float) -> np.ndarray:
    return np.array([[np.cos(theta), -1*np.sin(theta)], [np.sin(theta), np.cos(theta)]])

def rot_mapping(holding: set, rot_voxel: tuple) -> tuple:
    # is rot_voxel in holding?
    # no ---> new voxel = rot_voxel
    # yes --> check rot_voxel[0] + 1, rot_voxel[0] - 1, etc. until empty voxel found
    # return empty voxel for assignment
    
    if not (rot_voxel in holding):
        empty_vox = rot_voxel

    # Check along x +/- 1, y +/- 1
    elif not ((rot_voxel[0] + 1, rot_voxel[1]) in holding):
        empty_vox = (rot_voxel[0] + 1, rot_voxel[1])

    elif not ((rot_voxel[0], rot_voxel[1] - 1) in holding):
        empty_vox = (rot_voxel[0], rot_voxel[1] - 1)

    elif not ((rot_voxel[0] - 1, rot_voxel[1]) in holding):
        empty_vox = (rot_voxel[0] - 1, rot_voxel[1])

    elif not ((rot_voxel[0], rot_voxel[1] + 1) in holding):
        empty_vox = (rot_voxel[0], rot_voxel[1] + 1)

    # Check four corners
    elif not ((rot_voxel[0] + 1, rot_voxel[1] + 1) in holding):
        empty_vox = (rot_voxel[0] + 1, rot_voxel[1] + 1)

    elif not ((rot_voxel[0] + 1, rot_voxel[1] - 1) in holding):
        empty_vox = (rot_voxel[0] + 1, rot_voxel[1] - 1)

    elif not ((rot_voxel[0] - 1, rot_voxel[1] - 1) in holding):
        empty_vox = (rot_voxel[0] - 1, rot_voxel[1] - 1)

    elif not ((rot_voxel[0] - 1, rot_voxel[1] + 1) in holding):
        empty_vox = (rot_voxel[0] - 1, rot_voxel[1] + 1)

    else:
        raise ValueError("No empty voxel found for " + str(rot_voxel))

    return empty_vox

def rotate_array(X: np.ndarray, Y: np.ndarray, energy: np.ndarray, angle: float, bins: int, rngX: tuple, 
	lattice: float) -> np.ndarray:
	"""
	Rotates the input energy array by theta. 
	Assumes that the energy array is square, i.e. rngX = rngY
	"""
	rotation = np.zeros(np.shape(energy))
	holding = set()

	rot = twoD_rot(angle)

	dose_grid_half = (rngX[1] - rngX[0])/2

	buffer = 1.5*np.sqrt(2)*lattice # still getting out-of-bound errors, even with this padding

	for i in np.arange(0, np.shape(X)[0]):
		for j in np.arange(0, np.shape(Y)[0]):
			vector = np.array([X[i], Y[j]])

			if np.linalg.norm(vector) <= dose_grid_half - buffer:
				height = energy[i][j]

				rotated_vec = rot @ vector

				rotated_voxel = cm_to_voxel(rotated_vec, bins, lattice)

				# Note that we convert rotated_voxel to a tuple
				rotated_voxel = rot_mapping(holding, (rotated_voxel[0], rotated_voxel[1]))

				# Check that rotated voxel is inside inscribed circle before assigning to rotation tensor?

				rotation[rotated_voxel[0]][rotated_voxel[1]] = height

				holding.add((rotated_voxel[0], rotated_voxel[1]))

	return rotation

def rotate_array_updated(X: np.ndarray, Y: np.ndarray, energy: np.ndarray, angle: float, bins: int, lattice: float) -> np.ndarray:
	"""
	Checking for out-of-bounds in a different way. Possibly slower runtime?
	"""
	rotation = np.zeros(np.shape(energy))
	holding = set()

	rot = twoD_rot(angle)

	#dose_grid_half = (rngX[1] - rngX[0])/2 # not needed in this implementation

	#buffer = 1.5*np.sqrt(2)*lattice # not needed in this implementation

	for i in np.arange(0, np.shape(X)[0]):
		for j in np.arange(0, np.shape(Y)[0]):
			vector = np.array([X[i], Y[j]])

			height = energy[i][j]

			rotated_vec = rot @ vector
 
			rotated_voxel = cm_to_voxel(rotated_vec, bins, lattice)

			# Note that we convert rotated_voxel to a tuple
			rotated_voxel = rot_mapping(holding, (rotated_voxel[0], rotated_voxel[1]))

			if (rotated_voxel[0] < np.shape(X)[0]) and (rotated_voxel[1] < np.shape(Y)[0]):	
				rotation[rotated_voxel[0]][rotated_voxel[1]] = height
				holding.add((rotated_voxel[0], rotated_voxel[1]))

	return rotation