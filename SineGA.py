__author__ = 'Jonathan Spitz'

import numpy as np
from Tester import CurveFitTester
from Picker import SinglePicker
from Builder import Builder
from GenAlg import GenAlg

# ######################### SINE GEN. ALG. SCRIPT ######################### #
# Optimize a curve-fit of a sine function to given (x,y) data.
#   Fit: sum of distance squares
#   Encode: A*sin(B*x+C)
#   Genome: [A B C], min [0 0 0], max [10, 100, 2*pi]
#   Select by best fit (single fit, simple)
#   Reproduce: n-point crossover + mutation

if __name__ == '__main__':
    # Genetic algorithm parameters
    n_genomes = 500
    n_generations = 20

    gen_min = [0, 0, 0]
    gen_max = [10, 100, 2*np.pi]

    # Generate random sine data
    Amp = 3.
    Omega = 5.
    Phi = np.pi/2.
    xError = 0.05
    yError = 0.01*Amp

    x = np.array(np.array(range(0, 30))/10.0)
    x += np.random.rand(1, len(x))[0]*xError
    y = np.array(Amp*np.sin(Omega*x + Phi))
    y += np.random.rand(1, len(y))[0]*yError

    # Generation build plan
    top_n = 0.2
    build_plan = [[top_n],
                  [top_n, 'randn_mut'],
                  [1-2*top_n, 'rand_pair_pick', 'n_point_cross', 'randn_mut']]

    # Create objects
    tester = CurveFitTester.CurveFitTester(x, y)
    picker = SinglePicker.SinglePicker(top_n)
    builder = Builder.Builder(gen_min, gen_max, n_genomes, build_plan)

    GA = GenAlg(n_genomes, n_generations, tester, picker, builder)
    GA = GA.run()
