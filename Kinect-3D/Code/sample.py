import os.path
from KinectUtils import KinectDataReader

FILE_PATH = os.path.abspath('../') + '/Data/'
file_name = 'kinect_recording_alvar'

kinect = KinectDataReader(FILE_PATH+file_name)

joints = []
Time = []
frame = kinect.readNextFrame()
first_time = frame[3]

while frame is not None:

    frame_index = frame[0]
    hands_included = frame[1]
    # skeleton_included = frame[2]
    frame_time = frame[3]

    if frame[2]:  # skeleton_included
        skel = frame[8]
        Time.append(frame_time-first_time)
        joints.append(skel.joints)

        '''
        print('Idx:', frame_index, 'Time:', frame_time-first_time)
        print('Head x,y,z [mm]: ', joints[-1][0].x, joints[-1][0].y,
              joints[-1][0].z)
        print('Torso x,y,z [mm]: ', joints[-1][8].x, joints[-1][8].y,
              joints[-1][8].z)
              '''
    frame = kinect.readNextFrame()
print('END OF FILE')
print(joints[-1][0].x)
print(joints[-1][0].y)
print(joints[-1][0].z)
