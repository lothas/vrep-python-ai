__author__ = 'Jonathan Spitz'

import numpy as np


# ##################################### BUILDER CLASS ##################################### #
# A Builder object creates a new population using a given population by applying
# reproduction operators like crossover and mutation.
# To create an object you'll need to provide a build plan for the new generation:
#   [(pop%, picker, operator1, operator2, ..., operatorn), (pop%, ...), ...]
#   for example:
#       [[0.1], [0.1, '', 'mutation'], [0.8, 'rand_pick', 'n_point_cross', 'mutation']]
class Builder():
    def __init__(self, gen_min, gen_max, pop_size, build_plan):
        self.gen_min = gen_min          # Min. values for genome
        self.gen_max = gen_max          # Max. values for genome
        self.pop_size = pop_size        # Population size to be created
        self.build_plan = build_plan    # Instructions on how to build the new population

        self.mut_strength = 0.03        # Percentage of max-min variation added as mutation

    def build_pop(self, pop, top_ids=None):
        if type(pop) is int:
            # A single value was passed = number of genes
            # required for initial generation
            new_pop = [
                [g_min+(1-np.random.random())*(g_max-g_min)
                 for g_min, g_max in zip(self.gen_min, self.gen_max)]
                for i in range(pop)]
            parents = [[] for i in range(pop)]
        else:
            top_pop = [pop[id] for id in top_ids]
            new_pop = []
            parents = []
            for batch in self.build_plan:
                # Set the number of genomes to create on this batch
                if batch != self.build_plan[-1]:
                    n_genomes = int(np.floor(batch[0]*self.pop_size))
                else:
                    n_genomes = self.pop_size - len(new_pop)

                # Grab the desired number of genomes from top_pop
                # (or all of top_pop if n_genomes>len(top_pop))
                pop_batch = top_pop[:n_genomes]
                par_batch = [[id] for id in top_ids]
                for step in batch[1:]:
                    # Perform the building step
                    pop_batch, par_batch = \
                        getattr(self, step)(pop_batch, par_batch, n_genomes)

                # Add the new batch to the population
                new_pop += pop_batch
                parents += par_batch
        return new_pop, parents

    @staticmethod
    def rand_pick(pop, parents, n_genomes):
        n_pop = len(pop)
        ids = np.random.choice(range(n_pop), n_genomes)
        return [pop[id] for id in ids], ids
        # Return ids as parents

    @staticmethod
    def rand_pair_pick(pop, parents, n_genomes):
        # Pick 2N pairs at random
        n_pop = len(pop)
        ids = np.random.choice(range(n_pop), 2*n_genomes)

        # Check that the same parent wasn't repeated
        i = 0
        parents = []
        while i < n_genomes:
            # Check the pair
            while ids[2*i] == ids[2*i+1]:
                ids[2*i:2*i+2] = np.random.choice(range(n_pop), 2)
            parents.append([ids[2*i], ids[2*i+1]])
            i += 1
        return [pop[id] for id in ids], parents

    @staticmethod
    def n_point_cross(pop, parents, n_genomes):
        # Mix the given pairs using n-point crossover
        new_pop = []
        n_genes = len(pop[0])

        for i in range(n_genomes):
            offspring = []
            parent = True
            for gen in range(n_genes):
                # "Toss a coin"
                if np.random.random() >= 0.5:
                    # If "heads", take genes from the other parent
                    parent = not parent
                offspring.append(pop[2*i+(parent and 1 or 0)][gen])
            new_pop.append(offspring)

        return new_pop, parents

    def randn_mut(self, pop, parents, n_genomes):
        # Apply a normally distributed random mutation to the population
        gen_range = self.mut_strength*(np.array(self.gen_max)-np.array(self.gen_min))
        new_pop = [gen + np.random.randn(1, len(gen_range))[0]*gen_range
                   for gen in pop]
        new_pop = np.clip(new_pop, self.gen_min, self.gen_max).tolist()
        return new_pop, parents