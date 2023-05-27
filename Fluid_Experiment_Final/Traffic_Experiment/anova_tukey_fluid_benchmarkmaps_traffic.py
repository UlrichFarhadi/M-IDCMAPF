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
from generate_start_and_target import generate_start_and_target_to_list, generate_start_and_target_from_scenario

def environment_func(rule_order, chromosome, start_position, target_position, env, amount_of_agents = 10, agent_type=IDCMAPF_agent,  delay=0.0001, fig_size_factor=20, node_size=10, linewidth=0.5, dpi=40 , display=False, max_timestep=1000, traffic_id=-1):
    # Create the map object
    map = Map_directed()
    map.generate_map(env)
    if len(chromosome) != 0:
        map.update_weight_on_map_by_directional(chromosome)

    swarm = Swarm_IDCMAPF(map, amount_of_agents = amount_of_agents, agent_type=agent_type, rule_order=rule_order, traffic_id=traffic_id)
    renderer = Renderer(map, delay=delay, fig_size_factor=fig_size_factor, node_size=node_size, linewidth=linewidth, dpi=dpi)
    simulator = Simulator(map, swarm, renderer, display=display, max_timestep=max_timestep, positions_for_agents=[start_position, target_position])
    return simulator.main_loop()

def run_experiment(times, rule_order, chromosome, startpos, targetpos, environment, agents_amt, traffic_id=-1):
    list_of_cost = []
    list_of_makespan = []
    for i in range(times):
        cost, makespan = delayed(environment_func, nout=2)(rule_order=rule_order, chromosome=chromosome, start_position=startpos[i], target_position=targetpos[i], env=environment, amount_of_agents=agents_amt, traffic_id=(traffic_id + i))
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

def main():
    cluster = LocalCluster()
    client = Client(cluster)
    print(f"Link to dask dashboard {client.dashboard_link}")

    for num_agents in [200]:
        #num_agents = 600
        num_experiments = 25
        # num_repetitions = 25
        #env_name_direct = "empty-10-10"
        env_name_direct = "random-32-32-20"
        env = "Environments/" + env_name_direct + ".map"
        chromosome = []
        # data_filename = "Rule_Perm_Experiment_Final/data/permtestcsv_" + env_name_direct + "_" + str(num_agents) + "_agents.csv"
        
        #best_rule_perm = find_best_rule_perm(filename=data_filename, num_repetitions=num_repetitions)
        # best_rule_perm = [0, 4, 3, 2, 1, 5, 6]
        # #startpos, targetpos = generate_start_and_target_to_list(number_of_experiments=num_experiments , number_of_agents=num_agents, env=env)
        # startpos, targetpos =  generate_start_and_target_from_scenario("Scenario/" + env_name_direct + "-random-", num_agents)
        #best_rule_perm = [0, 4, 3, 1, 5, 6, 2]
        best_rule_perm = [0,1,2,3,4,5,6]
        # startpos, targetpos = generate_start_and_target_to_list(number_of_experiments=num_experiments , number_of_agents=num_agents, env=env)
        startpos, targetpos =  generate_start_and_target_from_scenario("Scenario/" + env_name_direct + "-random-", num_agents)
        best_cost_avg = []
        best_span_avg = []
        default_cost_avg = []
        default_span_avg = []
        best_failrate_avg = 0
        default_failrate_avg = 0
        i = 10

        traffic_id_tmp = 0
        for _ in range(i):
            #best_cost, best_span, best_failrate = run_experiment(times=num_experiments, rule_order=best_rule_perm, chromosome=chromosome, startpos=startpos, targetpos=targetpos, environment=env, agents_amt=num_agents, traffic_id=traffic_id_tmp)
            default_cost, default_span, default_failrate = run_experiment(times=num_experiments, rule_order=best_rule_perm, chromosome=[], startpos=startpos, targetpos=targetpos, environment=env, agents_amt=num_agents, traffic_id=traffic_id_tmp)
            traffic_id_tmp += 1 * num_experiments
            #best_cost_avg.append(best_cost)
            #best_span_avg.append(best_span)
            default_cost_avg.append(default_cost)
            default_span_avg.append(default_span)
            #best_failrate_avg += best_failrate
            default_failrate_avg += default_failrate


        # def flatten(l):
        #     return [item for sublist in l for item in sublist]

        # #best_cost = flatten(best_cost_avg)
        # #best_span = flatten(best_span_avg)
        # default_cost = flatten(default_cost_avg)
        # default_span = flatten(default_span_avg)
        # #best_failrate = best_failrate_avg/i
        # default_failrate = default_failrate_avg/i

        #print("best_cost_rule: ", best_rule_perm)
        #print("cost of best rule order: ", sum(best_cost)/len(best_cost))
        #print("span of best rule order: ", sum(best_span)/len(best_span))
        #print("failrate of best rule order: ", best_failrate / num_experiments)
        # print("cost of default rule order: ", sum(default_cost)/len(default_cost))
        # print("span of default rule order: ", sum(default_span)/len(default_span))
        # print("failrate of default rule order: ", default_failrate / num_experiments)

        # # Conduct the one-way ANOVA
        # print(f"Anova test for sum of costs for {env} map with {num_agents} agents")
        # f_value, p_value = stats.f_oneway(best_cost, default_cost)
        # print(f"f_value {f_value} and p_value {p_value}")

        # # Conduct the one-way ANOVA
        # print(f"Anova test for makespan for {env} map with {num_agents} agents")
        # f_value, p_value = stats.f_oneway(best_span, default_span)
        # print(f"f_value {f_value} and p_value {p_value}")

        # print("Tukey HSD test on cost")
        # print("0 is best_rule, 1 is default_rule")
        # res = stats.tukey_hsd(best_cost, default_cost)
        # print(res)

        # print("Tukey HSD test on span")
        # res = stats.tukey_hsd(best_span, default_span)
        # print(res)

    

if __name__ == "__main__":
    main()





