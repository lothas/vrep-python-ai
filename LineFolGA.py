__author__ = 'Jonathan Spitz'

from Tester import LineFolTester
from Picker import ParetoPicker
# from Picker import SinglePicker
from Builder import Builder
from GenAlg import GenAlg
import datetime

# ######################### SINE GEN. ALG. SCRIPT ######################### #
# Optimize the control gains for a simple 2-wheeled robot with 3 light
# sensors on its front. The speed for the left and right wheels is set by:
#   left_speed = k11 + k12 * left_sensor + k13 * middle_sensor +
#                k14 * right_sensor
#   right_speed = k21 + k22 * left_sensor + k23 * middle_sensor +
#                 k24 * right_sensor
#
#   Fit: distance traveled along x, -distance from x-axis
#   Encode: float signals for v-rep simulated robots
#   Genome: [k11, k12, k13, k14, k21, k22, k23, k24]
#   Select by pareto front with cluster weight
#   Reproduce: n-point crossover + mutation


if __name__ == '__main__':
    # Genetic algorithm parameters
    n_genomes = 25
    n_generations = 100

    base_val = 4
    sens_val = 8
    gen_max = [base_val, sens_val, sens_val, sens_val,
               base_val, sens_val, sens_val, sens_val]
    gen_min = [-val for val in gen_max]

    # Generation build plan
    top_n = 0.2
    build_plan = [[top_n, 'randn_mut'],
                  [1-top_n, 'rand_pair_pick', 'n_point_cross', 'randn_mut']]

    # Create objects
    tester = LineFolTester.LineFolTester(5, 'LineFolR')
    picker = ParetoPicker.ParetoPicker(top_n)
    builder = Builder.Builder(gen_min, gen_max, n_genomes, build_plan)

    filename = "LineFolGA-" + datetime.datetime.now().strftime("%m_%d-%H_%M") + ".txt"
    GA = GenAlg(n_genomes, n_generations, tester, picker, builder, filename=filename)

    # Load data from save file
    # GA = GA.load("LineFolGA-12_11-09_34.txt")

    GA = GA.run()
    print(GA.Fits)
    print(GA.Gens)

    tester.disconnect()