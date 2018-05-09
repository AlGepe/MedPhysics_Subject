import os.path
import myUtils as fnc
import numpy as np
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
folder = os.path.abspath('../') + '/Data/Results/'
filename = 'Result_Numbers_cm.txt'




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
plt.ylabel('Height / arbitrary units')
name = "Raw_data_Y-axis_"
plt.title(name)
plt.savefig(folder + name + 'cm.png', dpi=myDPI)
plt.close()

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

separator = fnc.getJumpStart(torso, rFoot)

############
# Conversion to cm
###########
plt.figure(figsize=(16, 9))
name = "Y-Axis_conversion to CM"
plt.xlabel('Time / s')
plt.ylabel('Height / arbitrary units')
plt.plot(time, head[1], 'g-.', label='Head')
plt.plot(time, rFoot[1], 'b-.', label='Right Foot')
plt.plot(time, lFoot[1], '-.', color='orange', label='Left Foot')


pos = np.zeros(2, dtype=np.int)
for i in range(len(time)):
    if time[i] < 26.2:
        pos[0] = i
    elif time[i] < 32.2:
        pos[1] = i

plt.plot(time[pos[0]:pos[1]], head[1][pos[0]:pos[1]], 'g',
         label='For Average', linewidth=4)
plt.plot(time[pos[0]:pos[1]], (lFoot[1][pos[0]:pos[1]] +
         rFoot[1][pos[0]:pos[1]])/2., 'm', label='For Average', linewidth=4)
#plt.plot(time[pos[0]:pos[1]], lFoot[1][pos[0]:pos[1]], color='orange', label='For Average', linewidth=5)
plt.title(name)
plt.legend(loc='upper right')
plt.savefig(folder + name + 'cm.png', dpi=myDPI)
# plt.show()
plt.close()

cteConv =   fnc.getConversion(head, rFoot, lFoot, pos)
footCorr = fnc.footCorrection(rFoot, lFoot, pos)

rFoot =     fnc.convert2cm(rFoot,     cteConv, footCorr)
lFoot =     fnc.convert2cm(lFoot,     cteConv, footCorr)
rKnee =     fnc.convert2cm(rKnee,     cteConv, footCorr)
lKnee =     fnc.convert2cm(lKnee,     cteConv, footCorr)
head =      fnc.convert2cm(head ,     cteConv, footCorr)
neck =      fnc.convert2cm(neck ,     cteConv, footCorr)
torso =     fnc.convert2cm(torso,     cteConv, footCorr)
rHip =      fnc.convert2cm(rHip,      cteConv, footCorr)
lHip =      fnc.convert2cm(lHip,      cteConv, footCorr)
rHand =     fnc.convert2cm(rHand,     cteConv, footCorr)
lHand =     fnc.convert2cm(lHand,     cteConv, footCorr)
rElbow =    fnc.convert2cm(rElbow,    cteConv, footCorr)
lElbow =    fnc.convert2cm(lElbow,    cteConv, footCorr)
rShoulder = fnc.convert2cm(rShoulder, cteConv, footCorr)
lShoulder = fnc.convert2cm(lShoulder, cteConv, footCorr)

########
# Analysis of the data
########

originalFoot = fnc.meaningFullOnly(fnc.getRightFoot(joints))
originalTorso = fnc.meaningFullOnly(fnc.getTorso(joints))
# separator = fnc.getJumpStart(originalTorso, originalFoot)
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
    outFile.write('KVM for Right Side: ' + str(rKVM[i]) + ' cm\n')
    outFile.write('KVM for Left  Side: ' + str(lKVM[i]) + ' cm\n')
    outFile.write('\n')
    outFile.write('FPKA for Right Side at IC: ' + str(rFPKA_ic[i] *
                  360/(2*np.pi)) + ' º\n')
    outFile.write('FPKA for Left  Side at IC: ' + str(lFPKA_ic[i] * 360 /
                  (2*np.pi)) + ' º\n')
    outFile.write('FPKA for Right Side at PF: ' + str(rFPKA_pf[i] * 360 /
                  (2*np.pi)) + ' º\n')
    outFile.write('FPKA for Left  Side at PF: ' + str(lFPKA_pf[i] * 360 /
                  (2*np.pi)) + ' º\n')
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
        outFile.write('KVM Right Side: ' + str(np.average(rKVM[1:i+1])) + ' cm\n')
        outFile.write('KVM Left  Side: ' + str(np.average(lKVM[1:i+1])) + ' cm\n')
        outFile.write('\n')
        outFile.write('FPKA for Right Side at IC: ' +
                str(np.average(rFPKA_ic[1:i+1]) * 360/(2*np.pi)) + ' º\n')
        outFile.write('FPKA for Left  Side at IC: ' +
                str(np.average(lFPKA_ic[1:i+1]) * 360 / (2*np.pi)) + ' º\n')
        outFile.write('FPKA for Right Side at PF: ' +
                str(np.average(rFPKA_pf[1:i+1]) * 360 / (2*np.pi)) + ' º\n')
        outFile.write('FPKA for Left  Side at PF: ' +
            str(np.average(lFPKA_pf[1:i+1]) * 360 / (2*np.pi)) + ' º\n')
        outFile.write('\n')
        outFile.write('FPKA for Right Side at IC: ' +
                      str(np.average(rFPKA_ic[1:i+1])) + '\n')
        outFile.write('FPKA for Left  Side at IC: ' +
                      str(np.average(lFPKA_ic[1:i+1])) + '\n')
        outFile.write('FPKA for Right Side at PF: ' +
                      str(np.average(rFPKA_pf[1:i+1])) + '\n')
        outFile.write('FPKA for Left  Side at PF: ' +
                      str(np.average(lFPKA_pf[1:i+1])) + '\n')
        outFile.write('\n')
        outFile.write('KASR at PF: ' + str(np.average(KASR[1:i+1])) + '\n')

####################################
#          PLOT ALL DATA           #
####################################

'''
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
plt.ylabel('Height / cm')
name = "All_data_Y-axis_noUseless"
plt.title(name)
plt.grid(which='both')
# plt.show()
plt.savefig(folder + name + 'cm.png', dpi=myDPI)
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
plt.ylabel('Height / cm')
name = "All_data_Y-axis_common_beginning"
plt.title(name)
plt.savefig(folder + name+'_cm.png', dpi=myDPI)
# plt.show()

#========================
# All 1 jump common beginning
#========================
name += '_One_Jump'
plt.axis([15, 18, -20, 100])
plt.title(name)
plt.legend(loc='lower left')
plt.savefig(folder + name+'_cm.png', dpi=myDPI)
#plt.show()
plt.close()

#========================
# Plot Head + Feet + Knee
#========================
plt.figure(figsize=(16, 9))
name = "Y-Axis_compare_Head_Knee_Foot_right"
plt.xlabel('Time / s')
plt.ylabel('Height / cm')
plt.plot(time, head[1], 'm', label='Head', linewidth=3)
plt.plot(time, (torso)[1], color='orange', label='Torso', linewidth=3.5)
plt.plot(time, rKnee[1], 'c', label='Right Knee', linewidth=3)
plt.plot(time, rFoot[1], 'g', label='Right Foot', linewidth=3)
plt.title(name)
plt.legend(loc='upper left')
plt.savefig(folder + name+'_cm.png', dpi=myDPI)
# plt.show()
plt.close()

#========================
# Jump detection (Torso2Foot diff)
#========================
plt.figure(figsize=(16, 9))
name += "_OnTop"
plt.xlabel('Time / s')
plt.ylabel('Height / cm')
plt.plot(time, fnc.commonBegining(head)[1], 'm', label='Head', linewidth=2)
plt.plot(time, fnc.commonBegining(torso)[1], color='orange', label='Torso', linewidth=2)
plt.plot(time, fnc.commonBegining(rKnee)[1], 'c', label='Right Knee', linewidth=2)
plt.plot(time, fnc.commonBegining(rFoot)[1], 'g', label='Right Foot', linewidth=2)
# plt.plot(time, fnc.commonBegining(rKnee)[1], 'c', label='Right Knee')
# plt.plot(time, fnc.commonBegining(rHip)[1], 'm', label='Right Hip')
#plt.plot(time, (fnc.getRealDiff(torso, rFoot-max(torso[1])))[1], 'k-', markersize=7, label='Torso2Foot Right', linewidth=3)
plt.title(name)
plt.legend(loc='best')
plt.savefig(folder + name+'_cm.png', dpi=myDPI)
# plt.show()

#========================
# JumpTrigger zoomed
#========================
name += '_zoom_Two_Jumps'
plt.axis([15, 26, -60, 50])
#plt.plot(time, (fnc.getRealDiff(torso, lFoot-max(torso[1])))[1], color='gray', markersize=7, label='Torso2Foot Left', linewidth=3)
plt.title(name)
plt.legend(loc='upper left')
plt.savefig(folder + name+'_cm.png', dpi=myDPI)
#plt.show()
plt.close()


#========================
# Resulting Jumps
#========================
plt.figure(figsize=(16, 9))
name = "Jumps_cut"
plt.xlabel('Time / s')
plt.ylabel('Height / cm')
plt.plot(time, (rFoot)[1], 'g-.', label='Foot', linewidth=1)
plt.plot(time, (rKnee)[1], 'c-.', label='Foot', linewidth=1)
color = ['r', 'k', 'm', 'b']  # np.random.rand(3)

for i in range(nJumps):
    plt.plot(time_cut[i], rFoot_cut[i][1], c=color[i], label='Jump' + str(i),
             linewidth=3)
    plt.plot(time_cut[i], rKnee_cut[i][1], c=color[i], linewidth=3)
plt.title(name)
plt.legend(loc='best')
plt.savefig(folder + name+'_cm.png', dpi=myDPI)
plt.close()

#========================
# Peak Flexion detection
#========================
plt.figure(figsize=(16, 9))
name = "PF_point_determination"
plt.xlabel('Time / s')
plt.ylabel('Height / cm')
plt.plot(np.full(100, time_cut[0][pf[0]]), np.linspace(-20, 100, 100), 'r-.',
         label='PF_point', linewidth=2)
plt.plot(np.full(100, time_cut[1][pf[1]]), np.linspace(-20, 100, 100), 'r-.',
         linewidth=2)
plt.plot(np.full(100, time_cut[2][pf[2]]), np.linspace(-20, 100, 100), 'r-.',
         linewidth=2)
plt.plot(np.full(100, time_cut[3][pf[3]]), np.linspace(-20, 100, 100), 'r-.',
         linewidth=2)
plt.plot(time, (fnc.getRealDiff(rKnee, rFoot))[1]-10, 'k.-', markersize=7,
         label='Knee2Foot ', linewidth=4)
plt.plot(time, (rFoot)[1], 'g-.', label='Foot', linewidth=2)
plt.plot(time, (rKnee)[1], 'b-.', label='Knee', linewidth=2)
plt.title(name)
plt.legend(loc='best')
plt.savefig(folder + name+'_cm.png', dpi=myDPI)

#========================
# PF_Trigger zoomed
#========================
name += '_zoom_Two_Jumps'
plt.axis([15, 26, -20, 100])
plt.title(name)
plt.legend(loc='upper left')
plt.savefig(folder + name+'_cm.png', dpi=myDPI)
#plt.show()
plt.close()


#========================
# Initial Contact detection
#========================
plt.figure(figsize=(16, 9))
plt.xlabel('Time / s')
plt.ylabel('Height / cm')
name = "IC_point_determination"
plt.plot(time, rFoot[1], 'g-.', label='Right Foot', linewidth=2)
plt.plot(time, lFoot[1], 'c-.', label='Left Foot', linewidth=2)
plt.savefig(folder + name + '1_cm.png', dpi=myDPI)
# plt.plot(time, lFoot[1], 'b-.', label='Foot', linewidth=2)
for i in range(nJumps):
    high = max([np.argmax(rFoot_cut[i][1]), np.argmax(lFoot_cut[i][1])])
    rebound = max([np.argmax(rFoot_cut[i][1][high+15:]),
                   np.argmax(lFoot_cut[i][1][high+15:])])
    rebound += high+15
    diff_l = np.diff(lFoot_cut[i][1])
    diff_r = np.diff(rFoot_cut[i][1])
    minPoint = int((np.argmin(rFoot_cut[i][1][:rebound]) +
                    np.argmin(lFoot_cut[i][1][:rebound])) / 2)
    if high <= 4:
        init = 0
        end = 4
    else:
        init = high - 4
        end = high + 2
    threshold = min([np.average(diff_r[init:end]),
                     np.average(diff_l[init:end])])
    startLooking = np.argmax(-1*(diff_l[high:rebound])) + high
    CI_point = minPoint - 1
    k = 1
    for j in range(startLooking, minPoint):
        if diff_r[j] > threshold or diff_l[j] > threshold:
            if k == 1:
                CI_point = j
                k = 2

    if i == 2:
        plt.plot(time_cut[i][startLooking:minPoint],
                rFoot_cut[i][1][startLooking:minPoint], color='orange', linewidth=7)
        plt.plot(time_cut[i][startLooking:minPoint],
                lFoot_cut[i][1][startLooking:minPoint], color='orange', linewidth=7,
                label='Segment for IC')
        plt.plot(time_cut[i][init:end], rFoot_cut[i][1][init:end], color='gray', label='Segment for Threshold', linewidth=7)
        plt.plot(time_cut[i][init:end], lFoot_cut[i][1][init:end],
                color='gray', linewidth=7)
        midTime = (time_cut[i][:-1] + time_cut[i][1:])/2
        plt.plot(midTime, diff_r, 'b', linewidth=4, label='Diff_right')
        plt.plot(midTime, diff_l, 'c', linewidth=4, label='Diff_left')
        plt.plot(time_cut[i], np.full(len(time_cut[i]), threshold), 'k-.', linewidth=2, label='Threshold')
        plt.plot(time, rFoot[1], 'g-.', label='Right Foot', linewidth=2)
        plt.plot(time, lFoot[1], 'c-.', label='Left Foot', linewidth=2)
        plt.plot(time_cut[i][high], rFoot_cut[i][1][high], 'r*', markersize=16, label='Highest point')
        plt.plot(time_cut[i][rebound], rFoot_cut[i][1][rebound], 'r^', markersize=16, label='Rebound Point')
        plt.plot(np.full(100, time_cut[i][CI_point]), np.linspace(-30, 50, 100), 'm-.', linewidth=2, label='IC point')
        plt.plot(time_cut[i][minPoint], rFoot_cut[i][1][minPoint], 'rs', markersize=16, label='Default IC [min]')

    else:
        plt.plot(time_cut[i][startLooking:minPoint], rFoot_cut[i][1][startLooking:minPoint], color='orange', linewidth=7)
        plt.plot(time_cut[i][startLooking:minPoint], lFoot_cut[i][1][startLooking:minPoint], color='orange', linewidth=7)
        plt.plot(time_cut[i][init:end], rFoot_cut[i][1][init:end], color='gray', linewidth=7)
        plt.plot(time_cut[i][init:end], lFoot_cut[i][1][init:end], color='gray', linewidth=7)
        midTime = (time_cut[i][:-1] + time_cut[i][1:])/2
        plt.plot(midTime, diff_r, 'b', linewidth=4)
        plt.plot(midTime, diff_l, 'c', linewidth=4)
        plt.plot(time_cut[i], np.full(len(time_cut[i]), threshold), 'k-.', linewidth=2)
        plt.plot(time, rFoot[1], 'g-.', linewidth=2)
        plt.plot(time, lFoot[1], 'c-.', linewidth=2)
        plt.plot(time_cut[i][high], rFoot_cut[i][1][high], 'r*', markersize=16)
        plt.plot(time_cut[i][rebound], rFoot_cut[i][1][rebound], 'r^', markersize=16)
        plt.plot(np.full(100, time_cut[i][CI_point]), np.linspace(-20, 50, 100), 'm-.', linewidth=2)
        plt.plot(time_cut[i][minPoint], rFoot_cut[i][1][minPoint], 'rs', markersize=16)


plt.title(name)
plt.legend(loc='best')
plt.savefig(folder + name+'_cm.png', dpi=myDPI)
plt.close()
# plt.grid()
# plt.show()

#========================
# IC_Trigger zoomed
#========================
plt.figure(figsize=(16, 9))
plt.xlabel('Time / s')
plt.ylabel('Height / cm')
name = "IC_point_determination_zoom"
plt.title('IC_determination')
plt.axis([22, 25, -15, 45])
plt.plot(time, rFoot[1], 'g-.', label='Right Foot', linewidth=2)
plt.plot(time, lFoot[1], 'c-.', label='Left Foot', linewidth=2)
plt.legend(loc='upper right')
plt.savefig(folder + name + '1_cm.png', dpi=myDPI)
plt.plot(time_cut[2][minPoint], rFoot_cut[2][1][minPoint], 'rs', markersize=16, label='Default IC [min]')
plt.plot(time_cut[2][high], rFoot_cut[2][1][high], 'r*', markersize=16, label='Highest point')
plt.plot(time_cut[2][rebound], rFoot_cut[2][1][rebound], 'r^', markersize=16, label='Rebound Point')
plt.legend(loc='upper right')
plt.savefig(folder + name + '2_cm.png', dpi=myDPI)
plt.plot(time_cut[2][init:end], rFoot_cut[2][1][init:end], color='gray', label='Segment for Threshold', linewidth=7)
plt.plot(time_cut[2][init:end], lFoot_cut[2][1][init:end], color='gray', linewidth=7)
plt.plot(time, rFoot[1], 'g-.', linewidth=2)
plt.plot(time, lFoot[1], 'c-.', linewidth=2)
plt.plot(time_cut[2][high], rFoot_cut[2][1][high], 'r*', markersize=16)
plt.legend(loc='upper right')
plt.savefig(folder + name + '3_cm.png', dpi=myDPI)
midTime = (time_cut[2][:-1] + time_cut[2][1:])/2
plt.plot(midTime, diff_r, 'b', linewidth=4, label='Diff_right')
plt.plot(midTime, diff_l, 'c', linewidth=4, label='Diff_left')
plt.legend(loc='upper right')
plt.savefig(folder + name + '4_cm.png', dpi=myDPI)
plt.plot(time_cut[2], np.full(len(time_cut[2]), threshold), 'k-.', linewidth=2, label='Threshold')
plt.legend(loc='upper right')
plt.savefig(folder + name + '5_cm.png', dpi=myDPI)
plt.plot(time_cut[2][startLooking:minPoint],
         rFoot_cut[2][1][startLooking:minPoint], color='orange', linewidth=7)
plt.plot(time_cut[2][startLooking:minPoint],
         lFoot_cut[2][1][startLooking:minPoint], color='orange', linewidth=7,
         label='Segment for IC')
plt.plot(time_cut[2][startLooking], diff_l[startLooking], '*',
         color='orange', markersize=16)
plt.plot(time, rFoot[1], 'g-.', linewidth=2)
plt.plot(time, lFoot[1], 'c-.', linewidth=2)
plt.legend(loc='upper right')
plt.savefig(folder + name + '6_cm.png', dpi=myDPI)
plt.plot(np.full(100, time_cut[2][CI_point]), np.linspace(-30, 50, 100), 'm-.', linewidth=2, label='IC point')
plt.legend(loc='upper right')
plt.savefig(folder + name + '7_cm.png', dpi=myDPI)
plt.close()



#========================
# Plots for presentation
#========================

plt.figure(figsize=(16, 9))
name = "Y-Axis_Hip(Avg)_Foot_Knee"
plt.xlabel('Time / s')
plt.ylabel('Height / cm')
plt.plot(time, rFoot[1], label='Right Foot')
plt.plot(time, lFoot[1], label='Left Foot')
plt.plot(time, rKnee[1], label='Right Knee')
plt.plot(time, lKnee[1], label='Left Knee')
plt.plot(time, (lHip[1] + rHip[1])/2, label='Average Hip')
plt.plot(np.full(100, time[separator[0]]), np.linspace(60, 160, 100), 'k-.',
         label='Jump_start', linewidth=2)
# plt.plot(time, rHip[1], label='Right Hip')
# plt.plot(time, lHip[1], label='Left Hip')
plt.legend(loc='upper right')
plt.savefig(folder + name + '_cm.png', dpi=myDPI)
plt.close()

plt.figure(figsize=(16, 9))
name = "X-Axis_Hip(Avg)_Foot_Knee"
plt.xlabel('Time / s')
plt.ylabel('Height / cm')
plt.plot(time, rFoot[0], label='Right Foot')
plt.plot(time, lFoot[0], label='Left Foot')
plt.plot(time, rKnee[0], label='Right Knee')
plt.plot(time, lKnee[0], label='Left Knee')
plt.plot(time, (lHip[0] + rHip[0])/2, label='Average Hip')
plt.plot(np.full(100, time[separator[0]]), np.linspace(60, 160, 100), 'k-.',
         label='Jump_start', linewidth=2)
plt.plot(np.full(100, time[separator[1]]), np.linspace(60, 160, 100), 'k-.',
         linewidth=2)
plt.plot(np.full(100, time[separator[2]]), np.linspace(60, 160, 100), 'k-.',
         linewidth=2)
plt.plot(np.full(100, time[separator[3]]), np.linspace(60, 160, 100), 'k-.',
         linewidth=2)

# plt.plot(time, lHip[0], label='Left Hip')
plt.legend(loc='upper right')
plt.savefig(folder + name + '_cm.png', dpi=myDPI)
plt.close()

plt.figure(figsize=(16, 9))
name = "X&Y-Axis_Hip(Avg)_Foot_Knee"
plt.xlabel('Time / s')
plt.ylabel('Height / cm')
plt.plot(time, rFoot[0], label='X Foot')
plt.plot(time, rFoot[1], label='Y Foot')
plt.legend(loc='upper right')
# plt.show()
plt.close
'''

#===========
# Animation
#==========
plt.figure(figsize=(16, 9))
name = "X_Y"
plt.xlabel('X / cm')
plt.ylabel('Y / cm')
rShoulder_cut = fnc.splitJumps(rShoulder, separator)
lShoulder_cut = fnc.splitJumps(lShoulder, separator)
head_cut = fnc.splitJumps(head, separator)
neck_cut = fnc.splitJumps(neck, separator)
rHand_cut = fnc.splitJumps(rHand, separator)
lHand_cut = fnc.splitJumps(lHand, separator)
rHip_cut = fnc.splitJumps(rHip, separator)
lHip_cut = fnc.splitJumps(lHip, separator)
lElbow_cut = fnc.splitJumps(lElbow, separator)
rElbow_cut = fnc.splitJumps(rElbow, separator)
torso_cut = fnc.splitJumps(torso, separator)
for j in range(nJumps):
    print(len(time_cut[j]))
    for i in range(len(time_cut[j]) - 3):
        plt.axis([25, 225, -50, 250])
        plt.title("Time {0}s".format(time[i]))
        plt.plot(rShoulder_cut[j][0][i], rShoulder_cut[j][1][i+3], 'r<', markersize=10, label='Right Shoulder')
        plt.plot(lShoulder_cut[j][0][i], lShoulder_cut[j][1][i+3], 'r>', markersize=10, label='Left Shoulder')
        plt.plot(     head_cut[j][0][i],      head_cut[j][1][i+3], 'bo', markersize=10, label='Head')
        plt.plot(     neck_cut[j][0][i],      neck_cut[j][1][i+3], 'b+', markersize=10, label='Neck')
        plt.plot(    rHand_cut[j][0][i],     rHand_cut[j][1][i+3], 'c<', markersize=10, label='Right Hand')
        plt.plot(    lHand_cut[j][0][i],     lHand_cut[j][1][i+3], 'c>', markersize=10, label='Left Hand')
        plt.plot(   rElbow_cut[j][0][i],    rElbow_cut[j][1][i+3], 'k<', markersize=10, label='Right Elbow')
        plt.plot(   lElbow_cut[j][0][i],    lElbow_cut[j][1][i+3], 'k>', markersize=10, label='Left Elbow')
        plt.plot(    torso_cut[j][0][i],     torso_cut[j][1][i+3], 'r*', markersize=10, label='Torso')
        plt.plot(    rFoot_cut[j][0][i],     rFoot_cut[j][1][i+3], 'g<', markersize=10, label='Right Foot')
        plt.plot(    lFoot_cut[j][0][i],     lFoot_cut[j][1][i+3], 'g>', markersize=10, label='Left Foot')
        plt.plot(    rKnee_cut[j][0][i],     rKnee_cut[j][1][i+3], 'm<', markersize=10, label='Right Knee')
        plt.plot(    lKnee_cut[j][0][i],     lKnee_cut[j][1][i+3], 'm>', markersize=10, label='Left Knee')
        plt.plot(     rHip_cut[j][0][i],      rHip_cut[j][1][i+3],  '<', markersize=10, label='Right Hip', color='xkcd:maroon')
        plt.plot(     lHip_cut[j][0][i],      lHip_cut[j][1][i+3],  '>', markersize=10, label='Left Hip',  color='xkcd:maroon')

        plt.plot(rShoulder_cut[j][0][i:i+3], rShoulder_cut[j][1][i:i+3], 'r<', markersize=3,)
        plt.plot(lShoulder_cut[j][0][i:i+3], lShoulder_cut[j][1][i:i+3], 'r>', markersize=3,)
        plt.plot(     head_cut[j][0][i:i+3],      head_cut[j][1][i:i+3], 'bo', markersize=3,)
        plt.plot(     neck_cut[j][0][i:i+3],      neck_cut[j][1][i:i+3], 'b+', markersize=3,)
        plt.plot(    rHand_cut[j][0][i:i+3],     rHand_cut[j][1][i:i+3], 'c<', markersize=3,)
        plt.plot(    lHand_cut[j][0][i:i+3],     lHand_cut[j][1][i:i+3], 'c>', markersize=3,)
        plt.plot(   rElbow_cut[j][0][i:i+3],    rElbow_cut[j][1][i:i+3], 'k<', markersize=3,)
        plt.plot(   lElbow_cut[j][0][i:i+3],    lElbow_cut[j][1][i:i+3], 'k>', markersize=3,)
        plt.plot(    torso_cut[j][0][i:i+3],     torso_cut[j][1][i:i+3], 'r*', markersize=3,)
        plt.plot(    rFoot_cut[j][0][i:i+3],     rFoot_cut[j][1][i:i+3], 'g<', markersize=3,)
        plt.plot(    lFoot_cut[j][0][i:i+3],     lFoot_cut[j][1][i:i+3], 'g>', markersize=3,)
        plt.plot(    rKnee_cut[j][0][i:i+3],     rKnee_cut[j][1][i:i+3], 'm<', markersize=3,)
        plt.plot(    lKnee_cut[j][0][i:i+3],     lKnee_cut[j][1][i:i+3], 'm>', markersize=3,)
        plt.plot(     rHip_cut[j][0][i:i+3],      rHip_cut[j][1][i:i+3],  '<', markersize=3, color='xkcd:maroon')
        plt.plot(     lHip_cut[j][0][i:i+3],      lHip_cut[j][1][i:i+3],  '>', markersize=3, color='xkcd:maroon')
        plt.legend(loc='best')
        # plt.show()
        name = folder + 'Animations/' + 'Jump{0:1d}LowerBody{1:02d}_cm.png'.format(j, i)
        plt.savefig(name, dpi=myDPI)
        plt.clf()


