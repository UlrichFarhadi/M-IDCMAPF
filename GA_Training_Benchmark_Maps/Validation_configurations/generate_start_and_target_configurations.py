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
parent_dir = os.path.abspath(os.path.join(script_dir, '../..'))
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

configurations = 1000

map_name = "random-32-32-20"
num_agents = 200

generate_start_and_target_to_numpy(configurations, num_agents, f"Environments/{map_name}.map", f"GA_Training_Benchmark_Maps/Validation_configurations/{map_name}_{num_agents}_start", f"GA_Training_Benchmark_Maps/Validation_configurations/{map_name}_{num_agents}_target")

map_name = "empty-48-48"
num_agents = 400

generate_start_and_target_to_numpy(configurations, num_agents, f"Environments/{map_name}.map", f"GA_Training_Benchmark_Maps/Validation_configurations/{map_name}_{num_agents}_start", f"GA_Training_Benchmark_Maps/Validation_configurations/{map_name}_{num_agents}_target")

map_name = "random-64-64-20"
num_agents = 400

generate_start_and_target_to_numpy(configurations, num_agents, f"Environments/{map_name}.map", f"GA_Training_Benchmark_Maps/Validation_configurations/{map_name}_{num_agents}_start", f"GA_Training_Benchmark_Maps/Validation_configurations/{map_name}_{num_agents}_target")