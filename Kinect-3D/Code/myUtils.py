# import os.path
import numpy as np
from KinectUtils import KinectDataReader


# Load data from file into python format (lists)
def getJointData(file_name):

    kinect = KinectDataReader(file_name)
    # numDatas = getNumberLines(file_name)

    joints = []
    Time = []
    frame = kinect.readNextFrame()
    first_time = frame[3]

    while frame is not None:

        # frame_index = frame[0]
        # hands_included = frame[1]
        # skeleton_included = frame[2]
        frame_time = frame[3]

        if frame[2]:  # skeleton_included
            skel = frame[8]
            Time.append(frame_time-first_time)
            joints.append(skel.joints)

        frame = kinect.readNextFrame()
    return np.asarray(Time), joints


# Obtain total number of data points/lines
def getNumberLines(file_name):
    kinect = KinectDataReader(file_name)
    i = 0
    while kinect.readNextFrame() is not None:
        i += 1
    return i


# Eliminate blank measurements and set the begining as zero displacement
def commonBegining(oneJoint):
    starts = np.array([0, 0, 0], dtype=int)
    for i in range(3):
        j = 0
        while oneJoint[i][j] == 0:
            j += 1
        starts[i] = j
    if np.any(starts - starts[0]):
        oneJoint[0] = oneJoint[0] - oneJoint[0][starts[0]]
        oneJoint[1] = oneJoint[1] - oneJoint[1][starts[1]]
        oneJoint[2] = oneJoint[2] - oneJoint[2][starts[2]]
        trimJoint = oneJoint
    else:
        trimJoint = np.ndarray(shape=(3, len(oneJoint[0])-starts[0]))
        for k in range(3):
            trimJoint[k] = oneJoint[k][starts[0]:] - oneJoint[k][starts[0]]
    return trimJoint


def meaningFullOnly(oneJoint, t0=3.5):
    start = int(t0 * 33)
    trimJoint = np.ndarray(shape=(3, len(oneJoint[0])-start))
    for i in range(3):
        trimJoint[i] = oneJoint[i][start:]  # - oneJoint[i][starts[0]]
    return trimJoint


def footCorrection(rFoot, lFoot, pos):
    return np.average(((rFoot[1][pos[0]:pos[1]] + lFoot[1][pos[0]:pos[1]])/2))


def getConversion(head, rFoot, lFoot, positions):
    height = head[1] - ((rFoot[1] + lFoot[1])/2)
    aver = np.average(height[positions[0]:positions[1]])
    return 175./aver


def convert2cm(joint, conversion, footCorr):
    for i in range(len(joint)):
        joint[i] = (joint[i]-footCorr) * conversion
    return joint


# Returns the position in the array of the PF point
# PF [peak flexion] is defined here as the point of minimum distance between
# the foot and the knee
def getPFindex(rKnee, lKnee, rFoot, lFoot):
    # peak flexion/ maximum squatting
    # Check only on Y axis (vertical)
    rSide = abs(abs(rKnee[1]) - abs(rFoot[1]))
    lSide = abs(abs(lKnee[1]) - abs(lFoot[1]))
    rPf = np.argmin(rSide)  # , axis=1)
    lPf = np.argmin(lSide)  # , axis=1)
    if (rPf == lPf):
        return rPf
    else:
        if rPf < 5:
            rPf = 5
        if lPf < 5:
            lPf = 5

        radius = 5
        distAround_rPf = (rSide[rPf-radius:rPf+radius] +
                          lSide[rPf-radius:rPf+radius])
        distAround_lPf = (rSide[lPf-radius:lPf+radius] +
                          lSide[lPf-radius:lPf+radius])

        if(min(distAround_lPf) < min(distAround_rPf)):  # lPf is the best PF
            return np.argmin(distAround_lPf) + (lPf - radius)
        else:  # rPf is the best PF or they are both equal
            return np.argmin(distAround_rPf) + (rPf - radius)


def getRealDiff(jointOne, jointTwo):
    return abs(abs(jointOne) - abs(jointTwo))


def getJumpStart(torso, foot, numJumps=4):
    jumpsStart = np.zeros(numJumps, dtype=int)
    jointDiff = getRealDiff(torso, foot)[1]
    trigger = max(jointDiff) - .05 * max(jointDiff)
    i = 0
    j = 0
    while j < numJumps and i < len(jointDiff):
        if jointDiff[i] >= trigger:
            jumpsStart[j] = i - 25
            j += 1
            i += 100
        i += 1
    return jumpsStart


def splitJumps(joint, starts, lenJump=60):
    nJumps = len(starts)
    nAxis = len(joint)
    if type(joint[0]) is not np.ndarray:
        splittedJoint = np.ndarray(shape=(nJumps), dtype=np.ndarray)
        for i in range(nJumps):
                splittedJoint[i] = joint[starts[i]:starts[i] + lenJump]
    else:
        splittedJoint = np.ndarray(shape=(nJumps, nAxis), dtype=np.ndarray)
        for i in range(nJumps):
            for j in range(nAxis):
                splittedJoint[i][j] = joint[j][starts[i]:starts[i] + lenJump]
    return splittedJoint


def lowPassJoint(jointNp):
    jointRC = np.zeros(shape=(len(jointNp), len(jointNp[0])))
    print(jointNp.shape)
    for j in range(jointNp.shape[0]):
        for i in range(len(jointNp[0])-1):
            # print(i)
            jointRC[j][i+1] = (jointNp[j][i] + jointNp[j][i+1])/2
    return jointRC


def getKVM(knee_x, ic, pf):
    return abs(knee_x[ic] - knee_x[pf])


def getKASR(rKnee_x, lKnee_x, rFoot_x, lFoot_x, pf):
    xKR = rKnee_x[pf]
    xKL = lKnee_x[pf]
    xFR = rFoot_x[pf]
    xFL = lFoot_x[pf]
    return (abs(xKR - xKL) / abs(xFR-xFL))


def getFPKA(knee, foot, point):

    u = [0, foot[1][point] - knee[1][point]]
    v = [foot[0][point] - knee[0][point], foot[1][point] - knee[1][point]]

    u /= np.linalg.norm(u)
    v /= np.linalg.norm(v)
    prod = sum(u*v)

    return np.arccos(prod)


def getICindex(rFoot, lFoot):
    # highest point in the jump
    high = max([np.argmax(rFoot[1]), np.argmax(lFoot[1])])
    # highest point second jump
    # return high+10
    rebound = max([np.argmax(rFoot[1][high+15:]), np.argmax(lFoot[1][high+15:])])
    # convert to absolute position
    rebound += high+15

    diff_l = np.diff(lFoot[1])
    diff_r = np.diff(rFoot[1])

    minPoint = int((np.argmin(rFoot[1][:rebound]) +
                   np.argmin(lFoot[1][:rebound])) / 2)
    if high <= 4:
        init = 0
        end = 4
    else:
        init = high - 4
        end = high + 2
    threshold = min([np.average(diff_r[init:end]), np.average(diff_l[init:end])])
    startLooking = np.argmax(-1*(diff_l[high:rebound])) + high
    for i in range(startLooking, minPoint):
        if diff_r[i] > threshold or diff_l[i] > threshold:
            return i

    return minPoint - 1


def getRightKnee(joints):

    jointPos = 11
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getLeftKnee(joints):

    jointPos = 12
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getRightFoot(joints):

    jointPos = 13
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getLeftFoot(joints):

    jointPos = 14
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getLeftHip(joints):

    jointPos = 10
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getRightHip(joints):

    jointPos = 9
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getTorso(joints):

    jointPos = 8
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getLeftHand(joints):

    jointPos = 7
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getRightHand(joints):

    jointPos = 6
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getLeftElbow(joints):

    jointPos = 5
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getRightElbow(joints):

    jointPos = 4
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getLeftShoulder(joints):

    jointPos = 3
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getRightShoulder(joints):

    jointPos = 2
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getNeck(joints):

    jointPos = 1
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


def getHead(joints):

    jointPos = 0
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return thisJoint


# Z is depth (from-to camera)
# Y is heigth
