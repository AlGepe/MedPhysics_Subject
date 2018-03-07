from obci_readmanager.signal_processing import read_manager as read
import os.path
import numpy as np
import matplotlib.pyplot as plt
from obci_readmanager.signal_processing.balance.wii_preprocessing import *
from obci_readmanager.signal_processing.balance.wii_analysis import *

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
    y = y * 13  # Convert to cm

    data = np.array([TIME, x, y])

    return data


def file2dataWtags(fileName, tags):

    wbr = read.ReadManager(fileName+'.obci.xml', fileName+'.obci.raw',
                           fileName + '.obci.tag')
    startTag = tags[0]
    endTag = tags[1]
    print(startTag)
    print(endTag)
    cropped_by_tag = wii_cut_fragments(wbr, start_tag_name=startTag,
                                       end_tags_names=[endTag])
    print(len(cropped_by_tag))
    TL = cropped_by_tag[0].get_samples()[0, :]
    TR = cropped_by_tag[0].get_samples()[1, :]
    BR = cropped_by_tag[0].get_samples()[2, :]
    BL = cropped_by_tag[0].get_samples()[3, :]
    TIME = cropped_by_tag[0].get_samples()[4, :]

    x = ((TR+BR) - (TL+BL)) / (TR+TL+BR+BL)
    y = ((TR+TL) - (BR+BL)) / (TR+TL+BR+BL)

    x = x * 22.5  # Convert to cm
    y = y * 13  # Convert to cm

    data = np.array([TIME, x, y])

    return data


allTheFiles = [os.path.abspath('../')+'/Data/']*3
index = len(allTheFiles[0])

allTheFiles[0] += "sway_left"
allTheFiles[1] += "sway_right"
allTheFiles[2] += "sway_forward"
"""
allTheFiles[1] += "still_eyes_closed_eyes_open"
allTheFiles[1] += "sway_back"
allTheFiles[2] += "sway_forward"
allTheFiles[3] += "sway_left"
allTheFiles[4] += "sway_right"
allTheFiles[5] += "sway_stay_with_feedback"
allTheFiles[6] += "sway_with_feedback"
tags = np.ndarray(
"""
for name in allTheFiles:
    print(name)
    tags = np.array([["start_fast", "stop_fast"],
                     ["start", "stop"]],
                    dtype=object)
    '''
    tags = np.array([["ss_start", "ss_stop"],
                     ["ss_eyes_closed_start", "ss_eyes_closed_stop"]],
                    dtype=object)
    '''
    currentData = file2dataWtags(name, tags[0])
    # create a subplot
    currentData[0] -= min(currentData[0])
    plt.plot(currentData[1], currentData[2], 'o-')
    plt.title(name[index:])
    # plt.axis([-22.5, 22.5, -13, 13])
    plt.show()
