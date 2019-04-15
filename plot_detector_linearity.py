import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from RadiationLaws.utils_plancks import straight_line, find_linear_lines, T_r_to_T_b, r_to_rel_r, remove_background, \
    cal_r, crop_data
from .read_data import read_filter_voltage, read_amplified_wheatstone
from RadiationLaws.spectrum import colours_plotting
from RadiationLaws.rel_r_to_T_r import rel_r_to_T_r
from matplotlib import rc
import csv

def detector_linearity():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    fig, ax = plt.subplots()
    # ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\detector_linearity.csv"
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        inverse_dis_squared, voltage = [], []
        for row in csv_reader:
            inverse_dis_squared.append(float(row[0]))
            voltage.append(float(row[1]))

    # ax.legend(loc='best')
    ax.set_xlabel(r"Wavelength (nm)")
    ax.set_ylabel(r"Responsivity (A/W)")
    ax.plot(inverse_dis_squared, voltage, '.', color='black', markersize=4, marker='d')
    plt.show()