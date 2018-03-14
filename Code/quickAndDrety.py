import numpy as np
from utils import file2data, analysisStatic, initialiseData, analysisSway
# TagObject, Measurement,
import matplotlib.pyplot as plt

measurementList = initialiseData()

# Feeback baseline data

raw_values = file2data(measurementList[11].fileName,
                       measurementList[11].tagData.tags)

t = raw_values[0]
x = raw_values[1]
y = raw_values[2]

COP = [np.mean(x), np.mean(y)]

analysisSway(measurementList[11], COP)

'''
plt.plot(x, y, 'o-')
x -= np.mean(x)
y -= np.mean(y)
plt.plot(x, y, 'x-')
plt.plot([0], [0], 'o')
plt.show()
# plt.axis([-11.3, 11.3, -6.5, 6.5])
# plt.show()
plt.hist2d(x, y, bins=150)
# plt.axis([-11.3, 11.3, -6.5, 6.5])
plt.show()




'''
