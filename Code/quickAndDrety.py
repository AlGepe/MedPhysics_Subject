import os.path
import matplotlib.pyplot as plt
from obci_readmanager.signal_processing import read_manager as read
import numpy as np
from obci_readmanager.signal_processing.balance.wii_preprocessing import *
# from obci_readmanager.signal_processing.balance.wii_analysis import *
from utils import file2data, analysisStatic, initialiseData, analysisSway, \
    file2dataGame
# TagObject, Measurement,
import matplotlib.pyplot as plt

measurementList = initialiseData()

# Feeback baseline data

dict_values = file2dataGame(measurementList[12].fileName,
                            measurementList[12].tagData.tags)

# print(type(labels[0]))
print(dict_values)

'''
for dataSet in data:
    t = dataSet[0]
    x = dataSet[1]
    y = dataSet[2]
    plt.plot(x, y, 'o-')
    plt.show()

COP = [np.mean(x), np.mean(y)]

analysisSway(measurementList[11], COP)

plt.plot(x, y, 'o-')
x -= np.mean(x)
y -= np.mean(y)
plt.plot(x, y, 'x-')
plt.plot([0], [0], 'o')
plt.show()
# plt.axis([-11.3, 11.3, -6.5, 6.5])
# plt.show()
plt.hist2d(x, y, bins=50)
# plt.axis([-11.3, 11.3, -6.5, 6.5])
plt.show()
'''
