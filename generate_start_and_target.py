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


def generate_start_and_target_to_numpy(number_of_experiments = 100 , number_of_agents= 200 ,env="Environments/random-32-32-20.map", save_start_path ="Positions_for_environment/nplist_start", save_target_path = "Positions_for_environment/nplist_target"):
    map = Map()
    map.generate_map(env)
    
    # Split the path into the directory path and filename
    dir_path, filename_with_ext = os.path.split(env)

    # Split the filename into the name and extension
    filename, ext = os.path.splitext(filename_with_ext)

    def generate_new_start_target_positions(map,amount_of_agents):
        start = []
        target = []
        start_positions = copy.deepcopy(map.free_nodes)
        for i in range(amount_of_agents):
            node_tag = random.choice(start_positions)
            start_positions.remove(node_tag)
            start.append(node_tag)

        target_positions = copy.deepcopy(map.free_nodes)
        for i in range(amount_of_agents):
            node_tag = random.choice(target_positions)
            target_positions.remove(node_tag)
            target.append(node_tag)
        return start, target

    list_start = []
    list_target = []

    for i in range(number_of_experiments):
        start , target = generate_new_start_target_positions(map,number_of_agents)
        list_start.append(start)
        list_target.append(target)

    np.save(save_start_path, list_start)
    np.save(save_target_path, list_target)

# def load_lists_from_nplist(env = "random-32-32-20"):
#     list_start = np.load("Positions_for_environment/"+env+".npy")
#     list_target = np.load("Positions_for_environment/nplist_target_"+env+".npy")
#     def numpy_to_list_of_tuple(list):
#         if len(list) > 0:                            # Any element in list
#             list_of_tuple = list.tolist()
#             for idx1, both_position in enumerate(list_of_tuple):      #start and target
#                 for idx2, position in enumerate(both_position):
#                     list_of_tuple[idx1][idx2] = tuple(position)
#             return list_of_tuple

    #positions = [start_list,target_list]


    # #print(list_start)
    # list_start = numpy_to_list_of_tuple(list_start)
    # list_target = numpy_to_list_of_tuple(list_target)
    # return list_start, list_target
    #print(list_start)


def load_position_list_from_nplist(env):
    list_start = np.load(env+".npy")
    #list_target = np.load("Positions_for_environment/nplist_target_"+env+".npy")
    def numpy_to_list_of_tuple(list):
        if len(list) > 0:                            # Any element in list
            list_of_tuple = list.tolist()
            for idx1, both_position in enumerate(list_of_tuple):      #start and target
                for idx2, position in enumerate(both_position):
                    list_of_tuple[idx1][idx2] = tuple(position)
            return list_of_tuple

    #positions = [start_list,target_list]


    #print(list_start)
    list_start = numpy_to_list_of_tuple(list_start)
    #list_target = numpy_to_list_of_tuple(list_target)
    return list_start#, list_target


#generate_start_and_target_to_numpy()
#list_start, list_target = load_lists_from_nplist()
#print(list_start)



def generate_start_and_target_to_list(number_of_experiments = 100 , number_of_agents= 200 ,env="Environments/random-32-32-20.map"):
    map = Map()
    map.generate_map(env)

    def generate_new_start_target_positions(map,amount_of_agents):
        start = []
        target = []
        start_positions = copy.deepcopy(map.free_nodes)
        for i in range(amount_of_agents):
            node_tag = random.choice(start_positions)
            start_positions.remove(node_tag)
            start.append(node_tag)

        target_positions = copy.deepcopy(map.free_nodes)
        for i in range(amount_of_agents):
            node_tag = random.choice(target_positions)
            target_positions.remove(node_tag)
            target.append(node_tag)
        return start, target

    list_start = []
    list_target = []

    for i in range(number_of_experiments):
        start , target = generate_new_start_target_positions(map,number_of_agents)
        list_start.append(start)
        list_target.append(target)


    return list_start , list_target


def read_scenario(file_path: str):
    #print(os.system("dir"))
    startpos = []
    targetpos = []
    map = None
    with open(file_path, "r") as file:
        next(file) # skip first line
        lines = file.readlines()
        for line in lines:
            elements = line.split()
            maybe_id = int(elements[0])
            environment_name = elements[1]
            if map is None:
                map = Map()
                map.generate_map("Environments/"+environment_name)
            width = elements[2]
            height = elements[3]
            start = (int(elements[4]), (int(height)-1) - int(elements[5]))
            target = (int(elements[6]),(int(height)-1) - int(elements[7]))
            if start in map.free_nodes and target in map.free_nodes:
                startpos.append(start)
                targetpos.append(target)
            # if start not in map.free_nodes:
            #     print(start)
            # if target not in map.free_nodes:
            #     print(target)
            random_float = float(elements[8])

    # print(len(startpos))
    return startpos , targetpos 

def generate_start_and_target_from_scenario(file_path: str, num_agents):
    start = []
    target = []
    for i in range(25):
        filename = file_path + str(i+1)+ ".scen"
        startpos , targetpos = read_scenario(filename)
        start.append(startpos[:num_agents])
        target.append(targetpos[:num_agents])
    return start , target