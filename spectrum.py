import matplotlib.pyplot as plt
from .read_data import read_spectrum
from matplotlib import rc
from scipy.optimize import curve_fit
from .utils_plancks import planks_radiation_law, volt_to_temp, wiens_displacement, planxs_radiation_law
import numpy as np

wavelengths = {"A": 600, "B": 552, "C": 501, "D": 458, "E": 403}
wavelength_err = {"A": 4, "B": 5.5, "C": 4, "D": 5.0, "E": 4.5}
colours_plotting = {"A": "red", "B": "blue", "C": "darkorange", "D": "hotpink", "E": "green"}
colours = ['b', 'r', 'g', 'c', 'm', 'royalblue', 'limegreen', 'tab:orange', 'tab:pink', 'tab:olive', 'crimson', 'palevioletred', 'darkkhaki']

def moving_average(data, temporal_window=200):
    """
    Produces an array of constant probability which is normalised over the whole data set.
    Mode ‘valid’ returns output of length max(M, N) - min(M, N) + 1. The convolution product is only given for points
    where the signals overlap completely. Values outside the signal boundary have no effect.
    :param data: The list of heights to average
    :param temporal_window: The size of the transient
    :return: The convolution of the data and the temporal_window
    """
    window = np.ones(temporal_window) / temporal_window
    return np.convolve(data, window, 'valid')


def filter_source_spectrum():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    for colour, indices in colour_index.items():
        file_name_filter = "C:\\Users\\18072\PycharmProjects\\3rdYearLab\\PhotoelectricEffect\\Data\\Filter\\"\
                           + source_to_filter[colour] + '_Filter_' + str(colour_time_filter[colour]) + 'ms.csv'
        file_name_source = "C:\\Users\\18072\PycharmProjects\\3rdYearLab\\PhotoelectricEffect\\Data\\Source\\"\
                           + colour + '_' + str(colour_time_source[colour]) + 'ms.csv'
        f_nm, f_inten = read_spectrum(file_name_filter, colour_index[colour][0], colour_index[colour][1])
        s_nm, s_inten = read_spectrum(file_name_source, colour_index[colour][0], colour_index[colour][1])

        fig, ax = plt.subplots()
        f_inten = [f / max(f_inten) for f in f_inten]
        s_inten = [s / max(s_inten) for s in s_inten]
        ax.plot(f_nm, f_inten, '--', color='black', linewidth=2)
        ax.plot(s_nm, s_inten, color=colours_plotting[colour], linewidth=2)
        ax.set_xlabel(r"\textbf{Wavelength} (nm)")
        ax.set_ylabel(r"\textbf{Normalised Intensity}")
        # plt.savefig("C:\\Users\\18072\\OneDrive\\Documents\\Academic\\University\\Physics\\3rd_Year\\Labs\\PhotoelectricEffect\\Graphs\\Spectrum\\" + str(colour) + "_spectrum.png")
    plt.show()


def CCD_spectrum():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    fig, ax = plt.subplots()
    temp = [293]
    temp.extend(np.array(volt_to_temp()))
    colours = ['b', 'r', 'g', 'c', 'm', 'royalblue', 'limegreen', 'tab:orange', 'tab:pink', 'tab:olive', 'crimson',
               'palevioletred', 'darkkhaki']
    colours = colours[::-1]
    print(temp)
    for voltage in np.arange(12, 7, -1):
        file_name = "C:\\Users\\18072\PycharmProjects\\3rdYearLab\\RadiationLaws\\Data\\Voltage\\" + \
                    str(voltage) + "V.csv"
        nm, inten = read_spectrum(file_name, 40, 3500)
        nm_plank = np.arange(0, 10000, 1)
        plank_fit = [planks_radiation_law(wl, temp[voltage]) for wl in nm_plank]
        wien = wiens_displacement(temp[voltage]) * 10 ** 9
        # print(temp[voltage])
        # plank_fit_shifted = [planks_radiation_law(temp_shifted, wl) for wl in nm]
        # inten = [i / max(inten) for i in inten]
        temporal_window = 100
        inten_smoothed = moving_average(inten, temporal_window=temporal_window)
        ax.plot(nm, inten, '-', color='gray', linewidth=0.4)
        nm_smooth = np.linspace(min(nm), max(nm), len(inten_smoothed) + temporal_window)
        nm_smooth = nm_smooth[int(temporal_window/2) : len(nm_smooth) - int(temporal_window/2)]
        inten_crop, nm_crop = [], []
        for inten_num, inten_s in enumerate(inten_smoothed):
            if nm_smooth[inten_num] < 630:
                inten_crop.append(inten_s)
                nm_crop.append(nm_smooth[inten_num])
        p0 = [10**-27, 10**-6]
        popt, pcov = curve_fit(planxs_radiation_law, nm_crop, inten_crop, p0=p0)
        # print(popt)
        ax.plot(nm_plank, planxs_radiation_law(nm_plank, *popt), '--', color=colours[voltage], label=str(voltage)+'V')
        ax.plot(nm_smooth, inten_smoothed, '-', linewidth=1, color=colours[voltage])
        # ax.plot(nm_plank, plank_fit, '-', color=colours[voltage])
        # ax.plot(nm, plank_fit_shifted, '--', color=colours[voltage])
        k_b = 1.38 * 10 ** -23
        c = 3 * 10 ** 8
        print((popt[1] * k_b * temp[voltage]) / c)
        # print((np.sqrt(np.diag(pcov))[1] * k_b * temp[voltage]) / c)
        # ax.axvline(wien, color=colours[voltage], linewidth=0.2)
        ax.set_xlim(450, 700)
        ax.set_ylim(0, 1)
    # ax.axvline(784.3, color='black', linewidth=3)
    # ax.set_xlim(400, 1600)
    # ax.set_ylim(0, 3)
    ax.set_xlabel(r'$\lambda \textbf{ (nm)}$')
    ax.set_ylabel(r'\textbf{Intensity (arb. units)}')
    plt.legend(loc='best')
    plt.show()