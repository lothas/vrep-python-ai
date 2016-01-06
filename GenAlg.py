__author__ = 'Jonathan Spitz'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime
import json

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
    def __init__(self, n_genomes, n_generations, tester, picker, builder, init_pop=0, end_cond=0, filename=[]):
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

        # Data saving info
        if not filename:
            self.save_filename = "GA-" + datetime.datetime.now().strftime("%m_%d-%H_%M") + ".txt"
        else:
            self.save_filename = filename
        self.description = "Results for GA with " + self.Tester.name + ", " + self.Picker.name + " and " \
                           + self.Builder.name + ".\n" \
                           + "Ran a population of " + str(self.nGenomes) + " over {0} generations on " \
                           + datetime.datetime.now().strftime("%Y-%m-%d starting at %H:%M")

        self.curGen = 0
    # End GenAlg constructor

    def load(self, filename):
        # Load data from the save file provided
        with open(filename, 'r') as f:
            data = json.load(f)
            print bcolors.OKGREEN + "Loaded data from " + filename + ":" + bcolors.ENDC
            print bcolors.OKBLUE + data[0] + bcolors.ENDC + "\n"
            self.Gens = [data[1][-1]]
        return self

    def run(self):
        if self.verbose:
            print bcolors.HEADER + bcolors.BOLD + "Running Genetic Algorithm..." + bcolors.ENDC

        # Open save file with 'w' to clean it up
        with open(self.save_filename, 'w') as f:
            f.close()


        # While the end-condition or the max. number of generations hasn't been reached do:
        while self.curGen < self.nGenerations and not self.endCond(self.Fits):
            if self.verbose:
                print bcolors.OKGREEN + "Running generation " + str(self.curGen) + \
                    " out of " + str(self.nGenerations) + bcolors.ENDC
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
                print bcolors.OKBLUE + "Top fitness results: "+str(fit_max)
                print "Avg. fitness results: "+str(fit_mean)
                print "" + bcolors.ENDC

            # Save results
            with open(self.save_filename, 'w') as f:
                output = [self.description.format(self.curGen+1), self.Gens, self.Fits]
                json.dump(output, f)
                f.close()

            # Select the top population for reproduction
            top_pop = self.Picker.pick_pop(self.nGenomes, fitness)

            # TODO: change the code so the generalisation of "GenAlg will not change
            # Rea's addition:
            if True: #display data for biPed robot change for other models
                genesNames = ["omega", "phi_start1", "phi_start2", "Amplitude",
                              "phi_start1", "phi_start2", "Amplitude",
                              "phi_start1", "phi_start2", "Amplitude",
                              "x_fitness", "y_fitness", "z_fitness"]
                bestFitnessOfBestGenes = [fitness[i] for i in top_pop]
                currentBestGenes = [self.Gens[self.curGen][i] for i in top_pop]
                currentBestGenes1 = np.concatenate((currentBestGenes, bestFitnessOfBestGenes), axis=1)
                currentBestGenesRounded = np.around(currentBestGenes1, decimals=4) #round the array for aesthetics
                row_format = "{:>15}" * (len(genesNames) + 1)
                print row_format.format("", *genesNames)
                for Gene, row in zip(np.arange(len(currentBestGenesRounded))+1, currentBestGenesRounded):
                   print row_format.format(str(Gene)+")", *row)
                print "" + bcolors.ENDC
            ###############

            # Build the next generation
            new_pop, parents = self.Builder.build_pop(self.Gens[self.curGen], top_pop)
            self.Gens.append(new_pop)
            self.Parents.append(parents)

            # Advance the generation counter
            self.curGen += 1

        if self.verbose:
            print 'Finished running Genetic Algorithm'

            plt.figure(1)
            plt.plot(range(self.nGenerations), self.fit_max)
            plt.xlabel('Generation number')
            plt.ylabel('Max fitness')
            plt.grid(True)
            plt.legend(['x_fit', 'y_fit', 'z_fit'])
            plt.show()

            plt.figure(2)
            plt.plot(range(self.nGenerations), self.fit_mean)
            plt.xlabel('Generation number')
            plt.ylabel('Mean fitness')
            plt.grid(True)
            plt.legend(['x_Mean_Fit', 'y_Mean_Fit', 'z_Mean_Fit'])
            plt.show()

        return self

    @staticmethod
    def false_cond():
        return 0


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'