# import os.path
from utils import analysisStatic, analysisSwayGame, \
    initialiseData, analysisSway  # , Measurement, TagObject, file2data,
# import numpy as np
# import matplotlib.pyplot as plt


measurementList = initialiseData()

# Static Eyes Open
valuesWanted = analysisStatic(measurementList[0])
calibrationCOP = valuesWanted[0]

# Static Eyes Closed
analysisStatic(measurementList[1], valuesWanted[1])

'''
# Analyse Sways
for measurement in measurementList[10:]:
    # measurement = measurementList[12]
    print(measurement.title)
    print(measurement.tagData.title)
    analysisSway(measurement, calibrationCOP)
    '''
analysisSwayGame(measurementList[11], valuesWanted[1])

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
