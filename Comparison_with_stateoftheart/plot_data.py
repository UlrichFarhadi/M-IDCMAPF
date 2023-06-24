import copy
from typing import List
import itertools
import numpy as np
from dask.distributed import Client, LocalCluster
from dask import delayed
import csv
import os
import sys
from statistics import mean

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)



def data(file_name,number_of_agent,env):
    soc_list = []
    solved_list = []
    new_soc_list = []

    with open(file_name, "r") as file:
        next(file)
        lines = csv.reader(file)

        for line in lines:
            #print(line)
            map_name,scen_num,num_agents,solver,solved,soc,lb_soc,makespan,lb_makespan,comp_time = line
            
            if map_name == env and int(num_agents) == number_of_agent:
                if solved == "-1":
                    solved = 0
                solved_list.append(int(solved))
                if soc == "-1":
                    continue
                soc_list.append(int(soc))
                #print(line)
                if soc == "-1" or int(solved) == 0:
                    continue
                new_soc_list.append(int(soc))


    print(f"method: {solver} soc: {mean(soc_list)} and success rate: {mean(solved_list)}")
    print(f"method: {solver} new soc: {mean(new_soc_list)}")

pibt = "Comparison_with_stateoftheart/PIBT.csv"
pibtplus = "Comparison_with_stateoftheart/PIBT_PLUS.csv"
eecbs = "Comparison_with_stateoftheart/EECBS.csv"
cbs = "Comparison_with_stateoftheart/CBS.csv"
dcmapf = "Comparison_with_stateoftheart/DCMAPF.csv"
idcmapf = "Comparison_with_stateoftheart/IDCMAPF.csv"

number_of_agent = 200
env = "random-32-32-20.map"

for number_of_agent in [50,100,150,200]:
    data(pibt,number_of_agent=number_of_agent,env=env)
    data(pibtplus,number_of_agent=number_of_agent,env=env)
#data(eecbs,number_of_agent=number_of_agent,env=env)


# import matplotlib.pyplot as plt

# # Define a line style for the plots
# line_style1 = '-'
# line_style2 = ':'
# line_style3 = '--'
# line_style4 = '-.'

# # Define the marker size
# marker_size = 6

# # Define the marker edge width
# marker_edge_width = 2

# title_size = 15
# legend_size = 12
# label_size = 13

# # Create some sample data
# random_32_32_20_pibt = [1319,3587,6861,12100]
# random_32_32_20_pibt_plus = [1323,3037,5258,8062]
# random_32_32_20_eecbs = [1156,2458,3811,5487]
# random_32_32_20_M_IDCMAPF = [3166,5697,9566]

# random_32_32_20_e_pibt = [0.92,0.56,0.44,0.16]
# random_32_32_20_e_pibt_plus = [1,1,1,1]
# random_32_32_20_e_eecbs = [1,1,1,0.08]
# random_32_32_20_e_M_IDCMAPF = [1-0.0, 1-0.004, 1-0.0]
# r_1_other = [50,100,150,200]
# r_1_our = [100,150,200]


# empty_48_48_pibt = [1681,3548,5607,7796,10081,12567,15232,17874]
# empty_48_48_pibt_plus = [1681,3548,5607,7796,10081,12567,15232,17874]
# empty_48_48_eecbs = [1585,3154,4765,6372,8002,9709,11452,13222]
# empty_48_48_M_IDCMAPF = [6856,16083]

# empty_48_48_e_pibt = [1,1,1,1,1,1,1,1]
# empty_48_48_e_pibt_plus = [1,1,1,1,1,1,1,1]
# empty_48_48_e_eecbs = [1,1,1,1,1,1,1,1]
# empty_48_48_e_M_IDCMAPF = [1-0, 1-0]
# r_2_other = [50,100,150,200,250,300,350,400]
# r_2_our = [200,400]

# random_64_64_20_pibt = [2385,5044,7874,11123,14640,18357,21945,26091]
# random_64_64_20_pibt_plus = [2385,5044,7874,10917,14241,17683,21294,25234]
# random_64_64_20_eecbs = [2251,4532,6825,9195,11663,14189,16844,19714]
# random_64_64_20_M_IDCMAPF = [10482,17679,27858]

# random_64_64_20_e_pibt = [1,1,1,0.8,0.64,0.56,0.48,0.08]
# random_64_64_20_e_pibt_plus = [1,1,1,1,1,1,1,1]
# random_64_64_20_e_eecbs = [1,1,1,1,1,1,1,1]
# random_64_64_20_e_M_IDCMAPF = [1-0, 1-0.008, 1-0.04]
# r_3_other = [50,100,150,200,250,300,350,400]
# r_3_our = [200,300,400]

# ost003d_pibt = [7934,16168,24781,33866,43426,53282]
# ost003d_pibt_plus = [7934,16168,24781,33866,43426,53282]
# ost003d_eecbs = []
# ost003d_M_IDCMAPF = [16351,34420,61843]

# ost003d_e_pibt = [1,1,1,1,1,1]
# ost003d_e_pibt_plus = [1,1,1,1,1,1]
# ost003d_e_eecbs = []
# ost003d_e_M_IDCMAPF = [1-0, 1-0, 1-0.044]
# r_4_other = [50,100,150,200,250,300]
# r_4_our = [100,200,300]




# y_bottom = 0.0
# y_top = 1.01

# maker1 = "o"
# maker2 = "o"
# maker3 = "D"
# maker4 = "D"

# markerfacecolor1 = 'w'
# markerfacecolor2 = 'w'
# markerfacecolor3 = None
# markerfacecolor4 = None

# # Create the first plot
# plt.plot(r_1_other, random_32_32_20_pibt, marker=maker1, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT', color="orange",markerfacecolor=markerfacecolor1)
# plt.plot(r_1_other, random_32_32_20_pibt_plus, marker=maker2, linestyle=line_style2, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT+', color="green",markerfacecolor=markerfacecolor2)
# plt.plot(r_1_other, random_32_32_20_eecbs, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='EECBS', color="blue",markerfacecolor=markerfacecolor3)
# plt.plot(r_1_our, random_32_32_20_M_IDCMAPF, marker=maker4, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='M_IDCMAPF', color="red",markerfacecolor=markerfacecolor4)


# plt.title('Map: random-32-32-20', fontsize=title_size)
# plt.xlabel('Number of robots', fontsize=label_size)
# plt.ylabel('Sum of costs', fontsize=label_size)
# plt.xticks(r_1_other[::])
# #plt.ylim()
# plt.legend(fontsize=legend_size)
# plt.show()

# plt.plot(r_1_other, random_32_32_20_e_pibt, marker=maker1, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT', color="orange",markerfacecolor=markerfacecolor1)
# plt.plot(r_1_other, random_32_32_20_e_pibt_plus, marker=maker2, linestyle=line_style2, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT+', color="green",markerfacecolor=markerfacecolor2)
# plt.plot(r_1_other, random_32_32_20_e_eecbs, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='EECBS', color="blue",markerfacecolor=markerfacecolor3)
# plt.plot(r_1_our, random_32_32_20_e_M_IDCMAPF, marker=maker4, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='M_IDCMAPF', color="red",markerfacecolor=markerfacecolor4)


# plt.title('Map: random-32-32-20', fontsize=title_size)
# plt.xlabel('Number of robots', fontsize=label_size)
# plt.ylabel('Success rate', fontsize=label_size)
# plt.xticks(r_1_other[::])
# plt.ylim((y_bottom, y_top))
# plt.legend(fontsize=legend_size)
# plt.show()

# # # Create the second plot
# plt.plot(r_2_other, empty_48_48_pibt, marker=maker1, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT', color="orange",markerfacecolor=markerfacecolor1)
# plt.plot(r_2_other, empty_48_48_pibt_plus, marker=maker2, linestyle=line_style2, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT+', color="green",markerfacecolor=markerfacecolor2)
# plt.plot(r_2_other, empty_48_48_eecbs, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='EECBS', color="blue",markerfacecolor=markerfacecolor3)
# plt.plot(r_2_our, empty_48_48_M_IDCMAPF, marker=maker4, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='M_IDCMAPF', color="red",markerfacecolor=markerfacecolor4)


# plt.title('Map: empty_48_48', fontsize=title_size)
# plt.xlabel('Number of robots', fontsize=label_size)
# plt.ylabel('Sum of costs', fontsize=label_size)
# plt.xticks(r_2_other[::])
# #plt.ylim()
# plt.legend(fontsize=legend_size)
# plt.show()

# plt.plot(r_2_other, empty_48_48_e_pibt, marker=maker1, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT', color="orange",markerfacecolor=markerfacecolor1)
# plt.plot(r_2_other, empty_48_48_e_pibt_plus, marker=maker2, linestyle=line_style2, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT+', color="green",markerfacecolor=markerfacecolor2)
# plt.plot(r_2_other, empty_48_48_e_eecbs, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='EECBS', color="blue",markerfacecolor=markerfacecolor3)
# plt.plot(r_2_our, empty_48_48_e_M_IDCMAPF, marker=maker4, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='M_IDCMAPF', color="red",markerfacecolor=markerfacecolor4)


# plt.title('Map: empty_48_48', fontsize=title_size)
# plt.xlabel('Number of robots', fontsize=label_size)
# plt.ylabel('Success rate', fontsize=label_size)
# plt.xticks(r_2_other[::])
# plt.ylim((y_bottom, y_top))
# plt.legend(fontsize=legend_size)
# plt.show()

# # # Create the 3 plot
# plt.plot(r_3_other, random_64_64_20_pibt, marker=maker1, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT', color="orange",markerfacecolor=markerfacecolor1)
# plt.plot(r_3_other, random_64_64_20_pibt_plus, marker=maker2, linestyle=line_style2, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT+', color="green",markerfacecolor=markerfacecolor2)
# plt.plot(r_3_other, random_64_64_20_eecbs, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='EECBS', color="blue",markerfacecolor=markerfacecolor3)
# plt.plot(r_3_our, random_64_64_20_M_IDCMAPF, marker=maker4, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='M_IDCMAPF', color="red",markerfacecolor=markerfacecolor4)


# plt.title('Map: random_64_64_20', fontsize=title_size)
# plt.xlabel('Number of robots', fontsize=label_size)
# plt.ylabel('Sum of costs', fontsize=label_size)
# plt.xticks(r_3_other[::])
# #plt.ylim()
# plt.legend(fontsize=legend_size)
# plt.show()

# plt.plot(r_3_other, random_64_64_20_e_pibt, marker=maker1, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT', color="orange",markerfacecolor=markerfacecolor1)
# plt.plot(r_3_other, random_64_64_20_e_pibt_plus, marker=maker2, linestyle=line_style2, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT+', color="green",markerfacecolor=markerfacecolor2)
# plt.plot(r_3_other, random_64_64_20_e_eecbs, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='EECBS', color="blue",markerfacecolor=markerfacecolor3)
# plt.plot(r_3_our, random_64_64_20_e_M_IDCMAPF, marker=maker4, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='M_IDCMAPF', color="red",markerfacecolor=markerfacecolor4)


# plt.title('Map: random_64_64_20', fontsize=title_size)
# plt.xlabel('Number of robots', fontsize=label_size)
# plt.ylabel('Success rate', fontsize=label_size)
# plt.xticks(r_3_other[::])
# plt.ylim((y_bottom, y_top))
# plt.legend(fontsize=legend_size)
# plt.show()


# # # Create the 4 plot
# plt.plot(r_4_other, ost003d_pibt, marker=maker1, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT', color="orange",markerfacecolor=markerfacecolor1)
# plt.plot(r_4_other, ost003d_pibt_plus, marker=maker2, linestyle=line_style2, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT+', color="green",markerfacecolor=markerfacecolor2)
# #plt.plot(r_4_other, ost003d_eecbs, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='EECBS', color="blue",markerfacecolor=markerfacecolor3)
# plt.plot(r_4_our, ost003d_M_IDCMAPF, marker=maker4, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='M_IDCMAPF', color="red",markerfacecolor=markerfacecolor4)


# plt.title('Map: ost003d', fontsize=title_size)
# plt.xlabel('Number of robots', fontsize=label_size)
# plt.ylabel('Sum of costs', fontsize=label_size)
# plt.xticks(r_4_other[::])
# #plt.ylim()
# plt.legend(fontsize=legend_size)
# plt.show()

# plt.plot(r_4_other, ost003d_e_pibt, marker=maker1, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT', color="orange",markerfacecolor=markerfacecolor1)
# plt.plot(r_4_other, ost003d_e_pibt_plus, marker=maker2, linestyle=line_style2, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT+', color="green",markerfacecolor=markerfacecolor2)
# #plt.plot(r_4_other, ost003d_e_eecbs, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='EECBS', color="blue",markerfacecolor=markerfacecolor3)
# plt.plot(r_4_our, ost003d_e_M_IDCMAPF, marker=maker4, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='M_IDCMAPF', color="red",markerfacecolor=markerfacecolor4)


# plt.title('Map: ost003d', fontsize=title_size)
# plt.xlabel('Number of robots', fontsize=label_size)
# plt.ylabel('Success rate', fontsize=label_size)
# plt.xticks(r_4_other[::])
# plt.ylim((y_bottom, y_top))
# plt.legend(fontsize=legend_size)
# plt.show()
