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
from GA.GA_Fluid import GA_Fluid

from generate_start_and_target import generate_start_and_target_to_numpy, load_position_list_from_nplist, generate_start_and_target_to_list

#test_intersection() # Duplicate found: (15, 11) x3
#test_follower()
#bug_hunting()
#big_intersection_conflict()
#generate_start_and_target_to_numpy()
# Raouf1()
# Raouf2()
# Raouf3()
# cost, span = agents200_random_32_32_20()
# print(cost)
# print(span)
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


# cost, span = agents400_empty_48_48(rule_order=[0,5,4,3,1,2,6])
# print(cost)
# print(span)
# sum_cost = 0
# sum_span = 0
# for i in tqdm(range(20)):
#     cost, span = agents200_random_32_32_20(rule_order=[0,5,4,3,1,2,6]) #[0,5,4,3,1,2,6]
#     sum_cost += cost
#     sum_span += span
# print(sum_cost/20)
# print(sum_span/20)

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


#agents8_fluid_testmap_INTERPOLATION(fluid=True)
# num = 200
# cost_sum = 0
# span_sum = 0
# for i in tqdm(range(num)):
#     cost, span = agents8_fluid_testmap_INTERPOLATION(fluid=False)
#     cost_sum += cost
#     span_sum += span
# print("Fluid is False")
# print(cost_sum/num)
# print(span_sum/num)


# def map_master_tester():
#     map_name = "random-32-32-20"
#     num_experiments = 250
#     num_agents = 30
#     rule_order = [0, 4, 3, 1, 5, 6, 2]
#     cluster = LocalCluster()
#     client = Client(cluster)
#     print(f"Link to dask dashboard {client.dashboard_link}")
#     #startpos, targetpos = generate_start_and_target_to_list(number_of_experiments=num_experiments, number_of_agents=num_agents, env="Environments/" + map_name + ".map")

#     cost_sum = []
#     span_sum = []
#     for i in tqdm(range(num_experiments)):
#         cost, span = delayed(maptester, nout=2)(num_agents, map_name, rule_order=rule_order, display=False, positions_for_agents=[startpos[i], targetpos[i]])
#         cost_sum.append(cost)
#         span_sum.append(span)
#     print("Fluid is False")
#     res = compute(*cost_sum, *span_sum)
#     print(sum(res[:num_experiments])/num_experiments) 
#     print(sum(res[num_experiments:])/num_experiments) 
    # chromosome = [0, 0.0021291609569782932, 0.4525921240002988, 0.7452301512288018, 0.002049857531222227, 0.027483986121584966, 1, 0.1346123548583485, 0.3159740211393973, 1, 0.6633735670760863, 0.5981982522966807, 0.40504055538951367, 0.4275702619285463, 0, 0.5260081245382606, 0.6518163192175468, 0.17010696052823088, 0.22688957049679162, 0.7344442715842078, 0.5753381716278295, 0.8270110957034169, 0.06234147970492719, 0.924079025786471, 0, 0.42105248803044526, 0, 1, 0.2183906313154356, 0.3535556037891211, 0.37028170887909995, 0, 0.5091998921266158, 0.40216379457601137, 0.43641663881901965, 0.8727744058045236, 0, 0.897788267501762, 0.0579579831466569, 0.2604343981113656, 0.01765655520933543, 1, 0.08310217859073815, 0.04752409876864948, 0.6307495663159337, 0.5181155895247396, 1, 0.18950674386108785, 0.9965635857139461, 0.25308671801502325, 0.38324870753791984, 0.47832854222289817, 0.9187881171407423, 0.551745889575347, 0.788274074102972, 0.46517652228702655, 0.8620124639660047, 0.1666917953246656, 0.9478828908382914, 0.10760913597589548, 0.17195205221326915, 0.04487642581922227, 0.3437933429379782, 0.8425428204996743, 0.7194894138272145, 0.946991490936333, 0.16090658493666005, 0.8734855386521889, 0.9041348945229959, 0.38399133779243255, 0.44323090942329174, 0.7225160687380374, 0.2566538885389381, 0.17969986650120584, 0.6989378155732777, 0.5724332169964962, 0.04079372595705, 0.7839765677008772, 0.961363120083127, 0.909275687131137, 0.8114616476112259, 0.6374041803044768, 0.8870033899861024, 0.9805551780747658, 0.27903174773916883, 0.21056301870771155, 0.6257412882693606, 0.5170723185617411, 0.5633136840536551, 0.5291401220117302, 0.358477407747799, 0.3185535158944859, 0.5593250691901637, 0.18526008514396264, 0.6771572536894125, 0.7079701986909813, 0.511724883333846, 0.5707408678332901, 0.18580798236687557, 0.22949554195064958, 0.4354930119168392, 1, 0.3940986339813318, 0.8929269401970185, 0.9103310139145047, 0.5806788100452642, 0.8376710031622765, 0.21312294438616347, 0.5260081041990847, 0.2865549565522046, 0.48409833767023125, 0.3166345484234914, 0.08902689307498993, 0.6490554910978593, 0.6252539215792164, 0, 0.597203825744128, 0.872261008194276, 0.25961348929588157, 0.6344271511901405, 0.07149909034940763, 0.3906706598438602, 0.5673212871392386, 0.13963645916905001, 0.6037671761108416, 0.417277206355912, 0.5848003546369209, 0.3142156133644055, 0.8063444162184044, 0.8550393163886085, 0.32409529185882535, 0, 0.7418920220126328, 0.6265699742480264, 0.26780380914604196, 0, 0.46791025804512154, 0.16130227321278978, 0.08187391130015978, 0.5570730859711819, 0.5067615192831707, 0, 1, 0.6423190492631244, 0.07227164364177893, 0.7067673926599944, 0.2839610212037787, 0.2577645546976059, 0.2306793934661633, 0.7760971968775356, 0.8194125831434806, 0.8658597840491474, 1, 1, 0.8619716967046158, 0.015792579999642176, 0.6995505783054408, 0.2842567351912412, 0.19182397285908315, 0.044200638169011944, 0.21929184724086173, 0.3243419970989516]
    # cost_sum = []
    # span_sum = []
    # for i in tqdm(range(num_experiments)):
    #     cost, span = delayed(maptester, nout=2)(num_agents, map_name, rule_order=rule_order, fluid=chromosome, display=False, directional=True, positions_for_agents=[startpos[i], targetpos[i]])
    #     cost_sum.append(cost)
    #     span_sum.append(span)
    # print("Fluid is True")
    # res = compute(*cost_sum, *span_sum)
    # print(sum(res[:num_experiments])/num_experiments) 
    # print(sum(res[num_experiments:])/num_experiments) 

# chromosome = [0.5737796822346665, 0.659800828868073, 0.08169945451225598, 0, 0.9566292503863503, 0.54549314880652, 0.8534176717041131, 0.8767127817625391, 0.5771900717758893, 0.7282936139834347, 0.8873213428154842, 0.8349043583296806, 0.7325727943583598, 0.7139101921926795, 0.9365483586899711, 0.306111345103949, 0, 1, 0.17439263565061022, 0, 0.2984811429222468, 0.7189089779864524, 0.817581325713724, 0.46000174491123325, 0.8687261066292203, 0, 0.5734548973209763, 0.4406063414174325, 0.15628975778425025, 0.7089376939131509, 0.238585950497646, 0.9459237762090182, 0.8734846479354832, 1, 0.3728930138314767, 0.1766313537383134, 0.2954434391041638, 0.493822810499969, 0, 0, 0.48415338755074044, 0.04034408010025158, 0.22456189405265004, 0.3722281851345162, 1, 0.3924264422016448, 0.3509120571094245, 0.3076203408391949, 0.916163429490526, 0.3543381800467574, 0.552011816668036, 0.22325535053162454, 0.32286730440468825, 0, 0.2647026871598468, 0.6383006547024365, 0.05383022209201814, 0.4504505752116738, 0.2627992884709593, 0.25693677309991886, 0.3179325586195364, 0.19071916128002658, 0, 0.24110358972278606, 0.42267086682003396, 0.48159118357640773, 0, 0.47584056736458064, 0.8659924743662799, 0.56606826705885, 0.5331488819766236, 0.3488850258968622, 0.6500026732511538, 0.017516048760321156, 0.424273215331708]
# cost, span = maptester(num_agents=4, fluid=chromosome, env_name="fluid_test_smallscale", display=True, directional=True)
# print(cost)
# print(span)

#cost, span = agents8_fluid_testmap(start_target_positions=[[(1,5), (1,4), (1,2), (1,1), (18,1), (18,2), (18,4), (18,5)], [(18,1), (18,2), (18,4), (18,5), (1,5), (1,4), (1,2), (1,1)]])
#agents200_random_32_32_20(fluid=False, display=True)
# num = 50
# cost_sum = 0
# span_sum = 0
# for i in tqdm(range(num)):
#     cost, span = agents200_random_32_32_20(fluid=False)
#     cost_sum += cost
#     span_sum += span
# print("Fluid is False")
# print(cost_sum/num)
# print(span_sum/num)

# num = 50
# cost_sum = 0
# span_sum = 0
# for i in tqdm(range(num)):
#     cost, span = agents200_random_32_32_20(fluid=True)
#     cost_sum += cost
#     span_sum += span
# print("Fluid is True")
# print(cost_sum/num) 
# print(span_sum/num)

#profile_func(agents900_warehouse_20_40_10_2_2)
#cost, span = agents900_warehouse_20_40_10_2_2()
# def main(agi, map_name, rul_ord):
#     # ga_obj = GA_Fluid(environment_function=universal_fitness_function_with_directed_map,
#     #                     env="Environments/fluid_test_smallscale.map",
#     #                     start_positions=[(1,5), (1,4), (1,2), (1,1), (18,1), (18,2), (18,4), (18,5)],
#     #                     target_positions=[(18,1), (18,2), (18,4), (18,5), (1,5), (1,4), (1,2), (1,1)],
#     #                     num_best_solutions_to_save = 3,
#     #                     population_size = 30,
#     #                     mutation_rate = 0.1,
#     #                     elitism = 3,
#     #                     max_num_generations = 5000,
#     #                     amount_of_agents = 8,
#     #                     mutation_rate_swap = 0.00,
#     #                     mutation_rate_point = 0.05,
#     #                     agent_type = IDCMAPF_agent,
#     #                     delay = 0.0001,
#     #                     fig_size_factor = 20,
#     #                     node_size = 10,
#     #                     linewidth = 0.5,
#     #                     dpi = 40,
#     #                     display = False,
#     #                     max_timestep = 1000)
#     # ga_obj = GA_Fluid(environment_function=universal_fitness_function_with_directed_map,
#     #                     env="Environments/empty-48-48.map",
#     #                     start_positions=[],
#     #                     target_positions=[],
#     #                     num_best_solutions_to_save = 3,
#     #                     population_size = 30,
#     #                     mutation_rate = 0.1,
#     #                     elitism = 3,
#     #                     max_num_generations = 5000,
#     #                     amount_of_agents = 400,
#     #                     mutation_rate_swap = 0.00,
#     #                     mutation_rate_point = 0.05,
#     #                     agent_type = IDCMAPF_agent,
#     #                     delay = 0.0001,
#     #                     fig_size_factor = 20,
#     #                     node_size = 10,
#     #                     linewidth = 0.5,
#     #                     dpi = 40,
#     #                     display = False,
#     #                     max_timestep = 1000)
#     #startpos, targetpos = generate_start_and_target_to_list(number_of_experiments=1, number_of_agents=30, env="Environments/" + "random-10-10-20" + ".map")
#     ga_obj = GA_Fluid(environment_function=universal_fitness_function_with_directed_map,
#                         env="Environments/" + map_name + ".map",
#                         #start_positions=startpos[0],
#                         #target_positions=targetpos[0],
#                         start_positions=[],
#                         target_positions=[],
#                         num_best_solutions_to_save = 3,
#                         population_size = 40,
#                         mutation_rate = 0.1,
#                         elitism = 3,
#                         max_num_generations = 101,
#                         amount_of_agents = agi,
#                         rule_order=rul_ord,
#                         mutation_rate_swap = 0.00,
#                         mutation_rate_point = 0.10,
#                         inter = False,
#                         inter_anchorpoints_height = 8,
#                         inter_anchorpoints_width = 8,
#                         agent_type = IDCMAPF_agent,
#                         delay = 0.0001,
#                         fig_size_factor = 20,
#                         node_size = 10,
#                         linewidth = 0.5,
#                         dpi = 400,
#                         display = False,
#                         max_timestep = 1000,
#                         save_trainings_animation=False)
#     ga_obj.fitness_exponent = 9
#     ga_obj.num_env_repetitions = 10
# #     ga_obj = GA_Fluid(environment_function=universal_fitness_function_with_directed_map_interpolation,
# #                         env="Environments/fluid_test_smallscale.map",
# #                         start_positions=[(1,5), (1,4), (1,2), (1,1), (18,1), (18,2), (18,4), (18,5)],
# #                         target_positions=[(18,1), (18,2), (18,4), (18,5), (1,5), (1,4), (1,2), (1,1)],
# #                         num_best_solutions_to_save = 3,
# #                         population_size = 30,
# #                         mutation_rate = 0.1,
# #                         elitism = 3,
# #                         max_num_generations = 5000,
# #                         amount_of_agents = 8,
# #                         mutation_rate_swap = 0.00,
# #                         mutation_rate_point = 0.05,
# #                         inter = True,
# #                         inter_anchorpoints_height = 7,
# #                         inter_anchorpoints_width = 20,
# #                         agent_type = IDCMAPF_agent,
# #                         delay = 0.0001,
# #                         fig_size_factor = 20,
# #                         node_size = 10,
# #                         linewidth = 0.5,
# #                         dpi = 40,
# #                         display = False,
# #                         max_timestep = 1000)
    
#     ga_obj.run()
#     #ga_obj.create_animation(filename="vec_and_mag_test(good).mp4", fps=5)

# if __name__ == '__main__':
    #map_master_tester()

    # cluster = LocalCluster()
    # client = Client(cluster)
    # print(f"Link to dask dashboard {client.dashboard_link}")
    
    # # main(60, "empty-10-10", [0,1,2,3,4,5,6])
    # # main(20, "empty-10-10", [0,1,2,3,4,5,6])
    # # main(40, "empty-10-10", [0,1,2,3,4,5,6])
    
    # # main(100, "random-32-32-20", [0,1,2,3,4,5,6])
    # main(150, "random-32-32-20", [0, 4, 1, 2, 5, 3, 6])
    # main(200, "random-32-32-20", [0, 4, 3, 1, 5, 6, 2])