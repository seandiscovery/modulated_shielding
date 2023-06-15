import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import phase space file
phase = np.genfromtxt("../Outputs/test_output_1.phsp")

# Extract energy deposition along z axis
x_pos = phase[:,0]
y_pos = phase[:,1]
mev = phase[:,5]

energy_z = np.column_stack((x_pos, y_pos, mev))

# Plot (x, y) positions receiving energy > 100 eV
plt.scatter(x_pos, y_pos)
plt.show()

# Generate contour map of energy deposition along (x, y) plane
# See matplotlib countour function: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html