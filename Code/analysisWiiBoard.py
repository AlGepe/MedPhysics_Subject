import os.path
from utils import Measurement,\
    TagObject, file2data, analysisStatic, initialiseData
import numpy as np
import matplotlib.pyplot as plt


measurementList = initialiseData()

# Static Eyes Open
analysisStatic(measurementList[0])

# Static Eyes Closed
analysisStatic(measurementList[1])

# Analyse Sways
for measurement in measurementList[2:10]:
    analysisSway(measurement)



# Repeat for eyes closed
stillFile.write("Data for standing still with eyes OPEN")
stillFile.write('\n')
stillFile.write("Maximal Sway in AP plane: " + str(maxSwayAP) + " cm")
stillFile.write("Maximal Sway in ML plane: " + str(maxSwayML) + " cm")
stillFile.write("Mean Velocity in AP plane: " + str(mean_vAP) + " cm")
stillFile.write("Mean Velocity in ML plane: " + str(mean_vML) + " cm")
stillFile.write("Path Length in AP plane: " + str(lengthAP) + " cm")
stillFile.write("Path Length in ML plane: " + str(lengthML) + " cm")

# Graphs of motion in AP, ML and AP/ML
# Histogram of COP points


for measurement in measurementList:
    currentData = file2data(measurement.fileName, measurement.tagData.tags)
    # create a subplot
    currentData[0] -= min(currentData[0])
    plt.plot(currentData[1], currentData[2], 'o-')
    plt.title(measurement.title + " " + measurement.tagData.title)
    # plt.axis([-22.5, 22.5, -13, 13])
    plt.show()


