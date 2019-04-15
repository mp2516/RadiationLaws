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


def detector_efficiency():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    colours_plotting = {"A": "red", "B": "blue", "C": "darkorange", "D": "hotpink", "E": "green"}
    wavelengths = {"A": 600, "B": 552, "C": 501, "D": 458, "E": 403}
    y_max = {"A": 0.32526732451436924, "B": 0.25935813529054963, "C": 0.18845690371065416, "D": 0.13093648016358472, "E": 0.05683814227487782}
    fig, ax = plt.subplots()
    # ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\detector_efficiency.csv"
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        wavelength, efficiency = [], []
        for row in csv_reader:
            wavelength.append(float(row[0]))
            efficiency.append(float(row[1]))

    # ax.legend(loc='best')
    for key, value in colours_plotting.items():
        ax.axvline(wavelengths[key], ymax=y_max[key]/0.75, color=value, linewidth=2.5)
    ax.set_xlabel(r"Wavelength (nm)")
    ax.set_ylabel(r"Responsivity (A/W)")
    ax.set_xlim(350, 1100)
    ax.set_ylim(0, 0.75)
    ax.plot(wavelength, efficiency, '-', color='black', linewidth=4)
    plt.show()