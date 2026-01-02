# Import matplotlib and numpy - helpful Python libraries for scientific computing
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as patches
from matplotlib import ticker
from math import pi
from decimal import Decimal

from scipy.optimize import curve_fit
from scipy.interpolate import RegularGridInterpolator

def numerator(r: float, L: float, theta: float, plus: bool=True) -> float:
	if plus:
		return r*np.cos(theta) + (L/2)
	else:
		return r*np.cos(theta) - (L/2)

def denominator(r: float, L: float, theta: float, plus: bool=True) -> float:
	if plus:
		return np.sqrt(r**2 + (L/2)**2 + L*r*np.cos(theta))
	else:
		return np.sqrt(r**2 + (L/2)**2 - L*r*np.cos(theta))

def geometry_func(r: float, L: float, theta: float) -> float:
	top_1 = np.arccos(numerator(r, L, theta, plus=False)/denominator(r, L, theta, plus=False))
	top_2 = np.arccos(numerator(r, L, theta, plus=True)/denominator(r, L, theta, plus=True))
	bottom = L*r*np.sin(theta)

	return (top_1 - top_2)/bottom