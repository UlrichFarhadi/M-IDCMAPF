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
import matplotlib.pyplot as plt

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)
# Create an empty list to store the data
data = []

# Open the CSV file
with open("Best_chromosomes/results.csv", 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Append the row to the data list
        data.append(row)

# Define a line style for the plots
line_style1 = '-'
line_style2 = ':'
line_style3 = '--'
line_style4 = '-.'

# Define the marker size
marker_size = 6

# Define the marker edge width
marker_edge_width = 2

title_size = 15
legend_size = 12
label_size = 13

y_bottom = 0.0
y_top = 1.01

maker1 = "o"
maker2 = "o"
maker3 = "D"
maker4 = "D"

markerfacecolor1 = 'w'
markerfacecolor2 = 'w'
markerfacecolor3 = None
markerfacecolor4 = None

map_name, num_agents, encoding_scheme_name, p_value_SOC, p_value_waits, p_value_conflicts, rule_order, best_cost, best_span, best_failrate, best_waits, best_conflicts, default_cost, default_span, default_failrate, default_waits, default_conflicts = range(len(data[0]))

for i in range(len(data)):
    if data[i][map_name] == "fluid_test_smallscale":
        data[i][map_name] = "passage"
    if data[i][encoding_scheme_name] == "edge_weight":
        data[i][encoding_scheme_name] = "Edge weight"
    elif data[i][encoding_scheme_name] == "node_vector":
        data[i][encoding_scheme_name] = "Node vector"

for i in range(len(data)):
    print(data[i][map_name] + " " + data[i][num_agents] + " " + data[i][encoding_scheme_name] + " : " + "SOC_best = " + data[i][best_cost] + " SOC_default = " + data[i][default_cost] + " P_value_SOC = " + data[i][p_value_SOC] + "Waits_best = " + data[i][best_waits] + " Waits_default = " + data[i][default_waits] + " P_value_Waits = " + data[i][p_value_waits] + "Conflicts_best = " + data[i][best_conflicts] + " Conflicts_default = " + data[i][default_conflicts] + " P_value_Conflicts = " + data[i][p_value_conflicts])



for i in range(4):
    i_1 = i * 3
    i_2 = i * 3 + 1
    i_3 = i * 3 + 2
    i_n_1 = i * 3 + 12
    i_n_2 = i * 3 + 1 + 12
    i_n_3 = i * 3 + 2 + 12

    # Create some sample data
    soc_best_edge = [float(data[i_1][best_cost]), float(data[i_2][best_cost]), float(data[i_3][best_cost])]
    soc_best_node = [float(data[i_n_1][best_cost]), float(data[i_n_2][best_cost]), float(data[i_n_3][best_cost])]
    soc_default = [float(data[i_1][default_cost]), float(data[i_2][default_cost]), float(data[i_3][default_cost])]

    error_best_edge = [1-float(data[i_1][best_failrate]), 1-float(data[i_2][best_failrate]), 1-float(data[i_3][best_failrate])]
    error_best_node = [1-float(data[i_n_1][best_failrate]), 1-float(data[i_n_2][best_failrate]), 1-float(data[i_n_3][best_failrate])]
    error_default = [1-float(data[i_1][default_failrate]), 1-float(data[i_2][default_failrate]), 1-float(data[i_3][default_failrate])]

    waits_best_edge = [float(data[i_1][best_waits]), float(data[i_2][best_waits]), float(data[i_3][best_waits])]
    waits_best_node = [float(data[i_n_1][best_waits]), float(data[i_n_2][best_waits]), float(data[i_n_3][best_waits])]
    waits_default = [float(data[i_1][default_waits]), float(data[i_2][default_waits]), float(data[i_3][default_waits])]

    conflicts_best_edge = [float(data[i_1][best_conflicts]), float(data[i_2][best_conflicts]), float(data[i_3][best_conflicts])]
    conflicts_best_node = [float(data[i_n_1][best_conflicts]), float(data[i_n_2][best_conflicts]), float(data[i_n_3][best_conflicts])]
    conflicts_default = [float(data[i_1][default_conflicts]), float(data[i_2][default_conflicts]), float(data[i_3][default_conflicts])]

    densities = [float(data[i_1][num_agents]), float(data[i_2][num_agents]), float(data[i_3][num_agents])]



    # SOC plot
    plt.plot(densities, soc_default, marker=maker2, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label="Default", color="red",markerfacecolor=markerfacecolor2)
    plt.plot(densities, soc_best_node, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label=data[i_n_1][encoding_scheme_name], color="blue",markerfacecolor=markerfacecolor3)
    plt.plot(densities, soc_best_edge, marker=maker1, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label=data[i_1][encoding_scheme_name], color="purple",markerfacecolor=markerfacecolor1)

    plt.title(data[i_1][map_name], fontsize=title_size)
    plt.xlabel('Number of robots', fontsize=label_size)
    plt.ylabel('Sum of costs', fontsize=label_size)
    plt.xticks(densities[::])
    #plt.ylim()
    plt.legend(fontsize=legend_size)
    plt.savefig("Best_chromosomes/Plots/" + data[i_1][map_name] + "_" + "soc" + ".png")
    plt.show()

    # Failrate Plot
    plt.plot(densities, error_default, marker=maker2, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label="Default", color="red",markerfacecolor=markerfacecolor2)
    plt.plot(densities, error_best_node, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label=data[i_n_1][encoding_scheme_name], color="blue",markerfacecolor=markerfacecolor3)
    plt.plot(densities, error_best_edge, marker=maker1, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label=data[i_1][encoding_scheme_name], color="purple",markerfacecolor=markerfacecolor1)

    plt.title(data[i_1][map_name], fontsize=title_size)
    plt.xlabel('Number of robots', fontsize=label_size)
    plt.ylabel('Success rate', fontsize=label_size)
    plt.xticks(densities[::])
    plt.ylim((y_bottom, y_top))
    plt.legend(fontsize=legend_size)
    plt.savefig("Best_chromosomes/Plots/" + data[i_1][map_name] + "_" + "success_rate" + ".png")
    plt.show()

    # Wait Plot
    plt.plot(densities, waits_default, marker=maker2, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label="Default", color="red",markerfacecolor=markerfacecolor2)
    plt.plot(densities, waits_best_node, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label=data[i_n_1][encoding_scheme_name], color="blue",markerfacecolor=markerfacecolor3)
    plt.plot(densities, waits_best_edge, marker=maker1, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label=data[i_1][encoding_scheme_name], color="purple",markerfacecolor=markerfacecolor1)

    plt.title(data[i_1][map_name], fontsize=title_size)
    plt.xlabel('Number of robots', fontsize=label_size)
    plt.ylabel('Average number of waits', fontsize=label_size)
    plt.xticks(densities[::])
    #plt.ylim()
    plt.legend(fontsize=legend_size)
    plt.savefig("Best_chromosomes/Plots/" + data[i_1][map_name] + "_" + "waits" + ".png")
    plt.show()
    

    # Conflicts Plot
    plt.plot(densities, conflicts_default, marker=maker2, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label="Default", color="red",markerfacecolor=markerfacecolor2)
    plt.plot(densities, conflicts_best_node, marker=maker3, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label=data[i_n_1][encoding_scheme_name], color="blue",markerfacecolor=markerfacecolor3)
    plt.plot(densities, conflicts_best_edge, marker=maker1, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label=data[i_1][encoding_scheme_name], color="purple",markerfacecolor=markerfacecolor1)

    plt.title(data[i_1][map_name], fontsize=title_size)
    plt.xlabel('Number of robots', fontsize=label_size)
    plt.ylabel('Average number of conflicts', fontsize=label_size)
    plt.xticks(densities[::])
    #plt.ylim()
    plt.legend(fontsize=legend_size)
    plt.savefig("Best_chromosomes/Plots/" + data[i_1][map_name] + "_" + "conflicts" + ".png")
    plt.show()