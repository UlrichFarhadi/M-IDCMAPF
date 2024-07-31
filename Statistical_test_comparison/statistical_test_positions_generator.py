import sys
import os

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from generate_start_and_target import generate_start_and_target_to_numpy

# We need to generate a number of start/target configurations to statistically compare the default case (no path cost optimization) with the optimized version
# This ensures that it is the SAME configurations (start/target positions) that are being used to make a fair comparison.

# ------------ You need to change these variables for each map you want to run ------------#
map_name = "experiment_map" # Change this name with the map you need to test
number_of_agents = 15 # IMPORTANT: if you have multiple "number of agents" in your cases.csv, then you need to run this script for each of that "num agent" amount beforehand
# -----------------------------------------------------------------------------------------#

# Don't change this below
path_of_positions = "Statistical_test_comparison/start_and_target_positions_for_experiments" # Do not change this path, the other code uses its relative path.
number_of_experiments = 1000 # The more the better (central limit theorem), 1000 is sufficient.
agents_name_path = path_of_positions + "/" + map_name + "_" + str(number_of_agents) # No need to change this
generate_start_and_target_to_numpy(number_of_experiments, number_of_agents, "Environments/" + map_name + ".map", agents_name_path + "_agents_start", agents_name_path + "_agents_target")

# We also need to generate the validation set used for evaluating each generation in the GA. This needs to be different to the one used for statistical test:
path_of_validation_positions = "GA_Training_Benchmark_Maps/Validation_configurations"
agents_name_path_validation = path_of_validation_positions + "/" + map_name + "_" + str(number_of_agents)
generate_start_and_target_to_numpy(number_of_experiments, number_of_agents, "Environments/" + map_name + ".map", agents_name_path_validation + "_start", agents_name_path_validation + "_target")