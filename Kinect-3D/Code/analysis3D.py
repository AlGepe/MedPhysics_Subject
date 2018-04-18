import os.path
from myUtils import *
import matplotlib
# matplotlib.use('pdf')
import matplotlib.pyplot as plt


file_name = os.path.abspath('../') + '/Data/' + 'kinect_recording_alvar'
time, joints = getJointData(file_name)
rFoot = getRightFoot(joints)
lFoot = getLeftFoot(joints)
rKnee = getRightKnee(joints)
lKnee = getLeftKnee(joints)
head = getHead(joints)
neck = getNeck(joints)
torso = getTorso(joints)

rFoot = meaningFullOnly(rFoot, 3.5)
lFoot = meaningFullOnly(lFoot, 3.5)
rKnee = meaningFullOnly(rKnee, 3.5)
lKnee = meaningFullOnly(lKnee, 3.5)
head =  meaningFullOnly(head , 3.5)
neck =  meaningFullOnly(neck , 3.5)
torso = meaningFullOnly(torso, 3.5)
'''
rFoot = commonBegining(rFoot)
lFoot = commonBegining(lFoot)
rKnee = commonBegining(rKnee)
lKnee = commonBegining(lKnee)
head =  commonBegining(head)
neck =  commonBegining(neck)
'''
pfPoint = getPFindex(rKnee, lKnee, rFoot, lFoot)


rSide = getRealDiff(rKnee, rFoot)
lSide = getRealDiff(lKnee, lFoot)
starts = getJumpStart(torso, rFoot)
# torso_knee = getRealDiff(meaningFullOnly(getTorso(joints)), rKnee)
rtorso_foot = getRealDiff(meaningFullOnly(getTorso(joints)), rFoot)
ltorso_foot = getRealDiff(meaningFullOnly(getTorso(joints)), lFoot)
lhip_knee = getRealDiff(meaningFullOnly(getLeftHip(joints)), lKnee)
quickPF = np.argmin(rSide)
time = time[-len(rFoot[0]):]
plt.plot(time, rFoot[1], 'g', label='Right Foot')
plt.plot(time, rSide[1], 'g', label='rSide')
# plt.plot(time, torso_knee[1], 'b', label='Torso_Knee')
plt.plot(time, rtorso_foot[1], 'r', label='Right_T2F')
# plt.plot(time, ltorso_foot[1], 'g', label='Left_T2F')
# plt.plot(time, lhip_knee[1], 'r', label='Hip2Knee_left')
for index in starts:
    print(index)
    plt.plot(time[index], rtorso_foot[1][index], 'b^', markersize='15')
plt.plot(time, head[1], 'm', label='Head')
# plt.plot(time, neck[1], 'k-+', label='Neck')
# plt.plot(time, rKnee[1], 'r', label='Knee')
# plt.plot(time, lSide[1], 'b+-', label='Left Side')
# plt.plot(time[pfPoint], head[1][pfPoint], 'mo', label='PF')
# plt.plot(time[quickPF], rFoot[1][quickPF], 'ro', label='quickPF')
# plt.plot(time, lFoot[1], 'b', label='Left Foot')
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
