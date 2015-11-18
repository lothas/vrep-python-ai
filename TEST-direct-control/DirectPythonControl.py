# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:00:31 2015

@author: Jonathan Spitz
"""

import vrep
import sys
import time
import numpy as np
import matplotlib.pyplot as mlp

from Pioneer3D import *


print ('Program started')

vrep.simxFinish(-1)  # just in case, close all opened connections

# Connect to the simulation using V-REP's remote API (configured in V-REP, not scene specific)
# http://www.coppeliarobotics.com/helpFiles/en/remoteApiServerSide.htm
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

# Use port 19999 and add simExtRemoteApiStart(19999) to some child-script in your scene for scene specific API
# (requires the simulation to be running)

if clientID != -1:
    print ('Connected to remote API server')
else:
    print ('Failed connecting to remote API server')
    sys.exit('Could not connect')

# Reset running simulation
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
time.sleep(0.2)

# Start running simulation
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

# Create Pioneer3D objects
Robot1 = Pioneer3D(clientID, '')
Robot2 = Pioneer3D(clientID, '#0')
Robot3 = Pioneer3D(clientID, '#1')

# Connect to camera (not necessary, just part of some tutorial)
# errorCode, cam_handle = vrep.simxGetObjectHandle(clientID,
#                                   'cam1',
#                                   vrep.simx_opmode_oneshot_wait)
#
# errorCode, resolution, image = \
#     vrep.simxGetVisionSensorImage(clientID, cam_handle,
#                                   0, vrep.simx_opmode_streaming_split+4000)

now = time.time()

while True:
    # Run the robot controller code (see Pioneer3D class)
    # The code is the same as the built-in script in V-REP.
    # It reads the proximity sensors and sets the left/right speed accordingly
    Robot1.drive()
    Robot2.drive()
    Robot3.drive()

    # Print elapsed time between each control step
    last = now  
    now = time.time()
    print now-last
    
    # errorCode, resolution, image = \
    #     vrep.simxGetVisionSensorImage(clientID, cam_handle,
    #                               0, vrep.simx_opmode_buffer)
    #
    # if not errorCode:
    #     im = np.array(image, dtype=np.uint8)
    #     im.resize([resolution[0], resolution[1], 3])
    #     mlp.imshow(im)
                         
print ('Program ended')