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
from generate_start_and_target import load_position_list_from_nplist

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

def run_experiment(times, rule_order):
    startpos = load_position_list_from_nplist("start_chosen32_32_20")
    targetpos = load_position_list_from_nplist("target_chosen32_32_20")
    sumcost = 0
    list_of_cost = []
    list_of_makespan = []
    for i in range(times):
        cost, makespan = delayed(agents200_random_32_32_20, nout=2)(rule_order, [startpos[i], targetpos[i]])
        #res = delayed(agents200_random_32_32_20)(rule_order)
        #cost = res[0]
        #makespan = res[1]
        #cost = agents400_random_64_64_20()
        #cost = agents400_empty_48_48()
        #print("i: ", i, ", sum_of_costs: ", cost)
        list_of_cost.append(cost)
        list_of_makespan.append(makespan)
        #sumcost += cost
    #sumcost = delayed(sum)(list_of_cost)
    #summakespan = delayed(sum)(list_of_makespan)
    #sumcost.visualize()
    #results_sumofcosts = sumcost.compute() / times
    #results_makespan = summakespan.compute() / times
    #return results_sumofcosts, results_makespan
    res = compute(*list_of_cost, *list_of_makespan)
    return res[:times], res[times:]

def main():
    cluster = LocalCluster()
    client = Client(cluster)
    print(f"Link to dask dashboard {client.dashboard_link}")

    # Write in a terminal. dask scheduler
    # Write in another terminal: dask worker <ip from scheduler (connect worker at.. that ip)>
    # Connect another pc using the same as previous step, the reason we also need a worker on the main pc is so that it is also a worker!
    #client = Client("10.126.85.122:8786")

    perms = list(itertools.permutations([1,2,3,4,5,6]))
    list_of_permutations = []

    for p in perms:
        tmp_list = list(p)
        tmp_list.insert(0, 0)
        list_of_permutations.append(tmp_list)

    #averages_costs = []
    #averages_makespan = []
    for perm in tqdm(list_of_permutations, desc="Processing"):
        average, makespan = run_experiment(100, perm)
        #averages_costs.append(average)
        #averages_makespan.append(makespan)
        write_to_csv(perm, average, makespan, filename="Logs/permtestcsv.csv")

if __name__ == "__main__":
    main()