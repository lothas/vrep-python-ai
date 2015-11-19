__author__ = 'Lothas'


# ############################## GENETIC ALGORITHM CLASS ############################## #
# A GenAlg object runs a genetic algorithm optimization for a given problem.
# To create an object you'll need to provide:
#       * A population size
#       * Max number of generations to run
#       * A testing object with a "testPop" method
#       * A selection object with a "selectPop" method
#       * A reproduction object with a "buildPop" method
# If no initial population is passed to the constructor, "buildPop" will be called to
# generate a random initial population.
# An end-condition function handle can be passed to stop the optimization. GenAlg will
# call this function and pass the fitness values encountered thus far. The function
# should return 0 to continue the optimization or 1 to stop the optimization. If no
# endCond is passed, GenAlg will run until the max number of generations is reached.
class GenAlg:
    # GenAlg constructor
    def __init__(self, n_genomes, n_generations, tester, picker, builder, init_pop=0, end_cond=0):
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
            init_pop = self.Builder.buildPop(n_genomes)

        # Get the genome size from the new population
        self.genomeLen = len(init_pop[0])

        # Prepare the data structures
        self.Gens = [init_pop]      # Stores all the genomes
        self.Fits = []              # Stores all the fitness values
        self.Parents = []           # Stores all the 

        self.curGen = 0
    # End GenAlg constructor

    def run(self):
        # While the end-condition or the max. number of generations hasn't been reached do:
        while self.curGen < self.nGenerations and not self.endCond(self.Fits[self.curGen]):
            # Calculate the current population's fitness
            fitness = self.Tester.testPop(self.Gens[self.curGen])
            self.Fits.append(fitness)

            # Select the top population for reproduction
            top_pop = self.Picker.selectPop(fitness)

    @staticmethod
    def false_cond():
        return 0

