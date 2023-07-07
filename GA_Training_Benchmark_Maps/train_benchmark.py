# Library imports
import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
import random
import copy
from typing import List
import itertools
import numpy as np
from dask.distributed import Client, LocalCluster
from dask import delayed
import csv
maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)
csv.field_size_limit(maxInt)
import ast
from tqdm import tqdm
from scipy import stats
import shutil

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Map.map import Map
#from Map.map import * # Dårlig kodeskik at importere en hel fil
from Agent.agent import Agent
from Agent.IDCMAPF_agent import IDCMAPF_agent
from Swarm.swarm import Swarm
from Swarm.swarm_IDCMAPF import Swarm_IDCMAPF
from Renderer.renderer import Renderer
#from Renderer.renderer_pygame import Renderer as Renderer_Pygame
from Simulator.simulator import Simulator
from IDCMAPF_Tests.tests import * # Dårlig kodeskik at importere en hel fil
from Logger.logger import Logger
from GA.GA_Rules import GA_Priority_rules
from GA.GA_Fluid import GA_Fluid

from generate_start_and_target import generate_start_and_target_to_numpy, load_position_list_from_nplist, generate_start_and_target_from_scenario, generate_start_and_target_to_list

def write_to_csv(info, filename='output.csv', append=True):
    # If append is True, open the CSV file in append mode
    mode = 'a' if append else 'w'
    
    # Open the CSV file in the specified mode
    with open(filename, mode, newline='') as file:
        writer = csv.writer(file)
        writer.writerow(info)

def count_rows(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        count = sum(1 for row in reader)  # Count the remaining rows
    return count


def main():
    #startpos_train, targetpos_train =  generate_start_and_target_to_list(number_of_experiments = max_gen, number_of_agents = num_agents,env="Environments/" + map_name + ".map")
    map_name_csv, num_agents_csv, rule_order_csv, encoding_scheme_csv, mutation_rate_csv, environment_repetitions_csv, pop_size_csv, budget_csv = 0,1,2,3,4,5,6,7
    logging_status_filename = "GA_Training_Benchmark_Maps/cases.csv"
    temp_file = "GA_Training_Benchmark_Maps/temp.csv"

    row_count = count_rows(logging_status_filename)

    max_runs_test = 1000 # runs for validation?

    with open(logging_status_filename, 'r') as log_file:
        csv_reader = csv.reader(log_file)
        headline = next(csv_reader)
        max_counter = 0
        for row in csv_reader:
            if int(row[-1]) >= 2:
                max_counter += 1
                continue
            else:
                map_name = row[map_name_csv]
                num_agents = int(row[num_agents_csv])
                rule_order = ast.literal_eval(row[rule_order_csv])
                encoding_scheme_name = row[encoding_scheme_csv]
                edge_weight = row[encoding_scheme_csv] == "edge_weight"
                mutation_rate = float(row[mutation_rate_csv])
                env_repetition = int(row[environment_repetitions_csv])
                population_size = int(row[pop_size_csv])
                budget = int(row[budget_csv])
                break
        if max_counter == row_count:
            with open('GA_Training_Benchmark_Maps/inner_script_complete.txt', 'w') as f:
                pass
            return

    chromosome_append_filename = "chromosomes.csv"
                
    # Load configurations
    startpos_test = load_position_list_from_nplist(f"GA_Training_Benchmark_Maps/Validation_configurations/{map_name}_{num_agents}_start")
    targetpos_test = load_position_list_from_nplist(f"GA_Training_Benchmark_Maps/Validation_configurations/{map_name}_{num_agents}_target")
    #startpos_test, targetpos_test =  generate_start_and_target_to_list(number_of_experiments = 1, number_of_agents = num_agents, env="Environments/" + map_name + ".map")

    ga_obj = GA_Fluid(environment_function=universal_fitness_function_with_directed_map,
                        env="Environments/" + map_name + ".map",
                        start_positions=[],
                        target_positions=[],
                        num_best_solutions_to_save = 3,
                        population_size = population_size,
                        mutation_rate = 0.1,
                        elitism = 3,
                        max_num_generations = 10000,
                        amount_of_agents = num_agents,
                        rule_order=rule_order,
                        mutation_rate_swap = 0.00,
                        mutation_rate_point = mutation_rate,
                        inter = False,
                        inter_anchorpoints_height = 8,
                        inter_anchorpoints_width = 8,
                        agent_type = IDCMAPF_agent,
                        delay = 0.0001,
                        fig_size_factor = 20,
                        node_size = 10,
                        linewidth = 0.5,
                        dpi = 40,
                        display = False,
                        max_timestep = 1000,
                        edge_weight_encoding = edge_weight,
                        budget=budget,
                        num_env_repetitions=env_repetition)
    ga_obj.fitness_exponent = 9
    soc, span, chromosome = ga_obj.run(csv_filename=chromosome_append_filename, start=None, target=None, v_num_agents=num_agents, v_env_name=map_name, v_start_pos=startpos_test, v_target_pos=targetpos_test, v_rule_order=rule_order, logging_inside_run=False)

    write_to_csv([map_name, num_agents, encoding_scheme_name, mutation_rate, env_repetition, population_size, budget, soc, span, chromosome], filename="GA_Training_Benchmark_Maps/chromosomes.csv")

    with open(logging_status_filename, 'r') as input_file, open(temp_file, 'w', newline='') as output_file:
        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(next(csv_reader))

        for row in csv_reader:
            if map_name == row[map_name_csv] and num_agents == int(row[num_agents_csv]) and encoding_scheme_name == row[encoding_scheme_csv] and mutation_rate == float(row[mutation_rate_csv]) and population_size == int(row[pop_size_csv]) and env_repetition == int(row[environment_repetitions_csv]):
                #new_row = row
                row[-1] = str(int(row[-1]) + 1) # check if this update row
                #csv_writer.writerow(row)
            csv_writer.writerow(row)

    shutil.move(temp_file, logging_status_filename)

    
if __name__ == '__main__':
    cluster = LocalCluster()
    client = Client(cluster)
    print(f"Link to dask dashboard {client.dashboard_link}")
    main()