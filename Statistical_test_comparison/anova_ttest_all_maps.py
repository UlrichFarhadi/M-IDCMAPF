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

def environment_func(rule_order, chromosome, start_position, target_position, env, amount_of_agents = 10, agent_type=IDCMAPF_agent,  delay=0.0001, fig_size_factor=20, node_size=10, linewidth=0.5, dpi=40 , display=False, max_timestep=1000, encoding):
    # Create the map object
    map = Map_directed()
    map.generate_map(env)
    if edge_weight_encoding == "edge weight":
        map.update_weight_on_map(chromosome)
    else:
        map.update_weight_on_map_by_directional(chromosome)

    swarm = Swarm_IDCMAPF(map, amount_of_agents = amount_of_agents, agent_type=agent_type, rule_order=rule_order)
    renderer = Renderer(map, delay=delay, fig_size_factor=fig_size_factor, node_size=node_size, linewidth=linewidth, dpi=dpi)
    simulator = Simulator(map, swarm, renderer, display=display, max_timestep=max_timestep, positions_for_agents=[start_position, target_position])
    return simulator.main_loop()

def run_experiment(times, rule_order, chromosome, startpos, targetpos, environment, agents_amt, encoding):
    list_of_cost = []
    list_of_makespan = []
    for i in range(times):
        cost, makespan, _, _ = delayed(environment_func, nout=4)(rule_order=rule_order, chromosome=chromosome, start_position=startpos[i], target_position=targetpos[i], env=environment, amount_of_agents=agents_amt, encoding=encoding)
        list_of_cost.append(cost)
        list_of_makespan.append(makespan)
    res = compute(*list_of_cost, *list_of_makespan)
    failrate = 0
    for span in res[times:]:
        if span == 1000:
            failrate += 1

    return res[:times], res[times:], failrate # returns cost, times

def read_my_file(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            row[0] = ast.literal_eval(row[0])
            data.append(row)
        return data
    
def load_csv_file_with_chromosomes(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

def find_highest_a_with_list(data):
    max_a = float('-inf')
    max_list = None
    for row in data:
        a = float(row[0])
        lst = row[2].strip('[]').split(',')
        if a > max_a:
            max_a = a
            max_list = lst
    return max_list

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

    map_name_csv, num_agents_csv, rule_order_csv, encoding_scheme_csv = 0,1,2,3

    with open("Best_chromosomes/logging_status_edge.csv", 'r') as log_file:
        csv_reader = csv.reader(log_file)
        headline = next(csv_reader)
        for row in csv_reader:
            map_names_list.append(row[map_name_csv])
            num_agents_list.append(int(row[num_agents_csv]))
            rule_orders_list.append(ast.literal_eval(row[rule_order_csv]))
            encoding_scheme_list.append(row[encoding_scheme_csv] == "edge_weight")
            encoding_scheme_names_list.append(row[encoding_scheme_csv])

    with open("Best_chromosomes/logging_status_node.csv", 'r') as log_file:
        csv_reader = csv.reader(log_file)
        headline = next(csv_reader)
        for row in csv_reader:
            map_names_list.append(row[map_name_csv])
            num_agents_list.append(int(row[num_agents_csv]))
            rule_orders_list.append(ast.literal_eval(row[rule_order_csv]))
            encoding_scheme_list.append(row[encoding_scheme_csv] == "edge_weight")
            encoding_scheme_names_list.append(row[encoding_scheme_csv])

    for test in range(len(map_names_list)):


        #num_agents = 600
        if map_names_list[test] == "random-32-32-20":
            num_experiments = 250
        else:
            num_experiments = 1000
        # env_name_direct = "empty-10-10"
        # env = "Environments/" + env_name_direct + ".map"
        # best_rule_perm = [0, 1, 2, 3, 4, 5, 6]
        # encoding_scheme = "edge weight" # node vector
        #chromosome = # LOAD FROM Best_chromosomes folder where we store the best chromosomes for node vector and edge weight

        startpos = load_position_list_from_nplist("start_and_target_positions_for_experiments/" + env_name_direct + "_" + str(num_agents) + "_agents_start")
        targetpos = load_position_list_from_nplist("start_and_target_positions_for_experiments/" + env_name_direct + "_" + str(num_agents) + "_agents_target")
        print("Running First Experiment...")
        best_cost, best_span, best_failrate = run_experiment(times=num_experiments, rule_order=best_rule_perm, chromosome=chromosome, startpos=startpos, targetpos=targetpos, environment=env, agents_amt=num_agents)
        print("Running Second Experiment...")
        default_cost, default_span, default_failrate = run_experiment(times=num_experiments, rule_order=best_rule_perm, chromosome=[], startpos=startpos, targetpos=targetpos, environment=env, agents_amt=num_agents)

        print("rule order used: ", best_rule_perm)
        print("SOC using " + encoding_scheme + " encoding: ", sum(best_cost)/len(best_cost))
        print("makespan using " + encoding_scheme + " encoding: ", sum(best_span)/len(best_span))
        print("failrate using " + encoding_scheme + " encoding: ", best_failrate / num_experiments)
        print("SOC using no encoding: ", sum(default_cost)/len(default_cost))
        print("makespan using no encoding: ", sum(default_span)/len(default_span))
        print("failrate using no encoding: ", default_failrate / num_experiments)

        print("T-test on cost")
        print("0 is best_rule, 1 is default_rule")
        t_statistic, p_value = stats.ttest_ind(best_cost, default_cost)
        print(f"t_statistic {t_statistic} and p_value {p_value}")

        print("T-test on span")
        t_statistic, p_value = stats.ttest_ind(best_span, default_span)
        print(f"t_statistic {t_statistic} and p_value {p_value}")

    

if __name__ == "__main__":
    main()





