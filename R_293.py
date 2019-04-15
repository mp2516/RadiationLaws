import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from PhotoelectricEffect.utils_dataproc import wavelength_to_frequency, chi_squared, find_linear_fit, \
    find_linear_lines, frequency_err, normalise_i
from PhotoelectricEffect.utils_dos import e
from PhotoelectricEffect.utils_plot import estimate_h
from .read_data import read_r_293, read_r_293_wheatstone
from matplotlib import rc

def straight_line(x, a, b):
    return x * a + b

def find_linear_fit(i, i_err, v):
    [m, c], err = curve_fit(straight_line, xdata=v, ydata=i, sigma=i_err, absolute_sigma=True)
    m_err, c_err = np.sqrt(np.diag(err))
    return m, m_err, c, c_err

def crop_data(i, i_err, v, low_lim, up_lim):
    return i[low_lim:up_lim], i_err[low_lim:up_lim], v[low_lim:up_lim]


def cal_r(i, v):
    r = []
    for num in range(len(i)):
        r.append(float(v[num]/i[num]))
    return r


def cal_r_err(i, i_err, v, v_err):
    r_err = []
    for num in range(len(i)):
        r_err.append((v[num]/i[num])*np.sqrt((i_err[num]/i[num])**2 + (v_err[num]/v[num])**2))
    return r_err


def find_linear_lines(m, m_err, c, c_err, x):
    y0 = m * x + c
    y_err = np.sqrt((m_err * m) ** 2 + c_err ** 2)
    y_up = m * x + (c + y_err)
    y_low = m * x + (c - y_err)
    return y0, y_up, y_low


def resistance_rtp():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    fig, ax = plt.subplots()

    file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\Wheatstone_R293.csv"
    i, i_err, r, r_err = read_r_293_wheatstone(file_name)
    r_err = [r_err_elem * 2 for r_err_elem in r_err]
    xaxis = np.arange(0, max(i), 0.001)
    # ax.errorbar(x=i, y=r, yerr=r_err, fmt='.', color='black', linewidth=2)
    m, m_err, c, c_err = find_linear_fit(r, r_err, i)
    m_err*=2
    c_err*=2
    y0, y_up, y_low = find_linear_lines(m, m_err, c, c_err, xaxis)
    # i, i_err, r = crop_data(i, i_err, r, low_lim=5, up_lim=15)
    ax.errorbar(x=i, y=r, yerr=r_err, fmt='.', color='black', linewidth=1, marker="v", markersize=6, label='Wheatstone')
    ax.plot(xaxis, y0, '--', color="blue", linewidth=2)
    ax.fill_between(xaxis, y_up, y_low, color='gainsboro')
    ax.set_ylabel(r"\textbf{Resistance} (" + "$\Omega$" + ")")
    ax.set_xlabel(r"\textbf{Current} (mA)")
    ax.set_xlim(0, 10)
    ax.set_ylim(0.48, 0.58)

    file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\R293.csv"
    i, i_err, v, v_err = read_r_293(file_name)
    xaxis = np.arange(0, max(i), 0.001)
    # ax.plot(current, voltage, '.', color='black', linewidth=2)
    r = cal_r(i, v)
    r_err = cal_r_err(i, i_err, v, v_err)
    r_err = [r_err_elem * 2 for r_err_elem in r_err]
    ax.errorbar(x=i, y=r, yerr=r_err, fmt='.', color='lightgrey', linewidth=1, marker="o", markersize=5)
    i, i_err, v = crop_data(i, i_err, v, low_lim=10, up_lim=32)
    r = cal_r(i, v)
    r_err = cal_r_err(i, i_err, v, v_err)
    r_err = [r_err_elem * 2 for r_err_elem in r_err]
    ax.errorbar(x=i, y=r, yerr=r_err, fmt='.', color='black', linewidth=1, marker="o", label='Voltmeter Method', markersize=5)
    m, m_err, c, c_err = find_linear_fit(r, r_err, i)
    y0, y_up, y_low = find_linear_lines(m, m_err, c, c_err, xaxis)

    ax.plot(xaxis, y0, ':', color="red")
    ax.fill_between(xaxis, y_up, y_low, color='gainsboro')

    print("\ngradient: {} +/- {}"
          "\nR293: {} +/- {}".format(m, m_err, c, c_err))
    plt.legend(loc=7)
    plt.show()