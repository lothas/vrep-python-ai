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
    n_genomes = 10  # was 25 before...
    n_generations = 5

    omega_val = 10
    phi_start_val = 0.8
    phi_end_val = 0.9  # phi_end can't be smaller than phi_start!
    amplitude_val = 20
    gen_max = [omega_val, phi_start_val, phi_end_val, amplitude_val,
               omega_val, phi_start_val, phi_end_val, amplitude_val,
               omega_val, phi_start_val, phi_end_val, amplitude_val]
    gen_min = [omega_val-0.01, 0, 0.1, -amplitude_val,
               omega_val-0.01, 0, 0.1, -amplitude_val,
               omega_val-0.01, 0, 0.1, -amplitude_val]

    # Generation build plan
    top_n = 0.2
    build_plan = [[top_n, 'randn_mut'],
                  [1-top_n, 'rand_pair_pick', 'n_point_cross', 'randn_mut']]

    # Create objects
    tester = WalkerTester.WalkerTester(5, 'Leg1')
    picker = ParetoPicker.ParetoPicker(top_n)
    builder = Builder.Builder(gen_min, gen_max, n_genomes, build_plan)

    filename = "WalkerGA-" + datetime.datetime.now().strftime("%m_%d-%H_%M") + ".txt"
    GA = GenAlg(n_genomes, n_generations, tester, picker, builder, filename=filename)

    # Load data from save file
    # GA = GA.load("LineFolGA-12_11-09_34.txt")

    GA = GA.run()
    print(GA.Fits)
    print(GA.Gens)

    tester.disconnect()