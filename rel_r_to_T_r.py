from .read_data import read_T_converter
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import rc

def first_order(b_1, a_1, x):
    return (b_1 * x + a_1)

def second_order(c_2, b_2, a_2, x):
    return (c_2 * x**2 + first_order(b_2, a_2, x))

def third_order(d, c, b, a, x):
    return d*x**3 + c*x**2 + b*x + a

def rel_r_to_T_r(lamp_rel_r):
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    temp_r, rel_r = read_T_converter()
    # fig, ax = plt.subplots()
    r_axis = np.arange(0, 15, 0.01)
    linestyles = ['--', '-.', ':', '-']
    for i in range(2):
        z = np.poly1d(np.polyfit(rel_r, temp_r, i+1))
        poly = [z(r_val) for r_val in r_axis]
        # ax.plot(r_axis, poly, linestyle=linestyles[i])
    # ax.plot(rel_r, temp_r, '.', color='black', markersize=6)
    # ax.set_xlabel(r"$\mathbf{\frac{R(T)}{R_{293}}}$")
    # ax.set_ylabel(r"$\mathbf{T_R}$")
    # plt.show()
    return list([z(lamp_rel_r_elem) for lamp_rel_r_elem in lamp_rel_r])
