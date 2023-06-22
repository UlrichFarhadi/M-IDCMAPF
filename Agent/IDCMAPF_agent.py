# Library imports

import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
import random
import copy
from enum import Enum
#from numba import jit

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
    def __init__(self, map: Map, waiting_threshold: int = 8, detour_constant:int = 2, repetition_threshold: int = 3, repeated_window: int = 15, rule_order = [0,1,2,3,4,5,6]):
        super().__init__(map)
        self.give_way_node = None

        self.leader: Agent = None
        self.priority = None
        self.neighboring_agents = []
        self.action = None 
        self.follower = None
        self.path_history = []
        self.waiting_time: int = 0                          
        self.waiting_threshold = waiting_threshold          
        self.repetition_threshold = repetition_threshold    
        self.repeated_window = repeated_window              
        self.direction = None
        self.id: int = None
        self.wait_propagated_flag: bool = False
        self.tmp_priority = random.random()
        self.step: int = 0
        self.detour_constant = detour_constant
        self.steps_moved: int = 0
        self.target_reached_once: bool = False
        self.idle_blocked = True
        self.action_history = ["."] * self.detour_constant * 2
        self.initial_rule_list = [self.rule_1, self.rule_2, self.rule_3, self.rule_4, self.rule_5, self.rule_6, self.rule_7]
        if len(self.initial_rule_list) == len(rule_order):
            self.rule_list = [self.initial_rule_list[i] for i in rule_order]
        else:
            raise KeyError("Length not the same")
        self.conflict_id = 0

    def change_rule_order(self, rule_order):
        if len(self.rule_list) == len(rule_order):
            self.rule_list = [self.initial_rule_list[i] for i in rule_order]
        else:
            raise KeyError("Length not the same")

    def move(self, step):
        self.step += 1
        # Find neighboring agents and store their references so we have their info
        self.find_neighboring_agents()
        self.get_direction()

        # Check if the target has been reached yet to calculate sum of costs
        if self.position == self.target:
            self.target_reached_once = True

        # Detect leadlocks and livelocks and replan if detected
        if len(self.path) != 0:
            self.deadlock_and_livelock_detection()

        if self.detect_opposite_conflict():
            self_prio, list_of_agents = self.check_priority_rules(conflict_type="opposite")
            if self_prio:
                self.action = "move"
            else:
                self.give_way() # Action is set inside this function
        elif self.detect_intersection_conflict():
            self_prio, list_of_agents = self.check_priority_rules(conflict_type="intersection")
            if self_prio:
                self.action = "move"
            else:
                if list_of_agents is not None:
                    n_t_2_conflict = False
                    for agent in list_of_agents:
                        if len(agent.path) > 1: 
                            if agent.path[1] == self.position:
                                n_t_2_conflict = True
                    if n_t_2_conflict:
                        self.give_way()
                    else:
                        self.action = "wait"
                else:
                    # In case of 2 or more agents in intersection conflict and all have equal priority, instead of being stuck, we need to detour
                    self.detour_replan()
                    self.action = "wait"
        elif len(self.path) == 0: # If the agent is at its target position
            if self.number_requests_my_node() > 0:
                self.give_way_idle_robot()
            elif self.check_blocked_neighbor():
                self.give_way_idle_robot()
            else:
                self.action = "wait"
                self.idle_blocked = False
        else:
            # Check if a follower has a longer path than "this" robot. If so, give way to the follower.
            self.get_follower() # Updates the follower, sets it to None if there is no follower
            if self.follower is not None:
                if len(self.follower.path) > len(self.path):
                    self.give_way()
                    return
            self.action = "move"

    def detour_replan(self):
        def add_random_offset(coordinate_tuple, z):
            x, y = coordinate_tuple
            x_offset = random.randint(-z, z)
            y_offset = random.randint(-z, z)
            new_x = x + x_offset
            new_y = y + y_offset
            return (new_x, new_y)
        
        counter_try = 0
        while(True):
            if counter_try > 100:
                return
            try:
                detour_target = add_random_offset(coordinate_tuple=self.position, z=self.detour_constant)
                if detour_target in self.map.free_nodes:
                    if self.map.map.nodes[detour_target].get("target") is None: # Do not detour to another agents target, since it will increase sum of costs
                        self.replan([self.target], detour_target)
                        self.path_history = []
                        return True
                else:
                    counter_try += 1
                    continue
            except:
                counter_try += 1
                continue

    def deadlock_and_livelock_detection(self):
        repeated_nodes = 0
        pair_counts = {}
        for pair in self.path_history:#[- self.repeated_window:]: # Take the last elements
            if pair in pair_counts:
                repeated_nodes += 1
                if repeated_nodes > self.repetition_threshold:
                    obstacle_list = []
                    for neighboring_agent in self.neighboring_agents:
                        obstacle_list.append(neighboring_agent.position)
                    if self.replan(obstacle_list):
                        self.path_history = []
                        return True
                    else:
                        # Find a random new node and replan to that insted (aka take a detour)
                        self.detour_replan()
                        return True
            else:
                pair_counts[pair] = 1
        return False

    def check_blocked_neighbor(self):
        for neighbor in self.neighboring_agents:
            if neighbor.idle_blocked:
                return True
        else:
            return False

    def get_follower(self):
        self.get_direction()

        # Special out of bounds cases
        if self.position[0] == 0 and self.direction == "R":
            self.follower = None
            return
        if self.position[0] == (self.map.map_width - 1) and self.direction == "L":
            self.follower = None
            return
        if self.position[1] == 0 and self.direction == "U":
            self.follower = None
            return
        if self.position[1] == (self.map.map_height - 1) and self.direction == "D":
            self.follower = None
            return
        
        def verify_follower(follower_tag):
            if self.is_agent_present_on_node_tag(follower_tag):
                possible_follower = self.get_agent_by_tag(follower_tag)
                if len(possible_follower.path) > 0:
                    if possible_follower.path[0] == self.position:
                        self.follower = possible_follower
                        return
                    else:
                        self.follower = None
                        return
                else:
                    self.follower = None
                    return
            else: # No follower
                self.follower = None
                return
                        
        if self.direction == "R":
            follower_tag = (self.position[0] - 1 , self.position[1])
            verify_follower(follower_tag)
        elif self.direction == "L":
            follower_tag = (self.position[0] + 1 , self.position[1])
            verify_follower(follower_tag)
        elif self.direction == "U":
            follower_tag = (self.position[0] , self.position[1] - 1)
            verify_follower(follower_tag)
        elif self.direction == "D":
            follower_tag = (self.position[0] , self.position[1] + 1)
            verify_follower(follower_tag)
        else:
            self.follower = None

    def final_move(self):
        if (len(self.path) > 0) and (self.target_reached_once == False):
            self.steps_moved += 1
        if (len(self.path) > 0): # and (self.position != self.target):
            self.path_history.append(self.position)

        if self.action == "move":
            self.action_history.pop(-1) # Pop the last element
            self.action_history.insert(0, "move")
            self.move_agent_forward()
        self.wait_propagated_flag = False
        if (self.action == "wait") and (self.position == self.target) and (len(self.path) == 0):
            self.action_history.pop(-1) # Pop the last element
            self.action_history.insert(0, "wait")
    
    def move_agent_forward(self):
        if len(self.path) == 0:
            self.map.update_agent_on_map(self, self.target, self.target)
            return False
        
        if len(self.path) > 0:
            x = self.position[0] - self.path[0][0]
            y = self.position[1] - self.path[0][1]
            if (abs(x) > 1) or (abs(y) > 1):
                print("Telport Detected")
            
        pos_prev = self.position
        pos_next = self.path.pop(0)
        
        # update agent position on the map
        self.map.update_agent_on_map(self, pos_prev, pos_next)
        self.position = pos_next
        self.idle_blocked = False   # Reset the idle_blocked since we are moving now

    def find_neighbors(self, depth, position=None):
        # Finds the positions of the neighbors excluding the agents' own position
        pos = position
        if position is None:
            pos = self.position
            
        neighbors = set([pos])
        for _ in range(depth):
            for n in neighbors.copy():
                neighbors.update(self.map.map.neighbors(n))
        neighbors.remove(pos)
        return list(neighbors)
    
    def find_neighboring_agents(self):
        neighbors_list = self.find_neighbors(2)
        agents = []
        # Only save those neighbors that have an Agent placed on them
        for neighbor in neighbors_list:
            if self.map.map.nodes.get(neighbor, {}).get("agent") is not None:  # Check if the node has an agent placed on it
                agents.append(self.map.map.nodes.get(neighbor, {}).get("agent"))
        self.neighboring_agents = agents

    def detect_opposite_conflict(self) -> bool: 
        if len(self.path) == 0:
            return False
        if self.is_agent_present_on_node_tag(self.path[0]):
            opposite_agent = self.get_agent_by_tag(self.path[0])
            if len(opposite_agent.path) == 0:
                return False
            else:
                if self.position == opposite_agent.path[0]:
                    return True
        return False

    def get_direction(self):
        if len(self.path) > 0:
            if self.path[0][0] - self.position[0] > 0 :
                self.direction = "R"
            elif self.path[0][0] - self.position[0] < 0:
                self.direction = "L"
            elif self.path[0][1] - self.position[1] > 0:
                self.direction = "U"
            elif self.path[0][1] - self.position[1] < 0:
                self.direction = "D"
            else:
                print("Error: No direction found (This should not happen)")

    def detect_intersection_conflict(self) -> bool:
        type_of_intersection = 0
        if len(self.path) >= 1:
            for neighbor in self.neighboring_agents:
                if len(neighbor.path) >= 1: 
                    if (self.path[0] == neighbor.path[0]):
                        type_of_intersection += 1
        if type_of_intersection >= 1:
            return True
        return False
        
    def is_agent_present_on_node_tag(self, node_tag):
        # Check if there is an agent on the given node tag
        if self.map.map.nodes.get(node_tag, {}).get("agent") is not None:
            return True
        else:
            return False

    def get_agent_by_tag(self, node_tag):
        # Returns the agent object by providing a tag
        return self.map.map.nodes.get(node_tag, {}).get("agent")

    def give_way(self):
        # Determines the action and updates path to a give way node
        self.get_follower()
        node_t2 = None
        neighbors = self.find_neighbors(1) # Find neighbors
        if self.detect_opposite_conflict(): # Check if give_way() was called because of an opposite conflict
            conflict_agent = self.get_agent_by_tag(self.path[0]) # Find the neighboring agent in opposite conflict
            neighbors.remove(conflict_agent.position) # Remove that agents position (since we cannot give way to that position)
            if len(conflict_agent.path) >= 2: # Check if the conflicting agent has a path longer than 1
                node_t2 = conflict_agent.path[1] # Remove its t2 node because if we give way to that in a tight corridoor, we will have another opposite conflict next turn
                if conflict_agent.position != node_t2:
                    neighbors.remove(node_t2)
        elif self.detect_intersection_conflict():
            neighbors.remove(self.path[0])
        
        if len(neighbors) == 0: # Ensure that we have any nodes to give way to
            self.action = "wait"
        
        while len(neighbors) != 0:
            possible_give_way_node = neighbors.pop(random.randint(0, len(neighbors)-1))
            if self.is_agent_present_on_node_tag(possible_give_way_node):
                neighboring_agent = self.get_agent_by_tag(possible_give_way_node)
                if len(neighboring_agent.path) >= 1:
                    if not (neighboring_agent.path[0] == self.position):
                        if neighboring_agent.number_requests_my_node() == 0:
                            self.action = "move"
                            self.update_give_way_path(possible_give_way_node)
                            return
            else:
                self.action = "move"
                self.update_give_way_path(possible_give_way_node)
                return

        # Check if node_t2 is free to move to (even though we removed it earlier) since this is last effort, we have to move to it
        if node_t2 is not None:
            if not self.is_agent_present_on_node_tag(node_t2):
                self.action = "move"
                self.update_give_way_path(node_t2)
                return
        
        # If not possible to give way, we need to wait :(
        self.action = "wait"

    def give_way_idle_robot(self):
        # Determines the action and updates path to a give way node

        node_t2 = [] # node at t + 2 time step
        neighbors = self.find_neighbors(1) # Find neighbors

        for neighbor in neighbors:
            if self.is_agent_present_on_node_tag(neighbor): 
                neighboring_agent = self.get_agent_by_tag(neighbor)
                if len(neighboring_agent.path) >= 2:
                    if neighboring_agent.path[0] == self.position: # Check if the beighboring agent next move is my position
                        node_t2.append(neighboring_agent.path[1])  # Add it's t+2 step to a list, this is so it will be taken as a give a way node but ONLY if no other is found
                                                                 
                        
        while len(neighbors) != 0: # Find the give_way_node
            possible_give_way_node = neighbors.pop(random.randint(0, len(neighbors)-1))
            if possible_give_way_node not in node_t2:
                if self.is_agent_present_on_node_tag(possible_give_way_node):
                    neighboring_agent = self.get_agent_by_tag(possible_give_way_node)
                    if len(neighboring_agent.path) >= 1:
                        if not (neighboring_agent.path[0] == self.position): # If the neighbor is moving away
                            if neighboring_agent.number_requests_my_node() == 0: # And no one is requesting it's node we move to it 
                                self.action = "move"
                                self.update_give_way_path(possible_give_way_node)
                                return
                else: # if no agent or t+2 node then we can move to it
                    self.action = "move"
                    self.update_give_way_path(possible_give_way_node)
                    return

        while len(node_t2) != 0: # Find a t+2 give_way_node
            possible_give_way_node = node_t2.pop(random.randint(0, len(node_t2)-1))
            if not self.is_agent_present_on_node_tag(possible_give_way_node): # if no agent is on it we can move
                self.action = "move"
                self.update_give_way_path(possible_give_way_node)
                return
        
        # If not possible to give way, we need to wait :(
        self.idle_blocked = True
        self.action = "wait" 

    def number_requests_my_node(self):
        neighbors = self.find_neighbors(1)
        num_requests = 0
        for neighbor in neighbors:
            if self.is_agent_present_on_node_tag(neighbor):
                neighboring_agent = self.get_agent_by_tag(neighbor)
                if len(neighboring_agent.path) > 0:
                    if neighboring_agent.path[0] == self.position:
                        num_requests += 1
        return num_requests
    
    def update_give_way_path(self, node):
        if node in self.path:
            pass
        else:
            self.path.insert(0, self.position)
            self.path.insert(0, node)
            
    def check_priority_rules(self, conflict_type):
        def find_agents_in_conflict():
            agents_in_conflict = []
            if conflict_type == "opposite":
                agents_in_conflict.append(self)
                agents_in_conflict.append(self.get_agent_by_tag(self.path[0]))
            elif conflict_type == "intersection":
                neighborhood = self.find_neighbors(1, position=self.path[0])
                for neighbor_tag in neighborhood:
                    if self.is_agent_present_on_node_tag(neighbor_tag):
                        neighbor = self.get_agent_by_tag(neighbor_tag)
                        if len(neighbor.path) >= 1:
                            if neighbor.path[0] == self.path[0]:
                                agents_in_conflict.append(neighbor)
            return agents_in_conflict

        def check_self(neighbor_list):
            """
            Check if the agent itself are in the list
            """
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
                    return (False, agents_with_priority)
                else:
                    if len(list_of_agents) == len(neighborhood):
                        return (None, list(neighborhood))
                    else:
                        return (None, list_of_agents)

        neighborhood = find_agents_in_conflict()

        list_of_agents = list(neighborhood)
        
        for rule in self.rule_list:
            agents_with_priority = rule(list_of_agents)
            result, list_of_agents = check_agents_with_priority(agents_with_priority, list_of_agents, neighborhood)
            if result is not None:
                return (result , list_of_agents)
        
        return (False, None)

    def rule_1(self, list_of_agents, critical_node = None):
        # rule1: a robot occupying a critical node is given priority.
        # NOTE: This rule does not make sense with the current implementation of give_way()
        return list_of_agents
        
    def rule_2(self, list_of_agents, _ = None):  # Maybe not correct
        # rule2: a robot moving out of another robot’s way is given priority.
        agents_with_priority = []
        if self.detect_opposite_conflict():
            for agent in list_of_agents:
                if agent.number_requests_my_node() > 1:  # Another robot other than the one in the opposite conflict is requesting our node
                    agents_with_priority.append(agent)
        elif self.detect_intersection_conflict():
            for agent in list_of_agents:
                if agent.number_requests_my_node() > 0:  # Another robot other than the one in the opposite conflict is requesting our node
                    agents_with_priority.append(agent)
        return agents_with_priority    

    def rule_3(self, list_of_agents, _ = None):  
        # rule3: the robot in conflict with another robot having a free adjacent node is given priority.
        # Alternative description: Robot-1 in conflict with another robot, and that other robot has a free adjacent node, then Robot-1 is given priority
        agents_with_priority = []

        for agent in list_of_agents:
            neighboring_nodes = agent.find_neighbors(1)
            for neighbor_node in neighboring_nodes:
                if (neighbor_node == self.path[0]):
                    if self.is_agent_present_on_node_tag(neighbor_node):
                        continue
                    else:
                        agents_with_priority.append(agent)
        return agents_with_priority
    
    def rule_4(self, list_of_agents, _ = None):
        # rule4: the robot with the largest numberFollowers is given priority.
        def number_followers(agent):
            agent.get_follower()
            if agent.follower is not None:
                return 1 + number_followers(agent.follower)
            else:
                return 0
        agents_with_priority = []
        max_followers = max(number_followers(agent) for agent in list_of_agents)
        agents_with_priority = [agent for agent in list_of_agents if number_followers(agent) == max_followers]
        return agents_with_priority
    
    def rule_5(self, list_of_agents, _ = None):
        # rule5: a robot having its node n_i(t+2) free is given priority.
        agents_with_priority = []
        for agent in list_of_agents:    # Loop through all agents
            if len(agent.path) >= 2:
                n_i_t2_node = agent.path[1]
                if not self.is_agent_present_on_node_tag(n_i_t2_node):
                    agents_with_priority.append(agent)
        return agents_with_priority
    
    def rule_6(self, list_of_agents, _ = None):
        # rule6: the robot having the largest numberRequestsMyNode is given priority.
        agents_with_priority = []
        max_request = max(agent.number_requests_my_node() for agent in list_of_agents)
        agents_with_priority = [agent for agent in list_of_agents if agent.number_requests_my_node == max_request]
        return agents_with_priority
        
    def rule_7(self, list_of_agents, _ = None):  
        # rule7: the robot with the longest remaining path is given priority.
        agents_with_priority=[]
        max_length = max(len(agent.path) for agent in list_of_agents)
        agents_with_priority = [agent for agent in list_of_agents if len(agent.path) == max_length]
        return agents_with_priority
    
    def a_star_heuristic(self, u, v):
        u_x = u[0]
        u_y = u[1]
        v_x = v[0]
        v_y = v[1]
        return (1/2) ** (((u_x - v_x)**2) + ((u_y - v_y)**2)) 
    
    def replan(self, obstacle_tags, intermediate_step = None):
        if nx.is_directed(self.map.map):
            edges_list = []

            for node_tag in obstacle_tags:
                edges = [e for e in self.map.map.in_edges(node_tag, data=True)]
                while len(edges) > 0:
                    u, v, data = edges.pop(0)
                    self.map.map.remove_edge(u,v)
                    edges_list.append([u ,v, data])

            
            try:
                if intermediate_step is not None:
                    path_a = nx.astar_path(self.map.map, self.position, intermediate_step, heuristic=self.a_star_heuristic)[1:]

                    for edge_with_data in edges_list:
                        self.map.map.add_edge(edge_with_data[0], edge_with_data[1], **edge_with_data[2]) # ** is from the documentation


                    path_b = nx.astar_path(self.map.map, intermediate_step, self.target, heuristic=self.a_star_heuristic)[1:]
                    new_path = path_a + path_b 
                else:
                    new_path = nx.astar_path(self.map.map, self.position, self.target, heuristic=self.a_star_heuristic)[1:]
            except:
                replaned = False
            else:
                self.path = new_path
                replaned = True
            finally:
                for edge_with_data in edges_list:
                    self.map.map.add_edge(edge_with_data[0], edge_with_data[1], **edge_with_data[2]) # ** is from the documentation

                return replaned                    

        else:
            edges_list = []

            for node_tag in obstacle_tags:
                edges = [e for e in self.map.map.edges(node_tag)]
                while len(edges) > 0:
                    edge = (edges.pop(0))
                    self.map.map.remove_edge(*edge)
                    edges_list.append(edge)

            try:
                if intermediate_step is not None:
                    path_a = nx.astar_path(self.map.map, self.position, intermediate_step, heuristic=self.a_star_heuristic)[1:]

                    for edge in edges_list:
                        if edge not in self.map.map.edges:
                            self.map.map.add_edge(*edge)
                

                    path_b = nx.astar_path(self.map.map, intermediate_step, self.target, heuristic=self.a_star_heuristic)[1:]
                    new_path = path_a + path_b 
                else:
                    new_path = nx.astar_path(self.map.map, self.position, self.target, heuristic=self.a_star_heuristic)[1:]
            except:
                replaned = False
            else:
                self.path = new_path
                replaned = True
            finally:
                for edge in edges_list:
                    if edge not in self.map.map.edges:
                        self.map.map.add_edge(*edge)
                return replaned
