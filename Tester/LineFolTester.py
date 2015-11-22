__author__ = 'Jonathan Spitz'

import sys
import os
# Get parent directory by joining this file's path [os.path.dirname(os.path.abspath(__file__))] with '..' [os.pardir]
parentDir = os.path.abspath(os.path.dirname(os.path.abspath(__file__))+'\\'+os.pardir)
sys.path.insert(0, parentDir)  # Add the parent directory where 'vrep' is located.

import vrep
import time


# ############################ LINE FOLLOWER TESTER CLASS ############################ #
# A Line follower tester object tests the given population of controller gains on
# V-REP simulated robots and returns the fitness values for each genome.
# The genomes encode controller gains for base speed and sensory feedback.
# The fitness function used measures the distance covered by the robot in a set
# trial time.
class LineFolTester():
    def __init__(self):
        pass

