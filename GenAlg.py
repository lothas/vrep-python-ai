__author__ = 'Jonathan Spitz'

import numpy as np
import matplotlib.pyplot as plt

# ############################## GENETIC ALGORITHM CLASS ############################## #
# A GenAlg object runs a genetic algorithm optimization for a given problem.
# To create an object you'll need to provide:
#       * A population size
#       * Max number of generations to run
#       * A testing object with a "test_pop" method
#       * A selection object with a "pick_pop" method
#       * A reproduction object with a "build_pop" method
# If no initial population is passed to the constructor, "build_pop" will be called to
# generate a random initial population.
# An end-condition function handle can be passed to stop the optimization. GenAlg will
# call this function and pass the fitness values encountered thus far. The function
# should return 0 to continue the optimization or 1 to stop the optimization. If no
# endCond is passed, GenAlg will run until the max number of generations is reached.
class GenAlg:
    # GenAlg constructor
    def __init__(self, n_genomes, n_generations, tester, picker, builder, init_pop=0, end_cond=0):
        self.verbose = True  # Set to true to print out intermediate optimization results

        self.nGenomes = n_genomes
        self.nGenerations = n_generations
        self.endCond = end_cond

        self.Tester = tester
        self.Picker = picker
        self.Builder = builder

        # Store the endCond function handle or use the built-in "0" function
        if hasattr(end_cond, '__call__'):
            self.endCond = end_cond
        else:
            self.endCond = lambda fits: self.false_cond()

        # Prepare initial population if none was given
        if not init_pop:
            init_pop, init_par = self.Builder.build_pop(n_genomes)
        else:
            init_par = [[] for i in range(n_genomes)]

        # Get the genome size from the new population
        self.genomeLen = len(init_pop[0])

        # Prepare the data structures
        self.Gens = [init_pop]      # Stores all the genomes
        self.Fits = []              # Stores all the fitness values
        self.Parents = init_par     # Stores all the genome parents (for ancestry)

        self.fit_max = []           # Stores the max fitness values
        self.fit_mean = []          # Stores the mean fitness values

        self.curGen = 0
    # End GenAlg constructor

    def run(self):
        if self.verbose:
            print "Running Genetic Algorithm..."

        # While the end-condition or the max. number of generations hasn't been reached do:
        while self.curGen < self.nGenerations and not self.endCond(self.Fits):
            if self.verbose:
                print "Running generation " + str(self.curGen) + \
                    " out of " + str(self.nGenerations)
                # TODO: calculate a run-time estimate for each generation

            # Calculate the current population's fitness
            fitness = self.Tester.test_pop(self.Gens[self.curGen])
            self.Fits.append(fitness)

            fit_array = np.array(fitness)
            fit_max = np.max(fit_array, 0)
            fit_mean = np.mean(fit_array, 0)
            self.fit_max.append(fit_max.tolist())
            self.fit_mean.append(fit_mean.tolist())

            if self.verbose:
                # Print average and max fitness values
                print "Top fitness results: "+str(fit_max)
                print "Avg. fitness results: "+str(fit_mean)
                print ""

            # Select the top population for reproduction
            top_pop = self.Picker.pick_pop(self.Gens[self.curGen], fitness)

            # Build the next generation
            new_pop, parents = self.Builder.build_pop(self.Gens[self.curGen], top_pop)
            self.Gens.append(new_pop)
            self.Parents.append(parents)

            # Advance the generation counter
            self.curGen += 1

        if self.verbose:
            print 'Finished running Genetic Algorithm'
            plt.plot(range(self.nGenerations),self.fit_max)
            plt.plot(range(self.nGenerations),self.fit_mean)
            plt.show()

    @staticmethod
    def false_cond():
        return 0

