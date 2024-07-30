# Library imports
import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
import random
import copy
import cProfile
import pstats
import numpy as np
from typing import List, Tuple, Callable


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
from Simulator.simulator import Simulator

from GA.GA_Rules import GA_Priority_rules

def profile_func(func):
    profiler = cProfile.Profile()
    result = profiler.runcall(func)
    #profiler.print_stats()

    stats = pstats.Stats(profiler)
    total_time = stats.total_tt

    print('\nTotal time: %.2f sec' % total_time)
    print('Sort after total time:')

    stats.strip_dirs().sort_stats('tottime').print_stats()

def universal_fitness_function(chromosome, start_position, target_position, env, amount_of_agents = 10, agent_type=IDCMAPF_agent,  delay=0.0001, fig_size_factor=20, node_size=10, linewidth=0.5, dpi=40 , display=False, max_timestep=1000):
    # Create the map object
    map = Map()
    map.generate_map(env)
    swarm = Swarm_IDCMAPF(map, amount_of_agents = amount_of_agents, agent_type=agent_type, rule_order=chromosome)
    renderer = Renderer(map, delay=delay, fig_size_factor=fig_size_factor, node_size=node_size, linewidth=linewidth, dpi=dpi)
    simulator = Simulator(map, swarm, renderer, display=display, max_timestep=max_timestep, positions_for_agents=[start_position, target_position])
    return simulator.main_loop()

def universal_fitness_function_with_directed_map(chromosome, start_position, target_position, env, amount_of_agents = 10, agent_type=IDCMAPF_agent,  delay=0.0001, fig_size_factor=20, node_size=10, linewidth=0.5, dpi=40 , display=False, max_timestep=1000, rule_order=[0,1,2,3,4,5,6], edge_weight_encoding = True ):
    map = Map_directed()
    map.generate_map(env)
    #map.update_weight_on_map(chromosome)
    if edge_weight_encoding:
        map.update_weight_on_map(chromosome)
    else:
        map.update_weight_on_map_by_directional(chromosome)
    # map.update_weight_on_map_by_directional(list_of_direction=chromosome)
    swarm = Swarm_IDCMAPF(map, amount_of_agents = amount_of_agents, agent_type=agent_type, rule_order=rule_order)
    renderer = Renderer(map, delay=delay, fig_size_factor=fig_size_factor, node_size=node_size, linewidth=linewidth, dpi=dpi)
    simulator = Simulator(map, swarm, renderer, display=display, max_timestep=max_timestep, positions_for_agents=[start_position, target_position])
    soc, span, _, _ = simulator.main_loop()
    return soc, span

def universal_fitness_function_with_directed_map_interpolation(chromosome, start_position, target_position, env, amount_of_agents = 10, agent_type=IDCMAPF_agent,  delay=0.0001, fig_size_factor=20, node_size=10, linewidth=0.5, dpi=40 , display=False, max_timestep=1000):
    map = Map_directed()
    map.generate_map(env)
    map.update_weight_on_map_by_node(chromosome)
    swarm = Swarm_IDCMAPF(map, amount_of_agents = amount_of_agents, agent_type=agent_type, rule_order=[0,5,4,3,1,2,6])
    renderer = Renderer(map, delay=delay, fig_size_factor=fig_size_factor, node_size=node_size, linewidth=linewidth, dpi=dpi)
    simulator = Simulator(map, swarm, renderer, display=display, max_timestep=max_timestep, positions_for_agents=[start_position, target_position])
    return simulator.main_loop()