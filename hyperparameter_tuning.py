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
import ast
from tqdm import tqdm
from scipy import stats

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

def main():
    
    def write_to_csv(tune_population_size, tune_mutation_rate, tune_fitness_exponent, tune_env_repetition, sum_of_cost, make_span, filename='output.csv', append=True):
        # If append is True, open the CSV file in append mode
        mode = 'a' if append else 'w'
        
        # Open the CSV file in the specified mode
        with open(filename, mode, newline='') as file:
            writer = csv.writer(file)
                
            # Append the experiment list (as a string) to the CSV file
            writer.writerow([tune_population_size, tune_mutation_rate, tune_fitness_exponent, tune_env_repetition, sum_of_cost, make_span,])

    
    def write_to_csv(list_to_write, filename='output.csv', append=True):
        # If append is True, open the CSV file in append mode
        mode = 'a' if append else 'w'
        
        # Open the CSV file in the specified mode
        with open(filename, mode, newline='') as file:
            writer = csv.writer(file)
                
            # Append the experiment list (as a string) to the CSV file
            writer.writerow(list_to_write)

    rule_order = [0, 4, 3, 1, 5, 6, 2]
    num_agents = 30
    max_gen = 200
    map_name = "random-10-10-20"
    max_runs_test = 1000
    edge_weight = False
    if edge_weight:
        folder = "edge_weight"
    else:
        folder = "node_vector"

    #startpos_train, targetpos_train =  generate_start_and_target_to_list(number_of_experiments = max_gen, number_of_agents = num_agents,env="Environments/" + map_name + ".map")
    startpos_test, targetpos_test =  generate_start_and_target_to_list(number_of_experiments = max_runs_test, number_of_agents = num_agents,env="Environments/" + map_name + ".map")

    folder_number = 0
    while True:
        if not os.path.exists(f"Tuning_data_ga/{folder}/{folder_number}"):
        # Create the folder
            os.makedirs(f"Tuning_data_ga/{folder}/{folder_number}")
        #print(f"Folder '{folder_name}' created successfully.")
        else:
            folder_number +=1
            continue
        for tune_mutation_rate in [0.05, 0.10, 0.15]:
            for tune_population_size in [30, 40, 50]:
                for tune_env_repetition in [5, 10, 15, 20]:
                    
                    ga_obj = GA_Fluid(environment_function=universal_fitness_function_with_directed_map,
                                        env="Environments/" + map_name + ".map",
                                        start_positions=[],
                                        target_positions=[],
                                        num_best_solutions_to_save = 3,
                                        population_size = tune_population_size,
                                        mutation_rate = 0.1,
                                        elitism = 3,
                                        max_num_generations = 200,
                                        amount_of_agents = num_agents,
                                        rule_order=rule_order,
                                        mutation_rate_swap = 0.00,
                                        mutation_rate_point = tune_mutation_rate,
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
                                        budget=20000)
                    ga_obj.fitness_exponent = 9
                    ga_obj.num_env_repetitions = tune_env_repetition
                    # Save
                    chromosome = ga_obj.run(csv_filename=f"Tuning_data_ga/{folder}/{folder_number}/_{tune_population_size}_{tune_mutation_rate}_{tune_env_repetition}_GA", start=None, target=None, v_num_agents=num_agents, v_env_name=map_name, v_start_pos=startpos_test, v_target_pos=targetpos_test, v_rule_order=rule_order)
                    #sum_of_cost , make_span = validator(num_agents=num_agents, env_name=map_name, fluid=chromosome, start_pos=startpos_test, target_pos=targetpos_test, rule_order=rule_order)
                    #write_to_csv(tune_population_size, tune_mutation_rate, tune_fitness_exponent, tune_env_repetition, sum_of_cost, make_span, filename='Tuning_data_ga/output.csv')
                    #write_to_csv([chromosome, sum_of_cost, make_span], filename='Tuning_data_ga/new_GA_hyperparameters_validation.csv')
        folder_number +=1


if __name__ == '__main__':
    cluster = LocalCluster()
    client = Client(cluster)
    print(f"Link to dask dashboard {client.dashboard_link}")
    main()