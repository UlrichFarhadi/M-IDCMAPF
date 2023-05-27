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
#from generate_start_and_target import load_lists_from_nplist, generate_start_and_target_to_numpy

#test_intersection() # Duplicate found: (15, 11) x3
#test_follower()
#bug_hunting()
#big_intersection_conflict()
#generate_start_and_target_to_numpy()
# Raouf1()
# Raouf2()
# Raouf3()
#print(agents300_ost003d())
#agents500_warehouse_10_20_10_2_2()
#agents900_warehouse_20_40_10_2_2()


# generate_start_and_target_to_numpy(number_of_experiments= 200)
# start, target = load_lists_from_nplist()

# start_chosen = []
# target_chosen = []

# total_cost = 0
# total_span = 0
# times = len(start)
# for i in tqdm(range(times)):
#     cost, span = agents200_random_32_32_20(start_target_positions=[start[i],target[i]])
#     total_cost += cost
#     total_span += span
#     if span < 500:
#         start_chosen.append(start[i])
#         target_chosen.append(target[i])
#     if len(start_chosen) >= 100:
#         break
# print("Amt of legal pos: ", len(start_chosen), " ", len(target_chosen))

# np.save("Positions_for_environment/start_chosen", start_chosen)
# np.save("Positions_for_environment/target_chosen", target_chosen)

# sum_cost = 0
# for i in tqdm(range(100)):
#     cost, span = agents400_empty_48_48(rule_order=[0,5,4,3,1,2,6])
#     sum_cost += cost
# print(sum_cost/100)



#agents400_random_64_64_20()
#profile_func(agents200_random_32_32_20)
# startpos , targetpos = read_scenario("Scenario/Berlin_1_256-random-1.scen")
# print(startpos)

# ga_obj = GA_Priority_rules(environment_function=universal_fitness_function,
#     env="Environments/random-32-32-20.map",
#     num_best_solutions_to_save=10,
#     population_size=20,
#     mutation_rate=0.1,
#     elitism=3,
#     max_num_generations=500,

#     amount_of_agents = 200,
#     agent_type=IDCMAPF_agent,
#     delay=0.0001,
#     fig_size_factor=20,
#     node_size=10,
#     linewidth=0.5,
#     dpi=40,
#     display=False,
#     max_timestep=1000)
# ga_obj.run()



def read_my_file(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            row[0] = ast.literal_eval(row[0])
            data.append(row)
        return data
    
filename = "../Logs/rule_perm_results.csv"
data = read_my_file(filename)

cost_averages = []
span_averages = []
rule_perm = []

for n in tqdm(range(720)):
    sum_cost = 0
    sum_span = 0
    fails = 0
    for i in range(n*100, (n+1)*100):
        if int(data[i][2]) == 1000:
            fails += 1
        else:
            sum_cost += int(data[i][1])
            sum_span += int(data[i][2])

    rule_perm.append(data[n*100][0])
    cost_averages.append(sum_cost/(100-fails))
    span_averages.append(sum_span/(100-fails))

min_cost_idx = cost_averages.index(min(cost_averages))
print("best_cost: ", cost_averages[min_cost_idx])
print("makespan of best_cost_rule: ", span_averages[min_cost_idx])
print("best_cost_rule: ", rule_perm[min_cost_idx])
min_span_idx = span_averages.index(min(span_averages))
print("best_span: ", span_averages[min_span_idx])
print("sum_of_costs of best_span_rule: ", cost_averages[min_span_idx])
print("best_span_rule: ", rule_perm[min_span_idx])

max_cost_idx = cost_averages.index(max(cost_averages))
print("worst_cost: ", cost_averages[max_cost_idx])
print("worst_cost_rule: ", rule_perm[max_cost_idx])
max_span_idx = span_averages.index(max(span_averages))
print("worst_span: ", span_averages[max_span_idx])
print("worst_span_rule: ", rule_perm[max_span_idx])

print("default_rule: ", rule_perm[0])
print("default_cost: ", cost_averages[0])
print("default_span: ", span_averages[0])

best_cost_list = []
best_span_list = []
for i in range(min_cost_idx*100 , (min_cost_idx+1)*100):
    if int(data[i][2]) != 1000:
        best_cost_list.append(int(data[i][1]))
        best_span_list.append(int(data[i][2]))

worst_cost_list = []
worst_span_list = []
for i in range(max_cost_idx*100 , (max_cost_idx+1)*100):
    if int(data[i][2]) != 1000:
        worst_cost_list.append(int(data[i][1]))
        worst_span_list.append(int(data[i][2]))

default_cost_list = []
default_span_list = []
for i in range(100):
    if int(data[i][2]) != 1000:
        default_cost_list.append(int(data[i][1]))
        default_span_list.append(int(data[i][2]))



# Conduct the one-way ANOVA
print("Anova test for sum of costs for random 32-32-20 map with 200 agents")
f_value, p_value = stats.f_oneway(best_cost_list, worst_cost_list, default_cost_list)
print(f"f_value {f_value} and p_value {p_value}")

# Conduct the one-way ANOVA
print("Anova test for makespan for random 32-32-20 map with 200 agents")
f_value, p_value = stats.f_oneway(best_span_list, worst_span_list, default_span_list)
print(f"f_value {f_value} and p_value {p_value}")


print("Tukey HSD test on cost")
print("0 is best_rule, 1 is worst_rule, 2 is default_rule")
res = stats.tukey_hsd(best_cost_list, worst_cost_list, default_cost_list)
print(res)


print("Tukey HSD test on span")
res = stats.tukey_hsd(best_span_list, worst_span_list, default_span_list)
print(res)