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
from generate_start_and_target import generate_start_and_target_to_list, generate_start_and_target_from_scenario, load_position_list_from_nplist

def environment_func(rule_order, chromosome, start_position, target_position, env, amount_of_agents = 10, agent_type=IDCMAPF_agent,  delay=0.0001, fig_size_factor=20, node_size=10, linewidth=0.5, dpi=40 , display=False, max_timestep=1000, encoding="edge_weight", traffic_id=-1):
    # Create the map object
    map = Map_directed()
    map.generate_map(env)
    if len(chromosome) == 0:
        pass
    elif encoding == "edge_weight":
        map.update_weight_on_map(chromosome)
    elif encoding == "node_vector":
        map.update_weight_on_map_by_directional(chromosome)

    swarm = Swarm_IDCMAPF(map, amount_of_agents = amount_of_agents, agent_type=agent_type, rule_order=rule_order, traffic_id=traffic_id, folder_path_traffic= "GA_Training_Benchmark_Maps/Traffic")
    renderer = Renderer(map, delay=delay, fig_size_factor=fig_size_factor, node_size=node_size, linewidth=linewidth, dpi=dpi)
    simulator = Simulator(map, swarm, renderer, display=display, max_timestep=max_timestep, positions_for_agents=[start_position, target_position])
    return simulator.main_loop()

def run_experiment(times, rule_order, chromosome, startpos, targetpos, environment, agents_amt, encoding , traffic_id=-1):
    list_of_cost = []
    list_of_makespan = []
    list_of_waits = []
    list_of_conflicts = []
    for i in range(times):
        cost, makespan, waits, conflicts = delayed(environment_func, nout=4)(rule_order=rule_order, chromosome=chromosome, start_position=startpos[i], target_position=targetpos[i], env=environment, amount_of_agents=agents_amt, encoding=encoding, traffic_id=1000*traffic_id+i)
        list_of_cost.append(cost)
        list_of_makespan.append(makespan)
        list_of_waits.append(waits)
        list_of_conflicts.append(conflicts)
    res = compute(*list_of_cost, *list_of_makespan, *list_of_waits, *list_of_conflicts)
    failrate = 0
    for span in res[times:]:
        if span == 1000:
            failrate += 1

    return res[:times], res[times:times*2], failrate, res[times*2:times*3], res[times*3:] # returns cost, span, failrate, waits, conflicts

def read_my_file(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            row[0] = ast.literal_eval(row[0])
            data.append(row)
        return data
    
def load_csv_file_with_chromosomes(filename, map_name, num_agents, encoding_scheme_name, mutation_rate, environment_repetitions, pop_size):
    map_name_csv, num_agents_csv, encoding_scheme_name_csv, mutation_rate_csv, environment_repetitions_csv, pop_size_csv, budget_csv, soc, span, chromosome = 0,1,2,3,4,5,6,7,8,9
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if map_name == row[map_name_csv] and num_agents == int(row[num_agents_csv]) and encoding_scheme_name == row[encoding_scheme_name_csv] and mutation_rate == float(row[mutation_rate_csv]) and environment_repetitions == int(row[environment_repetitions_csv]) and pop_size == int(row[pop_size_csv]):
                data.append(row)
    return data

def find_highest_a_with_list(data):
    max_a = float('inf')
    max_list = None
    for row in data:
        a = float(row[7])
        lst = ast.literal_eval(row[9])
        #lst = row[2].strip('[]').split(',')
        if a < max_a:
            max_a = a
            max_list = lst
    return max_list

def log_to_csv(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

def main():
    cluster = LocalCluster()
    client = Client(cluster)
    print(f"Link to dask dashboard {client.dashboard_link}")

    #map_name,num_agents,rule_order,encoding_scheme,finished_amt
    map_names_list = []
    num_agents_list = []
    rule_orders_list = []
    encoding_scheme_list = []
    encoding_scheme_names_list = []
    mutation_rate_list = []
    environment_repetitions_list = []
    pop_size_list = []

    map_name_csv, num_agents_csv, rule_order_csv, encoding_scheme_csv, mutation_rate_csv, environment_repetitions_csv, pop_size_csv, budget_csv = 0,1,2,3,4,5,6,7

    with open("GA_Training_Benchmark_Maps/cases.csv", 'r') as log_file:
        csv_reader = csv.reader(log_file)
        headline = next(csv_reader)
        for row in csv_reader:
            map_names_list.append(row[map_name_csv])
            num_agents_list.append(int(row[num_agents_csv]))
            rule_orders_list.append(ast.literal_eval(row[rule_order_csv]))
            encoding_scheme_list.append(row[encoding_scheme_csv] == "edge_weight")
            encoding_scheme_names_list.append(row[encoding_scheme_csv])
            mutation_rate_list.append(float(row[mutation_rate_csv]))
            environment_repetitions_list.append(int(row[environment_repetitions_csv]))
            pop_size_list.append(int(row[pop_size_csv]))

    for i in range(len(map_names_list)):
        #num_agents = 600
        # if map_names_list[i] == "random-32-32-20":
        traffic_id=i
        num_experiments = 250
        env = "Environments/" + map_names_list[i] + ".map"
        # best_rule_perm = [0, 1, 2, 3, 4, 5, 6]
        # encoding_scheme = "edge weight" # node vector
        #chromosome = # LOAD FROM Best_chromosomes folder where we store the best chromosomes for node vector and edge weight

        startpos = load_position_list_from_nplist("Statistical_test_comparison/start_and_target_positions_for_experiments/" + map_names_list[i] + "_" + str(num_agents_list[i]) + "_agents_start")
        targetpos = load_position_list_from_nplist("Statistical_test_comparison/start_and_target_positions_for_experiments/" + map_names_list[i] + "_" + str(num_agents_list[i]) + "_agents_target")
        data = load_csv_file_with_chromosomes("GA_Training_Benchmark_Maps/chromosomes.csv", map_names_list[i], num_agents_list[i], encoding_scheme_names_list[i], mutation_rate_list[i], environment_repetitions_list[i], pop_size_list[i])
        chromosome = find_highest_a_with_list(data)
        #print("Running First Experiment...")
        best_cost, best_span, best_failrate, best_waits, best_conflicts = run_experiment(times=num_experiments, rule_order=rule_orders_list[i], chromosome=chromosome, startpos=startpos, targetpos=targetpos, environment=env, agents_amt=num_agents_list[i], encoding=encoding_scheme_names_list[i],traffic_id=traffic_id)
        #print("Running Second Experiment...")
        # default_cost, default_span, default_failrate, default_waits, default_conflicts = run_experiment(times=num_experiments, rule_order=rule_orders_list[i], chromosome=[], startpos=startpos, targetpos=targetpos, environment=env, agents_amt=num_agents_list[i], encoding=encoding_scheme_names_list[i])

if __name__ == "__main__":
    main()




