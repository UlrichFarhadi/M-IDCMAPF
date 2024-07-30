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
print("Importing Done")

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


if __name__ == '__main__':
    #---------------------------------------------------------------------------------------------------------------------------------------------#
    # Run this line below for a visualization of the given map with "num_agents" amount of agents and rule order defined in "rule_order", with no graph optimization
    # - This is strictly for visualizing the map to see if everything looks right
    soc, makespan = run_one_sim(num_agents=10, env_name="experiment_map", rule_order=[0,1,2,3,4,5,6], display=True, save_video=False)
    print("Sum of Costs: ", soc)
    print("Makespan: ", makespan)
    #---------------------------------------------------------------------------------------------------------------------------------------------#
    