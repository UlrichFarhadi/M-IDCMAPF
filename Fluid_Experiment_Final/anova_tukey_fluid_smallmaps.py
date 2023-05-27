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

def environment_func(rule_order, chromosome, start_position, target_position, env, amount_of_agents = 10, agent_type=IDCMAPF_agent,  delay=0.0001, fig_size_factor=20, node_size=10, linewidth=0.5, dpi=40 , display=False, max_timestep=1000):
    # Create the map object
    map = Map_directed()
    map.generate_map(env)
    if len(chromosome) != 0:
        map.update_weight_on_map_by_directional(chromosome)

    swarm = Swarm_IDCMAPF(map, amount_of_agents = amount_of_agents, agent_type=agent_type, rule_order=rule_order)
    renderer = Renderer(map, delay=delay, fig_size_factor=fig_size_factor, node_size=node_size, linewidth=linewidth, dpi=dpi)
    simulator = Simulator(map, swarm, renderer, display=display, max_timestep=max_timestep, positions_for_agents=[start_position, target_position])
    return simulator.main_loop()

def run_experiment(times, rule_order, chromosome, startpos, targetpos, environment, agents_amt):
    list_of_cost = []
    list_of_makespan = []
    for i in range(times):
        cost, makespan = delayed(environment_func, nout=2)(rule_order=rule_order, chromosome=chromosome, start_position=startpos[i], target_position=targetpos[i], env=environment, amount_of_agents=agents_amt)
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

    for num_agents in [10]:
        #num_agents = 600
        num_experiments = 1000
        env_name_direct = "random-10-10-20"
        env = "Environments/" + env_name_direct + ".map"
        chromosome = [0, 1, 0.20858629236968843, 0.2953559229050575, 1, 0.09294548574640385, 0.3727735589188432, 0.13422240359355012, 0.8675533183065418, 0, 0.01881147921661433, 0.5717962579561789, 0.884558656101917, 0.2986187279936342, 0.4757268310553563, 0.7199065835333611, 0.1863690213671555, 0.6034651210203894, 0.9655515829579556, 0.6179200072298042, 0.6935230643522289, 0.3746269540680755, 0.5492267164014059, 0.8684861706735006, 0.370891669170245, 0.9146671066098264, 0.7917250649201173, 0.002896241853184045, 0.921872902910907, 0.9899901572080542, 0.08076809941413038, 1, 0.3322844105561251, 0.17488766635458877, 0, 0, 0.3526662715857882, 0.6139509132614216, 0.52202299932882, 0.10392910288296028, 0.8872677617291005, 0.38502157508342433, 0.7661660163596571, 0.5010847731058649, 0.70554216093529, 0.3452713837091571, 0.3830451109835305, 0.43735440652885166, 0.20068827831166236, 0.7214124683136047, 0, 0.2978712418904964, 0.5180738197732649, 1, 0.9016656674849334, 0.5543038530754214, 0.1525412139103846, 0.27329114056590265, 0.2448223823020873, 0.662670895746684, 0.2273542714585423, 0.9234021129571837, 1, 0.46549735290022504, 0.08842781876478267, 0.5836448999132816, 0.09506316021162817, 1, 1, 0, 0.810012992490251, 0.47837312862064346, 0.056190578164265176, 0.6718851004202423, 0.8506516896260206, 0.1113063661425396, 0.49344206990553385, 0.6148010370484442, 0.7639939083865129, 0.20176006240821936, 0, 0.772642614211412, 0, 0.6352300232137903, 0.7248890602399948, 0.7698731938992228, 0.5611327730496142, 1, 0.7007971593796295, 0.4842785694908618, 0.6894969650677969, 0.2243347659183882, 1, 0.493215713017117, 0, 0.5682526734374631, 0.36113831360272514, 0.6943141007540535, 0.2551643965697029, 0.5367785298457521, 0.4567162217078202, 0.3587844449864061, 1, 0, 0.6311371767515723, 0.717197086274004, 0.275158839694308, 0.6701442695066185, 0, 0, 0.9944385264760065, 0.5330732544376535, 0.16808429878680758, 0.5106444684204351, 0.5252398483678171, 0.6809716808580972, 0.5727442792705009, 0.7704376790326608, 0.7888224630916101, 0.6561652575548281, 0.9561017151751733, 0.48086255800427136, 0.1228102079754882, 0.567281324239115, 0.5644392405855181, 0.7035262485136213, 0.3198380222386528, 0.382971832130935, 0.40046576057164596, 0.027369631100290504, 0.682059171332318, 0.5401788033161031, 0.514555460425725, 0.16383351609907504, 0.3650123561347311, 0.7918205049464445, 0.804531830978605, 0.42449926656922476, 0.4256719372116739, 0.2709024763875713, 0.3125896794300896, 0.15190033806908682, 0.46100921147520046, 0.8677046017532596, 0.8986173028874006, 0.3662412490922879, 0.7813072107705615, 0.8659396000821646, 0.3763810842800106, 0.4136838952695237, 0.21447675244134157, 0.16684863219301482, 0.2721246762583853, 1, 0.6472745195612147, 0, 0.43984046617879796, 0.9457791016540884, 0.059796347243469494, 0.7190586179218147, 0.6453484727844887, 0.4316202634925298]

        best_rule_perm = [0,1,2,3,4,5,6]
        
        startpos = load_position_list_from_nplist("Rule_Perm_Experiment_Final/start_and_target_positions_for_experiments/" + env_name_direct + "_" + str(num_agents) + "_agents_start")
        targetpos = load_position_list_from_nplist("Rule_Perm_Experiment_Final/start_and_target_positions_for_experiments/" + env_name_direct + "_" + str(num_agents) + "_agents_target")
        print("Running First Experiment...")
        best_cost, best_span, best_failrate = run_experiment(times=num_experiments, rule_order=best_rule_perm, chromosome=chromosome, startpos=startpos, targetpos=targetpos, environment=env, agents_amt=num_agents)
        print("Running Second Experiment...")
        default_cost, default_span, default_failrate = run_experiment(times=num_experiments, rule_order=best_rule_perm, chromosome=[], startpos=startpos, targetpos=targetpos, environment=env, agents_amt=num_agents)

        print("best_cost_rule: ", best_rule_perm)
        print("cost of best rule order: ", sum(best_cost)/len(best_cost))
        print("span of best rule order: ", sum(best_span)/len(best_span))
        print("failrate of best rule order: ", best_failrate / num_experiments)
        print("cost of default rule order: ", sum(default_cost)/len(default_cost))
        print("span of default rule order: ", sum(default_span)/len(default_span))
        print("failrate of default rule order: ", default_failrate / num_experiments)

        # Conduct the one-way ANOVA
        print(f"Anova test for sum of costs for {env} map with {num_agents} agents")
        f_value, p_value = stats.f_oneway(best_cost, default_cost)
        print(f"f_value {f_value} and p_value {p_value}")

        # Conduct the one-way ANOVA
        print(f"Anova test for makespan for {env} map with {num_agents} agents")
        f_value, p_value = stats.f_oneway(best_span, default_span)
        print(f"f_value {f_value} and p_value {p_value}")

        print("Tukey HSD test on cost")
        print("0 is best_rule, 1 is default_rule")
        res = stats.tukey_hsd(best_cost, default_cost)
        print(res)

        print("Tukey HSD test on span")
        res = stats.tukey_hsd(best_span, default_span)
        print(res)

    

if __name__ == "__main__":
    main()





