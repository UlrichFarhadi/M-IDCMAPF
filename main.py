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
from dask import delayed, compute
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
from Map.map_directed import Map_directed
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

from generate_start_and_target import generate_start_and_target_to_numpy, load_position_list_from_nplist, generate_start_and_target_to_list, generate_start_and_target_from_scenario


def run_one_sim(num_agents, env_name, rule_order=[0,1,2,3,4,5,6], positions_for_agents=[], encoding_scheme="node_vector", encoding=[], display=False, save_video = False):
    # Create the map object
    map = Map_directed()
    # Import the environment
    env = "Environments/" + env_name + ".map"
    map.generate_map(env)
    if len(encoding) != 0:
        if encoding_scheme == "node_vector":
            map.update_weight_on_map_by_directional(encoding)
        else:
            map.update_weight_on_map(encoding)
    # Create the swarm object
    swarm = Swarm_IDCMAPF(map, amount_of_agents=num_agents, agent_type=IDCMAPF_agent, rule_order=rule_order)

    # Create the renderer object
    renderer = Renderer(map, delay=0.0001, fig_size_factor=6, node_size=75, linewidth=0.5, dpi=400)

    # Create the simulator object
    if len(positions_for_agents) == 0:
        pos = generate_start_and_target_to_list(number_of_experiments=1, number_of_agents=num_agents, env=env)
        positions_for_agents = [pos[0][0], pos[1][0]] # start/target  exoerments number
    simulator = Simulator(map, swarm, renderer, display=display, max_timestep=1000, positions_for_agents=positions_for_agents)
    cost, makespan ,_ ,_ = simulator.main_loop()

    if save_video:    
        renderer.create_animation("Videos/" + env_name + "_" + str(num_agents) + ".mp4", fps=5)

    return cost, makespan

def run_experiment(num_agents, env_name, start_position, target_position, rule_order=[0,1,2,3,4,5,6],  encoding_scheme="node_vector", encoding=[]):
    list_of_cost = []
    list_of_makespan = []
    for start_pos, target_pos in zip(start_position, target_position):
        cost, makespan = delayed(run_one_sim, nout=2)(num_agents=num_agents, env_name=env_name, rule_order=rule_order, positions_for_agents=[start_pos,target_pos], encoding_scheme=encoding_scheme, encoding=encoding)
        list_of_cost.append(cost)
        list_of_makespan.append(makespan)
    res = compute(*list_of_cost, *list_of_makespan)
    failrate = 0
    times=len(start_position)
    for span in res[times:]:
        if span == 1000:
            failrate += 1

    return res[:times], res[times:], failrate # returns cost, times

def flatten(l):
    return [item for sublist in l for item in sublist]

def exp1(num_agents, map_name, start_position, target_position):
    exp_soc, exp_makespan, exp_failrate = run_experiment(num_agents=num_agents, env_name=map_name, start_position=start_position, target_position=target_position, rule_order=[0,1,2,3,4,5,6],  encoding_scheme="node_vector", encoding=[])
    print("Default Rule Order: Average Sum of costs: ", sum(exp_soc)/len(exp_soc))
    print("Default Rule Order: Average Makespan: ", sum(exp_makespan)/len(exp_makespan))
    print("Default Rule Order: Average Failrate: ", exp_failrate / len(start_position))
    return exp_soc, exp_makespan

def exp2(num_agents, map_name, start_position, target_position):
    exp_soc, exp_makespan, exp_failrate = run_experiment(num_agents=num_agents, env_name=map_name, start_position=start_position, target_position=target_position, rule_order=[0,4,3,1,5,6,2],  encoding_scheme="node_vector", encoding=[])
    print("Best Rule Order: Average Sum of costs: ", sum(exp_soc)/len(exp_soc))
    print("Best Rule Order: Average Makespan: ", sum(exp_makespan)/len(exp_makespan))
    print("Best Rule Order: Average Failrate: ", exp_failrate / len(start_position))
    return exp_soc, exp_makespan

def exp3(num_agents, map_name, start_position, target_position):
    csv_file_path = 'node_encoding.csv'
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        csv_contents = list(csv_reader)
    # Convert the string representation of the list to an actual list
    encoding_string = csv_contents[0][0]  
    encoding = ast.literal_eval(encoding_string)

    exp_soc, exp_makespan, exp_failrate = run_experiment(num_agents=num_agents, env_name=map_name, start_position=start_position, target_position=target_position, rule_order=[0,4,3,1,5,6,2],  encoding_scheme="node_vector", encoding=encoding)
    print("Best Rule Order & Node Vector Encoding: Average Sum of costs: ", sum(exp_soc)/len(exp_soc))
    print("Best Rule Order & Node Vector Encoding: Average Makespan: ", sum(exp_makespan)/len(exp_makespan))
    print("Best Rule Order & Node Vector Encoding: Average Failrate: ", exp_failrate / len(start_position))
    return exp_soc, exp_makespan

def exp4(num_agents, map_name, start_position, target_position):
    csv_file_path = 'edge_encoding.csv'
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        csv_contents = list(csv_reader)
    # Convert the string representation of the list to an actual list
    encoding_string = csv_contents[0][0]  
    encoding = ast.literal_eval(encoding_string)

    exp_soc, exp_makespan, exp_failrate = run_experiment(num_agents=num_agents, env_name=map_name, start_position=start_position, target_position=target_position, rule_order=[0,4,3,1,5,6,2],  encoding_scheme="edge_weight", encoding=encoding)
    print("Best Rule Order & Edge Weight Encoding: Average Sum of costs: ", sum(exp_soc)/len(exp_soc))
    print("Best Rule Order & Edge Weight Encoding: Average Makespan: ", sum(exp_makespan)/len(exp_makespan))
    print("Best Rule Order & Edge Weight Encoding: Average Failrate: ", exp_failrate / len(start_position))
    return exp_soc, exp_makespan

if __name__ == '__main__':
    #---------------------------------------------------------------------------------------------------------------------------------------------#
    # Run this line below for a visualization of the map "random-32-32-20" with 100 agents and rule order [1,2,3,4,5,6] (no graph optimization)
    #run_one_sim(num_agents=100, env_name="random-32-32-20", rule_order=[0,1,2,3,4,5,6], display=True, save_video=False)
    #---------------------------------------------------------------------------------------------------------------------------------------------#
    
    #---------------------------------------------------------------------------------------------------------------------------------------------#
    # Example Experiment for random-32-32-20, running the 25 random benchmark scenarios 10 times each.
    #   4 Runs will be made:
    # Exp1: Only default rule order [1,2,3,4,5,6] (in the code we write [0,1,2,3,4,5,6], but the rule order 0 does nothing so just ignore it when reading the code).
    # Exp2: Only best rule order [4,3,1,5,6,2].
    # Exp3: With best rule order and node vector encoding.
    # Exp4: With best rule order and edge weight encoding.
    # Lastly, comparing all of those with each other using two-sample t-test.
    num_agents = 200
    map_name = "random-32-32-20"
    scenario_type = "-random-"
    # Generate the start and target positions for the agents from the benchmark scenario files
    start_position, target_position = generate_start_and_target_from_scenario(file_path="Scenario/" + map_name + scenario_type, num_agents=num_agents)
    start_position *= 10
    target_position *= 10

    # Start up Dask
    cluster = LocalCluster()
    client = Client(cluster)
    print(f"Link to dask dashboard {client.dashboard_link}")

    exp1_soc, exp1_span = exp1(num_agents=num_agents, map_name=map_name, start_position=start_position, target_position=target_position)
    exp2_soc, exp2_span = exp2(num_agents=num_agents, map_name=map_name, start_position=start_position, target_position=target_position)
    exp3_soc, exp3_span = exp3(num_agents=num_agents, map_name=map_name, start_position=start_position, target_position=target_position)
    exp4_soc, exp4_span = exp4(num_agents=num_agents, map_name=map_name, start_position=start_position, target_position=target_position)

    t_stat_exp1, p_val_exp1 = stats.ttest_ind(exp1_soc, exp2_soc)
    t_stat_exp2, p_val_exp2 = stats.ttest_ind(exp2_soc, exp3_soc)
    t_stat_exp3, p_val_exp3 = stats.ttest_ind(exp2_soc, exp4_soc)

    print("P_value for difference in means between default rule order and best rule order: ", p_val_exp1)
    print("P_value for difference in means between best rule order and best rule order & node vector encoding: ", p_val_exp2)
    print("P_value for difference in means between best rule order and best rule order & edge weight encoding: ", p_val_exp3)
    #---------------------------------------------------------------------------------------------------------------------------------------------#
