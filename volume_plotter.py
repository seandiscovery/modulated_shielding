import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# Import volume scorer file - comma delimited
volume = np.genfromtxt("../Outputs/cylinder_volume_test_output.csv", delimiter=",")

