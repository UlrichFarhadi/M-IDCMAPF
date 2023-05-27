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
from generate_start_and_target import generate_start_and_target_to_numpy, load_position_list_from_nplist


#generate_start_and_target_to_numpy(100, 400 , env="../Environments/empty-48-48.map", save_start_path="start_empty-48-48", save_target_path="target_empty-48-48")


# def write_to_csv(rule_order, sum_of_costs, makespan, filename='output.csv', append=True):
#     # If append is True, open the CSV file in append mode
#     mode = 'a' if append else 'w'
    
#     # Open the CSV file in the specified mode
#     with open(filename, mode, newline='') as file:
#         writer = csv.writer(file)
        
#         # If append is False, write the header row
#         if not append:
#             writer.writerow(['rule_order', 'sum_of_costs', 'makespan'])
        
#         # Loop through the elements of the two lists
#         for i in range(len(sum_of_costs)):
#             # Get the corresponding elements from the lists
#             element1 = sum_of_costs[i]
#             element2 = makespan[i]
            
#             # Append the experiment list (as a string) to the CSV file
#             writer.writerow([str(rule_order), element1, element2])

# def run_experiment(times, rule_order):
#     startpos = load_position_list_from_nplist("start_empty-48-48")
#     targetpos = load_position_list_from_nplist("target_empty-48-48")
#     sumcost = 0
#     list_of_cost = []
#     list_of_makespan = []
#     for i in range(times):
#         cost, makespan = delayed(agents400_empty_48_48, nout=2)(rule_order, [startpos[i], targetpos[i]])
#         list_of_cost.append(cost)
#         list_of_makespan.append(makespan)
#     res = compute(*list_of_cost, *list_of_makespan)
#     return res[:times], res[times:]

# def main():
#     cluster = LocalCluster()
#     client = Client(cluster)
#     print(f"Link to dask dashboard {client.dashboard_link}")

#     # Write in a terminal. dask scheduler
#     # Write in another terminal: dask worker <ip from scheduler (connect worker at.. that ip)>
#     # Connect another pc using the same as previous step, the reason we also need a worker on the main pc is so that it is also a worker!
#     #client = Client("10.126.85.122:8786")


#     #averages_costs = []
#     #averages_makespan = []
#     list_of_permutations = [[0,5,4,3,1,2,6],[0,5,6,4,3,2,1],[0,1,2,3,4,5,6]]

#     for perm in tqdm(list_of_permutations, desc="Processing"):
#         average, makespan = run_experiment(100, perm)
#         write_to_csv(perm, average, makespan, filename="random400_100runs_48_48_20.csv")

# if __name__ == "__main__":
#     main()



def read_my_file(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            row[0] = ast.literal_eval(row[0])
            data.append(row)
        return data
    
filename = "random400_100runs_48_48_20.csv"
data = read_my_file(filename)

cost_averages = []
span_averages = []
rule_perm = []

for n in range(3):
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


min_cost_idx = 0
min_span_idx = 0
max_cost_idx = 1
max_span_idx = 1


#min_cost_idx = cost_averages.index(min(cost_averages))
print("best_cost: ", cost_averages[min_cost_idx])
print("makespan of best_cost_rule: ", span_averages[min_cost_idx])
print("best_cost_rule: ", rule_perm[min_cost_idx])
#min_span_idx = span_averages.index(min(span_averages))
print("best_span: ", span_averages[min_span_idx])
print("sum_of_costs of best_span_rule: ", cost_averages[min_span_idx])
print("best_span_rule: ", rule_perm[min_span_idx])

#max_cost_idx = cost_averages.index(max(cost_averages))
print("worst_cost: ", cost_averages[max_cost_idx])
print("worst_cost_rule: ", rule_perm[max_cost_idx])
#max_span_idx = span_averages.index(max(span_averages))
print("worst_span: ", span_averages[max_span_idx])
print("worst_span_rule: ", rule_perm[max_span_idx])

print("default_rule: ", rule_perm[2])
print("default_cost: ", cost_averages[2])
print("default_span: ", span_averages[2])

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
for i in range(200, 300):
    if int(data[i][2]) != 1000:
        default_cost_list.append(int(data[i][1]))
        default_span_list.append(int(data[i][2]))



# Conduct the one-way ANOVA
print("Anova test for sum of costs for empty 48-48 map with 400 agents")
f_value, p_value = stats.f_oneway(best_cost_list, worst_cost_list, default_cost_list)
print(f"f_value {f_value} and p_value {p_value}")

# Conduct the one-way ANOVA
print("Anova test for makespan for empty 48-48 map with 400 agents")
f_value, p_value = stats.f_oneway(best_span_list, worst_span_list, default_span_list)
print(f"f_value {f_value} and p_value {p_value}")


print("Tukey HSD test on cost")
print("0 is best_rule, 1 is worst_rule, 2 is default_rule")
res = stats.tukey_hsd(best_cost_list, worst_cost_list, default_cost_list)
print(res)


print("Tukey HSD test on span")
res = stats.tukey_hsd(best_span_list, worst_span_list, default_span_list)
print(res)