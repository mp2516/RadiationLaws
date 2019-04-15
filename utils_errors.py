import numpy as np


def receprical_T_err(a, b, r_293, r_293_err, lamp_r, lamp_r_err):
    recep_T_err = []
    for lamp_r_elem in lamp_r:
        recep_T_err.append(np.sqrt(
            (a ** 2 / (r_293 ** 2 * (a * ((lamp_r_elem / r_293) - 1) + b) ** 4)) * lamp_r_err ** 2 + (
                    (a ** 2 * lamp_r_elem ** 2) / ((b - a) * r_293 + a * lamp_r_elem) ** 4) * (
                    r_293_err ** 2)) * 0.5)
    return recep_T_err