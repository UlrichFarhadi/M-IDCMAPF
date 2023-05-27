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
    # #bug hunting TODO remove
    # def print_pos(self):
    #     print("start: ", self.start)
    #     print("target: ", self.target)

    def set_rule_order_of_agents(self):
        # Generate a list of Agent objects and add them to self.agents
        for agent in self.agents:
            agent.change_rule_order(self.rule_order)

    def move_all_agents(self, step):
        for agent in self.agents:
            agent.move(step)
            # if random.random() < 0.33:
            #     agent.action = "wait"
            
        self.post_coordination()

        #self.clean_repetitive_movement()

        for agent in self.agents:
            agent.final_move()
        
        self.load_modify_save_trafic()

        #self.clean_up_path()

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
        
    def clean_repetitive_movement(self):
        for agent in self.agents:
            if len(agent.path) > 1:
                while ((agent.action == "wait") and (agent.position == agent.path[1])): # Agent goes back and forth in the same spot needs to decide again next time, so remove it
                    if len(agent.path) > 1:
                        agent.path.pop(0)
                        agent.path.pop(0)
                        #print("Path cleaned")
                    if len(agent.path) <= 1:
                        break
                    

    def post_coordination(self):
        def wait_propogate(agent):
            if agent.wait_propagated_flag: # Fix inf loop in wait propogate
                return

            agent.action = "wait"
            agent.wait_propagated_flag = True

            #if agent.position in agent.path: # if a give way node is given and the agent action is wait
            #    agent.path = agent.path[2:] # Remove the 2 first element, so the program don't crash  or add unnecessary node to path 
                # if len(agent.path) > 0:
                #     if abs(agent.position[0]-agent.path[0][0]) > 1 or abs(agent.position[1]-agent.path[0][1]) > 1:
                #         print("TELEPORT DETECTED")

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

    def clean_up_path(self):
        # TODO: Check if it ends up being used
        for agent in self.agents:
            if agent.position in agent.path:
                idx = agent.path.index(agent.position)
                agent.path = agent.path[idx+1:] # maybe not plus 1 
                #print(f"id {agent.id}  position: {agent.position} and path {agent.path}")

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