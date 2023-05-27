# Library imports

import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
import random
import copy
from typing import List
import networkit as nk

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Map.map import Map #
#from Map.map import * # Dårlig kodeskik at importere en hel fil
from Agent.agent import Agent

class Swarm:
    def __init__(self, map: Map, amount_of_agents: int, agent_type = Agent):
        self.agent_type = agent_type
        self.amount_of_agents = amount_of_agents
        self.agents: List[amount_of_agents] = []
        self.map = map
        self.generate_agents()
        #bug hunting TODO remove
        self.start = []
        self.target = []
    
    def move_all_agents(self, step):
        for agent in self.agents:
            agent.move(step)
            # call agent.move() method and check if it returns False
            # if so, assign a new goal position or make it stand still     
    
    def generate_agents(self):
        # Generate a list of Agent objects and add them to self.agents
        for idx in range(self.amount_of_agents):
            self.agents.append(self.agent_type(self.map))
            self.agents[idx].id = idx
    
    def set_initial_start_positions_of_agents(self, start_positions = []):
        # Currently generaing random starting positions for the agents
        
        if len(start_positions) == 0:
            self.start = []
            start_positions = copy.deepcopy(self.map.free_nodes)
            # Set the starting position of each agent on the map
            for agent in self.agents:
                node_tag = random.choice(start_positions)
                start_positions.remove(node_tag)
                agent.position = node_tag
                #bug hunting TODO remove
                self.start.append(node_tag)
                self.map.map.nodes[node_tag]["agent"] = agent
        else:
            assert len(start_positions) == self.amount_of_agents, f"Expected {self.amount_of_agents} elements in list (start_positions), but got {len(start_positions)} instead"
            start_pos = copy.deepcopy(start_positions)
            # Set the starting position of each agent on the map
            for agent in self.agents:
                node_tag = start_pos.pop(0)
                agent.position = node_tag
                self.map.map.nodes[node_tag]["agent"] = agent
    
    def set_initial_target_positions_of_agents(self, target_positions = []):
        # Currently generaing random target positions for the agents
        if len(target_positions) == 0:
            self.target = []
            target_positions = copy.deepcopy(self.map.free_nodes)
                    # Set the target position of each agent on the map
            for agent in self.agents:
                node_tag = random.choice(target_positions)
                target_positions.remove(node_tag)
                agent.target = node_tag
                #bug hunting TODO remove
                self.target.append(node_tag)
                #self.map.map.nodes[node_tag]["target"] = True
                self.map.map.nodes[node_tag]["target"] = agent.color
        else:
            assert len(target_positions) == self.amount_of_agents, f"Expected {self.amount_of_agents} elements in list (target_positions), but got {len(target_positions)} instead"

            target_pos = copy.deepcopy(target_positions)
            for agent in self.agents:
                node_tag = target_pos.pop(0)
                agent.target = node_tag
                self.map.map.nodes[node_tag]["target"] = agent.color
    
    def calculate_agent_path(self, agent):
        # Use A* to calculate path between each agenet start and goal position
        # astar = nk.distance.AStar(self.map.G_nk, self.map.nk_heuristic, self.map.nk_node_id[agent.position], self.map.nk_node_id[agent.target])
        # astar.run()
        # path = []
        # for node_id in astar.getPath():
        #     path.append(self.map.nk_reverse_node_id[node_id])
        # path.append(agent.target)
        # if agent.position == agent.target:
        #     path = []
        # return path
        return nx.astar_path(self.map.map, agent.position, agent.target, heuristic=agent.a_star_heuristic)[1:] #removes the first element because A* includes its own cell in the path

    def calculate_all_agent_paths(self):
        # Calculates paths for all agents
        for agent in self.agents:
            agent.path = self.calculate_agent_path(agent)