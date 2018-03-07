import os.path
from utils import Measurement, TagObject, file2data
import numpy as np
import matplotlib.pyplot as plt


def initialiseData():
    allTheFiles = [os.path.abspath('../')+'/Data/']*7
    allTheFiles[0] += "still_eyes_closed_eyes_open"
    allTheFiles[1] += "sway_back"
    allTheFiles[2] += "sway_forward"
    allTheFiles[3] += "sway_left"
    allTheFiles[4] += "sway_right"
    allTheFiles[5] += "sway_stay_with_feedback"
    allTheFiles[6] += "sway_with_feedback"
    measurementList = np.ndarray(23, dtype=object)
    measurementList[0] = Measurement("Static Measurement", allTheFiles[0],
                                     TagObject("Eyes open",
                                               "ss_start", "ss_stop"))
    measurementList[1] = Measurement("Static Measurement", allTheFiles[0],
                                     TagObject("Eyes closed",
                                               "ss_start", "ss_stop"))
    measurementList[2] = Measurement("Sway Back", allTheFiles[1],
                                     TagObject("Eyes closed",
                                               "ss_start", "ss_stop"))
    measurementList[3] = Measurement("Sway Back", allTheFiles[1],
                                     TagObject("Fast 1",
                                               "start_fast", "stop_fast"))
    measurementList[4] = Measurement("Sway Back", allTheFiles[1],
                                     TagObject("Fast 2",
                                               "start_fast", "stop_fast"))
    measurementList[5] = Measurement("Sway Back", allTheFiles[1],
                                     TagObject("Fast 3",
                                               "start_fast", "stop_fast"))
    measurementList[6] = Measurement("Sway Back", allTheFiles[1],
                                     TagObject("Stay", "start", "stop"))
    measurementList[7] = Measurement("Sway Back", allTheFiles[1],
                                     TagObject("Eyes closed",
                                               "ss_start", "ss_stop"))
    measurementList[8] = Measurement("Sway Forward", allTheFiles[2],
                                     TagObject("Fast 1",
                                               "start_fast", "stop_fast"))
    measurementList[9] = Measurement("Sway Forward", allTheFiles[2],
                                     TagObject("Fast 2",
                                               "start_fast", "stop_fast"))
    measurementList[10] = Measurement("Sway Forward", allTheFiles[2],
                                      TagObject("Fast 3",
                                                "start_fast", "stop_fast"))
    measurementList[11] = Measurement("Sway Forward", allTheFiles[2],
                                      TagObject("Stay", "start", "stop"))
    measurementList[12] = Measurement("Sway Left", allTheFiles[3],
                                      TagObject("Fast 1",
                                                "start_fast", "stop_fast"))
    measurementList[13] = Measurement("Sway Left", allTheFiles[3],
                                      TagObject("Fast 2",
                                                "start_fast", "stop_fast"))
    measurementList[14] = Measurement("Sway Left", allTheFiles[3],
                                      TagObject("Fast 3",
                                                "start_fast", "stop_fast"))
    measurementList[15] = Measurement("Sway Left", allTheFiles[3],
                                      TagObject("Stay", "start", "stop"))
    measurementList[16] = Measurement("Sway Right", allTheFiles[4],
                                      TagObject("Fast 1",
                                                "start_fast", "stop_fast"))
    measurementList[17] = Measurement("Sway Right", allTheFiles[4],
                                      TagObject("Fast 2",
                                                "start_fast", "stop_fast"))
    measurementList[18] = Measurement("Sway Right", allTheFiles[4],
                                      TagObject("Fast 3",
                                                "start_fast", "stop_fast"))
    measurementList[19] = Measurement("Sway Right", allTheFiles[4],
                                      TagObject("Stay", "start", "stop"))
    measurementList[20] = Measurement("Feeback Measurement", allTheFiles[5],
                                      TagObject("Baseline",
                                                "baseline_start",
                                                "baseline_stop"))
    measurementList[21] = Measurement("Feeback Measurement", allTheFiles[5],
                                      TagObject("Fast", "", ""))
    measurementList[22] = Measurement("Feeback Measurement", allTheFiles[6],
                                      TagObject("Stay", "start_1", "finish"))
    return measurementList


measurementList = initialiseData()
for measurement in measurementList:
    currentData = file2data(measurement.fileName, measurement.tagData.tags)
    # create a subplot
    currentData[0] -= min(currentData[0])
    plt.plot(currentData[1], currentData[2], 'o-')
    plt.title(measurement.title + " " + measurement.tagData.title)
    # plt.axis([-22.5, 22.5, -13, 13])
    plt.show()
