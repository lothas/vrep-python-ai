__author__ = 'Jonathan Spitz'

from Tester import LineFolTester
# from Picker import ParetoPicker
from Picker import SinglePicker
from Builder import Builder
from GenAlg import GenAlg

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
    n_genomes = 300
    n_generations = 20

    base_val = 1
    sens_val = 2
    gen_max = [base_val, sens_val, sens_val, sens_val,
               base_val, sens_val, sens_val, sens_val]
    gen_min = [-val for val in gen_max]

    # Generation build plan
    top_n = 0.2
    build_plan = [[top_n],
                  [top_n, 'randn_mut'],
                  [1-2*top_n, 'rand_pair_pick', 'n_point_cross', 'randn_mut']]

    # Create objects
    tester = LineFolTester.LineFolTester()
    picker = SinglePicker.SinglePicker(top_n)
    builder = Builder.Builder(gen_min, gen_max, n_genomes, build_plan)

    GA = GenAlg(n_genomes, n_generations, tester, picker, builder)
    GA = GA.run()