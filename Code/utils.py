from obci_readmanager.signal_processing import read_manager as read
import numpy as np
from obci_readmanager.signal_processing.balance.wii_preprocessing import *
from obci_readmanager.signal_processing.balance.wii_analysis import *


class Measurement:
    def __init__(self, title, fileName, tagData):
        self.title = title
        self.fileName = fileName
        self.tagData = tagData


class TagObject:
    def __init__(self, title, startTag, endTag):
        self.title = title
        self.tags = [startTag, endTag]

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


def file2dataNoTags(fileName):

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


def file2data(fileName, tags):

    if tags[0] == "" or tags[1] == "":
        return file2data(fileName)
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

