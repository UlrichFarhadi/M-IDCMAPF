# Library imports

import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
import random
import copy
from typing import List
import numpy as np

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Map.map import Map #
#from Map.map import * # Dårlig kodeskik at importere en hel fil
from Agent.agent import Agent
from Agent.IDCMAPF_agent import IDCMAPF_agent
from Swarm.swarm import Swarm

class Swarm_IDCMAPF(Swarm):
    def __init__(self, map: Map, amount_of_agents: int, agent_type = Agent, rule_order=[0,1,2,3,4,5,6], traffic_id=-1):
        super().__init__(map, amount_of_agents, agent_type)
        self.agents_at_goal = 0
        self.rule_order = rule_order
        self.set_rule_order_of_agents()
        self.traffic_id = traffic_id
        self.waitcount_trafic_bool = False
        self.waitcount_trafic = []
        self.conflictcount_bool = False
        self.conflictcount = []

    def set_rule_order_of_agents(self):
        # Generate a list of Agent objects and add them to self.agents
        for agent in self.agents:
            agent.change_rule_order(self.rule_order)

    def move_all_agents(self, step):

        if self.conflictcount_bool:
            self.count_number_of_conflicts()


        for agent in self.agents:
            agent.move(step)
            
        self.post_coordination()

        if self.waitcount_trafic_bool:
            self.count_number_of_waits()

        for agent in self.agents:
            agent.final_move()
        
        self.load_modify_save_trafic()

        positions_list = []  # create an empty list
        self.agents_at_goal = 0
        for agent in self.agents:
            if (agent.position == agent.target) and (len(agent.path) == 0):
                self.agents_at_goal += 1
            if agent.position not in positions_list:  # check if the value is not already in the list
                positions_list.append(agent.position)  # add agent.position to the list
            else:
                print(f"Duplicate found: {agent.position}")  # print a message if a duplicate is found
                print("Step = ", step)
                for i in self.agents:
                    if i.position == agent.position:
                        print(f"agent id {i.id}")
                        print(f"path: {i.path}")
                        print(f"path_history: {i.path_history}")
                        print(f"action: {i.action}")
                        print(f"action_history: {i.action_history}")


        #print("Agents still moving: ", self.amount_of_agents - self.agents_at_goal)   
        if self.agents_at_goal == self.amount_of_agents:
            return True              

    def post_coordination(self):
        def wait_propogate(agent):
            if agent.wait_propagated_flag:
                return

            agent.action = "wait"
            agent.wait_propagated_flag = True

            neighbors = agent.find_neighbors(1)
            for node in neighbors:
                if agent.is_agent_present_on_node_tag(node):
                    neighbor = agent.get_agent_by_tag(node)
                    if len(neighbor.path) > 0:
                        if neighbor.path[0] == agent.position:
                            wait_propogate(neighbor)

        def swaping(agent):
            if len(agent.path) > 0:
                if agent.is_agent_present_on_node_tag(agent.path[0]):
                    neighbor_agent = agent.get_agent_by_tag(agent.path[0])
                    if len(neighbor_agent.path) > 0:
                        if neighbor_agent.position == agent.path[0] and agent.position == neighbor_agent.path[0]:
                            return True
            return False

        list_of_position_t1 = []
        for agent in self.agents:
            if agent.action == "move":
                if len(agent.path) > 0:
                    if agent.path[0] in list_of_position_t1:
                        wait_propogate(agent)
                    elif swaping(agent): 
                        list_of_position_t1.append(agent.position) # Set my pos
                        list_of_position_t1.append(agent.path[0]) # set my neighbor pos
                        wait_propogate(agent)
                    else:
                        list_of_position_t1.append(agent.path[0])
            elif agent.action == "wait":
                if agent.position in list_of_position_t1:
                    wait_propogate(agent)
                else:
                    list_of_position_t1.append(agent.position)
            else:
                print("NO ACTION???")
                print(f"action {agent.action}")

    def all_agents_reached_target_once(self):
        for agent in self.agents:
            if agent.target_reached_once == False:
                return False
        return True

    def load_modify_save_trafic(self):
        if self.traffic_id != -1:
            filename = f"trafic_data/{os.path.splitext(os.path.basename(self.map.current_map_file))[0]}_{self.traffic_id}.txt"
            if os.path.isfile(filename):
                matrix = np.loadtxt(filename)
            else:
                matrix = np.zeros((self.map.map_width, self.map.map_height))  # Adjust the size as per your requirements

            for agent in self.agents:
                if agent.position != agent.target and len(agent.path) > 0:
                    x, y = agent.position
                    matrix[x,y] += 1
            
            
            np.savetxt(filename, matrix)
    
    def count_number_of_waits(self):
        wait_count = 0
        for agent in self.agents:
            if agent.position != agent.target and len(agent.path) > 0:
                if agent.action == "wait":
                    wait_count += 1
        self.waitcount_trafic.append(wait_count)


    def count_number_of_conflicts(self):
        def find_agents_in_conflict(agent, conflict_type):
            agents_in_conflict = []
            if conflict_type == "opposite":
                agents_in_conflict.append(agent)
                agents_in_conflict.append(agent.get_agent_by_tag(agent.path[0]))
            elif conflict_type == "intersection":
                neighborhood = agent.find_neighbors(1, position=agent.path[0])
                for neighbor_tag in neighborhood:
                    if agent.is_agent_present_on_node_tag(neighbor_tag):
                        neighbor = agent.get_agent_by_tag(neighbor_tag)
                        if len(neighbor.path) >= 1:
                            if neighbor.path[0] == agent.path[0]:
                                agents_in_conflict.append(neighbor)
            return agents_in_conflict
        
        conflicts = 0
        for agent in self.agents:
            if agent.conflict_id == 0:
                if agent.detect_opposite_conflict():
                    conflicts +=1
                    conflict_cluster = find_agents_in_conflict(agent=agent, conflict_type="opposite")
                    for agent_id in conflict_cluster:
                        agent_id.conflict_id = conflicts
                if agent.detect_intersection_conflict():
                    conflicts +=1
                    conflict_cluster = find_agents_in_conflict(agent=agent, conflict_type="intersection")
                    for agent_id in conflict_cluster:
                        agent_id.conflict_id = conflicts
        self.conflictcount.append(conflicts)
        #reset conflict id
        for agent in self.agents:
            agent.conflict_id = 0