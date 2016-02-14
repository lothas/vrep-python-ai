__author__ = 'Rea Yakar'
# based on the code of Jonathan Spitz

import sys
import os
import math
# Get parent directory by joining this file's path [os.path.dirname(os.path.abspath(__file__))] with '..' [os.pardir]
parentDir = os.path.abspath(os.path.dirname(os.path.abspath(__file__))+'\\'+os.pardir)
sys.path.insert(0, parentDir)  # Add the parent directory where 'vrep' is located.

import vrep
import time
import numpy as np


# ############################ Biped Walker TESTER CLASS ############################ #
# A Biped Walker tester object tests the given population of CPG controller parameters on
# V-REP simulated robots and returns the fitness values for each genome.
# The genomes encode controller parameters for frequency and phase of operation of each motor.
# The fitness function used measures the distance covered by the robot in a set
# trial time.

class WalkerTester():
    def __init__(self, n_robots, simTimeLimit, base_name):
        self.name = "walker tester"
        self.n_robots = n_robots
        self.base_name = base_name

        self.simTimeLimit = simTimeLimit

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
            vrep.simxGetFloatSignal(self.clientID, rbt_name+'_1', vrep.simx_opmode_streaming)
            vrep.simxGetFloatSignal(self.clientID, rbt_name+'_2', vrep.simx_opmode_streaming)
            vrep.simxGetFloatSignal(self.clientID, rbt_name+'_3', vrep.simx_opmode_streaming)
            vrep.simxGetFloatSignal(self.clientID, rbt_name+'_4', vrep.simx_opmode_streaming)
            vrep.simxGetFloatSignal(self.clientID, rbt_name+'_5', vrep.simx_opmode_streaming)

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
            genomes = pop[self.n_robots*trial:self.n_robots*(trial+1)]
            pop_fitness += self.run_trial(genomes)

        return pop_fitness


    def run_trial(self, genomes):
        # Set the parameters for each robot
        for genome, robot in zip(genomes, self.robot_names):
            par = [[genome[0], genome[1], genome[2], genome[3]],
                   [genome[0], genome[4], genome[5], genome[6]],
                   [genome[0], genome[7], genome[8], genome[9]],
                   [genome[0], genome[10], genome[11], genome[12]],
                   [genome[0], genome[13], genome[14], genome[15]],
                   [genome[0], genome[16], genome[17], genome[18]]]

            for j in range(len(par)):
                # For each motor
                for k in range(len(par[j])):
                    # For each joint (+ base value)
                    joint_name = robot+"_"+str(j+1)+"_"+str(k+1)
                    res = vrep.simxSetFloatSignal(self.clientID, joint_name, par[j][k],
                                                  vrep.simx_opmode_oneshot)
                    if res > 1:
                        print 'Error setting signal '+joint_name+': '+str(res)

        # Start running simulation
        # print 'Running trial'
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot_wait)

        # Initialize output arrays
        sim_time = [[] for i in range(self.n_robots)]
        robot_x = [[] for i in range(self.n_robots)]
        robot_y = [[] for i in range(self.n_robots)]
        robot_z = [[] for i in range(self.n_robots)]
        init_pos = [[] for i in range(self.n_robots)]
        robot_tStandScore = [[] for i in range(self.n_robots)]
        fit_y = [0 for i in range(self.n_robots)]

        t_step = 0.01  # how often to check the simulation's signals
        t_flag = time.time()+t_step
        once = True
        new_data = [0 for i in range(self.n_robots)]
        go_loop = True

        while go_loop:
            now = time.time()
            if now > t_flag:
                t_flag = now+t_step

                # Get info from robot
                for i in range(self.n_robots):
                    # get simulation time
                    res1, in1 = vrep.simxGetFloatSignal(self.clientID,
                                                        self.robot_names[i]+'_1', vrep.simx_opmode_buffer)
                    # get rel position 1
                    res2, in2 = vrep.simxGetFloatSignal(self.clientID,
                                                        self.robot_names[i]+'_2', vrep.simx_opmode_buffer)
                    # get rel position 2
                    res3, in3 = vrep.simxGetFloatSignal(self.clientID,
                                                        self.robot_names[i]+'_3', vrep.simx_opmode_buffer)
                    # get rel position z
                    res4, in4 = vrep.simxGetFloatSignal(self.clientID,
                                                        self.robot_names[i]+'_4', vrep.simx_opmode_buffer)
                    # stand time score
                    res5, in5 = vrep.simxGetFloatSignal(self.clientID,
                                                        self.robot_names[i]+'_5', vrep.simx_opmode_buffer)

                    if res1 == 0 and res2 == 0 and res3 == 0 and res4 == 0 and res5 == 0:
                        sim_time[i].append(in1)
                        robot_x[i].append(in2)
                        robot_y[i].append(in3)
                        robot_z[i].append(in4)
                        robot_tStandScore[i].append(in5)
                        new_data[i] = 1  # new data arrived

                if once:
                    if sum(new_data) == self.n_robots:
                        for i in range(self.n_robots):
                            init_pos[i] = [robot_x[i][-1], robot_y[i][-1], robot_z[i][-1]]
                        once = False
                else:
                    for i in range(self.n_robots):
                        if new_data[i] == 1:
                            fit_y[i] += abs(robot_y[i][-1])*(sim_time[i][-1]-sim_time[i][-2])
                            new_data[i] = 0
                            if sim_time[i][-1] > self.simTimeLimit:  # time limit for the simulation
                                go_loop = False
                                break

        trial_fitness = []
        for i in range(self.n_robots):
            x_fit = robot_x[i][-1] - init_pos[i][0]
            # y_fit = 1/(1+20*fit_y[i])
            # if robot_z[i][-1] < 0.5:
            #     z_fit = 0
            # else:
            #     z_fit = robot_z[i][-1]
            StandScore_fit = 0.1*robot_tStandScore[i][-1]

            # control effort normalized by x distance
            if x_fit > 0:
                HipEffort = math.pow(genome[3], 2)
                knee1Effort = math.pow(genome[6], 2)
                knee2Effort = math.pow(genome[9], 2)
                ankle1Effort = math.pow(genome[12], 2)
                ankle2Effort = math.pow(genome[15], 2)
                # normConEffortFit_temp = (genome[2]*HipEffort + genome[5]*knee1Effort + genome[8]*knee2Effort + genome[11]*ankle1Effort + genome[14]*ankle2Effort)/x_fit
                # knees are locked for now:
                normConEffortFit_temp = (genome[2]*HipEffort + genome[11]*ankle1Effort + genome[14]*ankle2Effort)/x_fit
                normConEffortFit = 1/normConEffortFit_temp
            else:
                normConEffortFit = 0

            trial_fitness.append([x_fit, normConEffortFit, StandScore_fit])

        # Stop and reset the simulation
        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot)
        time.sleep(0.35)

        return trial_fitness


    def disconnect(self):
        time.sleep(0.1)
        vrep.simxFinish(self.clientID)  # close connection to API


if __name__ == '__main__':
    tester = WalkerTester(5, 'Leg1')
    res = tester.run_trial([[[100, 0.3, 0.6, 50], [100, 0.2, 0.6, 50], [100, 0.2, 0.6, 50]],
          [[10, 0.3, 0.6, 50], [10, 0.2, 0.6, 50], [10, 0.2, 0.6, 50]],
          [[100, 0.3, 0.6, 50], [100, 0.2, 0.6, 50], [100, 0.2, 0.6, 50]],
          [[1000, 0.3, 0.6, 50], [1000, 0.2, 0.6, 50], [1000, 0.2, 0.6, 50]],
          [[1, 0.2, 0.6, 5], [1, 0.2, 0.6, 5], [1, 0.2, 0.6, 5]]])
    print res