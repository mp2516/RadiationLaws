import csv
import numpy as np


def read_r_293(file_name):
    """
    Opens the .csv file and parses the data converting into lists of data:
        current, voltage and current_error
    :param file_name:
    :return: voltage, current, current_error
    """
    line_count = 0
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        voltage, voltage_err = [], []
        current, current_err = [], []
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            elif line_count == 1:
                #print(f'\t Order of magnitude {row[0]} {row[1]} {row[2]}.')
                line_count += 1
            else:
                #print(f'\tVoltage: {row[0]}, Current: {row[1]} +/- {row[2]}.')
                voltage.append(float(row[0]))
                current.append(float(row[1]))
                current_err.append(0.0001)
                voltage_err.append(0.01)
                line_count += 1

    current.sort()
    voltage.sort()
    return current, current_err, voltage, voltage_err


def read_r_293_wheatstone(file_name):
    """
    Opens the .csv file and parses the data converting into lists of data:
        current, voltage and current_error
    :param file_name:
    :return: voltage, current, current_error
    """
    line_count = 0
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        r, r_err = [], []
        current, current_err = [], []
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            elif line_count == 1:
                #print(f'\t Order of magnitude {row[0]} {row[1]} {row[2]}.')
                line_count += 1
            else:
                #print(f'\tVoltage: {row[0]}, Current: {row[1]} +/- {row[2]}.')
                r.append(float(row[1]))
                current.append(float(row[0]))
                current_err.append(0.0001)
                r_err.append(0.001)
                line_count += 1

    # current.sort()
    # r.sort()
    return current, current_err, r, r_err


def read_T_converter():
    """
    Opens the .csv file and parses the data converting into lists of data:
        current, voltage and current_error
    :param file_name:
    :return: voltage, current, current_error
    """
    line_count = 0
    file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\T_r_vs_R_by_R_293.csv"
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        temp_r, rel_r = [], []
        for row in csv_reader:
            if line_count in [0]:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #print(f'\tVoltage: {row[0]}, Current: {row[1]} +/- {row[2]}.')
                temp_r.append(float(row[0]))
                rel_r.append(float(row[1]))
                line_count += 1

    return temp_r, rel_r

def read_filter_voltage(file_name):
    """
    Opens the .csv file and parses the data converting into lists of data:
        current, voltage and current_error
    :param file_name:
    :return: voltage, current, current_error
    """
    line_count = 0
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lamp_v, lamp_i, detec_v = [], [], []
        for row in csv_reader:
            if line_count in [0, 1]:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #print(f'\tVoltage: {row[0]}, Current: {row[1]} +/- {row[2]}.')
                lamp_v.append(float(row[0]))
                lamp_i.append(float(row[1]))
                detec_v.append(float(row[2]))
                line_count += 1

    return lamp_v, lamp_i, detec_v


def read_wheatstone(file_name):
    """
        Opens the .csv file and parses the data converting into lists of data:
            current, voltage and current_error
        :param file_name:
        :return: voltage, current, current_error
        """
    line_count = 0
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lamp_v, lamp_r, detec_i = [], [], []
        for row in csv_reader:
            if line_count in [0, 1]:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(f'\tVoltage: {row[0]}, Current: {row[1]} +/- {row[2]}.')
                lamp_v.append(float(row[0]))
                lamp_r.append(float(row[1]))
                detec_i.append(float(row[2]))
                line_count += 1

    return lamp_v, lamp_r, detec_i


def read_spectrum(file_name, low_index, high_index):
    line_count = 0
    with open(file_name) as spectrum_file:
        spectrum_reader = csv.reader(spectrum_file, delimiter=',')
        wavelength = []
        intensity = []
        for row in spectrum_reader:
            if line_count < low_index:
                line_count += 1
            elif line_count > high_index:
                line_count += 1
            else:
                wavelength.append(float(row[0]))
                intensity.append(float(row[1]))
                line_count += 1
    return wavelength, intensity


def read_amplified_wheatstone():
    filters = ["A", "B", "C", "D", "E"]
    file_name = "C:\\Users\\18072\\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\Amplified_Wheatstone\\Filter_amplified_wheatstone.csv"
    with open(file_name) as detector_file:
        filter_dict = {"A": [], "B": [], "C": [], "D": [], "E": []}
        detector_reader = csv.reader(detector_file, delimiter=',')
        background = 0.0525
        voltage, R_T = [], []
        for row in detector_reader:
            for num, f in enumerate(filters):
                filter_dict[f].append(float(row[num]) - background)
            voltage.append(float(row[5]))
            R_T.append(float(row[8]))
    return filter_dict, voltage, R_T


def read_time_dependence(file_name):
    with open(file_name) as time_dependence_file:
        time, intensity = [], []
        time_dependence_reader = csv.reader(time_dependence_file)
        for row_num, row in enumerate(time_dependence_reader):
            if row_num in [0,1,2]:
                pass
            else:
                time.append(float(row[0]))
                intensity.append(float(row[1]))
    return time, intensity
