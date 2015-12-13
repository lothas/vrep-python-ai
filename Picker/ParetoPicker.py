__author__ = 'Jonathan Spitz'

import numpy as np
import copy


# ############################ PARETO PICKER CLASS ############################ #
# A Pareto picker object selects the best genomes from a population based on
# multiple fitness values. The genomes are divided into Pareto fronts and the
# first N genomes taken from the outer-most fronts are returned as the top
# population.
class ParetoPicker():
    def __init__(self, n):
        self.n_top = n  # number of top genomes to select from population
        # (can be passed as a % of the population, in which case it will
        #  select the floor(%*pop_size) top genomes.
        self.name = "Pareto picker"

    def pick_pop(self, n_genomes, fit):
        # How many items do we need to pick?
        if type(self.n_top) == float:
            n_top = np.floor(self.n_top*n_genomes)
        else:
            n_top = self.n_top

        fronts = ParetoPicker.pareto(fit, n_genomes)

        short_list = []
        for f in fronts:
            for i in f:
                short_list.append(i)
                if len(short_list) == n_top:
                    return short_list

    @staticmethod
    def dominates(point_a, point_b):
        p_len = len(point_a)
        greater = [a > b for a, b in zip(point_a, point_b)]
        geq = [a >= b for a, b in zip(point_a, point_b)]
        if sum(greater) >= 1 and sum(geq) == p_len:
            # Point A dominates Point B
            return 1
        if sum(geq) == 0:
            # Point B strictly dominates Point A
            return -1
        return 0  # no point dominates

    @staticmethod
    def get_front(t_points):
        # Receives a list of tagged points and returns the non-dominated tags
        f_points = copy.copy(t_points)  # create a copy of the data
        cur_point_a = 0
        while True:
            cur_point_b = 0

            while True:
                if cur_point_b == cur_point_a:
                    cur_point_b += 1
                if cur_point_b >= len(f_points):
                    # Reached the end of the list
                    cur_point_a += 1
                    break

                # print cur_point_a, cur_point_b
                res = ParetoPicker.dominates(f_points[cur_point_a][1], f_points[cur_point_b][1])

                if res == 1:
                    # Point A dominates point B, remove point B
                    f_points.pop(cur_point_b)
                elif res == -1:
                    # Point B dominates point A, remove point A
                    f_points.pop(cur_point_a)
                    break
                else:
                    cur_point_b += 1

                if cur_point_a >= len(f_points):
                    # Reached the end of the list
                    break

            if cur_point_a >= len(f_points):
                # Reached the end of the list
                break

        return [f_points[tid][0] for tid in range(len(f_points))]

    @staticmethod
    def pareto(points, n):
        # Add an ID tag to the points
        t_points = [[tag, points[tag]] for tag in range(len(points))]

        fronts = []
        n_items = 0
        while len(t_points) > 0:
            # Get the outer-most Pareto front
            front_ids = ParetoPicker.get_front(t_points)
            front_ids.sort()
            fronts.append(front_ids)
            n_items += len(front_ids)
            if n_items >= n:
                break

            # Take out the front's points
            j = 0
            k = 0
            while True:
                if t_points[j][0] == fronts[-1][k]:
                    t_points.pop(j)
                    k += 1
                    if k >= len(fronts[-1]):
                        break
                else:
                    j += 1
                if j >= len(t_points):
                    break
        return fronts