import os.path
import myUtils as fnc
import numpy as np
# import matplotlib
# matplotlib.use('pdf')
import matplotlib.pyplot as plt

myDPI = 100


file_name = os.path.abspath('../') + '/Data/' + 'kinect_recording_alvar'
time, joints = fnc.getJointData(file_name)
rFoot        = fnc.getRightFoot(joints)
lFoot        = fnc.getLeftFoot(joints)
rKnee        = fnc.getRightKnee(joints)
lKnee        = fnc.getLeftKnee(joints)
head         = fnc.getHead(joints)
neck         = fnc.getNeck(joints)
torso        = fnc.getTorso(joints)
rHip         = fnc.getRightHip(joints)
lHip         = fnc.getLeftHip(joints)
rHand        = fnc.getRightHand(joints)
lHand        = fnc.getLeftHand(joints)
rElbow       = fnc.getRightElbow(joints)
lElbow       = fnc.getLeftElbow(joints)
rShoulder    = fnc.getRightShoulder(joints)
lShoulder    = fnc.getLeftShoulder(joints)


'''
rFoot        = fnc.commonBegining(rFoot)
lFoot        = fnc.commonBegining(lFoot)
rKnee        = fnc.commonBegining(rKnee)
lKnee        = fnc.commonBegining(lKnee)
head         = fnc.commonBegining(head)
neck         = fnc.commonBegining(neck)
torso        = fnc.commonBegining(torso)
rHip         = fnc.commonBegining(rHip)
lHip         = fnc.commonBegining(lHip)
rHand        = fnc.commonBegining(rHand)
lHand        = fnc.commonBegining(lHand)
rElbow       = fnc.commonBegining(rElbow)
lElbow       = fnc.commonBegining(lElbow)
rShoulder    = fnc.commonBegining(rShoulder)
lShoulder    = fnc.commonBegining(lShoulder)
'''




rFoot = fnc.meaningFullOnly(rFoot, 3.5)
lFoot = fnc.meaningFullOnly(lFoot, 3.5)
rKnee = fnc.meaningFullOnly(rKnee, 3.5)
lKnee = fnc.meaningFullOnly(lKnee, 3.5)
head =  fnc.meaningFullOnly(head , 3.5)
neck =  fnc.meaningFullOnly(neck , 3.5)
torso = fnc.meaningFullOnly(torso, 3.5)
rHip = fnc.meaningFullOnly(rHip, 3.5)
lHip = fnc.meaningFullOnly(lHip, 3.5)
rHand = fnc.meaningFullOnly(rHand, 3.5)
lHand = fnc.meaningFullOnly(lHand, 3.5)
rElbow = fnc.meaningFullOnly(rElbow, 3.5)
lElbow = fnc.meaningFullOnly(lElbow, 3.5)
rShoulder = fnc.meaningFullOnly(rShoulder, 3.5)
lShoulder = fnc.meaningFullOnly(lShoulder, 3.5)
time = time[-len(rFoot[0]):]

# PLOT ALL DATA
plt.figure(figsize=(16, 9))
plt.plot(time, fnc.commonBegining(rFoot)[1], label='Right Foot')
plt.plot(time, fnc.commonBegining(lFoot)[1], label='Left Foot')
plt.plot(time, fnc.commonBegining(rKnee)[1], label='Right Knee')
plt.plot(time, fnc.commonBegining(lKnee)[1], label='Left Knee')
plt.plot(time, fnc.commonBegining(head)[1], label='Head')
plt.plot(time, fnc.commonBegining(neck)[1], label='Neck')
plt.plot(time, fnc.commonBegining(torso)[1], label='Torso')
plt.plot(time, fnc.commonBegining(rHip)[1], label='Right Hip')
plt.plot(time, fnc.commonBegining(lHip)[1], label='Left Hip')
plt.plot(time, fnc.commonBegining(rHand)[1], label='Right Hand')
plt.plot(time, fnc.commonBegining(lHand)[1], label='Left Hand')
plt.plot(time, fnc.commonBegining(rElbow)[1], label='Right Elbow')
plt.plot(time, fnc.commonBegining(lElbow)[1], label='Left Elbow')
plt.plot(time, fnc.commonBegining(rShoulder)[1], label='Right Shoudler')
plt.plot(time, fnc.commonBegining(lShoulder)[1], label='Left Shoulder')
plt.legend(loc='best')
plt.xlabel('Time / s')
name = "All_data_Y-axis"
plt.title(name)
plt.savefig(name+'.png', dpi=myDPI)
# plt.show()
# PLOT ONE JUMP
plt.axis([13, 18, -800, 1050])
plt.legend(loc='upper left')
name += '_One_Jump'
plt.title(name)
plt.savefig(name+'.png', dpi=myDPI)
#plt.show()
plt.close()

# PLOT HEAD
plt.plot(time, head[1], label='Head')
plt.xlabel('Time / s')
name = "Head_Y-Axis"
plt.title(name)
plt.savefig(name+'.png')

# PLOT HEAD w/ KNEE AND FOOT
plt.plot(time, rKnee[1], label='Right Knee')
plt.plot(time, rFoot[1], label='Right Foot')
plt.legend(loc='upper left')
name = "Y-Axis_compare_Head_Knee_Foot_one_side"
plt.title(name)
plt.savefig(name+'.png', dpi=myDPI)
# plt.show()
plt.close()

# PLOT HEAD w/ TORSO-FOOT DIFF

name = "Y-Axis_Head_Torso2Foot_diff"
# plt.plot(time, head[1], 'g', label='Head')
plt.plot(time, fnc.commonBegining(rFoot)[1], 'g', label='Foot')
pfKnee = fnc.getPFindex(rKnee, lKnee, rFoot, lFoot)
# plt.plot(np.full(100, time[pfKnee]), np.linspace(-1000, 1000,100), 'g-', label='PfKNEE')
plt.plot(time, fnc.commonBegining(rKnee)[1], label='Right Knee')
plt.plot(time, fnc.commonBegining(rHip)[1], label='Right Hip')
plt.legend(loc='best')
plt.title(name)
plt.savefig(name+'.png', dpi=myDPI)
#plt.show()
plt.close()



########
# Calculate PF for each jump and valgus analysis
########


separator = fnc.getJumpStart(torso, rFoot)
rKnee_cut = fnc.splitJumps(rKnee, separator)
lKnee_cut = fnc.splitJumps(lKnee, separator)
rFoot_cut = fnc.splitJumps(rFoot, separator)
lFoot_cut = fnc.splitJumps(lFoot, separator)
time_cut = fnc.splitJumps(time, separator)
for i in range(len(separator)):
    pfPoint = fnc.getPFindex(rKnee_cut[i], lKnee_cut[i], rFoot_cut[i],
                             lFoot_cut[i])
    print('in main file pfReturned is: {0}'.format(pfPoint))
    plt.plot(time_cut[i], rKnee_cut[i][1], 'b')
    plt.plot(time_cut[i], lKnee_cut[i][1], 'r')
    plt.plot(time_cut[i], rFoot_cut[i][1], 'g')
    plt.plot(time_cut[i], lFoot_cut[i][1], 'k')
    plt.plot(np.full(100, time_cut[i][pfPoint]), np.linspace(-1000, 1000, 100),
             'g-', label='PfKNEE')
plt.show()



'''



pfPoint = fnc.getPFindex(rKnee, lKnee, rFoot, lFoot)
separator = fnc.getJumpStart(torso, rFoot)
rKnee_jumps = fnc.splitJumps(rKnee, separator)
time_jumps = fnc.splitJumps(time, separator)
plt.plot(time, rKnee[1], 'g', label='Right Foot')
for i in range(len(rKnee_jumps)):
    plt.plot(time_jumps[i], rKnee_jumps[i][1], '*m')
plt.show()
plt.clf







rSide = fnc.getRealDiff(rKnee, rFoot)
lSide = fnc.getRealDiff(lKnee, lFoot)
starts = fnc.getJumpStart(torso, rFoot)
# torso_knee = getRealDiff(meaningFullOnly(getTorso(joints)), rKnee)
rtorso_foot = fnc.getRealDiff(fnc.meaningFullOnly(fnc.getTorso(joints)), rFoot)
ltorso_foot = fnc.getRealDiff(fnc.meaningFullOnly(fnc.getTorso(joints)), lFoot)
lhip_knee = fnc.getRealDiff(fnc.meaningFullOnly(fnc.getLeftHip(joints)), lKnee)
quickPF = np.argmin(rSide)
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
