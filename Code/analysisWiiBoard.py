# import os.path
from utils import file2data, analysisStatic, \
    initialiseData, analysisSway  # , Measurement, TagObject
# import numpy as np
import matplotlib.pyplot as plt


measurementList = initialiseData()

# Static Eyes Open
calibrationCOP = analysisStatic(measurementList[0])

# Static Eyes Closed
analysisStatic(measurementList[1])

# Analyse Sways
for measurement in measurementList[4:10]:
    print(measurement.title)
    print(measurement.tagData.title)
    analysisSway(measurement, calibrationCOP)

# Graphs of motion in AP, ML and AP/ML
# Histogram of COP points
'''
for measurement in measurementList:
    currentData = file2data(measurement.fileName, measurement.tagData.tags)
    # create a subplot
    currentData[0] -= min(currentData[0])
    plt.plot(currentData[1], currentData[2], 'o-')
    plt.title(measurement.title + " " + measurement.tagData.title)
    # plt.axis([-22.5, 22.5, -13, 13])
    plt.show()
    '''
