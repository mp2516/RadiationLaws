import numpy as np
from RadiationLaws.rel_r_to_T_r import rel_r_to_T_r


def straight_line(x, a, b):
    return x * a + b


def find_linear_lines(m, c, x):
    y0 = m * x + c
    # y_err = np.sqrt((m_err * m) ** 2 + c_err ** 2)
    # y_up = m * x + (c + y_err)
    # y_low = m * x + (c - y_err)
    return y0


def T_r_to_T_b(T_r):
    """
    Converts the temperature calculated from the resistance to the brightness temperature
    :param T_r: The temperature calculated from resistance
    :return: The brightness temperature
    """
    T_b = [((0.95171 * T_r_elem) + 132.484) for T_r_elem in T_r]
    return T_b


def r_to_rel_r(r, R_293 = 0.51):
    """
    Converts the resistance measured to the relative resistance = R/R_{293}
    :param r: resistance measured
    :param R_293: room temperature resistance
    :return: relative resistance
    """
    rel_r = [r_elem / R_293 for r_elem in r]
    return rel_r


def remove_background(detec_v, background):
    detec_v = [detec_v_elem - background for detec_v_elem in detec_v]
    return detec_v


def cal_r(i, v):
    """
    Calculating the resistance from the current and the voltage
    :param i: current
    :param v: voltage
    :return: resistance
    """
    r = []
    for num in range(len(i)):
        r.append(float(v[num]/i[num]))
    return r


def cal_r_err(i, i_err, v, v_err):
    """
    Calculate the error on the resistance from the current and voltage
    :param i: current
    :param i_err: current error
    :param v: voltage
    :param v_err: voltage error
    :return: resistance error
    """
    r_err = []
    for num in range(len(i)):
        r_err.append((v[num]/i[num])*np.sqrt((i_err[num]/i[num])**2 + (v_err[num]/v[num])**2))
    return r_err


def crop_data(temp_plot, detec_v_ln, lim):
    """
    Crop the 1/T and ln(theta) to exclude the bottom [lim] data points
    :param temp_plot: 1/T
    :param detec_v_ln: ln(theta)
    :param lim: The number of points to exclude
    :return: cropped data
    """
    return temp_plot[lim:], detec_v_ln[lim:]

def crop_data_reverse(temp_plot, detec_v_ln, lim):
    """
    Crop the 1/T and ln(theta) to exclude the bottom [lim] data points
    :param temp_plot: 1/T
    :param detec_v_ln: ln(theta)
    :param lim: The number of points to exclude
    :return: cropped data
    """
    return temp_plot[:lim], detec_v_ln[:lim]

def planks_radiation_law(wl, T, A=10**-11, h=6.63 * 10 ** -34):
    c = 3 * 10 ** 8
    k_b = 1.38 * 10 ** -23
    return  A * ((2 * h * c**2) / ((wl*10**-9) ** 5)) * (1 / (np.exp((h * c) / ((wl*10**-9) * k_b * T)) - 1))

def volt_to_temp():
    resistance = [1.782372338, 2.780481023, 3.508156464, 4.074979625, 4.56933973, 4.975124378, 5.363368195, 5.722460658, 6.047777442, 6.357279085, 6.652253451, 6.927606512]
    lamp_rel_r = r_to_rel_r(resistance, R_293=0.565)
    lamp_temp_r = rel_r_to_T_r(lamp_rel_r)
    lamp_temp_b = np.array(T_r_to_T_b(lamp_temp_r))
    # print(lamp)
    # temperature = np.array([1 / lamp_temp_b_elem for lamp_temp_b_elem in lamp_temp_b])
    return lamp_temp_b

def wiens_displacement(temp):
    return 0.002898 / temp


def planxs_radiation_law(wl, const, x):
    return  (const / ((wl*10**-9) ** 5)) * (1 / (np.exp(x / (wl*10**-9)) - 1))

