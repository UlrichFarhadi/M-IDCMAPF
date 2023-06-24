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

# Colors
color_PIBT = "darkgoldenrod"
color_PIBT_PLUS = "green"
color_EECBS = "blue"
color_CBS = "teal"
color_DCMAPF = "purple"
color_IDCMAPF = "saddlebrown"
color_M_IDCMAPF = "red"

# Create some sample data

# random-32-32-20
random_32_32_20_PIBT_SOC = [1310.3478260869565, 2975.3571428571427, 5189.818181818182, 7747.5]
random_32_32_20_PIBT_PLUS_SOC = [1322.64, 3037.28, 5257.88, 8062.24]
random_32_32_20_EECBS_SOC = [1156.24, 2458.0, 3970.25, 5486.5]
random_32_32_20_CBS_SOC = [1140.6666666666667]
random_32_32_20_DCMAPF_SOC = [1302.64, 3170.84, 6481.44, 12417.2]
random_32_32_20_IDCMAPF_SOC = [1306.8, 3117.56, 5995.52, 10538.28]
random_32_32_20_M_IDCMAPF_SOC = [1273.5, 3068, 5589.54, 9495.18]

random_32_32_20_PIBT_SR = [0.92, 0.56, 0.44, 0.16]
random_32_32_20_PIBT_PLUS_SR = [1.0, 1.0, 1.0, 1.0]
random_32_32_20_EECBS_SR = [1.0, 1.0, 0.96, 0.08]
random_32_32_20_CBS_SR = [0.84]
random_32_32_20_DCMAPF_SR = [1.0, 1.0, 1.0, 1.0]
random_32_32_20_IDCMAPF_SR = [1.0, 1.0, 1.0, 1.0]
random_32_32_20_M_IDCMAPF_SR = [1, 1.0, 1.0, 1-0.008]
random_32_32_20_density = [50,100,150,200]

# empty-48-48
empty_48_48_PIBT_SOC = [1681.36, 3548.36, 5606.76, 7795.68, 10080.84, 12567.28, 15231.6, 17874.28]
empty_48_48_PIBT_PLUS_SOC = [1681.36, 3548.36, 5606.6, 7796.16, 10081.28, 12567.36, 15231.6, 17874.28]
empty_48_48_EECBS_SOC = [1584.64, 3153.84, 4765.2, 6371.96, 8001.68, 9709.16, 11452.4, 13222.12]
empty_48_48_CBS_SOC = [1583.64, 3143.375, 4724.272727272727, 6195.4]
empty_48_48_DCMAPF_SOC = [1660.88, 3348.04, 5140.92, 7002.04, 9006.16, 11279.92, 13980.84, 17283.72]
empty_48_48_IDCMAPF_SOC = [1660.36, 3350.08, 5138.96, 6996.16, 8944.52, 11151.6, 13572.88, 16516.12]
empty_48_48_M_IDCMAPF_SOC = [1610.72, 3262.148, 5021.62, 6866.352, 8830.296, 10993.208, 13405.964, 16145.364]

empty_48_48_PIBT_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
empty_48_48_PIBT_PLUS_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
empty_48_48_EECBS_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
empty_48_48_CBS_SR = [1.0, 0.96, 0.88, 0.2]
empty_48_48_DCMAPF_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
empty_48_48_IDCMAPF_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
empty_48_48_M_IDCMAPF_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
empty_48_48_density = [50,100,150,200,250,300,350,400]

# random-64-64-20
random_64_64_20_PIBT_SOC = [2384.88, 5043.96, 7873.64, 10905.1, 14264.125, 17744.14285714286, 21386.75, 25773.428571428572]
random_64_64_20_PIBT_PLUS_SOC = [2384.88, 5043.96, 7873.84, 10916.56, 14241.88, 17683.16, 21293.96, 25233.88]
random_64_64_20_EECBS_SOC = [2251.32, 4532.12, 6825.08, 9194.8, 11662.8, 14189.4, 16843.76, 19714.08]
random_64_64_20_CBS_SOC = [2246.04, 4469.733333333334]
random_64_64_20_DCMAPF_SOC = [2360.56, 4866.28, 7560.72, 10611.04, 14413.16, 19046.52, 25163.083333333332, 32186.916666666668]
random_64_64_20_IDCMAPF_SOC = [2358.84, 4870.72, 7515.48, 10519.76, 13880.24, 17754.68, 22583.84, 28168.24]
random_64_64_20_M_IDCMAPF_SOC = [2323.428, 4831.036, 7521.636, 10548.264, 13998.348, 17876.008, 22496.44, 28408.872]

random_64_64_20_PIBT_SR = [1.0, 1.0, 1.0, 0.8, 0.64, 0.56, 0.48, 0.28]
random_64_64_20_PIBT_PLUS_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
random_64_64_20_EECBS_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
random_64_64_20_CBS_SR = [1.0, 0.6]
random_64_64_20_DCMAPF_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.96, 0.96]
random_64_64_20_IDCMAPF_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
random_64_64_20_M_IDCMAPF_SR = [1.0, 1.0, 1.0, 0.996, 1.0, 1.0, 0.996, 0.956]
random_64_64_20_density = [50,100,150,200,250,300,350,400]

# ost003d
ost003d_PIBT_SOC = [7933.68, 16167.88, 24781.0, 33866.12, 43425.68, 53281.8]
ost003d_PIBT_PLUS_SOC = [7933.68, 16167.88, 24781.0, 33866.12, 43426.08, 53281.8]
ost003d_EECBS_SOC = []
ost003d_CBS_SOC = [7675.291666666667, 14469.6]
ost003d_DCMAPF_SOC = []
ost003d_IDCMAPF_SOC = [8080.52, 16831.24, 27041.8, 39483.68, 55416.28, 93879.32]
ost003d_M_IDCMAPF_SOC = [8062.664, 16362.788, 25061.936, 34489.812, 44993.492, 63206.132]

ost003d_PIBT_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
ost003d_PIBT_PLUS_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
ost003d_EECBS_SR = []
ost003d_CBS_SR = [0.96, 0.2]
ost003d_DCMAPF_SR = []
ost003d_IDCMAPF_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
ost003d_M_IDCMAPF_SR = [1.0, 1.0, 1.0, 1.0, 1.0, 0.944]
ost003d_density = [50,100,150,200,250,300]


PIBT_SOC = [random_32_32_20_PIBT_SOC, empty_48_48_PIBT_SOC, random_64_64_20_PIBT_SOC, ost003d_PIBT_SOC]
PIBT_PLUS_SOC = [random_32_32_20_PIBT_PLUS_SOC, empty_48_48_PIBT_PLUS_SOC, random_64_64_20_PIBT_PLUS_SOC, ost003d_PIBT_PLUS_SOC]
EECBS_SOC = [random_32_32_20_EECBS_SOC, empty_48_48_EECBS_SOC, random_64_64_20_EECBS_SOC, ost003d_EECBS_SOC]
CBS_SOC = [random_32_32_20_CBS_SOC, empty_48_48_CBS_SOC, random_64_64_20_CBS_SOC, ost003d_CBS_SOC]
DCMAPF_SOC = [random_32_32_20_DCMAPF_SOC, empty_48_48_DCMAPF_SOC, random_64_64_20_DCMAPF_SOC, ost003d_DCMAPF_SOC]
IDCMAPF_SOC = [random_32_32_20_IDCMAPF_SOC, empty_48_48_IDCMAPF_SOC, random_64_64_20_IDCMAPF_SOC, ost003d_IDCMAPF_SOC]
M_IDCMAPF_SOC = [random_32_32_20_M_IDCMAPF_SOC, empty_48_48_M_IDCMAPF_SOC, random_64_64_20_M_IDCMAPF_SOC, ost003d_M_IDCMAPF_SOC]

PIBT_SR = [random_32_32_20_PIBT_SR, empty_48_48_PIBT_SR, random_64_64_20_PIBT_SR, ost003d_PIBT_SR]
PIBT_PLUS_SR = [random_32_32_20_PIBT_PLUS_SR, empty_48_48_PIBT_PLUS_SR, random_64_64_20_PIBT_PLUS_SR, ost003d_PIBT_PLUS_SR]
EECBS_SR = [random_32_32_20_EECBS_SR, empty_48_48_EECBS_SR, random_64_64_20_EECBS_SR, ost003d_EECBS_SR]
CBS_SR = [random_32_32_20_CBS_SR, empty_48_48_CBS_SR, random_64_64_20_CBS_SR, ost003d_CBS_SR]
DCMAPF_SR = [random_32_32_20_DCMAPF_SR, empty_48_48_DCMAPF_SR, random_64_64_20_DCMAPF_SR, ost003d_DCMAPF_SR]
IDCMAPF_SR = [random_32_32_20_IDCMAPF_SR, empty_48_48_IDCMAPF_SR, random_64_64_20_IDCMAPF_SR, ost003d_IDCMAPF_SR]
M_IDCMAPF_SR = [random_32_32_20_M_IDCMAPF_SR, empty_48_48_M_IDCMAPF_SR, random_64_64_20_M_IDCMAPF_SR, ost003d_M_IDCMAPF_SR]

densities = [random_32_32_20_density, empty_48_48_density, random_64_64_20_density, ost003d_density]




y_bottom = 0.0
y_top = 1.01

maker1 = "o"
maker2 = "o"
maker3 = "D"
maker4 = "D"
maker5 = "^"
maker6 = "h"
maker7 = "h"

markerfacecolor1 = 'w'
markerfacecolor2 = 'w'
markerfacecolor3 = None
markerfacecolor4 = None

map_names = ["random-32-32-20", "empty-48-48", "random-64-64-20", "ost003d"]

for i in range(len(map_names)):
    if len(PIBT_SOC[i]) != 0:
        plt.plot(densities[i][:len(PIBT_SOC[i])], PIBT_SOC[i], marker=maker1, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT', color=color_PIBT,markerfacecolor=markerfacecolor3)
    if len(PIBT_PLUS_SOC[i]) != 0:
        plt.plot(densities[i][:len(PIBT_PLUS_SOC[i])], PIBT_PLUS_SOC[i], marker=maker2, linestyle=line_style2, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT+', color=color_PIBT_PLUS,markerfacecolor=markerfacecolor2)
    if len(EECBS_SOC[i]) != 0:
        plt.plot(densities[i][:len(EECBS_SOC[i])], EECBS_SOC[i], marker=maker7, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='EECBS', color=color_EECBS,markerfacecolor=markerfacecolor3)
    if len(CBS_SOC[i]) != 0:
        plt.plot(densities[i][:len(CBS_SOC[i])], CBS_SOC[i], marker=maker4, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='CBS', color=color_CBS,markerfacecolor=markerfacecolor2)
    if len(DCMAPF_SOC[i]) != 0:
        plt.plot(densities[i][:len(DCMAPF_SOC[i])], DCMAPF_SOC[i], marker=maker5, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='DCMAPF', color=color_DCMAPF,markerfacecolor=markerfacecolor3)
    if len(IDCMAPF_SOC[i]) != 0:
        plt.plot(densities[i][:len(IDCMAPF_SOC[i])], IDCMAPF_SOC[i], marker=maker6, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='IDCMAPF', color=color_IDCMAPF,markerfacecolor=markerfacecolor2)
    if len(M_IDCMAPF_SOC[i]) != 0:
        plt.plot(densities[i][:len(M_IDCMAPF_SOC[i])], M_IDCMAPF_SOC[i], marker=maker3, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='M-IDCMAPF', color=color_M_IDCMAPF,markerfacecolor=markerfacecolor3)


    plt.title(map_names[i], fontsize=title_size)
    plt.xlabel('Number of robots', fontsize=label_size)
    plt.ylabel('Sum of costs', fontsize=label_size)
    plt.xticks(densities[i][::])
    #plt.ylim()
    plt.legend(fontsize=legend_size)
    plt.savefig("Comparison_with_stateoftheart/Plots/" + map_names[i] + "_SOC" + ".png")
    plt.show()

    if len(PIBT_SR[i]) != 0:
        plt.plot(densities[i][:len(PIBT_SR[i])], PIBT_SR[i], marker=maker1, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT', color=color_PIBT,markerfacecolor=markerfacecolor3)
    if len(PIBT_PLUS_SR[i]) != 0:
        plt.plot(densities[i][:len(PIBT_PLUS_SR[i])], PIBT_PLUS_SR[i], marker=maker2, linestyle=line_style2, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='PIBT+', color=color_PIBT_PLUS,markerfacecolor=markerfacecolor2)
    if len(EECBS_SR[i]) != 0:
        plt.plot(densities[i][:len(EECBS_SR[i])], EECBS_SR[i], marker=maker7, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='EECBS', color=color_EECBS,markerfacecolor=markerfacecolor3)
    if len(CBS_SR[i]) != 0:
        plt.plot(densities[i][:len(CBS_SR[i])], CBS_SR[i], marker=maker4, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='CBS', color=color_CBS,markerfacecolor=markerfacecolor2)
    if len(DCMAPF_SR[i]) != 0:
        plt.plot(densities[i][:len(DCMAPF_SR[i])], DCMAPF_SR[i], marker=maker5, linestyle=line_style3, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='DCMAPF', color=color_DCMAPF,markerfacecolor=markerfacecolor3)
    if len(IDCMAPF_SR[i]) != 0:
        plt.plot(densities[i][:len(IDCMAPF_SR[i])], IDCMAPF_SR[i], marker=maker6, linestyle=line_style1, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='IDCMAPF', color=color_IDCMAPF,markerfacecolor=markerfacecolor2)
    if len(M_IDCMAPF_SR[i]) != 0:
        plt.plot(densities[i][:len(M_IDCMAPF_SR[i])], M_IDCMAPF_SR[i], marker=maker3, linestyle=line_style4, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='M-IDCMAPF', color=color_M_IDCMAPF,markerfacecolor=markerfacecolor3)


    plt.title(map_names[i], fontsize=title_size)
    plt.xlabel('Number of robots', fontsize=label_size)
    plt.ylabel('Success rate', fontsize=label_size)
    plt.xticks(densities[i][::])
    plt.ylim((y_bottom, y_top))
    plt.legend(fontsize=legend_size)
    plt.savefig("Comparison_with_stateoftheart/Plots/" + map_names[i] + "_SR" + ".png")
    plt.show()


