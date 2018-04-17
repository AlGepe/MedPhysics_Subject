import os.path
from myUtils import *
import matplotlib
# matplotlib.use('pdf')
import matplotlib.pyplot as plt


file_name = os.path.abspath('../') + '/Data/' + 'kinect_recording_alvar'
time, joints = getJointData(file_name)
rFoot = commonBegining(getRightFoot(joints))
lFoot = commonBegining(getLeftFoot(joints))
rKnee = commonBegining(getRightKnee(joints))
head = commonBegining(getHead(joints))
neck = commonBegining(getNeck(joints))
time = time[-len(rFoot[0]):]
plt.plot(time, rFoot[1], 'g', label='Right Foot')
plt.plot(time, head[1], 'm', label='Head')
plt.plot(time, neck[1], 'k+', label='Neck')
plt.plot(time, rKnee[1], 'r', label='Knee')
plt.plot(time, lFoot[1], 'b', label='Left Foot')
plt.legend(loc='best')
name = 'Feet_1knee_visualCI-PF'
plt.title(name)
# print(time[33]-time[0])
plt.show()
plt.savefig(name + '.png')
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
