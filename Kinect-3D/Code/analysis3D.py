import os.path
import myUtils as fnc
import numpy as np
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
folder = os.path.abspath('../') + '/Data/Results/'
filename = 'Result_Numbers.txt'


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

########
# Analysis of the data
########


separator = fnc.getJumpStart(torso, rFoot)
rKnee_cut = fnc.splitJumps(rKnee, separator)
lKnee_cut = fnc.splitJumps(lKnee, separator)
rFoot_cut = fnc.splitJumps(rFoot, separator)
lFoot_cut = fnc.splitJumps(lFoot, separator)
time_cut = fnc.splitJumps(time, separator)
nJumps = len(separator)
ic = np.zeros(nJumps, dtype=np.int)
pf = np.zeros(nJumps, dtype=np.int)
rKVM = np.zeros(nJumps)
lKVM = np.zeros(nJumps)
rFPKA_ic = np.zeros(nJumps)
lFPKA_ic = np.zeros(nJumps)
rFPKA_pf = np.zeros(nJumps)
lFPKA_pf = np.zeros(nJumps)
KASR = np.zeros(nJumps)

# Calculate all values
for i in range(nJumps):

    ic[i] = fnc.getICindex(rFoot_cut[i], rFoot_cut[i])
    pf[i] = fnc.getPFindex(rKnee_cut[i], lKnee_cut[i],
                           rFoot_cut[i], lFoot_cut[i])
    rKVM[i] = fnc.getKVM(rKnee_cut[i][0], ic[i], pf[i])
    lKVM[i] = fnc.getKVM(lKnee_cut[i][0], ic[i], pf[i])
    rFPKA_pf[i] = fnc.getFPKA(rKnee_cut[i], rFoot_cut[i], pf[i])
    lFPKA_pf[i] = fnc.getFPKA(lKnee_cut[i], lFoot_cut[i], pf[i])
    rFPKA_ic[i] = fnc.getFPKA(rKnee_cut[i], rFoot_cut[i], ic[i])
    lFPKA_ic[i] = fnc.getFPKA(lKnee_cut[i], lFoot_cut[i], ic[i])
    KASR[i] = fnc.getKASR(rKnee_cut[i][0], lKnee_cut[i][0],
                          rFoot_cut[i][0], lFoot_cut[i][0], pf[i])
outFile = open(folder + filename, 'w+')
outFile.write('########################################################\n')
outFile.write('#           KINECT 3D Camera Data Analysis             #\n') 
outFile.write('########################################################\n')

# Write to file
for i in range(nJumps): 
    outFile.write('\n')
    outFile.write('========================================================\n')
    outFile.write('=                 JUMP NUMBER ' + str(i) + '\n')
    outFile.write('========================================================\n')
    outFile.write('KVM for Right Side: ' + str(rKVM[i]) + '\n')
    outFile.write('KVM for Left  Side: ' + str(lKVM[i]) + '\n')
    outFile.write('\n')
    outFile.write('FPKA for Right Side at IC: ' + str(rFPKA_ic[i]) + '\n')
    outFile.write('FPKA for Left  Side at IC: ' + str(lFPKA_ic[i]) + '\n')
    outFile.write('FPKA for Right Side at PF: ' + str(rFPKA_pf[i]) + '\n')
    outFile.write('FPKA for Left  Side at PF: ' + str(lFPKA_pf[i]) + '\n')
    outFile.write('\n')
    outFile.write('KASR at PF: ' + str(KASR[i]) + '\n')

    if i == nJumps - 1:  # Last point, do averages
        outFile.write('\n')
        outFile.write('****************************************************\n')
        outFile.write('*             AVERAGE OVER 3 LAST JUMPS             \n')
        outFile.write('****************************************************\n')
        outFile.write('KVM Right Side: ' + str(np.average(rKVM[1:i])) + '\n')
        outFile.write('KVM Left  Side: ' + str(np.average(lKVM[1:i])) + '\n')
        outFile.write('\n')
        outFile.write('FPKA for Right Side at IC: ' +
                      str(np.average(rFPKA_ic[1:i])) + '\n')
        outFile.write('FPKA for Left  Side at IC: ' +
                      str(np.average(lFPKA_ic[1:i])) + '\n')
        outFile.write('FPKA for Right Side at PF: ' +
                      str(np.average(rFPKA_pf[1:i])) + '\n')
        outFile.write('FPKA for Left  Side at PF: ' +
                      str(np.average(lFPKA_pf[1:i])) + '\n')
        outFile.write('\n')
        outFile.write('KASR at PF: ' + str(np.average(KASR[1:i])) + '\n')

####################################
#          PLOT ALL DATA           #
####################################

#========================
# All data Raw
#========================
plt.figure(figsize=(16, 9))
plt.plot(time, rFoot[1], label='Right Foot')
plt.plot(time, lFoot[1], label='Left Foot')
plt.plot(time, rKnee[1], label='Right Knee')
plt.plot(time, lKnee[1], label='Left Knee')
plt.plot(time, head[1], label='Head')
plt.plot(time, neck[1], label='Neck')
plt.plot(time, torso[1], label='Torso')
plt.plot(time, rHip[1], label='Right Hip')
plt.plot(time, lHip[1], label='Left Hip')
plt.plot(time, rHand[1], label='Right Hand')
plt.plot(time, lHand[1], label='Left Hand')
plt.plot(time, rElbow[1], label='Right Elbow')
plt.plot(time, lElbow[1], label='Left Elbow')
plt.plot(time, rShoulder[1], label='Right Shoudler')
plt.plot(time, lShoulder[1], label='Left Shoulder')
plt.legend(loc='best')
plt.xlabel('Time / s')
name = "All_data_Y-axis"
plt.title(name)
plt.savefig(folder + name+'.png', dpi=myDPI)
plt.close()

#========================
# All data common beginning
#========================
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
name = "All_data_Y-axis_common_beginning"
plt.title(name)
plt.savefig(folder + name+'.png', dpi=myDPI)
# plt.show()

#========================
# All 1 jump common beginning
#========================
name += '_One_Jump'
plt.axis([15, 18, -800, 1050])
plt.title(name)
plt.legend(loc='lower left')
plt.savefig(folder + name+'.png', dpi=myDPI)
#plt.show()
plt.close()

#========================
# Plot Head + Feet + Knee
#========================
plt.figure(figsize=(16, 9))
name = "Y-Axis_compare_Head_Knee_Foot_right_side"
plt.xlabel('Time / s')
plt.plot(time, head[1], 'm', label='Head', linewidth=3)
plt.plot(time, rKnee[1], 'c', label='Right Knee', linewidth=3)
plt.plot(time, rFoot[1], 'g', label='Right Foot', linewidth=3)
plt.title(name)
plt.legend(loc='upper left')
plt.savefig(folder + name+'.png', dpi=myDPI)
# plt.show()
plt.close()

#========================
# Jump detection (Torso2Foot diff)
#========================
plt.figure(figsize=(16, 9))
name = "Y-Axis_Head_Torso2Foot_diff"
plt.plot(time, (rFoot)[1], 'g', label='Foot', linewidth=1.5)
plt.plot(time, (torso)[1], 'm', label='Torso', linewidth=1.5)
# plt.plot(time, fnc.commonBegining(rKnee)[1], 'c', label='Right Knee')
# plt.plot(time, fnc.commonBegining(rHip)[1], 'm', label='Right Hip')
plt.plot(time, (fnc.getRealDiff(torso, rFoot))[1], 'k-',
         markersize=7, label='Torso2Foot Right', linewidth=3)
plt.title(name)
plt.legend(loc='best')
plt.savefig(folder + name+'.png', dpi=myDPI)
# plt.show()

#========================
# JumpTrigger zoomed
#========================
name += '_zoom_Two_Jumps'
plt.axis([15, 26, -200, 900])
plt.plot(time, (fnc.getRealDiff(torso, lFoot))[1], 
         color='gray', markersize=7, label='Torso2Foot Left', linewidth=3)
plt.title(name)
plt.legend(loc='upper left')
plt.savefig(folder + name+'.png', dpi=myDPI)
#plt.show()
plt.close()


#========================
# Resulting Jumps
#========================
plt.figure(figsize=(16, 9))
name = "Jumps_cut"
plt.plot(time, (rFoot)[1], 'g-.', label='Foot', linewidth=1)
plt.plot(time, (rKnee)[1], 'c-.', label='Foot', linewidth=1)
color = ['r', 'k', 'm', 'b']  # np.random.rand(3)

for i in range(nJumps):
    plt.plot(time_cut[i], rFoot_cut[i][1], c=color[i], label='Foot'+str(i), linewidth=3)
    plt.plot(time_cut[i], rKnee_cut[i][1], c=color[i], label='Knee'+str(i), linewidth=3)
plt.title(name)
# plt.axis([2, 41, -1000, 250])
plt.legend(loc='best')
plt.savefig(folder + name+'.png', dpi=myDPI)





#========================
# Peak Flexion detection
#========================
plt.figure(figsize=(16, 9))
name = "PF_point_determination"
plt.plot(time, (fnc.getRealDiff(rKnee, rFoot))[1]-800, 'k.-', markersize=7,
        label='Knee2Foot (-500)', linewidth=4)
plt.plot(time, (rFoot)[1], 'g-.', label='Foot', linewidth=2)
plt.plot(time, (rKnee)[1], 'b-.', label='Knee', linewidth=2)
plt.title(name)
plt.legend(loc='best')
plt.savefig(folder + name+'.png', dpi=myDPI)

#========================
# PF_Trigger zoomed
#========================
name += '_zoom_Two_Jumps'
plt.axis([15, 26, -900, 100])
plt.title(name)
plt.legend(loc='upper left')
plt.savefig(folder + name+'.png', dpi=myDPI)
#plt.show()
plt.close()


#========================
# Initial Contact detection
#========================
plt.figure(figsize=(16, 9))
name = "PF_point_determination"
plt.plot(time, (rFoot)[1], 'g-.', label='Foot', linewidth=2)
plt.title(name)
plt.legend(loc='best')
plt.savefig(folder + name+'.png', dpi=myDPI)


    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.plot(time_cut[i], rKnee_cut[i][0], rKnee_cut[i][1], label='Righ Knee')
    # ax.plot(time_cut[i], lKnee_cut[i][0], lKnee_cut[i][1], label='Left Knee')
    # ax.plot(time_cut[i], rFoot_cut[i][0], rFoot_cut[i][1], label='Righ Foot')
    # ax.plot(time_cut[i], lFoot_cut[i][0], lFoot_cut[i][1], label='Left Foot')
    # ax.set_xlabel('Time')
    # ax.set_ylabel('X direction')
    # ax.set_zlabel('Y direction')
    # ax.legend()
    # plt.show()
    # plt.close()
    # midmidTime = (midTime[:-1] + midTime[1:]) /2
    # midTime = (time_cut[i][:-1] + time_cut[i][1:])/2 
    # plt.plot(np.full(100, time_cut[i][pfPoint]), np.linspace(-800, -400, 100), 'g-', label='PfKNEE')
    # plt.plot( np.linspace(-1, 40, 100), np.full(100, threshold-800), 'y-', label='threshold'+str(i))
    # plt.plot(np.full(100, time_cut[i][ciPoint]), np.linspace(-1000, 1000, 100), 'y-', label='CI')
    # plt.plot(time_cut[i], rKnee_cut[i][1], 'm', 'Right Knee')
    # plt.plot(time_cut[i], lKnee_cut[i][1], 'r', 'Left Knee')
    # plt.plot(time_cut[i], lFoot_cut[i][1], 'k', 'Left Foot')
    # plt.plot(time_cut[i], rFoot_cut[i][1], 'b', 'Right Foot')
    # plt.plot(midTime, np.diff(rFoot_cut[i][1])-800, 'g-*')
    # plt.plot(time_cut[i][ci], rFoot_cut[i][1][ci], 'k*', markersize=5) 
    # plt.plot(time_cut[i][ci], rFoot_cut[i][1][ci], 'k*', markersize=5)
    # plt.plot(time_cut[i][ciPoint], rFoot_cut[i][1][ciPoint], 'k*', markersize=10)
    # plt.plot(time_cut[i][ciPoint], lFoot_cut[i][1][ciPoint], 'k*', markersize=10)
    # plt.plot(midmidTime, np.diff(np.diff(rFoot_cut[i][1]))-800, 'b-*')
# plt.legend(loc='best')
# plt.show()


########
# Calculate CI for each jump and valgus analysis
########

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



