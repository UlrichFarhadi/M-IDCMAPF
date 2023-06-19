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


    #startpos_train, targetpos_train =  generate_start_and_target_to_list(number_of_experiments = max_gen, number_of_agents = num_agents,env="Environments/" + map_name + ".map")
    map_name_csv, num_agents_csv, rule_order_csv, encoding_scheme_csv = 0,1,2,3
    logging_status_filename = "Best_chromosomes/logging_status_edge.csv"
    temp_file = "Best_chromosomes/temp.csv"

    max_runs_test = 1000
    budget = 20000
    
    while True:

        with open(logging_status_filename, 'r') as log_file:
            csv_reader = csv.reader(log_file)
            headline = next(csv_reader)
            max_counter = 0
            for row in csv_reader:
                if int(row[-1]) == 10:
                    max_counter += 1
                    continue
                else:
                    rule_order = ast.literal_eval(row[rule_order_csv])
                    num_agents = int(row[num_agents_csv])
                    map_name = row[map_name_csv]
                    edge_weight = row[encoding_scheme_csv] == "edge_weight"
                    encoding_scheme_name = row[encoding_scheme_csv]
                    break
            if max_counter == 12:
                break
                
        # Load logging_status.csv
        #   Gå linjerne igennem fra top til bund og se hvilke der mangler at køre (dem under 10 runs)
        #   Gem rule order, agents, map navn
        #   Run 1 iteration
        #   Gem validation resultatet (måske bruger vi det til at selektere senere) og kromosomet i en fil ved navn "map_name_agents_chromosomes"
        #       Hvis ikke filen eksisterer, lav en ny, ellers append til den.
        #       UPDATE finished_amt variablen

        # Set the training hyperparameters
        if edge_weight:
            population_size = 50
            mutation_rate = 0.1
            env_repetition = 5
        else:
            population_size = 40
            mutation_rate = 0.1
            env_repetition = 15

        chromosome_append_filename = f"{map_name}_{num_agents}_{encoding_scheme_name}"
                    
        startpos_test, targetpos_test =  generate_start_and_target_to_list(number_of_experiments = max_runs_test, number_of_agents = num_agents,env="Environments/" + map_name + ".map")
        ga_obj = GA_Fluid(environment_function=universal_fitness_function_with_directed_map,
                            env="Environments/" + map_name + ".map",
                            start_positions=[],
                            target_positions=[],
                            num_best_solutions_to_save = 3,
                            population_size = population_size,
                            mutation_rate = 0.1,
                            elitism = 3,
                            max_num_generations = 200,
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
        chromosome = ga_obj.run(csv_filename=chromosome_append_filename, start=None, target=None, v_num_agents=num_agents, v_env_name=map_name, v_start_pos=startpos_test, v_target_pos=targetpos_test, v_rule_order=rule_order)

        with open(logging_status_filename, 'r') as input_file, open(temp_file, 'w', newline='') as output_file:
            csv_reader = csv.reader(input_file)
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(next(csv_reader))

            for row in csv_reader:
                if map_name == row[map_name_csv] and num_agents == int(row[num_agents_csv]) and encoding_scheme_name == row[encoding_scheme_csv]:
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