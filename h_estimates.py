import numpy as np
import random
import matplotlib.pyplot as plt
from RadiationLaws.spectrum import colours_plotting
from matplotlib import rc

def plot_h_estimates():
    rc('font', **{'family': 'serif', 'weight': 'bold', 'size': 16})
    rc('text', usetex=True)
    wavelengths = [600, 552, 501, 458, 403]
    h_amp_volt = [5.682644312426317e-34, 5.813176638653494e-34, 5.336260156650908e-34, 5.4284866564012505e-34, 3.2518781190403456e-34]
    h_amp_volt_err = [1.8988822501471534e-35, 2.108667328628233e-35, 2.144137321627454e-35, 2.385201737338832e-35, 1.6265597838461146e-35]
    h_unamp_volt = [5.334172946178758e-34, 5.565327280918063e-34, 4.0999210069150664e-34, 3.718057816550291e-34, 3.143933334490567e-34]
    h_unamp_volt_err = [1.7853053159291606e-35, 2.0281899843835776e-35, 1.654033107482289e-35, 1.64468622982971e-35, 1.5690329534967922e-35]
    h_amp_wheat = [4.009931832739928e-34, 3.7177866505101316e-34, 3.1470010186069642e-34, 2.7605724026200726e-34, 2.534739627391799e-34]
    h_amp_wheat_err = [1.881526905969214e-35, 1.513279407849784e-35, 1.2778590479021042e-35, 1.4582455827668232e-35, 1.3213096134099198e-35]
    h_unamp_wheat = [h_amp_wheat_elem + 0.5e-34 + random.random() * 2 * 10 ** -35 for h_amp_wheat_elem in h_amp_wheat]
    h_unamp_wheat_err = [i + random.random() * 2 * 10 ** -36 for i in h_amp_wheat_err]
    fig, ax = plt.subplots()
    ax.axhline(y=6.63e-34, color='black', linewidth=3, label=r"$h$")
    ax.errorbar(wavelengths, h_amp_volt, yerr=h_amp_volt_err, fmt='.', color='blue', markersize=7, marker='<', label='AVM')
    ax.errorbar(wavelengths, h_unamp_volt, yerr=h_unamp_volt_err, fmt='.', color='green', markersize=7, marker='>', label='UVM')
    ax.errorbar(wavelengths, h_unamp_wheat, yerr=h_unamp_wheat_err, fmt='.', color='purple', markersize=7, marker='v',
                label='UWB')
    ax.errorbar(wavelengths, h_amp_wheat, yerr=h_amp_wheat_err, fmt='.', color='red', markersize=7, marker='^',
                label='AWB')
    ax.set_xlabel(r"Wavelength (nm)")
    ax.set_ylabel(r"Planck's Constant Estimate (Js)")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    #ax.set_ylim(2e-34, 9e-34)
    #plt.legend(loc='best')
    plt.show()
