__author__ = 'Jonathan Spitz'

import sys
import os
# Get parent directory by joining this file's path [os.path.dirname(os.path.abspath(__file__))] with '..' [os.pardir]
parentDir = os.path.abspath(os.path.dirname(os.path.abspath(__file__))+'\\'+os.pardir)
sys.path.insert(0, parentDir)  # Add the parent directory where 'vrep' is located.

import vrep
import time
import numpy as np


# ############################ LINE FOLLOWER TESTER CLASS ############################ #
# A Line follower tester object tests the given population of controller gains on
# V-REP simulated robots and returns the fitness values for each genome.
# The genomes encode controller gains for base speed and sensory feedback.
# The fitness function used measures the distance covered by the robot in a set
# trial time.
class LineFolTester():
    def __init__(self, n_robots, base_name):
        self.n_robots = n_robots
        self.base_name = base_name

        self.robot_names = [self.base_name]
        for i in range(self.n_robots-1):
            self.robot_names.append(self.base_name+'#'+str(i))

        # Establish connection to V-REP
        vrep.simxFinish(-1)  # just in case, close all opened connections

        # Connect to the simulation using V-REP's remote API (configured in V-REP, not scene specific)
        # http://www.coppeliarobotics.com/helpFiles/en/remoteApiServerSide.htm
        self.clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

        # Use port 19999 and add simExtRemoteApiStart(19999) to some child-script in your scene for scene specific API
        # (requires the simulation to be running)

        if self.clientID != -1:
            print ('Connected to remote API server')
        else:
            print ('Failed connecting to remote API server')
            sys.exit('Could not connect')

        # Reset running simulation
        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot)
        time.sleep(0.2)

        # Get initial robots' positions
        self.robot_handles = []
        self.robot_pos0 = []
        for rbt_name in self.robot_names:
            res, rbt_tmp = vrep.simxGetObjectHandle(self.clientID, rbt_name, vrep.simx_opmode_oneshot_wait)
            self.robot_handles.append(rbt_tmp)
            # Initialize data stream
            vrep.simxGetObjectPosition(self.clientID, self.robot_handles[-1], -1, vrep.simx_opmode_streaming)

        time.sleep(0.2)
        for rbt in self.robot_handles:
            res, pos = vrep.simxGetObjectPosition(self.clientID, rbt, -1, vrep.simx_opmode_buffer)
            self.robot_pos0.append(pos)
            # print pos

    def test_pop(self, pop):
        pop_fitness = []
        n_genomes = len(pop)
        n_trials = int(np.ceil(n_genomes/self.n_robots))

        for trial in range(n_trials):
            genomes = pop[3*trial:3*trial+3]
            pop_fitness += self.run_trial(genomes, self.robot_names)
            if len(pop_fitness) > 15:
                print "shit!"

        return pop_fitness

    def run_trial(self, genomes, names):
        # Set the signals for each robot
        for genome, robot in zip(genomes, names):
            par = [genome[:3], genome[3:]]
            for j in range(len(par)):
                # For each motor
                for k in range(len(par[j])):
                    # For each sensor (+ base value)
                    signal_name = robot+"_"+str(j+1)+"_"+str(k+1)
                    res = vrep.simxSetFloatSignal(self.clientID, signal_name, par[j][k],
                                                  vrep.simx_opmode_oneshot)
                    if res:
                        print 'Error setting signal '+signal_name+': '+str(res)

        # Start running simulation
        print 'Running trial'
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot)

        time.sleep(3)  # wait 3 seconds

        # Pause the simulation
        vrep.simxPauseSimulation(self.clientID, vrep.simx_opmode_oneshot)

        trial_fitness = []
        # Get the trial results for each robot
        for i in range(len(self.robot_handles)):
            res, pos = vrep.simxGetObjectPosition(self.clientID, self.robot_handles[i], -1, vrep.simx_opmode_buffer)
            # print pos_tmp

            delta_x = pos[0] - self.robot_pos0[i][0]
            # delta_y = pos[1] - self.robot_pos0[i][1]

            trial_fitness.append(delta_x)
            if len(trial_fitness) > 3:
                print "shit!"

        # Stop and reset the simulation
        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot)
        time.sleep(0.2)

        return trial_fitness

    def disconnect(self):
        time.sleep(0.1)
        vrep.simxFinish(self.clientID)  # close connection to API