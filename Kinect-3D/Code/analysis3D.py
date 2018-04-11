import os.path
from myUtils import *
# import matplotlib
# matplotlib.use('pdf')
import matplotlib.pyplot as plt


file_name = os.path.abspath('../') + '/Data/' + 'kinect_recording_alvar'
time, joints = getJointData(file_name)
rFoot = getRightFoot(joints)
lFoot = getLeftFoot(joints)
rKnee = getRightKnee(joints)
time = time[-len(rFoot[0]):]
plt.plot(time, rFoot[1], 'g', label='Right Foot')
plt.plot(time, rKnee[1], 'r', label='Knee')
plt.plot(time, lFoot[1], 'b', label='Left Foot')
plt.legend(loc='best')
plt.show()
'''
rKnee = getRightKnee(joints)
time = time[-len(rKnee[0]):]
plt.plot(time, rKnee[0], 'm', label='x')
plt.plot(time, rKnee[1], 'g', label='y')
plt.plot(time, rKnee[2], 'b', label='z')
plt.title("Right Knee")
plt.legend(loc='best')
plt.show()

lKnee = getLeftKnee(joints)
plt.plot(time, lKnee[0], 'm', label='x')
plt.plot(time, lKnee[1], 'g', label='y')
plt.plot(time, lKnee[2], 'b', label='z')
plt.title("Left Knee")
plt.legend(loc='best')
plt.show()
# print(lKnee[0][1153:])

'''
