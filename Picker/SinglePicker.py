__author__ = 'Jonathan Spitz'

import numpy as np


# ############################ SINGLE PICKER CLASS ############################ #
# A Single picker object selects the best genomes from a population based on
# a single fitness value. The genomes are sorted by decreasing fitness and the
# first N genomes are returned as the top population.
class SinglePicker():
    def __init__(self, n):
        self.n_top = n  # number of top genomes to select from population
        # (can be passed as a % of the population, in which case it will
        #  select the floor(%*pop_size) top genomes.

    def pick_pop(self, pop, fit):
        # Create a structured array
        st_ar = []
        dtype = [('id', int), ('fit1', type(fit))]
        for i in range(len(fit)):
            st_ar.append((i, fit[i]))
        st_ar = np.array(st_ar, dtype)

        # Sort the array by the fitness value
        sort_st_array = np.sort(st_ar, order='fit1')
        dsort = sort_st_array[::-1]  # inverted array (descending order of fit)

        # Select the best items from pop
        if type(self.n_top) == float:
            n_top = np.floor(self.n_top*len(pop))
        else:
            n_top = self.n_top
        short_list = dsort[:n_top]['id']

        return short_list
