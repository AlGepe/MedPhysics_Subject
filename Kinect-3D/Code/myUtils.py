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
            for i in range(3):
                trimJoint[i] = oneJoint[i][starts[0]:] - oneJoint[i][starts[0]]
    return trimJoint


# Returns the position in the array of the PF point
def getPFindex(jointNp):
    # peak flexion/ maximum squatting
    return np.argmin(jointNp, axis=1)


# Returns the position in the array of the CI point
def getCIindex(jointNp):
    # Contact point
    return np.argmin(jointNp, axis=1)


def getRightKnee(joints):

    jointPos = 11
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getLeftKnee(joints):

    jointPos = 12
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getRightFoot(joints):

    jointPos = 13
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getLeftFoot(joints):

    jointPos = 14
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getLeftHip(joints):

    jointPos = 10
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getRightHip(joints):

    jointPos = 9
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getTorso(joints):

    jointPos = 8
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getLeftHand(joints):

    jointPos = 7
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getRightHand(joints):

    jointPos = 6
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getLeftElbow(joints):

    jointPos = 5
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getRightElbow(joints):

    jointPos = 4
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getLeftShoulder(joints):

    jointPos = 3
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getRightShoulder(joints):

    jointPos = 2
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getNeck(joints):

    jointPos = 1
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


def getHead(joints):

    jointPos = 0
    dataSize = len(joints)
    thisJoint = np.zeros(shape=(3, dataSize))
    for i in range(dataSize):
        thisJoint[0][i] = joints[i][jointPos].x
        thisJoint[1][i] = joints[i][jointPos].y
        thisJoint[2][i] = joints[i][jointPos].z
    return commonBegining(thisJoint)


# Z is depth (from-to camera)
# Y is heigh
