import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from RadiationLaws.utils_plancks import straight_line, find_linear_lines, T_r_to_T_b, r_to_rel_r, remove_background, \
    cal_r, crop_data, crop_data_reverse
from .read_data import read_filter_voltage, read_amplified_wheatstone
from RadiationLaws.spectrum import colours_plotting
from RadiationLaws.rel_r_to_T_r import rel_r_to_T_r
from matplotlib import rc

wavelengths = {"A": 600, "B": 552, "C": 501, "D": 458, "E": 403}
wavelength_err = {"A": 4, "B": 5.5, "C": 4, "D": 5.0, "E": 4.5}
colours_plotting = {"A": "red", "B": "blue", "C": "darkorange", "D": "hotpink", "E": "green"}
shapes_plotting = {"A": "o", "B": "^", "C": "s", "D": "d", "E": "v"}
linear_threshold = {"A": 7, "B": 7, "C": 11, "D": 11, "E": 11}
linear_threshold = {"A": 15, "B": 15, "C": 15, "D": 15, "E": 15}


def plot_unamplified_data():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    fig, ax = plt.subplots()
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    wavelengths = {"A": 600, "B": 552, "C": 501, "D": 458, "E": 403}
    wavelength_err = {"A": 4, "B": 5.5, "C": 4, "D": 5.0, "E": 4.5}
    linear_threshold = {"A": 19, "B": 19, "C": 19, "D": 19, "E": 19}
    for filter, wavelength in wavelengths.items():
        file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\Unamplified\\" + filter + "_Filter_unamplified.csv"
        lamp_v, lamp_i, detec_i = read_filter_voltage(file_name)
        lamp_r = cal_r(lamp_i, lamp_v)
        lamp_rel_r = r_to_rel_r(lamp_r)
        lamp_temp_r = rel_r_to_T_r(lamp_rel_r)
        lamp_temp_b = T_r_to_T_b(lamp_temp_r)
        temp_plot = [1 / lamp_temp_b_elem for lamp_temp_b_elem in lamp_temp_b]
        detec_i = remove_background(detec_i, background=detec_i[0])
        detec_i_err = 0.03
        detec_i_err_low, detec_i_err_up = [], []
        for detec_i_elem in detec_i:
            if detec_i_elem > detec_i_err:
                detec_i_err_up.append(np.abs(np.log(1 + detec_i_err / detec_i_elem)))
                detec_i_err_low.append(np.abs(np.log(1 - detec_i_err / detec_i_elem)))
            else:
                detec_i_err_up.append(0)
                detec_i_err_low.append(0)
        detec_i_ln = [np.log(detec_i_elem) for detec_i_elem in detec_i]
        a = 211.5
        b = 411.4
        r_293 = 0.51
        r_293_err = 0.01
        r_err = 0.01
        recep_T_err = []
        for lamp_r_elem in lamp_r:
            recep_T_err.append(np.sqrt((a**2 / (r_293**2 * (a * ((lamp_r_elem / r_293) - 1) + b)**4)) * r_err**2 +
            ((a**2 * lamp_r_elem**2) / ((b-a)*r_293 + a * lamp_r_elem)**4)*(r_293_err**2)) * 0.5)
        lim = linear_threshold[filter]
        ax.errorbar(temp_plot[:lim], detec_i_ln[:lim], xerr=recep_T_err[:lim],
                    yerr=[detec_i_err_low[:lim], detec_i_err_up[:lim]], color=colours_plotting[filter], fmt='.',
                    markersize=6, marker=shapes_plotting[filter], label=str(wavelength) + ' nm')
        ax.errorbar(temp_plot[lim:], detec_i_ln[lim:], xerr=recep_T_err[lim:],
                    yerr=[detec_i_err_low[lim:], detec_i_err_up[lim:]], color='black', fmt='.', markersize=6,
                    marker=shapes_plotting[filter])
        # temp_plot_rest, detec_i_ln = crop_data_reverse(temp_plot, detec_i_ln, linear_threshold[filter])
        # ax.plot(temp_plot_rest, detec_i_ln_rest, '.',
        #         color=colours_plotting[filter],
        #         markersize=5, marker=shapes_plotting[filter])
        temp_plot_crop, detec_v_ln_crop = crop_data(temp_plot, detec_i_ln, lim=linear_threshold[filter])
        [m, intercept], err = curve_fit(straight_line, xdata=temp_plot_crop, ydata=detec_v_ln_crop)
        k_b = 1.38 * 10 ** -23
        c = 3 * 10 ** 8
        m_err = np.sqrt(np.diag(err))[0]
        h_err = np.sqrt(((wavelength * 10 ** -9 * k_b) / c) ** 2 * m_err ** 2 + ((m * k_b) / c) ** 2 * 400 * 10 ** -18)
        xaxis = np.arange(0.0003, 0.001, 0.00000001)
        y0 = find_linear_lines(m, intercept, xaxis)
        print('\n')
        print(wavelength)
        print((-m * k_b * wavelength * 10 ** -9) / c)
        print(h_err)
        print('\n')
        ax.legend(loc='best')
        ax.set_xlabel(r"\textbf{1/T} (1/K)")
        ax.set_ylabel(r"$\ln{\theta}$")
        ax.set_xlim(3.5*10**-4, 6*10**-4)
        ax.set_ylim(-3, 4)
        ax.plot(xaxis, y0, '--', color=colours_plotting[filter])

    plt.show()


def plot_amplified_data():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    fig, ax = plt.subplots()
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    wavelengths = {"A": 600, "B": 552, "C": 501, "D": 458, "E": 403}
    wavelength_err = {"A": 4, "B": 5.5, "C": 4, "D": 5.0, "E": 4.5}
    linear_threshold = {"A": 19, "B": 19, "C": 19, "D": 19, "E": 19}
    for filter, wavelength in wavelengths.items():
        file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\amplified\\" + filter + "_Filter.csv"
        lamp_v, lamp_i, detec_v = read_filter_voltage(file_name)
        lamp_r = cal_r(lamp_i, lamp_v)
        lamp_rel_r = r_to_rel_r(lamp_r)
        lamp_temp_r = rel_r_to_T_r(lamp_rel_r)
        lamp_temp_b = T_r_to_T_b(lamp_temp_r)
        temp_plot = [1 / lamp_temp_b_elem for lamp_temp_b_elem in lamp_temp_b]
        detec_v = remove_background(detec_v, background=detec_v[0])
        detec_v_err = 0.0155
        detec_v_err_low, detec_v_err_up = [], []
        for detec_v_elem in detec_v:
            if detec_v_elem > detec_v_err:
                detec_v_err_up.append(np.abs(np.log(1 + detec_v_err/detec_v_elem)))
                detec_v_err_low.append(np.abs(np.log(1 - detec_v_err/detec_v_elem)))
            else:
                detec_v_err_up.append(0)
                detec_v_err_low.append(0)
        detec_v_ln = [np.log(detec_v_elem) for detec_v_elem in detec_v]
        ax.plot(temp_plot, detec_v_ln, '.',
                color=colours_plotting[filter],
                markersize=5, marker=shapes_plotting[filter])
        a = 211.5
        b = 411.4
        r_293 = 0.51
        r_293_err = 0.01
        r_err = 0.01
        recep_T_err = []
        for lamp_r_elem in lamp_r:
            recep_T_err.append(np.sqrt(
                (a ** 2 / (r_293 ** 2 * (a * ((lamp_r_elem / r_293) - 1) + b) ** 4)) * r_err ** 2 + (
                            (a ** 2 * lamp_r_elem ** 2) / ((b - a) * r_293 + a * lamp_r_elem) ** 4) * (
                            r_293_err ** 2)) * 0.5)
        lim = linear_threshold[filter]
        ax.errorbar(temp_plot[:lim], detec_v_ln[:lim], xerr=recep_T_err[:lim],
                    yerr=[detec_v_err_low[:lim], detec_v_err_up[:lim]], color=colours_plotting[filter], fmt='.',
                    markersize=6, marker=shapes_plotting[filter], label=str(wavelength) + ' nm')
        ax.errorbar(temp_plot[lim:], detec_v_ln[lim:], xerr=recep_T_err[lim:],
                    yerr=[detec_v_err_low[lim:], detec_v_err_up[lim:]], color='black', fmt='.', markersize=6,
                    marker=shapes_plotting[filter])
        temp_plot_crop, detec_v_ln_crop = crop_data(temp_plot, detec_v_ln, lim=linear_threshold[filter])
        [m, intercept], err = curve_fit(straight_line, xdata=temp_plot_crop, ydata=detec_v_ln_crop)
        k_b = 1.38 * 10 **-23
        c = 3 * 10 **8
        m_err = np.sqrt(np.diag(err))[0]
        h_err = np.sqrt(((wavelength*10**-9 * k_b)/c)**2 * m_err**2 + ((m * k_b)/c)**2 * 400 * 10 **-18)
        xaxis = np.arange(0.0003, 0.001, 0.00000001)
        y0 = find_linear_lines(m, intercept, xaxis)
        print('\n')
        print(wavelength)
        print((-m*k_b*wavelength*10**-9)/c)
        print(h_err)
        print('\n')
        ax.legend(loc='best')
        ax.set_xlabel(r"\textbf{1/T} (1/K)")
        ax.set_ylabel(r"$\ln{\theta}$")
        ax.set_xlim(2*10**-4, 8*10**-4)
        ax.set_ylim(-10, 6)
        ax.plot(xaxis, y0, '--', color=colours_plotting[filter])

    plt.show()


def plot_unamplified_wheatstone():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    fig, ax = plt.subplots()
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    wavelengths = {"A": 600}
    wavelength_err = {"A": 4}
    linear_threshold = {"A": 19, "B": 19, "C": 19, "D": 19, "E": 19}
    for filter, wavelength in wavelengths.items():
        file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\Unamplified_Wheatstone\\" + filter + "_Filter_unamplified_wheatstone.csv"
        lamp_v, lamp_r, detec_i = read_filter_voltage(file_name)
        # lamp_r = cal_r(lamp_i, lamp_v)
        lamp_rel_r = [r_elem / 0.565 for r_elem in lamp_r]
        lamp_temp_r = rel_r_to_T_r(lamp_rel_r)
        # print(lamp_temp_r)
        lamp_temp_b = T_r_to_T_b(lamp_temp_r)
        temp_plot = [1 / lamp_temp_b_elem for lamp_temp_b_elem in lamp_temp_b]
        detec_i = remove_background(detec_i, detec_i[0])
        detec_i_ln = [np.log(detec_i_elem) for detec_i_elem in detec_i]
        ax.plot(temp_plot, detec_i_ln, '.',
                color='black',
                markersize=3, marker=shapes_plotting[filter])
        detec_i_err = 0.03
        detec_i_err_low, detec_i_err_up = [], []
        for detec_i_elem in detec_i:
            if detec_i_elem > detec_i_err:
                detec_i_err_up.append(np.abs(np.log(1 + detec_i_err / detec_i_elem)))
                detec_i_err_low.append(np.abs(np.log(1 - detec_i_err / detec_i_elem)))
            else:
                detec_i_err_up.append(0)
                detec_i_err_low.append(0)
        a = 211.5
        b = 411.4
        r_293 = 0.51
        r_293_err = 0.01
        r_err = 0.01
        recep_T_err = []
        for lamp_r_elem in lamp_r:
            recep_T_err.append(np.sqrt(
                (a ** 2 / (r_293 ** 2 * (a * ((lamp_r_elem / r_293) - 1) + b) ** 4)) * r_err ** 2 + (
                            (a ** 2 * lamp_r_elem ** 2) / ((b - a) * r_293 + a * lamp_r_elem) ** 4) * (
                            r_293_err ** 2)) * 0.5)
        lim = linear_threshold[filter]
        ax.errorbar(temp_plot[:lim], detec_i_ln[:lim], xerr=recep_T_err[:lim],
                    yerr=[detec_i_err_low[:lim], detec_i_err_up[:lim]], color=colours_plotting[filter], fmt='.',
                    markersize=6, marker=shapes_plotting[filter], label=str(wavelength) + ' nm')
        ax.errorbar(temp_plot[lim:], detec_i_ln[lim:], xerr=recep_T_err[lim:],
                    yerr=[detec_i_err_low[lim:], detec_i_err_up[lim:]], color='black', fmt='.', markersize=6,
                    marker=shapes_plotting[filter])
        temp_plot_crop, detec_i_ln_crop = crop_data(temp_plot, detec_i_ln, lim=linear_threshold[filter])
        [m, intercept], err = curve_fit(straight_line, xdata=temp_plot_crop, ydata=detec_i_ln_crop)
        k_b = 1.38 * 10 ** -23
        c = 3 * 10 ** 8
        m_err = np.sqrt(np.diag(err))[0]
        h_err = np.sqrt(((wavelength * 10 ** -9 * k_b) / c) ** 2 * m_err ** 2 + ((m * k_b) / c) ** 2 * 400 * 10 ** -18)
        xaxis = np.arange(0.0003, 0.001, 0.00000001)
        y0 = find_linear_lines(m, intercept, xaxis)
        print('\n')
        print(wavelength)
        print((-m * k_b * wavelength * 10 ** -9) / c)
        print(h_err)
        print('\n')
        plt.legend(loc='best')
        ax.set_xlabel(r"\textbf{1/T} (1/K)")
        ax.set_ylabel(r"$\mathbf{\ln{\theta}}$")
        ax.set_xlim(0.0003, 0.0007)
        ax.set_ylim(-10, 5)
        ax.plot(xaxis, y0, '--', color=colours_plotting[filter])

    plt.show()

def plot_amplified_wheatstone():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    fig, ax = plt.subplots()
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    filter_dict, voltage, lamp_r = read_amplified_wheatstone()
    planks_constant = []
    planks_constant_err = []
    wavelengths = {"A": 600, "B": 552, "C": 501, "D": 458, "E": 403}
    wavelength_err = {"A": 4, "B": 5.5, "C": 4, "D": 5.0, "E": 4.5}
    linear_threshold = {"A": 9, "B": 9, "C": 6, "D": 7, "E": 8}
    for filter, wavelength in wavelengths.items():
        detec_v = filter_dict[filter]
        lamp_rel_r = [r_elem / 0.565 for r_elem in lamp_r]
        lamp_temp_r = rel_r_to_T_r(lamp_rel_r)
        lamp_temp_b = T_r_to_T_b(lamp_temp_r)
        temp_plot = [1 / lamp_temp_b_elem for lamp_temp_b_elem in lamp_temp_b]
        detec_v_ln = [np.log(detec_v_elem) for detec_v_elem in detec_v]
        detec_v_err = 0.0055
        detec_v_err_low, detec_v_err_up = [], []
        for detec_v_elem in detec_v:
            if detec_v_elem > detec_v_err:
                detec_v_err_up.append(np.abs(np.log(1 + detec_v_err / detec_v_elem)))
                detec_v_err_low.append(np.abs(np.log(1 - detec_v_err / detec_v_elem)))
            else:
                detec_v_err_up.append(0)
                detec_v_err_low.append(0)
        a = 211.5
        b = 411.4
        r_293 = 0.565
        r_293_err = 0.005
        r_err = 0.01
        recep_T_err = []
        for lamp_r_elem in lamp_r:
            recep_T_err.append(np.sqrt(
                (a ** 2 / (r_293 ** 2 * (a * ((lamp_r_elem / r_293) - 1) + b) ** 4)) * r_err ** 2 + (
                        (a ** 2 * lamp_r_elem ** 2) / ((b - a) * r_293 + a * lamp_r_elem) ** 4) * (
                        r_293_err ** 2)) * 0.5)
        lim = linear_threshold[filter]
        ax.errorbar(temp_plot[:lim], detec_v_ln[:lim], xerr=recep_T_err[:lim],
                    yerr=[detec_v_err_low[:lim], detec_v_err_up[:lim]], color=colours_plotting[filter], fmt='.',
                    markersize=6, marker=shapes_plotting[filter], label=str(wavelength) + ' nm')
        ax.errorbar(temp_plot[lim:], detec_v_ln[lim:], xerr=recep_T_err[lim:],
                    yerr=[detec_v_err_low[lim:], detec_v_err_up[lim:]], color='black', fmt='.', markersize=6,
                    marker=shapes_plotting[filter])
        temp_plot_crop, detec_v_ln_crop = crop_data(temp_plot, detec_v_ln, lim=linear_threshold[filter])
        [m, intercept], err = curve_fit(straight_line, xdata=temp_plot_crop, ydata=detec_v_ln_crop)
        xaxis = np.arange(0.0003, 0.001, 0.00000001)
        k_b = 1.38 * 10 ** -23
        c = 3 * 10 ** 8
        m_err = np.sqrt(np.diag(err))[0]
        h_err = np.sqrt(((wavelength * 10 ** -9 * k_b) / c) ** 2 * m_err ** 2 + ((m * k_b) / c) ** 2 * 400 * 10 ** -18)
        y0 = find_linear_lines(m, intercept, xaxis)
        print('\n')
        print(wavelength)
        print((-m * k_b * wavelength * 10 ** -9) / c)
        planks_constant.append((-m * k_b * wavelength * 10 ** -9) / c)
        planks_constant_err.append(h_err)
        print(h_err)
        print('\n')
        ax.legend(loc='best')
        ax.set_xlabel(r"\textbf{1/T} (1/K)")
        ax.set_ylabel(r"$\mathbf{\ln{\theta}}$")
        ax.set_xlim(0.0004, 0.0006)
        ax.set_ylim(-5, -1)
        ax.plot(xaxis, y0, '--', color=colours_plotting[filter])
    print(planks_constant)
    print(planks_constant_err)

    plt.show()
