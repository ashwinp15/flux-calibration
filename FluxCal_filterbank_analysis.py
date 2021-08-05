
import pandas as pd
import numpy as np
from scipy.integrate import simps 
import matplotlib.pyplot as plt

###################################################################################
#
#   READING THE DATA FROM THE DEDISPERSED FOLDED PROFILES GENERATED FROM 
#   FILTERBANK FILES
#
###################################################################################

# Reading the quasar files. 
onSrc_3C286 = pd.read_csv("path/to/3C286_dedispersed_folded.txt", header=None, delim_whitespace=True)
offSrc_3C286 = pd.read_csv("path/to/3C286OFF_dedispersed_folded.txt", header=None, delim_whitespace=True)

# Reading the pulsar files.
J1939_data = pd.read_csv("path/to/J1939_dedispersed_folded.txt", header=None, delim_whitespace=True)


###################################################################################
#
#   DEFINING FUNCTIONS AND GLOBAL VARIABLES
#
###################################################################################

# Defining functions for Theoretical flux density of calibrators based on frequency
def theoretical_3C286(freq):
    freq = freq/1000 		# changing frequencies into GHz
    a =  1.2481
    b = -0.4507
    c = -0.1798
    d =  0.0357
    fd = 10**(a + b*np.log10(freq) + c*(np.log10(freq))**2 + d*(np.log10(freq))**3)
    return fd

def theoretical_3C48(freq):
    freq = freq/1000 		# changing frequencies into GHz
    a = 1.3253 
    b = -0.7553
    c = -0.1914
    d = 0.0498
    fd = 10**(a + b*np.log10(freq) + c*(np.log10(freq))**2 + d*(np.log10(freq))**3)
    return fd


# Defining arrays to store the results of the calculations and use it for plotting
fluxDensArray = []
profiles_all_freq = []
scaling_factor_all_freq = []
freq_range = [] 
counts_3C286 = []
counts_3C286OFF = []

###################################################################################
#
#  MAIN CALCULATION LOOP 
#
###################################################################################

# The scale factor is calculated from quasar data
# And then the pulsar telescope counts are multiplied by the corresponding factor 
# to obtain the flux density in Jansky.
# The band is divided into 16 subbands, and the calculation henceforth is done for each of those subbands
for x in range (1, 17):
    # Calculating the scaling factor from the quasar data
    onSrc_3C286_median = np.nanmedian(onSrc_3C286[x])
    offSrc_3C286_median = np.nanmedian(offSrc_3C286[x])
    counts_3C286.append(onSrc_3C286_median)
    counts_3C286OFF.append(offSrc_3C286_median)
    scaling_factor =     theoretical_3C286(1460-(x*(200.0/16)))/np.nanmedian(onSrc_3C286[x] - offSrc_3C286[x])
    # Appending the scale factor to the list of scale factors for each frequency
    scaling_factor_all_freq.append(scaling_factor)

    # Appending frequency of current subband to the freq_range array to use while plotting
    freq_range.append(1460-(x*(200.0/16)))
    
    # Removing the baseline in the pulsar data and applying the scale factor
    reduced_counts_J1939 = J1939_data[x] - np.median(J1939_data[x])
    reduced_SEFD_J1939 = reduced_counts_J1939 * scaling_factor
    profiles_all_freq.append(reduced_SEFD_J1939)

    # Calculating the average flux density by summing over flux density for
    # all the phase bins and dividing by number of phase bins
    avg_FD = np.sum(reduced_SEFD_J1939) / 32
    fluxDensArray.append(avg_FD)


###################################################################################
#
#  PLOTS AND OUTPUT
#
###################################################################################

# Plotting the average Fvux density of pulsar for each subband
plt.plot(np.linspace(1260, 1460, 16), list(reversed(fluxDensArray)), '-ok')
plt.ylabel("Jansky")
plt.xlabel("Frequency MHz")
plt.show()
    

# Plots the on and off source telescope counts of the quasars
plt.figure(figsize=(15, 45))
plt.plot(range(16), counts_3C286, '-o', label="ON")
plt.plot(range(16), counts_3C286OFF, '-o', label="OFF")
plt.legend()
plt.show()


# Plotting the Flux density of the pulsar according to phase, for each of the 16 subbands
# Outputs 16 plots each havin Flux density on the Y axis and Phase on the X axis
plt.figure(figsize=(15, 45))
for i in range (16):
    plt.subplot(8, 2, i+1)
    plt.plot(np.linspace(0, 1, 32), profiles_all_freq[i], '-o')
    plt.title("Freq" + str(1460-((i+1)*(200.0/16))))
    plt.xlabel("phase")
    plt.ylabel("Jansky")
plt.savefig("Scaled_All_Frequency_Profiles.pdf")    
plt.show()



# Outputs the scaling factor calculated from the calibrator into a csv file
scaleFactorsDF = pd.DataFrame(np.array([freq_range, scaling_factor_all_freq]).T)
scaleFactorsDF.columns = ['Freq (MHz)', 'scale factor']
scaleFactorsDF.to_csv("Freq wise scale factors.csv")



