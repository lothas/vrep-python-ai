__author__ = 'Lothas'

import sys
import os
# Get parent directory by joining this file's path [os.path.dirname(os.path.abspath(__file__))] with '..' [os.pardir]
parentDir = os.path.abspath(os.path.dirname(os.path.abspath(__file__))+'\\'+os.pardir)
sys.path.insert(0, parentDir)  # Add the parent directory where 'vrep' is located.

import vrep
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
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
time.sleep(0.2)

# Initialize simulation parameters
RobotNames = ["LineTracer", "LineTracer#0", "LineTracer#1"]
Params = [[[0.1, 0.2, 0, 0], [0.1, 0, 0, 0.2]],
          [[0.2, 0.2, 0, 0], [0.2, 0, 0, 0.2]],
          [[0.3, 0.3, 0, 0], [0.3, 0, 0, 0.4]]]
for i in range(len(RobotNames)):
    rN = RobotNames[i]
    Par = Params[i]
    for j in range(len(Par)):
        # For each motor
        for k in range(len(Par[j])):
            # For each sensor (+ base value)
            SignalName = rN+"_"+str(j+1)+"_"+str(k+1)
            res = vrep.simxSetFloatSignal(clientID, SignalName, Par[j][k],
                                            vrep.simx_opmode_oneshot_wait)

rbt_names = ["LineTracer", "LineTracer#0", "LineTracer#1"]
init_pos = []
rbts = []
for rbt_name in rbt_names:
    res, rbt_tmp = vrep.simxGetObjectHandle(clientID, rbt_name, vrep.simx_opmode_oneshot_wait)
    rbts.append(rbt_tmp)
    res, pos = vrep.simxGetObjectPosition(clientID, rbts[-1], -1, vrep.simx_opmode_streaming)

time.sleep(0.2)
for rbt in rbts:
    res, pos = vrep.simxGetObjectPosition(clientID, rbt, -1, vrep.simx_opmode_buffer)
    init_pos.append(pos)
    # print pos

# Start running simulation
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

time.sleep(3)  # wait 10 seconds

# Pause the simulation to get results
vrep.simxPauseSimulation(clientID, vrep.simx_opmode_oneshot)
pos = []
for rbt in rbts:
    res, pos_tmp = vrep.simxGetObjectPosition(clientID, rbt, -1, vrep.simx_opmode_buffer)
    pos.append(pos_tmp)
    # print pos_tmp

# Stop running the simulation
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)

delta_x = []
delta_y = []
for i in range(len(pos)):
    delta_x.append(pos[i][0] - init_pos[i][0])
    delta_y.append(pos[i][1] - init_pos[i][1])

print(delta_x)
print(delta_y)

time.sleep(0.1)
vrep.simxFinish(clientID)  # close connection to API
print ('Program ended')
