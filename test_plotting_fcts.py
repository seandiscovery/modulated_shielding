from plotting_functions import *
from math import pi
import matplotlib.pyplot as plt
import matplotlib.colors as colors

#file = "../Outputs/SMART_Applicator_6channel_output.csv"

file = "../Outputs/1e7_test.csv"

#(plot, __) = radius_1D_plotter(file, pi, (51, 51, 51), 2.55, 25, plot_rng=(0.3, 1.0), std_dev=True, num_Hx=1e8, verbose=True)

#energy = energy_along_theta(file, pi, (51, 51, 51), 2.55, 25)

#test = average_energy(energy)

#plot, sd) = plotter_1D(test, plot_rng=(0.3,1.0), std_dev=True, num_Hx=1e8, verbose=True)

source_transZ = -0.5
source_plane = cm_to_voxel(source_transZ, 51, 1.25*2/51)

X, Y, energy = contour_energy(file, (51, 51), 1.25, source_plane, 2, (-0.6,0.6), (-0.6,0.6), 0.03, zero_source=True)

fig, ax = plt.subplots()

ax.contourf(X, Y, energy, norm=colors.LogNorm(), cmap="rainbow")

plt.show()