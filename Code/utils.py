import os.path
import matplotlib.pyplot as plt
from obci_readmanager.signal_processing import read_manager as read
import numpy as np
from obci_readmanager.signal_processing.balance.wii_preprocessing import *
# from obci_readmanager.signal_processing.balance.wii_analysis import *


###############################################################################
# Class to represent each measurement
#
# @param title Is the title of the Measurement (related to filename)
# @param fileName Name of the file where the data is stored (absolute path)
# @param tagData Object of class TagObject corresponding each measurement
#
###############################################################################


class Measurement:
    def __init__(self, title, fileName, tagData):
        self.title = title
        self.fileName = fileName
        self.tagData = tagData


###############################################################################
# Class to represent the tags of each measurement
#
# @param title Name of the specific measurement under this tags
# @param tags=[startTag, endTag] Markers for trimming data
#
###############################################################################


class TagObject:
    def __init__(self, title, startTag, endTag):
        self.title = title
        self.tags = [startTag, endTag]

###############################################################################
# Function that takes the file name and returns the measured data raw
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

    sumAll = TL + TR + BL + BR
    howManyZeros = np.sum(sumAll == 0.)

    if howManyZeros > 0:
        TL = TL[howManyZeros:]
        TR = TR[howManyZeros:]
        BL = BL[howManyZeros:]
        BR = BR[howManyZeros:]
        TIME = TIME[howManyZeros:]

    x = ((TR+BR) - (TL+BL)) / (TR+TL+BR+BL)
    y = ((TR+TL) - (BR+BL)) / (TR+TL+BR+BL)

    x = x * 22.5  # Convert to cm
    y = y * 13  # Convert to cm
    TIME -= min(TIME)

    data = np.array([TIME, x, y])

    return data

###############################################################################
# Function that takes the file name and tags to return the data trimmed using
# the tags provided. If no tags provided the function calls file2dataNoTags
#
#
# For measurements with n tags, returns an n-dimensional ndarray consisting of
# n x 3-dim arrays structured as follows:
#               data[0] being the time values
#               data[1] being the x values in cm
#               data[2] being the y values in cm
#
###############################################################################


def file2dataGame(fileName, tags):
    wbr = read.ReadManager(fileName+'.obci.xml', fileName+'.obci.raw',
                           fileName + '.obci.tag')
    cropped_by_tag = wii_cut_fragments(wbr, start_tag_name=tags[0],
                                       end_tags_names=[tags[1]])
    dimTags = len(cropped_by_tag)
    data = {}
    maxLevel = {'right': 0, 'left': 0, 'back': 0, 'forward': 0}
    for i in range(0, dimTags):
        grade = cropped_by_tag[i].get_end_tag()['desc']['value']
        tempDict = {}
        tempDict = eval(cropped_by_tag[i].get_start_tag()['desc']['value'])
        if (grade and maxLevel[tempDict['direction']] < tempDict['level']):

            maxLevel[tempDict['direction']] = tempDict['level']
            TL = cropped_by_tag[i].get_samples()[0, :]
            TR = cropped_by_tag[i].get_samples()[1, :]
            BR = cropped_by_tag[i].get_samples()[2, :]
            BL = cropped_by_tag[i].get_samples()[3, :]
            TIME = cropped_by_tag[i].get_samples()[4, :]
            # print((cropped_by_tag[i].get_start_tag()['desc']['value']))
            # print(type(cropped_by_tag[i].get_start_tag()['desc']['value']))
            # print(type(tempDict))
            # labels.append(tempDict)

            x = ((TR+BR) - (TL+BL)) / (TR+TL+BR+BL)
            y = ((TR+TL) - (BR+BL)) / (TR+TL+BR+BL)
            TIME -= min(TIME)

            x = x * 22.5  # Convert to cm
            y = y * 13  # Convert to cm

            data[tempDict['direction']] = np.array([TIME, x, y])

    return data
###############################################################################
# Function that takes the file name and tags to return the data trimmed using
# the tags provided. If no tags provided the function calls file2dataNoTags
#
#
# For measurements with n tags, returns an n-dimensional ndarray consisting of
# n x 3-dim arrays structured as follows:
#               data[0] being the time values
#               data[1] being the x values in cm
#               data[2] being the y values in cm
#
###############################################################################


def file2data(fileName, tags):

    # print(tags)
    if tags[0] == "" or tags[1] == "":
        return file2dataNoTags(fileName)
    wbr = read.ReadManager(fileName+'.obci.xml', fileName+'.obci.raw',
                           fileName + '.obci.tag')
    cropped_by_tag = wii_cut_fragments(wbr, start_tag_name=tags[0],
                                       end_tags_names=[tags[1]])
    dimTags = len(cropped_by_tag)
    data = np.ndarray(shape=(dimTags), dtype=object)
    for i in range(0, dimTags):
        TL = cropped_by_tag[i].get_samples()[0, :]
        TR = cropped_by_tag[i].get_samples()[1, :]
        BR = cropped_by_tag[i].get_samples()[2, :]
        BL = cropped_by_tag[i].get_samples()[3, :]
        TIME = cropped_by_tag[i].get_samples()[4, :]

        x = ((TR+BR) - (TL+BL)) / (TR+TL+BR+BL)
        y = ((TR+TL) - (BR+BL)) / (TR+TL+BR+BL)

        x = x * 22.5  # Convert to cm
        y = y * 13  # Convert to cm
        TIME -= min(TIME)

        data[i] = np.array([TIME, x, y])

    return data


###############################################################################
# Function Analyses data for Static mesurements with eyes closed and open
#
# Returns COP = [COP_x, COP_y] for further analysis
#
###############################################################################


def analysisStatic(measur, path4romberg=None):
    raw_data = file2data(measur.fileName, measur.tagData.tags)[0]
    t = raw_data[0] - min(raw_data[0])
    x = raw_data[1]
    y = raw_data[2]
    maxSwayAP = max(abs(max(x)), abs(min(x)))
    maxSwayML = max(abs(max(y)), abs(min(y)))
    deltaX = (x[1:] - x[:-1])
    deltaY = (y[1:] - y[:-1])
    deltaT = (t[1:] - t[:-1])
    mean_vAP = np.mean(deltaX/deltaT)
    mean_vML = np.mean(deltaY/deltaT)
    valueCOP = [np.average(x), np.average(y)]
    lengthAP = np.sum(abs(deltaX))
    lengthML = np.sum(abs(deltaY))
    folder = os.path.abspath('../') + '/Data/Results/'
    stillFile = open(folder + "Analysis_results.txt", 'a')
    stillFile.write("Data for standing still with " +
                    measur.tagData.title + '\n')
    stillFile.write("----------------------------------------"*2 + '\n')
    stillFile.write('\n')
    stillFile.write('\n')
    stillFile.write("Maximal Sway in AP plane: " + str(maxSwayAP) + " cm" +
                    '\n')
    stillFile.write("Maximal Sway in ML plane: " + str(maxSwayML) + " cm" +
                    '\n')
    stillFile.write("Mean Velocity in AP plane: " + str(mean_vAP) + " cm/s" +
                    '\n')
    stillFile.write("Mean Velocity in ML plane: " + str(mean_vML) + " cm/s" +
                    '\n')
    stillFile.write("Path Length in AP plane: " + str(lengthAP) + " cm" + '\n')
    stillFile.write("Path Length in ML plane: " + str(lengthML) + " cm" + '\n')
    stillFile.write("Path Length in ML plane: " + str(lengthML) + " cm" + '\n')
    stillFile.write("========================================"*2 + '\n'*2)

    # Plot COP wander path
    plt.plot(x, y, 'o-')
    filename = measur.title + '_' + measur.tagData.title + '_XYpath.png'
    plt.title(filename[:-4])
    plt.savefig(folder + filename, dpi=300, bbox_inches='tight')
    # plt.show()
    plt.close()

    # Plot COP_x(t)
    plt.plot(t, x, 'o-')
    filename = measur.title + '_' + measur.tagData.title + '_XinTime.png'
    plt.title(filename[:-4])
    plt.savefig(folder + filename, dpi=300, bbox_inches='tight')
    # plt.show()

    # Plot COP_y(t)
    plt.plot(t, y, 'o-')
    filename = measur.title + '_' + measur.tagData.title + '_YinTime.png'
    plt.title(filename[:-4])
    plt.savefig(folder + filename, dpi=300, bbox_inches='tight')
    # plt.show()
    plt.close()

    # Histogram of COP points
    plt.hist2d(x, y)
    filename = measur.title + '_' + measur.tagData.title + '_XYhisto.png'
    plt.title(filename[:-4])
    plt.savefig(folder + filename, dpi=300, bbox_inches='tight')
    # plt.show()
    plt.close()

    # Histogram of COP_x
    plt.hist(x)
    filename = measur.title + '_' + measur.tagData.title + '_Xhisto.png'
    plt.title(filename[:-4])
    plt.savefig(folder + filename, dpi=300, bbox_inches='tight')
    # plt.show()
    plt.close()

    # Histogram of COP_y
    plt.hist(y)
    filename = measur.title + '_' + measur.tagData.title + '_Yhisto.png'
    plt.title(filename[:-4])
    plt.savefig(folder + filename, dpi=300, bbox_inches='tight')
    # plt.show()
    plt.close()

    print("COP: " + str(valueCOP))
    if (path4romberg is not None):
        rombergSum = (sum(path4romberg) - lengthAP - lengthML) / \
            (sum(path4romberg) + lengthAP + lengthML)
        rombergX = (path4romberg[0] - lengthAP) / \
            (path4romberg[0] + lengthAP)
        rombergY = (path4romberg[0] - lengthAP) / \
            (path4romberg[0] + lengthAP)
        stillFile.write("****************************************" + '\n')
        stillFile.write("Romberg coefficient for sum: "
                        + str(rombergSum) + '\n')
        stillFile.write("Romberg coefficient for X: "
                        + str(rombergX) + '\n')
        stillFile.write("Romberg coefficient for Y: "
                        + str(rombergY) + '\n')
        stillFile.write("****************************************" + '\n'*2)
    paths_xy = [lengthAP, lengthML]
    valuesOfInterest = [valueCOP, paths_xy]
    return valuesOfInterest


###############################################################################
# Function Analyses data for Sway measurements both Fast and sway&stay
#
# void type of function
#
###############################################################################


def analysisSway(measur, COP):
    # Should be save for Fast and Stay variants, haven't checked
    raw_data_Sway = file2data(measur.fileName,
                              measur.tagData.tags)
    dimData = len(raw_data_Sway)
    # Calculate max displacement for each fast measurement
    x = np.ndarray(shape=(dimData), dtype=np.ndarray)
    y = np.ndarray(shape=(dimData), dtype=np.ndarray)
    t = np.ndarray(shape=(dimData), dtype=np.ndarray)
    swayX_max = np.zeros(dimData)
    swayY_max = np.zeros(dimData)
    # print(type(raw_data_Sway[0][0]) is np.float64)
    # print(type(raw_data_Sway[0][0]))
    # print(raw_data_Sway)
    if type(raw_data_Sway[0][0]) is np.float64:
        t = raw_data_Sway[0]
        x = raw_data_Sway[1]
        y = raw_data_Sway[2]
        plt.plot(x, y)
    else:
        print(len(raw_data_Sway))
        for i in range(0, len(raw_data_Sway)):
            t[i] = raw_data_Sway[i][0]
            x[i] = raw_data_Sway[i][1]
            y[i] = raw_data_Sway[i][2]
            # convert time to relative time
            plt.plot(x[i], y[i])
            swayX_max[i] = max(abs(x[i]))
            swayY_max[i] = max(abs(y[i]))
            # Correct for COP
    swayX_max -= COP[0]
    swayY_max -= COP[1]

    # Print to file
    folder = os.path.abspath('../') + '/Data/Results/'
    stillFile = open(folder + 'Analysis_results.txt', 'a')
    for i in range(0, len(swayX_max)):
        stillFile.write("Data for " + measur.title +
                        measur.tagData.title + '\n')
        stillFile.write("----------------------------------------"*2 + '\n')
        stillFile.write('\n')
        stillFile.write('\n')
        stillFile.write("Maximal Sway in AP plane: " + str(swayX_max[i]) +
                        " cm" + '\n')
        stillFile.write("Maximal Sway in ML plane: " + str(swayY_max[i]) +
                        " cm" + '\n')
        stillFile.write("========================================"*2 + '\n')
        stillFile.write('\n')

    # Plot for COP wandering path
    filename = measur.title + '_' + measur.tagData.title + '_XYpath.png'
    plt.title(filename[:-4])
    plt.savefig(folder + filename, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    # Plot for COP_x(t)
    if (type(raw_data_Sway[0][0]) is np.float64):
        plt.plot(t, x-COP[0])
    else:
        for dataSet in raw_data_Sway:
            plt.plot(dataSet[0], dataSet[1]-COP[0])
    filename = measur.title + '_' + measur.tagData.title + '_Xontime.png'
    plt.title(filename[:-4])
    plt.savefig(folder + filename)  # , dpi=300, bbox_inches='tight')
    plt.show()
    plt.clf()

    # Plot for COP_y(t)
    if (type(raw_data_Sway[0][0]) is np.float64):
        plt.plot(t, y-COP[1])
    else:
        for dataSet in raw_data_Sway:
            plt.plot(dataSet[0], dataSet[2]-COP[1])
    filename = measur.title + '_' + measur.tagData.title + '_Yontime.png'
    plt.title(filename[:-4])
    plt.savefig(folder + filename, dpi=300, bbox_inches='tight')
    plt.show()
    plt.clf()

###############################################################################
# Initialise the data according to the filename existing in '../Data/' folder
#
# This function is highly personal and is here only to make the
# 'analysisWiiBoard.py' more readeable
#
# returns a list of 'Measurement' objects
#
###############################################################################


def initialiseData():
    # I know it's ugly but it cannot be much prettier with so much 'manual'
    # input, can it?
    allTheFiles = [os.path.abspath('../')+'/Data/']*7
    allTheFiles[0] += "still_eyes_closed_eyes_open"
    allTheFiles[1] += "sway_back"
    allTheFiles[2] += "sway_forward"
    allTheFiles[3] += "sway_left"
    allTheFiles[4] += "sway_right"
    allTheFiles[5] += "sway_with_feedback"
    allTheFiles[6] += "sway_stay_with_feedback"
    measurementList = np.ndarray(13, dtype=object)
    measurementList[0] = Measurement("Static_Measurement", allTheFiles[0],
                                     TagObject("Eyes_open",
                                               "ss_start", "ss_stop"))
    measurementList[1] = Measurement("Static_Measurement", allTheFiles[0],
                                     TagObject("Eyes_closed",
                                               'ss_eyes_closed_start',
                                               'ss_eyes_closed_stop'))
    measurementList[2] = Measurement("Sway_Back", allTheFiles[1],
                                     TagObject("Fast",
                                               "start_fast", "stop_fast"))
    measurementList[3] = Measurement("Sway_Back", allTheFiles[1],
                                     TagObject("Stay", "start", "stop"))
    measurementList[4] = Measurement("Sway_Forward", allTheFiles[2],
                                     TagObject("Fast", "start_fast",
                                               "stop_fast"))
    measurementList[5] = Measurement("Sway_Forward", allTheFiles[2],
                                     TagObject("Stay", "start", "stop"))
    measurementList[6] = Measurement("Sway_Left", allTheFiles[3],
                                     TagObject("Fast", "start_fast",
                                               "stop_fast"))
    measurementList[7] = Measurement("Sway_Left", allTheFiles[3],
                                     TagObject("Stay", "start", "stop"))
    measurementList[8] = Measurement("Sway_Right", allTheFiles[4],
                                     TagObject("Fast", "start_fast",
                                               "stop_fast"))
    measurementList[9] = Measurement("Sway_Right", allTheFiles[4],
                                     TagObject("Stay", "start", "stop"))
    measurementList[10] = Measurement("Feeback Measurement", allTheFiles[5],
                                      TagObject("Baseline", "baseline_start",
                                                "baseline_stop"))
    measurementList[11] = Measurement("Feeback Measurement", allTheFiles[5],
                                      TagObject("Fast", "", ""))
    measurementList[12] = Measurement("Feeback Measurement", allTheFiles[6],
                                      TagObject("Stay", "start_1", "finish"))
    return measurementList
