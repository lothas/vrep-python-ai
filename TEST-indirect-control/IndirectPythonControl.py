# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:00:31 2015

@author: Jonathan Spitz
"""

import vrep
import sys
import time

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
print ('Stopping (resetting) current simulation...')
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
time.sleep(0.5)

# Start running simulation
print ('Starting new simulation...')
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

speeds1 = [1, 0, -1, 2, -1, 1]
speeds2 = [2, 0, -2, 4, -2, 2]
speeds3 = [0.1, 0.2, 0.3, 0.2, 0.1, 0]
t0 = time.time()
dT = 5
cur_speed = 0
    
# errorCode, cam_handle = vrep.simxGetObjectHandle(clientID,
#                                   'cam1',
#                                   vrep.simx_opmode_oneshot_wait)
#
# errorCode, resolution, image = \
#     vrep.simxGetVisionSensorImage(clientID, cam_handle,
#                                   0, vrep.simx_opmode_streaming_split+4000)

now = time.time()
t0 = now-dT

while True:
    if now > t0+dT:
        # Set the float signal that tells the robot how fast to drive
        res = vrep.simxSetFloatSignal(clientID, "Pioneer_p3dx_v0", speeds1[cur_speed],
                                vrep.simx_opmode_oneshot)

        res = vrep.simxSetFloatSignal(clientID, "Pioneer_p3dx#0_v0", speeds2[cur_speed],
                                vrep.simx_opmode_oneshot)

        res = vrep.simxSetFloatSignal(clientID, "Pioneer_p3dx#1_v0", speeds3[cur_speed],
                                vrep.simx_opmode_oneshot)

        print 'New speeds: '+str(speeds1[cur_speed])+' '+str(speeds2[cur_speed])+' '+str(speeds3[cur_speed])
        
        t0 = now
        cur_speed += 1
        if cur_speed >= len(speeds1):
            cur_speed = 0

    # Print elapsed time between each control step
    last = now  
    now = time.time()

    time.sleep(0.01)
#    print now-last
                         
print ('Program ended')