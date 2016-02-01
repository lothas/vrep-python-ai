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
    n_genomes = 20
    n_generations = 2
    simTimeLimit = 3  # t in [seconds]

    genesNames = ["omega", "phi_s_Hip", "phi_e_Hip", "Amp_Hip",
                  "phi_s_knee1", "phi_e_knee1", "Amp_knee1",
                  "phi_s_knee2", "phi_e_knee2", "Amp_knee2",
                  "phi_s_toeOff", "dphi_toeOff", "Amp_toeOff",
                  "phi_s_flex", "dphi_flex", "Amp_flex"]
    FitNames = ["x_fitness", "U_fit", "STS_fitness"]

    # temp change: 1) toe_off start = 0 always
    #              2) phiStart_flex = delta_phi_toeOff
    #              3) phiStart_hip_real = delta_phi_toeOff + phiStart_hip (that I give in Python)
    gen_max = [0.8, 0.05, 0.1, -10,
               0.9, 0.09, 20,
               0.9, 0.09, 20,
               0.01, 0.2, -15,
               0.4, 0.2, 4]
    gen_min = [0.4, 0, 0.01, -25,
               0, 0.01, 0,
               0, 0.01, 0,
               0, 0.05, -25,
               0.1, 0.1, 2]

    # Generation build plan
    top_n = 0.2
    build_plan = [[top_n, 'randn_mut'],
                  [1-top_n, 'rand_pair_pick', 'n_point_cross', 'randn_mut']]

    # Create objects
    tester = WalkerTester.WalkerTester(5, simTimeLimit, 'Leg1')
    picker = ParetoPicker.ParetoPicker(top_n)
    builder = Builder.Builder(gen_min, gen_max, n_genomes, build_plan)

    filename = "WalkerGA_noKnee-" + datetime.datetime.now().strftime("%m_%d-%H_%M") + ".txt"
    best_filename = "WalkerGA_BestPop-" + datetime.datetime.now().strftime("%m_%d-%H_%M") + ".txt"
    GA = GenAlg(n_genomes, n_generations, tester, picker, builder,  genesNames, FitNames, filename=filename, filename1=best_filename)

    # Load data from save file
    # GA = GA.load("WalkerGA_noKnee_try3-01d_31-09_49.txt")

    GA = GA.run
    print(GA.Fits)
    print(GA.Gens)

    tester.disconnect()
