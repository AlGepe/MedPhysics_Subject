from obci_readmanager.signal_processing import read_manager as read
import numpy as np
import matplotlib.pyplot as plt
import obci_readmanager.signal_processing.balance.wii_preprocessing
import obci_readmanager.signal_processing.balance.wii_analysis

# fileName = 'still_eyes_closed_eyes_open'


###############################################################################
# Function that takes the file name and returns the data already processed
#
#
# The data is returned as a 3-dim nadarray with:
#               data[0] being the time values
#               data[1] being the x values in cm
#               data[2] being the y values in cm
#
###############################################################################

def file2data(fileName):

    wbr = read.ReadManager(fileName+'.obci.xml', fileName+'.obci.raw',
                           fileName + '.obci.tag')
    TL = wbr.get_samples()[0, :]
    TR = wbr.get_samples()[1, :]
    BR = wbr.get_samples()[2, :]
    BL = wbr.get_samples()[3, :]
    TIME = wbr.get_samples()[4, :]

    x = ((TR+BR) - (TL+BL)) / (TR+TL+BR+BL)
    y = ((TR+TL) - (BR+BL)) / (TR+TL+BR+BL)

    x = x * 22.5  # Convert to cm
    y = y * 22.5  # Convert to cm

    data = np.array(TIME, x, y)

    return data


for name in allTheFiles :
    currentData = file2data(name)
    # create a subplot

# show plots







