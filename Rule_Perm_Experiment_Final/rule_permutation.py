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
from dask import compute
import time
from tqdm import tqdm
import csv

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
from generate_start_and_target import generate_start_and_target_to_list

import csv

def write_to_csv(rule_order, sum_of_costs, makespan, filename='output.csv', append=True):
    # If append is True, open the CSV file in append mode
    mode = 'a' if append else 'w'
    
    # Open the CSV file in the specified mode
    with open(filename, mode, newline='') as file:
        writer = csv.writer(file)
        
        # If append is False, write the header row
        if not append:
            writer.writerow(['rule_order', 'sum_of_costs', 'makespan'])
        
        # Loop through the elements of the two lists
        for i in range(len(sum_of_costs)):
            # Get the corresponding elements from the lists
            element1 = sum_of_costs[i]
            element2 = makespan[i]
            
            # Append the experiment list (as a string) to the CSV file
            writer.writerow([str(rule_order), element1, element2])

def environment_func(rule_order, start_position, target_position, env, amount_of_agents = 10, agent_type=IDCMAPF_agent,  delay=0.0001, fig_size_factor=20, node_size=10, linewidth=0.5, dpi=40 , display=False, max_timestep=1000):
    # Create the map object
    map = Map()
    map.generate_map(env)
    swarm = Swarm_IDCMAPF(map, amount_of_agents = amount_of_agents, agent_type=agent_type, rule_order=rule_order)
    renderer = Renderer(map, delay=delay, fig_size_factor=fig_size_factor, node_size=node_size, linewidth=linewidth, dpi=dpi)
    simulator = Simulator(map, swarm, renderer, display=display, max_timestep=max_timestep, positions_for_agents=[start_position, target_position])
    return simulator.main_loop()


def run_experiment(times, rule_order, startpos, targetpos, environment, agents_amt):
    list_of_cost = []
    list_of_makespan = []
    for i in range(times):
        cost, makespan = delayed(environment_func, nout=2)(rule_order=rule_order, start_position=startpos[i], target_position=targetpos[i], env=environment, amount_of_agents=agents_amt)
        list_of_cost.append(cost)
        list_of_makespan.append(makespan)
    res = compute(*list_of_cost, *list_of_makespan)
    return res[:times], res[times:]

def main():
    env_name = "Environments/random-32-32-20.map"
    
    #print(os.system("dir"))
    num_agents = 100
    num_experiments = 100

    cluster = LocalCluster()
    client = Client(cluster)
    print(f"Link to dask dashboard {client.dashboard_link}")

    perms = list(itertools.permutations([1,2,3,4,5,6]))
    list_of_permutations = []

    for p in perms:
        tmp_list = list(p)
        tmp_list.insert(0, 0)
        list_of_permutations.append(tmp_list)
    list_start , list_target = generate_start_and_target_to_list(number_of_experiments=num_experiments, number_of_agents=num_agents, env=env_name)
    for perm in tqdm(list_of_permutations, desc="Processing"):
        average, makespan = run_experiment(num_experiments, perm, list_start, list_target, environment= env_name, agents_amt= num_agents)
        filename_str = "Rule_Perm_Experiment_Final/data/" + "permtestcsv_" + os.path.splitext(os.path.basename(env_name))[0] + "_" + str(num_agents) + "_agents" + ".csv"
        write_to_csv(perm, average, makespan, filename=filename_str)
        
if __name__ == "__main__":
    main()