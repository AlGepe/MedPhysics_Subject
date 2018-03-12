import os.path
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

        data[i] = np.array([TIME, x, y])

    return data


def analysisStatic(measurement):
    raw_data = file2data(measurement.fileName, measurement.tagData.tags)[0]
    t = raw_data[0]
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
    stillFile = open('Analysis_results.txt', 'a')
    stillFile.write("Data for standing still with " +
                    measurement.tagData.title + '\n')
    stillFile.write("----------------------------------------"*2 + '\n')
    stillFile.write('\n')
    stillFile.write('\n')
    stillFile.write("Maximal Sway in AP plane: " + str(maxSwayAP) + " cm" +
                    '\n')
    stillFile.write("Maximal Sway in ML plane: " + str(maxSwayML) + " cm" +
                    '\n')
    stillFile.write("Mean Velocity in AP plane: " + str(mean_vAP) + " cm" +
                    '\n')
    stillFile.write("Mean Velocity in ML plane: " + str(mean_vML) + " cm" +
                    '\n')
    stillFile.write("Path Length in AP plane: " + str(lengthAP) + " cm" + '\n')
    stillFile.write("Path Length in ML plane: " + str(lengthML) + " cm" + '\n')
    stillFile.write("========================================"*2 + '\n'*2)

    # Graphs of motion in AP, ML and AP/ML
    # Histogram of COP points
    print("COP: " + str(valueCOP))
    return valueCOP


def analysisSway(measurement):
    raw_data = file2data(measurement.fileName, measurement.tagData.tags)
    for dataSet in raw_data:
        t = dataSet[0]
        x = dataSet[1]
        y = dataSet[2]


def initialiseData():
    allTheFiles = [os.path.abspath('../')+'/Data/']*7
    allTheFiles[0] += "still_eyes_closed_eyes_open"
    allTheFiles[1] += "sway_back"
    allTheFiles[2] += "sway_forward"
    allTheFiles[3] += "sway_left"
    allTheFiles[4] += "sway_right"
    allTheFiles[5] += "sway_stay_with_feedback"
    allTheFiles[6] += "sway_with_feedback"
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