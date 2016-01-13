__author__ = 'Rea Yakar'
# based on the code of Jonathan Spitz

from Tester import WalkerTester
from Picker import ParetoPicker
# from Picker import SinglePicker
from Builder import Builder
from GenAlg import GenAlg
import datetime

# ######################## WALKER GEN. ALG. SCRIPT ######################### #
# Optimize the CPG control parameters for a simple biped robot with 3 joints
#
#   Fit: distance traveled along x, -distance from x-axis
#   Encode: float signals for v-rep simulated robots
#   Genome: [omega, phi_start, phi_end, torque_amplitude] for each motor (omega is the same for all motors!)
#   Select by pareto front with cluster weight
#   Reproduce: n-point crossover + mutation


if __name__ == '__main__':
    # Genetic algorithm parameters
    n_genomes = 200
    n_generations = 10
    simTimeLimit = 5  # t in [seconds]

    genesNames = ["omega", "phi_start1", "phi_end1", "Amplitude",
                  "phi_start1", "phi_end2", "Amplitude",
                  "phi_start1", "phi_end3", "Amplitude"]
    FitNames = ["x_fitness", "U_fit", "STS_fitness"]

    gen_max = [5, 0.9, 0.09, 40,
               0.9, 0.09, 30,
               0.9, 0.09, 30]
    gen_min = [0.3, 0, 0.01, 0,
               0, 0.01, -30,
               0, 0.01, -30]
        # TODO: 3) add to the fitness energy calculation

    # Generation build plan
    top_n = 0.2
    build_plan = [[top_n, 'randn_mut'],
                  [1-top_n, 'rand_pair_pick', 'n_point_cross', 'randn_mut']]

    # Create objects
    tester = WalkerTester.WalkerTester(5, simTimeLimit, 'Leg1')
    picker = ParetoPicker.ParetoPicker(top_n)
    builder = Builder.Builder(gen_min, gen_max, n_genomes, build_plan)

    filename = "WalkerGA_try4-" + datetime.datetime.now().strftime("%m_%d-%H_%M") + ".txt"
    GA = GenAlg(n_genomes, n_generations, tester, picker, builder,  genesNames, FitNames, filename=filename)

    # Load data from save file
    GA = GA.load("WalkerGA_try4-01_12-16_09.txt")

    GA = GA.run()
    print(GA.Fits)
    print(GA.Gens)

    tester.disconnect()
