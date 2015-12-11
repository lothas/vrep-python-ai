__author__ = 'Jonathan Spitz'

import numpy as np
import matplotlib.pyplot as plt
import time


# ############################ CURVE FIT TESTER CLASS ############################ #
# A Curve fit tester object tests the given population and returns the fitness
# values for each genome.
# The genomes encode function parameters, e.g.: A*sin(B*x+C)
# The fitness function used measures the distance between the data-points provided
# and the function encoded by the genome.
class CurveFitTester():
    def __init__(self, data_x, data_y):
        self.name = "curve-fit tester"
        self.data_x = data_x
        self.data_y = data_y

    def test_pop(self, pop):
        fitness = []
        for gen in pop:
            gen_fit = self.test_gen(gen)
            fitness.append(gen_fit)

        # fitness = super(CurveFitTester, self).test_pop(pop)
        # TODO: Figure out how to properly use inheritance in python

        # Plot the best solution
        best = fitness.index(max(fitness))
        self.test_gen(pop[best], 1)

        return fitness

    def test_gen(self, gen, plot=0):
        fitness = 0
        # Calculate the fitness values for the genomes
        for x, y in zip(self.data_x, self.data_y):
            # Calculate the estimated value from the curve-fit
            y_est = gen[0]*np.sin(gen[1]*x+gen[2])
            dist = (y_est-y)**2
            fitness += dist

        if plot:
            y = gen[0]*np.sin(gen[1]*self.data_x+gen[2])
            plt.plot(self.data_x, y)
            plt.plot(self.data_x, self.data_y)
            plt.show()

        return -fitness
        # (we want to maximize fitness, so we take the sum of squares as a
        #  "penalty" to be minimized)





