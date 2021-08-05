## Overview

This python script contains the code that was used for flux calibration using filterbank files. <br>
Dedispersed and folded profiles were created directly from the filterbank files of the pulsar (J1939+2134 in this case).<br>
The reason to use filterbank files was to make sure the baseline is not affected while reading the data from the FITS file using PSRCHIVE. <br>
We had to have full surety that the baseline wasn't affected while reading the data so as to move forward with developing the calibration logic.

However, moving forward, we have to prepare a calibration script that works with FITS files. 

### Preparation of required data files

If you wish to run this code, you need to have the dedisperse and subsequent fold output of 3 files:
* Pulsar filterbank
* On source quasar filterbank
* Off source quasar filterbank

The command used for my specific case was:
```bash
dedisperse J1939+2134_58804.421650_1460.norfix.fil -d 71.025634765625 -b 16 -nobaseline | /Data/bcj/INPTA/bin/fold -p 1.5579127187508547 -n 32 -nobaseline > J1939_profile
```

For generating profile from the quasar filterbank file, the dispersion measure doesn't matter but the fold period (value of the ``p`` flag) 
should be the same as that used for the pulsar.

### Usage

The paths to the prepared files needs to be edited into the corresponding lines in the script:
```python
# Reading the quasar files. 
onSrc_3C286 = pd.read_csv("path/to/3C286_dedispersed_folded.txt", header=None, delim_whitespace=True)
offSrc_3C286 = pd.read_csv("path/to/3C286OFF_dedispersed_folded.txt", header=None, delim_whitespace=True)

# Reading the pulsar files.
J1939_data = pd.read_csv("path/to/J1939_dedispersed_folded.txt", header=None, delim_whitespace=True)
```





