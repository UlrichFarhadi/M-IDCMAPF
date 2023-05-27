# Library imports

import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
import random
import copy

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Map.map import Map #
#from Map.map import * # Dårlig kodeskik at importere en hel fil
from Agent.agent import Agent


class IDCMAPF_agent(Agent):
    def __init__(self, map: Map, waiting_threshold: int = 8, repetition_threshold: int = 3, repeated_window: int = 15, rule_order = [0,1,2,3,4,5,6]):
        super().__init__(map)
        self.give_way_node = None
        self.number_requests_my_node: int = 0
        self.number_followers: int = 0
        self.leader: Agent = None
        self.priority = None
        self.neighboring_agents = []
        self.action = None 
        self.follower = None
        self.path_history = []
        self.waiting_time: int = 0                          # numberWaitingtime
        self.waiting_threshold = waiting_threshold          # waitngThreshold
        self.repetition_threshold = repetition_threshold    # repetitionThreshold
        self.repeated_window = repeated_window              # l (How many nodes should we look back in the path when seaching for repeated nodes)

        self.rule_list = [self.rule_1, self.rule_2, self.rule_3, self.rule_4, self.rule_5, self.rule_6, self.rule_7]
        if len(self.rule_list) == len(rule_order):
            self.rule_list = [self.rule_list[i] for i in rule_order]
        else:
            raise KeyError("Length not the same")

    def find_neighbors(self, depth):
        # Finds the positions of the neighbors
        neighbors = set([self.position])
        for _ in range(depth):
            for n in neighbors.copy():
                neighbors.update(self.map.map.neighbors(n))
        
        neighbors.remove(self.position)
        return neighbors

    # def find_neighbors(self, depth):
    #     # Finds the positions of the neighbors
    #     neighbors = set([self.position])
    #     for _ in range(depth):
    #         new_neighbors = set()
    #         for n in neighbors:
    #             for neighbor in self.map.map.neighbors(n):
    #                 if neighbor not in neighbors and neighbor not in new_neighbors:
    #                     new_neighbors.add(neighbor)
    #         neighbors |= new_neighbors
    #     neighbors.remove(self.position)
    #     return neighbors


    def fetch_data_from_local_neighboring_agents(self):
        # Find agents (agent objects, NOT positions!!!)
        neighbors_list = self.find_neighbors(2)
        agents = []
        # Only save those neighbors that have an Agent placed on them
        for x in neighbors_list:
            #print(self.map.map.nodes[x])
            if self.map.map.nodes[x]["agent"] is not None:  # Check if the node has an agent placed on it
                agents.append(self.map.map.nodes[x]["agent"])
        self.neighboring_agents = agents
        
    def get_number_requests_my_node(self):
        number_request_my_node = 0
        for agent in self.neighboring_agents:
            if len(agent.path) > 0:
                if agent.path[0] == self.position:
                    number_request_my_node += 1
                elif  len(agent.path) > 1:
                    if agent.path[1] == self.position:
                        number_request_my_node += 1
        return number_request_my_node

    #def get_number_of_followers

    def get_path_length_of_neighbors(self):
        path_length_list = []
        for agent in self.neighboring_agents:
            path_length_list.append(len(agent.path))
        return path_length_list
    
    def update_give_way_node(self, critical_node = None):
        # In the another method than DCMAPF take the cost into consideration when chosing between the available give_way_nodes (there can be up to 3 give_way_nodes)
        # If there are more than one neighbor, choose one randomly to be the give_way_node

        first_neighbors = self.find_neighbors(depth=1) 
        # Create a new set to store the neighbors we want to keep
        new_neighbors = []

        for n in first_neighbors:
            if self.map.map.nodes[n]["agent"] is not None: # If an agent is standing on the node (remove it)
                continue  # skip this node
            if critical_node is not None and n == critical_node: # Check if the neighboring node is THE critical node, then remove it (because we cannot enter it). n is a pos (x,y) of the neighbor which is the same for the critical node
                continue  # skip this node
            new_neighbors.append(n)  # add this node to the new set

        # # Update the `first_neighbors` set to contain only the nodes we want to keep
        # first_neighbors = new_neighbors
        # if len(first_neighbors) == 0:
        #     self.give_way_node = None
        # if len(first_neighbors) == 1:
        #     self.give_way_node = first_neighbors[0]
        # else:
        #     self.give_way_node = random.choice(first_neighbors)
        if not new_neighbors:
            self.give_way_node = None
        else:
            if len(new_neighbors) == 1:
                self.give_way_node = new_neighbors[0]
            else:
                self.give_way_node = random.choice(new_neighbors)
        
    def neighbors_remaining_nodes(self) -> bool:
        path_lengths = self.get_path_length_of_neighbors()
        for agent_path in path_lengths:
            if agent_path > 0:  # Check if an agent is still not done moving
                return True
        return False

    def node_is_free(self, position_of_node):
        if self.map.map.nodes[position_of_node]["agent"] is None:
            return True
        else:
            return False
        
    def get_follower(self):
        follower_count: int = 0
        for i in self.neighboring_agents:
            if len(i.path) == 0:
                continue
            elif self.position == i.path[0]:
                follower_count += 1
        
        if follower_count == 1:
            for i in self.neighboring_agents:
                if len(i.path) == 0:
                    continue
                elif self.position == i.path[0]:
                    self.follower = i
        else: # If there is doubt about who the follower is, then ignore it, because the neighbors have not decided for the conflict yet because of the execution
            self.follower = None
        
    def find_repeated_pairs(self):
        pair_counts = {}
        for pair in self.path_history[- self.repeated_window:]: # Take the last elements
            if pair in pair_counts:
                pair_counts[pair] += 1
                if pair_counts[pair] > self.repetition_threshold:
                    return True
            else:
                pair_counts[pair] = 1
        return False
    

    def IDCMAPF(self): # Algorithm 1
        self.fetch_data_from_local_neighboring_agents()
        if not ((len(self.path) != 0) or (self.neighbors_remaining_nodes())):   # Scuffed but okay for now
            return  # If path length of "this" robot is 0 and ANY of its neighbors also dont have a remainin path length, then nothing needs to be done and we can return
        
        if (self.find_repeated_pairs()):
            new_map = copy.deepcopy(self.map.map)
            
            new_map.remove_node(self.path_history[-1])

            try:
                self.path = nx.astar_path(new_map, self.position, self.target)
            except:
                self.action = "wait"
            
        if (self.waiting_time > self.waiting_threshold):
            new_map = copy.deepcopy(self.map.map)

            for neighbor in self.neighboring_agents:
                new_map.remove_node(neighbor.position)

            try:
                self.path = nx.astar_path(new_map, self.position, self.target)
            except:
                self.action = "wait"

        if len(self.neighboring_agents) == 0:
            self.action = "move"
        # Note: self.path[0] not the current agent position, but the next element in its path (aka agentpos_t+1)
        #       This is the same with neighboring_agent.path[0] -> It is "that" neighboring agents t+1 position
        # Note: se
        for neighboring_agent in self.neighboring_agents:
            # Something is fishy here, ask Anders
            # if len(neighboring_agent.path) > 0:
            #print(" VAR: ", len(self.neighboring_agents))
            if self.opposite_detection(neighboring_agent): # OBS, SUBSCRIPTING ERROR!!!  MAKE THIS A FUNCTION TO HANDLE THE SUBSCRIPTING ERROR
                critical_nodes = [self.position, self.path[0]]
                self.solve_opposite_conflict(critical_nodes, self.neighboring_agents)
            elif self.intersection_detection(neighboring_agent):
                critical_node = self.path[0]
                self.solve_intersection_conflict(critical_node, self.neighboring_agents)
            else:
                self.action = "move"
                self.get_follower()
                if self.follower == None:
                    continue
                if (len(self.follower.path) > len(self.path)):
                    self.update_give_way_node() # FEJL, der er ingen critical node..._
                    if (self.give_way_node is not None):
                        self.path.insert(0, self.position)
                        self.path.insert(0, self.give_way_node)
                    else:
                        self.action = "wait"
                        
            
    def solve_intersection_conflict(self, critical_node, neighborhood):  # Algorithm 3
        
        priority = self.check_priority_rules(critical_node, neighborhood)

        if len(self.path) > 1:   
            if priority and self.node_is_free(self.path[1]):
                self.action = "move"
        elif not priority: # not sure if we should delete this 
            self.update_give_way_node() # FEJL, der er ingen critical node..._
            if (self.give_way_node is not None):
                self.path.insert(0, self.position)
                self.path.insert(0, self.give_way_node)
                self.action = "move"
            else:
                self.action = "wait"
        else:
            self.action = "wait"
        #HOW SHOULD I MOVE THE OTHER AGENTS BLOCKING ME, WITHOUT ENDING IN A RACE CONDITION
        # Answer: We cant, and need to REPLAN

    def solve_opposite_conflict(self, critical_node, neighborhood):  # Algorithm 4 
        # hvorfor spilde tid på at regne de andres action når de selv regner deres???
        
        #neighborhood = Nt.append(self) #list for check_priority
        
        # # Step 1: Determine the highest priority agent
        # priority_robot = check_priority_rules(critical_node, neighborhood)
        
        self.action = "move"
        if not self.check_priority_rules(critical_node, neighborhood):
            self.update_give_way_node(critical_node)
            #check give way node for being empty
            if self.give_way_node is None:
                self.action = "wait"
            else:
                self.path.insert(0, self.position)
                self.path.insert(0, self.give_way_node)
         
    def check_priority_rules(self, critical_node, neighborhood_input):

        # Implement priority rules for determining the highest priority agent
        # rule1: a robot occupying a critical node is given priority.
        
        def check_self(neighbor_list):
            for neighbor in neighbor_list:
                if self.position == neighbor.position:
                    return True
            return False
        
        def check_agents_with_priority(agents_with_priority, list_of_agents, neighborhood):
            if check_self(agents_with_priority):
                if len(agents_with_priority) == 1:
                    return (True, None)
                else:
                    return (None, list(agents_with_priority))
            else:
                if len(agents_with_priority) > 0:
                    return (False, None)
                else:
                    if len(list_of_agents) == len(neighborhood):
                        return (None, list(neighborhood))
                    else:
                        return (None, list_of_agents)

        neighborhood = list(neighborhood_input)
        neighborhood.append(self)

        list_of_agents = list(neighborhood)
        
        for rule in self. rule_list:
            agents_with_priority = rule(list_of_agents, critical_node)
            result, list_of_agents = check_agents_with_priority(agents_with_priority, list_of_agents, neighborhood)
            if result is not None:
                return result
        return False

    
    def post_coordination(self):    # Algorithm 2
        for agent in self.neighboring_agents:
            if self.intersection_detection(agent) and self.action == "move" and agent.action == "move":
                critical_node = self.path[0]
                self.solve_intersection_conflict(critical_node, self.neighboring_agents)
            else:
                if len(self.path) > 0 :
                    if self.map.map.nodes[self.path[0]].get("agent") is not None:
                        leader = self.map.map.nodes[self.path[0]].get("agent")
                        if len(leader.path) > 0:
                            if leader.action == "wait":
                                self.action = "wait"
                            elif leader.action == "move" and leader.path[0] == self.position: #DETTE BURDE LÆNGE VÆRE LØST ???
                                self.action = "move"
                                self.update_give_way_node()
                                if self.give_way_node == None:
                                    self.action = "wait"
                                else:
                                    self.path.insert(0, self.position)
                                    self.path.insert(0, self.give_way_node) # SKAL MÅSKE TJEKKES OM DETTE OGSÅ SKABER PROBLEMER 

    def move(self):
        if self.action == "move": # and (self.position != self.target):
            if len(self.path) > 0:
                self.path_history.append(self.path[0])
                pos_prev = self.position
                pos_next = self.path.pop(0)
            else:
                pos_prev = self.position
                pos_next = self.position
            
            # update agent position on the map
            self.map.update_agent_on_map(self, pos_prev, pos_next)
            self.position = pos_next

            self.waiting_time = 0
        else:
            self.waiting_time += 1
            self.map.update_agent_on_map(self, self.position, self.position)
        
        self.action = None
    

    def opposite_detection(self, neighboring_agent) -> bool: 
        if (len(self.path) >= 1) and len(neighboring_agent.path) >= 1:
            if (self.path[0] == neighboring_agent.position) and (neighboring_agent.path[0] == self.position):
                return True
        return False

    def intersection_detection(self, neighboring_agent) -> bool:
        if (len(self.path) >= 1) and len(neighboring_agent.path) >= 1:
            if (self.path[0] == neighboring_agent.path[0]):
                return True
        return False
    
       
    def rule_1(self, list_of_agents, critical_node):
        agents_with_priority = []
        for neighbor in list_of_agents:
            for node in critical_node:
                if neighbor.position == node:
                    agents_with_priority.append(neighbor)
        return agents_with_priority

    def rule_2(self, list_of_agents, _ = None):
        agents_with_priority = []
        for i in list_of_agents:
            for j in list_of_agents:
                if i is not j:
                    if len(j.path) > 0 and len(i.path) > 0 :
                        if i.position == j.path[0] and i.path[0] != j.position:
                            agents_with_priority.append(i)
        return agents_with_priority

    def rule_3(self, list_of_agents, critical_node):
        agents_with_priority = []
        for i in list_of_agents:
            nodes = i.find_neighbors(1)
            for node in nodes:
                if self.node_is_free(node) and node not in critical_node:
                    agents_with_priority.append(i)
                    break
        return agents_with_priority



    def rule_4(self, list_of_agents, _ = None):
        agents_with_priority = []
        max_followers = max(agent.number_followers for agent in list_of_agents)
        agents_with_priority = [agent for idx, agent in enumerate(list_of_agents) if agent.number_followers == max_followers]
        return agents_with_priority


    def rule_5(self, list_of_agents, _ = None):
        agents_with_priority = []
        for agent in list_of_agents:
            if len(agent.path) > 1: 
                if self.node_is_free(agent.path[1]):
                    agents_with_priority.append(agent)
        return agents_with_priority

    def rule_6(self, list_of_agents, _ = None):
        agents_with_priority = []
        max_request = max(agent.number_requests_my_node for agent in list_of_agents)
        agents_with_priority = [agent for agent in list_of_agents if agent.number_requests_my_node == max_request]
        return agents_with_priority

    def rule_7(self, list_of_agents, _ = None):
        agents_with_priority = []
        longest_path = max(len(agent.path) for agent in list_of_agents)
        agents_with_priority = [agent for agent in list_of_agents if len(agent.path) == longest_path]
        return agents_with_priority

         