import matplotlib.pyplot as plt
import numpy as np
from .read_data import read_time_dependence
from matplotlib import rc
from scipy.optimize import curve_fit

wavelengths = {"A": 600, "B": 552, "C": 501, "D": 458, "E": 403}
wavelength_err = {"A": 4, "B": 5.5, "C": 4, "D": 5.0, "E": 4.5}
colours_plotting = {"A": "red", "B": "blue", "C": "darkorange", "D": "hotpink", "E": "green"}


def normalise_intensity(intensity):
    norm_intensity = []
    for inten in intensity:
        norm_intensity.append(inten/max(intensity))
    return norm_intensity


def exponential(xaxis, a, gamma, b):
    return a * np.exp(-1 * gamma * xaxis) + b


def plot_time_dependence():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    fig, ax = plt.subplots()
    intensity_err = []
    file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\time_dependence_10mins.csv"
    t_axis = np.arange(0, 600, 0.1)
    exp_axis = np.arange(-200, 800, 0.1)
    time, intensity = read_time_dependence(file_name)
    intensity = normalise_intensity(intensity)
    # time = normalise_intensity(time)
    for _ in range(len(intensity)):
        intensity_err.append(0.0001)
    ax.errorbar(x=time, y=intensity, yerr=intensity_err, fmt='.', color='blue', markersize=4, marker='v', label='Amplified Voltage')
    # ax.loglog(time, intensity)
    [a, gamma, b], err = curve_fit(exponential, xdata=time[20:], ydata=intensity[20:], p0=[0.04, 0.01, 0.96])
    exp_fit = exponential(exp_axis, a, gamma, b)
    print(gamma)
    print(b)
    ax.plot(exp_axis, exp_fit, '-.', color='red', label='Exp. Fit Amplified')
    file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\time_dependence_10mins_unamplified.csv"
    time, intensity = read_time_dependence(file_name)
    intensity = normalise_intensity(intensity)
    # time = normalise_intensity(time)
    intensity_err = []
    for _ in range(len(intensity)):
        intensity_err.append(0.0001)
    ax.errorbar(x=time, y=intensity, yerr=intensity_err, fmt='.', color='black', markersize=4, marker='^', label='Unamplified Current')
    [a, gamma, b], err = curve_fit(exponential, xdata=time[20:], ydata=intensity[20:], p0=[0.04, 0.01, 0.96])
    print(gamma)
    exp_fit = exponential(exp_axis, a, gamma, b)
    ax.plot(exp_axis, exp_fit, '--', color='red', label='Exp. Fit Unamplified')
    #[a, gamma, b], err = curve_fit(exponential, xdata=time[:10], ydata=intensity[:10], p0=[0.04, 0.01, 0.96])
    #exp_fit = exponential(t_axis, a, gamma, b)
    #ax.plot(t_axis, exp_fit, color='black')
    ax.set_xlim(0, 700)
    ax.set_ylim(0.96, 1)
    # ax.loglog(time, intensity)
    plt.legend(loc='best')
    ax.set_xlabel(r"Time (s)")
    ax.set_ylabel(r"Normalised Intensity (arb. units)")
    plt.show()
